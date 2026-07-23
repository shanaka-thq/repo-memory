## Reviews Index Template

Use this index when a target repo creates `docs/reviews/` for substantive review records.

```md
# Review Records

Use this folder for substantive plan, specialist, second-agent, or human reviews that need provenance beyond a short entry in the owning doc.

| Review                              | Subject                                     | Reviewer               | Role or lens  | Disposition                     |
| ----------------------------------- | ------------------------------------------- | ---------------------- | ------------- | ------------------------------- |
| `answer-search-game-design-pass.md` | `../features/answer-search-improvements.md` | game-design-specialist | game designer | accepted with follow-up changes |
```

## Review Record Template

Use this template for `docs/reviews/<review-slug>.md` when a plan, specialist review, second-agent critique, or human review needs provenance and disposition tracking outside the owning doc.

```md
# Review: answer-search-game-design-pass

Doc type: review-record
Owner: current-agent-or-team
Status: active
Review subject: `../features/answer-search-improvements.md`
Reviewer: game-design-specialist
Tool or agent surface: Codex sub-agent
Role or lens: game designer
Last updated: 2026-04-30
Last verified: unknown
Verified against: unknown
Confidence: medium
Canonical source: `docs/reviews/answer-search-game-design-pass.md`
Related docs: `../features/answer-search-improvements.md`
Inputs reviewed: feature doc, implementation diff, tests
Disposition: proposed

## Purpose

State why this review was requested and what decision or implementation risk it informs.

## Findings

- Finding 1.

## Recommendations

- Recommendation 1.

## Accepted Outcomes

- Record what was accepted, adjusted, rejected, or deferred, and where mapped owners were updated.

## Follow-Up

- Owner:
- Next safe step:
- Related implementation or decision-log entry:
```