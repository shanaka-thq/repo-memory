#!/usr/bin/env python3
"""Validate Repo Memory structure and adopted project docs."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_SKILL_FILES = [
    "README.md",
    "STANDARD.md",
    "AGENTS.md",
    "CHANGELOG.md",
    "SKILL.md",
    "SECURITY.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SUPPORT.md",
    "ROADMAP.md",
    ".gitignore",
    "references/templates.md",
    "references/docs-structure-rules.md",
    "references/existing-project-audit.md",
    "references/decision-log-reconstruction.md",
    "references/continuity-governance.md",
    "references/documentation-metadata-schema.md",
    "agents/openai-codex.md",
    "agents/github-copilot.md",
    "agents/claude-code.md",
    "agents/openai.yaml",
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

KEBAB_PATH = re.compile(r"^[a-z0-9][a-z0-9-]*(\.[a-z0-9]+)?$")
LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
FENCE_LINE = re.compile(r"^( {0,3})([`~]{3,})(.*)$")
VERSION = re.compile(r"^Version:\s*(\d+\.\d+)", re.MULTILINE)
HEADING = re.compile(r"^#{2,6}\s+(.+?)\s*$", re.MULTILINE)


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


def check_relative_links(root: Path) -> list[str]:
    errors: list[str] = []
    for md in root.rglob("*.md"):
        if ".git" in md.parts:
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


def check_skill_version(root: Path) -> list[str]:
    skill = root / "SKILL.md"
    standard = root / "STANDARD.md"
    changelog = root / "CHANGELOG.md"
    if not skill.exists() or not changelog.exists():
        return []

    skill_text = skill.read_text(encoding="utf-8")
    skill_match = VERSION.search(skill_text)
    if not skill_match:
        return ["SKILL.md missing Version: X.Y line"]

    version = skill_match.group(1)
    if standard.exists():
        standard_text = standard.read_text(encoding="utf-8")
        standard_match = VERSION.search(standard_text)
        if not standard_match:
            return ["STANDARD.md missing Version: X.Y line"]
        standard_version = standard_match.group(1)
        if standard_version != version:
            return [
                "STANDARD.md version "
                f"{standard_version} does not match SKILL.md version {version}"
            ]

    changelog_text = changelog.read_text(encoding="utf-8")
    if not re.search(rf"^## \[{re.escape(version)}\]", changelog_text, re.MULTILINE):
        return [f"CHANGELOG.md missing entry for SKILL.md version {version}"]

    return []


def check_skill_repo(root: Path) -> list[str]:
    errors: list[str] = []
    errors.extend(check_required(root, REQUIRED_SKILL_FILES))
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
    args = parser.parse_args()

    root = Path(args.path).resolve()
    errors: list[str] = []

    if args.skill_repo:
        errors.extend(check_skill_repo(root))
    if args.project_docs:
        errors.extend(check_project_docs(root))
    if not args.skill_repo and not args.project_docs:
        if (root / "SKILL.md").exists() and (root / "references").exists():
            errors.extend(check_skill_repo(root))
        else:
            errors.extend(check_project_docs(root))

    errors.extend(check_relative_links(root))

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("Documentation validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
