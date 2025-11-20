# Observability Overview

| Repo     | Doc Type            | Date                | Branch |
|----------|---------------------|---------------------|--------|
| Tapestry | Observability (800) | 2025-08-04 19:08    | None   |

---

## Overview

This document provides an overview of the observability features—logging, metrics, and health checks—implemented in the Tapestry project. Observability is essential for monitoring application health, diagnosing issues, and ensuring reliable operations in production environments.

## Current State

**As of the latest review of the codebase and documentation (see "Primary Sources" below), there is no evidence of explicit observability mechanisms such as:**

- **Logging configuration or usage** (e.g., no use of Python's `logging` module, FastAPI/Next.js logging, or third-party logging libraries)
- **Metrics collection** (e.g., no Prometheus, StatsD, or custom metrics endpoints)
- **Health check endpoints** (e.g., `/health`, `/ready`, or similar routes)
- **Tracing or distributed tracing instrumentation**

### Backend

- **FastAPI** is used as the backend framework (`backend/app/main.py`), which provides basic access logs via the ASGI server (e.g., Uvicorn). However, there are no custom loggers or structured logging set up in the codebase.
- **No explicit logging statements** are present in the routers, models, or utility modules.
- **No health check routes** are defined in any of the routers (see `backend/app/routers/`).
- **No metrics or monitoring integrations** (e.g., Prometheus, OpenTelemetry) are present in the dependencies (`backend/pyproject.toml`).

### Frontend

- **Next.js** is used for the frontend (`frontend/`). There is no evidence of custom logging, error reporting, or analytics integrations in the configuration files or code.
- **No monitoring or error tracking** (e.g., Sentry, LogRocket) is configured in `frontend/package.json` or related files.

### Configuration

- **No observability-related environment variables** are documented in the backend or frontend README files.
- **No references to log levels, log destinations, or external monitoring services**.

## Recommendations

To improve observability in Tapestry, consider implementing the following:

1. **Backend Logging**
   - Configure Python's `logging` module or use a structured logging library (e.g., `loguru`).
   - Add log statements to key operations (user actions, errors, external API calls).
   - Route logs to files or external log aggregators in production.

2. **Health Checks**
   - Add a `/health` or `/ready` endpoint to the FastAPI app for basic liveness/readiness checks.
   - Optionally, include database connectivity and external service checks.

3. **Metrics**
   - Integrate a metrics library (e.g., `prometheus_fastapi_instrumentator`) to expose application metrics.
   - Track request counts, latency, error rates, and custom business metrics (e.g., chores completed).

4. **Frontend Monitoring**
   - Integrate error tracking (e.g., Sentry) and performance monitoring in the Next.js app.
   - Optionally, add analytics for user behavior.

5. **Documentation**
   - Document observability endpoints and log formats for operators and developers.

## Summary Table

| Aspect      | Current State | Recommendation                |
|-------------|--------------|-------------------------------|
| Logging     | Not present  | Add structured logging        |
| Metrics     | Not present  | Integrate metrics collection  |
| Healthcheck | Not present  | Add `/health` endpoint        |
| Tracing     | Not present  | Add tracing if needed         |
| Frontend    | Not present  | Add error/perf monitoring     |

---

## Primary Sources

- [`README.md`](./README.md) (Last modified: 2025-08-04 19:08)
- [`backend/README.md`](./backend/README.md) (Last modified: 2025-08-04 19:08)
- [`backend/pyproject.toml`](./backend/pyproject.toml) (Last modified: 2025-08-04 19:08)
- [`frontend/package.json`](./frontend/package.json) (Last modified: 2025-08-04 19:08)
- [`frontend/tsconfig.json`](./frontend/tsconfig.json) (Last modified: 2025-08-04 19:08)
- [`frontend/README.md`](./frontend/README.md) (Last modified: 2025-08-04 19:08)

---

**Note:** This assessment is based on the latest available files and documentation. If observability features are added in the future, this document should be updated accordingly.