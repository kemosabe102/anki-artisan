# schemas/ Directory - test-creator

**Purpose**: JSON Schema definitions for validating agent inputs and outputs

---

## Contents

| File | Purpose | Required |
|------|---------|----------|
| `test-creator.schema.json` | Agent I/O validation | YES |

---

## Schema Overview

### Input Properties

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `context` | string | YES | Test creation task description |
| `operation_type` | enum | YES | `create_tests`, `analyze_coverage`, `fix_test_bug` |
| `files_to_test` | array | NO | Files requiring test creation |
| `coverage_threshold` | number | NO | Target coverage % (default 80) |
| `execution_timestamp` | datetime | YES | ISO 8601 UTC timestamp |

### Output States

**SUCCESS**: Returns `agent_specific_output` with:
- `tests_created`: Array of test file paths
- `test_patterns_applied`: Patterns used (AAA, mocking, etc.)
- `test_strategy`: Approach, coverage achieved, next steps

**FAILURE**: Returns `failure_details` with:
- `failure_type`: Category of failure
- `reasons`: Why test creation failed
- `recovery_suggestions`: How to resolve

---

## Validation

```bash
uv run python scripts/validate_agent_file.py .claude/agents/dev-tools/test-creator/test-creator.md
```

---

## See Also

- **Base schema**: `.claude/docs/shared/schemas/base-agent.schema.json`
- **Main agent**: `../test-creator.md`
