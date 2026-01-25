# Stress Test Metrics

## Purpose

Defines tail risk metrics and calculations used for crisis stress testing.

---

## Value at Risk (VaR)

### Definition
VaR answers: "What is the maximum loss at X% confidence over a given period?"

### Calculation
```
VaR_X% = Percentile(returns, 1 - X/100)

Example:
- VaR_95% = 5th percentile of daily returns
- VaR_99% = 1st percentile of daily returns
```

### Thresholds
| Confidence | Soft Gate | Hard Gate |
|------------|-----------|-----------|
| VaR 95% | -5% daily | -8% daily |
| VaR 99% | -8% daily | -12% daily |

### Interpretation
- VaR 95% = -5% means: "95% of days, losses will not exceed 5%"
- Breaching soft gate: Warning, monitor closely
- Breaching hard gate: Strategy may be too risky

---

## Conditional VaR (CVaR / Expected Shortfall)

### Definition
CVaR answers: "When losses exceed VaR, what is the average loss?"

### Calculation
```
CVaR_X% = Mean(returns | returns < VaR_X%)

Example:
- CVaR_99% = Average of worst 1% of returns
```

### Why CVaR Matters
- VaR ignores tail severity
- CVaR captures "how bad can it get when it's bad"
- More useful for crisis scenarios

### Thresholds
| Confidence | Soft Gate | Hard Gate |
|------------|-----------|-----------|
| CVaR 95% | -7% daily | -10% daily |
| CVaR 99% | -10% daily | -15% daily |

---

## Maximum Drawdown

### Definition
Largest peak-to-trough decline during the test period.

### Calculation
```
For each point t:
  running_max[t] = max(equity[0:t])
  drawdown[t] = (equity[t] - running_max[t]) / running_max[t]

max_drawdown = min(drawdown)
```

### Crisis-Specific Thresholds
| Crisis | Strategy Gate | Benchmark |
|--------|---------------|-----------|
| GFC 2008 | < 2x benchmark | -57% |
| COVID 2020 | < 50% | -34% |
| Rate Hike 2022 | < 30% (or Sharpe > 0) | -27% |

---

## Recovery Time

### Definition
Days from maximum drawdown to equity recovery.

### Calculation
```
recovery_days = first_date(equity >= pre_dd_peak) - date(max_dd)
```

### Thresholds
| Category | Days | Interpretation |
|----------|------|----------------|
| Excellent | < 90 | Quick recovery |
| Acceptable | 90-365 | Normal recovery |
| Concerning | 365-730 | Slow recovery |
| Unacceptable | > 730 | May never recover |

---

## Maximum Consecutive Losses

### Definition
Longest streak of consecutive losing periods.

### Calculation
```
For each period:
  IF return < 0:
    current_streak += 1
  ELSE:
    max_streak = max(max_streak, current_streak)
    current_streak = 0
```

### Thresholds (Daily)
| Streak | Assessment |
|--------|------------|
| < 10 | Normal |
| 10-20 | Elevated risk |
| > 20 | Severe (soft gate fail) |

---

## Overall Score Calculation

### Formula
```python
overall_score = (
    crisis_survival_score * 0.50 +
    tail_risk_score * 0.30 +
    recovery_score * 0.20
)
```

### Component Calculations

**Crisis Survival Score** (0-100):
```python
for crisis in [GFC_2008, COVID_2020, RATE_HIKE_2022]:
    survival_ratio = 1 - (strategy_dd / benchmark_dd)
    # Capped at 1.0 (can't be better than 100%)
    crisis_scores.append(min(survival_ratio, 1.0) * 100)

crisis_survival_score = mean(crisis_scores)
```

**Tail Risk Score** (0-100):
```python
# Based on VaR 99%
var_ratio = abs(var_99) / abs(tolerance_var_99)
tail_risk_score = max(0, (1 - var_ratio) * 100)
```

**Recovery Score** (0-100):
```python
# Based on average recovery time across crises
avg_recovery = mean(recovery_days)
recovery_score = max(0, (1 - avg_recovery / 365) * 100)
```

---

## Verdict Mapping

| Overall Score | Verdict | Action |
|---------------|---------|--------|
| >= 70 | CRISIS_PROOF | Safe for deployment |
| 50-69 | VULNERABLE | Review warnings, may deploy with monitoring |
| < 50 | FRAGILE | Do not deploy, redesign required |

---

## Example Calculation

**Strategy Performance During Crises**:
- GFC 2008: DD = -40% (benchmark -57%)
- COVID 2020: DD = -25% (benchmark -34%)
- Rate Hike 2022: DD = -18%, Sharpe = 0.1

**Scores**:
```python
# Crisis Survival
gfc_survival = (1 - 40/57) * 100 = 29.8
covid_survival = (1 - 25/34) * 100 = 26.5
rate_survival = 100 (passed both conditions)
crisis_score = mean([29.8, 26.5, 100]) = 52.1

# Tail Risk (VaR 99% = -7%, tolerance = -10%)
tail_score = (1 - 7/10) * 100 = 30

# Recovery (avg 120 days)
recovery_score = (1 - 120/365) * 100 = 67.1

# Overall
overall = 52.1 * 0.5 + 30 * 0.3 + 67.1 * 0.2
overall = 26.05 + 9 + 13.42 = 48.47

# Verdict: FRAGILE (score < 50)
```
