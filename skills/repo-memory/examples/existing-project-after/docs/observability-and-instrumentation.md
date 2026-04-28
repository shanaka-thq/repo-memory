# Observability and Instrumentation

Doc type: observability-and-instrumentation
Owner: maintainers
Status: active
Last updated: 2026-04-28
Last verified: 2026-04-28
Verified against: synthetic example scope
Confidence: low
Canonical source: `docs/observability-and-instrumentation.md`
Related docs: `operations-runbook.md`, `security-and-privacy.md`, `requirements/non-functional-requirements.md`

## Goals

- Show whether issue creation, assignment, status changes, and label updates are
  succeeding.
- Give maintainers enough runtime signals to diagnose failed requests.

## Logs

| Signal | Source | Purpose | Retention or privacy notes |
| --- | --- | --- | --- |
| Request log | API service | Diagnose failed issue operations | Do not log issue descriptions when they may contain sensitive details |

## Metrics

| Metric | Source | Purpose | Alert or dashboard |
| --- | --- | --- | --- |
| Issue mutation error rate | API service | Detect degraded issue workflows | Not configured in this synthetic example |

## Traces

- No distributed tracing is configured in this synthetic example.

## Product Analytics Events

| Event | Trigger | Properties | Privacy notes |
| --- | --- | --- | --- |
| `issue_created` | User creates an issue | issue id, creator role | Do not include full issue description |
| `issue_label_added` | User adds a label | issue id, label id | Label names may be sensitive in some repos |

## Audit Events

- Assignment changes should be auditable when permissions are introduced.
- Label changes should record actor, issue id, label id, and timestamp.

## Dashboards and Alerts

- Dashboard: not configured in this synthetic example.
- Alert: not configured in this synthetic example.
- Escalation path: maintainer checks API logs and issue mutation failures.

## Privacy and Retention

- PII handling: do not log free-form issue descriptions.
- Sampling: unknown.
- Retention: unknown.
- Access controls: unknown.

## Known Blind Spots

- Production retention and alerting are not modeled.
- No tracing is available for multi-service diagnostics.

## Related Code and Config

- Synthetic example only; a real repo should cite logging, metrics, analytics,
  alerting, and deployment configuration.
