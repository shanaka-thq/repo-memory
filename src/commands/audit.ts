import * as fs from 'fs';
import * as path from 'path';
import { loadConfig } from '../core/config';
import { findProjectRoot } from '../core/paths';
import { loadFeatures } from '../core/feature-index';
import { loadDocs } from '../core/doc-index';
import { planSchema } from '../schemas/plan.schema';
import { reviewSchema } from '../schemas/review.schema';

export interface AuditOptions {
  projectRoot?: string;
  write?: boolean;
  json?: boolean;
}

export interface AuditIssue {
  severity: 'critical' | 'warning' | 'info';
  category: string;
  message: string;
  suggestion?: string;
}

export interface AuditResult {
  passed: boolean;
  issues: AuditIssue[];
  summary: {
    critical: number;
    warnings: number;
    info: number;
    features: number;
    plans: number;
    reviews: number;
  };
}

/**
 * Check if a generated file has been manually edited (missing its header).
 */
function isManuallyEdited(filePath: string, expectedHeader: string): boolean {
  if (!fs.existsSync(filePath)) return false;
  const content = fs.readFileSync(filePath, 'utf8');
  return !content.startsWith(expectedHeader);
}

/**
 * Run the full audit and return a structured result.
 */
export function runAudit(projectRoot: string): AuditResult {
  const issues: AuditIssue[] = [];

  const config = loadConfig(projectRoot);
  if (!config) {
    return {
      passed: false,
      issues: [
        {
          severity: 'critical',
          category: 'config',
          message: 'No repo-memory.config.yml found.',
          suggestion: 'Run: npx repo-memory init',
        },
      ],
      summary: { critical: 1, warnings: 0, info: 0, features: 0, plans: 0, reviews: 0 },
    };
  }

  // ── Feature validation ──────────────────────────────────────────────────
  const featuresDir = path.resolve(projectRoot, config.paths.features);
  const { features, duplicateIds: dupFeatureIds } = loadFeatures(featuresDir);

  for (const entry of features) {
    const rel = path.relative(projectRoot, entry.filePath);
    if (!entry.hasFrontmatter) {
      if (config.validation.require_feature_frontmatter) {
        issues.push({
          severity: 'critical',
          category: 'feature-frontmatter',
          message: `${rel}: missing YAML frontmatter`,
          suggestion: 'Add frontmatter with id, title, status, doc_type, ready, next_safe_step.',
        });
      } else {
        issues.push({
          severity: 'warning',
          category: 'feature-frontmatter',
          message: `${rel}: missing YAML frontmatter`,
          suggestion: 'Consider adding frontmatter to enable generate and validate.',
        });
      }
    } else if (entry.errors.length > 0) {
      for (const err of entry.errors) {
        issues.push({
          severity: 'critical',
          category: 'feature-schema',
          message: `${rel}: ${err}`,
          suggestion: 'Fix the frontmatter field and run: npx repo-memory validate',
        });
      }
    }
  }

  for (const id of dupFeatureIds) {
    issues.push({
      severity: 'critical',
      category: 'feature-duplicate',
      message: `Duplicate feature ID: "${id}"`,
      suggestion: 'Ensure each docs/features/*.md has a unique id field.',
    });
  }

  // ── Plan validation ──────────────────────────────────────────────────────
  const plansDir = path.resolve(projectRoot, config.paths.plans);
  const { docs: plans, duplicateIds: dupPlanIds } = loadDocs(plansDir, planSchema);

  for (const entry of plans) {
    const rel = path.relative(projectRoot, entry.filePath);
    if (!entry.hasFrontmatter) {
      const required = config.validation.require_plan_frontmatter;
      issues.push({
        severity: required ? 'critical' : 'warning',
        category: 'plan-frontmatter',
        message: `${rel}: missing YAML frontmatter`,
        suggestion: 'Add frontmatter with id, title, status, doc_type.',
      });
      continue;
    } else if (entry.errors.length > 0) {
      for (const err of entry.errors) {
        issues.push({
          severity: 'warning',
          category: 'plan-schema',
          message: `${rel}: ${err}`,
        });
      }
    }
  }

  for (const id of dupPlanIds) {
    issues.push({
      severity: 'warning',
      category: 'plan-duplicate',
      message: `Duplicate plan ID: "${id}"`,
    });
  }

  // ── Review validation ───────────────────────────────────────────────────
  const reviewsDir = path.resolve(projectRoot, config.paths.reviews);
  const { docs: reviews, duplicateIds: dupReviewIds } = loadDocs(reviewsDir, reviewSchema);

  for (const entry of reviews) {
    const rel = path.relative(projectRoot, entry.filePath);
    if (!entry.hasFrontmatter) {
      const required = config.validation.require_review_frontmatter;
      issues.push({
        severity: required ? 'critical' : 'warning',
        category: 'review-frontmatter',
        message: `${rel}: missing YAML frontmatter`,
        suggestion: 'Add frontmatter with id, title, status, doc_type.',
      });
      continue;
    } else if (entry.errors.length > 0) {
      for (const err of entry.errors) {
        issues.push({
          severity: 'warning',
          category: 'review-schema',
          message: `${rel}: ${err}`,
        });
      }
    }
  }

  for (const id of dupReviewIds) {
    issues.push({
      severity: 'warning',
      category: 'review-duplicate',
      message: `Duplicate review ID: "${id}"`,
    });
  }

  // ── Generated file integrity ────────────────────────────────────────────
  if (config.validation.fail_on_generated_file_manual_edit) {
    const generatedHeader = config.generated.header;
    const generatedFiles = [
      config.generated.feature_registry,
      config.generated.next_work_queue,
      config.generated.doc_health,
    ];
    for (const relPath of generatedFiles) {
      const absPath = path.resolve(projectRoot, relPath);
      if (isManuallyEdited(absPath, generatedHeader)) {
        issues.push({
          severity: 'critical',
          category: 'generated-file',
          message: `${relPath}: generated file has been manually edited (missing generated header)`,
          suggestion: 'Run: npx repo-memory generate to rebuild this file.',
        });
      }
    }
  }

  // ── Ownership map check ─────────────────────────────────────────────────
  const ownershipMapPath = path.resolve(projectRoot, config.paths.ownership_map);
  if (!fs.existsSync(ownershipMapPath)) {
    issues.push({
      severity: 'warning',
      category: 'ownership-map',
      message: `Ownership map not found: ${config.paths.ownership_map}`,
      suggestion: 'Create docs/README.md with a Canonical Ownership Map table.',
    });
  }

  // ── Interop warnings ────────────────────────────────────────────────────
  if (config.adapters.installed.length === 0) {
    issues.push({
      severity: 'info',
      category: 'adapters',
      message: 'No adapters recorded as installed in config.',
      suggestion:
        'Run: npx repo-memory install-adapter <agent> to install the adapter for your tool.',
    });
  }

  const critical = issues.filter((i) => i.severity === 'critical').length;
  const warnings = issues.filter((i) => i.severity === 'warning').length;
  const info = issues.filter((i) => i.severity === 'info').length;

  return {
    passed: critical === 0,
    issues,
    summary: {
      critical,
      warnings,
      info,
      features: features.length,
      plans: plans.length,
      reviews: reviews.length,
    },
  };
}

/**
 * Build doc-health content from an audit result.
 */
function buildDocHealthFromAudit(result: AuditResult, generatedAt: string, header: string): string {
  const { summary } = result;

  const criticalLines = result.issues
    .filter((i) => i.severity === 'critical')
    .map((i) => `- [${i.category}] ${i.message}`)
    .join('\n') || '_None._';

  const warningLines = result.issues
    .filter((i) => i.severity === 'warning')
    .map((i) => `- [${i.category}] ${i.message}`)
    .join('\n') || '_None._';

  return [
    header,
    '',
    '# Documentation Health',
    '',
    `> Generated: ${generatedAt} (from \`npx repo-memory audit --write\`)`,
    '',
    '## Summary',
    '',
    `- Features: ${summary.features}`,
    `- Plans: ${summary.plans}`,
    `- Reviews: ${summary.reviews}`,
    `- Critical issues: ${summary.critical}`,
    `- Warnings: ${summary.warnings}`,
    `- Info: ${summary.info}`,
    '',
    '## Critical Issues',
    '',
    criticalLines,
    '',
    '## Warnings',
    '',
    warningLines,
    '',
  ].join('\n');
}

/**
 * CLI entry point for the audit command.
 */
export function runAuditCommand(options: AuditOptions): void {
  const projectRoot = options.projectRoot ?? findProjectRoot();
  let result: AuditResult;

  try {
    result = runAudit(projectRoot);
  } catch (err: any) {
    if (options.json) {
      console.error(JSON.stringify({ passed: false, error: err.message }));
    } else {
      console.error(`Audit error: ${err.message}`);
    }
    process.exit(1);
  }

  if (options.json) {
    console.log(JSON.stringify(result, null, 2));
    if (!result.passed) process.exit(1);
    return;
  }

  console.log('Repo Memory Audit');
  console.log('=================');
  console.log(
    `Features: ${result.summary.features} | ` +
    `Plans: ${result.summary.plans} | ` +
    `Reviews: ${result.summary.reviews}`
  );
  console.log('');

  if (result.issues.length === 0) {
    console.log('✓ No issues found.');
  } else {
    const bySeverity: Record<string, AuditIssue[]> = { critical: [], warning: [], info: [] };
    for (const issue of result.issues) bySeverity[issue.severity].push(issue);

    if (bySeverity.critical.length > 0) {
      console.log('Critical:');
      for (const issue of bySeverity.critical) {
        console.log(`  [${issue.category}] ${issue.message}`);
        if (issue.suggestion) console.log(`    → ${issue.suggestion}`);
      }
      console.log('');
    }
    if (bySeverity.warning.length > 0) {
      console.log('Warnings:');
      for (const issue of bySeverity.warning) {
        console.log(`  [${issue.category}] ${issue.message}`);
        if (issue.suggestion) console.log(`    → ${issue.suggestion}`);
      }
      console.log('');
    }
    if (bySeverity.info.length > 0) {
      console.log('Info:');
      for (const issue of bySeverity.info) {
        console.log(`  [${issue.category}] ${issue.message}`);
        if (issue.suggestion) console.log(`    → ${issue.suggestion}`);
      }
      console.log('');
    }
  }

  const statusLabel = result.passed ? 'PASS' : 'FAIL';
  console.log(
    `Result: ${statusLabel} ` +
    `(${result.summary.critical} critical, ${result.summary.warnings} warnings, ${result.summary.info} info)`
  );

  if (options.write) {
    const config = loadConfig(projectRoot);
    if (config) {
      const generatedAt = new Date().toISOString().split('T')[0];
      const content = buildDocHealthFromAudit(result, generatedAt, config.generated.header);
      const docHealthPath = path.resolve(projectRoot, config.generated.doc_health);
      fs.mkdirSync(path.dirname(docHealthPath), { recursive: true });
      fs.writeFileSync(docHealthPath, content, 'utf8');
      console.log(`\nWritten: ${config.generated.doc_health}`);
    }
  }

  if (!result.passed) process.exit(1);
}
