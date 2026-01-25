# TDD Workflow Reference

## Core Philosophy

**Tests define the implementation contract.** Before writing any production code:

1. **Find existing tests** - Search for tests related to the implementation task
2. **Use or create tests FIRST** - If tests exist, understand them. If not, write them before implementation
3. **Build code around tests** - Implementation follows test requirements

## Why TDD Works

- Prevents over-engineering (build only what tests require)
- Forces modular design (testable code = loosely coupled code)
- Makes refactoring safe (comprehensive test coverage catches regressions)
- Clarifies requirements (writing tests reveals ambiguities early)

---

## TDD Decision Tree

```
Task Received
    |
Search for existing tests
    |
+---------------------------+
|   Tests exist for task?   |
+---------------------------+
    | YES              | NO
    v                  v
Read & understand    Create tests FIRST
test expectations    
    |                  |
    v                  v
Tests define the     Tests define the
implementation       implementation
contract             contract
    |                  |
    v                  v
Implement code to    Implement code to
pass existing tests  pass new tests
    |                  |
    v                  v
Run tests, verify    Run tests, verify
all pass             all pass
```

---

## Test Discovery Patterns

```python
# Search by module name
Grep("test.*<module_name>", path="tests/")

# Search by feature
Glob("tests/**/*<feature>*.py")

# Search by function name
Grep("def test_<function_name>", path="tests/")
```

**Document findings**: `existing_tests: [list]` or `tests_needed: true`

---

## Test Creation Guidelines

**Before writing ANY implementation code:**

1. **Identify test file location**: `tests/unit/test_<module>.py`
2. **Write minimal, focused tests** with AAA pattern (Arrange-Act-Assert)
3. **Run tests to verify they fail** (Red phase)
4. **Only then** proceed to implementation (Green phase)
5. **Refactor** with confidence (tests catch regressions)

---

## Example TDD Cycle

```python
# 1. Write failing test FIRST
def test_calculate_total_with_discount_returns_reduced_price():
    # Arrange
    items = [{"price": 100}, {"price": 50}]
    discount = 0.1
    
    # Act
    result = calculate_total(items, discount)
    
    # Assert
    assert result == 135.0  # (100 + 50) * 0.9

# 2. Run test - it fails (function doesn't exist)
# 3. Implement minimal code to pass
# 4. Run test - it passes
# 5. Refactor if needed (test ensures safety)
```

---

## Test Design Principles

| Principle | Description |
|-----------|-------------|
| Simple tests -> Well-designed code | If a test is complex, the design needs work |
| Test public interfaces | Focus on inputs/outputs, not internals |
| Mock external dependencies | Keep tests fast and isolated |
| Descriptive names | `test_<function>_<scenario>_<expected_result>` |
