import { describe, it, expect } from 'vitest';
import { parseFrontmatter } from '../../src/core/frontmatter';

describe('parseFrontmatter', () => {
  it('parses a valid YAML frontmatter block', () => {
    const content = `---
id: my-feature
title: My Feature
status: planned
---

# My Feature

Body text here.
`;
    const result = parseFrontmatter(content);
    expect(result.hasFrontmatter).toBe(true);
    expect(result.data.id).toBe('my-feature');
    expect(result.data.title).toBe('My Feature');
    expect(result.data.status).toBe('planned');
    expect(result.body).toContain('Body text here.');
  });

  it('returns hasFrontmatter false when there is no frontmatter block', () => {
    const content = `# My Feature\n\nBody text here.\n`;
    const result = parseFrontmatter(content);
    expect(result.hasFrontmatter).toBe(false);
    expect(result.data).toEqual({});
  });

  it('returns hasFrontmatter false for an empty frontmatter block', () => {
    const content = `---\n---\n\n# Body\n`;
    const result = parseFrontmatter(content);
    expect(result.hasFrontmatter).toBe(false);
  });

  it('returns the body without the frontmatter block', () => {
    const content = `---
id: x
---

Some body.
`;
    const result = parseFrontmatter(content);
    expect(result.body.trim()).toBe('Some body.');
  });

  it('handles frontmatter with array fields', () => {
    const content = `---
id: feat
blocked_by:
  - dep-one
  - dep-two
---
`;
    const result = parseFrontmatter(content);
    expect(result.data.blocked_by).toEqual(['dep-one', 'dep-two']);
  });

  it('handles frontmatter with numeric fields', () => {
    const content = `---
id: feat
priority: 3
---
`;
    const result = parseFrontmatter(content);
    expect(result.data.priority).toBe(3);
  });

  it('throws for syntactically invalid YAML inside the block', () => {
    // gray-matter itself may not throw on all invalid YAML; this is a
    // best-effort test for clearly broken input.
    const content = `---
id: [unclosed bracket
---
`;
    expect(() => parseFrontmatter(content)).toThrow();
  });
});
