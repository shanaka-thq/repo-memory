# Repo Memory

<p align="center">
  <img src="./assets/project-logo.png" alt="Repo Memory project logo" width="640">
</p>

## The Problem

You use multiple AI coding agents. Maybe Claude today, Codex tomorrow, Copilot
for a PR review. Each one has its own memory — but that memory **doesn't
transfer between tools.**

- Claude's Projects memory is invisible to Codex
- Cursor's context doesn't exist in Kiro
- When an agent crashes mid-feature, the next session starts from zero
- Nobody wrote down "here's where I stopped, here's what to do next"

Agent-local memory solves recall within one tool. It doesn't solve **continuity
across tools and sessions.**

## What Repo Memory Does

It gives every agent (and you) a **shared memory layer** that lives in your
repo as plain Markdown files:

```text
docs/
├── README.md                  ← "where does each kind of truth live?" (ownership map)
├── features/
│   ├── auth-refresh.md        ← "what's the status? what's next? who's blocked?"
│   └── search-v2.md
└── generated/
    ├── feature-registry.md    ← auto-built summary of all features
    └── next-work-queue.md     ← "what should the next agent pick up?"
```

That's it. An ownership map, feature docs with machine-readable frontmatter, and
auto-generated indexes. Any agent that can read a file can use it.

## What It Does NOT Do

Repo Memory is a **continuity layer.** It fills the gap that no other tool
covers. It does not compete with:

| Tool                    | What it does                  | What RM does instead                                           |
| ----------------------- | ----------------------------- | -------------------------------------------------------------- |
| **Kiro specs**          | Define requirements and tasks | Link to the spec, track implementation status                  |
| **Superpowers planner** | Create implementation plans   | Link to the plan, record what was accepted                     |
| **Code review skills**  | Review code quality/security  | Record that a review happened, link the output                 |
| **Agent-local memory**  | Recall within one tool        | Capture the cross-tool bits that don't transfer                |
| **MCP memory servers**  | Shared memory via protocol    | Works without extra infra, versioned in git, reviewable in PRs |

RM doesn't plan, review, or spec. It records where those outputs live and keeps
feature state resumable across agents.

## Why Not Just an MCP Memory Server?

MCP memory servers exist, but:

- They require every agent to have the same MCP server configured
- The memory isn't versioned or reviewable in PRs
- They're still maturing — most don't handle structured feature state well
- They add infrastructure (a running server) vs. just files in your repo

Repo Memory works today, with zero infrastructure, across any tool that reads
files. When MCP memory servers mature, they could read from these same docs.

## The Three Things RM Owns

1. **Ownership map** (`docs/README.md`) — "where does each kind of truth live?"
   Points to existing docs (ADRs, specs, OpenAPI, etc.) instead of duplicating them.

2. **Feature state** (`docs/features/*.md`) — status, handoff notes, next safe
   step, blockers. Machine-readable frontmatter:

   ```yaml
   ---
   id: auth-refresh
   title: Token Refresh Flow
   status: in_progress
   ready: ready
   next_safe_step: "Wire refresh endpoint to session store, run auth tests"
   priority: 2
   ---
   ```

3. **Work queue** (`docs/generated/next-work-queue.md`) — auto-generated from
   frontmatter. "What should the next agent pick up?" No manual sync needed.

## Quick Start

Install the skill for your agent:

```bash
npx skills add akanahs-dev/repo-memory --skill repo-memory -g -a claude-code -y
```

Change `-a claude-code` to: `generic`, `github-copilot`, `cursor`, `windsurf`,
`kiro`, `opencode`, or `codex`. Drop `-g` to install into the current project only.

Or copy the adapter file manually from [`templates/`](./templates/).

### Scripts (zero dependencies, just Python 3)

```bash
# Validate feature docs and structure
python3 <skill-dir>/scripts/validate-docs.py --project-docs .

# Generate indexes from feature frontmatter
python3 <skill-dir>/scripts/generate-indexes.py .

# Scaffold initial docs (empty repos)
python3 <skill-dir>/scripts/scaffold-docs.py .
```

## How It Works (30 seconds)

1. Agent reads a 10-line adapter file → gets pointed to `docs/README.md`
2. Ownership map tells it where everything lives (existing docs, not RM copies)
3. Agent reads the feature doc for its current task
4. Agent does its work, updates feature frontmatter (`status`, `next_safe_step`)
5. Next agent — any agent, any tool — picks up from where the last one stopped

No chat history needed. No shared MCP server. Just files in git.

## Modes

| Mode             | When                                                    |
| ---------------- | ------------------------------------------------------- |
| **Maintainer**   | Normal work — keep feature state current                |
| **Bootstrapper** | First-time setup — create ownership map + feature stubs |
| **Auditor**      | Health check — find drift, stale docs, broken links     |
| **Generator**    | Rebuild auto-generated indexes                          |

No planner mode. No reviewer mode. Use your planning and review tools — RM just
links their outputs.

## Works With Everything

Because it's just Markdown in your repo:

- Claude, Codex, Copilot, Cursor, Windsurf, Kiro, OpenCode
- Superpowers plans and specs (link them from feature docs)
- Kiro spec directories (link them from the ownership map)
- Any MCP tool, any IDE, any CI pipeline
- Humans reading docs on GitHub

## Token Cost

The skill router is 35 lines. During normal work, an agent loads:

- The ownership map (~20 lines)
- The active feature doc (~30-50 lines)
- That's it.

Full references are loaded only when doing doc maintenance, not during regular
coding. RM is designed to stay out of the way.

## Manual Install

Copy from [`templates/`](./templates/):

| Agent           | File                                        |
| --------------- | ------------------------------------------- |
| Claude Code     | `templates/CLAUDE.md`                       |
| Codex / generic | `templates/AGENTS.md`                       |
| GitHub Copilot  | `templates/.github/copilot-instructions.md` |
| Cursor          | `templates/.cursor/rules/repo-memory.mdc`   |
| Windsurf        | `templates/.windsurf/rules/repo-memory.md`  |
| Kiro            | `templates/.kiro/steering/repo-memory.md`   |

Also copy `templates/repo-memory.config.yml` and `templates/docs/features/_template.md`.

## Repository Layout

```text
repo-memory/
├── skills/repo-memory/        # the skill (what agents read)
│   ├── SKILL.md               # 35-line router
│   ├── STANDARD.md            # the portable standard
│   ├── modes/                 # maintainer, bootstrapper, auditor, generator
│   ├── references/            # naming rules, templates, metadata schema
│   └── scripts/               # validate, generate, scaffold (Python, zero deps)
├── adapters/                  # pre-built adapter files
└── templates/                 # files you copy into your repo
```

## Key Principles

- **Link, don't duplicate.** If a fact already has an owner (ADR, OpenAPI, spec file), point to it.
- **Features drive the queue.** Frontmatter is the source of truth. Scripts generate indexes.
- **Don't compete.** Planning, reviewing, and spec-writing belong to dedicated tools.
- **Stay cheap.** Load minimal context during normal work. Full refs only for doc maintenance.

## Learn More

- [`SKILL.md`](./skills/repo-memory/SKILL.md) — what agents load
- [`STANDARD.md`](./skills/repo-memory/STANDARD.md) — the full standard
- [`CONTRIBUTING.md`](./CONTRIBUTING.md) — how to contribute
- [`CHANGELOG.md`](./CHANGELOG.md) — version history
