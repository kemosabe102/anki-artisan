---
title: "Backtest Metrics Reference"
date: 2026-01-09
status: ACTIVE
tags: [backtest, metrics, dashboard]
---

# Backtest Metrics Reference

Comprehensive guide to the 6-dimension performance metrics used in backtest evaluation.

---

## Overview

The dashboard tracks performance across **six independent dimensions**. Each dimension contains multiple related metrics that together provide a complete picture of strategy performance.

| Dimension | Focus | Metric Count |
|-----------|-------|--------------|
| Profitability | How much money? | 6 |
| Risk-Adjusted Efficiency | Return per unit of risk | 4 |
| Downside Protection | How bad does it get? | 5 |
| Trade Quality | What's your trading edge? | 7 |
| Consistency | Does it hold up over time? | 7 |
| Recovery Efficiency | How fast do you bounce back? | 3 |


---

## Dimension 1: Profitability

**Question**: How much money does the strategy make?

| Metric | Calculation | Ideal for Trends | Relationship |
|--------|-------------|------------------|--------------|
| **Total Return %** | (Ending - Starting) / Starting | 15-50% | Baseline—affected by time period |
| **CAGR %** | (Ending/Starting)^(1/Years) - 1 | 8-20% annually | Normalizes return over time |
| **Monthly Avg Return %** | Mean of monthly returns | 0.5-2% | Shows monthly consistency |
| **Best Month Return %** | Highest single month | 5-15% | Peak performance capture |
| **Worst Month Return %** | Lowest single month | -10% to -2% | Painful period depth |
| **Profit Factor** | Gross Profit / Gross Loss | 1.75-2.5 | Overall profitability ratio |

**Relationships**:
- Total Return is raw outcome
- CAGR normalizes across different time periods (compare 1-year vs 5-year fairly)
- Monthly breakdown reveals consistency vs lumpiness

**Red Flags**:
- Return 30% but CAGR 5% = Lucky period, not robust
- CAGR 15% but worst month -25% = Too concentrated in few trades


---

## Dimension 2: Risk-Adjusted Efficiency

**Question**: How much return do you get per unit of risk taken?

| Metric | Calculation | Ideal for Trends | Interpretation |
|--------|-------------|------------------|----------------|
| **Sharpe Ratio** | (Return - RiskFree) / StdDev | 0.5-1.5 | Standard institutional metric |
| **Sortino Ratio** | (Return - RiskFree) / DownsideVol | 1.0-2.0 | Better for positive skew strategies |
| **Calmar Ratio** | CAGR / Max Drawdown | 0.5-1.2 | Return per worst-case loss |
| **Volatility %** | StdDev × √252 | 15-25% | Raw portfolio turbulence |

**Key Insight**:
- For trend strategies, **Sortino should exceed Sharpe**
- If Sortino < Sharpe, downside volatility is too high (concerning)
- Calmar > 0.8 means you earn annual return quickly

**Scenario Interpretation**:
```
Sharpe 1.0 / Sortino 1.0 / Calmar 0.5 → Drawdown too severe
Sharpe 0.8 / Sortino 1.4 / Calmar 0.8 → Positive skew, healthy
Sharpe 1.2 / Sortino 0.9 / Calmar 0.4 → Negative skew, concerning
```


---

## Dimension 3: Downside Protection

**Question**: How bad does it get?

| Metric | Calculation | Ideal for Trends | Why It Matters |
|--------|-------------|------------------|----------------|
| **Max Drawdown %** | (Worst - Peak) / Peak | 15-35% | Portfolio capacity constraint |
| **Avg Drawdown %** | Mean of all DD periods | 5-15% | Frequency of painful losses |
| **DD Duration (days)** | Longest recovery time | <180 days | How long capital is impaired |
| **VaR 95%** | Worst 5% of daily losses | -2% to -5%/day | Extreme scenario quantification |
| **Max Consecutive Losses** | Longest losing streak | <10 days | Psychological tolerance |

**Relationships**:
```
Max DD 25% but Avg DD 12% = Infrequent severe losses (GOOD for trends)
Max DD 15% but Avg DD 14% = Consistently painful (BAD)
VaR 95% -3% but Max DD 30% = Normal days OK, rare events hurt (NORMAL)
```

**Critical Rule**: Prepare for 2× historical max drawdown in live trading.


---

## Dimension 4: Trade Quality & Edge

**Question**: What's your actual trading edge?

| Metric | Calculation | Ideal for Trends | Why It Matters |
|--------|-------------|------------------|----------------|
| **Total Trades** | Entry-exit cycles | 50-500 | More trades = statistical confidence |
| **Win Rate %** | Winners / Total × 100 | 35-50% | Low % OK if wins are large |
| **Profit Factor** | Gross Profit / Gross Loss | 1.75-2.5 | Win magnitude vs loss |
| **Avg Win %** | Profit / # winners | 3-5× avg loss | Typical winner size |
| **Avg Loss %** | Loss / # losers | 1/3 to 1/5 of win | Typical loser size |
| **Win/Loss Ratio** | Avg Win / Avg Loss | 3:1 to 5:1 | Core edge signature |
| **Expectancy** | (WR×AvgWin) - (LR×AvgLoss) | Positive | Per-trade profitability |

**Edge Profiles**:
```
PROFITABLE TREND PROFILE:
- Win Rate: 40% (losing 60% of trades)
- Avg Win: $1,000 / Avg Loss: $200
- Profit Factor: 2.0
- Expectancy: $280/trade
→ HEALTHY: Small losses, large wins

PROBLEMATIC PROFILE:
- Win Rate: 70%
- Avg Win: $100 / Avg Loss: $1,000
- Profit Factor: 0.7 (LOSING!)
- Expectancy: -$230/trade
→ BAD: High win rate masks negative expectancy
```

**Key Insight**: Win Rate alone is worthless. PF < 1.0 = losing money.

---

## Dimension 5: Consistency & Robustness

**Question**: Does it hold up over time?

| Metric | Calculation | Ideal for Trends | Why It Matters |
|--------|-------------|------------------|----------------|
| **Max Consecutive Wins** | Longest win streak | 5-15 | Momentum capture |
| **Max Consecutive Losses** | Longest loss streak | 5-10 | Psychology breaking point |
| **% Months Profitable** | Positive/Total × 100 | 60-80% | Monthly reliability |
| **Best/Worst Month Ratio** | Best / |Worst| | 2:1 to 5:1 | Spread consistency |
| **Avg Trade Duration** | Mean entry-to-exit | 60-180 days | Holding period match |
| **Win/Loss Duration Ratio** | Winner days / Loser days | 5:1 to 10:1 | Trade discipline |
| **Regime CV** | StdDev(regime returns) / Mean | <0.5 | Cross-regime stability |


**Relationships**:
```
Max Losses 8 + Months Profitable 65% = Manageable
Max Losses 12 + Months Profitable 40% = Dangerous

Win Duration 90d + Loss Duration 5d = Good discipline
Win Duration 30d + Loss Duration 45d = Backwards (bad)
```

---

## Dimension 6: Recovery Efficiency

**Question**: How fast do you bounce back?

| Metric | Calculation | Ideal for Trends | Why It Matters |
|--------|-------------|------------------|----------------|
| **Recovery Factor** | Net Profit / Max DD $ | 2.0-5.0 | $ earned per $ lost at worst |
| **Time to New High** | Days from DD to peak | <90 days | Capital impairment duration |
| **DD Depth (days)** | Longest continuous DD | <180 days | Opportunity cost exposure |

**Relationships**:
```
RF 3.0 = Earn $3 for every $1 lost at worst (excellent)
RF 1.2 = Profits barely exceed worst loss (thin margin)

RF 2.0 + Time to High 200d = Profitable but slow recovery
RF 3.0 + Time to High 15d = Excellent, fast compounding resumes
```


---

## Decision Tree

Quick interpretation framework:

```
START: Review metrics
│
├→ Total Return > 15%?
│  NO → Under-leveraged or weak signal
│
├→ Max Drawdown < 30%?
│  NO → Reduce position size or improve stops
│
├→ Sharpe Ratio > 0.6?
│  NO → Review entry/exit logic
│
├→ Sortino > Sharpe?
│  NO → Check for tail risk (negative skew)
│
├→ Calmar Ratio > 0.4?
│  NO → Improve stops or diversify
│
├→ Win Rate 30-50%?
│  >60% → Might be overfitted, investigate
│
├→ Profit Factor > 1.5?
│  NO → Thin edge, vulnerable to costs
│
├→ Win/Loss Ratio > 2.0:1?
│  NO → Let profits run longer
│
├→ Win/Loss Duration Ratio > 3:1?
│  NO → Holding losers too long
│
├→ Recovery Factor > 2.0?
│  NO → Needs refinement
│
└→ Max Consecutive Losses < 10?
   YES → DEPLOYMENT READY
   NO → Prepare psychologically
```

---

## Metric Groups

### Return Efficiency
```
Total Return → CAGR → Sharpe → Sortino
Each adds sophistication layer
```

### Drawdown Story
```
Max DD ← → Calmar ← → Recovery Factor
Worst case → Justified? → Recovery speed
```


### Trade Edge
```
Win Rate + Win/Loss Ratio → Profit Factor → Expectancy
Win rate means nothing alone
```

### Consistency Check
```
Max Losses + Months Profitable + Duration Ratio
Shows resilience vs fragility
```

---

## Thresholds by Tier

| Metric | Tier 1 | Tier 2 | Tier 3 | Tier 4 |
|--------|--------|--------|--------|--------|
| Sharpe | ≥0.20 | ≥0.30 | ≥0.50 | ≥0.35 (DSR) |
| Max DD | ≤50% | ≤35% | ≤30% | ≤25% |
| Trades | ≥20 | ≥50 | ≥100 | ≥150 |
| Win Rate | - | ≥35% | ≥40% | ≥42% |

---

## Live Monitoring Priority

**Daily** (Tier 1):
1. Daily/Weekly Return
2. Current Drawdown %
3. Max DD to date
4. Trades executed
5. Current Win Rate


**Weekly** (Tier 2):
6. Rolling Sharpe
7. Rolling Profit Factor
8. Monthly pace
9. Avg trade duration
10. Days to recovery

**Monthly** (Tier 3):
11. Full ratios (Sharpe/Sortino/Calmar)
12. Win/Loss streaks
13. Months profitable %
14. Regime performance
15. Benchmark correlation

---

## Alert Triggers

| Condition | Action |
|-----------|--------|
| Running DD > 1.5× historical max | REVIEW POSITION SIZING |
| Monthly return < 50% baseline | REVIEW SIGNAL LOGIC |
| Win rate > 70% or < 20% | REGIME CHANGE DETECTED |
| Zero trades for 30 days | CHECK DATA FEED |

---

## Related Documentation

- `dashboard.schema.json` - JSON schema for these metrics
- `performance-dashboard.md` - ASCII output template
- `gate-thresholds.md` - Tier-specific validation gates
