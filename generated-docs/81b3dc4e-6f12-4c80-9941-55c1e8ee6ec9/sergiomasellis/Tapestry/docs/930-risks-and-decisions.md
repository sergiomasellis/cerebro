# Risks & Architectural Decisions – Tapestry

| Repo     | Doc Type         | Date                | Branch |
|----------|------------------|---------------------|--------|
| Tapestry | Risks & Decisions | 2025-08-04          | main   |

---

This document captures key architectural decisions, known risks, limitations, and trade-offs for the Tapestry family calendar application. It is intended to provide transparency for contributors and stakeholders regarding why certain choices were made, and to highlight areas that may require future attention or mitigation.

## 1. Architectural Decisions

### 1.1. Monorepo with Clear Frontend/Backend Separation

- **Decision**: The project uses a monorepo with `frontend/` (Next.js, TypeScript) and `backend/` (FastAPI, Python) directories.
- **Rationale**: Simplifies dependency management, onboarding, and cross-team collaboration. Enables atomic PRs across stack.
- **Trade-off**: Increases repo size and complexity for CI/CD. Requires discipline in interface contracts.

### 1.2. SQLite for Development

- **Decision**: SQLite is used as the default database for development.
- **Rationale**: Zero-config, easy onboarding, and suitable for prototyping.
- **Limitation**: Not suitable for production scale or concurrent writes. Migration to PostgreSQL or similar is expected for production.

### 1.3. REST API with FastAPI

- **Decision**: Backend exposes RESTful endpoints using FastAPI.
- **Rationale**: FastAPI offers rapid development, async support, and automatic OpenAPI docs.
- **Trade-off**: No GraphQL or real-time API (WebSockets) at this stage. May limit some client-side flexibility.

### 1.4. AI-Powered Chore Generation (LangGraph)

- **Decision**: Chore suggestions and point assignments leverage LangGraph pipelines.
- **Rationale**: Provides dynamic, context-aware task recommendations for families.
- **Risk**: AI pipeline is experimental; may produce inconsistent or non-actionable results. Requires ongoing tuning and fallback logic.

### 1.5. Minimal External Integrations (MVP)

- **Decision**: Integrations with Google Calendar, Alexa, and OAuth are stubbed/mocked in the initial release.
- **Rationale**: Focus on core flows and reduce initial complexity.
- **Limitation**: Limits real-world utility for families with existing digital calendars. Integration work is deferred.

### 1.6. Authentication Model

- **Decision**: Simple token-based authentication with a master admin password for development.
- **Rationale**: Expedites development and testing.
- **Risk**: Not secure for production. Requires upgrade to robust authentication (OAuth, password hashing, etc.) before launch.

### 1.7. TypeScript/Next.js Frontend

- **Decision**: Next.js with TypeScript and Tailwind CSS for the frontend.
- **Rationale**: Modern developer experience, SSR/SSG support, and strong typing.
- **Trade-off**: SSR adds complexity for stateful interactions; requires careful API design.

---

## 2. Known Risks & Limitations

### 2.1. Data Consistency and Concurrency

- **Risk**: SQLite's concurrency limitations may cause data corruption or lost updates under concurrent access.
- **Mitigation**: Acceptable for development; must migrate to a production-grade RDBMS before scaling.

### 2.2. Security

- **Risk**: Development secrets are hardcoded (see `.env.example`). Token management is basic.
- **Mitigation**: Secrets management and secure authentication are required for production.

### 2.3. AI Pipeline Reliability

- **Risk**: LangGraph-based AI may generate inappropriate or irrelevant chores.
- **Mitigation**: Human-in-the-loop review and fallback to manual entry.

### 2.4. API Surface Instability

- **Risk**: API endpoints and schemas may change rapidly during early development.
- **Mitigation**: Version endpoints and document changes; communicate breaking changes clearly.

### 2.5. Limited Observability

- **Risk**: Minimal logging and monitoring in MVP.
- **Mitigation**: Add structured logging, error tracking, and health checks before production.

### 2.6. Vendor/Dependency Lock-in

- **Risk**: Heavy reliance on Next.js, FastAPI, and LangGraph.
- **Mitigation**: Abstract interfaces where possible; document migration paths.

---

## 3. Trade-offs

| Area                  | Chosen Approach                | Alternatives Considered         | Trade-off/Reasoning                         |
|-----------------------|-------------------------------|---------------------------------|---------------------------------------------|
| Database              | SQLite (dev)                  | PostgreSQL, MySQL               | Simplicity vs. scalability                  |
| API                   | REST (FastAPI)                | GraphQL, gRPC                   | Familiarity, tooling, speed of dev          |
| Frontend              | Next.js + TypeScript          | React SPA, Vue, Svelte          | SSR/SSG, ecosystem, hiring                  |
| AI Integration        | LangGraph pipeline            | Manual rules, OpenAI API        | Flexibility vs. predictability              |
| Auth                  | Token, master password (dev)  | OAuth, JWT, SSO                 | Speed vs. security                          |
| Calendar Integration  | Mocked                        | Full Google/Alexa integration   | Focus on core, defer complexity             |

---

## 4. Future Considerations

- **Production Database**: Plan migration scripts and test with PostgreSQL.
- **Authentication**: Implement OAuth2, hashed passwords, and session management.
- **External Integrations**: Prioritize Google Calendar and Alexa APIs.
- **Observability**: Add metrics, tracing, and alerting.
- **AI Controls**: Add admin override and feedback loop for AI-generated chores.
- **API Versioning**: Adopt semantic versioning for endpoints.

---

## Primary Sources

- [[README.md](https://github.com/sergiomasellis/Tapestry/blob/main/README.md)](./[README.md](https://github.com/sergiomasellis/Tapestry/blob/main/README.md)) (Last modified: 2025-08-04 19:08)
- [[frontend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/README.md)](./[frontend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/README.md)) (Last modified: 2025-08-04 19:08)
- [[backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md)](./[backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md)) (Last modified: 2025-08-04 19:08)
- [[frontend/package.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/package.json)](./[frontend/package.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/package.json)) (Last modified: 2025-08-04 19:08)
- [[frontend/tsconfig.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/tsconfig.json)](./[frontend/tsconfig.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/tsconfig.json)) (Last modified: 2025-08-04 19:08)
- [backend/pyproject.toml](./backend/pyproject.toml) (Last modified: 2025-08-04 19:08)

---

*This document is living and should be updated as new risks and decisions emerge.*