import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';
import { loadDocs } from '../../src/core/doc-index';
import { planSchema } from '../../src/schemas/plan.schema';
import { reviewSchema } from '../../src/schemas/review.schema';

// ─── Plan helpers ────────────────────────────────────────────────────────────

const validPlanFm = (overrides: Record<string, unknown> = {}): string => {
  const fm = { id: 'my-plan', title: 'My Plan', status: 'draft', doc_type: 'plan', ...overrides };
  const lines = Object.entries(fm).map(([k, v]) => `${k}: ${JSON.stringify(v)}`).join('\n');
  return `---\n${lines}\n---\n\n# Plan\n`;
};

// ─── Review helpers ──────────────────────────────────────────────────────────

const validReviewFm = (overrides: Record<string, unknown> = {}): string => {
  const fm = { id: 'my-review', title: 'My Review', status: 'active', doc_type: 'review', ...overrides };
  const lines = Object.entries(fm).map(([k, v]) => `${k}: ${JSON.stringify(v)}`).join('\n');
  return `---\n${lines}\n---\n\n# Review\n`;
};

// ─── Shared setup ─────────────────────────────────────────────────────────────

describe('loadDocs (plan schema)', () => {
  let tmpDir: string;

  beforeEach(() => {
    tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'rm-doc-index-test-'));
  });

  afterEach(() => {
    fs.rmSync(tmpDir, { recursive: true, force: true });
  });

  it('returns empty result when directory does not exist', () => {
    const result = loadDocs(path.join(tmpDir, 'does-not-exist'), planSchema);
    expect(result.docs).toHaveLength(0);
    expect(result.duplicateIds).toHaveLength(0);
  });

  it('returns empty result for an empty directory', () => {
    const result = loadDocs(tmpDir, planSchema);
    expect(result.docs).toHaveLength(0);
  });

  it('parses a valid plan file', () => {
    fs.writeFileSync(path.join(tmpDir, 'my-plan.md'), validPlanFm(), 'utf8');
    const { docs } = loadDocs(tmpDir, planSchema);
    expect(docs).toHaveLength(1);
    expect(docs[0].slug).toBe('my-plan');
    expect(docs[0].hasFrontmatter).toBe(true);
    expect(docs[0].frontmatter).not.toBeNull();
    expect(docs[0].errors).toHaveLength(0);
  });

  it('reports an error when frontmatter is missing', () => {
    fs.writeFileSync(path.join(tmpDir, 'no-fm.md'), '# No Frontmatter\n', 'utf8');
    const { docs } = loadDocs(tmpDir, planSchema);
    expect(docs[0].hasFrontmatter).toBe(false);
    expect(docs[0].errors[0]).toContain('Missing YAML frontmatter block');
  });

  it('reports an error for invalid plan status', () => {
    fs.writeFileSync(path.join(tmpDir, 'bad.md'), validPlanFm({ id: 'bad', status: 'in_progress' }), 'utf8');
    const { docs } = loadDocs(tmpDir, planSchema);
    expect(docs[0].frontmatter).toBeNull();
    expect(docs[0].errors.some((e) => e.includes('status'))).toBe(true);
  });

  it('reports an id mismatch', () => {
    fs.writeFileSync(path.join(tmpDir, 'my-plan.md'), validPlanFm({ id: 'wrong-id' }), 'utf8');
    const { docs } = loadDocs(tmpDir, planSchema);
    expect(docs[0].errors.some((e) => e.includes('id mismatch'))).toBe(true);
  });

  it('skips _template.md and README.md', () => {
    fs.writeFileSync(path.join(tmpDir, '_template.md'), validPlanFm({ id: 'tpl' }), 'utf8');
    fs.writeFileSync(path.join(tmpDir, 'README.md'), '# Plans\n', 'utf8');
    fs.writeFileSync(path.join(tmpDir, 'real-plan.md'), validPlanFm({ id: 'real-plan' }), 'utf8');
    const { docs } = loadDocs(tmpDir, planSchema);
    expect(docs).toHaveLength(1);
    expect(docs[0].slug).toBe('real-plan');
  });

  it('detects duplicate plan IDs', () => {
    fs.writeFileSync(path.join(tmpDir, 'p1.md'), validPlanFm({ id: 'dup-id' }), 'utf8');
    fs.writeFileSync(path.join(tmpDir, 'p2.md'), validPlanFm({ id: 'dup-id', title: 'Dup 2' }), 'utf8');
    const { duplicateIds } = loadDocs(tmpDir, planSchema);
    expect(duplicateIds).toContain('dup-id');
  });

  it('parses optional plan fields', () => {
    const fm = validPlanFm({ id: 'opt', feature: 'auth', owner: 'team', confidence: 'high' });
    fs.writeFileSync(path.join(tmpDir, 'opt.md'), fm, 'utf8');
    const { docs } = loadDocs(tmpDir, planSchema);
    const data = docs[0].frontmatter as any;
    expect(data.feature).toBe('auth');
    expect(data.owner).toBe('team');
    expect(data.confidence).toBe('high');
  });
});

describe('loadDocs (review schema)', () => {
  let tmpDir: string;

  beforeEach(() => {
    tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'rm-review-index-test-'));
  });

  afterEach(() => {
    fs.rmSync(tmpDir, { recursive: true, force: true });
  });

  it('parses a valid review file', () => {
    fs.writeFileSync(path.join(tmpDir, 'my-review.md'), validReviewFm(), 'utf8');
    const { docs } = loadDocs(tmpDir, reviewSchema);
    expect(docs).toHaveLength(1);
    expect(docs[0].frontmatter).not.toBeNull();
    expect(docs[0].errors).toHaveLength(0);
  });

  it('reports an error for invalid review status', () => {
    fs.writeFileSync(path.join(tmpDir, 'bad.md'), validReviewFm({ id: 'bad', status: 'shipped' }), 'utf8');
    const { docs } = loadDocs(tmpDir, reviewSchema);
    expect(docs[0].frontmatter).toBeNull();
    expect(docs[0].errors.some((e) => e.includes('status'))).toBe(true);
  });

  it('parses optional review fields', () => {
    const fm = validReviewFm({
      id: 'opt',
      review_type: 'security',
      subject: 'auth module',
      reviewer: 'agent-x',
      disposition: 'accepted',
    });
    fs.writeFileSync(path.join(tmpDir, 'opt.md'), fm, 'utf8');
    const { docs } = loadDocs(tmpDir, reviewSchema);
    const data = docs[0].frontmatter as any;
    expect(data.review_type).toBe('security');
    expect(data.disposition).toBe('accepted');
    expect(data.reviewer).toBe('agent-x');
  });

  it('detects duplicate review IDs', () => {
    fs.writeFileSync(path.join(tmpDir, 'r1.md'), validReviewFm({ id: 'dup' }), 'utf8');
    fs.writeFileSync(path.join(tmpDir, 'r2.md'), validReviewFm({ id: 'dup', title: 'Dup 2' }), 'utf8');
    const { duplicateIds } = loadDocs(tmpDir, reviewSchema);
    expect(duplicateIds).toContain('dup');
  });
});
