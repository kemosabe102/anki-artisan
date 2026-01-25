# ORIENT Phase Formulas

Scoring and rating formulas. Combines OBSERVE outputs into debt assessments.

**Skills Using This File**: `scoring-sqale-methodology`

---

## 1. Hotspot Score

### Option A: WEIGHTED (Recommended)

```
hotspot_score = (CC_norm × 0.4) + (churn_norm × 0.3) + (coupling_norm × 0.3)
```

**Benefits**: Partial credit, doesn't zero out, industry standard

**Normalization**:
```
CC_norm = min(cyclomatic_complexity / 25, 1.0)
churn_norm = min(commits_90d / 30, 1.0)
coupling_norm = min(external_deps / 10, 1.0)
```

**Example**:
```
File: auth.py
- CC: 28 → CC_norm = min(28/25, 1.0) = 1.0
- Churn: 18 commits → churn_norm = min(18/30, 1.0) = 0.6
- Coupling: 7 deps → coupling_norm = min(7/10, 1.0) = 0.7

hotspot_score = (1.0 × 0.4) + (0.6 × 0.3) + (0.7 × 0.3)
              = 0.40 + 0.18 + 0.21 = 0.79 (CRITICAL)
```

### Option B: MULTIPLICATIVE (Legacy)

```
hotspot_score = churn × complexity × defects × criticality
```

**Scale**: Multiply by 10 for 0-10 range

**Warning**: Zero in any dimension zeros entire score (false negatives)

**Classification**:
| Score | Risk | Action |
|-------|------|--------|
| 0.00-0.30 | LOW | Monitor |
| 0.30-0.50 | MEDIUM | Next sprint |
| 0.50-0.75 | HIGH | This sprint |
| 0.75-1.00 | CRITICAL | Urgent refactor |

---

## 2. Technical Debt Ratio (TDR)

**Formula**:
```
TDR = (remediation_hours / development_hours) × 100%
```

**Remediation Hours Calculation**:
```
remediation_hours = Σ(issue_count × effort_per_issue)
```

**Effort Estimates by Category**:
| Category | Minutes | Per Unit |
|----------|---------|----------|
| Duplication | 30 | block |
| Complexity | 45 | function |
| Security | 60 | vulnerability |
| Test coverage | 20 | uncovered branch |
| Documentation | 15 | missing API doc |
| Performance | 40 | bottleneck |

**Development Hours Estimation**:
```
development_hours = total_LOC / 10
```

**Grade Mapping**:
| Grade | TDR Range | Interpretation | Action |
|-------|-----------|----------------|--------|
| A | <5% | Excellent | Maintain practices |
| B | 5-10% | Good | Monitor, minor fixes |
| C | 10-20% | Fair | Plan remediation sprint |
| D | 20-50% | Poor | Prioritize debt reduction |
| E | >50% | Critical | Emergency intervention |

**Example**:
```
Issues:
- 45 duplication blocks × 30 min = 1,350 min
- 12 complex functions × 45 min = 540 min
- 87 uncovered branches × 20 min = 1,740 min

Total remediation = 3,630 min = 60.5 hours

Codebase: 24,000 LOC → dev_hours = 2,400

TDR = (60.5 / 2,400) × 100 = 2.5%
Grade = A (Excellent)
```

---

## 3. SIG Star Ratings

### Option A: TDR-Based (Simpler)

| TDR | Stars | Label |
|-----|-------|-------|
| ≤5% | ★★★★★ | Excellent |
| ≤10% | ★★★★☆ | Good |
| ≤20% | ★★★☆☆ | Average (market benchmark) |
| ≤50% | ★★☆☆☆ | Poor |
| >50% | ★☆☆☆☆ | Critical |

### Option B: Percentile-Based (Original SIG)

| Stars | Percentile | Interpretation |
|-------|------------|----------------|
| 5★ | Top 5% | Exceptional maintainability |
| 4★ | Top 30% | Above average |
| 3★ | Average | Industry median |
| 2★ | Below 30% | Below average |
| 1★ | Bottom 5% | Critical concerns |

**Business Translation**:
| Stars | Maintenance Cost | Dev Speed | Risk |
|-------|------------------|-----------|------|
| 5★ | Very Low | Very Fast | Minimal |
| 4★ | Low | Fast | Low |
| 3★ | Moderate | Normal | Moderate |
| 2★ | High | Slow | High |
| 1★ | Very High | Very Slow | Critical |

---

## 4. Composite Debt Score

**Formula**:
```
debt_score = Σ(category_weight × category_score)
```

**Category Weights** (must sum to 100%):
| Category | Weight | Focus |
|----------|--------|-------|
| Code Quality | 40% | Complexity, duplication, violations |
| Testing | 20% | Coverage, flakiness, missing tests |
| Architecture | 15% | Coupling, cohesion, dependencies |
| Documentation | 10% | Missing docs, outdated READMEs |
| Infrastructure | 10% | Deprecated APIs, outdated deps |
| Design | 5% | UX patterns, accessibility |

**Category Scores**: 0-100 (higher = healthier)

**Classification**:
| Score | Level | Interpretation |
|-------|-------|----------------|
| 81-100 | Low | Healthy codebase |
| 61-80 | Moderate | Normal maintenance |
| 41-60 | High | Active remediation needed |
| 0-40 | Severe | Critical intervention |

---

## Output Contract (ORIENT Phase)

```json
{
  "hotspot_scores": [
    {"file": "auth.py", "score": 0.79, "risk": "CRITICAL"}
  ],
  "tdr": {
    "ratio_pct": 2.5,
    "grade": "A",
    "remediation_hours": 60.5,
    "development_hours": 2400
  },
  "sig_rating": {
    "stars": 5,
    "label": "Excellent"
  },
  "composite_score": {
    "total": 72.5,
    "level": "Moderate",
    "by_category": {
      "code_quality": 70,
      "testing": 85,
      "architecture": 60,
      "documentation": 50,
      "infrastructure": 75,
      "design": 80
    }
  }
}
```

---

## Cross-References

- **FORMULAS-OBSERVE.md**: Provides input metrics (CC, churn, coupling)
- **DEFINITIONS.md**: Effort estimates, threshold values
- **FORMULAS-DECIDE.md**: Consumes scores for prioritization
