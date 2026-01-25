# Context Optimizer Schemas

JSON Schema definitions for context-optimizer agent input/output contracts.

## Files

| File | Purpose |
|------|---------|
| `context-optimizer.schema.json` | Input parameters and output structure for context optimization analysis |

## Schema Overview

### Input Parameters

- `analysis_scope`: agents | orchestrator | mcp | full
- `target_agents`: "all" | ["agent1", "agent2"] | "pattern-*"
- `depth_level`: quick | standard | comprehensive
- `focus_areas`: redundancy | structure | compression | tooling | all

### Output Structure

**Success Output**:
- `analysis_summary`: Token counts, targeting mode, optimization potential
- `findings[]`: Category, severity, location, tokens_wasted, description
- `recommendations[]`: Priority (P1-P4), savings, effort, ROI, implementation_steps
- `metrics`: Health scores (redundancy, progressive_disclosure, token_density, overall)
- `implementation_plan`: Phased roadmap with timeline

**Failure Output**:
- `failure_type`: scope_validation_error | file_read_error | insufficient_data | etc.
- `reasons[]`: Specific failure reasons
- `recovery_suggestions[]`: How to resolve and retry
