import sys
import time

from .api_client import ApiClient, ApiError
from .config import load_config
from .logger import create_logger
from .system_info import collect_heartbeat_info, collect_registration_info


def find_existing_computer(client, hostname):
    for computer in client.list_computers() or []:
        if computer.get("hostname") == hostname or computer.get("name") == hostname:
            return computer
    return None


def register_or_reuse(client, registration_info, logger):
    try:
        computer = client.register(registration_info)
        logger.info("Registered computer %s with id %s", registration_info["hostname"], computer["id"])
        return computer["id"]
    except ApiError as error:
        if error.status_code != 409:
            raise
        logger.info("Computer already registered; looking up existing record")
        existing = find_existing_computer(client, registration_info["hostname"])
        if existing is None:
            raise ApiError("Registration conflict and existing computer was not found")
        logger.info("Reusing computer id %s", existing["id"])
        return existing["id"]


def run(config_path=None):
    config = load_config(config_path)
    logger = create_logger()
    client = ApiClient(config.server_url)
    registration_info = collect_registration_info(config.server_url, config.agent_version)
    computer_id = None

    logger.info("Starting Lab Management Agent %s for %s", config.agent_version, registration_info["hostname"])
    logger.info("Configured server: %s; heartbeat interval: %s seconds", config.server_url, config.heartbeat_interval)

    while True:
        try:
            if computer_id is None:
                computer_id = register_or_reuse(client, registration_info, logger)

            heartbeat_info = collect_heartbeat_info(config.server_url, config.agent_version)
            client.heartbeat(computer_id, heartbeat_info)
            logger.info("Heartbeat sent for computer id %s", computer_id)
        except ApiError as error:
            logger.warning("Backend unavailable or request failed: %s", error)
            if error.status_code == 404:
                computer_id = None
        except Exception:
            logger.exception("Unexpected agent error; will retry")

        try:
            time.sleep(config.heartbeat_interval)
        except KeyboardInterrupt:
            logger.info("Agent stopped by user")
            return


if __name__ == "__main__":
    config_file = sys.argv[1] if len(sys.argv) > 1 else None
    run(config_file)
