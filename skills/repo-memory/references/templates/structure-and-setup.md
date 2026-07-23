# Project Documentation Templates

Use these templates when the repository does not already define a stronger format.

> **Canonical definitions:** Field names, allowed status values, and metadata schemas are defined in [STANDARD.md](../../STANDARD.md) and [documentation-metadata-schema.md](../documentation-metadata-schema.md). These templates show example usage — defer to those files when definitions differ.

## Default Docs Structure

```text
docs/
├── README.md
├── intake/                         # raw brainstorms, project dumps, and planning output
│   └── README.md
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
├── reviews/                        # optional review records
│   ├── README.md
│   └── <review-slug>.md
├── ui-ux/                          # optional user journeys, states, accessibility notes
│   ├── README.md
│   └── <topic-or-flow-slug>.md
├── superpowers/                     # optional companion workflow artifacts
│   ├── specs/
│   │   └── <date>-<topic>.md
│   └── plans/
│       └── <date>-<topic>.md
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

For existing projects, start with the capability owners the repo already has.
Use the baseline files as defaults only for capabilities with no trustworthy
existing owner.

## Partial Adoption Pattern for Existing Repos

When a repo already has useful architecture notes, ADRs, RFCs, wiki pages, or
team-specific runbooks, keep them if they still help. Do not force an immediate
rewrite just to match the full baseline.

The usual minimal add-first set is:

- `docs/README.md` to define the canonical ownership map
- `docs/feature-registry.md` to track active work and the next ready task
- `docs/doc-health.md` to record freshness, conflicts, and verification state
- `docs/features/<feature-slug>.md` for active or risky work that needs resumable handoff
- a thin repo-level agent entrypoint that points into the ownership map

That partial setup improves cross-agent continuity immediately. Expand toward
the full baseline when the repo needs stronger standardization or verification.

## Canonical Ownership Map Template

Use this in `docs/README.md` for any Level 1 or higher adoption. It prevents
Repo Memory from duplicating ADRs, runbooks, API specs, setup docs, or other
healthy existing documentation.

```md
## Canonical Ownership Map

| Capability                          | Canonical owner                   | Supporting docs                    | Notes                                                            |
| ----------------------------------- | --------------------------------- | ---------------------------------- | ---------------------------------------------------------------- |
| Documentation map and ownership map | `docs/README.md`                  | `AGENTS.md`                        | This table owns routing, not all project facts.                  |
| Decisions and rationale             | `docs/adr/`                       | `docs/decision-log.md`             | ADRs are canonical; decision log links or indexes only.          |
| Interfaces and contracts            | `openapi.yaml`                    | `docs/interfaces-and-contracts.md` | OpenAPI is canonical; prose explains usage and gaps.             |
| Local development and tooling       | `CONTRIBUTING.md`                 | `README.md`                        | Do not duplicate setup commands elsewhere.                       |
| Active feature handoff              | `docs/features/<feature-slug>.md` | `docs/feature-registry.md`         | Repo Memory owns resumable feature state.                        |
| Documentation health and conflicts  | `docs/doc-health.md`              | None                               | Tracks stale docs, duplicate-owner migrations, and verification. |
```

### Artifact Locations (Typed Slots)

Add this section below the Canonical Ownership Map when the repo uses workflow
skills that produce durable artifacts. It tells agents where each category of
artifact lands — skill-agnostic, path-based.

```md
## Artifact Locations

<!-- Where durable artifacts from workflow skills land.
     Update when you install new skills or change conventions. -->

| Category   | Location                  | Example producers                 |
| ---------- | ------------------------- | --------------------------------- |
| Plans      | `plans/`                  | /writing-plans, /improve          |
| Specs      | `.kiro/specs/`            | Kiro specs, /to-spec              |
| Tickets    | GitHub Issues             | /to-tickets, /triage, /wayfinder  |
| ADRs       | `docs/adr/`              | /grill-with-docs, /domain-modeling |
| Reviews    | PR comments               | /code-review                      |
| Handoff    | `docs/features/`          | Repo Memory (native)              |
| Research   | `research/` branches      | /research, /improve               |
| Additional | —                         | —                                 |
```

Not every slot needs a value. Fill only what the repo actually uses. The
Bootstrapper mode asks about each category during first-time setup.

See [compatible-skills.md](../compatible-skills.md) for the full list of known
integrations and future-proofing guidance.

Each capability should appear once. Put alternatives, legacy docs, and detail
sources in `Supporting docs`, not in `Canonical owner`.

The `docs/diagrams/`, `docs/designs/`, `docs/project-details/`, `docs/components/`, `docs/reviews/`, `docs/ui-ux/`, and per-feature deep-dive folders are optional. Add them when the codebase has maintained diagrams, design decisions, project-specific behavior, substantive reviews, user-flow complexity, or feature or component logic that another agent would otherwise have to reverse-engineer. Do not create empty optional folders or index-only optional folders as placeholders.

`docs/intake/` is also different: it is a raw source-material inbox for brainstorms, copied chat notes, imported plans, and user-provided project dumps. Use it to collect context without forcing a template, then promote accepted facts into mapped owners before building from them.

`docs/superpowers/` is different: it is an optional companion workflow folder for Obra Superpowers specs and plans, not a Repo Memory deep-dive folder. Link those artifacts from owning feature or design docs and promote accepted outcomes into mapped owners.

## Empty Repository Scaffold

Use the scaffold helper when a target repository has no useful implementation
or documentation evidence yet:

```bash
python3 <skill-dir>/scripts/scaffold-docs.py /path/to/repo --with-agents
```

Resolve `<skill-dir>` to the installed `repo-memory` skill directory. When
working from this repository root, use `skills/repo-memory/scripts/...`.

The scaffold creates the default baseline docs, ownership map,
`docs/requirements/`, `docs/features/_template.md`, `docs/intake/README.md`,
initial decision and implementation log entries, and a doc-health note that
marks the placeholders as unverified. Add
`--include-user-stories` when users, actors, journeys, or acceptance paths are
already known. Use `--project-name "<name>"` when the target directory name is
not the right project name.

After scaffolding, replace TODOs only with confirmed facts, user statements, or
clearly marked inference. Keep unknowns explicit until implementation evidence
exists.
