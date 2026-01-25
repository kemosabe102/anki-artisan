---
name: flaky-test-detection
description: >
  Use this skill when detecting and diagnosing flaky tests. Provides N-run
  repeatability validation, 15 flakiness indicator patterns, and failure rate
  thresholds. Trigger keywords: flaky test, intermittent, inconsistent, random
  failure, repeatability, non-deterministic.
---

# Flaky Test Detection Skill

Identify and diagnose intermittent test failures using statistical validation.

## Reference Documentation

- **Indicator Patterns** -> [reference/indicator-patterns.md](reference/indicator-patterns.md)

---

## N-Run Repeatability Validation

```bash
# Run test N times (default: 5)
for i in {1..5}; do
  uv run pytest path/to/test.py::test_name -v
done
```

### Failure Rate Classification

| Failure Rate | Classification | Action |
|--------------|----------------|--------|
| 0% (0/N) | STABLE | Not flaky - investigate original failure |
| 1-15% | FLAKY_LOW | Monitor, may be environment-sensitive |
| 16-99% | FLAKY_HIGH | Requires immediate fix |
| 100% | CONSISTENT_FAILURE | Not flaky - real bug |

---

## Utility Scripts

**detect_flakiness.py** - Static analysis and N-run validation

```bash
# Analyze test file for flakiness indicators
python scripts/detect_flakiness.py tests/test_example.py

# Run test N times to validate flakiness
python scripts/detect_flakiness.py --run tests/test_example.py -n 5
```

Returns JSON report with flakiness score, indicators by category, and recommendations.

---

## Quick Reference: 15 Flakiness Indicators

| # | Indicator | Root Cause | Fix |
|---|-----------|------------|-----|
| 1 | Time-dependent assertions | `datetime.now()` | Use frozen time |
| 2 | Random data without seed | `random.choice()` | Set `random.seed()` |
| 3 | File system timing | Race conditions | Use temp directories |
| 4 | Network calls | External dependency | Mock network |
| 5 | Database state | Shared state | Isolate transactions |
| 6 | Thread safety | Race conditions | Add synchronization |
| 7 | Order dependency | Test pollution | Reset state in fixtures |
| 8 | Resource exhaustion | Memory/handles | Proper cleanup |
| 9 | Async timing | Missing await | Add proper waits |
| 10 | Float comparison | Precision issues | Use `pytest.approx()` |
| 11 | Dict ordering | Python < 3.7 assumption | Use sorted() |
| 12 | Environment variables | Missing setup | Mock os.environ |
| 13 | Timezone sensitivity | Server timezone | Use UTC explicitly |
| 14 | Cache state | Stale data | Clear caches |
| 15 | Global state | Singleton mutation | Reset globals |

---

## Detection Protocol

1. **Observe**: Test fails inconsistently
2. **Validate**: Run N times to confirm flakiness
3. **Identify**: Match against 15 indicator patterns
4. **Diagnose**: Examine test code for root cause
5. **Fix**: Apply pattern-specific remediation

---

## Risk Score Calculation

```
Risk_Score = (Failure_Rate × 0.5) + (Blast_Radius × 0.3) + (Frequency_of_Runs × 0.2)
```

| Risk Score | Priority |
|------------|----------|
| > 0.7 | CRITICAL - Fix immediately |
| 0.4-0.7 | HIGH - Fix this sprint |
| 0.2-0.4 | MEDIUM - Schedule fix |
| < 0.2 | LOW - Monitor |

---

## Output Format

```json
{
  "test_name": "test_async_handler_timeout",
  "is_flaky": true,
  "failure_rate": 0.40,
  "runs": 5,
  "outcomes": ["PASS", "FAIL", "PASS", "PASS", "FAIL"],
  "indicators_matched": ["async_timing", "network_calls"],
  "risk_score": 0.65,
  "recommended_fix": "Add explicit timeout and mock network calls"
}
```
