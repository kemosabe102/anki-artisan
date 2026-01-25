# Market Impact Models

## Overview

Market impact is the price movement caused by an order's presence in the market. It scales with order size relative to available liquidity.

## Model Selection Criteria

| Order Size vs ADV | Recommended Model | Rationale |
|-------------------|-------------------|-----------|
| < 1% | Linear | Simple, conservative |
| 1% - 5% | Square-Root | Standard institutional |
| > 5% | Almgren-Chriss | Separates temp/perm impact |

## Linear Model

**Use Case**: Small orders, conservative estimates

```
impact_bps = coefficient * (order_size / ADV)
```

**Coefficient by Asset Class**:
| Asset Class | Coefficient |
|-------------|-------------|
| Large-cap equities | 5-10 |
| Mid-cap equities | 10-15 |
| Small-cap equities | 15-25 |
| Liquid ETFs | 3-5 |

## Square-Root Model

**Use Case**: Medium orders, standard institutional trading

```
impact_bps = coefficient * sqrt(order_size / ADV) * volatility_factor
```

**Parameters**:
- coefficient: 0.1 - 0.5 (calibrated per market)
- volatility_factor: normalized daily volatility

**Derivation**: Based on Kyle (1985) lambda model where impact scales with sqrt of order flow.

## Almgren-Chriss Model

**Use Case**: Large institutional orders requiring execution optimization

```
total_impact = temporary_impact + permanent_impact

temporary_impact = gamma * sigma * (order_size / ADV)^0.5
permanent_impact = eta * sigma * (order_size / ADV)
```

**Standard Parameters**:
- gamma (temporary): 0.314 (Almgren 2005 estimate)
- eta (permanent): 0.142 (Almgren 2005 estimate)
- sigma: daily volatility

**Key Insight**: Temporary impact decays after execution; permanent impact persists.

## ADV Thresholds

| Order/ADV Ratio | Risk Level | Action |
|-----------------|------------|--------|
| < 0.5% | Low | Standard execution |
| 0.5% - 1% | Moderate | Monitor impact |
| 1% - 2% | Elevated | VWAP/TWAP recommended |
| 2% - 5% | High | Multi-day execution |
| > 5% | Very High | Algorithmic execution required |

## Validation Requirements

- MARKET_IMPACT_MODEL gate requires model selection
- Model must be appropriate for order_size / ADV ratio
- Impact estimate must be non-zero for orders > 0.1% ADV
