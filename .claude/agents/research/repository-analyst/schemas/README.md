# Repository Analyst Schemas

## Contents

| File | Purpose |
|------|---------|
| `repository-analyst.schema.json` | Input/output contract for repository analysis operations |

## Schema Overview

The schema defines:
- **Input**: task_id, operation_type, target_directory, output_format, component_patterns
- **Output (SUCCESS)**: analysis_summary, components, categorization, validation_results, output_artifacts
- **Output (FAILURE)**: failure_type, reasons, affected_components, recovery_suggestion

## Validation

All agent responses must validate against this schema before returning to orchestrator.
