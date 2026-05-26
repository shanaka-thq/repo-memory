#!/usr/bin/env node

import { readFileSync } from 'fs';
import { join } from 'path';
import { Command } from 'commander';
import { runDoctorCommand } from '../commands/doctor';
import { runValidateCommand } from '../commands/validate';
import { runGenerateCommand } from '../commands/generate';

const pkg = JSON.parse(readFileSync(join(__dirname, '../../package.json'), 'utf8'));

const program = new Command();

program
  .name('repo-memory')
  .description('Repo Memory v3 CLI support engine for AI-assisted software teams.')
  .version(pkg.version);

// doctor command
program
  .command('doctor')
  .description('Detect repo state and suggest next actions')
  .option('--json', 'Output results in JSON format')
  .action((options) => {
    runDoctorCommand(options);
  });

// Stubs for other commands to be implemented in subsequent phases
program
  .command('init')
  .description('Initialize Repo Memory in a new or clean repository')
  .option('--lite', 'Lite installation')
  .option('--full', 'Full installation')
  .option('--agent <type>', 'Configure for specific agent (generic, claude-code, etc.)')
  .option('--dry-run', 'Show actions without writing them')
  .option('--force', 'Force initialization')
  .action(() => {
    console.log('Command "init" is not implemented in Milestone 1.');
  });

program
  .command('adopt')
  .description('Adopt Repo Memory in an existing repository with custom docs')
  .option('--dry-run', 'Show actions without writing them')
  .option('--write', 'Perform the adoption write operations')
  .option('--agent <type>', 'Configure agent instructions')
  .option('--map-existing', 'Automatically map existing directories')
  .action(() => {
    console.log('Command "adopt" is not implemented in Milestone 1.');
  });

program
  .command('migrate <type>')
  .description('Migrate an older Repo Memory installation (e.g. v2-to-v3)')
  .option('--dry-run', 'Show migration actions without writing')
  .option('--backup', 'Create backup of legacy files before migrating')
  .option('--write', 'Perform write operations')
  .option('--force', 'Force migration execution')
  .action((type) => {
    console.log(`Command "migrate" for type "${type}" is not implemented in Milestone 1.`);
  });

program
  .command('map <capability> <path>')
  .description('Map an existing path for a capability in the configuration')
  .action((capability, path) => {
    console.log(`Command "map" for capability "${capability}" to path "${path}" is not implemented in Milestone 1.`);
  });

program
  .command('validate')
  .description('Validate Repo Memory files and project health')
  .option('--json', 'Output results in JSON format')
  .action((options) => {
    runValidateCommand(options);
  });

program
  .command('generate')
  .description('Generate derived indexes (feature registry, next work queue, doc health)')
  .option('--dry-run', 'Show what would be written without writing', false)
  .option('--json', 'Output results in JSON format')
  .action((options) => {
    runGenerateCommand({ ...options, dryRun: options.dryRun });
  });

program
  .command('audit')
  .description('Deep audit of Repo Memory structure and drift detection')
  .option('--write', 'Write results to doc-health file')
  .option('--json', 'Output results in JSON format')
  .action(() => {
    console.log('Command "audit" is not implemented in Milestone 1.');
  });

program
  .command('install-adapter <agent>')
  .description('Install or update thin adapter files for coding agents')
  .option('--dry-run', 'Show install actions without writing')
  .option('--append', 'Append instructions to existing file')
  .option('--force', 'Force overwrite existing files')
  .option('--print', 'Print instruction block to stdout')
  .action((agent) => {
    console.log(`Command "install-adapter" for agent "${agent}" is not implemented in Milestone 1.`);
  });

program.parse(process.argv);
