<!-- Target platform: OpenAI Codex and Codex CLI. Usage: use this guide when wiring the skill into Codex-driven repos or when resuming work with Codex after another agent. -->

# OpenAI Codex Integration Guide

This guide explains how to use the Repo Memory standard and skill with OpenAI
Codex-style coding agents while keeping each project fact in one mapped owner.

## Core Rule

Treat `docs/README.md` as the first map. Its `Canonical Ownership Map` names
the single owner for architecture, requirements, contracts, decisions, setup,
feature state, implementation history, and resumable handoff context.

Agent-specific prompts, CLI instructions, or wrapper files should point to the
mapped owners instead of duplicating mutable project facts.

If the target repo already has multiple agent instruction files, keep the ones
the tools need, but reduce them to aligned entrypoints. Preserve useful
tool-specific behavior notes and move mutable project state into the mapped
owners.

## How Codex Agents Should Use This Skill

### When starting on a new or unfamiliar repo

1. Check for `AGENTS.md` and any repo-level agent instruction files.
2. If the repo has a `docs/` folder, read `docs/README.md` first and follow the
   `Canonical Ownership Map`.
3. Read the mapped owners for project overview, architecture, and feature
   registry.
4. If no task was assigned, pick the lowest-rank `ready` row in `docs/feature-registry.md` `Next Work Queue`.
5. If `docs/intake/` exists and contains raw brainstorms, project notes, or
   plans relevant to the work, review them and promote accepted facts into the
   mapped owner before building from them.
6. If the repo is empty or nearly empty, run `python3 <skill-dir>/scripts/scaffold-docs.py <repo> --with-agents`, resolving `<skill-dir>` to the installed `repo-memory` skill directory.
7. If the docs are missing, stale, or inconsistent, apply the Repo Memory workflow from [`SKILL.md`](../SKILL.md).

### When resuming interrupted work

1. Run `git status --short` before editing if the previous session may have crashed, the prior agent is unknown, or the working tree is not clean.
2. Inspect unstaged diffs, staged diffs, and untracked files before deleting, overwriting, or continuing them.
3. Read the active `docs/features/<feature-slug>.md`.
4. Use `Resume Context`, `Next Agent Handoff`, and `Exact Next Prompt` as the primary resume surface.
5. Confirm linked deep-dive docs, validation notes, blockers, and files to inspect before changing code.
6. Prefer the docs over prior chat summaries if they conflict, then refresh the docs if they are stale.
7. Check `docs/doc-health.md` for known stale areas, conflicts,
   duplicate-owner migrations, renames, and verification state when available.
8. When interrupted work is found, record what was found, what was verified, and the next safe step in the feature doc or `docs/doc-health.md`.

### When finishing a session

1. Update `docs/feature-registry.md`, especially `Next Work Queue`, when priority, readiness, or pickup instructions change.
2. Update the active feature doc, especially `Implementation Status`, `Validation`, `Resume Context`, and `Next Agent Handoff`.
3. Update the mapped implementation-history owner if meaningful work landed.
4. Update the mapped decision owner if a lasting technical choice changed.
5. Update `docs/doc-health.md` when docs were materially changed, verified, found stale, renamed, or superseded.
6. If the repo has multiple agent instruction files, keep them aligned to the same docs entrypoints before stopping.

## Recommended Codex Prompt Shape

When telling Codex to maintain project docs, include expectations like these:

- use the Repo Memory workflow from [`SKILL.md`](../SKILL.md)
- follow `docs/README.md` and its `Canonical Ownership Map`
- keep `docs/project-overview.md` current for project goal, problem statement, target users, success criteria, scope, and non-goals
- review `docs/intake/` when raw brainstorms or plans exist, then promote accepted outcomes into mapped owners
- preserve strong existing ADRs, specs, runbooks, setup docs, security docs, and product docs as owners when they are healthy
- keep active feature docs resumable for a different future agent
- keep `docs/feature-registry.md` ranked so a cloud agent can pick the first `ready` row
- keep `docs/doc-health.md` current for freshness, conflicts, renames, and terminal feature states
- keep `docs/observability-and-instrumentation.md` current for logs, metrics, traces, analytics, audit events, dashboards, and alerts
- update implementation and decision logs when warranted
- keep repo-level agent instruction files short and aligned to the docs workflow

## Repo Setup Guidance

If a target repo uses Codex together with other agents:

1. Add a short repo instruction block that points to `docs/README.md`, the
   mapped feature registry owner, and the active feature doc.
2. Avoid storing feature status, blockers, or next steps only in Codex-specific prompts.
3. Keep durable project knowledge in the mapped owners so Copilot, Codex,
   Claude, OpenCode, and humans can all resume from the same place.

## Related Docs

- Skill definition: [`SKILL.md`](../SKILL.md)
- GitHub Copilot guide: [`agents/github-copilot.md`](./github-copilot.md)
- OpenAI Agents SDK config: [`agents/openai.yaml`](./openai.yaml)
- OpenCode guide: [`agents/opencode.md`](./opencode.md)
- Agent integration and enforcement: [`references/agent-integration-and-enforcement.md`](../references/agent-integration-and-enforcement.md)
- File templates: [`references/templates.md`](../references/templates.md)
- Continuity governance: [`references/continuity-governance.md`](../references/continuity-governance.md)
