# Skills Repository Structures and Manifest Formats

## Common Repository Structures

### 1. **Matt Pocock / Skills** Structure
```
mattpocock/skills/
├── skills/
│   ├── engineering/
│   │   ├── ask-matt/
│   │   │   └── SKILL.md
│   │   ├── code-review/
│   │   │   └── SKILL.md
│   │   ├── grill-with-docs/
│   │   │   └── SKILL.md
│   │   └── ...
│   ├── productivity/
│   │   ├── grill-me/
│   │   │   └── SKILL.md
│   │   ├── handoff/
│   │   │   └── SKILL.md
│   │   └── ...
│   └── writing/
│       ├── writing-beats/
│       │   └── SKILL.md
│       └── ...
├── .agents/
│   └── adr/                    # Architectural Decision Records
├── .claude-plugin/
│   ├── marketplace.json
│   └── plugin.json
├── .changeset/                # Version management
├── docs/                      # Documentation
├── scripts/                   # Helper scripts
├── AGENTS.md                  # Agent instructions
├── CLAUDE.md                  # Claude-specific instructions
├── CONTEXT.md                 # Domain context template
├── package.json
└── README.md
```

### 2. **Vercel Labs / Agent-Skills** Structure
```
vercel-labs/agent-skills/
├── skills/
│   ├── vercel-optimize/
│   │   ├── SKILL.md
│   │   └── scripts/           # Optional helper scripts
│   ├── react-best-practices/
│   │   └── SKILL.md
│   ├── web-design-guidelines/
│   │   └── SKILL.md
│   └── ...
├── .github/workflows/
├── packages/                  # Shared packages
├── skills.sh.json            # Skills.sh manifest
├── AGENTS.md
├── CLAUDE.md
└── README.md
```

### 3. **Microsoft / Azure-Skills** Structure
```
microsoft/azure-skills/
├── .github/plugins/azure-skills/
│   └── skills/               # Azure skill definitions
├── skills/                   # Main skills directory
│   ├── azure-prepare/
│   │   └── SKILL.md
│   ├── azure-validate/
│   │   └── SKILL.md
│   └── ...
├── .claude-plugin/
├── .cursor-plugin/
├── hooks/                    # Lifecycle hooks
├── landing-page/            # Documentation site (Astro)
├── .mcp.json                # MCP server configuration
├── apm.yml                  # APM configuration
├── gemini-extension.json
├── plugin.json
└── README.md
```

### 4. **Anthropics / Skills** Structure
```
anthropics/skills/
├── skills/
│   ├── creative-design/
│   │   └── ...
│   ├── development-technical/
│   │   └── ...
│   ├── enterprise-communication/
│   │   └── ...
│   ├── docx/                # Document skills (source-available)
│   │   └── SKILL.md
│   ├── pdf/
│   │   └── SKILL.md
│   ├── pptx/
│   │   └── SKILL.md
│   └── xlsx/
│       └── SKILL.md
├── .claude-plugin/
├── spec/                    # Agent Skills specification
├── template/               # Skill template
├── THIRD_PARTY_NOTICES.md
└── README.md
```

### 5. **Obra / Superpowers** Structure
```
obra/superpowers/
├── skills/
│   ├── brainstorming/
│   │   └── SKILL.md
│   ├── writing-plans/
│   │   └── SKILL.md
│   ├── executing-plans/
│   │   └── SKILL.md
│   └── ...
├── .agents/plugins/
├── .claude-plugin/
├── .codex-plugin/
├── .cursor-plugin/
├── .kimi-plugin/
├── .opencode/
├── .pi/extensions/
├── assets/                  # Images and assets
├── docs/                    # Documentation
├── hooks/                   # Session hooks
├── scripts/                 # Helper scripts
├── tests/                   # Test files
├── AGENTS.md
├── CLAUDE.md
├── GEMINI.md
├── gemini-extension.json
└── README.md
```

## Manifest File Formats

### 1. **SKILL.md Format (Standard)**
```yaml
---
name: skill-name              # Required: lowercase, hyphens for spaces
description: What this skill does and when to use it  # Required
# Optional fields:
metadata:
  internal: true             # Hide from discovery (INSTALL_INTERNAL_SKILLS=1)
allowed-tools: []            # Restrict tool usage
context: fork               # Agent-specific context handling
hooks:                      # Lifecycle hooks
  session-start: |
    # Code to run at session start
---

# Skill Title

## When to Use
Describe scenarios where this skill should be used.

## Steps
1. First step
2. Second step

## Examples
- Example usage 1
- Example usage 2

## Guidelines
- Guideline 1
- Guideline 2
```

### 2. **skills.sh.json Manifest**
```json
{
  "name": "repository-name",
  "description": "Repository description",
  "skills": [
    {
      "name": "skill-name",
      "path": "skills/skill-name/SKILL.md",
      "description": "Skill description"
    }
  ],
  "topics": ["react", "nextjs", "design"],
  "agents": ["claude-code", "cursor", "codex"],
  "license": "MIT"
}
```

### 3. **Claude Plugin Configuration (.claude-plugin/)**
**marketplace.json**:
```json
{
  "metadata": {
    "pluginRoot": "./plugins"
  },
  "plugins": [
    {
      "name": "plugin-name",
      "source": "plugin-source",
      "skills": ["./skills/skill1", "./skills/skill2"]
    }
  ]
}
```

**plugin.json**:
```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Plugin description",
  "author": "Author Name",
  "skills": [
    {
      "name": "skill-name",
      "path": "skills/skill-name/SKILL.md"
    }
  ],
  "hooks": {
    "session-start": "echo 'Session starting'"
  }
}
```

### 4. **APM Configuration (apm.yml)**
```yaml
name: azure-skills
version: 1.0.0
description: Azure skills plugin
author: Microsoft
agents:
  claude-code:
    skills:
      - path: .github/plugins/azure-skills/skills
  cursor:
    skills:
      - path: .github/plugins/azure-skills/skills
  codex:
    skills:
      - path: .github/plugins/azure-skills/skills
mcp:
  - name: azure
    command: npx @azure/mcp-server
    args: []
  - name: foundry
    command: npx @microsoft/foundry-mcp-server
    args: []
```

### 5. **MCP Configuration (.mcp.json)**
```json
{
  "mcpServers": {
    "azure": {
      "command": "npx",
      "args": ["@azure/mcp-server"],
      "env": {
        "AZURE_TENANT_ID": "${AZURE_TENANT_ID}",
        "AZURE_CLIENT_ID": "${AZURE_CLIENT_ID}"
      }
    },
    "foundry": {
      "command": "npx",
      "args": ["@microsoft/foundry-mcp-server"]
    }
  }
}
```

## Agent-Specific Configuration Files

### 1. **AGENTS.md**
Common across most repositories:
- Lists all available skills
- Provides installation instructions for different agents
- Agent compatibility matrix
- Usage examples

### 2. **CLAUDE.md**
Claude-specific instructions:
- How to load skills in Claude Code
- Plugin installation instructions
- Claude.ai integration notes

### 3. **Agent-Specific Files**
- `GEMINI.md` - Gemini/Antigravity instructions
- `.opencode/` - OpenCode configuration
- `.pi/extensions/` - Pi agent extensions
- `.kimi-plugin/` - Kimi Code configuration

## Skill Discovery Patterns

### 1. **Standard Discovery Locations**
The skills.sh CLI searches for skills in:
- Root directory (if contains `SKILL.md`)
- `skills/` directory
- `skills/.curated/`, `skills/.experimental/`, `skills/.system/`
- Agent-specific directories (`.claude/skills/`, `.agents/skills/`, etc.)
- Paths declared in plugin manifests

### 2. **Catalog Layouts**
- **Flat layout**: `skills/<name>/SKILL.md` (most common)
- **Categorized layout**: `skills/<category>/<name>/SKILL.md`
- **Shadowing**: SKILL.md at shallower level shadows nested ones
- **Full depth search**: `--full-depth` flag for non-standard locations

### 3. **Internal Skills**
```yaml
metadata:
  internal: true
```
- Hidden from normal discovery
- Visible with `INSTALL_INTERNAL_SKILLS=1`
- Useful for WIP skills or internal tooling

## Installation Paths by Agent

### Common Installation Locations:
- **Claude Code**: `~/.claude/skills/` (global), `./.claude/skills/` (project)
- **Codex**: `~/.codex/skills/` (global), `./.agents/skills/` (project)
- **Cursor**: `~/.cursor/skills/` (global), `./.agents/skills/` (project)
- **GitHub Copilot**: `~/.copilot/skills/` (global), `./.agents/skills/` (project)
- **Kiro CLI**: `~/.kiro/skills/` (global), `./.kiro/skills/` (project)
- **OpenCode**: `~/.config/opencode/skills/` (global), `./.agents/skills/` (project)

### Installation Methods:
1. **Symlink** (recommended): Single source of truth, easy updates
2. **Copy**: Independent copies, use when symlinks not supported
3. **Plugin**: Managed bundle with automatic updates

## Best Practices Observed

### 1. **Skill Organization**
- Group related skills into categories
- Use consistent naming (kebab-case)
- Include clear "When to Use" sections
- Provide concrete examples

### 2. **Repository Structure**
- Separate skill definitions from plugin configuration
- Include documentation and examples
- Provide agent-specific installation guides
- Include validation scripts

### 3. **Multi-Agent Support**
- Create agent-specific configuration files
- Test across all supported agents
- Handle agent-specific features gracefully
- Provide fallback options

### 4. **Version Management**
- Use semantic versioning
- Include changelogs (CHANGELOG.md)
- Use release automation (.changeset/)
- Tag releases on GitHub

### 5. **Documentation**
- Clear README with quickstart
- Agent-specific installation guides
- Skill usage examples
- Troubleshooting sections

## Skills.sh Ecosystem Integration

### For Repository Owners:
1. **Register on skills.sh**: Appear in search and leaderboards
2. **Add skills.sh.json**: Optional manifest for better discovery
3. **Use telemetry**: Anonymous usage tracking for leaderboard ranking
4. **Tag skills**: Use relevant topics for categorization

### For Skill Consumers:
1. **Browse skills.sh**: Discover skills by topic or popularity
2. **Use skills CLI**: `npx skills add <owner/repo>`
3. **Check compatibility**: Verify agent support before installing
4. **Update regularly**: `npx skills update` to get latest versions

### For Agent Developers:
1. **Follow Agent Skills spec**: agentskills.io
2. **Support standard paths**: `~/.<agent>/skills/` and `./.<agent>/skills/`
3. **Implement skill discovery**: Auto-load skills from standard locations
4. **Provide hooks**: Session lifecycle hooks for skill initialization