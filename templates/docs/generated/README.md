# Generated Docs

Files in this directory are generated from feature doc frontmatter.

**Do not edit these files manually.** Changes will be overwritten on the next generation run.

## Files

| File                  | Description                                                          |
| --------------------- | -------------------------------------------------------------------- |
| `feature-registry.md` | All tracked features, their status, priority, and readiness.         |
| `next-work-queue.md`  | Ranked list of actionable features for the next agent or maintainer. |

## Regenerate

```bash
python3 <skill-dir>/scripts/generate-indexes.py .
```

To preview without writing:

```bash
python3 <skill-dir>/scripts/generate-indexes.py . --dry-run
```
