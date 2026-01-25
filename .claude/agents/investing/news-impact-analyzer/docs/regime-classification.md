# Regime Classification Methodology

## Overview

The regime classification system uses a 5-factor composite score to determine market risk appetite (risk_off, neutral, risk_on). This classification drives the regime_multiplier used in impact calculations.

## 5-Factor Methodology

### Factor Weights

| Factor | Weight | Source Table | Description |
|--------|--------|--------------|-------------|
| VIX_inverse | 25% | risk_sentiment | Inverse of VIX (fear gauge) |
| fear_greed | 25% | risk_sentiment | CNN Fear & Greed Index |
| HY_spread | 20% | risk_sentiment | High-yield credit spreads |
| put_call_ratio | 15% | risk_sentiment | Options market sentiment |
| 200DMA_position | 15% | market data | S&P 500 vs 200-day MA |

### Normalization

Each factor is normalized to 0-100 scale:
- **VIX_inverse**: `100 - min(VIX, 80)` (capped at 80)
- **fear_greed**: Direct 0-100 scale
- **HY_spread**: `100 - (spread_bps / 10)` (wider = more fear)
- **put_call_ratio**: `100 - min(ratio * 100, 100)` (higher ratio = more fear)
- **200DMA_position**: `50 + (pct_above_200dma * 50)` (above = bullish)

### Composite Score Calculation

```python
composite = (
    VIX_inverse * 0.25 +
    fear_greed * 0.25 +
    HY_spread_normalized * 0.20 +
    put_call_normalized * 0.15 +
    DMA_position * 0.15
)
```


## Regime Thresholds

| Classification | Score Range | Market Behavior | Multiplier |
|----------------|-------------|-----------------|------------|
| risk_off | 0-30 | Fear dominant, flight to safety | 1.5x |
| neutral | 31-69 | Balanced sentiment | 1.0x |
| risk_on | 70-100 | Greed dominant, risk-seeking | 0.7x |

## Confidence Scoring

Regime confidence is calculated based on:
1. **Data freshness**: Full confidence if <24h, degraded if >3 days
2. **Factor agreement**: Higher when factors align, lower when divergent
3. **Score extremity**: More confident at extremes (0-15, 85-100)

```python
confidence = base_confidence * freshness_factor * agreement_factor * extremity_bonus
```

## Fallback Hierarchy

When primary data unavailable:

1. **Primary**: Full 5-factor from risk_sentiment table
2. **Secondary**: VIX-only classification
   - VIX > 30: risk_off
   - VIX 15-30: neutral
   - VIX < 15: risk_on
3. **Tertiary**: Default to neutral with LOW_CONFIDENCE flag

## SQL Query Pattern

```sql
SELECT 
    vix_inverse,
    fear_greed_index,
    hy_spread_normalized,
    put_call_ratio,
    sp500_vs_200dma,
    composite_score,
    recorded_at
FROM risk_sentiment
WHERE recorded_at <= $analysis_date
ORDER BY recorded_at DESC
LIMIT 1;
```

## Edge Cases

- **Regime transition**: If score within 5 points of threshold, reduce confidence by 20%
- **Conflicting signals**: VIX and fear_greed diverge > 30 points = flag uncertainty
- **Stale data**: >7 days old = use with 0.6x confidence multiplier
