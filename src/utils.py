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


def parse_dependencies(root_path: str) -> str:
    """Parse dependency files and extract comprehensive dependency information."""
    import json
    import re

    dependencies = {}
    dependency_files = []

    # Find all dependency files
    for root, dirs, files in os.walk(root_path):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith(".")]

        for file in files:
            if file in [
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
            ]:
                dependency_files.append(os.path.join(root, file))

    content_lines = []

    for dep_file in dependency_files:
        rel_path = os.path.relpath(dep_file, root_path)
        filename = os.path.basename(dep_file)

        try:
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
