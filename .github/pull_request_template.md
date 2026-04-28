## Summary

-

## Change Type

- [ ] Documentation clarification
- [ ] Template or reference update
- [ ] Skill workflow change
- [ ] Agent/platform adapter
- [ ] Validation or CI change
- [ ] Example update

## Checklist

- [ ] `skills/repo-memory/SKILL.md` version was bumped if the workflow changed.
- [ ] `CHANGELOG.md` has an entry for the current `skills/repo-memory/SKILL.md` version.
- [ ] New reference docs are linked from `README.md` and `AGENTS.md`.
- [ ] New templates include a usage note.
- [ ] Agent-specific files stay thin and point to canonical docs.
- [ ] `python3 skills/repo-memory/scripts/validate-docs.py --skill-repo .` passes.
