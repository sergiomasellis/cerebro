# Tapestry CI/CD Pipeline

| Repo     | Doc Type     | Date                | Branch |
|----------|--------------|---------------------|--------|
| Tapestry | CI/CD Pipeline | 2025-08-04 19:08   | main   |

---

This document describes the Continuous Integration and Continuous Deployment (CI/CD) pipeline for the Tapestry project, which consists of a Next.js/TypeScript frontend and a FastAPI/Python backend. Each component is managed, built, and deployed independently, but both are orchestrated to deliver a cohesive family calendar and chore management application.

## Overview

Tapestry's CI/CD pipeline ensures that both frontend and backend codebases are automatically linted, tested, built, and deployed on every push to the `main` branch (and optionally on pull requests). The pipeline is designed to:

- Maintain code quality and consistency
- Automate dependency installation and environment setup
- Build and test both frontend and backend in isolation
- Deploy artifacts to the appropriate environments (e.g., Vercel for frontend, cloud VM/container for backend)
- Support environment variable management and secrets injection

## Pipeline Stages

### 1. Trigger

- **On push**: Any commit to `main` triggers the pipeline.
- **On pull request**: Optionally, the pipeline runs for PRs to `main` for validation.

### 2. Frontend Pipeline

**Location:** `frontend/`  
**Stack:** Next.js, TypeScript, Tailwind CSS  
**Key Files:**  
- package.json (Last modified: 2025-08-04 19:08)
- tsconfig.json (Last modified: 2025-08-04 19:08)

**Steps:**
1. **Install dependencies**
   - `npm ci` (or `pnpm install` if using pnpm)
2. **Lint**
   - `npm run lint`
3. **Type-check**
   - `tsc --noEmit`
4. **Build**
   - `npm run build`
5. **Test** (if tests are present)
   - `npm test` or equivalent
6. **Deploy**
   - Deploy to Vercel (recommended) or another static hosting provider
   - Environment variables are injected via Vercel dashboard or `.env` files

### 3. Backend Pipeline

**Location:** `backend/`  
**Stack:** FastAPI, SQLAlchemy, Pydantic, LangGraph, SQLite  
**Key Files:**  
- pyproject.toml (Last modified: 2025-08-04 19:08)
- main.py (Last modified: 2025-08-04 19:08)

**Steps:**
1. **Install dependencies**
   - `uv pip install -r requirements.txt` or `uv sync`
2. **Lint**
   - `ruff check .`
3. **Test** (if tests are present)
   - `pytest` or equivalent
4. **Build**
   - (Optional) Build Docker image for deployment
5. **Migrate database**
   - Ensure SQLite schema is up-to-date (auto-migrates on app start)
6. **Deploy**
   - Deploy to cloud VM, container platform, or PaaS (e.g., Fly.io, Azure, AWS)
   - Environment variables loaded from `.env` (see [backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md) for details)

### 4. Integration & Smoke Tests

- Optionally, run end-to-end tests against deployed staging environments to verify integration between frontend and backend.

### 5. Notifications

- Pipeline status (success/failure) is reported to maintainers via repository integrations (e.g., GitHub Actions, Slack, email).

---

## Example Pipeline Flow (Mermaid)

```mermaid
flowchart TD
    A[Code Push / PR to main] --> B[Frontend Pipeline]
    B --> B1[Install deps (npm ci)]
    B1 --> B2[Lint (npm run lint)]
    B2 --> B3[Type-check (tsc)]
    B3 --> B4[Build (npm run build)]
    B4 --> B5[Deploy to Vercel]

    A --> C[Backend Pipeline]
    C --> C1[Install deps (uv sync)]
    C1 --> C2[Lint (ruff)]
    C2 --> C3[Test (pytest)]
    C3 --> C4[Build Docker image]
    C4 --> C5[Deploy to Cloud/VM]

    B5 & C5 --> D[Integration Tests (optional)]
    D --> E[Notify Maintainers]
```

---

## Environment & Secrets Management

- **Frontend:**  
  - Environment variables managed via Vercel dashboard or `.env.local` (not committed)
- **Backend:**  
  - `.env` file in `backend/` directory (see [backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md), Last modified: 2025-08-04 19:08)
  - Example variables: `DATABASE_URL`, `SECRET_KEY`, `ACCESS_TOKEN_EXPIRE_MINUTES`

## Deployment Targets

- **Frontend:**  
  - Vercel (recommended), Netlify, or similar static hosting
- **Backend:**  
  - Cloud VM/container (Docker), PaaS (Fly.io, Azure, AWS), or local server for development

## Rollback & Failure Handling

- Failed builds or tests prevent deployment
- Previous successful deployment remains active until new deployment passes all checks
- Manual rollback possible via hosting provider dashboard

## Local Development vs. CI

- Developers follow the same steps locally as in CI (see [README.md](https://github.com/sergiomasellis/Tapestry/blob/main/README.md) files)
- CI pipeline enforces consistency and prevents "works on my machine" issues

---

## Primary Sources

- [README.md](https://github.com/sergiomasellis/Tapestry/blob/main/README.md) (Last modified: 2025-08-04 19:08)
- [frontend/package.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/package.json) (Last modified: 2025-08-04 19:08)
- [frontend/tsconfig.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/tsconfig.json) (Last modified: 2025-08-04 19:08)
- [frontend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/README.md) (Last modified: 2025-08-04 19:08)
- backend/pyproject.toml (Last modified: 2025-08-04 19:08)
- [backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md) (Last modified: 2025-08-04 19:08)