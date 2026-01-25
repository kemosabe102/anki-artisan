# Doc Reference Optimizer - Schemas

This directory contains the JSON schema for the doc-reference-optimizer agent.

## Contents

| File | Purpose |
|------|---------|
| `doc-reference-optimizer.schema.json` | Input/output contract for agent |

## Schema Overview

The schema defines:

- **Input**: Agent name, optional sections, optimization depth, execution timestamp
- **Output (SUCCESS)**: Analysis summary, optimization opportunities, documentation gaps
- **Output (FAILURE)**: Failure type, reasons, partial results, recovery suggestions

## Key Structures

### optimization_opportunities[]
- section, current_location, current_tokens
- optimization_strategy: reference_existing | extend_base | create_new | keep_inline
- documentation_match with overlap_percentage
- savings, savings_metadata, confidence, recommendation

### documentation_gaps[]
- gap_description, content_pattern, affected_agents
- total_savings, suggested_doc_path, confidence

## Validation

Schema follows JSON Schema Draft 07. Validates:
- Required fields presence
- Enum value constraints
- Numeric ranges (confidence 0-1, overlap 0-100)
