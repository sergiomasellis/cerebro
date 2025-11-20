# RAG Indexing Guidelines

| Repo      | Doc Type              | Date                | Branch |
|-----------|----------------------|---------------------|--------|
| Tapestry  | RAG Indexing Guidelines | 2025-08-04 19:08   | None   |

## Purpose

This document provides guidelines for indexing the Tapestry repository for Retrieval-Augmented Generation (RAG) systems. It covers best practices for tagging, question generation, and document clustering to optimize retrieval accuracy and semantic coverage.

---

## 1. Tagging Guidelines

### 1.1. Tag Granularity

- **File-level tags:** Assign tags reflecting the file's primary domain (e.g., `api`, `frontend`, `backend`, `chore`, `calendar`, `auth`, `points`, `goals`, `family`).
- **Section-level tags:** For large files (e.g., `/backend/app/routers/*.py`), tag sections by endpoint or class (e.g., `endpoint:GET /chores`, `model:User`).
- **Feature tags:** Use tags for cross-cutting features (`leaderboard`, `integration:google-calendar`, `integration:alexa`, `ai:langgraph`).

### 1.2. Tag Format

- Use lowercase, hyphen-separated tags (e.g., `user-management`, `event-tracking`).
- For endpoints, use `endpoint:<METHOD> <PATH>` (e.g., `endpoint:POST /auth/login`).
- For models/schemas, use `model:<Entity>` (e.g., `model:Chore`).

### 1.3. Tag Placement

- Place tags in a dedicated metadata block at the top of each indexed chunk or section.
- Example:
  ```
  [tags: api, endpoint:GET /chores, model:Chore, points]
  ```

---

## 2. Question Generation

### 2.1. Coverage

- For each indexed chunk, generate 2–5 natural language questions that a user or developer might ask.
- Cover:
  - **Functionality:** "How do I create a new family group?"
  - **Usage:** "What parameters are required for the /auth/login endpoint?"
  - **Integration:** "How does Tapestry sync with Google Calendar?"
  - **Business logic:** "How are points assigned for chores?"

### 2.2. Question Style

- Use clear, concise, and unambiguous language.
- Prefer "How", "What", "Which", and "Where" questions.
- Avoid overly broad or vague questions.

### 2.3. Placement

- Place questions in a `[questions:]` block after the tags.
- Example:
  ```
  [questions:
    How do I mark a chore as complete?
    What is the schema for the Chore entity?
    Which endpoints allow updating user points?
  ]
  ```

---

## 3. Clustering & Chunking

### 3.1. Chunk Size

- Target 300–800 tokens per chunk for optimal retrieval and context window fit.
- Split at logical boundaries: function, class, or endpoint level for code; section or heading for Markdown/docs.

### 3.2. Clustering Strategy

- Group related chunks by:
  - **Domain:** (e.g., all `chores` endpoints and models)
  - **Feature:** (e.g., all AI/LangGraph logic)
  - **Layer:** (e.g., all frontend components, all backend routers)

### 3.3. Cross-linking

- Where possible, include references to related chunks (e.g., "See also: endpoint:GET /points").

---

## 4. Example Index Entry

```
[tags: api, endpoint:POST /chores, model:Chore, points]
[questions:
  How do I create a new chore?
  What fields are required to create a chore?
  How are points assigned when a chore is created?
]
---
def create_chore(...):
    ...
```

---

## 5. Special Considerations

- **AI/Chore Generation:** Tag all LangGraph and AI pipeline code with `ai:langgraph` and generate questions about automation and AI-driven features.
- **Integrations:** Tag integration points (Google Calendar, Alexa) with `integration:<service>`.
- **Security:** Tag authentication/authorization logic with `auth`, and generate questions about permissions and access control.

---

## 6. File & Section Mapping

| Path                                      | Tag Examples                | Notes                                      |
|--------------------------------------------|-----------------------------|--------------------------------------------|
| `/backend/app/routers/chores.py`           | `api`, `endpoint`, `chore`  | Chore CRUD endpoints                       |
| `/backend/app/ai/chore_graph.py`           | `ai:langgraph`, `chore`     | AI pipeline for chore generation           |
| `/backend/app/models/models.py`            | `model:<Entity>`            | SQLAlchemy models                          |
| `/frontend/src/features/leaderboard/`      | `frontend`, `leaderboard`   | Leaderboard UI logic                       |
| `/backend/app/routers/auth.py`             | `api`, `auth`               | Auth endpoints                             |
| `/backend/app/routers/calendars.py`        | `api`, `calendar`, `integration:google-calendar`, `integration:alexa` | Calendar integrations |

---

## 7. Review & Maintenance

- Periodically review tags and questions for accuracy as the codebase evolves.
- Update clusters and cross-links when features or endpoints are added/removed.

---

## Primary Sources

- [README.md](./README.md) (Last modified: 2025-08-04 19:08)
- [backend/README.md](./backend/README.md) (Last modified: 2025-08-04 19:08)
- [backend/pyproject.toml](./backend/pyproject.toml) (Last modified: 2025-08-04 19:08)
- [frontend/package.json](./frontend/package.json) (Last modified: 2025-08-04 19:08)
- [frontend/tsconfig.json](./frontend/tsconfig.json) (Last modified: 2025-08-04 19:08)
- [frontend/README.md](./frontend/README.md) (Last modified: 2025-08-04 19:08)