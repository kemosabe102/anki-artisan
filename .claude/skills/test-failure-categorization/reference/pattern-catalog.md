# Pattern Catalog: 12 Failure Heuristics

Reference for test failure categorization patterns with base confidence scores.

---

## APPLICATION_BUG Patterns

### Pattern 1: Assertion Value Mismatch
**Base Confidence**: 0.85
**Signals**:
- `AssertionError` with expected vs actual values
- Values differ but types match
- No test setup issues visible

**Example**:
```
AssertionError: assert 42 == 41
Expected: 42
Actual: 41
```

### Pattern 2: Missing Return Value
**Base Confidence**: 0.80
**Signals**:
- Function returns `None` unexpectedly
- `assert result is not None` failures
- Missing implementation indicators

### Pattern 3: Unexpected Exception Type
**Base Confidence**: 0.75
**Signals**:
- `pytest.raises` caught wrong exception
- Expected `ValueError`, got `TypeError`
- Exception hierarchy mismatch

### Pattern 4: State Corruption
**Base Confidence**: 0.70
**Signals**:
- Object state differs from expected
- Attribute values changed unexpectedly
- Side effects not cleaned up

---

## TEST_BUG Patterns

### Pattern 5: Fixture Misuse
**Base Confidence**: 0.85
**Signals**:
- `fixture 'x' not found`
- Wrong fixture scope causing stale data
- Missing `@pytest.fixture` decorator

### Pattern 6: Mock Configuration Error
**Base Confidence**: 0.80
**Signals**:
- `MagicMock` where real object expected
- `return_value` not set correctly
- `side_effect` misconfigured

### Pattern 7: Assertion Logic Error
**Base Confidence**: 0.75
**Signals**:
- Test passes when it should fail
- Inverted comparison operators
- Wrong variable in assertion

### Pattern 8: Setup/Teardown Failure
**Base Confidence**: 0.70
**Signals**:
- Error in `setup_method` or `teardown`
- Test preconditions not met
- Resource not properly initialized

---

## ENVIRONMENT Patterns

### Pattern 9: Missing Dependency
**Base Confidence**: 0.90
**Signals**:
- `ModuleNotFoundError`
- `ImportError: No module named`
- Package not in environment

### Pattern 10: Resource Unavailable
**Base Confidence**: 0.85
**Signals**:
- `ConnectionRefusedError`
- `FileNotFoundError` for external files
- Database connection failures

### Pattern 11: Permission Denied
**Base Confidence**: 0.80
**Signals**:
- `PermissionError`
- `OSError: [Errno 13]`
- File/directory access issues

---

## FLAKY Patterns

### Pattern 12: Non-Deterministic Failure
**Base Confidence**: 0.65 (requires N-run validation)
**Signals**:
- Same test passes/fails inconsistently
- Timing-dependent assertions
- Order-dependent state

**Validation Required**: Run N times before confirming FLAKY category.

---

## Pattern Matching Algorithm

```python
def match_pattern(error_output: str, stack_trace: str) -> tuple[str, float]:
    """Match failure to pattern, return (category, confidence)."""
    
    # Check ENVIRONMENT patterns first (highest certainty)
    if "ModuleNotFoundError" in error_output:
        return ("ENVIRONMENT", 0.90)
    if "ConnectionRefusedError" in error_output:
        return ("ENVIRONMENT", 0.85)
    if "PermissionError" in error_output:
        return ("ENVIRONMENT", 0.80)
    
    # Check TEST_BUG patterns
    if "fixture" in error_output and "not found" in error_output:
        return ("TEST_BUG", 0.85)
    if "MagicMock" in error_output:
        return ("TEST_BUG", 0.80)
    
    # Check APPLICATION_BUG patterns
    if "AssertionError" in error_output:
        if "==" in error_output or "!=" in error_output:
            return ("APPLICATION_BUG", 0.85)
        return ("APPLICATION_BUG", 0.70)
    
    # Default: needs investigation
    return ("UNKNOWN", 0.50)
```

---

## Quick Reference Table

| Pattern | Category | Base Confidence |
|---------|----------|-----------------|
| Assertion mismatch | APPLICATION_BUG | 0.85 |
| Missing return | APPLICATION_BUG | 0.80 |
| Wrong exception | APPLICATION_BUG | 0.75 |
| State corruption | APPLICATION_BUG | 0.70 |
| Fixture misuse | TEST_BUG | 0.85 |
| Mock config error | TEST_BUG | 0.80 |
| Assertion logic | TEST_BUG | 0.75 |
| Setup/teardown | TEST_BUG | 0.70 |
| Missing dependency | ENVIRONMENT | 0.90 |
| Resource unavailable | ENVIRONMENT | 0.85 |
| Permission denied | ENVIRONMENT | 0.80 |
| Non-deterministic | FLAKY | 0.65* |

*Requires N-run validation
