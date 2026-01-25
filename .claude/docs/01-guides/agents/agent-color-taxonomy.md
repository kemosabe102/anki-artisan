---
title: "Agent Color Taxonomy"
date: 2025-11-30
status: ACTIVE
tags: [agents, claude-docs, visual-design]
---

# Agent Color Taxonomy

**Purpose**: Standardized color assignments for agent visual identification by work type.

**Usage**: When creating or updating agents, assign colors based on the agent's primary work type.

## Supported Colors (Claude Code Limitation)

Claude Code only supports **8 simple color names**. CSS named colors (e.g., `dodgerblue`, `forestgreen`) do NOT work.

| Valid Color | Works |
|-------------|-------|
| `red` | ✅ |
| `blue` | ✅ |
| `green` | ✅ |
| `yellow` | ✅ |
| `purple` | ✅ |
| `orange` | ✅ |
| `pink` | ✅ |
| `cyan` | ✅ |

**Source**: [cclint - Claude Code Linter](https://github.com/carlrannaberg/cclint)

## Color-to-Category Mapping

| Work Type | Color | Semantic Rationale |
|-----------|-------|-------------------|
| **Research/Exploration** | `blue` | Discovery, knowledge gathering |
| **Implementation/Coding** | `green` | Building, creation, growth |
| **Review/Validation** | `purple` | Quality, judgment, wisdom |
| **Testing** | `yellow` | Attention, test results need focus |
| **Documentation** | `cyan` | Informational, readable |
| **Planning/Architecture** | `blue` | Strategy, design, authority |
| **Security** | `red` | Danger, critical attention |
| **Observability** | `cyan` | Monitoring, dashboards, data |
| **Infrastructure/DevOps** | `orange` | Operations, deployment |
| **Analysis/Debugging** | `pink` | Investigative |
| **Domain-Specific** | `purple` | Specialized expertise |

## Assignment Rules

1. **Primary work type wins**: If an agent does multiple things, use its PRIMARY function
2. **Domain-specific overrides**: Investing, creative, or other specialized domains use `purple`
3. **Security is exclusive**: Only security-focused agents (SAST, auth) use `red`
4. **No duplicates within category**: All agents in a category share the same color

## Examples by Category

### Research (`blue`)
- researcher-codebase, researcher-lead, researcher-external, repository-analyst

### Implementation (`green`)
- development, claude-code-ecosystem, debugger

### Review (`purple`)
- code-quality, architectureer, planning, planning

### Testing (`yellow`)
- code-quality, code-quality, test-dataset-creator

### Documentation (`cyan`)
- documentation, documentation

### Planning (`blue`)
- planning, architecture, planning, planning, contingency-planner

### Security (`red`)
- sast-scanner

### Observability (`cyan`)
- grafana-dashboard-builder, promql-query-builder, loki-query-specialist

### Infrastructure (`orange`)
- source-control, deployment-release, postgres-timescale-specialist, workflow

### Analysis (`pink`)
- tech-debt-investigator, context-optimizer, feature-analyzer, intent-analyzer, context-readiness-assessor, root-cause-identifier, claude-code-ecosystem

### Domain-Specific (`purple`)
- market-data-specialist, pattern-detector, portfolio-compliance-analyzer, risk-management-specialist, sentiment-nlp-specialist, technical-indicator-specialist, ttrpg-campaign-architect

## Technical Notes

- Only 8 colors are supported by Claude Code: red, blue, green, yellow, purple, orange, pink, cyan
- CSS named colors (dodgerblue, forestgreen, etc.) do NOT work - they display as no color
- The `color` field is undocumented by Anthropic but functional
- No schema enforcement exists - these are conventions
