# Documentation Standard

This docs tree owns active feature state, handoff context, and documentation
freshness. It preserves useful existing docs instead of duplicating them.

## Canonical Ownership Map

| Capability                         | Canonical owner              | Supporting docs              | Notes                                                                          |
| ---------------------------------- | ---------------------------- | ---------------------------- | ------------------------------------------------------------------------------ |
| Project overview                   | `../README.md`               | `feature-registry.md`        | Existing README stays canonical for high-level project description.            |
| Architecture notes                 | `../ARCHITECTURE_NOTES.md`   | `doc-health.md`              | Preserved legacy notes; do not duplicate them into a new architecture doc yet. |
| Feature state and next work        | `feature-registry.md`        | `features/search-refresh.md` | Repo Memory owns the queue and feature list.                                   |
| Active feature handoff             | `features/search-refresh.md` | `feature-registry.md`        | Repo Memory owns resumable handoff state.                                      |
| Documentation health and conflicts | `doc-health.md`              | `../ARCHITECTURE_NOTES.md`   | Tracks preserved docs, stale areas, and future migration.                      |

## Preserved Existing Docs

- [`../ARCHITECTURE_NOTES.md`](../ARCHITECTURE_NOTES.md) — preserved legacy
  architecture notes still used as supporting context.

The preserved doc remains useful, but active shared state now lives in this
`docs/` tree so different agents can resume from the same place.
