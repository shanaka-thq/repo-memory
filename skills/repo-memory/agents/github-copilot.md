# GitHub Copilot Integration Guide

This guide extends the [common agent workflow](../references/agent-workflow-common.md) with GitHub Copilot specifics.

## Overview

Repo Memory works alongside Copilot's custom instruction files:
`.github/copilot-instructions.md`, path-specific `.github/instructions/*.instructions.md`,
VS Code `.instructions.md`, and `AGENTS.md`.

## Core Rule

Treat `docs/README.md` as the first map. Keep Copilot-specific instruction
files concise and point them to the same owners that other agents use.

## Platform-Specific Notes

### Linking This Skill to a Target Repo

Add to the repo's `AGENTS.md` or `.github/copilot-instructions.md`:

```md
## Documentation Standard

This project uses the Repo Memory standard to maintain its `docs/` folder.

When starting a session:

1. Read `docs/README.md` for the Canonical Ownership Map.
2. Follow the mapped owner for project overview, architecture, decisions,
   contracts, setup, operations, security, and feature state.
3. Review `docs/intake/` if raw brainstorms or plans are relevant, then
   promote accepted facts into the mapped owner.
4. Check `docs/generated/next-work-queue.md` for the ranked `Next Work Queue`.
5. When no task is assigned, pick the first `ready` row in `docs/generated/next-work-queue.md`.

When making changes:

- Keep `docs/features/<feature-slug>.md` current for the feature you are working on.
- Update `docs/features/<feature-slug>.md` when feature status, priority, or readiness changes, then run `python3 <skill-dir>/scripts/generate-indexes.py <repo>` to regenerate the indexes.
- Update the mapped implementation-history and decision owners when warranted.
- Update `docs/doc-health.md` when docs change materially.
- Do not duplicate mutable project facts in Copilot instruction files.
```

### Using the default prompt

The default prompt from [`agents/openai.yaml`](./openai.yaml) works well as a starting point:

```text
Use $repo-memory to audit this repo, create or update docs/README.md with a Canonical Ownership Map, preserve strong existing ADRs/specs/runbooks/setup docs as owners, add only missing handoff surfaces, keep feature docs current and regenerate docs/generated/next-work-queue.md with the next ready task, update the mapped owners for changed capabilities, avoid duplicate project facts in agent instructions, and leave resumable handoff notes.
```

### Handling repos with multiple instruction files

1. Keep the files that the toolchain expects.
2. Reduce them to thin entrypoints pointing to the same ownership map.
3. Preserve useful tool-specific behavior instructions.
4. Move mutable project facts into mapped owners.

### Integration with GitHub Actions

Ensure CI validation checks:

- kebab-case file and folder names
- `Canonical Ownership Map` with one owner per capability
- feature registry status values matching the allowed set from [STANDARD.md](../STANDARD.md#status-model)
- `docs/doc-health.md` reflecting material documentation changes

See [`references/docs-structure-rules.md`](../references/docs-structure-rules.md) for the complete validation checklist.

## Related Docs

- Common agent workflow: [`references/agent-workflow-common.md`](../references/agent-workflow-common.md)
- Skill definition: [`SKILL.md`](../SKILL.md)
- File templates: [`references/templates/`](../references/templates/) (per-template files)
- Naming and placement rules: [`references/docs-structure-rules.md`](../references/docs-structure-rules.md)
- Agent integration and enforcement: [`references/agent-integration-and-enforcement.md`](../references/agent-integration-and-enforcement.md)
- OpenAI Agents SDK config: [`agents/openai.yaml`](./openai.yaml)
