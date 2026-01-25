# Gate Criteria

**Purpose**: Define pass/fail thresholds for integration review.

---

## Gate Status Definitions

| Status | Meaning | Action |
|--------|---------|--------|
| **PASS** | All integration points validated | Proceed to `/git` |
| **PASS_WITH_CONDITIONS** | Minor issues found | Review findings, proceed with caution |
| **FAIL** | Critical issues blocking PR | Must fix before PR |
| **SKIPPED** | No integration pairs found | Single-component feature, no review needed |

---

## Decision Matrix

### Standard Mode

| Condition | Gate Result |
|-----------|-------------|
| Zero pairs detected | **SKIPPED** |
| Zero CRITICAL + Zero HIGH | **PASS** |
| Zero CRITICAL + 1-3 HIGH | **PASS_WITH_CONDITIONS** |
| Zero CRITICAL + 4+ HIGH | **FAIL** |
| Any CRITICAL | **FAIL** |
| Integration tests fail | **FAIL** |

### Strict Mode (`--strict`)

| Condition | Gate Result |
|-----------|-------------|
| Zero CRITICAL + Zero HIGH + Zero MEDIUM | **PASS** |
| Any MEDIUM or above | **FAIL** |

---

## Severity Thresholds

### CRITICAL (Immediate Blocker)
- Contract type mismatch causing certain runtime error
- Missing required field that will raise exception
- Data loss path (writes without confirmation)

**Threshold**: ANY CRITICAL = FAIL

### HIGH (Should Fix)
- Null/None not handled but may not always occur
- Schema field mismatch that could cause issues
- Exception swallowed without logging

**Threshold**: ≤3 HIGH = PASS_WITH_CONDITIONS, 4+ HIGH = FAIL

### MEDIUM (Advisory)
- Error context lost in propagation
- Edge case not handled (empty list, zero value)
- Suboptimal but functional pattern

**Threshold**: No limit (documented in report)

### LOW (Optional)
- Performance suggestion
- Style at boundary
- Documentation gap

**Threshold**: No limit (documented in report)

---

## Reliability Findings

Reliability findings from the `reliability-reviewer` agent use the **same severity thresholds** as other integration findings:

| Reliability Check | Severity | Threshold Impact |
|-------------------|----------|------------------|
| Race condition without guard | CRITICAL | Any = FAIL |
| Unbounded allocation | CRITICAL | Any = FAIL |
| Missing timeout budget | HIGH | ≤3 = PASS_WITH_CONDITIONS |
| Missing precondition validation | HIGH | ≤3 = PASS_WITH_CONDITIONS |
| Missing "why" logs | MEDIUM | No limit |
| Cognitive load concern | LOW | No limit |

Reliability findings are aggregated with other findings for gate calculation—there is no separate reliability gate.

---

## Integration Test Requirements

### Test Coverage Check
Integration tests must exist for the reviewed pair.

| Coverage Status | Impact on Gate |
|-----------------|---------------|
| COVERED | No impact |
| PARTIAL | Warning only |
| MISSING | Warning + recommendation |

**Note**: Missing integration tests do NOT automatically fail the gate, but are flagged for action.

### Test Execution
If `--skip-tests` is NOT specified:
- Run: `pytest tests/integration/ -v --tb=short`
- Any test failure = **FAIL**

---

## Conditional Pass Requirements

When gate result is **PASS_WITH_CONDITIONS**, the report must include:

1. **List of HIGH findings** with:
   - Clear description
   - Evidence location
   - Recommended fix
   - Impact if not fixed

2. **Acknowledgment requirement**:
   - Findings documented in PR description
   - OR explicit justification why fix is deferred

---

## Override Conditions

### Manual Override
User can override gate with justification:
```
/integration-review {path} --override "Known limitation, tracked in #123"
```

Override is logged in report with timestamp and justification.

### Excluded Pairs
Specific pairs can be excluded:
```
/integration-review {path} --exclude-pair 3,5
```

Excluded pairs are noted in report, not factored into gate.

---

## Gate Decision Flow

```
START
  │
  ├── Count findings by severity
  │     CRITICAL: {C}
  │     HIGH: {H}
  │     MEDIUM: {M}
  │     LOW: {L}
  │
  ├── Check strict mode?
  │     YES → Any MEDIUM+? → FAIL
  │     NO  → Continue
  │
  ├── Any CRITICAL?
  │     YES → FAIL
  │     NO  → Continue
  │
  ├── HIGH count > 3?
  │     YES → FAIL
  │     NO  → Continue
  │
  ├── Integration tests fail?
  │     YES → FAIL
  │     NO  → Continue
  │
  ├── HIGH count > 0?
  │     YES → PASS_WITH_CONDITIONS
  │     NO  → Continue
  │
  └── PASS
```

---

## Report Gate Summary

The final report includes a gate summary section:

```markdown
## Gate Decision

**Result**: PASS_WITH_CONDITIONS

**Criteria Applied**:
- [x] Zero CRITICAL findings
- [x] HIGH findings ≤3 (found: 2)
- [x] Integration tests pass
- [ ] Zero HIGH findings (found: 2)

**Blocking Issues**: None

**Action Required**:
1. Review HIGH finding INT-003 (error propagation)
2. Review HIGH finding INT-006 (schema compatibility)
3. Document justification in PR or fix before merge
```

---

## Metrics Tracked

| Metric | Purpose |
|--------|---------|
| `total_pairs` | Scope of review |
| `findings_by_severity` | Issue distribution |
| `gate_result` | Final decision |
| `review_duration` | Performance tracking |
| `pairs_with_issues` | Problem density |
