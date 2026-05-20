# Repo Memory Portable Standard

Version: 2.1.0 <!-- x-release-please-version -->

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
- a ranked next-work queue so cloud agents can choose the next safe task without prior chat context
- raw brainstorms, project dumps, user notes, and planning output as intake evidence before accepted facts are promoted
- provenance for substantial plans, specialist reviews, and tool-generated guidance that influence implementation
- compatibility with companion spec/plan workflows, when accepted outcomes are promoted into mapped owners
- documentation freshness, conflicts, renames, and verification evidence

The standard is intentionally plain Markdown plus optional validation. A repo
can adopt it without choosing a particular AI provider, editor, plugin, or
agent framework.

Repo Memory is also meant to coexist with strong existing repository
documentation. A team does not need to delete useful ADRs, RFCs, architecture
notes, wiki pages, runbooks, OpenAPI specs, security docs, changelogs, or agent
entrypoints to use it. The important move is to make each durable documentation
capability have exactly one canonical owner, then link supporting material into
that owner instead of letting mutable project truth fragment across tools.

Strict no-duplicate ownership is part of the standard. Repo Memory standardizes
the missing memory roles a repo needs; it does not force duplicate files when an
existing world-standard document already owns that role.

## Standard Components

A Repo Memory adoption has five layers:

1. A canonical ownership map that names the single owner for each documentation capability.
2. Canonical project docs, which may be Repo Memory files or existing repo-standard docs.
3. Thin agent entrypoints that point agents to the canonical owners.
4. Metadata and status values that make docs consistent across tools.
5. A continuity process for keeping docs verified, current, and resumable.

The standard does not require an agent runtime. Platform-specific integrations
are adapters around the docs, not replacements for them.

## Conformance Levels

Use these levels to describe how fully a repository has adopted the standard.

Level 0 is valid. Adoption is optional. The levels matter when a repo wants to
describe how far it has gone toward Repo Memory conformance, not as a claim
that every repository must adopt the full baseline immediately.

| Level | Name               | Requirement                                                                                                                                                                        |
| ----- | ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 0     | Not adopted        | No maintained Repo Memory docs set exists.                                                                                                                                         |
| 1     | Continuity overlay | A canonical ownership map exists, no duplicate canonical owners are introduced, thin agent entrypoints point to the map, and the repo has shared handoff surfaces for active work. |
| 2     | Baseline coverage  | All baseline capabilities have canonical owners, satisfied either by existing repo-standard docs or Repo Memory docs.                                                              |
| 3     | Verified           | Baseline coverage plus metadata, verification dates, confidence, evidence links, no-duplicate ownership checks, and validator checks in local workflow or CI.                      |
| 4     | Integrated         | Verified plus aligned agent entrypoints and optional platform adapters, CLI, plugin, or MCP integration.                                                                           |

A useful open source or production repo should aim for Level 2 or Level 3.
Level 4 is optional and tool-specific.

## Progressive Adoption

Existing repositories can adopt Repo Memory progressively before they claim
Level 2 baseline coverage.

A practical transition often looks like this:

1. preserve useful existing docs and agent entrypoints
2. create or update a canonical ownership map
3. add the missing shared-state surfaces first, usually `docs/README.md`,
   `docs/feature-registry.md`, `docs/doc-health.md`, and active feature docs
4. link older but still useful docs from the ownership map
5. expand to baseline coverage when the repo needs stricter continuity,
   verification, or cross-agent coordination

Level 1 is intentionally small. It should make a repo resumable without forcing
teams to migrate healthy ADRs, RFCs, runbooks, API specs, or security docs.

## No Duplicate Ownership

Every durable documentation capability must have one canonical owner.

A duplicate owner is created when two maintained files both claim to be the
current source of truth for the same mutable project fact, decision, contract,
workflow, or handoff state.

Allowed:

- one canonical owner plus links from supporting docs
- a lightweight index that points to the canonical owner
- a deprecated or superseded doc with a replacement pointer
- temporary migration notes that clearly say which owner wins

Not allowed:

- copying ADR rationale into a second decision log as current truth
- restating OpenAPI, GraphQL, protobuf, or schema contracts in another doc as the canonical contract
- keeping build commands in both `README.md` and `docs/local-development.md` without naming one owner
- storing feature status, blockers, or next steps in both an agent instruction file and a feature doc
- letting `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md`, or OpenCode rules become separate mutable project manuals

If a repo already has a world-standard owner, use it. Repo Memory only adds a
file when no trusted owner exists or when cross-agent continuity needs a small
handoff surface.

## Baseline Capabilities and Canonical Owners

A repo claiming Repo Memory Level 2 or higher has owners for these baseline
capabilities. The default owner is the Repo Memory path to create when the repo
does not already have a trustworthy owner.

| Capability                            | Default owner when missing                  | Existing docs that can satisfy it                                                                            |
| ------------------------------------- | ------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| Documentation map and ownership map   | `docs/README.md`                            | Existing docs index, contributor handbook                                                                    |
| Project goal, users, scope, non-goals | `docs/project-overview.md`                  | Product brief, README, PRD                                                                                   |
| Architecture and system shape         | `docs/architecture.md`                      | Architecture notes, C4 docs, diagrams, RFCs                                                                  |
| Decisions and rationale               | `docs/decision-log.md`                      | ADR folder, RFC archive, decision records                                                                    |
| Interfaces and contracts              | `docs/interfaces-and-contracts.md`          | OpenAPI, AsyncAPI, protobuf, GraphQL schema, MCP docs, CLI docs                                              |
| Data model                            | `docs/data-model.md`                        | Schema files, ERD docs, migration docs                                                                       |
| Local development and tooling         | `docs/local-development.md`                 | README setup, CONTRIBUTING, Makefile docs                                                                    |
| Testing strategy                      | `docs/testing-strategy.md`                  | Test docs, CI docs, quality handbook                                                                         |
| Operations and runbooks               | `docs/operations-runbook.md`                | Runbooks, SRE docs, deploy docs                                                                              |
| Security and privacy                  | `docs/security-and-privacy.md`              | `SECURITY.md`, threat model, compliance docs                                                                 |
| Observability and instrumentation     | `docs/observability-and-instrumentation.md` | Telemetry docs, dashboard docs, analytics specs                                                              |
| Implementation history                | `docs/implementation-log.md`                | CHANGELOG, release notes, migration history                                                                  |
| Feature registry and next work queue  | `docs/feature-registry.md`                  | Usually missing; can be an existing roadmap or issue board if it is maintained in-repo and agent-readable    |
| Active feature handoff                | `docs/features/<feature-slug>.md`           | Usually missing; can be a maintained feature brief if it includes status, validation, and next-agent handoff |
| Documentation health and conflicts    | `docs/doc-health.md`                        | Usually missing; can be an existing documentation health/audit record                                        |

The canonical ownership map should name the owner for each adopted capability
and list supporting docs separately. Supporting docs may contain useful context,
but they do not own mutable truth unless the map names them as the owner.

When no existing owner exists, the full Repo Memory default layout is:

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

Optional and special-purpose docs are added only when they serve a clear intake,
workflow, or deep-dive need:

- `docs/intake/`
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

Repos may also contain companion workflow artifacts such as Obra Superpowers
specs and plans in `docs/superpowers/specs/` and `docs/superpowers/plans/`.
These are allowed as linked evidence and provenance, but they are not Repo
Memory baseline docs and do not replace the owning feature, design,
requirements, decision, implementation, or doc-health records.

Useful pre-existing docs may remain outside this exact baseline during a
transition, provided the canonical ownership map links to them clearly and does
not leave current mutable project state stranded outside a named owner.

## Empty Repository Bootstrap

An empty or nearly empty repository can adopt Repo Memory before implementation
exists. In that case, create the default baseline docs and ownership map as a
skeleton, mark project-specific facts as `TODO` or `unknown`, and record in
`docs/doc-health.md` that the initial docs are placeholders that still need
evidence.

The skill package includes a scaffold helper:

```bash
python3 <skill-dir>/scripts/scaffold-docs.py /path/to/repo --with-agents
```

Resolve `<skill-dir>` to the directory that contains `SKILL.md`. When working
from this repository root, use `skills/repo-memory/scripts/...`.

The skeleton is a starting state, not verified project truth. Replace
placeholders only with confirmed user statements, source evidence, tests,
configuration, or explicitly marked inference.

## Raw Intake Folder

Repos may keep `docs/intake/` as a low-friction inbox for unstructured source
material that could shape the project:

- brainstorm dumps
- copied chat notes or user-provided project dumps
- sketches, screenshots, imported plans, or planning-agent output
- rough product, architecture, or feature notes that are not yet accepted

`docs/intake/` is source evidence, not canonical project truth. Before building
from intake material, agents should extract accepted facts into the relevant
mapped baseline, requirements, feature, design, decision, implementation, and
doc-health owners. High-impact missing foundations should be clarified with the
user; lower-risk unknowns should be recorded in `Open Questions`.

Raw intake files may keep source filenames and rough formatting. Validation may
ignore naming and link hygiene inside `docs/intake/` because the folder is not a
maintained ownership layer. Once content is curated as durable documentation, move or
summarize it into the mapped owner and apply normal Repo Memory naming,
metadata, link, and verification rules.

## Required Behaviors

When a repository claims Repo Memory Level 1 or higher conformance, it must:

- maintain a canonical ownership map that says where each adopted capability lives
- avoid duplicate canonical owners for the same mutable project fact, decision, contract, or handoff state
- keep agent instruction files thin and linked to the ownership map and active handoff surfaces
- review relevant `docs/intake/` source material before greenfield planning or implementation, then promote accepted outcomes into mapped owners
- use existing standard docs as canonical owners when they already satisfy a capability
- make the mapped project-overview owner the canonical home for project goal, problem statement, target users or actors, success criteria, scope, and non-goals
- document current behavior from evidence before documenting assumptions
- document the users, actors, personas, journeys, acceptance paths, and edge cases that matter to user-facing or workflow-heavy systems
- document logging, metrics, traces, analytics events, audit events, alerts, dashboards, and privacy boundaries in the mapped observability owner
- mark inferred, stale, superseded, deprecated, or unknown facts explicitly
- track feature work and the ranked next-work queue in the mapped feature registry owner
- make the first ready row in the feature registry the default next task when a user asks an agent to pick up the next repo task
- keep active feature docs resumable without prior chat history
- keep implementable plans in the owning feature or design doc, with provenance for the planner, tool, role or lens, inputs reviewed, assumptions, confidence, and next safe implementation step
- link companion spec or plan artifacts from the owning Repo Memory doc when another workflow materially shaped the work, then promote accepted outcomes into mapped owners
- record specialist or second-agent reviews in a short owning-doc `Review Log`, or in `docs/reviews/<review-slug>.md` when the review is substantive, cross-cutting, or audit-worthy
- recover interrupted or crashed agent work by inspecting the working tree before editing, preserving uncommitted and untracked files until understood, and recording recovery evidence in the affected feature doc or doc-health record
- update the mapped decision and implementation owners when durable choices or landed work change
- update the mapped doc-health owner when docs are created, verified, found stale, renamed, superseded, or materially changed
- use the standard status values and metadata fields where applicable

## Evidence Order

When docs disagree, resolve current behavior in this order:

1. source code, tests, schemas, runtime config, and deployment config
2. explicit user statements, ADRs, design docs, and code comments
3. raw intake files, copied planning notes, and companion artifacts, after checking whether their content was accepted or is only advisory
4. existing docs, after checking whether they are stale
5. git history, changelogs, issues, and pull requests
6. clearly marked inference

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

## Next Work Queue

`docs/feature-registry.md` owns the ranked next-work queue. Use it when a
human or cloud agent asks what should be picked up next.

The queue should include:

- `Rank`
- `Work item`
- `Type`
- `Status`
- `Ready`
- `Why next`
- `Next safe step`
- `Canonical doc`
- `Last verified`

Use these readiness values:

- `ready`: safe for an agent to implement from the linked canonical doc
- `verify-first`: inspect or validate current code and docs before editing
- `needs-human`: product, scope, or priority direction is missing
- `blocked`: known dependency, failing state, or unresolved conflict prevents progress

When no task is assigned, agents should choose the lowest-rank `ready` row. If
no row is ready, they should perform verification only for `verify-first` rows
or ask for human direction for `needs-human` and `blocked` rows.

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

1. Read `docs/README.md` or the repo's canonical ownership map.
2. Read the mapped project overview, architecture, and feature registry owners.
3. Review `docs/intake/` when it exists and contains raw brainstorms, project notes, or planning output relevant to the work.
4. Promote accepted intake outcomes into the mapped owner before building from them.
5. If no specific task was assigned, choose the lowest-rank `ready` item in the feature registry `Next Work Queue`; if none is ready, verify only `verify-first` items or ask for human input on `needs-human` or `blocked` items.
6. Read the active `docs/features/<feature-slug>.md` before changing related code.
7. Inspect `git status`, unstaged diffs, staged diffs, and untracked files before editing when resuming after an interruption or unknown prior agent state.
8. Update the mapped feature registry queue, feature handoff notes, doc health, decision history, and implementation history when warranted.
9. Do not duplicate mutable project facts in the agent instruction file.
10. Do not create optional deep-dive folders unless there is real content to own.
11. Preserve useful custom docs and link them from the ownership map.
12. Treat plan and review records as advisory evidence until verified against current code, docs, and user intent.

Platform guides in [`agents/`](./agents/) show how to adapt this flow for
Codex, Claude Code, GitHub Copilot, and OpenAI Agents SDK.
Use [`references/agent-integration-and-enforcement.md`](./references/agent-integration-and-enforcement.md)
for cloud, VS Code, OpenCode, Claude Code, Copilot, hook, and CI setup guidance.

## Validation

The standard is designed to be easy to validate without a service.

This repository includes a lightweight validator:

```bash
python3 <skill-dir>/scripts/validate-docs.py --project-docs /path/to/repo --adoption-level continuity
```

Validation should catch missing docs for the selected adoption level, broken
relative links, invalid docs path names, duplicate canonical ownership entries,
and version drift in this standard repository. It also emits warnings for
likely hygiene issues such as generated artifacts, empty optional deep-dive
folders, invalid or stale feature status metadata, malformed next-work queue
readiness values, and stale interrupted-work handoff text in terminal feature
docs. Raw files under
`docs/intake/` are exempt from naming and relative-link checks because they are
source material, not maintained mapped owners. Use `--strict` to treat warnings
as failures.

## Non-Goals

Repo Memory does not try to:

- replace `AGENTS.md`, `CLAUDE.md`, Copilot instructions, or editor memory files
- replace useful existing ADRs, RFCs, architecture notes, or team docs just to match a new filename
- duplicate canonical owners for facts already owned by healthy existing docs
- become a complete agent orchestration framework
- require a specific AI provider or IDE
- generate all documentation automatically without review
- force every project into the same documentation depth

The goal is a portable source of project truth that agents and humans can
trust, inspect, version, and improve.
