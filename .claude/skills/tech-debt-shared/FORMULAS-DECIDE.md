# DECIDE Phase Formulas

Prioritization and investment decision formulas. Used for action planning.

**Skills Using This File**: `prioritizing-impact-effort`

---

## 1. Priority Ranking Score

**Formula**:
```
priority_score = (impact_score × 2) - effort_score
```

**Range**: -10 to +20 (higher = higher priority)

**Tiebreaker**: Higher churn files rank first

**P1 Validation**: Effort must be <4 hours for quick wins

**Example**:
```
Finding: Missing input validation in API endpoint
- impact_score: 8 (security vulnerability)
- effort_score: 2 (simple fix)

priority_score = (8 × 2) - 2 = 14 (HIGH priority)
```

---

## 2. Impact/Effort Matrix (P1-P4 Quadrants)

**Quadrant Assignment**:
| Quadrant | Impact | Effort | Action |
|----------|--------|--------|--------|
| **P1 Quick Wins** | High (≥6) | Low (≤4) | Do immediately |
| **P2 Strategic** | High (≥6) | High (>4) | Plan and resource |
| **P3 Defer** | Low (<6) | High (>4) | Deprioritize |
| **P4 Opportunistic** | Low (<6) | Low (≤4) | Boy Scout Rule |

**Impact Scoring** (0-10):
| Score | Criteria |
|-------|----------|
| 9-10 | Security vulnerability, data integrity, core functionality |
| 7-8 | Performance, reliability, critical path |
| 5-6 | Maintainability, testability, developer experience |
| 3-4 | Code clarity, documentation, minor UX |
| 1-2 | Cosmetic, style preferences |

**Effort Scoring** (0-10):
| Score | Time | Criteria |
|-------|------|----------|
| 9-10 | >2 weeks | Architectural changes, multiple teams |
| 7-8 | 1-2 weeks | Significant refactoring |
| 5-6 | 2-5 days | Moderate changes |
| 3-4 | 1-2 days | Localized changes |
| 1-2 | <1 day | Quick fixes |

---

## 3. ROI Calculation

### Option A: Principal/Interest Model (Sprint-Based)

**Formula**:
```
ROI = (interest_per_sprint × expected_sprints) / principal
```

**Definitions**:
- **Principal**: One-time remediation cost (hours)
- **Interest**: Recurring maintenance burden per sprint (hours)
- **expected_sprints**: Planning horizon (default: 6)

**Threshold**: ROI >2.0 = high priority

**Payback Period**:
```
payback_sprints = principal / interest_per_sprint
```

**Example**:
```
Issue: Legacy authentication module
- principal: 40 hours (refactor cost)
- interest: 8 hours/sprint (ongoing workarounds)
- expected_sprints: 6

ROI = (8 × 6) / 40 = 1.2 (moderate priority)
payback = 40 / 8 = 5 sprints to break even
```

### Option B: Annual Cost Model (Business-Focused)

**Formula**:
```
Annual_Carrying_Cost = Team_Budget × (TDR / 100)
Annual_Savings = Current_Cost - Target_Cost
Break_Even_Months = Remediation_Cost / Monthly_Savings
```

**NPV Calculation** (3-year projection):
```
NPV = -remediation_cost + Σ(annual_savings / (1 + discount_rate)^year)
```

**Default discount rate**: 10%

**Approval Matrix**:
| Break-Even | Decision |
|------------|----------|
| <6 months | Approve immediately (high ROI) |
| 6-12 months | Strong business case |
| 12-18 months | Marginal (defer if capacity) |
| >18 months | Reject (poor ROI) |

**Example**:
```
Current state:
- Team budget: $1.8M/year
- TDR: 25% → Annual cost = $450,000

Target state (after refactoring):
- TDR: 10% → Annual cost = $180,000
- Annual savings: $270,000

Investment:
- Remediation cost: $75,000
- Break-even: $75,000 / ($270,000/12) = 3.3 months

Year 1 ROI: ($270,000 - $75,000) / $75,000 = 260%
3-Year NPV: ~$621,000

Decision: APPROVE (breaks even in 3 months)
```

---

## 4. Sprint Grouping

**Allocation Rules**:
- Sprint capacity: ~40 hours tech debt (team-dependent)
- P1 items first, then P2 by priority_score
- Never mix P3 items with P1/P2 in same sprint
- Group related files to minimize context switching

**Sprint Assignment**:
```
for each item in sorted(items, by=priority_score, desc):
    if current_sprint_hours + item.effort <= sprint_capacity:
        assign to current sprint
    else:
        move to next sprint
```

---

## Output Contract (DECIDE Phase)

```json
{
  "impact_effort_matrix": [
    {
      "id": "finding-001",
      "file": "auth.py",
      "impact_score": 8,
      "effort_score": 3,
      "quadrant": "P1",
      "priority_score": 13
    }
  ],
  "sprint_assignments": [
    {
      "sprint": 1,
      "items": ["finding-001", "finding-003"],
      "total_hours": 38,
      "capacity_pct": 95
    }
  ],
  "roi_analysis": {
    "model": "annual_cost",
    "current_tdr": 25,
    "target_tdr": 10,
    "annual_savings": 270000,
    "remediation_cost": 75000,
    "break_even_months": 3.3,
    "year1_roi_pct": 260,
    "decision": "APPROVE"
  }
}
```

---

## Cross-References

- **FORMULAS-ORIENT.md**: Provides TDR, hotspot scores for prioritization
- **DEFINITIONS.md**: Effort estimates for principal calculation
- **FORMULAS-ACT.md**: Report formatting for decisions
