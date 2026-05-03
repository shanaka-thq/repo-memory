# Existing Project Audit

Use this reference when a repository already exists but does not follow the documentation standard, or when you need to reconstruct missing docs from code and history.

## Goal

Build a comprehensive baseline of project documentation from evidence, without inventing unsupported rationale, then add targeted deep-dive docs for project-specific logic, user-facing behavior, local tooling, observability, diagrams, and component logic where the baseline is not enough. Record freshness, conflicts, stale areas, and verification evidence in `docs/doc-health.md`.

## Evidence Order

Prefer evidence in this order:

1. source code, tests, schemas, and config
2. setup, build, CI, deployment, and runtime files
3. current documentation in the repo
4. git history, changelog, release notes, issues, or PR references when available
5. user statements or prior chat summaries

## Audit Workflow

### 1. Inventory the repo

Capture:

- entrypoints and app boundaries
- main packages, services, or apps
- project goal, problem statement, target users or actors, success criteria, scope, and non-goals
- persistence layers and schemas
- domain workflows, business rules, and non-obvious operational flows
- actors, personas, user journeys, and use cases when the system has end users
- exposed interfaces such as APIs, CLIs, MCP tools, jobs, webhooks, events
- state machines, orchestration paths, queue or job behavior, and UI state flows
- local setup files, package scripts, Makefiles, task runners, codegen, fixtures, mocks, and developer tooling
- instrumentation and runtime signals such as logs, metrics, traces, analytics events, audit events, dashboards, alerts, retention rules, and known blind spots
- agent entrypoint files such as `AGENTS.md`, `.github/copilot-instructions.md`, `CLAUDE.md`, or other agent-specific repo instructions
- design artifacts such as RFCs, planning docs, issue threads, diagrams, or rollout notes
- diagram sources and assets such as `.mmd`, `.mermaid`, `.drawio`, `.drawio.svg`, `.svg`, and `.png`
- accessibility, responsive behavior, and key UI states when the system has a UI
- extension points, compatibility boundaries, migrations, feature flags, or deprecation paths that affect future evolution
- durable decisions across project foundation, architecture, integrations, contracts, UI, testing, operations, security, docs, and product scope
- test suites and what they imply about intended behavior
- operational artifacts such as Docker, CI, deploy config, and setup scripts
- existing docs and whether they are current, stale, or partial
- raw intake material such as brainstorms, copied chat notes, user-provided project dumps, or planning-agent output under `docs/intake/`
- companion workflow artifacts such as Obra Superpowers specs and plans under `docs/superpowers/`
- whether agent-specific instruction files duplicate mutable project knowledge that should instead live in the canonical docs set
- stale docs, conflicting docs, renamed docs, superseded work, and verification gaps that should be captured in `docs/doc-health.md`

### 2. Map the standard docs to evidence

For each target document, identify:

- primary evidence sources
- confidence level
- missing areas

Use a simple coverage matrix:

```md
| Target doc | Evidence source | Confidence | Gaps |
| --- | --- | --- | --- |
| `docs/architecture.md` | `src/`, `docker-compose.yml`, deployment config | High | no explicit scaling notes |
| `docs/local-development.md` | package scripts, Makefile, setup docs | High | fixture reset flow unclear |
| `docs/doc-health.md` | current docs, audit evidence, recent changes | Medium | full verification incomplete |
| `docs/observability-and-instrumentation.md` | logging config, telemetry code, alert config | Medium | production retention unknown |
| `docs/requirements/user-stories-and-use-cases.md` | UI tests, support notes, product docs | Medium | admin flows incomplete |
| `docs/diagrams/system-context.mmd` | architecture docs, service map, deploy config | High | async edges unclear |
| `docs/decision-log.md` | ADRs, commit history, comments | Medium | weak rationale for storage choice |
| `docs/designs/notifications-delivery.md` | RFC notes, issue history, architecture comments | Medium | rollout plan incomplete |
| `docs/reviews/notifications-product-review.md` | review notes, PR comments, feature doc | Medium | accepted outcomes not fully mapped |
| `docs/project-details/order-lifecycle.md` | workflow services, tests, release notes | Medium | refund edge cases only partially confirmed |
| `docs/components/session-manager.md` | auth code, UI state container, tests | High | no explicit cleanup rationale |
| `docs/diagrams/checkout-flow.drawio` | workshop artifact, browser checks, support notes | Medium | Markdown-linked export missing |
| `docs/ui-ux/checkout-flow.md` | mocks, browser checks, component stories | Medium | mobile states not fully confirmed |
| `docs/testing-strategy.md` | `tests/`, CI, package scripts | High | no performance tests |
```

Confidence labels should be simple:

- `high`
- `medium`
- `low`

### 3. Identify dedicated doc candidates

Look for logic that does not fit cleanly in the baseline set but would matter during implementation:

- user stories, actors, or end-to-end use cases that are not captured in the functional requirements alone
- local setup or tooling behavior that would otherwise stay trapped in scripts or tribal knowledge
- instrumentation behavior that would otherwise stay scattered across logging, analytics, tracing, monitoring, alerting, and audit code
- doc freshness, stale areas, conflicts, renamed docs, superseded work, or verification gaps that require `docs/doc-health.md`
- maintained diagrams that explain architecture, flows, or state better than prose alone
- design docs needed to preserve tradeoffs, rollout intent, or future evolution
- UI or UX docs needed to preserve flows, states, accessibility, or responsive behavior
- project-specific workflows or domain rules
- shared component or subsystem behavior
- feature-only state transitions, edge cases, or algorithms
- deployment or integration quirks that are too detailed for the runbook alone

For each candidate, record:

- proposed doc path
- owner doc or related feature
- evidence sources
- whether the current repo already documents it well enough
- whether the source format should remain Mermaid, Draw.io, or both
- whether any agent-specific instruction files should be reduced to lightweight pointers into the canonical docs set
- whether a doc-health entry is required because the source is stale, conflicting, renamed, superseded, or only partially verified

### 4. Separate facts from rationale

Use this distinction:

- current behavior: what the system does now
- implementation history: what changed and when
- decision rationale: why a durable choice was made

Do not upgrade implementation facts into decision rationale without evidence.

When updating the decision log, do not stop at recent choices. Reconstruct all durable decisions visible in the project from start to current state, add a confidence score to each entry, and mark rationale as explicit, inferred, or unknown.

### 5. Extract decisions carefully

A decision-log entry is justified when there is evidence of:

- a durable technical choice
- a meaningful tradeoff
- an intentional policy or workflow
- a chosen approach among alternatives
- a foundational project choice such as framework, starter/template, deployment target, package manager, folder structure, validation strategy, state management, integration style, UI system, testing approach, security posture, documentation workflow, or scoped deferral

Evidence may come from:

- ADRs
- code comments or docs that explain the tradeoff
- commit messages
- PR or issue references when available
- repeated architecture patterns that clearly imply an intentional standard
- explicit user statements describing project history or rationale

If rationale is weak but the current choice matters, document it like this:

- record the system shape in `architecture.md`
- record the landed change in `implementation-log.md`
- add the decision-log entry with confidence `medium` or `low`, and note that the rationale is inferred or incomplete

### 6. Backfill feature state

For existing projects, create or update feature docs when:

- work is actively in progress
- a recent change is central to current behavior
- a subsystem is complex enough that another agent needs handoff context
- a partially implemented feature may be resumed later

Sources for retrospective feature docs:

- recent commits
- changed files
- tests added or updated
- config flags
- migrations
- changelog or release notes

When the feature logic is complex, also create or update:

- `docs/features/<feature-slug>/logic.md`
- `docs/features/<feature-slug>/components/<component-slug>.md`
- `docs/components/<component-slug>.md` when the behavior is shared across features
- `docs/diagrams/...` when architecture, sequence, state, or flow diagrams materially help
- `docs/ui-ux/<topic-or-flow-slug>.md` when the user-facing behavior is important and detailed
- `docs/designs/<design-slug>.md` when the feature introduced a significant design or rollout plan
- `docs/reviews/<review-slug>.md` when a plan, specialist review, or second-agent critique materially shaped implementation and needs provenance
- `docs/doc-health.md` when feature state, linked docs, or verification evidence changed materially

If companion specs or plans exist under `docs/superpowers/`, link them from the
owning feature or design doc and promote accepted outcomes into canonical Repo
Memory docs instead of duplicating whole artifacts.

If raw intake exists under `docs/intake/`, review it before planning or
implementation, then promote accepted user statements, decisions, requirements,
feature ideas, constraints, and unresolved high-impact questions into the owning
canonical docs. Leave unaccepted or speculative intake as source material.

When feature work stopped or changed direction, use terminal statuses instead of deleting history:

- `abandoned`
- `superseded`
- `deprecated`
- `rolled_back`

### 7. Record uncertainty explicitly

When evidence is incomplete, prefer wording like:

- `Current behavior confirmed from tests and handlers.`
- `Rationale inferred from module structure and supporting comments.`
- `Original tradeoff not fully documented.`
- `Operational assumptions based on local setup artifacts; production posture unknown.`

This keeps the docs honest and still useful.

## Minimum Comprehensive Baseline

For an existing project, do not consider the documentation pass complete until the standard set exists and each file has at least a concise baseline of current known state:

- project overview
- architecture
- functional requirements
- non-functional requirements
- interfaces and contracts
- data model
- local development and tooling
- doc health
- observability and instrumentation
- testing strategy
- operations runbook
- security and privacy
- decision log
- implementation log
- feature registry

Feature docs are then added for active, recent, or important work.

For user-facing or workflow-heavy systems, also add user stories and use cases with actors, personas or user segments, primary journeys, alternative flows, failure states, permissions, accessibility considerations, and acceptance notes.

Add deep-dive docs for any design, diagram, UI or UX behavior, project-specific workflow, shared subsystem, or feature logic that another agent would otherwise have to infer from scattered code.
