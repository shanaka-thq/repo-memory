# Compatible Skills

Repo Memory is a **state persistence layer** that sits beneath workflow skills.
It doesn't plan, review, spec, or implement — it records where those outputs
live and keeps feature state resumable across agents and sessions.

## How Compatibility Works

RM's ownership map has **typed slots** for common artifact categories. Any skill
that produces durable artifacts can register its output location in the relevant
slot. RM doesn't need to know which skill wrote the artifact — only what kind it
is and where it lives.

### The Protocol

1. **Session start** — agent reads RM's ownership map to orient (where things
   live, what's in flight)
2. **Session middle** — agent uses whatever workflow skills it wants. RM doesn't
   interfere.
3. **Session end** — agent updates feature frontmatter (status, next_safe_step)
   and links any new artifacts produced this session.

RM doesn't require skill authors to cooperate. It requires agents to update
state before stopping — enforced by the adapter file loaded on session start.

## Typed Slots (Artifact Categories)

The ownership map pre-defines these categories. Each maps to a path (or
external location) in the target repo:

| Category | What lives here | Example producers |
|----------|-----------------|-------------------|
| Plans | Implementation plans, architecture plans | /writing-plans, /improve, Kiro specs |
| Specs | Requirements, specifications, PRDs | /to-spec, /brainstorming, manual specs |
| Tickets | Work items, issues, backlog | /to-tickets, /triage, /wayfinder |
| ADRs | Architecture decision records | /grill-with-docs, /domain-modeling |
| Reviews | Code review outputs | /code-review, PR comments |
| Handoff | Session state, next steps, blockers | RM feature docs (native) |
| Research | Investigation outputs, findings | /research, /improve audit reports |
| Additional | Anything not covered above | Custom skills, one-off artifacts |

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
| `/handoff` | OS temp dir (ephemeral!) | — |

Note: `/handoff` writes to the OS temp directory and is lost on reboot. RM's
feature docs persist the durable parts (status, next step, blockers) in-repo
where any agent can find them.

### Obra / Superpowers

| Skill | Writes to | RM slot |
|-------|-----------|---------|
| Brainstorming | Specs directory | `specs` |
| Writing plans | `docs/superpowers/plans/` | `plans` |
| Executing plans | Git worktrees (transient) | — |
| Subagent development | Git worktrees (transient) | — |

### Kiro

| Artifact | Location | RM slot |
|----------|----------|---------|
| Spec files | `.kiro/specs/` | `specs` |
| Steering rules | `.kiro/steering/` | — (config, not artifacts) |

### Anthropic Skills (`anthropics/skills`)

| Skill | Writes to | RM slot |
|-------|-----------|---------|
| Frontend design | Code files | — (code, not docs) |
| Skill creator | Skill files | — (meta) |

### Shadcn / Improve (`shadcn/improve`)

| Skill | Writes to | RM slot |
|-------|-----------|---------|
| `/improve` | `plans/` or `advisor-plans/` | `plans` |
| `/improve execute` | Git worktrees (transient) | — |

## Adding a New Skill's Outputs

When you install a new workflow skill that writes durable artifacts:

1. Identify which category its output belongs to (see typed slots above)
2. Update the ownership map's Artifact Locations table with the path
3. Done — RM checks that location when orienting the next agent

Example: You install a skill that writes architecture reports to
`.scratch/architecture/`:

```markdown
<!-- In docs/README.md ownership map, Artifact Locations section -->
| Additional | `.scratch/architecture/` | /architecture-review |
```

No RM code changes needed. The typed slots are the extension point.

## Future-Proofing

This compatibility model is designed to survive new skill packs without changes:

- **New skill, existing category**: Add a row to the ownership map. Done.
- **New skill, new category**: Add to the "additional" slot. If the category
  becomes common across multiple repos, propose it as a first-class slot.
- **Skill changes its output path**: Update the ownership map. RM reads paths,
  not skill internals.
- **MCP memory servers mature**: They could read from RM's feature docs. The
  format (Markdown + YAML frontmatter) is already machine-readable.

## What RM Does NOT Do With These Skills

- ❌ Invoke or orchestrate other skills (RM is passive)
- ❌ Require skill authors to add RM support (zero coupling)
- ❌ Duplicate artifacts other skills produce (link, don't copy)
- ❌ Override skill-specific workflows (RM owns start + end, not the middle)
