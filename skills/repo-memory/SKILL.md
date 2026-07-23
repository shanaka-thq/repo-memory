---
name: repo-memory
description: >-
  Persist feature state, ownership maps, and work queues as repo-native Markdown
  so any agent resumes where the last one stopped. Use when switching between
  agents or sessions and the next agent needs to know what's in progress, what's
  blocked, and what to pick up next. Also use when the user says "where did I
  leave off," "what's the status," "set up project memory," "what should I work
  on next," "handoff notes," "resume from last session," "shared work queue,"
  or "what's in flight." For planning, see /writing-plans or /wayfinder. For
  implementation, see /implement. For code review, see /code-review.
---

# Repo Memory Skill

Version: 3.2.1 <!-- x-release-please-version -->

> This version marker is managed by release-please. Do not edit it manually.

Repo Memory is the **state persistence layer** for AI-assisted repos. It tracks
where things live, what state they're in, and what's next — so any agent resumes
where the last one stopped.

It does NOT plan, review, spec, or implement. It connects the skills that do.

Use the smallest mode that fits the task.

## Modes

Load one mode file from `modes/` based on your task:

- **[Bootstrapper](modes/bootstrapper.md)**: first-time setup — create the ownership map, discover installed skills, configure typed slots.
- **[Maintainer](modes/maintainer.md)**: every session close — update feature frontmatter, link new artifacts.
- **[Auditor](modes/auditor.md)**: session start or on-demand — check for drift, stale docs, broken links.
- **[Generator](modes/generator.md)**: runs automatically after Maintainer writes — rebuild generated indexes.

## References (load only when needed)

Detailed rules and templates in `references/` — load only during doc maintenance:

- [docs-structure-rules.md](references/docs-structure-rules.md) — naming, placement, enforcement
- [templates.md](references/templates.md) — template index (per-template files in `references/templates/`)
- [compatible-skills.md](references/compatible-skills.md) — typed slots, known integrations, future-proofing
- [agent-workflow-common.md](references/agent-workflow-common.md) — shared start/resume/finish steps
- [STANDARD.md](STANDARD.md) — full portable standard (conformance levels, evidence order, status values)

## What Repo Memory Does (and Doesn't Do)

| Repo Memory does                          | Repo Memory does NOT do                                          |
| ----------------------------------------- | ---------------------------------------------------------------- |
| Track feature status and handoff state    | Write implementation plans (use /writing-plans, /wayfinder)      |
| Maintain a "what should I do next?" queue | Do code reviews (use /code-review)                               |
| Map where each kind of truth lives        | Create specs or requirements (use /to-spec, Kiro specs)          |
| Enable resumption across different agents | Replace agent-local memory or context                            |
| Link to outputs from other skills         | Duplicate what other skills already produce                      |
| Register artifact locations (typed slots) | Orchestrate or invoke other skills                               |

## How It Connects With Other Skills

Repo Memory is a **state persistence layer**, not a competing workflow:

```text
┌───────────────────────────────────────────┐
│         Repo Memory (state layer)         │
│  ownership map · feature docs · work queue│
└─────────────────────┬─────────────────────┘
                      │ agents read on start
      ┌───────────────┼───────────────────┐
      ▼               ▼                   ▼
┌───────────┐  ┌────────────┐  ┌───────────────┐
│ Planning  │  │ Building   │  │ Reviewing     │
│           │  │            │  │               │
│/wayfinder │  │/implement  │  │/code-review   │
│/to-tickets│  │/tdd        │  │/triage        │
│/to-spec   │  │/exec-plans │  │/improve       │
└─────┬─────┘  └─────┬──────┘  └───────┬───────┘
      │               │                 │
      └───────────────┼─────────────────┘
                      ▼ agents write on close
┌───────────────────────────────────────────┐
│         Repo Memory (state layer)         │
│  update status · link artifacts · next step│
└───────────────────────────────────────────┘
```

Each skill writes to its own location. RM doesn't interfere with the middle —
it owns the **start** (orient) and **end** (persist state) of each session.

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

## Related Skills

- **/writing-plans**, **/wayfinder**: Planning and decomposition — RM links their outputs, tracks status
- **/implement**, **/executing-plans**: Implementation — RM records progress before/after
- **/code-review**: Review — RM records that a review happened, links the output
- **/to-tickets**, **/triage**: Work tracking — RM's ownership map points to the tracker
- **/handoff**: Ephemeral session handoff — RM persists the durable parts in-repo
- **/domain-modeling**, **/grill-with-docs**: ADRs and context — RM maps where they live
- **/research**, **/improve**: Investigation outputs — RM registers their artifact locations
