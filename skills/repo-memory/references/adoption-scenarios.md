# Adoption Scenarios

Internal reference for all situations where Repo Memory may be adopted. Use this to verify the skill works correctly across the full spectrum of real-world repos.

## Core Principle

In every scenario, RM adds only the **continuity layer** (ownership map + feature state + work queue). It never duplicates what exists or competes with companion skills.

---

## Greenfield Projects

| #   | Scenario                   | Existing State                              | RM Output                                                                |
| --- | -------------------------- | ------------------------------------------- | ------------------------------------------------------------------------ |
| 1   | Empty repo                 | README + package.json                       | Ownership map + feature template                                         |
| 2   | Empty with intake dumps    | `docs/intake/` has brainstorms, chat notes  | Ownership map, link intake as source, feature stubs from accepted ideas  |
| 3   | New with Kiro specs        | `.kiro/specs/` defines requirements + tasks | Ownership map points to specs. Feature docs track implementation status. |
| 4   | New with Superpowers plans | `docs/superpowers/plans/` has plans         | Ownership map, feature docs link plans, track what's been implemented    |
| 5   | Multiple agents from day 1 | Empty CLAUDE.md + AGENTS.md                 | Ownership map, thin adapters, feature tracking for handoffs              |

## Existing Projects — Good State

| #   | Scenario                          | Existing State                                          | RM Output                                                                  |
| --- | --------------------------------- | ------------------------------------------------------- | -------------------------------------------------------------------------- |
| 6   | Good docs, outdated               | Architecture.md, ADRs, README — stale 6+ months         | Ownership map pointing to existing docs, staleness noted in doc-health     |
| 7   | Good docs, no handoff             | Solid README, CONTRIBUTING, API docs — no "what's next" | Feature tracking layer only. Existing docs untouched.                      |
| 8   | Good docs, single-agent expanding | Well-maintained with Claude — adding Codex/Copilot      | Thin adapters + feature state as cross-tool bridge                         |
| 9   | Mature OSS repo                   | CHANGELOG, ADR folder, RFC process, issue tracker       | Ownership map links everything. RM adds only: feature handoff + work queue |

## Existing Projects — Bad State

| #   | Scenario                 | Existing State                                       | RM Output                                                                              |
| --- | ------------------------ | ---------------------------------------------------- | -------------------------------------------------------------------------------------- |
| 10  | Horrible docs, scattered | Random .md files, outdated wiki dumps, conflicts     | Ownership map naming what exists. Don't rewrite — map and add feature tracking.        |
| 11  | No docs, large codebase  | 50+ files, tests, CI — zero documentation            | Ownership map with "TODO" for most capabilities. Feature stubs for active work only.   |
| 12  | Docs exist but lie       | Architecture.md says monolith, code is microservices | Ownership map, flag discrepancy in doc-health. Don't rewrite — that's a separate task. |
| 13  | AI-generated docs dump   | Previous agent hallucinated 15 doc files             | Ownership map, mark everything `confidence: low`. Don't delete — just don't trust.     |

## Mid-Project / Transition

| #   | Scenario                               | Existing State                                        | RM Output                                                                    |
| --- | -------------------------------------- | ----------------------------------------------------- | ---------------------------------------------------------------------------- |
| 14  | Agent crashed mid-feature              | Uncommitted changes, half-written feature, no handoff | Feature doc with recovery state: what was found, what's safe, what's risky.  |
| 15  | Switching agents                       | Was Cursor, now Claude Code                           | Install adapter, same ownership map. Feature docs carry the state.           |
| 16  | Adding RM alongside existing specs     | Kiro specs + tasks already driving development        | RM sits alongside — cross-session continuity only. Links to specs.           |
| 17  | Team project, multiple humans + agents | 3 devs, different tools, stepping on each other       | Feature registry as coordination surface. "I'm working on X" in frontmatter. |

## Edge Cases

| #   | Scenario             | Existing State                           | RM Output                                                                              |
| --- | -------------------- | ---------------------------------------- | -------------------------------------------------------------------------------------- |
| 18  | Monorepo             | 5 apps, different doc states each        | One root ownership map, per-app feature docs with prefixes                             |
| 19  | Tests-as-docs        | Great test coverage, zero prose          | Ownership map acknowledges tests as behavior source. Feature tracking for active work. |
| 20  | Custom doc framework | Company uses Docusaurus, mdbook, or wiki | RM adds continuity layer only (feature state + queue). Links to existing system.       |

## Companion Workflows

| #   | Scenario                       | Existing State                                     | RM Output                                                                              |
| --- | ------------------------------ | -------------------------------------------------- | -------------------------------------------------------------------------------------- |
| 21  | Superpowers specs + plans      | Full Obra workflow: specs → plans → implementation | Ownership map + feature status + queue. Links to specs/plans. Doesn't duplicate.       |
| 22  | Kiro specs as driver           | `.kiro/specs/` defines all work, Kiro tracks tasks | Cross-session handoff only. Ownership map says "requirements in .kiro/specs/".         |
| 23  | Dedicated planning skill       | Planning skill writes to `docs/plans/`             | RM doesn't plan. Feature doc links plan, records "at step 3/7."                        |
| 24  | Dedicated review skill         | Review skill produces findings/recommendations     | RM doesn't review. Feature doc notes "review done, 2 findings accepted" + link.        |
| 25  | Acquire-codebase-knowledge     | Skill produced ARCHITECTURE.md, STACK.md, etc.     | Ownership map points to those outputs. Doesn't regenerate.                             |
| 26  | Multiple companion skills      | Superpowers + review skill + planning skill + RM   | RM is routing/status only. Each skill owns its output. RM links all from feature docs. |
| 27  | Skill output conflicts with RM | Planning skill says 80% done, RM says in_progress  | RM feature doc is canonical status. Skill output is advisory evidence.                 |
| 28  | MCP memory server alongside RM | Agent has memory MCP for session recall + RM       | MCP handles intra-session. RM handles cross-tool status and "what's official."         |

---

## Validation Rules (Across All Scenarios)

In every scenario, verify:

- [ ] RM did NOT create docs that another skill/tool already owns
- [ ] RM did NOT rewrite existing healthy docs
- [ ] RM DID create an ownership map (or note that one should exist)
- [ ] RM DID track feature state for active work
- [ ] RM DID make the next-work-queue available for any agent to pick up
- [ ] Token cost stays minimal (ownership map + relevant feature doc only during normal work)
- [ ] Companion skill outputs are linked, not duplicated
- [ ] Agent-local memory is complemented, not replaced
