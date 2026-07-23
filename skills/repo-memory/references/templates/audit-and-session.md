## Existing Project Audit Snippet

```md
## Documentation Audit

| Target doc                                   | Evidence source                                          | Confidence | Gaps                                   |
| -------------------------------------------- | -------------------------------------------------------- | ---------- | -------------------------------------- |
| `architecture.md`                            | `src/`, runtime config, deploy files                     | High       | no explicit scaling rationale          |
| `local-development.md`                       | package scripts, Makefile, setup docs                    | High       | seed-data workflow unclear             |
| `doc-health.md`                              | current docs, code evidence, recent changes              | Medium     | full audit not yet completed           |
| `observability-and-instrumentation.md`       | logging config, telemetry code, dashboards, alert config | Medium     | production retention unknown           |
| `requirements/user-stories-and-use-cases.md` | product notes, UI tests, support docs                    | Medium     | admin use cases incomplete             |
| `diagrams/system-context.mmd`                | architecture docs, service boundaries, deploy files      | High       | queue edges not yet shown              |
| `decision-log.md`                            | legacy docs, commits, comments                           | Medium     | some rationale inferred                |
| `designs/answer-search-architecture.md`      | RFC notes, recent commits, architecture comments         | Medium     | rollout plan only partially documented |
| `project-details/order-lifecycle.md`         | workflow services, tests, ops notes                      | Medium     | failure handling still inferred        |
| `components/search-results-panel.md`         | UI state code, component tests                           | High       | accessibility rationale missing        |
| `diagrams/search-flow.drawio`                | design workshop artifact, implementation notes           | Medium     | Mermaid equivalent not maintained      |
| `ui-ux/search-results-experience.md`         | design mocks, component stories, browser checks          | Medium     | mobile behavior not fully documented   |
| `security-and-privacy.md`                    | env config, auth middleware, infra docs                  | Medium     | production posture unclear             |
```

## Session-Close Checklist

Before ending a session, confirm:

1. The feature doc status is current.
2. The checklist reflects reality.
3. Files touched are listed.
4. Blockers and risks are explicit.
5. The next step is written for another agent, not just for yourself.
6. The feature registry `Next Work Queue` reflects what a cloud agent should pick next.
7. The implementation log is updated if meaningful work landed.
8. The decision log is updated if a lasting technical choice changed.
9. Inferred statements and missing rationale are explicitly marked.
10. Any deep-dive docs are linked from their parent feature doc, index, or baseline doc.
11. Tricky project or component logic is documented in the repo, not stranded in chat history.
12. Local tooling changes are reflected in `local-development.md`.
13. Runtime signals, product analytics, audit events, dashboards, and alerts are reflected in `observability-and-instrumentation.md`.
14. User-facing changes update user stories, use cases, and UI or UX docs when relevant.
15. Diagram sources are preserved and linked, not replaced casually with screenshots or chat-only sketches.
16. Any agent-specific instruction files still point to the ownership map.
17. `doc-health.md` records material doc changes, stale docs, conflicts, renames, and verification state.
