# Chandelier Stop Methodology (ATR-Based)

## Core Formulas

**Long Position**:
```
Stop = Highest_High(N) - (ATR(N) x Multiplier)
```

**Short Position**:
```
Stop = Lowest_Low(N) + (ATR(N) x Multiplier)
```

**Defaults**: N = 22 periods, Multiplier = 3.0x

## Trailing Logic (CRITICAL)

**Long**: Stops ONLY move UP - never lower
**Short**: Stops ONLY move DOWN - never raise

```python
# Long position trailing
if new_stop > current_stop:
    stop = new_stop  # Lock profit
else:
    stop = current_stop  # Preserve locked gains
```

## Parameter Selection by Style

| Trading Style | Lookback (N) | ATR Multiplier |
|---------------|--------------|----------------|
| Scalping | 7-10 | 2.0-2.5x |
| Day Trading | 10-14 | 2.5-3.0x |
| **Swing Trading** | **22** | **3.0x** |
| Position Trading | 30-40 | 3.5-4.0x |

## ATR Multiplier by Risk Profile

| Multiplier | Risk Profile | Stop-Out Rate |
|------------|--------------|---------------|
| 2.0-2.5x | Tight | 60-70% |
| **3.0x** | **Standard** | **40-50%** |
| 3.5-4.0x | Wide | 25-35% |

## Delegation Pattern

ATR calculation requires technical-indicator-specialist:

```
1. Request: ATR(22) for ticker
2. Retry: 2x with exponential backoff (1s, 2s)
3. Fallback: 2% fixed stop if ATR unavailable
```

## Workflow

1. Get ATR(22) from technical-indicator-specialist
2. Calculate highest high over 22-period lookback
3. Apply formula: `stop = HH - (ATR x 3.0)`
4. Validate: stop < entry (longs), stop > entry (shorts)
5. Apply trailing logic on each bar close

## Key Rules

- **Same period**: Use identical N for ATR and high/low lookback
- **Bar close only**: Update stops at bar close, not intrabar
- **Cache ATR**: Within trading session (avoid redundant calculations)
- **Max stop distance**: 15% of entry price (sanity check)

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Moving stop against position | Gives back locked profit | Strict directional check |
| Percentage stops | Ignores volatility | Use ATR-based |
| No lookback window | Noise sensitivity | Use 22-period HH/LL |
| Intrabar updates | Whipsaw | Update at bar close only |