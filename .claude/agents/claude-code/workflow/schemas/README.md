# Workflow Agent Schema

This directory contains the JSON Schema contract for the workflow agent.

## Contents

| File | Description |
|------|-------------|
| `workflow.schema.json` | Input/output contract for all 10 workflow operations |

## Schema Overview

**Version**: 2.2.0
**Extends**: `base-agent.schema.json` (two-state SUCCESS/FAILURE model)

### Input Contract

Required fields:
- `context` - Primary instruction defining what workflow agent should accomplish
- `execution_timestamp` - ISO 8601 UTC timestamp from orchestrator
- `operation` - One of 10 operation types

Optional fields:
- `operation_id` - ULID/UUID for idempotency
- `apply_mode` - `dry_run` or `commit` (default: commit)
- `workflow_details` - Workflow-specific configuration
- `sync_requirements` - Documents and sections to synchronize
- `validation_config` - Smoke testing, auto-fix, compliance options

### Output Contract

**SUCCESS** requires:
- `status: "SUCCESS"`
- `validation_checklist` with `all_checks_passed: true`
- `success_evidence` with operation result, provenance, validation results, changes
- `confidence` (0.0-1.0)
- `severity` (Critical/Major/Minor)

**FAILURE** requires:
- `status: "FAILURE"`
- `validation_checklist` with `all_checks_passed: false` and `failed_checks`
- `failure_details` with type, reasons, proposed next steps
- Recovery suggestions with effort estimates

## Validation

All workflow agent outputs must validate against this schema before being returned to the orchestrator.

```bash
# Validate output against schema
AGENT_NAME=workflow uv run python -c "
import json
from jsonschema import validate
schema = json.load(open('.claude/agents/claude-code/workflow/schemas/workflow.schema.json'))
output = {...}  # Agent output
validate(output, schema['properties']['output'])
"
```

## Versioning

- **Major** (3.x): Breaking changes to required fields
- **Minor** (x.2): New optional fields, operation types
- **Patch** (x.x.1): Documentation, description updates
