# TDR Calculation Reference

Technical Debt Ratio (TDR) calculation methodology from SQALE.

---

## Core Formula

```
TDR = (remediation_cost / development_cost) x 100
```

**Result**: Percentage representing debt relative to total development investment.

---

## Cost Estimation Methods

### Remediation Cost

Sum of estimated hours to fix all identified issues:

| Issue Severity | Typical Hours | Examples |
|----------------|---------------|----------|
| Critical | 8-16 hours | Security vulnerabilities, data corruption risks |
| Major | 4-8 hours | Performance bottlenecks, major refactoring |
| Minor | 1-4 hours | Code smells, missing tests |
| Info | 0.5-1 hour | Style violations, documentation gaps |

**Calculation**: `remediation_cost = SUM(issue_count x severity_hours)`


### Development Cost

Industry standard estimation based on codebase size:

```
development_cost = total_LOC / 10
```

**Rationale**: Average developer produces ~10 LOC per hour (including design, testing, review).

**Alternative Methods**:
- Historical: Actual development hours from time tracking
- Function Points: FP-based estimation for complex systems
- COCOMO: For large enterprise codebases

---

## Grade Mapping Table

| Grade | TDR Range | Interpretation | Quality Gate |
|-------|-----------|----------------|--------------|
| **A** | <5% | Excellent - minimal debt | PASS |
| **B** | 5-10% | Good - manageable debt | PASS |
| **C** | 10-20% | Fair - attention needed | CONDITIONAL |
| **D** | 20-50% | Poor - significant debt | FAIL |
| **E** | >50% | Critical - debt crisis | FAIL |

---


## Example Calculation

### Scenario: Medium Python Codebase

**Inputs**:
- Total LOC: 50,000
- Critical issues: 5 (avg 12 hours each)
- Major issues: 20 (avg 6 hours each)
- Minor issues: 80 (avg 2 hours each)
- Info issues: 150 (avg 0.5 hours each)

**Step 1: Calculate Development Cost**
```
development_cost = 50,000 / 10 = 5,000 hours
```

**Step 2: Calculate Remediation Cost**
```
remediation_cost = (5 x 12) + (20 x 6) + (80 x 2) + (150 x 0.5)
                 = 60 + 120 + 160 + 75
                 = 415 hours
```

**Step 3: Calculate TDR**
```
TDR = (415 / 5,000) x 100 = 8.3%
```

**Result**: Grade **B** (Good - manageable debt)

---

## Threshold Adjustments

Default thresholds may be adjusted for context:

| Context | Adjustment | Rationale |
|---------|------------|-----------|
| Legacy system | Relax by 5% | Higher acceptable debt |
| Greenfield | Tighten by 2% | Should start clean |
| Critical path | Tighten by 5% | Lower risk tolerance |
| Prototype | Relax by 10% | Speed over quality |
