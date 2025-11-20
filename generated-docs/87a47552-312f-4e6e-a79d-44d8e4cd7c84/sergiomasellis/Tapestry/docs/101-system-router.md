# Tapestry System Router 101

| Repo     | Doc Type         | Date                | Branch |
|----------|------------------|---------------------|--------|
| Tapestry | System Router 101| 2025-08-04 19:08    | main   |

## Overview

The Tapestry backend is structured as a FastAPI application, with all HTTP API entrypoints organized via modular routers. Each domain (users, points, goals, families, chores, calendars, authentication) is encapsulated in its own router module under `backend/app/routers/`. The main FastAPI app (`[backend/app/main.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/main.py)`) includes these routers, exposing a unified REST API surface.

This document describes the routing topology, entrypoint structure, and router composition for the Tapestry backend.

---

## Entrypoint: FastAPI Application

- **File:** [backend/app/main.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/main.py) (Last modified: 2025-08-04 19:08)
- **Purpose:** Defines the FastAPI app instance and includes all routers.
- **Entrypoint:** `app = FastAPI()`
- **Router Inclusion:** Each router from `backend/app/routers/` is imported and included with a specific prefix.

### Example (Pseudocode)

```python
from fastapi import FastAPI
from app.routers import users, points, goals, families, chores, calendars, auth

app = FastAPI()

app.include_router(auth.router, prefix="/auth")
app.include_router(users.router, prefix="/users")
app.include_router(families.router, prefix="/families")
app.include_router(calendars.router, prefix="/calendars")
app.include_router(chores.router, prefix="/chores")
app.include_router(points.router, prefix="/points")
app.include_router(goals.router, prefix="/goals")
```

---

## Router Modules

All routers are located in `backend/app/routers/` (Last modified: 2025-08-04 19:08):

- users.py
- points.py
- goals.py
- families.py
- chores.py
- calendars.py
- auth.py

Each router:
- Defines a FastAPI `APIRouter` instance.
- Declares endpoints for its domain (CRUD, listing, actions).
- Is included in the main app with a route prefix.

### Router Prefixes and Example Endpoints

| Router Module      | Prefix         | Example Endpoint(s)           |
|--------------------|---------------|-------------------------------|
| auth.py            | /auth         | /auth/login, /auth/admin-login|
| users.py           | /users        | /users/, /users/{id}          |
| families.py        | /families     | /families/, /families/invite  |
| calendars.py       | /calendars    | /calendars/, /calendars/sync  |
| chores.py          | /chores       | /chores/, /chores/generate    |
| points.py          | /points       | /points/, /points/add         |
| goals.py           | /goals        | /goals/, /goals/{id}          |

---

## Routing Flow

1. **HTTP Request** arrives at the FastAPI server (default: port 8000).
2. **FastAPI app** (`[backend/app/main.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/main.py)`) receives the request.
3. **Router dispatch:** The app matches the request path to the appropriate router based on the prefix.
4. **Endpoint handler:** The router's endpoint function is invoked, handling authentication, validation, and business logic.
5. **Response** is returned to the client.

---

## Router Topology Diagram

```mermaid
graph TD
    A[FastAPI App<br>[backend/app/main.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/main.py)] --> B1[/auth<br>routers/auth.py]
    A --> B2[/users<br>routers/users.py]
    A --> B3[/families<br>routers/families.py]
    A --> B4[/calendars<br>routers/calendars.py]
    A --> B5[/chores<br>routers/chores.py]
    A --> B6[/points<br>routers/points.py]
    A --> B7[/goals<br>routers/goals.py]
```

---

## Router Inclusion Pattern

- All routers are included in the main app at startup.
- Each router is responsible for its own path operations and dependencies.
- This modular approach enables separation of concerns and easier scaling.

---

## Primary Sources

- [backend/app/main.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/main.py) (Last modified: 2025-08-04 19:08)
- [backend/app/routers/auth.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/auth.py) (Last modified: 2025-08-04 19:08)
- [backend/app/routers/users.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/users.py) (Last modified: 2025-08-04 19:08)
- [backend/app/routers/families.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/families.py) (Last modified: 2025-08-04 19:08)
- [backend/app/routers/calendars.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/calendars.py) (Last modified: 2025-08-04 19:08)
- [backend/app/routers/chores.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/chores.py) (Last modified: 2025-08-04 19:08)
- [backend/app/routers/points.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/points.py) (Last modified: 2025-08-04 19:08)
- [backend/app/routers/goals.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/goals.py) (Last modified: 2025-08-04 19:08)
- [backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md) (Last modified: 2025-08-04 19:08)