# Tapestry System Router 101

| Repo     | Doc Type         | Date                | Branch |
|----------|------------------|---------------------|--------|
| Tapestry | System Router 101| 2025-08-04 19:08    | main   |

---

## Overview

Tapestry is a modern, multi-user family calendar and chore tracking application. Its architecture is split into a Next.js frontend and a FastAPI backend. Both layers implement routing logic to manage navigation and API endpoints, respectively.

This document explains the routing systems for both the frontend and backend, detailing how requests are handled, routed, and dispatched to the appropriate handlers.

---

## 1. Frontend Routing (Next.js)

**Location:** `frontend/src/app/`  
**Relevant files:**  
- `frontend/src/app/page.tsx` (Last modified: 2025-08-04 19:08)  
- `frontend/src/app/layout.tsx` (Last modified: 2025-08-04 19:08)

### Routing Model

Tapestry uses the [Next.js App Router](https://nextjs.org/docs/app/building-your-application/routing) (introduced in Next.js 13+) which is filesystem-based. Each file or folder under `frontend/src/app/` represents a route or layout.

- `page.tsx`: Defines the component rendered for the root route (`/`).
- `layout.tsx`: Defines the layout (shared UI, e.g., navigation) for all nested routes.
- Additional folders/files under `app/` (e.g., `app/calendar/page.tsx`) would define further routes like `/calendar`.

### Routing Flow

1. **User navigates to a URL** (e.g., `/`, `/calendar`).
2. **Next.js matches the path** to a file in `src/app/`.
3. **Layout(s) are composed** (from `layout.tsx` files up the tree).
4. **Page component is rendered** for the matched route.

**Example:**
- `/` → `src/app/page.tsx`
- `/calendar` → `src/app/calendar/page.tsx` (if exists)

---

## 2. Backend Routing (FastAPI)

**Location:** `backend/app/routers/`  
**Relevant files:**  
- `[backend/app/main.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/main.py)` (Last modified: 2025-08-04 19:08)  
- `backend/app/routers/*.py` (Last modified: 2025-08-04 19:08)

### Routing Model

Tapestry's backend uses FastAPI's router system. Each domain (users, chores, points, etc.) has its own router module under `app/routers/`.

- `main.py` creates the FastAPI app and includes all routers.
- Each router file (e.g., `users.py`, `chores.py`) defines endpoints for its resource.

**Router files:**
- `users.py` → `/users`
- `auth.py` → `/auth`
- `families.py` → `/families`
- `calendars.py` → `/calendars`
- `chores.py` → `/chores`
- `points.py` → `/points`
- `goals.py` → `/goals`

### Routing Flow

1. **HTTP request arrives** at the FastAPI server.
2. **FastAPI matches the path and method** to a route in the included routers.
3. **The corresponding handler function** is invoked.
4. **Response is returned** (JSON, error, etc.).

**Example:**
- `GET /users/` → `users.py` router, `list_users` handler
- `POST /chores/` → `chores.py` router, `create_chore` handler

---

## 3. Router Topology Diagram

```mermaid
flowchart TD
    subgraph Frontend (Next.js)
        F1["/ (app/page.tsx)"]
        F2["/calendar (app/calendar/page.tsx)"]
        F3["/chores (app/chores/page.tsx)"]
        F4["/goals (app/goals/page.tsx)"]
    end

    subgraph Backend (FastAPI)
        B1["/users (routers/users.py)"]
        B2["/auth (routers/auth.py)"]
        B3["/families (routers/families.py)"]
        B4["/calendars (routers/calendars.py)"]
        B5["/chores (routers/chores.py)"]
        B6["/points (routers/points.py)"]
        B7["/goals (routers/goals.py)"]
    end

    F1 --"API calls"--> B1
    F1 --"API calls"--> B2
    F2 --"API calls"--> B4
    F3 --"API calls"--> B5
    F3 --"API calls"--> B6
    F4 --"API calls"--> B7
```

---

## 4. Routing Style & Best Practices

- **Frontend:**  
  - Use the filesystem-based router for all navigation.
  - Place new pages under `src/app/` as needed.
  - Use layouts for shared UI (navigation, headers).
  - For API calls, use `fetch` or a client library to communicate with the backend.

- **Backend:**  
  - Add new routers in `app/routers/` for new resources.
  - Register routers in `app/main.py` using `app.include_router`.
  - Use path parameters and query parameters as appropriate for RESTful design.

---

## 5. Summary Table

| Layer    | Router Type       | Entry Point                       | Route Files/Dirs                  | Example Route      |
|----------|-------------------|-----------------------------------|-----------------------------------|--------------------|
| Frontend | Next.js App Router| `frontend/src/app/`               | `page.tsx`, `[route]/page.tsx`    | `/calendar`        |
| Backend  | FastAPI Routers   | `[backend/app/main.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/main.py)`             | `routers/*.py`                    | `/chores/`         |

---

## Primary Sources

- [`[README.md](https://github.com/sergiomasellis/Tapestry/blob/main/README.md)`](./[README.md](https://github.com/sergiomasellis/Tapestry/blob/main/README.md)) (Last modified: 2025-08-04 19:08)
- [`[frontend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/README.md)`](./[frontend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/README.md)) (Last modified: 2025-08-04 19:08)
- [`[backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md)`](./[backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md)) (Last modified: 2025-08-04 19:08)
- [`frontend/src/app/page.tsx`](./frontend/src/app/page.tsx) (Last modified: 2025-08-04 19:08)
- [`frontend/src/app/layout.tsx`](./frontend/src/app/layout.tsx) (Last modified: 2025-08-04 19:08)
- [`[backend/app/main.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/main.py)`](./[backend/app/main.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/main.py)) (Last modified: 2025-08-04 19:08)
- [`backend/app/routers/`](./backend/app/routers/) (Last modified: 2025-08-04 19:08)