# Tapestry Architecture & Topology

| Repo     | Doc Type             | Date                | Branch |
|----------|---------------------|---------------------|--------|
| Tapestry | Architecture & Topology | 2025-08-04 19:08   | main   |

---

## Overview

Tapestry is a modern, touch-friendly, multi-user calendar and family management application. It consists of two main components:

- **Frontend**: Built with Next.js (TypeScript, Tailwind CSS), providing a responsive web UI for families to manage calendars, chores, points, and goals.
- **Backend**: Built with FastAPI (Python), using SQLAlchemy ORM and SQLite for development, exposing a REST API for all business logic, authentication, and data persistence.

The architecture is designed for clear separation of concerns, scalability, and ease of development.

---

## High-Level Architecture

```mermaid
flowchart TD
    subgraph Frontend [Next.js Frontend]
        FE[User Browser<br/>React Components]
        FE_API[API Layer (/api)]
    end

    subgraph Backend [FastAPI Backend]
        API[REST API Endpoints]
        AUTH[Authentication & AuthZ]
        DOMAIN[Business Logic<br/>(Chores, Points, Goals, Families)]
        DB[(SQLite DB)]
        AI[LangGraph<br/>Chore Generation]
    end

    FE -- HTTP/JSON --> API
    FE_API -- Proxy/SSR --> API
    API -- ORM --> DB
    API -- Invokes --> AI
    API -- Handles --> AUTH
    API -- Implements --> DOMAIN
```

---

## Component Breakdown

### 1. Frontend (`frontend/`)

- **Framework**: Next.js (React, TypeScript)
- **UI**: Tailwind CSS, Radix UI components
- **Structure**:
  - `src/app/`: Main application entrypoint, layouts, and pages
  - `src/features/`, `src/components/`: Feature modules and reusable UI components
  - **API Calls**: Uses fetch/Axios to communicate with backend REST endpoints
- **Responsibilities**:
  - Render weekly calendar, chore lists, points leaderboard, and goal tracking
  - Handle user authentication (token-based)
  - Provide responsive, touch-friendly UX

### 2. Backend (`backend/`)

- **Framework**: FastAPI (Python 3.12+)
- **ORM**: SQLAlchemy 2.0
- **Database**: SQLite (development)
- **Structure**:
  - `app/main.py`: FastAPI app, includes all routers
  - `app/routers/`: Modular route handlers (users, families, chores, points, goals, calendars, auth)
  - `app/models/`: SQLAlchemy models
  - `app/schemas/`: Pydantic schemas for validation/serialization
  - `app/db/session.py`: DB engine/session management
  - `app/ai/chore_graph.py`: LangGraph pipeline for AI-powered chore generation
- **Responsibilities**:
  - Expose RESTful API for all entities and actions
  - Authenticate and authorize users (JWT tokens)
  - Persist and query data
  - Integrate with AI pipeline for chore suggestions and point assignment

### 3. Database

- **Type**: SQLite (default for development)
- **Location**: `backend/data.db`
- **Entities**: Users, Families, Chores, Points, Goals, Calendars

---

## Interaction Flow

1. **User accesses the frontend** via browser (Next.js app).
2. **Frontend authenticates** the user (login/signup), stores JWT token.
3. **Frontend makes API requests** (e.g., fetch calendar, add chore) to the backend, including the JWT token.
4. **Backend validates the token**, processes the request, interacts with the database, and returns data.
5. **For AI-powered features** (e.g., chore suggestions), backend invokes the LangGraph pipeline.
6. **Frontend updates UI** based on backend responses.

---

## Architectural Style

- **Client-Server**: Clear separation between frontend (client) and backend (server).
- **RESTful API**: All data and actions are exposed via HTTP endpoints.
- **Modular Monorepo**: Both frontend and backend are maintained in a single repository for easier development and deployment.
- **Stateless Backend**: Authentication is token-based (JWT), enabling stateless API servers.

---

## Technology Stack

- **Frontend**: Next.js, React, TypeScript, Tailwind CSS, Radix UI
- **Backend**: FastAPI, SQLAlchemy, Pydantic, LangGraph (AI), Uvicorn
- **Database**: SQLite (development), pluggable for production
- **Dev Tools**: uv (Python env manager), ruff (lint), dotenv

---

## Directory Structure (Key Parts)

- `frontend/`
  - `src/app/`, `src/features/`, `src/components/`
  - `package.json`, `tsconfig.json`
- `backend/`
  - `app/main.py`, `app/routers/`, `app/models/`, `app/schemas/`, `app/db/`, `app/ai/`
  - `pyproject.toml`, `data.db`

---

## Primary Sources

- [README.md](https://github.com/sergiomasellis/Tapestry/blob/main/README.md) (Last modified: 2025-08-04 19:08)
- [frontend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/README.md) (Last modified: 2025-08-04 19:08)
- [backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md) (Last modified: 2025-08-04 19:08)
- [frontend/tsconfig.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/tsconfig.json) (Last modified: 2025-08-04 19:08)
- [frontend/package.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/package.json) (Last modified: 2025-08-04 19:08)
- backend/pyproject.toml (Last modified: 2025-08-04 19:08)