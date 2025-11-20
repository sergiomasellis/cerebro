import os
import json
import uuid
import logging
import asyncio
import re
from typing import Dict
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from .state import AgentState
from .utils import (
    clone_repo,
    get_directory_structure,
    read_key_files,
    read_relevant_files,
)

logger = logging.getLogger("cerebro")

# Define the global taxonomy as a constant to guide the LLM
DOCS_TAXONOMY = """
000 - Index / table of contents
100 - Architecture & topology (High-level components, interaction, style)
101 - System Router (Entrypoints, routing logic)
200 - Domain & business rules (Entities, flows, context)
311 - REST API endpoints (Table of endpoints, purposes, semantics)
330 - Event topics (if applicable)
421 - Main entity schema (ER diagrams, key entities)
500 - Key dependencies (Internal services, 3rd party APIs)
600 - Config & environments (Files, vars, secrets management)
701 - Authentication model (Mechanisms, permissions)
800 - Observability overview (Logs, metrics, health)
850 - Runbook operations (Failure modes, debugging, restart)
900 - CI/CD pipeline (Build, test, deploy)
930 - Risks & decisions (ADRs, limitations, trade-offs)
980 - RAG indexing guidelines (Tags, questions, clustering)
"""


def get_llm():
    model_name = os.getenv("OPENAI_MODEL", "gpt-4o")
    return ChatOpenAI(model=model_name, temperature=0.2)


def clone_node(state: AgentState) -> Dict:
    url = state["repo_url"]
    branch = state.get("branch_name")
    logger.info(f"Executing clone_node for {url} (branch: {branch or 'default'})...")
    try:
        path = clone_repo(url, branch)
    except Exception as e:
        logger.warning(f"Clone failed ({e}), using current directory as fallback.")
        path = os.getcwd()

    structure = get_directory_structure(path)
    repo_name = url.split("/")[-1].replace(".git", "")
    run_id = str(uuid.uuid4())

    # Get current branch name
    try:
        from git import Repo

        repo = Repo(path)
        branch_name = repo.active_branch.name
        last_commit = repo.head.commit.hexsha[:7]
    except Exception:
        branch_name = "unknown"
        last_commit = "HEAD"

    logger.info(
        f"Repository cloned successfully. Run ID: {run_id}, Branch: {branch_name}"
    )
    return {
        "local_path": path,
        "file_listing": [structure],
        "repo_name": repo_name,
        "last_commit": last_commit,
        "branch_name": branch_name,
        "run_id": run_id,
    }


def plan_documentation(state: AgentState) -> Dict:
    """Decides which documents to generate based on repo content."""
    logger.info("Executing plan_documentation...")
    structure = state["file_listing"][0]
    key_content = read_key_files(state["local_path"])

    llm = get_llm()
    prompt = f"""
    You are a documentation strategist.
    Based on the file structure and key files, decide which of the following documents are relevant for this repository.
    Detect the tech stack (e.g., React, Angular, Spring Boot, FastAPI, or mixed) and adjust relevance accordingly.

    Taxonomy:
    {DOCS_TAXONOMY}

    Repo Structure:
    {structure}

    Key Content Preview:
    {key_content[:5000]}

    Return a JSON object where keys are the doc IDs (e.g., "100", "311") and values are a short reason why it's needed.
    ALWAYS include "100", "200", "900", "980". Include others only if evidence exists (e.g., "311" if routes found, "421" if models found).
    For mixed stacks, include docs for each detected technology.
    """

    messages = [
        SystemMessage(content="You return only JSON."),
        HumanMessage(content=prompt),
    ]

    try:
        response = llm.invoke(messages)
        content = (
            str(response.content).strip().replace("```json", "").replace("```", "")
        )
        plan = json.loads(content)
    except Exception as e:
        logger.error(f"Planning failed, falling back to defaults: {e}")
        plan = {"100": "Default", "200": "Default", "900": "Default", "980": "Default"}

    logger.info(f"Planned docs: {list(plan.keys())}")
    return {"planned_docs": plan}


async def generate_docs(state: AgentState) -> Dict:
    """Generates content for all planned docs in parallel."""
    logger.info("Executing generate_docs in parallel...")
    plan = state["planned_docs"]

    # Pre-load context once to avoid I/O thrashing in parallel threads
    path = state["local_path"]
    structure = state["file_listing"][0]
    key_content = read_key_files(path)  # Read ONCE

    llm = get_llm()

    async def generate_single_doc(doc_id: str, reason: str):
        logger.info(f"Starting generation for {doc_id}...")
        system_prompt = f"""
        You are a technical writer generating {doc_id} for the repo '{state.get("repo_name")}'.

        Follow these strict rules:
        1. Output MkDocs Material-compatible Markdown. Use Material theme features like admonitions (e.g., !!! note, !!! warning, !!! tip), tabs, and icons where appropriate.
        2. No YAML frontmatter.
        3. Start with a top-level # Title.
        4. Include a metadata table (Repo, Doc Type, Date).
        5. **METADATA REQUIREMENT**: In the metadata table, you MUST include the branch name: "{state.get("branch_name")}".
        6. **METADATA REQUIREMENT**: When citing files, refer to the "Last modified" dates provided in the file headers.
        7. Use project-relative paths for file references, without markdown links.
        8. Include a "Primary Sources" section at the end.
        9. If {doc_id} in ["100", "101", "311", "421"], INCLUDE A MERMAID DIAGRAM.
        10. Include small, relevant code snippets (3-10 lines) from the provided files to illustrate key concepts, wrapped in ```language blocks (e.g., ```python, ```typescript).
        11. Use admonitions for important notes, warnings, or tips to enhance readability.
        """

        user_prompt = f"""
        Generate the content for document ID {doc_id}.
        
        Reason/Context:
        {reason}
        
        File Structure:
        {structure}
        
        Key Files (with timestamps and line numbers):
        {key_content}
        """

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt),
        ]

        try:
            # Use ainvoke for async LLM call
            response = await llm.ainvoke(messages)
            return doc_id, str(response.content)
        except Exception as e:
            logger.error(f"Failed to generate {doc_id}: {e}")
            return doc_id, f"# Error\nFailed to generate document: {e}"

    # Launch all tasks
    tasks = [generate_single_doc(did, reason) for did, reason in plan.items()]
    results = await asyncio.gather(*tasks)

    generated = {doc_id: content for doc_id, content in results}

    logger.info(f"Generated {len(generated)} documents.")
    return {"generated_content": generated}


def fix_linkages(state: AgentState) -> Dict:
    """Fixes file linkages in generated docs to point to GitHub URLs."""
    logger.info("Executing fix_linkages...")
    base_url = (
        state["repo_url"].replace(".git", "") + "/blob/" + state["branch_name"] + "/"
    )
    generated = state["generated_content"]
    fixed = {}

    # Regex for file paths with common extensions
    pattern = r"\b([a-zA-Z0-9_/-]+\.(py|js|ts|md|json|yaml|yml|txt|html|css|xml|sh))\b"

    for doc_id, content in generated.items():

        def replace_path(match):
            path = match.group(1)
            full_path = os.path.join(state["local_path"], path)
            if os.path.exists(full_path):
                return f"[{path}]({base_url}{path})"
            else:
                return path  # leave as is

        fixed_content = re.sub(pattern, replace_path, content)
        fixed[doc_id] = fixed_content

    logger.info("Linkages fixed.")
    return {"generated_content": fixed}


def write_files(state: AgentState) -> Dict:
    """Writes all generated docs to disk."""
    logger.info("Executing write_files...")

    repo_url_parts = state["repo_url"].rstrip("/").split("/")
    if len(repo_url_parts) > 1:
        repo_full_name = f"{repo_url_parts[-2]}/{repo_url_parts[-1]}".replace(
            ".git", ""
        )
    else:
        repo_full_name = state["repo_name"]

    base_output_dir = os.path.join("generated-docs", state["run_id"], repo_full_name)
    docs_path = os.path.join(base_output_dir, "docs")

    os.makedirs(docs_path, exist_ok=True)
    logger.info(f"Output directory: {docs_path}")

    generated = state["generated_content"]

    # Taxonomy map for filenames
    names = {
        "100": "architecture-overview",
        "101": "system-router",
        "200": "business-domain-overview",
        "311": "rest-api-endpoints",
        "330": "event-topics",
        "421": "main-entity-schema",
        "500": "key-dependencies",
        "600": "config-and-environments",
        "701": "authentication-model",
        "800": "observability-overview",
        "850": "runbook-operations",
        "900": "ci-cd-pipeline",
        "930": "risks-and-decisions",
        "980": "rag-indexing-guidelines",
    }

    final_files = []

    for doc_id, content in generated.items():
        slug = names.get(doc_id, "misc-doc")
        filename = f"{doc_id}-{slug}.md"
        full_path = os.path.join(docs_path, filename)

        with open(full_path, "w") as f:
            f.write(content)
        final_files.append(f"docs/{filename}")

    # Generate Index
    logger.info("Generating index file...")
    index_content = "# Documentation Index\n\n"
    index_content += f"**Repository:** {state.get('repo_name')}\n\n"

    sorted_ids = sorted(generated.keys())
    for doc_id in sorted_ids:
        slug = names.get(doc_id, "misc-doc")
        filename = f"{doc_id}-{slug}.md"
        # Use project-relative link
        index_content += (
            f"- [{doc_id} - {slug.replace('-', ' ').title()}]({filename})\n"
        )

    with open(os.path.join(docs_path, "index.md"), "w") as f:
        f.write(index_content)
    final_files.insert(0, "docs/index.md")

    # Generate mkdocs.yml
    logger.info("Generating mkdocs.yml...")
    mkdocs_config = f"""site_name: '{state.get("repo_name")} Documentation'
site_description: 'Auto-generated documentation for {state.get("repo_name")}'
site_author: 'Cerebro AI'
site_url: ''

theme:
  name: material
  palette:
    - scheme: default
      primary: blue
      accent: blue
  features:
    - navigation.tabs
    - navigation.sections
    - toc.integrate
    - search.suggest
    - search.highlight
  icon:
    repo: fontawesome/brands/github

repo_url: '{state["repo_url"]}'
repo_name: '{state.get("repo_name")}'

nav:
  - Home: index.md
"""

    for doc_id in sorted_ids:
        slug = names.get(doc_id, "misc-doc")
        title = f"{doc_id} - {slug.replace('-', ' ').title()}"
        filename = f"{doc_id}-{slug}.md"
        mkdocs_config += f"  - '{title}': {filename}\n"

    with open(os.path.join(base_output_dir, "mkdocs.yml"), "w") as f:
        f.write(mkdocs_config)

    logger.info("All files written successfully.")
    return {"final_documentation": "\n".join(final_files)}


def create_doc_subgraph(doc_id: str):
    def node_func(state: AgentState) -> Dict:
        structure = state["file_listing"][0]
        relevant_content = read_relevant_files(state["local_path"], doc_id)
        llm = get_llm()
        system_prompt = f"""
        You are a technical writer generating {doc_id} for the repo '{state.get("repo_name")}'.

        Follow these strict rules:
        1. Output MkDocs Material-compatible Markdown. Use Material theme features like admonitions (e.g., !!! note, !!! warning, !!! tip), tabs, and icons where appropriate.
        2. No YAML frontmatter.
        3. Start with a top-level # Title.
        4. Include a metadata table (Repo, Doc Type, Date).
        5. **METADATA REQUIREMENT**: In the metadata table, you MUST include the branch name: "{state.get("branch_name")}".
        6. **METADATA REQUIREMENT**: When citing files, refer to the "Last modified" dates provided in the file headers.
        7. Use project-relative paths for file references, without markdown links.
        8. Include a "Primary Sources" section at the end.
        9. If {doc_id} in ["100", "101", "311", "421"], INCLUDE A MERMAID DIAGRAM.
        10. Include small, relevant code snippets (3-10 lines) from the provided files to illustrate key concepts, wrapped in ```language blocks (e.g., ```python, ```typescript).
        11. Include admonitions for important notes, warnings, or tips to enhance readability.
        """

        user_prompt = f"""
        Generate the content for document ID {doc_id}.

        Reason/Context:
        Auto-generated for {doc_id}.

        File Structure:
        {structure}

        Key Files (with timestamps and line numbers):
        {relevant_content}
        """

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt),
        ]

        try:
            response = llm.invoke(messages)
            return {"generated_content": {doc_id: str(response.content)}}
        except Exception as e:
            return {
                "generated_content": {
                    doc_id: f"# Error\nFailed to generate document: {e}"
                }
            }

    return node_func
