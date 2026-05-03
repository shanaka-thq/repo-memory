#!/usr/bin/env python3
"""Validate Repo Memory structure and adopted project docs."""

from __future__ import annotations

import argparse
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
    "skills/repo-memory/references/decision-log-reconstruction.md",
    "skills/repo-memory/references/continuity-governance.md",
    "skills/repo-memory/references/superpowers-compatibility.md",
    "skills/repo-memory/references/documentation-metadata-schema.md",
    "skills/repo-memory/agents/openai-codex.md",
    "skills/repo-memory/agents/github-copilot.md",
    "skills/repo-memory/agents/claude-code.md",
    "skills/repo-memory/agents/openai.yaml",
    "skills/repo-memory/examples/README.md",
    "skills/repo-memory/scripts/forward-test.py",
    "skills/repo-memory/scripts/scaffold-docs.py",
    "skills/repo-memory/scripts/validate-docs.py",
]

REQUIRED_PROJECT_DOCS = [
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

KEBAB_PATH = re.compile(r"^[a-z0-9][a-z0-9-]*(\.[a-z0-9]+)?$")
LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
FENCE_LINE = re.compile(r"^( {0,3})([`~]{3,})(.*)$")
VERSION = re.compile(r"^Version:\s*(\d+\.\d+)", re.MULTILINE)
HEADING = re.compile(r"^\s{0,3}#{2,6}\s+(.+?)\s*$", re.MULTILINE)
STATUS = re.compile(r"^\s*Status:\s*([a-z_]+)\b", re.MULTILINE | re.IGNORECASE)
SECTION = re.compile(r"^\s{0,3}##\s+(.+?)\s*$", re.MULTILINE)


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
    return target.startswith(("http://", "https://", "mailto:", "#"))


def is_raw_intake_path(root: Path, path: Path) -> bool:
    try:
        rel = path.relative_to(root)
    except ValueError:
        return False
    return any(rel == intake or intake in rel.parents for intake in RAW_INTAKE_DIRS)


def check_relative_links(root: Path) -> list[str]:
    errors: list[str] = []
    for md in root.rglob("*.md"):
        if ".git" in md.parts:
            continue
        if is_raw_intake_path(root, md):
            continue
        text = strip_fenced_code(md.read_text(encoding="utf-8"))
        for target in LINK.findall(text):
            if is_external_link(target):
                continue
            rel = target.split("#", 1)[0]
            if not rel:
                continue
            if not (md.parent / rel).resolve().exists():
                errors.append(f"{md.relative_to(root)}: broken link -> {target}")
    return errors


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
    for path in docs.rglob("*"):
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


def check_empty_optional_deep_dive_dirs(root: Path) -> list[str]:
    warnings: list[str] = []
    for rel_dir in OPTIONAL_DEEP_DIVE_DIRS:
        directory = root / rel_dir
        if not directory.is_dir():
            continue

        files = [
            path
            for path in directory.rglob("*")
            if path.is_file() and ".git" not in path.parts
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
    for path in root.rglob("*"):
        if ".git" in path.parts:
            continue
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
    if not re.search(rf"^## \[{re.escape(version)}\]", changelog_text, re.MULTILINE):
        return [f"CHANGELOG.md missing entry for SKILL.md version {version}"]

    return []


def check_skill_repo(root: Path) -> list[str]:
    errors: list[str] = []
    errors.extend(check_required(root, REQUIRED_REPO_FILES))
    errors.extend(check_required(root, REQUIRED_SKILL_PACKAGE_FILES))
    errors.extend(check_skill_version(root))
    return errors


def check_project_docs(root: Path) -> list[str]:
    errors: list[str] = []
    if not (root / "docs").exists():
        errors.append("missing docs/ directory")
        return errors
    errors.extend(check_required(root, REQUIRED_PROJECT_DOCS))
    errors.extend(check_docs_kebab_case(root))
    errors.extend(check_required_headings(root))
    return errors


def check_project_warnings(root: Path) -> list[str]:
    warnings: list[str] = []
    warnings.extend(check_empty_optional_deep_dive_dirs(root))
    warnings.extend(check_generated_artifacts(root))
    warnings.extend(check_feature_statuses(root))
    warnings.extend(check_terminal_feature_handoff(root))
    warnings.extend(check_next_work_queue(root))
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
    args = parser.parse_args()

    root = Path(args.path).resolve()
    errors: list[str] = []
    warnings: list[str] = []

    if args.skill_repo:
        errors.extend(check_skill_repo(root))
    if args.project_docs:
        errors.extend(check_project_docs(root))
        warnings.extend(check_project_warnings(root))
    if not args.skill_repo and not args.project_docs:
        if (root / SKILL_PACKAGE / "SKILL.md").exists():
            errors.extend(check_skill_repo(root))
        elif (root / "SKILL.md").exists() and (root / "references").exists():
            errors.extend(check_skill_version(root))
        else:
            errors.extend(check_project_docs(root))
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
