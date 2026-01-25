# PromQL Query Builder - Schemas

JSON Schema definitions for input/output contracts.

## Contents

| Schema | Purpose |
|--------|---------|
| [promql-query-builder.schema.json](./promql-query-builder.schema.json) | Input/output contract for all PromQL operations |

## Schema Structure

The schema defines a two-state model (SUCCESS/FAILURE) with:

### Input Requirements
- `task_id`: Unique identifier
- `operation_type`: construct_query | validate_query | optimize_query | generate_recording_rules | discover_metrics
- `intent_description`: Natural language goal
- `execution_timestamp`: ISO 8601 UTC

### Success Output
- `constructed_query`: Validated PromQL string
- `query_metadata`: Labels, rate_interval, cardinality estimate
- `clarifying_questions_asked`: OODA questions with assumed answers
- `validation_report`: Syntax, metrics existence, performance

### Failure Output
- `failure_type`: prometheus_connectivity_error | invalid_promql_syntax | metric_not_found | high_cardinality_detected | ambiguous_intent
- `recovery_suggestions`: Actionable steps to resolve
- `partial_results`: Any work completed before failure
