# Changelog

All notable changes to Repo Memory are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Version numbers match the `Version:` fields in [`skills/repo-memory/STANDARD.md`](./skills/repo-memory/STANDARD.md)
and [`skills/repo-memory/SKILL.md`](./skills/repo-memory/SKILL.md).

Minor versions add non-breaking content. Major versions restructure the workflow.

---

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
- `skills/repo-memory/SKILL.md` as the Codex-compatible Repo Memory implementation.
- Reference templates, naming rules, metadata schema, existing-project audit workflow, decision reconstruction guidance, and continuity governance.
- Interrupted-work recovery protocol for crashed, resumed, or unknown prior-agent sessions.
- Agent integration guides for OpenAI Agents SDK, OpenAI Codex, GitHub Copilot, and Claude Code.
- Example adopted docs trees and multi-agent handoff references.
- Local validation script and GitHub workflow templates for documentation quality checks.
