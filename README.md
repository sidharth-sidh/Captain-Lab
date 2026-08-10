# Lab Management System

Lab Management System is a local-first project for monitoring and managing a computer lab. It currently contains:

- A React/Vite dashboard with API-backed computer data and sample data for features not yet connected to the backend.
- A separate FastAPI backend for computer registration, heartbeats, and online/offline status tracking.

The Windows agent is not implemented yet. Shutdown, restart, software installation, deployments, authentication, and persistence from the dashboard are not connected to real machines yet.

## Repository layout

```text
dashboard/   React, TypeScript, Vite, and Tailwind frontend
server/      Python, FastAPI, SQLAlchemy, and SQLite backend
docs/        Project documentation
```

See [docs/FILES.md](docs/FILES.md) for the complete file inventory.

## Frontend setup

```bash
cd dashboard
npm install
npm run dev
```

The Vite development server normally runs at `http://localhost:5173`.

Frontend commands:

| Command | Purpose |
| --- | --- |
| `npm run dev` | Start the Vite development server |
| `npm run build` | Type-check and create a production build |
| `npm run preview` | Preview the production build |

## Backend setup

```bash
cd server
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

On Windows, activate the environment with `.venv\\Scripts\\activate`.

The backend runs at `http://localhost:8000`. FastAPI’s interactive documentation is available at [http://localhost:8000/docs](http://localhost:8000/docs).

## Backend API

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/api/health` | Check whether the API is running |
| `GET` | `/api/computers` | List registered computers |
| `GET` | `/api/computers/{computer_id}` | Get one computer |
| `POST` | `/api/computers/register` | Register a computer |
| `POST` | `/api/computers/{computer_id}/heartbeat` | Mark a computer online and update its heartbeat data |
| `DELETE` | `/api/computers/{computer_id}` | Delete a computer |

The SQLite database is created as `server/lab_management.db` when the API starts. A computer is marked offline when no heartbeat has been received for 20 seconds. The background monitor checks every five seconds, and computer reads also perform a stale-status check.

The API allows CORS requests from the Vite origins `http://localhost:5173` and `http://127.0.0.1:5173`.

The dashboard requests `GET http://localhost:8000/api/computers` on startup and polls it every five seconds. It shows loading, connection-error, and empty-database states. The Computers page and dashboard computer statistics use the returned API data.

## Example requests

Register a computer:

```bash
curl -X POST http://localhost:8000/api/computers/register \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "LAB-PC-01",
    "hostname": "LAB-PC-01",
    "ip_address": "192.168.10.21",
    "operating_system": "Windows",
    "os_version": "Windows 10",
    "username": "lab-user",
    "agent_version": "0.1.0"
  }'
```

Send a heartbeat:

```bash
curl -X POST http://localhost:8000/api/computers/1/heartbeat \
  -H 'Content-Type: application/json' \
  -d '{
    "ip_address": "192.168.10.21",
    "username": "lab-user",
    "agent_version": "0.1.0"
  }'
```

## Current status and limitations

- The Computers page and computer statistics are connected to the API; software, deployments, activity logs, and settings still use sample/local data.
- The backend has no authentication or authorization.
- No Windows 7/10 agent has been built.
- Restart and shutdown menu actions are currently frontend confirmations only.
- No software catalog, deployment service, logs API, or settings API is implemented.
- Automated backend tests are not included yet.

## Validation

The backend source compiles with Python’s bytecode compiler. Full API validation requires installing the packages in `server/requirements.txt`, starting Uvicorn, and exercising the endpoints through the running server.
