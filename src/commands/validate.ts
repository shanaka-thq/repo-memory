import * as path from 'path';
import { loadConfig } from '../core/config';
import { findProjectRoot } from '../core/paths';
import { loadFeatures } from '../core/feature-index';
import { loadDocs } from '../core/doc-index';
import { planSchema } from '../schemas/plan.schema';
import { reviewSchema } from '../schemas/review.schema';

export interface ValidateOptions {
  json?: boolean;
  projectRoot?: string;
}

export interface ValidationIssue {
  file: string;
  type: 'error' | 'warning';
  message: string;
}

export interface ValidationResult {
  valid: boolean;
  issues: ValidationIssue[];
  featureCount: number;
  planCount: number;
  reviewCount: number;
  errorCount: number;
  warningCount: number;
}

/**
 * Run validation and return a structured result without printing anything.
 * This is the testable core that runValidateCommand wraps.
 */
export function runValidation(projectRoot: string): ValidationResult {
  const issues: ValidationIssue[] = [];

  const config = loadConfig(projectRoot);
  if (!config) {
    return {
      valid: false,
      issues: [
        {
          file: 'repo-memory.config.yml',
          type: 'error',
          message: 'No repo-memory.config.yml found. Run: npx repo-memory init',
        },
      ],
      featureCount: 0,
      planCount: 0,
      reviewCount: 0,
      errorCount: 1,
      warningCount: 0,
    };
  }

  const MISSING_FM = 'Missing YAML frontmatter block';

  // ── Features ────────────────────────────────────────────────────────────
  const featuresDir = path.resolve(projectRoot, config.paths.features);
  const { features, duplicateIds: dupFeatureIds } = loadFeatures(featuresDir);

  for (const entry of features) {
    const relPath = path.relative(projectRoot, entry.filePath);
    const onlyMissingFm = !entry.hasFrontmatter && entry.errors.length === 1 && entry.errors[0] === MISSING_FM;

    if (onlyMissingFm) {
      if (config.validation.require_feature_frontmatter) {
        issues.push({ file: relPath, type: 'error', message: `${MISSING_FM} (require_feature_frontmatter is enabled)` });
      }
      continue;
    }
    for (const err of entry.errors) {
      issues.push({ file: relPath, type: 'error', message: err });
    }
  }

  for (const id of dupFeatureIds) {
    issues.push({ file: config.paths.features, type: 'error', message: `Duplicate feature ID: "${id}" appears in more than one file` });
  }

  // ── Plans ────────────────────────────────────────────────────────────────
  const plansDir = path.resolve(projectRoot, config.paths.plans);
  const { docs: plans, duplicateIds: dupPlanIds } = loadDocs(plansDir, planSchema);

  for (const entry of plans) {
    const relPath = path.relative(projectRoot, entry.filePath);
    const onlyMissingFm = !entry.hasFrontmatter && entry.errors.length === 1 && entry.errors[0] === MISSING_FM;

    if (onlyMissingFm) {
      if (config.validation.require_plan_frontmatter) {
        issues.push({ file: relPath, type: 'error', message: `${MISSING_FM} (require_plan_frontmatter is enabled)` });
      }
      continue;
    }
    for (const err of entry.errors) {
      issues.push({ file: relPath, type: config.validation.require_plan_frontmatter ? 'error' : 'warning', message: err });
    }
  }

  for (const id of dupPlanIds) {
    issues.push({ file: config.paths.plans, type: 'warning', message: `Duplicate plan ID: "${id}" appears in more than one file` });
  }

  // ── Reviews ──────────────────────────────────────────────────────────────
  const reviewsDir = path.resolve(projectRoot, config.paths.reviews);
  const { docs: reviews, duplicateIds: dupReviewIds } = loadDocs(reviewsDir, reviewSchema);

  for (const entry of reviews) {
    const relPath = path.relative(projectRoot, entry.filePath);
    const onlyMissingFm = !entry.hasFrontmatter && entry.errors.length === 1 && entry.errors[0] === MISSING_FM;

    if (onlyMissingFm) {
      if (config.validation.require_review_frontmatter) {
        issues.push({ file: relPath, type: 'error', message: `${MISSING_FM} (require_review_frontmatter is enabled)` });
      }
      continue;
    }
    for (const err of entry.errors) {
      issues.push({ file: relPath, type: config.validation.require_review_frontmatter ? 'error' : 'warning', message: err });
    }
  }

  for (const id of dupReviewIds) {
    issues.push({ file: config.paths.reviews, type: 'warning', message: `Duplicate review ID: "${id}" appears in more than one file` });
  }

  const errorCount = issues.filter((i) => i.type === 'error').length;
  const warningCount = issues.filter((i) => i.type === 'warning').length;

  return {
    valid: errorCount === 0,
    issues,
    featureCount: features.length,
    planCount: plans.length,
    reviewCount: reviews.length,
    errorCount,
    warningCount,
  };
}

/**
 * CLI entry point for the validate command.
 * Exits with code 1 when validation fails.
 */
export function runValidateCommand(options: ValidateOptions): void {
  const projectRoot = options.projectRoot ?? findProjectRoot();
  let result: ValidationResult;

  try {
    result = runValidation(projectRoot);
  } catch (err: any) {
    if (options.json) {
      console.error(JSON.stringify({ valid: false, error: err.message }));
    } else {
      console.error(`Validation error: ${err.message}`);
    }
    process.exit(1);
  }

  if (options.json) {
    console.log(JSON.stringify(result, null, 2));
    if (!result.valid) process.exit(1);
    return;
  }

  console.log('Repo Memory Validate');
  console.log('====================');
  console.log(`Features found: ${result.featureCount}`);

  if (result.issues.length === 0) {
    console.log('✓ All checks passed.');
  } else {
    for (const issue of result.issues) {
      const prefix = issue.type === 'error' ? '[ERROR]' : '[WARN] ';
      console.log(`${prefix} ${issue.file}: ${issue.message}`);
    }
  }

  console.log('');
  if (result.valid) {
    console.log(`Result: PASS (${result.featureCount} features, 0 errors)`);
  } else {
    console.log(
      `Result: FAIL (${result.errorCount} error${result.errorCount !== 1 ? 's' : ''}, ${result.warningCount} warning${result.warningCount !== 1 ? 's' : ''})`
    );
    process.exit(1);
  }
}
