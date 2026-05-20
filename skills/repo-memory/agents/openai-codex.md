<!-- Target platform: OpenAI Codex and Codex CLI. Usage: use this guide when wiring the skill into Codex-driven repos or when resuming work with Codex after another agent. -->

# OpenAI Codex Integration Guide

This guide explains how to use the Repo Memory standard and skill with OpenAI Codex-style coding agents while keeping the project docs as the canonical cross-agent source of truth.

## Core Rule

Treat the maintained `docs/` tree as the canonical source of truth for architecture, requirements, feature state, implementation history, and resumable handoff context.

Agent-specific prompts, CLI instructions, or wrapper files should point into the docs set instead of duplicating mutable project facts.

## How Codex Agents Should Use This Skill

### When starting on a new or unfamiliar repo

1. Check for `AGENTS.md` and any repo-level agent instruction files.
2. If the repo has a `docs/` folder, read `docs/README.md` first.
3. Read `docs/project-overview.md`, `docs/architecture.md`, and `docs/feature-registry.md`.
4. If no task was assigned, pick the lowest-rank `ready` row in `docs/feature-registry.md` `Next Work Queue`.
5. If `docs/intake/` exists and contains raw brainstorms, project notes, or plans relevant to the work, review them and promote accepted facts into canonical docs before building from them.
6. If the repo is empty or nearly empty, run `python3 <skill-dir>/scripts/scaffold-docs.py <repo> --with-agents`, resolving `<skill-dir>` to the installed `repo-memory` skill directory.
7. If the docs are missing, stale, or inconsistent, apply the Repo Memory workflow from [`SKILL.md`](../SKILL.md).

### When resuming interrupted work

1. Run `git status --short` before editing if the previous session may have crashed, the prior agent is unknown, or the working tree is not clean.
2. Inspect unstaged diffs, staged diffs, and untracked files before deleting, overwriting, or continuing them.
3. Read the active `docs/features/<feature-slug>.md`.
4. Use `Resume Context`, `Next Agent Handoff`, and `Exact Next Prompt` as the primary resume surface.
5. Confirm linked deep-dive docs, validation notes, blockers, and files to inspect before changing code.
6. Prefer the docs over prior chat summaries if they conflict, then refresh the docs if they are stale.
7. Check `docs/doc-health.md` for known stale areas, conflicts, renames, and verification state when the repo has adopted the full standard.
8. When interrupted work is found, record what was found, what was verified, and the next safe step in the feature doc or `docs/doc-health.md`.

### When finishing a session

1. Update `docs/feature-registry.md`, especially `Next Work Queue`, when priority, readiness, or pickup instructions change.
2. Update the active feature doc, especially `Implementation Status`, `Validation`, `Resume Context`, and `Next Agent Handoff`.
3. Update `docs/implementation-log.md` if meaningful work landed.
4. Update `docs/decision-log.md` if a lasting technical choice changed.
5. Update `docs/doc-health.md` when docs were materially changed, verified, found stale, renamed, or superseded.
6. If the repo has multiple agent instruction files, keep them aligned to the same docs entrypoints before stopping.

## Recommended Codex Prompt Shape

When telling Codex to maintain project docs, include expectations like these:

- use the Repo Memory workflow from [`SKILL.md`](../SKILL.md)
- treat the `docs/` tree as canonical
- keep `docs/project-overview.md` current for project goal, problem statement, target users, success criteria, scope, and non-goals
- review `docs/intake/` when raw brainstorms or plans exist, then promote accepted outcomes into canonical docs
- keep active feature docs resumable for a different future agent
- keep `docs/feature-registry.md` ranked so a cloud agent can pick the first `ready` row
- keep `docs/doc-health.md` current for freshness, conflicts, renames, and terminal feature states
- keep `docs/observability-and-instrumentation.md` current for logs, metrics, traces, analytics, audit events, dashboards, and alerts
- update implementation and decision logs when warranted
- keep repo-level agent instruction files short and aligned to the docs workflow

## Repo Setup Guidance

If a target repo uses Codex together with other agents:

1. Add a short repo instruction block that points to `docs/README.md`, `docs/feature-registry.md`, and the active feature doc.
2. Avoid storing feature status, blockers, or next steps only in Codex-specific prompts.
3. Keep durable project knowledge in the maintained docs so Copilot, Codex, Claude, and humans can all resume from the same place.

## Related Docs

- Skill definition: [`SKILL.md`](../SKILL.md)
- GitHub Copilot guide: [`agents/github-copilot.md`](./github-copilot.md)
- OpenAI Agents SDK config: [`agents/openai.yaml`](./openai.yaml)
- File templates: [`references/templates.md`](../references/templates.md)
- Continuity governance: [`references/continuity-governance.md`](../references/continuity-governance.md)
