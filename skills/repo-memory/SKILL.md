---
name: repo-memory
description: Apply the Repo Memory standard to create and maintain repo-native project context docs. Use when an AI coding agent or maintainer is starting a project, adopting an existing codebase, reconstructing architecture or feature decisions from code and history, adding or researching features, resuming interrupted work, or standardizing documentation so humans and agents can understand goals, users, architecture, requirements, decisions, implementation status, evidence, and exact handoff state.
---

# Repo Memory Skill

Version: 3.0.0 <!-- x-release-please-version -->

> This version marker is managed by release-please. Do not edit it manually.

Repo Memory is an agent-first, CLI-assisted memory protocol for software repositories.
Use the smallest mode that fits the task.

## Modes

- Maintainer: update existing Repo Memory docs during normal feature work.
- Bootstrapper: inspect an existing or legacy repo and draft initial memory docs into `docs/intake/`.
- Planner: create implementation plans in the configured plans path.
- Reviewer: create codebase, architecture, security, performance, accessibility, or AI reviews in the configured reviews path.
- Auditor: check documentation drift, missing ownership, stale docs, and risky duplication.
- Generator: generate derived indexes such as feature registry, next-work queue, and doc-health reports.

## Always-loaded rules

1. Load only task-relevant docs.
2. Use `docs/README.md` or configured ownership map as the context router.
3. Do not duplicate canonical facts.
4. Do not manually edit generated files.
5. Do not promote intake, plans, or reviews into canonical docs without review.
6. Mark inferred claims clearly with evidence.
7. Prefer small, reviewable changes.
8. Use the Repo Memory CLI for doctor, validate, generate, migrate, and adapter installation when available.

Choose the mode, then load only that mode file and relevant examples.
