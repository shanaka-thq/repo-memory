# Reviewer Mode

Use this mode when requested to review a codebase, architecture, feature, security posture, performance, accessibility, or AI-generated code.

## Instructions

1. **Target paths:** Save reviews in the appropriate subdirectory under the configured reviews path (default: `docs/reviews/`):
   - `docs/reviews/codebase/YYYY-MM-DD-<slug>.md`
   - `docs/reviews/architecture/YYYY-MM-DD-<slug>.md`
   - `docs/reviews/security/YYYY-MM-DD-<slug>.md`
   - `docs/reviews/performance/YYYY-MM-DD-<slug>.md`
   - `docs/reviews/accessibility/YYYY-MM-DD-<slug>.md`
   - `docs/reviews/ai/YYYY-MM-DD-<slug>.md`
2. **Reviews are evidence only:** Treat reviews as assessment records. They represent analysis at a point in time, not canonical truth.
3. **Categorize findings:** Classify issues by severity (Critical, High, Medium, Low) and confidence (High, Medium, Low).
4. **Link evidence:** Every finding must cite explicit supporting evidence (source file/line, behavior, log, or specification).
5. **Durable promotion:** Accepted findings must be converted into plans, issues, feature document updates, or ADRs. Do not directly rewrite canonical documents solely from a review report.
