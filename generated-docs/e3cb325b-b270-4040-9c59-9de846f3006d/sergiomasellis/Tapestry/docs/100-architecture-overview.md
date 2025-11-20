# Tapestry Architecture & Topology

| Repo     | Doc Type                | Date                | Branch |
|----------|------------------------|---------------------|--------|
| Tapestry | Architecture & Topology | 2025-08-04 19:08    | main   |

---

## Overview

Tapestry is a modern, touch-friendly, multi-user family calendar and chore management application. The system is architected with a clear separation of concerns between the frontend and backend, enabling independent development, deployment, and scaling.

- **Frontend:** Built with Next.js (TypeScript, Tailwind CSS), providing a responsive, interactive UI.
- **Backend:** Built with FastAPI (Python), using SQLAlchemy for ORM and SQLite for development storage. Integrates LangGraph for AI-powered chore generation and point assignment.

The architecture follows a classic web application topology, with the frontend acting as a client to the backend's REST API. All persistent data and business logic reside in the backend.

---

## High-Level Components

### 1. Frontend (`frontend/`)
- **Framework:** Next.js (React, TypeScript)
- **Responsibilities:**
  - User authentication and session management (via API)
  - Calendar/event display and interaction
  - Chore tracking and leaderboard UI
  - Goal and prize management UI
  - API communication with backend (REST)
- **Key Files:**
  - `frontend/src/app/page.tsx`, `layout.tsx` — main app shell and routing
  - `[frontend/package.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/package.json)`, `tsconfig.json` — configuration and dependencies

### 2. Backend (`backend/`)
- **Framework:** FastAPI (Python)
- **Responsibilities:**
  - User, family, event, chore, point, and goal management
  - Authentication (token-based)
  - AI-powered chore generation (LangGraph)
  - Data persistence (SQLite via SQLAlchemy)
  - REST API endpoints for all business entities
- **Key Files:**
  - `[backend/app/main.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/main.py)` — FastAPI app and router includes
  - `backend/app/routers/` — modular API routers (users, families, chores, etc.)
  - `backend/app/models/` — SQLAlchemy models
  - `backend/app/schemas/` — Pydantic schemas
  - `[backend/app/ai/chore_graph.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/ai/chore_graph.py)` — LangGraph pipeline for AI features

### 3. Database
- **Type:** SQLite (development)
- **Location:** `backend/data.db`
- **Managed by:** SQLAlchemy ORM

---

## Component Interaction

- **Frontend** communicates with **Backend** exclusively via HTTP REST API calls.
- **Backend** exposes endpoints for all CRUD operations and business flows.
- **AI features** (chore suggestion, point assignment) are triggered by API calls and handled server-side.
- **Database** is accessed only by the backend; the frontend has no direct data access.

---

## Deployment Topology

- **Frontend**: Deployed as a static site or server-rendered app (e.g., Vercel, Netlify, or custom Node.js server).
- **Backend**: Deployed as a Python web service (e.g., Uvicorn, Docker container, or cloud function).
- **Communication**: All client-to-server communication is via REST API over HTTP(S).
- **Environment Variables**: Used for secrets and configuration (see [backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md)).

---

## Architecture Diagram

```mermaid
flowchart LR
    subgraph Frontend [Next.js Frontend]
        FE[User Browser<br/>Next.js App]
    end

    subgraph Backend [FastAPI Backend]
        API[REST API<br/>(FastAPI)]
        DB[(SQLite Database)]
        AI[LangGraph<br/>Chore AI]
    end

    FE -- "HTTP (REST API)" --> API
    API -- "ORM" --> DB
    API -- "Chore/Point Requests" --> AI
    AI -- "DB Writes" --> DB
```

---

## Design Principles

- **Separation of Concerns:** UI/UX logic is isolated from business logic and data management.
- **API-First:** All features are exposed via documented REST endpoints.
- **Extensibility:** Modular backend routers and frontend features allow for easy addition of new domains (e.g., calendar integrations).
- **Security:** Authentication and authorization handled server-side; secrets managed via environment variables.

---

## Primary Sources

- [README.md](https://github.com/sergiomasellis/Tapestry/blob/main/README.md) (Last modified: 2025-08-04 19:08)
- [frontend/tsconfig.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/tsconfig.json) (Last modified: 2025-08-04 19:08)
- [frontend/package.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/package.json) (Last modified: 2025-08-04 19:08)
- [frontend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/README.md) (Last modified: 2025-08-04 19:08)
- backend/pyproject.toml (Last modified: 2025-08-04 19:08)
- [backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md) (Last modified: 2025-08-04 19:08)