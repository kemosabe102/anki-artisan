# Burst Detection Reference

Volume spike detection, sentiment momentum, and PEAD enhancement patterns.

---

## Burst Types

### 1. Volume Burst
News volume spike relative to baseline.

```python
volume_multiplier = current_volume / rolling_mean_volume
is_volume_burst = volume_multiplier >= 2.5
```

### 2. Sentiment Burst
Rapid sentiment shift (momentum).

```python
sentiment_change = current_zS - previous_zS
is_sentiment_burst = abs(sentiment_change) >= 0.4
```

### 3. Combined Burst
Both volume and sentiment spike together (strongest signal).

```python
is_combined_burst = is_volume_burst and is_sentiment_burst
```

---

## Detection Thresholds

| Burst Type | Default Threshold | Configurable |
|------------|-------------------|--------------|
| Volume multiplier | >= 2.5x baseline | Yes |
| Sentiment change | >= 0.4 z-score | Yes |
| Combined | Both conditions | N/A |

### Significance Levels

| Level | Criteria |
|-------|----------|
| **High** | Combined burst OR volume >= 5x |
| **Medium** | Volume burst (2.5-5x) OR sentiment burst |
| **Low** | Volume 1.5-2.5x with any sentiment change |

---

## Burst Alert Format

```json
{
  "symbol": "XYZ",
  "timestamp": "2024-01-15T09:30:00Z",
  "burst_type": "combined",
  "metrics": {
    "volume_multiplier": 3.5,
    "sentiment_change": 0.45,
    "current_zS": 1.8,
    "previous_zS": 1.35
  },
  "significance": "high",
  "baseline_period": "1hour"
}
```

---

## PEAD Enhancement

### Post-Earnings Announcement Drift
When earnings surprise and sentiment align, boost prediction confidence.

### Enhancement Rule
```python
def apply_pead_boost(
    sentiment_score: float,
    earnings_surprise: str,  # 'positive' | 'negative' | 'neutral'
    sentiment_polarity: str  # 'positive' | 'negative' | 'neutral'
) -> float:
    """Apply +0.2 boost when earnings and sentiment align."""
    if earnings_surprise == 'positive' and sentiment_polarity == 'positive':
        return sentiment_score + 0.2
    elif earnings_surprise == 'negative' and sentiment_polarity == 'negative':
        return sentiment_score - 0.2  # Reinforce negative
    return sentiment_score
```

### Temporal Alignment
- Sentiment buckets must align with PEAD event windows
- Event window: [-1 day, +3 days] around announcement
- Sentiment aggregation: Match PEAD time granularity

---

## Baseline Calculation

### Volume Baseline
```python
# Rolling mean of headline counts
volume_baseline = df.groupby('symbol')['volume'].rolling(
    window=lookback,
    min_periods=lookback // 2
).mean()
```

### Sentiment Baseline
```python
# Same as z-score baseline
sentiment_baseline = df.groupby('symbol')['raw_sentiment'].rolling(
    window=lookback,
    min_periods=lookback // 2
).mean()
```

---

## Detection Algorithm

```python
def detect_bursts(
    current: dict,
    baseline: dict,
    thresholds: dict
) -> dict:
    """Detect news bursts across volume and sentiment."""
    result = {
        'volume_burst': False,
        'sentiment_burst': False,
        'combined_burst': False,
        'significance': 'none'
    }
    
    # Volume check
    volume_ratio = current['volume'] / max(baseline['volume'], 1)
    if volume_ratio >= thresholds.get('volume_multiplier', 2.5):
        result['volume_burst'] = True
        result['volume_multiplier'] = volume_ratio
    
    # Sentiment check
    sentiment_delta = abs(current['zS'] - baseline['zS'])
    if sentiment_delta >= thresholds.get('sentiment_change', 0.4):
        result['sentiment_burst'] = True
        result['sentiment_change'] = sentiment_delta
    
    # Combined check
    result['combined_burst'] = result['volume_burst'] and result['sentiment_burst']
    
    # Significance
    if result['combined_burst'] or volume_ratio >= 5:
        result['significance'] = 'high'
    elif result['volume_burst'] or result['sentiment_burst']:
        result['significance'] = 'medium'
    elif volume_ratio >= 1.5:
        result['significance'] = 'low'
    
    return result
```

---

## Integration with PEAD Detector

### Input Format
```python
sentiment_features = {
    'symbol': 'XYZ',
    'sentiment_score': 0.85,  # After any boosts
    'zS': 1.8,
    'zΔS': 0.45,
    'volume': 15,
    'confidence': 0.92,
    'burst_detected': True,
    'burst_type': 'combined',
    'timestamp': '2024-01-15T09:30:00Z'
}
```

### PEAD Consumption
- PEAD detector reads `sentiment_score` for drift prediction
- Burst detection flags inform alert priority
- Temporal alignment ensures causality
