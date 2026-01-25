---
name: test-generation
description: >
  Use this skill when creating tests for Python code. Provides AAA pattern guidance,
  fixture design taxonomy, mock decision trees, and coverage gap analysis.
  Trigger keywords: create tests, write tests, test generation, AAA pattern,
  fixtures, mocking, coverage, pytest, unit tests.
---

# Test Generation Skill

Create focused, maintainable tests using AAA pattern and strategic mocking.

## Reference Documentation

- **AAA Pattern** -> [reference/aaa-pattern.md](reference/aaa-pattern.md)
- **Fixture Design** -> [reference/fixture-design.md](reference/fixture-design.md)
- **Mock Decision Tree** -> [reference/mock-decision-tree.md](reference/mock-decision-tree.md)

**Utility Scripts**:
- **Coverage Gap Analyzer** -> `scripts/analyze_coverage_gaps.py <module_path>`
  - Identifies untested public interfaces
  - Suggests test cases by category
  - Returns JSON with coverage percentage

---

## Quick Reference: AAA Pattern

```python
def test_<method>_<condition>_<expected_outcome>():
    """Verify <what> when <condition>."""
    # Arrange - Set up test data and dependencies
    user = create_test_user(role="admin")
    
    # Act - Execute the code under test
    result = authorize_action(user, "delete")
    
    # Assert - Verify the outcome
    assert result.allowed is True
```

---

## Test Naming Convention

`test_<method>_<condition>_<expected_result>`

| Component | Example |
|-----------|---------|
| Method | `validate_token` |
| Condition | `when_expired` |
| Expected | `returns_false` |

**Full**: `test_validate_token_when_expired_returns_false`

---

## Mock Decision Tree

```
Should I mock this dependency?

Is it EXTERNAL (API, DB, filesystem)?
  → YES: Mock it

Is it SLOW (>100ms)?
  → YES: Mock it

Is it NON-DETERMINISTIC (time, random)?
  → YES: Mock it

Is it the CODE UNDER TEST?
  → NO: Don't mock it

Otherwise?
  → NO: Use real implementation
```

---

## Fixture Scope Selection

| Scope | Use When | Example |
|-------|----------|---------|
| `function` | Each test needs fresh state | User objects |
| `class` | Tests in class share setup | DB connection |
| `module` | Expensive, read-only resource | Config loading |
| `session` | One-time global setup | Test database schema |

**Default**: Use `function` scope unless you have a specific reason.

---

## Coverage Gap Analysis

1. **Map interfaces**: List all public functions/methods
2. **Check existing tests**: `grep -r "def test_<function>" tests/`
3. **Identify gaps**: Functions without corresponding tests
4. **Prioritize by criticality**:
   - Business logic > Utilities > Logging
   - Public API > Internal helpers

---

## Scenario Categories

| Category | Description | Example |
|----------|-------------|---------|
| Happy path | Normal input, expected output | Valid user login |
| Edge cases | Boundary values, empty input | Empty list, max int |
| Error paths | Invalid input, exceptions | Missing field, null |
| Async | Concurrent, timeout scenarios | Race conditions |
