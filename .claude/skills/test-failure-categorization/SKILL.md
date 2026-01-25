---
name: test-failure-categorization
description: >
  Use this skill when categorizing test failures for proper routing and resolution.
  Provides 12 heuristic patterns, 4 failure categories, confidence calibration,
  and delegation recommendations. Trigger keywords: test failure, categorize,
  APPLICATION_BUG, TEST_BUG, ENVIRONMENT, FLAKY, failure analysis.
---

# Test Failure Categorization Skill

Systematically categorize test failures using heuristic pattern matching.

## Reference Documentation

- **Pattern Catalog** -> [reference/pattern-catalog.md](reference/pattern-catalog.md)
- **Confidence Calibration** -> [reference/confidence-calibration.md](reference/confidence-calibration.md)

---

## 4 Failure Categories

| Category | Description | Route To |
|----------|-------------|----------|
| APPLICATION_BUG | Bug in production code | debugger agent |
| TEST_BUG | Bug in test code itself | code-quality agent |
| ENVIRONMENT | Infrastructure/config issue | orchestrator |
| FLAKY_TEST | Intermittent pass/fail | flaky-test-detection skill |

---

## Utility Scripts

**categorize_failure.py** - Automated pattern matching and categorization

```bash
# Analyze pytest output file
python scripts/categorize_failure.py pytest_output.txt

# Read from stdin
pytest tests/ 2>&1 | python scripts/categorize_failure.py --stdin
```

Returns JSON with category, confidence, pattern matched, and recommendation.

---

## Quick Reference: 12 Heuristic Patterns

| # | Pattern | Category | Confidence |
|---|---------|----------|------------|
| 1 | AssertionError | APPLICATION_BUG | 0.60 |
| 2 | ImportError/ModuleNotFoundError | ENVIRONMENT | 0.95 |
| 3 | FixtureNotFound/ScopeMismatch | TEST_BUG | 0.90 |
| 4 | RuntimeError in app code | APPLICATION_BUG | 0.75 |
| 5 | ValueError/TypeError | APPLICATION_BUG | 0.55 |
| 6 | Stack trace in test_*.py only | TEST_BUG | 0.85 |
| 7 | Stack trace in packages/**/*.py | APPLICATION_BUG | 0.85 |
| 8 | Stack trace in fixture function | TEST_BUG | 0.90 |
| 9 | "connection refused", "timeout" | ENVIRONMENT | 0.85 |
| 10 | "fixture not found" | TEST_BUG | 0.90 |
| 11 | "expected X but got Y" + app origin | APPLICATION_BUG | 0.80 |
| 12 | "no module named" | ENVIRONMENT | 0.95 |

---

## Confidence Calibration

Apply adjustments based on context:

| Context | Adjustment |
|---------|------------|
| Stack trace clearly in app code | +0.15 |
| Stack trace in test code | -0.10 |
| Recent app code changes (git) | +0.10 |
| Test recently created (<1 week) | -0.10 |
| Test previously passed consistently | +0.15 |

---

## Confidence Thresholds

| Range | Action |
|-------|--------|
| 0.80-1.0 | Categorize and route immediately |
| 0.60-0.79 | Categorize with explanatory notes |
| 0.40-0.59 | Provide both candidates, ask user |
| < 0.40 | Flag as MANUAL_REVIEW_NEEDED |

---

## Categorization Output Format

```json
{
  "test_name": "test_auth_login_success",
  "category": "APPLICATION_BUG",
  "confidence": 0.85,
  "pattern_matched": "Stack trace in packages/auth/login.py",
  "delegation": "debugger",
  "evidence": {
    "error_type": "AssertionError",
    "stack_trace_location": "packages/auth/login.py:45",
    "recent_changes": true
  }
}
```
