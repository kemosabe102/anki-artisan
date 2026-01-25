# Test Executor Domain Expertise

**Purpose**: Core domain knowledge for test execution, failure categorization, and test health analysis

---

## Failure Categories

| Category | Description | Examples |
|----------|-------------|----------|
| APPLICATION_BUG | Failure in application code under test | Business logic errors, runtime exceptions |
| TEST_BUG | Failure in test code itself | Fixture errors, assertion logic, test data issues |
| ENVIRONMENT | Infrastructure/configuration issues | Missing dependencies, connection failures |
| FLAKY_TEST | Inconsistent pass/fail without code changes | Timing issues, race conditions, shared state |

---

## Failure Categorization Heuristics (12 Patterns)

### Exception Type Patterns

1. **AssertionError / AssertEqual failed** -> APPLICATION_BUG (0.60 base, context-dependent)
2. **ImportError / ModuleNotFoundError** -> ENVIRONMENT (0.95)
3. **AttributeError in test setup** -> TEST_BUG (0.85)
4. **AttributeError in application code** -> APPLICATION_BUG (0.80)
5. **TypeError in test** -> TEST_BUG (0.70)
6. **TypeError in application** -> APPLICATION_BUG (0.75)

### Environment Patterns

7. **FileNotFoundError / PermissionError** -> ENVIRONMENT (0.85)
8. **ConnectionError / TimeoutError** -> ENVIRONMENT (0.90)

### Flaky Patterns

9. **"sometimes passes" / "timing-dependent"** -> FLAKY_TEST (0.80)
10. **Random/non-deterministic patterns** -> FLAKY_TEST (0.85)

### Exit Code Patterns

11. **Exit code 5** (no tests collected) -> ENVIRONMENT (0.95)
12. **Exit code 2** (test interrupted) -> ENVIRONMENT (0.90)

---

## Confidence Calibration

### Base Confidence Adjustments

| Factor | Adjustment |
|--------|------------|
| Stack trace clearly in app code | +0.15 |
| Stack trace in test code | -0.10 |
| Recent app code changes (git log) | +0.10 |
| Test recently created (<1 week) | -0.10 |
| Test previously passed | +0.15 |

### Confidence Ranges & Actions

| Range | Interpretation | Action |
|-------|----------------|--------|
| 0.80-1.0 | Very Confident | Categorize immediately |
| 0.60-0.79 | Confident | Categorize with notes |
| 0.40-0.59 | Uncertain | Escalate to user |
| 0.00-0.39 | Very Uncertain | MANUAL_REVIEW_NEEDED |

---

## Exit Code Interpretation

| Code | Meaning | Category | Action |
|------|---------|----------|--------|
| 0 | All tests passed | - | Report success |
| 1 | Some tests failed | Varies | Categorize each failure |
| 2 | Test interrupted | ENVIRONMENT | Check timeout/resources |
| 3 | Internal runner error | ENVIRONMENT | Check framework config |
| 4 | Command line error | ENVIRONMENT | Validate test command |
| 5 | No tests collected | ENVIRONMENT | Check paths/discovery |

---

## Test Health Metrics

### Independence Score (0.0-1.0)

Measures whether tests pass in isolation AND together:
- 1.0 = Fully independent (same results isolated vs together)
- <0.8 = Possible test interference
- <0.5 = Significant dependency issues

### Repeatability Score (0.0-1.0)

Measures consistency across N runs:
- 1.0 = Same result every run
- <0.85 = Potentially flaky
- <0.70 = Definitely flaky

### Flaky Test Indicators

- `time.sleep()` calls without justification
- `random.random()` without seed
- Global variables modified in tests
- External service dependencies (not mocked)
- Platform-specific assumptions

---

## Coverage Gap Analysis

### Severity Levels

| Severity | Criteria | Action |
|----------|----------|--------|
| Critical | Core business logic uncovered | Immediate test creation |
| High | Important functions uncovered | High priority |
| Medium | Utility functions uncovered | Normal priority |
| Low | Edge cases, error handlers | Low priority |

---

## Delegation Routing

### By Category

| Category | Next Step | Rationale |
|----------|-----------|-----------|
| APPLICATION_BUG | Investigate and fix logic error in application code | Root cause in app |
| TEST_BUG | Fix test assertions, fixtures, or mocks | Root cause in test |
| ENVIRONMENT | Environment setup required (escalate for user intervention) | Infrastructure issue |
| FLAKY_TEST | Fix test isolation and timing dependencies | Unreliable test |
| Coverage gaps | Generate unit tests for uncovered functions | Missing coverage |

---

## Telemetry Testing Support

For load testing observability infrastructure:

### telemetrygen Usage

- Use for synthetic trace generation to test OTEL Collector/Jaeger
- NOT for code instrumentation (use OpenTelemetry SDK)

### K8s Load Scenarios

| Scenario | Rate | Duration | Total Spans |
|----------|------|----------|-------------|
| baseline | 100/sec | 30s | 3,000 |
| high-throughput | 1,000/sec | 60s | 60,000 |
| spike | 5,000/sec | 30s | 150,000 |

### Success Criteria

- Success rate >= 99% (e.g., 2,970/3,000 spans)
- All spans appear in Jaeger within timeout
- No collector errors in logs

---

## Framework Detection

### Detection Order

1. **pyproject.toml** with `[tool.pytest]` -> pytest
2. **package.json** with jest/mocha in scripts -> jest/mocha
3. **go.mod** with test files -> go test
4. **Default**: pytest (Python), jest (Node.js)

### Command Construction

| Framework | Base Command | Common Flags |
|-----------|--------------|--------------|
| pytest | `uv run pytest` | `-v --cov=packages --maxfail=5` |
| jest | `npm test --` | `--coverage --verbose` |
| go test | `go test` | `-v -cover ./...` |
