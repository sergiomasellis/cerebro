import os
import json
import uuid6
import logging
import asyncio
import re
import time
from datetime import datetime
from typing import Dict
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from .state import AgentState
from .utils import (
    clone_repo,
    build_file_index,
    read_relevant_files,
    read_relevant_files_async,
    parse_dependencies,
    read_relevant_files,
    read_relevant_files_async,
    parse_dependencies,
    select_doc_candidates,
)
from .config import settings
from .models import CerebroConfig
import pydantic

logger = logging.getLogger("cerebro")


def extract_latest_date(content: str) -> str:
    """Extract the latest last modified date from file headers in the content."""
    pattern = r"Last modified: (\d{4}-\d{2}-\d{2} \d{2}:\d{2})"
    dates = re.findall(pattern, content)
    if not dates:
        return datetime.now().strftime("%Y-%m-%d")
    # Parse and find the latest
    parsed_dates = []
    for date_str in dates:
        try:
            parsed_dates.append(datetime.strptime(date_str, "%Y-%m-%d %H:%M"))
        except ValueError:
            continue
    if not parsed_dates:
        return datetime.now().strftime("%Y-%m-%d")
    latest = max(parsed_dates)
    return latest.strftime("%Y-%m-%d")


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
720 - Testing & quality (Test strategy, coverage gates, tooling)
740 - Security posture (AuthZ hooks, scanners, secrets handling)
760 - Performance & scalability (Caching, concurrency, throttling)
780 - Data & migrations (Schema evolution, migrations, data jobs)
800 - Observability overview (Logs, metrics, health)
850 - Runbook operations (Failure modes, debugging, restart)
900 - CI/CD pipeline (Build, test, deploy)
930 - Risks & decisions (ADRs, limitations, trade-offs)
980 - RAG indexing guidelines (Tags, questions, clustering)
"""


def get_llm():
    model_name = settings.OPENAI_MODEL
    return ChatOpenAI(model=model_name, temperature=0.2)


def clone_node(state: AgentState) -> Dict:
    url = state["repo_url"]
    branch = state.get("branch_name")
    logger.info("🔄 STAGE 1/7: Cloning Repository")
    logger.info(f"   Repository URL: {url}")
    logger.info(f"   Target branch: {branch or 'default'}")

    try:
        logger.info(
            "   📥 Cloning repository (this may take a moment for large repos)..."
        )
        path = clone_repo(url, branch)
        logger.info("   ✅ Clone successful")
    except Exception as e:
        logger.warning(
            f"   ⚠️  Clone failed ({e}), using current directory as fallback."
        )
        path = os.getcwd()

    logger.info("   📁 Indexing repository (single pass)...")
    index_result = build_file_index(path)
    structure = index_result["structure"]
    file_index = index_result["files"]
    hash_index = index_result["hash_index"]
    repo_name = url.split("/")[-1].replace(".git", "")
    run_id = str(uuid6.uuid7())

    # Get current branch name
    try:
        from git import Repo

        repo = Repo(path)
        branch_name = repo.active_branch.name
        last_commit = repo.head.commit.hexsha[:7]
        logger.info(f"   📋 Branch: {branch_name}, Last commit: {last_commit}")
    except Exception:
        branch_name = "unknown"
        last_commit = "HEAD"
        logger.info("   📋 Could not determine branch/commit info")

    logger.info(f"   🎯 Run ID: {run_id}")
    logger.info("   ✅ Repository preparation complete")
    return {
        "local_path": path,
        "file_listing": [structure],
        "file_index": file_index,
        "hash_index": hash_index,
        "doc_candidates": select_doc_candidates(file_index),
        "repo_name": repo_name,
        "last_commit": last_commit,
        "branch_name": branch_name,
        "run_id": run_id,
    }


def plan_documentation(state: AgentState) -> Dict:
    """Decides which documents to generate based on repo content and optional config."""
    logger.info("🔄 STAGE 2/7: Planning Documentation")
    
    path = state["local_path"]
    config_path = os.path.join(path, ".cerebro", "cerebro.json")
    cerebro_config = None
    
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config_data = json.load(f)
                cerebro_config = CerebroConfig(**config_data)
                logger.info("   ⚙️  Loaded .cerebro/cerebro.json configuration")
        except Exception as e:
            logger.warning(f"   ⚠️  Failed to load .cerebro/cerebro.json: {e}")

    # If pages are explicitly defined, use them
    if cerebro_config and cerebro_config.pages:
        logger.info(f"   📋 Using explicit page configuration ({len(cerebro_config.pages)} pages)")
        plan = {}
        for i, page in enumerate(cerebro_config.pages):
            # Use title as ID if simple, else generate one
            # For simplicity, we'll try to map known titles to IDs or use custom IDs
            # But the system expects specific IDs for some logic (like 100, 200).
            # If the user provides custom pages, we might lose the taxonomy benefits.
            # However, the requirement says: "bypass the default cluster-based planning and create exactly the pages you specify"
            
            # We need a way to map these custom pages to the doc_id system or extend it.
            # Let's generate a pseudo-ID for custom pages if they don't match standard ones.
            # Or better, just use the title as the key if the downstream supports it.
            # The downstream `generate_docs` uses `titles.get(doc_id, "Document")`.
            # So if we pass the title as doc_id, it might work if we adjust `generate_docs`.
            
            # Let's use a prefix "custom-" + index to avoid collisions and keep order
            doc_id = f"custom-{i:03d}"
            plan[doc_id] = f"Explicitly requested page: {page.title}. Purpose: {page.purpose}"
            
            # Store metadata for generation
            state.setdefault("custom_pages", {})[doc_id] = page

        logger.info(f"   📝 Planned {len(plan)} custom pages")
        return {"planned_docs": plan, "cerebro_config": cerebro_config}

    logger.info(
        "   📋 Analyzing repository content to determine relevant documentation..."
    )

    structure = state["file_listing"][0]
    doc_candidates = state.get("doc_candidates", {})

    mandatory = {
        "100": "Always generate architecture overview",
        "200": "Always generate business/domain overview",
    }
    plan: Dict[str, str] = dict(mandatory)

    candidate_summary = {}
    for doc_id, files in doc_candidates.items():
        if doc_id in mandatory:
            continue
        if files:
            plan[doc_id] = f"Found {len(files)} relevant files"
        candidate_summary[doc_id] = {"count": len(files), "examples": files[:5]}

    llm = get_llm()
    
    # Inject repo_notes into planning prompt if available
    repo_notes_context = ""
    if cerebro_config and cerebro_config.repo_notes:
        notes_text = "\n".join([f"- {note.content}" for note in cerebro_config.repo_notes])
        repo_notes_context = f"\nRepository Notes from User:\n{notes_text}\n"

    prompt = {
        "taxonomy": DOCS_TAXONOMY,
        "structure": structure[:4000],
        "candidates": candidate_summary,
        "repo_notes": repo_notes_context,
        "instruction": (
            'Return JSON mapping doc_id -> reason. Always include "100","200". '
            "Keep only doc_ids with evidence (count > 0). If no evidence, exclude the doc_id."
            "Consider the provided repository notes when making decisions."
        ),
    }

    messages = [
        SystemMessage(content="You return only compact JSON with reasons."),
        HumanMessage(content=json.dumps(prompt)),
    ]

    try:
        logger.info("   ⏳ AI planning in progress...")
        response = llm.invoke(messages)
        content = (
            str(response.content).strip().replace("```json", "").replace("```", "")
        )
        refined = json.loads(content)
        refined.update({k: v for k, v in plan.items() if k not in refined})
        plan = refined
        logger.info("   ✅ AI planning completed")
    except Exception as e:
        logger.error(f"   ❌ AI planning failed, using heuristic plan: {e}")

    if "000" in plan:
        del plan["000"]

    planned_count = len(plan)
    logger.info(
        f"   📝 Planned {planned_count} documentation sections: {', '.join(plan.keys())}"
    )
    logger.info("   ✅ Documentation planning complete")
    return {"planned_docs": plan, "cerebro_config": cerebro_config}


async def generate_docs(state: AgentState) -> Dict:
    """Generates content for all planned docs in parallel."""
    logger.info("🔄 STAGE 3/7: Generating Documentation")
    start_time = time.perf_counter()
    plan = state["planned_docs"]
    planned_count = len(plan)

    logger.info(
        f"   📝 Starting parallel generation of {planned_count} documentation sections..."
    )

    path = state["local_path"]
    structure = state["file_listing"][0]
    doc_candidates = state.get("doc_candidates", {})
    hash_index = state.get("hash_index", {})
    llm = get_llm()
    semaphore = asyncio.Semaphore(settings.CONCURRENT_DOCS)
    file_sizes = {rec["path"]: rec.get("size", 0) for rec in state.get("file_index", [])}
    max_default_candidates = settings.MAX_DOC_CANDIDATES
    max_rag_candidates = settings.MAX_RAG_CANDIDATES

    async def generate_single_doc(doc_id: str, reason: str):
        titles = {
            "100": "Architecture Overview",
            "101": "System Router",
            "200": "Business Domain Overview",
            "311": "REST API Endpoints",
            "330": "Event Topics",
            "421": "Main Entity Schema",
            "500": "Key Dependencies",
            "600": "Config and Environments",
            "701": "Authentication Model",
            "720": "Testing & Quality",
            "740": "Security Posture",
            "760": "Performance & Scalability",
            "780": "Data & Migrations",
            "800": "Observability Overview",
            "850": "Runbook Operations",
            "900": "CI/CD Pipeline",
            "930": "Risks and Decisions",
            "980": "RAG Indexing Guidelines",
        }
        
        custom_page = state.get("custom_pages", {}).get(doc_id)
        if custom_page:
            title = custom_page.title
        else:
            title = titles.get(doc_id, "Document")

        logger.info(f"   🤖 Generating {doc_id}: {title}...")
        all_candidates = doc_candidates.get(doc_id, [])
        max_candidates = max_rag_candidates if doc_id == "980" else max_default_candidates

        def batched(seq, size):
            for i in range(0, len(seq), size):
                yield seq[i : i + size]

        candidate_batches = list(batched(sorted(all_candidates, key=lambda p: file_sizes.get(p, 0)), max_candidates))
        if len(all_candidates) > max_candidates:
            logger.info(
                f"   📑 Processing {len(all_candidates)} candidates in {len(candidate_batches)} batches of {max_candidates} for {doc_id}"
            )
        doc_content = ""
        if doc_id == "500":
            relevant_content = parse_dependencies(path, state.get("file_index"))
            relevant_batches = [("deps", relevant_content)]
        else:
            relevant_batches = []
            if candidate_batches:
                for idx, batch in enumerate(candidate_batches, 1):
                    relevant_batches.append((f"{idx}/{len(candidate_batches)}", await read_relevant_files_async(
                        path,
                        doc_id,
                        candidate_paths=batch,
                        hash_index=hash_index,
                        size_map=file_sizes,
                        max_total_chars=300_000 if doc_id == "980" else 200_000,
                        smart_mode=(doc_id in ["100", "200"]),
                    )))
            else:
                # No candidates; still run once with empty content to allow "Not found" messaging
                relevant_batches.append(("1/1", ""))
        for batch_label, relevant_content in relevant_batches:
            latest_date = extract_latest_date(relevant_content)
            existing_excerpt = doc_content[-8000:] if doc_content else ""

        extra_sections = ""
        if doc_id == "100":
            extra_sections = """
            Include a subsection "Agent Workflow & Large Files" that explains how the documentation agent works for any repo:
            - Repo scan and file indexing (single pass, ignore vendor dirs).
            - Candidate selection by doc type.
            - Chunked reading for oversized files (128KB chunks, limited per file), dedup by sha256.
            - Concurrency controls on LLM calls.
            If prompt/config files exist (e.g., AGENTS.md, example.prompt.md, README), reference them; otherwise describe the generic workflow."""
        elif doc_id == "980":
            extra_sections = """
            Add a section "Agent Prompts & Pipeline" that, if available, cites repo prompt/config files (e.g., example.prompt.md, AGENTS.md) and otherwise summarizes the generic workflow for planning docs, chunking large files, and writing outputs.
            Add a "Large File Handling" subsection summarizing chunk sizes, chunk limits, dedup, and sampling rules."""

        system_prompt = f"""
        You are a technical writer generating {doc_id} for the repo '{state.get("repo_name")}'.

        Follow these strict rules:
        1. Output MkDocs Material-compatible Markdown. Use Material theme features like admonitions (e.g., !!! note, !!! warning, !!! tip), tabs, and icons where appropriate.
        2. No YAML frontmatter.
        3. Start with a top-level # {title}.
        4. Include a metadata table (Repo, Doc Type, Date) and set Date to {latest_date}. Doc Type MUST be the descriptive title "{title}" (not the numeric id).
        5. **METADATA REQUIREMENT**: In the metadata table, you MUST include the branch name: "{state.get("branch_name")}".
        6. **METADATA REQUIREMENT**: When citing files, refer to the "Last modified" dates provided in the file headers.
        7. Use project-relative paths for file references, without markdown links.
        8. Include a "Primary Sources" section at the end using markdown footnotes (e.g., [^1]: path/to/file.ext). Cite these footnotes INLINE immediately after the file reference (e.g., "In utils.py[^1]..."). Do NOT add a "Sources: ..." line at the end. If no sources, omit the section.
        9. If {doc_id} in ["100", "101", "311", "421"], INCLUDE A MERMAID DIAGRAM.
        10. Include small, relevant code snippets (3-10 lines) from the provided files to illustrate key concepts, wrapped in ```language blocks (e.g., ```python title="Descriptive title (filename.ext)", ```typescript).
        11. Include admonitions for important notes, warnings, or tips to enhance readability.
        12. MERMAID RULES: only flowchart syntax; keep labels alphanumeric/spaces; no special chars (<, >, :, |); each edge must end at a valid node; prefer `A[Label] --> B[Label]`; avoid indentation; use consistent arrow style.
        13. PRIMARY SOURCES RULES: do not output placeholders like "Sources: 1 2"; always use inline citations like `[^1]` in the text. Define the footnotes at the end with project-relative paths only (strip any temp/local prefixes). Omit the section if there are no sources.
        14. TABS: You may use MkDocs Material tabbed syntax (pymdownx.tabbed, e.g., `=== "Title"`) when it improves clarity.
        15. ACCURACY: If a topic or data is not present in the provided content, explicitly say "Not found in repository" and do NOT invent or speculate. Do not fabricate CI/CD, APIs, or other sections when no evidence exists.
        {extra_sections}
        {extra_sections}
        """
        
        # Inject repo notes if available
        cerebro_config = state.get("cerebro_config")
        if cerebro_config and cerebro_config.repo_notes:
            notes_text = "\n".join([f"- {note.content}" for note in cerebro_config.repo_notes])
            system_prompt += f"\n\nIMPORTANT REPOSITORY CONTEXT:\n{notes_text}\n"
            
        if custom_page:
            system_prompt += f"\n\nPAGE SPECIFIC INSTRUCTIONS:\nTitle: {custom_page.title}\nPurpose: {custom_page.purpose}\n"
            if custom_page.page_notes:
                page_notes = "\n".join([f"- {note}" for note in custom_page.page_notes])
                system_prompt += f"Notes:\n{page_notes}\n"

        user_prompt = f"""
Generate the content for document ID {doc_id}.

Reason/Context:
{reason}

File Structure:
{structure}

Existing draft (keep and merge; renumber footnotes consistently across batches; do not drop earlier content):
{existing_excerpt or "None yet"}

New sources batch {batch_label} (with timestamps and line numbers):
{relevant_content}
"""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt),
        ]

        try:
            async with semaphore:
                response = await llm.ainvoke(messages)
            doc_content = str(response.content)
        except Exception as e:
            logger.error(f"   ❌ Failed to generate {doc_id} batch {batch_label}: {e}")
            return doc_id, f"# Error\nFailed to generate document: {e}"

        logger.info(f"   ✅ Completed {doc_id}: {title}")
        return doc_id, doc_content

    # Launch all tasks
    logger.info("   🚀 Launching parallel AI generation tasks...")
    tasks = [generate_single_doc(did, reason) for did, reason in plan.items()]
    results = await asyncio.gather(*tasks)

    generated = {doc_id: content for doc_id, content in results}

    logger.info(f"   ✅ Generated {len(generated)} documentation sections successfully")
    elapsed = time.perf_counter() - start_time
    logger.info(f"   ✅ Documentation generation complete in {elapsed:.2f}s")
    return {"generated_content": generated}


def fix_linkages(state: AgentState) -> Dict:
    """Fixes file linkages in generated docs to point to GitHub URLs."""
    logger.info("🔄 STAGE 4/7: Fixing Linkages")
    logger.info("   🔗 Converting file references to GitHub links...")

    base_url = (
        state["repo_url"].replace(".git", "") + "/blob/" + state["branch_name"] + "/"
    )
    generated = state["generated_content"]
    fixed = {}

    # Regex for file paths with common extensions
    pattern = r"\b([a-zA-Z0-9_/-]+\.(py|js|ts|md|json|yaml|yml|txt|html|css|xml|sh))\b"

    total_docs = len(generated)
    processed = 0

    for doc_id, content in generated.items():
        processed += 1
        logger.info(f"   🔗 Processing {doc_id} ({processed}/{total_docs})...")

        def replace_path(match):
            path = match.group(1)
            full_path = os.path.join(state["local_path"], path)
            if os.path.exists(full_path):
                return f"[{path}]({base_url}{path})"
            else:
                return path  # leave as is

        # Split content by code block fences to avoid linking inside code blocks
        parts = content.split("```")
        for i in range(len(parts)):
            if i % 2 == 0:  # Even indices are outside code blocks
                parts[i] = re.sub(pattern, replace_path, parts[i])
        fixed_content = "```".join(parts)
        fixed[doc_id] = fixed_content

    logger.info(f"   ✅ Fixed linkages for {total_docs} documents")
    logger.info("   ✅ Linkage fixing complete")
    return {"generated_content": fixed}


def write_files(state: AgentState) -> Dict:
    """Writes all generated docs to disk."""
    logger.info("🔄 STAGE 5/7: Writing Files")
    logger.info("   💾 Preparing output directory...")

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
    logger.info(f"   📁 Output directory: {docs_path}")

    generated = state["generated_content"]

    # Taxonomy map for filenames and titles
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
        "720": "testing-and-quality",
        "740": "security-posture",
        "760": "performance-and-scalability",
        "780": "data-and-migrations",
        "800": "observability-overview",
        "850": "runbook-operations",
        "900": "ci-cd-pipeline",
        "930": "risks-and-decisions",
        "980": "rag-indexing-guidelines",
    }
    titles = {
        "100": "Architecture Overview",
        "101": "System Router",
        "200": "Business Domain Overview",
        "311": "REST API Endpoints",
        "330": "Event Topics",
        "421": "Main Entity Schema",
        "500": "Key Dependencies",
        "600": "Config and Environments",
        "701": "Authentication Model",
        "720": "Testing & Quality",
        "740": "Security Posture",
        "760": "Performance & Scalability",
        "780": "Data & Migrations",
        "800": "Observability Overview",
        "850": "Runbook Operations",
        "900": "CI/CD Pipeline",
        "930": "Risks and Decisions",
        "930": "Risks and Decisions",
        "980": "RAG Indexing Guidelines",
    }
    
    # Update names/titles for custom pages
    custom_pages = state.get("custom_pages", {})
    for doc_id, page in custom_pages.items():
        slug = page.title.lower().replace(" ", "-")
        names[doc_id] = slug
        titles[doc_id] = page.title

    final_files = []
    total_docs = len(generated)
    written = 0

    logger.info(f"   📄 Writing {total_docs} documentation files...")
    for doc_id, content in generated.items():
        written += 1
        slug = names.get(doc_id, "misc-doc")
        filename = f"{doc_id}-{slug}.md"
        full_path = os.path.join(docs_path, filename)

        # Ensure content is properly encoded as UTF-8
        if isinstance(content, str):
            content_utf8 = content
        else:
            content_utf8 = str(content)

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content_utf8)
        final_files.append(f"docs/{filename}")
        logger.info(f"   📄 Written {doc_id} ({written}/{total_docs})")

    # Generate Index
    logger.info("   📋 Generating documentation index...")
    index_content = "# Documentation Index\n\n"
    index_content += f"**Repository:** {state.get('repo_name')}\n\n"

    sorted_ids = sorted(generated.keys())
    for doc_id in sorted_ids:
        slug = names.get(doc_id, "misc-doc")
        title = titles.get(doc_id, slug.replace("-", " ").title())
        filename = f"{doc_id}-{slug}.md"
        # Use project-relative link
        index_content += f"- [{title}]({filename})\n"

    with open(os.path.join(docs_path, "index.md"), "w", encoding="utf-8") as f:
        f.write(index_content)
    final_files.insert(0, "docs/index.md")
    logger.info("   ✅ Index file generated")

    # Generate mkdocs.yml
    logger.info("   ⚙️  Generating MkDocs configuration...")
    mkdocs_config = f"""site_name: '{state.get("repo_name")} Documentation'
site_description: 'Auto-generated documentation for {state.get("repo_name")}'
site_author: 'Cerebro AI'
site_url: ''

theme:
  name: material
  palette:
    # Dark-first palette with orange highlights
    - scheme: slate
      primary: custom
      accent: deep orange
      toggle:
        icon: material/white-balance-sunny
        name: Switch to light mode

    # Optional light mode for users who prefer it
    - scheme: default
      primary: custom
      accent: deep orange
      toggle:
        icon: material/weather-night
        name: Switch to dark mode
  features:
    - navigation.tabs
    - navigation.sections
    - toc.integrate
    - search.suggest
    - search.highlight
    - content.code.copy
    - content.code.annotate
  icon:
    repo: fontawesome/brands/github

extra_css:
  - styles/theme.css

markdown_extensions:
  - admonition
  - footnotes
  - pymdownx.highlight:
      anchor_linenums: true
      line_spans: __span
      pygments_lang_class: true
  - pymdownx.inlinehilite
  - pymdownx.snippets
  - pymdownx.tabbed:
      alternate_style: true
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format

nav:
  - Home: index.md
"""

    for doc_id in sorted_ids:
        slug = names.get(doc_id, "misc-doc")
        title = titles.get(doc_id, slug.replace("-", " ").title())
        filename = f"{doc_id}-{slug}.md"
        mkdocs_config += f"  - '{title}': {filename}\n"

    styles_dir = os.path.join(docs_path, "styles")
    os.makedirs(styles_dir, exist_ok=True)
    theme_css = """
:root {
  --md-primary-fg-color: #ff8a1f;
  --md-primary-fg-color--light: #ffb14a;
  --md-primary-fg-color--dark: #d66900;
  --md-accent-fg-color: #ff9c2f;
}

[data-md-color-scheme="default"],
[data-md-color-scheme="slate"] {
  --md-default-bg-color: #0f131a;
  --md-default-fg-color: #e8ecf1;
  --md-default-fg-color--light: #f5f7fb;
  --md-default-fg-color--lighter: #cfd6e1;
  --md-default-fg-color--lightest: #aeb7c4;
  --md-typeset-a-color: #ff9c2f;
  --md-typeset-a-color--hover: #ffb14a;
  --md-code-bg-color: #111827;
  --md-code-fg-color: #e8ecf1;
  --md-code-hl-color: #172033;
  --md-code-border-color: #1b2433;
  --md-shadow-z2: 0 10px 30px rgba(0, 0, 0, 0.45);
}

[data-md-color-scheme="slate"] .md-header,
[data-md-color-scheme="slate"] .md-tabs {
  background-color: #0c1016;
}

[data-md-color-scheme="slate"] .md-sidebar__scrollwrap,
[data-md-color-scheme="slate"] .md-nav--primary {
  background-color: #0c1016;
}

[data-md-color-scheme="slate"] .md-nav__link--active,
[data-md-color-scheme="slate"] .md-nav__link:focus,
[data-md-color-scheme="slate"] .md-nav__link:hover {
  color: #ffb14a;
}

[data-md-color-scheme="slate"] .md-button--primary {
  background-color: #ff9c2f;
  border-color: #ff9c2f;
  color: #0f131a;
}

[data-md-color-scheme="slate"] .md-button--primary:hover {
  background-color: #ffb14a;
  border-color: #ffb14a;
  color: #0a0d12;
}
"""
    styles_path = os.path.join(styles_dir, "theme.css")
    with open(styles_path, "w", encoding="utf-8") as css_file:
        css_file.write(theme_css)
    logger.info(f"   🎨 Theme overrides written to {styles_path}")

    with open(os.path.join(base_output_dir, "mkdocs.yml"), "w", encoding="utf-8") as f:
        f.write(mkdocs_config)

    logger.info("   ✅ MkDocs configuration generated")
    logger.info(f"   🎉 All {len(final_files)} files written successfully")
    logger.info("   ✅ File writing complete")
    return {"final_documentation": "\n".join(final_files)}


def create_overview(state: AgentState) -> Dict:
    """Creates a complete overview page and updates the Documentation Index."""
    logger.info("🔄 STAGE 6/7: Creating Overview")
    logger.info("   📊 Generating comprehensive system overview...")

    generated = state["generated_content"]
    repo_name = state.get("repo_name", "Unknown Repo")

    logger.info("   📁 Collecting indexed file inventory...")
    file_index = state.get("file_index", [])
    inventory_lines = []
    max_inventory = 2000
    for i, record in enumerate(file_index):
        if i >= max_inventory:
            inventory_lines.append("... [TRUNCATED: inventory shortened for brevity] ...")
            break
        inventory_lines.append(
            f"- {record['path']} | {record.get('ext') or 'noext'} | {record.get('size', 0)} bytes | Modified: {record.get('mtime', 'Unknown')}"
        )
    all_files_info = f"Total files indexed: {len(file_index)}\n\n" + "\n".join(
        inventory_lines
    )

    # Prepare content from all generated docs for LLM
    all_docs_content = "\n\n".join(
        [f"## {doc_id}\n{content}" for doc_id, content in generated.items()]
    )

    llm = get_llm()

    # Generate the overview document
    logger.info("   🤖 AI generating system overview document...")
    overview_prompt = f"""
    You are a technical writer creating a comprehensive system overview for the repository '{repo_name}'.

    Based on all the generated documentation and complete file listing below, create a complete overview page that synthesizes the entire system.

    IMPORTANT: Ensure complete coverage of ALL files in the repository. The goal is file-by-file documentation and understanding.

    Follow these strict rules:
    1. Output MkDocs Material-compatible Markdown.
    2. No YAML frontmatter.
    3. Start with a top-level # System Overview.
    4. Include a metadata table (Repo, Doc Type, Date, Branch).
    5. Provide a high-level summary of the entire system based on all documents.
    6. Include sections for key components, architecture, and how everything fits together.
    7. Include a comprehensive "File Inventory" section that covers ALL files (not just key ones) with their purposes and roles.
    8. Use admonitions for important notes.
    9. Include a Mermaid diagram showing the overall system architecture if possible. MERMAID RULES: use flowchart syntax only; consistent arrow style; no special characters in labels (<, >, :, |); ensure every edge has a valid target; keep labels short and alphanumeric with spaces; prefer `A[Label] --> B[Label]`.
    10. Include a brief "Agent Workflow & Large Files" note describing repo scan, candidate selection, chunked reads for oversized files, and how prompts (e.g., AGENTS.md/example.prompt.md) drive documentation generation.
    10. End with a "Primary Sources" section using markdown footnotes (e.g., [^1]: docs/xyz.md) listing all documents used. Cite these footnotes INLINE immediately after the file reference (e.g., "As seen in the architecture doc[^1]..."). Do NOT add a "Sources: ..." line. Define the footnotes at the end using project-relative paths only. Tabs are allowed (pymdownx.tabbed `=== "Title"`) when they improve clarity. If information is missing, state "Not found in repository" instead of speculating.

    Complete File Listing (ALL files in repository):
    {all_files_info}

    Generated Documentation Content:
    {all_docs_content[:8000]}  # Truncate if too long
    """

    messages = [
        SystemMessage(
            content="You return only the markdown content for the overview document."
        ),
        HumanMessage(content=overview_prompt),
    ]

    try:
        logger.info("   ⏳ AI overview generation in progress...")
        response = llm.invoke(messages)
        overview_content = str(response.content)
        logger.info("   ✅ System overview document generated")
    except Exception as e:
        logger.error(f"   ❌ Failed to generate overview: {e}")
        overview_content = f"# System Overview\n\nError generating overview: {e}"

    # Add overview to generated content
    updated_generated = dict(generated)
    updated_generated["000"] = overview_content

    # Now update the index.md with the required sections
    logger.info("   📋 Enhancing documentation index...")
    repo_url_parts = state["repo_url"].rstrip("/").split("/")
    if len(repo_url_parts) > 1:
        repo_full_name = f"{repo_url_parts[-2]}/{repo_url_parts[-1]}".replace(
            ".git", ""
        )
    else:
        repo_full_name = state["repo_name"]

    base_output_dir = os.path.join("generated-docs", state["run_id"], repo_full_name)
    docs_path = os.path.join(base_output_dir, "docs")
    index_path = os.path.join(docs_path, "index.md")

    # Read existing index
    with open(index_path, "r") as f:
        existing_index = f.read()

    # Generate enhanced index content
    logger.info("   🤖 AI enhancing index with detailed sections...")
    enhanced_index_prompt = f"""
    You are enhancing the Documentation Index page for '{repo_name}'.

    Based on all generated documentation and complete file listing, update the index to include these sections at the top:

    - Purpose and Scope
    - What is this Repo about?
    - Repo Structure (format as a markdown table with columns: Directory/File | Description - ensure ALL directories and files are covered)
    - Repository Architecture Overview
    - Key Components
    - Module Descriptions

    IMPORTANT: Ensure the Repo Structure table includes comprehensive coverage of ALL files and directories in the repository.

    Output MkDocs Material-compatible Markdown for these sections only.
    Do not include the document list - that will be added separately.
    Do not include YAML frontmatter.
    Use proper markdown formatting that works with MkDocs Material theme.
    If you reference specific files, use markdown footnotes (e.g., [^1]: path/to/file.ext) and cite them INLINE immediately after the reference (e.g., utils.py[^1]). Define footnotes at the end.

    Complete File Listing (ALL files in repository):
    {all_files_info}

    Generated Documentation Summary:
    {all_docs_content[:4000]}

    Return only the markdown content for the new sections.
    """

    messages_index = [
        SystemMessage(
            content="You return only the updated markdown content for the index."
        ),
        HumanMessage(content=enhanced_index_prompt),
    ]

    try:
        logger.info("   ⏳ AI index enhancement in progress...")
        response_index = llm.invoke(messages_index)
        new_sections = str(response_index.content).strip()
        # Prepend new sections to existing index
        updated_index_content = new_sections + "\n\n" + existing_index
        logger.info("   ✅ Documentation index enhanced")
    except Exception as e:
        logger.error(f"   ❌ Failed to update index: {e}")
        updated_index_content = existing_index  # Fallback to existing

    # Write updated index
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(updated_index_content)

    # Write the overview file
    overview_filename = "000-system-overview.md"
    overview_path = os.path.join(docs_path, overview_filename)
    with open(overview_path, "w", encoding="utf-8") as f:
        f.write(overview_content)
    logger.info("   📄 System overview file written")

    # Update mkdocs.yml to include the overview
    mkdocs_path = os.path.join(base_output_dir, "mkdocs.yml")
    with open(mkdocs_path, "r") as f:
        mkdocs_content = f.read()

    # Add overview to nav
    nav_line = "  - Home: index.md\n"
    overview_nav = f"  - 'System Overview': {overview_filename}\n"
    updated_mkdocs = mkdocs_content.replace(nav_line, nav_line + overview_nav)

    with open(mkdocs_path, "w", encoding="utf-8") as f:
        f.write(updated_mkdocs)

    logger.info("   ⚙️  MkDocs navigation updated")
    logger.info("   ✅ Overview creation and index enhancement complete")
    logger.info("🔄 STAGE 7/7: Documentation Generation Complete")
    logger.info("   🎉 All documentation has been successfully generated!")
    return {"generated_content": updated_generated}
