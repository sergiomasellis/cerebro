# Domain & Business Rules

| Repo      | Doc Type                | Date       |
|-----------|------------------------|------------|
| gambit    | Domain & business rules | 2024-06-09 |

---

This document describes the core domain logic, business rules, and main flows of the Gambit Coding Agent. It covers how the agent interprets user messages, leverages tools, and orchestrates code explanation and coding assistance tasks.

## Overview

Gambit is a coding agent designed to help users understand code, answer programming questions, and perform controlled file and command operations. It is powered by LangChain, OpenAI-compatible APIs (via OpenRouter), and a set of custom tools for interacting with the local environment.

The agent is accessible via:
- A Textual-based TUI (`main.py tui`)
- A FastAPI server (`main.py uv`)
- CLI and shell shims (`gambit`, `gambit.ps1`, `gambit.cmd`)

## Core Business Logic

### 1. Message Handling

The agent processes two main types of user input:
- **Code explanations**: Users submit code snippets for explanation.
- **General coding queries**: Users ask questions about programming concepts or request help with code.

#### Flow

1. **Input Reception**: User input is received via TUI, CLI, or API endpoint.
2. **Intent Detection**: The agent determines if the message is a code explanation request or a general query.
3. **Prompt Construction**: The agent builds a prompt using system and user context, possibly leveraging prompt templates from `gambit_coding_agent/prompts/`.
4. **LLM Invocation**: The prompt is sent to the LLM (via LangChain/OpenRouter).
5. **Tool Use (if needed)**: If the LLM determines that a tool is required (e.g., file read, command execution), it invokes the appropriate tool.
6. **Response Assembly**: The agent composes the final response, integrating LLM output and tool results.
7. **Output Delivery**: The response is returned to the user via the original interface.

### 2. Tool Usage

The agent is augmented with several tools, each encapsulating a specific capability:

| Tool Name             | Purpose                                               |
|-----------------------|------------------------------------------------------|
| execute_command_tool  | Run a shell command and return its output            |
| read_file_tool        | Read and return the contents of a file               |
| write_file_tool       | Write content to a file                              |
| list_directory_tool   | List files/directories at a given path               |
| search_files_tool     | Search for a pattern in files and return matches     |

**Tool invocation is controlled and sandboxed** to prevent unsafe operations. The agent only uses tools when the LLM determines they are necessary for fulfilling the user's request.

### 3. API Key and Environment Management

- The agent requires an OpenRouter API key, loaded from `.env` or provided per request.
- The `/status` endpoint and diagnostics logic check for API key presence and agent initialization state.

### 4. Error Handling

- If a tool fails (e.g., file not found, command error), the agent captures the error and includes a user-friendly message in the response.
- If the LLM or API is unavailable, the agent returns a clear error message.

## Main Flows

### Code Explanation Flow

1. User submits code via `/explain` endpoint or TUI.
2. Agent constructs a prompt using `todo.prompt.md` or `system.prompt.md`.
3. LLM generates a natural language explanation.
4. Agent returns the explanation to the user.

### General Message Flow

1. User submits a message via `/message` endpoint, TUI, or CLI.
2. Agent determines if tool use is required (e.g., file operation).
3. If so, agent invokes the tool and integrates results.
4. LLM generates a response, possibly referencing tool output.
5. Agent returns the response.

### Tool Use Example

- User: "Show me the contents of `main.py`."
- Agent: Invokes `read_file_tool` on `main.py`.
- Tool returns file contents.
- Agent summarizes or presents the contents as appropriate.

## Context Management

- The agent maintains conversational context for multi-turn interactions, allowing follow-up questions and clarifications.
- Context is managed in memory per session (TUI, API, or CLI invocation).

## Security & Safety

- All tool invocations are restricted to the project directory and use safe APIs.
- Dangerous commands or file operations are filtered or require explicit confirmation.

---

## Primary Sources

- [README.md](README.md)
- [gambit_coding_agent/agent.py](gambit_coding_agent/agent.py)
- [gambit_coding_agent/tools.py](gambit_coding_agent/tools.py)
- [gambit_coding_agent/server.py](gambit_coding_agent/server.py)
- [gambit_coding_agent/prompts/todo.prompt.md](gambit_coding_agent/prompts/todo.prompt.md)
- [gambit_coding_agent/prompts/system.prompt.md](gambit_coding_agent/prompts/system.prompt.md)
- [main.py](main.py)
- [setup.py](setup.py)
- [pyproject.toml](pyproject.toml)