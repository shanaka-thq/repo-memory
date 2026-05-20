# Agent Integration and Enforcement

Use this reference when adopting Repo Memory in a repo that may be touched by
multiple coding agents, cloud agents, IDE assistants, or local CLI tools. It
explains which files to add, why they exist, what different tools will likely
read, and what still needs validation or hooks.

## Core Model

Repo Memory has three enforcement layers:

| Layer | Purpose | Reliability |
| --- | --- | --- |
| Canonical docs | Store current project truth, ownership, feature state, and handoff context | High when maintained and validated |
| Thin agent adapters | Tell tools where the ownership map lives and how to update mapped owners | Helpful but not hard enforcement |
| Validator, CI, and hooks | Detect missing owners, stale handoff, duplicate ownership, and required updates | Strongest practical enforcement |

Installing the skill helps an agent run the workflow when it has access to that
skill. It does not automatically make every future agent update documentation.
For reliable behavior, commit thin instruction files and validation checks into
the target repository.

## Strict No-Duplicate Rule

Agent instruction files may duplicate routing instructions only.

Allowed in multiple agent files:

- read `docs/README.md` first
- use the canonical ownership map
- update the active feature doc when behavior changes
- keep agent files thin

Not allowed in multiple agent files:

- current architecture facts
- build or test commands if another doc owns them
- ADR rationale
- API contracts
- feature status, blockers, or next steps
- implementation history

If an agent file needs a fact, it should point to the owner instead of copying
the fact.

## Recommended Adapter Stack

Use the smallest set that covers the tools in the repo.

| Situation | Recommended files | Why |
| --- | --- | --- |
| Any multi-agent repo | `AGENTS.md`, `docs/README.md`, `docs/feature-registry.md`, `docs/doc-health.md` | `AGENTS.md` is a broad cross-agent entrypoint, while Repo Memory stores durable state in docs. |
| Claude Code is used | `CLAUDE.md` importing or pointing to `AGENTS.md` | Claude Code reads `CLAUDE.md`; use it as a router, not a duplicate manual. |
| GitHub Copilot or VS Code is used | `.github/copilot-instructions.md` plus optional `.github/instructions/*.instructions.md` | Copilot and VS Code use these as repository and path-specific instructions. |
| OpenCode is used | `AGENTS.md`, optionally `opencode.json` with shared instruction paths | OpenCode reads `AGENTS.md` and can combine configured instruction files. |
| Cloud agents pick work without a human prompt | `docs/feature-registry.md` with `Next Work Queue` | The first `ready` row becomes the default pickup task. |
| Docs must not drift | CI running `validate-docs.py`, plus optional hooks | Instructions guide behavior; validation catches missed updates. |

## Why Each Piece Exists

| Piece | Required when | Why it exists | What it must not become |
| --- | --- | --- | --- |
| `docs/README.md` | Any Level 1 or higher adoption | Owns the documentation map and tells agents which file owns each capability. | A giant summary that copies every other doc. |
| `Canonical Ownership Map` | Any Level 1 or higher adoption | Prevents duplicate ADR, API, setup, runbook, security, and feature-state owners. | A vague index without single owners. |
| `docs/feature-registry.md` | Any repo with active or future work | Gives agents a ranked queue and feature status without prior chat context. | A second implementation log. |
| `docs/features/<feature-slug>.md` | Any paused, risky, or multi-session feature | Holds resumable context, validation, files touched, and next handoff. | A replacement for ADRs, specs, or broad architecture docs. |
| `docs/doc-health.md` | Any Level 1 or higher adoption | Records stale docs, conflicts, verification, duplicate-owner migrations, and unknowns. | A place to hide unresolved product decisions without owners. |
| `AGENTS.md` | Multi-agent repos and Codex/OpenCode repos | Gives common startup instructions and points to the ownership map. | A duplicate project manual. |
| `.github/copilot-instructions.md` | GitHub Copilot or VS Code workspaces | Routes Copilot to the same ownership map and update rules. | A separate Copilot-only source of truth. |
| `CLAUDE.md` | Claude Code repos | Imports or points to shared instructions because Claude Code reads this file. | A fork of `AGENTS.md` with copied facts. |
| `opencode.json` | OpenCode repos that need extra shared instruction files | Lets OpenCode combine reusable instruction files without copying them. | A second rules hierarchy that competes with `AGENTS.md`. |
| CI or hooks | Repos where doc drift is costly | Catches missing owners, broken links, stale handoff, and malformed queues. | The only place where documentation behavior is described. |

## Canonical Ownership Map

Every adopted repo should have a `Canonical Ownership Map`, usually in
`docs/README.md`.

```md
## Canonical Ownership Map

| Capability | Canonical owner | Supporting docs | Notes |
| --- | --- | --- | --- |
| Decisions and rationale | `docs/adr/` | `docs/README.md` | ADRs are canonical; do not copy decisions into `docs/decision-log.md`. |
| Interfaces and contracts | `openapi.yaml` | `docs/interfaces-and-contracts.md` | OpenAPI is canonical; docs summarize how to use it. |
| Active feature handoff | `docs/features/search-refresh.md` | `docs/feature-registry.md` | Repo Memory owns resumable state. |
| Local development | `CONTRIBUTING.md` | `README.md` | Do not duplicate setup commands elsewhere. |
```

Use the map to answer one question quickly: if a fact changes, which single
file or folder must be updated?

## Tool Behavior

### Codex

Codex discovers `AGENTS.md` as project guidance. For Repo Memory, make
`AGENTS.md` a thin router to the ownership map, feature registry, active feature
docs, and validator command. Do not keep mutable project facts in `AGENTS.md`.

Reference: [OpenAI Codex AGENTS.md guide](https://developers.openai.com/codex/guides/agents-md).

### GitHub Copilot and VS Code

GitHub Copilot supports repository instructions in
`.github/copilot-instructions.md`, path-specific
`.github/instructions/*.instructions.md` files, and agent instruction files
such as `AGENTS.md`, though support differs by Copilot surface. VS Code
automatically detects `.github/copilot-instructions.md` in the workspace root
and recommends `AGENTS.md` when multiple AI agents share a workspace.

Use `.github/copilot-instructions.md` as a short router:

```md
# Copilot Instructions

This repo uses Repo Memory.

- Read `docs/README.md` for the canonical ownership map.
- Do not duplicate current project facts in this file.
- When behavior changes, update the mapped canonical owner.
- Keep active feature state in `docs/features/<feature-slug>.md`.
- Keep the next pickup task in `docs/feature-registry.md`.
- Run `python3 skills/repo-memory/scripts/validate-docs.py --project-docs . --adoption-level continuity` before finishing docs-only changes when available.
```

References: [GitHub Copilot custom instructions](https://docs.github.com/en/copilot/concepts/prompting/response-customization) and [VS Code custom instructions](https://code.visualstudio.com/docs/copilot/customization/custom-instructions).

### Claude Code

Claude Code reads `CLAUDE.md`, not `AGENTS.md`. If a repo already has
`AGENTS.md`, create a tiny `CLAUDE.md` that imports or points to it.

```md
@AGENTS.md

## Claude Code

Use `docs/README.md` as the canonical ownership map. Do not copy mutable
project facts into `CLAUDE.md`.
```

Claude Code documentation describes `CLAUDE.md` as context rather than hard
enforcement. If a behavior must happen at a fixed lifecycle point, use hooks
where available.

References: [Claude Code memory](https://code.claude.com/docs/en/memory) and [Claude Code hooks](https://code.claude.com/docs/en/hooks).

### OpenCode

OpenCode reads `AGENTS.md` for project rules and can also combine configured
instruction files through `opencode.json`.

Use `AGENTS.md` as the primary router. If the repo uses `opencode.json`, point
it at shared instruction files instead of copying their contents:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": ["AGENTS.md", "docs/README.md"]
}
```

Reference: [OpenCode rules](https://dev.opencode.ai/docs/rules/).

## Scenarios

### New or Empty Repo

Use when there is no trusted documentation owner yet.

1. Run the scaffold helper.
2. Keep generated facts marked `TODO`, `unknown`, or explicitly inferred.
3. Fill `docs/README.md` with the canonical ownership map.
4. Add thin agent adapters for the tools the team actually uses.
5. Validate with baseline mode once the generated baseline is meant to be maintained.

```bash
python3 skills/repo-memory/scripts/scaffold-docs.py /path/to/repo --with-agents
python3 skills/repo-memory/scripts/validate-docs.py --project-docs /path/to/repo --adoption-level baseline
```

### Existing Repo With Good Docs

Use when the repo already has ADRs, runbooks, API specs, README setup docs, or
other useful documentation.

1. Inventory existing docs before writing new ones.
2. Create or update `docs/README.md` with the ownership map.
3. Name existing docs as canonical owners where they are still trustworthy.
4. Add only missing continuity surfaces first: feature registry, doc health, and active feature docs.
5. Validate with continuity mode.

```bash
python3 skills/repo-memory/scripts/validate-docs.py --project-docs /path/to/repo --adoption-level continuity
```

### Existing Repo With Stale or Conflicting Docs

Use when docs disagree with code or with each other.

1. Resolve current behavior from code, tests, schemas, runtime config, and explicit user statements.
2. Update the canonical owner only.
3. Mark stale supporting docs as superseded or link them to the owner.
4. Record the correction in the doc-health owner.
5. Avoid creating a second summary that competes with the owner.

### Feature Work

Use when behavior, contracts, UX, runtime signals, or architecture changes.

1. Read the ownership map.
2. Read the active feature doc and feature registry.
3. Update only the mapped owner for each changed capability.
4. Update the feature doc with implementation status, validation, files touched, and next handoff.
5. Update the feature registry when priority, readiness, or next safe step changes.

### Cloud Agent Pickup

Use when a cloud agent is expected to choose work without a detailed human
prompt.

1. Keep `docs/feature-registry.md` committed.
2. Keep `Next Work Queue` ranked.
3. Make the first `ready` row safe to start from the linked canonical doc.
4. Use `verify-first` when the next agent should inspect before editing.
5. Use `needs-human` when product direction is missing.
6. Use `blocked` when the agent should not proceed.

### Planning Dumps and Brainstorms

Use when a human or planning agent produces messy project material.

1. Put raw material under `docs/intake/`.
2. Treat intake as evidence, not truth.
3. Promote accepted facts into the mapped canonical owner before implementation depends on them.
4. Record unresolved high-impact questions in doc health or the owning feature doc.

## Hooks and CI

Instruction files guide agents, but they are not enough for strict compliance.
Use validation and hooks when missed updates would be costly.

Good CI checks:

- relative links are valid
- adoption-level required docs exist
- the ownership map has no duplicate capability rows
- feature registry readiness values are valid
- terminal feature docs do not contain stale interrupted-work language
- generated artifacts are not left behind

Good hook uses:

- remind an agent at session start to read the ownership map
- block or warn when Markdown docs changed without doc-health updates
- run `validate-docs.py` before session end or commit

Hooks are tool-specific. Prefer CI for shared team guarantees because it runs
outside any one agent's memory or instruction system.

## Setup Recipes

### Minimal Multi-Agent Setup

```text
AGENTS.md
docs/
├── README.md              # ownership map
├── doc-health.md
├── feature-registry.md
└── features/
    └── <feature-slug>.md
```

Use this when the repo already has good docs and only needs shared agent
continuity.

### Full Baseline Setup

Use the default scaffold when the repo has no strong existing docs or wants a
complete maintained docs baseline.

```bash
python3 skills/repo-memory/scripts/scaffold-docs.py /path/to/repo --with-agents
```

### Tool Adapter Setup

```text
AGENTS.md                         # shared router
CLAUDE.md                         # imports or points to AGENTS.md
.github/copilot-instructions.md   # Copilot and VS Code router
opencode.json                     # optional OpenCode instruction include
```

Keep all adapters short. Their job is to route agents to the canonical owners,
not to become more places where project truth can drift.
