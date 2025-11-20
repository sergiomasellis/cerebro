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
    MAX_TOTAL_CHARS = 150_000  # Safety cap (~40k tokens)

    # Initialize Repo object for git operations
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
                    return "\n".join(content)

                path = os.path.join(root, file)
                rel_path = os.path.relpath(path, root_path)

                # Get Git metadata (Last Commit Date)
                last_modified = "Unknown"
                if repo:
                    try:
                        # Get last commit for this specific file
                        # %cd = commit date, --date=iso-strict
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

                        # Add line numbers to content
                        numbered_lines = []
                        char_count = 0
                        limit_reached = False

                        for i, line in enumerate(lines, 1):
                            # Check per-file limit (approx 5k chars)
                            if char_count > 5000:
                                limit_reached = True
                                break

                            # Format: "120 | content"
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
