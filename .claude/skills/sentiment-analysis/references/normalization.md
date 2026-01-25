# Normalization Reference

Z-score calculation, rolling baselines, and outlier handling for sentiment normalization.

---

## Z-Score Formula

### Primary Sentiment Score (zS)
```
zS = (raw_score - rolling_mean) / rolling_std
```

Where:
- `raw_score`: FinBERT polarity score (-1 to +1)
- `rolling_mean`: Mean of scores over lookback window
- `rolling_std`: Standard deviation over lookback window

### Sentiment Momentum (zΔS)
```
zΔS = z-score of (current_score - previous_score)
```

This measures rate of change in sentiment, normalized.

---

## Lookback Windows

| Time Bucket | Default Lookback | Periods | Use Case |
|-------------|------------------|---------|----------|
| 1min | 60 periods | 1 hour | High-frequency trading signals |
| 5min | 48 periods | 4 hours | Intraday momentum |
| 15min | 32 periods | 8 hours | Swing trading |
| 1hour | 24 periods | 1 day | Daily sentiment baseline |
| 1day | 20 periods | 1 month | Long-term trends |

### Window Selection Logic
```python
LOOKBACK_WINDOWS = {
    '1min': 60,
    '5min': 48,
    '15min': 32,
    '1hour': 24,
    '1day': 20
}

def get_lookback(time_bucket: str) -> int:
    return LOOKBACK_WINDOWS.get(time_bucket, 20)
```

---

## Baseline Types

### Time-Series Baseline (Default)
- Compare symbol to its own history
- Best for: Momentum signals, detecting shifts
- Calculation: Rolling window per symbol

### Cross-Sectional Baseline (Optional)
- Compare symbol to peer group at same time
- Best for: Relative strength, sector comparison
- Calculation: All symbols in same time bucket

### Selection Criteria
| Goal | Baseline Type |
|------|---------------|
| Detect sentiment momentum | Time-series |
| Find relative strength | Cross-sectional |
| Combine signals | Both (weighted average) |

---

## Outlier Handling

### 3-Sigma Rule
```python
# Clip z-scores to [-3, +3] range
zS_clipped = np.clip(zS, -3, +3)
```

### Flagging Extremes
```python
if abs(zS) > 3:
    result['outlier_flag'] = True
    result['raw_zscore'] = zS
    result['clipped_zscore'] = np.sign(zS) * 3
```

### NaN Handling
- **Insufficient data**: If < 50% of lookback window has data, return NaN
- **Forward-fill**: Missing baselines forward-filled from last valid
- **Documentation**: Flag gaps in metadata

---

## Rolling Calculation

```python
import pandas as pd
import numpy as np

def calculate_zscore(
    scores: pd.Series,
    lookback: int = 20,
    min_periods: int = 10
) -> pd.Series:
    """Calculate rolling z-score for sentiment normalization."""
    rolling_mean = scores.rolling(
        window=lookback,
        min_periods=min_periods
    ).mean()
    
    rolling_std = scores.rolling(
        window=lookback,
        min_periods=min_periods
    ).std()
    
    # Avoid division by zero
    rolling_std = rolling_std.replace(0, np.nan)
    
    zscore = (scores - rolling_mean) / rolling_std
    
    # Clip to 3-sigma
    return zscore.clip(-3, 3)
```

---

## Quality Checks

- [ ] Z-scores distributed (mean ~0, std ~1)
- [ ] No extreme values beyond [-3, +3]
- [ ] NaN flagged with reason
- [ ] Lookback window documented
