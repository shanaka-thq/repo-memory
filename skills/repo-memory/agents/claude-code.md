<!-- Target platform: Claude Code. Usage: use this guide when wiring the skill into Claude Code projects or when keeping CLAUDE.md aligned with the canonical docs workflow. -->

# Claude Code Integration Guide

This guide explains how to use the Repo Memory standard and skill with Claude Code
while keeping the project docs as the canonical cross-agent source of truth.

## Core Rule

Keep `CLAUDE.md` concise. It should point Claude Code to the maintained `docs/`
tree instead of duplicating mutable architecture, feature status, blockers, or
handoff notes.

## Recommended `CLAUDE.md` Shape

```md
# Claude Project Instructions

This repo uses the Repo Memory standard.

When starting work:
1. Read `docs/README.md`.
2. Read `docs/project-overview.md` and `docs/architecture.md`.
3. Review `docs/intake/` if it contains raw brainstorms, project notes, or
   plans relevant to the work, then promote accepted facts into canonical docs.
4. Check `docs/feature-registry.md` and the active feature doc.
5. Follow `Resume Context`, `Validation`, and `Next Agent Handoff`.

When changing behavior:
- Update affected baseline docs.
- Update the active feature doc.
- Update `docs/implementation-log.md` for meaningful landed work.
- Update `docs/decision-log.md` for durable technical choices.
- Update `docs/doc-health.md` when docs are verified, stale, renamed, or
  corrected.
- Update `docs/observability-and-instrumentation.md` when runtime signals,
  analytics, audit events, dashboards, or alerts change.
```

## When Starting on a Repo

1. Read `CLAUDE.md` or other repo-level instructions.
2. If the repo has a `docs/` folder, read `docs/README.md` first.
3. Check `docs/doc-health.md` for stale or conflicting docs.
4. Review `docs/intake/` when it contains raw brainstorms, project notes, or plans relevant to the work.
5. If the repo is empty or nearly empty, run `python3 <skill-dir>/scripts/scaffold-docs.py <repo> --with-agents`, resolving `<skill-dir>` to the installed `repo-memory` skill directory.
6. If the docs are missing, stale, or inconsistent, apply the workflow from
   [`SKILL.md`](../SKILL.md).

## When Resuming Work

1. Read the active `docs/features/<feature-slug>.md`.
2. Check `Resume Context`, `Validation`, `Next Agent Handoff`, and
   `Exact Next Prompt`.
3. Prefer the docs over chat memory when they conflict, then update stale docs.
4. Check `docs/doc-health.md` before changing shared architecture or contracts.

## When Finishing Work

1. Update the active feature doc.
2. Update implementation and decision logs when warranted.
3. Record verification status and stale areas in `docs/doc-health.md`.
4. Keep `CLAUDE.md`, `AGENTS.md`, and other agent entrypoints aligned to the
   same docs workflow.

## Related Docs

- Skill definition: [`SKILL.md`](../SKILL.md)
- OpenAI Codex guide: [`agents/openai-codex.md`](./openai-codex.md)
- GitHub Copilot guide: [`agents/github-copilot.md`](./github-copilot.md)
- File templates: [`references/templates.md`](../references/templates.md)
