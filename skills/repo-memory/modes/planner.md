# Planner Mode

Use this mode when the user requests an implementation, migration, refactor, release, or investigation plan.

## Instructions

1. **Target path:** Output new plans to the active directory under the configured plans path (default: `docs/plans/active/YYYY-MM-DD-<slug>.md`).
2. **Plans are not canonical truth:** Treat plans as proposed, temporary work items. They contain intent, not current system shape.
3. **Cross-link:** Link plans back to related features (`docs/features/`), reviews, ADRs, and relevant source code areas.
4. **Draft sections:** Include goals, options, risks, unknowns, proposed changes, and step-by-step checklists.
5. **Durable promotion:** When the plan is implemented, promote any durable outcomes (such as architecture changes, new features, or decisions) to feature documents, ADRs, or architecture documents.
6. **Plan lifecycle:**
   - Move completed plans to `<plans-path>/completed/`.
   - Move abandoned plans to `<plans-path>/abandoned/`.
