# Gambit FastAPI Routing System 101

| Repo      | Doc Type | Date       | Branch |
|-----------|----------|------------|--------|
| gambit    | 101      | 2025-09-23 | main   |

## Overview

The Gambit project exposes a FastAPI-based HTTP API for interacting with its coding agent. The routing logic is primarily defined in `[main.py](https://github.com/sergiomasellis/gambit/blob/main/main.py)` and `[gambit_coding_agent/server.py](https://github.com/sergiomasellis/gambit/blob/main/gambit_coding_agent/server.py)`, providing endpoints for code explanation, messaging, status checks, and diagnostics. This document explains the system router, endpoint structure, and key implementation details.

---

## Routing Architecture

The FastAPI server is launched via:

```bash
python [main.py](https://github.com/sergiomasellis/gambit/blob/main/main.py) uv
```

This starts the API server, making endpoints available at `http://127.0.0.1:8000`.

### Entry Point: [main.py](https://github.com/sergiomasellis/gambit/blob/main/main.py)

**File:** [main.py](https://github.com/sergiomasellis/gambit/blob/main/main.py) (Last modified: 2025-09-23 08:59)

The `[main.py](https://github.com/sergiomasellis/gambit/blob/main/main.py)` file acts as the entry point for launching the server or the TUI. When run with the `uv` argument, it starts the FastAPI server:

```python
if __name__ == "__main__":
    import sys
    if sys.argv[1] == "uv":
        import uvicorn
        from gambit_coding_agent.server import app
        uvicorn.run(app, host="127.0.0.1", port=8000)
```

This imports the FastAPI `app` instance from `[gambit_coding_agent/server.py](https://github.com/sergiomasellis/gambit/blob/main/gambit_coding_agent/server.py)`.

---

### FastAPI App and Endpoints: server.py

**File:** [gambit_coding_agent/server.py](https://github.com/sergiomasellis/gambit/blob/main/gambit_coding_agent/server.py) (Last modified: 2025-09-23 08:59)

The main API logic is defined in `server.py`. The FastAPI app is created and endpoints are registered as follows:

```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/explain")
async def explain_code(request: ExplainRequest):
    # Logic to explain code

@app.post("/message")
async def send_message(request: MessageRequest):
    # Logic to handle free-form messages

@app.get("/status")
async def get_status():
    # Logic to check server and agent status

@app.get("/diagnose")
async def diagnose():
    # Logic to provide diagnostics
```

#### Endpoint Summary

- **POST /explain**: Explain a code snippet.
- **POST /message**: Send a free-form message to the agent.
- **GET /status**: Check API key and agent initialization status.
- **GET /diagnose**: Retrieve diagnostic information.

#### Example Endpoint Implementation

```python
@app.post("/explain")
async def explain_code(request: ExplainRequest):
    explanation = await agent.explain(request.code, api_key=request.api_key)
    return {"explanation": explanation}
```

---

## Endpoint Flow Diagram

```mermaid
flowchart TD
    A[Client Request] --> B{Route}
    B -- POST /explain --> C[explain_code()]
    B -- POST /message --> D[send_message()]
    B -- GET /status --> E[get_status()]
    B -- GET /diagnose --> F[diagnose()]
    C --> G[Agent Logic]
    D --> G
    E --> H[Status Info]
    F --> I[Diagnostics]
    G --> J[Response]
    H --> J
    I --> J
    J --> K[Client Response]
```

---

## Example Requests and Responses

**POST /explain**

_Request:_
```json
{
  "code": "def hello(): print('Hello, World!')",
  "api_key": "optional_override_key"
}
```
_Response:_
```json
{
  "explanation": "This function defines a simple procedure that prints 'Hello, World!' to the console."
}
```

**POST /message**

_Request:_
```json
{
  "message": "What is a Python decorator?"
}
```
_Response:_
```json
{
  "response": "A Python decorator is a design pattern..."
}
```

**GET /status**

_Response:_
```json
{
  "has_env_api_key": true,
  "agent_initialized": true
}
```

---

## Key Concepts

- **FastAPI** is used for HTTP routing and request handling.
- Endpoints are defined using decorators (`@app.post`, `@app.get`).
- The agent logic is abstracted and invoked within each endpoint.
- The server is started via `uvicorn` for ASGI compatibility.

---

## Primary Sources

- [main.py](https://github.com/sergiomasellis/gambit/blob/main/main.py) (Last modified: 2025-09-23 08:59)
- [gambit_coding_agent/server.py](https://github.com/sergiomasellis/gambit/blob/main/gambit_coding_agent/server.py) (Last modified: 2025-09-23 08:59)
- [README.md](https://github.com/sergiomasellis/gambit/blob/main/README.md) (Last modified: 2025-09-23 08:59)