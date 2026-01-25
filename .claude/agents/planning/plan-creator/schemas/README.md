# Plan Creator Schemas

JSON schemas for plan-creator agent input/output validation.

## Contents

| Schema | Purpose |
|--------|---------|
| `plan-creator.schema.json` | Agent output validation schema |

## Output Schema Summary

### SUCCESS Response
```json
{
  "status": "SUCCESS",
  "agent": "plan-creator",
  "confidence": 0.85-1.0,
  "output_files": { "plan_json": "string" },
  "summary": { ... },
  "next_step": "string",
  "skill_invocations": ["string"],
  "metadata": { ... },
  "warnings": []
}
```

### FAILURE Response
```json
{
  "status": "FAILURE",
  "agent": "plan-creator",
  "error_code": "string",
  "error_message": "string",
  "phase_failed": "string",
  "partial_output": null,
  "recovery_suggestions": ["string"],
  "skill_invocations": ["string"]
}
```

## Related Schemas

- PLAN.json schema: `.claude/docs/command-docs/plan/templates/feature_plan_blank.json`
- Base agent schema: `.claude/schemas/base-agent.schema.json`
