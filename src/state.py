from typing import List, TypedDict, Dict, Annotated


def add_docs(left: Dict[str, str], right: Dict[str, str]) -> Dict[str, str]:
    return {**left, **right}


class FileRecord(TypedDict):
    """Lightweight file metadata for planning and retrieval without loading content."""

    path: str
    size: int
    mtime: str
    ext: str
    is_text: bool
    sha256: str | None


class AgentState(TypedDict, total=False):
    repo_url: str
    local_path: str
    file_listing: List[str]
    file_index: List[FileRecord]
    hash_index: Dict[str, List[str]]

    # Candidate files per doc id based on heuristics (pre-filter to avoid repeated walks)
    doc_candidates: Dict[str, List[str]]

    # Planned docs to generate
    # Map of "doc_id" (e.g. "100") to "reason"
    planned_docs: Dict[str, str]

    # Generated Content
    # Map of "doc_id" to actual markdown content
    generated_content: Annotated[Dict[str, str], add_docs]

    # Metadata for the final report
    repo_name: str
    last_commit: str
    run_id: str
    branch_name: str
