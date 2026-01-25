# schemas/ Directory

**Purpose**: JSON Schema for postgres-schema-specialist agent input/output validation

---

## Schema Location

The schema is in the **agent-local directory**:

```
postgres-schema-specialist.schema.json
```

---

## Schema Overview

The schema follows the two-state SUCCESS/FAILURE model:

### SUCCESS State
```json
{
  "status": "SUCCESS",
  "agent": "postgres-schema-specialist",
  "confidence": 0.88,
  "agent_specific_output": {
    "mode": "design_schema",
    "ddl_script": "CREATE TABLE ...",
    "normalization_level": "3NF",
    "design_decisions": ["Rationale for design choices"]
  }
}
```

### FAILURE State
```json
{
  "status": "FAILURE",
  "agent": "postgres-schema-specialist",
  "confidence": 0.3,
  "failure_details": {
    "failure_type": "insufficient_context",
    "reasons": ["Missing table name"],
    "recovery_suggestions": ["Provide table name"]
  }
}
```

---

## Mode-Specific Output Properties

| Mode | Key Properties |
|------|---------------|
| `design_schema` | ddl_script, normalization_level, design_decisions |
| `create_migration` | migration_up, migration_down, lock_assessment |
| `design_indexes` | indexes_designed (array with type, columns, rationale) |
| `setup_hypertable` | hypertable_config (chunk_interval, compression, retention) |
| `design_constraints` | constraints_designed (array with type, ddl) |
| `design_backup_strategy` | backup_strategy (schedule, retention, recovery_steps) |

---

## Validation

Run validation with:
```bash
uv run python scripts/validate_agent_file.py .claude/agents/infra/postgres-schema-specialist/postgres-schema-specialist.md
```

---

## See Also

- **Base schema**: `.claude/docs/shared/schemas/base-agent.schema.json`
- **Main agent**: `../postgres-schema-specialist.md`
