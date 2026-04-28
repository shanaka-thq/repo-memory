# Security and Privacy

Status: current
Doc Type: baseline
Owner: maintainers
Last Verified: 2026-04-28
Confidence: medium

## Security Expectations

- authenticate API requests
- authorize issue updates by role
- avoid logging secrets
- validate all user-provided issue fields server-side

## Privacy Expectations

Issue content may contain customer-sensitive information. Logs and exports
should avoid unnecessary issue body content.
