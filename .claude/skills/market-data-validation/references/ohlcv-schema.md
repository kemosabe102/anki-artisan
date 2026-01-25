# OHLCV Schema Reference

Complete specification for OHLCV (Open, High, Low, Close, Volume) data validation.

---

## 8-Field Schema

### Field Definitions

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| **open** | float64 | >= 0 | Opening price for time period |
| **high** | float64 | >= 0 | Highest price during time period |
| **low** | float64 | >= 0 | Lowest price during time period |
| **close** | float64 | >= 0 | Closing price for time period |
| **volume** | int64 | >= 0 | Number of shares/contracts traded |
| **timestamp** | datetime64 | ISO 8601 UTC | Format: YYYY-MM-DDTHH:MM:SSZ |
| **adj_close** | float64 | >= 0 | Corporate-action adjusted close |
| **ticker** | string | 1-5 chars | Uppercase alphanumeric symbol |

### Type Validation

```python
expected_types = {
    'open': 'float64',
    'high': 'float64',
    'low': 'float64',
    'close': 'float64',
    'volume': 'int64',
    'timestamp': 'datetime64[ns, UTC]',
    'adj_close': 'float64',
    'ticker': 'object'  # string
}
```

---

## 7 Consistency Rules

### Rule 1: High >= max(Open, Close)
High must be at least as large as both Open and Close.

```python
violations = df[df['high'] < df[['open', 'close']].max(axis=1)].index
```

### Rule 2: Low <= min(Open, Close)
Low must be at most as small as both Open and Close.

```python
violations = df[df['low'] > df[['open', 'close']].min(axis=1)].index
```

### Rule 3: High >= Low
High cannot be less than Low (basic price range sanity).

```python
violations = df[df['high'] < df['low']].index
```

### Rule 4: Volume >= 0
Volume cannot be negative.

```python
violations = df[df['volume'] < 0].index
```

### Rule 5: No Negative Prices
All price fields must be non-negative.

```python
price_cols = ['open', 'high', 'low', 'close', 'adj_close']
for col in price_cols:
    violations.extend(df[df[col] < 0].index)
```


### Rule 6: Chronological Ordering
Timestamps must be strictly increasing (no duplicates, no reversals).

```python
violations = df[df['timestamp'].diff() <= pd.Timedelta(0)].index
```

### Rule 7: Valid Ticker Format
1-5 uppercase alphanumeric characters.

```python
import re
violations = df[~df['ticker'].str.match(r'^[A-Z0-9]{1,5}$')].index
```

---

## Validation Report Structure

```python
validation_result = {
    'status': 'PASS' | 'FAIL',
    'total_rows': int,
    'violations': list[int],  # row indices
    'violation_rate': float,  # violations / total_rows
    'rules_failed': list[str],  # e.g., ['Rule 1', 'Rule 5']
    'timestamp': 'ISO 8601 UTC'
}
```

---

## Example Validation Output

```json
{
  "status": "FAIL",
  "total_rows": 252,
  "violations": [45, 87, 201],
  "violation_rate": 0.0119,
  "rules_failed": ["Rule 1"],
  "timestamp": "2025-01-15T10:30:00Z"
}
```

---

## Source References

- [FINRA Rule 6893](https://www.finra.org/rules-guidance/rulebooks/finra-rules/6893)
- [ISO 8601 Standard](https://www.iso.org/iso-8601-date-and-time-format.html)
