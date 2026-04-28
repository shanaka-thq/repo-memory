# Decision Log Reconstruction

Use this reference whenever creating or updating `docs/decision-log.md`. The decision log should be a comprehensive architectural and project-history record, not a short list of recent implementation choices.

## Goal

Reconstruct every durable decision that shaped the project from the beginning through the current state. Include decisions even when the original rationale is incomplete, as long as the current system clearly embodies the choice. Mark confidence and uncertainty explicitly.

## Evidence Order

Prefer evidence in this order:

1. explicit user statements, ADRs, design docs, PR notes, issue notes, and code comments that explain intent
2. source code, tests, schemas, runtime configuration, package manifests, and folder structure
3. existing repository docs and feature docs
4. git history, changelog, release notes, or deployment artifacts
5. inferred rationale from repeated architecture patterns

Explicit user statements are valid high-confidence rationale evidence when they explain why a decision was made.

## Decision Entry Template

Each durable decision should use this shape or an equivalent structure:

```md
## DL-000: Decision Title

Status: implemented | planned | deprecated | superseded
Confidence: high | medium | low

Decision: State the durable choice in one or two sentences.

Rationale: Explain why the choice was made. If rationale is not fully known, say `Rationale inferred from...` or `Original rationale unknown`.

Evidence: List files, docs, tests, user statements, commits, or other artifacts.

Consequences:

- What this decision enables.
- What constraints or follow-up work it creates.
```

Optional fields:

- Alternatives considered
- Related decisions
- Supersedes
- Open questions

## Confidence Rules

- `high`: direct support from explicit rationale, current source, config, tests, or docs.
- `medium`: decision is clearly embodied by the codebase, but original rationale is inferred.
- `low`: decision is visible but rationale or permanence is uncertain.

Do not omit a visible durable decision just because the rationale is incomplete. Include it with lower confidence and explicit uncertainty.

## Coverage Checklist

Review all categories below. A mature decision log should usually have entries for most categories that apply.

### Project Foundation

- framework choice
- starter/template choice
- custom build abandoned or superseded
- language choice
- package manager
- runtime and build tooling
- deploy target
- repository and app boundaries

### Architecture

- route structure
- major folders and ownership boundaries
- client/server split
- data/state separation
- domain logic location
- extension model
- source of truth for docs and handoff

### Integration

- API, MCP, webhook, job, or connector patterns
- external SDKs and why they are used
- widget/resource registration patterns
- CORS and asset loading choices
- environment variable strategy

### Data And Contracts

- primary model/entity choices
- schema validation choices
- runtime defaulting or repair choices
- persistence or no-persistence decisions
- metadata handling
- compatibility and migration assumptions

### UI And UX

- design system and component library
- visual theme
- primary layout constraints
- responsive and accessibility choices
- view/surface choices
- deferred or rejected UI patterns

### Testing And Quality

- unit/component/E2E test stack
- visual testing or Storybook choices
- deferred test types
- verification expectations
- known local tooling constraints

### Operations And Security

- deployment and rollback strategy
- logging/observability stance
- auth/no-auth stance
- secrets and privacy posture
- CORS/security tradeoffs

### Product Scope

- MVP scope boundaries
- deterministic fixtures vs generated behavior
- future feature/model decisions
- explicitly deferred functionality

## Reconstruction Workflow

1. Read product requirements, architecture docs, feature registry, implementation log, package manifests, route handlers, schemas, and tests.
2. Inventory visible durable choices by category.
3. Add entries for confirmed choices first.
4. Add entries for inferred choices with confidence and uncertainty.
5. Add user-provided rationale when available, citing it as evidence.
6. Add consequences so future agents know what the choice constrains.
7. Cross-check the decision log against architecture, requirements, data model, operations, security, and feature docs.

## Example

```md
## DL-001: Build On A Working Starter Template

Status: implemented
Confidence: high

Decision: Use the vendor-provided starter template instead of continuing a custom implementation.

Rationale: The maintainer explicitly stated that the custom build attempt did not work, the starter was already working, and the maintainer was familiar with the framework and deployment platform.

Evidence: User statement; `README.md`; `app/api/...`; package manifest; deployment config.

Consequences:

- Preserve starter-compatible route and resource patterns unless there is a strong reason to change them.
- Future agents should treat template conventions as intentional, not incidental.
```
