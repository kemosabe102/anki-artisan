# Viability Thresholds

## Overview

Viability thresholds determine whether a strategy can survive realistic execution costs. All gates must pass for VIABLE verdict.

## Gates

### SLIPPAGE_ESTIMATE (Required)

**Requirement**: Slippage must be estimated in basis points.

**Failure Mode**: Cannot proceed without slippage estimate.

**Minimum Acceptable**: Any non-zero estimate with documented assumptions.

### MARKET_IMPACT_MODEL (Required)

**Requirement**: Impact model must be selected and applied for orders > 1% ADV.

**Model Options**:
- `linear`: For orders < 1% ADV
- `square_root`: For orders 1-5% ADV
- `almgren_chriss`: For orders > 5% ADV

**Failure Mode**: Blocking for large orders without appropriate model.

### SENSITIVITY_PASS (Required)

**Requirement**: Strategy Sharpe must survive +50% slippage scenario.

**Threshold**: Stress Sharpe >= 0.3 (minimum viable)

**Calculation**:
```
stress_slippage = base_slippage * 1.5
stress_costs = slippage + impact + commission (with stress_slippage)
stress_sharpe = (return - costs) / volatility
```

## Viability Verdict Matrix

| Stress Sharpe | Cost/Return Ratio | Impact/ADV | Verdict |
|---------------|-------------------|------------|---------|
| >= 0.5 | < 30% | < 1% | VIABLE |
| 0.3-0.5 | 30-50% | 1-2% | MARGINAL |
| < 0.3 | > 50% | > 2% | NOT_VIABLE |

## Recommendations by Verdict

### VIABLE
- Strategy can proceed to deployment consideration
- Document execution cost assumptions for monitoring

### MARGINAL
- Strategy may work in favorable conditions
- Consider reducing trade frequency
- Consider increasing position hold time
- Consider focusing on more liquid assets

### NOT_VIABLE
- Strategy unlikely to survive real-world execution
- Recommendations:
  - Reduce turnover by 50%+
  - Increase average holding period
  - Focus on more liquid universe
  - Accept lower expected returns

## Confidence Requirements

All estimates must include confidence score (0.0-1.0):

| Data Quality | Confidence Range |
|--------------|------------------|
| Live market data, fresh ADV | 0.8-1.0 |
| Recent data (<30 days) | 0.6-0.8 |
| Default assumptions used | 0.4-0.6 |
| Multiple assumptions stacked | 0.2-0.4 |

**Minimum for viability verdict**: Confidence >= 0.5
