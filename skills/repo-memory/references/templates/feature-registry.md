## Feature Registry Template

```md
# Feature Registry

## Next Work Queue

| Rank | Work item                  | Type    | Status        | Ready   | Why next                        | Next safe step                                    | Canonical doc                                                                        | Last verified |
| ---- | -------------------------- | ------- | ------------- | ------- | ------------------------------- | ------------------------------------------------- | ------------------------------------------------------------------------------------ | ------------- |
| 1    | Answer search improvements | feature | `in_progress` | `ready` | Highest user-visible search gap | Finish frontend wiring and run search flow checks | [`features/answer-search-improvements.md`](./features/answer-search-improvements.md) | 2026-04-22    |

## Feature List

| Feature                    | Slug                         | Status        | Priority | Last updated | Notes                                                                                                            |
| -------------------------- | ---------------------------- | ------------- | -------- | ------------ | ---------------------------------------------------------------------------------------------------------------- |
| Answer search improvements | `answer-search-improvements` | `in_progress` | High     | 2026-04-22   | [Feature doc](./features/answer-search-improvements.md), [Logic](./features/answer-search-improvements/logic.md) |
```

Allowed statuses are defined in [STANDARD.md](../../STANDARD.md#status-model). Do not invent new values.

Use `Next Work Queue` as the cloud-agent pickup surface. The lowest-rank row
with `Ready` set to `ready` is the default next task when a user asks an agent
to pick up repo work without choosing a feature manually. Use `verify-first`
when the agent should inspect or validate before editing, `needs-human` when
the next step depends on product direction, and `blocked` when known blockers
prevent progress.