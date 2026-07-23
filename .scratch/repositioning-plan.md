# Repo Memory — Repositioning Plan

## Decisions Locked (from grilling session)

1. **Identity:** RM is the state persistence layer. Always. Thickness flexes based on what other skills exist, identity doesn't.
2. **Protocol:** Session-start read → work with any skills → session-end write-back.
3. **Staleness:** Best-effort write-back + drift detection on next session start. Self-correcting.
4. **Compatibility:** Level 2 — typed slots in ownership map, skill-agnostic. RM knows artifact *categories*, not specific skills.
5. **Extensibility:** Opinionated categories (plans, specs, tickets, ADRs, reviews, handoff, research) + open "additional" section.
6. **Modes:** Keep all four (Bootstrapper, Maintainer, Auditor, Generator). Generator becomes invisible (auto-runs after Maintainer writes).
7. **Name:** Keep "Repo Memory" — reframe as "institutional memory."

---

## 1. New Description (SKILL.md frontmatter)

Current:
```
Use when AI coding agents need cross-tool continuity, resumable feature state, or a shared work queue...
```

Proposed (≤1024 chars, front-loaded leading word, "Use when" trigger format, heavy trigger phrases):
```yaml
description: >-
  Persist feature state, ownership maps, and work queues as repo-native Markdown
  so any agent resumes where the last one stopped. Use when switching between
  agents or sessions and the next agent needs to know what's in progress, what's
  blocked, and what to pick up next. Also use when the user says "where did I
  leave off," "what's the status," "set up project memory," "what should I work
  on next," "handoff notes," "resume from last session," "shared work queue,"
  or "what's in flight." For planning, see /writing-plans or /wayfinder. For
  implementation, see /implement. For code review, see /code-review.
```

Key changes:
- Leads with the verb "Persist" (what it does, not what it is)
- "repo-native Markdown" signals zero-infra
- Heavy trigger-phrase loading (learned from marketingskills pattern)
- Cross-references complementary skills with "For X, see Y" pattern
- Drops the laundry list of agent names from the description (that goes in README)

### Related Skills section (add to bottom of SKILL.md)

Following the marketingskills pattern, add a "Related Skills" section:

```markdown
## Related Skills

- **writing-plans** / **wayfinder**: Planning and decomposition — RM links their outputs
- **implement** / **executing-plans**: Implementation — RM tracks status before/after
- **code-review**: Review — RM records that a review happened
- **to-tickets** / **triage**: Work tracking — RM's ownership map points to the tracker
- **handoff**: Ephemeral session handoff — RM persists the durable parts
- **domain-modeling** / **grill-with-docs**: ADRs and context — RM maps where they live
- **research** / **improve**: Investigation outputs — RM registers their artifact locations
```

### Foundation Skill Pattern

Following marketingskills' `product-marketing` pattern (read by all other skills first),
position RM's ownership map as the foundation context that any workflow skill can check:

```
┌──────────────────────────────────────────────┐
│          Repo Memory (state layer)           │
│   ownership map · feature docs · work queue  │
└──────────────────────┬───────────────────────┘
                       │ read on session start
       ┌───────────────┼───────────────────┐
       ▼               ▼                   ▼
┌─────────────┐ ┌─────────────┐ ┌──────────────────┐
│  Planning   │ │Implementa-  │ │  Review & QA     │
│             │ │   tion      │ │                  │
├─────────────┤ ├─────────────┤ ├──────────────────┤
│/wayfinder   │ │/implement   │ │/code-review      │
│/writing-plan│ │/executing-  │ │/triage           │
│/to-tickets  │ │  plans      │ │/improve          │
│/to-spec     │ │/tdd         │ │/qa               │
└──────┬──────┘ └──────┬──────┘ └────────┬─────────┘
       │               │                 │
       └───────────────┼─────────────────┘
                       ▼ write on session end
┌──────────────────────────────────────────────┐
│          Repo Memory (state layer)           │
│   update frontmatter · link artifacts        │
└──────────────────────────────────────────────┘
```

---

## 2. Compatibility Surface (new reference doc)

Create `skills/repo-memory/references/compatible-skills.md`:

```markdown
# Compatible Skills

Repo Memory is a **state persistence layer** that sits beneath workflow skills.
It doesn't plan, review, spec, or implement — it records where those outputs
live and keeps feature state resumable across agents.

## How Compatibility Works

RM's ownership map has **typed slots** for common artifact categories. Any skill
that produces durable artifacts can register its output location in the relevant
slot. RM doesn't need to know which skill wrote the artifact — only what kind it
is and where it lives.

## Artifact Categories (typed slots)

| Category | What lives here | Example skills that produce this |
|----------|----------------|----------------------------------|
| `plans` | Implementation plans, architecture plans | /writing-plans, /improve, Kiro specs |
| `specs` | Requirements, specifications, PRDs | /to-spec, /brainstorming, manual specs |
| `tickets` | Work items, issues, backlog | /to-tickets, /triage, /wayfinder maps |
| `adrs` | Architecture decision records | /grill-with-docs, /domain-modeling |
| `reviews` | Code review outputs | /code-review, PR comments |
| `handoff` | Session state, next steps, blockers | RM feature docs (native), /handoff |
| `research` | Investigation outputs, findings | /research, /improve audit reports |

## Adding a New Skill's Outputs

When you install a new workflow skill that writes durable artifacts:

1. Identify which category its output belongs to
2. Update the ownership map slot with the path where artifacts land
3. Done — RM will check that location when orienting

Example: Installing `/improve` which writes plans to `plans/`:
```yaml
# In docs/README.md ownership map
plans: plans/    # /improve, /writing-plans
```

## Known Integrations

### Matt Pocock's Skills (`mattpocock/skills`)
| Skill | Writes to | RM slot |
|-------|-----------|---------|
| `/writing-plans` | `docs/superpowers/plans/` | `plans` |
| `/to-tickets` | `.scratch/<feature>/issues/` or GitHub Issues | `tickets` |
| `/to-spec` | GitHub Issues or local file | `specs` |
| `/wayfinder` | Issue tracker (map + child tickets) | `tickets` |
| `/grill-with-docs` | `CONTEXT.md`, `docs/adr/` | `adrs` |
| `/domain-modeling` | `CONTEXT.md` | `adrs` |
| `/code-review` | PR comments or stdout | `reviews` |
| `/research` | `research/<name>` branch | `research` |
| `/improve` | `plans/` or `advisor-plans/` | `plans` |
| `/handoff` | OS temp dir (ephemeral!) | — (RM replaces this) |

### Obra / Superpowers
| Skill | Writes to | RM slot |
|-------|-----------|---------|
| Brainstorming | Specs directory | `specs` |
| Writing plans | `docs/superpowers/plans/` | `plans` |
| Subagent development | Git worktrees | — (transient) |

### Kiro
| Artifact | Location | RM slot |
|----------|----------|---------|
| Spec files | `.kiro/specs/` | `specs` |
| Steering rules | `.kiro/steering/` | — (config, not artifacts) |

## Future-Proofing

To add compatibility with a new skill pack:
1. Identify what artifacts it produces
2. Map each to an existing category (or add to "additional")
3. Add a row to this table
4. No code changes needed — RM's typed slots are the extension point
```

---

## 3. Ownership Map — Typed Slots

Update the ownership map template in `skills/repo-memory/references/templates.md`.

Current ownership map is a flat prose document. Proposed: add a structured section with typed slots:

```markdown
## Artifact Locations

<!-- Where durable artifacts from your workflow skills land.
     Update these when you install new skills. -->

| Category | Location | Produced by |
|----------|----------|-------------|
| Plans | `plans/` | /writing-plans, /improve |
| Specs | `.kiro/specs/` | Kiro specs |
| Tickets | GitHub Issues | /to-tickets, /triage |
| ADRs | `docs/adr/` | /grill-with-docs |
| Reviews | PR comments | /code-review |
| Handoff | `docs/features/` | Repo Memory (native) |
| Research | `research/` branches | /research |
| Additional | — | — |
```

The Bootstrapper mode should ask the user about each category during setup.

---

## 4. Mode Changes

### Bootstrapper (richer)
Add a "skill discovery" step:
- Detect installed skills (check `.agents/skills/`, `.kiro/skills/`, `.claude/skills/`)
- Ask where each category's artifacts land
- Pre-populate the ownership map typed slots

### Maintainer (thinner)
Simplify to:
1. Update feature frontmatter (status, next_safe_step)
2. Link any new artifacts produced this session to the relevant slot
3. Trigger Generator automatically (no separate mode invocation needed)

### Auditor (add drift detection)
Add cross-reference check:
- Compare feature doc status against tracker state (if accessible)
- Flag feature docs that haven't been updated in N sessions
- Check typed slots point to paths that actually exist

### Generator (invisible)
- Remove as a user-facing mode choice
- Auto-runs when Maintainer writes
- Document as "runs automatically" not "pick this mode"

---

## 5. README Rewrite

### New structure:

```
# Repo Memory

[logo]

## One-liner
The state persistence layer for AI-assisted repos. Any agent resumes
where the last one stopped.

## The Problem (shorter — 3 lines max)
Workflow skills produce artifacts everywhere. Plans in one folder,
tickets in another, specs in a third. When you switch agents or sessions,
nobody knows where things are or what state they're in.

## What Repo Memory Is
A thin persistence layer that tracks:
1. **Where things live** (ownership map with typed slots)
2. **What state they're in** (feature frontmatter)
3. **What's next** (auto-generated work queue)

## What It Is NOT (keep this — it's strong)
[existing table, slightly updated]

## How Skills Work Together (NEW — learned from marketingskills)

Position RM as the foundation layer with a composition diagram:

    ┌───────────────────────────────────────────┐
    │         Repo Memory (state layer)         │
    │  ownership map · feature docs · work queue│
    └─────────────────────┬─────────────────────┘
                          │ agents read on start
          ┌───────────────┼───────────────────┐
          ▼               ▼                   ▼
    ┌───────────┐  ┌────────────┐  ┌───────────────┐
    │ Planning  │  │ Building   │  │ Reviewing     │
    │           │  │            │  │               │
    │/wayfinder │  │/implement  │  │/code-review   │
    │/to-tickets│  │/tdd        │  │/triage        │
    │/to-spec   │  │/exec-plans │  │/improve       │
    └─────┬─────┘  └─────┬──────┘  └───────┬───────┘
          │               │                 │
          └───────────────┼─────────────────┘
                          ▼ agents write on close
    ┌───────────────────────────────────────────┐
    │         Repo Memory (state layer)         │
    │  update status · link artifacts · next step│
    └───────────────────────────────────────────┘

RM doesn't compete with these skills — it connects them.
Each writes to its own location; RM tracks where everything lives.

## Works With (NEW — prominent)
| Skill Pack | What RM adds |
|------------|-------------|
| Matt Pocock's skills | Persists state between /implement sessions, routes agents to plans/tickets |
| Obra / Superpowers | Links plans and specs, tracks which are accepted vs in-progress |
| Kiro specs | Maps spec directories, tracks implementation status per feature |
| Standalone (no skills) | Full feature state tracking — RM carries more weight |
| Your custom skills | Register artifact locations in typed slots, zero coupling |

## Quick Start
[keep — works well]

## How It Works (simplify)
1. Agent loads adapter → reads ownership map
2. Ownership map says where everything lives (plans, tickets, specs, etc.)
3. Agent reads the feature doc for its task (status + next step)
4. Agent works (using whatever skills it wants)
5. Agent updates feature doc before stopping
6. Next agent — any tool — picks up from there

## Modes (3 visible + 1 auto)
- Bootstrapper: first-time setup
- Maintainer: every session close
- Auditor: health check on session start
- (Generator runs automatically)

## Install
[keep npx skills add command]

## Related Skills (NEW — cross-references, learned from marketingskills)
| If you need... | Use | RM's role |
|---------------|-----|-----------|
| Planning | /writing-plans, /wayfinder | Links plans, tracks status |
| Implementation | /implement, /executing-plans | Records progress, next step |
| Code review | /code-review | Records outcome, links output |
| Issue tracking | /to-tickets, /triage | Maps tracker location |
| Handoff (ephemeral) | /handoff | Persists the durable parts |
| Research | /research, /improve | Registers artifact location |
| Specs | /to-spec, Kiro specs | Maps spec directory |

## Typed Slots (NEW section)
Brief explanation of the artifact categories and how to register
new skill outputs. Link to compatible-skills.md for full table.
```

---

## 6. Structural Changes for skills.sh Compatibility

Based on research, the repo needs:

### Already correct:
- ✅ `skills/repo-memory/SKILL.md` with proper frontmatter
- ✅ Kebab-case naming
- ✅ References in subdirectory

### Needs adding/updating:
- [ ] Verify `name` in SKILL.md frontmatter matches what skills.sh expects
- [ ] Consider adding `.claude-plugin/plugin.json` for Claude marketplace discovery
- [ ] Consider `skills.sh.json` manifest if publishing to registry
- [ ] Ensure description field is ≤1024 chars
- [ ] Add `argument-hint` to frontmatter if appropriate

### Folder structure decision:
Current: `skills/repo-memory/SKILL.md` (single skill in a folder)
This is fine — matches the standard. No restructuring needed.

---

## 7. Execution Order

1. **Update SKILL.md description** — new frontmatter with better pitch
2. **Create `references/compatible-skills.md`** — the compatibility surface
3. **Update ownership map template** — add typed slots section
4. **Simplify mode docs** — thin Maintainer, enrich Bootstrapper, make Generator auto
5. **Rewrite README.md** — new structure with "Works With" section prominent
6. **Add AGENTS.md link** to compatible-skills.md reference
7. **Update CHANGELOG.md** — document the repositioning
8. **Run validate-docs.py** — ensure nothing broke

---

## 8. What NOT to Change

- Don't rename the repo or skill
- Don't break the existing `npx skills add` install path
- Don't remove modes — just adjust weight
- Don't add orchestration logic (RM stays passive)
- Don't couple to specific skills (typed slots are category-based, not skill-based)
- Don't add new dependencies or scripts
- Don't change the standard (STANDARD.md) — this is packaging/positioning only
