# Interfaces and Contracts

Status: current
Doc Type: baseline
Owner: maintainers
Last Verified: 2026-04-28
Confidence: medium

## HTTP API

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/api/issues` | List issues |
| `POST` | `/api/issues` | Create an issue |
| `PATCH` | `/api/issues/{id}` | Update issue fields |
| `POST` | `/api/issues/{id}/labels` | Attach a label |

## Contract Rules

- Issue titles are required.
- Status values are `open`, `in_progress`, and `closed`.
- Labels must exist before being attached to an issue.
