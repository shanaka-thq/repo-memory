import * as path from 'path';
import * as fs from 'fs';

/**
 * Finds the project root directory by traversing upwards from the current directory,
 * looking for files that indicate the root of a Git repository or repo-memory project.
 */
export function findProjectRoot(startDir: string = process.cwd()): string {
  let currentDir = startDir;
  while (true) {
    const gitDir = path.join(currentDir, '.git');
    const configYml = path.join(currentDir, 'repo-memory.config.yml');
    const packageJson = path.join(currentDir, 'package.json');

    if (fs.existsSync(gitDir) || fs.existsSync(configYml) || fs.existsSync(packageJson)) {
      return currentDir;
    }

    const parentDir = path.dirname(currentDir);
    if (parentDir === currentDir) {
      // Reached the filesystem root without finding project indicators, default to startDir
      return startDir;
    }
    currentDir = parentDir;
  }
}

/**
 * Resolves a target path. If it's absolute, returns it directly. If it is relative,
 * resolves it relative to the project root.
 */
export function resolvePath(projectRoot: string, targetPath: string): string {
  if (path.isAbsolute(targetPath)) {
    return targetPath;
  }
  return path.resolve(projectRoot, targetPath);
}
