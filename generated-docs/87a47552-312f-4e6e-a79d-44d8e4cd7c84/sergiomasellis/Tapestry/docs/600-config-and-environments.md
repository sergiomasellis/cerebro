# Tapestry Configuration & Environments

| Repo    | Doc Type                | Date                | Branch |
|---------|-------------------------|---------------------|--------|
| Tapestry| Config & environments   | 2025-08-04 19:08    | main   |

---

This document details the configuration files, environment variables, and setup steps for both the frontend and backend of the Tapestry application. It is intended for developers and operators who need to understand, modify, or troubleshoot the system's configuration and deployment environments.

---

## Overview

Tapestry is a modern, multi-user family calendar and chore-tracking application. It is structured as a monorepo with two main components:

- **frontend/**: Next.js (TypeScript, Tailwind CSS)
- **backend/**: FastAPI (Python), SQLAlchemy, SQLite

Both components have their own configuration files and environment requirements.

---

## Frontend Configuration

### Key Files

- **[frontend/tsconfig.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/tsconfig.json)** (Last modified: 2025-08-04 19:08)  
  TypeScript compiler configuration.  
  - Sets strict type checking, module resolution, JSX handling, and path aliases (`@/*` → `src/*`).
  - Includes Next.js plugin for type support.

- **[frontend/package.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/package.json)** (Last modified: 2025-08-04 19:08)  
  Node.js project manifest.  
  - Defines scripts (`dev`, `build`, `start`, `lint`).
  - Lists dependencies (Next.js, React, Tailwind, Radix UI, etc.).
  - Dev dependencies include ESLint, Tailwind, TypeScript.

- **frontend/next.config.ts** (Last modified: 2025-08-04 19:08)  
  Next.js runtime configuration.  
  - Used to customize build, routing, and environment variables for the app.

- **frontend/postcss.config.mjs** (Last modified: 2025-08-04 19:08)  
  PostCSS configuration for CSS processing (used by Tailwind).

- **frontend/eslint.config.mjs** (Last modified: 2025-08-04 19:08)  
  ESLint configuration for code linting.

#### Environment Variables

- Next.js supports environment variables via `.env.local`, `.env.development`, etc.
- No `.env` files are present in the repo by default; create as needed for API URLs or secrets.

#### Setup Steps

1. Enter the frontend directory:
   ```
   cd frontend
   ```
2. Install dependencies:
   ```
   npm install
   ```
3. Run the development server:
   ```
   npm run dev
   ```
   - The app will be available at `http://localhost:3000`.

#### Build & Lint

- Build: `npm run build`
- Lint: `npm run lint`

---

## Backend Configuration

### Key Files

- **backend/pyproject.toml** (Last modified: 2025-08-04 19:08)  
  Python project metadata and dependencies.  
  - Main dependencies: FastAPI, SQLAlchemy, Pydantic, LangGraph, python-dotenv, uvicorn.
  - Dev dependencies: ruff (linter).

- **backend/uv.lock**  
  Lockfile for `uv` (Python project/env manager).

- **[backend/app/db/session.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/db/session.py)**  
  SQLAlchemy engine/session configuration.

- **backend/.env.example** (not present, but referenced)  
  Template for environment variables.  
  - Copy to `.env` and edit as needed.

#### Environment Variables

From **[backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md)** (Last modified: 2025-08-04 19:08):

- `.env` file in `backend/` directory, with at least:
  ```
  DATABASE_URL=sqlite:///./data.db
  SECRET_KEY=dev-secret-change
  ACCESS_TOKEN_EXPIRE_MINUTES=60
  ```
- Loaded automatically by `python-dotenv`.

#### Setup Steps

1. Enter the backend directory:
   ```
   cd backend
   ```
2. Sync and install dependencies (using uv):
   ```
   uv sync
   ```
3. Create a `.env` file:
   ```
   cp .env.example .env
   # Edit values as needed
   ```
4. Run the development server:
   ```
   uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   - API docs at `http://localhost:8000/docs`

#### Database

- Uses SQLite for development (`data.db` in backend root).
- Auto-creates tables on first run.

---

## Secrets Management

- **Frontend**:  
  - Use `.env.local` for secrets (not committed).
  - Never commit API keys or secrets to the repo.

- **Backend**:  
  - Use `.env` for secrets (not committed).
  - Example secrets: `SECRET_KEY`, database credentials, token expiry.

---

## Configuration File Topology

```mermaid
graph TD
  A[[frontend/tsconfig.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/tsconfig.json)] --> B[TypeScript settings]
  A1[[frontend/package.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/package.json)] --> C[Node scripts & deps]
  A2[frontend/next.config.ts] --> D[Next.js runtime config]
  A3[frontend/postcss.config.mjs] --> E[PostCSS/Tailwind]
  A4[frontend/eslint.config.mjs] --> F[ESLint rules]
  G[backend/pyproject.toml] --> H[Python deps]
  I[backend/.env] --> J[Secrets & DB URL]
  K[[backend/app/db/session.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/db/session.py)] --> L[DB engine/session]
```

---

## Environment Summary Table

| Component | Config Files                        | Env Vars File      | Secrets Managed | Notes                         |
|-----------|-------------------------------------|--------------------|----------------|-------------------------------|
| Frontend  | tsconfig.json, package.json,        | .env.local         | Yes            | Next.js, TypeScript, Tailwind |
|           | next.config.ts, postcss.config.mjs, |                    |                |                               |
|           | eslint.config.mjs                   |                    |                |                               |
| Backend   | pyproject.toml, uv.lock,            | .env               | Yes            | FastAPI, SQLAlchemy, SQLite   |
|           | app/db/session.py                   |                    |                |                               |

---

## Best Practices

- **Never commit `.env` or `.env.local` files containing secrets.**
- Use `.env.example` as a template for required environment variables.
- For production, use secure secret management (e.g., cloud secrets manager, CI/CD secrets).
- Keep configuration files under version control, but not files containing secrets.

---

## Primary Sources

- [frontend/tsconfig.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/tsconfig.json) (Last modified: 2025-08-04 19:08)
- [frontend/package.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/package.json) (Last modified: 2025-08-04 19:08)
- frontend/next.config.ts (Last modified: 2025-08-04 19:08)
- frontend/postcss.config.mjs (Last modified: 2025-08-04 19:08)
- frontend/eslint.config.mjs (Last modified: 2025-08-04 19:08)
- backend/pyproject.toml (Last modified: 2025-08-04 19:08)
- [backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md) (Last modified: 2025-08-04 19:08)
- [README.md](https://github.com/sergiomasellis/Tapestry/blob/main/README.md) (Last modified: 2025-08-04 19:08)