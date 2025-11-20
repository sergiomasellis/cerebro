# Gambit Coding Agent: Runbook Operations

| Repo      | Doc Type         | Date         |
|-----------|------------------|--------------|
| gambit    | Runbook (850)    | 2024-06-11   |

---

This runbook provides operational guidance for running, monitoring, troubleshooting, and recovering the Gambit Coding Agent system. It covers typical failure modes, diagnostic procedures, and safe restart instructions for both the FastAPI server and CLI/TUI interfaces.

---

## 1. System Overview

Gambit is a coding agent powered by LangChain and OpenAI-compatible APIs (via OpenRouter). It exposes:

- A **FastAPI server** (`main.py uv`) with endpoints for code explanation, messaging, status, and diagnostics.
- A **Textual TUI** (`main.py tui`) for interactive chat.
- A **CLI** (`gambit` command or shims) for direct messaging.

The agent uses tools for file and command operations, and requires an OpenRouter API key (set via `.env`).

---

## 2. Operational Modes

| Mode         | Command Example                | Description                                 |
|--------------|-------------------------------|---------------------------------------------|
| API Server   | `python main.py uv`           | Starts FastAPI server at http://127.0.0.1:8000 |
| TUI          | `python main.py tui`          | Launches interactive Textual UI             |
| CLI          | `gambit -m "message"`         | Sends message via CLI                       |
| PowerShell   | `.\gambit.ps1 -m "message"`   | Windows PowerShell shim                     |
| CMD          | `.\gambit.cmd -m "message"`   | Windows CMD shim                            |

---

## 3. Health & Diagnostics

### 3.1. Status Endpoint

- **GET /status**
  - Checks if the API key is loaded and agent is initialized.
  - Example response:
    ```json
    {
      "has_env_api_key": true,
      "agent_initialized": true
    }
    ```

### 3.2. Diagnostic Endpoint

- **GET /diagnose**
  - Returns deeper diagnostic info (implementation-dependent).
  - Use this endpoint to gather troubleshooting data.

### 3.3. Logs

- The server and CLI output logs to stdout/stderr.
- For more verbose logs, run with increased verbosity if supported (see `README.md` or code for options).

---

## 4. Failure Modes & Troubleshooting

### 4.1. Startup Failures

| Symptom                          | Likely Cause                     | Resolution                                  |
|-----------------------------------|----------------------------------|---------------------------------------------|
| `OPENROUTER_API_KEY` missing      | No `.env` or key not set         | Create `.env` with correct key              |
| `ModuleNotFoundError`             | Missing dependencies             | Run `uv sync` or `pip install -e .`         |
| Port 8000 in use                  | Another process on port 8000     | Kill process or change port in code         |
| Permission denied (file ops)      | Insufficient OS permissions      | Run as user with required access            |

### 4.2. API Key Issues

- **Symptom:** All API calls fail with authentication errors.
- **Action:** Check `.env` for `OPENROUTER_API_KEY`. Validate the key at [OpenRouter](https://openrouter.ai).

### 4.3. Agent Not Responding

- **Symptom:** `/status` shows `"agent_initialized": false` or requests hang.
- **Action:** Restart the server. Check logs for stack traces or initialization errors.

### 4.4. Tool Failures

- **Symptom:** File or command tools return errors.
- **Action:** Check file paths, permissions, and command syntax. Ensure the agent process has access to the relevant directories.

### 4.5. TUI/CLI Issues

- **Symptom:** TUI does not launch, or CLI returns errors.
- **Action:** Ensure dependencies are installed. Try running with `python main.py tui` or `gambit -m "message"` in an activated virtual environment.

---

## 5. Restart & Recovery Procedures

### 5.1. Restarting the FastAPI Server

1. **Stop the server**: Press `Ctrl+C` in the terminal running `python main.py uv`.
2. **Check for lingering processes**: Ensure no orphaned processes are holding port 8000.
3. **Start the server**: Run `python main.py uv` again.

### 5.2. Restarting the TUI

1. **Stop the TUI**: Press `Ctrl+C` or close the window.
2. **Start the TUI**: Run `python main.py tui`.

### 5.3. Restarting the CLI

- No persistent process; simply re-run the `gambit` command.

---

## 6. Environment & Configuration

- **API Key**: Set `OPENROUTER_API_KEY` in `.env` at the project root.
- **Dependencies**: Managed via `pyproject.toml`. Install with `uv sync` or `pip install -e .`.
- **Virtual Environment**: Strongly recommended for isolation.

---

## 7. Debugging Checklist

1. **Check `/status` and `/diagnose` endpoints** for server health.
2. **Review logs** for errors or stack traces.
3. **Validate `.env`** for correct API key.
4. **Test with CLI**: `gambit -m "Hello"`
5. **Test with TUI**: `python main.py tui`
6. **Test API endpoints** with `curl` or Postman.
7. **Run tests**: `pytest`

---

## 8. Escalation

If issues persist after following this runbook:

- Gather logs and diagnostic output.
- Document steps taken and observed symptoms.
- Escalate to the development team with all collected information.

---

## Primary Sources

- [README.md](README.md)
- [pyproject.toml](pyproject.toml)
- [setup.py](setup.py)
- [main.py](main.py)
- [gambit.ps1](gambit.ps1)
- [gambit.cmd](gambit.cmd)
- [.github/workflows/python-app.yml](.github/workflows/python-app.yml)

---