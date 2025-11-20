# RAG Indexing Guidelines

| Repo      | Doc Type             | Date                | Branch |
|-----------|---------------------|---------------------|--------|
| Tapestry  | RAG Indexing Guide  | 2025-08-04 19:08    | main   |

## Purpose

This document provides guidelines for indexing the Tapestry repository for Retrieval-Augmented Generation (RAG) systems. It covers tagging, question formulation, and clustering strategies to ensure high-quality, context-rich retrieval for downstream AI and search applications.

---

## 1. Tagging Guidelines

### 1.1. File-Level Tagging

- **Assign tags based on file purpose and taxonomy.**  
  Example tags: `frontend`, `backend`, `api`, `entity-schema`, `config`, `auth`, `ai`, `calendar`, `chore`, `points`, `goal`, `family`, `user`, `docs`, `setup`, `env`, `test`, `dependency`.

- **Use the taxonomy codes as meta-tags** for cross-referencing (e.g., `100-architecture`, `311-api`, `421-schema`).

- **Include modification date** from the file header for traceability.

### 1.2. Section-Level Tagging

- For large files (e.g., [backend/app/routers/chores.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/chores.py)), tag logical sections (e.g., endpoint definitions, business logic, model definitions) with:
  - `endpoint:<name>`
  - `model:<name>`
  - `logic:<purpose>`
  - `ai:<purpose>` (for LangGraph/AI logic)

- **Example:**  
  In [backend/app/routers/chores.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/chores.py) (Last modified: 2025-08-04 19:08):  
  - Tag `@router.post("/chores/")` as `endpoint:create-chore`, `api`, `chore`, `311-api`.

---

## 2. Question Generation

### 2.1. Coverage

- **Generate questions for each major entity, endpoint, and flow.**
- **Include both high-level and granular questions.**

### 2.2. Examples

- *What is the schema for a Chore?*  
  Tags: `chore`, `schema`, `421-schema`, `[backend/app/models/models.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/models/models.py)`

- *How does the AI chore generation pipeline work?*  
  Tags: `ai`, `chore`, `langgraph`, `[backend/app/ai/chore_graph.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/ai/chore_graph.py)`

- *How are points assigned and tracked?*  
  Tags: `points`, `logic`, `endpoint`, `[backend/app/routers/points.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/points.py)`

- *How does authentication work?*  
  Tags: `auth`, `jwt`, `[backend/app/routers/auth.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/auth.py)`, `701-auth`

- *How do I add a new family member?*  
  Tags: `family`, `user`, `endpoint`, `[backend/app/routers/families.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/families.py)`

### 2.3. Question Format

- Use clear, concise, and unambiguous language.
- Prefer "How", "What", "Where", "Which", and "Why" formulations.
- For code, reference project-relative paths and last modified dates.

---

## 3. Clustering Strategies

### 3.1. By Domain Entity

- Cluster all content related to a major entity (e.g., `Chore`, `User`, `Family`, `Goal`, `Calendar`).
- Include models, endpoints, business logic, and relevant UI components.

### 3.2. By Feature/Flow

- Cluster files and sections that together implement a feature (e.g., "Chore Completion", "Leaderboard Calculation", "Calendar Sync").

### 3.3. By Layer

- Group by architectural layer:
  - `frontend` (UI, Next.js components)
  - `backend` (API, models, routers)
  - `ai` (LangGraph, AI pipelines)
  - `config` (env, setup, package management)

### 3.4. By Taxonomy Code

- Use taxonomy codes (e.g., `311`, `421`, `701`) as cluster anchors for cross-cutting documentation and retrieval.

---

## 4. Indexing Process

1. **Extract file and section metadata:**  
   - Path, last modified date, taxonomy code(s), tags.

2. **Generate Q&A pairs:**  
   - For each tagged section, create at least one representative question and answer.

3. **Cluster Q&A pairs:**  
   - Assign to clusters as per above strategies.

4. **Store with references:**  
   - Always include project-relative path and last modified date for traceability.

---

## 5. Example Index Entry

```
{
  "question": "How does the backend assign points for completed chores?",
  "answer": "Points are assigned in [backend/app/routers/points.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/points.py) (Last modified: 2025-08-04 19:08) when a user marks a chore as complete. The endpoint updates the user's point total and emits an event for leaderboard recalculation.",
  "tags": ["points", "chore", "endpoint", "311-api"],
  "cluster": "points-tracking",
  "source": "[backend/app/routers/points.py](https://github.com/sergiomasellis/Tapestry/blob/main/backend/app/routers/points.py)",
  "last_modified": "2025-08-04 19:08"
}
```

---

## 6. Best Practices

- **Keep tags consistent and minimal.**
- **Update tags and clusters when files or flows change.**
- **Reference last modified dates for all indexed content.**
- **Favor semantic over syntactic clustering for better retrieval.**
- **Document any custom or project-specific tags in this guide.**

---

## Primary Sources

- [README.md](https://github.com/sergiomasellis/Tapestry/blob/main/README.md) (Last modified: 2025-08-04 19:08)
- [backend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/backend/README.md) (Last modified: 2025-08-04 19:08)
- backend/pyproject.toml (Last modified: 2025-08-04 19:08)
- [frontend/tsconfig.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/tsconfig.json) (Last modified: 2025-08-04 19:08)
- [frontend/package.json](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/package.json) (Last modified: 2025-08-04 19:08)
- [frontend/README.md](https://github.com/sergiomasellis/Tapestry/blob/main/frontend/README.md) (Last modified: 2025-08-04 19:08)

---

**Note:**  
For any new files or flows, update this guide with new tags, question templates, and clustering strategies as needed.