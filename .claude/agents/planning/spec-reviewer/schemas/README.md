# schemas/ - spec-reviewer

**Purpose**: JSON Schema definitions for validating agent inputs and outputs

---

## Contents

| File | Purpose |
|------|---------|
| `spec-reviewer.schema.json` | Input/output validation schema |

---

## Schema Model

Extends base-agent two-state model:
- **SUCCESS**: Review completed with quality assessment
- **FAILURE**: Review failed with recovery guidance

---

## Validation

```bash
uv run python scripts/validate_agent_file.py .claude/agents/dev-tools/spec-reviewer/spec-reviewer.md
```

---

## See Also

- **Base schema**: `.claude/docs/shared/schemas/base-agent.schema.json`
- **Agent definition**: `../spec-reviewer.md`
