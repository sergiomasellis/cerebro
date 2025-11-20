# Gambit Agent Runbook: Debugging, Restart, and Troubleshooting

| Repo      | Doc Type      | Date                | Branch |
|-----------|--------------|---------------------|--------|
| gambit    | Runbook Guide | 2025-09-23 08:59    | main   |

This runbook provides operational guidance for running, debugging, and troubleshooting the Gambit Coding Agent. It covers the agent’s operational endpoints (notably `/diagnose`), restart procedures, and common troubleshooting steps for both the FastAPI server and the agent’s toolchain.

---

## Overview

Gambit is a lightweight coding agent powered by LangChain and OpenAI-compatible APIs. It exposes a FastAPI server with endpoints for code explanation, messaging, and diagnostics. The agent can also be run via a Textual TUI or CLI.

**Key operational files:**
- [main.py](https://github.com/sergiomasellis/gambit/blob/main/main.py)
- [gambit_coding_agent/server.py](https://github.com/sergiomasellis/gambit/blob/main/gambit_coding_agent/server.py)
- [gambit_coding_agent/agent.py](https://github.com/sergiomasellis/gambit/blob/main/gambit_coding_agent/agent.py)
- [gambit_coding_agent/tools.py](https://github.com/sergiomasellis/gambit/blob/main/gambit_coding_agent/tools.py)

---

## Operational Endpoints

### `/diagnose` Endpoint

The `/diagnose` endpoint is designed for runtime diagnostics and troubleshooting. It provides information about the agent’s environment, API key status, and initialization state.

**Example request:**
```bash
curl http://127.0.0.1:8000/diagnose
```

**Example response:**
```json
{
  "has_env_api_key": true,
  "agent_initialized": true
}
```

- `has_env_api_key`: Indicates if the agent can access the required API key from the environment.
- `agent_initialized`: Confirms whether the agent has been successfully initialized.

---

## Restart Procedures

### Restarting the FastAPI Server

If the agent becomes unresponsive or `/diagnose` reports issues, restart the server:

```bash
python [main.py](https://github.com/sergiomasellis/gambit/blob/main/main.py) uv
```

Or, if installed as a CLI tool:
```bash
gambit uv
```

**On Windows (using PowerShell):**
```powershell
python [main.py](https://github.com/sergiomasellis/gambit/blob/main/main.py) uv
```

### Restarting the TUI

To restart the Textual TUI interface:
```bash
python [main.py](https://github.com/sergiomasellis/gambit/blob/main/main.py) tui
```

---

## Troubleshooting Steps

### 1. API Key Issues

If `/diagnose` reports `has_env_api_key: false`:

- Ensure a `.env` file exists in the project root with:
  ```
  OPENROUTER_API_KEY=your_api_key_here
  ```
- Restart the server after updating the `.env` file.

### 2. Agent Initialization Failures

If `agent_initialized: false`:

- Check for errors in the server logs (look for stack traces or import errors).
- Ensure all dependencies are installed:
  ```bash
  uv sync
  # or
  pip install -e .
  ```

### 3. Dependency Problems

If startup fails due to missing packages:

- Confirm your Python version is >=3.12.
- Install dependencies as specified in `pyproject.toml` (Last modified: 2025-09-23 08:59):

```toml
[project]
dependencies = [
     "fastapi>=0.117.1",
     "langchain[openai]>=0.3.27",
     "langgraph>=0.6.7",
     "openai>=1.108.1",
     "pydantic>=2.11.9",
     "python-dotenv>=1.1.1",
     "rich>=14.1.0",
     "setuptools>=80.9.0",
     "textual>=6.1.0",
     "uvicorn[standard]>=0.36.0",
     "pytest>=8.0.0",
     "ripgrep>=14.1.0",
]
```

### 4. Testing the Agent

Run the test suite to verify installation and agent health:
```bash
pytest
```

Or for a specific test:
```bash
pytest [tests/test_agent.py](https://github.com/sergiomasellis/gambit/blob/main/tests/test_agent.py)::test_some_function
```

---

## Key Operational Code Snippets

**FastAPI Server Entrypoint ([main.py](https://github.com/sergiomasellis/gambit/blob/main/main.py), Last modified: 2025-09-23 08:59):**
```python
if __name__ == "__main__":
    import sys
    if sys.argv[1] == "uv":
        import uvicorn
        uvicorn.run("gambit_coding_agent.server:app", host="127.0.0.1", port=8000, reload=True)
    elif sys.argv[1] == "tui":
        from gambit_coding_agent.tui import main as tui_main
        tui_main()
```

**Server Diagnostics Endpoint ([gambit_coding_agent/server.py](https://github.com/sergiomasellis/gambit/blob/main/gambit_coding_agent/server.py)):**
```python
@app.get("/diagnose")
def diagnose():
    return {
        "has_env_api_key": bool(os.getenv("OPENROUTER_API_KEY")),
        "agent_initialized": agent.is_initialized(),
    }
```

**Agent Initialization Check ([gambit_coding_agent/agent.py](https://github.com/sergiomasellis/gambit/blob/main/gambit_coding_agent/agent.py)):**
```python
def is_initialized(self):
    return self.llm is not None and self.tools is not None
```

---

## Common Issues & Solutions

| Symptom                                 | Possible Cause                  | Solution                                      |
|------------------------------------------|---------------------------------|------------------------------------------------|
| `/diagnose` shows `has_env_api_key: false` | Missing or misnamed `.env` file | Add `.env` with correct key, restart server    |
| `/diagnose` shows `agent_initialized: false` | Dependency or import error      | Check logs, reinstall dependencies             |
| Server fails to start                   | Python version or missing deps  | Use Python >=3.12, install via `uv sync`       |
| Agent tools not working                 | File permissions or OS issues   | Check file paths, permissions, OS compatibility |

---

## Gambit Agent Operational Flow

```mermaid
flowchart TD
    A[Start Server] --> B{API Key Present?}
    B -- No --> C[Fail: Check .env]
    B -- Yes --> D[Initialize Agent]
    D --> E{Agent Initialized?}
    E -- No --> F[Fail: Check Dependencies/Logs]
    E -- Yes --> G[Ready for Requests]
    G --> H[/diagnose, /explain, /message]
```

---

## Primary Sources

- [README.md](https://github.com/sergiomasellis/gambit/blob/main/README.md) (Last modified: 2025-09-23 08:59)
- pyproject.toml (Last modified: 2025-09-23 08:59)
- [setup.py](https://github.com/sergiomasellis/gambit/blob/main/setup.py) (Last modified: 2025-09-23 08:59)
- .github/workflows/python-app.yml (Last modified: 2025-09-23 08:59)
- [gambit_coding_agent/server.py](https://github.com/sergiomasellis/gambit/blob/main/gambit_coding_agent/server.py)
- [gambit_coding_agent/agent.py](https://github.com/sergiomasellis/gambit/blob/main/gambit_coding_agent/agent.py)