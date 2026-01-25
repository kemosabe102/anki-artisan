# Pytest Exit Codes Reference

## Exit Code Summary

| Code | Name | Meaning | Action |
|------|------|---------|--------|
| 0 | OK | All tests passed | Success - proceed |
| 1 | TESTS_FAILED | Some tests failed | Investigate failures |
| 2 | INTERRUPTED | Execution interrupted | Check for Ctrl+C or timeout |
| 3 | INTERNAL_ERROR | Internal pytest error | Check pytest config |
| 4 | USAGE_ERROR | Command line usage error | Check command syntax |
| 5 | NO_TESTS_COLLECTED | No tests found | Check test discovery |

---

## Exit Code 0: OK

All tests passed successfully.

**Action**: Proceed with confidence.

---

## Exit Code 1: TESTS_FAILED

One or more tests failed.

**Action**:
1. Review failure output
2. Categorize failures (APPLICATION_BUG, TEST_BUG, etc.)
3. Fix or route to appropriate handler

---

## Exit Code 2: INTERRUPTED

Test execution was interrupted before completion.

**Common causes**:
- User pressed Ctrl+C
- Timeout exceeded
- System signal received

**Action**: Rerun tests. If persistent, check for hanging tests.

---

## Exit Code 3: INTERNAL_ERROR

Pytest encountered an internal error.

**Common causes**:
- Plugin compatibility issues
- Corrupt cache
- Python version mismatch

**Action**:
1. Clear pytest cache: `rm -rf .pytest_cache`
2. Check pytest and plugin versions
3. Review pytest.ini/pyproject.toml

---

## Exit Code 4: USAGE_ERROR

Invalid command line arguments.

**Common causes**:
- Misspelled flags
- Invalid option combinations
- Missing required arguments

**Action**: Review command syntax with `pytest --help`.

---

## Exit Code 5: NO_TESTS_COLLECTED

Pytest ran but found no tests.

**Common causes**:
- Test file naming (must be `test_*.py` or `*_test.py`)
- Test function naming (must start with `test_`)
- Wrong directory
- Import errors preventing collection

**Action**:
1. Check file/function naming conventions
2. Verify path exists
3. Run with `-v` to see collection details
4. Check for import errors: `pytest --collect-only`
