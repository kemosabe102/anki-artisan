# Workflow Analyzer Documentation

This directory contains domain knowledge and frameworks for the workflow-analyzer agent.

## Contents

| File | Purpose |
|------|---------|
| `domain-expertise.md` | Workflow analysis patterns and best practices |
| `frameworks.md` | Analysis frameworks and methodologies |

## Quick Reference

### Agent Purpose
Analyze slash command workflows in `.claude/commands/**` for correctness, safety, and optimization opportunities.

### Primary Capabilities
1. 7-dimension quality matrix evaluation
2. Subagent existence and capability verification
3. Skill reference validation
4. SCAMPER workflow optimization

### Output Format
Structured JSON with:
- `workflow_score`: 0-100
- `grade`: A-F
- `dimension_scores`: 7 weighted dimensions
- `violations`: Issue catalog with codes
- `recommendations`: Prioritized fixes
- `scamper_optimizations`: Optimization candidates (OPTIMIZE mode)

## Related Resources

- `../phases/` - OODA phase workflows
- `../schemas/workflow-analyzer.schema.json` - Output contract
- `.claude/skills/command-quality-evaluation/` - Quality matrix reference
