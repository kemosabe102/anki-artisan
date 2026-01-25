# TDD Workflow for Python Code Implementer

## Core Philosophy

**Tests define the implementation contract.** Before writing any production code, you MUST:

> **Authoritative Source**: For schema enforcement and HALT conditions, see the main agent definition at `python-code-implementer.md` > Enforcement Gates > TDD-First Gate.

1. **Find existing tests** - Search for tests related to the implementation task
2. **Use or create tests FIRST** - If tests exist, understand them. If not, write them before implementation
3. **Build code around tests** - Implementation follows test requirements, not the other way around

## Core Principles

- **Simple tests, well-designed code** - Simple test requirements lead to clean, modular implementations
- **Code testability is a primary design goal** - If code is hard to test, it's poorly designed
- **Tests are the specification** - Tests document expected behavior more precisely than prose

## Why TDD Works

- Prevents over-engineering (you only build what tests require)
- Forces modular design (testable code = loosely coupled code)
- Makes refactoring safe (comprehensive test coverage catches regressions)
- Clarifies requirements (writing tests reveals ambiguities early)

---

## TDD Decision Tree

```
Task Received
    ↓
Search for existing tests (Pre-Flight step 9)
    ↓
┌─────────────────────────────────────────┐
│         Tests exist for this task?       │
└─────────────────────────────────────────┘
        ↓ YES                    ↓ NO
   Read & understand        Create tests FIRST
   test expectations        (see Test Creation below)
        ↓                         ↓
   Tests define the          Tests define the
   implementation            implementation
   contract                  contract
        ↓                         ↓
   Implement code to         Implement code to
   pass existing tests       pass new tests
        ↓                         ↓
   Run tests, verify         Run tests, verify
   all pass                  all pass
        ↓                         ↓
   Refactor if needed        Refactor if needed
   (tests ensure safety)     (tests ensure safety)
```

---

## Test Discovery Patterns

Use these patterns to find existing tests:

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

## Test Creation Guidelines (When Tests Don't Exist)

**Before writing ANY implementation code:**

1. **Identify test file location**: `tests/unit/test_<module>.py` or `tests/integration/test_<feature>.py`
2. **Write minimal, focused tests** that specify expected behavior:
   - One test per behavior/requirement
   - Use AAA pattern (Arrange-Act-Assert)
   - Keep assertions simple and specific
3. **Run tests to verify they fail** (Red phase)
4. **Only then** proceed to implementation (Green phase)
5. **Refactor** with confidence (tests catch regressions)

## Test Design Principles

- **Simple tests → Well-designed code**: If a test is complex, the design needs work
- **Test public interfaces**: Focus on inputs/outputs, not internals
- **Mock external dependencies**: Keep tests fast and isolated
- **Name tests descriptively**: `test_<function>_<scenario>_<expected_result>`

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

## Interaction With Other Agents

- **TDD-First**: If tests don't exist for the task, create them BEFORE implementation (not after)
- Defer **comprehensive test suite design** to test-creator agent for complex scenarios
- If you uncover design gaps or spec contradictions, **stop** and emit a "Standards/Spec Gap Note"
