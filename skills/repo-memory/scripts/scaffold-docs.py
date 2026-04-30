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
        # {project_name} Documentation

        This `docs/` tree is the canonical source of truth for project context,
        architecture, requirements, decisions, feature status, and handoff state.

        ## Agent Startup Order

        1. Read this file.
        2. Read `project-overview.md` and `architecture.md`.
        3. Read `feature-registry.md`.
        4. Read the active `features/<feature-slug>.md` before changing related code.

        ## Baseline Docs

        - [Project overview](./project-overview.md)
        - [Architecture](./architecture.md)
        - [Interfaces and contracts](./interfaces-and-contracts.md)
        - [Data model](./data-model.md)
        - [Local development](./local-development.md)
        - [Doc health](./doc-health.md)
        - [Observability and instrumentation](./observability-and-instrumentation.md)
        - [Testing strategy](./testing-strategy.md)
        - [Operations runbook](./operations-runbook.md)
        - [Security and privacy](./security-and-privacy.md)
        - [Decision log](./decision-log.md)
        - [Implementation log](./implementation-log.md)
        - [Feature registry](./feature-registry.md)
        - [Functional requirements](./requirements/functional-requirements.md)
        - [Non-functional requirements](./requirements/non-functional-requirements.md)
        - [Feature template](./features/_template.md)

        ## Maintenance Rules

        - Keep durable project facts in this docs tree.
        - Mark unknowns explicitly instead of guessing.
        - Update feature docs, implementation log, decision log, and doc health
          when project reality changes.
        - Keep agent instruction files thin and linked here.
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

        This repository uses the `docs/` folder as the canonical source of truth
        for project context, architecture, requirements, feature status,
        implementation history, and cross-agent handoff state.

        ## Startup

        1. Read `docs/README.md`.
        2. Read `docs/project-overview.md` and `docs/architecture.md`.
        3. Read `docs/feature-registry.md`.
        4. Read the active `docs/features/<feature-slug>.md` before changing
           related code.

        ## Maintenance

        - Keep durable project facts in `docs/`, not only in chat history.
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
    return parser.parse_args(argv)


def run(argv: list[str]) -> int:
    args = parse_args(argv)
    target = Path(args.path).resolve()
    if target.exists() and not target.is_dir():
        print(f"Error: target path is not a directory: {target}", file=sys.stderr)
        return 1

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
