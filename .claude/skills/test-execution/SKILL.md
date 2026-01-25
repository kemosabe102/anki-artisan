---
name: test-execution
description: >
  Use this skill when running tests and analyzing results. Provides execution modes,
  pytest exit code interpretation, test health metrics, and independence validation.
  Trigger keywords: run tests, execute tests, pytest, test results, exit code,
  test health, independence, isolation.
---

# Test Execution Skill

Execute tests systematically with proper isolation and result interpretation.

## Reference Documentation

- **Execution Modes** -> [reference/execution-modes.md](reference/execution-modes.md)
- **Exit Codes** -> [reference/exit-codes.md](reference/exit-codes.md)
- **Independence Validation** -> [reference/independence-validation.md](reference/independence-validation.md)

**Utility Scripts**:
- **Test Runner with Analysis** -> `scripts/run_tests_with_analysis.py <test_path> [--validate-independence]`
  - Parses pytest output with failure extraction
  - Interprets exit codes automatically
  - Optional independence validation for failed tests

---

## Quick Reference: Execution Modes

| Mode | Command | Purpose |
|------|---------|---------|
| Full Suite | `uv run pytest` | Run all tests |
| Single File | `uv run pytest tests/unit/test_auth.py` | Run one module |
| Single Test | `uv run pytest tests/unit/test_auth.py::test_login` | Run one test |
| With Coverage | `uv run pytest --cov=packages` | Measure coverage |
| Verbose | `uv run pytest -v` | Detailed output |

---

## Pytest Exit Codes

| Code | Meaning | Action |
|------|---------|--------|
| 0 | All tests passed | Success |
| 1 | Some tests failed | Investigate failures |
| 2 | Test execution interrupted | Check for keyboard interrupt |
| 3 | Internal error | Check pytest configuration |
| 4 | pytest usage error | Check command syntax |
| 5 | No tests collected | Check test discovery patterns |

---

## Test Health Metrics

### Independence Score
```
Run each test in isolation: pytest test_X.py::test_name
Run full suite: pytest test_X.py

Independence = (isolated_results == suite_results) ? 1.0 : 0.0
```

**Target**: 100% tests pass both isolated and in-suite

### Repeatability Score
```
Run N times: for i in {1..5}; do pytest test_X.py; done

Repeatability = consistent_results / total_runs
```

**Target**: 100% consistent results across runs

---

## Isolated Rerun Protocol

When a test fails:

1. **Rerun in isolation**: `uv run pytest path/to/test.py::test_name -v`
2. **Compare results**: Same failure? Different failure? Pass?
3. **Interpret**:
   - Same failure → Likely real bug
   - Different failure → Possible test interaction
   - Pass → Likely test order dependency or flaky test

---

## Quick Validation Checklist

- [ ] Exit code 0 (all pass)
- [ ] No warnings about unclosed resources
- [ ] Coverage meets threshold (≥80%)
- [ ] No tests skipped unexpectedly
- [ ] Execution time reasonable (<60s for unit tests)
