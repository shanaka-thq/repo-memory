import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';
import { loadFeatures } from '../../src/core/feature-index';

// Minimal valid frontmatter for a feature doc
const validFrontmatter = (overrides: Record<string, unknown> = {}): string => {
  const fm = {
    id: 'my-feature',
    title: 'My Feature',
    status: 'planned',
    doc_type: 'feature',
    ready: 'ready',
    next_safe_step: 'Do something useful',
    ...overrides,
  };
  const lines = Object.entries(fm)
    .map(([k, v]) => `${k}: ${JSON.stringify(v)}`)
    .join('\n');
  return `---\n${lines}\n---\n\n# My Feature\n`;
};

describe('loadFeatures', () => {
  let tmpDir: string;

  beforeEach(() => {
    tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'repo-memory-fi-test-'));
  });

  afterEach(() => {
    fs.rmSync(tmpDir, { recursive: true, force: true });
  });

  it('returns empty result when the features directory does not exist', () => {
    const result = loadFeatures(path.join(tmpDir, 'does-not-exist'));
    expect(result.features).toHaveLength(0);
    expect(result.duplicateIds).toHaveLength(0);
  });

  it('returns empty result for an empty directory', () => {
    const result = loadFeatures(tmpDir);
    expect(result.features).toHaveLength(0);
  });

  it('parses a valid feature file', () => {
    fs.writeFileSync(path.join(tmpDir, 'my-feature.md'), validFrontmatter(), 'utf8');
    const { features } = loadFeatures(tmpDir);
    expect(features).toHaveLength(1);
    expect(features[0].slug).toBe('my-feature');
    expect(features[0].hasFrontmatter).toBe(true);
    expect(features[0].frontmatter).not.toBeNull();
    expect(features[0].frontmatter!.title).toBe('My Feature');
    expect(features[0].errors).toHaveLength(0);
  });

  it('reports an error for a file with no frontmatter', () => {
    fs.writeFileSync(
      path.join(tmpDir, 'no-fm.md'),
      '# No Frontmatter\n\nBody only.\n',
      'utf8'
    );
    const { features } = loadFeatures(tmpDir);
    expect(features[0].hasFrontmatter).toBe(false);
    expect(features[0].frontmatter).toBeNull();
    expect(features[0].errors[0]).toContain('Missing YAML frontmatter block');
  });

  it('reports validation errors for invalid status', () => {
    const content = validFrontmatter({ id: 'bad-status', status: 'unknown-status' });
    fs.writeFileSync(path.join(tmpDir, 'bad-status.md'), content, 'utf8');
    const { features } = loadFeatures(tmpDir);
    expect(features[0].frontmatter).toBeNull();
    expect(features[0].errors.some((e) => e.includes('status'))).toBe(true);
  });

  it('reports an id mismatch when frontmatter id differs from the file slug', () => {
    const content = validFrontmatter({ id: 'wrong-id' });
    fs.writeFileSync(path.join(tmpDir, 'my-feature.md'), content, 'utf8');
    const { features } = loadFeatures(tmpDir);
    // id mismatch: frontmatter is valid but there is an id-mismatch error
    expect(features[0].errors.some((e) => e.includes('id mismatch'))).toBe(true);
  });

  it('skips _template.md and README.md', () => {
    fs.writeFileSync(path.join(tmpDir, '_template.md'), validFrontmatter({ id: '_template' }), 'utf8');
    fs.writeFileSync(path.join(tmpDir, 'README.md'), '# Features\n', 'utf8');
    fs.writeFileSync(path.join(tmpDir, 'real-feature.md'), validFrontmatter({ id: 'real-feature' }), 'utf8');
    const { features } = loadFeatures(tmpDir);
    expect(features).toHaveLength(1);
    expect(features[0].slug).toBe('real-feature');
  });

  it('detects duplicate IDs across feature files', () => {
    const fm1 = validFrontmatter({ id: 'dup-feature' });
    const fm2 = validFrontmatter({ id: 'dup-feature', title: 'Dup Feature 2' });
    fs.writeFileSync(path.join(tmpDir, 'dup-feature.md'), fm1, 'utf8');
    fs.writeFileSync(path.join(tmpDir, 'dup-feature-2.md'), fm2, 'utf8');
    const { duplicateIds } = loadFeatures(tmpDir);
    expect(duplicateIds).toContain('dup-feature');
  });

  it('parses optional fields correctly', () => {
    const content = validFrontmatter({
      id: 'optional-fields',
      priority: 5,
      owner: 'backend-team',
      confidence: 'high',
      blocked_by: ['other-feature'],
      last_updated: '2026-05-01',
    });
    fs.writeFileSync(path.join(tmpDir, 'optional-fields.md'), content, 'utf8');
    const { features } = loadFeatures(tmpDir);
    const fm = features[0].frontmatter!;
    expect(fm.priority).toBe(5);
    expect(fm.owner).toBe('backend-team');
    expect(fm.confidence).toBe('high');
    expect(fm.blocked_by).toEqual(['other-feature']);
    expect(fm.last_updated).toBe('2026-05-01');
  });

  it('handles multiple valid feature files', () => {
    const slugs = ['alpha', 'beta', 'gamma'];
    for (const slug of slugs) {
      fs.writeFileSync(
        path.join(tmpDir, `${slug}.md`),
        validFrontmatter({ id: slug, title: slug }),
        'utf8'
      );
    }
    const { features, duplicateIds } = loadFeatures(tmpDir);
    expect(features).toHaveLength(3);
    expect(duplicateIds).toHaveLength(0);
  });
});
