# Project Overview

Doc type: project-overview
Owner: maintainers
Status: active
Last updated: 2026-04-28
Last verified: 2026-04-28
Verified against: synthetic example scope
Confidence: medium
Canonical source: `docs/project-overview.md`
Related docs: `architecture.md`, `requirements/user-stories-and-use-cases.md`

## Project Goal

Provide a simple issue tracker that helps a small team capture, assign, label,
and close work items without losing current status.

## Problem Statement

Small teams need a shared place to record issue ownership and state. Without a
tracked workflow, work can be duplicated, forgotten, or blocked without a clear
owner.

## Target Users or Actors

| User or actor | Goal | Notes |
| --- | --- | --- |
| Contributor | Create and update issues | Primary user of the web UI |
| Maintainer | Assign work and manage labels | Needs visibility into status and ownership |
| Agent or automation | Resume issue-label work safely | Reads feature docs and implementation state |

## Success Criteria

- Users can create, assign, label, and close issues.
- Maintainers can see issue status and ownership without reading code.
- Agents can resume active feature work from the docs without prior chat history.

## Current Scope

- issue CRUD
- assignee selection
- status changes
- label management in progress

## Non-Goals

- billing
- public issue submission
- external integrations

## Evidence

This example is synthetic. In a real repository, this section should cite source
files, tests, routes, schemas, configuration, and user guidance.

## Open Questions

- Production deployment and real user permissions are outside the example scope.
