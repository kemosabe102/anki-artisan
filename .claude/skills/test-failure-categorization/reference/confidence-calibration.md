# Confidence Calibration

Reference for adjusting base confidence scores based on contextual factors.

---

## Calibration Formula

```
Final_Confidence = Base_Confidence × (1 + Σ Adjustments)
```

Cap at 0.95 maximum, floor at 0.30 minimum.

---

## Positive Adjustments (+)

### Evidence Strength (+0.05 to +0.15)

| Factor | Adjustment |
|--------|------------|
| Error message explicitly states cause | +0.15 |
| Stack trace points to single location | +0.10 |
| Multiple signals converge | +0.10 |
| Similar failure in test history | +0.05 |

### Pattern Clarity (+0.05 to +0.10)

| Factor | Adjustment |
|--------|------------|
| Exact match to known pattern | +0.10 |
| Clear category indicators | +0.05 |
| No conflicting signals | +0.05 |

### Context Support (+0.05 to +0.10)

| Factor | Adjustment |
|--------|------------|
| Recent code change in failed area | +0.10 |
| Known problematic module | +0.05 |
| Test has failed before with same error | +0.05 |

---

## Negative Adjustments (-)

### Evidence Weakness (-0.05 to -0.20)

| Factor | Adjustment |
|--------|------------|
| Generic error message | -0.10 |
| No stack trace available | -0.15 |
| Multiple possible causes | -0.10 |
| Error in third-party code | -0.05 |

### Pattern Ambiguity (-0.05 to -0.15)

| Factor | Adjustment |
|--------|------------|
| Matches multiple patterns | -0.15 |
| Partial pattern match only | -0.10 |
| Conflicting signals present | -0.10 |

### Context Uncertainty (-0.05 to -0.10)

| Factor | Adjustment |
|--------|------------|
| No recent changes to area | -0.05 |
| First time seeing this failure | -0.05 |
| Complex test setup | -0.10 |

---

## Category-Specific Calibration

### APPLICATION_BUG Calibration

**Increase confidence when**:
- Assertion clearly shows business logic error
- Code under test recently modified
- Error in core application module

**Decrease confidence when**:
- Error could be test expectation issue
- Mock might be returning wrong value
- Unclear what "correct" behavior should be

### TEST_BUG Calibration

**Increase confidence when**:
- Error in test file, not application code
- Fixture/mock mentioned in error
- Test recently modified

**Decrease confidence when**:
- Error originates in application code
- Test logic appears correct
- Similar tests pass

### ENVIRONMENT Calibration

**Increase confidence when**:
- Import/connection error explicit
- Works locally, fails in CI
- External resource clearly involved

**Decrease confidence when**:
- Might be test/app code issue
- Resource exists but may be misconfigured
- Partial environment setup

### FLAKY Calibration

**Increase confidence when**:
- Multiple runs show inconsistent results
- Timing-related code involved
- Parallel test execution

**Decrease confidence when**:
- Only failed once
- No timing/async code
- Tests run sequentially

---

## Decision Thresholds

| Confidence | Action |
|------------|--------|
| ≥ 0.85 | Proceed with categorization |
| 0.70 - 0.84 | Proceed with caveat |
| 0.50 - 0.69 | Request additional investigation |
| < 0.50 | Escalate to human review |

---

## Calibration Examples

### Example 1: High Confidence APPLICATION_BUG

```
Error: AssertionError: assert calculate_tax(100) == 10
       assert 8 == 10
```

- Base confidence: 0.85 (assertion mismatch)
- +0.10 (clear expected vs actual)
- +0.05 (single location)
- **Final: 0.95 (capped)**

### Example 2: Medium Confidence TEST_BUG

```
Error: AttributeError: 'MagicMock' has no attribute 'save'
```

- Base confidence: 0.80 (mock config)
- -0.10 (could be app expecting wrong type)
- +0.05 (mock clearly mentioned)
- **Final: 0.75**

### Example 3: Low Confidence FLAKY

```
Error: TimeoutError after 30s
(First occurrence)
```

- Base confidence: 0.65 (non-deterministic)
- -0.15 (only failed once)
- -0.05 (first time seeing)
- **Final: 0.45 → Needs N-run validation**

---

## Calibration Checklist

Before finalizing confidence:

- [ ] Reviewed all positive factors
- [ ] Applied relevant negative adjustments
- [ ] Checked for conflicting signals
- [ ] Verified against decision thresholds
- [ ] Considered need for additional investigation
