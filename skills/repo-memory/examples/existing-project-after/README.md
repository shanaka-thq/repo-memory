# Existing Project After Adoption

This example shows the shape of a small repository after applying the
Repo Memory standard.

The sample project is fictional: a minimal issue tracker API with a web UI.
The point is the documentation structure, not the product details.

## Example Tree

```text
docs/
├── README.md
├── project-overview.md
├── architecture.md
├── interfaces-and-contracts.md
├── data-model.md
├── local-development.md
├── doc-health.md
├── observability-and-instrumentation.md
├── testing-strategy.md
├── operations-runbook.md
├── security-and-privacy.md
├── decision-log.md
├── implementation-log.md
├── feature-registry.md
├── requirements/
│   ├── functional-requirements.md
│   ├── non-functional-requirements.md
│   └── user-stories-and-use-cases.md
└── features/
    ├── _template.md
    └── issue-labels.md
```

## What Changed

Before adoption, project facts were split across a README, stale comments, and
agent chat history.

After adoption:

- baseline docs summarize current behavior
- feature work has a tracked owner and status
- durable decisions are recorded with evidence and confidence
- `doc-health.md` records what was verified and what is still uncertain
- agent instruction files point into `docs/` instead of duplicating project
  state

See [`docs/README.md`](./docs/README.md) for the example documentation map.
