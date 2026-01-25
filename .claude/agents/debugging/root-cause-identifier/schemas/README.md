# Root Cause Identifier Schemas

JSON schemas defining input/output contracts for root-cause-identifier.

## Contents

| File | Purpose |
|------|---------|
| `root-cause-identifier.schema.json` | Complete input/output schema |

## Schema Overview

### Input
- `task_id`: Unique identifier
- `problem_statement`: Symptom, context, timeline
- `evidence_available`: Logs, code references, previous occurrences
- `execution_timestamp`: ISO 8601 UTC from orchestrator

### Output (SUCCESS)
- `five_whys_chain`: 3-5 levels with evidence at each
- `root_cause`: Description, actionable flag, category, recurrence risk
- `scamper_recommendations`: 2-5 improvements with effort/impact
- `analysis_metadata`: Evidence quality, alternatives considered

### Output (FAILURE)
- `failure_type`: insufficient_evidence, circular_root_cause, etc.
- `partial_analysis`: Progress made before failure
- `evidence_gaps`: Specific information needed
- `recovery_suggestions`: Paths to resolve failure
