# Hotspot Formula Reference

Quantitative scoring formula for identifying code hotspots requiring immediate attention.

---

## Formula

```
hotspot_score = churn x complexity x defects x criticality
```

**Normalization**: Scale result to 0-10 range

**Urgency Threshold**: Score > 7.0 = urgent attention required

---

## Component Definitions

| Component | Range | Source | Description |
|-----------|-------|--------|-------------|
| churn | 0.0-1.0 | Normalized commit count (3-month window) | See [churn-analysis.md](churn-analysis.md) |
| complexity | 0.0-1.0 | Cyclomatic complexity / 50 (capped at 1.0) | From static analysis |
| defects | 0.0-1.0 | Bug-related commits / total commits | From commit message parsing |
| criticality | 0.0-1.0 | Business impact factor | Manual classification |

---

## Criticality Classification

| Category | Value | Examples |
|----------|-------|----------|
| Core | 1.0 | Authentication, payment processing, data integrity |
| Critical Path | 0.8 | API handlers, core business logic |
| Support | 0.5 | Utilities, helpers, non-critical services |
| Utility | 0.2 | Logging, formatting, test utilities |

---

## Example Calculation

**File**: `packages/core/auth.py`

**Raw Metrics**:
- Commits in 3-month window: 45 (max in codebase: 50)
- Cyclomatic complexity: 30
- Bug-related commits: 8 out of 20 total
- Business category: Authentication (core)

**Normalized Components**:
```
churn      = 45 / 50           = 0.80
complexity = min(30 / 50, 1.0) = 0.60
defects    = 8 / 20            = 0.40
criticality = 1.0              (core component)
```

**Calculation**:
```
raw_score = 0.80 x 0.60 x 0.40 x 1.0 = 0.192
hotspot_score = 0.192 x 10 = 1.92
```

**Result**: Score 1.92 (below 7.0 threshold) - no urgent action needed

---

## High Score Example

**File**: `packages/api/legacy_handler.py`

**Normalized Components**:
```
churn      = 0.95  (very high change rate)
complexity = 0.90  (cyclomatic = 45)
defects    = 0.70  (14 bug commits / 20 total)
criticality = 0.80 (critical path)
```


**Calculation**:
```
raw_score = 0.95 x 0.90 x 0.70 x 0.80 = 0.4788
hotspot_score = 0.4788 x 10 = 4.79
```

**Result**: Score 4.79 - elevated but not urgent. Still recommend review.

---

## Urgency Classification

| Score Range | Urgency | Action |
|-------------|---------|--------|
| > 7.0 | Critical | Immediate refactoring sprint |
| 5.0 - 7.0 | High | Schedule for next sprint |
| 3.0 - 4.9 | Moderate | Add to tech debt backlog |
| 1.0 - 2.9 | Low | Monitor |
| < 1.0 | Minimal | No action |

---

## Formula Variants

### Additive (Alternative)
For cases where multiplicative produces too many low scores:
```
hotspot_score = (churn + complexity + defects + criticality) / 4 x 10
```

### Weighted (Custom)
Adjust weights based on team priorities:
```
hotspot_score = (churn x w1 + complexity x w2 + defects x w3 + criticality x w4) x 10
where w1 + w2 + w3 + w4 = 1.0
```

---

## Related

- [Churn Analysis](churn-analysis.md) - Source for churn component
- [Ownership](ownership.md) - Inform criticality based on ownership
- Shared Formulas: `.claude/skills/tech-debt-shared/FORMULAS.md` (authoritative reference)
