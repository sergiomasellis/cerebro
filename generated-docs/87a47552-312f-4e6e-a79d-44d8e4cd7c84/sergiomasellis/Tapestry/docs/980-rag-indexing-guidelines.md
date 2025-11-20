# RAG Indexing Guidelines

| Repo     | Doc Type             | Date                | Branch |
|----------|---------------------|---------------------|--------|
| Tapestry | RAG Indexing Manual | 2025-08-04 19:08    | main   |

## Purpose

This document provides guidelines for indexing the Tapestry codebase and documentation for Retrieval-Augmented Generation (RAG) systems. It defines tagging conventions, question formulation, and clustering strategies to optimize retrieval accuracy and developer productivity.

## Indexing Scope

Indexing should cover:

- All source code (backend/app/, frontend/src/)
- API schemas and endpoint documentation
- Configuration files and environment variables
- README and design documents
- Changelog and ADRs (if present)

## Tagging Conventions

Each indexed chunk must be tagged with:

- **File path** (relative to repo root)
- **Section or function/class name** (if applicable)
- **Last modified date** (from file header)
- **Type** (e.g., "api", "model", "config", "doc", "component")
- **Domain** (e.g., "calendar", "chore", "user", "auth", "points", "goal")
- **Language** (e.g., "python", "typescript", "markdown", "json")

**Example Tag Block:**
```
file: [backend/app/routers/chores.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/chores.py)
section: ChoreRouter
last_modified: 2025-08-04 19:08
type: api
domain: chore
language: python
```

## Chunking Strategy

- **Code:** Chunk by top-level class/function or logical module (≤ 100 lines per chunk).
- **Docs:** Chunk by heading (e.g., each ## section in Markdown).
- **Config:** Chunk by logical block (e.g., each env var or config section).
- **Schemas:** Chunk by entity or endpoint.

## Question Generation

For each chunk, generate 2–3 canonical questions that a developer or user might ask. Questions should be:

- Specific to the chunk's content
- Use natural language
- Cover both "how" and "what" aspects

**Examples:**
- "How do I create a new chore via the API?"
- "What fields are required in the Family model?"
- "Where is the database connection configured?"

## Clustering Guidelines

- Group chunks by domain (e.g., all "chore" features together)
- Within a domain, cluster by type (api, model, schema, component)
- Cross-link related clusters (e.g., API endpoint ↔ schema ↔ model)

## Update & Maintenance

- Re-index whenever a file's "Last modified" date changes
- Remove obsolete chunks and update tags as files are refactored
- Maintain a mapping of file paths to indexed chunks for traceability

## Example Index Entry

```
file: [backend/app/routers/points.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/points.py)
section: add_points
last_modified: 2025-08-04 19:08
type: api
domain: points
language: python

Q1: How can points be added to a user?
Q2: What permissions are required to modify points?
```

## RAG System Integration

- Ensure the retriever uses both tags and content for filtering
- Prefer recent chunks (by last_modified) when resolving ambiguities
- Support tag-based search (e.g., "domain:calendar type:api")

## Primary Sources

- [README.md](https://github.com/sergiomasellis/Tapestry/blob/main/README.md) (Last modified: 2025-08-04 19:08)
- [backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md) (Last modified: 2025-08-04 19:08)
- backend/pyproject.toml (Last modified: 2025-08-04 19:08)
- [frontend/tsconfig.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/tsconfig.json) (Last modified: 2025-08-04 19:08)
- [frontend/package.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/package.json) (Last modified: 2025-08-04 19:08)
- [frontend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/README.md) (Last modified: 2025-08-04 19:08)
