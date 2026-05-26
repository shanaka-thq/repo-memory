import * as path from 'path';
import * as fs from 'fs';

/**
 * Finds the project root directory by traversing upwards from the current directory,
 * looking for files that indicate the root of a Git repository or repo-memory project.
 */
export function findProjectRoot(startDir: string = process.cwd()): string {
  let currentDir = startDir;
  let packageJsonDir: string | null = null;

  while (true) {
    const gitDir = path.join(currentDir, '.git');
    const configYml = path.join(currentDir, 'repo-memory.config.yml');
    const configYaml = path.join(currentDir, 'repo-memory.config.yaml');
    const packageJson = path.join(currentDir, 'package.json');

    // .git or repo-memory config are definitive root indicators — stop immediately
    if (fs.existsSync(gitDir) || fs.existsSync(configYml) || fs.existsSync(configYaml)) {
      return currentDir;
    }

    // package.json is a fallback; record the first (innermost) match and keep walking
    // upward so that in a monorepo we don't stop at a package directory
    if (fs.existsSync(packageJson) && packageJsonDir === null) {
      packageJsonDir = currentDir;
    }

    const parentDir = path.dirname(currentDir);
    if (parentDir === currentDir) {
      // Reached the filesystem root without finding a definitive indicator
      return packageJsonDir ?? startDir;
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
