# GitHub Copilot Instructions

This repo uses Repo Memory for durable project context.
Start with:

- `skills/repo-memory/SKILL.md`
- the configured ownership map, usually `docs/README.md`
Use task-relevant mode files only.
Never edit generated files directly.
For feature work:
- Update the matching file in `docs/features/`.
- Let `repo-memory generate` update registries and queues.
Use validation/generation commands when available.
