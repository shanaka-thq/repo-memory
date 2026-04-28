# Contributing

Thanks for helping improve Repo Memory.

This repository is a documentation standard and skill library. Contributions
should make the standard clearer, easier to adopt, safer for agents to follow,
or easier to validate.

## Good Contributions

- clearer workflow guidance in `SKILL.md`
- stronger templates in `references/templates.md`
- practical examples in `examples/`
- platform adapter guides in `agents/`
- validation checks in `scripts/`
- issue reports showing where the standard is confusing or unsafe

## Before Opening a Pull Request

1. Read [`AGENTS.md`](./AGENTS.md).
2. If you changed `SKILL.md`, bump its `Version:` value.
3. Add a matching entry to [`CHANGELOG.md`](./CHANGELOG.md).
4. If you added a reference document, link it from [`README.md`](./README.md)
   and [`AGENTS.md`](./AGENTS.md).
5. If you added a template block, include a short usage note above it.
6. Run the local checks:

```bash
python3 scripts/validate-docs.py --skill-repo .
```

## Pull Request Scope

Keep pull requests focused. A platform adapter, a reference rule change, and a
large template rewrite are usually separate changes.

When changing the documentation standard, explain:

- what user or agent problem the change solves
- whether existing adopters need to change their docs
- whether the change is minor or structural
- what examples or validation cover the change

## Style

- Use concise, imperative guidance.
- Prefer agent-neutral language unless a file is platform-specific.
- Keep mutable project facts out of agent-specific guides.
- Use kebab-case for new file and folder names.
- Mark inferred guidance as inferred when it depends on current platform behavior.

## Security-Sensitive Changes

This repo can influence how agents modify user repositories. Treat instructions
about credentials, shell commands, destructive operations, generated files, or
automation as security-sensitive. Follow [`SECURITY.md`](./SECURITY.md) for
vulnerability reports.
