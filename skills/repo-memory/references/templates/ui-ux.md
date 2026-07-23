## UI and UX Index Template

```md
# UI and UX

Use this folder for user journeys, screen or surface behavior, interaction rules, accessibility notes, and responsive requirements that should stay aligned with implementation.

| Topic                          | Purpose                                                                   | Owner doc                                       |
| ------------------------------ | ------------------------------------------------------------------------- | ----------------------------------------------- |
| `search-results-experience.md` | Defines search result states, ranking presentation, and keyboard behavior | `../requirements/user-stories-and-use-cases.md` |
| `settings-flow.md`             | Documents the settings journey and permissions-related states             | `../features/settings.md`                       |
```

## UI and UX Doc Template

```md
# UI and UX: search-results-experience

Owner doc: `../features/answer-search-improvements.md`
Last updated: 2026-04-23

## User Goal

Describe what the user is trying to achieve.

## Surfaces

- Page, panel, modal, or component involved

## Main Flow

Describe the expected interaction flow.

## States

- Empty
- Loading
- Success
- Error
- Permission denied

## Interaction Rules

- Keyboard behavior
- Focus behavior
- Selection behavior

## Accessibility

- Screen reader requirements
- Contrast or semantics notes

## Responsive Behavior

- Mobile behavior
- Desktop behavior

## Related Code

- `src/...`
- `ui/...`

## Related Docs

- `../requirements/user-stories-and-use-cases.md`
- `../features/answer-search-improvements.md`
- `../diagrams/README.md`
```
