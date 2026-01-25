# Test Generation Expertise for test-creator

**Purpose**: Core domain knowledge for creating high-quality, maintainable test suites

---

## 4-Phase Workflow

### Phase 1: Analyze Code Under Test (5-10 min)

**Actions**:
- Read source files with Read tool
- Identify components (classes, functions, methods)
- Map dependencies (external APIs, databases, file I/O)
- Find untested paths using Grep on tests/**
- Assess complexity (unit vs. integration)

**Key Questions**:
- What are the public interfaces?
- What external dependencies exist?
- What are the edge cases and error paths?

### Phase 2: Design Test Strategy (5-10 min)

**Actions**:
- Enumerate scenarios (happy path, edge cases, errors)
- Plan fixtures (reusable setup with cleanup)
- Apply mock decision tree
- Structure tests (single/parametrized/class-based)
- Verify independence (no shared state)

**Scenario Categories**:
| Category | Examples |
|----------|----------|
| Happy path | Normal input, expected output |
| Edge cases | Empty input, boundary values, large data |
| Error paths | Invalid input, missing dependencies, exceptions |
| Async behavior | Concurrent operations, timeouts |

### Phase 3: Generate Test Files (10-20 min)

**Actions**:
- Create tests/unit/test_*.py or tests/integration/test_*.py
- Import dependencies (pytest, mocks, source code)
- Define fixtures with proper cleanup
- Write test functions following AAA pattern
- Add docstrings explaining validation purpose

### Phase 4: Verify Generation (5 min)

**Actions**:
- Delegate to test-executor for execution
- Review results (syntax, logic correctness)
- Assess coverage (meaningful, not just line count)
- Document design decisions (rationale)

---

## AAA Pattern Details

### Structure

```python
def test_function_condition_outcome():
    """Verify [behavior] when [condition]."""
    # Arrange
    input_data = create_test_input()
    expected = "expected_result"
    
    # Act
    result = function_under_test(input_data)
    
    # Assert
    assert result == expected
```

### Rules
- **Arrange**: Set up preconditions, create test data
- **Act**: Single action being tested (one line ideally)
- **Assert**: Verify outcome (single logical assertion)
- **Comments**: Always include # Arrange, # Act, # Assert

### Naming Convention
`test_<method>_<condition>_<outcome>`

Examples:
- `test_parse_empty_string_returns_none`
- `test_validate_invalid_email_raises_error`
- `test_calculate_large_input_handles_overflow`

---

## Fixture Design

### Scope Selection

| Scope | Use When | Cleanup |
|-------|----------|---------|
| `function` | Isolated per test (default) | Automatic |
| `class` | Shared across class methods | End of class |
| `module` | Expensive setup, read-only | End of module |
| `session` | Very expensive, truly global | End of session |

### Best Practices

- Use `tmp_path` for file operations (automatic cleanup)
- Prefer `function` scope unless setup is expensive
- Never share mutable state between tests
- Use `yield` for fixtures needing cleanup

```python
@pytest.fixture
def temp_config_file(tmp_path):
    """Create temporary config file."""
    config = tmp_path / "config.json"
    config.write_text('{"key": "value"}')
    yield config
    # Cleanup automatic with tmp_path
```

---

## Mock Decision Tree

### When to Mock

```
Is it external (API, DB, filesystem)?
    YES → Mock it
    NO ↓
Is it slow (>100ms)?
    YES → Mock it
    NO ↓
Is it non-deterministic (time, random)?
    YES → Mock it
    NO → Use real object
```

### Mock Types

| Type | Use Case | Example |
|------|----------|---------|
| `MagicMock` | General purpose | `mock_api = MagicMock()` |
| `patch` | Replace module attribute | `@patch('module.function')` |
| `AsyncMock` | Async functions | `mock_async = AsyncMock()` |
| `PropertyMock` | Properties | `type(obj).prop = PropertyMock(return_value=x)` |

### Documentation Requirement
Always document WHY you're mocking in test docstring:

```python
def test_fetch_handles_timeout(mock_api):
    """Verify timeout handling.
    
    Mock rationale: External API call would be slow and flaky in tests.
    """
```

---

## Coverage Analysis

### Gap Identification Process
1. Run Grep for existing test files: `tests/**/test_*.py`
2. Map tested functions to source functions
3. Identify untested public interfaces
4. Prioritize by criticality (business logic > utilities)

### Criticality Assessment

| Priority | Characteristics | Action |
|----------|----------------|--------|
| Critical | Business logic, security, data integrity | Test immediately |
| High | Core functionality, frequent use | Test soon |
| Medium | Utilities, helpers | Test when time allows |
| Low | Logging, debug code | Optional |

---

## Quick Reference Checklist

Before delivering tests, verify:

- [ ] All tests follow AAA pattern with comments
- [ ] Test names follow `test_method_condition_outcome`
- [ ] Fixtures use appropriate scope
- [ ] Mocks documented with rationale
- [ ] No shared mutable state between tests
- [ ] Coverage target (80%+) addressed
- [ ] Tests delegated to test-executor (not run by you)
