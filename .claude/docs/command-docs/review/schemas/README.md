# Review Command Schemas

JSON schemas for structured output from the `/review` command.

## Files

| File | Purpose |
|------|---------|
| `review.schema.json` | Complete finding structure schema |

## Schema Categories

- **Finding Schema** - Structure of individual review findings
- **Investigation Trail** - Research history for confidence-driven investigation
- **Report Structure** - Overall review report format

## Usage

The finding schema is used by:
- Review agents to structure their output
- Report generation to validate findings
- Downstream consumers (CI/CD, dashboards) for parsing
