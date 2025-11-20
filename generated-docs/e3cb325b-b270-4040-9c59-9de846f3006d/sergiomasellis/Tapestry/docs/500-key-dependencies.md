# Key Dependencies

| Repo     | Doc Type            | Date                | Branch |
|----------|---------------------|---------------------|--------|
| Tapestry | Key Dependencies    | 2025-08-04 19:08    | main   |

This document outlines the critical dependencies for both the backend and frontend of the Tapestry application. It covers internal services, core libraries, and third-party APIs or frameworks that are essential for development, runtime, and deployment.

---

## Overview

Tapestry is a modern, multi-user family calendar and chore management application. It is architected as a full-stack project with a FastAPI/SQLAlchemy backend and a Next.js/TypeScript frontend. The following sections detail the major dependencies for each part of the system.

---

## Backend Dependencies

**Location:** backend/  
**Reference:** backend/pyproject.toml (Last modified: 2025-08-04 19:08), [backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md) (Last modified: 2025-08-04 19:08)

### Core Libraries

- **FastAPI**  
  - Purpose: High-performance Python web framework for building RESTful APIs.
  - Usage: Main API server, routing, dependency injection, OpenAPI docs.
  - Version: >=0.116.1

- **SQLAlchemy**  
  - Purpose: Python SQL toolkit and ORM.
  - Usage: Database models, schema management, query abstraction.
  - Version: >=2.0.42

- **SQLite**  
  - Purpose: Lightweight, file-based SQL database.
  - Usage: Default development database (DATABASE_URL=sqlite:///./data.db).
  - Note: Production deployments should consider PostgreSQL or similar.

- **Pydantic v2**  
  - Purpose: Data validation and settings management using Python type annotations.
  - Usage: API request/response schemas.
  - Version: >=2.11.7

- **LangGraph**  
  - Purpose: AI workflow orchestration.
  - Usage: Chore generation and point assignment pipeline (see [backend/app/ai/chore_graph.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/ai/chore_graph.py)).
  - Version: >=0.6.3

- **python-dotenv**  
  - Purpose: Loads environment variables from .env files.
  - Usage: Configuration management (secrets, DB URL, etc.).
  - Version: >=1.1.1

- **uvicorn**  
  - Purpose: ASGI server for FastAPI.
  - Usage: Local and production server runtime.
  - Version: >=0.35.0

- **typing-extensions**  
  - Purpose: Backports and enhancements for Python typing.
  - Usage: Type hints and compatibility.
  - Version: >=4.14.1

#### Dev Tools

- **uv**  
  - Purpose: Python project and environment manager.
  - Usage: Dependency management, virtualenvs.
- **ruff**  
  - Purpose: Linter for Python code.
  - Usage: Code quality enforcement.

---

## Frontend Dependencies

**Location:** frontend/  
**Reference:** [frontend/package.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/package.json) (Last modified: 2025-08-04 19:08), [frontend/tsconfig.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/tsconfig.json) (Last modified: 2025-08-04 19:08)

### Core Frameworks

- **Next.js**  
  - Purpose: React-based web framework for SSR, routing, and API routes.
  - Usage: Main frontend application.
  - Version: 15.4.5

- **React**  
  - Purpose: UI library for building component-based interfaces.
  - Usage: Core UI rendering.
  - Version: 19.1.0

- **TypeScript**  
  - Purpose: Typed superset of JavaScript.
  - Usage: Type safety and developer tooling.
  - Version: ^5

### Styling & UI Libraries

- **Tailwind CSS**  
  - Purpose: Utility-first CSS framework.
  - Usage: Styling components.
  - Version: ^4

- **Radix UI**  
  - Purpose: Accessible, unstyled UI primitives for React.
  - Usage: Dialogs, dropdowns, navigation, popovers, tabs, tooltips, etc.
  - Packages:
    - @radix-ui/react-avatar
    - @radix-ui/react-dialog
    - @radix-ui/react-dropdown-menu
    - @radix-ui/react-navigation-menu
    - @radix-ui/react-popover
    - @radix-ui/react-select
    - @radix-ui/react-separator
    - @radix-ui/react-slot
    - @radix-ui/react-tabs
    - @radix-ui/react-tooltip

- **class-variance-authority**  
  - Purpose: Utility for managing Tailwind class variants.
  - Usage: Dynamic styling.

- **clsx**  
  - Purpose: Conditional className utility.
  - Usage: Simplifies className logic.

- **tailwind-merge**  
  - Purpose: Merges Tailwind CSS classes intelligently.
  - Usage: Prevents conflicting classes.

- **date-fns**  
  - Purpose: Modern JavaScript date utility library.
  - Usage: Date formatting and manipulation.

- **lucide-react**  
  - Purpose: Icon library for React.
  - Usage: UI icons.

### Tooling

- **ESLint**  
  - Purpose: Linting for JavaScript/TypeScript.
  - Usage: Code quality.
- **@types/\***  
  - Purpose: TypeScript type definitions for Node, React, etc.

---

## Third-Party APIs & Integrations

- **Google Calendar API**  
  - Purpose: (Planned) Syncing external calendars.
  - Status: Placeholder/mocked; see [backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md).
- **Amazon Alexa Reminders API**  
  - Purpose: (Planned) Voice assistant integration for chores/events.
  - Status: Placeholder/mocked; see [backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md).

---

## Dependency Topology

```mermaid
graph TD
  subgraph Backend
    A[FastAPI]
    B[SQLAlchemy]
    C[SQLite]
    D[Pydantic v2]
    E[LangGraph]
    F[python-dotenv]
    G[uvicorn]
    H[typing-extensions]
    I[uv (dev)]
    J[ruff (dev)]
    A --> B
    B --> C
    A --> D
    A --> E
    A --> F
    A --> G
    A --> H
    I -.-> A
    J -.-> A
  end

  subgraph Frontend
    K[Next.js]
    L[React]
    M[TypeScript]
    N[Tailwind CSS]
    O[Radix UI]
    P[class-variance-authority]
    Q[clsx]
    R[tailwind-merge]
    S[date-fns]
    T[lucide-react]
    U[ESLint/dev]
    V[@types/*]
    K --> L
    K --> M
    K --> N
    L --> O
    N --> P
    N --> Q
    N --> R
    K --> S
    K --> T
    U -.-> K
    V -.-> K
  end

  A -.-> K
  K -.-> A
```

---

## Primary Sources

- [README.md](https://github.com/sergiomasellis/Tapestry/blob/main/README.md) (Last modified: 2025-08-04 19:08)
- backend/pyproject.toml (Last modified: 2025-08-04 19:08)
- [backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md) (Last modified: 2025-08-04 19:08)
- [frontend/package.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/package.json) (Last modified: 2025-08-04 19:08)
- [frontend/tsconfig.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/tsconfig.json) (Last modified: 2025-08-04 19:08)
- [frontend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/README.md) (Last modified: 2025-08-04 19:08)