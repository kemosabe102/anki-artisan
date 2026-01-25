# schemas/ Directory

**Purpose**: JSON Schema definitions for validating sast-scanner inputs and outputs

---

## Contents

| File | Purpose |
|------|---------|
| `sast-scanner.schema.json` | Agent-specific I/O validation (SUCCESS/FAILURE states) |

---

## Schema Overview

The schema defines:
- **Input**: operation, files, commit_groups, baseline_commit, severity_threshold
- **SUCCESS Output**: scan_summary, group_results with security_status
- **FAILURE Output**: failure_type, reasons, recovery_suggestions

---

## Validation

```bash
uv run python scripts/validate_agent_file.py .claude/agents/code-review/sast-scanner/sast-scanner.md
```

---

## See Also

- **Base schema**: `.claude/docs/shared/schemas/base-agent.schema.json`
- **Schema guide**: `.claude/docs/01-guides/agents/agent-standards-runtime.md`
