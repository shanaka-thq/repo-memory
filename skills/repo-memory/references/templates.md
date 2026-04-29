# Project Documentation Templates

Use these templates when the repository does not already define a stronger format.

## Default Docs Structure

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
├── diagrams/                       # optional diagram sources and exports
│   ├── README.md
│   ├── <topic-slug>.mmd
│   ├── <topic-slug>.drawio
│   └── exports/
│       └── <topic-slug>.svg
├── designs/                        # optional design docs and proposals
│   ├── README.md
│   └── <design-slug>.md
├── project-details/                # optional project-specific deep dives
│   ├── README.md
│   └── <topic-slug>.md
├── components/                     # optional shared subsystem or component docs
│   ├── README.md
│   └── <component-slug>.md
├── ui-ux/                          # optional user journeys, states, accessibility notes
│   ├── README.md
│   └── <topic-or-flow-slug>.md
├── requirements/
│   ├── functional-requirements.md
│   ├── non-functional-requirements.md
│   └── user-stories-and-use-cases.md  # required for user-facing or workflow-heavy systems
└── features/
    ├── _template.md
    ├── <feature-slug>.md
    └── <feature-slug>/             # optional feature deep-dive folder
        ├── logic.md
        └── components/
            └── <component-slug>.md
```

For existing projects, use the baseline files as the comprehensive minimum and populate every file with concise current-state content before polishing any single document too much.

The `docs/diagrams/`, `docs/designs/`, `docs/project-details/`, `docs/components/`, `docs/ui-ux/`, and per-feature deep-dive folders are optional. Add them when the codebase has maintained diagrams, design decisions, project-specific behavior, user-flow complexity, or feature or component logic that another agent would otherwise have to reverse-engineer.

## Empty Repository Scaffold

Use the scaffold helper when a target repository has no useful implementation
or documentation evidence yet:

```bash
python3 <skill-dir>/scripts/scaffold-docs.py /path/to/repo --with-agents
```

Resolve `<skill-dir>` to the installed `repo-memory` skill directory. When
working from this repository root, use `skills/repo-memory/scripts/...`.

The scaffold creates the required baseline docs, `docs/requirements/`,
`docs/features/_template.md`, initial decision and implementation log entries,
and a doc-health note that marks the placeholders as unverified. Add
`--include-user-stories` when users, actors, journeys, or acceptance paths are
already known. Use `--project-name "<name>"` when the target directory name is
not the right project name.

After scaffolding, replace TODOs only with confirmed facts, user statements, or
clearly marked inference. Keep unknowns explicit until implementation evidence
exists.

## Common Metadata Block

Use this block near the top of maintained docs. See [documentation-metadata-schema.md](./documentation-metadata-schema.md) for allowed values and doc-type-specific fields.

```md
Doc type:
Owner:
Status:
Last updated:
Last verified:
Verified against:
Confidence:
Canonical source:
Related docs:
```

## Agent Instruction Snippet Template

Use this snippet in repo-level instruction files such as `AGENTS.md`, `.github/copilot-instructions.md`, `CLAUDE.md`, or similar agent entrypoints when the target repo should treat the `docs/` folder as the canonical source of truth.

```md
## Documentation Source of Truth

This project uses the `docs/` folder as the canonical source of truth for architecture, requirements, feature status, implementation history, and cross-agent handoff state.

When starting or resuming work:
1. Read `docs/README.md`.
2. Read `docs/project-overview.md` and `docs/architecture.md`.
3. Read `docs/feature-registry.md` and the active `docs/features/<feature-slug>.md` before making changes.

When making changes:
- Update the active feature doc as the work changes.
- Put durable project facts in `docs/`, not only in agent-specific instruction files or chat history.
- Keep any agent-specific instruction files short and aligned to the same docs entrypoints.

Before stopping:
- Update `docs/features/<feature-slug>.md`, especially `Implementation Status`, `Validation`, `Resume Context`, `Next Agent Handoff`, and `Exact Next Prompt` when present.
- Update `docs/implementation-log.md` for meaningful landed work.
- Update `docs/decision-log.md` when a durable technical choice changed.
```

## Deep-Dive Placement Rules

- Use `docs/requirements/user-stories-and-use-cases.md` for actors, user stories, end-to-end use cases, alternative flows, and acceptance paths in user-facing or workflow-heavy projects.
- Use `docs/local-development.md` for local setup, scripts, tooling, fixtures, codegen, local services, and contributor troubleshooting.
- Use `docs/observability-and-instrumentation.md` for logs, metrics, traces, analytics events, audit events, dashboards, alerts, retention, sampling, and known blind spots.
- Use `docs/diagrams/` for maintained `.mmd`, `.drawio`, exported SVG or PNG assets, and diagram indexes.
- Use `docs/designs/` for substantial designs, proposals, rollout plans, tradeoffs, and future-evolution notes.
- Use `docs/project-details/` for domain workflows, business rules, integration quirks, deployment-specific behavior, or repo-specific conventions.
- Use `docs/components/` for shared subsystems, reusable UI components, state containers, orchestration layers, or services that span multiple features.
- Use `docs/ui-ux/` for user journeys, screens or surfaces, interaction states, accessibility requirements, content notes, or responsive rules.
- Use `docs/features/<feature-slug>/logic.md` for feature-local flows, state transitions, algorithms, edge cases, or event sequencing.
- Use `docs/features/<feature-slug>/components/` when the component logic only matters inside that feature and would be noise in the shared component registry.
- Always link deep-dive docs from the parent feature doc, index, or relevant baseline doc.

## Diagram Guidance

- Prefer Mermaid fenced blocks inside Markdown docs for small and medium diagrams that are easiest to review beside the prose.
- Prefer standalone `.mmd` files in `docs/diagrams/` when the diagram is large, shared, or reused across multiple docs.
- Preserve existing `.drawio` files when the team uses visual editing or when the diagram is not practical to maintain as Mermaid.
- Keep exported `.svg` or `.png` artifacts only when the repo already relies on rendered diagram assets or the Markdown target needs them.
- Link every maintained diagram from an owning doc such as `docs/architecture.md`, a design doc, a feature doc, or `docs/diagrams/README.md`.
- When Mermaid is used, prefer an explicit `init` block so the diagram remains readable even when the Markdown renderer does not provide shared theming.

## Default Mermaid Theme Snippet

````md
```mermaid
%%{init: {
  "theme": "base",
  "themeVariables": {
    "background": "#fffdf8",
    "primaryColor": "#1f6feb",
    "primaryTextColor": "#0b1220",
    "primaryBorderColor": "#174ea6",
    "lineColor": "#475467",
    "secondaryColor": "#e8f1ff",
    "tertiaryColor": "#f6f8fb",
    "clusterBkg": "#f8fafc",
    "clusterBorder": "#98a2b3",
    "fontFamily": "system-ui, sans-serif",
    "fontSize": "14px"
  }
}}%%
flowchart TD
  A["Start"] --> B["Next Step"]
```
````

This default favors accessibility and readability: a light background, high-contrast text, restrained accent color, and readable font settings.

If the Markdown environment supports a shared theme, align Mermaid to that theme. If not, keep Mermaid self-contained with the `init` block.

## Feature Registry Template

```md
# Feature Registry

| Feature | Slug | Status | Priority | Last updated | Notes |
| --- | --- | --- | --- | --- | --- |
| Answer search improvements | `answer-search-improvements` | `in_progress` | High | 2026-04-22 | [Feature doc](./features/answer-search-improvements.md), [Logic](./features/answer-search-improvements/logic.md) |
```

Allowed statuses: `research`, `planned`, `in_progress`, `blocked`, `implemented`, `verified`, `shipped`, `abandoned`, `superseded`, `deprecated`, `rolled_back`.

## Decision Log Entry Template

Use this shape for comprehensive decision logs:

```md
## DL-000: Decision Title

Status: implemented
Confidence: high | medium | low

Decision: State the durable choice clearly.

Rationale: Explain why it was chosen. If the original rationale is not confirmed, mark it as inferred or unknown.

Evidence: Cite source files, tests, docs, config, user statements, commits, or other artifacts.

Consequences:

- Practical implication 1.
- Practical implication 2.
```

Decision logs should cover foundational project choices, architecture, integrations, data contracts, UI/UX, testing, operations, security, docs workflow, and explicit scope deferrals. See [decision-log-reconstruction.md](./decision-log-reconstruction.md) for the full checklist.

## Project Overview Template

Use this template for `docs/project-overview.md`. This document owns the durable "why" of the project, so keep the goal, problem, users, success criteria, scope, and non-goals explicit.

```md
# Project Overview

Doc type: project-overview
Owner: current-agent-or-team
Status: active
Last updated: 2026-04-28
Last verified: unknown
Verified against: unknown
Confidence: medium
Canonical source: `docs/project-overview.md`
Related docs: `architecture.md`, `requirements/functional-requirements.md`, `requirements/user-stories-and-use-cases.md`

## Project Goal

State the outcome this project is trying to achieve.

## Problem Statement

Describe the user, business, developer, or operational problem this project exists to solve.

## Target Users or Actors

| User or actor | Goal | Notes |
| --- | --- | --- |
| Primary user | What they need to accomplish | Relevant constraints or context |
| Admin or operator | What they need to manage | Relevant permissions or responsibilities |

## Success Criteria

- Observable result 1
- User or operational outcome 1
- Quality or reliability bar 1

## Current Scope

- Capability 1
- Capability 2

## Non-Goals

- Explicitly excluded scope 1
- Explicitly deferred scope 1

## Evidence

- Source files, tests, product notes, user statements, or other artifacts that support this overview.

## Open Questions

- Unknown or unverified product context that future agents should not assume.
```

## Feature Doc Template

```md
# Feature: answer-search-improvements

Doc type: feature
Feature slug: answer-search-improvements
Status: in_progress
Owner: current-agent-or-team
Priority: High
Last updated: 2026-04-22
Last verified: unknown
Verified against: unknown
Confidence: medium
Canonical source: `docs/features/answer-search-improvements.md`
Related docs: `../feature-registry.md`
Validation status: implementation in progress
Next safe step: continue from `Next Agent Handoff`

## Goal

State the user problem and intended outcome.

## Research Summary

- Summarize what was investigated.
- Note rejected options only if they affect future work.

## Decision

- Record the chosen approach and why.

## Scope

In:
- What this feature covers

Out:
- What it does not cover

## User Impact

- Affected actor or persona:
- Main use case or journey:
- Important UX states:

## Supporting Docs

- Detailed logic: `./answer-search-improvements/logic.md`
- Related shared component: `../components/search-results-panel.md`
- Related UX doc: `../ui-ux/search-results-experience.md`
- Related design doc: `../designs/answer-search-architecture.md`

## Edge Cases and Failure Modes

- Edge case 1
- Failure mode 1

## Implementation Status

- [x] API response shape defined
- [x] backend implementation started
- [ ] frontend wiring complete
- [ ] tests updated
- [ ] docs updated
- [ ] manual verification complete

## Files Touched

- `src/...`
- `dashboard/src/...`

## Open Questions

- Question 1
- Question 2

## Validation

- Tests run
- Manual checks
- Remaining verification gaps

## Change Governance

- Last verified:
- Verified against:
- Docs updated:
- Decision log impact:
- Implementation log impact:
- Conflicts or stale docs found:
- Supersedes or replaces:

## Resume Context

- Canonical docs to read first:
- Files or directories to inspect first:
- Last known good state:
- Known blockers or constraints:
- Interrupted work recovery:
  - Workspace state checked:
  - Unexpected modified, staged, or untracked files:
  - Recovery evidence:
  - Preserved or unresolved changes:

## Next Agent Handoff

- Done:
- Next safe step:
- Risks:
- Validation status:
- Inspect first:
- Active owner:
- Avoid parallel changes in:
- Safe to parallelize:
- Avoid changing:
- If recovering from interruption: run `git status --short`, inspect diffs and untracked files, then record what was found before editing.

## Exact Next Prompt

Continue implementing answer-search-improvements. Read this feature doc first, then inspect `src/...` and `dashboard/src/...`. Finish the frontend wiring, add tests for fallback behavior, and update docs before stopping.
```

## User Stories and Use Cases Template

```md
# User Stories and Use Cases

Doc type: user-stories-and-use-cases
Owner: current-agent-or-team
Status: active
Last updated: 2026-04-28
Last verified: unknown
Verified against: unknown
Confidence: medium
Canonical source: `docs/requirements/user-stories-and-use-cases.md`
Related docs: `../project-overview.md`, `functional-requirements.md`, `../ui-ux/README.md`

## Actors

| Actor | Primary goal | Permissions or constraints | Related journeys |
| --- | --- | --- | --- |
| Analyst | Find relevant answers quickly | Authenticated dashboard user | Search, inspect result |
| Admin | Audit and tune answer quality | Advanced controls | Review low-confidence results |

## Personas or User Segments

| Persona or segment | Context | Needs | Risks |
| --- | --- | --- | --- |
| Primary persona | Where and why they use the system | Outcome they need | Failure or confusion risk |

## User Stories

- As an analyst, I want the best matching answers first so that I can respond faster.
- As an admin, I want to inspect low-confidence results so that I can tune the system.

## Journey Map

| Journey | Actor | Start state | Desired outcome | Related docs |
| --- | --- | --- | --- | --- |
| Search for an answer | Analyst | Needs a response | Finds a relevant answer | `../ui-ux/search-results-experience.md` |

## Primary Use Cases

### Use Case: Search for an answer

Actor: Analyst
Preconditions:
- User is authenticated
- Search index is available

Main flow:
1. User enters a query.
2. System returns ranked answers.
3. User opens a result for more detail.

Alternative flows:
- No results found
- Search service degraded
- User lacks permission

Failure states:
- Query validation fails
- Search backend times out
- Result data is stale or incomplete

Acceptance notes:
- Results should show ranking rationale when available
- Empty, loading, and error states must be clear
- Permission and privacy boundaries must be visible where relevant

Instrumentation notes:
- Track search request count, no-result rate, timeout rate, and result-open events when product analytics are allowed.

## Accessibility and Inclusion Notes

- Keyboard or assistive technology expectations
- Language, contrast, or interaction constraints

## Open Questions

- User behavior, permission boundary, or acceptance detail that still needs evidence
```

## Local Development Template

```md
# Local Development and Tooling

## Prerequisites

- Runtime versions
- Package manager
- Local services or containers

## First-Time Setup

1. Install dependencies
2. Configure environment variables
3. Start required local services
4. Seed or sync local data if needed

## Core Commands

- Install:
- Dev server:
- Test:
- Lint:
- Typecheck:
- Build:
- Format:

## Tooling Map

- Codegen:
- Storybook or component preview:
- Mocks or fixtures:
- Task runner or scripts:

## Local Services and Data

- Database:
- Cache or queue:
- Third-party service stubs:

## Troubleshooting

- Common failure 1
- Common failure 2
```

## Observability and Instrumentation Template

Use this template for `docs/observability-and-instrumentation.md`. This document owns the runtime and product signals that explain whether the system is healthy, usable, and diagnosable.

```md
# Observability and Instrumentation

Doc type: observability-and-instrumentation
Owner: current-agent-or-team
Status: active
Last updated: 2026-04-28
Last verified: unknown
Verified against: unknown
Confidence: medium
Canonical source: `docs/observability-and-instrumentation.md`
Related docs: `operations-runbook.md`, `security-and-privacy.md`, `requirements/non-functional-requirements.md`

## Goals

- What operators, maintainers, or product owners need to understand from runtime signals.

## Logs

| Signal | Source | Purpose | Retention or privacy notes |
| --- | --- | --- | --- |
| Request log | API gateway or app server | Diagnose request failures | Do not log secrets or sensitive payloads |

## Metrics

| Metric | Source | Purpose | Alert or dashboard |
| --- | --- | --- | --- |
| Request error rate | API service | Detect degraded behavior | Operations dashboard |

## Traces

- Trace boundaries, sampled operations, spans, or known gaps.

## Product Analytics Events

| Event | Trigger | Properties | Privacy notes |
| --- | --- | --- | --- |
| `search_submitted` | User submits search | query length, result count | Do not store raw sensitive query text unless explicitly allowed |

## Audit Events

- Security, compliance, permission, or administrative events that must be recorded.

## Dashboards and Alerts

- Dashboard:
- Alert:
- Escalation path:

## Privacy and Retention

- PII or sensitive-data handling:
- Sampling:
- Retention:
- Access controls:

## Known Blind Spots

- Signal gap 1
- Unverified production behavior 1

## Related Code and Config

- `src/...`
- deployment, logging, tracing, analytics, or monitoring config
```

## Doc Health Template

Use this template for `docs/doc-health.md` in target repos that adopt the standard.

```md
# Documentation Health

This file tracks freshness, verification evidence, known drift, conflicts, and renamed or superseded docs.

## Health Summary

Last full audit:
Current overall confidence: high | medium | low
Known stale areas:
Open doc conflicts:

## Verification Matrix

| Doc | Last verified | Verified against | Confidence | Known drift or action |
| --- | --- | --- | --- | --- |
| `architecture.md` | 2026-04-28 | `src/`, deployment config, tests | high | None |
| `data-model.md` | 2026-04-28 | schemas, migrations, storage code | medium | Confirm production retention rules |

## Conflicts and Corrections

| Date | Conflict | Resolution | Evidence |
| --- | --- | --- | --- |
| 2026-04-28 | Legacy README described old deployment target | `operations-runbook.md` updated to current target | deploy config |

## Renames and Supersessions

| Old slug or doc | New slug or doc | Status | Notes |
| --- | --- | --- | --- |
| `legacy-search.md` | `answer-search-improvements.md` | superseded | New feature doc owns active work |
```

## Architecture Change Governance Template

Use this block inside a design doc, feature doc, implementation log entry, or doc-health correction note when a material architecture or contract change needs explicit lifecycle tracking.

```md
## Architecture Change Record

Date:
Change summary:
Reason:
Affected docs:
Affected code or contracts:
Migration or compatibility notes:
Rollback or recovery notes:
Validation performed:
Decision log entry:
Implementation log entry:
Doc-health update:
```

## Diagrams Index Template

```md
# Diagrams

Use this folder for maintained diagram sources and rendered exports that support architecture, design, workflow, sequence, or state documentation.

## Diagram Inventory

| Diagram | Format | Owner doc | Notes |
| --- | --- | --- | --- |
| `system-context.mmd` | Mermaid source | `../architecture.md` | Canonical architecture context diagram |
| `search-flow.drawio` | Draw.io source | `../designs/answer-search-architecture.md` | Visual editing retained for cross-team updates |
| `exports/search-flow.svg` | Rendered asset | `../designs/answer-search-architecture.md` | Used by Markdown target that cannot render Mermaid |

## Diagram Rules

- Prefer Mermaid in Markdown for text-centric, reviewable diagrams.
- Preserve `.drawio` when the repo already depends on visual editing.
- Keep sources and exports together, and link them from the owning docs.
```

## Designs Index Template

```md
# Design Docs

Use this folder for substantial designs, proposals, or adopted solution shapes that need goals, tradeoffs, rollout notes, and future-evolution context.

| Design | Purpose | Status |
| --- | --- | --- |
| `answer-search-architecture.md` | Documents the ranking pipeline redesign | `adopted` |
| `notifications-delivery.md` | Proposes a new delivery flow | `proposed` |
```

## Design Doc Template

```md
# Design: answer-search-architecture

Status: adopted
Owner: codex
Last updated: 2026-04-23

## Problem

Describe the problem this design addresses.

## Goals

- Goal 1
- Goal 2

## Non-Goals

- Non-goal 1

## Current State

Summarize the current implementation or limitation.

## Proposed Design

Describe the chosen structure, flow, and major interfaces.

## Alternatives Considered

- Alternative 1 and why it was rejected

## Tradeoffs

- Tradeoff 1

## Rollout and Migration

- Step 1
- Step 2

## Future Evolution

- Expected extension points
- Compatibility or deprecation notes

## Related Docs

- `../architecture.md`
- `../decision-log.md`
- `../diagrams/README.md`
```

## Project Details Index Template

```md
# Project Details

Use this folder for project-specific deep-dive documentation that is too detailed for the baseline docs but important for future implementation and maintenance.

| Topic | Purpose | Owner doc |
| --- | --- | --- |
| `order-lifecycle.md` | Describes the end-to-end order workflow and business rules | `../architecture.md` |
| `multi-tenant-routing.md` | Documents routing and tenant resolution behavior | `../interfaces-and-contracts.md` |
```

## Components Index Template

```md
# Components and Subsystems

Use this folder for shared component or subsystem deep dives that cut across features and would otherwise be hard to reconstruct from code alone.

| Component | Purpose | Owner doc |
| --- | --- | --- |
| `search-results-panel.md` | Documents state, rendering rules, and interaction behavior for the shared results panel | `../architecture.md` |
| `session-manager.md` | Explains session ownership, refresh logic, and cleanup rules | `../security-and-privacy.md` |
```

## Project Detail Template

```md
# Project Detail: order-lifecycle

Owner doc: `../architecture.md`
Last updated: 2026-04-22

## Purpose

Explain why this topic needs deeper documentation.

## Context

- Where this logic appears in the system
- Which teams, services, or features depend on it

## Detailed Behavior

Describe the workflow, rules, and branches in enough detail that another agent can change it safely.

## Invariants and Assumptions

- Business rule 1
- Operational constraint 1

## Edge Cases and Failure Modes

- Edge case 1
- Failure mode 1

## Related Code

- `src/...`
- `services/...`

## Related Docs

- `../architecture.md`
- `../requirements/functional-requirements.md`
```

## Shared Component Logic Template

```md
# Component Logic: search-results-panel

Owner doc: `../architecture.md`
Last updated: 2026-04-22

## Purpose

Explain why this component or subsystem needs its own logic doc.

## Responsibilities

- Responsibility 1
- Responsibility 2

## Inputs and Outputs

- Inputs:
- Outputs:

## State and Lifecycle

Describe initialization, updates, teardown, or other state transitions.

## Rules and Invariants

- Invariant 1
- Invariant 2

## Edge Cases

- Edge case 1
- Edge case 2

## Failure Modes

- Failure mode 1

## Related Code

- `src/...`
- `ui/...`

## Related Docs

- `../architecture.md`
- `../features/answer-search-improvements.md`
```

Reuse this template for `docs/features/<feature-slug>/components/<component-slug>.md` when the component logic is feature-local instead of shared.

## UI and UX Index Template

```md
# UI and UX

Use this folder for user journeys, screen or surface behavior, interaction rules, accessibility notes, and responsive requirements that should stay aligned with implementation.

| Topic | Purpose | Owner doc |
| --- | --- | --- |
| `search-results-experience.md` | Defines search result states, ranking presentation, and keyboard behavior | `../requirements/user-stories-and-use-cases.md` |
| `settings-flow.md` | Documents the settings journey and permissions-related states | `../features/settings.md` |
```

## UI and UX Doc Template

```md
# UI and UX: search-results-experience

Owner doc: `../features/answer-search-improvements.md`
Last updated: 2026-04-23

## User Goal

Describe what the user is trying to achieve.

## Surfaces

- Page, panel, modal, or component involved

## Main Flow

Describe the expected interaction flow.

## States

- Empty
- Loading
- Success
- Error
- Permission denied

## Interaction Rules

- Keyboard behavior
- Focus behavior
- Selection behavior

## Accessibility

- Screen reader requirements
- Contrast or semantics notes

## Responsive Behavior

- Mobile behavior
- Desktop behavior

## Related Code

- `src/...`
- `ui/...`

## Related Docs

- `../requirements/user-stories-and-use-cases.md`
- `../features/answer-search-improvements.md`
- `../diagrams/README.md`
```

## Feature Logic Template

```md
# Feature Logic: answer-search-improvements

Feature doc: `../answer-search-improvements.md`
Last updated: 2026-04-22

## Purpose

Describe the logic that is too detailed for the main feature doc.

## Entry Points

- API route, page, event, CLI command, job, or user action

## Main Flow

Describe the happy-path sequence.

## Branches and State Transitions

- Branch 1
- Branch 2

## Rules and Edge Cases

- Rule 1
- Edge case 1
- Failure mode 1

## Dependencies

- Service or module 1
- Config or flag 1

## Validation

- Tests that cover this logic
- Gaps that still need coverage

## Related Code

- `src/...`
- `dashboard/src/...`

## Open Questions

- Question 1
```

## Docs README Template

```md
# Documentation Standard

This folder is the engineering source of truth for how the project works, what contracts exist, what decisions have been made, what work is in progress, and where detailed project or component logic is documented.

## Agent Startup Order

When an agent starts or resumes work:

1. Read this file.
2. Read `project-overview.md` and `architecture.md`.
3. Read `feature-registry.md`.
4. Read the active `features/<feature-slug>.md` before making changes to that feature.

## Single Source of Truth Rules

- Keep durable project facts and active handoff state in this `docs/` tree.
- Keep repo-level agent instruction files concise and point them here instead of duplicating mutable facts.
- If multiple agent instruction files exist, align them to the same docs entrypoints and feature workflow.

## Always Maintain

- `project-overview.md`
- `architecture.md`
- `requirements/functional-requirements.md`
- `requirements/non-functional-requirements.md`
- `interfaces-and-contracts.md`
- `data-model.md`
- `local-development.md`
- `doc-health.md`
- `observability-and-instrumentation.md`
- `testing-strategy.md`
- `operations-runbook.md`
- `security-and-privacy.md`
- `decision-log.md`
- `implementation-log.md`
- `feature-registry.md`

## Optional Deep Dives

Create these only when the topic needs more detail than the baseline set should hold:

- `requirements/user-stories-and-use-cases.md`
- `diagrams/<topic-slug>.mmd`
- `diagrams/<topic-slug>.drawio`
- `designs/<design-slug>.md`
- `project-details/<topic-slug>.md`
- `components/<component-slug>.md`
- `ui-ux/<topic-or-flow-slug>.md`
- `features/<feature-slug>/logic.md`
- `features/<feature-slug>/components/<component-slug>.md`

## Per-feature Maintenance

For non-trivial work, create or update:

- `features/<feature-slug>.md`
- `requirements/user-stories-and-use-cases.md` when user journeys or acceptance paths changed
- `diagrams/...` when architecture views, flows, or state diagrams changed
- `ui-ux/...` when screen states, interaction rules, or accessibility changed
- `designs/...` when the solution shape or rollout plan changed materially
- linked deep-dive docs when the feature has meaningful internal logic
- `doc-health.md` when docs were materially changed, verified, stale, renamed, or superseded
- `implementation-log.md`
- `decision-log.md` when the change is architectural
```

## Existing Project Audit Snippet

```md
## Documentation Audit

| Target doc | Evidence source | Confidence | Gaps |
| --- | --- | --- | --- |
| `architecture.md` | `src/`, runtime config, deploy files | High | no explicit scaling rationale |
| `local-development.md` | package scripts, Makefile, setup docs | High | seed-data workflow unclear |
| `doc-health.md` | current docs, code evidence, recent changes | Medium | full audit not yet completed |
| `observability-and-instrumentation.md` | logging config, telemetry code, dashboards, alert config | Medium | production retention unknown |
| `requirements/user-stories-and-use-cases.md` | product notes, UI tests, support docs | Medium | admin use cases incomplete |
| `diagrams/system-context.mmd` | architecture docs, service boundaries, deploy files | High | queue edges not yet shown |
| `decision-log.md` | legacy docs, commits, comments | Medium | some rationale inferred |
| `designs/answer-search-architecture.md` | RFC notes, recent commits, architecture comments | Medium | rollout plan only partially documented |
| `project-details/order-lifecycle.md` | workflow services, tests, ops notes | Medium | failure handling still inferred |
| `components/search-results-panel.md` | UI state code, component tests | High | accessibility rationale missing |
| `diagrams/search-flow.drawio` | design workshop artifact, implementation notes | Medium | Mermaid equivalent not maintained |
| `ui-ux/search-results-experience.md` | design mocks, component stories, browser checks | Medium | mobile behavior not fully documented |
| `security-and-privacy.md` | env config, auth middleware, infra docs | Medium | production posture unclear |
```

## Session-Close Checklist

Before ending a session, confirm:

1. The feature doc status is current.
2. The checklist reflects reality.
3. Files touched are listed.
4. Blockers and risks are explicit.
5. The next step is written for another agent, not just for yourself.
6. The implementation log is updated if meaningful work landed.
7. The decision log is updated if a lasting technical choice changed.
8. Inferred statements and missing rationale are explicitly marked.
9. Any deep-dive docs are linked from their parent feature doc, index, or baseline doc.
10. Tricky project or component logic is documented in the repo, not stranded in chat history.
11. Local tooling changes are reflected in `local-development.md`.
12. Runtime signals, product analytics, audit events, dashboards, and alerts are reflected in `observability-and-instrumentation.md`.
13. User-facing changes update user stories, use cases, and UI or UX docs when relevant.
14. Diagram sources are preserved and linked, not replaced casually with screenshots or chat-only sketches.
15. Any agent-specific instruction files still point to these docs as the canonical source of truth.
16. `doc-health.md` records material doc changes, stale docs, conflicts, renames, and verification state.
