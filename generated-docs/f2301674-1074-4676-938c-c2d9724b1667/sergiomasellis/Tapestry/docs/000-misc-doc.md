# Tapestry Documentation Index

| Repo     | Doc Type                | Date                | Branch |
|----------|------------------------|---------------------|--------|
| Tapestry | Table of Contents (000) | 2025-08-04 19:08    | None   |

Welcome to the documentation for **Tapestry**, a modern, touch-friendly multi-user calendar and family management application. This index will help you navigate the technical documentation for both the frontend (Next.js) and backend (FastAPI) components.

---

## Table of Contents

1. **[100 - Architecture & Topology](./TAPESTRY_PRD_AND_SYSTEM_DESIGN.md#architecture--topology)**
   - High-level system components, their interactions, and architectural style.
2. **[101 - System Router](./TAPESTRY_PRD_AND_SYSTEM_DESIGN.md#system-router)**
   - Entrypoints, routing logic, and request flow.
3. **[200 - Domain & Business Rules](./TAPESTRY_PRD_AND_SYSTEM_DESIGN.md#domain--business-rules)**
   - Core entities, business logic, and domain flows.
4. **[311 - REST API Endpoints](./TAPESTRY_PRD_AND_SYSTEM_DESIGN.md#rest-api-endpoints)**
   - List of API endpoints, their purposes, and semantics.
5. **[330 - Event Topics](./TAPESTRY_PRD_AND_SYSTEM_DESIGN.md#event-topics)**
   - Event-driven architecture topics (if applicable).
6. **[421 - Main Entity Schema](./TAPESTRY_PRD_AND_SYSTEM_DESIGN.md#main-entity-schema)**
   - Entity-relationship diagrams and key data models.
7. **[500 - Key Dependencies](./TAPESTRY_PRD_AND_SYSTEM_DESIGN.md#key-dependencies)**
   - Internal services and third-party APIs.
8. **[600 - Config & Environments](./TAPESTRY_PRD_AND_SYSTEM_DESIGN.md#config--environments)**
   - Configuration files, environment variables, and secrets management.
9. **[701 - Authentication Model](./TAPESTRY_PRD_AND_SYSTEM_DESIGN.md#authentication-model)**
   - Auth mechanisms, flows, and permissions.
10. **[800 - Observability Overview](./TAPESTRY_PRD_AND_SYSTEM_DESIGN.md#observability-overview)**
    - Logging, metrics, and health checks.
11. **[850 - Runbook Operations](./TAPESTRY_PRD_AND_SYSTEM_DESIGN.md#runbook-operations)**
    - Failure modes, debugging, and restart procedures.
12. **[900 - CI/CD Pipeline](./TAPESTRY_PRD_AND_SYSTEM_DESIGN.md#cicd-pipeline)**
    - Build, test, and deployment automation.
13. **[930 - Risks & Decisions](./TAPESTRY_PRD_AND_SYSTEM_DESIGN.md#risks--decisions)**
    - Architectural decisions, limitations, and trade-offs.
14. **[980 - RAG Indexing Guidelines](./TAPESTRY_PRD_AND_SYSTEM_DESIGN.md#rag-indexing-guidelines)**
    - Retrieval-augmented generation (RAG) tagging and clustering.

---

## Project Structure

```
.
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── ...
├── backend/
│   ├── app/
│   ├── data.db
│   ├── main.py
│   └── ...
├── TAPESTRY_PRD_AND_SYSTEM_DESIGN.md
├── README.md
└── ...
```

---

## Primary Sources

- [README.md](./README.md) (Last modified: 2025-08-04 19:08)
- [frontend/README.md](./frontend/README.md) (Last modified: 2025-08-04 19:08)
- [backend/README.md](./backend/README.md) (Last modified: 2025-08-04 19:08)
- [frontend/package.json](./frontend/package.json) (Last modified: 2025-08-04 19:08)
- [frontend/tsconfig.json](./frontend/tsconfig.json) (Last modified: 2025-08-04 19:08)
- [backend/pyproject.toml](./backend/pyproject.toml) (Last modified: 2025-08-04 19:08)

---

For detailed information on each topic, follow the links above or refer to the [TAPESTRY_PRD_AND_SYSTEM_DESIGN.md](./TAPESTRY_PRD_AND_SYSTEM_DESIGN.md) file.