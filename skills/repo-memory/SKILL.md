---
name: repo-memory
description: Use when AI coding agents need cross-tool continuity, resumable feature state, or a shared work queue. Use when switching between agents (Claude, Codex, Copilot, Cursor, Kiro, etc.) and the next agent needs to know what happened, what's in progress, and what to pick up next — without re-reading the entire codebase or relying on tool-specific memory that doesn't transfer.
---

# Repo Memory Skill

Version: 3.2.0 <!-- x-release-please-version -->

> This version marker is managed by release-please. Do not edit it manually.

Repo Memory gives agents a shared, portable project memory that lives in your
repo as Markdown. It does NOT replace your planning skill, review skill, or spec
workflow. It fills the gap those tools leave: **what happened, what's next, and
where does everything live.**

Use the smallest mode that fits the task.

## Modes

Load one mode file from `modes/` based on your task:

- **[Maintainer](modes/maintainer.md)**: update feature state and ownership map during normal work.
- **[Bootstrapper](modes/bootstrapper.md)**: adopt an existing repo — create the ownership map and feature stubs.
- **[Auditor](modes/auditor.md)**: check for drift, stale docs, broken links, and duplicate ownership.
- **[Generator](modes/generator.md)**: rebuild generated indexes (feature registry, next-work-queue).

## References (load only when needed)

Detailed rules and templates in `references/` — load only during doc maintenance:

- [docs-structure-rules.md](references/docs-structure-rules.md) — naming, placement, enforcement
- [templates.md](references/templates.md) — copy-paste doc templates
- [agent-workflow-common.md](references/agent-workflow-common.md) — shared start/resume/finish steps
- [STANDARD.md](STANDARD.md) — full portable standard (conformance levels, evidence order, status values)

## What Repo Memory Does (and Doesn't Do)

| Repo Memory does                          | Repo Memory does NOT do                                          |
| ----------------------------------------- | ---------------------------------------------------------------- |
| Track feature status and handoff state    | Write implementation plans (use your planning skill)             |
| Maintain a "what should I do next?" queue | Do code reviews (use your review skill)                          |
| Map where each kind of truth lives        | Create specs or requirements (use Kiro specs, Superpowers, etc.) |
| Enable resumption across different agents | Replace agent-local memory or context                            |
| Link to outputs from other skills         | Duplicate what other skills already produce                      |

## Works Alongside Other Skills

Repo Memory is a **continuity layer**, not a competing workflow:

- **Superpowers plans/specs** → RM links them from the feature doc, records what was accepted
- **Kiro specs** → RM links the spec directory, tracks implementation status
- **Dedicated review skills** → RM records that a review happened and links the output
- **Agent-local memory** → RM captures the cross-agent bits that local memory can't share

## Always-Loaded Rules

1. Load only task-relevant docs.
2. Use `docs/README.md` (ownership map) as the context router.
3. Do not duplicate facts already owned by other files or tools.
4. Do not manually edit generated files.
5. Do not do planning, reviewing, or spec-writing — link to those outputs instead.
6. Mark inferred claims clearly.
7. Prefer small, reviewable changes.
8. Run validation and generation scripts when available.

Choose the mode, then load only that mode file.
