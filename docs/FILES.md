# Repository File Documentation

This document explains the current Lab Management System repository. The project is split into an independent frontend and backend so the dashboard can continue to evolve while the machine-management API is developed separately.

## Directory structure

```text
.
├── README.md
├── docs/
│   └── FILES.md
├── dashboard/
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   ├── src/
│   │   ├── App.tsx
│   │   ├── index.css
│   │   ├── main.tsx
│   │   └── vite-env.d.ts
│   ├── tsconfig.app.json
│   ├── tsconfig.json
│   ├── tsconfig.node.json
│   └── vite.config.ts
├── agent/
│   ├── README.md
│   ├── requirements.txt
│   ├── app/
│   │   ├── __init__.py
│   │   ├── api_client.py
│   │   ├── config.py
│   │   ├── logger.py
│   │   ├── main.py
│   │   └── system_info.py
│   └── config/
│       └── agent.example.ini
└── server/
    ├── README.md
    ├── requirements.txt
    └── app/
        ├── __init__.py
        ├── database.py
        ├── main.py
        ├── models.py
        ├── schemas.py
        └── routers/
            ├── __init__.py
            └── computers.py
```

Generated local files such as `dashboard/node_modules/`, `dashboard/dist/`, `server/.venv/`, `server/lab_management.db`, and Python `__pycache__/` directories are not source files and should not be committed.

## Root files

### `README.md`

The main project guide. It covers the frontend and backend setup, API endpoints, example requests, current architecture, and known limitations.

### `docs/FILES.md`

This file. It is the detailed file inventory and responsibility guide for the repository.

## Dashboard files

### `dashboard/package.json`

Defines the frontend package metadata, React/Vite/Tailwind dependencies, React type packages, and scripts:

- `npm run dev` starts Vite.
- `npm run build` runs TypeScript project checks and creates a production build.
- `npm run preview` serves the production build locally.

### `dashboard/package-lock.json`

Locks the exact npm dependency tree for repeatable frontend installation.

### `dashboard/index.html`

The browser entry document. It defines the viewport, page title, theme color, React mount element (`#root`), and `src/main.tsx` module entry.

### `dashboard/vite.config.ts`

Configures Vite with the React plugin and Tailwind CSS Vite plugin.

### `dashboard/src/main.tsx`

Bootstraps React by importing `App` and the global stylesheet, then rendering the app into `#root` inside `StrictMode`.

### `dashboard/src/App.tsx`

Contains the dashboard UI and its local state. It includes:

- Sidebar navigation for Dashboard, Computers, Software, Deployments, Logs, and Settings.
- API-backed computer data plus sample software, deployment, and activity data.
- Computer filtering and search.
- The three-dot computer action menu with frontend-only Restart and Shut down confirmations.
- Reusable icons, badges, status labels, headers, cards, and page components.

The dashboard fetches `GET http://localhost:8000/api/computers` on startup and polls it every five seconds. It passes the API data to the Computers page and calculates total, online, and offline computer statistics for the Dashboard page. It displays loading, connection-error, and empty-database states without falling back to mock computers.

### `dashboard/src/index.css`

Loads Google Fonts and Tailwind CSS, defines the Tailwind theme font, and contains global layout, typography, and scrollbar styles.

### `dashboard/src/vite-env.d.ts`

Loads Vite’s client-side TypeScript declarations, including support for CSS imports in `main.tsx`.

### `dashboard/tsconfig.json`

Root TypeScript project-reference configuration for the application and Vite configuration projects.

### `dashboard/tsconfig.app.json`

Strict TypeScript configuration for React source files under `src`, including JSX and browser libraries.

### `dashboard/tsconfig.node.json`

TypeScript configuration for the Node-side Vite configuration file.

## Backend files

### `server/requirements.txt`

Lists the Python dependencies required by the backend: FastAPI, Uvicorn, SQLAlchemy, and Pydantic.

### `server/README.md`

Backend-specific setup instructions, run command, API endpoint summary, SQLite behavior, and heartbeat timeout behavior.

### `server/app/__init__.py`

Marks `app` as a Python package.

### `server/app/main.py`

Creates the FastAPI application, configures CORS for the Vite development origins, registers routers, creates database tables at startup, exposes `/api/health`, and runs the five-second offline monitor.

### `server/app/database.py`

Configures the SQLite engine and SQLAlchemy session factory. The database file is located at `server/lab_management.db`. It also provides the request-scoped `get_db` dependency.

### `server/app/models.py`

Defines the SQLAlchemy `Computer` model and the `computers` table fields:

- Identity: `id`, `name`, `hostname`
- Network and platform: `ip_address`, `operating_system`, `os_version`
- Monitoring: `status`, `username`, `last_seen`, `agent_version`
- Audit timestamps: `created_at`, `updated_at`

### `server/app/schemas.py`

Defines Pydantic request and response models for computer registration, heartbeats, and API output. Status values are constrained to `online` and `offline`.

### `server/app/routers/__init__.py`

Marks the routers directory as a Python package.

### `server/app/routers/computers.py`

Implements computer inventory endpoints, registration, heartbeat updates, deletion, not-found/conflict responses, and the stale-heartbeat function that marks computers offline after 20 seconds.

## Agent files

### `agent/README.md`

Explains the Windows agent scope, configuration, manual execution, testing workflow, and Windows 7 compatibility considerations.

### `agent/requirements.txt`

Documents that the agent has no third-party dependencies and uses only Python’s standard library.

### `agent/app/main.py`

Runs the registration and heartbeat loop, retries failed requests, and reuses an existing computer record after a duplicate-registration response.

### `agent/app/config.py`

Loads the agent INI configuration and supports `SERVER_URL`, `HEARTBEAT_INTERVAL`, and `AGENT_VERSION` environment-variable overrides.

### `agent/app/system_info.py`

Collects hostname, local IP address, operating system/version, and logged-in username for registration and heartbeat payloads.

### `agent/app/api_client.py`

Provides the standard-library HTTP client for the existing backend registration, list, and heartbeat endpoints.

### `agent/app/logger.py`

Creates console and rotating file logging for the agent.

### `agent/config/agent.example.ini`

Safe configuration template for the server URL, heartbeat interval, and agent version. The local `agent/config/agent.ini` file is intentionally ignored by Git.

## API route map

| Method | Route | Implemented in | Responsibility |
| --- | --- | --- | --- |
| `GET` | `/api/health` | `main.py` | API health check |
| `GET` | `/api/computers` | `computers.py` | List computers |
| `GET` | `/api/computers/{computer_id}` | `computers.py` | Get one computer |
| `POST` | `/api/computers/register` | `computers.py` | Register a computer |
| `POST` | `/api/computers/{computer_id}/heartbeat` | `computers.py` | Mark online and update heartbeat fields |
| `DELETE` | `/api/computers/{computer_id}` | `computers.py` | Delete a computer |

FastAPI automatically exposes the OpenAPI schema and Swagger UI at `/docs`.

## Development boundaries

The backend currently owns only computer registration and monitoring. The following are intentionally outside the current implementation:

- Remote Windows commands beyond registration and heartbeat monitoring
- Real restart or shutdown commands
- Software installation and deployment jobs
- Authentication and authorization
- Dashboard-to-API integration
- Automated API tests
