# Tapestry Routing & Entrypoints 101

| Repo      | Doc Type   | Date                | Branch |
|-----------|------------|---------------------|--------|
| Tapestry  | 101        | 2025-08-04 19:08    | main   |

---

This document provides a high-level overview of routing and entrypoints in the Tapestry application, covering both the FastAPI backend and the Next.js frontend. It is intended for developers seeking to understand how HTTP requests flow through the system, how endpoints are structured, and where to start when extending or debugging the app.

---

## Overview

Tapestry is a modern, multi-user family calendar and chore management app. Its architecture is split into:

- **Backend**: FastAPI app with modular routers for users, points, chores, families, calendars, goals, and authentication.
- **Frontend**: Next.js app using the `/app` directory for file-based routing, with TypeScript and Tailwind CSS.

---

## Backend Routing (FastAPI)

The backend is organized around FastAPI's router system, with each domain (users, points, chores, etc.) having its own router module under `backend/app/routers/`. All routers are included in the main FastAPI app instance.

**Entrypoint:**
- `[backend/app/main.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/main.py)` — creates the FastAPI app and includes all routers.

**Router Modules:**
- `[backend/app/routers/users.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/users.py)`
- `[backend/app/routers/points.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/points.py)`
- `[backend/app/routers/chores.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/chores.py)`
- `[backend/app/routers/families.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/families.py)`
- `[backend/app/routers/calendars.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/calendars.py)`
- `[backend/app/routers/goals.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/goals.py)`
- `[backend/app/routers/auth.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/auth.py)`

**Router Inclusion Example**  
(from `[backend/app/main.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/main.py)`, Last modified: 2025-08-04 19:08):

```python
from fastapi import FastAPI
from app.routers import users, points, chores, families, calendars, goals, auth

app = FastAPI()

app.include_router(users.router)
app.include_router(points.router)
app.include_router(chores.router)
app.include_router(families.router)
app.include_router(calendars.router)
app.include_router(goals.router)
app.include_router(auth.router)
```

**Router Structure Example**  
(from `[backend/app/routers/users.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/users.py)`, Last modified: 2025-08-04 19:08):

```python
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
async def list_users():
    return [{"id": 1, "name": "Alice"}]
```

**API Entrypoints:**
- `/users/` — User management
- `/points/` — Points tracking
- `/chores/` — Chore management
- `/families/` — Family group management
- `/calendars/` — Calendar integrations
- `/goals/` — Goal setting
- `/auth/` — Authentication

---

## Frontend Routing (Next.js)

The frontend uses Next.js's App Router (`/app` directory) for file-based routing. Each file in `frontend/src/app/` corresponds to a route.

**Entrypoints:**
- `frontend/src/app/page.tsx` — Home page (`/`)
- `frontend/src/app/layout.tsx` — Root layout (wraps all pages)

**Page Example**  
(from `frontend/src/app/page.tsx`, Last modified: 2025-08-04 19:08):

```typescript
export default function HomePage() {
  return (
    <main>
      <h1>Welcome to Tapestry</h1>
      {/* Calendar and leaderboard components here */}
    </main>
  );
}
```

**Layout Example**  
(from `frontend/src/app/layout.tsx`, Last modified: 2025-08-04 19:08):

```typescript
export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        {/* Global navigation, modals, etc. */}
        {children}
      </body>
    </html>
  );
}
```

**Routing Principles:**
- Each `.tsx` file in `app/` becomes a route.
- Nested folders create nested routes.
- API calls from the frontend are made to the backend FastAPI endpoints (e.g., `/api/users` → `http://localhost:8000/users/`).

---

## Routing Flow Diagram

```mermaid
flowchart TD
    subgraph Frontend (Next.js)
      A[User visits /] --> B[app/page.tsx]
      B --> C[Fetch data from backend]
    end

    subgraph Backend (FastAPI)
      D[/users/] --> E[users.py router]
      F[/points/] --> G[points.py router]
      H[/chores/] --> I[chores.py router]
      J[/families/] --> K[families.py router]
      L[/calendars/] --> M[calendars.py router]
      N[/goals/] --> O[goals.py router]
      P[/auth/] --> Q[auth.py router]
    end

    C -->|HTTP| D
    C -->|HTTP| F
    C -->|HTTP| H
    C -->|HTTP| J
    C -->|HTTP| L
    C -->|HTTP| N
    C -->|HTTP| P
```

---

## Key Takeaways

- **Backend routers** are modular and grouped by domain, all included in `app/main.py`.
- **Frontend routes** are file-based, with `page.tsx` as the main entrypoint.
- **API calls** from the frontend are routed to the backend's RESTful endpoints.
- **Extending routing**: Add new routers in `backend/app/routers/` and include them in `main.py`; add new pages/components in `frontend/src/app/`.

---

## Primary Sources

- [README.md](https://github.com/sergiomasellis/Tapestry/blob/main/README.md) (Last modified: 2025-08-04 19:08)
- [backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md) (Last modified: 2025-08-04 19:08)
- [backend/app/main.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/main.py) (Last modified: 2025-08-04 19:08)
- [backend/app/routers/users.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/users.py) (Last modified: 2025-08-04 19:08)
- frontend/src/app/page.tsx (Last modified: 2025-08-04 19:08)
- frontend/src/app/layout.tsx (Last modified: 2025-08-04 19:08)
- [frontend/tsconfig.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/tsconfig.json) (Last modified: 2025-08-04 19:08)
- [frontend/package.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/package.json) (Last modified: 2025-08-04 19:08)