# Superpowers Compatibility

Use this reference when a repository uses Repo Memory together with Obra
Superpowers or another companion workflow that writes separate spec and plan
artifacts.

Repo Memory remains the canonical durable memory layer. Companion specs and
plans remain useful source artifacts, but accepted outcomes must be reflected in
the owning Repo Memory docs before another agent relies on them as current
project state.

## Default Relationship

| Companion artifact | Repo Memory treatment |
| --- | --- |
| `docs/superpowers/specs/<date>-<topic>.md` | Link as source evidence from the owning feature, design, requirements, or project-overview doc. |
| `docs/superpowers/plans/<date>-<topic>.md` | Link from `Plan Provenance` or the owning design doc and summarize the implementable pickup. |
| Completed implementation from a plan | Update the feature doc, implementation log, validation notes, and decision log when warranted. |
| Rejected or superseded spec/plan advice | Record the disposition in the owning feature or design doc so future agents do not rediscover stale advice. |

Do not copy whole Superpowers plans into Repo Memory docs. Summarize the parts
that became accepted project state and link the source artifact for provenance.

## Workflow

1. Before changing related code or docs, read the relevant Repo Memory feature
   or design doc, then read any linked companion specs or plans.
2. Treat companion specs and plans as advisory until verified against current
   code, current docs, and user intent.
3. If a companion artifact changes requirements, architecture, UX, contracts,
   validation, or implementation status, update the canonical owning Repo
   Memory docs in the same work.
4. Keep the next safe implementation step in the feature or design doc, not
   only in `docs/superpowers/plans/`.
5. Update `docs/doc-health.md` when companion artifacts reveal stale docs,
   conflicts, superseded plans, or unverified state.

## Placement Rules

- Keep Superpowers artifacts in `docs/superpowers/specs/` and
  `docs/superpowers/plans/` when that is the repository's established workflow.
- Do not require `docs/superpowers/` to follow Repo Memory optional deep-dive
  index rules. It is a companion workflow folder, not a Repo Memory baseline or
  optional deep-dive folder.
- Use `docs/features/<feature-slug>.md` for the canonical feature state,
  implementation checklist, validation state, and next-agent handoff.
- Use `docs/designs/<design-slug>.md` when the accepted solution shape is large
  enough to outgrow the feature doc.
- Use `docs/reviews/<review-slug>.md` only when a review or critique is
  substantive, cross-cutting, or audit-worthy.

## Conflict Handling

When Superpowers artifacts conflict with Repo Memory docs, use the standard
evidence order:

1. source code, tests, schemas, runtime config, and deployment config
2. explicit user statements, ADRs, design docs, and code comments
3. existing docs, after checking whether they are stale
4. git history, changelogs, issues, and pull requests
5. clearly marked inference

Record the resolved disposition in the owning feature or design doc. If the
conflict affects documentation trust, also update `docs/doc-health.md`.

## Plan Provenance Example

```md
## Plan Provenance

- Planned by: Obra Superpowers writing-plans skill
- Tool or agent surface: Superpowers
- Role or lens: implementation planner
- Date: 2026-04-30
- Inputs reviewed: `../superpowers/specs/2026-04-30-search-refresh.md`, current feature doc, tests
- Source artifacts: `../superpowers/specs/2026-04-30-search-refresh.md`, `../superpowers/plans/2026-04-30-search-refresh.md`
- Assumptions: Search API contract remains stable.
- Confidence: medium
- Plan disposition: accepted with adjustments
- Implementer pickup: start from the feature checklist below; verify plan steps against current code before editing.
```

## Agent Prompt Note

When asking an agent to continue from a Superpowers plan, point it at the Repo
Memory feature or design doc first, then the companion plan. This keeps the
agent grounded in current canonical state while preserving the planning context.
