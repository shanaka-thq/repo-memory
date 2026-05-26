# Repo Memory Artifact Taxonomy

This document describes the taxonomy of artifacts in a Repo Memory v3 compliant project. Use this reference to determine where files belong, whether they represent canonical truth, and how findings are promoted.

## Artifact Classification

| Artifact type | Default location | Canonical? | Purpose |
| :--- | :--- | :--- | :--- |
| **Project overview** | `docs/project-overview.md` | Yes | Durable summary of project goals, actors, success criteria, and non-goals. |
| **Architecture** | `docs/architecture.md` | Yes | Durable system truth, service boundaries, and architecture structure. |
| **Feature state** | `docs/features/*.md` | Yes | Per-feature current status, next safe steps, blockers, and evidence. |
| **ADRs** | `docs/adr/*.md` | Yes | Durable, cross-cutting architectural and design decisions. |
| **Runbooks** | `docs/runbooks/*.md` | Yes | Operational guidelines, commands, and deployment verification. |
| **Plans** | `docs/plans/` | No | Working implementation intent, risks, checklist steps. |
| **Reviews** | `docs/reviews/` | No | Evidence, specialist assessment, second-agent reviews. |
| **Intake drafts** | `docs/intake/` | No | Unreviewed raw material, brainstorms, bootstrap output. |
| **Generated registry** | `docs/generated/feature-registry.md` | No | Derived feature list (automatically generated). |
| **Generated queue** | `docs/generated/next-work-queue.md` | No | Derived next-work queue (automatically generated). |
| **Generated health** | `docs/generated/doc-health.md` | No | Derived health and validation report (automatically generated). |
| **History** | `docs/history/` | Historical | Archived plans, reviews, or deprecated central registries. |

## Key Rule

Only **canonical** documents represent durable project truth. Plans, reviews, intake files, generated files, and history are **supporting artifacts** and must not be used as canonical sources of truth without a formal review/promotion step.

## Promotion Flow

Findings and planning flow through a specific lifecycle to maintain documentation health:

```text
Review finding
   ↓ accepted
Plan or task
   ↓ implemented
Feature doc / ADR / architecture doc
   ↓ generated
Registry / queue / doc-health
```
