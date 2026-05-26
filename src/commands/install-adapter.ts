import * as fs from 'fs';
import * as path from 'path';
import { findProjectRoot } from '../core/paths';
import {
  isSupportedAdapter,
  ADAPTER_DEFINITIONS,
  SUPPORTED_ADAPTERS,
  upsertManagedBlock,
  wrapInManagedBlock,
  MANAGED_BLOCK_START,
} from '../adapters/content';

export interface InstallAdapterOptions {
  projectRoot?: string;
  dryRun?: boolean;
  append?: boolean;
  force?: boolean;
  print?: boolean;
}

export interface InstallAdapterResult {
  agent: string;
  targetFile: string;
  action: 'written' | 'appended' | 'skipped' | 'printed' | 'dry-run';
  message: string;
}

/**
 * Core install logic. Returns a result describing what happened (or would happen).
 * Does not write to disk; callers handle writing based on dryRun.
 */
export function installAdapter(
  agent: string,
  projectRoot: string,
  options: InstallAdapterOptions
): InstallAdapterResult {
  if (!isSupportedAdapter(agent)) {
    return {
      agent,
      targetFile: '',
      action: 'skipped',
      message: `Unknown agent "${agent}". Supported: ${SUPPORTED_ADAPTERS.join(', ')}`,
    };
  }

  const def = ADAPTER_DEFINITIONS[agent];
  const targetPath = path.resolve(projectRoot, def.targetFile);
  const content = def.content;

  // --print: just output the content, no file operations
  if (options.print) {
    return {
      agent,
      targetFile: def.targetFile,
      action: 'printed',
      message: content,
    };
  }

  const exists = fs.existsSync(targetPath);

  // --append: insert/update a managed block in the existing file
  if (options.append) {
    if (options.dryRun) {
      const verb = exists ? 'upsert managed block in' : 'create with managed block';
      return {
        agent,
        targetFile: def.targetFile,
        action: 'dry-run',
        message: `Would ${verb} ${def.targetFile}`,
      };
    }

    fs.mkdirSync(path.dirname(targetPath), { recursive: true });

    if (exists) {
      const existing = fs.readFileSync(targetPath, 'utf8');
      const updated = upsertManagedBlock(existing, content);
      fs.writeFileSync(targetPath, updated, 'utf8');
      const hadBlock = existing.includes(MANAGED_BLOCK_START);
      return {
        agent,
        targetFile: def.targetFile,
        action: 'appended',
        message: hadBlock
          ? `Updated managed block in ${def.targetFile}`
          : `Appended managed block to ${def.targetFile}`,
      };
    } else {
      fs.writeFileSync(targetPath, wrapInManagedBlock(content), 'utf8');
      return {
        agent,
        targetFile: def.targetFile,
        action: 'appended',
        message: `Created ${def.targetFile} with managed block`,
      };
    }
  }

  // Default mode: write full file
  if (exists && !options.force) {
    return {
      agent,
      targetFile: def.targetFile,
      action: 'skipped',
      message: `${def.targetFile} already exists. Use --force to overwrite or --append for a managed block.`,
    };
  }

  if (options.dryRun) {
    return {
      agent,
      targetFile: def.targetFile,
      action: 'dry-run',
      message: `Would write ${def.targetFile}`,
    };
  }

  fs.mkdirSync(path.dirname(targetPath), { recursive: true });
  fs.writeFileSync(targetPath, content, 'utf8');
  return {
    agent,
    targetFile: def.targetFile,
    action: 'written',
    message: `Written: ${def.targetFile}`,
  };
}

/**
 * CLI entry point for install-adapter.
 * Handles --print specially: outputs content to stdout without any wrapper.
 */
export function runInstallAdapterCommand(
  agent: string,
  options: InstallAdapterOptions
): void {
  const projectRoot = options.projectRoot ?? findProjectRoot();
  const result = installAdapter(agent, projectRoot, options);

  if (options.print) {
    // Print the raw adapter content with no decoration
    process.stdout.write(result.message);
    return;
  }

  if (result.action === 'skipped') {
    console.error(`[ERROR] ${result.message}`);
    process.exit(1);
  }

  console.log(result.message);
}
