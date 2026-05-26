import * as fs from 'fs';
import * as path from 'path';
import { loadConfig } from '../core/config';
import { findProjectRoot } from '../core/paths';
import { loadFeatures, FeatureEntry } from '../core/feature-index';
import { FeatureFrontmatter, READY_VALUES } from '../schemas/feature.schema';

export interface GenerateOptions {
  json?: boolean;
  projectRoot?: string;
  dryRun?: boolean;
}

export interface GeneratedFile {
  path: string;
  content: string;
}

export interface GenerateResult {
  generated: GeneratedFile[];
  skipped: string[];
  errors: string[];
}

// ─── helpers ────────────────────────────────────────────────────────────────

function pad(s: string, width: number): string {
  return s.length >= width ? s : s + ' '.repeat(width - s.length);
}

/** Format an ISO date string to YYYY-MM-DD, or return "—" if absent. */
function fmtDate(d: string | undefined): string {
  return d ?? '—';
}

/** Format a priority value for display. */
function fmtPriority(p: number | undefined): string {
  return p !== undefined ? String(p) : '—';
}

// ─── feature-registry.md ────────────────────────────────────────────────────

function buildFeatureRegistry(
  features: FeatureEntry[],
  header: string,
  generatedAt: string
): string {
  const validFeatures = features.filter((f) => f.frontmatter !== null);

  const rows = validFeatures
    .slice()
    .sort((a, b) => {
      const pa = a.frontmatter!.priority ?? Infinity;
      const pb = b.frontmatter!.priority ?? Infinity;
      if (pa !== pb) return pa - pb;
      return a.slug.localeCompare(b.slug);
    })
    .map((f) => {
      const fm = f.frontmatter!;
      return {
        id: fm.id,
        title: fm.title,
        status: fm.status,
        priority: fmtPriority(fm.priority),
        ready: fm.ready,
        owner: fm.owner ?? '—',
        lastUpdated: fmtDate(fm.last_updated),
      };
    });

  // Column widths
  const cols = {
    id: Math.max(2, ...rows.map((r) => r.id.length)),
    title: Math.max(5, ...rows.map((r) => r.title.length)),
    status: Math.max(6, ...rows.map((r) => r.status.length)),
    priority: Math.max(8, ...rows.map((r) => r.priority.length)),
    ready: Math.max(5, ...rows.map((r) => r.ready.length)),
    owner: Math.max(5, ...rows.map((r) => r.owner.length)),
    lastUpdated: Math.max(12, ...rows.map((r) => r.lastUpdated.length)),
  };

  const header1 = [
    pad('ID', cols.id),
    pad('Title', cols.title),
    pad('Status', cols.status),
    pad('Priority', cols.priority),
    pad('Ready', cols.ready),
    pad('Owner', cols.owner),
    pad('Last Updated', cols.lastUpdated),
  ].join(' | ');
  const separator = [
    '-'.repeat(cols.id),
    '-'.repeat(cols.title),
    '-'.repeat(cols.status),
    '-'.repeat(cols.priority),
    '-'.repeat(cols.ready),
    '-'.repeat(cols.owner),
    '-'.repeat(cols.lastUpdated),
  ].join(' | ');

  const tableRows = rows
    .map((r) =>
      [
        pad(r.id, cols.id),
        pad(r.title, cols.title),
        pad(r.status, cols.status),
        pad(r.priority, cols.priority),
        pad(r.ready, cols.ready),
        pad(r.owner, cols.owner),
        pad(r.lastUpdated, cols.lastUpdated),
      ].join(' | ')
    )
    .join('\n');

  const invalidCount = features.length - validFeatures.length;
  const invalidNote =
    invalidCount > 0
      ? `\n> ⚠ ${invalidCount} feature file${invalidCount > 1 ? 's' : ''} skipped — missing or invalid frontmatter. Run \`npx repo-memory validate\` for details.\n`
      : '';

  return [
    header,
    '',
    '# Feature Registry',
    '',
    `> Generated: ${generatedAt}`,
    invalidNote,
    '## Feature List',
    '',
    `| ${header1} |`,
    `| ${separator} |`,
    ...rows.map((r, i) => `| ${tableRows.split('\n')[i]} |`),
    '',
  ].join('\n');
}

// ─── next-work-queue.md ──────────────────────────────────────────────────────

function buildNextWorkQueue(
  features: FeatureEntry[],
  header: string,
  generatedAt: string,
  lowerNumberIsHigher: boolean
): string {
  const actionable = features
    .filter((f) => f.frontmatter !== null)
    .filter((f) => {
      const status = f.frontmatter!.status;
      // Exclude terminal statuses
      return !['shipped', 'abandoned', 'superseded', 'deprecated', 'rolled_back'].includes(status);
    })
    .sort((a, b) => {
      const fm_a = a.frontmatter!;
      const fm_b = b.frontmatter!;

      // Sort by readiness first: ready → verify-first → needs-human → blocked
      const readyOrder = READY_VALUES.indexOf(fm_a.ready) - READY_VALUES.indexOf(fm_b.ready);
      if (readyOrder !== 0) return readyOrder;

      // Then by priority
      const pa = fm_a.priority ?? Infinity;
      const pb = fm_b.priority ?? Infinity;
      if (pa !== pb) return lowerNumberIsHigher ? pa - pb : pb - pa;

      return a.slug.localeCompare(b.slug);
    });

  if (actionable.length === 0) {
    return [
      header,
      '',
      '# Next Work Queue',
      '',
      `> Generated: ${generatedAt}`,
      '',
      '_No actionable features found. All features are shipped, abandoned, or have no valid frontmatter._',
      '',
    ].join('\n');
  }

  const rows = actionable.map((f) => {
    const fm = f.frontmatter!;
    return {
      id: fm.id,
      title: fm.title,
      status: fm.status,
      ready: fm.ready,
      priority: fmtPriority(fm.priority),
      nextSafeStep: fm.next_safe_step,
    };
  });

  const cols = {
    id: Math.max(2, ...rows.map((r) => r.id.length)),
    title: Math.max(5, ...rows.map((r) => r.title.length)),
    status: Math.max(6, ...rows.map((r) => r.status.length)),
    ready: Math.max(5, ...rows.map((r) => r.ready.length)),
    priority: Math.max(8, ...rows.map((r) => r.priority.length)),
    nextSafeStep: Math.max(14, ...rows.map((r) => r.nextSafeStep.length)),
  };

  const headerRow = [
    pad('ID', cols.id),
    pad('Title', cols.title),
    pad('Status', cols.status),
    pad('Ready', cols.ready),
    pad('Priority', cols.priority),
    pad('Next Safe Step', cols.nextSafeStep),
  ].join(' | ');
  const sep = [
    '-'.repeat(cols.id),
    '-'.repeat(cols.title),
    '-'.repeat(cols.status),
    '-'.repeat(cols.ready),
    '-'.repeat(cols.priority),
    '-'.repeat(cols.nextSafeStep),
  ].join(' | ');

  const tableRows = rows.map((r) =>
    [
      pad(r.id, cols.id),
      pad(r.title, cols.title),
      pad(r.status, cols.status),
      pad(r.ready, cols.ready),
      pad(r.priority, cols.priority),
      pad(r.nextSafeStep, cols.nextSafeStep),
    ].join(' | ')
  );

  return [
    header,
    '',
    '# Next Work Queue',
    '',
    `> Generated: ${generatedAt}`,
    '',
    `| ${headerRow} |`,
    `| ${sep} |`,
    ...tableRows.map((r) => `| ${r} |`),
    '',
  ].join('\n');
}

// ─── doc-health.md ───────────────────────────────────────────────────────────

function buildDocHealth(
  features: FeatureEntry[],
  header: string,
  generatedAt: string
): string {
  const total = features.length;
  const valid = features.filter((f) => f.frontmatter !== null).length;
  const invalid = total - valid;
  const withErrors = features.filter((f) => f.errors.length > 0 && f.frontmatter === null);

  const statusCounts: Record<string, number> = {};
  for (const f of features) {
    if (f.frontmatter) {
      const s = f.frontmatter.status;
      statusCounts[s] = (statusCounts[s] ?? 0) + 1;
    }
  }

  const statusLines = Object.entries(statusCounts)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([status, count]) => `- ${status}: ${count}`)
    .join('\n');

  const errorSection =
    withErrors.length > 0
      ? [
          '',
          '## Files With Validation Errors',
          '',
          ...withErrors.map((f) => `- \`${path.basename(f.filePath)}\`: ${f.errors.join('; ')}`),
        ].join('\n')
      : '';

  return [
    header,
    '',
    '# Documentation Health',
    '',
    `> Generated: ${generatedAt}`,
    '',
    '## Feature Doc Summary',
    '',
    `- Total feature files: ${total}`,
    `- Valid (parseable frontmatter): ${valid}`,
    `- Invalid or missing frontmatter: ${invalid}`,
    '',
    '## Status Distribution',
    '',
    statusLines || '_No valid features found._',
    errorSection,
    '',
  ].join('\n');
}

// ─── main generate logic ─────────────────────────────────────────────────────

/**
 * Core generate logic. Returns the files that would be written.
 * Does not write anything — callers decide based on dryRun.
 */
export function runGeneration(projectRoot: string): GenerateResult {
  const errors: string[] = [];
  const skipped: string[] = [];
  const generated: GeneratedFile[] = [];

  const config = loadConfig(projectRoot);
  if (!config) {
    return {
      generated: [],
      skipped: [],
      errors: ['No repo-memory.config.yml found. Run: npx repo-memory init'],
    };
  }

  const featuresDir = path.resolve(projectRoot, config.paths.features);
  const { features, duplicateIds } = loadFeatures(featuresDir);

  if (duplicateIds.length > 0) {
    errors.push(`Duplicate feature IDs found: ${duplicateIds.join(', ')}`);
  }

  const generatedAt = new Date().toISOString().split('T')[0];
  const fileHeader = config.generated.header;

  generated.push({
    path: path.resolve(projectRoot, config.generated.feature_registry),
    content: buildFeatureRegistry(features, fileHeader, generatedAt),
  });

  generated.push({
    path: path.resolve(projectRoot, config.generated.next_work_queue),
    content: buildNextWorkQueue(
      features,
      fileHeader,
      generatedAt,
      config.priority.lower_number_is_higher
    ),
  });

  generated.push({
    path: path.resolve(projectRoot, config.generated.doc_health),
    content: buildDocHealth(features, fileHeader, generatedAt),
  });

  return { generated, skipped, errors };
}

/**
 * Write all generated files to disk, creating parent directories as needed.
 */
function writeGeneratedFiles(files: GeneratedFile[]): void {
  for (const file of files) {
    fs.mkdirSync(path.dirname(file.path), { recursive: true });
    fs.writeFileSync(file.path, file.content, 'utf8');
  }
}

/**
 * CLI entry point for the generate command.
 */
export function runGenerateCommand(options: GenerateOptions): void {
  const projectRoot = options.projectRoot ?? findProjectRoot();
  let result: GenerateResult;

  try {
    result = runGeneration(projectRoot);
  } catch (err: any) {
    if (options.json) {
      console.error(JSON.stringify({ success: false, error: err.message }));
    } else {
      console.error(`Generate error: ${err.message}`);
    }
    process.exit(1);
  }

  if (result.errors.length > 0) {
    for (const err of result.errors) {
      console.error(`[ERROR] ${err}`);
    }
    if (!options.dryRun) {
      process.exit(1);
    }
  }

  if (options.dryRun) {
    if (options.json) {
      console.log(JSON.stringify({ dryRun: true, wouldGenerate: result.generated.map((f) => f.path) }));
    } else {
      console.log('Repo Memory Generate (dry run)');
      console.log('==============================');
      for (const file of result.generated) {
        console.log(`Would write: ${file.path}`);
      }
    }
    return;
  }

  writeGeneratedFiles(result.generated);

  if (options.json) {
    console.log(
      JSON.stringify({
        success: true,
        generated: result.generated.map((f) => f.path),
        errors: result.errors,
      })
    );
    return;
  }

  console.log('Repo Memory Generate');
  console.log('====================');
  for (const file of result.generated) {
    console.log(`✓ Written: ${path.relative(projectRoot, file.path)}`);
  }
  if (result.errors.length > 0) {
    console.log('');
    for (const err of result.errors) {
      console.log(`[ERROR] ${err}`);
    }
  }
}
