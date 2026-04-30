# Repo Memory Portable Standard

Version: 1.5

Repo Memory is a repo-native project context standard for AI-assisted software
projects. It defines documentation files, metadata, status values, evidence
rules, and handoff expectations that help humans and coding agents understand,
resume, and change a project from shared repo docs.

This file is the normative entrypoint for the standard. `SKILL.md` describes
one installable skill implementation of the same standard.

## Purpose

Repo Memory exists to make project context portable across tools.

Agent instruction files such as `AGENTS.md`, `.github/copilot-instructions.md`,
and `CLAUDE.md` tell an agent how to behave in a repository. Repo Memory defines
where durable project truth lives:

- architecture and system shape
- requirements and user-facing behavior
- interfaces, contracts, and data model
- local development, testing, operations, and security posture
- observability, instrumentation, telemetry, and production signals
- durable decisions and implementation history
- active feature state and next-agent handoff context
- provenance for substantial plans, specialist reviews, and tool-generated guidance that influence implementation
- documentation freshness, conflicts, renames, and verification evidence

The standard is intentionally plain Markdown plus optional validation. A repo
can adopt it without choosing a particular AI provider, editor, plugin, or
agent framework.

## Standard Components

A Repo Memory adoption has four layers:

1. Canonical project docs in `docs/`.
2. Thin agent entrypoints that point agents to the canonical docs.
3. Metadata and status values that make docs consistent across tools.
4. A continuity process for keeping docs verified, current, and resumable.

The standard does not require an agent runtime. Platform-specific integrations
are adapters around the docs, not replacements for them.

## Conformance Levels

Use these levels to describe how fully a repository has adopted the standard.

| Level | Name | Requirement |
| --- | --- | --- |
| 0 | Not adopted | No maintained Repo Memory docs set exists. |
| 1 | Baseline | Required docs exist in `docs/` and follow naming rules. |
| 2 | Continuity | Baseline plus feature registry, active feature handoffs, decision log, implementation log, and doc health. |
| 3 | Verified | Continuity plus metadata, verification dates, confidence, evidence links, and validator checks in local workflow or CI. |
| 4 | Integrated | Verified plus aligned agent entrypoints and optional platform adapters, CLI, plugin, or MCP integration. |

A useful open source or production repo should aim for Level 2 or Level 3.
Level 4 is optional and tool-specific.

## Required Baseline

A Repo Memory-compliant repo keeps these files directly under `docs/`:

```text
docs/
├── README.md
├── project-overview.md
├── architecture.md
├── interfaces-and-contracts.md
├── data-model.md
├── local-development.md
├── doc-health.md
├── observability-and-instrumentation.md
├── testing-strategy.md
├── operations-runbook.md
├── security-and-privacy.md
├── decision-log.md
├── implementation-log.md
├── feature-registry.md
├── requirements/
│   ├── functional-requirements.md
│   └── non-functional-requirements.md
└── features/
    └── _template.md
```

Optional docs are added only when the project needs the depth:

- `docs/requirements/user-stories-and-use-cases.md`
- `docs/diagrams/`
- `docs/designs/`
- `docs/reviews/`
- `docs/project-details/`
- `docs/components/`
- `docs/ui-ux/`
- `docs/features/<feature-slug>/`

All placement and naming details are defined in
[`references/docs-structure-rules.md`](./references/docs-structure-rules.md).

## Empty Repository Bootstrap

An empty or nearly empty repository can adopt Repo Memory before implementation
exists. In that case, create the required baseline docs as a skeleton, mark
project-specific facts as `TODO` or `unknown`, and record in `docs/doc-health.md`
that the initial docs are placeholders that still need evidence.

The skill package includes a scaffold helper:

```bash
python3 <skill-dir>/scripts/scaffold-docs.py /path/to/repo --with-agents
```

Resolve `<skill-dir>` to the directory that contains `SKILL.md`. When working
from this repository root, use `skills/repo-memory/scripts/...`.

The skeleton is a starting state, not verified project truth. Replace
placeholders only with confirmed user statements, source evidence, tests,
configuration, or explicitly marked inference.

## Required Behaviors

A Repo Memory-compliant repository must:

- treat `docs/` as the canonical source of truth for durable project context
- keep agent instruction files thin and linked to the docs set
- make `docs/project-overview.md` the canonical home for project goal, problem statement, target users or actors, success criteria, scope, and non-goals
- document current behavior from evidence before documenting assumptions
- document the users, actors, personas, journeys, acceptance paths, and edge cases that matter to user-facing or workflow-heavy systems
- document logging, metrics, traces, analytics events, audit events, alerts, dashboards, and privacy boundaries in `docs/observability-and-instrumentation.md`
- mark inferred, stale, superseded, deprecated, or unknown facts explicitly
- track feature work in `docs/feature-registry.md` and feature docs
- keep active feature docs resumable without prior chat history
- keep implementable plans in the owning feature or design doc, with provenance for the planner, tool, role or lens, inputs reviewed, assumptions, confidence, and next safe implementation step
- record specialist or second-agent reviews in a short owning-doc `Review Log`, or in `docs/reviews/<review-slug>.md` when the review is substantive, cross-cutting, or audit-worthy
- recover interrupted or crashed agent work by inspecting the working tree before editing, preserving uncommitted and untracked files until understood, and recording recovery evidence in the affected feature doc or doc-health record
- update decision and implementation logs when durable choices or landed work change
- update `docs/doc-health.md` when docs are created, verified, found stale, renamed, superseded, or materially changed
- use the standard status values and metadata fields where applicable

## Evidence Order

When docs disagree, resolve current behavior in this order:

1. source code, tests, schemas, runtime config, and deployment config
2. explicit user statements, ADRs, design docs, and code comments
3. existing docs, after checking whether they are stale
4. git history, changelogs, issues, and pull requests
5. clearly marked inference

Do not present inferred rationale as confirmed intent.

## Status Model

Feature docs and feature registry entries use these status values:

- `research`
- `planned`
- `in_progress`
- `blocked`
- `implemented`
- `verified`
- `shipped`
- `abandoned`
- `superseded`
- `deprecated`
- `rolled_back`

Do not invent new status values. Add detail in the feature doc when the state
needs explanation.

## Metadata

Maintained docs should include metadata that records:

- doc type
- owner
- status
- last updated date
- last verified date
- confidence
- canonical source
- related docs
- evidence
- plan or review provenance when applicable
- supersession or replacement state when relevant

The field names, allowed values, and required fields by doc type are defined in
[`references/documentation-metadata-schema.md`](./references/documentation-metadata-schema.md).

## Agent Entry Points

Agent-specific files should be short adapters.

They should tell the agent:

1. Read `docs/README.md`.
2. Read `docs/project-overview.md`, `docs/architecture.md`, and `docs/feature-registry.md`.
3. Read the active `docs/features/<feature-slug>.md` before changing related code.
4. Inspect `git status`, unstaged diffs, staged diffs, and untracked files before editing when resuming after an interruption or unknown prior agent state.
5. Update feature handoff notes, doc health, decision log, and implementation log when warranted.
6. Do not duplicate mutable project facts in the agent instruction file.
7. Do not create optional deep-dive folders unless there is real content to own.
8. Preserve useful custom docs and link them from the canonical docs layer.
9. Treat plan and review records as advisory evidence until verified against current code, docs, and user intent.

Platform guides in [`agents/`](./agents/) show how to adapt this flow for
Codex, Claude Code, GitHub Copilot, and OpenAI Agents SDK.

## Validation

The standard is designed to be easy to validate without a service.

This repository includes a lightweight validator:

```bash
python3 <skill-dir>/scripts/validate-docs.py --project-docs /path/to/repo
```

Validation should catch missing required docs, broken relative links, invalid
docs path names, and version drift in this standard repository. It also emits
warnings for likely hygiene issues such as generated artifacts, empty optional
deep-dive folders, invalid or stale feature status metadata, and stale
interrupted-work handoff text in terminal feature docs. Use `--strict` to treat
warnings as failures.

## Non-Goals

Repo Memory does not try to:

- replace `AGENTS.md`, `CLAUDE.md`, Copilot instructions, or editor memory files
- become a complete agent orchestration framework
- require a specific AI provider or IDE
- generate all documentation automatically without review
- force every project into the same documentation depth

The goal is a portable source of project truth that agents and humans can
trust, inspect, version, and improve.
