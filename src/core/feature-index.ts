import * as fs from 'fs';
import * as path from 'path';
import { parseFrontmatter } from './frontmatter';
import { featureSchema, FeatureFrontmatter } from '../schemas/feature.schema';

export interface FeatureEntry {
  /** Slug derived from the file name (without .md) */
  slug: string;
  /** Absolute path to the feature file */
  filePath: string;
  /** True when the file has a YAML frontmatter block */
  hasFrontmatter: boolean;
  /** Parsed and validated frontmatter data (null when validation failed or missing) */
  frontmatter: FeatureFrontmatter | null;
  /** Validation errors from the Zod schema (empty when valid) */
  errors: string[];
}

export interface FeatureIndexResult {
  features: FeatureEntry[];
  /** Feature slugs that appear more than once */
  duplicateIds: string[];
}

/**
 * Resolve the slug from a feature file path.
 * Extracts the file name without the .md extension.
 * Skips _template.md and README.md.
 */
function slugFromPath(filePath: string): string {
  return path.basename(filePath, '.md');
}

/**
 * Return true when the file name should be excluded from indexing.
 * Excludes template and README files.
 */
function isSkippedFile(filePath: string): boolean {
  const name = path.basename(filePath);
  return name === '_template.md' || name.toLowerCase() === 'readme.md';
}

/**
 * Load and parse all feature docs from the features directory.
 *
 * For each *.md file in `featuresDir` (non-recursive, top-level only):
 *   - Parses YAML frontmatter via gray-matter.
 *   - Validates the frontmatter against the featureSchema.
 *   - Collects validation errors without throwing.
 *   - Detects duplicate feature IDs.
 *
 * Returns all entries plus the list of duplicate IDs.
 * Returns an empty result when featuresDir does not exist.
 */
export function loadFeatures(featuresDir: string): FeatureIndexResult {
  if (!fs.existsSync(featuresDir)) {
    return { features: [], duplicateIds: [] };
  }

  const entries = fs.readdirSync(featuresDir, { withFileTypes: true });
  const mdFiles = entries
    .filter((e) => e.isFile() && e.name.endsWith('.md') && !isSkippedFile(e.name))
    .map((e) => path.join(featuresDir, e.name));

  const features: FeatureEntry[] = mdFiles.map((filePath) => {
    const slug = slugFromPath(filePath);
    const rawContent = fs.readFileSync(filePath, 'utf8');
    const hasFrontmatterFence = rawContent.trimStart().startsWith('---');

    let parsed;
    try {
      parsed = parseFrontmatter(rawContent);
    } catch (err: any) {
      return {
        slug,
        filePath,
        hasFrontmatter: hasFrontmatterFence,
        frontmatter: null,
        errors: [`YAML parse error: ${err.message}`],
      };
    }

    if (!parsed.hasFrontmatter) {
      return {
        slug,
        filePath,
        hasFrontmatter: false,
        frontmatter: null,
        errors: ['Missing YAML frontmatter block'],
      };
    }

    const result = featureSchema.safeParse(parsed.data);
    if (!result.success) {
      const errors = result.error.errors.map(
        (e) => `${e.path.join('.') || 'root'}: ${e.message}`
      );
      return {
        slug,
        filePath,
        hasFrontmatter: true,
        frontmatter: null,
        errors,
      };
    }

    // Warn when the frontmatter id does not match the file slug
    const idErrors: string[] = [];
    if (result.data.id !== slug) {
      idErrors.push(
        `id mismatch: frontmatter id "${result.data.id}" does not match file slug "${slug}"`
      );
    }

    return {
      slug,
      filePath,
      hasFrontmatter: true,
      frontmatter: result.data,
      errors: idErrors,
    };
  });

  // Detect duplicate IDs across all entries that have valid frontmatter
  const idCounts: Map<string, number> = new Map();
  for (const entry of features) {
    const id = entry.frontmatter?.id ?? entry.slug;
    idCounts.set(id, (idCounts.get(id) ?? 0) + 1);
  }
  const duplicateIds = Array.from(idCounts.entries())
    .filter(([, count]) => count > 1)
    .map(([id]) => id);

  return { features, duplicateIds };
}
