# Roadmap

This roadmap is directional. It describes the intended shape of the project,
not a guarantee of dates or release scope.

## Current Focus

- Keep the core skill platform-neutral.
- Treat Repo Memory as the portable standard and `skills/repo-memory/SKILL.md` as one implementation.
- Make the standard easier to evaluate through examples.
- Add lightweight validation that works in any repository.
- Keep platform-specific agent guides thin and linked to the same canonical
  documentation workflow.

## Near Term

- Keep `skills/repo-memory/STANDARD.md`, `skills/repo-memory/SKILL.md`, templates, examples, and validator behavior aligned.
- Expand `skills/repo-memory/examples/` with before-and-after documentation sets.
- Improve the empty-repo scaffold helper with richer metadata and optional
  baseline variants.
- Improve `skills/repo-memory/scripts/validate-docs.py` coverage for metadata, orphaned docs,
  feature statuses, and stale links.
- Add a blind, scenario-based forward-test harness that runs agents on
  disposable fixture repos and scores the resulting docs without leaking the
  expected answers.
- Trim `skills/repo-memory/SKILL.md` below the preferred skill-body size by
  moving lower-frequency detail into directly linked reference files.
- Add platform adapters for common agent tools.
- Add clearer migration guidance for repos that already have substantial docs.

## Later

- Add an audit command that reports missing baseline docs and likely stale
  areas without rewriting files.
- Explore optional packaging as a CLI, plugin, or MCP integration.
- Add richer examples for multi-agent handoff and concurrent work.

## Non-Goals

- Replacing `AGENTS.md`, `CLAUDE.md`, Copilot instructions, or editor-specific
  memory files.
- Becoming a full agent orchestration framework.
- Forcing every project into identical documentation depth.
