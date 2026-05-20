<!-- Target platform: Claude Code. Usage: use this guide when wiring the skill into Claude Code projects or when keeping CLAUDE.md aligned with the ownership-map workflow. -->

# Claude Code Integration Guide

This guide explains how to use the Repo Memory standard and skill with Claude Code
while keeping project facts in the single mapped owner that all agents share.

## Core Rule

Keep `CLAUDE.md` concise. It should point Claude Code to `docs/README.md` and
the `Canonical Ownership Map` instead of duplicating mutable architecture,
feature status, blockers, setup commands, decision rationale, contracts, or
handoff notes.

If the repo already has multiple agent entrypoints, keep them aligned and thin.
Preserve useful platform-specific instructions, but move mutable project facts
into the mapped owner so Claude is not resuming from a different truth than
other agents.

## Recommended `CLAUDE.md` Shape

```md
# Claude Project Instructions

This repo uses the Repo Memory standard.

When starting work:
1. Read `docs/README.md` for the Canonical Ownership Map.
2. Follow the mapped owner for project overview, architecture, decisions,
   contracts, setup, security, operations, and feature state.
3. Review `docs/intake/` if it contains raw brainstorms, project notes, or
   plans relevant to the work, then promote accepted facts into the mapped
   owner.
4. Check `docs/feature-registry.md`; when no task is assigned, pick the first
   `ready` row in `Next Work Queue`.
5. Check the active feature doc and follow `Resume Context`, `Validation`, and
   `Next Agent Handoff`.

When changing behavior:
- Update the mapped owner for each changed documentation capability.
- Update `docs/feature-registry.md` when next-work priority or readiness changes.
- Update the active feature doc.
- Update the mapped implementation-history owner for meaningful landed work.
- Update the mapped decision owner for durable technical choices.
- Update `docs/doc-health.md` when docs are verified, stale, renamed, or
  corrected.
- Update `docs/observability-and-instrumentation.md` when runtime signals,
  analytics, audit events, dashboards, or alerts change.
```

## When Starting on a Repo

1. Read `CLAUDE.md` or other repo-level instructions.
2. If the repo has a `docs/` folder, read `docs/README.md` first and follow the
   `Canonical Ownership Map`.
3. Check `docs/doc-health.md` for stale or conflicting docs.
4. Review `docs/intake/` when it contains raw brainstorms, project notes, or
   plans relevant to the work, then promote accepted facts into the mapped
   owner before implementation depends on them.
5. If the repo is empty or nearly empty, run `python3 <skill-dir>/scripts/scaffold-docs.py <repo> --with-agents`, resolving `<skill-dir>` to the installed `repo-memory` skill directory.
6. If the docs are missing, stale, or inconsistent, apply the workflow from
   [`SKILL.md`](../SKILL.md).

## When Resuming Work

1. Read the active `docs/features/<feature-slug>.md`.
2. If no task was assigned, choose the lowest-rank `ready` row in `docs/feature-registry.md`.
3. Check `Resume Context`, `Validation`, `Next Agent Handoff`, and
   `Exact Next Prompt`.
4. Prefer the docs over chat memory when they conflict, then update stale docs.
5. Check `docs/doc-health.md` before changing shared architecture or contracts.

## When Finishing Work

1. Update the active feature doc.
2. Update `docs/feature-registry.md` `Next Work Queue`.
3. Update the mapped implementation and decision owners when warranted.
4. Record verification status, stale areas, and duplicate-owner migrations in
   `docs/doc-health.md`.
5. Keep `CLAUDE.md`, `AGENTS.md`, and other agent entrypoints aligned to the
   same docs workflow.

## Related Docs

- Skill definition: [`SKILL.md`](../SKILL.md)
- OpenAI Codex guide: [`agents/openai-codex.md`](./openai-codex.md)
- GitHub Copilot guide: [`agents/github-copilot.md`](./github-copilot.md)
- OpenCode guide: [`agents/opencode.md`](./opencode.md)
- Agent integration and enforcement: [`references/agent-integration-and-enforcement.md`](../references/agent-integration-and-enforcement.md)
- File templates: [`references/templates.md`](../references/templates.md)
