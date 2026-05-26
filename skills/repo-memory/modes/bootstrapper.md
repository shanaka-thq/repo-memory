# Bootstrapper Mode

Use this mode when adopting an existing or legacy repository that has no prior Repo Memory documentation.

## Instructions

1. **Scope writes:** Write draft files ONLY to the configured intake path (default: `docs/intake/`). Do not modify or create canonical documents directly.
2. **Classify information:** Group findings into confirmed facts, inferred facts, and unknowns.
3. **Require evidence:** Citing code, configuration, comments, commits, or git history is mandatory for any inferred claims. Never present guesses as canonical truth.
4. **No fabrication:** Do not invent user personas, business objectives, architecture, or architectural decisions. State them as unknown if not backed by evidence.
5. **Generate draft files:** Reconstruct the project state by writing the following files to `docs/intake/`:
   - `bootstrap-summary.md`: General description of findings.
   - `evidence-map.md`: Map of code patterns, tests, and configuration files to functional behavior.
   - `inferred-architecture.md`: Inferred system architecture and boundaries.
   - `inferred-data-model.md`: Inferred databases, key models, and data types.
   - `inferred-decisions.md`: Reconstructed decisions with confidence levels (high, medium, low).
   - `unknowns.md`: Consolidated checklist of unresolved questions.
   - `recommended-canonical-docs.md`: Proposed ownership map and transition plan.
6. **Create a promotion checklist:** Include instructions on how the maintainer can review, confirm, and promote these drafts to `docs/` canonical locations.
