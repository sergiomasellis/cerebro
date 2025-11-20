# Risks & Architectural Decisions

| Repo     | Doc Type              | Date                | Branch |
|----------|----------------------|---------------------|--------|
| Tapestry | Risks & Decisions (930) | 2025-08-04           | main   |

## Overview

This document summarizes the known architectural risks, limitations, and implicit design decisions for the Tapestry project, based on the current repository structure and available documentation. As of the latest review, there is **no explicit evidence of formal ADRs (Architectural Decision Records)** or a dedicated risk/decision log in the codebase or README files.

## 1. Lack of Formal ADRs

- **Observation:**  
  No files or directories (e.g., `docs/adr/`, `decisions/`, or `adr-*.md`) are present in the repository. The README files do not mention any process or location for tracking architectural decisions or risk assessments.
- **Implication:**  
  Architectural and technical decisions are likely being made informally or are embedded in code and commit history, which may hinder future onboarding, audits, or major refactors.

## 2. Key Architectural Decisions (Inferred)

Based on the README and project structure, the following implicit decisions and trade-offs are evident:

### a. Tech Stack Choices

- **Frontend:** Next.js (TypeScript, Tailwind CSS)
- **Backend:** FastAPI (Python), SQLAlchemy ORM, SQLite (development)
- **AI/Automation:** LangGraph for AI-driven chore generation and point assignment

**Risks:**
- **SQLite for Development:**  
  - *Limitation:* Not suitable for production-scale concurrency or multi-user writes.
  - *Decision:* Chosen for simplicity and ease of setup in development.
- **LangGraph Integration:**  
  - *Risk:* AI pipeline for chore generation is experimental; may introduce instability or unpredictable results.
- **Monorepo Structure:**  
  - *Trade-off:* Easier cross-team collaboration, but may complicate CI/CD and dependency management.

### b. Authentication & Security

- **Observation:**  
  Backend README references "admin-login (master password)" and `.env`-based secrets.
- **Risks:**
  - *Master Password:* Single point of failure; if leaked, all admin access is compromised.
  - *Environment Secrets:* Reliance on `.env` files for secrets is common, but may be insecure if not handled properly.

### c. External Integrations

- **Observation:**  
  README notes "mock behavior where external integrations are required" (e.g., Google Calendar, Alexa Reminders).
- **Risks:**
  - *Mocked Integrations:* Real-world edge cases and error handling may be missed until late in development.
  - *Incremental Replacement:* Risk of technical debt if mocks are not systematically replaced.

### d. Minimal Error Handling & Observability

- **Observation:**  
  No mention of logging, monitoring, or error reporting in the documentation or file structure.
- **Risks:**
  - *Limited Observability:* Harder to debug or monitor failures in production.
  - *Minimal Error Handling:* Increased risk of silent failures or poor user experience.

### e. Testing & CI/CD

- **Observation:**  
  No explicit mention of automated tests or CI/CD pipelines in the README or file structure.
- **Risks:**
  - *Manual QA Burden:* Increased risk of regressions and deployment errors.
  - *Delayed Feedback:* Issues may only surface in manual testing or production.

## 3. Limitations

- **No Production Database Configuration:**  
  Only SQLite is documented; migration to PostgreSQL/MySQL for production is not addressed.
- **No Documented Data Migration Strategy:**  
  Schema changes or upgrades may be manual and error-prone.
- **No API Versioning:**  
  All endpoints are assumed to be unversioned, risking breaking changes for clients.

## 4. Recommendations

- **Introduce ADRs:**  
  Adopt a lightweight ADR process (e.g., Markdown files in a `/docs/adr/` directory) to record major decisions and rationale.
- **Formalize Risk Log:**  
  Track known risks and mitigation strategies in a living document.
- **Plan for Productionization:**  
  Document steps for moving from SQLite to a production-grade database, and for replacing mocks with real integrations.
- **Add Observability:**  
  Integrate logging and error reporting early to aid debugging and support.
- **Automate Testing & CI/CD:**  
  Add basic test coverage and CI/CD scripts to reduce manual QA burden.

## 5. Summary Table

| Area                  | Risk / Limitation                                 | Status / Mitigation         |
|-----------------------|---------------------------------------------------|-----------------------------|
| ADRs                  | No formal records                                 | Not present                 |
| Database              | SQLite only, no prod config                       | Not addressed               |
| Authentication        | Master password, .env secrets                     | Not hardened                |
| Integrations          | Mocks for external APIs                           | Not replaced                |
| Observability         | No logging/monitoring                             | Not implemented             |
| Testing/CI            | No automated tests or pipelines                   | Not present                 |
| API Versioning        | None                                              | Not addressed               |
| Data Migration        | No documented strategy                            | Not addressed               |

---

## Primary Sources

- [README.md](https://github.com/sergiomasellis/Tapestry/blob/main/README.md) (Last modified: 2025-08-04 19:08)
- [backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md) (Last modified: 2025-08-04 19:08)
- backend/pyproject.toml (Last modified: 2025-08-04 19:08)
- [frontend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/README.md) (Last modified: 2025-08-04 19:08)
- [frontend/package.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/package.json) (Last modified: 2025-08-04 19:08)
- [frontend/tsconfig.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/tsconfig.json) (Last modified: 2025-08-04 19:08)