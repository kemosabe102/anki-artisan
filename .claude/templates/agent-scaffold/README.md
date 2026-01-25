# Agent Scaffold Template

**Version**: 1.0.0 | **Last Updated**: 2025-11-30

**Purpose**: Self-contained directory structure for creating new agents

**Reference Implementation**: `.claude/agents/ttrpg-campaign-architect/`

---

## When to Use This Scaffold

Use this directory structure (not flat files) when your agent:
- Has domain-specific knowledge (methodologies, frameworks, taxonomies)
- Needs examples or interactive templates
- Requires complex schema definitions
- Would exceed 300 lines as a single file

For simple agents (<200 lines), a single `.md` file may suffice.

---

## Directory Structure

```
.claude/agents/{{domain}}/{{agent-name}}/
├── {{agent-name}}.md           # Core agent definition (<200 lines)
├── docs/                       # Domain knowledge (externalized)
│   ├── domain-expertise.md     # Core domain concepts
│   └── frameworks.md           # Methodologies and patterns
├── examples/                   # Usage patterns
│   ├── delegation-examples.md  # How orchestrator calls this agent
│   └── output-template.md      # Expected output formats
└── schemas/
    └── {{agent-name}}.schema.json  # Input/output validation
```

---

## Domain Directory Selection

Place your agent directory in the appropriate domain:

| Domain | Directory | Use For |
|--------|-----------|---------|
| Development Tools | `dev-tools/` | Code, testing, debugging, CI/CD |
| Research | `research/` | Investigation, analysis, web search |
| Investing | `investing/` | Financial analysis, portfolio |
| TTRPG | `ttrpg-campaign-architect/` | Gaming, storytelling |
| Documentation | `docs/` | Writing, editing, knowledge management |

**New domains**: Create new directory if no existing domain fits.

---

## Quick Start

1. **Copy this scaffold**: `cp -r .claude/templates/agent-scaffold/ .claude/agents/{{domain}}/{{agent-name}}/`
2. **Rename files**: Replace `{{agent-name}}` in filenames
3. **Fill templates**: Complete each file following inline guidance
4. **Validate**: Run `uv run python scripts/validate_agent_file.py .claude/agents/{{domain}}/{{agent-name}}/{{agent-name}}.md`
5. **Register**: Add to CLAUDE.md Complete Agent List table

---

## Files Explained

| File | Purpose | When Required |
|------|---------|---------------|
| `{{agent-name}}.md` | Core definition | ALWAYS |
| `docs/*.md` | Domain knowledge | When agent needs specialized expertise |
| `examples/*.md` | Usage patterns | When delegation is complex |
| `schemas/*.json` | Validation | ALWAYS (extends base-agent.schema.json) |

---

## Key Principles

1. **Core agent stays lean** (<200 lines) - externalize knowledge to `docs/`
2. **Examples show, don't tell** - real usage patterns beat abstract descriptions
3. **Schemas validate** - machine-readable contracts prevent drift
4. **Reference, don't duplicate** - link to shared frameworks when possible

---

## See Also

- **Gold standard example**: `.claude/agents/ttrpg-campaign-architect/`
- **Flat agent template**: `.claude/templates/agent.template.md`
- **Agent creation guide**: `docs/04-guides/agent-creation-guide.md`
- **Naming conventions**: `.claude/docs/01-guides/agents/agent-naming-conventions.md`
