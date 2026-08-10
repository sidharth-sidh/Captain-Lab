import configparser
import os
from pathlib import Path


DEFAULT_CONFIG_PATH = Path(__file__).resolve().parents[1] / "config" / "agent.ini"


class AgentConfig:
    def __init__(self, server_url, heartbeat_interval, agent_version):
        self.server_url = server_url.rstrip("/")
        self.heartbeat_interval = max(1.0, heartbeat_interval)
        self.agent_version = agent_version


def load_config(config_path=None):
    path = Path(config_path) if config_path else DEFAULT_CONFIG_PATH
    parser = configparser.ConfigParser()
    parser.read(str(path), encoding="utf-8")
    section = parser["agent"] if parser.has_section("agent") else {}

    server_url = os.environ.get("SERVER_URL", section.get("server_url", "http://127.0.0.1:8000"))
    interval_value = os.environ.get("HEARTBEAT_INTERVAL", section.get("heartbeat_interval", "5"))
    agent_version = os.environ.get("AGENT_VERSION", section.get("agent_version", "1.0.0"))
    try:
        heartbeat_interval = float(interval_value)
    except (TypeError, ValueError):
        heartbeat_interval = 5.0

    return AgentConfig(server_url, heartbeat_interval, agent_version)
