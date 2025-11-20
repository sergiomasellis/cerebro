# Key Dependencies

| Repo      | Doc Type         | Date       |
|-----------|------------------|------------|
| gambit    | Dependencies (500) | 2024-06-13 |

This document outlines the key dependencies for the **gambit** coding agent project. It covers both core Python packages and critical external APIs/services required for the agent's operation.

---

## 1. Core Python Dependencies

The following dependencies are defined in [`pyproject.toml`](pyproject.toml) and are essential for the agent's core functionality:

| Package                | Purpose / Usage                                                                                   |
|------------------------|--------------------------------------------------------------------------------------------------|
| **fastapi**            | Provides the REST API server for agent interaction.                                              |
| **langchain[openai]**  | Framework for building LLM-powered agents; integrates with OpenAI-compatible APIs.                |
| **langgraph**          | Enables graph-based orchestration of agent workflows.                                            |
| **openai**             | Python client for OpenAI-compatible APIs (used via OpenRouter).                                  |
| **pydantic**           | Data validation and settings management (used in API models and config).                         |
| **python-dotenv**      | Loads environment variables from `.env` files (e.g., API keys).                                  |
| **rich**               | Provides rich formatting for CLI and TUI outputs.                                                |
| **setuptools**         | Packaging and distribution utilities.                                                            |
| **textual**            | Powers the Textual-based TUI for interactive agent chat.                                         |
| **uvicorn[standard]**  | ASGI server for running the FastAPI app.                                                         |
| **pytest**             | Testing framework for unit and integration tests.                                                |
| **ripgrep**            | Fast file searching utility, used by the agent's file search tool.                               |

**Development-only dependencies** (in `[dependency-groups] dev`):

- **coverage**, **pytest-cov**: For code coverage reporting during tests.

---

## 2. External APIs and Services

### OpenRouter API

- **Purpose:** The agent relies on the [OpenRouter API](https://openrouter.ai) to access OpenAI-compatible LLMs.
- **Authentication:** Requires an API key, which should be set in a `.env` file as `OPENROUTER_API_KEY`.
- **Usage:** All LLM calls (via LangChain/OpenAI client) are routed through OpenRouter, enabling model selection and usage tracking.

**Example `.env` configuration:**
```
OPENROUTER_API_KEY=your_api_key_here
```

---

## 3. Internal Service Integration

The agent exposes its own services via:

- **REST API** (FastAPI): Endpoints for code explanation, messaging, status, and diagnostics.
- **Textual TUI**: Local interactive terminal UI for chatting with the agent.

These services are implemented in project modules such as:

- `gambit_coding_agent/server.py` (API server)
- `gambit_coding_agent/tui.py` (TUI)
- `gambit_coding_agent/agent.py` (agent logic)
- `gambit_coding_agent/tools.py` (tool integrations)

---

## 4. Dependency Management

- **Primary management:** All dependencies are declared in [`pyproject.toml`](pyproject.toml).
- **Installation:** Use `uv sync` (recommended) or `pip install -e .` for local development.
- **Environment variables:** Managed via `.env` and loaded with `python-dotenv`.

---

## 5. Dependency Diagram

```mermaid
graph TD
    subgraph "gambit"
        A[main.py / CLI / TUI / API]
        B[Agent Logic<br>(agent.py)]
        C[Tools<br>(tools.py)]
        D[API Server<br>(server.py)]
    end

    subgraph "Core Dependencies"
        E[FastAPI]
        F[LangChain<br>+ OpenAI]
        G[LangGraph]
        H[Pydantic]
        I[Textual]
        J[python-dotenv]
        K[Uvicorn]
        L[Rich]
        M[Ripgrep]
    end

    subgraph "External Service"
        N[OpenRouter API]
    end

    A --> D
    A --> I
    D --> E
    D --> H
    B --> F
    B --> G
    B --> N
    B --> J
    C --> M
    A --> L
    D --> K
```

---

## 6. Notes

- **Ripgrep** must be installed and available in the system PATH for file search tools to function.
- **OpenRouter API key** is mandatory for LLM operations; without it, the agent cannot respond to code or message queries.
- **Textual** and **Rich** are optional for headless API usage but required for the TUI.

---

## Primary Sources

- [pyproject.toml](pyproject.toml)
- [setup.py](setup.py)
- [README.md](README.md)
- [gambit_coding_agent/agent.py](gambit_coding_agent/agent.py)
- [gambit_coding_agent/tools.py](gambit_coding_agent/tools.py)
- [gambit_coding_agent/server.py](gambit_coding_agent/server.py)
- [gambit_coding_agent/tui.py](gambit_coding_agent/tui.py)