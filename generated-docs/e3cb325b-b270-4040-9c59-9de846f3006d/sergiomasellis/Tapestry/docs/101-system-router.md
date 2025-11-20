# Tapestry System Router 101

| Repo    | Doc Type         | Date                | Branch |
|---------|------------------|---------------------|--------|
| Tapestry | System Router 101 | 2025-08-04 19:08    | main   |

## Overview

This document describes the system routing and entrypoints for the Tapestry backend, focusing on how HTTP requests are routed to the appropriate business logic. The backend is built with FastAPI and organizes its API endpoints using modular routers, each responsible for a distinct domain (users, families, chores, etc.).

## Entrypoint

- **Primary Entrypoint:**  
  `[backend/app/main.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/main.py)` (Last modified: 2025-08-04 19:08)  
  This file creates the FastAPI application instance and includes all API routers.

## Router Structure

Routers are defined in the `backend/app/routers/` directory (Last modified: 2025-08-04 19:08). Each file corresponds to a logical domain:

- `users.py` – User management (CRUD)
- `auth.py` – Authentication (login, admin-login)
- `families.py` – Family group management
- `calendars.py` – Calendar integrations (iCal, Google, Alexa)
- `chores.py` – Chore management and AI-powered chore generation
- `points.py` – Points tracking
- `goals.py` – Goal setting and tracking

Each router defines a set of endpoints (e.g., `/users/`, `/auth/`, etc.) and is included in the main FastAPI app.

## Routing Logic

1. **Request Reception:**  
   All HTTP requests are received by the FastAPI app instance in `[backend/app/main.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/main.py)`.

2. **Router Inclusion:**  
   The main app includes routers from `app/routers/` using FastAPI's `include_router` method. Each router is mounted at a specific path prefix (e.g., `/users`, `/chores`).

3. **Endpoint Dispatch:**  
   FastAPI matches the incoming request path and HTTP method to the appropriate route handler defined in the router modules.

4. **Dependency Injection:**  
   Routers can declare dependencies (e.g., authentication, DB session) that are automatically resolved by FastAPI.

5. **Response:**  
   The route handler processes the request, interacts with the database or other services as needed, and returns a response (typically JSON).

## Example: Router Inclusion (Pseudocode)

```python
# [backend/app/main.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/main.py)

from fastapi import FastAPI
from app.routers import users, auth, families, calendars, chores, points, goals

app = FastAPI()

app.include_router(users.router, prefix="/users")
app.include_router(auth.router, prefix="/auth")
app.include_router(families.router, prefix="/families")
app.include_router(calendars.router, prefix="/calendars")
app.include_router(chores.router, prefix="/chores")
app.include_router(points.router, prefix="/points")
app.include_router(goals.router, prefix="/goals")
```

## Routing Topology (Mermaid Diagram)

```mermaid
graph TD
    A[FastAPI App<br>[backend/app/main.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/main.py)] --> B1[/users<br>routers/users.py/]
    A --> B2[/auth<br>routers/auth.py/]
    A --> B3[/families<br>routers/families.py/]
    A --> B4[/calendars<br>routers/calendars.py/]
    A --> B5[/chores<br>routers/chores.py/]
    A --> B6[/points<br>routers/points.py/]
    A --> B7[/goals<br>routers/goals.py/]
```

## Path Prefixes and Responsibilities

| Prefix      | Router File                | Responsibility                  |
|-------------|---------------------------|---------------------------------|
| `/users`    | routers/users.py          | User CRUD                       |
| `/auth`     | routers/auth.py           | Authentication                  |
| `/families` | routers/families.py       | Family group management         |
| `/calendars`| routers/calendars.py      | Calendar integrations           |
| `/chores`   | routers/chores.py         | Chore management & AI pipeline  |
| `/points`   | routers/points.py         | Points tracking                 |
| `/goals`    | routers/goals.py          | Goal setting & tracking         |

## Notes

- All routers are included in the main app at startup.
- Each router can define its own dependencies and error handling.
- The modular router structure enables clear separation of concerns and easy extensibility.

---

## Primary Sources

- [backend/app/main.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/main.py) (Last modified: 2025-08-04 19:08)
- [backend/app/routers/users.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/users.py) (Last modified: 2025-08-04 19:08)
- [backend/app/routers/auth.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/auth.py) (Last modified: 2025-08-04 19:08)
- [backend/app/routers/families.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/families.py) (Last modified: 2025-08-04 19:08)
- [backend/app/routers/calendars.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/calendars.py) (Last modified: 2025-08-04 19:08)
- [backend/app/routers/chores.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/chores.py) (Last modified: 2025-08-04 19:08)
- [backend/app/routers/points.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/points.py) (Last modified: 2025-08-04 19:08)
- [backend/app/routers/goals.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/goals.py) (Last modified: 2025-08-04 19:08)
- [backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md) (Last modified: 2025-08-04 19:08)