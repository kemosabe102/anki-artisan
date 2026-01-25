# Contingency Planner Schema

JSON Schema for contingency-planner agent input/output validation.

## Files

| File | Purpose |
|------|---------|
| `contingency-planner.schema.json` | Input/output contract extending base-agent.schema.json |

## Schema Overview

- **Input**: Ranked hypotheses from orchestrator with confidence scores and risk factors
- **Output**: SUCCESS with contingency plans or FAILURE with recovery suggestions
- **Key Fields**: failure_modes_identified, fallback_strategies, retry_plans, risk_assessment
