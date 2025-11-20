# Observability Overview

| Repo      | Doc Type             | Date                | Branch   |
|-----------|---------------------|---------------------|----------|
| Tapestry  | Observability (800) | 2025-08-04 19:08    | main     |

---

## Introduction

Observability is a critical aspect of any production-grade application, enabling teams to monitor system health, diagnose issues, and ensure reliable operation. This document outlines the current state of observability in the Tapestry project, including logging, metrics, and health checks, based on the available codebase and documentation as of the last update.

---

## Current Observability State

### 1. Logging

**Backend:**
- The backend is built with FastAPI (see [backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md), Last modified: 2025-08-04 19:08), which provides built-in logging via Uvicorn and FastAPI’s own logger.
- There is no explicit mention or configuration of structured logging, log levels, or log aggregation in the provided files.
- By default, FastAPI and Uvicorn will output access logs and error logs to the console. This is suitable for development but may require enhancement for production (e.g., JSON logging, external log sinks).

**Frontend:**
- The frontend is a Next.js application (see [frontend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/README.md), Last modified: 2025-08-04 19:08).
- No explicit logging libraries or custom logging logic are present in the configuration or code.
- Next.js outputs build and runtime logs to the console, which can be captured by hosting platforms such as Vercel.

### 2. Metrics

- There is no evidence of custom metrics collection (e.g., Prometheus, StatsD) in either the backend or frontend.
- FastAPI does not expose metrics endpoints by default. No `/metrics` or similar endpoints are defined in [backend/app/main.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/main.py) or routers.
- Next.js does not provide built-in application metrics, but hosting providers may offer basic request and error metrics.

### 3. Health Checks

- No explicit health check endpoints (e.g., `/healthz`, `/readyz`) are defined in the backend routers or main application file.
- FastAPI applications can easily add such endpoints, but as of the current codebase, this is not implemented.
- The database (SQLite) is initialized on backend startup, but there is no runtime check for database connectivity or external service health.

### 4. Error Reporting

- Error handling is managed by FastAPI’s default exception handlers, which return HTTP error responses and log stack traces to the console.
- No integration with external error tracking services (e.g., Sentry, Rollbar) is present.
- The frontend does not appear to use any error boundary or reporting tools.

### 5. Environment and Configuration

- Environment variables are managed via python-dotenv in the backend (see backend/pyproject.toml, Last modified: 2025-08-04 19:08).
- No observability-specific configuration (e.g., log level, log format, metrics endpoint) is present.

---

## Observability Gaps and Recommendations

| Area         | Current State | Recommendation                                 |
|--------------|--------------|------------------------------------------------|
| Logging      | Console only | Add structured logging, log rotation, external aggregation (e.g., ELK, Loki) |
| Metrics      | None         | Add metrics endpoint (e.g., Prometheus), track request/response stats, DB health |
| Health Check | None         | Implement `/healthz` and `/readyz` endpoints for liveness/readiness |
| Error Report | Console only | Integrate with Sentry or similar for backend and frontend |
| Tracing      | None         | Consider OpenTelemetry for distributed tracing  |

---

## Observability Topology

```mermaid
flowchart TD
    subgraph Frontend (Next.js)
        FE[User Browser]
        FEApp[Next.js App]
    end

    subgraph Backend (FastAPI)
        BEApp[FastAPI App]
        DB[(SQLite DB)]
    end

    FE --> FEApp
    FEApp -->|HTTP API| BEApp
    BEApp --> DB

    %% Observability flows
    BEApp -.->|Logs (stdout)| DevConsole
    BEApp -.->|Errors (stdout)| DevConsole
    FEApp -.->|Logs (stdout)| DevConsole

    classDef obs fill:#f9f,stroke:#333,stroke-width:2px;
    DevConsole[Dev Console / Hosting Logs]:::obs
```

**Legend:**
- Dashed arrows represent log/error flows to developer consoles or hosting logs.
- No explicit metrics or health check flows are present.

---

## Implementation Guidance

To improve observability for Tapestry, consider the following steps:

1. **Backend:**
   - Add a `/healthz` endpoint in [backend/app/main.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/main.py) to check API and database health.
   - Integrate Python logging with structured output (e.g., JSON) and configurable log levels.
   - Add Prometheus-compatible metrics endpoint (e.g., using `prometheus_fastapi_instrumentator`).
   - Integrate error reporting (e.g., Sentry SDK).

2. **Frontend:**
   - Use Next.js error boundaries for client-side error capture.
   - Integrate with a frontend error reporting service (e.g., Sentry).
   - Consider logging key user actions and errors to an external service.

3. **Deployment:**
   - Ensure logs are captured and rotated by the hosting environment (e.g., Vercel, Docker).
   - Monitor resource usage and uptime via external tools.

---

## Primary Sources

- [README.md](https://github.com/sergiomasellis/Tapestry/blob/main/README.md) (Last modified: 2025-08-04 19:08)
- [frontend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/README.md) (Last modified: 2025-08-04 19:08)
- [backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md) (Last modified: 2025-08-04 19:08)
- backend/pyproject.toml (Last modified: 2025-08-04 19:08)
- [frontend/package.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/package.json) (Last modified: 2025-08-04 19:08)
- [frontend/tsconfig.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/tsconfig.json) (Last modified: 2025-08-04 19:08)