# Gambit Coding Agent Documentation

| Repo      | Doc Type         | Date       |
|-----------|------------------|------------|
| gambit    | Index / Contents | 2024-06-13 |

---

Welcome to the documentation for the **Gambit Coding Agent** project. This index provides an overview of the available documentation, organized by major architectural and operational areas. Use this as your starting point for navigating the codebase, understanding system design, and referencing implementation details.

---

## Table of Contents

### 1. Architecture & Topology
- [100 - Architecture & Topology](100.md): High-level components, interactions, and system style.
- [101 - System Router](101.md): Entrypoints, routing logic, and flow overview.

### 2. Domain & Business Rules
- [200 - Domain & Business Rules](200.md): Core entities, business flows, and context.

### 3. Interfaces & APIs
- [311 - REST API Endpoints](311.md): List of REST endpoints, purposes, and semantics.
- [330 - Event Topics](330.md): Event-driven topics (if applicable).

### 4. Data Model
- [421 - Main Entity Schema](421.md): Entity-relationship diagrams and key data structures.

### 5. Dependencies
- [500 - Key Dependencies](500.md): Internal services and third-party APIs.

### 6. Configuration & Environments
- [600 - Config & Environments](600.md): Config files, environment variables, and secrets management.

### 7. Security & Access
- [701 - Authentication Model](701.md): Auth mechanisms and permissions.

### 8. Observability & Operations
- [800 - Observability Overview](800.md): Logging, metrics, and health checks.
- [850 - Runbook Operations](850.md): Failure modes, debugging, and restart procedures.

### 9. CI/CD & Quality
- [900 - CI/CD Pipeline](900.md): Build, test, and deployment automation.

### 10. Risks & Decisions
- [930 - Risks & Decisions](930.md): Architectural decisions, limitations, and trade-offs.

### 11. Retrieval-Augmented Generation (RAG)
- [980 - RAG Indexing Guidelines](980.md): Tagging, question clustering, and retrieval strategies.

---

## Project Components

- **CLI**: Command-line interface for agent interaction.
- **TUI**: Textual-based UI for interactive sessions.
- **API**: FastAPI server for programmatic access.
- **Tools**: File and command utilities for agent use.
- **Prompts**: System and task-specific prompt templates.
- **Tests**: Automated test suite for validation.

---

## Quick Reference

- **Entry Point**: `main.py` (for both TUI and API server)
- **CLI Entrypoint**: `gambit_coding_agent/cli.py`
- **Server Entrypoint**: `gambit_coding_agent/server.py`
- **TUI Entrypoint**: `gambit_coding_agent/tui.py`
- **Tools**: `gambit_coding_agent/tools.py`
- **Prompts**: `gambit_coding_agent/prompts/`
- **Tests**: `tests/`
- **CI/CD**: `.github/workflows/python-app.yml`
- **Configuration**: `.env`, `pyproject.toml`, `setup.py`

---

## Primary Sources

- [README.md](README.md)
- [setup.py](setup.py)
- [pyproject.toml](pyproject.toml)
- [main.py](main.py)
- [gambit_coding_agent/cli.py](gambit_coding_agent/cli.py)
- [gambit_coding_agent/server.py](gambit_coding_agent/server.py)
- [gambit_coding_agent/tui.py](gambit_coding_agent/tui.py)
- [gambit_coding_agent/tools.py](gambit_coding_agent/tools.py)
- [gambit_coding_agent/prompts/](gambit_coding_agent/prompts/)
- [tests/](tests/)
- [.github/workflows/python-app.yml](.github/workflows/python-app.yml)

---

**For detailed documentation on each topic, follow the links above or navigate to the corresponding Markdown files in the repository.**