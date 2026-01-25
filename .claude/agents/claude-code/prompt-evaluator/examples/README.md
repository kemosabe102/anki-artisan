# Prompt Evaluator Examples

Usage examples demonstrating how to invoke the prompt-evaluator agent.

## Contents

| File | Purpose |
|------|---------|
| `delegation-examples.md` | Orchestrator delegation patterns and expected outputs |

## Quick Example

```
Task(prompt-evaluator, "Evaluate .claude/agents/researcher-external.md with focus=all")
```

## Output Format

All evaluations return structured JSON per `schemas/prompt-evaluator.schema.json` with:
- SUCCESS: Complete evaluation with 7 framework scores
- FAILURE: Partial results with recovery suggestions
