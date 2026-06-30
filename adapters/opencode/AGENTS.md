# OpenCode Instructions

This repo uses Repo Memory.
Start with:

- `skills/repo-memory/SKILL.md`
- the configured ownership map, usually `docs/README.md`
  Choose the smallest relevant mode:
- Maintainer for normal feature/doc updates.
- Bootstrapper for first-time setup (ownership map + feature stubs).
- Auditor for drift and health checks.
- Generator for generated indexes.
  Rules:
- Load only task-relevant docs.
- Do not edit generated files directly.
- Do not promote intake, plans, or reviews into canonical docs without review.
- Do not duplicate canonical facts.
- Use the Repo Memory CLI for doctor, validate, generate, migrate, and adapter installation when available.
