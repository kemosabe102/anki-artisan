# Feature Analyzer Schemas

## Contents

| File | Purpose |
|------|---------|
| `feature-analyzer.schema.json` | Input/output contract extending base-agent.schema.json |

## Base Schema Reference

Extends: `.claude/docs/shared/schemas/base-agent.schema.json`

## Agent-Specific Outputs

### SUCCESS Output
- `comparison_matrix`: Overlap percentages and indicators per feature pair
- `separation_report`: Responsibility boundaries and ownership recommendations
- `integration_architecture`: Merge strategy or separation contracts
- `alignment_assessment`: Architecture goal validation with risks
- `recommended_action`: merge/separate/refactor with confidence

### FAILURE Output
- `failure_type`: missing_context | access_error | validation_failure | circular_dependency
- `reasons`: Specific blocking issues
- `recovery_suggestions`: Agent delegations with effort estimates
- `partial_results`: Work completed before failure
