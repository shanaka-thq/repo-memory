# Bootstrapper Mode

Use this mode when adopting a repository that has no Repo Memory setup yet. The goal is to create the **continuity layer** — not to rewrite all project docs.

## What You Create

1. `docs/README.md` with a **Canonical Ownership Map** — points to where each kind of truth already lives
2. `docs/features/<slug>.md` for any active or recent work that needs handoff context
3. Feature frontmatter so the generation script can build the work queue

## What You Do NOT Create

- Architecture docs (the repo probably already has these, or another skill handles it)
- Requirements or specs (use your spec/planning skill)
- Decision logs (link to existing ADRs if they exist)
- Full baseline docs you weren't asked for
- Copies of anything that lives in `.kiro/specs/`, `docs/superpowers/`, or other skill outputs

## Instructions

1. **Inventory existing docs and companion artifacts.** Look for README, ADRs, architecture notes, specs, runbooks, OpenAPI, CONTRIBUTING, SECURITY. Also check for `.kiro/specs/`, `docs/superpowers/`, `docs/plans/`, `docs/reviews/`, or other skill-managed directories.
2. **Create the ownership map.** Write `docs/README.md` with a table mapping each capability to its existing owner — including companion skill outputs. Only add "TODO" for capabilities that genuinely have no owner and matter for continuity.
3. **Create feature stubs.** For active or recent work, create `docs/features/<slug>.md` with frontmatter (id, title, status, ready, next_safe_step, priority). Link to relevant specs/plans/reviews if they exist.
4. **Link, don't duplicate.** If architecture is in `ARCHITECTURE.md`, map it. If requirements are in `.kiro/specs/`, map them. If plans are in `docs/superpowers/plans/`, link them from the feature doc.
5. **Record unknowns honestly.** Don't invent user personas, decisions, or architecture. If it's unknown, say so.
6. **Run generation.** `python3 <skill-dir>/scripts/generate-indexes.py .` to build the initial indexes.
