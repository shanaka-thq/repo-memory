# Scenario Simulations

What Repo Memory actually produces in representative scenarios. Each simulation shows the exact files created and their content.

---

## Scenario 1: Empty Repo

**State:** Fresh `npx create-next-app`, has README.md and package.json. No docs.

**RM creates:**

```text
docs/
├── README.md
└── features/
    └── _template.md
```

**docs/README.md:**

```md
# Project Documentation

## Canonical Ownership Map

| Capability       | Owner                               | Notes                                 |
| ---------------- | ----------------------------------- | ------------------------------------- |
| Project overview | `README.md` (root)                  | Update when project goals clarify     |
| Architecture     | TODO                                | Add when system shape emerges         |
| Decisions        | TODO                                | Add when first durable choice is made |
| Feature state    | `docs/features/*.md`                | RM-managed                            |
| Work queue       | `docs/generated/next-work-queue.md` | Auto-generated                        |
```

**What RM does NOT create:** architecture.md, decision-log.md, requirements.md, testing-strategy.md, or any other baseline doc. Those don't exist yet because there's nothing to document.

---

## Scenario 7: Good Docs, No Handoff Surface

**State:** Mature project with solid README, CONTRIBUTING.md, `docs/architecture.md`, `docs/adr/` folder with 5 ADRs, OpenAPI spec. Currently 2 features in progress but no way to tell the next agent what to pick up.

**RM creates:**

```text
docs/
├── README.md          ← adds ownership map section only
├── features/
│   ├── auth-refresh.md
│   └── search-v2.md
└── generated/
    ├── feature-registry.md
    └── next-work-queue.md
```

**Added to existing docs/README.md:**

```md
## Canonical Ownership Map

| Capability        | Owner                               | Notes             |
| ----------------- | ----------------------------------- | ----------------- |
| Project overview  | `README.md` (root)                  | Existing, current |
| Architecture      | `docs/architecture.md`              | Existing, current |
| Decisions         | `docs/adr/`                         | 5 ADRs, healthy   |
| API contracts     | `openapi.yaml`                      | Existing, current |
| Local development | `CONTRIBUTING.md`                   | Existing          |
| Feature state     | `docs/features/*.md`                | RM-managed        |
| Work queue        | `docs/generated/next-work-queue.md` | Auto-generated    |
```

**docs/features/auth-refresh.md:**

```yaml
---
id: auth-refresh
title: Token Refresh Flow
status: in_progress
ready: ready
next_safe_step: "Wire refresh endpoint to session store, run auth integration tests"
priority: 1
owner: backend
last_updated: 2026-06-11
---
```

```md
## Context

Implementing token refresh to replace the current force-logout-on-expiry behavior.

## What's Done

- Refresh endpoint exists at `/api/auth/refresh`
- Token rotation logic implemented
- Unit tests passing

## What's Next

Wire the endpoint into the session store middleware so it's called automatically on 401.

## Blockers

None.
```

**What RM does NOT touch:** architecture.md, ADRs, CONTRIBUTING.md, OpenAPI spec — all left untouched.

---

## Scenario 11: No Docs, Large Codebase

**State:** 50+ source files, tests, CI pipeline, Docker setup. Zero documentation.

**RM creates:**

```text
docs/
├── README.md
└── features/
    └── _template.md
```

**docs/README.md:**

```md
# Project Documentation

## Canonical Ownership Map

| Capability        | Owner                               | Notes                                  |
| ----------------- | ----------------------------------- | -------------------------------------- |
| Project overview  | TODO                                | No docs exist                          |
| Architecture      | TODO                                | Inferable from code but not documented |
| Decisions         | TODO                                | No ADRs or decision records            |
| API contracts     | TODO                                | Handlers exist but no spec             |
| Local development | TODO                                | Scripts exist, no prose docs           |
| Testing           | TODO                                | Tests exist, no strategy doc           |
| Feature state     | `docs/features/*.md`                | RM-managed                             |
| Work queue        | `docs/generated/next-work-queue.md` | Auto-generated                         |
```

**What RM does NOT do:**

- Does NOT try to reconstruct architecture from code
- Does NOT generate requirements from test names
- Does NOT create decision-log.md with "inferred" decisions
- Does NOT produce 15 doc files from code analysis

It creates the map, marks gaps as TODO, and adds feature tracking. Filling the gaps is a separate effort (potentially using `acquire-codebase-knowledge` or similar skills).

---

## Scenario 14: Agent Crashed Mid-Feature

**State:** `git status` shows 3 modified files, 1 untracked file. Feature doc exists but says `status: in_progress` with a `next_safe_step` that's already partially done.

**RM updates:**

**docs/features/payment-flow.md** (frontmatter change):

```yaml
---
id: payment-flow
title: Stripe Payment Integration
status: in_progress
ready: verify-first
next_safe_step: "Inspect uncommitted changes in src/payments/. Previous agent modified 3 files — verify state before continuing."
priority: 1
last_updated: 2026-06-11
---
```

**Added to the feature doc:**

```md
## Recovery Notes (2026-06-11)

Previous session interrupted. Found:

- Modified: `src/payments/stripe.ts`, `src/payments/webhook.ts`, `tests/payments.test.ts`
- Untracked: `src/payments/refund.ts` (appears partially implemented)
- Staged: nothing
- Tests: not run since changes

Preserved all uncommitted work. Next agent should:

1. Read the diff in the 3 modified files
2. Run `npm test -- --filter payments` to see current state
3. Decide whether `refund.ts` is salvageable or should be restarted
```

**What RM does NOT do:** Doesn't commit, doesn't delete, doesn't continue the implementation, doesn't run the tests itself.

---

## Scenario 22: Kiro Specs as Development Driver

**State:** `.kiro/specs/search-feature/` has `requirements.md`, `design.md`, `tasks.md`. Kiro is tracking task completion. Developer switches to Claude Code for a session.

**RM creates (if not already present):**

```text
docs/
├── README.md
└── features/
    └── search-feature.md
```

**docs/README.md ownership map:**

```md
## Canonical Ownership Map

| Capability              | Owner                                        | Notes          |
| ----------------------- | -------------------------------------------- | -------------- |
| Requirements (search)   | `.kiro/specs/search-feature/requirements.md` | Kiro-managed   |
| Design (search)         | `.kiro/specs/search-feature/design.md`       | Kiro-managed   |
| Task tracking (search)  | `.kiro/specs/search-feature/tasks.md`        | Kiro-managed   |
| Feature state + handoff | `docs/features/search-feature.md`            | RM-managed     |
| Work queue              | `docs/generated/next-work-queue.md`          | Auto-generated |
```

**docs/features/search-feature.md:**

```yaml
---
id: search-feature
title: Full-Text Search
status: in_progress
ready: ready
next_safe_step: "Task 3 of 5 in .kiro/specs/search-feature/tasks.md — implement result ranking"
priority: 1
last_updated: 2026-06-11
---
```

```md
## Context

Requirements and design defined in Kiro specs. See `.kiro/specs/search-feature/`.

## Implementation Progress

- Tasks 1-2 complete (indexing + basic query)
- Task 3 in progress (result ranking)
- Tasks 4-5 pending (filters + UI)

## Handoff Notes

Switching from Kiro to Claude Code for this session. Specs are canonical for requirements. This doc tracks cross-session status only.
```

**What RM does NOT do:**

- Does NOT copy requirements from the Kiro spec
- Does NOT redefine the tasks
- Does NOT create its own design doc
- Does NOT compete with Kiro's task tracking

It adds only the cross-tool bridge: "if you're not in Kiro, here's where to look and what's the current state."

---

## Scenario 26: Multiple Companion Skills Active

**State:** Project uses Superpowers for specs, a dedicated review skill for architecture reviews, a planning skill for implementation plans, and RM for continuity. All four produce different outputs.

**What each skill owns:**

```text
.kiro/specs/                          ← Kiro specs (requirements, design, tasks)
docs/superpowers/specs/               ← Superpowers specs
docs/superpowers/plans/               ← Superpowers plans
docs/reviews/architecture-2026-06.md  ← Review skill output
docs/plans/migration-plan.md          ← Planning skill output
docs/                                 ← RM's continuity layer
├── README.md                         ← Ownership map
├── features/
│   └── api-migration.md              ← Feature state + handoff
└── generated/
    └── next-work-queue.md            ← Work queue
```

**docs/features/api-migration.md:**

```yaml
---
id: api-migration
title: REST to GraphQL Migration
status: in_progress
ready: ready
next_safe_step: "Implement resolver for UserType (step 4 of plan)"
priority: 1
last_updated: 2026-06-11
---
```

```md
## Context

Migration from REST to GraphQL for the user-facing API.

## Companion Artifacts

- Spec: `docs/superpowers/specs/2026-05-api-migration.md`
- Plan: `docs/plans/migration-plan.md` (7 steps, currently on step 4)
- Architecture review: `docs/reviews/architecture-2026-06.md` (2 findings accepted)

## Status

Steps 1-3 complete. Step 4 (UserType resolver) in progress.
Review finding #1 (N+1 query risk) addressed in step 3.
Review finding #2 (auth middleware gap) scheduled for step 5.

## Handoff

Any agent, any tool — read this doc + the plan step 4 to continue.
```

**What RM owns:** The feature doc (status + handoff) and the work queue.
**What RM links to:** Everything else.
**What RM duplicates:** Nothing.

---

## Simulation Results

| Scenario           | Files RM creates                | Docs RM leaves alone     | Token cost (normal work) |
| ------------------ | ------------------------------- | ------------------------ | ------------------------ |
| #1 Empty           | 2 files                         | —                        | ~50 lines                |
| #7 Good docs       | 2-3 feature files + map section | All existing docs        | ~80 lines                |
| #11 No docs        | 2 files (map + template)        | —                        | ~50 lines                |
| #14 Crash recovery | Updates 1 feature file          | All code, all other docs | ~60 lines                |
| #22 Kiro specs     | 2 files (map + 1 feature)       | All Kiro specs           | ~70 lines                |
| #26 Multi-skill    | 1-2 feature files + map         | All companion outputs    | ~80 lines                |

In every case: **ownership map + relevant feature doc = the only context loaded during normal coding.**
