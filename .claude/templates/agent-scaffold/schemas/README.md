# schemas/ Directory

**Purpose**: JSON Schema definitions for validating agent inputs and outputs

---

## What Goes Here

| File | Purpose | Required |
|------|---------|----------|
| `{{agent-name}}.schema.json` | Agent-specific I/O validation | YES |

---

## Schema Requirements

### Must Extend Base Schema

All agent schemas MUST follow the two-state SUCCESS/FAILURE model:

```json
{
  "oneOf": [
    { "properties": { "status": { "const": "SUCCESS" }, ... } },
    { "properties": { "status": { "const": "FAILURE" }, ... } }
  ]
}
```

### Required Fields

Every schema MUST include:
- `status`: "SUCCESS" or "FAILURE"
- `agent`: Agent name (const value)
- `confidence`: Number 0-1

### SUCCESS State

Define `agent_specific_output` with your agent's output structure.

### FAILURE State

Define `failure_details` with:
- `failure_type`: Enum of failure categories
- `reasons`: Array of strings
- `recovery_suggestions`: Array of strings

---

## Schema Template

See `{{agent-name}}.schema.template.json` for complete template.

---

## Validation

Run validation with:
```bash
uv run python scripts/validate_agent_file.py .claude/agents/{{domain}}/{{agent-name}}/{{agent-name}}.md
```

---

## See Also

- **Base schema**: `.claude/docs/shared/schemas/base-agent.schema.json`
- **Reference example**: `.claude/agents/ttrpg-campaign-architect/schemas/`
- **Schema guide**: `.claude/docs/01-guides/agents/agent-standards-runtime.md`
