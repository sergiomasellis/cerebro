# Tapestry CI/CD Pipeline

| Repo     | Doc Type      | Date                | Branch |
|----------|--------------|---------------------|--------|
| Tapestry | CI/CD Pipeline | 2025-08-04 19:08   | main   |

---

## Overview

Tapestry is a full-stack application with a Next.js (TypeScript) frontend and a FastAPI (Python) backend. The CI/CD pipeline is designed to ensure code quality, automate testing, and enable reliable deployments for both components. This document describes the typical CI/CD flow, the build and test steps, and deployment strategies for the `main` branch.

---

## Pipeline Stages

### 1. Trigger

- **Pushes** and **pull requests** to the `main` branch trigger the pipeline.
- Optionally, feature branches may trigger limited pipelines (lint/test only).

### 2. Lint & Static Analysis

- **Frontend**: Runs ESLint and TypeScript checks.
  - Uses configuration from `frontend/eslint.config.mjs` and `[frontend/tsconfig.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/tsconfig.json)` (Last modified: 2025-08-04 19:08).
- **Backend**: Runs Ruff (Python linter) and checks Pydantic/SQLAlchemy models.
  - Uses configuration from `backend/pyproject.toml` (Last modified: 2025-08-04 19:08).

### 3. Dependency Installation

- **Frontend**: Installs dependencies via `npm ci` or `pnpm install` using `[frontend/package.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/package.json)` (Last modified: 2025-08-04 19:08).
- **Backend**: Installs dependencies via `uv pip install -r requirements.txt` or `uv sync` using `backend/pyproject.toml` (Last modified: 2025-08-04 19:08).

### 4. Build

- **Frontend**: Runs `npm run build` to generate the production build.
- **Backend**: No explicit build step (Python is interpreted), but database migrations and static checks are performed.

### 5. Test

- **Frontend**: Runs any configured unit/integration tests (e.g., Jest, React Testing Library).
- **Backend**: Runs Python tests (e.g., pytest) and FastAPI endpoint checks.

### 6. Artifact Creation

- **Frontend**: Produces a `.next` build directory for deployment.
- **Backend**: Prepares the application for deployment (e.g., collects static files, ensures DB migrations).

### 7. Deployment

- **Frontend**: Deploys to Vercel (recommended, see `[frontend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/README.md)` Last modified: 2025-08-04 19:08) or another static host.
- **Backend**: Deploys to a cloud VM, container platform, or serverless environment (e.g., via Docker, Uvicorn/Gunicorn).
- **Environment Variables**: Managed via `.env` files (see `[backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md)` Last modified: 2025-08-04 19:08).

### 8. Post-Deployment

- **Smoke Tests**: Optionally, run basic endpoint checks to verify deployment.
- **Notify**: Send status notifications (e.g., Slack, email) on success/failure.

---

## Example CI/CD Workflow (Pseudocode)

```mermaid
flowchart TD
    A[Code Push / PR to main] --> B[Install Dependencies]
    B --> C[Lint & Static Analysis]
    C --> D[Build Frontend]
    D --> E[Run Frontend Tests]
    C --> F[Run Backend Tests]
    E --> G[Build Artifacts]
    F --> G
    G --> H[Deploy Frontend (Vercel)]
    G --> I[Deploy Backend (Cloud/VM)]
    H --> J[Post-Deploy Smoke Tests]
    I --> J
    J --> K[Notify Team]
```

---

## Configuration Files

- **Frontend**
  - `[frontend/package.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/package.json)` (Last modified: 2025-08-04 19:08): Defines scripts for build, lint, test.
  - `[frontend/tsconfig.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/tsconfig.json)` (Last modified: 2025-08-04 19:08): TypeScript configuration.
  - `frontend/eslint.config.mjs` (Last modified: 2025-08-04 19:08): Linting rules.
- **Backend**
  - `backend/pyproject.toml` (Last modified: 2025-08-04 19:08): Python dependencies and dev tools.
  - `.env` (see `[backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md)`): Secrets and environment variables.

---

## Deployment Targets

- **Frontend**: Vercel (recommended), Netlify, or custom static hosting.
- **Backend**: Cloud VM (e.g., AWS EC2), Docker container, or serverless (e.g., AWS Lambda with API Gateway).

---

## Environment Management

- **Development**: Local `.env` files, SQLite database.
- **Production**: Secure secrets management, production-grade database (e.g., PostgreSQL).

---

## Rollback & Recovery

- Deployments are atomic; previous build can be restored via Vercel/host dashboard or by redeploying a previous artifact.
- Database migrations should be reversible or require manual confirmation.

---

## Primary Sources

- [README.md](https://github.com/sergiomasellis/Tapestry/blob/main/README.md) (Last modified: 2025-08-04 19:08)
- [frontend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/README.md) (Last modified: 2025-08-04 19:08)
- [frontend/package.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/package.json) (Last modified: 2025-08-04 19:08)
- [frontend/tsconfig.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/tsconfig.json) (Last modified: 2025-08-04 19:08)
- [backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md) (Last modified: 2025-08-04 19:08)
- backend/pyproject.toml (Last modified: 2025-08-04 19:08)