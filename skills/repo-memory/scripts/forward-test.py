#!/usr/bin/env python3
"""Run blind forward-test scenarios for the Repo Memory skill.

This helper creates disposable repositories, optionally runs a child Codex
agent against them, then scores the resulting artifacts. It is intentionally
manual: live agent runs depend on local Codex auth and spend model tokens.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import textwrap
from dataclasses import dataclass
from pathlib import Path


TEST_DATE = "2026-04-29"
SCENARIOS = [
    "interrupted-worktree",
    "custom-docs-preservation",
    "feature-continuation",
    "stale-docs-conflict",
]
OPTIONAL_DEEP_DIVE_DIRS = [
    "docs/diagrams",
    "docs/designs",
    "docs/project-details",
    "docs/components",
    "docs/reviews",
    "docs/ui-ux",
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


def iter_paths(base: Path):
    """Yield every dir entry and file under base, pruning IGNORED_DIR_NAMES."""
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = [d for d in dirnames if d not in IGNORED_DIR_NAMES]
        dp = Path(dirpath)
        for name in dirnames:
            yield dp / name
        for name in filenames:
            yield dp / name


TERMINAL_FEATURE_STATUSES = {
    "implemented",
    "verified",
    "shipped",
}


@dataclass(frozen=True)
class Check:
    name: str
    passed: bool
    detail: str


@dataclass(frozen=True)
class Scenario:
    name: str
    prompt: str


def run(
    command: list[str],
    *,
    cwd: Path,
    check: bool = True,
    timeout: int | None = None,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
    )
    if check and result.returncode != 0:
        raise RuntimeError(
            f"command failed ({result.returncode}): {' '.join(command)}\n"
            f"{result.stdout}"
        )
    return result


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")


def commit_all(repo: Path, message: str) -> None:
    run(["git", "add", "."], cwd=repo)
    run(["git", "commit", "-m", message], cwd=repo)


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def scaffold(repo: Path, project_name: str) -> None:
    script = skill_root() / "scripts" / "scaffold-docs.py"
    run(
        [
            sys.executable,
            str(script),
            str(repo),
            "--with-agents",
            "--project-name",
            project_name,
            "--date",
            TEST_DATE,
        ],
        cwd=repo,
    )


def init_repo(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    run(["git", "init"], cwd=path)
    run(
        ["git", "config", "user.email", "repo-memory-forward-test@example.invalid"],
        cwd=path,
    )
    run(["git", "config", "user.name", "Repo Memory Forward Test"], cwd=path)


def build_interrupted_worktree(repo: Path) -> None:
    init_repo(repo)
    scaffold(repo, "Expense Splitter")
    write(
        repo / "README.md",
        """
        # Expense Splitter

        Split shared expenses from the command line.
        """,
    )
    write(
        repo / "src/splitter.py",
        """
        #!/usr/bin/env python3
        import argparse


        def split_evenly(amount, people):
            if not people:
                raise ValueError("at least one person is required")
            share = round(amount / len(people), 2)
            return {person: share for person in people}


        def main():
            parser = argparse.ArgumentParser()
            parser.add_argument("amount", type=float)
            parser.add_argument("people", nargs="+")
            args = parser.parse_args()

            for person, share in split_evenly(args.amount, args.people).items():
                print(f"{person}: {share:.2f}")


        if __name__ == "__main__":
            main()
        """,
    )
    write_feature_doc(
        repo,
        "rounding-policy",
        status="in_progress",
        validation_status="interrupted",
        next_step=(
            "inspect the working tree before editing; partial rounding "
            "changes may already exist."
        ),
        goal="Ensure split shares add back to the original amount after cent rounding.",
    )
    write(
        repo / "docs/feature-registry.md",
        """
        # Feature Registry

        Doc type: feature-registry
        Owner: current-agent-or-team
        Status: active
        Last updated: 2026-04-29
        Last verified: 2026-04-29
        Verified against: docs tree
        Confidence: medium
        Canonical source: `docs/feature-registry.md`
        Related docs: `features/rounding-policy.md`

        ## Next Work Queue

        | Rank | Work item | Type | Status | Ready | Why next | Next safe step | Canonical doc | Last verified |
        | --- | --- | --- | --- | --- | --- | --- | --- | --- |
        | 1 | Rounding policy | feature | `in_progress` | `ready` | Interrupted money-splitting bug has known expected behavior | Inspect the working tree before editing, then finish cent allocation | [`features/rounding-policy.md`](./features/rounding-policy.md) | 2026-04-29 |

        ## Feature List

        | Feature | Status | Owner | Canonical doc | Notes |
        | --- | --- | --- | --- | --- |
        | Rounding policy | in_progress | current-agent-or-team | `features/rounding-policy.md` | Interrupted work exists in the tree. |
        """,
    )
    commit_all(repo, "Initial interrupted worktree fixture")
    write(
        repo / "src/splitter.py",
        """
        #!/usr/bin/env python3
        import argparse


        def split_evenly(amount, people):
            if not people:
                raise ValueError("at least one person is required")
            cents = round(amount * 100)
            base_share = cents // len(people)
            remainder = cents % len(people)
            # TODO: finish allocating remainder cents to the earliest people.
            return {person: base_share / 100 for person in people}


        def main():
            parser = argparse.ArgumentParser()
            parser.add_argument("amount", type=float)
            parser.add_argument("people", nargs="+")
            args = parser.parse_args()

            for person, share in split_evenly(args.amount, args.people).items():
                print(f"{person}: {share:.2f}")


        if __name__ == "__main__":
            main()
        """,
    )
    write(
        repo / "NOTES.tmp",
        """
        Interrupted thought:
        - Remainder cents should be assigned to people in input order.
        - Example: 10 split across 3 should be 3.34, 3.33, 3.33.
        """,
    )


def build_custom_docs_preservation(repo: Path) -> None:
    init_repo(repo)
    write(repo / "README.md", "# Appointment API\n\nA small appointment module.")
    write(
        repo / "app/appointments.py",
        """
        from dataclasses import dataclass


        @dataclass
        class Appointment:
            patient_id: str
            starts_at: str
            clinician_id: str


        def create_appointment(payload):
            required = {"patient_id", "starts_at", "clinician_id"}
            missing = sorted(required - set(payload))
            if missing:
                return {"ok": False, "error": "missing_fields", "fields": missing}
            return {
                "ok": True,
                "appointment": Appointment(
                    patient_id=payload["patient_id"],
                    starts_at=payload["starts_at"],
                    clinician_id=payload["clinician_id"],
                ),
            }
        """,
    )
    write(
        repo / "docs/product/appointment-workflow.md",
        """
        # Appointment Workflow

        Patients request appointments with a clinician and start time.

        ## Confirmed Scope

        - Create appointment requests.
        - Validate required fields.
        """,
    )
    write(
        repo / "docs/adr/001-python-module.md",
        """
        # ADR 001: Keep Appointment Logic in a Python Module

        Status: accepted

        Use a small Python module while the contract is still changing.
        """,
    )
    write(
        repo / "AGENTS.md",
        """
        # Agent Notes

        Current docs live in `docs/product/` and `docs/adr/`.
        Preserve those docs; do not replace them with a new unrelated structure.
        """,
    )
    commit_all(repo, "Initial custom docs fixture")


def build_feature_continuation(repo: Path) -> None:
    init_repo(repo)
    scaffold(repo, "Task Notes")
    write(
        repo / "src/task_notes.py",
        """
        #!/usr/bin/env python3
        import argparse
        import json
        from pathlib import Path


        DATA_FILE = Path("notes.json")


        def load_notes(path=DATA_FILE):
            if not path.exists():
                return []
            return json.loads(path.read_text())


        def save_notes(notes, path=DATA_FILE):
            path.write_text(json.dumps(notes, indent=2) + "\\n")


        def add_note(text, path=DATA_FILE):
            notes = load_notes(path)
            next_id = max([note["id"] for note in notes], default=0) + 1
            notes.append({"id": next_id, "text": text, "done": False})
            save_notes(notes, path)
            return next_id


        def list_notes(show_done=False, path=DATA_FILE):
            notes = load_notes(path)
            return [note for note in notes if show_done or not note["done"]]


        def main():
            parser = argparse.ArgumentParser()
            subcommands = parser.add_subparsers(dest="command", required=True)
            add = subcommands.add_parser("add")
            add.add_argument("text")
            list_cmd = subcommands.add_parser("list")
            list_cmd.add_argument("--all", action="store_true")
            args = parser.parse_args()
            if args.command == "add":
                print(f"Added note {add_note(args.text)}")
            elif args.command == "list":
                for note in list_notes(show_done=args.all):
                    status = "done" if note["done"] else "open"
                    print(f"{note['id']}: [{status}] {note['text']}")


        if __name__ == "__main__":
            main()
        """,
    )
    write_feature_doc(
        repo,
        "add-due-dates",
        status="in_progress",
        validation_status="tests not updated yet",
        next_step=(
            "add optional due date support to the CLI, persistence shape, "
            "output, and tests."
        ),
        goal="Allow users to attach an optional due date to a note when adding it.",
    )
    write(
        repo / "docs/feature-registry.md",
        """
        # Feature Registry

        Doc type: feature-registry
        Owner: current-agent-or-team
        Status: active
        Last updated: 2026-04-29
        Last verified: 2026-04-29
        Verified against: docs tree
        Confidence: medium
        Canonical source: `docs/feature-registry.md`
        Related docs: `features/add-due-dates.md`

        ## Next Work Queue

        | Rank | Work item | Type | Status | Ready | Why next | Next safe step | Canonical doc | Last verified |
        | --- | --- | --- | --- | --- | --- | --- | --- | --- |
        | 1 | Add due dates | feature | `in_progress` | `ready` | Active user-visible feature with implementation scope already defined | Add optional due date support to CLI, persistence, output, tests, and docs | [`features/add-due-dates.md`](./features/add-due-dates.md) | 2026-04-29 |

        ## Feature List

        | Feature | Status | Owner | Canonical doc | Notes |
        | --- | --- | --- | --- | --- |
        | Add due dates | in_progress | current-agent-or-team | `features/add-due-dates.md` | Implement next. |
        """,
    )
    commit_all(repo, "Initial feature continuation fixture")


def build_stale_docs_conflict(repo: Path) -> None:
    init_repo(repo)
    write(
        repo / "README.md",
        """
        # Link Check

        A tiny CLI that checks URL shape for local smoke tests.
        """,
    )
    write(
        repo / "src/link_check.py",
        """
        #!/usr/bin/env python3
        import argparse
        from urllib.parse import urlparse


        def classify_url(url):
            parsed = urlparse(url)
            if parsed.scheme not in {"http", "https"}:
                return "invalid-scheme"
            if not parsed.netloc:
                return "missing-host"
            return "valid"


        def main():
            parser = argparse.ArgumentParser()
            parser.add_argument("urls", nargs="+")
            args = parser.parse_args()
            exit_code = 0
            for url in args.urls:
                status = classify_url(url)
                print(f"{url}: {status}")
                if status != "valid":
                    exit_code = 1
            raise SystemExit(exit_code)


        if __name__ == "__main__":
            main()
        """,
    )
    write(
        repo / "docs/architecture.md",
        """
        # Architecture

        Link Check is a hosted web crawler backed by PostgreSQL and workers.
        """,
    )
    write(
        repo / "docs/old-plan.md",
        """
        # Old Plan

        - Build a web crawler.
        - Add PostgreSQL.
        - This may no longer match current code.
        """,
    )
    commit_all(repo, "Initial stale docs conflict fixture")


def write_feature_doc(
    repo: Path,
    slug: str,
    *,
    status: str,
    validation_status: str,
    next_step: str,
    goal: str,
) -> None:
    title = slug.replace("-", " ").title()
    write(
        repo / f"docs/features/{slug}.md",
        f"""
        # Feature: {title}

        Doc type: feature
        Feature slug: {slug}
        Status: {status}
        Owner: current-agent-or-team
        Priority: high
        Last updated: 2026-04-29
        Last verified: 2026-04-29
        Verified against: source and docs
        Confidence: medium
        Canonical source: `docs/features/{slug}.md`
        Related docs: `../feature-registry.md`
        Validation status: {validation_status}
        Next safe step: {next_step}

        ## Goal

        {goal}

        ## Implementation Status

        - [ ] Preserve current context.
        - [ ] Finish scoped behavior.
        - [ ] Update docs and validation notes.

        ## Next Agent Handoff

        Continue from this feature doc and keep the registry current.
        """,
    )


BUILDERS = {
    "interrupted-worktree": build_interrupted_worktree,
    "custom-docs-preservation": build_custom_docs_preservation,
    "feature-continuation": build_feature_continuation,
    "stale-docs-conflict": build_stale_docs_conflict,
}


PROMPTS = {
    "interrupted-worktree": (
        "Use the Repo Memory skill at {skill_dir} to resume the active "
        "rounding-policy feature in this repository. Read the docs first, "
        "inspect the working tree before editing, preserve existing "
        "uncommitted work, finish the scoped rounding behavior if possible, "
        "update docs and handoff notes, run relevant validation, and report "
        "what changed."
    ),
    "custom-docs-preservation": (
        "Use the Repo Memory skill at {skill_dir} to standardize this "
        "repository documentation for future agents. Preserve the existing "
        "docs/product and docs/adr knowledge; do not replace useful custom "
        "docs. Add or update a canonical ownership map, add only the missing "
        "handoff surfaces needed for future agents, align AGENTS.md to the "
        "mapped owners, run "
        "relevant validation, and report what changed."
    ),
    "feature-continuation": (
        "Use the Repo Memory skill at {skill_dir} to pick up the next ready "
        "task from docs/feature-registry.md. Read the repo docs first, "
        "implement the scoped feature from the ranked queue, update tests and "
        "Repo Memory docs or handoff notes, run relevant validation, and report "
        "what changed."
    ),
    "stale-docs-conflict": (
        "Use the Repo Memory skill at {skill_dir} to audit this repository "
        "and make the docs reliable for future agents. Inspect the code and "
        "existing docs, fix stale or conflicting documentation in the single "
        "mapped owner, create only missing Repo Memory docs that are needed, "
        "run relevant validation, and report what changed."
    ),
}


def validator_command(
    repo: Path,
    *,
    strict: bool = False,
    adoption_level: str = "continuity",
) -> list[str]:
    script = skill_root() / "scripts" / "validate-docs.py"
    command = [
        sys.executable,
        str(script),
        "--project-docs",
        str(repo),
        "--adoption-level",
        adoption_level,
    ]
    if strict:
        command.append("--strict")
    return command


def validate(
    repo: Path,
    *,
    strict: bool = False,
    adoption_level: str = "continuity",
) -> subprocess.CompletedProcess[str]:
    return run(
        validator_command(repo, strict=strict, adoption_level=adoption_level),
        cwd=repo,
        check=False,
    )


def generated_artifacts(repo: Path) -> list[str]:
    found: list[str] = []
    for path in iter_paths(repo):
        if path.name in GENERATED_ARTIFACT_NAMES:
            found.append(str(path.relative_to(repo)))
    return sorted(found)


def empty_optional_dirs(repo: Path) -> list[str]:
    found: list[str] = []
    for rel_dir in OPTIONAL_DEEP_DIVE_DIRS:
        directory = repo / rel_dir
        if not directory.is_dir():
            continue
        files = [path for path in iter_paths(directory) if path.is_file()]
        meaningful = [
            path
            for path in files
            if path.name != "README.md" and not path.name.startswith(".")
        ]
        if files and not meaningful:
            found.append(rel_dir)
    return found


def file_contains(path: Path, *needles: str) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8").lower()
    return all(needle.lower() in text for needle in needles)


def feature_status(path: Path) -> str | None:
    if not path.exists():
        return None
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.lower().startswith("status:"):
            return stripped.split(":", 1)[1].strip().lower()
    return None


def feature_has_terminal_status(path: Path) -> bool:
    status = feature_status(path)
    return status in TERMINAL_FEATURE_STATUSES


def common_checks(repo: Path) -> list[Check]:
    standard = validate(repo)
    strict = validate(repo, strict=True)
    artifacts = generated_artifacts(repo)
    empty_dirs = empty_optional_dirs(repo)
    return [
        Check(
            "validator",
            standard.returncode == 0,
            "passed" if standard.returncode == 0 else standard.stdout.strip(),
        ),
        Check(
            "strict-validator",
            strict.returncode == 0,
            "passed" if strict.returncode == 0 else strict.stdout.strip(),
        ),
        Check(
            "no-generated-artifacts",
            not artifacts,
            "none" if not artifacts else ", ".join(artifacts),
        ),
        Check(
            "no-empty-optional-deep-dive-folders",
            not empty_dirs,
            "none" if not empty_dirs else ", ".join(empty_dirs),
        ),
    ]


def score_interrupted_worktree(repo: Path) -> list[Check]:
    result = run(
        [sys.executable, "src/splitter.py", "10", "A", "B", "C"],
        cwd=repo,
        check=False,
    )
    feature_doc = repo / "docs/features/rounding-policy.md"
    return common_checks(repo) + [
        Check("preserved-untracked-work", (repo / "NOTES.tmp").exists(), "NOTES.tmp"),
        Check(
            "rounding-output",
            result.stdout.strip().splitlines() == ["A: 3.34", "B: 3.33", "C: 3.33"],
            result.stdout.strip(),
        ),
        Check(
            "feature-terminal",
            feature_has_terminal_status(feature_doc),
            f"actual status: {feature_status(feature_doc) or 'missing'}",
        ),
    ]


def score_custom_docs_preservation(repo: Path) -> list[Check]:
    return common_checks(repo) + [
        Check(
            "product-doc-preserved",
            (repo / "docs/product/appointment-workflow.md").exists(),
            "docs/product/appointment-workflow.md",
        ),
        Check(
            "adr-doc-preserved",
            (repo / "docs/adr/001-python-module.md").exists(),
            "docs/adr/001-python-module.md",
        ),
        Check(
            "canonical-links-custom-docs",
            file_contains(repo / "docs/README.md", "docs/product", "docs/adr")
            or file_contains(repo / "docs/README.md", "product/appointment-workflow.md", "adr/001-python-module.md"),
            "docs/README.md links custom docs",
        ),
    ]


def score_feature_continuation(repo: Path) -> list[Check]:
    feature_doc = repo / "docs/features/add-due-dates.md"
    return common_checks(repo) + [
        Check("code-added-due", file_contains(repo / "src/task_notes.py", "--due", "due"), "src/task_notes.py"),
        Check(
            "feature-terminal",
            feature_has_terminal_status(feature_doc),
            f"actual status: {feature_status(feature_doc) or 'missing'}",
        ),
        Check("data-model-updated", file_contains(repo / "docs/data-model.md", "due"), "docs/data-model.md"),
    ]


def score_stale_docs_conflict(repo: Path) -> list[Check]:
    architecture = repo / "docs/architecture.md"
    stale_arch = False
    if architecture.exists():
        text = architecture.read_text(encoding="utf-8").lower()
        stale_arch = "postgresql" in text or "hosted web crawler" in text
    return common_checks(repo) + [
        Check("architecture-corrected", not stale_arch, "docs/architecture.md"),
        Check(
            "doc-health-recorded-stale-docs",
            file_contains(repo / "docs/doc-health.md", "stale")
            or file_contains(repo / "docs/doc-health.md", "conflict")
            or file_contains(repo / "docs/doc-health.md", "superseded"),
            "docs/doc-health.md",
        ),
    ]


SCORERS = {
    "interrupted-worktree": score_interrupted_worktree,
    "custom-docs-preservation": score_custom_docs_preservation,
    "feature-continuation": score_feature_continuation,
    "stale-docs-conflict": score_stale_docs_conflict,
}


def selected_scenarios(values: list[str]) -> list[str]:
    if not values or "all" in values:
        return SCENARIOS
    return values


def run_child_agent(
    *,
    scenario: str,
    repo: Path,
    logs_dir: Path,
    args: argparse.Namespace,
) -> int:
    logs_dir.mkdir(parents=True, exist_ok=True)
    stdout_log = logs_dir / f"{scenario}.stdout.log"
    final_message = logs_dir / f"{scenario}.final.md"
    prompt = PROMPTS[scenario].format(skill_dir=args.skill_dir)
    command = [
        args.codex_bin,
        "exec",
        "-m",
        args.model,
        "-c",
        f"model_reasoning_effort={args.reasoning_effort!r}",
        "-C",
        str(repo),
        "--full-auto",
        "-o",
        str(final_message),
        prompt,
    ]
    with stdout_log.open("w", encoding="utf-8") as log:
        process = subprocess.run(
            command,
            cwd=repo,
            text=True,
            stdout=log,
            stderr=subprocess.STDOUT,
            timeout=args.timeout,
        )
    return process.returncode


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--scenario",
        action="append",
        choices=["all", *SCENARIOS],
        default=[],
        help="Scenario to run. Repeat to run multiple scenarios. Defaults to all.",
    )
    parser.add_argument(
        "--codex-bin",
        default=os.environ.get("CODEX_BIN") or shutil.which("codex") or "codex",
        help="Codex executable used for live child-agent runs.",
    )
    parser.add_argument("--model", default="gpt-5.4-mini")
    parser.add_argument("--reasoning-effort", default="low")
    parser.add_argument("--skill-dir", default=str(skill_root()))
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument(
        "--work-root",
        help="Directory for disposable fixtures and logs. Defaults to a temp dir.",
    )
    parser.add_argument(
        "--fixture-only",
        action="store_true",
        help="Create fixtures and skip live Codex runs.",
    )
    parser.add_argument(
        "--score-only",
        help="Score an existing fixture path. Requires exactly one --scenario.",
    )
    parser.add_argument(
        "--keep",
        action="store_true",
        help="Keep disposable fixtures after the run.",
    )
    return parser.parse_args(argv)


def print_checks(scenario: str, checks: list[Check]) -> bool:
    passed = True
    print(f"\n## {scenario}")
    for check in checks:
        marker = "PASS" if check.passed else "FAIL"
        print(f"{marker}: {check.name} - {check.detail}")
        passed = passed and check.passed
    return passed


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    scenarios = selected_scenarios(args.scenario)

    if args.score_only:
        if len(scenarios) != 1:
            print("ERROR: --score-only requires exactly one --scenario", file=sys.stderr)
            return 2
        repo = Path(args.score_only).resolve()
        return 0 if print_checks(scenarios[0], SCORERS[scenarios[0]](repo)) else 1

    temp_root: Path | None = None
    if args.work_root:
        work_root = Path(args.work_root).resolve()
        work_root.mkdir(parents=True, exist_ok=True)
    else:
        temp_root = Path(tempfile.mkdtemp(prefix="repo-memory-forward-test-"))
        work_root = temp_root

    logs_dir = work_root / "logs"
    fixtures_dir = work_root / "fixtures"
    all_passed = True

    try:
        for scenario in scenarios:
            repo = fixtures_dir / scenario
            if repo.exists():
                shutil.rmtree(repo)
            BUILDERS[scenario](repo)
            print(f"Created fixture: {repo}")
            if args.fixture_only:
                continue
            if not args.fixture_only:
                code = run_child_agent(
                    scenario=scenario,
                    repo=repo,
                    logs_dir=logs_dir,
                    args=args,
                )
                if code != 0:
                    print(f"Child agent failed for {scenario} with exit code {code}")
                    all_passed = False
            checks = SCORERS[scenario](repo)
            all_passed = print_checks(scenario, checks) and all_passed

        print(f"\nFixtures: {fixtures_dir}")
        print(f"Logs: {logs_dir}")
        return 0 if all_passed else 1
    finally:
        if temp_root and not args.keep:
            shutil.rmtree(temp_root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
