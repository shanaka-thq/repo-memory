# GitHub Copilot Integration Guide

This guide explains how to use the Repo Memory standard and skill with GitHub
Copilot Coding Agent, VS Code Copilot, and related Copilot instruction
features.

## Overview

Repo Memory is designed to work alongside GitHub Copilot's custom instruction
files. Copilot surfaces can use repository instructions such as
`.github/copilot-instructions.md`, path-specific
`.github/instructions/*.instructions.md` files, VS Code `.instructions.md`
files, and agent instruction files such as `AGENTS.md` depending on the
environment.

Treat `docs/README.md` as the first map. Its `Canonical Ownership Map` names
the single owner for each documentation capability. Keep Copilot-specific
instruction files concise and point them to the same owners that other agents
use.

If the target repo already has `AGENTS.md`, `.github/copilot-instructions.md`,
`CLAUDE.md`, or other agent entrypoints, preserve useful platform guidance but
collapse mutable project facts into the mapped canonical owners. Thin aligned
entrypoints beat competing mini-manuals every time.

## How Copilot Agents Should Use This Skill

### When starting on a new or unfamiliar repo

1. Check for an existing `AGENTS.md` or `.github/copilot-instructions.md`.
2. If the repo has a `docs/` folder, read `docs/README.md` first and follow the
   `Canonical Ownership Map`.
3. Review `docs/intake/` when it contains raw brainstorms, project notes, or
   plans relevant to the work, then promote accepted facts into the mapped
   owner.
4. If the repo is empty or nearly empty, use `python3 <skill-dir>/scripts/scaffold-docs.py <repo> --with-agents` to create the baseline skeleton, resolving `<skill-dir>` to the installed `repo-memory` skill directory.
5. If docs are missing or stale, invoke the Repo Memory workflow via the default prompt in [`agents/openai.yaml`](./openai.yaml) or by reading [`SKILL.md`](../SKILL.md) directly.

### When resuming work

1. Read the relevant `docs/features/<feature-slug>.md` for the current feature.
2. Use `docs/README.md` to find the mapped owner for any architecture,
   contract, setup, operations, security, or decision facts touched by the work.
3. Check `docs/feature-registry.md` for status of related features and the ranked `Next Work Queue`.
4. If no task was assigned, pick the lowest-rank `ready` row in `Next Work Queue`.
5. Read `Resume Context`, `Validation`, and `Next Agent Handoff` in the feature doc.
6. Follow the `Exact Next Prompt` section when present.
7. Check `docs/doc-health.md` for known stale docs, conflicts, renamed docs, duplicate-owner migrations, and terminal feature states when available.

### When finishing a session

1. Update `docs/feature-registry.md`, especially `Next Work Queue`, when priority, readiness, or pickup instructions change.
2. Update the feature doc status, `Resume Context`, and `Next Agent Handoff` section.
3. Update the mapped implementation-history owner if meaningful work landed.
4. Update the mapped decision owner if a lasting technical choice changed.
5. Update `docs/doc-health.md` when docs were materially changed, verified, found stale, renamed, or superseded.
6. Confirm all new or changed docs follow the rules in [`references/docs-structure-rules.md`](../references/docs-structure-rules.md).
7. Keep `.github/copilot-instructions.md` or `AGENTS.md` aligned to the ownership map instead of storing mutable feature state there.

## Linking This Skill to a Target Repo

To make Copilot agents automatically apply this skill in a target repository, add an instruction to that repo's `AGENTS.md` or `.github/copilot-instructions.md`:

```md
## Documentation Standard

This project uses the Repo Memory standard to maintain its `docs/` folder.

When starting a session:
1. Read `docs/README.md` for the Canonical Ownership Map.
2. Follow the mapped owner for project overview, architecture, decisions,
   contracts, setup, operations, security, and feature state.
3. Review `docs/intake/` if raw brainstorms, project notes, or plans are
   relevant to the work, then promote accepted facts into the mapped owner.
4. Check `docs/feature-registry.md` for active work.
5. When no task is assigned, pick the first `ready` row in
   `docs/feature-registry.md` `Next Work Queue`.

When making changes:
- Keep `docs/features/<feature-slug>.md` current for the feature you are working on.
- Keep `docs/feature-registry.md` current as the ranked next-work queue.
- Follow naming and placement rules from `docs/docs-structure-rules.md` (copy or link `references/docs-structure-rules.md` into the target repo if needed).
- Update the mapped implementation-history owner when meaningful work lands.
- Update the mapped decision owner when an architectural choice changes.
- Update `docs/doc-health.md` when docs change materially, become stale, conflict, are renamed, or are superseded.
- Update `docs/observability-and-instrumentation.md` when logs, metrics, traces, analytics, audit events, dashboards, or alerts change.
- Do not duplicate mutable project facts in Copilot instruction files.
```

## Copilot-Specific Tips

### Using the default prompt

The default prompt from [`agents/openai.yaml`](./openai.yaml) works well as a starting point for a Copilot session. Paste it into the Copilot chat as-is, or adapt it for the specific work:

```text
Use $repo-memory to audit this repo, create or update docs/README.md with a Canonical Ownership Map, preserve strong existing ADRs/specs/runbooks/setup docs as owners, add only missing handoff surfaces, keep docs/feature-registry.md ranked with the next ready task, update the mapped owners for changed capabilities, avoid duplicate project facts in agent instructions, and leave resumable handoff notes.
```

### Copilot coding agent session workflow

When running as a Copilot Coding Agent (not interactive chat):

1. Read repo-level instructions and then `docs/README.md`.
2. Use the ownership map to determine which docs to create or update.
3. Use `references/templates.md` for any Repo Memory-owned doc that does not already exist.
4. Enforce naming and ownership rules from `references/docs-structure-rules.md` before committing.
5. Leave `Resume Context`, `Validation`, and `Next Agent Handoff` current in the active feature doc before the session ends.

### Handling repos without an `AGENTS.md`

If the target repo has no `AGENTS.md`:

1. Create one as the first documentation action.
2. Populate it with instructions for future agents to read `docs/README.md` and follow the ownership map.
3. Keep it concise — the full documentation lives in `docs/`, not in `AGENTS.md`.
4. Do not let `.github/copilot-instructions.md` become a second source of truth for active feature state.

### Handling repos with existing instruction files

If a target repo already has multiple agent instruction files:

1. Keep the files that the toolchain expects.
2. Reduce them to thin entrypoints that point to the same ownership map.
3. Preserve any useful tool-specific behavior instructions.
4. Move mutable project facts, feature state, blockers, and next steps into the
   mapped owners so Copilot, Codex, Claude, OpenCode, and humans resume from
   the same place.

## Integration with GitHub Actions

If the target repo has a CI workflow that lints or validates docs, ensure generated files conform to:

- kebab-case file and folder names
- no orphaned deep-dive docs
- a `Canonical Ownership Map` with one owner per capability
- all optional subfolders containing a `README.md` index
- raw `docs/intake/` source material promoted into mapped owners before implementation depends on it
- feature registry status values matching the allowed set
- `docs/doc-health.md` reflecting material documentation changes

See [`references/docs-structure-rules.md`](../references/docs-structure-rules.md) for the complete validation checklist.

## Related Docs

- Skill definition: [`SKILL.md`](../SKILL.md)
- File templates: [`references/templates.md`](../references/templates.md)
- Naming and placement rules: [`references/docs-structure-rules.md`](../references/docs-structure-rules.md)
- Continuity governance: [`references/continuity-governance.md`](../references/continuity-governance.md)
- Agent integration and enforcement: [`references/agent-integration-and-enforcement.md`](../references/agent-integration-and-enforcement.md)
- OpenAI Codex guide: [`agents/openai-codex.md`](./openai-codex.md)
- OpenAI Agents SDK config: [`agents/openai.yaml`](./openai.yaml)
