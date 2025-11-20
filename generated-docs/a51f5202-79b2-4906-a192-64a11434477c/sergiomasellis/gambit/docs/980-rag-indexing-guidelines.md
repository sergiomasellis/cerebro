# RAG Indexing Guidelines for Gambit

| Repo   | Doc Type            | Date       |
|--------|---------------------|------------|
| gambit | RAG Indexing Guide  | 2024-06-13 |

---

## Purpose

This document provides guidelines for Retrieval-Augmented Generation (RAG) indexing within the Gambit coding agent project. Proper RAG indexing ensures that documentation, code, and knowledge assets are discoverable, contextually relevant, and efficiently retrievable for both automated agents and human users.

---

## 1. Tagging Conventions

### 1.1. File-Level Tags

- **Location:** At the top of each Markdown or documentation file.
- **Format:** Use a `Tags:` line with comma-separated values.
- **Example:**
  ```
  Tags: api, agent, explain, usage
  ```

- **Recommended Tags:**
  - `api`, `agent`, `tool`, `explain`, `usage`, `install`, `config`, `test`, `dependency`, `prompt`, `tui`, `server`, `cli`, `workflow`, `diagnostics`, `schema`, `entity`, `security`, `auth`, `observability`, `runbook`, `ci`, `cd`, `decision`, `risk`, `rag`, `indexing`

### 1.2. Section-Level Tags

- **Location:** Before major sections in large documents.
- **Format:** Use a Markdown comment.
- **Example:**
  ```
  <!-- tags: api, endpoint, explain -->
  ```

---

## 2. Question Annotation

### 2.1. Explicit Q&A Blocks

- **Format:** Use a heading with `Q:` and `A:` for question-answer pairs.
- **Example:**
  ```markdown
  ### Q: How do I start the FastAPI server?
  A: Run `python main.py uv` from the project root.
  ```

- **Purpose:** Enables RAG systems to extract FAQs and direct answers for user queries.

### 2.2. Implicit Questions

- When documentation answers a question implicitly, add a hidden comment:
  ```
  <!-- answers: How do I install dependencies? -->
  ```

---

## 3. Clustering and Document Granularity

- **Cluster by Functionality:** Group related topics (e.g., all API endpoints, all tool descriptions) in single documents for efficient retrieval.
- **Granularity:** Prefer smaller, focused documents (e.g., one per tool, endpoint, or workflow) over monolithic files.
- **Cross-linking:** Use relative Markdown links to connect related documents.

---

## 4. Metadata for RAG

- **Mandatory Metadata Table:** Each indexed document must start with a table specifying:
  - Repo
  - Doc Type
  - Date
- **Example:**
  | Repo   | Doc Type   | Date       |
  |--------|------------|------------|
  | gambit | API Guide  | 2024-06-13 |

- **Additional Metadata:** Optionally include `Version`, `Author`, or `Source File` fields.

---

## 5. Indexing Prompts and Examples

- **Prompt Files:** Tag all prompt files (e.g., `gambit_coding_agent/prompts/*.prompt.md`) with `prompt`, `rag`, and relevant context tags.
- **Example Blocks:** Clearly mark code or API usage examples with `example` tags.

---

## 6. Updating the RAG Index

- **On Change:** Whenever documentation or code is updated, review and update tags and Q&A blocks.
- **Automation:** Consider scripts to extract tags and Q&A for building/updating the RAG index.

---

## 7. Example: RAG-Ready Document Structure

```markdown
| Repo   | Doc Type   | Date       |
|--------|------------|------------|
| gambit | API Guide  | 2024-06-13 |

Tags: api, endpoint, explain

<!-- tags: api, explain -->

### Q: How do I get an explanation for a code snippet?
A: Use the POST /explain endpoint with your code in the request body.
```

---

## 8. File and Directory Recommendations

- **Prompts:** `gambit_coding_agent/prompts/` — Tag with `prompt`, `rag`, `agent`.
- **API:** `gambit_coding_agent/server.py` — Tag with `api`, `server`, `endpoint`.
- **Tools:** `gambit_coding_agent/tools.py` — Tag with `tool`, `file`, `command`.
- **Tests:** `tests/` — Tag with `test`, `coverage`, `example`.
- **Workflows:** `.github/workflows/` — Tag with `ci`, `workflow`, `automation`.

---

## 9. RAG Indexing Checklist

- [ ] Metadata table present at top of each document.
- [ ] File-level tags included.
- [ ] Section-level tags for major topics.
- [ ] Q&A blocks for common questions.
- [ ] Prompt and example blocks clearly marked.
- [ ] Cross-links to related documents.
- [ ] Tags updated on every change.

---

## Primary Sources

- README.md
- gambit_coding_agent/prompts/todo.prompt.md
- gambit_coding_agent/prompts/system.prompt.md
- gambit_coding_agent/prompts/init.prompt.md
- gambit_coding_agent/server.py
- gambit_coding_agent/tools.py
- tests/test_todos.py
- tests/test_agent.py
- .github/workflows/python-app.yml
- setup.py
- pyproject.toml