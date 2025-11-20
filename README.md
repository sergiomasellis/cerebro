# Cerebro

Cerebro is an AI agent built with LangGraph that autonomously generates comprehensive, taxonomy-based documentation for software repositories.

## Features
- **Universal Support**: Works with Bitbucket, GitHub, and any Git repository.
- **Taxonomy-Based Docs**: Generates a structured suite of Markdown files (e.g., `100-architecture-overview.md`, `900-ci-cd-pipeline.md`) rather than a single monolith.
- **Adaptive Planning**: intelligently decides which documents are needed based on the repository's content.
- **Deep Analysis**:
  - **Architecture & Diagrams**: Infers architecture and generates C4/Sequence/ER diagrams using Mermaid.js.
  - **Business Logic**: Summarizes domain entities and rules.
  - **CI/CD & Ops**: Documents pipelines, config, and observability.
  - **APIs**: Indexes REST endpoints and contracts.
- **RAG-Ready**: Generates optimized index and meta-docs for downstream AI consumption.

## Usage

1. **Install dependencies**:
   ```bash
   uv sync
   ```

2. **Configure Environment**:
   Edit `.env` or set variables:
   ```bash
   OPENAI_API_KEY=sk-...
   OPENAI_MODEL=gpt-4o
   ```

3. **Run the Agent**:
   ```bash
   uv run main.py <repository_url>
   ```
   
   Examples:
   ```bash
   # GitHub
   uv run main.py https://github.com/fastapi/fastapi
   ```

## Output Structure
The agent creates a `docs/` directory in the repository root (or local cache) containing:
- `000-index.md`: Main Table of Contents.
- `100-architecture-overview.md`: High-level system design.
- `200-business-domain-overview.md`: Domain logic.
- `...`: Other sections (API, Config, Dependencies) as relevant.
- `980-rag-indexing-guidelines.md`: Metadata for AI indexing.

## Tech Stack
- **LangGraph**: Orchestration.
- **LangChain**: LLM interaction.
- **GitPython**: Git operations.
