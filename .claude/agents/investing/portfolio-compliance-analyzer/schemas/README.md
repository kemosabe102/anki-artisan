# schemas/ Directory

**Purpose**: JSON Schema definitions for validating agent inputs and outputs

---

## Contents

| File | Description |
|------|-------------|
| `portfolio-compliance-analyzer.schema.json` | Agent I/O validation schema (SUCCESS/FAILURE model) |

---

## Schema Overview

The schema defines:
- **Input**: IPS document, holdings data, analysis_date, market_data (optional), analysis_mode
- **SUCCESS Output**: 5 core sections (gap_analysis, rebalancing, tax_optimization, tactical_sleeves, compliance_flags)
- **FAILURE Output**: failure_type, error_details, recovery_suggestions, partial_results

---

## Validation

```bash
# Validate agent output
uv run python scripts/validate_agent_file.py \
  .claude/agents/investing/portfolio-compliance-analyzer/portfolio-compliance-analyzer.md
```

---

## See Also

- **Base schema**: `.claude/docs/shared/schemas/base-agent.schema.json`
- **Main agent**: `../portfolio-compliance-analyzer.md`
