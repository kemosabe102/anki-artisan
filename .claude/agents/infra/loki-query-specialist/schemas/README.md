# schemas/ Directory

**Purpose**: JSON Schema definitions for loki-query-specialist I/O validation

---

## Contents

| File | Purpose |
|------|---------|
| `loki-query-specialist.schema.json` | Agent-specific I/O validation |

---

## Schema Overview

Extends `base-agent.schema.json` with two-state SUCCESS/FAILURE model.

### Operations Supported

| Operation | Input | Output |
|-----------|-------|--------|
| `construct_query` | extraction_goal, log_sample | query_construction_result |
| `analyze_format` | log_sample, extraction_goal | format_analysis |
| `validate_syntax` | logql_query, loki_endpoint | validation_result |
| `optimize_query` | logql_query, performance_context | optimization_recommendations |
| `recommend_format` | log_sample, current_issues | format_recommendations |
| `assess_log_quality` | log_sample, loki_labels, depth | log_quality_assessment |

### Required Input Fields

- `task_id`: Unique task identifier
- `operation_type`: One of 6 operation types
- `execution_timestamp`: ISO 8601 UTC timestamp

### SUCCESS Output

- `agent_specific_output`: Contains operation-specific results
- `confidence`: 0-1 confidence score
- `summary`: 1-3 sentence description

### FAILURE Output

- `failure_details`: Contains failure_type, reasons, recovery_suggestions
- `partial_results`: Any completed work before failure

---

## Validation

```bash
uv run python scripts/validate_agent_file.py \
  .claude/agents/dev-tools/loki-query-specialist/loki-query-specialist.md
```

---

## See Also

- **Base schema**: `.claude/docs/shared/schemas/base-agent.schema.json`
- **Schema guide**: `.claude/docs/01-guides/agents/agent-standards-runtime.md`
