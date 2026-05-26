/**
 * Generic document indexer used by plan-index and review-index.
 *
 * Reads *.md files from a directory, parses YAML frontmatter, and validates
 * each file against a supplied Zod schema. Returns structured entries and a
 * list of duplicate IDs.
 */

import * as fs from 'fs';
import * as path from 'path';
import { ZodSchema } from 'zod';
import { parseFrontmatter } from './frontmatter';

export interface DocEntry<T> {
  slug: string;
  filePath: string;
  hasFrontmatter: boolean;
  frontmatter: T | null;
  errors: string[];
}

export interface DocIndexResult<T> {
  docs: DocEntry<T>[];
  duplicateIds: string[];
}

const SKIPPED_FILES = new Set(['_template.md', 'readme.md']);

function isSkipped(name: string): boolean {
  return SKIPPED_FILES.has(name.toLowerCase());
}

/**
 * Load and validate all Markdown docs from `docsDir` against `schema`.
 *
 * Files named `_template.md` or `README.md` (case-insensitive) are skipped.
 * Returns an empty result when `docsDir` does not exist.
 */
export function loadDocs<T>(docsDir: string, schema: ZodSchema<T>): DocIndexResult<T> {
  if (!fs.existsSync(docsDir)) {
    return { docs: [], duplicateIds: [] };
  }

  const entries = fs.readdirSync(docsDir, { withFileTypes: true });
  const mdFiles = entries
    .filter((e) => e.isFile() && e.name.endsWith('.md') && !isSkipped(e.name))
    .map((e) => path.join(docsDir, e.name));

  const docs: DocEntry<T>[] = mdFiles.map((filePath) => {
    const slug = path.basename(filePath, '.md');
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

    const result = schema.safeParse(parsed.data);
    if (!result.success) {
      const errors = result.error.errors.map(
        (e) => `${e.path.join('.') || 'root'}: ${e.message}`
      );
      return { slug, filePath, hasFrontmatter: true, frontmatter: null, errors };
    }

    const idErrors: string[] = [];
    const data = result.data as any;
    if (data.id && data.id !== slug) {
      idErrors.push(`id mismatch: frontmatter id "${data.id}" does not match file slug "${slug}"`);
    }

    return { slug, filePath, hasFrontmatter: true, frontmatter: result.data, errors: idErrors };
  });

  // Detect duplicate IDs
  const idCounts = new Map<string, number>();
  for (const doc of docs) {
    const id = (doc.frontmatter as any)?.id ?? doc.slug;
    idCounts.set(id, (idCounts.get(id) ?? 0) + 1);
  }
  const duplicateIds = [...idCounts.entries()]
    .filter(([, n]) => n > 1)
    .map(([id]) => id);

  return { docs, duplicateIds };
}
