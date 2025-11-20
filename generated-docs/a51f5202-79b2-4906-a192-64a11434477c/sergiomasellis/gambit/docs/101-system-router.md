# Gambit System Router 101

| Repo   | Doc Type         | Date       |
|--------|------------------|------------|
| gambit | System Router 101 | 2024-06-13 |

---

## Overview

This document details the system entrypoints and routing logic for the Gambit Coding Agent. It covers how commands and API requests are routed to their respective handlers, including CLI, TUI, and FastAPI server entrypoints.

---

## Entrypoints

### 1. CLI Entrypoint

- **Executable:** `gambit` (via `setup.py` and `pyproject.toml`)
- **Shim Scripts:** `gambit.ps1`, `gambit.cmd`
- **Module:** `gambit_coding_agent.cli:main`

**How it works:**
- The CLI entrypoint is registered via both `setup.py` and `pyproject.toml` under `console_scripts` and `[project.scripts]`.
- Running `gambit ...` or `python -m gambit_coding_agent.cli ...` invokes the `main()` function in `gambit_coding_agent/cli.py`.
- The CLI parses arguments (e.g., `-m "message"`) and dispatches to agent logic.

### 2. Python Main Entrypoint

- **File:** `main.py`
- **Usage:** `python main.py [tui|uv]`

**How it works:**
- `main.py` acts as a multiplexer for two main modes:
    - `tui`: Launches the Textual-based terminal UI (`gambit_coding_agent/tui.py`)
    - `uv`: Starts the FastAPI server (`gambit_coding_agent/server.py`)
- The mode is determined by the first command-line argument.

### 3. FastAPI Server Entrypoint

- **Module:** `gambit_coding_agent/server.py`
- **Startup:** Invoked via `main.py uv` or directly with `uvicorn gambit_coding_agent.server:app`
- **Framework:** FastAPI

**How it works:**
- Defines the HTTP API surface for agent interaction.
- Exposes endpoints such as `/explain`, `/message`, `/status`, and `/diagnose`.
- Handles JSON requests and responses.

---

## Routing Logic

### CLI Routing

- The CLI entrypoint (`gambit_coding_agent.cli:main`) parses command-line arguments.
- Depending on the flags and arguments, it routes the request to agent logic (e.g., sending a message, explaining code).

### Main.py Routing

- `main.py` inspects `sys.argv`:
    - If `tui`, imports and runs `gambit_coding_agent.tui`.
    - If `uv`, imports and runs `gambit_coding_agent.server`.
    - Otherwise, prints usage/help.

### FastAPI Routing

- `gambit_coding_agent/server.py` defines FastAPI routes:
    - `POST /explain` → Explains code snippets.
    - `POST /message` → Handles general agent messages.
    - `GET /status` → Reports API key and agent status.
    - `GET /diagnose` → Returns diagnostic info.

---

## Routing Topology Diagram

```mermaid
flowchart TD
    A[User] -->|CLI: gambit ...| B(gambit_coding_agent.cli:main)
    A -->|python main.py tui| C(gambit_coding_agent.tui)
    A -->|python main.py uv| D(gambit_coding_agent.server)
    A -->|gambit.ps1 / gambit.cmd| B
    D -->|FastAPI| E[/explain, /message, /status, /diagnose]
```

---

## Summary Table

| Entrypoint           | How to Invoke                        | Routes/Handlers                                      |
|----------------------|--------------------------------------|------------------------------------------------------|
| CLI                  | `gambit ...`<br>`gambit.ps1 ...`     | `gambit_coding_agent.cli:main`                       |
| TUI                  | `python main.py tui`                 | `gambit_coding_agent.tui`                            |
| FastAPI Server       | `python main.py uv`<br>`uvicorn ...` | `gambit_coding_agent.server`<br>FastAPI endpoints    |

---

## Primary Sources

- `main.py`
- `gambit_coding_agent/server.py`
- `gambit_coding_agent/cli.py`
- `setup.py`
- `pyproject.toml`
- `gambit.ps1`
- `gambit.cmd`
- `README.md`