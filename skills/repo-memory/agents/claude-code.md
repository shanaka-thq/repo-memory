<!-- Target platform: Claude Code. Usage: use this guide when wiring the skill into Claude Code projects or when keeping CLAUDE.md aligned with the ownership-map workflow. -->

# Claude Code Integration Guide

This guide extends the [common agent workflow](../references/agent-workflow-common.md) with Claude Code specifics.

## Core Rule

Keep `CLAUDE.md` concise. It should point Claude Code to `docs/README.md` and
the `Canonical Ownership Map` instead of duplicating mutable architecture,
feature status, blockers, setup commands, decision rationale, contracts, or
handoff notes.

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

## Platform-Specific Notes

- Claude Code uses `CLAUDE.md` as its primary instruction file. Keep it under 50 lines.
- When the repo also has `AGENTS.md`, align both to the same docs entrypoints.
- Claude Code supports `@file` references — use them to point at specific docs rather than copying content into `CLAUDE.md`.

## Related Docs

- Common agent workflow: [`references/agent-workflow-common.md`](../references/agent-workflow-common.md)
- Skill definition: [`SKILL.md`](../SKILL.md)
- Agent integration and enforcement: [`references/agent-integration-and-enforcement.md`](../references/agent-integration-and-enforcement.md)
- File templates: [`references/templates/`](../references/templates/) (per-template files)
