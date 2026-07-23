## Diagrams Index Template

```md
# Diagrams

Use this folder for maintained diagram sources and rendered exports that support architecture, design, workflow, sequence, or state documentation.

## Diagram Inventory

| Diagram                   | Format         | Owner doc                                  | Notes                                              |
| ------------------------- | -------------- | ------------------------------------------ | -------------------------------------------------- |
| `system-context.mmd`      | Mermaid source | `../architecture.md`                       | Canonical architecture context diagram             |
| `search-flow.drawio`      | Draw.io source | `../designs/answer-search-architecture.md` | Visual editing retained for cross-team updates     |
| `exports/search-flow.svg` | Rendered asset | `../designs/answer-search-architecture.md` | Used by Markdown target that cannot render Mermaid |

## Diagram Rules

- Prefer Mermaid in Markdown for text-centric, reviewable diagrams.
- Preserve `.drawio` when the repo already depends on visual editing.
- Keep sources and exports together, and link them from the owning docs.
```