# User Stories and Use Cases

Doc type: user-stories-and-use-cases
Owner: maintainers
Status: active
Last updated: 2026-04-28
Last verified: 2026-04-28
Verified against: synthetic example scope
Confidence: medium
Canonical source: `docs/requirements/user-stories-and-use-cases.md`
Related docs: `../project-overview.md`, `functional-requirements.md`

## Actors

| Actor | Primary goal | Permissions or constraints | Related journeys |
| --- | --- | --- | --- |
| Contributor | Create and update issues | Can create issues and update own issue details | Create issue, update issue |
| Maintainer | Assign, label, and close issues | Can manage labels and assignment | Triage issue, close issue |
| Agent or automation | Resume work safely | Must follow docs and feature handoff state | Continue label-management feature |

## Personas or User Segments

| Persona or segment | Context | Needs | Risks |
| --- | --- | --- | --- |
| Small-team contributor | Reports issues during development | Fast issue creation and clear ownership | Duplicated or forgotten work |
| Project maintainer | Reviews issue queue | Reliable status and label management | Incorrect assignment or unclear priority |

## User Stories

- As a contributor, I want to create an issue with a title and description so that work is visible to the team.
- As a maintainer, I want to assign an issue to a team member so that ownership is clear.
- As a maintainer, I want to add labels to an issue so that related work can be grouped.
- As an agent, I want a current feature handoff so that I can resume implementation without prior chat context.

## Journey Map

| Journey | Actor | Start state | Desired outcome | Related docs |
| --- | --- | --- | --- | --- |
| Create issue | Contributor | Has a bug or task to report | Issue exists with title and description | `../interfaces-and-contracts.md` |
| Triage issue | Maintainer | Issue is open and unassigned | Issue has owner, status, and labels | `../features/issue-labels.md` |

## Primary Use Cases

### Use Case: Create an issue

Actor: Contributor
Preconditions:

- User can access the issue tracker.

Main flow:

1. User enters title and description.
2. System validates required fields.
3. System creates the issue with status `open`.

Alternative flows:

- User submits a missing title.
- User cancels before saving.

Failure states:

- Validation fails.
- API request fails.

Acceptance notes:

- Missing title errors are deterministic.
- Created issue appears in the issue list.

Instrumentation notes:

- Record issue creation success and validation failure counts when analytics are enabled.

## Accessibility and Inclusion Notes

- Form errors should be visible near the affected field.
- Status and label changes should not rely on color alone.

## Open Questions

- Real production permission boundaries are not modeled in this synthetic example.
