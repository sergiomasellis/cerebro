# Observability and Production Readiness in Tapestry

| Repo     | Doc Type         | Date                | Branch |
|----------|------------------|---------------------|--------|
| Tapestry | Technical Guide  | 2025-08-04 19:08    | main   |

## Introduction

Production readiness for modern web applications like Tapestry—comprising a FastAPI backend and a Next.js frontend—requires robust observability. This includes logging, health checks, and basic monitoring to ensure reliability, quick troubleshooting, and smooth deployments. This document outlines how Tapestry approaches observability, with practical code snippets and architectural diagrams.

---

## Observability in FastAPI Backend

### Logging

FastAPI leverages Python’s standard logging. Proper logging is essential for tracking errors, requests, and system events.

**Example: Logging Setup in FastAPI**

```python
# [backend/app/main.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/main.py) (Last modified: 2025-08-04 19:08)
import logging
from fastapi import FastAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    logger.info("Tapestry backend starting up")
```

This setup ensures that all logs at INFO level and above are captured, and logs are emitted on application startup.

### Health Checks

A health check endpoint allows orchestration platforms (like Kubernetes) and uptime monitors to verify that the backend is alive and responsive.

**Example: Health Check Endpoint**

```python
# [backend/app/main.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/main.py) (Last modified: 2025-08-04 19:08)
from fastapi import APIRouter

router = APIRouter()

@router.get("/healthz")
async def health_check():
    return {"status": "ok"}
```

This endpoint can be expanded to check database connectivity or external dependencies.

### Error Handling

FastAPI supports custom exception handlers for structured error reporting.

```python
# [backend/app/main.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/main.py) (Last modified: 2025-08-04 19:08)
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi import status

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )
```

---

## Observability in Next.js Frontend

### Logging

In the browser, logging is typically done via `console.log`, but for production, logs should be sent to a remote service.

**Example: Client-side Logging Utility**

```typescript
// [frontend/src/lib/utils.ts](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/src/lib/utils.ts) (Last modified: 2025-08-04 19:08)
export function logEvent(event: string, data?: any) {
  if (process.env.NODE_ENV !== "production") {
    console.log(`[Tapestry] ${event}`, data);
  }
  // In production, send to remote logging endpoint
}
```

### Health Checks

For frontend deployments (e.g., on Vercel), health is often inferred from the ability to serve the root page. Optionally, a `/healthz` route can be added to the Next.js app for explicit checks.

**Example: Simple Health Route**

```typescript
// frontend/src/app/healthz/page.tsx (pseudo-code)
export default function Healthz() {
  return <div>{"status": "ok"}</div>;
}
```

---

## Monitoring and Alerts

- **Backend**: Integrate with tools like Prometheus, Grafana, or Sentry for metrics and error tracking.
- **Frontend**: Use services like Vercel Analytics, Sentry, or LogRocket for error and performance monitoring.

---

## System Observability Diagram

```mermaid
flowchart TD
  subgraph Frontend [Next.js Frontend]
    F1[User Browser]
    F2[Next.js App]
    F1 --> F2
  end

  subgraph Backend [FastAPI Backend]
    B1[FastAPI App]
    B2[Logging (stdout/file)]
    B3[Health Check /healthz]
    B1 --> B2
    B1 --> B3
  end

  F2 -- API Calls --> B1
  B1 -- Logs --> B2
  B1 -- Health Status --> B3

  subgraph Monitoring
    M1[Sentry/Prometheus]
  end

  B2 -- Error/Metric Export --> M1
  F2 -- Frontend Error Export --> M1
```

---

## Example: Production-Ready FastAPI Startup

```python
# [backend/app/main.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/main.py) (Last modified: 2025-08-04 19:08)
import logging
from fastapi import FastAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("tapestry")

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    logger.info("Tapestry backend started.")

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}
```

---

## Example: Next.js Logging Utility

```typescript
// [frontend/src/lib/utils.ts](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/src/lib/utils.ts) (Last modified: 2025-08-04 19:08)
export function logEvent(event: string, data?: any) {
  if (process.env.NODE_ENV !== "production") {
    console.log(`[Tapestry] ${event}`, data);
  }
}
```

---

## Recommendations

- **Backend**: Always expose a `/healthz` endpoint and configure logging to include timestamps and log levels.
- **Frontend**: Use a logging utility and consider integrating a browser error reporting service.
- **Both**: Document observability endpoints and logging conventions in your README for contributors and operators.

---

## Primary Sources

- [README.md](https://github.com/sergiomasellis/Tapestry/blob/main/README.md) (Last modified: 2025-08-04 19:08)
- [backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md) (Last modified: 2025-08-04 19:08)
- [backend/app/main.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/main.py) (Last modified: 2025-08-04 19:08)
- [frontend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/README.md) (Last modified: 2025-08-04 19:08)
- [frontend/src/lib/utils.ts](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/src/lib/utils.ts) (Last modified: 2025-08-04 19:08)
- [frontend/package.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/package.json) (Last modified: 2025-08-04 19:08)