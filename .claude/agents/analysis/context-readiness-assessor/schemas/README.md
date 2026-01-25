# Context Readiness Assessor - Schemas

## Overview

This directory contains JSON Schema definitions for context-readiness-assessor input/output contracts.

## Files

| File | Purpose |
|------|---------|
| `context-readiness-assessor.schema.json` | Input/output schema for context quality assessment |

## Schema Summary

### Input Requirements
- `task_id`: Unique identifier
- `intent_analysis`: Output from intent-analyzer (OBSERVE phase)
- `task_description`: Task to assess
- `domain_scope`: Directories/files involved
- `previous_iteration`: (optional) State from prior iteration

### Output States

**SUCCESS** (gate_status = PASS):
- `context_quality_score`: 0.85-1.0
- `component_scores`: All 4 components with rationale
- `ready_for_implementation`: true

**SUCCESS** (gate_status = GATHER_MORE_CONTEXT):
- `context_quality_score`: < 0.85
- `information_gaps`: Remaining gaps with severity
- `ready_for_implementation`: false

**FAILURE** (gate_status = BLOCKED):
- `failure_type`: Why blocked
- `recovery_suggestions`: How to resolve
- `escalation_reason`: Why manual intervention needed
