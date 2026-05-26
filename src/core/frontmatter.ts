import matter from 'gray-matter';

export interface ParsedFrontmatter {
  /** Parsed YAML frontmatter data */
  data: Record<string, unknown>;
  /** Document body with the frontmatter block removed */
  body: string;
  /** True when the file has a non-empty YAML frontmatter block (--- delimited) */
  hasFrontmatter: boolean;
}

/**
 * Parse YAML frontmatter from a Markdown file's raw content.
 *
 * Returns structured data and the remaining body. Uses gray-matter so the
 * caller does not need to handle --- delimiter parsing directly.
 *
 * Throws if the YAML inside the frontmatter block is syntactically invalid.
 */
export function parseFrontmatter(rawContent: string): ParsedFrontmatter {
  const result = matter(rawContent);
  const hasFrontmatter =
    rawContent.trimStart().startsWith('---') && Object.keys(result.data).length > 0;
  return {
    data: result.data as Record<string, unknown>,
    body: result.content,
    hasFrontmatter,
  };
}
