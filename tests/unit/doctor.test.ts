import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';
import { runDoctorCommand } from '../../src/commands/doctor';

function mkdirp(dir: string) {
  fs.mkdirSync(dir, { recursive: true });
}

function touch(filePath: string, content = '') {
  mkdirp(path.dirname(filePath));
  fs.writeFileSync(filePath, content, 'utf8');
}

/** Capture console.log calls during fn() and return the collected lines. */
function captureLog(fn: () => void): string[] {
  const logs: string[] = [];
  const spy = vi.spyOn(console, 'log').mockImplementation((...args) => {
    logs.push(args.join(' '));
  });
  try {
    fn();
  } finally {
    spy.mockRestore();
  }
  return logs;
}

describe('runDoctorCommand', () => {
  let tmpDir: string;

  beforeEach(() => {
    tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'repo-memory-doctor-test-'));
    mkdirp(path.join(tmpDir, '.git'));
  });

  afterEach(() => {
    fs.rmSync(tmpDir, { recursive: true, force: true });
  });

  it('runs without error on absent repo and shows header', () => {
    const logs = captureLog(() => runDoctorCommand({ projectRoot: tmpDir }));
    expect(logs.some(l => l.includes('Repo Memory Doctor'))).toBe(true);
    expect(logs.some(l => l.includes('absent'))).toBe(true);
  });

  it('outputs valid JSON when --json flag is set', () => {
    let output = '';
    const spy = vi.spyOn(console, 'log').mockImplementation((msg) => { output = msg; });
    try {
      runDoctorCommand({ json: true, projectRoot: tmpDir });
    } finally {
      spy.mockRestore();
    }
    const parsed = JSON.parse(output);
    expect(parsed).toHaveProperty('repoMemoryVersion');
    expect(parsed).toHaveProperty('configExists');
    expect(parsed).toHaveProperty('existingAgentFiles');
    expect(Array.isArray(parsed.existingAgentFiles)).toBe(true);
  });

  it('detects v2-style and recommends migration', () => {
    touch(path.join(tmpDir, 'docs/feature-registry.md'), '# FR');
    mkdirp(path.join(tmpDir, 'skills/repo-memory'));
    touch(path.join(tmpDir, 'skills/repo-memory/SKILL.md'), 'Version: 2.5.0');

    const logs = captureLog(() => runDoctorCommand({ projectRoot: tmpDir }));
    expect(logs.some(l => l.includes('v2-style'))).toBe(true);
    expect(logs.some(l => l.includes('migrate'))).toBe(true);
  });

  it('detects v3-style and recommends validate', () => {
    mkdirp(path.join(tmpDir, 'skills/repo-memory/modes'));
    touch(path.join(tmpDir, 'repo-memory.config.yml'), 'version: 3\n');

    const logs = captureLog(() => runDoctorCommand({ projectRoot: tmpDir }));
    expect(logs.some(l => l.includes('v3-style'))).toBe(true);
    expect(logs.some(l => l.includes('validate'))).toBe(true);
  });

  it('detects AGENTS.md in agent files section', () => {
    touch(path.join(tmpDir, 'AGENTS.md'), '# Agent Instructions');

    const logs = captureLog(() => runDoctorCommand({ projectRoot: tmpDir }));
    expect(logs.some(l => l.includes('AGENTS.md'))).toBe(true);
  });

  it('detects plans directory and reports it', () => {
    mkdirp(path.join(tmpDir, 'docs/plans'));

    const logs = captureLog(() => runDoctorCommand({ projectRoot: tmpDir }));
    expect(logs.some(l => l.includes('docs/plans'))).toBe(true);
  });

  it('detects superpowers plans and recommends map command', () => {
    mkdirp(path.join(tmpDir, 'skills/repo-memory'));
    touch(path.join(tmpDir, 'skills/repo-memory/SKILL.md'), 'Version: 2.5.0');
    mkdirp(path.join(tmpDir, 'docs/superpowers/plans'));

    const logs = captureLog(() => runDoctorCommand({ projectRoot: tmpDir }));
    expect(logs.some(l => l.includes('map plans'))).toBe(true);
  });

  it('shows conflict warning when multiple plan dirs exist', () => {
    mkdirp(path.join(tmpDir, 'docs/plans'));
    mkdirp(path.join(tmpDir, 'docs/superpowers/plans'));

    const logs = captureLog(() => runDoctorCommand({ projectRoot: tmpDir }));
    // conflict prints with [!] prefix
    expect(logs.some(l => l.includes('[!]') && l.includes('plans'))).toBe(true);
  });
});
