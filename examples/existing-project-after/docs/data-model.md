# Data Model

Status: current
Doc Type: baseline
Owner: maintainers
Last Verified: 2026-04-28
Confidence: medium

## Entities

| Entity | Purpose |
| --- | --- |
| User | Person who can own or update issues |
| Issue | Work item tracked by the system |
| Label | Reusable classification attached to issues |
| Status History | Audit trail of issue state changes |

## Relationships

- An issue has one assignee.
- An issue can have many labels.
- Status history belongs to one issue.
