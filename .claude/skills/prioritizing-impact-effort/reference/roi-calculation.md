# ROI Calculation

Principal/Interest framework for technical debt ROI analysis.

---

## Principal/Interest Framework

### Core Concepts

| Term | Definition | Unit |
|------|------------|------|
| **Principal** | One-time cost to remediate now | Hours |
| **Interest** | Recurring cost per sprint if left unfixed | Hours/sprint |
| **Expected Sprints** | Planning horizon for ROI calculation | Sprints (default: 6) |

### Analogy

Technical debt behaves like financial debt:
- **Principal** = Loan amount (effort to fix)
- **Interest** = Ongoing payments (maintenance burden)
- **Payback** = When accumulated interest exceeds principal

---

## ROI Formula

### Calculation

```
ROI = (interest_per_sprint x expected_sprints) / principal
```

### Interpretation

| ROI | Priority | Interpretation |
|-----|----------|----------------|
| >3.0 | Very High | Strong ROI, prioritize aggressively |
| >2.0 | High | Good ROI, include in remediation plan |
| 1.0-2.0 | Moderate | Marginal ROI, consider if capacity allows |
| <1.0 | Low | Poor ROI, defer or deprioritize |

**Threshold**: ROI >2.0 = high priority remediation candidate

---

## Payback Period

### Formula

```
payback_sprints = principal / interest_per_sprint
```

### Interpretation

| Payback Period | Recommendation |
|----------------|----------------|
| <2 sprints | Immediate action - quick return |
| 2-4 sprints | Plan for current quarter |
| 4-6 sprints | Include in roadmap |
| >6 sprints | Low priority, document only |

---

## Interest Estimation

### Common Interest Sources

| Source | Typical Interest | Example |
|--------|------------------|---------|
| Bug fixes | 2-8 hrs/sprint | Workarounds, hotfixes |
| Workarounds | 1-4 hrs/sprint | Code duplication, special cases |
| Onboarding | 2-6 hrs/sprint | Explaining quirks to new devs |
| Testing overhead | 1-3 hrs/sprint | Manual testing, flaky tests |
| Performance issues | 2-5 hrs/sprint | Monitoring, incident response |
| Security patches | 4-10 hrs/sprint | Vulnerability management |

### Estimation Questions

To estimate interest, ask:
1. How much time does the team spend working around this issue per sprint?
2. How often do bugs related to this area get reported?
3. How much extra testing/verification is needed?
4. How much time is spent explaining this to new team members?

---

## Calculation Examples

### Example 1: High ROI - Security Vulnerability

```
Issue: Outdated authentication library
Principal: 40 hours (refactor + testing)
Interest: 8 hours/sprint (security patches, workarounds)
Expected Sprints: 6

ROI = (8 x 6) / 40 = 48 / 40 = 1.2
Payback = 40 / 8 = 5 sprints

Recommendation: Moderate priority (ROI 1.2, payback in 5 sprints)
```

### Example 2: Very High ROI - Performance Hotspot

```
Issue: Inefficient database queries causing slowdowns
Principal: 16 hours (query optimization)
Interest: 12 hours/sprint (incident response, monitoring)
Expected Sprints: 6

ROI = (12 x 6) / 16 = 72 / 16 = 4.5
Payback = 16 / 12 = 1.3 sprints

Recommendation: Very high priority (ROI 4.5, payback in <2 sprints)
```

### Example 3: Low ROI - Code Cleanup

```
Issue: Legacy naming conventions in utility module
Principal: 24 hours (rename + update references)
Interest: 1 hour/sprint (minor confusion)
Expected Sprints: 6

ROI = (1 x 6) / 24 = 6 / 24 = 0.25
Payback = 24 / 1 = 24 sprints

Recommendation: Defer (ROI 0.25, payback in 24 sprints)
```

---

## Break-Even Analysis

Break-even occurs when accumulated interest equals principal:

```
break_even_sprints = principal / interest_per_sprint
```

### Decision Matrix

| Break-Even | Expected Sprints | Action |
|------------|------------------|--------|
| < expected | Within horizon | Fix now (positive ROI) |
| = expected | At boundary | Consider other factors |
| > expected | Beyond horizon | Defer (negative ROI in horizon) |

---

## Sensitivity Analysis

When estimates are uncertain, calculate ROI for optimistic/pessimistic scenarios:

| Scenario | Principal | Interest | ROI |
|----------|-----------|----------|-----|
| Optimistic | -20% | +20% | Higher |
| Base | Estimate | Estimate | Baseline |
| Pessimistic | +20% | -20% | Lower |

If ROI >2.0 in pessimistic scenario, high confidence in prioritization.

---

## Cross-References

- **Sprint Assignment**: [sprint-grouping.md](sprint-grouping.md)
- **Shared Formulas**: `.claude/skills/tech-debt-shared/FORMULAS.md` section 6
- **Phase 3 DECIDE**: `.claude/agents/specialists/tech-debt-investigator/phases/phase-3-decide.md`
