import { z } from 'zod';

export const pathsSchema = z.object({
  ownership_map: z.string(),
  project_overview: z.string(),
  architecture: z.string(),
  features: z.string(),
  plans: z.string(),
  reviews: z.string(),
  generated: z.string(),
  intake: z.string(),
  adr: z.string(),
  history: z.string(),
  runbooks: z.string(),
});

export const generatedSchema = z.object({
  header: z.string(),
  feature_registry: z.string(),
  next_work_queue: z.string(),
  doc_health: z.string(),
});

export const prioritySchema = z.object({
  lower_number_is_higher: z.boolean(),
});

export const compatibilitySchema = z.object({
  preserve_existing_agent_files: z.boolean(),
  use_managed_blocks: z.boolean(),
  allow_external_paths: z.boolean(),
  map_existing_plan_dirs: z.boolean(),
  map_existing_review_dirs: z.boolean(),
});

export const externalSourcesSchema = z.object({
  docs: z.array(z.string()),
  plans: z.array(z.string()),
  reviews: z.array(z.string()),
});

export const capabilitySchema = z.object({
  owner: z.string(),
  type: z.enum(['local', 'generated', 'external']),
});

export const ownershipSchema = z.object({
  capabilities: z.record(z.string(), capabilitySchema),
});

export const adaptersSchema = z.object({
  installed: z.array(z.string()),
  available: z.array(z.string()),
});

export const validationSchema = z.object({
  allow_manual_central_registry: z.boolean(),
  require_feature_frontmatter: z.boolean(),
  require_plan_frontmatter: z.boolean(),
  require_review_frontmatter: z.boolean(),
  require_evidence_for_inferred_claims: z.boolean(),
  warn_on_unmapped_plan_dirs: z.boolean(),
  warn_on_unmapped_review_dirs: z.boolean(),
  fail_on_generated_file_manual_edit: z.boolean(),
});

export const configSchema = z.object({
  version: z.literal(3),
  mode: z.enum(['standard', 'lite', 'full']),
  docs_root: z.string(),
  paths: pathsSchema,
  generated: generatedSchema,
  priority: prioritySchema,
  compatibility: compatibilitySchema,
  external_sources: externalSourcesSchema,
  ownership: ownershipSchema,
  adapters: adaptersSchema,
  validation: validationSchema,
});

export type RepoMemoryConfig = z.infer<typeof configSchema>;
