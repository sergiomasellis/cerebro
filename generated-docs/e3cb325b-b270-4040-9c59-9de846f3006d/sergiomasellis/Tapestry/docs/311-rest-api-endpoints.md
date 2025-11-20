# Tapestry REST API Endpoints

| Repo     | Doc Type         | Date                | Branch |
|----------|------------------|---------------------|--------|
| Tapestry | REST API (311)   | 2025-08-04 19:08    | main   |

## Overview

The Tapestry backend exposes a RESTful API for managing users, families, events, chores, points, and goals. The API is implemented using FastAPI and organized into modular routers, each handling a specific domain. This document summarizes the available endpoints, their purposes, and semantics, as described in the project documentation and backend code structure.

---

## Endpoint Table

| Resource   | Router File (Last Modified)         | Example Endpoints (RESTful)                       | Purpose / Semantics                                                                                 |
|------------|-------------------------------------|---------------------------------------------------|-----------------------------------------------------------------------------------------------------|
| Users      | [backend/app/routers/users.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/users.py)        | `GET /users`, `POST /users`, `GET /users/{id}`    | CRUD operations for user accounts (create, read, update, delete).                                   |
| Families   | [backend/app/routers/families.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/families.py)     | `POST /families`, `POST /families/invite`         | Create family groups, invite members, manage family membership.                                     |
| Auth       | [backend/app/routers/auth.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/auth.py)         | `POST /auth/login`, `POST /auth/admin-login`      | User authentication (login), admin/master password login.                                           |
| Calendars  | [backend/app/routers/calendars.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/calendars.py)    | `GET /calendars`, `POST /calendars/ical`          | List calendars, add iCal feeds, connect/sync with Google or Alexa calendars.                        |
| Chores     | [backend/app/routers/chores.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/chores.py)       | `GET /chores`, `POST /chores`, `PUT /chores/{id}` | List, create, update, delete chores; mark as complete; generate chores via AI (LangGraph pipeline). |
| Points     | [backend/app/routers/points.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/points.py)       | `GET /points`, `POST /points`                     | List and add points for users (chore completion, rewards, etc.).                                    |
| Goals      | [backend/app/routers/goals.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/goals.py)        | `GET /goals`, `POST /goals`, `PUT /goals/{id}`    | List, create, update, and delete goals (prizes, achievements, etc.).                                |

**Note:** All endpoint paths are prefixed by the FastAPI application root (typically `/`), and may require authentication (see [backend/app/routers/auth.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/auth.py)).

---

## Endpoint Details

### Users

- **GET /users**: List all users.
- **POST /users**: Create a new user.
- **GET /users/{id}**: Retrieve a user by ID.
- **PUT /users/{id}**: Update user details.
- **DELETE /users/{id}**: Delete a user.

### Families

- **POST /families**: Create a new family group.
- **POST /families/invite**: Invite a user to a family.
- **GET /families/{id}**: Get family details.
- **PUT /families/{id}**: Update family info.
- **DELETE /families/{id}**: Remove a family.

### Auth

- **POST /auth/login**: User login (returns JWT or session).
- **POST /auth/admin-login**: Admin/master password login.

### Calendars

- **GET /calendars**: List all calendars for the user/family.
- **POST /calendars/ical**: Add an iCal feed.
- **POST /calendars/google**: Connect Google Calendar.
- **POST /calendars/alexa**: Connect Alexa Reminders.
- **POST /calendars/sync**: Trigger calendar sync.

### Chores

- **GET /chores**: List chores (optionally filter by user/family/date).
- **POST /chores**: Create a new chore.
- **PUT /chores/{id}**: Update a chore.
- **DELETE /chores/{id}**: Delete a chore.
- **POST /chores/{id}/complete**: Mark a chore as complete.
- **POST /chores/generate**: Generate chores using AI (LangGraph).

### Points

- **GET /points**: List points for users/family.
- **POST /points**: Add points (e.g., for chore completion).

### Goals

- **GET /goals**: List all goals.
- **POST /goals**: Create a new goal.
- **PUT /goals/{id}**: Update a goal.
- **DELETE /goals/{id}**: Delete a goal.

---

## Endpoint Relationships (Mermaid Diagram)

```mermaid
flowchart TD
    subgraph Users & Auth
        A[User] -- login --> B(Auth)
        A -- belongs to --> C(Family)
    end

    subgraph Family
        C -- has --> D[Calendar]
        C -- has --> E[Chore]
        C -- has --> F[Goal]
        C -- has --> G[Points]
    end

    D -- syncs with --> H[External Calendars]
    E -- completion --> G
    E -- generated by --> I[AI (LangGraph)]
    G -- leaderboard --> A
    F -- rewards --> A
```

---

## Notes

- All endpoints are implemented using FastAPI routers in backend/app/routers/.
- Data validation and serialization are handled via Pydantic models ([backend/app/schemas/schemas.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/schemas/schemas.py)).
- Authentication is required for most endpoints (see [backend/app/routers/auth.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/auth.py)).
- Chore generation leverages an AI pipeline ([backend/app/ai/chore_graph.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/ai/chore_graph.py)).
- For full OpenAPI/Swagger docs, run the backend and visit `/docs`.

---

## Primary Sources

- [backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md) (Last modified: 2025-08-04 19:08)
- [backend/app/routers/users.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/users.py) (see file for latest modification)
- [backend/app/routers/families.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/families.py) (see file for latest modification)
- [backend/app/routers/auth.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/auth.py) (see file for latest modification)
- [backend/app/routers/calendars.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/calendars.py) (see file for latest modification)
- [backend/app/routers/chores.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/chores.py) (see file for latest modification)
- [backend/app/routers/points.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/points.py) (see file for latest modification)
- [backend/app/routers/goals.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/goals.py) (see file for latest modification)
- [backend/app/schemas/schemas.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/schemas/schemas.py) (see file for latest modification)
- [README.md](https://github.com/sergiomasellis/Tapestry/blob/main/README.md) (Last modified: 2025-08-04 19:08)