# schemas/ Directory

**Purpose**: JSON Schema definitions for validating agent inputs and outputs.

---

## Contents

| File | Description |
|------|-------------|
| `sentiment-nlp-specialist.schema.json` | Input/output validation for all 4 operations |

---

## Schema Overview

### Input Schema
- `task_id`: Unique task identifier
- `operation_type`: analyze_sentiment | aggregate_sentiment | detect_bursts | extract_themes
- `headlines`: Array of {text, symbol, timestamp, source}
- `aggregation_params`, `burst_params`, `theme_params`: Operation-specific config
- `config`: Model and processing configuration
- `execution_timestamp`: ISO 8601 UTC from orchestrator

### Output Schema (SUCCESS)
- `status`: "SUCCESS"
- `agent`: "sentiment-nlp-specialist"
- `agent_specific_output`: Varies by operation type
- `metadata`: model_version, processing_time_ms, device_used

### Output Schema (FAILURE)
- `status`: "FAILURE"
- `failure_details`: failure_type, reasons, recovery_suggestions
- `partial_results`: If batch partially processed

---

## Validation

```bash
uv run python scripts/validate_agent_file.py .claude/agents/investing/sentiment-nlp-specialist/sentiment-nlp-specialist.md
```

---

## See Also

- **Main agent**: `../sentiment-nlp-specialist.md`
- **Base schema**: `.claude/docs/shared/schemas/base-agent.schema.json`
