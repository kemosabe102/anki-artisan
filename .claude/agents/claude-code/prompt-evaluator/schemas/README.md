# Prompt Evaluator Schemas

JSON Schema definitions for the prompt-evaluator agent's input/output contract.

## Contents

| File | Purpose |
|------|---------|
| `prompt-evaluator.schema.json` | Complete I/O schema with SUCCESS/FAILURE models |

## Schema Overview

The schema defines:
- **Input**: agent_file_path, schema_file_path (optional), evaluation_focus, execution_timestamp
- **Output (SUCCESS)**: 9 required sections including evaluation_summary, structural_quality, prompt_engineering_quality, token_optimization, testing_strategy, issues, recommended_improvements, anti_patterns_detected, confidence_scores
- **Output (FAILURE)**: failure_type, reasons, partial_results, recovery_suggestions

## Validation

All agent outputs are validated against this schema before delivery. Use `additionalProperties: false` for strict compliance.
