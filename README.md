# Repo Memory

<p align="center">
  <img src="./assets/project-logo.png" alt="Repo Memory project logo" width="640">
</p>

**The state persistence layer for AI-assisted repos.** Any agent resumes where
the last one stopped.

## The Problem

You use workflow skills — planning, implementation, review, triage. They produce
artifacts everywhere: plans in one folder, tickets in another, specs in a third.
When you switch agents or sessions, nobody knows where things are or what state
they're in.

Agent-local memory solves recall within one tool. It doesn't solve **continuity
across tools and sessions.**

## What Repo Memory Does

A thin persistence layer that tracks three things:

1. **Where things live** — an ownership map with typed slots for every artifact category
2. **What state they're in** — feature docs with machine-readable frontmatter
3. **What's next** — an auto-generated work queue from that frontmatter

```text
docs/
├── README.md                  ← ownership map + artifact locations
├── features/
│   ├── auth-refresh.md        ← status, next step, links to plan/spec/tickets
│   └── search-v2.md
└── generated/
    ├── feature-registry.md    ← auto-built summary of all features
    └── next-work-queue.md     ← "what should the next agent pick up?"
```

That's it. Any agent that can read a file can use it.

## How It Connects With Other Skills

RM doesn't plan, review, spec, or implement. It **connects** the skills that do:

```text
┌───────────────────────────────────────────┐
│         Repo Memory (state layer)         │
│  ownership map · feature docs · work queue│
└─────────────────────┬─────────────────────┘
                      │ agents read on start
      ┌───────────────┼───────────────────┐
      ▼               ▼                   ▼
┌───────────┐  ┌────────────┐  ┌───────────────┐
│ Planning  │  │ Building   │  │ Reviewing     │
│           │  │            │  │               │
│/wayfinder │  │/implement  │  │/code-review   │
│/to-tickets│  │/tdd        │  │/triage        │
│/to-spec   │  │/exec-plans │  │/improve       │
└─────┬─────┘  └─────┬──────┘  └───────┬───────┘
      │               │                 │
      └───────────────┼─────────────────┘
                      ▼ agents write on close
┌───────────────────────────────────────────┐
│         Repo Memory (state layer)         │
│  update status · link artifacts · next step│
└───────────────────────────────────────────┘
```

Each skill writes to its own location. RM doesn't interfere with the middle —
it owns the **start** (orient) and **end** (persist state) of each session.

## Works With

| Skill Pack | What RM adds |
|------------|--------------|
| **Matt Pocock's skills** | Persists state between /implement sessions, routes agents to plans/tickets |
| **Obra / Superpowers** | Links plans and specs, tracks which are accepted vs in-progress |
| **Kiro specs** | Maps spec directories, tracks implementation status per feature |
| **Shadcn / Improve** | Registers plan locations, tracks plan execution status |
| **Standalone (no skills)** | Full feature state tracking — RM carries more weight |
| **Your custom skills** | Register artifact locations in typed slots, zero coupling |

See [`compatible-skills.md`](./skills/repo-memory/references/compatible-skills.md)
for the full integration table.

## What It Does NOT Do

| Tool                    | What it does                  | What RM does instead                                           |
| ----------------------- | ----------------------------- | -------------------------------------------------------------- |
| **Planning skills**     | Decompose work into plans     | Link to the plan, track implementation status                  |
| **Review skills**       | Review code quality/security  | Record that a review happened, link the output                 |
| **Spec skills**         | Define requirements           | Link to the spec, track what was accepted                      |
| **Agent-local memory**  | Recall within one tool        | Capture the cross-tool bits that don't transfer                |
| **MCP memory servers**  | Shared memory via protocol    | Works without extra infra, versioned in git, reviewable in PRs |

RM doesn't plan, review, or spec. It records where those outputs live and keeps
feature state resumable across agents.

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

1. Agent loads adapter → reads ownership map
2. Ownership map tells it where everything lives (plans, tickets, specs, ADRs — via typed slots)
3. Agent reads the feature doc for its current task (status + next step)
4. Agent does its work using whatever skills it wants
5. Agent updates feature frontmatter before stopping (`status`, `next_safe_step`)
6. Next agent — any agent, any tool — picks up from there

No chat history needed. No shared MCP server. Just files in git.

## Typed Slots

The ownership map includes an **Artifact Locations** table — typed slots for
each category of workflow artifact:

| Category | What lives here | Example producers |
|----------|-----------------|-------------------|
| Plans | Implementation plans | /writing-plans, /improve |
| Specs | Requirements, PRDs | /to-spec, Kiro specs |
| Tickets | Work items, issues | /to-tickets, /triage, /wayfinder |
| ADRs | Architecture decisions | /grill-with-docs, /domain-modeling |
| Reviews | Code review outputs | /code-review |
| Handoff | Session state, next steps | RM feature docs (native) |
| Research | Investigation outputs | /research, /improve |

When you install a new skill, just update the relevant slot with where its
artifacts land. No RM code changes needed.

## Modes

| Mode | When | Frequency |
|------|------|-----------|
| **Bootstrapper** | First-time setup — create ownership map, discover skills, configure slots | Once per repo |
| **Maintainer** | Session close — update feature frontmatter, link new artifacts | Every session |
| **Auditor** | Health check — find drift, stale docs, broken links | On-demand |
| **Generator** | Rebuild auto-generated indexes | Automatic |

No planner mode. No reviewer mode. Use your planning and review tools — RM just
links their outputs.

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
│   ├── modes/                 # bootstrapper, maintainer, auditor, generator
│   ├── references/            # naming rules, templates, compatibility, metadata
│   └── scripts/               # validate, generate, scaffold (Python, zero deps)
├── adapters/                  # pre-built adapter files
└── templates/                 # files you copy into your repo
```

## Key Principles

- **Link, don't duplicate.** If a fact already has an owner (ADR, spec, plan), point to it.
- **Features drive the queue.** Frontmatter is the source of truth. Scripts generate indexes.
- **Don't compete.** Planning, reviewing, and spec-writing belong to dedicated skills.
- **Stay cheap.** Load minimal context during normal work. Full refs only for doc maintenance.
- **Typed slots, not skill coupling.** RM knows artifact categories, not specific skills.

## Related Skills

| If you need... | Use | RM's role |
|---------------|-----|-----------|
| Planning & decomposition | /writing-plans, /wayfinder | Links plans, tracks status |
| Implementation | /implement, /executing-plans | Records progress, next step |
| Code review | /code-review | Records outcome, links output |
| Issue tracking | /to-tickets, /triage | Maps tracker location |
| Handoff (ephemeral) | /handoff | Persists the durable parts |
| Research | /research, /improve | Registers artifact location |
| Specs & requirements | /to-spec, Kiro specs | Maps spec directory |

## Learn More

- [`SKILL.md`](./skills/repo-memory/SKILL.md) — what agents load
- [`STANDARD.md`](./skills/repo-memory/STANDARD.md) — the full standard
- [`compatible-skills.md`](./skills/repo-memory/references/compatible-skills.md) — integration table
- [`CONTRIBUTING.md`](./CONTRIBUTING.md) — how to contribute
- [`CHANGELOG.md`](./CHANGELOG.md) — version history
