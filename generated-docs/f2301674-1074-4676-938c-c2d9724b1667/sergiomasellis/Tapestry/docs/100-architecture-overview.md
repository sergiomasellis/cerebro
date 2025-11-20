# Tapestry Architecture & Topology

| Repo    | Doc Type                | Date                | Branch |
|---------|------------------------|---------------------|--------|
| Tapestry| Architecture & Topology | 2025-08-04 19:08    | None   |

---

## Overview

Tapestry is a modern, touch-friendly multi-user calendar and family management application. Its architecture is split into two primary components:

- **Frontend**: Built with Next.js (TypeScript, Tailwind CSS), providing the user interface and client-side logic.
- **Backend**: Built with FastAPI (Python, SQLAlchemy), exposing RESTful APIs, handling business logic, and managing persistence.

This separation enables clear boundaries between presentation and business/data layers, supporting scalability, maintainability, and independent development.

---

## High-Level Architecture

```mermaid
flowchart TD
    subgraph Frontend [frontend/ (Next.js)]
        FE_App[UI (React Components)]
        FE_Features[Features (Calendar, Chores, Leaderboard)]
        FE_Utils[Shared Utils]
        FE_App --> FE_Features
        FE_Features --> FE_Utils
    end

    subgraph Backend [backend/ (FastAPI)]
        BE_API[REST API (FastAPI Routers)]
        BE_Models[SQLAlchemy Models]
        BE_Schemas[Pydantic Schemas]
        BE_AI[AI Chore Pipeline (LangGraph)]
        BE_DB[SQLite DB]
        BE_API --> BE_Models
        BE_API --> BE_Schemas
        BE_API --> BE_AI
        BE_Models --> BE_DB
    end

    FE_App -- HTTP (REST) --> BE_API
```

---

## Component Breakdown

### 1. Frontend (`frontend/`)

- **Framework**: Next.js (React, TypeScript, Tailwind CSS)
- **Structure**:
  - `src/app/`: Application entrypoints (`layout.tsx`, `page.tsx`)
  - `src/features/`: Feature modules (calendar, chores, leaderboard, etc.)
  - `src/components/`: Shared UI components
  - `src/lib/`: Utility functions
  - `public/`: Static assets (SVGs, images)
- **Responsibilities**:
  - Renders interactive UI for family members
  - Handles client-side state and navigation
  - Communicates with backend via REST API

### 2. Backend (`backend/`)

- **Framework**: FastAPI (Python 3.12+)
- **Structure**:
  - `app/main.py`: FastAPI app instantiation and router inclusion
  - `app/routers/`: API route handlers (users, families, chores, points, goals, calendars, auth)
  - `app/models/`: SQLAlchemy ORM models
  - `app/schemas/`: Pydantic data validation schemas
  - `app/db/session.py`: Database session/engine setup
  - `app/ai/chore_graph.py`: AI pipeline for chore generation/point assignment (LangGraph)
- **Responsibilities**:
  - Exposes RESTful endpoints for all domain entities
  - Handles authentication, authorization, and business logic
  - Manages persistence in SQLite (development)
  - Integrates AI for chore suggestions and point calculations

---

## Interaction Flow

1. **User Interaction**: Users interact with the web UI (calendar, chores, leaderboard, etc.).
2. **API Requests**: The frontend issues HTTP requests to the backend REST API for data retrieval and mutations.
3. **Backend Processing**:
    - API routers validate and process requests.
    - Business logic is applied (e.g., point assignment, chore completion).
    - AI pipeline may be invoked for advanced features (e.g., chore suggestions).
    - Data is persisted/retrieved via SQLAlchemy models.
4. **Response**: Backend returns JSON responses, which the frontend consumes to update the UI.

---

## Technology Stack

- **Frontend**: Next.js, React 19, TypeScript, Tailwind CSS, Radix UI, date-fns
- **Backend**: FastAPI, SQLAlchemy 2, Pydantic v2, LangGraph, SQLite, python-dotenv, uvicorn

---

## Directory Topology

```
.
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── features/
│   │   ├── components/
│   │   └── lib/
│   └── public/
└── backend/
    ├── app/
    │   ├── main.py
    │   ├── routers/
    │   ├── models/
    │   ├── schemas/
    │   ├── db/
    │   └── ai/
    └── data.db
```

---

## Key Architectural Principles

- **Separation of Concerns**: UI and API layers are strictly separated.
- **Modularity**: Features are encapsulated in both frontend and backend for maintainability.
- **Scalability**: The architecture supports future enhancements (e.g., external calendar integrations, AI features).
- **Developer Experience**: Modern frameworks and tooling for rapid development and testing.

---

## Primary Sources

- [README.md](./README.md) (Last modified: 2025-08-04 19:08)
- [frontend/README.md](./frontend/README.md) (Last modified: 2025-08-04 19:08)
- [backend/README.md](./backend/README.md) (Last modified: 2025-08-04 19:08)
- [frontend/tsconfig.json](./frontend/tsconfig.json) (Last modified: 2025-08-04 19:08)
- [frontend/package.json](./frontend/package.json) (Last modified: 2025-08-04 19:08)
- [backend/pyproject.toml](./backend/pyproject.toml) (Last modified: 2025-08-04 19:08)
