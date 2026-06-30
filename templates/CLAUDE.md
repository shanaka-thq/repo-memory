# Claude Code Instructions

This repo uses Repo Memory.
Read `skills/repo-memory/SKILL.md`, then choose the smallest relevant mode.
Use lazy context loading:

- feature work → relevant feature doc
- architecture work → canonical architecture owner
- decisions → configured ADR path
- first-time setup → Bootstrapper mode

Do not manually edit generated files.
Do not duplicate canonical facts.
Use `python3 skills/repo-memory/scripts/validate-docs.py` for validation and `python3 skills/repo-memory/scripts/generate-indexes.py` for generating indexes.
