# Tapestry Configuration & Environment Setup

| Repo      | Doc Type      | Date                | Branch |
|-----------|---------------|---------------------|--------|
| Tapestry  | Configuration | 2025-08-04 19:08    | main   |

This document describes the configuration files, environment management, and setup conventions for the Tapestry project, covering both frontend and backend. It is intended for developers seeking to understand or modify the build, runtime, and environment-specific behaviors of the system.

---

## Overview

Tapestry is a full-stack application with a Next.js/TypeScript/Tailwind frontend and a FastAPI/SQLAlchemy backend. Both layers require specific configuration for development and deployment, managed via config files and environment variables.

---

## Frontend Configuration

The frontend is located in the `frontend/` directory and is built with Next.js, TypeScript, and Tailwind CSS. Key configuration files include:

### TypeScript Configuration (`[frontend/tsconfig.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/tsconfig.json)`)

_Last modified: 2025-08-04 19:08_

Defines TypeScript compiler options, including module resolution, strictness, JSX handling, and path aliases.

```json
{
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "strict": true,
    "jsx": "preserve",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

**Key Points:**
- Uses modern ECMAScript and DOM libraries.
- Enforces strict type checking.
- Path alias `@/*` maps to `src/*` for cleaner imports.

### Next.js Configuration (`frontend/next.config.ts`)

_Last modified: 2025-08-04 19:08_

Controls Next.js build and runtime behavior. (File contents not shown, but typically includes custom webpack, env, and routing settings.)

### PostCSS Configuration (`frontend/postcss.config.mjs`)

_Last modified: 2025-08-04 19:08_

Configures PostCSS plugins, essential for Tailwind CSS and modern CSS features.

### Package Management (`[frontend/package.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/package.json)`)

_Last modified: 2025-08-04 19:08_

Defines scripts, dependencies, and devDependencies. Notable scripts:

```json
"scripts": {
  "dev": "next dev --turbopack",
  "build": "next build",
  "start": "next start",
  "lint": "next lint"
}
```

**Key Points:**
- Uses `next dev --turbopack` for fast development.
- Supports multiple package managers (npm, yarn, pnpm, bun).
- Tailwind, ESLint, and TypeScript are included as dev dependencies.

### Environment Variables

Frontend environment variables (if any) are typically set in `.env.local` (not shown in repo). These can be accessed in Next.js via `process.env.NEXT_PUBLIC_*`.

---

## Backend Configuration

The backend is in the `backend/` directory, using FastAPI and SQLAlchemy. Configuration is managed via Python files and environment variables.

### Python Project Configuration (`backend/pyproject.toml`)

_Last modified: 2025-08-04 19:08_

Specifies project metadata and dependencies:

```toml
[project]
name = "backend"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.116.1",
    "langgraph>=0.6.3",
    "pydantic[email]>=2.11.7",
    "python-dotenv>=1.1.1",
    "sqlalchemy>=2.0.42",
    "uvicorn>=0.35.0",
]
```

- Uses `python-dotenv` to load environment variables from `.env`.
- `uvicorn` is used as the ASGI server.

### Environment Variables (`backend/.env`)

_Described in [backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md) (Last modified: 2025-08-04 19:08)_

Example `.env` content:

```
DATABASE_URL=sqlite:///./data.db
SECRET_KEY=dev-secret-change
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

**Key Points:**
- `DATABASE_URL` controls the database connection (SQLite for development).
- `SECRET_KEY` is used for JWT or session security.
- `ACCESS_TOKEN_EXPIRE_MINUTES` sets token lifetime.

### Backend Startup

From `[backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md)`:

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- Loads environment from `.env`.
- Hot-reloads on code changes for development.

---

## Environment-Specific Setup

### Development

- **Frontend:** Run `npm run dev` (or `yarn dev`, `pnpm dev`, `bun dev`) in `frontend/`.
- **Backend:** Use `uv sync` to install dependencies, then run the server as above.

### Production

- **Frontend:** Build with `npm run build` and start with `npm start`.
- **Backend:** Run `uvicorn app.main:app --host 0.0.0.0 --port 8000` with production-ready settings and secrets.

---

## Configuration Flow (Mermaid Diagram)

```mermaid
flowchart TD
    A[Developer] -->|Edits| B[Config Files<br>(tsconfig.json, next.config.ts, postcss.config.mjs, pyproject.toml)]
    B --> C[Frontend Build/Dev Server]
    B --> D[Backend Uvicorn Server]
    E[.env File] --> D
    C --> F[Browser]
    D --> F
```

---

## Primary Sources

- [README.md](https://github.com/sergiomasellis/Tapestry/blob/main/README.md) (Last modified: 2025-08-04 19:08)
- [frontend/tsconfig.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/tsconfig.json) (Last modified: 2025-08-04 19:08)
- [frontend/package.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/package.json) (Last modified: 2025-08-04 19:08)
- [frontend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/README.md) (Last modified: 2025-08-04 19:08)
- backend/pyproject.toml (Last modified: 2025-08-04 19:08)
- [backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md) (Last modified: 2025-08-04 19:08)