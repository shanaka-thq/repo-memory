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

Repo Memory is meant to complement strong existing documentation workflows, not
declare war on them. If a repo already has useful ADRs, OpenAPI specs,
architecture notes, runbooks, RFCs, wiki pages, security docs, or agent
instructions, keep what works. Repo Memory adds a canonical ownership map and
only the missing handoff surfaces future humans and coding agents need for
shared state, cross-agent pickup, and safe resumption.

The strict rule is: **one canonical owner per documentation capability**. ADRs
can own decisions. `CONTRIBUTING.md` can own setup commands. `openapi.yaml` can
own API contracts. Repo Memory should link to those owners, not create duplicate
competing summaries.

## What Is This Repository For?

This repository is a **documentation standard + installable agent skill**.

It helps teams keep project context understandable across humans and AI coding
agents by defining:

- what documentation capabilities need a canonical owner
- how to keep feature state and handoff notes resumable
- how to avoid duplicate, conflicting docs across tools

It is **not** a product application, framework runtime, or template starter app.

## Who This Is For

- **Engineering teams** that lose context between sessions, handoffs, or tools
- **Maintainers** who want documentation drift checks in normal workflows
- **Agent users** (Copilot, Codex, Claude, OpenCode, etc.) who need one shared
  source of project truth

If you are just evaluating quickly: this repo gives you the standard,
implementation workflow, examples, and validator scripts needed to adopt Repo
Memory in another repository.

## What You Should Understand in 2 Minutes

After a quick scan, a new visitor should be able to answer:

1. **What is it?** A portable docs ownership and handoff standard for AI-assisted software projects.
2. **Why does it exist?** To reduce context loss and documentation drift.
3. **How do I use it?** Install the `repo-memory` skill, then apply it to a target repo.
4. **Where is the source of truth?** `STANDARD.md` (normative) and `SKILL.md` (workflow).

## Short Version (Start Here)

If the full docs feel like a lot, use this minimal path first:

1. Read [`README.md`](./README.md) (this file) for what Repo Memory is.
2. Read [`skills/repo-memory/STANDARD.md`](./skills/repo-memory/STANDARD.md) for the canonical model.
3. Read [`skills/repo-memory/SKILL.md`](./skills/repo-memory/SKILL.md) for operational workflow.
4. Use [`CHANGELOG.md`](./CHANGELOG.md) for current version and recent changes.

Everything else is reference depth you can pull in only when needed.

## Install and Use

Install Repo Memory from the repository root and select the skill by name:

```bash
npx skills add akanahs-dev/repo-memory --skill repo-memory -g -a codex -y
```

Install for another supported agent by changing the `-a` value, or omit `-a`
to choose interactively. Omit `-g` to install into the current project instead
of your global agent skills directory.

You can also install directly from the skill folder:

```bash
npx skills add https://github.com/akanahs-dev/repo-memory/tree/main/skills/repo-memory -g -a codex -y
```

After installing, ask your agent to use `repo-memory` on a target repository:

```text
Use $repo-memory to audit this repo, create or update the Repo Memory docs,
and leave current handoff notes for future agents.
```

This repository follows the common multi-skill repository layout:
`skills/<skill-name>/SKILL.md`. The installable payload is
[`skills/repo-memory/`](./skills/repo-memory/); the repository root contains
governance files, CI, release notes, and public project documentation.

### What Gets Installed (and What Does Not)

When you install with `--skill repo-memory`, the installable payload is the
`skills/repo-memory/` directory.

- **Included for skill runtime:** `SKILL.md`, `STANDARD.md`, `references/`,
  `agents/`, `examples/`, and `scripts/` under `skills/repo-memory/`.
- **Not the skill payload:** repository-root governance and meta files such as
  root `AGENTS.md`, root `README.md`, CI workflows, and issue templates.

Root `AGENTS.md` in this repository is primarily for agents working **on this
repository itself** (the skill source repo). It describes how to maintain this
repo and keep standard/skill docs aligned.

In contrast, when Repo Memory is applied to a target project, that target repo
may have its own root `AGENTS.md` as a thin entrypoint into that target
project's canonical docs.

## What This Project Provides

This project provides a portable standard plus one installable skill package:

- [`skills/repo-memory/STANDARD.md`](./skills/repo-memory/STANDARD.md) defines the portable Repo Memory standard and capability ownership model.
- [`skills/repo-memory/SKILL.md`](./skills/repo-memory/SKILL.md) implements the standard as an agent-facing skill workflow.
- [`skills/repo-memory/references/`](./skills/repo-memory/references/) contains rules, templates, metadata schema, audit workflow, decision reconstruction, continuity governance, agent integration and enforcement, and companion workflow guidance, including interrupted-work recovery.
- [`skills/repo-memory/agents/`](./skills/repo-memory/agents/) contains thin platform adapters for agent tools.
- [`skills/repo-memory/examples/`](./skills/repo-memory/examples/) shows what adoption and handoff state look like.
- [`skills/repo-memory/scripts/`](./skills/repo-memory/scripts/) provides empty-repo scaffolding, lightweight local validation, and manual blind forward-testing.

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
- keep a ranked next-work queue so cloud agents can pick the next ready task
  without burning a session on orientation
- keep one canonical owner for each project documentation capability
- keep one docs layer that humans and different coding agents can share without
  duplicating ADRs, API specs, setup docs, runbooks, or active handoff state
- give greenfield projects a simple `docs/intake/` inbox for messy brainstorms,
  project dumps, copied chat notes, sketches, and planning output
- bridge companion spec and plan workflows such as Obra Superpowers without
  losing canonical feature, decision, validation, or handoff state
- track doc freshness, conflicts, renamed docs, superseded work, and
  verification evidence
- validate expected docs structure locally or in CI

## Progressive Adoption

Repo Memory can be adopted incrementally.

If a repo already has solid project docs, the first useful step is often not a
full rewrite. Start by:

1. creating or updating `docs/README.md` with a `Canonical Ownership Map`
2. naming existing ADRs, specs, runbooks, READMEs, and security docs as owners
   where they are already strong
3. adding only the missing cross-agent surfaces, such as
   `docs/feature-registry.md`, `docs/doc-health.md`, and active feature docs
4. expanding toward the full baseline only where no good existing owner exists

Full baseline and continuity conformance still matter for repos that want the
complete standard. Progressive adoption just makes the on-ramp less dramatic
and more compatible with existing team habits.

## When to Use It

| Situation                                                   | Action                                                                                                     |
| ----------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| Starting a new project                                      | Run the scaffold to create a full baseline and ownership map                                               |
| Dumping greenfield brainstorms or AI plans                  | Put raw material in `docs/intake/`, then run the skill to promote accepted facts into the mapped owner     |
| Existing repo with strong docs                              | Add an ownership map and continuity surfaces first; do not duplicate ADRs, specs, runbooks, or setup docs  |
| Onboarding an existing codebase                             | Run the skill to audit evidence, assign owners, backfill only missing capabilities, and record stale areas |
| Adding or resuming a feature                                | Run the skill to update feature docs, ranked queue, and handoff notes                                      |
| Handing off to another agent                                | Run the skill to confirm docs are current and resumable                                                    |
| Asking a cloud agent to pick up work                        | Point it at `docs/feature-registry.md` and tell it to pick the first `ready` row in `Next Work Queue`      |
| Using Codex, Copilot, Claude, OpenCode, or VS Code together | Add thin tool-specific adapters that all point to `docs/README.md` and the same ownership map              |
| Docs have drifted from code                                 | Update the single canonical owner, mark stale supporting docs, and record the correction in doc health     |

## When Not to Use It

Repo Memory is optional.

It may be overkill when:

- the repo is tiny and has little durable context beyond the code itself
- the team already has a strong maintained documentation system and only needs
  a few minor handoff habits rather than a new Repo Memory ownership map
- the project is short-lived enough that feature handoff and decision history
  are not worth the maintenance cost

In those cases, keep the current workflow or adopt only the few Repo Memory
practices that help, such as a thin agent entrypoint, a feature registry, or a
hand-off-friendly feature doc.

## Will Agents Update Docs Automatically?

Not just because the skill exists.

The skill helps an agent maintain documentation when that agent has the skill
installed and chooses to use it. For reliable behavior across different tools,
commit repo-local instructions and validation:

| Layer          | What to add                                                                              | Why                                                                                             |
| -------------- | ---------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| Canonical docs | `docs/README.md` with a `Canonical Ownership Map`                                        | Tells every human and agent where each kind of truth lives.                                     |
| Thin adapters  | `AGENTS.md`, `.github/copilot-instructions.md`, `CLAUDE.md`, `opencode.json` when needed | Makes each tool start from the same docs without copying project facts.                         |
| Validation     | `validate-docs.py` locally or in CI                                                      | Catches missing handoff docs, duplicate ownership rows, stale feature state, and link problems. |
| Hooks          | Tool-specific lifecycle hooks when available                                             | Useful for reminders or pre-finish checks, but CI is the shared guarantee.                      |

For setup details by tool, read
[`agent-integration-and-enforcement.md`](./skills/repo-memory/references/agent-integration-and-enforcement.md).

## Use by Environment

| Environment                       | Minimum setup                                                                                               | Expected behavior                                                                                                |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| Local Codex                       | Install the skill and commit `AGENTS.md` pointing to `docs/README.md`                                       | Codex reads repo instructions, follows the ownership map, and updates mapped owners when asked to use the skill. |
| Codex cloud or other cloud agents | Commit `AGENTS.md`, `docs/README.md`, `docs/feature-registry.md`, and active feature docs                   | The agent can pick the first `ready` queue row and resume from committed docs without chat history.              |
| GitHub Copilot and VS Code        | Add `.github/copilot-instructions.md` and optional `.github/instructions/*.instructions.md` as thin routers | Copilot gets the same docs workflow while project facts stay in the mapped owners.                               |
| Claude Code                       | Add `CLAUDE.md` that imports or points to `AGENTS.md`                                                       | Claude starts from its expected memory file without duplicating project facts.                                   |
| OpenCode                          | Use `AGENTS.md`; add `opencode.json` only for shared instruction includes                                   | OpenCode gets project rules from committed files and can combine reusable instruction files.                     |
| CI or hooks                       | Run `validate-docs.py` with the right `--adoption-level`                                                    | Missed ownership maps, broken links, malformed queue rows, and stale handoff warnings become visible.            |

## Repository Structure

```text
repo-memory/
├── README.md                          # this file
├── AGENTS.md                          # instructions for AI coding agents
├── CHANGELOG.md                       # version history
├── LICENSE                            # MIT license
├── CONTRIBUTING.md                    # contribution guidelines
├── CODE_OF_CONDUCT.md                 # community behavior expectations
├── SUPPORT.md                         # support and issue guidance
├── ROADMAP.md                         # directional project roadmap
├── .gitignore                         # local generated-file ignores
├── .gitattributes                     # source archive export rules
├── .markdownlint.json                 # Markdown lint config
├── .github/
│   ├── ISSUE_TEMPLATE/                # issue templates
│   ├── pull_request_template.md       # pull request checklist
│   └── workflows/
│       ├── pr-checks.yml              # lint, link check, version validate on PRs
│       └── release.yml                # auto-tag and GitHub Release on main
└── skills/
    └── repo-memory/                   # installable skill payload
        ├── SKILL.md                   # full skill definition and workflow
        ├── STANDARD.md                # portable Repo Memory standard
        ├── LICENSE.txt                # skill package license
        ├── agents/                    # platform adapter guides
        ├── examples/                  # adopted docs and handoff examples
        ├── scripts/
        │   ├── forward-test.py        # manual blind agent scenario harness
        │   ├── scaffold-docs.py       # empty repo docs skeleton helper
        │   └── validate-docs.py       # local docs validation helper
        └── references/                # rules, templates, audit, governance
```

## Quick Start

### Install the Skill

Preferred install command:

```bash
npx skills add akanahs-dev/repo-memory --skill repo-memory -g -a codex -y
```

Install from the skill folder when you want to bypass repository skill
selection:

```bash
npx skills add https://github.com/akanahs-dev/repo-memory/tree/main/skills/repo-memory -g -a codex -y
```

For Codex's built-in installer, use the same GitHub directory URL:

```text
$skill-installer install https://github.com/akanahs-dev/repo-memory/tree/main/skills/repo-memory
```

The `skills/repo-memory/` folder contains the installable payload. The repository
root keeps project governance, CI, issue templates, release notes, and branding
assets that do not need to be installed as part of the skill.

### For AI Agents

Read [`AGENTS.md`](./AGENTS.md) first for a concise entry point. Then read
[`skills/repo-memory/STANDARD.md`](./skills/repo-memory/STANDARD.md) for the portable standard and [`skills/repo-memory/SKILL.md`](./skills/repo-memory/SKILL.md)
for the skill workflow.

### For Humans

1. Read [`skills/repo-memory/STANDARD.md`](./skills/repo-memory/STANDARD.md) to understand what adoption means.
2. Read [`skills/repo-memory/SKILL.md`](./skills/repo-memory/SKILL.md) for the complete workflow.
3. Use [`skills/repo-memory/references/templates.md`](./skills/repo-memory/references/templates.md) as a copy-paste starting point for any new doc.
4. Use [`skills/repo-memory/references/existing-project-audit.md`](./skills/repo-memory/references/existing-project-audit.md) to audit an existing codebase.
5. Use [`skills/repo-memory/references/docs-structure-rules.md`](./skills/repo-memory/references/docs-structure-rules.md) to check naming and placement before committing.
6. Use [`skills/repo-memory/references/continuity-governance.md`](./skills/repo-memory/references/continuity-governance.md) when docs conflict, drift, work is interrupted, files need recovery, docs are renamed, or features need terminal-state handling.
7. Use [`skills/repo-memory/references/documentation-metadata-schema.md`](./skills/repo-memory/references/documentation-metadata-schema.md) to keep doc metadata consistent across agents.
8. Use [`skills/repo-memory/references/agent-integration-and-enforcement.md`](./skills/repo-memory/references/agent-integration-and-enforcement.md) to wire Repo Memory into Codex, GitHub Copilot, VS Code, Claude Code, OpenCode, cloud agents, hooks, and CI without creating duplicate sources of truth.

### Empty Repository Scaffold

Create the standard skeleton in a new or empty repo:

```bash
python3 skills/repo-memory/scripts/scaffold-docs.py /path/to/repo --with-agents
```

The scaffold includes `docs/intake/README.md` as a low-friction inbox for raw
brainstorms, copied chat notes, user-provided project dumps, and planning output
that still needs to be promoted into mapped owners.

This command is shown from the repository root. If using an installed skill,
run the script from that installed `repo-memory` skill directory.

Use `--project-name "<name>"` when the directory name is not the right project
name. Add `--include-user-stories` when users, actors, or journeys are already
known. The scaffold refuses to overwrite existing files unless `--force` is
passed.

### Validate Locally

Run the validator against this skill repo:

```bash
python3 skills/repo-memory/scripts/validate-docs.py --skill-repo .
```

Run the validator against a target repo that adopted the standard:

```bash
python3 skills/repo-memory/scripts/validate-docs.py --project-docs /path/to/repo --adoption-level baseline
```

Validate a partial adoption that only claims the continuity overlay:

```bash
python3 skills/repo-memory/scripts/validate-docs.py --project-docs /path/to/repo --adoption-level continuity
```

Use `--strict` when warnings such as generated artifacts, empty optional
deep-dive folders, duplicate ownership risks, inconsistent feature status
metadata, or stale terminal feature handoff text should fail the run:

```bash
python3 skills/repo-memory/scripts/validate-docs.py --project-docs /path/to/repo --adoption-level continuity --strict
```

This command is shown from the repository root. If using an installed skill,
run the script from that installed `repo-memory` skill directory.

### Forward Test Manually

Create disposable blind-test fixtures without running a child agent:

```bash
python3 skills/repo-memory/scripts/forward-test.py --fixture-only --keep
```

Run one live child-agent scenario when local Codex auth and token budget are
available:

```bash
python3 skills/repo-memory/scripts/forward-test.py --scenario interrupted-worktree --model gpt-5.4-mini --reasoning-effort low --keep
```

The harness writes child-agent stdout and final messages outside each fixture
repo so generated test logs do not contaminate scoring.

### Examples

- [`skills/repo-memory/examples/existing-project-after/`](./skills/repo-memory/examples/existing-project-after/) shows
  a compact target repo after adoption.
- [`skills/repo-memory/examples/existing-project-partial/`](./skills/repo-memory/examples/existing-project-partial/) shows
  partial adoption in a repo that keeps useful existing docs and adds only the
  missing canonical handoff surfaces.
- [`skills/repo-memory/examples/multi-agent-handoff/`](./skills/repo-memory/examples/multi-agent-handoff/) shows how
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

- **One owner per capability.** Avoid overlapping documentation systems by
  naming the one file or folder that owns decisions, contracts, setup,
  operations, feature state, and handoff state.
- **Markdown first.** The standard should be readable in the repo without a
  specific AI provider, editor, plugin, or service.
- **Two layers.** Keep stable project-wide docs concise, then add deep-dive docs
  for subsystems, features, designs, or flows that need more detail.
- **Evidence first.** Document what is confirmed before what is assumed, and mark
  inferred claims clearly.
- **Raw intake is not truth yet.** Use `docs/intake/` for messy brainstorms and
  planning dumps, then promote accepted facts into the normal docs before
  building from them.
- **Easy to resume.** A paused or interrupted session should leave enough notes
  for a future human or agent to continue safely.
- **Plans and reviews need provenance.** When a plan or specialist review shapes
  implementation, record who or what produced it, what evidence it used, and
  which outcomes were accepted.
- **Companion specs and plans stay linked.** When a workflow such as Obra
  Superpowers creates `docs/superpowers/specs/` or `docs/superpowers/plans/`,
  link those artifacts as evidence and promote accepted outcomes into Repo
  Memory docs.
- **Product context matters.** Goals, users, stories, use cases, and acceptance
  expectations are part of the engineering context, not separate from it.
- **History should not disappear.** Doc changes, conflicts, stale areas, renames,
  and abandoned or superseded work should be recorded when they matter.

## Default Docs Structure

The target docs layout for a repo that wants the full Repo Memory baseline.
Existing repos may satisfy some capabilities with existing files instead.

```text
docs/
├── README.md
├── intake/                             # raw brainstorms and planning dumps
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
├── requirements/
│   ├── functional-requirements.md
│   ├── non-functional-requirements.md
│   └── user-stories-and-use-cases.md  # optional
├── diagrams/                           # optional
├── designs/                            # optional
├── project-details/                    # optional
├── components/                         # optional
├── reviews/                            # optional
├── superpowers/                         # optional companion workflow artifacts
│   ├── specs/
│   └── plans/
├── ui-ux/                              # optional
└── features/
    ├── _template.md
    └── <feature-slug>.md
```

See [`skills/repo-memory/references/templates.md`](./skills/repo-memory/references/templates.md) for the full layout, templates, and placement rules.

Existing repos can reach this layout progressively. Keep useful pre-existing
docs during the transition, name them in the ownership map, then link or migrate
them deliberately instead of rewriting everything at once.

## Naming and Structure Rules

All file and folder names in `docs/` must follow strict kebab-case conventions. See [`skills/repo-memory/references/docs-structure-rules.md`](./skills/repo-memory/references/docs-structure-rules.md) for the complete ruleset.

## Versioning

The standard and skill use the same two-number version (`MAJOR.MINOR`) recorded
as `Version:` in [`skills/repo-memory/STANDARD.md`](./skills/repo-memory/STANDARD.md) and [`skills/repo-memory/SKILL.md`](./skills/repo-memory/SKILL.md).

| Change type                                              | Action          |
| -------------------------------------------------------- | --------------- |
| New content or non-breaking additions                    | Increment minor |
| Required baseline changes or structural workflow changes | Increment major |

Each version is tagged `vMAJOR.MINOR` and published as a GitHub Release. The release body is pulled from [`CHANGELOG.md`](./CHANGELOG.md). Update `CHANGELOG.md` in the same PR that bumps the version.

## Related Docs

- Portable standard: [`skills/repo-memory/STANDARD.md`](./skills/repo-memory/STANDARD.md)
- Full skill definition: [`skills/repo-memory/SKILL.md`](./skills/repo-memory/SKILL.md)
- Version history: [`CHANGELOG.md`](./CHANGELOG.md)
- AI agent instructions: [`AGENTS.md`](./AGENTS.md)
- OpenAI Codex guide: [`skills/repo-memory/agents/openai-codex.md`](./skills/repo-memory/agents/openai-codex.md)
- GitHub Copilot guide: [`skills/repo-memory/agents/github-copilot.md`](./skills/repo-memory/agents/github-copilot.md)
- Claude Code guide: [`skills/repo-memory/agents/claude-code.md`](./skills/repo-memory/agents/claude-code.md)
- OpenCode guide: [`skills/repo-memory/agents/opencode.md`](./skills/repo-memory/agents/opencode.md)
- File templates: [`skills/repo-memory/references/templates.md`](./skills/repo-memory/references/templates.md)
- Audit workflow: [`skills/repo-memory/references/existing-project-audit.md`](./skills/repo-memory/references/existing-project-audit.md)
- Agent integration and enforcement: [`skills/repo-memory/references/agent-integration-and-enforcement.md`](./skills/repo-memory/references/agent-integration-and-enforcement.md)
- Structure rules: [`skills/repo-memory/references/docs-structure-rules.md`](./skills/repo-memory/references/docs-structure-rules.md)
- Documentation metadata schema: [`skills/repo-memory/references/documentation-metadata-schema.md`](./skills/repo-memory/references/documentation-metadata-schema.md)
- Decision reconstruction: [`skills/repo-memory/references/decision-log-reconstruction.md`](./skills/repo-memory/references/decision-log-reconstruction.md)
- Continuity governance: [`skills/repo-memory/references/continuity-governance.md`](./skills/repo-memory/references/continuity-governance.md)
- Superpowers compatibility: [`skills/repo-memory/references/superpowers-compatibility.md`](./skills/repo-memory/references/superpowers-compatibility.md)
- Examples: [`skills/repo-memory/examples/README.md`](./skills/repo-memory/examples/README.md)
- Roadmap: [`ROADMAP.md`](./ROADMAP.md)
- Contributing: [`CONTRIBUTING.md`](./CONTRIBUTING.md)
