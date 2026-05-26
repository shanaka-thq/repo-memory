import { discoverRepoState } from '../core/discovery';
import { findProjectRoot } from '../core/paths';

export interface DoctorOptions {
  json?: boolean;
  projectRoot?: string;
}

export function runDoctorCommand(options: DoctorOptions): void {
  const projectRoot = options.projectRoot ?? findProjectRoot();
  const state = discoverRepoState(projectRoot);

  if (options.json) {
    console.log(JSON.stringify(state, null, 2));
    return;
  }

  console.log('Repo Memory Doctor');
  console.log('==================');
  console.log('Detected:');
  console.log(`- Repo Memory: ${state.repoMemoryVersion} installation`);
  console.log(`- Config file: ${state.configExists ? 'present' : 'missing'}`);
  if (state.configExists && state.configVersion) {
    console.log(`  - Config version: ${state.configVersion}`);
  }

  // Feature registry and doc health presence
  const featureRegistryFile = state.v2CentralFiles.find(f => f.endsWith('feature-registry.md'));
  const docHealthFile = state.v2CentralFiles.find(f => f.endsWith('doc-health.md'));

  console.log(`- Feature registry: ${featureRegistryFile ? 'manual central file found' : 'none detected or generated only'}`);
  console.log(`- Doc health: ${docHealthFile ? 'manual central file found' : 'none detected or generated only'}`);

  console.log(`- Agent files: ${state.existingAgentFiles.length > 0 ? state.existingAgentFiles.join(', ') : 'none detected'}`);

  // Plans and Reviews
  if (state.existingPlansDirs.length > 0) {
    console.log(`- Plans directories: ${state.existingPlansDirs.join(', ')}`);
  } else {
    console.log('- Plans directory: none detected');
  }

  if (state.existingReviewsDirs.length > 0) {
    console.log(`- Reviews directories: ${state.existingReviewsDirs.join(', ')}`);
  } else {
    console.log('- Reviews directory: none detected');
  }

  if (state.monorepoIndicators.length > 0) {
    console.log(`- Monorepo indicators: ${state.monorepoIndicators.join(', ')}`);
  }

  if (state.conflicts.length > 0) {
    console.log('\nConflicts/Warnings:');
    for (const conflict of state.conflicts) {
      console.log(`[!] ${conflict}`);
    }
  }

  console.log('\nRecommended:');
  const recommendations: string[] = [];

  if (state.repoMemoryVersion === 'v2-style') {
    recommendations.push('- Run: npx repo-memory migrate v2-to-v3 --dry-run');
  } else if (state.repoMemoryVersion === 'absent') {
    recommendations.push('- Run: npx repo-memory init --lite --agent generic');
    recommendations.push('  Or to adopt an existing docs setup: npx repo-memory adopt --dry-run');
  } else if (state.repoMemoryVersion === 'v3-style') {
    recommendations.push('- Everything looks aligned to v3.');
    recommendations.push('  Run: npx repo-memory validate');
  }

  // Check if non-standard plans or reviews directories exist and config maps them
  const hasSuperpowersPlans = state.existingPlansDirs.includes('docs/superpowers/plans');
  const hasStandardPlans = state.existingPlansDirs.includes('docs/plans');
  if (hasSuperpowersPlans && !hasStandardPlans && state.repoMemoryVersion === 'v2-style') {
    recommendations.push('- Then: npx repo-memory map plans docs/superpowers/plans');
  }

  for (const rec of recommendations) {
    console.log(rec);
  }
}
