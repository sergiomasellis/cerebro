# Observability Overview

| Repo      | Doc Type             | Date                | Branch |
|-----------|---------------------|---------------------|--------|
| Tapestry  | Observability (800) | 2025-08-04 19:08    | main   |

---

## Introduction

Observability in Tapestry ensures that both the backend (FastAPI) and frontend (Next.js) are transparent, diagnosable, and production-ready. This document outlines the logging, metrics, and health check strategies implemented or recommended for the Tapestry application, referencing the current codebase and best practices for each stack.

---

## Backend Observability (FastAPI)

### Logging

- **Default Logging**: FastAPI (via Uvicorn) provides structured access and error logs out-of-the-box.
- **Custom Logging**: For more granular logs (e.g., business events, warnings), Python's `logging` module should be configured in `[backend/app/main.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/main.py)` or via Uvicorn CLI flags.
- **Log Levels**: INFO for routine operations, WARNING/ERROR for failures, DEBUG for development.
- **Log Sinks**: By default, logs are output to stdout/stderr. For production, consider log aggregation (e.g., Loki, ELK, or cloud logging).

**Example log output:**
```
INFO:     127.0.0.1:54321 - "POST /api/chores/complete HTTP/1.1" 200 OK
ERROR:    Chore assignment failed for user_id=42: NotFound
```

### Health Checks

- **Liveness/Readiness**: Implement a `/health` or `/status` endpoint in `[backend/app/main.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/main.py)` to report:
  - Database connectivity (e.g., test a simple query)
  - Application status (e.g., FastAPI running)
- **OpenAPI Docs**: FastAPI auto-generates `/docs` and `/openapi.json` endpoints for API inspection.

**Recommended Implementation:**
```python
@app.get("/health")
def health_check():
    try:
        db.execute("SELECT 1")
        return {"status": "ok"}
    except Exception:
        return JSONResponse(status_code=503, content={"status": "error"})
```

### Metrics

- **Uvicorn/FastAPI**: Native support for Prometheus metrics is not included, but can be added via [prometheus-fastapi-instrumentator](https://github.com/trallnag/prometheus-fastapi-instrumentator).
- **Key Metrics**:
  - Request count, latency, error rate
  - Database query times
  - Chore/point/goal event counts

### Error Reporting

- **Unhandled Exceptions**: FastAPI returns JSON error responses with stack traces in development.
- **Production**: Integrate with Sentry or similar for error aggregation.

---

## Frontend Observability (Next.js)

### Logging

- **Client-Side**: Use `console.log`, `console.error` for development. For production, integrate a browser logging service (e.g., Sentry, LogRocket).
- **Server-Side (SSR)**: Next.js logs server errors to stdout/stderr. These can be captured by the hosting platform (e.g., Vercel, Docker logs).

### Health Checks

- **Static Health**: The frontend is static/SSR; health is typically inferred from HTTP 200 responses.
- **Custom Health Endpoint**: Optionally, expose `/api/health` in Next.js (via API routes) to check SSR and backend connectivity.

### Metrics

- **Performance**: Next.js provides [Web Vitals](https://nextjs.org/docs/advanced-features/measuring-performance) (LCP, FID, CLS) via built-in reporting hooks.
- **Custom Metrics**: Integrate with analytics (e.g., Google Analytics, Vercel Analytics) for user behavior and performance.

### Error Reporting

- **Error Boundaries**: Use React error boundaries to catch and report UI errors.
- **Monitoring**: Integrate with Sentry or similar for both client and server errors.

---

## Observability Topology

```mermaid
flowchart TD
    subgraph Backend (FastAPI)
        A1[Uvicorn Logs]
        A2[Custom Logging]
        A3[Health Endpoint /health]
        A4[Prometheus Metrics (optional)]
        A5[Sentry (optional)]
    end

    subgraph Frontend (Next.js)
        B1[Console Logs]
        B2[Web Vitals]
        B3[Error Boundaries]
        B4[Sentry/LogRocket (optional)]
        B5[API Route /api/health (optional)]
    end

    A1 -->|stdout| C[Log Aggregator (optional)]
    A2 -->|stdout| C
    A3 -->|HTTP| D[Monitoring System]
    A4 -->|metrics| E[Prometheus/Grafana]
    A5 -->|errors| F[Sentry Dashboard]

    B1 -->|console| G[Browser DevTools]
    B2 -->|metrics| H[Analytics Platform]
    B3 -->|errors| F
    B4 -->|logs/errors| F
    B5 -->|HTTP| D

    D -.->|alerts| Ops[Ops/Oncall]
    E -.->|dashboards| Ops
    F -.->|alerts| Ops
```

---

## Recommendations

- **Implement `/health` endpoints** in both backend and frontend for liveness/readiness probes.
- **Configure log levels and formats** for clarity and aggregation.
- **Integrate metrics** (Prometheus or similar) for backend API monitoring.
- **Adopt error reporting** (e.g., Sentry) for both backend and frontend.
- **Document log/metric retention and alerting policies** for production.

---

## Primary Sources

- [[README.md](https://github.com/sergiomasellis/Tapestry/blob/main/README.md)](./[README.md](https://github.com/sergiomasellis/Tapestry/blob/main/README.md)) (Last modified: 2025-08-04 19:08)
- [[backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md)](./[backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md)) (Last modified: 2025-08-04 19:08)
- [backend/pyproject.toml](./backend/pyproject.toml) (Last modified: 2025-08-04 19:08)
- [[frontend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/README.md)](./[frontend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/README.md)) (Last modified: 2025-08-04 19:08)
- [[frontend/package.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/package.json)](./[frontend/package.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/package.json)) (Last modified: 2025-08-04 19:08)
- [[frontend/tsconfig.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/tsconfig.json)](./[frontend/tsconfig.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/tsconfig.json)) (Last modified: 2025-08-04 19:08)