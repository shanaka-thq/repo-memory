import { z } from 'zod';

export const REVIEW_STATUSES = ['draft', 'active', 'superseded'] as const;

export const REVIEW_TYPES = [
  'codebase',
  'architecture',
  'security',
  'performance',
  'accessibility',
  'ai',
] as const;

export const REVIEW_DISPOSITIONS = [
  'accepted',
  'rejected',
  'partial',
  'pending',
] as const;

/**
 * Zod schema for YAML frontmatter in docs/reviews/*.md files.
 *
 * Reviews are evidence documents: specialist, second-agent, tool-generated, or
 * human review records that need provenance and disposition tracking.
 *
 * Required fields: id, title, status, doc_type
 */
export const reviewSchema = z.object({
  id: z.string().min(1, 'Review id is required'),
  title: z.string().min(1, 'Review title is required'),
  status: z.enum(REVIEW_STATUSES, {
    errorMap: () => ({
      message: `status must be one of: ${REVIEW_STATUSES.join(', ')}`,
    }),
  }),
  doc_type: z.literal('review', {
    errorMap: () => ({ message: 'doc_type must be "review"' }),
  }),

  // Optional fields
  /** Category of the review */
  review_type: z.enum(REVIEW_TYPES).optional(),
  /** What or who was reviewed (file path, feature slug, or description) */
  subject: z.string().optional(),
  /** Who or what produced this review */
  reviewer: z.string().optional(),
  /** Final disposition of this review's findings */
  disposition: z.enum(REVIEW_DISPOSITIONS).optional(),
  /** ISO date string of last material edit */
  last_updated: z.string().optional(),
  /** Confidence level of the review findings */
  confidence: z.enum(['high', 'medium', 'low']).optional(),
});

export type ReviewFrontmatter = z.infer<typeof reviewSchema>;
