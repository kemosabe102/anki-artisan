# Crisis Stress Tester Documentation

## Overview

The crisis-stress-tester agent validates strategies against historical market crises and synthetic tail scenarios to ensure survivability before deployment.

## Document Index

| Document | Purpose |
|----------|---------|
| `crisis-periods.md` | Historical crisis period definitions and benchmarks |
| `stress-metrics.md` | Tail risk metric calculations and thresholds |

## Quick Reference

### Crisis Periods

| Crisis | Period | Benchmark DD |
|--------|--------|--------------|
| GFC 2008 | 2008-09-01 to 2009-03-31 | -57% |
| COVID 2020 | 2020-02-19 to 2020-03-23 | -34% |
| Rate Hike 2022 | 2022-01-01 to 2022-10-31 | -27% |

### Hard Gates

| Gate | Threshold |
|------|-----------|
| CRISIS_2008_SURVIVE | Max DD < 2x S&P DD (-114%) |
| CRISIS_2020_SURVIVE | Max DD < 50% |
| CRISIS_2022_SURVIVE | Sharpe > 0 OR DD < 30% |

### Verdict Thresholds

| Verdict | Score | Meaning |
|---------|-------|---------|
| CRISIS_PROOF | >= 70 | Safe for deployment |
| VULNERABLE | 50-69 | Warnings present, review needed |
| FRAGILE | < 50 | Not suitable for deployment |

## Integration

This agent requires:
- Prior backtest validation via `backtester` agent
- Strategy spec from `strategy-builder` agent
- Risk calculations from `risk-management-specialist` agent
