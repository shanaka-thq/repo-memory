# Existing Project Partial Adoption

This example shows a repo that already had useful documentation and only added
the missing Repo Memory surfaces needed for shared agent state.

The goal is not to rewrite every existing document. The goal is to make the
current source of truth discoverable, resumable, and safe for different coding
agents to share.

## Scenario

The sample project already had:

- a legacy architecture note
- team runbook content outside `docs/`
- agent instructions that had grown too stateful

The partial adoption keeps the useful legacy material, adds a thin `AGENTS.md`,
and introduces only the ownership and handoff files needed for cross-agent
continuity.

## Example Tree

```text
AGENTS.md
ARCHITECTURE_NOTES.md
docs/
├── README.md
├── doc-health.md
├── feature-registry.md
└── features/
    └── search-refresh.md
```

## What This Example Demonstrates

- preserved existing docs can stay where they are when they still help
- mapped Repo Memory owners can start small
- the feature registry and feature doc provide the shared handoff surface
- doc health records what is preserved, what is owned where, and what still needs migration

Full baseline adoption can happen later if the repo needs tighter verification
or more complete standardization.
