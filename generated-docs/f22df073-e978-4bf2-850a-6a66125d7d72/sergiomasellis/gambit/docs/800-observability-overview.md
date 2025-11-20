# Observability and Diagnostics in Gambit

| Repo      | Doc Type      | Date                | Branch |
|-----------|--------------|---------------------|--------|
| gambit    | Technical Doc | 2025-09-23 08:59    | main   |

## Overview

Observability is a critical aspect of the Gambit coding agent, enabling users and developers to monitor system health, diagnose issues, and ensure reliable operation. Gambit provides dedicated API endpoints for diagnostics and health checks, leverages logging and metrics, and is designed for easy integration with modern observability stacks.

This document describes the observability features of Gambit, focusing on the `/diagnose` and `/status` endpoints, logging, and health check mechanisms.

---

## Health and Diagnostic Endpoints

Gambit exposes two primary endpoints for observability:

- **GET /status**: Returns the basic health status of the server, including API key presence and agent initialization.
- **GET /diagnose**: Returns diagnostic information for troubleshooting.

These endpoints are implemented in the FastAPI server and are intended for both human and automated consumption.

### Example: `/status` Endpoint

From [README.md](https://github.com/sergiomasellis/gambit/blob/main/README.md) (Last modified: 2025-09-23 08:59):

```json
{
  "has_env_api_key": true,
  "agent_initialized": true
}
```

This endpoint allows you to quickly verify that the environment is correctly configured and the agent is ready to serve requests.

### Example: `/diagnose` Endpoint

The `/diagnose` endpoint provides deeper diagnostic information, which may include environment variables, dependency versions, and other runtime details useful for debugging.

---

## Observability Architecture

Below is a high-level diagram of how observability is integrated into Gambit:

```mermaid
flowchart TD
    User[User / Monitoring System]
    subgraph Gambit FastAPI Server
        S1[/status endpoint/]
        S2[/diagnose endpoint/]
        LOGS[Logging]
        METRICS[Metrics (future)]
    end
    User -- HTTP GET /status --> S1
    User -- HTTP GET /diagnose --> S2
    S1 -- Health JSON --> User
    S2 -- Diagnostics JSON --> User
    S1 & S2 -- Log events --> LOGS
    LOGS -- Log output --> User
```

---

## Logging

Gambit uses Python's standard logging facilities (see [gambit_coding_agent/server.py](https://github.com/sergiomasellis/gambit/blob/main/gambit_coding_agent/server.py), Last modified: 2025-09-23 08:59) to record key events, errors, and diagnostics. Logs are emitted for:

- Server startup and shutdown
- Endpoint access and errors
- Agent initialization and failures

Example snippet ([gambit_coding_agent/server.py](https://github.com/sergiomasellis/gambit/blob/main/gambit_coding_agent/server.py)):

```python
import logging

logger = logging.getLogger("gambit.server")

@app.get("/status")
async def status():
    logger.info("Status endpoint called")
    return {"has_env_api_key": True, "agent_initialized": True}
```

Logs can be directed to stdout, files, or external log aggregation systems, depending on deployment configuration.

---

## Metrics

While Gambit does not currently export Prometheus or OpenTelemetry metrics by default, its FastAPI foundation and modular design make it straightforward to add such integrations. Metrics can include:

- Request counts and latencies for `/status` and `/diagnose`
- Error rates
- Agent response times

For advanced observability, consider wrapping endpoints with middleware or using FastAPI-compatible metrics libraries.

---

## Health Check Integration

The `/status` endpoint is suitable for use as a Kubernetes or cloud-native health check. It returns a simple JSON payload indicating readiness and configuration status.

Example usage ([README.md](https://github.com/sergiomasellis/gambit/blob/main/README.md)):

```bash
curl http://127.0.0.1:8000/status
```

Response:

```json
{
  "has_env_api_key": true,
  "agent_initialized": true
}
```

---

## Example: Adding a Custom Diagnostic

To extend diagnostics, you can add more fields to the `/diagnose` endpoint in `[gambit_coding_agent/server.py](https://github.com/sergiomasellis/gambit/blob/main/gambit_coding_agent/server.py)`:

```python
@app.get("/diagnose")
async def diagnose():
    import sys
    return {
        "python_version": sys.version,
        "dependencies": list(sys.modules.keys()),
        "env": dict(os.environ),
    }
```

This approach provides richer context for debugging and support.

---

## Continuous Integration and Observability

The GitHub Actions workflow (.github/workflows/python-app.yml, Last modified: 2025-09-23 08:59) ensures that tests and linting are run on every push to the `main` branch. This CI pipeline is an important part of operational observability, catching regressions and code quality issues early.

```yaml
- name: Test with pytest
  run: |
    pytest
```

---

## Summary

Gambit provides robust observability out of the box via:

- `/status` and `/diagnose` endpoints for health and diagnostics
- Logging of key events and errors
- Easy extensibility for metrics and advanced diagnostics
- CI/CD integration for operational visibility

These features make Gambit suitable for production deployment and easy to monitor in modern environments.

---

## Primary Sources

- [README.md](https://github.com/sergiomasellis/gambit/blob/main/README.md) (Last modified: 2025-09-23 08:59)
- [gambit_coding_agent/server.py](https://github.com/sergiomasellis/gambit/blob/main/gambit_coding_agent/server.py) (Last modified: 2025-09-23 08:59)
- .github/workflows/python-app.yml (Last modified: 2025-09-23 08:59)
- pyproject.toml (Last modified: 2025-09-23 08:59)