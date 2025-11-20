# Gambit Architecture Overview

| Repo   | Doc Type      | Date       | Branch |
|--------|--------------|------------|--------|
| gambit | Architecture | 2025-09-23 | main   |

---

This document provides a high-level architectural overview of the Gambit coding agent project. It explains the main components, their interactions, and how the system is structured to support multiple interfaces (FastAPI server, TUI, CLI), agent logic, and tool integration.

## System Components

Gambit is designed as a modular, extensible coding agent platform. Its core components are:

- **FastAPI Server**: Provides HTTP endpoints for code explanation, messaging, and diagnostics.
- **Textual TUI**: An interactive terminal UI for chatting with the agent.
- **CLI**: Command-line interface for scripting and quick queries.
- **Agent Logic**: The core reasoning and orchestration, powered by LangChain and OpenAI-compatible APIs.
- **Tool Integration**: Safe, extensible tools for file and command operations.

Below is a diagram and detailed explanation of each component.

## High-Level Architecture

```mermaid
flowchart TD
    subgraph Interfaces
        A1[CLI ([gambit_coding_agent/cli.py](https://github.com/sergiomasellis/gambit/blob/main/gambit_coding_agent/cli.py))]
        A2[TUI ([gambit_coding_agent/tui.py](https://github.com/sergiomasellis/gambit/blob/main/gambit_coding_agent/tui.py))]
        A3[FastAPI Server ([gambit_coding_agent/server.py](https://github.com/sergiomasellis/gambit/blob/main/gambit_coding_agent/server.py))]
    end
    subgraph Core
        B1[Agent Logic ([gambit_coding_agent/agent.py](https://github.com/sergiomasellis/gambit/blob/main/gambit_coding_agent/agent.py))]
        B2[Tools ([gambit_coding_agent/tools.py](https://github.com/sergiomasellis/gambit/blob/main/gambit_coding_agent/tools.py))]
    end
    subgraph Prompts
        C1[System, Init, Todo (prompts/*.prompt.md)]
    end

    A1 --> B1
    A2 --> B1
    A3 --> B1
    B1 --> B2
    B1 --> C1
    A3 -.->|HTTP| User
    A2 -.->|Text UI| User
    A1 -.->|Shell| User
```

### 1. Interfaces

#### FastAPI Server (`[gambit_coding_agent/server.py](https://github.com/sergiomasellis/gambit/blob/main/gambit_coding_agent/server.py)`)
- Exposes endpoints such as `/explain`, `/message`, `/status`, and `/diagnose`.
- Handles JSON requests and responses for code explanations and agent queries.

**Example (from [README.md](https://github.com/sergiomasellis/gambit/blob/main/README.md), Last modified: 2025-09-23 08:59):**
```json
POST /explain
{
  "code": "def hello(): print('Hello, World!')"
}
```

#### Textual TUI (`[gambit_coding_agent/tui.py](https://github.com/sergiomasellis/gambit/blob/main/gambit_coding_agent/tui.py)`)
- Provides an interactive terminal-based UI using the `textual` library.
- Allows users to chat with the agent in real-time.

#### CLI (`[gambit_coding_agent/cli.py](https://github.com/sergiomasellis/gambit/blob/main/gambit_coding_agent/cli.py)`)
- Offers a scriptable command-line interface.
- Entry point is registered via both `[setup.py](https://github.com/sergiomasellis/gambit/blob/main/setup.py)` and `pyproject.toml`:

**[setup.py](https://github.com/sergiomasellis/gambit/blob/main/setup.py) (Last modified: 2025-09-23 08:59):**
```python
entry_points={
    "console_scripts": [
        "gambit=gambit_coding_agent.cli:main",
    ]
}
```

**pyproject.toml (Last modified: 2025-09-23 08:59):**
```
[project.scripts]
gambit = "gambit_coding_agent.cli:main"
```

### 2. Core

#### Agent Logic (`[gambit_coding_agent/agent.py](https://github.com/sergiomasellis/gambit/blob/main/gambit_coding_agent/agent.py)`)
- Implements the main reasoning loop.
- Integrates with LangChain, OpenAI-compatible APIs, and orchestrates tool usage.
- Loads system and task prompts from the `prompts/` directory.

#### Tool Integration (`[gambit_coding_agent/tools.py](https://github.com/sergiomasellis/gambit/blob/main/gambit_coding_agent/tools.py)`)
- Defines tools for file operations and command execution.
- Tools are invoked by the agent as needed to fulfill user requests.

**Available Tools (from [README.md](https://github.com/sergiomasellis/gambit/blob/main/README.md)):**
- `execute_command_tool`: Run shell commands.
- `read_file_tool`: Read file contents.
- `write_file_tool`: Write to files.
- `list_directory_tool`: List files/directories.
- `search_files_tool`: Search for patterns in files.

**Example tool definition (illustrative):**
```python
def read_file_tool(path: str) -> str:
    with open(path, "r") as f:
        return f.read()
```

### 3. Prompts

- Located in `gambit_coding_agent/prompts/`
- Used to guide agent behavior for different tasks (e.g., system initialization, to-do management).

## Data Flow

1. **User Input**: Provided via CLI, TUI, or HTTP API.
2. **Interface Layer**: Parses input and forwards it to the agent logic.
3. **Agent Logic**: Processes the request, possibly invoking tools.
4. **Tool Layer**: Executes file or command operations as needed.
5. **Agent Response**: Returns output to the interface, which presents it to the user.

## Extensibility

- **Adding Tools**: Implement new functions in `tools.py` and register them with the agent.
- **New Interfaces**: Add new entry points or UI modules that interact with the agent logic.
- **Prompt Customization**: Modify or add prompt files in `prompts/` to change agent behavior.

## Testing and CI

- Tests are located in `tests/`.
- CI is configured via `.github/workflows/python-app.yml` to run linting and tests on the `main` branch.

**.github/workflows/python-app.yml (Last modified: 2025-09-23 08:59):**
```yaml
on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python 3.10
      - uses: actions/setup-python@v3
        with:
          python-version: "3.10"
      - name: Install dependencies
      - run: |
          python -m pip install --upgrade pip
          pip install flake8 pytest
      - name: Lint with flake8
      - run: |
          flake8 .
      - name: Test with pytest
      - run: |
          pytest
```

## Primary Sources

- [gambit_coding_agent/cli.py](https://github.com/sergiomasellis/gambit/blob/main/gambit_coding_agent/cli.py) (Last modified: 2025-09-23 08:59)
- [gambit_coding_agent/tui.py](https://github.com/sergiomasellis/gambit/blob/main/gambit_coding_agent/tui.py) (Last modified: 2025-09-23 08:59)
- [gambit_coding_agent/server.py](https://github.com/sergiomasellis/gambit/blob/main/gambit_coding_agent/server.py) (Last modified: 2025-09-23 08:59)
- [gambit_coding_agent/agent.py](https://github.com/sergiomasellis/gambit/blob/main/gambit_coding_agent/agent.py) (Last modified: 2025-09-23 08:59)
- [gambit_coding_agent/tools.py](https://github.com/sergiomasellis/gambit/blob/main/gambit_coding_agent/tools.py) (Last modified: 2025-09-23 08:59)
- gambit_coding_agent/prompts/system.prompt.md (Last modified: 2025-09-23 08:59)
- [setup.py](https://github.com/sergiomasellis/gambit/blob/main/setup.py) (Last modified: 2025-09-23 08:59)
- pyproject.toml (Last modified: 2025-09-23 08:59)
- [README.md](https://github.com/sergiomasellis/gambit/blob/main/README.md) (Last modified: 2025-09-23 08:59)
- .github/workflows/python-app.yml (Last modified: 2025-09-23 08:59)