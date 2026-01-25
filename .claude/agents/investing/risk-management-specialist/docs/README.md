# Risk Management Specialist Documentation

Domain knowledge and methodology documentation for the risk-management-specialist agent.

## Contents

| Document | Description |
|----------|-------------|
| [position-sizing.md](position-sizing.md) | Van Tharp R-multiple methodology |
| [circuit-breaker.md](circuit-breaker.md) | Four-state trading circuit breaker |
| [chandelier-stops.md](chandelier-stops.md) | ATR-based trailing stop methodology |
| [atr-integration.md](atr-integration.md) | ATR delegation patterns |
| [volatility-regimes.md](volatility-regimes.md) | Percentile-based regime detection |
| [trend-classification.md](trend-classification.md) | 200DMA trend filter methodology |

## Quick Reference

### Core Formulas

**Position Size**: `shares = (account_equity * risk_pct) / |entry - stop|`

**Chandelier Stop (Long)**: `stop = highest_high(22) - (ATR(22) * 3.0)`

**Portfolio Heat**: `heat_pct = sum(position_risk) / account_equity * 100`

### Key Thresholds

| Parameter | Default | Range |
|-----------|---------|-------|
| Risk per trade | 1% | 0.5-2% |
| Portfolio heat limit | 10% | 5-15% |
| Circuit breaker | -3% | - |
| ATR multiplier | 3.0x | 2.5-4.0x |
| Lookback period | 22 bars | 14-40 |
