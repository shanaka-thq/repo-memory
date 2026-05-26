import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';
import { installAdapter } from '../../src/commands/install-adapter';
import { MANAGED_BLOCK_START, MANAGED_BLOCK_END, wrapInManagedBlock, upsertManagedBlock } from '../../src/adapters/content';

describe('installAdapter', () => {
  let tmpDir: string;

  beforeEach(() => {
    tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'rm-install-adapter-test-'));
  });

  afterEach(() => {
    fs.rmSync(tmpDir, { recursive: true, force: true });
  });

  it('writes the adapter file when it does not exist', () => {
    const result = installAdapter('claude-code', tmpDir, {});
    expect(result.action).toBe('written');
    expect(fs.existsSync(path.join(tmpDir, 'CLAUDE.md'))).toBe(true);
    expect(fs.readFileSync(path.join(tmpDir, 'CLAUDE.md'), 'utf8')).toContain('Claude Code Instructions');
  });

  it('skips when file already exists and --force is not set', () => {
    fs.writeFileSync(path.join(tmpDir, 'CLAUDE.md'), '# Existing\n', 'utf8');
    const result = installAdapter('claude-code', tmpDir, {});
    expect(result.action).toBe('skipped');
    expect(fs.readFileSync(path.join(tmpDir, 'CLAUDE.md'), 'utf8')).toBe('# Existing\n');
  });

  it('overwrites when --force is set', () => {
    fs.writeFileSync(path.join(tmpDir, 'CLAUDE.md'), '# Old content\n', 'utf8');
    const result = installAdapter('claude-code', tmpDir, { force: true });
    expect(result.action).toBe('written');
    expect(fs.readFileSync(path.join(tmpDir, 'CLAUDE.md'), 'utf8')).toContain('Claude Code Instructions');
  });

  it('returns dry-run without writing when --dry-run is set', () => {
    const result = installAdapter('claude-code', tmpDir, { dryRun: true });
    expect(result.action).toBe('dry-run');
    expect(fs.existsSync(path.join(tmpDir, 'CLAUDE.md'))).toBe(false);
  });

  it('returns printed content without writing when --print is set', () => {
    const result = installAdapter('claude-code', tmpDir, { print: true });
    expect(result.action).toBe('printed');
    expect(result.message).toContain('Claude Code Instructions');
    expect(fs.existsSync(path.join(tmpDir, 'CLAUDE.md'))).toBe(false);
  });

  it('creates nested directories for adapters with nested target paths', () => {
    const result = installAdapter('github-copilot', tmpDir, {});
    expect(result.action).toBe('written');
    expect(fs.existsSync(path.join(tmpDir, '.github', 'copilot-instructions.md'))).toBe(true);
  });

  it('returns an error result for an unknown agent', () => {
    const result = installAdapter('unknown-agent', tmpDir, {});
    expect(result.action).toBe('skipped');
    expect(result.message).toContain('Unknown agent');
  });

  it('appends a managed block to an existing file', () => {
    fs.writeFileSync(path.join(tmpDir, 'CLAUDE.md'), '# Existing content\n', 'utf8');
    const result = installAdapter('claude-code', tmpDir, { append: true });
    expect(result.action).toBe('appended');
    const content = fs.readFileSync(path.join(tmpDir, 'CLAUDE.md'), 'utf8');
    expect(content).toContain('# Existing content');
    expect(content).toContain(MANAGED_BLOCK_START);
    expect(content).toContain(MANAGED_BLOCK_END);
    expect(content).toContain('Claude Code Instructions');
  });

  it('updates an existing managed block on re-append', () => {
    const initial = `# Existing\n\n${MANAGED_BLOCK_START}\n# Old block\n${MANAGED_BLOCK_END}\n`;
    fs.writeFileSync(path.join(tmpDir, 'CLAUDE.md'), initial, 'utf8');
    installAdapter('claude-code', tmpDir, { append: true });
    const content = fs.readFileSync(path.join(tmpDir, 'CLAUDE.md'), 'utf8');
    // Should have exactly one managed block
    expect(content.split(MANAGED_BLOCK_START).length - 1).toBe(1);
    expect(content).not.toContain('# Old block');
    expect(content).toContain('Claude Code Instructions');
  });

  it('creates the file with a managed block when --append and file does not exist', () => {
    const result = installAdapter('generic', tmpDir, { append: true });
    expect(result.action).toBe('appended');
    const content = fs.readFileSync(path.join(tmpDir, 'AGENTS.md'), 'utf8');
    expect(content).toContain(MANAGED_BLOCK_START);
  });

  it('supports all 8 known adapters', () => {
    const agents = ['generic', 'claude-code', 'github-copilot', 'codex', 'opencode', 'cursor', 'windsurf', 'kiro'];
    for (const agent of agents) {
      const dir = fs.mkdtempSync(path.join(os.tmpdir(), `rm-adapter-${agent}-`));
      try {
        const result = installAdapter(agent, dir, {});
        expect(result.action).toBe('written');
        expect(fs.existsSync(path.join(dir, result.targetFile))).toBe(true);
      } finally {
        fs.rmSync(dir, { recursive: true, force: true });
      }
    }
  });
});

describe('managed block helpers', () => {
  it('wrapInManagedBlock wraps content with start/end markers', () => {
    const wrapped = wrapInManagedBlock('hello\nworld');
    expect(wrapped.startsWith(MANAGED_BLOCK_START)).toBe(true);
    expect(wrapped).toContain(MANAGED_BLOCK_END);
    expect(wrapped).toContain('hello');
  });

  it('upsertManagedBlock appends when no existing block', () => {
    const result = upsertManagedBlock('# Existing\n', 'new content');
    expect(result).toContain('# Existing');
    expect(result).toContain(MANAGED_BLOCK_START);
    expect(result).toContain('new content');
  });

  it('upsertManagedBlock replaces an existing block', () => {
    const existing = `# File\n\n${MANAGED_BLOCK_START}\nold\n${MANAGED_BLOCK_END}\n`;
    const result = upsertManagedBlock(existing, 'replaced');
    expect(result).toContain('# File');
    expect(result).toContain('replaced');
    expect(result).not.toContain('old');
    expect(result.split(MANAGED_BLOCK_START).length - 1).toBe(1);
  });
});
