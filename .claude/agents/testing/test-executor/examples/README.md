# examples/ Directory

**Purpose**: Concrete usage patterns showing how test-executor is called and what it produces

---

## Contents

| File | Purpose |
|------|---------|
| `delegation-examples.md` | How orchestrator delegates to test-executor |

---

## Quick Reference

### Basic Test Execution
```
Task(test-executor, "Run tests in tests/unit/ and categorize any failures")
```

### Fix Failing Tests
```
Task(test-executor, "Fix failing tests in tests/unit/test_auth.py using 3-attempt OODA loop")
```

### Coverage Analysis
```
Task(test-executor, "Run tests with coverage and identify gaps in packages/core/")
```

---

## See Also

- **Main agent**: `../test-executor.md`
- **Schema**: `../schemas/test-executor.schema.json`
- **Domain knowledge**: `../docs/`
