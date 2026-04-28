# AGENTS.md

Instructions for AI coding agents (GitHub Copilot, OpenAI Codex, Claude, and others) working on or with this repository.

## What This Repo Is

This repository defines **Repo Memory**: a portable, repo-native project memory and handoff standard for AI-assisted software projects. It also includes the **Repo Memory** Codex skill implementation of that standard. It is not a product codebase; it is a standard, skill definition, and reference library.

## Entry Points

Read these files in order when starting a session:

1. [`README.md`](./README.md) — repo overview and quick-start guide
2. [`STANDARD.md`](./STANDARD.md) — portable Repo Memory standard and conformance model
3. [`SKILL.md`](./SKILL.md) — full skill definition, workflow, and quality bar
4. [`references/docs-structure-rules.md`](./references/docs-structure-rules.md) — strict naming and placement rules that all docs must follow
5. [`references/templates.md`](./references/templates.md) — copy-paste templates for every standard doc type
6. [`references/existing-project-audit.md`](./references/existing-project-audit.md) — audit workflow for backfilling docs in existing projects
7. [`references/documentation-metadata-schema.md`](./references/documentation-metadata-schema.md) — standard metadata fields by doc type
8. [`references/decision-log-reconstruction.md`](./references/decision-log-reconstruction.md) — comprehensive decision log reconstruction
9. [`references/continuity-governance.md`](./references/continuity-governance.md) — freshness, conflict, rename, feature closure, and multi-agent protocols
10. [`examples/README.md`](./examples/README.md) — concrete reference outputs for adopted docs and handoff state

## How to Apply This Skill

When a user asks you to apply this skill to a target repo:

1. **Detect state** — classify the repo as `new_project`, `existing_project_needs_standardization`, or `existing_project_with_structure`.
2. **Audit evidence** — inventory source code, tests, config, scripts, and existing docs before writing anything.
3. **Follow the workflow** in `SKILL.md`, section by section.
4. **Use the templates** in `references/templates.md` as the default format for any doc you create.
5. **Enforce the rules** in `references/docs-structure-rules.md` for all file names, folder names, and placement decisions.
6. **Keep one canonical docs layer** — agent-specific instruction files should point into the maintained docs set instead of duplicating mutable project facts.
7. **Track doc health** — use `docs/doc-health.md` in target repos to record verification state, stale docs, conflicts, renames, and superseded work.
8. **Use metadata consistently** — apply `references/documentation-metadata-schema.md` so doc type, status, owner, verification, evidence, and related docs are recorded predictably.
9. **Leave the repo resumable** — always close with current handoff notes in the active feature doc before ending a session.

## Maintaining This Skill Repo

When making changes to this repository itself:

- All docs in `references/` must follow the rules in [`references/docs-structure-rules.md`](./references/docs-structure-rules.md).
- Changes to the portable standard belong in [`STANDARD.md`](./STANDARD.md) and must preserve its relationship to `SKILL.md`.
- All changes to `SKILL.md` must preserve the version number at the top; increment the minor version for non-breaking additions and the major version for required baseline or structural changes.
- **Update [`CHANGELOG.md`](./CHANGELOG.md)** in the same PR that bumps `SKILL.md`. Add an entry under the new version number.
- New templates added to `references/templates.md` must include a brief usage note at the top of the template block.
- New agent configuration files belong in `agents/` and must include a comment describing the target platform and usage.
- New reference documents belong in `references/` and must be linked from both `README.md` and this file.
- New examples belong in `examples/` and must be linked from [`examples/README.md`](./examples/README.md).
- If `SKILL.md` changes, the new version must have a matching `CHANGELOG.md` section.
- If `STANDARD.md` changes, keep its `Version:` aligned with `SKILL.md`.
- Run `python3 scripts/validate-docs.py --skill-repo .` before stopping when validation-relevant files changed.

## Agent-Specific Guides

| Platform | Guide |
| --- | --- |
| OpenAI Agents SDK | [`agents/openai.yaml`](./agents/openai.yaml) |
| OpenAI Codex | [`agents/openai-codex.md`](./agents/openai-codex.md) |
| GitHub Copilot | [`agents/github-copilot.md`](./agents/github-copilot.md) |
| Claude Code | [`agents/claude-code.md`](./agents/claude-code.md) |

## Quality Checks Before Stopping

Before ending any session on this repo, confirm:

- [ ] Any changed templates still have a matching usage note.
- [ ] Any new reference doc is linked from `README.md` and this file.
- [ ] Any new example is linked from `examples/README.md`.
- [ ] `SKILL.md` version number is updated if the workflow changed.
- [ ] `STANDARD.md` and `SKILL.md` versions match.
- [ ] `CHANGELOG.md` has an entry for the new version.
- [ ] `SKILL.md` version matches the top relevant entry in `CHANGELOG.md`.
- [ ] No orphaned docs were left without a link from the repo root or another reference doc.
- [ ] File and folder names follow the kebab-case rules in `references/docs-structure-rules.md`.
- [ ] PR checks pass: Markdown lint, relative links, local validator, and SKILL.md version validation.
