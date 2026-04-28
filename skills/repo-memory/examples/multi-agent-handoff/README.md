# Multi-Agent Handoff Example

This example shows the minimum handoff information an active feature doc should
contain before one agent stops and another resumes.

## Scenario

Agent A audited the code and started documenting a search feature. Agent B will
continue later without access to the original chat.

## Handoff Surface

The handoff lives in [`search-indexing.md`](./search-indexing.md), not in a chat
summary or platform-specific agent memory.

The important fields are:

- implementation status
- validation state
- exact next safe step
- files or docs already inspected
- areas to avoid
- exact next prompt
