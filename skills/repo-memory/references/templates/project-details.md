## Project Details Index Template

```md
# Project Details

Use this folder for project-specific deep-dive documentation that is too detailed for the baseline docs but important for future implementation and maintenance.

| Topic                     | Purpose                                                    | Owner doc                        |
| ------------------------- | ---------------------------------------------------------- | -------------------------------- |
| `order-lifecycle.md`      | Describes the end-to-end order workflow and business rules | `../architecture.md`             |
| `multi-tenant-routing.md` | Documents routing and tenant resolution behavior           | `../interfaces-and-contracts.md` |
```

## Project Detail Template

```md
# Project Detail: order-lifecycle

Owner doc: `../architecture.md`
Last updated: 2026-04-22

## Purpose

Explain why this topic needs deeper documentation.

## Context

- Where this logic appears in the system
- Which teams, services, or features depend on it

## Detailed Behavior

Describe the workflow, rules, and branches in enough detail that another agent can change it safely.

## Invariants and Assumptions

- Business rule 1
- Operational constraint 1

## Edge Cases and Failure Modes

- Edge case 1
- Failure mode 1

## Related Code

- `src/...`
- `services/...`

## Related Docs

- `../architecture.md`
- `../requirements/functional-requirements.md`
```