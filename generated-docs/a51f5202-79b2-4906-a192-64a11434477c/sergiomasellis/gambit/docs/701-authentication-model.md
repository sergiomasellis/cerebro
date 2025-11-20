# Authentication Model

| Repo    | Doc Type            | Date       |
|---------|---------------------|------------|
| gambit  | Authentication (701) | 2024-06-13 |

---

This document describes the authentication model for the **Gambit Coding Agent** project, focusing on how API keys are managed, validated, and used to secure access to OpenAI-compatible APIs via OpenRouter. It also covers how authentication is handled in both server and CLI/TUI contexts, and the permissions model in effect.

---

## Overview

Gambit relies on an **API key** for authenticating requests to the OpenRouter API, which is the backend for all LLM-powered operations. The API key is required for both the FastAPI server and CLI/TUI modes. The authentication model is designed to:

- Ensure that only authorized users can access OpenRouter resources.
- Allow flexible API key management (environment variable, .env file, or per-request override).
- Provide minimal but effective permission boundaries (all-or-nothing access).

---

## API Key Sources and Precedence

The Gambit agent supports multiple ways to provide the OpenRouter API key:

1. **Environment Variable**:  
   - The key `OPENROUTER_API_KEY` can be set in the environment or in a `.env` file at the project root.
   - This is the default and recommended method for most deployments.

2. **Per-Request Override** (API server only):  
   - For endpoints like `/explain` and `/message`, the request body may include an `api_key` field.
   - If present, this key is used for that request only, overriding the environment variable.

3. **CLI/TUI**:  
   - The CLI and TUI modes use the environment variable or `.env` file exclusively.
   - There is no per-command override for the API key in CLI/TUI.

**Precedence Order**:
1. Per-request `api_key` (API server endpoints)
2. `OPENROUTER_API_KEY` from environment or `.env`

---

## Authentication Flow

### FastAPI Server

1. **Startup**:  
   - On startup, the server loads `OPENROUTER_API_KEY` from the environment or `.env`.
   - If missing, endpoints requiring LLM access will fail with an error.

2. **Request Handling**:  
   - For endpoints like `/explain` and `/message`, the handler checks if an `api_key` is provided in the request body.
   - If present, this key is used for the outbound OpenRouter API call.
   - If not, the server falls back to the environment variable.

3. **Status Endpoint**:  
   - `/status` returns a boolean indicating whether an API key is present in the environment.

4. **Security**:  
   - There is no user/session authentication; all clients with access to the server can use the API.
   - The only boundary is possession of a valid OpenRouter API key.

### CLI and TUI

- The CLI (`gambit` command) and TUI (`python main.py tui`) modes require the API key to be set in the environment or `.env`.
- If the key is missing, the agent will not function and will prompt for setup.

---

## Permissions Model

- **All-or-Nothing**:  
  Possession of a valid OpenRouter API key grants full access to all agent features (code explanation, messaging, tool usage).
- **No User Roles**:  
  There are no user accounts, roles, or fine-grained permissions within Gambit itself.
- **No Session Tokens**:  
  All authentication is based on the API key; there are no session cookies or JWTs.

---

## Security Considerations

- **Key Exposure**:  
  - API keys should be kept secret. Do not commit `.env` files or keys to version control.
  - When running the server, ensure it is not exposed to untrusted networks unless access is controlled externally (e.g., via firewall or reverse proxy).
- **Per-Request Key Override**:  
  - The ability to override the API key per request is convenient for testing but can be a security risk if the server is public.
  - Consider disabling or restricting this feature in production environments.

---

## Example: API Key Usage

### .env File

```
OPENROUTER_API_KEY=sk-xxxxxxx
```

### POST /explain Request (with override)

```json
{
  "code": "def foo(): pass",
  "api_key": "sk-override-xxxx"
}
```

### POST /explain Request (without override)

```json
{
  "code": "def foo(): pass"
}
```
*(Uses the environment key)*

---

## Summary Table

| Context         | Key Source(s)                | Override Possible | Required for Functionality |
|-----------------|-----------------------------|-------------------|---------------------------|
| FastAPI Server  | .env / env, per-request     | Yes               | Yes                       |
| CLI / TUI       | .env / env                  | No                | Yes                       |

---

## Primary Sources

- [README.md](README.md)
- [pyproject.toml](pyproject.toml)
- [main.py](main.py)
- [gambit_coding_agent/server.py](gambit_coding_agent/server.py)
- [gambit_coding_agent/cli.py](gambit_coding_agent/cli.py)
- [.github/workflows/python-app.yml](.github/workflows/python-app.yml)
