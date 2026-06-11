<!-- Target platform: OpenCode. Usage: use this guide when wiring Repo Memory into OpenCode projects or aligning opencode.json with a repo's canonical documentation owners. -->

# OpenCode Integration Guide

This guide extends the [common agent workflow](../references/agent-workflow-common.md) with OpenCode specifics.

## Core Rule

Use `AGENTS.md` as the primary OpenCode router. Keep mutable project facts in
the mapped canonical owners from `docs/README.md`, not in OpenCode-only rules.

## Platform-Specific Notes

- Use `opencode.json` only when the repo needs OpenCode to load extra shared instruction files.
- Prefer references to existing files over copied content.

```json
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": ["AGENTS.md", "docs/README.md"]
}
```

## Validation

Run the validator when available:

```bash
python3 skills/repo-memory/scripts/validate-docs.py --project-docs . --adoption-level continuity
```

## Related Docs

- Common agent workflow: [`references/agent-workflow-common.md`](../references/agent-workflow-common.md)
- Skill definition: [`SKILL.md`](../SKILL.md)
- Agent integration and enforcement: [`references/agent-integration-and-enforcement.md`](../references/agent-integration-and-enforcement.md)
- Naming and placement rules: [`references/docs-structure-rules.md`](../references/docs-structure-rules.md)
