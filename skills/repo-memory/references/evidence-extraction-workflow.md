# Evidence Extraction Workflow

Use this reference when an agent needs to extract project behavior,
requirements, feature candidates, or handoff context from an existing
repository without turning uncertain findings into canonical truth too early.

This workflow is intentionally lighter than a clean-room reimplementation
analysis. It borrows the useful discipline of multi-source evidence,
provenance, behavioral wording, and completeness checks, while keeping Repo
Memory focused on maintained project context.

## Goal

Create a reviewable evidence report that helps the agent update the mapped Repo
Memory owners. The report may suggest candidate surfaces, requirements, feature
areas, risks, and questions, but it does not become canonical project truth.

Canonical project truth still belongs in the ownership map:

- accepted requirements in the mapped requirements owner
- current architecture in the mapped architecture owner
- active or recent feature state in the mapped feature owner
- durable rationale in the mapped decision owner
- verification state and unresolved trust issues in the mapped doc-health owner

## When To Use

Use this workflow when:

- an existing repo has little or stale documentation
- the user asks what behavior, requirements, or features can be extracted from
  the codebase
- raw intake, external plans, or companion artifacts need to be checked against
  current code before promotion
- a feature registry or next-work queue needs evidence-backed candidates
- docs disagree and the agent needs a structured way to resolve what is known

Do not use it as a reason to perform exhaustive reverse engineering for every
small task. For a narrow bugfix or obvious doc refresh, inspect the directly
relevant files and update the mapped owner.

## Output Location

Write the extraction report to `docs/intake/YYYY-MM-DD-evidence-extraction.md`
when the target repo has Repo Memory docs. Intake is the right location because
the report is source material, not maintained truth.

If the repo has not adopted Repo Memory yet, keep the report outside the repo
or in another explicit scratch location until the user asks to adopt the docs.

## Workflow

### 1. Inventory Evidence

List available evidence before drawing conclusions:

- source files, tests, schemas, migrations, and runtime configuration
- package manifests, scripts, local tooling, CI, deploy, and container files
- existing docs, ADRs, specs, READMEs, runbooks, issue templates, and changelogs
- API contracts, CLI help, MCP tools, event names, config keys, and env vars
- UI flows, screenshots, diagrams, design notes, or product docs when present
- git history, PRs, or issues when available and worth the cost
- raw intake and companion plans or specs, such as `docs/superpowers/`

Record gaps explicitly. A missing source is useful information when it affects
confidence.

### 2. Extract Candidate Surfaces

Extract observable surfaces in behavioral language:

- user-facing commands, routes, tools, screens, workflows, jobs, and events
- inputs, outputs, config keys, env vars, flags, file formats, and APIs
- state transitions, lifecycle stages, failure modes, permissions, and limits
- tests that imply intended behavior
- docs or comments that explain purpose, constraints, or tradeoffs

Call them candidate surfaces until they are confirmed and promoted. Avoid
phrasing like "the feature is" when the evidence only says "this file or test
suggests a feature area."

### 3. Synthesize Candidates

Group candidate surfaces into likely docs updates:

- requirements candidates
- feature candidates
- architecture or data-model candidates
- decision candidates, with rationale marked explicit, inferred, or unknown
- local-development, testing, observability, operations, security, or UI/UX
  candidates
- open questions that block safe promotion

Keep implementation names out of user-facing requirement prose unless the name
is an external contract, such as an API field, CLI flag, config key, event
name, or environment variable.

### 4. Record Evidence and Confidence

Every promoted candidate should have evidence. Use simple confidence labels:

- `high`: multiple strong sources agree, or one direct source is decisive
- `medium`: direct evidence exists, but important context is missing
- `low`: plausible inference from weak or partial evidence

Do not write inferred rationale as confirmed intent. If the code clearly does
something but the reason is unknown, say that.

### 5. Promote Accepted Findings

After reviewing the evidence report, update only the mapped owners:

- update requirements for accepted behavior
- update feature docs and the feature registry for accepted feature state
- update architecture, data model, contracts, or operations docs where they own
  the changed capability
- update decision logs only when there is a durable choice and enough evidence
  to distinguish current shape from rationale
- update doc health with stale areas, conflicts, unresolved questions, and
  what was verified

Leave rejected, speculative, or unreviewed findings in intake. Link the intake
report from the promoted docs when it materially shaped the outcome.

### 6. Check Completeness

Before finishing, run a small gap check against the evidence inventory:

- Do all important user-facing surfaces have an owner or an explicit question?
- Did any accepted requirement or feature remain only in intake?
- Did any companion plan or external analysis change accepted state without a
  mapped owner update?
- Are low-confidence or conflicting findings recorded in doc health?
- Is the next safe task reflected in the feature registry when future work is
  expected?

This check should prevent silent drift, not force every low-value detail into
the docs.

## Report Template

Use this template for `docs/intake/YYYY-MM-DD-evidence-extraction.md`.

```md
# Evidence Extraction Report

Date:
Agent or tool:
Target repo:
Purpose:

## Evidence Inventory

| Source area | Evidence checked | Notes | Confidence impact |
| --- | --- | --- | --- |
| Source | `src/`, `app/` |  |  |
| Tests | `tests/` |  |  |
| Config and tooling | `package.json`, CI |  |  |
| Existing docs | `README.md`, `docs/` |  |  |

## Candidate Surfaces

| Candidate | Evidence | Confidence | Suggested owner | Status |
| --- | --- | --- | --- | --- |
|  |  | low/medium/high |  | unreviewed |

## Suggested Promotions

| Finding | Promote to | Rationale evidence | Confidence |
| --- | --- | --- | --- |
|  |  |  |  |

## Open Questions

- 

## Promotion Log

| Finding | Disposition | Owner updated | Notes |
| --- | --- | --- | --- |
|  | accepted/rejected/deferred |  |  |
```

## Relationship To Companion Workflows

Companion workflows may create specs, plans, or analysis reports outside the
Repo Memory owners. Treat those artifacts as evidence. Promote only accepted
current state into the mapped owner, and record the source artifact in
`Source artifacts`, `Plan Provenance`, `Evidence`, or doc-health notes.

When a companion artifact conflicts with code, tests, current docs, or user
intent, use the normal evidence order from the standard and record the
disposition in the mapped owner.
