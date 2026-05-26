import { z } from 'zod';

export const FEATURE_STATUSES = [
  'research',
  'planned',
  'in_progress',
  'blocked',
  'implemented',
  'verified',
  'shipped',
  'abandoned',
  'superseded',
  'deprecated',
  'rolled_back',
] as const;

export const READY_VALUES = ['ready', 'verify-first', 'needs-human', 'blocked'] as const;
export const CONFIDENCE_VALUES = ['high', 'medium', 'low'] as const;

/**
 * Zod schema for YAML frontmatter in docs/features/*.md files.
 *
 * Required fields (always validated when require_feature_frontmatter is true):
 *   id, title, status, doc_type, ready, next_safe_step
 *
 * Optional fields add metadata for richer generation and audit.
 */
export const featureSchema = z.object({
  /** Slug identifier — must match the file name without .md */
  id: z.string().min(1, 'Feature id is required'),
  /** Human-readable title */
  title: z.string().min(1, 'Feature title is required'),
  /** Lifecycle status — must be one of the allowed values */
  status: z.enum(FEATURE_STATUSES, {
    errorMap: () => ({
      message: `status must be one of: ${FEATURE_STATUSES.join(', ')}`,
    }),
  }),
  /** Document type — must be "feature" */
  doc_type: z.literal('feature', {
    errorMap: () => ({ message: 'doc_type must be "feature"' }),
  }),
  /** Readiness for the next agent to pick up */
  ready: z.enum(READY_VALUES, {
    errorMap: () => ({
      message: `ready must be one of: ${READY_VALUES.join(', ')}`,
    }),
  }),
  /** What the next agent should do first */
  next_safe_step: z.string().min(1, 'next_safe_step is required'),

  // --- Optional fields ---
  /** Numeric priority (lower = higher priority when lower_number_is_higher is true) */
  priority: z.number().optional(),
  /** Team or agent responsible */
  owner: z.string().optional(),
  /** Path to this feature document */
  canonical_doc: z.string().optional(),
  /** Feature IDs or work items blocking this feature */
  blocked_by: z.array(z.string()).optional(),
  /** Evidence supporting the current status */
  evidence: z.string().optional(),
  /** Confidence level for the current state */
  confidence: z.enum(CONFIDENCE_VALUES).optional(),
  /** ISO date string of last material edit */
  last_updated: z.string().optional(),
  /** ISO date string of last evidence-backed verification */
  last_verified: z.string().optional(),
});

export type FeatureFrontmatter = z.infer<typeof featureSchema>;
