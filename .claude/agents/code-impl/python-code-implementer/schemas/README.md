# Python Code Implementer Schemas

## Contents

| File | Purpose |
|------|---------|
| `python-code-implementer.schema.json` | Agent output contract (extends base-agent.schema.json) |

## Schema Overview

The python-code-implementer schema defines:

### SUCCESS Output
- `files_modified`: Array of files with path, change_type, lines_changed, description
- `implementation_summary`: Brief summary of changes and approach
- `pre_flight_checks_passed`: Boolean for pre-flight validation
- `standards_compliance`: Coding guidelines, Context7 patterns, ADR compliance, components leveraged
- `self_review_results`: Pass/fail for correctness, readability, maintainability, security, performance
- `tests_created`: Array of test files with coverage areas
- `next_actions`: Recommended orchestrator coordination steps
- `unclear_items_resolved` / `unclear_items_escalated`: Pre-flight resolution tracking

### FAILURE Output
- `failure_type`: One of standards_conflict, file_operation_failure, dependency_missing, scope_boundary_violation, pre_flight_validation_failed, build_failure, test_failure, schema_validation_failed
- `reasons`: Specific failure reasons
- `pre_flight_failures`: Validation patterns that failed
- `partial_results`: Files modified and completed phases before failure
- `recovery_suggestions`: Approaches to resolve with rationale
- `delegation_needed`: Agent to delegate for recovery (debugger, python-code-implementer, researcher-codebase, none)

## Base Schema Reference

This schema extends: `.claude/docs/shared/schemas/base-agent.schema.json`
