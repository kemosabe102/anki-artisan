# Backtest Schemas

JSON Schema definitions for backtest command data structures.

## Files

| Schema | Validates | Usage |
|--------|-----------|-------|
| `run-manifest.schema.json` | Run output manifest | Validate completed backtest runs |
| `checkpoint.schema.json` | Checkpoint state | Validate/recover interrupted runs |
| `dashboard.schema.json` | Performance dashboard | 35 metrics across 6 dimensions with historical comparison |

## Validation

Use these schemas to validate JSON files programmatically:

```python
import json
import jsonschema

with open("run-manifest.schema.json") as f:
    schema = json.load(f)

with open("path/to/run-manifest.json") as f:
    data = json.load(f)

jsonschema.validate(data, schema)
```
