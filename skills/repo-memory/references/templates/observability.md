## Observability and Instrumentation Template

Use this template for `docs/observability-and-instrumentation.md`. This document owns the runtime and product signals that explain whether the system is healthy, usable, and diagnosable.

```md
# Observability and Instrumentation

Doc type: observability-and-instrumentation
Owner: current-agent-or-team
Status: active
Last updated: 2026-04-28
Last verified: unknown
Verified against: unknown
Confidence: medium
Canonical source: `docs/observability-and-instrumentation.md`
Related docs: `operations-runbook.md`, `security-and-privacy.md`, `requirements/non-functional-requirements.md`

## Goals

- What operators, maintainers, or product owners need to understand from runtime signals.

## Logs

| Signal      | Source                    | Purpose                   | Retention or privacy notes               |
| ----------- | ------------------------- | ------------------------- | ---------------------------------------- |
| Request log | API gateway or app server | Diagnose request failures | Do not log secrets or sensitive payloads |

## Metrics

| Metric             | Source      | Purpose                  | Alert or dashboard   |
| ------------------ | ----------- | ------------------------ | -------------------- |
| Request error rate | API service | Detect degraded behavior | Operations dashboard |

## Traces

- Trace boundaries, sampled operations, spans, or known gaps.

## Product Analytics Events

| Event              | Trigger             | Properties                 | Privacy notes                                                   |
| ------------------ | ------------------- | -------------------------- | --------------------------------------------------------------- |
| `search_submitted` | User submits search | query length, result count | Do not store raw sensitive query text unless explicitly allowed |

## Audit Events

- Security, compliance, permission, or administrative events that must be recorded.

## Dashboards and Alerts

- Dashboard:
- Alert:
- Escalation path:

## Privacy and Retention

- PII or sensitive-data handling:
- Sampling:
- Retention:
- Access controls:

## Known Blind Spots

- Signal gap 1
- Unverified production behavior 1

## Related Code and Config

- `src/...`
- deployment, logging, tracing, analytics, or monitoring config
```