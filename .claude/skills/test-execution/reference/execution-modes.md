# Test Execution Modes Reference

## Mode Overview

| Mode | Purpose | When to Use |
|------|---------|-------------|
| Full Suite | Run all tests | Before commit, CI/CD |
| Single File | Run one module | Developing specific feature |
| Single Test | Run one test | Debugging specific failure |
| Coverage | Measure coverage | Quality gates |
| Verbose | Detailed output | Investigating failures |

---

## Full Suite Execution

```bash
# Run all tests
uv run pytest

# Run all tests with output
uv run pytest -v

# Run with coverage
uv run pytest --cov=packages --cov-report=term-missing
```

**Use when**: Final validation before commit or in CI/CD pipeline.

---

## Single File Execution

```bash
# Run specific test file
uv run pytest tests/unit/test_auth.py

# Run specific directory
uv run pytest tests/unit/

# Run with pattern match
uv run pytest tests/unit/test_auth*.py
```

**Use when**: Developing or debugging specific module.

---

## Single Test Execution

```bash
# Run specific test function
uv run pytest tests/unit/test_auth.py::test_login_success

# Run specific test class
uv run pytest tests/unit/test_auth.py::TestLoginFlow

# Run specific method in class
uv run pytest tests/unit/test_auth.py::TestLoginFlow::test_valid_credentials
```

**Use when**: Debugging specific test failure.

---

## Coverage Mode

```bash
# Basic coverage
uv run pytest --cov=packages

# Coverage with missing lines
uv run pytest --cov=packages --cov-report=term-missing

# Coverage with HTML report
uv run pytest --cov=packages --cov-report=html

# Coverage with minimum threshold
uv run pytest --cov=packages --cov-fail-under=80
```

**Use when**: Measuring test coverage for quality gates.

---

## Additional Useful Flags

| Flag | Purpose |
|------|---------|
| `-v` | Verbose output |
| `-vv` | Very verbose output |
| `-x` | Stop on first failure |
| `-s` | Show print statements |
| `--tb=short` | Shorter tracebacks |
| `--tb=long` | Full tracebacks |
| `-k "pattern"` | Run tests matching pattern |
| `--lf` | Run last failed tests |
| `--ff` | Run failed tests first |
| `-n auto` | Parallel execution (pytest-xdist) |
