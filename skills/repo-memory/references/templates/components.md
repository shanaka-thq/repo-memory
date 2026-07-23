## Components Index Template

```md
# Components and Subsystems

Use this folder for shared component or subsystem deep dives that cut across features and would otherwise be hard to reconstruct from code alone.

| Component                 | Purpose                                                                                 | Owner doc                    |
| ------------------------- | --------------------------------------------------------------------------------------- | ---------------------------- |
| `search-results-panel.md` | Documents state, rendering rules, and interaction behavior for the shared results panel | `../architecture.md`         |
| `session-manager.md`      | Explains session ownership, refresh logic, and cleanup rules                            | `../security-and-privacy.md` |
```

## Shared Component Logic Template

```md
# Component Logic: search-results-panel

Owner doc: `../architecture.md`
Last updated: 2026-04-22

## Purpose

Explain why this component or subsystem needs its own logic doc.

## Responsibilities

- Responsibility 1
- Responsibility 2

## Inputs and Outputs

- Inputs:
- Outputs:

## State and Lifecycle

Describe initialization, updates, teardown, or other state transitions.

## Rules and Invariants

- Invariant 1
- Invariant 2

## Edge Cases

- Edge case 1
- Edge case 2

## Failure Modes

- Failure mode 1

## Related Code

- `src/...`
- `ui/...`

## Related Docs

- `../architecture.md`
- `../features/answer-search-improvements.md`
```

Reuse this template for `docs/features/<feature-slug>/components/<component-slug>.md` when the component logic is feature-local instead of shared.