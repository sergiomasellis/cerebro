# Tapestry REST API Endpoints

| Repo      | Doc Type         | Date                | Branch |
|-----------|------------------|---------------------|--------|
| Tapestry  | REST API (311)   | 2025-08-04 19:08    | main   |

## Overview

Tapestry exposes a RESTful API for managing users, families, events, chores, points, goals, and authentication. The backend is implemented in FastAPI, with routers organized by domain in `backend/app/routers/`. The API is designed for use by the Next.js frontend and supports CRUD operations, authentication, and integrations (e.g., Google Calendar, Alexa).

_Last modified dates for referenced files are included per file header._

---

## Endpoint Table

| Domain      | Router File (Last Modified)         | Path Prefix      | Methods & Main Endpoints                                                                                 | Purpose / Notes                                                                                 |
|-------------|-------------------------------------|------------------|----------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------|
| Auth        | app/routers/auth.py (2025-08-04)    | /auth            | POST /login<br>POST /admin-login                                                                         | User and admin authentication, token issuance                                                   |
| Users       | app/routers/users.py (2025-08-04)   | /users           | GET /users<br>POST /users<br>GET /users/{id}<br>PUT /users/{id}<br>DELETE /users/{id}                    | User CRUD                                                                                       |
| Families    | app/routers/families.py (2025-08-04)| /families        | POST /families<br>POST /families/invite<br>GET /families/{id}                                            | Family group creation, invitation, retrieval                                                    |
| Calendars   | app/routers/calendars.py (2025-08-04)| /calendars      | GET /calendars<br>POST /calendars/ical<br>POST /calendars/google<br>POST /calendars/alexa<br>POST /calendars/sync | List, add iCal, connect Google/Alexa, sync calendars                                            |
| Chores      | app/routers/chores.py (2025-08-04)  | /chores          | GET /chores<br>POST /chores<br>PUT /chores/{id}<br>DELETE /chores/{id}<br>POST /chores/{id}/complete<br>POST /chores/generate | Chore CRUD, completion, AI-based generation (LangGraph)                                         |
| Points      | app/routers/points.py (2025-08-04)  | /points          | GET /points<br>POST /points                                                                              | List and add points (for chores, leaderboard)                                                   |
| Goals       | app/routers/goals.py (2025-08-04)   | /goals           | GET /goals<br>POST /goals<br>PUT /goals/{id}<br>DELETE /goals/{id}                                       | Goal CRUD                                                                                       |

---

## Endpoint Details

### Auth

- **POST /auth/login**: Authenticate user, returns JWT or session token.
- **POST /auth/admin-login**: Authenticate admin (master password), returns admin token.

### Users

- **GET /users**: List all users.
- **POST /users**: Create a new user.
- **GET /users/{id}**: Retrieve user by ID.
- **PUT /users/{id}**: Update user details.
- **DELETE /users/{id}**: Remove user.

### Families

- **POST /families**: Create a new family group.
- **POST /families/invite**: Invite a user to a family.
- **GET /families/{id}**: Get family details.

### Calendars

- **GET /calendars**: List all calendars for the user/family.
- **POST /calendars/ical**: Add an iCal calendar.
- **POST /calendars/google**: Connect Google Calendar.
- **POST /calendars/alexa**: Connect Alexa Reminders.
- **POST /calendars/sync**: Sync all connected calendars.

### Chores

- **GET /chores**: List chores (optionally filtered by user/family).
- **POST /chores**: Create a new chore.
- **PUT /chores/{id}**: Update a chore.
- **DELETE /chores/{id}**: Delete a chore.
- **POST /chores/{id}/complete**: Mark a chore as completed (awards points).
- **POST /chores/generate**: Generate chores using AI pipeline (LangGraph).

### Points

- **GET /points**: List points for users/family (for leaderboard).
- **POST /points**: Add points (e.g., for manual adjustment or admin).

### Goals

- **GET /goals**: List all goals.
- **POST /goals**: Create a new goal.
- **PUT /goals/{id}**: Update a goal.
- **DELETE /goals/{id}**: Delete a goal.

---

## REST API Topology (Mermaid Diagram)

```mermaid
graph TD
    subgraph Auth
        A1[POST /auth/login]
        A2[POST /auth/admin-login]
    end
    subgraph Users
        U1[GET /users]
        U2[POST /users]
        U3[GET /users/{id}]
        U4[PUT /users/{id}]
        U5[DELETE /users/{id}]
    end
    subgraph Families
        F1[POST /families]
        F2[POST /families/invite]
        F3[GET /families/{id}]
    end
    subgraph Calendars
        C1[GET /calendars]
        C2[POST /calendars/ical]
        C3[POST /calendars/google]
        C4[POST /calendars/alexa]
        C5[POST /calendars/sync]
    end
    subgraph Chores
        CH1[GET /chores]
        CH2[POST /chores]
        CH3[PUT /chores/{id}]
        CH4[DELETE /chores/{id}]
        CH5[POST /chores/{id}/complete]
        CH6[POST /chores/generate]
    end
    subgraph Points
        P1[GET /points]
        P2[POST /points]
    end
    subgraph Goals
        G1[GET /goals]
        G2[POST /goals]
        G3[PUT /goals/{id}]
        G4[DELETE /goals/{id}]
    end

    A1 --> U1
    U1 --> F1
    F1 --> C1
    C1 --> CH1
    CH1 --> P1
    P1 --> G1
```

---

## Notes

- All endpoints are implemented as FastAPI routers in `backend/app/routers/` (Last modified: 2025-08-04).
- Authentication is required for most endpoints except `/auth/login` and `/auth/admin-login`.
- Chore generation leverages the AI pipeline in `[backend/app/ai/chore_graph.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/ai/chore_graph.py)` (Last modified: 2025-08-04).
- The OpenAPI/Swagger UI is available at `/docs` when the backend is running.

---

## Primary Sources

- [backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md) (Last modified: 2025-08-04 19:08)
- [backend/app/routers/auth.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/auth.py) (Last modified: 2025-08-04 19:08)
- [backend/app/routers/users.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/users.py) (Last modified: 2025-08-04 19:08)
- [backend/app/routers/families.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/families.py) (Last modified: 2025-08-04 19:08)
- [backend/app/routers/calendars.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/calendars.py) (Last modified: 2025-08-04 19:08)
- [backend/app/routers/chores.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/chores.py) (Last modified: 2025-08-04 19:08)
- [backend/app/routers/points.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/points.py) (Last modified: 2025-08-04 19:08)
- [backend/app/routers/goals.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/goals.py) (Last modified: 2025-08-04 19:08)
- [backend/app/ai/chore_graph.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/ai/chore_graph.py) (Last modified: 2025-08-04 19:08)
- [README.md](https://github.com/sergiomasellis/Tapestry/blob/main/README.md) (Last modified: 2025-08-04 19:08)