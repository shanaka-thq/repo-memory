# Operations Runbook

Status: current
Doc Type: baseline
Owner: maintainers
Last Verified: 2026-04-28
Confidence: low

## Local Recovery

1. Check service logs.
2. Confirm database connectivity.
3. Re-run migrations if schema drift is suspected.

## Runtime Signals

See [`observability-and-instrumentation.md`](./observability-and-instrumentation.md)
for expected logs, metrics, analytics events, audit events, alerts, and known
blind spots.

## Production Notes

Production deployment details are not included in this example.
