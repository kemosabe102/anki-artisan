# Tech Debt Investigator Schemas

JSON Schema definitions for agent input/output contracts.

## Contents

| Schema | Purpose |
|--------|---------|
| `tech-debt-investigator.schema.json` | Input/output contract extending base-agent.schema.json |

## Base Schema

This agent extends `.claude/docs/shared/schemas/base-agent.schema.json` with:
- Two-state model: SUCCESS with findings OR FAILURE with recovery guidance
- Required meta-flags: status, agent, confidence, execution_timestamp
- Agent-specific output structure for debt analysis results

## Output Structure

```json
{
  "status": "SUCCESS|FAILURE",
  "agent": "tech-debt-investigator",
  "confidence": 0.0-1.0,
  "execution_timestamp": "ISO8601",
  "agent_specific_output": {
    "debt_score": 0-100,
    "tdr": 0.0-1.0,
    "sqale_grade": "A-E",
    "sig_rating": 1-5,
    "category_breakdown": {...},
    "impact_effort_matrix": {...},
    "hotspots": [...],
    "remediation_roadmap": [...],
    "trend_analysis": {...}
  }
}
```
