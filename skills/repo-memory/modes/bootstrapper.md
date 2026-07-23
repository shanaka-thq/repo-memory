# Bootstrapper Mode

Use this mode when adopting a repository that has no Repo Memory setup yet. The goal is to create the **state persistence layer** — not to rewrite all project docs.

## What You Create

1. `docs/README.md` with a **Canonical Ownership Map** and **Artifact Locations** table
2. `docs/features/<slug>.md` for any active or recent work that needs handoff context
3. Feature frontmatter so the generation script can build the work queue

## What You Do NOT Create

- Architecture docs (the repo probably already has these, or another skill handles it)
- Requirements or specs (use your spec/planning skill)
- Decision logs (link to existing ADRs if they exist)
- Full baseline docs you weren't asked for
- Copies of anything that lives in `.kiro/specs/`, `docs/superpowers/`, or other skill outputs

## Instructions

### 1. Inventory existing docs and skills

Look for:
- **Existing docs:** README, ADRs, architecture notes, specs, runbooks, OpenAPI, CONTRIBUTING, SECURITY
- **Installed skills:** Check `.agents/skills/`, `.kiro/skills/`, `.claude/skills/`, `node_modules/.skills/` for workflow skills that produce artifacts
- **Skill outputs already present:** `.kiro/specs/`, `docs/superpowers/plans/`, `plans/`, `advisor-plans/`, `.scratch/`, `docs/adr/`, `CONTEXT.md`, `research/` branches

### 2. Create the ownership map

Write `docs/README.md` with:
- **Canonical Ownership Map** — mapping each capability to its existing owner
- **Artifact Locations** — typed slots showing where each category of artifact lives

For the Artifact Locations table, ask (or detect) for each category:
- **Plans:** Where do implementation plans land? (`plans/`, `docs/superpowers/plans/`, etc.)
- **Specs:** Where do requirements/specs live? (`.kiro/specs/`, `docs/specs/`, etc.)
- **Tickets:** Where is work tracked? (GitHub Issues, `.scratch/`, Linear, etc.)
- **ADRs:** Where do decisions get recorded? (`docs/adr/`, `CONTEXT.md`, etc.)
- **Reviews:** Where do code reviews live? (PR comments, `docs/reviews/`, etc.)
- **Research:** Where do investigation outputs go? (`research/` branches, etc.)

Fill only what the repo actually uses. Leave unused slots empty.

### 3. Create feature stubs

For active or recent work, create `docs/features/<slug>.md` with frontmatter (id, title, status, ready, next_safe_step, priority). Link to relevant specs/plans/reviews if they exist.

Active or recent = any of: open branches with commits in the last 2 weeks, open PRs, in-progress tickets, or work mentioned in recent commits that isn't shipped yet.

### 4. Link, don't duplicate

If architecture is in `ARCHITECTURE.md`, map it. If requirements are in `.kiro/specs/`, map them. If plans are in `docs/superpowers/plans/`, link them from the feature doc.

### 5. Record unknowns honestly

Don't invent user personas, decisions, or architecture. If it's unknown, say so.

### 6. Run generation

`python3 <skill-dir>/scripts/generate-indexes.py .` to build the initial indexes.
