# Volatility Regime Detection

**Status**: Post-MVP Enhancement

## Percentile-Based Classification

```python
atr_window = atr[-252:]  # 1-year rolling window
p25, p75 = np.percentile(atr_window, [25, 75])
current_atr = atr[-1]

if current_atr < p25:
    regime = "LOW"
elif current_atr < p75:
    regime = "NORMAL"
else:
    regime = "HIGH"
```

## Regime Multipliers

| Regime | Position Size | Stop Multiplier | Rationale |
|--------|---------------|-----------------|-----------|
| LOW | 1.2x | 2.5x ATR | Larger positions, tighter stops |
| NORMAL | 1.0x | 3.0x ATR | Standard settings |
| HIGH | 0.7x | 4.0x ATR | Smaller positions, wider stops |

## Application

```python
# Base position from 1% risk
base_position = 200 shares

# Apply regime adjustment
LOW:    200 × 1.2 = 240 shares
NORMAL: 200 × 1.0 = 200 shares
HIGH:   200 × 0.7 = 140 shares
```

## Key Parameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Lookback | 252 days | 1-year rolling window |
| ATR period | 22 | Consistent with agent defaults |
| Min data | 126 days | 6-month minimum |

## Validation Rules

1. **Percentile sanity**: `p25 < p75` and both > 0
2. **Stability check**: <=3 regime changes per 5 days
3. **Hysteresis**: 10% buffer to prevent flipping

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| VIX-based | External dependency, symbol mismatch | Use symbol-specific ATR |
| Static thresholds | Ignores symbol volatility profile | Dynamic percentiles |
| No validation | NaN/Inf propagation | Validate before classify |
| Daily flipping | Excessive adjustments | Add hysteresis buffer |

## Integration

- **Input**: ATR(22) from technical-indicator-specialist
- **Output**: Regime label + multipliers for position sizing
- **Frequency**: Daily at market close
