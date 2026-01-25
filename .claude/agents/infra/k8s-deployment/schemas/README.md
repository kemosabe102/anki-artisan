# k8s-deployment Schemas

**Purpose**: JSON Schema definitions for validating agent inputs and outputs

---

## Contents

| File | Purpose | Required |
|------|---------|----------|
| `k8s-deployment.schema.json` | Agent-specific I/O validation | YES |

---

## Schema Requirements

### Two-State Model

All outputs follow SUCCESS/FAILURE pattern:
- **SUCCESS**: Includes `agent_specific_output` with operation results
- **FAILURE**: Includes `failure_details` with recovery suggestions

### Required Fields

- `status`: "SUCCESS" or "FAILURE"
- `agent`: "k8s-deployment"
- `confidence`: Number 0-1

---

## Validation

```bash
uv run python scripts/validate_agent_file.py .claude/agents/dev-tools/k8s-deployment/k8s-deployment.md
```

---

## See Also

- **Base schema**: `.claude/docs/shared/schemas/base-agent.schema.json`
- **Main agent**: `../k8s-deployment.md`
