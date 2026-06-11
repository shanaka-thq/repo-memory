<!-- Target platform: OpenAI Codex and Codex CLI. Usage: use this guide when wiring the skill into Codex-driven repos or when resuming work with Codex after another agent. -->

# OpenAI Codex Integration Guide

This guide extends the [common agent workflow](../references/agent-workflow-common.md) with OpenAI Codex specifics.

## Core Rule

Treat `docs/README.md` as the first map. Its `Canonical Ownership Map` names
the single owner for architecture, requirements, contracts, decisions, setup,
feature state, implementation history, and resumable handoff context.

Agent-specific prompts, CLI instructions, or wrapper files should point to the
mapped owners instead of duplicating mutable project facts.

## Platform-Specific Notes

- Codex uses `AGENTS.md` as its primary instruction surface.
- When telling Codex to maintain project docs, include expectations like:
  - use the Repo Memory workflow from [`SKILL.md`](../SKILL.md)
  - follow `docs/README.md` and its `Canonical Ownership Map`
  - keep active feature docs resumable for a different future agent
  - keep `docs/feature-registry.md` ranked so a cloud agent can pick the first `ready` row
  - preserve strong existing ADRs, specs, runbooks, and security docs as owners when healthy

## Repo Setup Guidance

If a target repo uses Codex together with other agents:

1. Add a short repo instruction block that points to `docs/README.md`, the
   mapped feature registry owner, and the active feature doc.
2. Avoid storing feature status, blockers, or next steps only in Codex-specific prompts.
3. Keep durable project knowledge in the mapped owners so Copilot, Codex,
   Claude, OpenCode, and humans can all resume from the same place.

## Related Docs

- Common agent workflow: [`references/agent-workflow-common.md`](../references/agent-workflow-common.md)
- Skill definition: [`SKILL.md`](../SKILL.md)
- Agent integration and enforcement: [`references/agent-integration-and-enforcement.md`](../references/agent-integration-and-enforcement.md)
- File templates: [`references/templates.md`](../references/templates.md)
