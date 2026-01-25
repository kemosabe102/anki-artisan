# Slippage Estimation Models

## Overview

Slippage is the difference between expected execution price and actual execution price. It comprises multiple components that must be modeled separately.

## Components

### 1. Bid-Ask Spread Cost

The minimum cost of any market order is half the bid-ask spread.

```
spread_cost_bps = (ask - bid) / mid * 10000 / 2
```

**Asset Class Defaults** (when live spread unavailable):

| Asset Class | Typical Spread (bps) |
|-------------|---------------------|
| Large-cap equities (>$10B) | 1-3 |
| Mid-cap equities ($2B-$10B) | 3-8 |
| Small-cap equities (<$2B) | 10-30 |
| Micro-cap equities (<$300M) | 30-100 |
| Liquid ETFs (SPY, QQQ) | 1-2 |
| Crypto majors (BTC, ETH) | 5-15 |
| Crypto altcoins | 20-100 |

### 2. Volatility Adjustment

Additional slippage from price movement during execution.

```
volatility_adj_bps = daily_volatility_bps * sqrt(execution_time_fraction)
```

Where `execution_time_fraction` = execution_minutes / 390 (trading day)

### 3. Timing Risk

Adverse movement between decision and execution.

```
timing_risk_bps = daily_volatility_bps * sqrt(delay_fraction)
```

## Total Slippage Formula

```
slippage_bps = spread_cost_bps + volatility_adj_bps + timing_risk_bps
```

## Stress Scenarios

| Scenario | Multiplier | Use Case |
|----------|------------|----------|
| Base | 1.0x | Normal market conditions |
| Elevated | 1.25x | Increased volatility (VIX > 20) |
| Stress | 1.5x | REQUIRED for viability validation |
| Crisis | 2.0x | Flash crash, market stress events |

## Validation Requirements

- SLIPPAGE_ESTIMATE gate requires non-zero slippage estimate
- Stress scenario (1.5x) must be evaluated for viability verdict
- All assumptions must be documented in output
