<!-- Target platform: OpenCode. Usage: use this guide when wiring Repo Memory into OpenCode projects or aligning opencode.json with a repo's canonical documentation owners. -->

# OpenCode Integration Guide

This guide explains how to use Repo Memory with OpenCode while keeping project
truth in mapped owners instead of duplicating it in agent rules.

## Core Rule

Use `AGENTS.md` as the primary OpenCode router.

Keep mutable project facts, decisions, feature state, build commands, and
handoff notes in the mapped canonical owners from `docs/README.md`. Do not copy
those facts into OpenCode-only rules unless the ownership map names that file as
the owner.

## Recommended Files

```text
AGENTS.md
docs/
├── README.md
├── doc-health.md
├── feature-registry.md
└── features/
    └── <feature-slug>.md
opencode.json          # optional
```

Use `opencode.json` only when the repo needs OpenCode to load extra shared
instruction files. Prefer references to existing files over copied content.

```json
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": ["AGENTS.md", "docs/README.md"]
}
```

## Startup Flow

1. Read `AGENTS.md`.
2. Read `docs/README.md` for the canonical ownership map.
3. Read `docs/feature-registry.md`.
4. If no task was assigned, pick the first `ready` row in `Next Work Queue`.
5. Read the active feature doc before editing related code.
6. Review `docs/intake/` only when raw source material is relevant to the task,
   then promote accepted facts into the mapped owner before implementation
   depends on them.

## Finishing Flow

1. Update the active feature doc with status, validation, and next-agent handoff.
2. Update the feature registry when priority, readiness, or pickup instructions change.
3. Update only the mapped canonical owner for changed decisions, contracts, local setup, operations, security, or runtime signals.
4. Update the doc-health owner when docs were verified, corrected, renamed, found stale, or superseded.
5. Run the validator when available.

```bash
python3 skills/repo-memory/scripts/validate-docs.py --project-docs . --adoption-level continuity
```

## Related Docs

- Skill definition: [`SKILL.md`](../SKILL.md)
- Integration and enforcement: [`references/agent-integration-and-enforcement.md`](../references/agent-integration-and-enforcement.md)
- File templates: [`references/templates.md`](../references/templates.md)
- Naming and placement rules: [`references/docs-structure-rules.md`](../references/docs-structure-rules.md)
