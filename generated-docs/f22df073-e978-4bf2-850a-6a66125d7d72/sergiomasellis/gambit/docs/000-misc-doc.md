# Gambit Documentation Table of Contents

| Repo   | Doc Type           | Date       | Branch |
|--------|--------------------|------------|--------|
| gambit | Table of Contents  | 2025-09-23 | main   |

---

## Overview

Gambit is a tiny coding agent powered by LangChain and OpenAI-compatible APIs, supporting multiple entrypoints (CLI, TUI, API) and a suite of tools for code explanation, file operations, and command execution.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Entrypoints](#entrypoints)
    - [CLI](#cli)
    - [Textual TUI](#textual-tui)
    - [FastAPI Server (API)](#fastapi-server-api)
4. [API Endpoints](#api-endpoints)
5. [Available Tools](#available-tools)
6. [Testing](#testing)
7. [Development](#development)
8. [Local Development / CLI](#local-development--cli)
9. [Project Structure](#project-structure)
10. [Primary Sources](#primary-sources)

---

## Introduction

Gambit is a coding agent that can explain code snippets, answer coding questions, and interact with your file system in a controlled way. It is designed for both interactive and programmatic use.

---

## Installation

- Requires Python >=3.12.
- Install dependencies using `uv` or `pip`:

```bash
uv sync
# or
pip install -e .
```

- Set up your API key in a `.env` file:

```
OPENROUTER_API_KEY=your_api_key_here
```

---

## Entrypoints

### CLI

A `gambit` command is available after installation, invoking the agent via the command line.

**[setup.py](https://github.com/sergiomasellis/gambit/blob/main/setup.py)** (Last modified: 2025-09-23 08:59):

```python
entry_points={
    "console_scripts": [
        "gambit=gambit_coding_agent.cli:main",
    ]
},
```

### Textual TUI

Launch the interactive Textual-based UI:

```bash
python [main.py](https://github.com/sergiomasellis/gambit/blob/main/main.py) tui
```

### FastAPI Server (API)

Start the API server:

```bash
python [main.py](https://github.com/sergiomasellis/gambit/blob/main/main.py) uv
```

The server runs at `http://127.0.0.1:8000`.

---

## API Endpoints

- **POST /explain**: Explain a code snippet.
- **POST /message**: Send a free-form message to the agent.
- **GET /status**: Check server and agent status.
- **GET /diagnose**: Retrieve diagnostic information.

Example request for `/explain`:

```json
{
  "code": "def hello(): print('Hello, World!')",
  "api_key": "optional_override_key"
}
```

---

## Available Tools

The agent can use the following tools:

- `execute_command_tool`: Execute shell commands.
- `read_file_tool`: Read file contents.
- `write_file_tool`: Write content to a file.
- `list_directory_tool`: List files/directories.
- `search_files_tool`: Search for patterns in files.

**pyproject.toml** (Last modified: 2025-09-23 08:59):

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

---

## Testing

Run all tests:

```bash
pytest
```

Run a specific test:

```bash
pytest [tests/test_agent.py](https://github.com/sergiomasellis/gambit/blob/main/tests/test_agent.py)::test_some_function
```

---

## Development

- Build, lint, and test commands are described in `[AGENTS.md](https://github.com/sergiomasellis/gambit/blob/main/AGENTS.md)`.
- Code style guidelines are in `[AGENTS.md](https://github.com/sergiomasellis/gambit/blob/main/AGENTS.md)`.
- Dependencies are managed via `pyproject.toml`.

---

## Local Development / CLI

Install in a virtual environment for local development:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
.\.venv\Scripts\python.exe -m pip install -e .
gambit -m "Explain the Observer pattern in Python."
```

Alternatively, use the provided `gambit.ps1` or `gambit.cmd` shims.

---

## Project Structure

```mermaid
graph TD
  A[[main.py](https://github.com/sergiomasellis/gambit/blob/main/main.py)]
  B[gambit_coding_agent/]
  C[tests/]
  D[[README.md](https://github.com/sergiomasellis/gambit/blob/main/README.md)]
  E[[setup.py](https://github.com/sergiomasellis/gambit/blob/main/setup.py)]
  F[pyproject.toml]
  G[.github/]
  B1[tui.py]
  B2[tools.py]
  B3[slash_commands.py]
  B4[server.py]
  B5[cli.py]
  B6[agent.py]
  B7[__init__.py]
  B8[prompts/]
  B8a[todo.prompt.md]
  B8b[system.prompt.md]
  B8c[init.prompt.md]
  C1[test_todos.py]
  C2[test_agent.py]
  G1[workflows/python-app.yml]
  B --> B1
  B --> B2
  B --> B3
  B --> B4
  B --> B5
  B --> B6
  B --> B7
  B --> B8
  B8 --> B8a
  B8 --> B8b
  B8 --> B8c
  C --> C1
  C --> C2
  G --> G1
```

---

## Primary Sources

- [README.md](https://github.com/sergiomasellis/gambit/blob/main/README.md) (Last modified: 2025-09-23 08:59)
- [setup.py](https://github.com/sergiomasellis/gambit/blob/main/setup.py) (Last modified: 2025-09-23 08:59)
- pyproject.toml (Last modified: 2025-09-23 08:59)
- .github/workflows/python-app.yml (Last modified: 2025-09-23 08:59)
- [gambit_coding_agent/cli.py](https://github.com/sergiomasellis/gambit/blob/main/gambit_coding_agent/cli.py), tui.py, server.py, agent.py, tools.py, slash_commands.py, prompts/
- [tests/test_agent.py](https://github.com/sergiomasellis/gambit/blob/main/tests/test_agent.py), [tests/test_todos.py](https://github.com/sergiomasellis/gambit/blob/main/tests/test_todos.py)