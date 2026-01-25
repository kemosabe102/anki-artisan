# Delegation Examples for test-creator

**Purpose**: Show orchestrator and other agents how to delegate tasks

---

## When to Delegate to This Agent

### Trigger Conditions

Delegate to `test-creator` when:
- User asks to "create tests", "generate tests", "write tests"
- Coverage gaps need to be identified
- Test strategy design is needed
- Untested code needs test files

### NOT This Agent

Do NOT delegate when:
- Tests need to be **run** → Use `test-executor`
- Application bugs revealed by tests → Use `debugger`
- Pre-commit test validation → Use `test-executor`

---

## Basic Delegation Pattern

### Create Tests

**Orchestrator says**:
```
Task(test-creator, "Create unit tests for packages/core/validator.py with 80%+ coverage")
```

**Agent returns** (success):
```json
{
  "status": "SUCCESS",
  "agent": "test-creator",
  "confidence": 0.9,
  "agent_specific_output": {
    "tests_created": ["tests/unit/test_validator.py"],
    "test_patterns_applied": ["AAA pattern", "pytest-mock for file I/O"],
    "test_strategy": {
      "approach": "unit-first",
      "test_types": ["unit", "edge cases"],
      "coverage_achieved": 85,
      "next_steps": ["Execute with test-executor"]
    }
  }
}
```

---

## Complex Delegation Pattern

### With Context

**Orchestrator says**:
```
Task(test-creator, "Create unit tests for packages/core/auth.py. 
Context: Uses JWT tokens, external OAuth provider.
Constraints: Mock all external API calls.
Coverage target: 90%.")
```

**Required context**:
- `source_files`: Files to test
- `test_type`: unit or integration
- `coverage_target`: Percentage (default 80%)

---

## Analyze Coverage Mode

**Orchestrator says**:
```
Task(test-creator, "Analyze test coverage gaps in packages/core/")
```

**Agent returns**:
```json
{
  "status": "SUCCESS",
  "agent": "test-creator",
  "confidence": 0.85,
  "agent_specific_output": {
    "coverage_gaps": [
      {
        "file": "packages/core/validator.py",
        "function": "validate_schema",
        "severity": "critical",
        "recommendation": "Add edge case tests for malformed input"
      }
    ],
    "test_strategy": {
      "approach": "gap-driven",
      "test_types": ["unit", "edge cases"],
      "remaining_gaps": 3
    }
  }
}
```

---

## Fix Test Bug Mode

**Orchestrator says**:
```
Task(test-creator, "Fix failing test.
test_file: tests/unit/test_parser.py
test_name: test_parse_empty_returns_none
failure_category: TEST_BUG
error_message: AssertionError: expected None, got ''")
```

**Note**: Only accepts `TEST_BUG` category. Application bugs go to `debugger`.

---

## Multi-Agent Coordination

### Upstream Agents

| Agent | Provides | Example |
|-------|----------|---------|
| `python-code-implementer` | Implementation context | New module to test |
| `debugger` | TEST_BUG delegation | Test code needing repair |

### Downstream Agents

| Agent | Uses | For |
|-------|------|-----|
| `test-executor` | Test files | Validation execution |
| `debugger` | Failure reports | App bug fixes |

---

## Error Handling

### Retry Conditions
- `confidence < 0.5` → Provide more context
- `failure_type: "insufficient_context"` → Add specifications

### Escalation Conditions
- 2+ retries failed
- Expected behavior unclear
- User specification needed
