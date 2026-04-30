# Continuity Governance

Use this reference when documentation changes materially, conflicts with implementation or other docs, becomes stale, is renamed, or must support multiple agents working concurrently.

## Goal

Keep the documentation system trustworthy over time. The docs should not only describe the project; they should also show when they were verified, what changed, what is stale, what was superseded, and how another agent can continue safely.

## Architecture and Contract Change Lifecycle

For material changes to architecture, interfaces, data model, security posture, operations, local tooling, or documentation structure:

1. Update the directly affected baseline doc.
2. Update affected deep-dive docs, diagrams, feature docs, and agent instruction pointers.
3. Add or update a decision-log entry when the change is durable.
4. Add an implementation-log entry when work landed or behavior changed.
5. Update `docs/doc-health.md` with verification evidence, known gaps, and stale areas.
6. Record migration, compatibility, rollback, or recovery notes when the change affects existing users, data, deploys, integrations, or future agents.

Do not leave architecture-impacting changes only in a feature doc. Feature docs track active work; baseline docs and decision logs preserve durable project state.

## Conflict Resolution Protocol

When sources disagree, resolve in this order:

1. Current source code, tests, schemas, runtime config, deployment config, and generated contracts establish current behavior.
2. Explicit user statements, ADRs, design docs, and code comments establish intent and rationale.
3. Existing docs establish prior understanding, but stale docs must be corrected.
4. Git history, changelogs, issues, and PR notes help explain how the conflict happened.
5. Inference is allowed only when marked clearly.

After resolving a conflict:

- update the stale doc
- add a correction note to `docs/doc-health.md`
- update decision or implementation logs if the correction changes durable understanding
- keep replacement links when an old doc or slug may still be referenced

## Staleness and Verification Protocol

`docs/doc-health.md` is the freshness ledger for the documentation system.

Track:

- last full documentation audit
- last verified date for important docs
- evidence used for verification
- confidence level
- known stale sections
- open conflicts
- renamed, superseded, deprecated, or rolled-back docs

Use confidence values:

- `high`: verified against current code, tests, config, or explicit current user guidance
- `medium`: mostly verified but some rationale, environment, or production detail is incomplete
- `low`: useful but likely stale, inferred, or incomplete

## Feature Closure Protocol

Do not delete feature docs just because work stopped.

Use terminal statuses:

- `abandoned` when work intentionally stopped without replacement
- `superseded` when another feature, design, or approach replaced it
- `deprecated` when the feature still exists but should not be extended
- `rolled_back` when implemented work was reverted, disabled, or withdrawn

For terminal feature states, update:

- `docs/feature-registry.md`
- the feature doc status and handoff section
- replacement links or rationale
- implementation log if code landed, was reverted, or was disabled
- decision log if a durable project choice changed
- doc health if stale docs or superseded docs remain

When a feature moves to `implemented`, `verified`, or `shipped`, update the feature doc `Status`, update the feature registry row, and remove stale interrupted-work phrasing from the handoff. The final handoff should describe the latest verified state, validation gaps, residual risks, and next safe maintenance step. Keep dirty-worktree warnings only when unresolved uncommitted work still exists.

## Rename and Move Protocol

Avoid renames unless the current slug is actively misleading.

When renaming or moving docs:

- update every link in baseline docs, feature docs, indexes, diagrams, and agent instruction files
- record `Formerly: <old-slug>` in the registry or index
- keep the old doc only when it contains useful history; mark it `superseded` and link to the replacement
- update `docs/doc-health.md` with the rename

## Multi-Agent Concurrency Protocol

When more than one agent may work in the repo:

- active feature docs must include current owner, files or docs being touched, safe parallel work, and areas to avoid
- another agent should check `docs/feature-registry.md`, active feature docs, and `docs/doc-health.md` before starting related work
- if two handoff notes conflict, prefer the one with newer verification evidence and update the stale note
- do not overwrite another agent's feature state without reconciling the docs and recording the correction

## Plan and Review Provenance Protocol

Use this protocol when one agent creates a plan for another agent to implement,
or when a specialist, second-agent, human, or tool review materially shapes work.

- keep the implementable summary, assumptions, confidence, disposition, and next safe implementation step in the owning feature or design doc
- record who or what produced the plan or review, the tool or agent surface, role or lens, date, inputs reviewed, and any source artifacts
- link companion spec or plan files such as `docs/superpowers/specs/...` and `docs/superpowers/plans/...` when they materially shaped the work
- put short reviews in the owning doc `Review Log`
- create `docs/reviews/<review-slug>.md` only when the record is substantive, cross-cutting, or likely to be audited later
- treat plan and review records as advisory evidence until checked against current code, docs, and user intent
- promote accepted outcomes into the canonical owning docs, such as requirements, UI/UX, architecture, feature, decision-log, or implementation-log docs
- record rejected, adjusted, deferred, or superseded advice so future agents do not rediscover the same review context

When a repository also uses Obra Superpowers, keep `docs/superpowers/` as the companion artifact folder and use Repo Memory docs for current state, accepted decisions, validation, and next-agent handoff. See [superpowers-compatibility.md](./superpowers-compatibility.md).

## Interrupted Work Recovery Protocol

Use this protocol when an agent crashes, a session is interrupted, work starts from a different tool, or the current working tree contains changes the new agent did not make.

Before editing:

1. Run `git status --short` to inventory modified, staged, deleted, renamed, and untracked files.
2. Inspect unstaged changes with `git diff`.
3. Inspect staged changes with `git diff --staged` when files are already staged.
4. Review untracked files before deleting or overwriting them. Treat them as possible user work, generated artifacts, or unfinished agent output until evidence says otherwise.
5. Read `docs/feature-registry.md`, the active feature doc, and `docs/doc-health.md` to compare the documented handoff with the workspace state.
6. If the workspace and docs disagree, treat the workspace as interrupted state. Resolve using evidence order, then update the stale handoff or doc-health record.

Recovery notes should record:

- date of recovery
- files or directories found in an unexpected state
- whether changes were staged, unstaged, or untracked
- evidence inspected before continuing
- what was preserved, adopted, ignored, or left unresolved
- remaining uncertainty and any user confirmation needed
- next safe step

Do not delete, revert, or overwrite uncommitted work from another user or agent unless the user explicitly asks or the files are verified disposable generated artifacts.

When the interrupted state belongs to an active feature, put the recovery note in that feature doc under `Resume Context` or `Next Agent Handoff`. When the interrupted state affects documentation trust, generated docs, or multiple features, also update `docs/doc-health.md`.

After tests or validation, remove disposable generated artifacts you created, such as `__pycache__`, `.pytest_cache`, `.DS_Store`, or `agent-final.txt`, unless the repo intentionally tracks or ignores them. Prefer validation commands that avoid artifacts up front; for Python one-off checks, use `python3 -B` or `PYTHONDONTWRITEBYTECODE=1 python3` when practical. If an artifact cannot be removed, record it as an unresolved workspace hygiene issue.

## Self-Consistency Checks

Before stopping after documentation work:

- `SKILL.md` version matches a `CHANGELOG.md` entry
- newly referenced files are linked from `README.md`, `AGENTS.md`, or another discoverable entrypoint
- all optional docs folders have indexes
- no optional docs folder is only an empty index
- changed docs are represented in `docs/doc-health.md` when applying the standard to a target repo
- completed features use `implemented`, `verified`, or `shipped` in the feature doc and registry
- generated artifacts from validation or forward testing are not left in the target repo
- agent-specific instruction files still point to the canonical docs instead of duplicating mutable state
