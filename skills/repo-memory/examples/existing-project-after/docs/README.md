# Project Docs

This is the documentation set for the example issue tracker. The ownership map
names the single owner for each maintained documentation capability.

## Start Here

1. Read [`project-overview.md`](./project-overview.md).
2. Read [`architecture.md`](./architecture.md).
3. Check [`feature-registry.md`](./feature-registry.md).
4. Check [`doc-health.md`](./doc-health.md) for stale or inferred areas.

## Canonical Ownership Map

| Capability | Canonical owner | Supporting docs | Notes |
| --- | --- | --- | --- |
| Project goal, actors, scope, and success criteria | [`project-overview.md`](./project-overview.md) | [`README.md`](./README.md) | Product intent lives here. |
| Architecture and runtime topology | [`architecture.md`](./architecture.md) | [`data-model.md`](./data-model.md), [`interfaces-and-contracts.md`](./interfaces-and-contracts.md) | Example repo has no separate ADR/RFC owner. |
| Interfaces and contracts | [`interfaces-and-contracts.md`](./interfaces-and-contracts.md) | [`architecture.md`](./architecture.md) | API and UI contracts are summarized here. |
| Data model | [`data-model.md`](./data-model.md) | [`interfaces-and-contracts.md`](./interfaces-and-contracts.md) | Domain records and relationships live here. |
| Local development and tooling | [`local-development.md`](./local-development.md) | [`testing-strategy.md`](./testing-strategy.md) | Setup commands live here. |
| Documentation health and conflicts | [`doc-health.md`](./doc-health.md) | [`feature-registry.md`](./feature-registry.md) | Stale areas and verification state live here. |
| Observability and runtime signals | [`observability-and-instrumentation.md`](./observability-and-instrumentation.md) | [`operations-runbook.md`](./operations-runbook.md) | Runtime signals live here. |
| Testing strategy | [`testing-strategy.md`](./testing-strategy.md) | [`local-development.md`](./local-development.md) | Test layers and commands live here. |
| Operations and support | [`operations-runbook.md`](./operations-runbook.md) | [`observability-and-instrumentation.md`](./observability-and-instrumentation.md) | Support procedures live here. |
| Security and privacy | [`security-and-privacy.md`](./security-and-privacy.md) | None | Security posture lives here. |
| Decisions and rationale | [`decision-log.md`](./decision-log.md) | [`implementation-log.md`](./implementation-log.md) | Example uses one decision log instead of ADRs. |
| Implementation history | [`implementation-log.md`](./implementation-log.md) | [`decision-log.md`](./decision-log.md), [`features/`](./features/) | Meaningful landed work lives here. |
| Feature state and next work | [`feature-registry.md`](./feature-registry.md) | [`features/`](./features/) | Ranked queue and feature list live here. |
| Active feature handoff | [`features/issue-labels.md`](./features/issue-labels.md) | [`feature-registry.md`](./feature-registry.md) | Resume context and validation live here. |

## Baseline Docs

- [`project-overview.md`](./project-overview.md)
- [`architecture.md`](./architecture.md)
- [`interfaces-and-contracts.md`](./interfaces-and-contracts.md)
- [`data-model.md`](./data-model.md)
- [`local-development.md`](./local-development.md)
- [`observability-and-instrumentation.md`](./observability-and-instrumentation.md)
- [`testing-strategy.md`](./testing-strategy.md)
- [`operations-runbook.md`](./operations-runbook.md)
- [`security-and-privacy.md`](./security-and-privacy.md)
- [`decision-log.md`](./decision-log.md)
- [`implementation-log.md`](./implementation-log.md)
- [`feature-registry.md`](./feature-registry.md)
- [`doc-health.md`](./doc-health.md)

## Requirements

- [`requirements/functional-requirements.md`](./requirements/functional-requirements.md)
- [`requirements/non-functional-requirements.md`](./requirements/non-functional-requirements.md)
- [`requirements/user-stories-and-use-cases.md`](./requirements/user-stories-and-use-cases.md)

## Active Features

- [`features/issue-labels.md`](./features/issue-labels.md)
