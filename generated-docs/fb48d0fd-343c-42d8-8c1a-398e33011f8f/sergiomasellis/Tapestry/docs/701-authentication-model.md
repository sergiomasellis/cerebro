# Tapestry Authentication Overview

| Repo     | Doc Type   | Date                | Branch |
|----------|------------|---------------------|--------|
| Tapestry | Reference  | 2025-08-04 19:08    | main   |

## Introduction

Authentication is a core requirement for Tapestry, as it is a multi-user family calendar and chore management application. The backend includes a dedicated `auth.py` router, and user management is a documented feature. This document provides an overview of the authentication system, its structure, and its integration points within the Tapestry project.

## Authentication Architecture

Tapestry uses a FastAPI backend with a modular router structure. Authentication endpoints are implemented in `[backend/app/routers/auth.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/auth.py)` (see file structure and [backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md), last modified: 2025-08-04 19:08). The authentication system is responsible for:

- User login (with password)
- Admin login (with master password)
- Token issuance (likely JWT)
- Securing endpoints for user and family data

### Key Components

- **FastAPI**: Provides the HTTP API and dependency injection for authentication.
- **Pydantic**: Defines schemas for login requests and token responses.
- **SQLAlchemy**: Manages user data persistence.
- **Environment Variables**: Store secrets and token expiry settings.

### Authentication Flow

The typical authentication flow is as follows:

1. **User submits credentials** to the `/auth/login` endpoint.
2. **Credentials are validated** against the database.
3. **Access token is generated** (e.g., JWT) and returned.
4. **Token is used** in subsequent requests for protected endpoints.

#### Example: FastAPI Router Inclusion

From `[backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md)` (last modified: 2025-08-04 19:08):

```
- app/
  - main.py (FastAPI app, router includes)
  - routers/
    - auth.py, users.py, ...
```

This indicates that `auth.py` is included in the main FastAPI app, registering authentication endpoints.

#### Example: Environment Variables

From `[backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md)` (last modified: 2025-08-04 19:08):

```
- .env
  DATABASE_URL=sqlite:///./data.db
  SECRET_KEY=dev-secret-change
  ACCESS_TOKEN_EXPIRE_MINUTES=60
```

These variables are used for token signing and expiry.

#### Example: Dependency Installation

From `backend/pyproject.toml` (last modified: 2025-08-04 19:08):

```toml
dependencies = [
    "fastapi>=0.116.1",
    "pydantic[email]>=2.11.7",
    "sqlalchemy>=2.0.42",
    "python-dotenv>=1.1.1",
    "uvicorn>=0.35.0",
]
```

These dependencies enable authentication, schema validation, and secure environment management.

### Code Snippet: FastAPI Auth Router (Typical Structure)

While the actual code for `auth.py` is not shown, a typical FastAPI authentication router would look like:

```python
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(request: LoginRequest):
    # Validate credentials, generate token
    ...
```

### Frontend Integration

The frontend (Next.js, see [frontend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/README.md), last modified: 2025-08-04 19:08) is expected to:

- Collect user credentials via a login form
- Send a POST request to `/auth/login`
- Store the returned token (e.g., in localStorage or cookies)
- Attach the token to subsequent API requests

#### Example: Frontend API Call (Pseudo-code)

```typescript
async function login(username: string, password: string) {
  const res = await fetch('/api/auth/login', {
    method: 'POST',
    body: JSON.stringify({ username, password }),
    headers: { 'Content-Type': 'application/json' }
  });
  const data = await res.json();
  // Save data.token for future requests
}
```

## Authentication System Diagram

```mermaid
flowchart TD
    A[User] -->|Login Request| B[FastAPI /auth/login]
    B -->|Validate Credentials| C[Database (SQLAlchemy)]
    C -->|Valid| D[Generate Token]
    D -->|Return Token| A
    A -->|Authenticated Request (with Token)| E[Protected Endpoint]
    E -->|Verify Token| D
```

## Security Considerations

- **Secret keys** must be kept secure and not committed to source control.
- **Token expiry** should be set appropriately (see `ACCESS_TOKEN_EXPIRE_MINUTES`).
- **Password storage** should use secure hashing (e.g., bcrypt).
- **HTTPS** is required in production for secure token transmission.

## Primary Sources

- [backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md) (Last modified: 2025-08-04 19:08)
- backend/pyproject.toml (Last modified: 2025-08-04 19:08)
- [frontend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/README.md) (Last modified: 2025-08-04 19:08)
- [frontend/package.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/package.json) (Last modified: 2025-08-04 19:08)
- Project file structure and router organization