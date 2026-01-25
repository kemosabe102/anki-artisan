# Frameworks: SQALE, SIG, and Scoring Methodology

Complete methodology reference for technical debt analysis.

---

## SQALE Methodology (Software Quality Assessment based on Lifecycle Expectations)

### TDR Calculation
```
Technical Debt Ratio (TDR) = remediation_cost / development_cost
```

### SQALE Grades
| Grade | TDR Range | Interpretation |
|-------|-----------|----------------|
| A | <5% | Excellent - minimal debt |
| B | 5-10% | Good - manageable debt |
| C | 10-20% | Fair - attention needed |
| D | 20-50% | Poor - significant debt |
| E | >50% | Critical - debt crisis |

### Orthogonal Classification
Each issue counted ONCE in exactly one category:
1. **Code Quality** (40%) - Complexity, duplication, violations
2. **Testing** (20%) - Coverage, flakiness, missing tests
3. **Architecture** (15%) - Coupling, cohesion, dependencies
4. **Documentation** (10%) - Missing docs, outdated READMEs
5. **Infrastructure** (10%) - Deprecated APIs, outdated deps
6. **Design/UI** (5%) - UX patterns, accessibility

---

## SIG Maintainability Model (Software Improvement Group)

### Star Ratings
| Stars | Percentile | Interpretation |
|-------|------------|----------------|
| 5 | Top 5% | Exceptional maintainability |
| 4 | Top 30% | Above average |
| 3 | Average | Industry median |
| 2 | Below 30% | Below average |
| 1 | Bottom 5% | Critical concerns |

### Low-Risk Thresholds
- Volume: <66 KLOC per component
- Complexity: <15 per method
- Duplication: <5% of code
- Unit Size: <15 LOC per method
- Unit Interfacing: <4 parameters

---

## Composite Scoring Formula

### debt_score (0-100)
```
debt_score = Σ(category_weight × category_score)

Where category scores:
- Code Quality: 40%
- Testing: 20%
- Architecture: 15%
- Documentation: 10%
- Infrastructure: 10%
- Design/UI: 5%
```

### Hotspot Score
```
hotspot_score = churn × complexity × defects × business_criticality

Threshold: >7.0 = urgent attention
```

---

## Impact/Effort Matrix

### Quadrant Assignments
| Quadrant | Impact | Effort | Action |
|----------|--------|--------|--------|
| P1 Quick Wins | High | Low | Do immediately |
| P2 Strategic | High | High | Plan and resource |
| P3 Defer | Low | High | Deprioritize |
| P4 Opportunistic | Low | Low | Boy Scout Rule |

### Scoring Criteria
**Impact** (1-5):
- 5: Core functionality, security, data integrity
- 4: Performance, reliability
- 3: Maintainability, testability
- 2: Code clarity, documentation
- 1: Cosmetic, style

**Effort** (1-5):
- 5: >2 weeks, architectural changes
- 4: 1-2 weeks, significant refactoring
- 3: 2-5 days, moderate changes
- 2: 1-2 days, localized changes
- 1: <1 day, quick fixes

---

## Principal vs Interest Framework

### Definitions
- **Principal**: One-time cost to fix now
- **Interest**: Recurring cost if left unfixed

### ROI Calculation
```
ROI = (interest_per_sprint × expected_sprints) / principal
```

High ROI items (>2.0) should be prioritized.

---

## OODA Loop Workflow

### 1. OBSERVE
- Parse artifacts using 6-category taxonomy
- Collect metrics (complexity, duplication, coverage)
- Analyze git history (churn, ownership, defects)

### 2. ORIENT
- Apply SQALE classification
- Calculate quantitative metrics vs thresholds
- Map findings to Impact/Effort quadrants

### 3. DECIDE
- Calculate composite debt_score
- Compute TDR, assign SQALE grade
- Rank remediation by P1-P4

### 4. ACT
- Generate structured findings JSON
- Produce Impact/Effort matrix
- Create remediation roadmap

### 5. OBSERVE (Iterative)
- Compare vs baseline (if provided)
- Calculate deltas (TDR Δ%, coverage Δ%)
- Detect regressions (TDR >5%, coverage drop >5%)

---

## Trend Analysis

### Regression Thresholds
- TDR increase >5% = regression
- Coverage drop >5% = regression
- New hotspots (score >7.0) = regression

### Direction Classification
- **Improving**: debt_score decreased, TDR decreased
- **Stable**: <5% change in key metrics
- **Worsening**: debt_score increased, TDR increased
