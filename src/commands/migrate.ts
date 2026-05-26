import * as fs from 'fs';
import * as path from 'path';
import { findProjectRoot } from '../core/paths';
import { discoverRepoState } from '../core/discovery';

export interface MigrateOptions {
  projectRoot?: string;
  dryRun?: boolean;
  backup?: boolean;
  json?: boolean;
}

export interface MigrationAction {
  type: 'preserve' | 'deprecate' | 'create' | 'skip';
  path: string;
  description: string;
}

export interface MigrateResult {
  fromVersion: string;
  toVersion: string;
  actions: MigrationAction[];
  warnings: string[];
  requiresWrite: boolean;
}

/**
 * Build a migration plan from v2 to v3 for the given project root.
 * Does not write any files — callers decide based on dryRun.
 */
export function buildMigrationPlan(projectRoot: string): MigrateResult {
  const state = discoverRepoState(projectRoot);
  const actions: MigrationAction[] = [];
  const warnings: string[] = [];

  if (state.repoMemoryVersion !== 'v2-style') {
    return {
      fromVersion: state.repoMemoryVersion,
      toVersion: 'v3-style',
      actions: [],
      warnings: [`Repo Memory version is "${state.repoMemoryVersion}", not "v2-style". Migration may not apply.`],
      requiresWrite: false,
    };
  }

  // v2 central files: docs/feature-registry.md, docs/doc-health.md (manually maintained)
  for (const centralFile of state.v2CentralFiles) {
    const rel = path.relative(projectRoot, centralFile);

    if (rel.endsWith('feature-registry.md')) {
      actions.push({
        type: 'deprecate',
        path: rel,
        description:
          'Manual feature-registry.md will be superseded by the generated version. ' +
          'Preserve existing content as docs/intake/feature-registry-v2.md for review, ' +
          'then migrate feature entries into individual docs/features/<slug>.md files with YAML frontmatter.',
      });
    } else if (rel.endsWith('doc-health.md')) {
      actions.push({
        type: 'preserve',
        path: rel,
        description:
          'doc-health.md will be superseded by the generated version. ' +
          'Preserve for reference; the generated version will overwrite it once generate runs.',
      });
    } else {
      actions.push({
        type: 'preserve',
        path: rel,
        description: 'v2 central file — preserve and review before migrating.',
      });
    }
  }

  // Agent files: preserve (don't overwrite)
  for (const agentFile of state.existingAgentFiles) {
    actions.push({
      type: 'preserve',
      path: agentFile,
      description:
        'Existing agent file preserved. Use `npx repo-memory install-adapter --append` ' +
        'to add a managed Repo Memory block without replacing the file.',
    });
  }

  // Config: needs to be created
  if (!state.configExists) {
    actions.push({
      type: 'create',
      path: 'repo-memory.config.yml',
      description:
        'v3 config not found. Copy templates/repo-memory.config.yml into this repo and adjust paths.',
    });
  }

  // Plans/reviews directories
  for (const plansDir of state.existingPlansDirs) {
    if (plansDir !== 'docs/plans') {
      actions.push({
        type: 'skip',
        path: plansDir,
        description: `Non-standard plans directory detected. Map it with: npx repo-memory map plans ${plansDir}`,
      });
    }
  }

  for (const reviewsDir of state.existingReviewsDirs) {
    if (reviewsDir !== 'docs/reviews') {
      actions.push({
        type: 'skip',
        path: reviewsDir,
        description: `Non-standard reviews directory detected. Map it with: npx repo-memory map reviews ${reviewsDir}`,
      });
    }
  }

  if (state.v2CentralFiles.length === 0 && state.existingAgentFiles.length === 0) {
    warnings.push('No v2 artifacts detected. Nothing to migrate.');
  }

  return {
    fromVersion: 'v2-style',
    toVersion: 'v3-style',
    actions,
    warnings,
    requiresWrite: actions.some((a) => a.type === 'create'),
  };
}

/**
 * CLI entry point for migrate.
 */
export function runMigrateCommand(type: string, options: MigrateOptions): void {
  if (type !== 'v2-to-v3') {
    console.error(`[ERROR] Unknown migration type "${type}". Supported: v2-to-v3`);
    process.exit(1);
  }

  const projectRoot = options.projectRoot ?? findProjectRoot();
  const plan = buildMigrationPlan(projectRoot);

  if (options.json) {
    console.log(JSON.stringify(plan, null, 2));
    return;
  }

  console.log('Repo Memory Migrate: v2-to-v3');
  console.log('===============================');

  if (plan.warnings.length > 0) {
    for (const w of plan.warnings) {
      console.log(`[WARN] ${w}`);
    }
    if (plan.actions.length === 0) return;
    console.log('');
  }

  if (plan.actions.length === 0) {
    console.log('Nothing to migrate.');
    return;
  }

  const dryRun = options.dryRun !== false;  // default to dry-run for safety

  console.log(
    dryRun
      ? 'Migration plan (dry run — no files written):'
      : 'Migration actions (write mode is not yet implemented; showing planned actions):'
  );
  console.log('');

  for (const action of plan.actions) {
    const icon = { preserve: '→', deprecate: '⚠', create: '+', skip: '·' }[action.type];
    console.log(`${icon} [${action.type.toUpperCase()}] ${action.path}`);
    console.log(`  ${action.description}`);
    console.log('');
  }

  if (!dryRun) {
    console.log(
      'Note: Full write-mode migration is not yet implemented.\n' +
      'Follow the actions above manually, or use --dry-run for a plan.'
    );
  }
}
