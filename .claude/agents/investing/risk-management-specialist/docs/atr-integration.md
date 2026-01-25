# ATR Integration Patterns

## Delegation Pattern

**Always delegate ATR to technical-indicator-specialist** - never compute directly.

```python
atr_request = {
    "symbol": "AAPL",
    "indicator": "ATR",
    "timeperiod": 22,
    "data_rows": 100  # Include buffer for stability
}
# Returns wide-format Parquet with ATR_22 column
```

## Data Requirements

| ATR Period | Minimum Rows | Recommended |
|------------|--------------|-------------|
| 14 | 34 | 50+ |
| 22 | 42 | 70+ |

**Why buffer?** Wilder's smoothing needs ~15-20 rows to stabilize (unstable period).

## NaN Handling

First `timeperiod` values are NaN by design.

```python
atr_values = df['ATR_22'].dropna()
if len(atr_values) == 0:
    # Fallback to fixed stop
    stop_distance = entry_price * fallback_pct  # See asset-class table in agent.md
else:
    stop_distance = atr_values.iloc[-1] * multiplier
```

## Retry Pattern

```python
max_retries = 2
delays = [1000, 2000]  # ms, exponential backoff

for attempt in range(max_retries + 1):
    result = delegate_atr(symbol, period=22)
    if result.status == "SUCCESS":
        return result.atr_value
    if attempt < max_retries:
        time.sleep(delays[attempt] / 1000)

# All retries failed - use fallback
return fallback_fixed_stop(entry_price, pct=0.02)
```

## Caching Strategy

```python
class ATRCache:
    ttl = timedelta(minutes=15)  # Intraday
    # ttl = timedelta(days=1)    # Daily systems
    
    def get(self, symbol, period):
        key = f"{symbol}:ATR_{period}"
        if key in cache and not expired:
            return cache[key]
        return None
```

## Validation Checks

| Check | Pass Criteria | Fail Action |
|-------|---------------|-------------|
| ATR > 0 | Non-zero volatility | Use 2% fixed stop |
| ATR/Price ratio | 1-20% range | Log warning, validate data |
| Non-NaN count | >= 1 valid value | Request more history |

## Anti-Patterns

- **EMA instead of Wilder's**: ATR uses `((Prior × (N-1)) + TR) / N`, not standard EMA
- **No NaN handling**: Causes runtime errors
- **No caching**: Slow backtests, excessive API calls
- **Direct TA-Lib calls**: Bypass specialist agent coordination
