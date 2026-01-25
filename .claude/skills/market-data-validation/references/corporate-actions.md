# Corporate Actions Reference

CRSP methodology for stock splits, dividends, and historical price adjustments.

---

## Stock Split Adjustment

### Formula
```
adjusted_price = price * (1 / split_ratio)
adjusted_volume = volume * split_ratio
```

### Examples

| Event | Ratio | Price Before | Price After | Volume Before | Volume After |
|-------|-------|--------------|-------------|---------------|--------------|
| 2-for-1 | 2.0 | $100 | $50 | 1000 | 2000 |
| 3-for-1 | 3.0 | $150 | $50 | 1000 | 3000 |
| 1-for-10 (reverse) | 0.1 | $5 | $50 | 10000 | 1000 |

### Implementation

```python
def apply_split(df: pd.DataFrame, split_date: str, ratio: float) -> pd.DataFrame:
    """Apply split adjustment to historical prices."""
    mask = df['timestamp'] < split_date
    
    # Adjust prices (divide by ratio)
    for col in ['open', 'high', 'low', 'close', 'adj_close']:
        df.loc[mask, col] = df.loc[mask, col] / ratio
    
    # Adjust volume (multiply by ratio)
    df.loc[mask, 'volume'] = df.loc[mask, 'volume'] * ratio
    
    return df
```

---

## Dividend Adjustment

### Formula
```
adjustment_factor = 1 - (dividend / close_price_on_ex_date)
adjusted_price = price * adjustment_factor
```

### Example
- Close on ex-date: $50
- Dividend: $1
- Factor: 1 - (1/50) = 0.98
- $100 historical price -> $98 adjusted

### Implementation

```python
def apply_dividend(df: pd.DataFrame, ex_date: str, 
                   dividend: float, ex_close: float) -> pd.DataFrame:
    """Apply dividend adjustment to historical prices."""
    factor = 1 - (dividend / ex_close)
    mask = df['timestamp'] < ex_date
    
    for col in ['open', 'high', 'low', 'close', 'adj_close']:
        df.loc[mask, col] = df.loc[mask, col] * factor
    
    # Volume NOT adjusted for dividends
    return df
```

---

## CRSP Methodology

### Key Principles

1. **Direction**: Adjustments applied retroactively (before event date)
2. **Cumulative**: Multiple events compound adjustment factors
3. **Ex-Date**: Use ex-dividend date, not record date
4. **Precision**: Minimum 6 decimal places to avoid rounding errors

### Processing Order

```
Most Recent Event --> Oldest Event
     ↓
Each event adjusts all rows BEFORE its date
     ↓
Cumulative factor tracked for audit
```

---

## Validation Rules

### Adjustment Factor Bounds
```python
assert 0.01 < adjustment_factor < 100, "Factor out of range"
```

### Precision Requirement
```python
MINIMUM_PRECISION = 6  # decimal places
df['adj_close'] = df['adj_close'].round(MINIMUM_PRECISION)
```

### Post-Adjustment Checks
- No negative prices introduced
- High >= Low still holds
- Chronological order preserved

---

## Preserving Unadjusted Data

Always store original prices for auditability:

```python
df['close_unadjusted'] = df['close'].copy()
df['adjustment_factor'] = 1.0

# After all adjustments:
df['close_adjusted'] = df['close_unadjusted'] * df['adjustment_factor']
```

---

## Source References

- [CRSP Calculations](https://www.crsp.org/products/documentation/crsp-calculations)
- [StockCharts Adjustment Guide](https://school.stockcharts.com/doku.php?id=data)
