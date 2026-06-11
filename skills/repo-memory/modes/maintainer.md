# Maintainer Mode

Use this mode during normal work when Repo Memory is already set up. Your job is to keep the continuity layer current — not to maintain all project documentation.

## Instructions

1. **Load lazily.** Read only `docs/README.md` (ownership map) and the relevant feature doc. Don't load the full docs tree.
2. **Update feature state.** If your task changes feature status, scope, or progress, update `docs/features/<slug>.md` frontmatter and handoff notes.
3. **Link companion outputs.** If a planning skill produced a plan, a review skill produced a review, or a spec was updated — link it from the feature doc. Don't recreate it.
4. **Update the ownership map** only when new docs are created or ownership actually changes.
5. **Don't edit generated files.** Let the generation script rebuild `docs/generated/` from frontmatter.
6. **Don't duplicate.** If the fact already lives somewhere (OpenAPI, ADRs, Kiro specs, Superpowers plans), just point to it.
7. **Run scripts** when done: `python3 <skill-dir>/scripts/validate-docs.py --project-docs .` and `python3 <skill-dir>/scripts/generate-indexes.py .`

## On Crash Recovery

If you find uncommitted changes, untracked files, or a dirty working tree from a previous agent:

1. Run `git status` and inspect before editing.
2. Don't delete, commit, or overwrite what you don't understand.
3. Update the feature doc with a **Recovery Notes** section: what you found, what's safe, what needs verification.
4. Set `ready: verify-first` in frontmatter until the state is confirmed.
