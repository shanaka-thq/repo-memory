# Agent Workflow (Common)

Shared workflow steps for all agents using Repo Memory. Platform-specific adapters in `agents/` extend this with tool-specific guidance.

## When Starting on a Repo

1. Check for agent instruction files (`AGENTS.md`, `.github/copilot-instructions.md`, `CLAUDE.md`, etc.).
2. If the repo has `docs/`, read `docs/README.md` first and follow the `Canonical Ownership Map`.
3. Read the mapped owners for project overview, architecture, and feature registry.
4. If no task was assigned, check the mapped work-queue owner (typically `docs/generated/next-work-queue.md`) and pick the lowest-rank `ready` row.
5. If `docs/intake/` exists and contains raw brainstorms, project notes, or plans relevant to the work, review them and promote accepted facts into the mapped owner before building from them.
6. If the repo is empty or nearly empty, run `python3 <skill-dir>/scripts/scaffold-docs.py <repo> --with-agents`.
7. If docs are missing, stale, or inconsistent, apply the workflow from [`SKILL.md`](../SKILL.md).

## When Resuming Interrupted Work

1. Run `git status --short` before editing if the previous session may have crashed or the working tree is not clean.
2. Inspect unstaged diffs, staged diffs, and untracked files before deleting, overwriting, or continuing them.
3. Read the active `docs/features/<feature-slug>.md`.
4. Use `Resume Context`, `Next Agent Handoff`, and `Exact Next Prompt` as the primary resume surface.
5. Confirm linked deep-dive docs, validation notes, blockers, and files to inspect before changing code.
6. Prefer the docs over prior chat summaries if they conflict, then refresh the docs if stale.
7. Check `docs/doc-health.md` for known stale areas, conflicts, duplicate-owner migrations, renames, and verification state.
8. When interrupted work is found, record what was found, what was verified, and the next safe step in the feature doc or `docs/doc-health.md`.

## When Finishing a Session

1. Update `docs/features/<feature-slug>.md` when status, priority, readiness, or pickup instructions change, then run `python3 <skill-dir>/scripts/generate-indexes.py <repo>` to regenerate `docs/generated/feature-registry.md` and `docs/generated/next-work-queue.md`.
2. Update the active feature doc: status, `Implementation Status`, `Validation`, `Resume Context`, and `Next Agent Handoff`.
3. Update the mapped implementation-history owner if meaningful work landed.
4. Update the mapped decision owner if a lasting technical choice changed.
5. Update `docs/doc-health.md` when docs were materially changed, verified, found stale, renamed, or superseded.
6. Keep agent-specific instruction files aligned to the same docs entrypoints.

## Cross-Agent Alignment

- Keep durable project facts in mapped canonical owners, not in agent instruction files.
- Agent instruction files should be thin entrypoints pointing to the ownership map.
- If multiple agent entrypoints exist, keep them aligned to the same documentation workflow.
- Do not duplicate mutable project facts across agent files.
