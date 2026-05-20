# Docs Structure Rules

Use these naming conventions and placement rules for the canonical Repo Memory
`docs/` layer. These rules apply once a repository chooses to adopt Repo Memory
for that maintained docs layer. They do not require rewriting every pre-existing
document on day one; useful existing docs can be preserved and linked during a
progressive adoption.

## Cross-Agent Source-of-Truth Rules

- Treat the `Canonical Ownership Map` in `docs/README.md` as the place that names the single owner for each adopted documentation capability.
- Treat the maintained `docs/` set as the canonical source of truth only for capabilities it owns. Existing ADRs, RFCs, runbooks, API specs, schemas, and security docs can remain canonical owners when the map says so.
- Do not create duplicate canonical owners. Link supporting docs instead of copying mutable decisions, contracts, commands, feature state, or handoff notes.
- Treat `docs/intake/` as raw source material when present, not as canonical truth. Promote accepted brainstorm, planning, or user-provided facts into the maintained docs before building from them.
- Keep agent-specific instruction files such as `AGENTS.md`, `.github/copilot-instructions.md`, `CLAUDE.md`, or similar repo entrypoints concise. They should point agents to the ownership map instead of restating mutable project facts.
- If multiple agent instruction files exist, keep them aligned to the same docs entrypoints and active feature-tracking workflow.
- Do not let important resume state live only in chat history. Put resumable state in `docs/features/<feature-slug>.md` and linked docs.

## Naming Conventions

### Folders

- Use **kebab-case** only: all lowercase letters, digits, and hyphens.
- No spaces, underscores, capital letters, dots, or special characters.
- Keep folder names short and descriptive.

| Allowed             | Not Allowed        |
| ------------------- | ------------------ |
| `feature-registry/` | `FeatureRegistry/` |
| `project-details/`  | `project_details/` |
| `ui-ux/`            | `UI-UX/`           |
| `auth-flow/`        | `authFlow/`        |

### Files

- Use **kebab-case** with the `.md` extension for all Markdown documentation files.
- No spaces, underscores, capital letters (except `README.md`, `_template.md`), or special characters.
- Feature slugs, component slugs, design slugs, and topic slugs must be consistent across the registry, file name, and folder name.

| Allowed                         | Not Allowed                   |
| ------------------------------- | ----------------------------- |
| `functional-requirements.md`    | `FunctionalRequirements.md`   |
| `local-development.md`          | `local_development.md`        |
| `answer-search-improvements.md` | `answerSearchImprovements.md` |
| `README.md`                     | `readme.md`                   |
| `_template.md`                  | `template.md`                 |

### Slugs

A **slug** is the shared identifier used as a folder name, file name, and registry key for features, components, designs, and project-detail topics.

Rules:

- Derive slugs from the feature or topic name using kebab-case.
- Use the same slug everywhere: in `docs/feature-registry.md`, as the feature file name (`<slug>.md`), and as the feature subfolder name (`<slug>/`).
- Do not change a slug after it is registered without updating every reference.
- Do not include version numbers or dates in slugs unless the topic is version-specific.

| Topic name                 | Correct slug                 |
| -------------------------- | ---------------------------- |
| Answer search improvements | `answer-search-improvements` |
| Order lifecycle            | `order-lifecycle`            |
| Multi-tenant routing       | `multi-tenant-routing`       |
| Session manager            | `session-manager`            |

## Default Folder and File Placement

### Continuity overlay

Every Level 1 continuity overlay should have these files unless the ownership
map names a different maintained owner:

```text
docs/
├── README.md             # includes Canonical Ownership Map
├── doc-health.md
├── feature-registry.md
└── features/
    └── <feature-slug>.md # when active or risky work needs handoff
```

### Baseline docs

For Level 2 baseline coverage, each capability must have an owner. Create these
default files directly in `docs/` only when no trustworthy existing owner
already satisfies that capability:

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

Do not place Repo Memory-created baseline docs in subfolders. Each default
baseline file must live directly in `docs/`. If an existing owner lives
elsewhere, link it from the ownership map instead of duplicating it.

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

| Folder                  | When to create                                                                    | Required index file              |
| ----------------------- | --------------------------------------------------------------------------------- | -------------------------------- |
| `docs/diagrams/`        | When diagram sources or exports are checked in                                    | `docs/diagrams/README.md`        |
| `docs/designs/`         | When significant designs or proposals need their own docs                         | `docs/designs/README.md`         |
| `docs/project-details/` | When domain workflows or integration quirks need deep treatment                   | `docs/project-details/README.md` |
| `docs/components/`      | When shared subsystems or components need behavior docs                           | `docs/components/README.md`      |
| `docs/reviews/`         | When substantive plan, specialist, or second-agent reviews need their own records | `docs/reviews/README.md`         |
| `docs/ui-ux/`           | When user journeys, interaction states, or accessibility need dedicated docs      | `docs/ui-ux/README.md`           |

Rules:

- Every optional subfolder must contain a `README.md` index listing all files in the folder.
- Files in optional subfolders must be linked from the owning baseline owner, feature doc, or index.
- Do not create partial optional subfolders (e.g., `docs/designs/` without `docs/designs/README.md`).
- Do not create an optional subfolder that contains only `README.md`; index-only optional folders are noise unless they point to existing assets or topic docs.
- `docs/intake/` is an allowed raw intake folder for brainstorms, project dumps, copied chat notes, imported plans, sketches, and planning-agent output. It is not a Repo Memory optional deep-dive folder. Raw intake files may keep source filenames and rough formatting; once content is accepted as durable project documentation, move or summarize it into the mapped owner and apply normal naming, metadata, link, and verification rules.
- `docs/superpowers/` is an allowed companion workflow folder for Obra Superpowers specs and plans. It is not a Repo Memory optional deep-dive folder and does not need a Repo Memory index unless the target project wants one.

## Content Placement Rules

Use this table to decide where any piece of content belongs by default:

Treat these as the default locations for Repo Memory-owned capabilities. If a repo
already has a strong doc in another location, preserve it first, then link or
migrate it deliberately instead of creating competing current-state summaries.

| Content type                                                                                            | Correct location                                                                                                                  |
| ------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| Project goal, problem statement, target users or actors, success criteria, scope, non-goals             | `docs/project-overview.md`                                                                                                        |
| Service boundaries, major modules, topology                                                             | `docs/architecture.md`                                                                                                            |
| APIs, schemas, MCP tools, CLI, contracts                                                                | `docs/interfaces-and-contracts.md`                                                                                                |
| Entities, relationships, lifecycle, storage                                                             | `docs/data-model.md`                                                                                                              |
| Setup, commands, scripts, codegen, fixtures                                                             | `docs/local-development.md`                                                                                                       |
| Doc freshness, verification state, known drift                                                          | `docs/doc-health.md`                                                                                                              |
| Logs, metrics, traces, analytics events, audit events, dashboards, alerts                               | `docs/observability-and-instrumentation.md`                                                                                       |
| Test strategy, coverage gaps, tools                                                                     | `docs/testing-strategy.md`                                                                                                        |
| Deploy, ops, runbooks, alerts, rollback                                                                 | `docs/operations-runbook.md`                                                                                                      |
| Auth, secrets, PII, threat model                                                                        | `docs/security-and-privacy.md`                                                                                                    |
| Durable technical choices with rationale                                                                | `docs/decision-log.md`                                                                                                            |
| What landed and when                                                                                    | `docs/implementation-log.md`                                                                                                      |
| All tracked features, their status, and the ranked next-work queue                                      | `docs/feature-registry.md`                                                                                                        |
| Raw brainstorms, copied chat notes, user-provided project dumps, sketches, and imported planning output | `docs/intake/`, then promote accepted outcomes into the mapped owner                                                              |
| Feature goal, status, checklist, handoff                                                                | `docs/features/<feature-slug>.md`                                                                                                 |
| Canonical resume state for interrupted work                                                             | `docs/features/<feature-slug>.md`                                                                                                 |
| Feature-local flows, edge cases, algorithms                                                             | `docs/features/<feature-slug>/logic.md`                                                                                           |
| Feature-local component behavior                                                                        | `docs/features/<feature-slug>/components/<component-slug>.md`                                                                     |
| Functional behaviors and acceptance criteria                                                            | `docs/requirements/functional-requirements.md`                                                                                    |
| Performance, scalability, compliance limits                                                             | `docs/requirements/non-functional-requirements.md`                                                                                |
| Actors, personas, user stories, journeys, alternative flows, failure states, acceptance paths           | `docs/requirements/user-stories-and-use-cases.md`                                                                                 |
| Diagram sources and exports                                                                             | `docs/diagrams/<topic-slug>.mmd` or `.drawio`                                                                                     |
| Proposed or adopted designs and tradeoffs                                                               | `docs/designs/<design-slug>.md`                                                                                                   |
| Domain rules, integration quirks too long for baseline                                                  | `docs/project-details/<topic-slug>.md`                                                                                            |
| Shared subsystem or component behavior                                                                  | `docs/components/<component-slug>.md`                                                                                             |
| Substantive specialist or second-agent review records                                                   | `docs/reviews/<review-slug>.md`                                                                                                   |
| Short plan or review provenance for one feature                                                         | `docs/features/<feature-slug>.md`                                                                                                 |
| Major plan, proposal, or rollout shape                                                                  | `docs/designs/<design-slug>.md`                                                                                                   |
| Companion workflow specs and plans                                                                      | `docs/superpowers/specs/<date>-<topic>.md` and `docs/superpowers/plans/<date>-<topic>.md`, linked from the owning Repo Memory doc |
| User journeys, screen states, accessibility                                                             | `docs/ui-ux/<topic-or-flow-slug>.md`                                                                                              |

## Metadata Rules

- Every maintained doc should include the common metadata fields from `documentation-metadata-schema.md`.
- Metadata should identify doc type, owner, status, last updated date, verification state, confidence, canonical source, and related docs.
- If metadata is unknown, write `unknown` instead of leaving the field blank.
- Feature metadata must use the same slug and status as `docs/feature-registry.md`.
- `docs/feature-registry.md` must include `Next Work Queue` and `Feature List` sections.
- The `Next Work Queue` must use `ready`, `verify-first`, `needs-human`, or `blocked` readiness values.
- Stale, superseded, deprecated, or rolled-back docs must include a replacement pointer or correction note.

## Canonical Ownership Map Rules

`docs/README.md` should include a `Canonical Ownership Map` table for every
Repo Memory Level 1 or higher adoption.

Minimum columns:

- `Capability`
- `Canonical owner`
- `Supporting docs`
- `Notes`

Rules:

- Each capability appears once.
- Each capability has exactly one canonical owner.
- Related or legacy docs go in `Supporting docs`, not in `Canonical owner`.
- If ownership is unknown, use `unknown` temporarily and record the question in doc health.
- If a default Repo Memory file only points to an existing owner, say so clearly.
- Do not copy mutable content from the owner into the pointer file.

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

| Status        | Meaning                                                   |
| ------------- | --------------------------------------------------------- |
| `research`    | Being investigated; no implementation started             |
| `planned`     | Scoped and ready; implementation not yet started          |
| `in_progress` | Actively being implemented                                |
| `blocked`     | Waiting on something external                             |
| `implemented` | Code landed; not yet verified end-to-end                  |
| `verified`    | Manually or automatically confirmed working               |
| `shipped`     | Released to users                                         |
| `abandoned`   | Work intentionally stopped without shipping               |
| `superseded`  | Replaced by another feature, design, or approach          |
| `deprecated`  | Still exists but should not be extended for new work      |
| `rolled_back` | Landed work was reverted or disabled after implementation |

Do not invent new status values. If a feature has a state not covered here, document the reason in the feature file under `Open Questions`.

## Rename and Supersession Rules

- Do not rename registered slugs unless the current name is misleading enough to hurt future work.
- When renaming, update the registry, owning doc, index files, diagrams, feature links, and agent instruction references in the same change.
- Record the previous slug in the relevant registry or index as `Formerly: <old-slug>` until the transition is clear.
- When replacing one feature, design, component, or diagram with another, keep the old doc and mark it `superseded`, `deprecated`, or `rolled_back` instead of deleting useful history.

## Prohibited Patterns

| Pattern                                                                      | Reason                                                                                                      |
| ---------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| Files named `notes.md`, `temp.md`, `todo.md` outside `docs/intake/`          | Not part of the maintained standard structure; use feature docs instead                                     |
| Folders named `misc/`, `old/`, `archive/`                                    | Use `decision-log.md` or `implementation-log.md` to record history instead                                  |
| Deep-dive docs with no link from an owner doc                                | Creates orphaned docs that agents cannot discover                                                           |
| Duplicate content across baseline and deep-dive docs                         | Baseline summarizes; deep-dive docs hold the detail                                                         |
| Duplicate canonical owners for one capability                                | Creates conflicting truth; use the ownership map to name one owner                                          |
| Empty optional deep-dive folders                                             | Delete them until there is real topic content to own                                                        |
| Slugs with uppercase letters, spaces, or underscores                         | Breaks consistency across registry, file names, and folder names                                            |
| Optional subfolders without a `README.md` index                              | Leaves the folder undiscoverable                                                                            |
| Plan or review findings left only in chat history                            | Future agents cannot verify who produced the advice, what evidence it used, or which outcomes were accepted |
| Accepted companion spec or plan outcomes left only under `docs/superpowers/` | Future agents may miss changed requirements, decisions, validation, or handoff state in mapped owners       |
| Accepted brainstorm or planning outcomes left only under `docs/intake/`      | Raw intake is easy to miss and may contain unaccepted assumptions                                           |
| Baseline docs placed in subfolders                                           | Baseline docs must live directly in `docs/`                                                                 |
| Mutable project facts duplicated across agent-specific instruction files     | Creates competing sources of truth and stale handoff state                                                  |
| Deleted feature/design history without a replacement pointer                 | Breaks continuity for future agents                                                                         |
| Renamed slugs without registry or index notes                                | Makes old links and prior handoffs hard to interpret                                                        |

## Enforcement Checklist

Before committing documentation changes, confirm:

- [ ] All folder names are kebab-case.
- [ ] All file names are kebab-case with `.md` extension (except `README.md` and `_template.md`).
- [ ] Slugs are consistent across `docs/feature-registry.md`, the feature file name, and any feature subfolder.
- [ ] `docs/README.md` has a `Canonical Ownership Map` with one owner per capability.
- [ ] Existing ADRs, RFCs, runbooks, API specs, security docs, and setup docs are linked as owners or supporting docs instead of duplicated.
- [ ] Every optional subfolder has a `README.md` index.
- [ ] No optional subfolder exists only as an empty index.
- [ ] Accepted facts from `docs/intake/` have been promoted into mapped owners, with unresolved high-impact questions recorded.
- [ ] Every deep-dive doc is linked from an owner doc, feature doc, or index.
- [ ] Substantive plan and review records include provenance and are linked from the owning feature, design, UI/UX, component, or baseline doc.
- [ ] Companion spec or plan artifacts that shaped work are linked from owning docs, with accepted outcomes promoted into mapped owners.
- [ ] No prohibited folder or file names are present.
- [ ] Status values in feature docs match the allowed set.
- [ ] Maintained docs include required metadata fields for their doc type.
- [ ] `docs/project-overview.md` includes project goal, problem statement, users or actors, success criteria, current scope, non-goals, and evidence.
- [ ] No baseline docs have been moved into subfolders.
- [ ] Agent-specific instruction files point to the ownership map instead of duplicating mutable project state.
- [ ] `docs/doc-health.md` is updated for material doc changes, known stale areas, and verification state.
- [ ] Renamed or superseded docs have replacement pointers in the relevant registry or index.
