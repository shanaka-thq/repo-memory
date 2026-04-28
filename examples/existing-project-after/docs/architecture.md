# Architecture

Status: current
Doc Type: baseline
Owner: maintainers
Last Verified: 2026-04-28
Confidence: medium

## Overview

The app uses a web client, an HTTP API, and a relational database.

```mermaid
%%{init: {
  "theme": "base",
  "themeVariables": {
    "background": "#fffdf8",
    "primaryColor": "#1f6feb",
    "primaryTextColor": "#0b1220",
    "primaryBorderColor": "#174ea6",
    "lineColor": "#475467",
    "secondaryColor": "#e8f1ff",
    "tertiaryColor": "#f6f8fb",
    "fontFamily": "system-ui, sans-serif"
  }
}}%%
flowchart LR
  User["User"] --> Web["Web UI"]
  Web --> Api["HTTP API"]
  Api --> Db["Database"]
```

## Boundaries

- Web UI owns presentation and client-side validation.
- API owns authorization, persistence, and business rules.
- Database stores users, issues, labels, and status history.

## Open Questions

- Background job processing is not documented in this example.
