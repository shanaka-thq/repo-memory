import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';
import { discoverRepoState } from '../../src/core/discovery';

function mkdirp(dir: string) {
  fs.mkdirSync(dir, { recursive: true });
}

function touch(filePath: string, content = '') {
  mkdirp(path.dirname(filePath));
  fs.writeFileSync(filePath, content, 'utf8');
}

describe('discoverRepoState', () => {
  let tmpDir: string;

  beforeEach(() => {
    tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'repo-memory-test-'));
    // Make it look like a git repo
    mkdirp(path.join(tmpDir, '.git'));
  });

  afterEach(() => {
    fs.rmSync(tmpDir, { recursive: true, force: true });
  });

  it('detects absent when nothing exists', () => {
    const state = discoverRepoState(tmpDir);
    expect(state.repoMemoryVersion).toBe('absent');
    expect(state.configExists).toBe(false);
    expect(state.existingAgentFiles).toHaveLength(0);
  });

  it('detects v2-style when SKILL.md exists but no v3 modes dir', () => {
    mkdirp(path.join(tmpDir, 'skills/repo-memory'));
    touch(path.join(tmpDir, 'skills/repo-memory/SKILL.md'), 'Version: 2.5.0');
    const state = discoverRepoState(tmpDir);
    expect(state.repoMemoryVersion).toBe('v2-style');
  });

  it('detects v2-style from v2 central files', () => {
    touch(path.join(tmpDir, 'docs/feature-registry.md'), '# Feature Registry');
    const state = discoverRepoState(tmpDir);
    expect(state.repoMemoryVersion).toBe('v2-style');
    expect(state.v2CentralFiles).toContain('docs/feature-registry.md');
  });

  it('detects v3-style when modes dir exists', () => {
    mkdirp(path.join(tmpDir, 'skills/repo-memory/modes'));
    const state = discoverRepoState(tmpDir);
    expect(state.repoMemoryVersion).toBe('v3-style');
  });

  it('detects v3-style from config version 3', () => {
    touch(path.join(tmpDir, 'repo-memory.config.yml'), 'version: 3\n');
    const state = discoverRepoState(tmpDir);
    expect(state.repoMemoryVersion).toBe('v3-style');
    expect(state.configExists).toBe(true);
    expect(state.configVersion).toBe(3);
  });

  it('detects AGENTS.md in existingAgentFiles', () => {
    touch(path.join(tmpDir, 'AGENTS.md'), '# Agent Instructions');
    const state = discoverRepoState(tmpDir);
    expect(state.existingAgentFiles).toContain('AGENTS.md');
  });

  it('detects CLAUDE.md in existingAgentFiles', () => {
    touch(path.join(tmpDir, 'CLAUDE.md'), '# Claude Code Instructions');
    const state = discoverRepoState(tmpDir);
    expect(state.existingAgentFiles).toContain('CLAUDE.md');
  });

  it('detects GitHub Copilot instructions', () => {
    touch(path.join(tmpDir, '.github/copilot-instructions.md'), '# Copilot');
    const state = discoverRepoState(tmpDir);
    expect(state.existingAgentFiles).toContain('.github/copilot-instructions.md');
  });

  it('detects plans directories', () => {
    mkdirp(path.join(tmpDir, 'docs/plans'));
    const state = discoverRepoState(tmpDir);
    expect(state.existingPlansDirs).toContain('docs/plans');
  });

  it('detects superpowers plans directory', () => {
    mkdirp(path.join(tmpDir, 'docs/superpowers/plans'));
    const state = discoverRepoState(tmpDir);
    expect(state.existingPlansDirs).toContain('docs/superpowers/plans');
  });

  it('detects reviews directories', () => {
    mkdirp(path.join(tmpDir, 'docs/reviews'));
    const state = discoverRepoState(tmpDir);
    expect(state.existingReviewsDirs).toContain('docs/reviews');
  });

  it('detects monorepo indicator turbo.json', () => {
    touch(path.join(tmpDir, 'turbo.json'), '{}');
    const state = discoverRepoState(tmpDir);
    expect(state.monorepoIndicators).toContain('turbo.json');
  });

  it('detects monorepo packages/ directory', () => {
    mkdirp(path.join(tmpDir, 'packages/my-pkg'));
    const state = discoverRepoState(tmpDir);
    expect(state.monorepoIndicators).toContain('packages/');
  });

  it('flags conflict when multiple plan dirs exist', () => {
    mkdirp(path.join(tmpDir, 'docs/plans'));
    mkdirp(path.join(tmpDir, 'docs/superpowers/plans'));
    const state = discoverRepoState(tmpDir);
    expect(state.conflicts.some(c => c.includes('Multiple plans directories'))).toBe(true);
  });

  it('detects all v2 central files', () => {
    touch(path.join(tmpDir, 'docs/feature-registry.md'), '# FR');
    touch(path.join(tmpDir, 'docs/doc-health.md'), '# DH');
    touch(path.join(tmpDir, 'docs/implementation-log.md'), '# IL');
    const state = discoverRepoState(tmpDir);
    expect(state.v2CentralFiles).toContain('docs/feature-registry.md');
    expect(state.v2CentralFiles).toContain('docs/doc-health.md');
    expect(state.v2CentralFiles).toContain('docs/implementation-log.md');
  });

  it('detects docs root', () => {
    mkdirp(path.join(tmpDir, 'docs'));
    const state = discoverRepoState(tmpDir);
    expect(state.docsRootExists).toBe(true);
  });
});
