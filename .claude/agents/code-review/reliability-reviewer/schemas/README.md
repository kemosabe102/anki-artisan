# Reliability Reviewer Schemas

## Input Schema

```json
{
  "type": "object",
  "required": ["id", "upstream", "downstream", "upstream_file", "downstream_file"],
  "properties": {
    "id": { "type": "integer" },
    "upstream": { "type": "string" },
    "downstream": { "type": "string" },
    "upstream_file": { "type": "string" },
    "downstream_file": { "type": "string" },
    "data_flow_type": { 
      "type": "string",
      "enum": ["direct", "event", "storage", "api"]
    }
  }
}
```

## Output Schema

Findings are output in markdown table format with:
- ID (hat prefix + number)
- Category (check type)
- Issue (description)
- Severity (CRITICAL/HIGH/MEDIUM/LOW)
- Evidence (file:line)
- Recommendation (action)
