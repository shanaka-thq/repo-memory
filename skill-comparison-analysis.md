# Skill Analysis: Repo-Memory vs. Matt Pocock Skills

## Overview

This analysis compares the **repo-memory skill** (cross-tool continuity layer) with **15 Matt Pocock engineering skills** to identify overlaps, gaps, and integration opportunities.

## Skill Comparison Table

| Skill | What It Does (One Sentence) | Artifacts/State Produced | Artifact Location | Cross-Session/Cross-Agent Continuity? | Overlap with RM Concepts |
|-------|----------------------------|--------------------------|-------------------|--------------------------------------|--------------------------|
| **repo-memory** | Provides cross-tool continuity through repository-based feature state tracking, ownership maps, and auto-generated work queues | Ownership maps, feature docs with frontmatter, generated indexes (feature registry, next-work-queue) | `docs/` directory in repo (Markdown files) | **YES** - Explicitly designed for cross-tool/session continuity | **CORE** - Directly implements feature state tracking, ownership maps, work queues, handoff notes |
| **handoff** | Compacts current conversation into handoff document for another agent | Handoff summary document | OS temporary directory (ephemeral) | **Partial** - Only immediate session transfer | Overlap: Handoff notes (but ephemeral vs. repo-based) |
| **implement** | Implements work based on a spec or set of tickets | Code implementation, commits | Code files in repo | **NO** - Single-session execution | No direct overlap |
| **wayfinder** | Plans large work as shared map of decision tickets on issue tracker | Wayfinder maps, decision tickets | Issue tracker (GitHub/GitLab/issues) or local files | **Partial** - Through issue tracker | Partial: Work planning but issue-based, not repo-based feature state |
| **to-spec** | Turns conversation into spec and publishes to issue tracker | Specification documents | Issue tracker (issues) | **Partial** - Through issue tracker | Partial: Spec creation but issue-based, not linked to feature state |
| **to-tickets** | Breaks plans/specs into tracer-bullet tickets with blocking edges | Implementation tickets | Issue tracker or `.scratch/` directory | **Partial** - Through issue tracker | Partial: Work breakdown but issue-based, not auto-generated queues |
| **triage** | Moves issues through triage state machine and writes agent-ready briefs | Triage labels, agent briefs | Issue tracker (comments, labels) | **Partial** - Through issue tracker | No direct overlap |
| **code-review** | Reviews changes along Standards and Spec axes via parallel sub-agents | Review findings | Console output (ephemeral) | **NO** - Single-session review | No direct overlap |
| **writing-plans** | Creates comprehensive implementation plans from specs | Implementation plans | `docs/superpowers/plans/` directory | **Partial** - Plan files persist | Partial: Planning but separate from feature state |
| **executing-plans** | Executes written implementation plans with review checkpoints | Code implementation | Code files in repo | **NO** - Single-session execution | No direct overlap |
| **claude-handoff** | Hands conversation to fresh background agent with summary | Background agent process | Background process (ephemeral) | **Partial** - Immediate agent transfer | Overlap: Handoff (but process-based vs. document-based) |
| **domain-modeling** | Builds and sharpens project domain model | CONTEXT.md, ADRs | `CONTEXT.md`, `docs/adr/` in repo | **YES** - Repository-based | Partial: Documentation but focused on domain, not feature state |
| **improve** | Surveys codebase and produces implementation plans for other agents | Audit findings, implementation plans | `plans/` or `advisor-plans/` directory | **Partial** - Plan files persist | Partial: Planning but separate from feature state |
| **research** | Investigates questions via background agent and captures findings | Research notes | Markdown files in repo | **YES** - Repository-based | Partial: Documentation but focused on research, not feature state |
| **setup-matt-pocock-skills** | Configures repo for engineering skills (issue tracker, triage labels, domain docs) | Configuration files | `docs/agents/` directory | **YES** - Configuration persists | No direct overlap |
| **grill-with-docs** | Runs grilling session while creating docs (ADRs and glossary) | ADRs, glossary updates | `docs/adr/`, `CONTEXT.md` | **YES** - Repository-based | Partial: Documentation creation |

## Gap Analysis: What Repo-Memory Provides That NO Matt Pocock Skill Covers

Repo-memory fills **critical gaps** in the Matt Pocock skill ecosystem:

### 1. **Repository-Based Feature State Tracking**
- **Gap**: No Matt Pocock skill provides a standardized way to track feature status, next safe steps, blockers, and handoff notes **in the repository itself**
- **Repo-Memory Solution**: `docs/features/*.md` with machine-readable frontmatter (status, ready, next_safe_step, priority)

### 2. **Canonical Ownership Maps**
- **Gap**: No skill answers "where does each kind of truth live?" - which doc owns ADRs, specs, OpenAPI, setup, security, etc.
- **Repo-Memory Solution**: `docs/README.md` ownership map that points to existing docs instead of duplicating them

### 3. **Auto-Generated Work Queues**
- **Gap**: Skills create work items (tickets, plans) but none auto-generates "what should the next agent pick up?" from feature metadata
- **Repo-Memory Solution**: `docs/generated/next-work-queue.md` auto-built from feature frontmatter

### 4. **Cross-Tool Continuity Layer**
- **Gap**: Matt Pocock skills use different storage methods (issue trackers, temp files, local files) with no unified persistence
- **Repo-Memory Solution**: Single repository-based persistence layer that works with any tool that reads files

### 5. **Explicit Handoff State Management**
- **Gap**: Handoff skills create ephemeral documents; no persistent record of where work stopped and what's next
- **Repo-Memory Solution**: Feature docs capture handoff state that survives agent crashes and tool switches

### 6. **Skill Integration Framework**
- **Gap**: Skills operate independently with no standard way to link their outputs
- **Repo-Memory Solution**: Ownership map links to outputs from planning, review, and spec skills

### 7. **Drift Detection and Validation**
- **Gap**: No skill validates documentation health or detects stale/broken docs
- **Repo-Memory Solution**: Validation scripts check for drift, stale docs, broken links, duplicate ownership

## Redundancies: Where Repo-Memory Duplicates Existing Skills

**Minimal redundancy** - Repo-memory is designed as a **complementary layer**, not a competitor:

### 1. **Planning Skills (`wayfinder`, `to-spec`, `to-tickets`, `writing-plans`)**
- **No duplication**: These create plans/specs; repo-memory **links to them** from feature docs
- **Integration**: Feature docs reference spec URLs, record what was accepted from planning sessions

### 2. **Review Skills (`code-review`, `triage`, `improve`)**
- **No duplication**: These perform reviews/audits; repo-memory **records that they happened** and links to outputs
- **Integration**: Feature docs note review completion and link to review artifacts

### 3. **Handoff Skills (`handoff`, `claude-handoff`)**
- **Partial overlap but complementary**: These create immediate handoffs; repo-memory provides persistent handoff state
- **Integration**: Ephemeral handoffs can reference repo-memory feature docs for context

### 4. **Documentation Skills (`domain-modeling`, `research`, `grill-with-docs`)**
- **No duplication**: These create specific docs; repo-memory's ownership map **points to them**
- **Integration**: Ownership map declares which doc owns domain modeling, research findings, etc.

## Integration Architecture

Repo-memory serves as the **glue layer** between Matt Pocock skills:

```
┌─────────────────────────────────────────────────────────────┐
│                    Matt Pocock Skills                        │
├─────────────┬─────────────┬─────────────┬─────────────┤
│  Planning   │  Execution  │   Review    │    Docs     │
│  (wayfinder,│  (implement,│  (code-     │  (domain-   │
│   to-spec,  │  executing- │   review,   │   modeling, │
│   to-tickets│   plans)    │   triage,   │   research) │
│   writing-  │             │   improve)  │             │
│   plans)    │             │             │             │
└─────────────┴─────────────┴─────────────┴─────────────┘
        │             │             │             │
        │             │             │             │
        ▼             ▼             ▼             ▼
┌─────────────────────────────────────────────────────────────┐
│                 Repo-Memory Continuity Layer                 │
│                                                             │
│  docs/README.md          ← Ownership Map                   │
│  docs/features/*.md      ← Feature State & Handoff         │
│  docs/generated/*.md     ← Auto-Generated Indexes          │
│                                                             │
│  • Links to planning outputs                               │
│  • Records review completion                               │
│  • Tracks implementation status                            │
│  • Points to documentation owners                          │
└─────────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│                Any AI Agent / Human Developer                │
│                (Claude, Codex, Copilot, Cursor,             │
│                 Kiro, OpenCode, etc.)                       │
└─────────────────────────────────────────────────────────────┘
```

## Recommendations

### 1. **Adopt Repo-Memory as Complementary Layer**
- Use repo-memory alongside existing Matt Pocock skills
- Update feature docs during planning, execution, and review
- Link skill outputs from ownership map

### 2. **Skill Integration Points**
- **Planning skills**: Reference created specs in feature docs
- **Execution skills**: Update feature status and next_safe_step
- **Review skills**: Record review completion in feature docs
- **Handoff skills**: Include reference to feature doc in handoff

### 3. **Configuration Synchronization**
- Ensure `setup-matt-pocock-skills` config works with repo-memory ownership map
- Add repo-memory to `## Agent skills` section in `CLAUDE.md`/`AGENTS.md`

### 4. **Workflow Enhancement**
- Agents should check `docs/generated/next-work-queue.md` when idle
- Use feature docs as primary handoff surface instead of ephemeral documents
- Run repo-memory validation scripts during CI/CD

## Conclusion

Repo-memory fills **critical continuity gaps** in the Matt Pocock skill ecosystem without duplicating core functionality. It provides the missing repository-based persistence layer that enables:

1. **Cross-tool handoffs** without relying on tool-specific memory
2. **Feature state tracking** that survives agent crashes
3. **Auto-generated work queues** from feature metadata
4. **Ownership maps** that prevent documentation duplication
5. **Integration framework** that links planning, execution, and review artifacts

The Matt Pocock skills remain essential for their specialized workflows (planning, review, implementation), while repo-memory provides the connective tissue that makes the entire ecosystem **resumable across sessions and tools**.