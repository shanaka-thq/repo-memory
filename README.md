# Repo Memory

<p align="center">
  <img src="./assets/project-logo.png" alt="Repo Memory project logo" width="640">
</p>

A simple documentation pattern for keeping project context in the repo.

Repo Memory keeps the parts of a project that code alone does not explain:
why it exists, who it serves, what it is meant to do, where important context
lives, and how decisions, features, and handoffs have evolved. The code remains
the source of truth for implementation; Repo Memory keeps the surrounding
context close enough that humans and agents can understand and change it
safely.

Repo Memory is for projects where important context should not live only in chat
history, agent memory, or one tool-specific instruction file.

It gives a project a maintained place for the things future work depends on:
the project goal, users or actors, requirements, architecture, decisions,
feature status, testing notes, and handoff context.

The point is not to create heavy documentation. The point is to make the project
easier to leave, resume, review, and change without losing why things are being
built a certain way.

## What This Project Provides

This project provides a portable standard plus one skill implementation:

- [`STANDARD.md`](./STANDARD.md) defines the portable Repo Memory standard.
- [`SKILL.md`](./SKILL.md) implements the standard as a Codex-compatible skill.
- [`references/`](./references/) contains rules, templates, metadata schema, audit workflow, decision reconstruction, and continuity governance, including interrupted-work recovery.
- [`agents/`](./agents/) contains thin platform adapters for agent tools.
- [`examples/`](./examples/) shows what adoption and handoff state look like.
- [`scripts/validate-docs.py`](./scripts/validate-docs.py) provides lightweight local validation.

Use Repo Memory when you want to:

- bootstrap a `docs/` folder for a new project from scratch
- audit an existing repo and backfill missing or stale documentation
- reconstruct architecture, requirements, decisions, and feature state from
  code evidence
- keep project goals, users or actors, success criteria, scope, and non-goals
  explicit
- document observability and instrumentation signals such as logs, metrics,
  traces, analytics events, audit events, dashboards, and alerts
- keep documentation current as features are researched, implemented, paused,
  recovered, or handed off
- keep one docs layer that humans and different coding agents can share
- track doc freshness, conflicts, renamed docs, superseded work, and
  verification evidence
- validate expected docs structure locally or in CI

## When to Use It

| Situation | Action |
| --- | --- |
| Starting a new project | Run the skill to create the full `docs/` baseline |
| Onboarding an existing codebase | Run the skill to audit, backfill, and standardize |
| Adding or resuming a feature | Run the skill to update feature docs and handoff notes |
| Handing off to another agent | Run the skill to confirm docs are current and resumable |
| Docs have drifted from code | Run the skill to realign the documentation set |

## Repository Structure

```text
repo-memory/
├── README.md                          # this file
├── STANDARD.md                        # portable Repo Memory standard
├── AGENTS.md                          # instructions for AI coding agents
├── CHANGELOG.md                       # version history
├── SKILL.md                           # full skill definition and workflow
├── LICENSE                            # MIT license
├── CONTRIBUTING.md                    # contribution guidelines
├── CODE_OF_CONDUCT.md                 # community behavior expectations
├── SUPPORT.md                         # support and issue guidance
├── ROADMAP.md                         # directional project roadmap
├── .gitignore                         # local generated-file ignores
├── .markdownlint.json                 # Markdown lint config
├── .github/
│   ├── ISSUE_TEMPLATE/                # issue templates
│   ├── pull_request_template.md       # pull request checklist
│   └── workflows/
│       ├── pr-checks.yml              # lint, link check, version validate on PRs
│       └── release.yml                # auto-tag and GitHub Release on main
├── agents/
│   ├── openai-codex.md                # OpenAI Codex session guide
│   ├── claude-code.md                 # Claude Code integration guide
│   ├── openai.yaml                    # OpenAI Agents SDK configuration
│   └── github-copilot.md              # GitHub Copilot integration guide
├── examples/
│   ├── existing-project-after/        # adopted docs tree example
│   └── multi-agent-handoff/           # feature handoff example
├── scripts/
│   └── validate-docs.py               # local docs validation helper
└── references/
    ├── templates.md                   # default docs structure and file templates
    ├── existing-project-audit.md      # audit workflow for existing projects
    ├── decision-log-reconstruction.md # comprehensive durable decision capture
    ├── continuity-governance.md       # conflict, freshness, recovery, rename, and closure protocols
    ├── documentation-metadata-schema.md # standard metadata fields by doc type
    └── docs-structure-rules.md        # strict naming conventions and placement rules
```

## Quick Start

### For AI Agents

Read [`AGENTS.md`](./AGENTS.md) first for a concise entry point. Then read
[`STANDARD.md`](./STANDARD.md) for the portable standard and [`SKILL.md`](./SKILL.md)
for the skill workflow.

### For Humans

1. Read [`STANDARD.md`](./STANDARD.md) to understand what adoption means.
2. Read [`SKILL.md`](./SKILL.md) for the complete workflow.
3. Use [`references/templates.md`](./references/templates.md) as a copy-paste starting point for any new doc.
4. Use [`references/existing-project-audit.md`](./references/existing-project-audit.md) to audit an existing codebase.
5. Use [`references/docs-structure-rules.md`](./references/docs-structure-rules.md) to check naming and placement before committing.
6. Use [`references/continuity-governance.md`](./references/continuity-governance.md) when docs conflict, drift, work is interrupted, files need recovery, docs are renamed, or features need terminal-state handling.
7. Use [`references/documentation-metadata-schema.md`](./references/documentation-metadata-schema.md) to keep doc metadata consistent across agents.

### Validate Locally

Run the validator against this skill repo:

```bash
python3 scripts/validate-docs.py --skill-repo .
```

Run the validator against a target repo that adopted the standard:

```bash
python3 scripts/validate-docs.py --project-docs /path/to/repo
```

### Examples

- [`examples/existing-project-after/`](./examples/existing-project-after/) shows
  a compact target repo after adoption.
- [`examples/multi-agent-handoff/`](./examples/multi-agent-handoff/) shows how
  active feature state should let another agent resume without chat history.

## Philosophy

Most projects have more context than the code alone can show.

There is usually a goal, a set of users or actors, expected behavior, tradeoffs,
and decisions that shape the work. When those things are not written down, each
agent or contributor has to rediscover them, guess them, or rely on stale memory.

Repo Memory keeps that context close to the code. It helps agents and humans check
whether new work still fits the project goal, whether features match user
stories, and whether tests cover the behavior people actually care about.

## Key Principles

- **One place for project context** per project. Avoid overlapping documentation
  systems when one maintained docs layer is enough.
- **Markdown first.** The standard should be readable in the repo without a
  specific AI provider, editor, plugin, or service.
- **Two layers.** Keep stable project-wide docs concise, then add deep-dive docs
  for subsystems, features, designs, or flows that need more detail.
- **Evidence first.** Document what is confirmed before what is assumed, and mark
  inferred claims clearly.
- **Easy to resume.** A paused or interrupted session should leave enough notes
  for a future human or agent to continue safely.
- **Product context matters.** Goals, users, stories, use cases, and acceptance
  expectations are part of the engineering context, not separate from it.
- **History should not disappear.** Doc changes, conflicts, stale areas, renames,
  and abandoned or superseded work should be recorded when they matter.

## Default Docs Structure

The target docs layout for any project using the Repo Memory standard:

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
│   ├── non-functional-requirements.md
│   └── user-stories-and-use-cases.md  # optional
├── diagrams/                           # optional
├── designs/                            # optional
├── project-details/                    # optional
├── components/                         # optional
├── ui-ux/                              # optional
└── features/
    ├── _template.md
    └── <feature-slug>.md
```

See [`references/templates.md`](./references/templates.md) for the full layout, templates, and placement rules.

## Naming and Structure Rules

All file and folder names in `docs/` must follow strict kebab-case conventions. See [`references/docs-structure-rules.md`](./references/docs-structure-rules.md) for the complete ruleset.

## Versioning

The standard and skill use the same two-number version (`MAJOR.MINOR`) recorded
as `Version:` in [`STANDARD.md`](./STANDARD.md) and [`SKILL.md`](./SKILL.md).

| Change type | Action |
| --- | --- |
| New content or non-breaking additions | Increment minor |
| Required baseline changes or structural workflow changes | Increment major |

Each version is tagged `vMAJOR.MINOR` and published as a GitHub Release. The release body is pulled from [`CHANGELOG.md`](./CHANGELOG.md). Update `CHANGELOG.md` in the same PR that bumps the version.

## Related Docs

- Portable standard: [`STANDARD.md`](./STANDARD.md)
- Full skill definition: [`SKILL.md`](./SKILL.md)
- Version history: [`CHANGELOG.md`](./CHANGELOG.md)
- AI agent instructions: [`AGENTS.md`](./AGENTS.md)
- OpenAI Codex guide: [`agents/openai-codex.md`](./agents/openai-codex.md)
- Claude Code guide: [`agents/claude-code.md`](./agents/claude-code.md)
- File templates: [`references/templates.md`](./references/templates.md)
- Audit workflow: [`references/existing-project-audit.md`](./references/existing-project-audit.md)
- Structure rules: [`references/docs-structure-rules.md`](./references/docs-structure-rules.md)
- Documentation metadata schema: [`references/documentation-metadata-schema.md`](./references/documentation-metadata-schema.md)
- Decision reconstruction: [`references/decision-log-reconstruction.md`](./references/decision-log-reconstruction.md)
- Continuity governance: [`references/continuity-governance.md`](./references/continuity-governance.md)
- Examples: [`examples/README.md`](./examples/README.md)
- Roadmap: [`ROADMAP.md`](./ROADMAP.md)
- Contributing: [`CONTRIBUTING.md`](./CONTRIBUTING.md)
