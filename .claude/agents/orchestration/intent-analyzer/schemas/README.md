# Intent Analyzer Schema

JSON Schema for intent-analyzer input/output validation.

## Contents

| File | Purpose |
|------|---------|
| `intent-analyzer.schema.json` | Input/output contract for intent analysis |

## Schema Overview

Extends `base-agent.schema.json` with two-state SUCCESS/FAILURE model.

### SUCCESS Output
- `intents_identified`: Array of parsed intents with type, domain, confidence
- `task_graph`: DAG with nodes (tasks) and edges (dependencies)
- `execution_order`: Parallel groups and critical path
- `implicit_requirements`: Inferred requirements with rationale
- `complexity_estimate`: Hours, sprint points, risk factors
- `clarifications_needed`: Questions for user (non-blocking)
- `delegation_confidence_scores`: DCS components for orchestrator

### FAILURE Output
- `failure_type`: ambiguous_request | insufficient_context | conflicting_intents
- `reasons`: Why analysis failed
- `ambiguities_detected`: Specific ambiguities with interpretations
- `partial_analysis`: Any completed analysis
- `recovery_suggestions`: How to resolve

## Validation

All outputs must validate against this schema before returning to orchestrator.
