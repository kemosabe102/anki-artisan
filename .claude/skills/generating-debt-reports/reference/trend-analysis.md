# Trend Analysis Reference

Baseline comparison calculations for iterative technical debt tracking.

---

## When to Include Trend Analysis

Include `trend_analysis` in output when:
- Baseline report timestamp provided
- Previous analysis JSON available for comparison
- Quality gate requires regression detection
- Tracking debt paydown over sprints

---

## Delta Metrics

Calculate change for each key metric:

### debt_score_delta

```json
{
  "previous": 65,
  "current": 72,
  "change_pct": 10.77,
  "trend_direction": "improving"
}
```

**change_pct Formula**:
```
change_pct = ((current - previous) / previous) * 100
```

Positive = improvement (debt score increased)
Negative = regression (debt score decreased)

---

### tdr_ratio_delta

```json
{
  "previous": 0.15,
  "current": 0.12,
  "change_pct": -20.0,
  "trend_direction": "improving"
}
```

Note: For TDR, lower is better, so negative change_pct = improvement.

---

### category_deltas

Per-category score changes:

```json
{
  "code_quality": +5,
  "testing": +10,
  "architecture": 0,
  "documentation": -3,
  "infrastructure": +2,
  "design_ui": 0
}
```

---

## Regression Detection

### Regression Thresholds

| Metric | Regression Threshold | Severity |
|--------|---------------------|----------|
| TDR increase | >5% | critical |
| Coverage drop | >5% | critical |
| New hotspots (>7.0) | Any new | warning |
| debt_score decrease | >5 points | warning |
| Category score drop | >1 star | warning |

### Regression Object Format

```json
{
  "metric": "test_coverage",
  "previous_value": 85,
  "current_value": 78,
  "threshold_violated": "Coverage drop >5%",
  "severity": "critical"
}
```

---

## Direction Classification

### Improving

Criteria (ANY of):
- debt_score increased >5 points
- TDR decreased >5%
- 2+ categories improved by 1+ star

### Stable

Criteria:
- <5% change in debt_score
- <5% change in TDR
- No new critical hotspots

### Worsening

Criteria (ANY of):
- debt_score decreased >5 points
- TDR increased >5%
- New hotspots with score >7.0
- Coverage dropped >5%

---

## New Hotspots Detection

Compare current hotspots array against baseline:

```json
{
  "new_hotspots": [
    "packages/core/payment_processor.py",
    "packages/api/routes/checkout.py"
  ]
}
```

A file is a "new hotspot" if:
1. Not in baseline hotspots array, AND
2. Current hotspot_score >7.0

---

## Complete Trend Analysis Example

```json
{
  "trend_analysis": {
    "baseline_timestamp": "2025-11-15T10:30:00Z",
    "debt_score_delta": {
      "previous": 58,
      "current": 67,
      "change_pct": 15.5,
      "trend_direction": "improving"
    },
    "category_deltas": {
      "code_quality": +8,
      "testing": +12,
      "architecture": +3,
      "documentation": 0,
      "infrastructure": +5,
      "design_ui": 0
    },
    "regressions": [],
    "new_hotspots": []
  }
}
```

---

## Quality Gate Integration

For CI/CD quality gates, use regression detection to fail builds:

| Condition | Gate Action |
|-----------|-------------|
| Any critical regression | FAIL |
| >2 warning regressions | FAIL |
| 1-2 warning regressions | WARN |
| No regressions | PASS |
