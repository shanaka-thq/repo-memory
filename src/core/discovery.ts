import * as fs from 'fs';
import * as path from 'path';
import * as yaml from 'js-yaml';

export interface RepoState {
  repoMemoryVersion: 'absent' | 'v2-style' | 'v3-style' | 'unknown';
  configExists: boolean;
  configVersion: number | null;
  docsRootExists: boolean;
  existingDocsDirs: string[];
  existingAgentFiles: string[];
  existingPlansDirs: string[];
  existingReviewsDirs: string[];
  v2CentralFiles: string[];
  customConventions: string[];
  monorepoIndicators: string[];
  conflicts: string[];
}

/**
 * Scans the repository starting at projectRoot to detect state, files, directories,
 * and monorepo indicators.
 */
export function discoverRepoState(projectRoot: string): RepoState {
  const state: RepoState = {
    repoMemoryVersion: 'absent',
    configExists: false,
    configVersion: null,
    docsRootExists: false,
    existingDocsDirs: [],
    existingAgentFiles: [],
    existingPlansDirs: [],
    existingReviewsDirs: [],
    v2CentralFiles: [],
    customConventions: [],
    monorepoIndicators: [],
    conflicts: [],
  };

  // 1. Detect config existence and version
  const configPathYml = path.join(projectRoot, 'repo-memory.config.yml');
  const configPathYaml = path.join(projectRoot, 'repo-memory.config.yaml');
  let configPath: string | null = null;
  if (fs.existsSync(configPathYml)) {
    configPath = configPathYml;
  } else if (fs.existsSync(configPathYaml)) {
    configPath = configPathYaml;
  }

  if (configPath) {
    state.configExists = true;
    try {
      const fileContent = fs.readFileSync(configPath, 'utf8');
      const doc = yaml.load(fileContent) as any;
      if (doc && typeof doc.version === 'number') {
        state.configVersion = doc.version;
      }
    } catch {
      // Ignore reading errors for classification, version remains null
    }
  }

  // 2. Check docs root
  const docsRoot = path.join(projectRoot, 'docs');
  if (fs.existsSync(docsRoot)) {
    state.docsRootExists = true;
  }

  // 3. Scan common directories
  const docsSubdirs = ['features', 'plans', 'reviews', 'adr', 'runbooks', 'intake', 'generated', 'history', 'superpowers'];
  for (const subdir of docsSubdirs) {
    const dirPath = path.join(projectRoot, 'docs', subdir);
    if (fs.existsSync(dirPath)) {
      state.existingDocsDirs.push(`docs/${subdir}`);
    }
  }

  // 4. Detect Agent files
  const agentFilesToCheck = [
    'AGENTS.md',
    'CLAUDE.md',
    '.github/copilot-instructions.md',
    '.codex/instructions.md',
    '.cursor/rules/repo-memory.mdc',
    '.windsurf/rules/repo-memory.md',
    '.kiro/steering/repo-memory.md',
  ];
  for (const file of agentFilesToCheck) {
    if (fs.existsSync(path.join(projectRoot, file))) {
      state.existingAgentFiles.push(file);
    }
  }
  // Check if directories .cursor/rules, .windsurf/rules, etc. exist as custom conventions
  const dirAgentCheck = [
    { dir: '.cursor/rules', name: 'Cursor Rules Dir' },
    { dir: '.windsurf/rules', name: 'Windsurf Rules Dir' },
    { dir: '.kiro/steering', name: 'Kiro Steering Dir' },
    { dir: '.kiro/specs', name: 'Kiro Specs Dir' },
  ];
  for (const item of dirAgentCheck) {
    if (fs.existsSync(path.join(projectRoot, item.dir))) {
      state.customConventions.push(item.name);
    }
  }

  // 5. Detect Plans directories
  const plansToCheck = [
    'docs/plans',
    'plans',
    'docs/superpowers/plans',
  ];
  for (const p of plansToCheck) {
    if (fs.existsSync(path.join(projectRoot, p))) {
      state.existingPlansDirs.push(p);
    }
  }

  // 6. Detect Reviews directories
  const reviewsToCheck = [
    'docs/reviews',
    'reviews',
    'docs/ai-reviews',
  ];
  for (const r of reviewsToCheck) {
    if (fs.existsSync(path.join(projectRoot, r))) {
      state.existingReviewsDirs.push(r);
    }
  }

  // 7. Detect V2 central files
  const v2FilesToCheck = [
    'docs/feature-registry.md',
    'docs/doc-health.md',
    'docs/implementation-log.md',
  ];
  for (const vf of v2FilesToCheck) {
    if (fs.existsSync(path.join(projectRoot, vf))) {
      state.v2CentralFiles.push(vf);
    }
  }

  // 8. Detect Monorepo indicators
  const monorepoFiles = [
    'pnpm-workspace.yaml',
    'turbo.json',
    'nx.json',
    'lerna.json',
    'rush.json',
  ];
  for (const mf of monorepoFiles) {
    if (fs.existsSync(path.join(projectRoot, mf))) {
      state.monorepoIndicators.push(mf);
    }
  }
  // Check for common packages/apps folders
  if (fs.existsSync(path.join(projectRoot, 'packages')) && fs.statSync(path.join(projectRoot, 'packages')).isDirectory()) {
    state.monorepoIndicators.push('packages/');
  }
  if (fs.existsSync(path.join(projectRoot, 'apps')) && fs.statSync(path.join(projectRoot, 'apps')).isDirectory()) {
    state.monorepoIndicators.push('apps/');
  }

  // 9. Classify Version
  const hasV3Modes = fs.existsSync(path.join(projectRoot, 'skills/repo-memory/modes'));
  const hasSkillDir = fs.existsSync(path.join(projectRoot, 'skills/repo-memory'));
  const hasSkillFile = fs.existsSync(path.join(projectRoot, 'skills/repo-memory/SKILL.md'));

  if (state.configExists && state.configVersion === 3) {
    state.repoMemoryVersion = 'v3-style';
  } else if (hasV3Modes) {
    state.repoMemoryVersion = 'v3-style';
  } else if (hasSkillDir || hasSkillFile || state.v2CentralFiles.length > 0) {
    state.repoMemoryVersion = 'v2-style';
  } else {
    state.repoMemoryVersion = 'absent';
  }

  // 10. Detect Conflicts
  // E.g., multiple conflicting agent instructions, or plans/reviews folders in duplicate locations
  if (state.existingPlansDirs.length > 1) {
    state.conflicts.push(`Multiple plans directories detected: ${state.existingPlansDirs.join(', ')}`);
  }
  if (state.existingReviewsDirs.length > 1) {
    state.conflicts.push(`Multiple reviews directories detected: ${state.existingReviewsDirs.join(', ')}`);
  }
  if (state.v2CentralFiles.length > 0 && state.repoMemoryVersion === 'v3-style') {
    state.conflicts.push(`Legacy v2 files detected alongside v3 installation: ${state.v2CentralFiles.join(', ')}`);
  }

  return state;
}
