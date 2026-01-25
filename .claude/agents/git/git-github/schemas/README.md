# Git-GitHub Agent Schemas

**Purpose**: JSON Schema definitions for agent input/output contracts

---

## Contents

| File | Description |
|------|-------------|
| `git-github.schema.json` | Complete input/output schema for all 3 operations |

---

## Schema Overview

The schema defines:

1. **Input Contract**: Operation type + operation-specific options
2. **Output Contract**: SUCCESS with results OR FAILURE with recovery guidance

### Operations

| Operation | Input Options | Output Structure |
|-----------|---------------|------------------|
| `analyze_changes` | `include_context` | commit_groups, grouping_summary |
| `execute_commits` | `groups_to_commit[]` | committed_groups, summary |
| `monitor_ci` | `commit_sha`, `run_id`, `branch` | workflow_runs, recommended_actions |

---

## Validation

Schema follows JSON Schema Draft-07 specification.

**Required fields for all outputs**:
- `status`: "SUCCESS" or "FAILURE"
- `agent`: "git-github"
- `confidence`: 0.0-1.0 (0.0 for failures)

---

## See Also

- **Base schema**: `.claude/docs/shared/schemas/base-agent.schema.json`
- **Output examples**: `../examples/output-examples.md`
- **Main agent**: `../git-github.md`
