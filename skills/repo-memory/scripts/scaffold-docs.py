#!/usr/bin/env python3
"""Create a Repo Memory docs skeleton in an empty or new repository."""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from textwrap import dedent


@dataclass(frozen=True)
class ScaffoldFile:
    path: str
    content: str


def clean(text: str) -> str:
    return dedent(text).strip() + "\n"


def metadata(
    *,
    doc_type: str,
    canonical_source: str,
    related_docs: str,
    today: str,
    status: str = "draft",
    confidence: str = "low",
) -> str:
    return clean(
        f"""
        Doc type: {doc_type}
        Owner: current-agent-or-team
        Status: {status}
        Last updated: {today}
        Last verified: unknown
        Verified against: unknown
        Confidence: {confidence}
        Canonical source: `{canonical_source}`
        Related docs: {related_docs}
        """
    )


def docs_readme(project_name: str) -> str:
    return clean(
        f"""
        # {project_name} Docs 🧭

        Welcome, future human or agent. This folder is the project map, not a
        mystery novel. Use it to find the one place each kind of project truth
        lives.

        ## Start Here

        1. Find the topic in the ownership map.
        2. Open only the owner you need.
        3. If no task was assigned, use `feature-registry.md` and pick the
           first `ready` row.
        4. Before changing a feature, read its `features/<feature-slug>.md`.

        ```mermaid
        flowchart TD
          A["Start here"] --> B["Find the topic"]
          B --> C["Open the canonical owner"]
          C --> D["Update that owner when facts change"]
          B --> E["No task assigned?"]
          E --> F["Use feature-registry.md"]
        ```

        ## Canonical Ownership Map

        One row, one owner. Supporting docs can help, but the owner is where
        current truth changes.

        | Capability | Canonical owner | Supporting docs | Notes |
        | --- | --- | --- | --- |
        | Goal, users, scope | `project-overview.md` | root `README.md` | Product intent goes here. |
        | Functional requirements | `requirements/functional-requirements.md` | `project-overview.md` | Accepted behavior. |
        | Non-functional requirements | `requirements/non-functional-requirements.md` | `project-overview.md` | Quality attributes and constraints. |
        | Architecture | `architecture.md` | `data-model.md`, `interfaces-and-contracts.md` | Replace with a stronger existing architecture owner if one exists. |
        | Interfaces and contracts | `interfaces-and-contracts.md` | API specs, schemas, MCP docs | External contracts beat prose summaries. |
        | Data model | `data-model.md` | schemas, migrations | Durable entities, relationships, and lifecycle. |
        | Local development | `local-development.md` | `CONTRIBUTING.md` | Commands live in one place. Everyone breathes easier. |
        | Testing strategy | `testing-strategy.md` | CI docs | Test layers, gaps, and verification habits. |
        | Observability | `observability-and-instrumentation.md` | dashboards, analytics docs | Logs, metrics, traces, alerts, and production clues. |
        | Operations and support | `operations-runbook.md` | deploy docs | Runbooks, rollout notes, and support paths. |
        | Security and privacy | `security-and-privacy.md` | `SECURITY.md` | Secrets, PII, permissions, and trust boundaries. |
        | Decisions and rationale | `decision-log.md` | ADRs | Why choices were made. |
        | Implementation history | `implementation-log.md` | changelog | What landed and when. |
        | Feature state and next work | `feature-registry.md` | `features/` | Queue, statuses, and default next task. |
        | Active handoff | `features/<feature-slug>.md` | `feature-registry.md` | Resume context, validation, and next safe step. |
        | Doc health | `doc-health.md` | this file | Stale docs, conflicts, verification gaps. |
        | Raw ideas and evidence | `intake/README.md` | intake files | Brain dumps live here until accepted facts graduate. 🎓 |

        ## Handy Links

        - 🧠 Product intent: [project-overview.md](./project-overview.md)
        - 🧱 Architecture: [architecture.md](./architecture.md)
        - ✅ Requirements: [requirements/](./requirements/)
        - 🧪 Tests: [testing-strategy.md](./testing-strategy.md)
        - 🚦 Next work: [feature-registry.md](./feature-registry.md)
        - 🩺 Doc health: [doc-health.md](./doc-health.md)
        - 📥 Raw intake: [intake/README.md](./intake/README.md)

        ## Tiny Rules

        - Keep facts in their owner, not sprinkled everywhere.
        - Link to strong existing docs instead of copying them.
        - Mark unknowns as unknown. Guessing wears a fake mustache.
        - When reality changes, update the owner and `doc-health.md`.
        """
    )


def intake_readme() -> str:
    return clean(
        """
        # Intake

        Use this folder as a low-friction inbox for raw brainstorms, project
        notes, chat exports, AI plans, sketches, or imported planning docs that
        have not yet been promoted into canonical Repo Memory docs.

        ## How to Use

        - Drop raw source material here when it is useful but not yet structured.
        - Prefer kebab-case names for authored Markdown, but imported files can
          keep their source names.
        - Do not treat raw intake as canonical project truth.
        - Before building from an intake item, extract accepted facts into the
          relevant baseline, requirements, design, decision, feature, or handoff
          docs.
        - Link important intake files from `Evidence`, `Plan Provenance`, or
          `Source artifacts` where they shaped accepted project direction.
        - Record reviewed intake, unresolved questions, and stale or superseded
          source material in `../doc-health.md` when it affects future work.

        ## Suggested File Names

        - `YYYY-MM-DD-initial-brainstorm.md`
        - `YYYY-MM-DD-planning-notes.md`
        - `YYYY-MM-DD-ai-plan.md`
        """
    )


def project_overview(today: str) -> str:
    meta = metadata(
            doc_type="project-overview",
            canonical_source="docs/project-overview.md",
            related_docs="`architecture.md`, `requirements/functional-requirements.md`",
            today=today,
        ).strip()
    body = clean(
        """
        ## Project Goal

        TODO: State the outcome this project is meant to achieve.

        ## Problem Statement

        TODO: Describe the user, business, developer, or operational problem this
        project exists to solve.

        ## Target Users or Actors

        | User or actor | Goal | Notes |
        | --- | --- | --- |
        | TODO | TODO | TODO |

        ## Success Criteria

        - TODO: Add an observable success criterion.

        ## Current Scope

        - TODO: List confirmed in-scope capabilities.

        ## Non-Goals

        - TODO: List explicitly out-of-scope or deferred work.

        ## Evidence

        - TODO: Add source files, tests, product notes, or user statements that
          support this overview.

        ## Open Questions

        - TODO: Add unverified project intent or product context.
        """
    )
    return f"# Project Overview\n\n{meta}\n\n{body}"


def simple_doc(
    *,
    title: str,
    doc_type: str,
    canonical_source: str,
    related_docs: str,
    today: str,
    sections: list[tuple[str, list[str]]],
) -> str:
    body = [
        f"# {title}",
        "",
        metadata(
            doc_type=doc_type,
            canonical_source=canonical_source,
            related_docs=related_docs,
            today=today,
        ).strip(),
    ]
    for heading, bullets in sections:
        body.append("")
        body.append(f"## {heading}")
        body.append("")
        for bullet in bullets:
            body.append(f"- {bullet}")
    return "\n".join(body).strip() + "\n"


def feature_template(today: str) -> str:
    return clean(
        f"""
        # Feature: feature-slug

        Doc type: feature
        Feature slug: feature-slug
        Owner: current-agent-or-team
        Status: planned
        Priority: medium
        Last updated: {today}
        Last verified: unknown
        Verified against: unknown
        Confidence: low
        Canonical source: `docs/features/feature-slug.md`
        Related docs: `../feature-registry.md`
        Validation status: not started
        Next safe step: define the feature goal and scope.

        ## Goal

        TODO: State the feature outcome.

        ## Scope

        - TODO: In scope.
        - TODO: Out of scope.

        ## Plan Provenance

        - Planned by: TODO
        - Tool or agent surface: TODO
        - Role or lens: TODO
        - Date: TODO
        - Inputs reviewed: TODO
        - Source artifacts: TODO
        - Assumptions: TODO
        - Confidence: low
        - Plan disposition: proposed
        - Implementer pickup: TODO

        ## Implementation Status

        - [ ] TODO: Add implementation task.

        ## Files Touched or Expected

        - TODO: Add likely files after discovery.

        ## Validation

        - TODO: Add commands, tests, or manual checks.

        ## Review Log

        | Date | Reviewer | Tool or agent surface | Role or lens | Subject | Disposition | Record |
        | --- | --- | --- | --- | --- | --- | --- |
        | TODO | TODO | TODO | TODO | TODO | TODO | TODO |

        ## Open Questions

        - TODO: Add unknowns.

        ## Next Agent Handoff

        TODO: Write the next safe step for another agent.
        """
    )


def user_stories(today: str) -> str:
    meta = metadata(
            doc_type="user-stories-and-use-cases",
            canonical_source="docs/requirements/user-stories-and-use-cases.md",
            related_docs="`../project-overview.md`, `functional-requirements.md`",
            today=today,
        ).strip()
    body = clean(
        """
        ## Actors

        | Actor | Goal | Notes |
        | --- | --- | --- |
        | TODO | TODO | TODO |

        ## Personas or User Segments

        - TODO: Add personas or segments when known.

        ## User Stories

        - TODO: As a user, I want a capability so that I get an outcome.

        ## Journey Map

        - TODO: Describe the main journey when known.

        ## Primary Use Cases

        - TODO: Add the main use cases and acceptance paths.

        ## Alternative Flows

        - TODO: Add non-happy-path flows.

        ## Failure States

        - TODO: Add expected failure or empty states.

        ## Accessibility and Inclusion Notes

        - TODO: Add accessibility expectations.

        ## Acceptance Notes

        - TODO: Add acceptance criteria or examples.

        ## Open Questions

        - TODO: Add unknown user or workflow context.
        """
    )
    return f"# User Stories and Use Cases\n\n{meta}\n\n{body}"


def agents_md() -> str:
    return clean(
        """
        # Agent Instructions

        This repository uses Repo Memory. `docs/README.md` contains the
        Canonical Ownership Map that names the single owner for each durable
        documentation capability.

        ## Startup

        1. Read `docs/README.md`.
        2. Run the validator (`python3 skills/repo-memory/scripts/validate-docs.py --project-docs --strict` when installed) to check for documentation drift.
        3. Follow the Canonical Ownership Map to the owner for the current task.
        4. Read `docs/feature-registry.md`; when no task is assigned, pick the
           first `ready` row in `Next Work Queue`.
        5. If `docs/intake/` contains raw brainstorms, project notes, or plans,
           review them and promote accepted facts into the mapped owner before
           building from them.
        6. Read the active `docs/features/<feature-slug>.md` before changing
           related code.

        ## Maintenance

        - Run the validator (`python3 skills/repo-memory/scripts/validate-docs.py --project-docs --strict` when installed) before ending a session to fix drift or broken links.
        - Place companion plans/specs only in `docs/superpowers/plans/` or `docs/superpowers/specs/` (or `docs/designs/`).
        - Keep durable project facts in their mapped owner, not only in chat history.
        - Do not duplicate mutable facts in this file.
        - Keep `docs/feature-registry.md` current as the ranked next-work queue.
        - Update feature docs, `docs/implementation-log.md`,
          `docs/decision-log.md`, and `docs/doc-health.md` when warranted.
        - Mark inferred or unknown facts explicitly.
        """
    )


def build_files(
    *,
    project_name: str,
    today: str,
    include_user_stories: bool,
    with_agents: bool,
) -> list[ScaffoldFile]:
    files = [
        ScaffoldFile("docs/README.md", docs_readme(project_name)),
        ScaffoldFile("docs/intake/README.md", intake_readme()),
        ScaffoldFile("docs/project-overview.md", project_overview(today)),
        ScaffoldFile(
            "docs/architecture.md",
            simple_doc(
                title="Architecture",
                doc_type="architecture",
                canonical_source="docs/architecture.md",
                related_docs="`project-overview.md`, `interfaces-and-contracts.md`, `data-model.md`",
                today=today,
                sections=[
                    ("System Shape", ["TODO: Describe the main application, services, packages, or modules."]),
                    ("Runtime Topology", ["TODO: Describe how the system runs locally and in deployment."]),
                    ("Key Components", ["TODO: List major components and responsibilities."]),
                    ("Data and Control Flow", ["TODO: Describe important flows once known."]),
                    ("External Dependencies", ["TODO: List external systems or services."]),
                    ("Evidence", ["TODO: Add source, config, test, or design evidence."]),
                    ("Open Questions", ["TODO: Add unknown architecture context."]),
                ],
            ),
        ),
        ScaffoldFile(
            "docs/interfaces-and-contracts.md",
            simple_doc(
                title="Interfaces and Contracts",
                doc_type="interfaces-and-contracts",
                canonical_source="docs/interfaces-and-contracts.md",
                related_docs="`architecture.md`, `data-model.md`",
                today=today,
                sections=[
                    ("Public Interfaces", ["TODO: Document APIs, CLI commands, MCP tools, events, or UI contracts."]),
                    ("Payloads and Schemas", ["TODO: Document request, response, and data contracts."]),
                    ("External Integrations", ["TODO: Document third-party or cross-service contracts."]),
                    ("Compatibility Notes", ["TODO: Document versioning or migration constraints."]),
                    ("Evidence", ["TODO: Add handlers, schemas, clients, tests, or config evidence."]),
                    ("Open Questions", ["TODO: Add contract unknowns."]),
                ],
            ),
        ),
        ScaffoldFile(
            "docs/data-model.md",
            simple_doc(
                title="Data Model",
                doc_type="data-model",
                canonical_source="docs/data-model.md",
                related_docs="`architecture.md`, `interfaces-and-contracts.md`",
                today=today,
                sections=[
                    ("Entities", ["TODO: List domain entities or records."]),
                    ("Relationships", ["TODO: Describe ownership and relationships."]),
                    ("Lifecycle", ["TODO: Describe creation, update, archival, and deletion rules."]),
                    ("Storage", ["TODO: Document persistence, files, caches, queues, or external stores."]),
                    ("Evidence", ["TODO: Add schema, type, migration, storage, or fixture evidence."]),
                    ("Open Questions", ["TODO: Add data ownership or retention unknowns."]),
                ],
            ),
        ),
        ScaffoldFile(
            "docs/local-development.md",
            simple_doc(
                title="Local Development",
                doc_type="local-development",
                canonical_source="docs/local-development.md",
                related_docs="`testing-strategy.md`, `operations-runbook.md`",
                today=today,
                sections=[
                    ("Prerequisites", ["TODO: List runtime, package manager, services, and credentials."]),
                    ("Setup", ["TODO: Add first-run setup commands."]),
                    ("Common Commands", ["TODO: Add build, test, lint, dev server, and codegen commands."]),
                    ("Fixtures and Local Data", ["TODO: Add seed, mock, or fixture workflows."]),
                    ("Troubleshooting", ["TODO: Add common local failure modes."]),
                    ("Open Questions", ["TODO: Add unknown tooling context."]),
                ],
            ),
        ),
        ScaffoldFile(
            "docs/doc-health.md",
            "# Documentation Health\n\n"
            + metadata(
                    doc_type="doc-health",
                    canonical_source="docs/doc-health.md",
                    related_docs="`README.md`, `feature-registry.md`, `decision-log.md`",
                    today=today,
                    status="active",
                ).strip()
            + "\n\n"
            + clean(
                f"""
                Last full audit: unknown
                Known stale areas: initial skeleton contains placeholders
                Open doc conflicts: none known

                ## Verification Summary

                | Doc | Last verified | Evidence | Confidence | Notes |
                | --- | --- | --- | --- | --- |
                | `project-overview.md` | unknown | unknown | low | Replace scaffold placeholders. |
                | `intake/README.md` | {today} | scaffold-docs.py | low | Raw intake inbox created for unstructured source material. |

                ## Known Stale Areas

                - Initial scaffold placeholders need project-specific evidence.

                ## Open Doc Conflicts

                - None known.

                ## Rename and Supersession Notes

                - None.

                ## Change Log

                | Date | Change | Evidence |
                | --- | --- | --- |
                | {today} | Created Repo Memory documentation skeleton. | scaffold-docs.py |
                | {today} | Created raw intake inbox for brainstorms and planning dumps. | `docs/intake/README.md` |
                """
            ),
        ),
        ScaffoldFile(
            "docs/observability-and-instrumentation.md",
            simple_doc(
                title="Observability and Instrumentation",
                doc_type="observability-and-instrumentation",
                canonical_source="docs/observability-and-instrumentation.md",
                related_docs="`operations-runbook.md`, `security-and-privacy.md`",
                today=today,
                sections=[
                    ("Logs", ["TODO: Document logs, log levels, correlation IDs, and redaction rules."]),
                    ("Metrics", ["TODO: Document service, product, and business metrics."]),
                    ("Traces", ["TODO: Document tracing boundaries and propagation."]),
                    ("Product Analytics Events", ["TODO: Document analytics events and event ownership."]),
                    ("Audit Events", ["TODO: Document security or compliance audit events."]),
                    ("Dashboards and Alerts", ["TODO: Link dashboards and alert rules."]),
                    ("Privacy and Retention", ["TODO: Document telemetry privacy boundaries and retention."]),
                    ("Known Blind Spots", ["TODO: List missing instrumentation or monitoring gaps."]),
                ],
            ),
        ),
        ScaffoldFile(
            "docs/testing-strategy.md",
            simple_doc(
                title="Testing Strategy",
                doc_type="testing-strategy",
                canonical_source="docs/testing-strategy.md",
                related_docs="`local-development.md`, `requirements/functional-requirements.md`",
                today=today,
                sections=[
                    ("Test Types", ["TODO: Document unit, integration, end-to-end, manual, or contract tests."]),
                    ("Commands", ["TODO: Add commands used to run tests."]),
                    ("Coverage Expectations", ["TODO: Document critical behavior that must be covered."]),
                    ("Gaps", ["TODO: List missing tests or manual-only checks."]),
                    ("Open Questions", ["TODO: Add unknown test strategy context."]),
                ],
            ),
        ),
        ScaffoldFile(
            "docs/operations-runbook.md",
            simple_doc(
                title="Operations Runbook",
                doc_type="operations-runbook",
                canonical_source="docs/operations-runbook.md",
                related_docs="`local-development.md`, `observability-and-instrumentation.md`",
                today=today,
                sections=[
                    ("Runtime Commands", ["TODO: Add start, stop, deploy, rollback, and maintenance commands."]),
                    ("Environment and Configuration", ["TODO: Document runtime config and secret handling."]),
                    ("Release and Rollback", ["TODO: Document release and rollback process."]),
                    ("Troubleshooting", ["TODO: Add operational failure modes and checks."]),
                    ("Open Questions", ["TODO: Add unknown operations context."]),
                ],
            ),
        ),
        ScaffoldFile(
            "docs/security-and-privacy.md",
            simple_doc(
                title="Security and Privacy",
                doc_type="security-and-privacy",
                canonical_source="docs/security-and-privacy.md",
                related_docs="`interfaces-and-contracts.md`, `data-model.md`, `observability-and-instrumentation.md`",
                today=today,
                sections=[
                    ("Security Model", ["TODO: Document auth, authorization, trust boundaries, and threat model."]),
                    ("Secrets and Credentials", ["TODO: Document secret sources and handling rules."]),
                    ("Data Sensitivity", ["TODO: Document PII, sensitive data, and retention rules."]),
                    ("Privacy Boundaries", ["TODO: Document logging, analytics, and telemetry privacy constraints."]),
                    ("Open Questions", ["TODO: Add unknown security or privacy context."]),
                ],
            ),
        ),
        ScaffoldFile(
            "docs/decision-log.md",
            "# Decision Log\n\n"
            + metadata(
                    doc_type="decision-log",
                    canonical_source="docs/decision-log.md",
                    related_docs="`architecture.md`, `implementation-log.md`",
                    today=today,
                    status="active",
                ).strip()
            + "\n\n"
            + clean(
                f"""
                Decision ID format: `DL-000`
                Confidence rule: use `high`, `medium`, or `low`
                Supersession rule: keep superseded decisions and link replacements

                ## DL-000: Adopt Repo Memory Documentation Skeleton

                Status: implemented
                Confidence: high

                Decision: Initialize the standard Repo Memory docs skeleton.

                Rationale: The repository needs a canonical place for project
                context before implementation details exist.

                Evidence: `docs/` scaffold generated on {today}.

                Consequences:

                - Future project facts should be recorded in `docs/`.
                - Placeholder sections should be replaced with evidence-backed content.
                """
            ),
        ),
        ScaffoldFile(
            "docs/implementation-log.md",
            "# Implementation Log\n\n"
            + metadata(
                    doc_type="implementation-log",
                    canonical_source="docs/implementation-log.md",
                    related_docs="`decision-log.md`, `feature-registry.md`",
                    today=today,
                    status="active",
                ).strip()
            + "\n\n"
            + clean(
                f"""
                ## {today}

                Change summary: Created the initial Repo Memory documentation skeleton.

                Evidence: `docs/` scaffold exists.
                """
            ),
        ),
        ScaffoldFile(
            "docs/feature-registry.md",
            "# Feature Registry\n\n"
            + metadata(
                    doc_type="feature-registry",
                    canonical_source="docs/feature-registry.md",
                    related_docs="`features/_template.md`",
                    today=today,
                    status="active",
                ).strip()
            + "\n\n"
            + clean(
                f"""
                ## Next Work Queue

                | Rank | Work item | Type | Status | Ready | Why next | Next safe step | Canonical doc | Last verified |
                | --- | --- | --- | --- | --- | --- | --- | --- | --- |

                Ready values: `ready`, `verify-first`, `needs-human`, `blocked`.
                Pick the lowest-rank `ready` row when no task is assigned. Use
                `verify-first` for inspection-only pickup until evidence is refreshed.

                ## Feature List

                | Feature | Slug | Status | Priority | Last updated | Notes |
                | --- | --- | --- | --- | --- | --- |

                Allowed statuses: `research`, `planned`, `in_progress`, `blocked`,
                `implemented`, `verified`, `shipped`, `abandoned`, `superseded`,
                `deprecated`, `rolled_back`.
                """
            ),
        ),
        ScaffoldFile(
            "docs/requirements/functional-requirements.md",
            simple_doc(
                title="Functional Requirements",
                doc_type="functional-requirements",
                canonical_source="docs/requirements/functional-requirements.md",
                related_docs="`../project-overview.md`, `../feature-registry.md`",
                today=today,
                sections=[
                    ("Current Requirements", ["TODO: Add confirmed functional behavior."]),
                    ("Acceptance Criteria", ["TODO: Add acceptance criteria or examples."]),
                    ("Out of Scope", ["TODO: Add explicitly excluded behavior."]),
                    ("Evidence", ["TODO: Add product notes, tests, UI flows, APIs, or user statements."]),
                    ("Open Questions", ["TODO: Add unverified behavior."]),
                ],
            ),
        ),
        ScaffoldFile(
            "docs/requirements/non-functional-requirements.md",
            simple_doc(
                title="Non-Functional Requirements",
                doc_type="non-functional-requirements",
                canonical_source="docs/requirements/non-functional-requirements.md",
                related_docs="`../architecture.md`, `../operations-runbook.md`, `../security-and-privacy.md`",
                today=today,
                sections=[
                    ("Performance", ["TODO: Add latency, throughput, or resource expectations."]),
                    ("Reliability", ["TODO: Add availability, retry, backup, or recovery expectations."]),
                    ("Scalability", ["TODO: Add scale assumptions and limits."]),
                    ("Security and Privacy", ["TODO: Add compliance, data, and access constraints."]),
                    ("Compatibility", ["TODO: Add platform, browser, runtime, or API compatibility constraints."]),
                    ("Open Questions", ["TODO: Add unknown quality constraints."]),
                ],
            ),
        ),
        ScaffoldFile("docs/features/_template.md", feature_template(today)),
    ]
    if include_user_stories:
        files.append(
            ScaffoldFile(
                "docs/requirements/user-stories-and-use-cases.md",
                user_stories(today),
            )
        )
    if with_agents:
        files.append(ScaffoldFile("AGENTS.md", agents_md()))
    return files


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a Repo Memory docs skeleton in a target repository."
    )
    parser.add_argument("path", nargs="?", default=".", help="Target repository path")
    parser.add_argument(
        "--project-name",
        help="Project name to use in docs/README.md. Defaults to the directory name.",
    )
    parser.add_argument(
        "--date",
        default=date.today().isoformat(),
        help="Date to write in metadata. Defaults to today.",
    )
    parser.add_argument(
        "--include-user-stories",
        action="store_true",
        help="Also create docs/requirements/user-stories-and-use-cases.md.",
    )
    parser.add_argument(
        "--with-agents",
        action="store_true",
        help="Also create a thin root AGENTS.md entrypoint.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing scaffold files.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print files that would be created without writing them.",
    )
    parser.add_argument(
        "--new-feature",
        help="Scaffold a single new feature file and register it in the registry.",
    )
    parser.add_argument(
        "--priority",
        default="medium",
        help="Priority for the new feature (default: medium).",
    )
    parser.add_argument(
        "--status",
        default="planned",
        help="Status for the new feature (default: planned).",
    )
    return parser.parse_args(argv)


import re

def split_table_row(line: str) -> list[str]:
    return [cell.strip().strip("`").strip() for cell in line.strip().strip("|").split("|")]


def register_feature_in_file(registry_path: Path, slug: str, status: str, priority: str, today: str) -> None:
    if not registry_path.exists():
        return

    content = registry_path.read_text(encoding="utf-8")
    lines = content.splitlines()

    queue_heading_idx = -1
    list_heading_idx = -1
    for idx, line in enumerate(lines):
        if line.strip().startswith("## Next Work Queue"):
            queue_heading_idx = idx
        elif line.strip().startswith("## Feature List"):
            list_heading_idx = idx

    # Append to Next Work Queue
    if queue_heading_idx != -1:
        last_row_idx = -1
        for idx in range(queue_heading_idx + 1, len(lines)):
            line = lines[idx].strip()
            if line.startswith("|"):
                last_row_idx = idx
            elif last_row_idx != -1:
                break
        
        if last_row_idx != -1:
            title = slug.replace("-", " ").title()
            new_queue_row = f"| TBD | {title} | feature | `{status}` | `ready` | TODO: why this is next | TODO: next safe step | [`features/{slug}.md`](./features/{slug}.md) | {today} |"
            lines.insert(last_row_idx + 1, new_queue_row)
            if list_heading_idx > last_row_idx:
                list_heading_idx += 1

    # Append to Feature List
    if list_heading_idx != -1:
        last_row_idx = -1
        for idx in range(list_heading_idx + 1, len(lines)):
            line = lines[idx].strip()
            if line.startswith("|"):
                last_row_idx = idx
            elif last_row_idx != -1:
                break
        
        if last_row_idx != -1:
            title = slug.replace("-", " ").title()
            new_list_row = f"| {title} | `{slug}` | `{status}` | {priority.title()} | {today} | [Feature doc](./features/{slug}.md) |"
            lines.insert(last_row_idx + 1, new_list_row)

    registry_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def scaffold_single_feature(target: Path, slug: str, status: str, priority: str, today: str, force: bool = False, dry_run: bool = False) -> int:
    docs_dir = target / "docs"
    if not docs_dir.exists():
        print("Error: docs/ directory does not exist. Initialize Repo Memory first using scaffold-docs.py", file=sys.stderr)
        return 1

    if dry_run:
        print(f"Would create feature doc: docs/features/{slug}.md")
        print(f"Would register feature '{slug}' in docs/feature-registry.md")
        return 0

    features_dir = docs_dir / "features"
    features_dir.mkdir(parents=True, exist_ok=True)
    feature_path = features_dir / f"{slug}.md"
    
    if feature_path.exists() and not force:
        print(f"Error: feature file already exists: {feature_path}. Use --force to overwrite.", file=sys.stderr)
        return 1

    template_path = features_dir / "_template.md"
    if template_path.exists():
        content = template_path.read_text(encoding="utf-8")
    else:
        content = feature_template(today)

    title = slug.replace("-", " ").title()
    content = content.replace("Feature: feature-slug", f"Feature: {title}")
    content = content.replace("feature-slug", slug)
    content = content.replace("Priority: medium", f"Priority: {priority}")
    content = content.replace("Status: planned", f"Status: {status}")
    content = re.sub(r"Last updated:\s*\d{4}-\d{2}-\d{2}", f"Last updated: {today}", content)

    feature_path.write_text(content, encoding="utf-8")
    print(f"Created feature doc: {feature_path.relative_to(target)}")

    registry_path = docs_dir / "feature-registry.md"
    if registry_path.exists():
        register_feature_in_file(registry_path, slug, status, priority, today)
        print(f"Updated feature registry: {registry_path.relative_to(target)}")
    else:
        print("Warning: feature-registry.md not found, feature was not registered.", file=sys.stderr)

    return 0


def run(argv: list[str]) -> int:
    args = parse_args(argv)
    target = Path(args.path).resolve()
    if target.exists() and not target.is_dir():
        print(f"Error: target path is not a directory: {target}", file=sys.stderr)
        return 1

    if args.new_feature:
        return scaffold_single_feature(
            target=target,
            slug=args.new_feature,
            status=args.status,
            priority=args.priority,
            today=args.date,
            force=args.force,
            dry_run=args.dry_run,
        )

    project_name = args.project_name or target.name or "Project"
    files = build_files(
        project_name=project_name,
        today=args.date,
        include_user_stories=args.include_user_stories,
        with_agents=args.with_agents,
    )

    existing = [file.path for file in files if (target / file.path).exists()]
    if existing and not args.force:
        print("Error: refusing to overwrite existing files:", file=sys.stderr)
        for path in existing:
            print(f"  {path}", file=sys.stderr)
        print("Use --force to overwrite scaffold files.", file=sys.stderr)
        return 1

    if args.dry_run:
        print(f"Would scaffold Repo Memory docs in {target}:")
        for file in files:
            print(f"  {file.path}")
        return 0

    target.mkdir(parents=True, exist_ok=True)
    for file in files:
        path = target / file.path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(file.content, encoding="utf-8")

    print(f"Created Repo Memory docs skeleton in {target}")
    for file in files:
        print(f"  {file.path}")
    return 0


if __name__ == "__main__":
    sys.exit(run(sys.argv[1:]))
