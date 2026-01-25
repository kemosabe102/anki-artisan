# Grafana Dashboard Builder Schemas

JSON Schema definitions for input/output contracts.

## Contents

| Schema | Purpose |
|--------|---------|
| `grafana-dashboard-builder.schema.json` | Input/output contract for dashboard operations |

## Schema Overview

The schema extends `base-agent.schema.json` with a two-state model:

### SUCCESS Output
- `dashboard_json_path`: Path to generated dashboard JSON
- `configmap_yaml_path`: Path to ConfigMap YAML
- `dashboard_uid`: Unique dashboard identifier
- `panel_count`: Number of panels created
- `framework_applied`: RED, USE, Four Golden Signals, or Custom
- `deployment_instructions`: k8s-deployment delegation details

### FAILURE Output
- `failure_type`: One of 5 categories (prometheus_connectivity_error, invalid_intent, missing_metrics, promql_syntax_error, datasource_not_found)
- `reasons`: Array of failure reason strings
- `proposed_next_steps`: Recommended recovery actions

## Operation Types

| Operation | Required Input | Output |
|-----------|---------------|--------|
| `create_from_intent` | intent_text | Dashboard JSON + ConfigMap |
| `import_enhance` | dashboard_source | Enhanced dashboard JSON |
| `modify_panel` | dashboard_path, panel ID | Modified dashboard JSON |
| `validate_dashboard` | dashboard_path, validation_level | Validation report |
