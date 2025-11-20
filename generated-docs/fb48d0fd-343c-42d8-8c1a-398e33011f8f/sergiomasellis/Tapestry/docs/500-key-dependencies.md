# Tapestry: Key Dependencies and Service Structure

| Repo      | Doc Type      | Date                | Branch |
|-----------|--------------|---------------------|--------|
| Tapestry  | Dependencies | 2025-08-04 19:08    | main   |

## Overview

Tapestry is a modern, touch-friendly multi-user calendar and family management application. Its architecture is split into a Next.js/TypeScript frontend and a FastAPI/SQLAlchemy backend, with SQLite as the development database. This document outlines the project's key dependencies—both third-party and internal—and illustrates the service structure.

---

## Dependency Summary

### Frontend (`[frontend/package.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/package.json)`, Last modified: 2025-08-04 19:08)

- **Frameworks & Core Libraries**
  - `next` (v15.4.5): React-based SSR/SSG framework.
  - `react` (v19.1.0), `react-dom` (v19.1.0): UI library.
  - `typescript` (dev): Type safety.
- **Styling**
  - `tailwindcss`, `postcss`, `tw-animate-css`: Utility-first CSS and animation.
  - `clsx`, `class-variance-authority`, `tailwind-merge`: Class name composition.
- **UI Components**
  - `@radix-ui/react-*`: Accessible, composable UI primitives (Avatar, Dialog, DropdownMenu, NavigationMenu, Popover, Select, Separator, Slot, Tabs, Tooltip).
  - `lucide-react`: Icon set.
- **Date Handling**
  - `date-fns`: Modern date utility library.
- **Linting & Tooling**
  - `eslint`, `eslint-config-next`, `@eslint/eslintrc`: Linting.
  - `@types/*`: TypeScript type definitions.

#### Example: Next.js Custom Layout (from `frontend/src/app/layout.tsx`)
```typescript
export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="bg-gray-50">{children}</body>
    </html>
  );
}
```

---

### Backend (`backend/pyproject.toml`, Last modified: 2025-08-04 19:08)

- **Frameworks & Core Libraries**
  - `fastapi`: High-performance Python web API.
  - `uvicorn`: ASGI server for FastAPI.
  - `sqlalchemy`: ORM for database access.
  - `pydantic[email]`: Data validation and settings management.
- **AI/Automation**
  - `langgraph`: Pipeline for AI-driven chore generation and point assignment.
- **Environment & Typing**
  - `python-dotenv`: Loads environment variables from `.env`.
  - `typing-extensions`: Typing support for Python.
- **Development**
  - `ruff`: Linter.
  - `uv`: Project/env manager.

#### Example: FastAPI App Initialization (from `[backend/app/main.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/main.py)`)
```python
from fastapi import FastAPI
from app.routers import users, chores, goals

app = FastAPI()
app.include_router(users.router)
app.include_router(chores.router)
app.include_router(goals.router)
```

---

## Internal Service Structure

### Frontend

- **`frontend/src/app/`**: Next.js app directory (routing, layouts, pages).
- **`frontend/src/components/`**: Shared React components.
- **`frontend/src/lib/`**: Utility functions.
- **`[frontend/package.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/package.json)`**: Dependency and script definitions.
- **`[frontend/tsconfig.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/tsconfig.json)`**: TypeScript configuration, including path aliases for `@/*`.

#### Example: TypeScript Path Alias (from `[frontend/tsconfig.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/tsconfig.json)`)
```json
"paths": {
  "@/*": ["./src/*"]
}
```

---

### Backend

- **`[backend/app/main.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/main.py)`**: FastAPI app entrypoint, includes routers.
- **`backend/app/routers/`**: Modular API endpoints (users, families, chores, calendars, points, goals, auth).
- **`backend/app/models/`**: SQLAlchemy models for database tables.
- **`backend/app/schemas/`**: Pydantic models for request/response validation.
- **`[backend/app/db/session.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/db/session.py)`**: Database engine/session management.
- **`[backend/app/ai/chore_graph.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/ai/chore_graph.py)`**: LangGraph pipeline for AI-powered chore/point logic.

#### Example: SQLAlchemy Session (from `[backend/app/db/session.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/db/session.py)`)
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///./data.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

---

## Service Architecture

```mermaid
graph TD
  subgraph Frontend (Next.js/TypeScript)
    A[User Interface]
    B[Radix UI Components]
    C[API Calls]
    A --> B
    A --> C
  end

  subgraph Backend (FastAPI/Python)
    D[API Routers]
    E[SQLAlchemy Models]
    F[Pydantic Schemas]
    G[LangGraph AI Pipeline]
    H[SQLite Database]
    D --> E
    D --> F
    D --> G
    E --> H
  end

  C -- REST/JSON --> D
```

---

## Primary Sources

- [README.md](https://github.com/sergiomasellis/Tapestry/blob/main/README.md) (Last modified: 2025-08-04 19:08)
- [frontend/package.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/package.json) (Last modified: 2025-08-04 19:08)
- [frontend/tsconfig.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/tsconfig.json) (Last modified: 2025-08-04 19:08)
- [frontend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/README.md) (Last modified: 2025-08-04 19:08)
- backend/pyproject.toml (Last modified: 2025-08-04 19:08)
- [backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md) (Last modified: 2025-08-04 19:08)