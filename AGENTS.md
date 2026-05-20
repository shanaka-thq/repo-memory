# AGENTS.md

Instructions for AI coding agents (GitHub Copilot, OpenAI Codex, Claude, and others) working on or with this repository.

## What This Repo Is

This repository defines **Repo Memory**: a portable, repo-native project memory and handoff standard for AI-assisted software projects. It also includes the **Repo Memory** agent-facing skill implementation of that standard. It is not a product codebase; it is a standard, skill definition, and reference library.

Repo Memory is intended to complement strong existing repository documentation,
not replace it mechanically. When adopting it in a target repo, preserve useful
ADRs, specs, runbooks, setup docs, security docs, and product docs. Add a
`Canonical Ownership Map`, create only the missing handoff surfaces, and keep
agent-specific entrypoints thin.

## Entry Points

Read these files in order when starting a session:

1. [`README.md`](./README.md) — repo overview and quick-start guide
2. [`skills/repo-memory/STANDARD.md`](./skills/repo-memory/STANDARD.md) — portable Repo Memory standard and conformance model
3. [`skills/repo-memory/SKILL.md`](./skills/repo-memory/SKILL.md) — full skill definition, workflow, and quality bar
4. [`skills/repo-memory/references/docs-structure-rules.md`](./skills/repo-memory/references/docs-structure-rules.md) — strict naming and placement rules that all docs must follow
5. [`skills/repo-memory/references/templates.md`](./skills/repo-memory/references/templates.md) — copy-paste templates for every standard doc type
6. [`skills/repo-memory/references/existing-project-audit.md`](./skills/repo-memory/references/existing-project-audit.md) — audit workflow for backfilling docs in existing projects
7. [`skills/repo-memory/references/documentation-metadata-schema.md`](./skills/repo-memory/references/documentation-metadata-schema.md) — standard metadata fields by doc type
8. [`skills/repo-memory/references/decision-log-reconstruction.md`](./skills/repo-memory/references/decision-log-reconstruction.md) — comprehensive decision log reconstruction
9. [`skills/repo-memory/references/continuity-governance.md`](./skills/repo-memory/references/continuity-governance.md) — freshness, conflict, rename, feature closure, and multi-agent protocols
10. [`skills/repo-memory/references/agent-integration-and-enforcement.md`](./skills/repo-memory/references/agent-integration-and-enforcement.md) — Codex, Copilot, VS Code, Claude Code, OpenCode, cloud-agent, hook, and CI setup guidance
11. [`skills/repo-memory/references/superpowers-compatibility.md`](./skills/repo-memory/references/superpowers-compatibility.md) — bridge guidance for Obra Superpowers specs/plans and similar companion workflows
12. [`skills/repo-memory/examples/README.md`](./skills/repo-memory/examples/README.md) — concrete reference outputs for adopted docs and handoff state

## How to Apply This Skill

When a user asks you to apply this skill to a target repo:

1. **Detect state** — classify the repo as `new_project`, `existing_project_needs_standardization`, or `existing_project_with_structure`.
2. **Audit evidence** — inventory source code, tests, config, scripts, and existing docs before writing anything; identify which docs are already useful enough to preserve.
3. **Follow the workflow** in `skills/repo-memory/SKILL.md`, section by section.
4. **Assign canonical owners** — create or update `docs/README.md` with a `Canonical Ownership Map`; every durable documentation capability must have one owner.
5. **Avoid duplicates strictly** — do not create Repo Memory versions of facts already owned by healthy ADRs, OpenAPI specs, runbooks, `CONTRIBUTING.md`, `SECURITY.md`, product docs, or similar standards.
6. **Use the templates** in `skills/repo-memory/references/templates.md` as the default format for any doc you create; do not rewrite strong existing docs just to force a template.
7. **Enforce the rules** in `skills/repo-memory/references/docs-structure-rules.md` for all file names, folder names, ownership decisions, and placement decisions.
8. **Bootstrap empty repos** with `python3 skills/repo-memory/scripts/scaffold-docs.py <repo> --with-agents` when there is no implementation evidence yet.
9. **Keep one canonical owner per capability** — preserve useful existing docs, link them from the maintained docs set, and keep agent-specific instruction files pointed into the ownership map instead of duplicating mutable project facts.
10. **Track doc health** — use `docs/doc-health.md` in target repos to record verification state, stale docs, conflicts, renames, superseded work, and duplicate-owner migrations.
11. **Use metadata consistently** — apply `skills/repo-memory/references/documentation-metadata-schema.md` so doc type, status, owner, verification, evidence, and related docs are recorded predictably.
12. **Keep next work obvious** — keep `docs/feature-registry.md` current with a ranked `Next Work Queue`; cloud agents should pick the first `ready` row when no task is assigned.
13. **Leave the repo resumable** — always close with current handoff notes in the active feature doc before ending a session.

For existing repos with decent docs already in place, the first useful adoption
step is often partial: add the ownership map plus missing handoff and feature
state surfaces, then grow toward the full baseline only where that adds clear
value.

## Maintaining This Skill Repo

When making changes to this repository itself:

- All docs in `skills/repo-memory/references/` must follow the rules in [`skills/repo-memory/references/docs-structure-rules.md`](./skills/repo-memory/references/docs-structure-rules.md).
- Changes to the portable standard belong in [`skills/repo-memory/STANDARD.md`](./skills/repo-memory/STANDARD.md) and must preserve its relationship to `skills/repo-memory/SKILL.md`.
- All changes to `skills/repo-memory/SKILL.md` must preserve the version number at the top; increment the minor version for non-breaking additions and the major version for required baseline or structural changes.
- **Update [`CHANGELOG.md`](./CHANGELOG.md)** in the same PR that bumps `skills/repo-memory/SKILL.md`. Add an entry under the new version number.
- New templates added to `skills/repo-memory/references/templates.md` must include a brief usage note at the top of the template block.
- New scripts added to `skills/repo-memory/scripts/` must be documented in `README.md`, `SKILL.md`, or the relevant reference doc.
- New agent configuration files belong in `skills/repo-memory/agents/` and must include a comment describing the target platform and usage.
- New reference documents belong in `skills/repo-memory/references/` and must be linked from both `README.md` and this file.
- New examples belong in `skills/repo-memory/examples/` and must be linked from [`skills/repo-memory/examples/README.md`](./skills/repo-memory/examples/README.md).
- If `skills/repo-memory/SKILL.md` changes, the new version must have a matching `CHANGELOG.md` section.
- If `skills/repo-memory/STANDARD.md` changes, keep its `Version:` aligned with `skills/repo-memory/SKILL.md`.
- Run `python3 skills/repo-memory/scripts/validate-docs.py --skill-repo .` before stopping when validation-relevant files changed.

## Agent-Specific Guides

| Platform | Guide |
| --- | --- |
| OpenAI Agents SDK | [`skills/repo-memory/agents/openai.yaml`](./skills/repo-memory/agents/openai.yaml) |
| OpenAI Codex | [`skills/repo-memory/agents/openai-codex.md`](./skills/repo-memory/agents/openai-codex.md) |
| GitHub Copilot | [`skills/repo-memory/agents/github-copilot.md`](./skills/repo-memory/agents/github-copilot.md) |
| Claude Code | [`skills/repo-memory/agents/claude-code.md`](./skills/repo-memory/agents/claude-code.md) |
| OpenCode | [`skills/repo-memory/agents/opencode.md`](./skills/repo-memory/agents/opencode.md) |

## Quality Checks Before Stopping

Before ending any session on this repo, confirm:

- [ ] Any changed templates still have a matching usage note.
- [ ] Any new reference doc is linked from `README.md` and this file.
- [ ] Any new example is linked from `skills/repo-memory/examples/README.md`.
- [ ] `skills/repo-memory/SKILL.md` version number is updated if the workflow changed.
- [ ] `skills/repo-memory/STANDARD.md` and `skills/repo-memory/SKILL.md` versions match.
- [ ] `CHANGELOG.md` has an entry for the new version.
- [ ] `skills/repo-memory/SKILL.md` version matches the top relevant entry in `CHANGELOG.md`.
- [ ] `docs/README.md` examples include a `Canonical Ownership Map` when they claim adoption.
- [ ] No doc creates a duplicate canonical owner for ADRs, contracts, setup, security, operations, feature state, or handoff state.
- [ ] No orphaned docs were left without a link from the repo root or another reference doc.
- [ ] File and folder names follow the kebab-case rules in `skills/repo-memory/references/docs-structure-rules.md`.
- [ ] PR checks pass: Markdown lint, relative links, local validator, and SKILL.md version validation.
