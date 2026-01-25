# 200DMA Trend Classification

**Status**: Core Feature

## Methodology

The 200-day moving average (200DMA) serves as a long-term trend filter:

```python
sma_200 = SMA(close, period=200)
current_price = close[-1]

if current_price > sma_200:
    trend = "above_200dma"  # Bullish
else:
    trend = "below_200dma"  # Bearish
```

## Trading Implications

| Trend Filter | Strategy Bias | Position Sizing |
|--------------|---------------|-----------------|
| above_200dma | Long only | 100% of calculated size |
| below_200dma | Short or cash | 50% or 0% depending on strategy |


## Integration with Volatility Regime

The 200DMA filter COMBINES with volatility regime:

| Scenario | Trend | Regime | Recommendation |
|----------|-------|--------|----------------|
| Bullish calm | above | LOW | Full size, tight stops |
| Bullish normal | above | NORMAL | Standard sizing |
| Bullish volatile | above | HIGH | Reduced size, wide stops |
| Bearish calm | below | LOW | Reduce exposure |
| Bearish volatile | below | HIGH | Minimal or no exposure |

## Validation Rules

1. **Warmup**: Requires 200 bars minimum
2. **Hysteresis**: 1% buffer to prevent whipsaws (price must cross by 1%)
3. **Confirmation**: Use closing prices, not intraday

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Intraday 200DMA | False signals | Use daily close only |
| No buffer | Whipsaw in sideways | Add 1% hysteresis |
| Single bar cross | Noise | Require 3-day confirmation |
