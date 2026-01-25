# schemas/ Directory

**Purpose**: JSON Schema definitions for researcher-web agent outputs

---

## Contents

| File | Purpose |
|------|---------|
| `researcher-web.schema.json` | Agent-specific I/O validation (SUCCESS/FAILURE states) |

---

## Schema Overview

The schema defines:
- **SUCCESS**: findings, source_attribution, compression_stats, research_boundaries, security_validations, iteration_support
- **FAILURE**: failure_type, reasons, research_attempted, partial_results, recovery_suggestions

---

## See Also

- **Base schema**: `.claude/docs/shared/schemas/base-agent.schema.json`
- **Main agent**: `../researcher-web.md`
