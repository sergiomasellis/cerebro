# Cerebro Codebase Guide

## Operations
- **Run:** `uv run main.py` (CLI entry point)
- **Test:** `uv run pytest` (Single: `uv run pytest tests/test_file.py::test_name`)
- **Lint/Format:** `uv run ruff check .` / `uv run ruff format .`
- **Deps:** `uv add <pkg>` / `uv remove <pkg>`. Main deps: `langgraph`, `langchain`, `gitpython`.

## Architecture & Style
- **Structure:** Source in `src/` (graph, nodes, state, utils). Entry in `main.py`.
- **Python:** >=3.12. Strict type hints (`TypedDict` for graph state, `pydantic` models).
- **LangGraph:** Define state in `src/state.py`, nodes in `src/nodes.py`, graph in `src/graph.py`.
- **Formatting:** Ruff defaults (Black compatible). 4-space indent.
- **Imports:** Absolute imports (`from src.graph import ...`). Sort: Stdlib > 3rd-party > Local.
- **Naming:** `snake_case` vars/funcs, `PascalCase` classes.
- **Error Handling:** Typed exceptions. No bare `except:`.
- **Docs:** Keep `README.md` updated with usage.
