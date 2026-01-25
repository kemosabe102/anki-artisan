# schemas/ Directory

**Purpose**: JSON Schema definitions for validating test-executor inputs and outputs

---

## Contents

| File | Purpose |
|------|---------|
| `test-executor.schema.json` | Agent-specific I/O validation |

---

## Schema Overview

The test-executor schema follows the two-state SUCCESS/FAILURE model:

### SUCCESS State

Returns `agent_specific_output` with:
- `execution_summary`: Test counts, exit code
- `failures`: Categorized failure array
- `delegation_summary`: Primary category, confidence
- `delegation_recommendations`: Next steps for each category
- `test_health_metrics`: Independence, repeatability scores
- `coverage_gaps`: Uncovered files/functions

### FAILURE State

Returns `failure_details` with:
- `failure_type`: FRAMEWORK_NOT_FOUND, INVALID_PATH, EXECUTION_ERROR
- `reasons`: Array of failure causes
- `recovery_suggestions`: How to resolve

---

## Validation

```bash
uv run python scripts/validate_agent_file.py .claude/agents/dev-tools/test-executor/test-executor.md
```

---

## See Also

- **Base schema**: `.claude/docs/shared/schemas/base-agent.schema.json`
- **Main agent**: `../test-executor.md`
