import os
import tempfile
import logging
import asyncio
import re
from git import Repo
from typing import Optional
import hashlib
import mimetypes
import time
try:
    from ast_grep_py import SgRoot
except ImportError:
    SgRoot = None
from datetime import datetime

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

FILE_SIZE_HARD_CAP = 2 * 1024 * 1024  # 2MB hard cap for snippetable files
HASH_SIZE_CAP = 512 * 1024  # Only hash files up to 512KB to avoid large reads
DEFAULT_MAX_FILES = 150_000  # Guardrail for extremely large repos
DEFAULT_CHUNK_SIZE = 128 * 1024  # 128KB chunks for oversize files
DEFAULT_MAX_CHUNKS_PER_FILE = 3  # Limit per file to avoid runaway reads


def _safe_stat(path: str) -> tuple[int, float]:
    try:
        st = os.stat(path)
        return st.st_size, st.st_mtime
    except OSError:
        return 0, 0.0


def _safe_hash(path: str, size: int) -> str | None:
    """Return sha256 for reasonably sized files; skip huge/binary files."""
    if size > HASH_SIZE_CAP:
        return None
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return None


def _is_text_candidate(path: str, size: int) -> bool:
    if size == 0:
        return False
    # For very large files, still consider text, but chunk separately downstream
    if size > FILE_SIZE_HARD_CAP:
        mime, _ = mimetypes.guess_type(path)
        return bool(mime and mime.startswith("text"))
    mime, _ = mimetypes.guess_type(path)
    if mime and not mime.startswith("text"):
        return False
    try:
        with open(path, "rb") as f:
            sample = f.read(2048)
        sample.decode("utf-8")
        return True
    except Exception:
        return False


def _format_mtime(ts: float) -> str:
    if not ts:
        return "Unknown"
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")


def build_file_index(root_path: str, max_files: int = DEFAULT_MAX_FILES):
    """
    Single-pass repository scan to collect lightweight metadata and deduplicate identical files.

    Returns:
        {
            "files": List[FileRecord],
            "hash_index": Dict[sha256, List[path]],
            "structure": str,
        }
    """
    files: list[dict] = []
    hash_index: dict[str, list[str]] = {}
    structure_lines: list[str] = []
    root_path = os.path.abspath(root_path)
    total_files = 0
    start_time = time.perf_counter()

    for current_root, dirs, file_names in os.walk(root_path):
        dirs[:] = [
            d
            for d in dirs
            if d not in IGNORE_DIRS and (not d.startswith(".") or d == ".github")
        ]

        level = current_root.replace(root_path, "").count(os.sep)
        indent = "  " * level
        structure_lines.append(f"{indent}{os.path.basename(current_root)}/")
        subindent = "  " * (level + 1)

        for file_name in file_names:
            if total_files >= max_files:
                structure_lines.append(f"{subindent}... (max files cap reached)")
                break
            if file_name.startswith("."):
                continue
            path = os.path.join(current_root, file_name)
            rel_path = os.path.relpath(path, root_path)

            size, mtime = _safe_stat(path)
            ext = os.path.splitext(file_name)[1].lstrip(".")
            is_text = _is_text_candidate(path, size)
            sha256 = _safe_hash(path, size) if is_text else None

            oversized = size > FILE_SIZE_HARD_CAP
            chunk_size = DEFAULT_CHUNK_SIZE
            chunk_count = (size // chunk_size) + (1 if size % chunk_size else 0) if oversized else 0

            record = {
                "path": rel_path,
                "size": size,
                "mtime": _format_mtime(mtime),
                "ext": ext,
                "is_text": is_text,
                "sha256": sha256,
                "oversized": oversized,
                "chunk_count": chunk_count,
            }
            files.append(record)
            total_files += 1

            if sha256:
                hash_index.setdefault(sha256, []).append(rel_path)

        if total_files >= max_files:
            break


    elapsed = time.perf_counter() - start_time
    logger.info(f"File index built in {elapsed:.4f}s")
    return {
        "files": files,
        "hash_index": hash_index,
        "structure": "\n".join(structure_lines),
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


def parse_dependencies(root_path: str, file_index: Optional[list[dict]] = None) -> str:
    """
    Parse dependency files and extract comprehensive dependency information.

    Uses the prebuilt file_index when available to avoid extra repo walks.
    """
    import json
    import re

    dependencies = {}
    dependency_files: list[str] = []
    dep_names = {
        "requirements.txt",
        "pyproject.toml",
        "package.json",
        "package-lock.json",
        "yarn.lock",
        "Pipfile",
        "Pipfile.lock",
        "Cargo.toml",
        "Cargo.lock",
        "pom.xml",
        "build.gradle",
        "build.gradle.kts",
        "go.mod",
        "go.sum",
    }

    if file_index:
        for record in file_index:
            basename = os.path.basename(record["path"])
            if basename in dep_names:
                dependency_files.append(os.path.join(root_path, record["path"]))
    else:
        # Find all dependency files via walk as a fallback
        for root, dirs, files in os.walk(root_path):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith(".")]
            for file in files:
                if file in dep_names:
                    dependency_files.append(os.path.join(root, file))

    content_lines = []

    for dep_file in dependency_files:
        rel_path = os.path.relpath(dep_file, root_path)
        filename = os.path.basename(dep_file)

        try:
            try:
                if os.path.getsize(dep_file) > FILE_SIZE_HARD_CAP:
                    content_lines.append(
                        f"## {filename} ({rel_path})\n- Skipped: file exceeds {FILE_SIZE_HARD_CAP} bytes cap\n"
                    )
                    continue
            except OSError:
                pass

            with open(dep_file, "r", encoding="utf-8") as f:
                file_content = f.read()

            content_lines.append(f"## {filename} ({rel_path})")
            content_lines.append("")

            if filename == "requirements.txt":
                # Parse requirements.txt
                lines = file_content.strip().split("\n")
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        # Parse package==version or package>=version, etc.
                        match = re.match(r"^([a-zA-Z0-9\-_.]+)([><=~!]+.+)?", line)
                        if match:
                            package = match.group(1)
                            version = match.group(2) if match.group(2) else "latest"
                            dependencies[package] = {
                                "version": version,
                                "source": "requirements.txt",
                                "type": "python",
                            }
                            content_lines.append(f"- **{package}** {version}")

            elif filename == "pyproject.toml":
                # Parse pyproject.toml
                try:
                    import tomllib

                    data = tomllib.loads(file_content)
                except ImportError:
                    # Fallback for older Python versions
                    try:
                        import tomli

                        data = tomli.loads(file_content)
                    except ImportError:
                        content_lines.append(
                            "Could not parse TOML file (missing tomli/tomllib)"
                        )
                        continue

                # Extract dependencies from various sections
                dep_sections = [
                    "dependencies",
                    "dev-dependencies",
                    "optional-dependencies",
                ]
                for section in dep_sections:
                    if "tool" in data and "poetry" in data["tool"]:
                        poetry_deps = data["tool"]["poetry"].get(section, {})
                        for pkg, version in poetry_deps.items():
                            dependencies[pkg] = {
                                "version": str(version),
                                "source": "pyproject.toml (poetry)",
                                "type": "python",
                            }
                            content_lines.append(f"- **{pkg}** {version}")

                    if "project" in data:
                        project_deps = data["project"].get(section, [])
                        for dep in project_deps:
                            if isinstance(dep, str):
                                match = re.match(
                                    r"^([a-zA-Z0-9\-_.]+)([><=~!]+.+)?", dep
                                )
                                if match:
                                    pkg = match.group(1)
                                    version = (
                                        match.group(2) if match.group(2) else "latest"
                                    )
                                    dependencies[pkg] = {
                                        "version": version,
                                        "source": "pyproject.toml (PEP 621)",
                                        "type": "python",
                                    }
                                    content_lines.append(f"- **{pkg}** {version}")

            elif filename == "package.json":
                # Parse package.json
                try:
                    data = json.loads(file_content)
                    dep_types = [
                        "dependencies",
                        "devDependencies",
                        "peerDependencies",
                        "optionalDependencies",
                    ]

                    for dep_type in dep_types:
                        if dep_type in data:
                            for pkg, version in data[dep_type].items():
                                dependencies[pkg] = {
                                    "version": version,
                                    "source": f"package.json ({dep_type})",
                                    "type": "javascript",
                                }
                                content_lines.append(f"- **{pkg}** {version}")
                except json.JSONDecodeError:
                    content_lines.append("Could not parse JSON file")

            elif filename == "Cargo.toml":
                # Parse Cargo.toml
                try:
                    import tomllib

                    data = tomllib.loads(file_content)
                except ImportError:
                    try:
                        import tomli

                        data = tomli.loads(file_content)
                    except ImportError:
                        content_lines.append(
                            "Could not parse TOML file (missing tomli/tomllib)"
                        )
                        continue

                if "dependencies" in data:
                    for pkg, version_info in data["dependencies"].items():
                        if isinstance(version_info, str):
                            version = version_info
                        elif isinstance(version_info, dict):
                            version = version_info.get("version", "latest")
                        else:
                            version = str(version_info)

                        dependencies[pkg] = {
                            "version": version,
                            "source": "Cargo.toml",
                            "type": "rust",
                        }
                        content_lines.append(f"- **{pkg}** {version}")

            elif filename == "go.mod":
                # Parse go.mod
                lines = file_content.strip().split("\n")
                for line in lines:
                    if line.startswith("require ") or line.startswith("\t"):
                        parts = line.strip().split()
                        if len(parts) >= 2:
                            pkg = parts[0]
                            version = parts[1] if len(parts) > 1 else "latest"
                            dependencies[pkg] = {
                                "version": version,
                                "source": "go.mod",
                                "type": "go",
                            }
                            content_lines.append(f"- **{pkg}** {version}")

            elif filename == "pom.xml":
                # Basic XML parsing for Maven
                # Look for dependency blocks
                import xml.etree.ElementTree as ET

                try:
                    root = ET.fromstring(file_content)
                    ns = {"mvn": "http://maven.apache.org/POM/4.0.0"}
                    for dep in root.findall(".//mvn:dependency", ns):
                        group_id = dep.find("mvn:groupId", ns)
                        artifact_id = dep.find("mvn:artifactId", ns)
                        version_elem = dep.find("mvn:version", ns)

                        if group_id is not None and artifact_id is not None:
                            pkg = f"{group_id.text}:{artifact_id.text}"
                            version = (
                                version_elem.text
                                if version_elem is not None
                                else "latest"
                            )
                            dependencies[pkg] = {
                                "version": version,
                                "source": "pom.xml",
                                "type": "java",
                            }
                            content_lines.append(f"- **{pkg}** {version}")
                except ET.ParseError:
                    content_lines.append("Could not parse XML file")

            content_lines.append("")

        except Exception as e:
            content_lines.append(f"Error reading {filename}: {e}")
            content_lines.append("")

    # Create summary section
    if dependencies:
        content_lines.insert(0, "## Dependency Summary")
        content_lines.insert(1, "")
        content_lines.insert(2, f"Total unique dependencies found: {len(dependencies)}")
        content_lines.insert(3, "")

        # Group by type
        by_type = {}
        for pkg, info in dependencies.items():
            dep_type = info["type"]
            if dep_type not in by_type:
                by_type[dep_type] = []
            by_type[dep_type].append((pkg, info))

        for dep_type, deps in by_type.items():
            content_lines.insert(
                4, f"### {dep_type.title()} Dependencies ({len(deps)})"
            )
            for pkg, info in sorted(deps):
                content_lines.insert(
                    5, f"- **{pkg}** {info['version']} - {info['source']}"
                )
            content_lines.insert(6, "")

    return "\n".join(content_lines)


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


def select_doc_candidates(file_index: list[dict]) -> dict[str, list[str]]:
    """Compute candidate paths per doc id using a single pass index."""
    candidates: dict[str, list[str]] = {
        "100": [],
        "101": [],
        "200": [],
        "311": [],
        "330": [],
        "421": [],
        "500": [],
        "600": [],
        "701": [],
        "720": [],
        "740": [],
        "760": [],
        "780": [],
        "800": [],
        "850": [],
        "900": [],
        "930": [],
        "980": [],
    }

    for record in file_index:
        path = record["path"]
        lower = path.lower()
        ext = record["ext"]

        if any(
            k in lower
            for k in ["readme", "architecture", "overview", "main", "app", "index"]
        ):
            candidates["100"].append(path)
        if any(k in lower for k in ["route", "router", "entry", "main", "app"]):
            candidates["101"].append(path)
        if any(
            k in lower
            for k in ["business", "domain", "logic", "service", "model", "entity"]
        ):
            candidates["200"].append(path)
        if any(k in lower for k in ["route", "controller", "api", "endpoint", "rest"]):
            candidates["311"].append(path)
        if ext in {"ts", "tsx", "js", "jsx", "kt", "kts", "java", "go"}:
            candidates["311"].append(path)
        if any(k in lower for k in ["event", "topic", "message", "queue"]):
            candidates["330"].append(path)
        if any(k in lower for k in ["model", "schema", "entity", "dto"]):
            candidates["421"].append(path)
        if any(
            k in lower
            for k in [
                "dependency",
                "package",
                "requirements",
                "pom",
                "cargo",
                "go.mod",
                "gradle",
            ]
        ) or ext in {"toml", "lock", "json", "gradle", "kts"}:
            candidates["500"].append(path)
        if any(
            k in lower
            for k in [
                "config",
                "env",
                "properties",
                "settings",
                "yaml",
                "dockerfile",
                "containerfile",
                "docker-compose",
                "compose.yaml",
                "compose.yml",
                "terraform",
                "terragrunt",
            ]
        ) or ext in {"tf", "tfvars", "hcl"}:
            candidates["600"].append(path)
        if any(k in lower for k in ["auth", "security", "login", "jwt"]):
            candidates["701"].append(path)
        if any(
            k in lower
            for k in [
                "test",
                "tests",
                "spec",
                "playwright",
                "cypress",
                "jest",
                "vitest",
                "junit",
                "surefire",
                "pytest",
                "tox",
                "unittest",
            ]
        ):
            candidates["720"].append(path)
        if ext in {"feature"} or "gherkin" in lower:
            candidates["720"].append(path)
        if any(
            k in lower
            for k in [
                "security",
                "snyk",
                "bandit",
                "semgrep",
                "trivy",
                "grype",
                "iam",
                "policy",
                "jwt",
                "oidc",
                "secrets",
                "vault",
            ]
        ):
            candidates["740"].append(path)
        if any(
            k in lower
            for k in [
                "perf",
                "performance",
                "benchmark",
                "load",
                "k6",
                "locust",
                "gatling",
                "wrk",
                "cache",
                "rate_limit",
                "throttle",
                "concurrency",
            ]
        ):
            candidates["760"].append(path)
        if any(
            k in lower
            for k in [
                "migration",
                "migrate",
                "schema",
                "prisma",
                "knex",
                "flyway",
                "liquibase",
                "db",
                "database",
                "sql",
                "ddl",
                "seed",
                "etl",
                "cdc",
            ]
        ):
            candidates["780"].append(path)
        if any(k in lower for k in ["log", "monitor", "observability", "metrics"]):
            candidates["800"].append(path)
        if any(k in lower for k in ["runbook", "failure", "debug", "restart"]):
            candidates["850"].append(path)
        if any(
            k in lower
            for k in [
                "ci",
                "cd",
                "pipeline",
                "workflow",
                "github",
                "gitlab",
                "jenkins",
                "harness",
                ".harness",
                "drone",
            ]
        ):
            candidates["900"].append(path)
        if any(k in lower for k in ["adr", "decision", "risk", "tradeoff"]):
            candidates["930"].append(path)

        # RAG catches all text candidates but we will sample later
        if record["is_text"]:
            candidates["980"].append(path)

    return candidates


# In-memory cache for file content: {abs_path: (mtime, content)}
file_cache: dict[str, tuple[float, str]] = {}

def extract_code_structure(content: str, lang: str) -> str:
    """
    Extracts code structure (classes, functions) using ast-grep.
    Returns a simplified version of the code.
    """
    if not SgRoot:
        return content

    try:
        root = SgRoot(content, lang)
        node = root.root()
        lines = []
        
        # Simple extraction: just list classes and functions
        # This is a basic implementation; can be enhanced
        
        # Classes
        classes = node.find_all(kind="class_definition")
        for cls in classes:
            name_node = cls.field("name")
            name = name_node.text() if name_node else "Unknown"
            lines.append(f"class {name}: ...")

        # Functions
        functions = node.find_all(kind="function_definition")
        for func in functions:
            name_node = func.field("name")
            name = name_node.text() if name_node else "Unknown"
            lines.append(f"def {name}(...): ...")
            
        if not lines:
            return content # Fallback if nothing found (e.g. script)
            
        return "\n".join(lines)
    except Exception as e:
        logging.getLogger("cerebro").warning(f"ast-grep extraction failed: {e}")
        return content

async def read_relevant_files_async(
    root_path: str,
    doc_id: str,
    candidate_paths: Optional[list[str]] = None,
    hash_index: Optional[dict[str, list[str]]] = None,
    max_total_chars: int = 500_000,
    size_map: Optional[dict[str, int]] = None,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    max_chunks_per_file: int = DEFAULT_MAX_CHUNKS_PER_FILE,
    smart_mode: bool = False,
) -> str:
    """
    Async version of read_relevant_files.
    Reads content of files relevant to a specific doc type with git metadata and line numbers.
    Uses asyncio.to_thread for non-blocking I/O and implements caching.
    """
    return await asyncio.to_thread(
        read_relevant_files,
        root_path,
        doc_id,
        candidate_paths,
        hash_index,
        max_total_chars,
        size_map,
        chunk_size,
        max_chunks_per_file,
        smart_mode
    )

def read_relevant_files(
    root_path: str,
    doc_id: str,
    candidate_paths: Optional[list[str]] = None,
    hash_index: Optional[dict[str, list[str]]] = None,
    max_total_chars: int = 500_000,
    size_map: Optional[dict[str, int]] = None,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    max_chunks_per_file: int = DEFAULT_MAX_CHUNKS_PER_FILE,
    smart_mode: bool = False,
) -> str:
    """
    Reads content of files relevant to a specific doc type with git metadata and line numbers.
    If candidate_paths is provided, only those files are read (no directory walk).
    hash_index allows deduplication: if two paths share a hash, only read once.
    """
    content: list[str] = []
    total_chars = 0
    seen_hashes = set()

    path_hash_map: dict[str, str] = {}
    start_time = time.perf_counter()
    if hash_index:
        for sha, paths in hash_index.items():
            for rel in paths:
                path_hash_map[rel] = sha

    try:
        repo = Repo(root_path)
    except Exception:
        repo = None

    paths_to_read: list[str] = []
    if candidate_paths is not None:
        for candidate in candidate_paths:
            full_path = os.path.join(root_path, candidate)
            if os.path.exists(full_path):
                paths_to_read.append(full_path)
    else:
        for root, dirs, files in os.walk(root_path):
            dirs[:] = [
                d
                for d in dirs
                if d not in IGNORE_DIRS and (not d.startswith(".") or d == ".github")
            ]
            for file in files:
                paths_to_read.append(os.path.join(root, file))

    for path in paths_to_read:
        rel_path = os.path.relpath(path, root_path)
        if total_chars >= max_total_chars:
            content.append("\n--- [TRUNCATED: MAX SIZE REACHED FOR DOC TYPE] ---\n")
            break

        # Deduplicate identical content
        if hash_index is not None:
            sha = path_hash_map.get(rel_path)
            if sha and sha in seen_hashes:
                continue
            if sha:
                seen_hashes.add(sha)

        # Determine size for chunking decisions
        file_size = size_map.get(rel_path) if size_map else None
        if file_size is None:
            try:
                file_size = os.path.getsize(path)
            except OSError:
                file_size = 0

        last_modified = "Unknown"
        if repo:
            try:
                last_modified = repo.git.log(
                    "-1", "--format=%cd", "--date=format:%Y-%m-%d %H:%M", rel_path
                )
            except Exception:
                pass

        # Choose reading strategy
        try:
            if file_size > chunk_size:
                # Chunked read
                chunks_read = 0
                offset = 0
                while chunks_read < max_chunks_per_file and total_chars < max_total_chars:
                    try:
                        with open(path, "r", encoding="utf-8", errors="ignore") as f:
                            f.seek(offset)
                            data = f.read(chunk_size)
                    except (UnicodeDecodeError, OSError):
                        break
                    if not data:
                        break
                    lines = data.splitlines()
                    numbered_lines = []
                    char_count = 0
                    for i, line in enumerate(lines, 1):
                        formatted_line = f"{i:4d} | {line}\n"
                        numbered_lines.append(formatted_line)
                        char_count += len(formatted_line)
                        if char_count + total_chars >= max_total_chars:
                            break

                    header = (
                        f"--- {rel_path} [chunk {chunks_read + 1} @ bytes {offset}-{offset + len(data)}] "
                        f"(Last modified: {last_modified}) ---"
                    )
                    content.append(f"{header}\n{''.join(numbered_lines)}\n")
                    total_chars += char_count
                    chunks_read += 1
                    offset += chunk_size
                    if total_chars >= max_total_chars:
                        break
            else:
                # Check cache first
                try:
                    mtime = os.path.getmtime(path)
                    if path in file_cache:
                        cached_mtime, cached_content = file_cache[path]
                        if cached_mtime == mtime:
                            lines = cached_content.splitlines(keepends=True)
                            # Skip file read, use cached lines
                            # But we still need to do the line numbering and truncation logic below
                            # which expects 'lines'
                        else:
                            # Cache invalid
                            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                                content_str = f.read()
                                file_cache[path] = (mtime, content_str)
                                lines = content_str.splitlines(keepends=True)
                    else:
                        # Not in cache
                        with open(path, "r", encoding="utf-8", errors="ignore") as f:
                            content_str = f.read()
                            file_cache[path] = (mtime, content_str)
                            lines = content_str.splitlines(keepends=True)
                except (UnicodeDecodeError, OSError):
                    continue



                # AST-Grep Smart Mode
                if smart_mode and path.endswith(".py"):
                    try:
                        # Re-join lines to get full content for AST parsing
                        full_content = "".join(lines)
                        structure = extract_code_structure(full_content, "python")
                        lines = structure.splitlines(keepends=True)
                        # Reset file size check effectively since we reduced content
                        file_size = len(structure) 
                    except Exception:
                        pass # Fallback to full content

                if file_size <= chunk_size:
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

        except (UnicodeDecodeError, OSError):
            continue

    elapsed = time.perf_counter() - start_time
    logger.info(f"read_relevant_files for {doc_id} took {elapsed:.4f}s")
    return "\n".join(content)
