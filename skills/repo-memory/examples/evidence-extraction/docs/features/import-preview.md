# Import Preview

Doc type: feature
Owner: current-agent-or-team
Status: in_progress
Last updated: 2026-05-22
Last verified: 2026-05-22
Verified against: `../intake/2026-05-22-evidence-extraction.md`
Confidence: high
Canonical source: this file
Related docs: `../feature-registry.md`, `../doc-health.md`
Feature slug: import-preview

## Summary

Import preview lets a user inspect CSV import results before committing them.
The behavior is accepted as canonical feature state because both source and
tests in the evidence report support it.

## Evidence

- `../intake/2026-05-22-evidence-extraction.md`

## Implementation Status

Validation status: in_progress

- [x] Promote confirmed preview behavior into this feature doc.
- [ ] Verify whether rollback behavior is user-facing before adding it to
  functional requirements.

## Validation

- Confirmed from the evidence extraction report: preview happy path and
  malformed CSV behavior have test evidence.
- Not yet confirmed: rollback behavior.

## Next Agent Handoff

Start by verifying rollback behavior from tests or runtime behavior. Do not
promote rollback as a requirement until evidence supports it.
