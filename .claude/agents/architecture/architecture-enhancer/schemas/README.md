# Architecture Enhancer Schemas

JSON Schema definitions for input/output validation.

## Contents

| File | Purpose |
|------|---------|
| `architecture-enhancer.schema.json` | Input/output contract for enhancement operations |

## Schema Overview

The schema defines a two-state output model:

### SUCCESS State
- `file_path`: Path to enhanced plan file
- `placeholders_before`/`after`: Placeholder counts (after should be 0)
- `sections_enhanced`: List of populated sections
- `research_sources_used`: Context7, web, Component Almanac sources
- `architecture_decisions`: Decisions with rationale and alternatives
- `cleanup_tasks_generated`: Boolean for replacement cleanup

### FAILURE State
- `failure_type`: Category (missing_plan_file, context7_failed, etc.)
- `reasons`: Specific failure reasons
- `partial_results`: Any sections enhanced before failure
- `recovery_suggestions`: Approaches to resolve

## Related

- Main agent: `../architecture-enhancer.md`
- Base schema: `../../schemas/base-agent.schema.json`
