/**
 * Embedded adapter content for all supported agent tools.
 *
 * Each entry maps an agent name to:
 *   - `targetFile`: where the adapter should be installed in the user's repo
 *   - `content`: the full text of the adapter file
 *
 * This content is kept in sync with the source files under adapters/ in this
 * repository. When an adapter source file changes, update this module too.
 */

export interface AdapterDefinition {
  /** Relative path where the file should be installed in the target repo */
  targetFile: string;
  /** Full content of the adapter file */
  content: string;
}

export const SUPPORTED_ADAPTERS = [
  'generic',
  'claude-code',
  'github-copilot',
  'codex',
  'opencode',
  'cursor',
  'windsurf',
  'kiro',
] as const;

export type AdapterName = (typeof SUPPORTED_ADAPTERS)[number];

export function isSupportedAdapter(name: string): name is AdapterName {
  return (SUPPORTED_ADAPTERS as readonly string[]).includes(name);
}

export const ADAPTER_DEFINITIONS: Record<AdapterName, AdapterDefinition> = {
  'generic': {
    targetFile: 'AGENTS.md',
    content: `# Agent Instructions

This repo uses Repo Memory.
Start with:

- \`skills/repo-memory/SKILL.md\`
- the configured ownership map, usually \`docs/README.md\`

Choose the smallest relevant mode:

- Maintainer for normal feature/doc updates.
- Bootstrapper for existing-repo extraction into intake.
- Planner for implementation plans.
- Reviewer for codebase or architecture reviews.
- Auditor for drift and health checks.
- Generator for generated indexes.

Rules:

- Load only task-relevant docs.
- Do not edit generated files directly.
- Do not promote intake, plans, or reviews into canonical docs without review.
- Do not duplicate canonical facts.
- Use the Repo Memory CLI for doctor, validate, generate, migrate, and adapter installation when available.
`,
  },

  'claude-code': {
    targetFile: 'CLAUDE.md',
    content: `# Claude Code Instructions

This repo uses Repo Memory.
Read \`skills/repo-memory/SKILL.md\`, then choose the smallest relevant mode.
Use lazy context loading:

- feature work → relevant feature doc
- architecture work → canonical architecture owner
- planning → configured plans path
- reviews → configured reviews path
- decisions → configured ADR path
- legacy extraction → Bootstrapper mode into intake

Do not manually edit generated files.
Do not promote intake, plans, or reviews into canonical docs without review.
Use Repo Memory CLI commands when available.
`,
  },

  'github-copilot': {
    targetFile: '.github/copilot-instructions.md',
    content: `# GitHub Copilot Instructions

This repo uses Repo Memory for durable project context.
Start with:

- \`skills/repo-memory/SKILL.md\`
- the configured ownership map, usually \`docs/README.md\`

Use task-relevant mode files only.
Never edit generated files directly.
For feature work:

- Update the matching file in \`docs/features/\`.
- Let \`repo-memory generate\` update registries and queues.

Use validation/generation commands when available.
`,
  },

  'codex': {
    targetFile: '.codex/instructions.md',
    content: `# Codex Instructions

This repository uses Repo Memory.
Read \`skills/repo-memory/SKILL.md\` first.
Use it as a router, not as a full context dump.
For normal work:

- Use Maintainer mode.
- Read the ownership map.
- Load only relevant feature or owner docs.

Do not edit generated files.
Do not duplicate canonical facts.
Write inferred facts only with evidence.
Use Repo Memory CLI commands when available.
`,
  },

  'opencode': {
    targetFile: 'AGENTS.md',
    content: `# OpenCode Instructions

This repo uses Repo Memory.
Start with:

- \`skills/repo-memory/SKILL.md\`
- the configured ownership map, usually \`docs/README.md\`

Choose the smallest relevant mode:

- Maintainer for normal feature/doc updates.
- Bootstrapper for existing-repo extraction into intake.
- Planner for implementation plans.
- Reviewer for codebase or architecture reviews.
- Auditor for drift and health checks.
- Generator for generated indexes.

Rules:

- Load only task-relevant docs.
- Do not edit generated files directly.
- Do not promote intake, plans, or reviews into canonical docs without review.
- Do not duplicate canonical facts.
- Use the Repo Memory CLI for doctor, validate, generate, migrate, and adapter installation when available.
`,
  },

  'cursor': {
    targetFile: '.cursor/rules/repo-memory.mdc',
    content: `---
description: Routing rules for repositories using Repo Memory v3
globs: "*"
---

# Cursor Repo Memory Rules

This repository uses Repo Memory.
Start with:

- \`skills/repo-memory/SKILL.md\`
- the ownership map in \`docs/README.md\`

Use the modes defined under \`skills/repo-memory/modes/\` for planning, reviewing, and maintaining docs.
Do not modify generated files under \`docs/generated/\` directly.
Use Repo Memory CLI commands when available.
`,
  },

  'windsurf': {
    targetFile: '.windsurf/rules/repo-memory.md',
    content: `# Windsurf Repo Memory Rules

This repository uses Repo Memory.
Start with:

- \`skills/repo-memory/SKILL.md\`
- the ownership map in \`docs/README.md\`

Use the modes defined under \`skills/repo-memory/modes/\` for planning, reviewing, and maintaining docs.
Do not modify generated files under \`docs/generated/\` directly.
Use Repo Memory CLI commands when available.
`,
  },

  'kiro': {
    targetFile: '.kiro/steering/repo-memory.md',
    content: `# Kiro Repo Memory Rules

This repository uses Repo Memory.
Start with:

- \`skills/repo-memory/SKILL.md\`
- the ownership map in \`docs/README.md\`

Use the modes defined under \`skills/repo-memory/modes/\` for planning, reviewing, and maintaining docs.
Do not modify generated files under \`docs/generated/\` directly.
Use Repo Memory CLI commands when available.
`,
  },
};

export const MANAGED_BLOCK_START = '<!-- repo-memory start -->';
export const MANAGED_BLOCK_END = '<!-- repo-memory end -->';

/**
 * Wrap content in managed block markers so it can be updated without
 * replacing the entire file.
 */
export function wrapInManagedBlock(content: string): string {
  return `${MANAGED_BLOCK_START}\n${content.trimEnd()}\n${MANAGED_BLOCK_END}\n`;
}

/**
 * Insert or replace a managed block in existing file content.
 * If a managed block already exists, its contents are replaced.
 * If no managed block exists, the block is appended.
 */
export function upsertManagedBlock(existing: string, newBlockContent: string): string {
  const wrapped = wrapInManagedBlock(newBlockContent);
  const startIdx = existing.indexOf(MANAGED_BLOCK_START);
  const endIdx = existing.indexOf(MANAGED_BLOCK_END);

  if (startIdx !== -1 && endIdx !== -1 && endIdx > startIdx) {
    // Replace the existing block
    return (
      existing.slice(0, startIdx) +
      wrapped +
      existing.slice(endIdx + MANAGED_BLOCK_END.length).replace(/^\n/, '')
    );
  }

  // Append the block with a separating newline
  const separator = existing.endsWith('\n') ? '\n' : '\n\n';
  return existing + separator + wrapped;
}
