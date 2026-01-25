# Feature Final Review Schemas

## Output Schema

The `output.schema.json` defines the structured output format for both agent modes.

### Modes

| Mode | Output Type | Key Fields |
|------|-------------|------------|
| `detect` | `integration_pairs[]` | id, upstream, downstream, files, confidence |
| `review` | `pair_findings{}` | findings, checklist_scores, test_coverage |

### Status Variants

- **SUCCESS**: Mode completed with valid output
- **FAILURE**: Mode failed with recovery suggestions

### Detect Mode Output

Returns an array of discovered integration pairs:

```json
{
  "status": "SUCCESS",
  "mode": "detect",
  "feature": "alpha-phase-01",
  "total_pairs": 8,
  "integration_pairs": [...]
}
```

### Review Mode Output

Returns findings for a single integration pair:

```json
{
  "status": "SUCCESS",
  "mode": "review",
  "pair_id": 1,
  "gate_status": "PASS_WITH_CONDITIONS",
  "pair_findings": [...],
  "checklist_scores": {...}
}
```

### Failure Output

```json
{
  "status": "FAILURE",
  "mode": "detect",
  "failure_details": {
    "failure_type": "feature_not_found",
    "error_message": "Directory not found: packages/missing/",
    "recovery_suggestions": ["Verify feature path", "Check for typos"]
  }
}
```

### Related Schemas

- Skill schema: `.claude/skills/integration-boundary-reviewer/schemas/review-output.schema.json`
