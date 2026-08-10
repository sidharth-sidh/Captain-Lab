import getpass
import platform
import socket
from urllib.parse import urlparse


def get_hostname():
    return socket.gethostname()


def get_local_ip(server_url):
    """Find the LAN address used to reach the configured server."""
    parsed = urlparse(server_url)
    server_host = parsed.hostname or "127.0.0.1"
    probe = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        probe.connect((server_host, parsed.port or 80))
        return probe.getsockname()[0]
    except OSError:
        try:
            return socket.gethostbyname(get_hostname())
        except socket.error:
            return "127.0.0.1"
    finally:
        probe.close()


def get_operating_system():
    system_name = platform.system() or "Windows"
    release = platform.release()
    version = platform.version()
    os_version = "{} {}".format(release, version).strip()
    return system_name, os_version[:100]


def get_username():
    try:
        return getpass.getuser()
    except (KeyError, OSError):
        return "unknown"


def collect_registration_info(server_url, agent_version):
    hostname = get_hostname()
    operating_system, os_version = get_operating_system()
    return {
        "name": hostname,
        "hostname": hostname,
        "ip_address": get_local_ip(server_url),
        "operating_system": operating_system,
        "os_version": os_version,
        "username": get_username(),
        "agent_version": agent_version,
    }


def collect_heartbeat_info(server_url, agent_version):
    return {
        "ip_address": get_local_ip(server_url),
        "username": get_username(),
        "agent_version": agent_version,
    }
