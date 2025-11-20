# Tapestry – Risks & Architecture Decisions

| Repo      | Doc Type           | Date                | Branch   |
|-----------|--------------------|---------------------|----------|
| Tapestry  | Risks & Decisions  | 2025-08-04 19:08    | main     |

---

This document records key architecture decisions, trade-offs, and known limitations for the Tapestry project. It serves as a reference for future contributors and maintainers, capturing the rationale behind major technical choices and highlighting areas of risk.

## 1. Architecture Decision Records (ADRs)

### 1.1 Tech Stack Selection

- **Frontend:** Next.js (React, TypeScript, Tailwind CSS)
- **Backend:** FastAPI (Python), SQLAlchemy ORM
- **Database:** SQLite (development)
- **AI/Automation:** LangGraph (for AI-powered chore generation and point assignment)

**Rationale:**  
- Next.js offers rapid development, SSR/SSG, and a strong React ecosystem.
- FastAPI provides async support, type safety, and automatic OpenAPI docs.
- SQLite is lightweight and requires no setup for local development.
- LangGraph enables future AI/automation features with minimal integration overhead.

**Trade-offs:**  
- SQLite is not suitable for production-scale concurrency or multi-user writes.
- Next.js and FastAPI are separate stacks, requiring API contract discipline and CORS management.
- LangGraph is an emerging library; future maintenance risk if upstream changes.

---

### 1.2 Database Choice: SQLite for Development

**Decision:**  
- Use SQLite (`backend/data.db`) for all local development and initial testing.

**Rationale:**  
- Zero configuration, easy onboarding for new contributors.
- Sufficient for prototyping and small team/family usage.

**Limitations:**  
- Not horizontally scalable.
- No built-in user/role management.
- Migration to PostgreSQL or similar is required for production.

---

### 1.3 API Design: RESTful Endpoints

**Decision:**  
- All backend functionality is exposed via RESTful endpoints (see [backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md), last modified: 2025-08-04 19:08).

**Rationale:**  
- Simplicity and compatibility with frontend frameworks.
- Automatic docs via FastAPI.

**Trade-offs:**  
- No real-time updates (e.g., via WebSockets) in MVP.
- API versioning and backward compatibility must be managed manually.

---

### 1.4 Authentication

**Decision:**  
- Token-based authentication (JWT), with a master password for admin login (see [backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md)).

**Rationale:**  
- JWT is standard for stateless APIs.
- Master password simplifies admin/dev access during early development.

**Risks:**  
- Master password is a security risk if not managed properly.
- No OAuth/social login in MVP; will require future integration.

---

### 1.5 AI Integration (LangGraph)

**Decision:**  
- Use LangGraph for AI-powered features (e.g., chore suggestion, point assignment).

**Rationale:**  
- Enables advanced features with minimal code.
- Keeps AI logic modular and replaceable.

**Risks:**  
- LangGraph is a young dependency; API or support may change.
- AI features are experimental and may not be robust.

---

### 1.6 Monorepo Structure

**Decision:**  
- Use a single repository with `frontend/` and `backend/` directories.

**Rationale:**  
- Simplifies dependency management and cross-team collaboration.
- Easier to coordinate changes across stack.

**Trade-offs:**  
- Potential for accidental cross-contamination of dependencies.
- Requires discipline in CI/CD and environment setup.

---

## 2. Known Limitations & Risks

- **Scalability:**  
  - SQLite cannot handle high concurrency or large datasets.
  - No production-ready deployment scripts or Dockerfiles yet.

- **Security:**  
  - Master password approach is not secure for production.
  - No rate limiting or brute-force protection in MVP.

- **Extensibility:**  
  - External integrations (Google Calendar, Alexa) are stubbed/mocked.
  - Migration to production-grade DB and OAuth will require non-trivial refactoring.

- **Testing:**  
  - No end-to-end or integration tests defined yet.
  - Manual testing required for most flows.

- **Observability:**  
  - Minimal logging and no metrics/monitoring in place.

---

## 3. Decision Flow Diagram

```mermaid
flowchart TD
    A[Start: Project Requirements] --> B{Frontend Framework?}
    B -->|SSR/React Ecosystem| C[Next.js (TypeScript)]
    A --> D{Backend Framework?}
    D -->|Async, Type Safety| E[FastAPI (Python)]
    E --> F{Database?}
    F -->|Zero-config Dev| G[SQLite]
    E --> H{AI/Automation?}
    H -->|Chore/Point AI| I[LangGraph]
    C & G & I --> J[Monorepo Structure]
    J --> K[REST API Design]
    K --> L[Token-based Auth (JWT)]
    L --> M[Local Dev, MVP Ready]
```

---

## 4. Summary Table of Major Decisions

| Area           | Decision                    | Rationale                    | Risks/Limitations                |
|----------------|----------------------------|------------------------------|----------------------------------|
| Frontend       | Next.js (TS, Tailwind)      | Modern, SSR, React ecosystem | Learning curve, SSR complexity   |
| Backend        | FastAPI, SQLAlchemy         | Async, type safety           | Python/JS split, CORS            |
| Database       | SQLite (dev only)           | Zero-config, easy onboarding | Not scalable, prod migration     |
| AI             | LangGraph                   | Modular AI features          | Young library, future support    |
| Auth           | JWT, master password        | Simplicity, dev speed        | Security risk, no OAuth          |
| API            | RESTful                     | Simplicity, docs             | No real-time, manual versioning  |
| Structure      | Monorepo                    | Coordination, onboarding     | Dependency isolation             |

---

## Primary Sources

- [README.md](https://github.com/sergiomasellis/Tapestry/blob/main/README.md) (Last modified: 2025-08-04 19:08)
- [backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md) (Last modified: 2025-08-04 19:08)
- backend/pyproject.toml (Last modified: 2025-08-04 19:08)
- [frontend/package.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/package.json) (Last modified: 2025-08-04 19:08)
- [frontend/tsconfig.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/tsconfig.json) (Last modified: 2025-08-04 19:08)
