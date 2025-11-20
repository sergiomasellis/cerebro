# Tapestry Configuration & Environment Management

| Repo    | Doc Type        | Date                | Branch |
|---------|----------------|---------------------|--------|
| Tapestry| Config & Envs   | 2025-08-04 19:08    | None   |

---

This document details the configuration files, environment variables, and environment setup processes for the Tapestry project. It covers both the frontend (Next.js) and backend (FastAPI + SQLAlchemy) stacks, including secrets management and local development environment instructions.

---

## Overview

Tapestry is a full-stack application with a TypeScript/Next.js frontend and a Python/FastAPI backend. Each component has its own configuration files and environment setup requirements. The backend uses SQLite for development and manages secrets via environment variables loaded from a `.env` file. The frontend uses TypeScript and Next.js configuration files, with environment-specific settings handled via standard Next.js conventions.

---

## Configuration Files

### Frontend

- **`frontend/tsconfig.json`**  
  *TypeScript compiler options*  
  - Controls module resolution, strictness, JSX, and path aliases.  
  - [Last modified: 2025-08-04 19:08]

- **`frontend/next.config.ts`**  
  *Next.js runtime configuration*  
  - Used for customizing Next.js build and runtime behavior.  
  - [Last modified: 2025-08-04 19:08]

- **`frontend/package.json`**  
  *Project metadata and scripts*  
  - Defines dependencies, scripts (`dev`, `build`, `start`, `lint`), and project info.  
  - [Last modified: 2025-08-04 19:08]

- **Other config files:**  
  - `postcss.config.mjs`, `eslint.config.mjs`, `pnpm-lock.yaml`, etc.

### Backend

- **`backend/pyproject.toml`**  
  *Python project and dependency management*  
  - Specifies dependencies (FastAPI, SQLAlchemy, LangGraph, python-dotenv, etc.) and Python version.  
  - [Last modified: 2025-08-04 19:08]

- **`backend/uv.lock`**  
  *Lockfile for reproducible Python environments*  
  - Ensures consistent dependency versions.

- **`backend/app/db/session.py`**  
  *Database engine/session configuration*  
  - Handles SQLAlchemy engine setup, using the `DATABASE_URL` from environment variables.

---

## Environment Variables

### Backend

Backend configuration is managed via a `.env` file in the `backend/` directory.  
**Example (`.env`):**
```
DATABASE_URL=sqlite:///./data.db
SECRET_KEY=dev-secret-change
ACCESS_TOKEN_EXPIRE_MINUTES=60
```
- **DATABASE_URL**: Connection string for SQLite (default: `sqlite:///./data.db`)
- **SECRET_KEY**: Secret used for JWT signing and other cryptographic operations.
- **ACCESS_TOKEN_EXPIRE_MINUTES**: Token expiration duration (in minutes).

**Loading:**  
- Environment variables are loaded using `python-dotenv` (see [backend/README.md, Last modified: 2025-08-04 19:08]).

### Frontend

- No `.env` file is present by default, but Next.js supports environment variables via `.env.local`, `.env.development`, etc.
- For API URLs or secrets, use `NEXT_PUBLIC_` prefix for variables to be exposed to the browser.

---

## Local Development Environment Setup

### Backend

1. **Create/activate virtual environment:**  
   ```sh
   python -m venv venv
   # Windows: venv\Scripts\activate
   # macOS/Linux: source venv/bin/activate
   ```
   Or, using `uv` (recommended):  
   ```sh
   uv sync
   ```

2. **Copy and edit environment file:**  
   ```sh
   cp .env.example .env
   # Edit .env as needed
   ```

3. **Install dependencies:**  
   ```sh
   pip install -r requirements.txt
   # or, with uv:
   uv sync
   ```

4. **Run the backend server:**  
   ```sh
   uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Database:**  
   - SQLite file (`data.db`) is created automatically on first run.

### Frontend

1. **Install dependencies:**  
   ```sh
   npm install
   # or
   pnpm install
   # or
   yarn install
   # or
   bun install
   ```

2. **Run development server:**  
   ```sh
   npm run dev
   # or
   pnpm dev
   # or
   yarn dev
   # or
   bun dev
   ```

3. **Configuration:**  
   - TypeScript and Next.js settings are managed via `tsconfig.json` and `next.config.ts`.
   - For custom environment variables, create `.env.local` as needed.

---

## Secrets Management

- **Backend:**  
  - Secrets (e.g., `SECRET_KEY`) are stored in `.env`, which should **not** be committed to version control.
  - Use `.env.example` to document required variables.

- **Frontend:**  
  - Only expose non-sensitive variables using the `NEXT_PUBLIC_` prefix.

---

## Configuration/Environment Diagram

```mermaid
flowchart TD
    subgraph Frontend
        F1[tsconfig.json]
        F2[next.config.ts]
        F3[package.json]
        F4[.env.local (optional)]
    end
    subgraph Backend
        B1[pyproject.toml]
        B2[uv.lock]
        B3[.env]
        B4[data.db (SQLite)]
        B5[app/db/session.py]
    end
    F4 -- API requests --> B3
    F1 --> F2
    F2 --> F3
    B3 -- env vars --> B5
    B1 --> B2
    B5 -- connects --> B4
```

---

## Best Practices

- **Never commit real `.env` files or secrets to version control.**
- Use `.env.example` to document required environment variables.
- For production, use secure secret management (e.g., Vercel/Netlify/Heroku env vars, Docker secrets, etc.).
- Keep configuration files under version control for reproducibility.

---

## Primary Sources

- [README.md](./README.md) (Last modified: 2025-08-04 19:08)
- [frontend/tsconfig.json](./frontend/tsconfig.json) (Last modified: 2025-08-04 19:08)
- [frontend/package.json](./frontend/package.json) (Last modified: 2025-08-04 19:08)
- [frontend/README.md](./frontend/README.md) (Last modified: 2025-08-04 19:08)
- [backend/pyproject.toml](./backend/pyproject.toml) (Last modified: 2025-08-04 19:08)
- [backend/README.md](./backend/README.md) (Last modified: 2025-08-04 19:08)