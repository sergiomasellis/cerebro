# Authentication Model

| Repo     | Doc Type            | Date                | Branch |
|----------|---------------------|---------------------|--------|
| Tapestry | Authentication (701) | 2025-08-04 19:08    | main   |

## Overview

Tapestry uses a token-based authentication model for its backend API, implemented in FastAPI. The authentication logic is primarily handled in `[backend/app/routers/auth.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/auth.py)` (see file structure and [backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md), last modified: 2025-08-04 19:08). The system supports standard user login as well as an "admin-login" route with a master password. Authentication is required for most API endpoints related to user, family, calendar, chore, point, and goal management.

## Mechanisms

### 1. Token-Based Authentication

- **JWT Tokens**: Upon successful login, the backend issues a JWT (JSON Web Token) to the client. This token must be included in the `Authorization` header (as `Bearer <token>`) for subsequent requests.
- **Token Expiry**: The token's lifetime is controlled by the `ACCESS_TOKEN_EXPIRE_MINUTES` environment variable (see [backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md), last modified: 2025-08-04 19:08).
- **Secret Key**: Tokens are signed using the `SECRET_KEY` from environment variables.

### 2. Login Flows

- **Standard Login**: Users authenticate using their username/email and password. On success, a JWT is returned.
- **Admin Login**: There is a special admin login route that accepts a master password (see [backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md), last modified: 2025-08-04 19:08). This is intended for administrative or emergency access.

### 3. Permissions Model

- **User Roles**: The system distinguishes between regular users and admin users (via the admin-login route).
- **Family Context**: Most resources (chores, points, goals, calendars) are scoped to a family group. Users must belong to a family to access or modify these resources.
- **Route Protection**: All routers for users, families, calendars, chores, points, and goals are protected by dependency injection in FastAPI, requiring a valid JWT for access.

### 4. Environment & Configuration

- **Environment Variables** (see [backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md), last modified: 2025-08-04 19:08):
  - `SECRET_KEY`: Used for signing JWTs.
  - `ACCESS_TOKEN_EXPIRE_MINUTES`: Controls token expiry.
- **Configuration File**: `.env` in the backend directory.

## Authentication Flow

1. **User submits credentials** to `/auth/login` (or `/auth/admin-login` for admin).
2. **Backend verifies credentials** against the database (see [backend/app/models/models.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/models/models.py)).
3. **On success**, backend issues a JWT token with user ID, role, and expiry.
4. **Client stores token** (e.g., in localStorage or memory).
5. **Client includes token** in `Authorization: Bearer <token>` header for all protected API requests.
6. **Backend validates token** on each request, extracting user context and permissions.

## Permissions Table

| Endpoint Group   | Auth Required | Role Required | Notes                                 |
|------------------|--------------|---------------|---------------------------------------|
| /users           | Yes          | User/Admin    | CRUD operations on user profile       |
| /families        | Yes          | User/Admin    | Family creation, invite, join         |
| /calendars       | Yes          | User/Admin    | Calendar sync, iCal, Google, Alexa    |
| /chores          | Yes          | User/Admin    | Chore CRUD, completion, AI generation |
| /points          | Yes          | User/Admin    | Point tracking                        |
| /goals           | Yes          | User/Admin    | Goal management                       |
| /auth/login      | No           | -             | Issues JWT on success                 |
| /auth/admin-login| No           | -             | Issues admin JWT on success           |

## Security Considerations

- **Password Storage**: Passwords are stored securely (details in [backend/app/models/models.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/models/models.py), not shown here).
- **Token Expiry**: Short-lived tokens reduce risk of token theft.
- **Master Password**: The admin-login route should be protected and the master password rotated regularly.
- **No OAuth**: As of this version, there is no OAuth or third-party login (see [backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md), last modified: 2025-08-04 19:08).

## Example: FastAPI Dependency Injection for Auth

All protected routers use FastAPI's dependency injection to require authentication, e.g.:

```
@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    ...
```

Here, `get_current_user` validates the JWT and loads the user context.

---

## Primary Sources

- [backend/app/routers/auth.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/auth.py) (see file structure; last modified: not specified, but present as of 2025-08-04 19:08)
- [backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md) (Last modified: 2025-08-04 19:08)
- [backend/app/models/models.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/models/models.py) (see file structure)
- [backend/app/main.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/main.py) (see file structure)
- .env.example (see [backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md) for variable descriptions)
- [TAPESTRY_PRD_AND_SYSTEM_DESIGN.md](https://github.com/sergiomasellis/Tapestry/blob/main/TAPESTRY_PRD_AND_SYSTEM_DESIGN.md) (see file structure)