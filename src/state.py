from typing import List, TypedDict, Dict


class AgentState(TypedDict):
    repo_url: str
    local_path: str
    file_listing: List[str]

    # Planned docs to generate
    # Map of "doc_id" (e.g. "100") to "reason"
    planned_docs: Dict[str, str]

    # Generated Content
    # Map of "doc_id" to actual markdown content
    generated_content: Dict[str, str]

    # Metadata for the final report
    repo_name: str
    last_commit: str
    run_id: str
    branch_name: str
