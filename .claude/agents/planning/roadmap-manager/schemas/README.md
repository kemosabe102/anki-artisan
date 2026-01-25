# Roadmap Manager Schema

JSON Schema definition for roadmap-manager agent input/output contracts.

## Contents

| File | Purpose |
|------|---------|
| `roadmap-manager.schema.json` | Complete schema for all 7 operation types with SUCCESS/FAILURE response structures |

## Schema Overview

- **Extends**: `base-agent.schema.json` (two-state SUCCESS/FAILURE model)
- **Operations**: update_roadmap_status, manage_sprint_progress, apply_ai_best_practices, automate_sprint_transition, validate_cross_references, generate_health_metrics, create_roadmap
- **Validation**: All outputs must validate against this schema
