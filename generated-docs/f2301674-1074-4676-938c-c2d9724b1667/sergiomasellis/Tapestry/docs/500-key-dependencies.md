# Tapestry – Key Dependencies

| Repo      | Doc Type           | Date                | Branch |
|-----------|--------------------|---------------------|--------|
| Tapestry  | Key Dependencies   | 2025-08-04 19:08    | None   |

---

This document catalogs the key internal and external dependencies for the Tapestry project, as defined in the frontend and backend package manifests. Understanding these dependencies is crucial for development, troubleshooting, and future upgrades.

## Overview

Tapestry is a full-stack family calendar and chore management application. Its architecture is split into a **Next.js/React frontend** and a **FastAPI/Python backend**, each with its own dependency ecosystem.

---

## 1. Frontend Dependencies

**Source:** `frontend/package.json` (Last modified: 2025-08-04 19:08)

The frontend is built with Next.js and TypeScript, styled using Tailwind CSS, and leverages several UI and utility libraries.

### Core Frameworks & Libraries

- **next** (`15.4.5`): React-based framework for SSR, routing, and API routes.
- **react** (`19.1.0`) & **react-dom** (`19.1.0`): Core UI library.
- **typescript** (`^5`): Static typing for JavaScript.

### UI & Styling

- **@radix-ui/react-***: Suite of accessible UI primitives (avatar, dialog, dropdown, navigation, popover, select, separator, slot, tabs, tooltip).
- **tailwindcss** (`^4`): Utility-first CSS framework.
- **tw-animate-css**: Animation utilities for Tailwind.
- **tailwind-merge**: Utility class merging for Tailwind.
- **postcss**: Used via `postcss.config.mjs` for CSS processing.

### Utilities

- **clsx**: Conditional className utility.
- **class-variance-authority**: Variant management for class names.
- **date-fns**: Date manipulation utilities.
- **lucide-react**: Icon library.

### Tooling & Linting

- **eslint** & **eslint-config-next**: Linting and code quality.
- **@types/***: TypeScript type definitions for Node, React, etc.
- **@eslint/eslintrc**: ESLint configuration.
- **@tailwindcss/postcss**: Tailwind/PostCSS integration.

---

## 2. Backend Dependencies

**Source:** `backend/pyproject.toml` (Last modified: 2025-08-04 19:08)

The backend is a FastAPI application using SQLAlchemy for ORM and LangGraph for AI-driven features.

### Core Frameworks & Libraries

- **fastapi** (`>=0.116.1`): Modern, async Python web framework.
- **uvicorn** (`>=0.35.0`): ASGI server for FastAPI.
- **sqlalchemy** (`>=2.0.42`): ORM for database access.
- **pydantic[email]** (`>=2.11.7`): Data validation and settings management.
- **python-dotenv** (`>=1.1.1`): Loads environment variables from `.env`.
- **typing-extensions** (`>=4.14.1`): Backports for Python typing features.

### AI & Automation

- **langgraph** (`>=0.6.3`): Used for AI-based chore generation and point assignment pipelines.

### Development Tools

- **ruff** (`>=0.12.7`): Linter for Python (in `dev` dependency group).

---

## 3. Internal Service Dependencies

- **SQLite**: Used as the development database (see `backend/README.md`, Last modified: 2025-08-04 19:08).
- **LangGraph**: Integrated for AI-powered features (chore suggestion, point assignment).

---

## 4. Third-Party APIs & Integrations

While the current codebase scaffolds for integrations, the following are planned or partially mocked:

- **Google Calendar API**: For calendar sync (see `backend/README.md`).
- **Amazon Alexa Reminders API**: For voice assistant integration.
- **OAuth Providers**: For authentication (future).

---

## 5. Dependency Topology

Below is a high-level dependency graph showing the relationship between core components and their key dependencies:

```mermaid
graph TD
  subgraph Frontend
    FE[Next.js/React App]
    FE --> Tailwind[tailwindcss]
    FE --> Radix[@radix-ui/*]
    FE --> DateFns[date-fns]
    FE --> Lucide[lucide-react]
    FE --> Typescript[typescript]
  end

  subgraph Backend
    BE[FastAPI App]
    BE --> SQLA[SQLAlchemy]
    BE --> Pydantic[Pydantic]
    BE --> Uvicorn[uvicorn]
    BE --> Dotenv[python-dotenv]
    BE --> LangGraph[LangGraph]
    BE --> SQLite[SQLite]
  end

  FE <--> BE
  BE -->|Future| Google[Google Calendar API]
  BE -->|Future| Alexa[Alexa Reminders API]
```

---

## 6. Dependency Management

- **Frontend:** Managed via `npm`/`pnpm` and `package.json`. Lockfile: `pnpm-lock.yaml`.
- **Backend:** Managed via `uv` (see `backend/README.md`) and `pyproject.toml`. Lockfile: `uv.lock`.

---

## 7. Security & Upgrades

- **Frontend:** Keep dependencies up to date with `npm audit` and `pnpm update`.
- **Backend:** Use `uv` or `pip` to update, and monitor for vulnerabilities in Python packages.

---

## Primary Sources

- [`frontend/package.json`](frontend/package.json) (Last modified: 2025-08-04 19:08)
- [`backend/pyproject.toml`](backend/pyproject.toml) (Last modified: 2025-08-04 19:08)
- [`backend/README.md`](backend/README.md) (Last modified: 2025-08-04 19:08)
- [`frontend/README.md`](frontend/README.md) (Last modified: 2025-08-04 19:08)
- [`README.md`](README.md) (Last modified: 2025-08-04 19:08)