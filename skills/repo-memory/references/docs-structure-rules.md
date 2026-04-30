# Docs Structure Rules

Strict naming conventions and placement rules for the `docs/` folder. These rules apply to every repository that adopts the Repo Memory portable standard. Agents and contributors must follow these rules when creating or moving files.

## Cross-Agent Source-of-Truth Rules

- Treat the maintained `docs/` set as the canonical source of truth for architecture, requirements, feature state, implementation history, and handoff context.
- Keep agent-specific instruction files such as `AGENTS.md`, `.github/copilot-instructions.md`, `CLAUDE.md`, or similar repo entrypoints concise. They should point agents to the canonical docs instead of restating mutable project facts.
- If multiple agent instruction files exist, keep them aligned to the same docs entrypoints and active feature-tracking workflow.
- Do not let important resume state live only in chat history. Put resumable state in `docs/features/<feature-slug>.md` and linked docs.

## Naming Conventions

### Folders

- Use **kebab-case** only: all lowercase letters, digits, and hyphens.
- No spaces, underscores, capital letters, dots, or special characters.
- Keep folder names short and descriptive.

| Allowed | Not Allowed |
| --- | --- |
| `feature-registry/` | `FeatureRegistry/` |
| `project-details/` | `project_details/` |
| `ui-ux/` | `UI-UX/` |
| `auth-flow/` | `authFlow/` |

### Files

- Use **kebab-case** with the `.md` extension for all Markdown documentation files.
- No spaces, underscores, capital letters (except `README.md`, `_template.md`), or special characters.
- Feature slugs, component slugs, design slugs, and topic slugs must be consistent across the registry, file name, and folder name.

| Allowed | Not Allowed |
| --- | --- |
| `functional-requirements.md` | `FunctionalRequirements.md` |
| `local-development.md` | `local_development.md` |
| `answer-search-improvements.md` | `answerSearchImprovements.md` |
| `README.md` | `readme.md` |
| `_template.md` | `template.md` |

### Slugs

A **slug** is the shared identifier used as a folder name, file name, and registry key for features, components, designs, and project-detail topics.

Rules:

- Derive slugs from the feature or topic name using kebab-case.
- Use the same slug everywhere: in `docs/feature-registry.md`, as the feature file name (`<slug>.md`), and as the feature subfolder name (`<slug>/`).
- Do not change a slug after it is registered without updating every reference.
- Do not include version numbers or dates in slugs unless the topic is version-specific.

| Topic name | Correct slug |
| --- | --- |
| Answer search improvements | `answer-search-improvements` |
| Order lifecycle | `order-lifecycle` |
| Multi-tenant routing | `multi-tenant-routing` |
| Session manager | `session-manager` |

## Required Folder and File Placement

### Baseline docs

Every compliant project must have these files directly in `docs/`:

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
└── feature-registry.md
```

Do not place baseline docs in subfolders. Each baseline file must live directly in `docs/`.

### Requirements subfolder

```text
docs/requirements/
├── functional-requirements.md
├── non-functional-requirements.md
└── user-stories-and-use-cases.md   # optional; add when the project has meaningful actors or journeys
```

### Required project overview sections

`docs/project-overview.md` must include these sections:

- `Project Goal`
- `Problem Statement`
- `Target Users or Actors`
- `Success Criteria`
- `Current Scope`
- `Non-Goals`
- `Evidence`

Use `Open Questions` when project intent, user context, or success criteria are not fully verified.

### Features subfolder

```text
docs/features/
├── _template.md                    # copy this when creating a new feature doc
├── <feature-slug>.md               # one file per tracked feature
└── <feature-slug>/                 # optional deep-dive folder; use only when needed
    ├── logic.md
    └── components/
        └── <component-slug>.md
```

Rules:

- The feature file (`<feature-slug>.md`) must exist before any deep-dive subfolder is created.
- Deep-dive subfolders must be linked from the parent feature file.
- Do not create `docs/features/<feature-slug>/` without a corresponding `docs/features/<feature-slug>.md`.

### Optional deep-dive subfolders

Create these only when baseline docs cannot hold the detail without becoming unreadable:

| Folder | When to create | Required index file |
| --- | --- | --- |
| `docs/diagrams/` | When diagram sources or exports are checked in | `docs/diagrams/README.md` |
| `docs/designs/` | When significant designs or proposals need their own docs | `docs/designs/README.md` |
| `docs/project-details/` | When domain workflows or integration quirks need deep treatment | `docs/project-details/README.md` |
| `docs/components/` | When shared subsystems or components need behavior docs | `docs/components/README.md` |
| `docs/ui-ux/` | When user journeys, interaction states, or accessibility need dedicated docs | `docs/ui-ux/README.md` |

Rules:

- Every optional subfolder must contain a `README.md` index listing all files in the folder.
- Files in optional subfolders must be linked from the owning baseline doc, feature doc, or index.
- Do not create partial optional subfolders (e.g., `docs/designs/` without `docs/designs/README.md`).
- Do not create an optional subfolder that contains only `README.md`; index-only optional folders are noise unless they point to existing assets or topic docs.

## Content Placement Rules

Use this table to decide where any piece of content belongs:

| Content type | Correct location |
| --- | --- |
| Project goal, problem statement, target users or actors, success criteria, scope, non-goals | `docs/project-overview.md` |
| Service boundaries, major modules, topology | `docs/architecture.md` |
| APIs, schemas, MCP tools, CLI, contracts | `docs/interfaces-and-contracts.md` |
| Entities, relationships, lifecycle, storage | `docs/data-model.md` |
| Setup, commands, scripts, codegen, fixtures | `docs/local-development.md` |
| Doc freshness, verification state, known drift | `docs/doc-health.md` |
| Logs, metrics, traces, analytics events, audit events, dashboards, alerts | `docs/observability-and-instrumentation.md` |
| Test strategy, coverage gaps, tools | `docs/testing-strategy.md` |
| Deploy, ops, runbooks, alerts, rollback | `docs/operations-runbook.md` |
| Auth, secrets, PII, threat model | `docs/security-and-privacy.md` |
| Durable technical choices with rationale | `docs/decision-log.md` |
| What landed and when | `docs/implementation-log.md` |
| All tracked features and their status | `docs/feature-registry.md` |
| Feature goal, status, checklist, handoff | `docs/features/<feature-slug>.md` |
| Canonical resume state for interrupted work | `docs/features/<feature-slug>.md` |
| Feature-local flows, edge cases, algorithms | `docs/features/<feature-slug>/logic.md` |
| Feature-local component behavior | `docs/features/<feature-slug>/components/<component-slug>.md` |
| Functional behaviors and acceptance criteria | `docs/requirements/functional-requirements.md` |
| Performance, scalability, compliance limits | `docs/requirements/non-functional-requirements.md` |
| Actors, personas, user stories, journeys, alternative flows, failure states, acceptance paths | `docs/requirements/user-stories-and-use-cases.md` |
| Diagram sources and exports | `docs/diagrams/<topic-slug>.mmd` or `.drawio` |
| Proposed or adopted designs and tradeoffs | `docs/designs/<design-slug>.md` |
| Domain rules, integration quirks too long for baseline | `docs/project-details/<topic-slug>.md` |
| Shared subsystem or component behavior | `docs/components/<component-slug>.md` |
| User journeys, screen states, accessibility | `docs/ui-ux/<topic-or-flow-slug>.md` |

## Metadata Rules

- Every maintained doc should include the common metadata fields from `documentation-metadata-schema.md`.
- Metadata should identify doc type, owner, status, last updated date, verification state, confidence, canonical source, and related docs.
- If metadata is unknown, write `unknown` instead of leaving the field blank.
- Feature metadata must use the same slug and status as `docs/feature-registry.md`.
- Stale, superseded, deprecated, or rolled-back docs must include a replacement pointer or correction note.

## Diagram File Rules

- Mermaid source files: use `.mmd` extension.
- Draw.io source files: use `.drawio` extension.
- Rendered exports: use `.svg` or `.png` extension inside `docs/diagrams/exports/`.
- Embedded Mermaid blocks inside Markdown files do not need a separate `.mmd` file unless the diagram is large or shared.

```text
docs/diagrams/
├── README.md
├── <topic-slug>.mmd
├── <topic-slug>.drawio
└── exports/
    └── <topic-slug>.svg
```

## Status Values

Feature docs and feature registry entries must use one of these status values exactly:

| Status | Meaning |
| --- | --- |
| `research` | Being investigated; no implementation started |
| `planned` | Scoped and ready; implementation not yet started |
| `in_progress` | Actively being implemented |
| `blocked` | Waiting on something external |
| `implemented` | Code landed; not yet verified end-to-end |
| `verified` | Manually or automatically confirmed working |
| `shipped` | Released to users |
| `abandoned` | Work intentionally stopped without shipping |
| `superseded` | Replaced by another feature, design, or approach |
| `deprecated` | Still exists but should not be extended for new work |
| `rolled_back` | Landed work was reverted or disabled after implementation |

Do not invent new status values. If a feature has a state not covered here, document the reason in the feature file under `Open Questions`.

## Rename and Supersession Rules

- Do not rename registered slugs unless the current name is misleading enough to hurt future work.
- When renaming, update the registry, owning doc, index files, diagrams, feature links, and agent instruction references in the same change.
- Record the previous slug in the relevant registry or index as `Formerly: <old-slug>` until the transition is clear.
- When replacing one feature, design, component, or diagram with another, keep the old doc and mark it `superseded`, `deprecated`, or `rolled_back` instead of deleting useful history.

## Prohibited Patterns

| Pattern | Reason |
| --- | --- |
| Files named `notes.md`, `temp.md`, `todo.md` | Not part of the standard structure; use feature docs instead |
| Folders named `misc/`, `old/`, `archive/` | Use `decision-log.md` or `implementation-log.md` to record history instead |
| Deep-dive docs with no link from an owner doc | Creates orphaned docs that agents cannot discover |
| Duplicate content across baseline and deep-dive docs | Baseline summarizes; deep-dive docs hold the detail |
| Empty optional deep-dive folders | Delete them until there is real topic content to own |
| Slugs with uppercase letters, spaces, or underscores | Breaks consistency across registry, file names, and folder names |
| Optional subfolders without a `README.md` index | Leaves the folder undiscoverable |
| Baseline docs placed in subfolders | Baseline docs must live directly in `docs/` |
| Mutable project facts duplicated across agent-specific instruction files | Creates competing sources of truth and stale handoff state |
| Deleted feature/design history without a replacement pointer | Breaks continuity for future agents |
| Renamed slugs without registry or index notes | Makes old links and prior handoffs hard to interpret |

## Enforcement Checklist

Before committing documentation changes, confirm:

- [ ] All folder names are kebab-case.
- [ ] All file names are kebab-case with `.md` extension (except `README.md` and `_template.md`).
- [ ] Slugs are consistent across `docs/feature-registry.md`, the feature file name, and any feature subfolder.
- [ ] Every optional subfolder has a `README.md` index.
- [ ] No optional subfolder exists only as an empty index.
- [ ] Every deep-dive doc is linked from an owner doc, feature doc, or index.
- [ ] No prohibited folder or file names are present.
- [ ] Status values in feature docs match the allowed set.
- [ ] Maintained docs include required metadata fields for their doc type.
- [ ] `docs/project-overview.md` includes project goal, problem statement, users or actors, success criteria, current scope, non-goals, and evidence.
- [ ] No baseline docs have been moved into subfolders.
- [ ] Agent-specific instruction files point to the canonical docs instead of duplicating mutable project state.
- [ ] `docs/doc-health.md` is updated for material doc changes, known stale areas, and verification state.
- [ ] Renamed or superseded docs have replacement pointers in the relevant registry or index.
