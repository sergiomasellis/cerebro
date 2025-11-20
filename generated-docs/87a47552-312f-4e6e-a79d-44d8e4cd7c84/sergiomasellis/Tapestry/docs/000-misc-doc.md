# Tapestry Documentation Index

| Repo     | Doc Type            | Date                | Branch |
|----------|---------------------|---------------------|--------|
| Tapestry | Table of Contents   | 2025-08-04 19:08    | main   |

Welcome to the documentation for **Tapestry**, a modern, touch-friendly multi-user calendar and family management application. This index provides an overview of the available documentation sections to help you navigate the system's architecture, features, and operations.

---

## Table of Contents

1. **[100] Architecture & Topology**
   - High-level system components
   - Component interactions and deployment style
   - [Mermaid diagram included]

2. **[101] System Router**
   - Entrypoints for frontend and backend
   - Routing logic and flow
   - [Mermaid diagram included]

3. **[200] Domain & Business Rules**
   - Core entities and business logic
   - Domain flows and context

4. **[311] REST API Endpoints**
   - Table of backend REST endpoints
   - Endpoint purposes and semantics
   - [Mermaid diagram included]

5. **[330] Event Topics**
   - Event-driven architecture topics (if applicable)

6. **[421] Main Entity Schema**
   - Entity-relationship diagrams
   - Key entities and relationships
   - [Mermaid diagram included]

7. **[500] Key Dependencies**
   - Internal services and 3rd party APIs

8. **[600] Config & Environments**
   - Configuration files, environment variables, and secrets management

9. **[701] Authentication Model**
   - Authentication mechanisms and permissions

10. **[800] Observability Overview**
    - Logging, metrics, and health checks

11. **[850] Runbook Operations**
    - Failure modes, debugging, and restart procedures

12. **[900] CI/CD Pipeline**
    - Build, test, and deployment processes

13. **[930] Risks & Decisions**
    - Architectural decisions, limitations, and trade-offs

14. **[980] RAG Indexing Guidelines**
    - Retrieval-augmented generation (RAG) tagging, questions, and clustering

---

## Mermaid Diagram: High-Level System Overview

```mermaid
graph TD
    subgraph Frontend (Next.js)
        FE_App[App (page.tsx, layout.tsx)]
        FE_Components[UI Components]
        FE_Features[Feature Modules]
    end

    subgraph Backend (FastAPI)
        BE_App[FastAPI App (main.py)]
        BE_Routers[API Routers (users, families, chores, etc.)]
        BE_Models[SQLAlchemy Models]
        BE_Schemas[Pydantic Schemas]
        BE_AI[LangGraph AI Pipeline]
        BE_DB[(SQLite DB)]
    end

    FE_App -->|REST API| BE_App
    FE_Components --> FE_App
    FE_Features --> FE_App
    BE_App --> BE_Routers
    BE_Routers --> BE_Models
    BE_Routers --> BE_Schemas
    BE_Routers --> BE_AI
    BE_Models --> BE_DB
```

---

## Primary Sources

- [README.md](https://github.com/sergiomasellis/Tapestry/blob/main/README.md) (Last modified: 2025-08-04 19:08)
- [frontend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/README.md) (Last modified: 2025-08-04 19:08)
- [backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md) (Last modified: 2025-08-04 19:08)
- [frontend/tsconfig.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/tsconfig.json) (Last modified: 2025-08-04 19:08)
- [frontend/package.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/package.json) (Last modified: 2025-08-04 19:08)
- backend/pyproject.toml (Last modified: 2025-08-04 19:08)
- backend/app/routers/*.py (Last modified: see individual files)
- [backend/app/models/models.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/models/models.py) (Last modified: see individual file)
- [backend/app/schemas/schemas.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/schemas/schemas.py) (Last modified: see individual file)
- [backend/app/ai/chore_graph.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/ai/chore_graph.py) (Last modified: see individual file)

---

For detailed information, refer to each section as listed above.