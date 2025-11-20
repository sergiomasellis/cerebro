# Tapestry Architecture Overview

| Repo     | Doc Type      | Date                | Branch |
|----------|--------------|---------------------|--------|
| Tapestry | Architecture | 2025-08-04 19:08    | main   |

---

Tapestry is a modern, touch-friendly multi-user calendar and family management application. Its architecture is designed around a clear separation of concerns, using a Next.js frontend, a FastAPI backend, and a SQLite database for development. This document provides a high-level overview of the system's architecture, illustrating the relationships and data flow between its major components.

## High-Level Architecture

Tapestry is structured as a classic web application with a decoupled frontend and backend:

- **Frontend**: Built with Next.js (TypeScript, Tailwind CSS), responsible for all user interactions and UI rendering.
- **Backend**: Built with FastAPI (Python), exposes RESTful APIs, handles authentication, business logic, and data persistence.
- **Database**: SQLite (development), managed via SQLAlchemy ORM in the backend.

Below is a conceptual diagram of the system:

```mermaid
graph TD
    subgraph Frontend (Next.js)
        A[User Browser]
        B[Next.js App]
    end
    subgraph Backend (FastAPI)
        C[FastAPI API Server]
        D[LangGraph AI Pipeline]
        E[SQLAlchemy ORM]
    end
    F[(SQLite Database)]

    A -->|HTTP(S)| B
    B -->|REST API| C
    C -->|ORM| E
    E -->|SQL| F
    C --> D
    D --> C
```

---

## Component Breakdown

### 1. Frontend (`frontend/`)

- **Framework**: Next.js (TypeScript)
- **Features**: Weekly calendar, event details, chore tracking, leaderboard, goal/prize tracking.
- **Key Files**:
  - `frontend/src/app/page.tsx` – Main page component.
  - `frontend/src/app/layout.tsx` – Application layout.
  - `[frontend/package.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/package.json)` – Declares dependencies and scripts.
  - `[frontend/tsconfig.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/tsconfig.json)` – TypeScript configuration.

**Example: Next.js Page Component**
```typescript
// frontend/src/app/page.tsx
export default function HomePage() {
  return (
    <main>
      <h1>Welcome to Tapestry</h1>
      {/* Calendar and features rendered here */}
    </main>
  );
}
```

### 2. Backend (`backend/`)

- **Framework**: FastAPI (Python)
- **Responsibilities**: API endpoints, authentication, business logic, AI-powered chore generation, database access.
- **Key Files**:
  - `[backend/app/main.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/main.py)` – FastAPI app and router includes.
  - `backend/app/routers/` – Modular route handlers (users, chores, families, etc.).
  - `[backend/app/models/models.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/models/models.py)` – SQLAlchemy ORM models.
  - `[backend/app/schemas/schemas.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/schemas/schemas.py)` – Pydantic schemas for validation.
  - `[backend/app/ai/chore_graph.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/ai/chore_graph.py)` – LangGraph AI pipeline for chore generation.
  - `[backend/app/db/session.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/db/session.py)` – Database session and engine setup.

**Example: FastAPI App Initialization**
```python
# [backend/app/main.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/main.py)
from fastapi import FastAPI
from app.routers import users, chores, families

app = FastAPI()
app.include_router(users.router)
app.include_router(chores.router)
app.include_router(families.router)
```

### 3. Database

- **Engine**: SQLite (for development)
- **ORM**: SQLAlchemy (Python)
- **Schema**: Tables for users, families, events, chores, points, goals, etc.
- **Initialization**: Tables auto-created on first backend run.

**Example: SQLAlchemy Model**
```python
# [backend/app/models/models.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/models/models.py)
from sqlalchemy import Column, Integer, String
from app.db.session import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
```

---

## Data Flow

1. **User Interaction**: Users interact with the Next.js frontend in their browser.
2. **API Requests**: The frontend makes HTTP requests to the FastAPI backend for data (e.g., fetching events, submitting chores).
3. **Business Logic & AI**: The backend processes requests, applies business logic, and may invoke the LangGraph AI pipeline for features like chore suggestions.
4. **Persistence**: The backend reads from and writes to the SQLite database via SQLAlchemy.
5. **Response**: The backend returns JSON responses to the frontend, which updates the UI accordingly.

---

## Extensibility & Integrations

- **AI/Automation**: The backend integrates LangGraph for AI-powered features (e.g., chore assignment).
- **External Calendars**: Planned integrations with Google Calendar, Alexa Reminders, etc. (see [backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md)).
- **Authentication**: JWT-based, with support for admin/master password.

---

## Primary Sources

- [README.md](https://github.com/sergiomasellis/Tapestry/blob/main/README.md) (Last modified: 2025-08-04 19:08)
- [frontend/tsconfig.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/tsconfig.json) (Last modified: 2025-08-04 19:08)
- [frontend/package.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/package.json) (Last modified: 2025-08-04 19:08)
- [frontend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/README.md) (Last modified: 2025-08-04 19:08)
- backend/pyproject.toml (Last modified: 2025-08-04 19:08)
- [backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md) (Last modified: 2025-08-04 19:08)
- [backend/app/main.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/main.py)
- [backend/app/models/models.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/models/models.py)