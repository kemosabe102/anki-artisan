# schemas/ Directory

**Purpose**: JSON Schema definitions for validating agent inputs and outputs

---

## Contents

| File | Description |
|------|-------------|
| `technical-indicator-specialist.schema.json` | Two-state SUCCESS/FAILURE schema for indicator computation |

---

## Validation

Run validation with:
```bash
uv run python scripts/validate_agent_file.py .claude/agents/investing/technical-indicator-specialist/technical-indicator-specialist.md
```

---

## See Also

- **Base schema**: `.claude/docs/shared/schemas/base-agent.schema.json`
- **Main agent**: `../technical-indicator-specialist.md`
