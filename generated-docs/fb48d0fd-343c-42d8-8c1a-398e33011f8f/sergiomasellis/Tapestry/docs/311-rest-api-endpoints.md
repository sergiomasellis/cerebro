# Tapestry REST API Overview

| Repo    | Doc Type        | Date                | Branch |
|---------|----------------|---------------------|--------|
| Tapestry| API Reference  | 2025-08-04 19:08    | main   |

## Introduction

Tapestry provides a modern, family-oriented calendar and chore management system. Its backend exposes a comprehensive REST API for managing users, families, events, chores, points, and goals. This document summarizes the available endpoints, their organization, and the architectural flow of the API.

## API Structure

The backend is implemented using FastAPI and SQLAlchemy, with routers organized by resource type. Each router handles a specific domain, such as users, families, chores, etc.

**Key API resources:**
- Users: CRUD operations for user accounts.
- Families: Family group creation and invitations.
- Auth: Login and admin login.
- Calendars: Calendar integration and synchronization.
- Chores: Chore management, completion, and AI-powered generation.
- Points: Tracking and awarding points.
- Goals: Setting and tracking goals.

## Endpoint Organization

Routers are located in `backend/app/routers/`:

```
backend/app/routers/
  users.py
  families.py
  events.py
  chores.py
  points.py
  goals.py
  calendars.py
  auth.py
```

Each router defines endpoints following RESTful conventions. For example, `users.py` exposes `/users` endpoints, and `chores.py` exposes `/chores`.

### Example: Users Router

```python
# [backend/app/routers/users.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/users.py)
from fastapi import APIRouter

router = APIRouter()

@router.get("/users")
def list_users():
    # Return a list of users
    pass

@router.post("/users")
def create_user(user: UserCreate):
    # Create a new user
    pass
```

### Example: Chores Router

```python
# [backend/app/routers/chores.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/chores.py)
from fastapi import APIRouter

router = APIRouter()

@router.get("/chores")
def list_chores():
    # Return all chores
    pass

@router.post("/chores")
def create_chore(chore: ChoreCreate):
    # Add a new chore
    pass

@router.post("/chores/generate")
def generate_chores():
    # AI-powered chore generation
    pass
```

### Example: Points Router

```python
# [backend/app/routers/points.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/points.py)
from fastapi import APIRouter

router = APIRouter()

@router.get("/points")
def list_points():
    # List points for users/families
    pass

@router.post("/points")
def add_points(points: PointsCreate):
    # Add points to a user
    pass
```

## API Usage Flow

Below is a high-level diagram of how clients interact with the Tapestry REST API:

```mermaid
flowchart TD
    A[Client (Web/Mobile)] -->|HTTP (JSON)| B[FastAPI Backend]
    B --> C1[Users Router]
    B --> C2[Families Router]
    B --> C3[Events Router]
    B --> C4[Chores Router]
    B --> C5[Points Router]
    B --> C6[Goals Router]
    B --> C7[Calendars Router]
    B --> C8[Auth Router]
    C4 --> D[AI Chore Generation (LangGraph)]
    B --> E[SQLite Database (via SQLAlchemy)]
```

**Legend:**
- Each router handles a resource domain.
- Chore generation leverages AI via LangGraph.
- All data is persisted in SQLite (development).

## Example API Calls

- **List all users:** `GET /users`
- **Create a new family:** `POST /families`
- **Add a new event:** `POST /events`
- **Complete a chore:** `POST /chores/{chore_id}/complete`
- **Award points:** `POST /points`
- **Set a goal:** `POST /goals`

## Authentication

Authentication endpoints are provided in `auth.py`, supporting both standard and admin logins. Tokens are used for securing API access.

```python
# [backend/app/routers/auth.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/auth.py)
@router.post("/auth/login")
def login(credentials: LoginRequest):
    # Authenticate user and return token
    pass

@router.post("/auth/admin-login")
def admin_login(credentials: AdminLoginRequest):
    # Authenticate admin with master password
    pass
```

## Primary Sources

- [README.md](https://github.com/sergiomasellis/Tapestry/blob/main/README.md) (Last modified: 2025-08-04 19:08)
- [backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md) (Last modified: 2025-08-04 19:08)
- [backend/app/routers/users.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/users.py) (see project for details)
- [backend/app/routers/chores.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/chores.py) (see project for details)
- [backend/app/routers/points.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/points.py) (see project for details)
- [backend/app/routers/auth.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/auth.py) (see project for details)
- backend/pyproject.toml (Last modified: 2025-08-04 19:08)