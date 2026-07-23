# Skills.sh Ecosystem and Popular Agent Skills Repositories Analysis

## Overview of Skills.sh

**skills.sh** is the central registry and CLI tool for the open agent skills ecosystem. It serves as:

- **Registry**: Hosts a directory of ~260+ skills with leaderboards showing activity and install counts
- **CLI tool**: `npx skills add <owner/repo>` installs skills across 70+ supported agents
- **Discovery**: Searchable skill directory with topics, trending skills, and official collections
- **Standardization**: Based on the Agent Skills specification (agentskills.io)

### Key Features of Skills.sh
- **Telemetry**: Anonymous usage tracking for leaderboard rankings (opt-out with `DISABLE_TELEMETRY=1`)
- **Multi-agent support**: 70+ agents including Claude Code, Codex, Cursor, GitHub Copilot, Windsurf, etc.
- **Flexible installation**: Project-scoped (`./<agent>/skills/`) or global (`~/<agent>/skills/`)
- **Skill discovery**: CLI can search across GitHub repositories for SKILL.md files

### Skills.sh CLI Commands
```bash
npx skills add <owner/repo>           # Install skills
npx skills use <owner/repo>           # Use without installing
npx skills list                       # List installed skills
npx skills find [query]              # Search for skills
npx skills remove [skills]           # Remove skills
npx skills update [skills]           # Update to latest versions
npx skills init [name]               # Create new SKILL.md template
```

## Popular Agent Skills Repositories

### 1. **Matt Pocock / Skills** (`mattpocock/skills`)
**GitHub**: https://github.com/mattpocock/skills  
**Skills.sh**: https://skills.sh/mattpocock/skills  
**Stars**: 183k | **Forks**: 15.6k | **Skills**: ~30+

#### Taglines & Positioning
- "Skills For Real Engineers"
- "My agent skills that I use every day to do real engineering - not vibe coding"
- Positioned as practical engineering skills based on decades of experience
- Emphasis on small, composable, hackable skills that work with any model

#### Folder Structure
```
skills/
├── engineering/
│   ├── ask-matt/
│   ├── code-review/
│   ├── grill-with-docs/
│   ├── improve-codebase-architecture/
│   ├── setup-matt-pocock-skills/
│   └── ...
├── productivity/
│   ├── grill-me/
│   ├── handoff/
│   └── ...
└── writing/
    ├── writing-beats/
    └── ...
```

#### Key Skills
- **grill-me** / **grill-with-docs**: Most popular skills for alignment through questioning
- **tdd**: Test-driven development with red-green-refactor loop
- **diagnosing-bugs**: Systematic debugging methodology
- **improve-codebase-architecture**: Codebase analysis and improvement
- **handoff**: Compact conversations for agent continuation
- **domain-modeling**: DDD-style domain modeling and CONTEXT.md creation

#### Manifest/Configuration
- Uses standard `SKILL.md` format with YAML frontmatter
- Includes `.claude-plugin/` for Claude Code plugin integration
- `AGENTS.md` with agent-specific instructions
- `CLAUDE.md` for Claude-specific integration

### 2. **Vercel Labs / Agent-Skills** (`vercel-labs/agent-skills`)
**GitHub**: https://github.com/vercel-labs/agent-skills  
**Skills.sh**: https://skills.sh/vercel-labs/agent-skills  
**Stars**: 29.4k | **Forks**: 2.6k | **Skills**: ~8

#### Taglines & Positioning
- "A collection of skills for AI coding agents"
- Official Vercel engineering best practices
- Focus on React, Next.js, web performance, and Vercel platform optimization

#### Folder Structure
```
skills/
├── vercel-optimize/
├── react-best-practices/
├── web-design-guidelines/
├── writing-guidelines/
├── react-native-guidelines/
├── react-view-transitions/
├── composition-patterns/
└── vercel-deploy-claimable/
```

#### Key Skills
- **vercel-optimize**: Audit Vercel projects for cost, performance, caching
- **react-best-practices**: 40+ rules across 8 categories for React/Next.js
- **web-design-guidelines**: 100+ rules for accessibility, performance, UX
- **vercel-deploy-claimable**: Deploy to Vercel with claimable deployments

#### Manifest/Configuration
- `skills.sh.json` manifest file
- `CLAUDE.md` for Claude integration
- `AGENTS.md` with agent instructions

### 3. **Anthropics / Skills** (`anthropics/skills`)
**GitHub**: https://github.com/anthropics/skills  
**Skills.sh**: https://skills.sh/anthropics/skills  
**Stars**: 163k | **Forks**: 19.4k | **Skills**: ~20+

#### Taglines & Positioning
- Official Anthropic skills repository
- "Skills teach Claude how to complete specific tasks in a repeatable way"
- Includes creative, technical, and enterprise workflow skills
- Contains source-available document skills (docx, pdf, pptx, xlsx)

#### Folder Structure
```
skills/
├── creative-design/
├── development-technical/
├── enterprise-communication/
├── docx/          # Document creation skills
├── pdf/
├── pptx/
├── xlsx/
├── skill-creator/ # Skill creation guidance
└── frontend-design/
```

#### Key Skills
- **frontend-design**: Frontend design and development guidance
- **skill-creator**: Guidance for creating custom skills
- **webapp-testing**: Web application testing methodologies
- **mcp-builder**: MCP server creation guidance
- **docx/pdf/pptx/xlsx**: Document creation and editing skills

#### Manifest/Configuration
- `.claude-plugin/` with marketplace configuration
- Includes Agent Skills specification in `spec/` directory
- `template/` directory with skill creation templates

### 4. **Microsoft / Azure-Skills** (`microsoft/azure-skills`)
**GitHub**: https://github.com/microsoft/azure-skills  
**Skills.sh**: https://skills.sh/microsoft/azure-skills  
**Stars**: 1.3k | **Forks**: 215 | **Skills**: ~25+

#### Taglines & Positioning
- "Azure work is not just a code problem. It is a decision problem"
- Combines Azure expertise with MCP-backed execution
- Three-layer capability: skills (brain), MCP server (hands), Foundry MCP (AI specialist)

#### Folder Structure
```
skills/
├── azure-prepare/
├── azure-validate/
├── azure-deploy/
├── azure-cost/
├── azure-kubernetes/
├── azure-ai/
├── microsoft-foundry/
└── ...
```

#### Key Skills
- **azure-prepare**: Azure deployment preparation
- **azure-cost**: Azure cost optimization
- **azure-kubernetes**: AKS setup and management
- **azure-hosted-copilot-sdk**: Azure-hosted Copilot SDK integration
- **microsoft-foundry**: Microsoft Foundry workflows

#### Manifest/Configuration
- Comprehensive plugin system: `.claude-plugin/`, `.cursor-plugin/`, `apm.yml`
- `.mcp.json` for MCP server configuration
- Multi-harness support across 10+ agent platforms
- `landing-page/` with Astro-based documentation site

### 5. **Obra / Superpowers** (`obra/superpowers`)
**GitHub**: https://github.com/obra/superpowers  
**Skills.sh**: Not listed (but individual skills appear)
**Stars**: 259k | **Forks**: 23.1k | **Skills**: ~15

#### Taglines & Positioning
- "A complete software development methodology for your coding agents"
- Full SDLC workflow from brainstorming to deployment
- Subagent-driven development methodology
- Positioned as "superpowers" rather than just skills

#### Folder Structure
```
skills/
├── brainstorming/
├── writing-plans/
├── executing-plans/
├── test-driven-development/
├── systematic-debugging/
├── using-git-worktrees/
├── finishing-a-development-branch/
├── subagent-driven-development/
└── ...
```

#### Key Skills
- **brainstorming**: Socratic design refinement
- **subagent-driven-development**: Multi-agent workflow coordination
- **test-driven-development**: TDD methodology
- **systematic-debugging**: 4-phase debugging process
- **using-git-worktrees**: Git worktree management

#### Manifest/Configuration
- Extensive plugin support: `.claude-plugin/`, `.codex-plugin/`, `.cursor-plugin/`
- Multi-agent configuration files
- `hooks/` directory for session lifecycle hooks
- Commercial services offering through Prime Radiant

## Other Notable Skills Repositories

### 6. **Julius Brussee / Caveman** (`juliusbrussee/caveman`)
- **Focus**: Minimalist, pragmatic coding approach
- **Key skill**: `caveman` - minimalist coding methodology
- **Positioning**: Anti-over-engineering, simple solutions

### 7. **LeonXLnX / Taste-Skill** (`leonxlnx/taste-skill`)
- **Focus**: High-end visual design and UI/UX
- **Key skills**: `design-taste-frontend`, `high-end-visual-design`, `minimalist-ui`
- **Positioning**: Anti-AI-slop design, premium visual aesthetics

### 8. **Supabase / Agent-Skills** (`supabase/agent-skills`)
- **Focus**: Supabase and PostgreSQL best practices
- **Key skills**: `supabase-postgres-best-practices`, `supabase`

### 9. **Firebase / Agent-Skills** (`firebase/agent-skills`)
- **Focus**: Firebase development and deployment
- **Key skills**: `firebase-basics`, `firebase-auth-basics`, `firebase-hosting-basics`

### 10. **Corey Haines / MarketingSkills** (`coreyhaines31/marketingskills`)
- **Focus**: Marketing and content creation
- **Key skills**: `seo-audit`, `copywriting`, `content-strategy`, `programmatic-seo`

## Common Patterns and Conventions

### 1. **SKILL.md File Format**
All repositories follow the standard Agent Skills format:
```yaml
---
name: skill-name
description: What this skill does and when to use it
---
# Skill Name

Instructions for the agent...
```

### 2. **Folder Organization**
Common patterns:
- `skills/<category>/<skill-name>/SKILL.md` (categorized)
- `skills/<skill-name>/SKILL.md` (flat)
- `skills/.curated/`, `skills/.experimental/` (special categories)

### 3. **Plugin Integration**
Most repositories include:
- `.claude-plugin/` - Claude Code plugin configuration
- `.cursor-plugin/` - Cursor plugin configuration  
- `apm.yml` - APM (Agent Plugin Manager) configuration
- Agent-specific files: `CLAUDE.md`, `AGENTS.md`, etc.

### 4. **Multi-Agent Support**
Repositories typically support:
- Claude Code (primary)
- Codex / OpenAI
- Cursor
- GitHub Copilot
- Windsurf
- Kiro CLI
- OpenCode
- Gemini/Antigravity

### 5. **Skill Metadata and Discovery**
- `skills.sh.json` manifest files (optional)
- Telemetry for leaderboard ranking
- Tagging by topics (React, Next.js, Design, Mobile, etc.)

## Ecosystem Analysis

### Market Positioning
1. **Engineering-Focused**: Matt Pocock (practical engineering), Obra (methodology)
2. **Platform-Specific**: Vercel (web), Microsoft (Azure), Supabase/Firebase (BaaS)
3. **Creative/Design**: Anthropics (documents), LeonXLnX (visual design)
4. **Specialized**: Corey Haines (marketing), Julius Brussee (minimalism)

### Installation Methods
1. **skills.sh CLI**: `npx skills add <owner/repo>` (most common)
2. **Native Plugins**: Claude Code plugin marketplace, Cursor marketplace
3. **Direct Installation**: Manual file copying for specific agents
4. **APM**: Microsoft's Agent Plugin Manager for multi-harness installs

### Business Models
1. **Open Source**: Most repositories (MIT/Apache 2.0)
2. **Commercial Support**: Obra (Prime Radiant), Matt Pocock (newsletter/community)
3. **Platform Extension**: Vercel, Microsoft, Anthropics (platform enhancement)
4. **Source-Available**: Anthropics document skills (not open source)

## Comparison with Repo-Memory Skill

### Similarities
- All use `SKILL.md` format with YAML frontmatter
- Follow Agent Skills specification
- Designed for cross-agent compatibility
- Repository-based skill distribution

### Differences
1. **Scope**: Repo-memory focuses on **continuity and handoff**, while others focus on **execution methodologies**
2. **Artifacts**: Repo-memory creates **repository documentation**, others create **code or processes**
3. **Integration**: Repo-memory designed to **complement** other skills (ownership mapping)
4. **Persistence**: Repo-memory emphasizes **git-versioned persistence**, others use ephemeral or tool-specific storage

### Integration Opportunities
Repo-memory could:
1. **Track skill usage** in feature docs (which skills were used)
2. **Map skill outputs** in ownership map (where skill artifacts live)
3. **Generate skill registry** from installed skills
4. **Coordinate skill workflows** through feature state management

## Key Takeaways

1. **Skills.sh is the central ecosystem** with registry, CLI, and discovery
2. **Diverse skill categories** from engineering to design to platform-specific
3. **Standardized format** enables cross-agent compatibility
4. **Plugin ecosystem** emerging with marketplace integrations
5. **Business models evolving** from open source to commercial support
6. **Repo-memory fills continuity gap** missing from execution-focused skills

## Recommendations for Repo-Memory

1. **Register on skills.sh** to increase discoverability
2. **Create plugin configurations** for major agents (Claude Code, Cursor, etc.)
3. **Document integration patterns** with popular skills (Matt Pocock, Obra, Vercel)
4. **Consider skill categorization** - repo-memory as "continuity" or "workflow" category
5. **Explore telemetry options** for usage tracking (opt-in)
6. **Develop installation scripts** for easier adoption across agents

The skills ecosystem is maturing rapidly with clear standards, established players, and growing adoption across all major AI coding agents.