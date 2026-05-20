# Examples

These examples show how Repo Memory should feel in real repositories.
They are intentionally small, but they demonstrate the expected shape of the
docs tree, agent entrypoints, and handoff state.

They also show the strict no-duplicate rule: existing strong docs can remain
canonical owners, while Repo Memory adds only the missing ownership map,
feature state, doc health, and handoff surfaces.

## Available Examples

- [`existing-project-after/`](./existing-project-after/) — a compact example of
  a target repo after adopting the full baseline, including a canonical
  ownership map and a ranked `Next Work Queue` in `docs/feature-registry.md`.
- [`existing-project-partial/`](./existing-project-partial/) — a partial-adoption
  example showing how to keep useful existing docs as owners and add only the
  missing handoff surfaces.
- [`multi-agent-handoff/`](./multi-agent-handoff/) — a feature handoff example
  showing how one agent leaves enough context for another agent to continue.
- [`superpowers-bridge/`](./superpowers-bridge/) — an example of linking Obra
  Superpowers specs and plans without making them the canonical handoff state.

## How to Use These Examples

Use them as reference outputs, not as universal content. Target repos should
copy the structure and level of evidence, then replace the facts with evidence
from their own code, tests, configuration, and user guidance.

If a target repo already has decent documentation, start with the partial
adoption example. It is the best model for “complement, do not replace.”
