# Task Creator Schema

## Files

| File | Purpose |
|------|---------|
| `task-creator.schema.json` | Input/output contract for task generation |

## Schema Overview

The task-creator schema extends `base-agent.schema.json` with:

### Input Schema
- `task_id` - Unique task identifier from orchestrator
- `execution_timestamp` - ISO 8601 UTC timestamp
- `plan_file_path` - Absolute path to component-PLAN.md
- `spec_file_path` - Absolute path to parent SPEC.md
- `task_id_offset` - Starting offset for task numbering
- `component_context` - Component name, sprint points, requirements

### Success Output
- `tasks_file` - Path to generated tasks.md
- `json_file` - Path to generated TASKS.json
- `task_count` - Total tasks generated
- `tasks_generated` - Array of task objects with T-IDs
- `review_groups` - Review checkpoint groups with metadata
- `dependency_graph` - Task dependency relationships
- `parallel_execution_groups` - Parallelizable task sets
- `sprint_metadata` - Task breakdown by type
- `agent_assignments` - Task counts per agent
- `validation_checklist` - Validation results
- `unclear_items` - Ambiguous elements requiring clarification

### Failure Output
- `failure_type` - Category of failure
- `reasons` - Specific failure reasons
- `missing_sections` - Plan sections that were incomplete
- `partial_results` - Tasks generated before failure
- `recovery_suggestions` - Approaches to resolve failure

## Human-Readable Documentation

See `docs/04-guides/task-creator/tasks-schema.md` for detailed schema documentation with examples.
