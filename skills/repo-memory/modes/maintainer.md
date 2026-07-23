# Maintainer Mode

Use this mode at the **end of every session**. Your job is a quick write-back:
update what changed, link what was produced, move on.

## Instructions

1. **Load lazily.** Read only `docs/README.md` (ownership map) and the relevant feature doc. Don't load the full docs tree.
2. **Update feature frontmatter.** Set `status`, `ready`, `next_safe_step` to reflect current reality.
3. **Link new artifacts.** If this session produced plans, specs, tickets, reviews, or research — link them from the feature doc and ensure the ownership map's Artifact Locations table has the right path.
4. **Update the ownership map** only when new docs are created or ownership actually changes.
5. **Don't edit generated files.** Generation runs automatically after you write.
6. **Don't duplicate.** If the fact already lives somewhere (OpenAPI, ADRs, specs, plans), point to it.
7. **Run validation** when done: `python3 <skill-dir>/scripts/validate-docs.py --project-docs .`

Generation (`generate-indexes.py`) runs after validation — no need to invoke it
separately.

## What a Typical Session-Close Looks Like

```yaml
# Minimal update — just frontmatter + one line
status: in_progress → done
next_safe_step: "Run integration tests, then merge"
```

```markdown
## Session Notes
- Completed auth token refresh implementation
- Plan: docs/superpowers/plans/2024-03-15-auth-refresh.md (accepted)
- Review: PR #42 approved
```

That's it. Don't over-document. The feature doc is a routing surface, not a journal.

## On Crash Recovery

If you find uncommitted changes, untracked files, or a dirty working tree from a previous agent:

1. Run `git status` and inspect before editing.
2. Don't delete, commit, or overwrite what you don't understand.
3. Update the feature doc with a **Recovery Notes** section: what you found, what's safe, what needs verification.
4. Set `ready: verify-first` in frontmatter until the state is confirmed.
