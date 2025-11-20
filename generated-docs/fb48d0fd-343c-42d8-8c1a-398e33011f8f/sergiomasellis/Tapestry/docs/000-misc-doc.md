# Tapestry Repository Table of Contents

| Repo      | Doc Type           | Date                | Branch |
|-----------|--------------------|---------------------|--------|
| Tapestry  | Table of Contents  | 2025-08-04 19:08    | main   |

---

## Overview

Tapestry is a modern, touch-friendly multi-user calendar application designed for families. It features a weekly calendar, chore tracking with a point system, a leaderboard, and goal/prize management. The repository is organized into frontend, backend, and shared documentation components.

---

## Table of Contents

### 1. Root Directory

- [TAPESTRY_PRD_AND_SYSTEM_DESIGN.md](https://github.com/sergiomasellis/Tapestry/blob/main/TAPESTRY_PRD_AND_SYSTEM_DESIGN.md)  
  *Product requirements and system design documentation.*

- [README.md](https://github.com/sergiomasellis/Tapestry/blob/main/README.md)  
  *Project overview, features, tech stack, setup instructions, and contribution guidelines.*  
  *(Last modified: 2025-08-04 19:08)*

- LICENSE  
  *MIT License.*

- [CONTRIBUTING.md](https://github.com/sergiomasellis/Tapestry/blob/main/CONTRIBUTING.md)  
  *Contribution guidelines.*

---

### 2. Frontend (`frontend/`)

- [README.md](https://github.com/sergiomasellis/Tapestry/blob/main/README.md)  
  *Frontend-specific getting started guide and Next.js resources.*  
  *(Last modified: 2025-08-04 19:08)*

- package.json  
  *Frontend dependencies and scripts (Next.js, React, Tailwind CSS, Radix UI, etc.).*  
  *(Last modified: 2025-08-04 19:08)*

- tsconfig.json  
  *TypeScript configuration for the frontend.*  
  *(Last modified: 2025-08-04 19:08)*

- next.config.ts, postcss.config.mjs, eslint.config.mjs, components.json  
  *Build, lint, and component configuration files.*

- pnpm-lock.yaml  
  *Dependency lock file.*

- **src/**  
  - **app/**  
    - layout.tsx  
      *Root layout for the Next.js app.*
    - page.tsx  
      *Main page component.*
    - globals.css  
      *Global styles.*
    - favicon.ico  
      *App icon.*

  - **lib/**  
    - utils.ts  
      *Utility functions.*

  - **features/**  
    *Feature modules (details not shown).*

  - **components/**  
    *Reusable UI components.*

- **public/**  
  *Static assets (SVGs, PNGs, etc.).*

---

### 3. Backend (`backend/`)

- [README.md](https://github.com/sergiomasellis/Tapestry/blob/main/README.md)  
  *Backend stack, quick start, API overview, and directory structure.*  
  *(Last modified: 2025-08-04 19:08)*

- pyproject.toml  
  *Backend dependencies (FastAPI, SQLAlchemy, LangGraph, etc.).*  
  *(Last modified: 2025-08-04 19:08)*

- uv.lock  
  *Dependency lock file.*

- data.db  
  *SQLite database file (auto-generated).*

- main.py  
  *Entrypoint for the backend.*

- **app/**  
  - main.py  
    *FastAPI app and router includes.*
  - \_\_init\_\_.py  
    *Package marker.*
  - **schemas/**  
    - schemas.py  
      *Pydantic models for API schemas.*
  - **routers/**  
    - users.py, points.py, goals.py, families.py, chores.py, calendars.py, auth.py, \_\_init\_\_.py  
      *API route handlers for each domain.*
  - **models/**  
    - models.py  
      *SQLAlchemy ORM models.*
    - models.ts  
      *TypeScript models (for type sharing or documentation).*
  - **db/**  
    - session.py  
      *Database engine/session management.*
  - **ai/**  
    - chore_graph.py  
      *LangGraph pipeline for AI-powered chore generation.*

---

## Key Concepts Illustrated

### Example: FastAPI App Initialization ([backend/app/main.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/main.py))

```python
from fastapi import FastAPI
from .routers import users, chores, points, goals, families, calendars, auth

app = FastAPI()

app.include_router(users.router)
app.include_router(chores.router)
app.include_router(points.router)
app.include_router(goals.router)
app.include_router(families.router)
app.include_router(calendars.router)
app.include_router(auth.router)
```

### Example: Next.js Frontend Script ([frontend/package.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/package.json))

```json
{
  "scripts": {
    "dev": "next dev --turbopack",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  }
}
```

### Example: TypeScript Path Aliases ([frontend/tsconfig.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/tsconfig.json))

```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

---

## Project Structure Diagram

```mermaid
graph TD
  A[Root]
  A --> B[frontend/]
  A --> C[backend/]
  A --> D[Shared Docs]
  B --> B1[src/]
  B --> B2[public/]
  B --> B3[package.json, tsconfig.json, ...]
  C --> C1[app/]
  C --> C2[pyproject.toml, main.py, ...]
  C1 --> C1a[routers/]
  C1 --> C1b[schemas/]
  C1 --> C1c[models/]
  C1 --> C1d[db/]
  C1 --> C1e[ai/]
  D --> D1[[README.md](https://github.com/sergiomasellis/Tapestry/blob/main/README.md)]
  D --> D2[[TAPESTRY_PRD_AND_SYSTEM_DESIGN.md](https://github.com/sergiomasellis/Tapestry/blob/main/TAPESTRY_PRD_AND_SYSTEM_DESIGN.md)]
```

---

## Primary Sources

- [README.md](https://github.com/sergiomasellis/Tapestry/blob/main/README.md) (Last modified: 2025-08-04 19:08)
- [frontend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/README.md) (Last modified: 2025-08-04 19:08)
- [frontend/package.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/package.json) (Last modified: 2025-08-04 19:08)
- [frontend/tsconfig.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/tsconfig.json) (Last modified: 2025-08-04 19:08)
- [backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md) (Last modified: 2025-08-04 19:08)
- backend/pyproject.toml (Last modified: 2025-08-04 19:08)
