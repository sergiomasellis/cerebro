# Tapestry Architectural Risks & Decisions

| Repo     | Doc Type         | Date                | Branch |
|----------|------------------|---------------------|--------|
| Tapestry | Architecture ADR | 2025-08-04 19:08    | main   |

---

## Overview

Tapestry is a multi-stack, family-oriented calendar and chore management application. Its architecture leverages a modern TypeScript/Next.js frontend and a FastAPI/SQLAlchemy backend, with SQLite for development and AI-powered features via LangGraph.

Tracking architectural risks and decisions is essential for ensuring maintainability, scalability, and clarity as the project evolves, especially given the integration of multiple technologies and the need for future extensibility (e.g., external calendar providers, AI pipelines).

---

## Key Architectural Decisions

### 1. Multi-Stack Separation

**Decision:**  
The project is split into `frontend` (Next.js/TypeScript) and `backend` (FastAPI/Python), each with its own dependencies, tooling, and deployment pipeline.

**Rationale:**  
- Enables independent scaling and deployment.
- Allows teams to specialize and iterate separately.
- Facilitates adoption of best-in-class frameworks for each concern.

**Risks:**  
- Increased complexity in API contracts and versioning.
- Potential for duplicated logic (e.g., validation).
- Cross-stack debugging can be more challenging.

**Mitigation:**  
- Use OpenAPI schemas for backend API documentation.
- Shared API contract documentation.
- Automated integration tests.

---

### 2. Backend: FastAPI + SQLAlchemy + LangGraph

**Decision:**  
Backend uses FastAPI for HTTP APIs, SQLAlchemy for ORM, and LangGraph for AI-driven features (e.g., chore generation).

**Rationale:**  
- FastAPI offers async support and OpenAPI generation.
- SQLAlchemy is a mature, flexible ORM.
- LangGraph enables future AI/automation features.

**Risks:**  
- LangGraph is relatively new; risk of breaking changes or lack of support.
- Async/ORM integration can be tricky.
- SQLite is not suitable for production scale.

**Mitigation:**  
- Encapsulate AI features behind clear interfaces.
- Plan for migration to PostgreSQL or similar for production.
- Use Pydantic for strict schema validation.

**Illustrative Snippet** (from backend/pyproject.toml, Last modified: 2025-08-04 19:08):

```toml
[project]
dependencies = [
    "fastapi>=0.116.1",
    "langgraph>=0.6.3",
    "pydantic[email]>=2.11.7",
    "sqlalchemy>=2.0.42",
    "uvicorn>=0.35.0",
]
```

---

### 3. Frontend: Next.js with TypeScript and Tailwind CSS

**Decision:**  
Frontend is built with Next.js (App Router), TypeScript, and Tailwind CSS.

**Rationale:**  
- Next.js provides SSR/SSG and a strong developer experience.
- TypeScript enforces type safety.
- Tailwind CSS enables rapid UI iteration.

**Risks:**  
- Keeping frontend types in sync with backend schemas.
- Next.js major version upgrades can introduce breaking changes.
- Tailwind configuration drift.

**Mitigation:**  
- Use OpenAPI codegen or manual DTO mapping.
- Pin dependency versions and monitor release notes.
- Centralize Tailwind config.

**Illustrative Snippet** (from [frontend/tsconfig.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/tsconfig.json), Last modified: 2025-08-04 19:08):

```json
{
  "compilerOptions": {
    "target": "ES2017",
    "strict": true,
    "jsx": "preserve",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

---

### 4. Authentication & Security

**Decision:**  
Backend provides JWT-based authentication, with endpoints for user login and admin login (master password).

**Rationale:**  
- JWT is stateless and widely supported.
- Master password enables admin recovery.

**Risks:**  
- JWT misconfiguration can lead to security holes.
- Master password is a potential attack vector.

**Mitigation:**  
- Store secrets in environment variables.
- Enforce strong password policies.
- Regularly rotate master password.

---

### 5. AI/Automation Integration

**Decision:**  
AI features (e.g., chore suggestion, point assignment) are implemented via LangGraph in a dedicated backend module.

**Rationale:**  
- Modularizes AI logic.
- Allows future replacement or extension.

**Risks:**  
- AI outputs may be unpredictable or require tuning.
- Dependency on external libraries.

**Mitigation:**  
- Keep AI logic isolated.
- Provide fallback/manual override in UI.

---

## Trade-Offs

- **SQLite for Development:**  
  Chosen for simplicity, but not suitable for production. Migration to a scalable DB is planned.
- **Monorepo vs. Polyrepo:**  
  Monorepo chosen for now for ease of cross-stack changes, but may revisit as team grows.
- **Minimal External Integrations:**  
  Mocks are used for Google Calendar/Alexa; real integrations deferred to reduce initial complexity.

---

## Mermaid Diagram: High-Level Architecture

```mermaid
flowchart TD
    subgraph Frontend [Next.js (TypeScript)]
        FE[UI Components & Pages]
    end
    subgraph Backend [FastAPI (Python)]
        API[REST API Endpoints]
        DB[(SQLite DB)]
        AI[LangGraph AI Module]
    end
    FE -- HTTP/JSON --> API
    API -- ORM --> DB
    API -- Chore/Points --> AI
```

---

## Primary Sources

- [README.md](https://github.com/sergiomasellis/Tapestry/blob/main/README.md) (Last modified: 2025-08-04 19:08)
- [frontend/tsconfig.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/tsconfig.json) (Last modified: 2025-08-04 19:08)
- [frontend/package.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/package.json) (Last modified: 2025-08-04 19:08)
- [frontend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/README.md) (Last modified: 2025-08-04 19:08)
- backend/pyproject.toml (Last modified: 2025-08-04 19:08)
- [backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md) (Last modified: 2025-08-04 19:08)
