# Lab Management System Backend

FastAPI backend for registering and monitoring Windows lab computers. The API is intentionally limited to computer inventory and heartbeat tracking; Windows agents and machine-control commands are not included yet.

## Setup

```bash
cd server
python3 -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The SQLite database is created at `server/lab_management.db` on first startup. Interactive API documentation is available at http://localhost:8000/docs.

## Endpoints

- `GET /api/health` — health check
- `GET /api/computers` — list registered computers
- `GET /api/computers/{computer_id}` — retrieve one computer
- `POST /api/computers/register` — register a computer
- `POST /api/computers/{computer_id}/heartbeat` — mark a computer online and update heartbeat fields
- `DELETE /api/computers/{computer_id}` — delete a computer

Computers are marked offline when their last heartbeat is more than 20 seconds old. A background monitor checks every five seconds, and computer reads also perform a stale check.
