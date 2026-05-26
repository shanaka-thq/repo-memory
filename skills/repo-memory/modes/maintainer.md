# Maintainer Mode

Use this mode during normal feature work when Repo Memory is already set up in the repository.

## Instructions

1. **Load lazily:** Read only the documentation files relevant to your current task.
2. **Start with ownership map:** Use `docs/README.md` (or the configured ownership map) to find where canonical truth is stored.
3. **Update feature state:** If your task modifies feature behavior, scope, or status, update the specific feature document under `docs/features/<feature-slug>.md`.
4. **Update decisions (ADRs):** Only record enduring technical choices in the configured ADR path (e.g. `docs/adr/`).
5. **No manual generated updates:** Do not edit generated files (e.g. registry, next-work-queue, doc-health) directly. Let the CLI generate them.
6. **No duplicate facts:** Never duplicate details already owned by other canonical files (e.g. OpenAPI specs, README setup commands, runbooks).
7. **Use frontmatter:** Maintain metadata tags (ID, status, priority, ready, owner, next_safe_step, evidence, confidence) in the feature frontmatter.
8. **Record unknowns:** If some information is unknown, mark it as `unknown` rather than fabricating rationale or state.
9. **Run validation:** If the Repo Memory CLI is available, run `npx repo-memory validate` and `npx repo-memory generate` to sync indexes and verify changes.
