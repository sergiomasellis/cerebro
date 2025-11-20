# Gambit REST API Endpoints

| Repo    | Doc Type         | Date       |
|---------|------------------|------------|
| gambit  | REST API (311)   | 2024-06-12 |

This document provides an overview of the REST API endpoints exposed by the Gambit Coding Agent. The API is implemented using FastAPI and is designed for code explanation, coding Q&A, and agent diagnostics.

---

## API Endpoints Overview

| Method | Path        | Purpose / Description                                 | Request Body Example | Response Example |
|--------|-------------|-------------------------------------------------------|----------------------|------------------|
| POST   | `/explain`  | Explain a code snippet using the coding agent         | `{ "code": "def hello(): print('Hello, World!')", "api_key": "optional_override_key" }` | `{ "explanation": "This function defines a simple procedure that prints 'Hello, World!' to the console." }` |
| POST   | `/message`  | Send a free-form message (coding Q&A, etc.)           | `{ "message": "What is a Python decorator?" }` | `{ "response": "A Python decorator is a design pattern..." }` |
| GET    | `/status`   | Check server status (API key presence, agent ready)   | _None_               | `{ "has_env_api_key": true, "agent_initialized": true }` |
| GET    | `/diagnose` | Retrieve diagnostic information for troubleshooting    | _None_               | `{ ...diagnostic info... }` |

---

## Endpoint Details

### POST `/explain`

- **Purpose:** Get an explanation for a provided code snippet.
- **Request Body:**
  ```json
  {
    "code": "def hello(): print('Hello, World!')",
    "api_key": "optional_override_key"
  }
  ```
  - `code` (string, required): The code to explain.
  - `api_key` (string, optional): Override the default API key.
- **Response:**
  ```json
  {
    "explanation": "This function defines a simple procedure that prints 'Hello, World!' to the console."
  }
  ```

---

### POST `/message`

- **Purpose:** Send a free-form message to the agent (e.g., coding questions).
- **Request Body:**
  ```json
  {
    "message": "What is a Python decorator?"
  }
  ```
  - `message` (string, required): The user's question or message.
- **Response:**
  ```json
  {
    "response": "A Python decorator is a design pattern..."
  }
  ```

---

### GET `/status`

- **Purpose:** Check server status regarding API key and agent initialization.
- **Response:**
  ```json
  {
    "has_env_api_key": true,
    "agent_initialized": true
  }
  ```
  - `has_env_api_key` (bool): Whether an API key is set in the environment.
  - `agent_initialized` (bool): Whether the agent is ready to handle requests.

---

### GET `/diagnose`

- **Purpose:** Retrieve diagnostic information for troubleshooting.
- **Response:**  
  Diagnostic details (structure may vary), e.g.:
  ```json
  {
    "env": { "OPENROUTER_API_KEY": true },
    "agent_status": "ready",
    "tools_available": ["execute_command_tool", "read_file_tool", ...]
  }
  ```

---

## REST API Topology

```mermaid
graph TD
    Client[Client (curl, Postman, etc.)]
    subgraph Gambit FastAPI Server
        A[/explain/]
        B[/message/]
        C[/status/]
        D[/diagnose/]
    end
    Client --> A
    Client --> B
    Client --> C
    Client --> D
```

---

## Usage Notes

- The API expects JSON request bodies for POST endpoints.
- The agent can use tools for file operations and command execution (see [README.md](README.md) for details).
- API key can be set via `.env` or per-request override.

---

## Primary Sources

- [README.md](README.md)
- [gambit_coding_agent/server.py](gambit_coding_agent/server.py)
