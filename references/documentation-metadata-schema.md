# Documentation Metadata Schema

Use this reference when creating or refreshing project docs. It defines standard metadata fields that make docs consistent across agents, easier to audit, and easier to validate.

## Goal

Every maintained doc should explain what it is, who or what owns it, how current it is, what evidence supports it, and how it relates to other docs. Use these fields as Markdown metadata blocks, not necessarily YAML front matter, unless the target repo already prefers front matter.

## Common Metadata Fields

Use this block near the top of every maintained doc:

```md
Doc type:
Owner:
Status:
Last updated:
Last verified:
Verified against:
Confidence:
Canonical source:
Related docs:
```

## Field Definitions

| Field | Required | Purpose | Example |
| --- | --- | --- | --- |
| `Doc type` | Yes | Identifies the document category | `feature`, `architecture`, `doc-health` |
| `Owner` | Yes | Current responsible team, agent, or maintainer | `current-agent-or-team` |
| `Status` | Yes | Current lifecycle state | `active`, `in_progress`, `superseded` |
| `Last updated` | Yes | Last material edit date | `2026-04-28` |
| `Last verified` | Recommended | Last date checked against evidence | `2026-04-28` |
| `Verified against` | Recommended | Evidence used for verification | `src/`, tests, deploy config |
| `Confidence` | Recommended | Trust level for current content | `high`, `medium`, `low` |
| `Canonical source` | Recommended | Where authoritative facts live | `source code`, `decision-log.md`, `API schema` |
| `Related docs` | Recommended | Important linked docs | `architecture.md`, `feature-registry.md` |

## Allowed Values

### Doc Type

- `readme`
- `project-overview`
- `architecture`
- `functional-requirements`
- `non-functional-requirements`
- `user-stories-and-use-cases`
- `interfaces-and-contracts`
- `data-model`
- `local-development`
- `doc-health`
- `observability-and-instrumentation`
- `testing-strategy`
- `operations-runbook`
- `security-and-privacy`
- `decision-log`
- `implementation-log`
- `feature-registry`
- `feature`
- `feature-logic`
- `feature-component`
- `diagram-index`
- `design`
- `project-detail`
- `component`
- `ui-ux`

### General Status

- `draft`
- `active`
- `needs_review`
- `stale`
- `superseded`
- `deprecated`

Feature docs and feature registry entries must use the feature statuses from `docs-structure-rules.md`.

### Confidence

- `high`
- `medium`
- `low`

## Required Fields by Doc Type

| Doc type | Additional required fields |
| --- | --- |
| `project-overview` | `Project Goal`, `Problem Statement`, `Target Users or Actors`, `Success Criteria`, `Current Scope`, `Non-Goals` |
| `user-stories-and-use-cases` | `Actors`, `Personas or User Segments`, `User Stories`, `Primary Use Cases`, `Alternative flows`, `Failure states`, `Acceptance notes` |
| `observability-and-instrumentation` | `Logs`, `Metrics`, `Traces`, `Product Analytics Events`, `Audit Events`, `Dashboards and Alerts`, `Privacy and Retention`, `Known Blind Spots` |
| `feature` | `Feature slug`, `Priority`, `Validation status`, `Next safe step` |
| `decision-log` | `Decision ID format`, `Confidence rule`, `Supersession rule` |
| `implementation-log` | `Entry date`, `Change summary`, `Evidence` |
| `doc-health` | `Last full audit`, `Known stale areas`, `Open doc conflicts` |
| `design` | `Design status`, `Problem`, `Goals`, `Tradeoffs`, `Rollout` |
| `diagram-index` | `Diagram inventory`, `Source format`, `Owner doc` |
| `component` | `Responsibilities`, `Inputs and outputs`, `State and lifecycle` |
| `ui-ux` | `User goal`, `Surfaces`, `States`, `Accessibility`, `Responsive behavior` |
| `project-detail` | `Purpose`, `Detailed behavior`, `Invariants`, `Failure modes` |

## Feature Metadata Example

```md
# Feature: answer-search-improvements

Doc type: feature
Feature slug: answer-search-improvements
Owner: current-agent-or-team
Status: in_progress
Priority: High
Last updated: 2026-04-28
Last verified: 2026-04-28
Verified against: `src/search/`, API tests, manual search flow
Confidence: medium
Canonical source: `docs/features/answer-search-improvements.md`
Related docs: `../feature-registry.md`, `./answer-search-improvements/logic.md`
Validation status: backend tests pass; frontend verification pending
Next safe step: finish frontend wiring and rerun search flow checks
```

## Design Metadata Example

```md
# Design: answer-search-architecture

Doc type: design
Owner: current-agent-or-team
Status: active
Design status: adopted
Last updated: 2026-04-28
Last verified: 2026-04-28
Verified against: architecture doc, search service code, decision log
Confidence: high
Canonical source: `docs/designs/answer-search-architecture.md`
Related docs: `../architecture.md`, `../decision-log.md`
```

## Doc Health Metadata Example

```md
# Documentation Health

Doc type: doc-health
Owner: current-agent-or-team
Status: active
Last updated: 2026-04-28
Last verified: 2026-04-28
Verified against: docs tree, source code, tests, deployment config
Confidence: medium
Canonical source: `docs/doc-health.md`
Related docs: `README.md`, `feature-registry.md`, `decision-log.md`
Last full audit: 2026-04-28
Known stale areas: production retention rules
Open doc conflicts: none known
```

## Metadata Rules

- Prefer explicit `unknown` over leaving important metadata blank.
- Do not claim `high` confidence without current evidence.
- If a doc is `stale`, `superseded`, or `deprecated`, add a replacement pointer or correction note.
- If metadata conflicts with body content, update both and record the correction in `docs/doc-health.md`.
- Keep metadata concise; detailed explanation belongs in the body.
