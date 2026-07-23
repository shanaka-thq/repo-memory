## Feature Doc Template

```md
# Feature: answer-search-improvements

Doc type: feature
Feature slug: answer-search-improvements
Status: in_progress
Owner: current-agent-or-team
Priority: High
Last updated: 2026-04-22
Last verified: unknown
Verified against: unknown
Confidence: medium
Canonical source: `docs/features/answer-search-improvements.md`
Related docs: `../feature-registry.md`
Validation status: implementation in progress
Next safe step: continue from `Next Agent Handoff`

## Goal

State the user problem and intended outcome.

## Research Summary

- Summarize what was investigated.
- Note rejected options only if they affect future work.

## Decision

- Record the chosen approach and why.

## Plan Provenance

- Planned by:
- Tool or agent surface:
- Role or lens:
- Date:
- Inputs reviewed:
- Source artifacts:
- Assumptions:
- Confidence:
- Plan disposition: proposed | accepted | adjusted | rejected | superseded
- Implementer pickup: summarize the exact starting point for the next agent.

## Scope

In:

- What this feature covers

Out:

- What it does not cover

## User Impact

- Affected actor or persona:
- Main use case or journey:
- Important UX states:

## Supporting Docs

- Detailed logic: `./answer-search-improvements/logic.md`
- Related shared component: `../components/search-results-panel.md`
- Related UX doc: `../ui-ux/search-results-experience.md`
- Related design doc: `../designs/answer-search-architecture.md`

## Edge Cases and Failure Modes

- Edge case 1
- Failure mode 1

## Implementation Status

- [x] API response shape defined
- [x] backend implementation started
- [ ] frontend wiring complete
- [ ] tests updated
- [ ] docs updated
- [ ] manual verification complete

## Files Touched

- `src/...`
- `dashboard/src/...`

## Open Questions

- Question 1
- Question 2

## Validation

- Tests run
- Manual checks
- Remaining verification gaps

## Review Log

| Date       | Reviewer               | Tool or agent surface | Role or lens  | Subject                        | Disposition                     | Record                                         |
| ---------- | ---------------------- | --------------------- | ------------- | ------------------------------ | ------------------------------- | ---------------------------------------------- |
| 2026-04-22 | game-design-specialist | Codex sub-agent       | game designer | Search result interaction loop | accepted with follow-up changes | `../reviews/answer-search-game-design-pass.md` |

## Change Governance

- Last verified:
- Verified against:
- Docs updated:
- Decision log impact:
- Implementation log impact:
- Conflicts or stale docs found:
- Supersedes or replaces:

## Resume Context

- Canonical docs to read first:
- Files or directories to inspect first:
- Last known good state:
- Known blockers or constraints:
- Interrupted work recovery:
  - Workspace state checked:
  - Unexpected modified, staged, or untracked files:
  - Recovery evidence:
  - Preserved or unresolved changes:

## Next Agent Handoff

- Done:
- Next safe step:
- Risks:
- Validation status:
- Inspect first:
- Active owner:
- Avoid parallel changes in:
- Safe to parallelize:
- Avoid changing:
- If recovering from interruption: run `git status --short`, inspect diffs and untracked files, then record what was found before editing.

When a feature reaches `implemented`, `verified`, or `shipped`, update the feature doc `Status`, update the feature registry row, and replace interrupted-work language with completed-state handoff. Do not leave `interrupted`, `resume carefully`, or `do not discard uncommitted work` wording unless unresolved workspace state still exists and is documented as a current risk.

## Exact Next Prompt

Continue implementing answer-search-improvements. Read this feature doc first, then inspect `src/...` and `dashboard/src/...`. Finish the frontend wiring, add tests for fallback behavior, and update docs before stopping.
```