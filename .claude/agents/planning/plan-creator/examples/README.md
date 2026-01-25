# Plan Creator Examples

Example invocations and delegation patterns for the plan-creator agent.

## Contents

| Document | Purpose |
|----------|---------|
| `delegation-examples.md` | Orchestrator invocation patterns |

## Quick Reference

### Basic Invocation
```
/plan docs/01-planning/specifications/my-feature/SPEC.md
```

### Phase-Filtered Invocation
```
/plan docs/01-planning/specifications/my-feature/SPEC.md --phase=1
```

### Expected Output
```json
{
  "status": "SUCCESS",
  "output_files": {
    "plan_json": "/path/to/my-feature-PLAN.json"
  },
  "next_step": "/tasks /path/to/my-feature-PLAN.json"
}
```
