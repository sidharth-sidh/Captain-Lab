# Lab Management System Windows Agent

This is the first manual-run version of the Lab Management System agent. It registers a Windows PC with the FastAPI server and sends a heartbeat every five seconds. It does not execute remote commands.

## Supported scope

- Computer name and hostname detection
- Local IP detection
- Windows OS/version detection
- Logged-in username detection
- Registration with `POST /api/computers/register`
- Heartbeats with `POST /api/computers/{computer_id}/heartbeat`
- Automatic retries when the server is unavailable
- Duplicate-registration recovery after an agent restart
- Rotating log file at `agent/logs/agent.log`

Shutdown, restart, software installation, file transfer, remote command execution, and Windows Service installation are intentionally not included.

## Configuration

Copy `agent/config/agent.example.ini` to `agent/config/agent.ini`, then edit the local file:

```ini
[agent]
server_url = http://192.168.1.100:8000
heartbeat_interval = 5
agent_version = 1.0.0
```

The server URL can also be overridden with environment variables:

```bat
set SERVER_URL=http://192.168.1.100:8000
set HEARTBEAT_INTERVAL=5
set AGENT_VERSION=1.0.0
```

## Run manually on Windows

Install Python 3 on the Windows PC, copy the `agent` directory to the PC, configure the server URL, and run from the repository root:

```bat
cd agent
python -m app.main
```

You can provide another configuration file as the first argument:

```bat
python -m app.main C:\LabPilot\agent.ini
```

The agent uses no third-party packages, so `pip install` is not required. `requirements.txt` is included for consistency and documents that fact.

## Testing workflow

1. Start the backend on the admin machine:

   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. Set `server_url` to the admin machine’s LAN IP.
3. Run `python -m app.main` on the Windows PC.
4. Check the agent console or `agent/logs/agent.log` for registration and heartbeat messages.
5. Open the dashboard and confirm the computer is online.
6. Stop the agent and wait at least 20 seconds. The backend’s existing stale-heartbeat monitor should mark it offline.

## Windows 7 compatibility

The implementation uses the Python standard library only and avoids newer third-party dependencies. Use a Python 3 version that is supported by the specific Windows 7 installation and ensure the machine can make HTTP connections to the admin server. Windows 7 itself is end-of-life, so TLS, firewall, antivirus, and Python installer support may vary by machine.
