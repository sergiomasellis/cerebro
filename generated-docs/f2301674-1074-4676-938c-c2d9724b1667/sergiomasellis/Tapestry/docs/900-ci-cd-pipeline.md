# Tapestry CI/CD Pipeline

| Repo    | Doc Type        | Date       | Branch |
|---------|----------------|------------|--------|
| Tapestry | CI/CD Pipeline | 2025-08-04 | None   |

---

This document describes the Continuous Integration and Continuous Deployment (CI/CD) pipeline for the Tapestry project, which consists of a Next.js/TypeScript frontend and a FastAPI/SQLAlchemy backend. The pipeline ensures code quality, repeatable builds, automated testing, and safe deployments across multiple environments.

## Overview

The CI/CD pipeline for Tapestry is designed to:

- **Automate builds** for both frontend and backend.
- **Run linting and tests** to ensure code quality.
- **Build and publish Docker images** (or deploy to Vercel for frontend).
- **Deploy to multiple environments** (development, staging, production).
- **Manage secrets and environment variables** securely.

The pipeline is intended to be compatible with popular CI/CD platforms (e.g., GitHub Actions, Vercel, or similar).

---

## Pipeline Stages

### 1. Trigger

- **On Pull Request**: Run checks, lint, and tests.
- **On Push to Main/Release Branches**: Run full build, test, and deploy.

### 2. Lint & Static Analysis

#### Frontend

- Runs `npm run lint` (see `frontend/package.json`, Last modified: 2025-08-04 19:08).
- Uses ESLint with Next.js config.

#### Backend

- Runs `ruff` for Python linting (see `backend/pyproject.toml`, Last modified: 2025-08-04 19:08).

### 3. Build

#### Frontend

- Runs `npm run build` (Next.js static build).
- Artifacts: `.next/` directory.

#### Backend

- Installs dependencies via `uv` or `pip`.
- Optionally builds a Docker image for deployment.

### 4. Test

#### Frontend

- (If tests are present) Runs `npm test` or equivalent.

#### Backend

- (If tests are present) Runs `pytest` or similar.

### 5. Deploy

#### Frontend

- **Development/Preview**: Deploys preview builds to Vercel or similar.
- **Production**: Deploys to Vercel main project or serves static files via CDN.

#### Backend

- **Development**: Deploys to a dev server (e.g., via Docker Compose or direct `uvicorn` run).
- **Production**: Deploys Docker image to cloud VM, container service, or managed PaaS.

### 6. Environment Management

- Uses `.env` files for local development (see `backend/README.md`, Last modified: 2025-08-04 19:08).
- Secrets and environment variables are injected via the CI/CD platform for staging/production.

---

## Example CI/CD Workflow (Pseudocode)

```yaml
# .github/workflows/ci.yml (not present, for illustration)
on:
  push:
    branches: [main, release/*]
  pull_request:

jobs:
  lint-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: cd frontend && npm ci && npm run lint

  lint-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: cd backend && uv pip install -r pyproject.toml && uv run ruff app/

  build-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: cd frontend && npm ci && npm run build

  build-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: cd backend && uv pip install -r pyproject.toml

  deploy-frontend:
    needs: build-frontend
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          working-directory: ./frontend

  deploy-backend:
    needs: build-backend
    runs-on: ubuntu-latest
    steps:
      - name: Build and push Docker image
        run: |
          cd backend
          docker build -t ghcr.io/org/tapestry-backend:${{ github.sha }} .
          docker push ghcr.io/org/tapestry-backend:${{ github.sha }}
      - name: Deploy to server
        run: ssh user@host 'docker pull ghcr.io/org/tapestry-backend:${{ github.sha }} && docker compose up -d'
```

---

## Environment Matrix

| Environment   | Frontend Deploy Target | Backend Deploy Target | Secrets/Config Source      |
|---------------|-----------------------|----------------------|----------------------------|
| Development   | Vercel Preview        | Localhost / Dev VM   | `.env` files, CI secrets   |
| Staging       | Vercel Staging        | Staging VM/Container | CI/CD secrets              |
| Production    | Vercel Production     | Prod VM/Container    | CI/CD secrets              |

---

## Artifact & Dependency Management

- **Frontend**: Uses `pnpm-lock.yaml` for deterministic installs (see `frontend/pnpm-lock.yaml`, Last modified: 2025-08-04 19:08).
- **Backend**: Uses `pyproject.toml` and `uv.lock` for Python dependencies.

---

## Rollback & Monitoring

- **Frontend**: Vercel supports instant rollbacks to previous deployments.
- **Backend**: Docker image tags allow for quick rollback; logs and health checks should be monitored post-deploy.

---

## Example Pipeline Diagram

```mermaid
flowchart TD
    A[Code Commit / PR] --> B[CI: Lint & Test]
    B --> C[Build Frontend]
    B --> D[Build Backend]
    C --> E[Deploy Frontend (Vercel)]
    D --> F[Deploy Backend (Docker/VM)]
    E --> G[Preview/Production URL]
    F --> H[API Endpoint]
```

---

## Best Practices

- Keep secrets out of source control; use CI/CD secrets management.
- Use lockfiles for deterministic builds.
- Tag Docker images with commit SHA for traceability.
- Run lint and tests on every PR and push.
- Use preview deployments for feature branches.

---

## Primary Sources

- [README.md](./README.md) (Last modified: 2025-08-04 19:08)
- [frontend/package.json](./frontend/package.json) (Last modified: 2025-08-04 19:08)
- [frontend/tsconfig.json](./frontend/tsconfig.json) (Last modified: 2025-08-04 19:08)
- [frontend/README.md](./frontend/README.md) (Last modified: 2025-08-04 19:08)
- [backend/README.md](./backend/README.md) (Last modified: 2025-08-04 19:08)
- [backend/pyproject.toml](./backend/pyproject.toml) (Last modified: 2025-08-04 19:08)
- [backend/uv.lock](./backend/uv.lock) (Last modified: 2025-08-04 19:08)
