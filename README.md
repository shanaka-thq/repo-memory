# Repo Memory

<p align="center">
  <img src="./assets/project-logo.png" alt="Repo Memory project logo" width="640">
</p>

An agent-first, CLI-assisted memory protocol for software repositories.

Repo Memory keeps the context that code alone cannot explain — project goals,
architecture decisions, feature status, handoff notes — in maintained Markdown
docs close to the code. Any agent or human can read and update them without a
special tool or service.

## Why It Exists

In multi-agent workflows, shared state breaks in predictable ways: every new
session re-derives the same context, agents clobber each other's work, and
interrupted features get dropped because nobody wrote down the next safe step.

Repo Memory solves this by giving every agent one shared surface:

- one ownership map that names where each kind of truth lives
- one feature registry that tells the next agent what to pick up
- one handoff note per feature with enough context to resume safely
- generated indexes built from machine-readable frontmatter — no manual sync

Because it is just Markdown in your repo, it works across Claude, Codex,
Copilot, Cursor, Windsurf, Kiro, OpenCode, and any tool that can read a file.

## How It Works

**Three pieces:**

| Piece | What it is | Where |
| ----- | ---------- | ----- |
| Skill | A lean `SKILL.md` router that points agents to 6 mode files | `skills/repo-memory/` |
| Adapters | Thin agent-specific files (`CLAUDE.md`, `AGENTS.md`, etc.) | `adapters/` + `templates/` |
| CLI | `npx repo-memory` — doctor, validate, generate | `src/` (TypeScript) |

**The agent workflow:**

1. Agent reads the adapter file for its tool (e.g. `CLAUDE.md`) — 10–15 lines
2. Adapter points to `skills/repo-memory/SKILL.md` — another 35 lines
3. SKILL.md routes the agent to the right mode file (`maintainer`, `bootstrapper`, etc.)
4. Agent loads only the mode it needs, plus the relevant feature doc
5. After work, agent updates feature frontmatter — `status`, `ready`, `next_safe_step`
6. Next agent runs `npx repo-memory generate` to rebuild the indexes

Context loaded per session stays small because the skill is a router, not a monolith.

## CLI

```bash
npx repo-memory doctor    # detect repo state, suggest next actions
npx repo-memory validate  # validate feature frontmatter, catch duplicate IDs
npx repo-memory generate  # write feature-registry.md, next-work-queue.md, doc-health.md
npx repo-memory generate --dry-run  # preview without writing
```

The `generate` command reads YAML frontmatter from `docs/features/*.md` and
produces deterministic indexes. Agents update frontmatter; the CLI rebuilds the
indexes. No manual sync.

## Feature Frontmatter

Each feature doc carries machine-readable YAML at the top:

```yaml
---
id: auth-refresh
title: Token Refresh Flow
status: in_progress
doc_type: feature
ready: ready
next_safe_step: "Wire refresh endpoint to the session store, then run auth tests"
priority: 2
owner: backend-team
confidence: medium
last_updated: 2026-05-26
---
```

`npx repo-memory validate` checks every file against the schema. Invalid status
values, missing required fields, and duplicate IDs all fail with a clear error.

## Install the Skill in Your Repo

### Via `npx skills` (recommended)

```bash
npx skills add akanahs-dev/repo-memory --skill repo-memory -g -a codex -y
```

Change `-a codex` to your agent (`claude-code`, `github-copilot`, `cursor`,
`windsurf`, `kiro`, `opencode`, or `generic`). Omit `-g` to install into the
current project instead of your global skills directory.

### Via the CLI

Once you have the repo available locally, use the CLI to install the adapter
for your agent:

```bash
npx repo-memory install-adapter claude-code   # writes CLAUDE.md
npx repo-memory install-adapter generic       # writes AGENTS.md
npx repo-memory install-adapter github-copilot
npx repo-memory install-adapter cursor
npx repo-memory install-adapter windsurf
npx repo-memory install-adapter kiro
```

Use `--append` to add a managed block to an existing file instead of replacing
it, or `--print` to preview the adapter content before writing anything.

### Manually

Copy the adapter file for your agent from `templates/` into your repo root:

| Agent | File to copy |
| ----- | ------------ |
| Claude Code | `templates/CLAUDE.md` |
| Codex / generic | `templates/AGENTS.md` |
| GitHub Copilot | `templates/.github/copilot-instructions.md` |
| Cursor | `templates/.cursor/rules/repo-memory.mdc` |
| Windsurf | `templates/.windsurf/rules/repo-memory.md` |
| Kiro | `templates/.kiro/steering/repo-memory.md` |
| OpenCode | `templates/AGENTS.md` |

Then add `repo-memory.config.yml` (copy from `templates/repo-memory.config.yml`)
and `docs/features/_template.md` (copy from `templates/docs/features/_template.md`)
to your repo.

## Modes

Agents load the mode that fits the task:

| Mode | When to use |
| ---- | ----------- |
| **Maintainer** | Normal feature work — update docs as code changes |
| **Bootstrapper** | Adopt an existing repo — extract context into `docs/intake/` |
| **Planner** | Write an implementation plan in the configured plans path |
| **Reviewer** | Codebase, architecture, security, or AI review |
| **Auditor** | Check for drift, stale docs, missing ownership |
| **Generator** | Rebuild generated indexes |

## Multi-Agent Handoff

When handing off between agents or sessions:

1. Update the feature doc frontmatter: set `status`, `ready`, and `next_safe_step`
2. Run `npx repo-memory generate` to rebuild the indexes
3. The next agent runs `npx repo-memory doctor` to orient itself, then reads
   `docs/generated/next-work-queue.md` to pick the first `ready` row

No chat history needed. The feature doc carries the resume state.

## Repository Structure

```text
repo-memory/
├── skills/repo-memory/        # installable skill payload
│   ├── SKILL.md               # lean router (35 lines) — entry point for agents
│   ├── STANDARD.md            # portable Repo Memory standard
│   ├── modes/                 # 6 mode files (maintainer, bootstrapper, etc.)
│   ├── references/            # rules, templates, metadata schema, audit workflow
│   ├── examples/              # adopted docs and handoff examples
│   └── scripts/               # scaffold-docs.py, validate-docs.py
├── adapters/                  # thin adapter files by agent tool
│   ├── claude-code/CLAUDE.md
│   ├── generic/AGENTS.md
│   ├── codex/instructions.md
│   ├── cursor/repo-memory.mdc
│   ├── github-copilot/copilot-instructions.md
│   ├── kiro/repo-memory.md
│   ├── opencode/AGENTS.md
│   └── windsurf/repo-memory.md
├── templates/                 # copy these into your repo
│   ├── CLAUDE.md
│   ├── AGENTS.md
│   ├── repo-memory.config.yml
│   └── docs/features/_template.md
├── src/                       # TypeScript CLI source
│   ├── cli/index.ts
│   ├── commands/              # doctor, validate, generate
│   ├── core/                  # config, discovery, frontmatter, feature-index
│   └── schemas/               # Zod schemas for config and feature frontmatter
└── tests/unit/                # 68 unit tests
```

## Validate Locally or in CI

Validate your skill repo itself:

```bash
python3 skills/repo-memory/scripts/validate-docs.py --skill-repo .
```

Validate a target repo that adopted the standard:

```bash
python3 skills/repo-memory/scripts/validate-docs.py \
  --project-docs /path/to/repo --adoption-level baseline
```

Or use the CLI for feature-level validation:

```bash
npx repo-memory validate
```

## Key Rules

- **One owner per capability.** `docs/README.md` names one canonical owner for each doc capability. Agents link to it; they do not duplicate it.
- **Features drive the queue.** `docs/features/*.md` frontmatter is the source of truth. The CLI generates the registry and queue from it.
- **Generated files are not edited manually.** `docs/generated/` is owned by `npx repo-memory generate`.
- **Intake is not truth yet.** `docs/intake/` is a raw inbox. Accepted facts get promoted into mapped owners.

## Versioning

release-please manages version markers in `SKILL.md` and `STANDARD.md`
automatically. Do not edit them manually. See [`CHANGELOG.md`](./CHANGELOG.md)
for version history.

## Related

- [`skills/repo-memory/SKILL.md`](./skills/repo-memory/SKILL.md) — skill entry point
- [`skills/repo-memory/STANDARD.md`](./skills/repo-memory/STANDARD.md) — portable standard
- [`skills/repo-memory/references/docs-structure-rules.md`](./skills/repo-memory/references/docs-structure-rules.md) — naming and placement rules
- [`skills/repo-memory/references/templates.md`](./skills/repo-memory/references/templates.md) — copy-paste doc templates
- [`AGENTS.md`](./AGENTS.md) — instructions for agents working on this repo
- [`CONTRIBUTING.md`](./CONTRIBUTING.md) — contribution guide
- [`CHANGELOG.md`](./CHANGELOG.md) — version history
