# Technical PM Schemas

JSON Schema definitions for technical-pm agent input/output validation.

## Contents

| File | Purpose |
|------|---------|
| `technical-pm.schema.json` | Input/output contract for business review operations |

## Schema Overview

The schema defines a two-state output model:

### SUCCESS State
- `validation_checklist` with all checks passed
- `success_evidence` containing:
  - `plan_enhancements` (business context, NFR analysis, traceability, investigation agenda)
  - `files_enhanced` (list of reviewed files)
  - `handoff_package` (readiness for downstream agents)
  - `recommendations` (prioritized P1/P2/P3)
  - `next_actions` and `changes`

### FAILURE State
- `validation_checklist` with failed checks documented
- `failure_details` containing:
  - `failure_type` (missing_existing_plans, validation_error, etc.)
  - `reasons` and `missing` information
  - `recovery_suggestions` with effort estimates

## Validation

All technical-pm outputs MUST validate against this schema before returning to orchestrator.

```bash
# Validate output (example)
jsonschema -i output.json schemas/technical-pm.schema.json
```
