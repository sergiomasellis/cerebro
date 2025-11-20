import os
import tempfile
import logging
from git import Repo
from typing import Optional

logger = logging.getLogger("cerebro")


def clone_repo(repo_url: str, branch: Optional[str] = None) -> str:
    """Clones a repository to a temporary directory."""
    temp_dir = tempfile.mkdtemp()
    try:
        # Use shallow clone for performance on large repos
        logger.debug(f"Cloning {repo_url} to {temp_dir}...")
        if branch:
            Repo.clone_from(
                repo_url, temp_dir, depth=1, single_branch=True, branch=branch
            )
        else:
            Repo.clone_from(repo_url, temp_dir, depth=1, single_branch=True)
        return temp_dir
    except Exception as e:
        logger.error(f"Clone operation failed: {e}")
        raise Exception(f"Failed to clone repo: {e}")


IGNORE_DIRS = {
    "node_modules",
    "target",
    "build",
    "dist",
    "out",
    "venv",
    ".venv",
    "env",
    ".env",
    "virtualenv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".git",
    ".svn",
    ".hg",
    ".idea",
    ".vscode",
    ".settings",
    "vendor",
    "bower_components",
    "jspm_packages",
    "bin",
    "obj",
    "tmp",
    "temp",
    "logs",
    "coverage",
}


def get_directory_structure(root_path: str, max_depth: int = 3) -> str:
    """Returns a string representation of the directory structure."""
    output = []
    root_path = os.path.abspath(root_path)

    for root, dirs, files in os.walk(root_path):
        # Filter directories in-place
        dirs[:] = [
            d
            for d in dirs
            if d not in IGNORE_DIRS and (not d.startswith(".") or d == ".github")
        ]

        level = root.replace(root_path, "").count(os.sep)
        if level > max_depth:
            continue

        indent = "  " * level
        output.append(f"{indent}{os.path.basename(root)}/")
        subindent = "  " * (level + 1)

        # Limit file listing per directory to avoid massive output in huge folders
        files_to_list = [f for f in files if not f.startswith(".")]
        if len(files_to_list) > 50:
            output.append(f"{subindent}... ({len(files_to_list)} files)")
        else:
            for f in files_to_list:
                output.append(f"{subindent}{f}")

    return "\n".join(output)


def read_key_files(root_path: str) -> str:
    """Reads content of critical files with git metadata and line numbers."""
    # specific filenames
    key_files = {
        "README.md",
        "README",
        "readme.md",
        "bitbucket-pipelines.yml",
        ".gitlab-ci.yml",
        "azure-pipelines.yml",
        "docker-compose.yml",
        "docker-compose.yaml",
        "Dockerfile",
        "Containerfile",
        "pyproject.toml",
        "requirements.txt",
        "setup.py",
        "package.json",
        "tsconfig.json",
        "pom.xml",
        "build.gradle",
        "build.gradle.kts",
        "Makefile",
        "Justfile",
        "Procfile",
        "go.mod",
        "Cargo.toml",
        "mix.exs",
    }

    content = []
    total_chars = 0
    MAX_TOTAL_CHARS = 1_000_000  # Increased for large repos (~250k tokens)

    try:
        repo = Repo(root_path)
    except Exception:
        repo = None

    for root, dirs, files in os.walk(root_path):
        # Filter directories in-place
        dirs[:] = [
            d
            for d in dirs
            if d not in IGNORE_DIRS and (not d.startswith(".") or d == ".github")
        ]

        for file in files:
            is_key_file = file in key_files
            is_github_workflow = ".github/workflows" in root and file.endswith(
                (".yml", ".yaml")
            )

            if is_key_file or is_github_workflow:
                if total_chars >= MAX_TOTAL_CHARS:
                    content.append("\n--- [TRUNCATED: MAX SIZE REACHED] ---\n")
                    break

                path = os.path.join(root, file)
                rel_path = os.path.relpath(path, root_path)

                last_modified = "Unknown"
                if repo:
                    try:
                        last_modified = repo.git.log(
                            "-1",
                            "--format=%cd",
                            "--date=format:%Y-%m-%d %H:%M",
                            rel_path,
                        )
                    except Exception:
                        pass

                try:
                    with open(path, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                        numbered_lines = []
                        char_count = 0
                        limit_reached = False

                        for i, line in enumerate(lines, 1):
                            if char_count > 10000:
                                limit_reached = True
                                break
                            formatted_line = f"{i:4d} | {line}"
                            numbered_lines.append(formatted_line)
                            char_count += len(formatted_line)

                        file_content = "".join(numbered_lines)
                        if limit_reached:
                            file_content += "\n... [File truncated] ...\n"

                        header = f"--- {rel_path} (Last modified: {last_modified}) ---"
                        content.append(f"{header}\n{file_content}\n")
                        total_chars += char_count

                except Exception:
                    pass

    return "\n".join(content)


def get_all_files_info(root_path: str) -> str:
    """Gets information about all files in the repository (except filtered directories)."""
    content = []
    total_files = 0

    try:
        repo = Repo(root_path)
    except Exception:
        repo = None

    for root, dirs, files in os.walk(root_path):
        # Filter directories in-place (same as other functions)
        dirs[:] = [
            d
            for d in dirs
            if d not in IGNORE_DIRS and (not d.startswith(".") or d == ".github")
        ]

        for file in files:
            # Skip hidden files
            if file.startswith("."):
                continue

            path = os.path.join(root, file)
            rel_path = os.path.relpath(path, root_path)

            # Get file size
            try:
                file_size = os.path.getsize(path)
            except Exception:
                file_size = 0

            # Get last modified date
            last_modified = "Unknown"
            if repo:
                try:
                    last_modified = repo.git.log(
                        "-1", "--format=%cd", "--date=format:%Y-%m-%d %H:%M", rel_path
                    )
                except Exception:
                    pass

            # Get file extension for type
            _, ext = os.path.splitext(file)
            file_type = ext[1:] if ext else "no extension"

            content.append(
                f"- {rel_path} | {file_type} | {file_size} bytes | Modified: {last_modified}"
            )
            total_files += 1

            # Limit to prevent massive output
            if total_files >= 1000:
                content.append("... [TRUNCATED: Too many files] ...")
                break

        if total_files >= 1000:
            break

    return f"Total files: {total_files}\n\n" + "\n".join(content)


def read_relevant_files(root_path: str, doc_id: str) -> str:
    """Reads content of files relevant to a specific doc type, with git metadata and line numbers."""
    # Define relevance criteria per doc_id
    relevance_filters = {
        "100": lambda file, root: any(
            keyword in file.lower() or keyword in root.lower()
            for keyword in [
                "readme",
                "architecture",
                "overview",
                "main",
                "app",
                "index",
            ]
        ),  # Architecture
        "101": lambda file, root: any(
            keyword in file.lower() or keyword in root.lower()
            for keyword in ["route", "router", "entry", "main", "app"]
        ),  # System Router
        "200": lambda file, root: any(
            keyword in file.lower() or keyword in root.lower()
            for keyword in ["business", "domain", "logic", "service", "model"]
        ),  # Business domain
        "311": lambda file, root: any(
            keyword in file.lower() or keyword in root.lower()
            for keyword in ["route", "controller", "api", "endpoint", "rest"]
        )
        or file.endswith((".js", ".ts", ".py", ".java", ".go")),  # REST API
        "330": lambda file, root: any(
            keyword in file.lower() or keyword in root.lower()
            for keyword in ["event", "topic", "message", "queue"]
        ),  # Events
        "421": lambda file, root: any(
            keyword in file.lower() or keyword in root.lower()
            for keyword in ["model", "schema", "entity", "dto"]
        ),  # Entity schema
        "500": lambda file, root: any(
            keyword in file.lower() or keyword in root.lower()
            for keyword in ["dependency", "package", "requirements", "pom", "cargo"]
        ),  # Dependencies
        "600": lambda file, root: any(
            keyword in file.lower() or keyword in root.lower()
            for keyword in ["config", "env", "properties", "settings", "yml", "yaml"]
        ),  # Config
        "701": lambda file, root: any(
            keyword in file.lower() or keyword in root.lower()
            for keyword in ["auth", "security", "login", "jwt"]
        ),  # Auth
        "800": lambda file, root: any(
            keyword in file.lower() or keyword in root.lower()
            for keyword in ["log", "monitor", "observability", "metrics"]
        ),  # Observability
        "850": lambda file, root: any(
            keyword in file.lower() or keyword in root.lower()
            for keyword in ["runbook", "failure", "debug", "restart"]
        ),  # Runbook
        "900": lambda file, root: any(
            keyword in file.lower() or keyword in root.lower()
            for keyword in [
                "ci",
                "cd",
                "pipeline",
                "workflow",
                "github",
                "gitlab",
                "jenkins",
            ]
        ),  # CI/CD
        "930": lambda file, root: any(
            keyword in file.lower() or keyword in root.lower()
            for keyword in ["adr", "decision", "risk", "tradeoff"]
        ),  # Risks
        "980": lambda file, root: True,  # RAG: all files, but limited
    }

    filter_func = relevance_filters.get(doc_id, lambda f, r: False)

    content = []
    total_chars = 0
    MAX_TOTAL_CHARS = 500_000  # Per doc type limit

    try:
        repo = Repo(root_path)
    except Exception:
        repo = None

    for root, dirs, files in os.walk(root_path):
        dirs[:] = [
            d
            for d in dirs
            if d not in IGNORE_DIRS and (not d.startswith(".") or d == ".github")
        ]

        for file in files:
            if not filter_func(file, root):
                continue
            if total_chars >= MAX_TOTAL_CHARS:
                content.append("\n--- [TRUNCATED: MAX SIZE REACHED FOR DOC TYPE] ---\n")
                return "\n".join(content)

            path = os.path.join(root, file)
            rel_path = os.path.relpath(path, root_path)

            last_modified = "Unknown"
            if repo:
                try:
                    last_modified = repo.git.log(
                        "-1", "--format=%cd", "--date=format:%Y-%m-%d %H:%M", rel_path
                    )
                except Exception:
                    pass

            try:
                with open(path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    numbered_lines = []
                    char_count = 0
                    limit_reached = False

                    for i, line in enumerate(lines, 1):
                        if char_count > 10000:
                            limit_reached = True
                            break
                        formatted_line = f"{i:4d} | {line}"
                        numbered_lines.append(formatted_line)
                        char_count += len(formatted_line)

                    file_content = "".join(numbered_lines)
                    if limit_reached:
                        file_content += "\n... [File truncated] ...\n"

                    header = f"--- {rel_path} (Last modified: {last_modified}) ---"
                    content.append(f"{header}\n{file_content}\n")
                    total_chars += char_count

            except Exception:
                pass

    return "\n".join(content)
    # Define relevance criteria per doc_id
    relevance_filters = {
        "100": lambda file, root: any(
            keyword in file.lower() or keyword in root.lower()
            for keyword in [
                "readme",
                "architecture",
                "overview",
                "main",
                "app",
                "index",
            ]
        ),  # Architecture
        "101": lambda file, root: any(
            keyword in file.lower() or keyword in root.lower()
            for keyword in ["route", "router", "entry", "main", "app"]
        ),  # System Router
        "200": lambda file, root: any(
            keyword in file.lower() or keyword in root.lower()
            for keyword in ["business", "domain", "logic", "service", "model"]
        ),  # Business domain
        "311": lambda file, root: any(
            keyword in file.lower() or keyword in root.lower()
            for keyword in ["route", "controller", "api", "endpoint", "rest"]
        )
        or file.endswith((".js", ".ts", ".py", ".java", ".go")),  # REST API
        "330": lambda file, root: any(
            keyword in file.lower() or keyword in root.lower()
            for keyword in ["event", "topic", "message", "queue"]
        ),  # Events
        "421": lambda file, root: any(
            keyword in file.lower() or keyword in root.lower()
            for keyword in ["model", "schema", "entity", "dto"]
        ),  # Entity schema
        "500": lambda file, root: any(
            keyword in file.lower() or keyword in root.lower()
            for keyword in ["dependency", "package", "requirements", "pom", "cargo"]
        ),  # Dependencies
        "600": lambda file, root: any(
            keyword in file.lower() or keyword in root.lower()
            for keyword in ["config", "env", "properties", "settings", "yml", "yaml"]
        ),  # Config
        "701": lambda file, root: any(
            keyword in file.lower() or keyword in root.lower()
            for keyword in ["auth", "security", "login", "jwt"]
        ),  # Auth
        "800": lambda file, root: any(
            keyword in file.lower() or keyword in root.lower()
            for keyword in ["log", "monitor", "observability", "metrics"]
        ),  # Observability
        "850": lambda file, root: any(
            keyword in file.lower() or keyword in root.lower()
            for keyword in ["runbook", "failure", "debug", "restart"]
        ),  # Runbook
        "900": lambda file, root: any(
            keyword in file.lower() or keyword in root.lower()
            for keyword in [
                "ci",
                "cd",
                "pipeline",
                "workflow",
                "github",
                "gitlab",
                "jenkins",
            ]
        ),  # CI/CD
        "930": lambda file, root: any(
            keyword in file.lower() or keyword in root.lower()
            for keyword in ["adr", "decision", "risk", "tradeoff"]
        ),  # Risks
        "980": lambda file, root: True,  # RAG: all files, but limited
    }

    filter_func = relevance_filters.get(doc_id, lambda f, r: False)

    content = []
    total_chars = 0
    MAX_TOTAL_CHARS = 500_000  # Per doc type limit

    try:
        repo = Repo(root_path)
    except Exception:
        repo = None

    for root, dirs, files in os.walk(root_path):
        dirs[:] = [
            d
            for d in dirs
            if d not in IGNORE_DIRS and (not d.startswith(".") or d == ".github")
        ]

        for file in files:
            if not filter_func(file, root):
                continue
            if total_chars >= MAX_TOTAL_CHARS:
                content.append("\n--- [TRUNCATED: MAX SIZE REACHED FOR DOC TYPE] ---\n")
                return "\n".join(content)

            path = os.path.join(root, file)
            rel_path = os.path.relpath(path, root_path)

            last_modified = "Unknown"
            if repo:
                try:
                    last_modified = repo.git.log(
                        "-1", "--format=%cd", "--date=format:%Y-%m-%d %H:%M", rel_path
                    )
                except Exception:
                    pass

            try:
                with open(path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    numbered_lines = []
                    char_count = 0
                    limit_reached = False

                    for i, line in enumerate(lines, 1):
                        if char_count > 10000:
                            limit_reached = True
                            break
                        formatted_line = f"{i:4d} | {line}"
                        numbered_lines.append(formatted_line)
                        char_count += len(formatted_line)

                    file_content = "".join(numbered_lines)
                    if limit_reached:
                        file_content += "\n... [File truncated] ...\n"

                    header = f"--- {rel_path} (Last modified: {last_modified}) ---"
                    content.append(f"{header}\n{file_content}\n")
                    total_chars += char_count

            except Exception:
                pass

    return "\n".join(content)
