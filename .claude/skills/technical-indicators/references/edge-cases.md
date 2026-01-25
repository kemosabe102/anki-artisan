# Edge Cases Reference

Handling strategies for data quality issues in technical indicator computation.

---

## Core Principles

1. **No Data Fabrication**: Never forward/backward fill missing price/volume data
2. **Best-Effort Computation**: Compute with available data, annotate with confidence penalty
3. **Transparent Warnings**: Log all edge cases with structured format
4. **Fail-Safe Defaults**: Return NaN for uncomputable periods

---

## Missing Data

**Detection**:
```python
if pd.isna(df[['open', 'high', 'low', 'close', 'volume']]).any(axis=1).any():
    missing_indices = df[pd.isna(df[...]).any(axis=1)].index
```

**Handling**: SKIP PERIOD (return NaN)

**Warning Format**:
```json
{
  "type": "MISSING_DATA",
  "index": 42,
  "message": "Missing OHLCV data, skipping indicator computation",
  "severity": "WARNING"
}
```


---

## Insufficient History

**Detection**:
```python
required_periods = indicator_params.get('lookback', 14)
available_periods = len(df)
if available_periods < required_periods:
    confidence_penalty = available_periods / required_periods
```

**Handling**: COMPUTE with available data + apply confidence_penalty

**Warning Format**:
```json
{
  "type": "INSUFFICIENT_HISTORY",
  "indicator": "RSI",
  "required": 14,
  "available": 10,
  "confidence_penalty": 0.71,
  "severity": "WARNING"
}
```

---

## Zero Volume

**Detection**:
```python
zero_volume_mask = df['volume'] == 0
```

**Handling by Indicator Type**:

| Indicator Type | Action |
|---------------|--------|
| VWAP, RVOL, MFI | SKIP PERIOD (return NaN) |
| OBV (cumulative) | CARRY FORWARD prior value |


**Warning Format**:
```json
{
  "type": "ZERO_VOLUME",
  "index": 87,
  "indicator": "OBV",
  "action": "carried_forward",
  "severity": "INFO"
}
```

---

## Extreme Values

**Detection Thresholds**:
- Price: >20% single-period move
- Volume: >10x rolling 20-period average

**Handling**: LOG WARNING + PROCEED (flag for review)

**Warning Format**:
```json
{
  "type": "EXTREME_VALUE",
  "category": "PRICE",
  "price_change_pct": 23.5,
  "message": "Verify data quality",
  "severity": "WARNING"
}
```

---

## Confidence Penalties Summary

| Edge Case | Penalty |
|-----------|---------|
| Missing data (per 10%) | -0.05 |
| Insufficient history (<50%) | -0.10 |
| Zero volume (volume indicators) | NaN (skip) |
| Extreme values | No penalty (compute with flag) |
