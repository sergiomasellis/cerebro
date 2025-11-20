# Configuration & Environment Management

| Repo      | Doc Type           | Date         |
|-----------|--------------------|--------------|
| gambit    | Config & Environments (600) | 2024-06-13   |

---

This document details how configuration, environment variables, and secrets are managed in the **gambit** coding agent project. It covers local development, deployment, and CI/CD considerations, with a focus on the `.env` file, environment variables, and best practices for handling sensitive data.

---

## 1. Configuration Overview

The gambit project uses environment variables for runtime configuration, with a focus on API keys and service credentials. The main variable is:

- **OPENROUTER_API_KEY**: Required for authenticating with OpenRouter (an OpenAI-compatible API provider).

Configuration is loaded at runtime using the [`python-dotenv`](https://pypi.org/project/python-dotenv/) package, which reads variables from a `.env` file in the project root if present.

---

## 2. Environment Variables

### Required Variables

| Variable Name         | Purpose                                           | Required | Example Value         |
|-----------------------|---------------------------------------------------|----------|-----------------------|
| OPENROUTER_API_KEY    | API key for OpenRouter (OpenAI-compatible API)    | Yes      | sk-abc123...          |

### Optional Variables

Currently, no other environment variables are required or supported by default. Future versions may introduce additional configuration options.

---

## 3. Local Development

### Setting Up the `.env` File

For local development, create a `.env` file in the project root:

```
OPENROUTER_API_KEY=your_api_key_here
```

- **Never commit your real API keys to version control.** The `.env` file should be listed in `.gitignore` (add it if not present).
- You can obtain a free API key from [OpenRouter](https://openrouter.ai).

### How Configuration is Loaded

- The application uses `python-dotenv` to load variables from `.env` automatically.
- If `OPENROUTER_API_KEY` is not set, API requests will fail and the agent/server will not function.

### Overriding via CLI or API

- Some endpoints (e.g., `/explain`) allow you to override the API key per request by including an `api_key` field in the request body.
- This is useful for testing or multi-user scenarios.

---

## 4. Deployment & Production

### Environment Variables in Production

- In production, set `OPENROUTER_API_KEY` as an environment variable in your hosting environment (e.g., Docker, cloud service, CI/CD pipeline).
- Do **not** use a `.env` file in production unless you are certain it is secure and not exposed.

### Example: Setting in Bash

```bash
export OPENROUTER_API_KEY=sk-abc123...
python main.py uv
```

### Example: Dockerfile (snippet)

```dockerfile
ENV OPENROUTER_API_KEY=sk-abc123...
CMD ["python", "main.py", "uv"]
```

---

## 5. CI/CD and GitHub Actions

- The provided `.github/workflows/python-app.yml` does **not** reference secrets or environment variables by default.
- If you wish to run integration tests that require the API key, add a secret in your GitHub repository settings (`Settings > Secrets and variables > Actions`), e.g., `OPENROUTER_API_KEY`.
- Reference it in your workflow as follows:

```yaml
env:
  OPENROUTER_API_KEY: ${{ secrets.OPENROUTER_API_KEY }}
```

---

## 6. Security Best Practices

- **Never commit secrets** (API keys, tokens) to version control.
- Use `.env` only for local development, and ensure it is in `.gitignore`.
- For production and CI/CD, use environment variables or secret managers.
- Rotate API keys regularly and remove unused keys from your OpenRouter account.

---

## 7. Troubleshooting

- If you see errors related to authentication or missing API keys, ensure `OPENROUTER_API_KEY` is set in your environment or `.env` file.
- The `/status` API endpoint can be used to check if the agent has detected an API key and is initialized:

  ```json
  {
    "has_env_api_key": true,
    "agent_initialized": true
  }
  ```

---

## 8. Example `.env` File

```
# .env (do NOT commit to git)
OPENROUTER_API_KEY=sk-abc123...
```

---

## 9. Related Files

- **README.md**: Quickstart, `.env` usage, and setup instructions.
- **pyproject.toml**: Declares `python-dotenv` as a dependency.
- **main.py** and **gambit_coding_agent/server.py**: Load and use environment variables at runtime.
- **.github/workflows/python-app.yml**: CI pipeline; can be extended to use secrets.

---

## Primary Sources

- [README.md](README.md)
- [pyproject.toml](pyproject.toml)
- [setup.py](setup.py)
- [.github/workflows/python-app.yml](.github/workflows/python-app.yml)
- [main.py](main.py)
- [gambit_coding_agent/server.py](gambit_coding_agent/server.py)
