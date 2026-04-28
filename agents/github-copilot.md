# GitHub Copilot Integration Guide

This guide explains how to use the Repo Memory standard and skill with GitHub Copilot Coding Agent and related GitHub Copilot features.

## Overview

Repo Memory is designed to work alongside GitHub Copilot's agent instruction files. When Copilot agents start a session in a repository, they read `AGENTS.md` (or `.github/copilot-instructions.md`) first. The standard produces and maintains documentation that those instruction files can reference directly, creating a tight feedback loop between living project documentation and agent behavior.

Treat the maintained `docs/` tree as the canonical cross-agent source of truth. Keep Copilot-specific instruction files concise and point them to the same docs entrypoints that other agents use.

## How Copilot Agents Should Use This Skill

### When starting on a new or unfamiliar repo

1. Check for an existing `AGENTS.md` or `.github/copilot-instructions.md`.
2. If the repo has a `docs/` folder, read `docs/README.md` first.
3. If docs are missing or stale, invoke the Repo Memory workflow via the default prompt in [`agents/openai.yaml`](./openai.yaml) or by reading [`SKILL.md`](../SKILL.md) directly.

### When resuming work

1. Read the relevant `docs/features/<feature-slug>.md` for the current feature.
2. Check `docs/feature-registry.md` for status of related features.
3. Read `Resume Context`, `Validation`, and `Next Agent Handoff` in the feature doc.
4. Follow the `Exact Next Prompt` section when present.
5. Check `docs/doc-health.md` for known stale docs, conflicts, renamed docs, and terminal feature states when available.

### When finishing a session

1. Update the feature doc status, `Resume Context`, and `Next Agent Handoff` section.
2. Update `docs/implementation-log.md` if meaningful work landed.
3. Update `docs/decision-log.md` if a lasting technical choice changed.
4. Update `docs/doc-health.md` when docs were materially changed, verified, found stale, renamed, or superseded.
5. Confirm all new or changed docs follow the rules in [`references/docs-structure-rules.md`](../references/docs-structure-rules.md).
6. Keep `.github/copilot-instructions.md` or `AGENTS.md` aligned to the canonical docs flow instead of storing mutable feature state there.

## Linking This Skill to a Target Repo

To make Copilot agents automatically apply this skill in a target repository, add an instruction to that repo's `AGENTS.md` or `.github/copilot-instructions.md`:

```md
## Documentation Standard

This project uses the Repo Memory standard to maintain its `docs/` folder.

When starting a session:
1. Read `docs/README.md` for the documentation map.
2. Read `docs/project-overview.md` and `docs/architecture.md` to orient.
3. Check `docs/feature-registry.md` for active work.

When making changes:
- Keep `docs/features/<feature-slug>.md` current for the feature you are working on.
- Follow naming and placement rules from `docs/docs-structure-rules.md` (copy or link `references/docs-structure-rules.md` into the target repo if needed).
- Update `docs/implementation-log.md` when meaningful work lands.
- Update `docs/decision-log.md` when an architectural choice changes.
- Update `docs/doc-health.md` when docs change materially, become stale, conflict, are renamed, or are superseded.
- Update `docs/observability-and-instrumentation.md` when logs, metrics, traces, analytics, audit events, dashboards, or alerts change.
- Treat the `docs/` tree as the canonical source of truth for handoff state across agents.
```

## Copilot-Specific Tips

### Using the default prompt

The default prompt from [`agents/openai.yaml`](./openai.yaml) works well as a starting point for a Copilot session. Paste it into the Copilot chat as-is, or adapt it for the specific work:

```text
Use $repo-memory to audit this repo, backfill or maintain the full Repo Memory baseline documentation structure, treat the docs tree as the canonical source of truth across agent instruction files, keep project goal/problem/users/success criteria current, cover local tooling, data model, and observability details, preserve existing diagram assets, prefer Mermaid docs for new text-centric diagrams, add thorough user stories and use cases, design, UI/UX, diagram, and project-specific or feature/component deep-dive docs when warranted, and keep feature tracking, resumable handoff notes, and exact next-step context current.
```

### Copilot coding agent session workflow

When running as a Copilot Coding Agent (not interactive chat):

1. Read `AGENTS.md` automatically at session start.
2. Use the skill workflow from `SKILL.md` to determine which docs to create or update.
3. Use `references/templates.md` for any doc that does not already exist.
4. Enforce naming rules from `references/docs-structure-rules.md` before committing.
5. Leave `Resume Context`, `Validation`, and `Next Agent Handoff` current in the active feature doc before the session ends.

### Handling repos without an `AGENTS.md`

If the target repo has no `AGENTS.md`:

1. Create one as the first documentation action.
2. Populate it with instructions for future agents to read `docs/README.md` and the relevant feature doc.
3. Keep it concise — the full documentation lives in `docs/`, not in `AGENTS.md`.
4. Do not let `.github/copilot-instructions.md` become a second source of truth for active feature state.

## Integration with GitHub Actions

If the target repo has a CI workflow that lints or validates docs, ensure generated files conform to:

- kebab-case file and folder names
- no orphaned deep-dive docs
- all optional subfolders containing a `README.md` index
- feature registry status values matching the allowed set
- `docs/doc-health.md` reflecting material documentation changes

See [`references/docs-structure-rules.md`](../references/docs-structure-rules.md) for the complete validation checklist.

## Related Docs

- Skill definition: [`SKILL.md`](../SKILL.md)
- Agent instructions for this repo: [`AGENTS.md`](../AGENTS.md)
- File templates: [`references/templates.md`](../references/templates.md)
- Naming and placement rules: [`references/docs-structure-rules.md`](../references/docs-structure-rules.md)
- Continuity governance: [`references/continuity-governance.md`](../references/continuity-governance.md)
- OpenAI Codex guide: [`agents/openai-codex.md`](./openai-codex.md)
- OpenAI Agents SDK config: [`agents/openai.yaml`](./openai.yaml)
