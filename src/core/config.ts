import * as fs from 'fs';
import * as path from 'path';
import * as yaml from 'js-yaml';
import { configSchema, RepoMemoryConfig } from '../schemas/config.schema';

/**
 * Validates a configuration object against the Zod schema.
 * Throws an error with descriptive details if validation fails.
 */
export function validateConfig(configData: unknown): RepoMemoryConfig {
  const result = configSchema.safeParse(configData);
  if (!result.success) {
    const errorDetails = result.error.errors
      .map((err) => `${err.path.join('.')}: ${err.message}`)
      .join('\n');
    throw new Error(`Configuration validation failed:\n${errorDetails}`);
  }
  return result.data;
}

/**
 * Attempts to locate and load the repo-memory.config.yml configuration file from the project root.
 * Returns null if the file does not exist.
 * Throws an error if the file exists but fails parsing or schema validation.
 */
export function loadConfig(projectRoot: string): RepoMemoryConfig | null {
  const possiblePaths = [
    path.join(projectRoot, 'repo-memory.config.yml'),
    path.join(projectRoot, 'repo-memory.config.yaml'),
  ];

  for (const configPath of possiblePaths) {
    if (fs.existsSync(configPath)) {
      try {
        const fileContent = fs.readFileSync(configPath, 'utf8');
        const parsed = yaml.load(fileContent);
        return validateConfig(parsed);
      } catch (err: any) {
        throw new Error(`Error reading/parsing config file at ${configPath}: ${err.message}`);
      }
    }
  }

  return null;
}
