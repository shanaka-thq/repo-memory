#!/usr/bin/env python3
"""Validate Repo Memory structure and adopted project docs."""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path


SKILL_PACKAGE = Path("skills/repo-memory")

REQUIRED_REPO_FILES = [
    "README.md",
    "AGENTS.md",
    "CHANGELOG.md",
    "SECURITY.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SUPPORT.md",
    "ROADMAP.md",
    ".gitignore",
    ".gitattributes",
    ".markdownlint.json",
    ".github/workflows/pr-checks.yml",
    ".github/workflows/release.yml",
]

REQUIRED_SKILL_PACKAGE_FILES = [
    "skills/repo-memory/SKILL.md",
    "skills/repo-memory/STANDARD.md",
    "skills/repo-memory/LICENSE.txt",
    "skills/repo-memory/references/templates.md",
    "skills/repo-memory/references/docs-structure-rules.md",
    "skills/repo-memory/references/existing-project-audit.md",
    "skills/repo-memory/references/evidence-extraction-workflow.md",
    "skills/repo-memory/references/decision-log-reconstruction.md",
    "skills/repo-memory/references/continuity-governance.md",
    "skills/repo-memory/references/agent-integration-and-enforcement.md",
    "skills/repo-memory/references/superpowers-compatibility.md",
    "skills/repo-memory/references/documentation-metadata-schema.md",
    "skills/repo-memory/agents/openai-codex.md",
    "skills/repo-memory/agents/github-copilot.md",
    "skills/repo-memory/agents/claude-code.md",
    "skills/repo-memory/agents/opencode.md",
    "skills/repo-memory/agents/openai.yaml",
    "skills/repo-memory/examples/README.md",
    "skills/repo-memory/scripts/forward-test.py",
    "skills/repo-memory/scripts/scaffold-docs.py",
    "skills/repo-memory/scripts/validate-docs.py",
]

CONTINUITY_PROJECT_DOCS = [
    "docs/README.md",
    "docs/doc-health.md",
    "docs/feature-registry.md",
]

BASELINE_PROJECT_DOCS = [
    "docs/README.md",
    "docs/project-overview.md",
    "docs/architecture.md",
    "docs/interfaces-and-contracts.md",
    "docs/data-model.md",
    "docs/local-development.md",
    "docs/doc-health.md",
    "docs/observability-and-instrumentation.md",
    "docs/testing-strategy.md",
    "docs/operations-runbook.md",
    "docs/security-and-privacy.md",
    "docs/decision-log.md",
    "docs/implementation-log.md",
    "docs/feature-registry.md",
    "docs/requirements/functional-requirements.md",
    "docs/requirements/non-functional-requirements.md",
    "docs/features/_template.md",
]

REQUIRED_HEADINGS = {
    "docs/project-overview.md": [
        "Project Goal",
        "Problem Statement",
        "Target Users or Actors",
        "Success Criteria",
        "Current Scope",
        "Non-Goals",
        "Evidence",
    ],
    "docs/observability-and-instrumentation.md": [
        "Logs",
        "Metrics",
        "Traces",
        "Product Analytics Events",
        "Audit Events",
        "Dashboards and Alerts",
        "Privacy and Retention",
        "Known Blind Spots",
    ],
    "docs/feature-registry.md": [
        "Next Work Queue",
        "Feature List",
    ],
}

OPTIONAL_REQUIRED_HEADINGS = {
    "docs/requirements/user-stories-and-use-cases.md": [
        "Actors",
        "Personas or User Segments",
        "User Stories",
        "Journey Map",
        "Primary Use Cases",
        "Accessibility and Inclusion Notes",
        "Open Questions",
    ],
}

OPTIONAL_DEEP_DIVE_DIRS = [
    "docs/diagrams",
    "docs/designs",
    "docs/project-details",
    "docs/components",
    "docs/reviews",
    "docs/ui-ux",
]

RAW_INTAKE_DIRS = [
    Path("docs/intake"),
]

GENERATED_ARTIFACT_NAMES = {
    "__pycache__",
    ".pytest_cache",
    ".DS_Store",
    "agent-final.txt",
}

IGNORED_DIR_NAMES = {
    ".git", ".github", ".claude",
    "node_modules", ".venv", "venv", "env",
    "dist", "build", "out", "target",
    ".next", ".nuxt", ".cache", ".turbo",
    "vendor", "coverage", ".idea", ".vscode",
}

ALLOWED_FEATURE_STATUSES = {
    "research",
    "planned",
    "in_progress",
    "blocked",
    "implemented",
    "verified",
    "shipped",
    "abandoned",
    "superseded",
    "deprecated",
    "rolled_back",
}

TERMINAL_FEATURE_STATUSES = {
    "implemented",
    "verified",
    "shipped",
}

ACTIVE_FEATURE_STATUSES = {
    "research",
    "planned",
    "in_progress",
    "blocked",
}

ALLOWED_QUEUE_READY = {
    "ready",
    "verify-first",
    "needs-human",
    "blocked",
}

COMPLETED_FEATURE_EVIDENCE_PATTERNS = [
    re.compile(pattern, re.IGNORECASE | re.MULTILINE)
    for pattern in [
        r"^\s*Validation status:\s*(implemented|verified|shipped|complete|completed|passed|validated)\b",
        r"^\s*-\s*\[x\]\s+Finish scoped behavior\b",
        r"^\s*-\s*\[x\]\s+Update docs and validation notes\b",
        r"^\s{0,3}## Verified Behavior\s*$",
    ]
]

STALE_TERMINAL_HANDOFF_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in [
        r"\binterrupted\b",
        r"\bresume carefully\b",
        r"\bdo not discard uncommitted\b",
        r"\bpartial (rounding )?changes\b",
        r"\bpartial work\b",
        r"next safe step:\s*inspect the working tree",
        r"validation status:\s*interrupted",
    ]
]

KEBAB_PATH = re.compile(r"^[a-z0-9][a-z0-9-]*(\.[a-z0-9-]+)*$")
LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
FENCE_LINE = re.compile(r"^( {0,3})([`~]{3,})(.*)$")
VERSION = re.compile(r"^Version:\s*(\d+\.\d+(?:\.\d+)?)", re.MULTILINE)
HEADING = re.compile(r"^\s{0,3}#{2,6}\s+(.+?)\s*$", re.MULTILINE)
STATUS = re.compile(r"^\s*Status:\s*([a-z_]+)\b", re.MULTILINE | re.IGNORECASE)
SECTION = re.compile(r"^\s{0,3}##\s+(.+?)\s*$", re.MULTILINE)
CANONICAL_OWNER_HEADING = "Canonical Ownership Map"

CAPABILITY_DEFAULTS = {
    "goal": "docs/project-overview.md",
    "overview": "docs/project-overview.md",
    "functional requirements": "docs/requirements/functional-requirements.md",
    "non-functional requirements": "docs/requirements/non-functional-requirements.md",
    "architecture": "docs/architecture.md",
    "interfaces": "docs/interfaces-and-contracts.md",
    "contract": "docs/interfaces-and-contracts.md",
    "data model": "docs/data-model.md",
    "local development": "docs/local-development.md",
    "tooling": "docs/local-development.md",
    "testing": "docs/testing-strategy.md",
    "observability": "docs/observability-and-instrumentation.md",
    "operations": "docs/operations-runbook.md",
    "runbook": "docs/operations-runbook.md",
    "security": "docs/security-and-privacy.md",
    "privacy": "docs/security-and-privacy.md",
    "decisions": "docs/decision-log.md",
    "implementation": "docs/implementation-log.md",
    "feature state": "docs/feature-registry.md",
    "feature registry": "docs/feature-registry.md",
    "doc health": "docs/doc-health.md",
}

ALLOWED_DOC_TYPES = {
    "readme", "ownership-map", "project-overview", "architecture",
    "functional-requirements", "non-functional-requirements",
    "user-stories-and-use-cases", "interfaces-and-contracts", "data-model",
    "local-development", "doc-health", "observability-and-instrumentation",
    "testing-strategy", "operations-runbook", "security-and-privacy",
    "decision-log", "implementation-log", "feature-registry", "feature",
    "feature-logic", "feature-component", "diagram-index", "design",
    "review-record", "project-detail", "component", "ui-ux"
}

ALLOWED_GENERAL_STATUSES = {
    "draft", "active", "needs_review", "stale", "superseded", "deprecated"
}

REQUIRED_HEADINGS_BY_TYPE = {
    "project-overview": [
        "Project Goal",
        "Problem Statement",
        "Target Users or Actors",
        "Success Criteria",
        "Current Scope",
        "Non-Goals",
        "Evidence",
    ],
    "observability-and-instrumentation": [
        "Logs",
        "Metrics",
        "Traces",
        "Product Analytics Events",
        "Audit Events",
        "Dashboards and Alerts",
        "Privacy and Retention",
        "Known Blind Spots",
    ],
    "feature-registry": [
        "Next Work Queue",
        "Feature List",
    ],
    "user-stories-and-use-cases": [
        "Actors",
        "Personas or User Segments",
        "User Stories",
        "Journey Map",
        "Primary Use Cases",
        "Accessibility and Inclusion Notes",
        "Open Questions",
    ]
}

METADATA_LINE = re.compile(r"^\s*([A-Za-z ]+):\s*(.+?)\s*$", re.MULTILINE)
_links_cache = None


def iter_paths(base: Path):
    """Yield every dir entry and file under base, pruning IGNORED_DIR_NAMES."""
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = [d for d in dirnames if d not in IGNORED_DIR_NAMES]
        dp = Path(dirpath)
        for name in dirnames:
            yield dp / name
        for name in filenames:
            yield dp / name


def strip_fenced_code(text: str) -> str:
    lines = text.splitlines(keepends=True)
    stripped: list[str] = []
    in_fence = False
    fence_char = ""
    fence_len = 0

    for line in lines:
        match = FENCE_LINE.match(line)
        if not in_fence:
            if match:
                fence = match.group(2)
                fence_char = fence[0]
                fence_len = len(fence)
                in_fence = True
                continue
            stripped.append(line)
            continue

        if match:
            fence = match.group(2)
            if fence[0] == fence_char and len(fence) >= fence_len:
                in_fence = False
                fence_char = ""
                fence_len = 0

    return "".join(stripped)


def is_external_link(target: str) -> bool:
    return target.startswith(("http://", "https://", "mailto:", "#", "file://"))


def is_raw_intake_path(root: Path, path: Path) -> bool:
    try:
        rel = path.relative_to(root)
    except ValueError:
        return False
    return any(rel == intake or intake in rel.parents for intake in RAW_INTAKE_DIRS)


def slugify(text: str) -> str:
    text = re.sub(r"<[^>]*>", "", text)
    text = text.lower().strip()
    text = re.sub(r"\s+", "-", text)
    text = "".join(c for c in text if c.isalnum() or c in "-_")
    return text


def extract_anchors(path: Path) -> set[str]:
    anchors = set()
    if not path.exists():
        return anchors
    try:
        text = path.read_text(encoding="utf-8")
        text_without_code = strip_fenced_code(text)
        for line in text_without_code.splitlines():
            m = re.match(r"^\s{0,3}#{1,6}\s+(.+?)\s*$", line)
            if m:
                heading_text = m.group(1).strip()
                heading_text = heading_text.rstrip("#").strip()
                anchors.add(slugify(heading_text))
            for m_anchor in re.finditer(r'<(?:a\s+name|[^>]+id)\s*=\s*["\']([^"\']+)["\']', line):
                anchors.add(m_anchor.group(1).strip())
    except Exception:
        pass
    return anchors


def check_links_and_orphans(root: Path) -> tuple[list[str], list[str]]:
    global _links_cache
    if _links_cache is not None:
        return _links_cache

    errors: list[str] = []
    warnings: list[str] = []
    all_md_files = set()
    linked_files = set()
    docs_dir = root / "docs"

    if docs_dir.exists():
        for path in iter_paths(docs_dir):
            if path.is_file() and path.suffix == ".md":
                if not is_raw_intake_path(root, path):
                    all_md_files.add(path.resolve())

    for path in iter_paths(root):
        if not path.is_file() or path.suffix != ".md":
            continue
        if is_raw_intake_path(root, path):
            continue
        text = strip_fenced_code(path.read_text(encoding="utf-8"))
        for target in LINK.findall(text):
            if is_external_link(target) and not target.startswith("#"):
                continue
            
            if target.startswith("#"):
                anchor = target[1:]
                target_path = path.resolve()
            else:
                parts = target.split("#", 1)
                rel = parts[0]
                anchor = parts[1] if len(parts) > 1 else None
                target_path = (path.parent / rel).resolve()

            if not target.startswith("#") and not target_path.exists():
                errors.append(f"{path.relative_to(root)}: broken link -> {target}")
            else:
                if target_path.is_file():
                    linked_files.add(target_path)
                    if anchor:
                        valid_anchors = extract_anchors(target_path)
                        if anchor.lower() not in {a.lower() for a in valid_anchors}:
                            errors.append(f"{path.relative_to(root)}: broken anchor link -> {target} (anchor '{anchor}' not found in target file)")
                elif target_path.is_dir():
                    for index_name in ["README.md", "index.md"]:
                        index_path = target_path / index_name
                        if index_path.exists():
                            linked_files.add(index_path.resolve())

    for filepath in all_md_files:
        if filepath.name == "README.md" or filepath.name.startswith("_"):
            continue
        if filepath == (docs_dir / "README.md").resolve():
            continue
        if filepath not in linked_files:
            warnings.append(
                f"docs/{filepath.relative_to(docs_dir)}: orphaned document "
                "(no other Markdown document links to it)"
            )

    _links_cache = (errors, warnings)
    return _links_cache


def check_relative_links(root: Path) -> list[str]:
    errors, warnings = check_links_and_orphans(root)
    return errors


def resolve_ownership_paths(root: Path) -> dict[str, str]:
    docs_readme = root / "docs" / "README.md"
    resolved = {}
    if not docs_readme.exists():
        return resolved

    try:
        text = strip_fenced_code(docs_readme.read_text(encoding="utf-8"))
        section = find_section(text, CANONICAL_OWNER_HEADING)
        if not section:
            return resolved

        rows = [
            split_table_row(line)
            for line in section.splitlines()
            if line.strip().startswith("|") and line.strip().endswith("|")
        ]
        data_rows = [
            row for row in rows
            if row and not all(set(cell) <= {"-", ":", " "} for cell in row)
            and row[0].lower() != "capability"
        ]

        for row in data_rows:
            if len(row) < 2:
                continue
            capability = row[0].strip().lower()
            owner = row[1].strip().strip("`").strip()
            if not owner or owner.lower() in {"todo", "unknown", "tbd"}:
                continue

            matched_default = None
            for key, default_path in CAPABILITY_DEFAULTS.items():
                if key in capability:
                    matched_default = default_path
                    break

            if matched_default:
                owner_path = Path(owner)
                if owner_path.is_absolute():
                    resolved[matched_default] = str(owner_path.relative_to(root))
                else:
                    docs_owner = Path("docs") / owner_path
                    if (root / docs_owner).exists() or owner.startswith("docs/"):
                        resolved[matched_default] = str(docs_owner.as_posix())
                    else:
                        resolved[matched_default] = str(owner_path.as_posix())
    except Exception:
        pass
    return resolved


def validate_metadata_for_docs(root: Path) -> list[str]:
    docs_dir = root / "docs"
    if not docs_dir.exists():
        return []

    errors: list[str] = []
    for path in iter_paths(docs_dir):
        if not path.is_file() or path.suffix != ".md":
            continue
        if is_raw_intake_path(root, path):
            continue
        if path.name == "README.md" or path.name.startswith("_"):
            continue
        try:
            rel_to_docs = path.relative_to(docs_dir)
            if rel_to_docs.parts and rel_to_docs.parts[0] == "diagrams":
                continue
        except Exception:
            pass

        rel = path.relative_to(root)
        try:
            text = path.read_text(encoding="utf-8")
        except Exception as e:
            errors.append(f"{rel}: failed to read file: {e}")
            continue

        lines = text.splitlines()[:30]
        meta = {}
        for line in lines:
            if line.strip().startswith("##"):
                break
            m = METADATA_LINE.match(line)
            if m:
                key = m.group(1).strip().lower()
                val = m.group(2).strip().strip("`").strip()
                meta[key] = val

        required_fields = ["doc type", "owner", "status", "last updated"]
        missing = [f for f in required_fields if f not in meta]
        if missing:
            errors.append(f"{rel}: missing required metadata: {', '.join(missing)}")
            continue

        doc_type = meta["doc type"].lower()
        if doc_type not in ALLOWED_DOC_TYPES:
            errors.append(f"{rel}: invalid Doc type '{doc_type}'")

        status = meta["status"].lower()
        if doc_type in {"feature", "feature-logic", "feature-component"}:
            if status not in ALLOWED_FEATURE_STATUSES:
                errors.append(f"{rel}: invalid feature status '{status}'")
        else:
            if status not in ALLOWED_GENERAL_STATUSES:
                errors.append(f"{rel}: invalid status '{status}'")

        date_fields = ["last updated", "last verified"]
        for df in date_fields:
            if df in meta:
                val = meta[df]
                if val.lower() != "unknown" and not re.match(r"^\d{4}-\d{2}-\d{2}$", val):
                    errors.append(f"{rel}: invalid date format for '{df}': '{val}' (expected YYYY-MM-DD or 'unknown')")

        if doc_type in REQUIRED_HEADINGS_BY_TYPE:
            required_headings = REQUIRED_HEADINGS_BY_TYPE[doc_type]
            found_headings = set(HEADING.findall(text))
            for heading in required_headings:
                if heading not in found_headings:
                    errors.append(f"{rel}: missing required heading '{heading}'")

    return errors


def check_feature_cross_reference(root: Path) -> list[str]:
    registry_path = root / "docs" / "feature-registry.md"
    features_dir = root / "docs" / "features"
    if not registry_path.exists() or not features_dir.exists():
        return []

    warnings: list[str] = []
    registered_slugs = set()
    registered_statuses = {}
    
    try:
        text = strip_fenced_code(registry_path.read_text(encoding="utf-8"))
        headings = list(SECTION.finditer(text))
        list_start = None
        list_end = len(text)
        for index, heading in enumerate(headings):
            if heading.group(1).strip() == "Feature List":
                list_start = heading.end()
                if index + 1 < len(headings):
                    list_end = headings[index + 1].start()
                break

        if list_start is not None:
            rows = [
                split_table_row(line)
                for line in text[list_start:list_end].splitlines()
                if line.strip().startswith("|") and line.strip().endswith("|")
            ]
            data_rows = [
                row for row in rows
                if row and not all(set(cell) <= {"-", ":", " "} for cell in row)
                and row[0].lower() != "feature"
            ]
            
            header_row = None
            for line in text[list_start:list_end].splitlines():
                if line.strip().startswith("|") and line.strip().endswith("|"):
                    header_row = split_table_row(line)
                    if header_row and header_row[0].lower() == "feature":
                        break
            
            slug_idx = 1
            status_idx = 2
            if header_row:
                for i, h in enumerate(header_row):
                    if h.lower() == "slug":
                        slug_idx = i
                    elif h.lower() == "canonical doc":
                        slug_idx = i
                    elif h.lower() == "status":
                        status_idx = i
            
            for row in data_rows:
                if len(row) > max(slug_idx, status_idx):
                    cell_val = row[slug_idx].strip().strip("`").strip()
                    m_slug = re.search(r"features/([^.]+?)(?:\.md)?$", cell_val)
                    slug = None
                    if m_slug:
                        slug = m_slug.group(1)
                    elif cell_val and "/" not in cell_val and "." not in cell_val:
                        slug = cell_val
                    
                    if slug:
                        registered_slugs.add(slug)
                        registered_statuses[slug] = row[status_idx].strip().lower().strip("`").strip()
    except Exception:
        pass

    actual_slugs = set()
    for f in features_dir.glob("*.md"):
        if f.name != "_template.md":
            actual_slugs.add(f.stem)

    for slug in actual_slugs:
        if slug not in registered_slugs:
            warnings.append(
                f"docs/features/{slug}.md: feature file exists but is not "
                "registered in docs/feature-registry.md Feature List"
            )
        else:
            feature_doc = features_dir / f"{slug}.md"
            try:
                doc_text = feature_doc.read_text(encoding="utf-8")
                status_match = STATUS.search(doc_text)
                if status_match:
                    doc_status = status_match.group(1).lower()
                    reg_status = registered_statuses.get(slug)
                    if reg_status and doc_status != reg_status:
                        warnings.append(
                            f"docs/features/{slug}.md: status '{doc_status}' does "
                            f"not match status '{reg_status}' in feature registry"
                        )
            except Exception:
                pass
            
    for slug in registered_slugs:
        if slug == "feature-slug":
            continue
        if slug not in actual_slugs:
            warnings.append(
                f"docs/feature-registry.md: registered feature '{slug}' "
                f"has no corresponding file docs/features/{slug}.md"
            )

    return warnings


def check_required(root: Path, paths: list[str]) -> list[str]:
    return [
        f"missing required file: {path}"
        for path in paths
        if not (root / path).exists()
    ]


def check_docs_kebab_case(root: Path) -> list[str]:
    docs = root / "docs"
    if not docs.exists():
        return []

    errors: list[str] = []
    for path in iter_paths(docs):
        if not path.is_file():
            continue
        if is_raw_intake_path(root, path):
            continue
        rel = path.relative_to(docs)
        for part in rel.parts:
            if part == "README.md" or part == "_template.md":
                continue
            if not KEBAB_PATH.match(part):
                errors.append(f"docs path is not kebab-case: docs/{rel}")
                break
    return errors


def check_required_headings(root: Path) -> list[str]:
    errors: list[str] = []
    heading_sets = dict(REQUIRED_HEADINGS)
    for path, headings in OPTIONAL_REQUIRED_HEADINGS.items():
        if (root / path).exists():
            heading_sets[path] = headings

    for path, required in heading_sets.items():
        doc = root / path
        if not doc.exists():
            continue
        found = set(HEADING.findall(doc.read_text(encoding="utf-8")))
        for heading in required:
            if heading not in found:
                errors.append(f"{path}: missing required heading '{heading}'")
    return errors


def find_section(text: str, heading: str) -> str | None:
    headings = list(SECTION.finditer(text))
    for index, match in enumerate(headings):
        if match.group(1).strip() == heading:
            start = match.end()
            end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
            return text[start:end]
    return None


def check_canonical_ownership_map(root: Path) -> list[str]:
    docs_readme = root / "docs" / "README.md"
    if not docs_readme.exists():
        return []

    text = strip_fenced_code(docs_readme.read_text(encoding="utf-8"))
    section = find_section(text, CANONICAL_OWNER_HEADING)
    if section is None:
        return [
            "docs/README.md: missing 'Canonical Ownership Map' section for "
            "no-duplicate ownership"
        ]

    rows = [
        split_table_row(line)
        for line in section.splitlines()
        if line.strip().startswith("|") and line.strip().endswith("|")
    ]
    data_rows = [
        row for row in rows
        if row and not all(set(cell) <= {"-", ":", " "} for cell in row)
        and row[0].lower() != "capability"
    ]
    if not data_rows:
        return [
            "docs/README.md: Canonical Ownership Map has no capability rows"
        ]

    warnings: list[str] = []
    seen: dict[str, str] = {}
    for row in data_rows:
        if len(row) < 2:
            warnings.append(
                "docs/README.md: Canonical Ownership Map row has fewer than "
                "2 columns"
            )
            continue
        capability = row[0].strip().lower()
        owner = row[1].strip()
        if not capability:
            warnings.append(
                "docs/README.md: Canonical Ownership Map row has an empty "
                "Capability cell"
            )
            continue
        if not owner or owner.lower() in {"todo", "unknown", "tbd"}:
            warnings.append(
                "docs/README.md: Canonical Ownership Map capability "
                f"'{row[0]}' is missing a canonical owner"
            )
        if capability in seen:
            warnings.append(
                "docs/README.md: Canonical Ownership Map duplicates "
                f"capability '{row[0]}'"
            )
        seen[capability] = owner
        if re.search(r"\s+(and|or)\s+|[,;]", owner, re.IGNORECASE):
            warnings.append(
                "docs/README.md: Canonical Ownership Map capability "
                f"'{row[0]}' appears to name multiple canonical owners; "
                "put alternates in Supporting docs instead"
            )
    return warnings


def check_empty_optional_deep_dive_dirs(root: Path) -> list[str]:
    warnings: list[str] = []
    for rel_dir in OPTIONAL_DEEP_DIVE_DIRS:
        directory = root / rel_dir
        if not directory.is_dir():
            continue

        files = [
            path
            for path in iter_paths(directory)
            if path.is_file()
        ]
        meaningful = [
            path
            for path in files
            if path.name != "README.md" and not path.name.startswith(".")
        ]
        if files and not meaningful:
            warnings.append(
                f"{rel_dir}: optional deep-dive folder has only an index "
                "and no owned topic docs"
            )
    return warnings


def check_generated_artifacts(root: Path) -> list[str]:
    warnings: list[str] = []
    for path in iter_paths(root):
        if path.name in GENERATED_ARTIFACT_NAMES:
            warnings.append(
                f"{path.relative_to(root)}: generated or harness artifact "
                "should not be left in the repo"
            )
    return warnings


def check_feature_statuses(root: Path) -> list[str]:
    features = root / "docs" / "features"
    if not features.exists():
        return []

    warnings: list[str] = []
    for doc in features.glob("*.md"):
        if doc.name == "_template.md":
            continue

        text = doc.read_text(encoding="utf-8")
        status_match = STATUS.search(text)
        rel = doc.relative_to(root)
        if not status_match:
            warnings.append(f"{rel}: feature doc is missing a Status metadata field")
            continue

        status = status_match.group(1).lower()
        if status not in ALLOWED_FEATURE_STATUSES:
            allowed = ", ".join(sorted(ALLOWED_FEATURE_STATUSES))
            warnings.append(
                f"{rel}: unknown feature status '{status}' "
                f"(allowed: {allowed})"
            )
            continue

        completed_signals = sum(
            1 for pattern in COMPLETED_FEATURE_EVIDENCE_PATTERNS if pattern.search(text)
        )
        if status in ACTIVE_FEATURE_STATUSES and completed_signals >= 2:
            warnings.append(
                f"{rel}: feature appears completed or verified but status is "
                f"'{status}' instead of implemented, verified, or shipped"
            )
    return warnings


def check_terminal_feature_handoff(root: Path) -> list[str]:
    features = root / "docs" / "features"
    if not features.exists():
        return []

    warnings: list[str] = []
    for doc in features.glob("*.md"):
        if doc.name == "_template.md":
            continue
        text = doc.read_text(encoding="utf-8")
        status_match = STATUS.search(text)
        if not status_match:
            continue
        status = status_match.group(1).lower()
        if status not in TERMINAL_FEATURE_STATUSES:
            continue
        for pattern in STALE_TERMINAL_HANDOFF_PATTERNS:
            if pattern.search(text):
                warnings.append(
                    f"{doc.relative_to(root)}: terminal feature status "
                    f"'{status}' still contains interrupted-work handoff wording"
                )
                break
    return warnings


def split_table_row(line: str) -> list[str]:
    return [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]


def check_next_work_queue(root: Path) -> list[str]:
    registry = root / "docs" / "feature-registry.md"
    if not registry.exists():
        return []

    text = strip_fenced_code(registry.read_text(encoding="utf-8"))
    headings = list(SECTION.finditer(text))
    queue_start = None
    queue_end = len(text)
    for index, heading in enumerate(headings):
        if heading.group(1).strip() == "Next Work Queue":
            queue_start = heading.end()
            if index + 1 < len(headings):
                queue_end = headings[index + 1].start()
            break
    if queue_start is None:
        return []

    warnings: list[str] = []
    rows = [
        split_table_row(line)
        for line in text[queue_start:queue_end].splitlines()
        if line.strip().startswith("|") and line.strip().endswith("|")
    ]
    data_rows = [
        row for row in rows
        if row and not all(set(cell) <= {"-", ":", " "} for cell in row)
        and row[0].lower() != "rank"
    ]

    for row in data_rows:
        if len(row) < 9:
            warnings.append(
                "docs/feature-registry.md: Next Work Queue row has fewer "
                "than 9 columns"
            )
            continue
        ready = row[4].lower()
        if ready not in ALLOWED_QUEUE_READY:
            allowed = ", ".join(sorted(ALLOWED_QUEUE_READY))
            warnings.append(
                "docs/feature-registry.md: Next Work Queue row has invalid "
                f"Ready value '{row[4]}' (allowed: {allowed})"
            )
        if ready in {"ready", "verify-first"}:
            missing = []
            if not row[5] or row[5].lower() == "todo":
                missing.append("Why next")
            if not row[6] or row[6].lower() == "todo":
                missing.append("Next safe step")
            if not row[7] or row[7].lower() == "todo":
                missing.append("Canonical doc")
            if missing:
                warnings.append(
                    "docs/feature-registry.md: Next Work Queue "
                    f"'{row[1] or 'unnamed'}' is {ready} but missing "
                    + ", ".join(missing)
                )
    return warnings


def check_skill_version(root: Path) -> list[str]:
    package_root = root / SKILL_PACKAGE if (root / SKILL_PACKAGE).exists() else root
    skill = package_root / "SKILL.md"
    standard = package_root / "STANDARD.md"
    changelog = root / "CHANGELOG.md"
    if not skill.exists() or not changelog.exists():
        return []

    skill_text = skill.read_text(encoding="utf-8")
    skill_match = VERSION.search(skill_text)
    if not skill_match:
        return [f"{skill.relative_to(root)} missing Version: X.Y line"]

    version = skill_match.group(1)
    if standard.exists():
        standard_text = standard.read_text(encoding="utf-8")
        standard_match = VERSION.search(standard_text)
        if not standard_match:
            return [f"{standard.relative_to(root)} missing Version: X.Y line"]
        standard_version = standard_match.group(1)
        if standard_version != version:
            return [
                f"{standard.relative_to(root)} version "
                f"{standard_version} does not match "
                f"{skill.relative_to(root)} version {version}"
            ]

    changelog_text = changelog.read_text(encoding="utf-8")
    if not re.search(rf"^##\s*(?:\[{re.escape(version)}\]|{re.escape(version)}\b)", changelog_text, re.MULTILINE):
        return [f"CHANGELOG.md missing entry for SKILL.md version {version}"]

    return []


def check_skill_repo(root: Path) -> list[str]:
    errors: list[str] = []
    errors.extend(check_required(root, REQUIRED_REPO_FILES))
    errors.extend(check_required(root, REQUIRED_SKILL_PACKAGE_FILES))
    errors.extend(check_skill_version(root))
    return errors


def check_project_docs(root: Path, adoption_level: str = "baseline") -> list[str]:
    errors: list[str] = []
    if not (root / "docs").exists():
        errors.append("missing docs/ directory")
        return errors

    resolved_paths = resolve_ownership_paths(root)
    required = (
        CONTINUITY_PROJECT_DOCS
        if adoption_level == "continuity"
        else BASELINE_PROJECT_DOCS
    )

    modified_required = []
    for req in required:
        if req in resolved_paths:
            modified_required.append(resolved_paths[req])
        else:
            modified_required.append(req)

    errors.extend(check_required(root, modified_required))
    errors.extend(check_docs_kebab_case(root))
    if adoption_level == "baseline":
        errors.extend(check_required_headings(root))
        errors.extend(validate_metadata_for_docs(root))
    return errors


def check_plan_placement_drift(root: Path) -> list[str]:
    warnings: list[str] = []
    
    for d in ["plan", "plans", "spec", "specs", "superpowers"]:
        if (root / d).is_dir():
            warnings.append(
                f"{d}/: prohibited plan/spec directory at repo root. "
                "Move companion artifacts to docs/superpowers/plans/ or docs/superpowers/specs/"
            )
            
    for d in ["plan", "plans", "spec", "specs"]:
        if (root / "docs" / d).is_dir():
            warnings.append(
                f"docs/{d}/: prohibited plan/spec directory. "
                "Move companion artifacts to docs/superpowers/plans/ or docs/superpowers/specs/"
            )
            
    for f in ["plan.md", "plans.md", "spec.md", "specs.md"]:
        if (root / f).is_file():
            warnings.append(
                f"{f}: prohibited plan/spec file at repo root. "
                "Move to docs/superpowers/plans/ or docs/superpowers/specs/"
            )
        if (root / "docs" / f).is_file():
            warnings.append(
                f"docs/{f}: prohibited plan/spec file. "
                "Move to docs/superpowers/plans/ or docs/superpowers/specs/"
            )
            
    superpowers_dir = root / "docs" / "superpowers"
    if superpowers_dir.is_dir():
        for p in superpowers_dir.iterdir():
            if p.is_file() and p.name != "README.md" and not p.name.startswith("."):
                warnings.append(
                    f"docs/superpowers/{p.name}: plan/spec file directly in superpowers folder. "
                    "Move to docs/superpowers/plans/ or docs/superpowers/specs/"
                )
                
    return warnings


def check_project_warnings(root: Path) -> list[str]:
    warnings: list[str] = []
    warnings.extend(check_empty_optional_deep_dive_dirs(root))
    warnings.extend(check_generated_artifacts(root))
    warnings.extend(check_feature_statuses(root))
    warnings.extend(check_terminal_feature_handoff(root))
    warnings.extend(check_next_work_queue(root))
    warnings.extend(check_canonical_ownership_map(root))
    warnings.extend(check_plan_placement_drift(root))
    
    # Add link warnings (orphans) and feature registry cross-references
    errors, link_warnings = check_links_and_orphans(root)
    warnings.extend(link_warnings)
    warnings.extend(check_feature_cross_reference(root))
    
    return warnings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument(
        "--skill-repo",
        action="store_true",
        help="validate this repository as the Repo Memory standard repo",
    )
    parser.add_argument(
        "--project-docs",
        action="store_true",
        help="validate a target repository that adopted the docs standard",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="treat warnings as validation failures",
    )
    parser.add_argument(
        "--adoption-level",
        choices=["continuity", "baseline"],
        default="baseline",
        help=(
            "project-doc validation depth: continuity checks the minimal "
            "handoff overlay, baseline checks the full default capability set"
        ),
    )
    args = parser.parse_args()

    root = Path(args.path).resolve()
    errors: list[str] = []
    warnings: list[str] = []

    if args.skill_repo:
        errors.extend(check_skill_repo(root))
    if args.project_docs:
        errors.extend(check_project_docs(root, args.adoption_level))
        warnings.extend(check_project_warnings(root))
    if not args.skill_repo and not args.project_docs:
        if (root / SKILL_PACKAGE / "SKILL.md").exists():
            errors.extend(check_skill_repo(root))
        elif (root / "SKILL.md").exists() and (root / "references").exists():
            errors.extend(check_skill_version(root))
        else:
            errors.extend(check_project_docs(root, args.adoption_level))
            warnings.extend(check_project_warnings(root))

    errors.extend(check_relative_links(root))

    if errors or (args.strict and warnings):
        for error in errors:
            print(f"ERROR: {error}")
        for warning in warnings:
            print(f"WARNING: {warning}")
        return 1

    for warning in warnings:
        print(f"WARNING: {warning}")
    if warnings:
        print("Documentation validation passed with warnings")
        return 0

    print("Documentation validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
