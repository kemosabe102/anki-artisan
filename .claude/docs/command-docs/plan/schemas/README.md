# Plan Command Schemas

Schema documentation for the `/plan` slash command.

## Overview

The `/plan` command does not produce structured JSON output schemas like some other commands. Instead, it produces:

1. **Plan Files (Markdown)**: `[component-name]-PLAN.md` files following the plan template
2. **Workflow Reports**: Presented in markdown format during execution
3. **Quality Metrics**: Embedded in workflow output

## Plan File Template

Plan files are created from `docs/00-project/templates/plan-template.md` and contain:

- Business Context sections (populated by planning)
- Technical sections (populated by architecture)
- Implementation Plan with phases and tasks
- Integration points documentation

## Agent Input/Output Schemas

For detailed agent input/output schemas, see:

- **planning**: `.claude/agents/dev-tools/planning.md`
- **feature-analyzer**: `.claude/agents/dev-tools/feature-analyzer.md`
- **planning**: `.claude/agents/dev-tools/planning.md`
- **architecture**: `.claude/agents/dev-tools/architecture.md`
- **architectureer**: `.claude/agents/dev-tools/architectureer.md`

## Quality Metrics Schema

Quality metrics returned by architectureer:

```json
{
  "architecture_score": 4.2,
  "requirements_coverage": 0.95,
  "business_alignment": 0.85,
  "integration_analysis": {
    "status": "complete",
    "integration_points": 5,
    "issues": []
  },
  "production_readiness": {
    "security": "PASS",
    "scalability": "PASS",
    "observability": "PASS"
  }
}
```
