# Debugger Output Templates

## RCA Record

```markdown
**Baseline**: `pytest tests/test_calc.py::test_divide_by_zero` fails with ZeroDivisionError

**Hypothesis**: divide() missing zero check validation

**Experiment**: Created test harness in .claude/debug/ with boundary conditions

**Observation**: ZeroDivisionError raised without graceful handling

**5 Whys**:
1. Why crash? → No zero check
2. Why no check? → Assumed valid inputs
3. Why assumed? → No error handling in design
4. Why no error handling? → Spec didn't require it
5. Why spec incomplete? → Edge cases not considered

**Root Cause**: Missing input validation due to incomplete specification

**Fix**: Added zero check in divide() with ValueError

**Verification**: All tests pass, no regressions. Added regression test.
```

---

## Fix Summary

```markdown
**Files Changed**: src/calculator.py, tests/test_calculator.py

**Change Description**: Added zero validation guard in divide() function

**Rationale**: Addresses root cause of missing input validation

**Minimal Fix**: Yes (single guard statement + test)

**Verification**:
- Original failing test: ✅ PASS
- Regression suite: ✅ 47/47 PASS
- New regression guard: test_divide_by_zero_raises_value_error
```

---

## JSON Output Format

```json
{
  "status": "SUCCESS",
  "agent": "debugger",
  "operation_type": "debug",
  "confidence": 0.92,
  "summary": "Fixed division by zero using 5 Whys RCA",
  "agent_specific_output": {
    "bug_reproduced": true,
    "hypothesis": "divide() missing zero check validation",
    "experiment_method": "test_harness",
    "hypothesis_confirmed": true,
    "root_cause_analysis": {
      "baseline": "pytest tests/test_calc.py::test_divide_by_zero fails",
      "observation": "ZeroDivisionError raised without graceful handling",
      "five_whys": [
        "Why crash? → No zero check",
        "Why no check? → Assumed valid inputs",
        "Why assumed? → No error handling in design"
      ],
      "root_cause": "Missing input validation"
    },
    "fix_applied": true,
    "fix_summary": {
      "files_changed": ["src/calculator.py"],
      "change_description": "Added zero validation guard",
      "rationale": "Addresses missing input validation"
    },
    "verification_results": {
      "failing_test_passes": true,
      "regression_tests_passed": true,
      "new_regression_tests": ["test_divide_by_zero_raises_value_error"]
    }
  }
}
```

---

## Failure Output Format

```json
{
  "status": "FAILURE",
  "agent": "debugger",
  "operation_type": "debug",
  "confidence": 0.65,
  "summary": "Cannot reproduce issue after 3 attempts",
  "failure_details": {
    "failure_type": "cannot_reproduce",
    "reasons": [
      "Test passes consistently in local environment",
      "CI environment differs in PostgreSQL version"
    ],
    "hypotheses_attempted": [
      {
        "hypothesis": "Race condition in async handler",
        "result": "refuted",
        "evidence": "Added locks, issue persists"
      }
    ],
    "recovery_suggestions": [
      {
        "approach": "Request CI environment access",
        "rationale": "Debug directly in failing environment",
        "estimated_effort": "2-4 hours"
      }
    ],
    "escalation_needed": true
  }
}
```
