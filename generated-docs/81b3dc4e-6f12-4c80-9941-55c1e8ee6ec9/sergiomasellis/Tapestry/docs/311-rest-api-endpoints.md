# Tapestry REST API Endpoints

| Repo      | Doc Type         | Date                | Branch |
|-----------|------------------|---------------------|--------|
| Tapestry  | REST API (311)   | 2025-08-04 19:08    | main   |

---

This document provides an overview of the REST API endpoints exposed by the Tapestry backend. The API is designed to support a family calendar and chore management application, enabling CRUD operations and specialized flows for users, families, events, chores, points, and goals.

Endpoints are implemented in FastAPI and organized by resource in `backend/app/routers/` (see [[backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md)]([backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md)), Last modified: 2025-08-04 19:08).

## Endpoint Overview

| Resource   | Path Prefix         | Main Operations                                                                 |
|------------|---------------------|--------------------------------------------------------------------------------|
| Auth       | `/auth`             | Login, admin login, token management                                            |
| Users      | `/users`            | Create, read, update, delete users                                             |
| Families   | `/families`         | Create family, invite members, list families                                   |
| Calendars  | `/calendars`        | List, add iCal, connect Google/Alexa, sync                                     |
| Chores     | `/chores`           | List, create, update, delete, complete, AI generate                            |
| Points     | `/points`           | List, add points                                                               |
| Goals      | `/goals`            | List, create, update, delete goals                                             |

---

### 1. Auth Endpoints (`/auth`)

| Method | Path                | Purpose                                 | Notes                   |
|--------|---------------------|-----------------------------------------|-------------------------|
| POST   | `/auth/login`       | User login, returns JWT                 |                         |
| POST   | `/auth/admin-login` | Admin login (master password)           |                         |

---

### 2. Users Endpoints (`/users`)

| Method | Path                | Purpose                                 | Notes                   |
|--------|---------------------|-----------------------------------------|-------------------------|
| GET    | `/users/`           | List all users                          |                         |
| POST   | `/users/`           | Create a new user                       |                         |
| GET    | `/users/{user_id}`  | Get user by ID                          |                         |
| PUT    | `/users/{user_id}`  | Update user by ID                       |                         |
| DELETE | `/users/{user_id}`  | Delete user by ID                       |                         |

---

### 3. Families Endpoints (`/families`)

| Method | Path                        | Purpose                                 | Notes                   |
|--------|-----------------------------|-----------------------------------------|-------------------------|
| GET    | `/families/`                | List all families                       |                         |
| POST   | `/families/`                | Create a new family                     |                         |
| POST   | `/families/{id}/invite`     | Invite user to family                   |                         |

---

### 4. Calendars Endpoints (`/calendars`)

| Method | Path                                  | Purpose                                 | Notes                   |
|--------|---------------------------------------|-----------------------------------------|-------------------------|
| GET    | `/calendars/`                         | List calendars for user/family          |                         |
| POST   | `/calendars/ical`                     | Add iCal calendar                       |                         |
| POST   | `/calendars/google`                   | Connect Google Calendar                 |                         |
| POST   | `/calendars/alexa`                    | Connect Alexa Reminders                 |                         |
| POST   | `/calendars/{id}/sync`                | Sync calendar                           |                         |

---

### 5. Chores Endpoints (`/chores`)

| Method | Path                        | Purpose                                 | Notes                   |
|--------|-----------------------------|-----------------------------------------|-------------------------|
| GET    | `/chores/`                  | List chores                             |                         |
| POST   | `/chores/`                  | Create a new chore                      |                         |
| PUT    | `/chores/{id}`              | Update a chore                          |                         |
| DELETE | `/chores/{id}`              | Delete a chore                          |                         |
| POST   | `/chores/{id}/complete`     | Mark chore as complete                  |                         |
| POST   | `/chores/generate`          | Generate chores (AI, LangGraph)         |                         |

---

### 6. Points Endpoints (`/points`)

| Method | Path                        | Purpose                                 | Notes                   |
|--------|-----------------------------|-----------------------------------------|-------------------------|
| GET    | `/points/`                  | List points for user/family             |                         |
| POST   | `/points/`                  | Add points to user                      |                         |

---

### 7. Goals Endpoints (`/goals`)

| Method | Path                        | Purpose                                 | Notes                   |
|--------|-----------------------------|-----------------------------------------|-------------------------|
| GET    | `/goals/`                   | List goals                              |                         |
| POST   | `/goals/`                   | Create a new goal                       |                         |
| PUT    | `/goals/{id}`               | Update a goal                           |                         |
| DELETE | `/goals/{id}`               | Delete a goal                           |                         |

---

## Endpoint Relationships

```mermaid
flowchart TD
    subgraph Auth
        A1[POST /auth/login]
        A2[POST /auth/admin-login]
    end
    subgraph Users
        U1[GET/POST /users/]
        U2[GET/PUT/DELETE /users/{user_id}]
    end
    subgraph Families
        F1[GET/POST /families/]
        F2[POST /families/{id}/invite]
    end
    subgraph Calendars
        C1[GET /calendars/]
        C2[POST /calendars/ical]
        C3[POST /calendars/google]
        C4[POST /calendars/alexa]
        C5[POST /calendars/{id}/sync]
    end
    subgraph Chores
        H1[GET/POST /chores/]
        H2[PUT/DELETE /chores/{id}]
        H3[POST /chores/{id}/complete]
        H4[POST /chores/generate]
    end
    subgraph Points
        P1[GET/POST /points/]
    end
    subgraph Goals
        G1[GET/POST /goals/]
        G2[PUT/DELETE /goals/{id}]
    end

    A1 --> U1
    U1 --> F1
    F1 --> C1
    F1 --> H1
    H1 --> P1
    H1 --> G1
    H4 --> H1
    C2 --> C1
    C3 --> C1
    C4 --> C1
    C5 --> C1
```

---

## Usage Notes

- All endpoints are prefixed with `/api` in deployment (e.g., `/api/users/`).
- Authentication is required for most endpoints except login.
- The `/chores/generate` endpoint leverages AI (LangGraph) for chore suggestions.
- Calendar endpoints support integration with external services (Google, Alexa, iCal).

---

## Primary Sources

- [[backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md)]([backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md)) (Last modified: 2025-08-04 19:08)
- [[README.md](https://github.com/sergiomasellis/Tapestry/blob/main/README.md)]([README.md](https://github.com/sergiomasellis/Tapestry/blob/main/README.md)) (Last modified: 2025-08-04 19:08)
- [backend/app/routers/](backend/app/routers/) (see file names and structure)
- [backend/pyproject.toml](backend/pyproject.toml) (Last modified: 2025-08-04 19:08)
