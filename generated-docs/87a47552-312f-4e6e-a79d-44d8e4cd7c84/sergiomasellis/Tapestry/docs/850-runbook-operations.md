# Tapestry Runbook Operations

| Repo     | Doc Type        | Date                | Branch |
|----------|----------------|---------------------|--------|
| Tapestry | Runbook (850)  | 2025-08-04 19:08    | main   |

---

## Overview

This runbook provides operational guidance for running, monitoring, and troubleshooting the Tapestry application. Tapestry is a modern, multi-user family calendar and chore management system, composed of a Next.js frontend and a FastAPI backend with SQLite for development. This document covers the standard operational lifecycle, including startup, shutdown, and basic debugging, based on the current repository structure and documentation.

> **Note:** As of the latest update, there is no explicit evidence of custom health checks, automated recovery scripts, or advanced observability tooling in the repository. This runbook focuses on manual procedures and standard development workflows.

---

## 1. System Startup

### Backend

**Requirements:** Python 3.12+, `uv` (Python project/env manager), SQLite (bundled).

**Steps:**
1. **Install dependencies**  
   From `backend/`:
   ```
   uv sync
   ```
2. **Configure environment**  
   Copy and edit the environment file:
   ```
   cp .env.example .env
   # Edit .env as needed (DATABASE_URL, SECRET_KEY, etc.)
   ```
3. **Run the backend server**  
   ```
   uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   - The backend will auto-create the SQLite database (`backend/data.db`) and tables on first run.
   - API docs available at: `http://localhost:8000/docs`

### Frontend

**Requirements:** Node.js (v18+ recommended), npm/pnpm/yarn.

**Steps:**
1. **Install dependencies**  
   From `frontend/`:
   ```
   npm install
   ```
2. **Run the development server**  
   ```
   npm run dev
   ```
   - Access the frontend at: `http://localhost:3000`

---

## 2. System Shutdown

- **Backend:**  
  Stop the uvicorn process with `Ctrl+C` in the terminal.
- **Frontend:**  
  Stop the Next.js dev server with `Ctrl+C` in the terminal.

---

## 3. Failure Modes & Debugging

### Common Failure Scenarios

| Symptom                        | Likely Cause                | Resolution Steps                                   |
|---------------------------------|-----------------------------|----------------------------------------------------|
| Backend won't start             | Missing dependencies/env    | Run `uv sync`; check `.env` file                   |
| Backend port in use             | Port 8000 occupied          | Kill process or change port in `uvicorn` command   |
| Frontend won't start            | Missing deps/build errors   | Run `npm install`; check Node version              |
| 500 errors from API             | DB missing/migrated         | Ensure `backend/data.db` exists; restart backend   |
| CORS errors in frontend         | Backend misconfigured       | Check FastAPI CORS settings in `app/main.py`       |
| Data not persisting             | SQLite file not created     | Check write permissions in `backend/`              |

### Debugging Steps

- **Backend logs:**  
  Observe terminal output for Python exceptions or FastAPI errors.
- **Frontend logs:**  
  Check browser console and terminal output for build/runtime errors.
- **Database:**  
  Inspect `backend/data.db` using SQLite tools if data issues arise.

---

## 4. Restart Procedures

- **Backend:**  
  Stop and restart the uvicorn process as above.  
  If using Docker or a process manager (not present in repo), restart the container/service.
- **Frontend:**  
  Stop and restart the Next.js dev server.

---

## 5. Environment Variables

Defined in `backend/.env` (see [backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md), Last modified: 2025-08-04 19:08):

- `DATABASE_URL=sqlite:///./data.db`
- `SECRET_KEY=dev-secret-change`
- `ACCESS_TOKEN_EXPIRE_MINUTES=60`

Ensure these are set before starting the backend.

---

## 6. Data Persistence & Backups

- **Development:**  
  Data is stored in `backend/data.db` (SQLite).  
  To back up, copy this file to a safe location.
- **Restoration:**  
  Replace `data.db` with a backup copy and restart the backend.

---

## 7. Health & Observability

- **API Health:**  
  No explicit health check endpoint; verify by accessing `/docs` or hitting a simple API route (e.g., `/users`).
- **Logs:**  
  All logs are output to the terminal by default.

---

## 8. Recovery & Disaster Scenarios

- **Database corruption:**  
  Restore `data.db` from backup.
- **Lost environment file:**  
  Recreate from `.env.example` and update values.
- **Dependency issues:**  
  Re-run `uv sync` (backend) or `npm install` (frontend).

---

## 9. Upgrade & Maintenance

- **Backend:**  
  Update dependencies in `pyproject.toml`, then run `uv sync`.
- **Frontend:**  
  Update dependencies in `package.json`, then run `npm install`.

---

## 10. System Topology (Mermaid Diagram)

```mermaid
flowchart TD
    subgraph Frontend (Next.js)
        FE[User Browser]
        APP[frontend/app/]
    end
    subgraph Backend (FastAPI)
        API[app/main.py]
        DB[(SQLite data.db)]
    end
    FE -->|HTTP (3000)| APP
    APP -->|REST API (8000)| API
    API -->|ORM| DB
```

---

## Primary Sources

- [README.md](https://github.com/sergiomasellis/Tapestry/blob/main/README.md) (Last modified: 2025-08-04 19:08)
- [backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md) (Last modified: 2025-08-04 19:08)
- [frontend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/README.md) (Last modified: 2025-08-04 19:08)
- backend/pyproject.toml (Last modified: 2025-08-04 19:08)
- [frontend/package.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/package.json) (Last modified: 2025-08-04 19:08)
- [frontend/tsconfig.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/tsconfig.json) (Last modified: 2025-08-04 19:08)