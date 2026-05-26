# Changelog

All notable changes to Repo Memory are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Version numbers match the `Version:` fields in [`skills/repo-memory/STANDARD.md`](./skills/repo-memory/STANDARD.md)
and [`skills/repo-memory/SKILL.md`](./skills/repo-memory/SKILL.md).

## [3.2.0](https://github.com/akanahs-dev/repo-memory/compare/repo-memory-v3.1.0...repo-memory-v3.2.0) (2026-05-26)


### Features

* implement Phases 4-7 — plan/review schemas, install-adapter, migrate, audit ([1df4c4d](https://github.com/akanahs-dev/repo-memory/commit/1df4c4de9b4613b5601927508286027fd57e9e9a))

## [3.1.0](https://github.com/akanahs-dev/repo-memory/compare/repo-memory-v3.0.0...repo-memory-v3.1.0) (2026-05-26)


### Features

* implement Phase 3 — feature frontmatter, validate, and generate commands ([f7b7e4b](https://github.com/akanahs-dev/repo-memory/commit/f7b7e4b5b95b6fa0b2d1d890f3ecd31af75fc8ae))


### Bug Fixes

* address PR review feedback for feature parsing and generate output ([4a0780d](https://github.com/akanahs-dev/repo-memory/commit/4a0780dd0215a789574ccbcac9ddd1a152d11c6e))

## [3.0.0](https://github.com/akanahs-dev/repo-memory/compare/repo-memory-v2.3.0...repo-memory-v3.0.0) (2026-05-26)


### ⚠ BREAKING CHANGES

* the single-file SKILL.md workflow is replaced by a router + modes layout, and Repo Memory now ships a CLI package and config schema. Existing v2 installs require migration.

### Features

* enforce plan and specification directory placement via new validator check and updated documentation rules ([5571f1d](https://github.com/akanahs-dev/repo-memory/commit/5571f1d9fd2901563375616e81f4fb211de5c962))
* enhance documentation with quick start guide and repository purpose clarification ([6aee226](https://github.com/akanahs-dev/repo-memory/commit/6aee226e36374c197c596e6a2086553cf262950f))
* migrate release management to release-please and update documentation versioning strategy ([514e3e8](https://github.com/akanahs-dev/repo-memory/commit/514e3e8a331f6d9634840cc9e6cc8ccd1ab33a95))
* upgrade to Repo Memory v3 agent-first architecture ([951a350](https://github.com/akanahs-dev/repo-memory/commit/951a350e23239454b100c11b59ea6bf251a09ca7))


### Bug Fixes

* address all review comments from PR [#4](https://github.com/akanahs-dev/repo-memory/issues/4) ([2bb5600](https://github.com/akanahs-dev/repo-memory/commit/2bb5600064636c86eae8a51fd8feb936024b81e8))
* clean up workflows — remove duplicate link check, explicit release config ([69ceb92](https://github.com/akanahs-dev/repo-memory/commit/69ceb92cde991ce7ee255a9de9b2d10b96a2c554))
* ignore infra and dependency dirs in all validation traversals ([7ec8652](https://github.com/akanahs-dev/repo-memory/commit/7ec865253f6a853eb2c84d4fa16641a459303f61))
* make markdownlint pass — exclude infra dirs, fix lint errors in docs ([bb98c87](https://github.com/akanahs-dev/repo-memory/commit/bb98c87128c7e95464a337b6556aa8e64a153f36))
* resolve version drift and changelog header regex in validator ([e69c123](https://github.com/akanahs-dev/repo-memory/commit/e69c123dff7d62fd490478f7f933f6d57b96ec6f))

## [Unreleased]

### Added

- Added an evidence extraction workflow for turning repository evidence into
  candidate behavior, requirements, feature areas, and handoff context before
  accepted findings are promoted into mapped owners.
- Added an evidence extraction example showing raw extraction output in
  `docs/intake/` with accepted feature state promoted into canonical docs.

### Changed

- Updated the standard, skill workflow, README, roadmap, examples, and
  validator required-file list so evidence extraction is discoverable without
  adding premature automation.
- Refreshed the generated `docs/README.md` and template to be shorter,
  friendlier, and easier to scan.

## [2.3.0](https://github.com/akanahs-dev/repo-memory/compare/v2.2.0...v2.3.0) (2026-05-21)

### Features

- enforce plan and specification directory placement via new validator check and updated documentation rules ([5571f1d](https://github.com/akanahs-dev/repo-memory/commit/5571f1d9fd2901563375616e81f4fb211de5c962))
- enhance documentation with quick start guide and repository purpose clarification ([6aee226](https://github.com/akanahs-dev/repo-memory/commit/6aee226e36374c197c596e6a2086553cf262950f))
- migrate release management to release-please and update documentation versioning strategy ([514e3e8](https://github.com/akanahs-dev/repo-memory/commit/514e3e8a331f6d9634840cc9e6cc8ccd1ab33a95))

### Bug Fixes

- clean up workflows - remove duplicate link check, explicit release config ([69ceb92](https://github.com/akanahs-dev/repo-memory/commit/69ceb92cde991ce7ee255a9de9b2d10b96a2c554))
- ignore infra and dependency dirs in all validation traversals ([7ec8652](https://github.com/akanahs-dev/repo-memory/commit/7ec865253f6a853eb2c84d4fa16641a459303f61))
- make markdownlint pass - exclude infra dirs, fix lint errors in docs ([bb98c87](https://github.com/akanahs-dev/repo-memory/commit/bb98c87128c7e95464a337b6556aa8e64a153f36))
- resolve version drift and changelog header regex in validator ([e69c123](https://github.com/akanahs-dev/repo-memory/commit/e69c123dff7d62fd490478f7f933f6d57b96ec6f))

## [2.2.0] - 2026-05-20

### Added

- Added requirement to update feature doc status to `in_progress` and update registry entry before starting implementation to prevent duplicate or conflicting work.

## [2.1] - 2026-05-20

### Added

- Added automated plan and spec placement rules to `validate-docs.py` to prevent agents from creating plans in arbitrary root or docs directories.
- Added explicit rules to `docs-structure-rules.md` prohibiting plans and specs from being placed outside of `docs/superpowers/plans/`, `docs/superpowers/specs/`, or `docs/designs/`.
- Updated the main `AGENTS.md` and `SKILL.md` workflows, `scaffold-docs.py` templates, and `references/templates.md` snippets to require automated drift-checking validator calls at both the start and end of all agent sessions.

## [2.0] - 2026-05-20

### Added

- Added the `Canonical Ownership Map` model so each documentation capability has
  one named owner, whether that owner is a Repo Memory doc or an existing ADR,
  API spec, runbook, setup doc, security doc, or product doc.
- Added
  [`agent-integration-and-enforcement.md`](./skills/repo-memory/references/agent-integration-and-enforcement.md)
  with Codex, GitHub Copilot, VS Code, Claude Code, OpenCode, cloud-agent,
  hook, and CI setup guidance.
- Added an OpenCode adapter guide in
  [`skills/repo-memory/agents/opencode.md`](./skills/repo-memory/agents/opencode.md).
- Added validator support for `--adoption-level continuity` and
  `--adoption-level baseline`, plus warnings for missing or suspicious
  ownership maps.

### Changed

- Reframed the standard from a required file baseline to a capability ownership
  model: Repo Memory must complement existing documentation instead of
  duplicating world-standard docs.
- Split adoption into a Level 1 continuity overlay and Level 2 baseline
  coverage so existing repos can start with shared handoff state before broad
  baseline migration.
- Updated the skill workflow, templates, audit guidance, governance guidance,
  agent adapters, examples, scaffold output, and README guidance around strict
  no-duplicate ownership.

## [1.9] - 2026-05-20

### Added

- Added progressive-adoption guidance across the standard, skill workflow,
  references, and examples so existing repos can preserve strong docs and add
  only the missing handoff surfaces first.
- Added a partial-adoption example showing how Repo Memory can complement
  existing documentation rather than replacing it wholesale.

### Changed

- Clarified that Level 0 is valid, adoption is optional, and strict baseline
  requirements apply when a repo claims Repo Memory conformance.
- Updated agent guides and prompts to prefer thin aligned instruction files,
  preserve useful existing docs, and keep mutable project state in the
  maintained docs layer.

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
