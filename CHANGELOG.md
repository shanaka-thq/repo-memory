# Changelog

All notable changes to Repo Memory are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Version numbers match the `Version:` fields in [`skills/repo-memory/STANDARD.md`](./skills/repo-memory/STANDARD.md)
and [`skills/repo-memory/SKILL.md`](./skills/repo-memory/SKILL.md).

Minor versions add non-breaking content. Major versions restructure the workflow.

---

## [1.8] - 2026-05-03

### Added

- Added a ranked `Next Work Queue` to `docs/feature-registry.md` so cloud
  agents can pick the first ready repo task without prior chat context.
- Added readiness values for queue items: `ready`, `verify-first`,
  `needs-human`, and `blocked`.

### Changed

- Updated the standard, skill workflow, templates, scaffold output, examples,
  and agent guides so the feature registry owns both feature status and
  next-work pickup state.
- Updated validation to require `Next Work Queue` and `Feature List` sections
  in adopted project feature registries and warn on malformed queue rows.

## [1.7] - 2026-05-03

### Added

- Added the `docs/intake/` workflow for raw brainstorms, copied chat notes,
  user-provided project dumps, sketches, and planning-agent output.
- Added scaffold output for `docs/intake/README.md` so new repos have a simple
  place to collect unstructured project context before implementation starts.

### Changed

- Clarified that raw intake is source evidence, not canonical project truth:
  accepted outcomes must be promoted into baseline, requirements, feature,
  design, decision, implementation, and doc-health docs before building from
  them.
- Updated validation so raw files under `docs/intake/` are exempt from
  canonical docs filename and relative-link checks.

## [1.6] - 2026-04-30

### Added

- Added Obra Superpowers compatibility guidance so specs and plans in
  `docs/superpowers/` can complement Repo Memory without replacing canonical
  feature, design, decision, implementation, and handoff docs.
- Added a compatibility reference, example, scaffold provenance field, and
  validator awareness for companion spec/plan workflow artifacts.

### Changed

- Clarified that accepted outcomes from companion plans and specs must be
  promoted into the owning Repo Memory docs, while source artifacts remain
  linked evidence and provenance.

## [1.5] - 2026-04-30

### Added

- Added plan and review provenance guidance so one agent can generate a plan,
  another can implement it, and future agents can verify planner, tool, role,
  reviewed inputs, assumptions, confidence, disposition, and accepted outcomes.
- Added optional `docs/reviews/` placement, `review-record` metadata, review
  index and record templates, and feature-template `Plan Provenance` and
  `Review Log` sections.

### Changed

- Extended the skill, standard, structure rules, scaffold output, and validators
  so substantive specialist or second-agent reviews are linked from owning docs
  instead of living only in chat history.

## [1.4] - 2026-04-30

### Added

- Added `skills/repo-memory/scripts/forward-test.py` for manual blind
  forward-testing against disposable fixture repositories.
- Added validator warnings for generated artifacts, empty optional deep-dive
  folders, inconsistent feature status metadata, and terminal feature docs with
  stale interrupted-work handoff text.
- Added `--strict` validation mode to treat warnings as failures.

### Changed

- Strengthened guidance to avoid index-only optional deep-dive folders, preserve
  useful custom docs, and replace interrupted-work wording when features reach a
  terminal implemented, verified, or shipped state.
- Added Python validation hygiene guidance to avoid creating `__pycache__`
  during ad hoc checks.

## [1.3] - 2026-04-29

### Changed

- Made the `repo-memory` skill trigger description agent-neutral instead of
  Codex-specific.
- Clarified that bundled script commands should resolve paths from the
  installed skill directory, while repository-root examples use
  `skills/repo-memory/scripts/...`.
- Updated standard and repository wording to describe the skill package as an
  agent-facing implementation of the portable standard.

## [1.2] - 2026-04-29

### Added

- Added `skills/repo-memory/scripts/scaffold-docs.py` to create the standard
  Repo Memory docs skeleton in an empty or nearly empty repository.
- Added empty-repository bootstrap guidance to the skill workflow and portable
  standard, including validation and optional root `AGENTS.md` generation.

## [1.1] - 2026-04-28

### Changed

- Moved the installable skill payload into `skills/repo-memory/` so GitHub
  directory installs can target the skill without installing repository
  governance files, CI, issue templates, or branding assets.
- Updated repository documentation, validation, and release paths to treat
  `skills/repo-memory/` as the canonical skill package.
- Added package-local license text and source archive export rules for leaner
  GitHub archive-based installs.

## [1.0] - 2026-04-28

### Added

- Initial Repo Memory public release as a portable, repo-native project context and memory standard.
- `skills/repo-memory/STANDARD.md` as the normative standard entrypoint, including conformance levels, required docs, metadata expectations, validation guidance, and non-goals.
- `skills/repo-memory/SKILL.md` as the agent-facing Repo Memory skill implementation.
- Reference templates, naming rules, metadata schema, existing-project audit workflow, decision reconstruction guidance, and continuity governance.
- Interrupted-work recovery protocol for crashed, resumed, or unknown prior-agent sessions.
- Agent integration guides for OpenAI Agents SDK, OpenAI Codex, GitHub Copilot, and Claude Code.
- Example adopted docs trees and multi-agent handoff references.
- Local validation script and GitHub workflow templates for documentation quality checks.
