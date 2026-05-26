import { z } from 'zod';

export const PLAN_STATUSES = [
  'draft',
  'active',
  'implemented',
  'superseded',
  'abandoned',
] as const;

/**
 * Zod schema for YAML frontmatter in docs/plans/*.md files.
 *
 * Plans are working implementation-intent documents. They live in the configured
 * plans path and are classified as working docs, not canonical truth.
 *
 * Required fields: id, title, status, doc_type
 */
export const planSchema = z.object({
  id: z.string().min(1, 'Plan id is required'),
  title: z.string().min(1, 'Plan title is required'),
  status: z.enum(PLAN_STATUSES, {
    errorMap: () => ({
      message: `status must be one of: ${PLAN_STATUSES.join(', ')}`,
    }),
  }),
  doc_type: z.literal('plan', {
    errorMap: () => ({ message: 'doc_type must be "plan"' }),
  }),

  // Optional fields
  /** Which feature or capability this plan serves */
  feature: z.string().optional(),
  /** Team, agent, or person responsible for this plan */
  owner: z.string().optional(),
  /** Confidence level of the current plan content */
  confidence: z.enum(['high', 'medium', 'low']).optional(),
  /** ISO date string of last material edit */
  last_updated: z.string().optional(),
  /** Brief summary of the plan's intent */
  summary: z.string().optional(),
});

export type PlanFrontmatter = z.infer<typeof planSchema>;
