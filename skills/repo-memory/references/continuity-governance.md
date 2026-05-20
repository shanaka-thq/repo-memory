# Continuity Governance

Use this reference when documentation changes materially, conflicts with implementation or other docs, becomes stale, is renamed, or must support multiple agents working concurrently.

## Goal

Keep the documentation system trustworthy over time. The docs should not only describe the project; they should also show when they were verified, what changed, what is stale, what was superseded, and how another agent can continue safely.

## Coexisting with Other Documentation Systems

Repo Memory should complement useful repository documentation, not flatten it.

- preserve strong ADRs, RFCs, architecture notes, wiki pages, support notes,
  API specs, security docs, and team runbooks when they still add value
- choose one canonical owner for each documentation capability
- keep `docs/README.md` updated with the ownership map so another agent can
  discover owners quickly
- promote accepted durable outcomes into the mapped canonical owner when
  external artifacts materially affect current requirements, architecture,
  validation, or next-step guidance
- avoid parallel current-state summaries that drift from each other

The goal is one discoverable owner for each kind of current truth, with
supporting material linked around it rather than replaced for cosmetic reasons.

## Duplicate Ownership Protocol

Use this protocol when two or more docs claim the same current truth.

1. Identify the capability in conflict, such as decisions, API contracts, setup
   commands, feature state, security posture, or operations.
2. Choose one canonical owner using current evidence, existing team standards,
   and the ownership map.
3. Update `docs/README.md` `Canonical Ownership Map` with that owner.
4. Convert competing docs into supporting links, indexes, or superseded records.
5. Remove copied mutable content from adapter files such as `AGENTS.md`,
   `CLAUDE.md`, `.github/copilot-instructions.md`, and OpenCode rules.
6. Record the migration in the mapped doc-health owner.

Prefer established world-standard owners when they are healthy. ADRs should
usually own decisions, OpenAPI or equivalent specs should own API contracts,
`SECURITY.md` or a threat model should own security policy, and
`CONTRIBUTING.md` or README setup sections can own local setup when they are
already maintained.

## Architecture and Contract Change Lifecycle

For material changes to architecture, interfaces, data model, security posture, operations, local tooling, or documentation structure:

1. Read the ownership map and update the directly affected canonical owner.
2. Update affected supporting docs, deep-dive docs, diagrams, feature docs, and agent instruction pointers.
3. Add or update the mapped decision owner when the change is durable.
4. Add an implementation-history entry when work landed or behavior changed.
5. Update the mapped doc-health owner with verification evidence, known gaps, duplicate-owner changes, and stale areas.
6. Record migration, compatibility, rollback, or recovery notes when the change affects existing users, data, deploys, integrations, or future agents.

Do not leave architecture-impacting changes only in a feature doc. Feature docs
track active work; the mapped architecture and decision owners preserve durable
project state.

## Conflict Resolution Protocol

When sources disagree, resolve in this order:

1. Current source code, tests, schemas, runtime config, deployment config, and generated contracts establish current behavior.
2. Explicit user statements, ADRs, design docs, and code comments establish intent and rationale.
3. Existing docs establish prior understanding, but stale docs must be corrected.
4. Git history, changelogs, issues, and PR notes help explain how the conflict happened.
5. Inference is allowed only when marked clearly.

After resolving a conflict:

- update the stale doc or convert it into a supporting/superseded pointer
- add a correction note to the mapped doc-health owner
- update mapped decision or implementation owners if the correction changes durable understanding
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

- update every link in baseline owners, feature docs, indexes, diagrams, and agent instruction files
- record `Formerly: <old-slug>` in the registry or index
- keep the old doc only when it contains useful history; mark it `superseded` and link to the replacement
- update `docs/doc-health.md` with the rename

## Multi-Agent Concurrency Protocol

When more than one agent may work in the repo:

- active feature docs must include current owner, files or docs being touched, safe parallel work, and areas to avoid
- another agent should check `docs/feature-registry.md`, active feature docs, and `docs/doc-health.md` before starting related work
- if no task is assigned, the agent should pick the lowest-rank `ready` row from `docs/feature-registry.md` `Next Work Queue`
- `verify-first` queue rows are inspection or validation tasks until the agent updates evidence and readiness
- `needs-human` and `blocked` queue rows should not be implemented without resolving the missing direction or blocker
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
- promote accepted outcomes into the mapped owners, such as requirements, UI/UX, architecture, feature, decision, or implementation-history owners
- record rejected, adjusted, deferred, or superseded advice so future agents do not rediscover the same review context

When a repository also uses Obra Superpowers, keep `docs/superpowers/` as the companion artifact folder and use Repo Memory docs for current state, accepted decisions, validation, and next-agent handoff. See [superpowers-compatibility.md](./superpowers-compatibility.md).

## Intake Promotion Protocol

Use this protocol when `docs/intake/` contains raw brainstorms, copied chat
notes, user-provided project dumps, sketches, imported plans, or planning-agent
output that may shape the project.

Before planning or building from intake material:

1. Read the relevant intake files and identify confirmed user statements,
   accepted direction, assumptions, rejected ideas, and open questions.
2. Promote accepted durable facts into the mapped owners, such as
   `docs/project-overview.md`, requirements, architecture, data model, UI/UX,
   design, feature, decision-history, implementation-history, and doc-health
   docs, or into existing owners named by the ownership map.
3. Link important intake files from `Evidence`, `Plan Provenance`, or
   `Source artifacts` when they materially shaped the accepted direction.
4. Ask the user only for high-impact missing foundations that would change the
   project shape, such as primary user, first useful workflow, platform target,
   privacy constraints, success criteria, or explicit non-goals.
5. Record lower-risk unknowns in `Open Questions` and `docs/doc-health.md`.

Do not treat raw intake as canonical truth. Leave raw files intact unless the
user asks to reorganize them. If intake content becomes a maintained design,
feature, or requirements document, move or summarize it into the mapped owner
and apply normal naming, metadata, link, and verification rules.

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
- `docs/README.md` has a current `Canonical Ownership Map`
- no capability has two current canonical owners
- all optional docs folders have indexes
- no optional docs folder is only an empty index
- changed docs are represented in `docs/doc-health.md` when applying the standard to a target repo
- completed features use `implemented`, `verified`, or `shipped` in the feature doc and registry
- generated artifacts from validation or forward testing are not left in the target repo
- agent-specific instruction files still point to the ownership map instead of duplicating mutable state
