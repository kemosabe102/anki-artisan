# schemas/ Directory

**Purpose**: JSON Schema reference for postgres-timescale-specialist agent

---

## Schema Location

The schema for this agent is in the **shared schemas directory**:

```
.claude/docs/schemas/postgres-timescale-specialist.schema.json
```

**Why shared?** The schema is comprehensive (452 lines) and used for validation across the system. Keeping it in the shared location avoids duplication and ensures consistency.

---

## Schema Overview

The schema follows the two-state SUCCESS/FAILURE model:

### SUCCESS State
```json
{
  "status": "SUCCESS",
  "agent": "postgres-timescale-specialist",
  "confidence": 0.92,
  "agent_specific_output": {
    "original_query": "...",
    "optimized_query": "...",
    "improvement_factors": ["chunk_exclusion", "index_usage"],
    "estimated_speedup": "16x",
    "explain_analysis": "..."
  }
}
```

### FAILURE State
```json
{
  "status": "FAILURE",
  "agent": "postgres-timescale-specialist",
  "confidence": 0.3,
  "failure_details": {
    "failure_type": "crash_risk_detected",
    "reasons": ["Query matches crash-prone pattern"],
    "recovery_suggestions": ["Use symbols_cache instead"]
  }
}
```

---

## Validation

Run validation with:
```bash
uv run python scripts/validate_agent_file.py .claude/agents/dev-tools/postgres-timescale-specialist/postgres-timescale-specialist.md
```

---

## See Also

- **Full schema**: `.claude/docs/schemas/postgres-timescale-specialist.schema.json`
- **Base schema**: `.claude/docs/shared/schemas/base-agent.schema.json`
- **Main agent**: `../postgres-timescale-specialist.md`
