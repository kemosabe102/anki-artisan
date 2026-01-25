# Python Code Implementer Schema Tests

## Purpose

Validates agent outputs against `python-code-implementer.schema.json` to ensure:
- SUCCESS outputs include all required fields
- Field structures match schema definitions
- FAILURE outputs use valid failure_type enums

## Test Cases

| Test | Type | Validates |
|------|------|-----------|
| `valid_success_output` | Positive | All required SUCCESS fields present |
| `missing_tdd_evidence` | Negative | tdd_evidence is required |
| `invalid_self_review_structure` | Negative | self_review_results must use objects |
| `valid_failure_output` | Positive | FAILURE structure with failure_type |

## Running Tests

```bash
# Manual validation with jsonschema
uv run python -c "
import json
from jsonschema import validate, ValidationError

with open('schemas/python-code-implementer.schema.json') as f:
    schema = json.load(f)
with open('tests/scenarios.json') as f:
    scenarios = json.load(f)

for case in scenarios['test_cases']:
    try:
        validate(case['input'], schema)
        result = 'valid'
    except ValidationError as e:
        result = 'invalid'
    expected = case['expected']
    status = 'PASS' if result == expected else 'FAIL'
    print(f'{status} {case[\"name\"]}: {result} (expected {expected})')
"
```

## Adding New Test Cases

1. Add case to `scenarios.json` with:
   - `name`: Unique identifier
   - `description`: What the test validates
   - `expected`: "valid" or "invalid"
   - `expected_error`: (for invalid) field that should fail
   - `input`: The agent output to validate

2. Run validation to confirm test behaves as expected
