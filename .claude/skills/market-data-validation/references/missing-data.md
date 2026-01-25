# Missing Data Handling Reference

Time-series strategies for OHLCV gaps while preserving data integrity.

---

## Strategy Selection Decision Tree

```
Gap Size = 0?
  └── YES → No action required

Gap Size <= 5 bars?
  └── YES → Forward Fill (LOCF)
  
Gap Size 6-20 bars?
  └── Omit with Flagging (add 'is_missing' metadata)
  
Gap Size > 20 bars?
  └── Escalate to user (dataset may be incomplete)

End-of-series gap?
  └── Omit with flagging (NEVER backward fill)
```

---

## Strategy 1: Forward Fill (LOCF)

**Last Observation Carried Forward** - Primary strategy for small gaps.

### When to Use
- Gap size <= 5 bars
- Non-trading days, temporary feed outages
- Trading strategy / backtesting contexts

### Implementation

```python
def forward_fill(df: pd.DataFrame, max_gap: int = 5) -> pd.DataFrame:
    """Forward fill gaps up to max_gap bars."""
    df['data_quality_flag'] = 'valid'
    
    # Identify small gaps
    mask = (df['close'].isna() & 
            (df['close'].isna().groupby(
                df['close'].notna().cumsum()
            ).transform('size') <= max_gap))
    
    # Apply forward fill
    df.loc[mask, 'close'] = df['close'].fillna(method='ffill')
    df.loc[mask, 'data_quality_flag'] = 'forward_filled'
    
    return df
```

---

## Strategy 2: Omit with Flagging

**Conservative approach** - Preserve integrity, let downstream decide.

### When to Use
- Gap size > 5 bars
- Legitimate market closures
- When data quality > completeness

### Implementation

```python
def omit_with_flag(df: pd.DataFrame) -> pd.DataFrame:
    """Flag missing data without filling."""
    df['data_quality_flag'] = 'valid'
    df.loc[df['close'].isna(), 'data_quality_flag'] = 'missing'
    return df
```

---

## Strategy 3: Linear Interpolation (Prices Only)

**Use Cautiously** - Only for very short gaps in exploratory analysis.

### When to Use
- Gap size 1-2 bars only
- High-frequency data visualization
- NEVER for volume (meaningless)

### Implementation

```python
def interpolate_prices(df: pd.DataFrame, max_gap: int = 2) -> pd.DataFrame:
    """Interpolate small price gaps. NEVER use for volume."""
    price_cols = ['open', 'high', 'low', 'close', 'adj_close']
    
    for col in price_cols:
        df[col] = df[col].interpolate(method='linear', limit=max_gap)
    
    # Volume: forward fill only, never interpolate
    df['volume'] = df['volume'].fillna(method='ffill')
    
    return df
```

---

## Anti-Pattern: Backward Fill

**NEVER use in predictive contexts** - Creates look-ahead bias.

```python
# ❌ WRONG - Look-ahead bias
df['close'] = df['close'].fillna(method='bfill')

# ✅ CORRECT - Forward fill or omit
df['close'] = df['close'].fillna(method='ffill')
```

---

## Data Quality Flag Values

| Flag | Meaning | Downstream Action |
|------|---------|-------------------|
| `valid` | Original data, unmodified | Use directly |
| `forward_filled` | Gap filled with previous value | Treat cautiously |
| `interpolated` | Mathematically estimated | May exclude |
| `missing` | Gap not filled | Filter or handle |
