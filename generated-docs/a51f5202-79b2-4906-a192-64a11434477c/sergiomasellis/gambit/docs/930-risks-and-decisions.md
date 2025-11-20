# Gambit Coding Agent – Risks & Architectural Decisions

| Repo   | Doc Type         | Date       |
|--------|------------------|------------|
| gambit | Risks & Decisions (930) | 2024-06-13 |

---

## Overview

This document captures key architectural decisions, trade-offs, and known limitations in the design and implementation of the Gambit Coding Agent. It serves as a reference for maintainers and contributors to understand the rationale behind technology choices, integration patterns, and operational constraints.

---

## 1. Major Design Decisions

### 1.1 Use of LangChain and LangGraph

- **Decision:** The agent core is built using [LangChain](https://github.com/langchain-ai/langchain) and [LangGraph](https://github.com/langchain-ai/langgraph).
- **Rationale:** LangChain provides a robust abstraction for LLM orchestration, tool integration, and prompt management. LangGraph enables graph-based agent flows, supporting more complex tool use and reasoning patterns.
- **Trade-offs:** 
  - **Pros:** Rapid prototyping, rich ecosystem, easy tool integration.
  - **Cons:** Dependency on evolving libraries; potential for breaking changes and increased cold start time.

### 1.2 OpenRouter as LLM Gateway

- **Decision:** All LLM calls are routed through [OpenRouter](https://openrouter.ai), which proxies to OpenAI-compatible APIs.
- **Rationale:** OpenRouter offers free and paid API keys, supports multiple LLM providers, and is compatible with OpenAI’s API, simplifying integration.
- **Trade-offs:**
  - **Pros:** Flexibility in LLM backend, easy key management, cost control.
  - **Cons:** Reliance on a third-party gateway; subject to OpenRouter’s uptime and rate limits.

### 1.3 Controlled Tool Execution

- **Decision:** The agent exposes a limited set of tools for file and command operations (see [README.md](README.md)), with strict controls on execution context.
- **Rationale:** Enables the agent to perform useful coding tasks (e.g., reading/writing files, running shell commands) while minimizing security risks.
- **Trade-offs:**
  - **Pros:** Enhanced agent capability, practical for code assistance.
  - **Cons:** Potential for misuse if controls are bypassed; limited to the project directory and sandboxed environment.

### 1.4 API Key Handling

- **Decision:** API keys are loaded from a `.env` file (`OPENROUTER_API_KEY`) or can be overridden per request.
- **Rationale:** Simplifies local development and deployment; supports both global and per-request authentication.
- **Trade-offs:**
  - **Pros:** Developer convenience, flexible for multi-user scenarios.
  - **Cons:** Risk of accidental key exposure if `.env` is not secured; per-request override could be abused if not properly authenticated.

### 1.5 Multi-Interface Support

- **Decision:** The agent can be run as a FastAPI server, a Textual TUI, or via CLI shims.
- **Rationale:** Supports a range of user workflows (interactive, programmatic, or scriptable).
- **Trade-offs:**
  - **Pros:** Broad accessibility, easy integration into different environments.
  - **Cons:** Increased maintenance burden; potential for interface-specific bugs.

---

## 2. Known Limitations

### 2.1 Controlled Execution Environment

- **Limitation:** All tool execution is restricted to the project directory; no access to system-level resources or external networks.
- **Impact:** Prevents malicious or accidental system modifications, but limits agent’s ability to perform certain tasks (e.g., installing packages, accessing remote files).

### 2.2 API Key Security

- **Limitation:** API keys are stored in plaintext in `.env` files.
- **Impact:** If the `.env` file is committed or leaked, API keys may be compromised. Users must ensure `.env` is gitignored and access is restricted.

### 2.3 Dependency on External Services

- **Limitation:** The agent’s core functionality depends on OpenRouter and, by extension, the underlying LLM providers.
- **Impact:** Outages or API changes upstream can break agent functionality. No offline fallback is provided.

### 2.4 Limited Toolset

- **Limitation:** Only a fixed set of tools are available (see [README.md](README.md)). No plugin or dynamic tool loading.
- **Impact:** Limits extensibility; users cannot add custom tools without modifying source code.

### 2.5 No User Authentication

- **Limitation:** The FastAPI server does not implement user authentication or rate limiting.
- **Impact:** If exposed to a public network, the API could be abused (e.g., for key exhaustion or denial of service).

---

## 3. Architectural Decision Records (ADRs)

### ADR-001: Use of LangChain and LangGraph

- **Context:** Need for LLM orchestration and tool integration.
- **Decision:** Adopt LangChain and LangGraph as core agent frameworks.
- **Status:** Accepted
- **Consequences:** Rapid development, but increased dependency risk.

### ADR-002: OpenRouter API Gateway

- **Context:** Need for flexible, cost-effective LLM access.
- **Decision:** Route all LLM calls via OpenRouter.
- **Status:** Accepted
- **Consequences:** Simplifies integration, but introduces a third-party dependency.

### ADR-003: Controlled Tool Execution

- **Context:** Need to balance agent capability with security.
- **Decision:** Restrict tool execution to project directory and a fixed set of operations.
- **Status:** Accepted
- **Consequences:** Safer by default, but less extensible.

### ADR-004: API Key Management

- **Context:** Need for simple, flexible API key handling.
- **Decision:** Use `.env` file for default key, allow per-request override.
- **Status:** Accepted
- **Consequences:** Easy for developers, but requires careful handling of secrets.

---

## 4. Risk Summary Table

| Risk/Trade-off                         | Mitigation/Notes                                   |
|-----------------------------------------|----------------------------------------------------|
| Dependency on LangChain/LangGraph       | Pin versions; monitor upstream changes             |
| Reliance on OpenRouter                  | Monitor status; document fallback procedures       |
| Tool execution security                 | Restrict to project dir; review code for escapes   |
| API key exposure                        | `.env` in `.gitignore`; educate users              |
| No authentication on API                | Recommend local-only use; document risk            |
| Limited extensibility                   | Accept for MVP; revisit if user demand increases   |

---

## 5. Future Considerations

- **Authentication:** Add user authentication and rate limiting to the FastAPI server for safe multi-user or public deployment.
- **Plugin System:** Consider a plugin architecture for user-defined tools, with security sandboxing.
- **API Key Vault:** Integrate with secret managers (e.g., HashiCorp Vault, AWS Secrets Manager) for production deployments.
- **Offline Mode:** Explore local LLM support for environments without internet access.

---

## Primary Sources

- [README.md](README.md)
- [pyproject.toml](pyproject.toml)
- [setup.py](setup.py)
- [gambit_coding_agent/tools.py](gambit_coding_agent/tools.py)
- [gambit_coding_agent/server.py](gambit_coding_agent/server.py)
- [.github/workflows/python-app.yml](.github/workflows/python-app.yml)

---