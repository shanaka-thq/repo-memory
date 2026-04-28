# Decision Log

Status: current
Doc Type: decision-log
Owner: maintainers
Last Verified: 2026-04-28
Confidence: medium

## 2026-04-28: Use Repo Docs as Canonical Agent Memory

Status: accepted
Confidence: high

### Context

Multiple agents may work on the project, and chat history is not a reliable
handoff surface.

### Decision

Store architecture, requirements, implementation history, feature status, and
handoff notes under `docs/`.

### Consequences

- agent instruction files stay short
- feature docs must be updated before stopping work
- stale docs are tracked in `doc-health.md`
