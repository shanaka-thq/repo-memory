## Doc Health Template

Use this template for `docs/doc-health.md` in target repos that adopt the standard.

```md
# Documentation Health

This file tracks freshness, verification evidence, known drift, conflicts, and renamed or superseded docs.

## Health Summary

Last full audit:
Current overall confidence: high | medium | low
Known stale areas:
Open doc conflicts:

## Verification Matrix

| Doc               | Last verified | Verified against                  | Confidence | Known drift or action              |
| ----------------- | ------------- | --------------------------------- | ---------- | ---------------------------------- |
| `architecture.md` | 2026-04-28    | `src/`, deployment config, tests  | high       | None                               |
| `data-model.md`   | 2026-04-28    | schemas, migrations, storage code | medium     | Confirm production retention rules |

## Conflicts and Corrections

| Date       | Conflict                                      | Resolution                                        | Evidence      |
| ---------- | --------------------------------------------- | ------------------------------------------------- | ------------- |
| 2026-04-28 | Legacy README described old deployment target | `operations-runbook.md` updated to current target | deploy config |

## Renames and Supersessions

| Old slug or doc    | New slug or doc                 | Status     | Notes                            |
| ------------------ | ------------------------------- | ---------- | -------------------------------- |
| `legacy-search.md` | `answer-search-improvements.md` | superseded | New feature doc owns active work |
```
