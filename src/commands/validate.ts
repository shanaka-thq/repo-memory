import * as path from 'path';
import { loadConfig } from '../core/config';
import { findProjectRoot } from '../core/paths';
import { loadFeatures, FeatureEntry } from '../core/feature-index';

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
      errorCount: 1,
      warningCount: 0,
    };
  }

  const featuresDir = path.resolve(projectRoot, config.paths.features);
  const { features, duplicateIds } = loadFeatures(featuresDir);
  const missingFrontmatterMessage = 'Missing YAML frontmatter block';

  for (const entry of features) {
    const relPath = path.relative(projectRoot, entry.filePath);
    const hasOnlyMissingFrontmatterError =
      !entry.hasFrontmatter &&
      entry.errors.length === 1 &&
      entry.errors[0] === missingFrontmatterMessage;

    if (hasOnlyMissingFrontmatterError && config.validation.require_feature_frontmatter) {
      issues.push({
        file: relPath,
        type: 'error',
        message: 'Missing YAML frontmatter block (require_feature_frontmatter is enabled)',
      });
      continue;
    }

    if (entry.errors.length > 0 && !hasOnlyMissingFrontmatterError) {
      for (const err of entry.errors) {
        issues.push({ file: relPath, type: 'error', message: err });
      }
    }
  }

  for (const id of duplicateIds) {
    issues.push({
      file: config.paths.features,
      type: 'error',
      message: `Duplicate feature ID: "${id}" appears in more than one file`,
    });
  }

  const errorCount = issues.filter((i) => i.type === 'error').length;
  const warningCount = issues.filter((i) => i.type === 'warning').length;

  return {
    valid: errorCount === 0,
    issues,
    featureCount: features.length,
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
