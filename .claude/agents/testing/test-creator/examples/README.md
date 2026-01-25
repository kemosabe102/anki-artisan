# examples/ Directory - test-creator

**Purpose**: Concrete usage patterns for delegation and output

---

## Contents

| File | Purpose | Audience |
|------|---------|----------|
| `delegation-examples.md` | How orchestrator delegates | Orchestrator, other agents |

---

## Quick Reference

### Delegation Patterns

**Create tests**:
```
Task(test-creator, "Create unit tests for [file] with [coverage]% coverage")
```

**Analyze coverage**:
```
Task(test-creator, "Analyze test coverage gaps in [directory]")
```

**Fix test bug**:
```
Task(test-creator, "Fix failing test. test_file: [path] failure_category: TEST_BUG")
```

---

## See Also

- **Main agent**: `../test-creator.md`
- **Domain knowledge**: `../docs/domain-expertise.md`
- **Schema**: `../schemas/test-creator.schema.json`
