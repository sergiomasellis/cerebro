# Tapestry Configuration & Environments

| Repo     | Doc Type                | Date                | Branch |
|----------|------------------------|---------------------|--------|
| Tapestry | Config & Environments  | 2025-08-04 19:08    | main   |

---

This document details the configuration files, environment variables, and environment setup processes for the Tapestry project. It covers both the frontend (Next.js) and backend (FastAPI) stacks, referencing the latest file modifications and setup instructions.

---

## Overview

Tapestry is a full-stack family calendar and chore management application. It uses a modern React frontend (Next.js, TypeScript, Tailwind CSS) and a Python backend (FastAPI, SQLAlchemy, SQLite for development). Configuration is managed via JSON, TypeScript, TOML, and environment files.

---

## 1. Configuration Files

### Frontend (`/frontend`)

| File                       | Purpose                                                                 | Last Modified        |
|----------------------------|-------------------------------------------------------------------------|----------------------|
| `tsconfig.json`            | TypeScript compiler options and path aliases                             | 2025-08-04 19:08     |
| `next.config.ts`           | Next.js runtime and build configuration                                 | 2025-08-04 19:08     |
| `postcss.config.mjs`       | PostCSS plugin configuration (for Tailwind CSS, etc.)                   | 2025-08-04 19:08     |
| `package.json`             | NPM scripts, dependencies, and project metadata                         | 2025-08-04 19:08     |
| `pnpm-lock.yaml`           | Dependency lockfile (if using pnpm)                                     | 2025-08-04 19:08     |
| `eslint.config.mjs`        | ESLint rules for code quality                                           | 2025-08-04 19:08     |

#### Example: `tsconfig.json` (2025-08-04 19:08)
- Sets strict TypeScript rules, enables JSX, and configures path aliases (`@/*` → `./src/*`).
- Integrates with Next.js via plugin.

#### Example: `next.config.ts` (2025-08-04 19:08)
- Controls Next.js build and runtime options (custom routing, environment variables, etc.).

#### Example: `postcss.config.mjs` (2025-08-04 19:08)
- Loads Tailwind CSS and other PostCSS plugins.

#### Example: `package.json` (2025-08-04 19:08)
- Defines scripts: `dev`, `build`, `start`, `lint`.
- Lists all runtime and development dependencies.

---

### Backend (`/backend`)

| File                | Purpose                                                 | Last Modified        |
|---------------------|--------------------------------------------------------|----------------------|
| `pyproject.toml`    | Python project metadata and dependencies                | 2025-08-04 19:08     |
| `.env.example`      | Example environment variable file (not committed)       | (see README)         |
| `.env`              | Actual environment variables (local, not committed)     | (user-generated)     |
| `uv.lock`           | Python dependency lockfile (for `uv`/venv)              | 2025-08-04 19:08     |

#### Example: `pyproject.toml` (2025-08-04 19:08)
- Declares dependencies: FastAPI, SQLAlchemy, LangGraph, python-dotenv, etc.
- Supports dev dependencies (e.g., `ruff` for linting).

#### Environment Variables (`.env`)
As per `[backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md)` (2025-08-04 19:08):

```env
DATABASE_URL=sqlite:///./data.db
SECRET_KEY=dev-secret-change
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

- `DATABASE_URL`: Database connection string (SQLite for development).
- `SECRET_KEY`: Used for JWT or session signing.
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiry for authentication.

---

## 2. Environment Setup

### Backend

From `[backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md)` (2025-08-04 19:08):

1. **Install dependencies**:  
   ```sh
   uv sync
   ```
2. **Create environment file**:  
   ```sh
   cp .env.example .env
   # Edit .env as needed
   ```
3. **Run development server**:  
   ```sh
   uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
4. **Access API docs**:  
   - http://localhost:8000/docs

**Note:** The SQLite database (`data.db`) is created automatically on first run.

### Frontend

From `[frontend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/README.md)` (2025-08-04 19:08):

1. **Install dependencies**:  
   ```sh
   npm install
   # or: yarn install / pnpm install / bun install
   ```
2. **Run development server**:  
   ```sh
   npm run dev
   ```
3. **Access app**:  
   - http://localhost:3000

---

## 3. Environment Variables & Secrets Management

- **Backend**: Uses `.env` (not committed) for secrets and DB config. Loaded via `python-dotenv`.
- **Frontend**: Next.js supports environment variables via `.env.local`, `.env.development`, etc. (not shown in repo, but supported by Next.js).

**Best Practices:**
- Never commit `.env` files with secrets to version control.
- Use `.env.example` to document required variables.
- For production, set environment variables via deployment platform (e.g., Vercel, Docker, etc.).

---

## 4. Configuration Flow (Mermaid Diagram)

```mermaid
flowchart TD
    subgraph Frontend
        A1[tsconfig.json]
        A2[next.config.ts]
        A3[postcss.config.mjs]
        A4[package.json]
    end
    subgraph Backend
        B1[pyproject.toml]
        B2[.env]
        B3[uv.lock]
    end
    subgraph DevOps
        C1[.env.example]
        C2[[README.md](https://github.com/sergiomasellis/Tapestry/blob/main/README.md) Setup Steps]
    end

    A1 --> A2
    A2 --> A3
    A3 --> A4
    B1 --> B2
    B2 --> B3
    C1 --> B2
    C2 --> A4
    C2 --> B1
```

---

## 5. Summary Table

| Layer     | Config Files                        | Env Vars Location | Secrets Handling         |
|-----------|-------------------------------------|-------------------|-------------------------|
| Frontend  | tsconfig.json, next.config.ts, etc. | .env.local*       | Not shown, but supported|
| Backend   | pyproject.toml, .env                | .env              | .env (not committed)    |

---

## Primary Sources

- [`[README.md](https://github.com/sergiomasellis/Tapestry/blob/main/README.md)`](./[README.md](https://github.com/sergiomasellis/Tapestry/blob/main/README.md)) (Last modified: 2025-08-04 19:08)
- [`[frontend/tsconfig.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/tsconfig.json)`](./[frontend/tsconfig.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/tsconfig.json)) (Last modified: 2025-08-04 19:08)
- [`[frontend/package.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/package.json)`](./[frontend/package.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/package.json)) (Last modified: 2025-08-04 19:08)
- [`[frontend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/README.md)`](./[frontend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/README.md)) (Last modified: 2025-08-04 19:08)
- [`backend/pyproject.toml`](./backend/pyproject.toml) (Last modified: 2025-08-04 19:08)
- [`[backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md)`](./[backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md)) (Last modified: 2025-08-04 19:08)