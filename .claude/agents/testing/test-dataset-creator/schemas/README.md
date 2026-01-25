# schemas/ Directory

**Purpose**: JSON Schema definitions for validating agent inputs and outputs

---

## Contents

| File | Purpose | Required |
|------|---------|----------|
| `test-dataset-creator.schema.json` | Agent-specific I/O validation | YES |

---

## Schema Structure

Extends base-agent.schema.json with two-state SUCCESS/FAILURE model:

### SUCCESS State
- `datasets_created`: Array of dataset file info
- `diversity_metrics`: Change type/file count distributions, edge cases
- `quality_validation`: Diversity score, quality grade, coverage stats
- `generation_methodology`: Git range, sampling strategy, heuristic source

### FAILURE State
- `failure_type`: insufficient_diversity | missing_edge_cases | schema_validation | heuristic_extraction
- `reasons`: Specific gaps identified
- `recovery_suggestions`: Actionable next steps
- `partial_results`: What was generated before failure

---

## Validation

```bash
uv run python scripts/validate_agent_file.py .claude/agents/dev-tools/test-dataset-creator/test-dataset-creator.md
```
