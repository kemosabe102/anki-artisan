# Domain Expertise: Financial Sentiment NLP

**Purpose**: Technical specifications for FinBERT sentiment analysis, statistical normalization, and integration patterns.

---

## FinBERT Model Lifecycle Management

### Lazy Loading Strategy
- Load FinBERT only when first inference requested (not session start)
- Device detection: Check GPU availability (CUDA/MPS) -> fallback to CPU
- Model caching: Keep model in memory for session, reload only on version change
- Version tracking: Log model_version in all outputs for reproducibility

### Device Detection & Selection
```python
# Priority order: CUDA -> MPS -> CPU
device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
```

### Model Parameters
| Parameter | GPU Value | CPU Value | Description |
|-----------|-----------|-----------|-------------|
| batch_size | 32 | 8 | Headlines per inference batch |
| max_length | 128 | 128 | Max token length |
| timeout | 30s | 60s | Per-batch timeout |

### Memory Management
- Monitor cache size, evict LRU entries if >500MB
- GPU: Use batching for parallel inference
- CPU: Sequential processing to avoid thrashing

---

## Statistical Normalization Standards

### Z-Score Calculation
```
zS = (raw_score - rolling_mean) / rolling_std
zΔS = z-score of (current_score - previous_score)
```

### Lookback Windows
| Time Bucket | Default Lookback | Use Case |
|-------------|------------------|----------|
| 1min | 60 periods (1 hour) | High-frequency trading signals |
| 5min | 48 periods (4 hours) | Intraday momentum |
| 15min | 32 periods (8 hours) | Swing trading |
| 1hour | 24 periods (1 day) | Daily sentiment baseline |
| 1day | 20 periods (1 month) | Long-term trends |

### Outlier Handling
- Clip z-scores to [-3, +3] range (3-sigma rule)
- Flag extreme values for review
- NaN handling: Forward-fill missing baselines, flag insufficient data

### Cross-Sectional vs Time-Series
- **Time-series**: Compare symbol to its own history (default)
- **Cross-sectional**: Compare symbol to peer group (optional)
- Choice depends on use case: momentum (time-series) vs relative strength (cross-sectional)

---

## Batch Processing Strategy

### GPU Processing
- batch_size=32, parallel inference
- Memory bound: ~4GB VRAM for FinBERT
- Timeout: 30s per batch, retry with smaller batch on failure

### CPU Processing
- batch_size=8, sequential inference
- No memory bound concerns
- Timeout: 60s per batch, more forgiving

### Adaptive Strategy
```python
if device == "cuda":
    batch_size = min(32, config.batch_size)
elif device == "mps":
    batch_size = min(16, config.batch_size)
else:
    batch_size = min(8, config.batch_size)
```

---

## Integration Specifications

### News Connector Input Format
```json
{
  "text": "Company XYZ reports record earnings",
  "symbol": "XYZ",
  "timestamp": "2024-01-15T09:30:00Z",
  "source": "reuters"
}
```

### Feature Export Format (Parquet)
| Column | Type | Description |
|--------|------|-------------|
| symbol | string | Stock ticker |
| time_bucket | datetime | Bucket start time |
| zS | float | Normalized sentiment |
| zΔS | float | Sentiment momentum |
| volume | int | Headline count |
| confidence | float | Avg classification confidence |

### PEAD Enhancement Hook
- Provide sentiment_score field for PEAD detector consumption
- +0.2 score boost on positive earnings surprises with positive sentiment
- Temporal alignment: Sentiment buckets must align with PEAD event windows

### Burst Alert Format
```json
{
  "symbol": "XYZ",
  "timestamp": "2024-01-15T09:30:00Z",
  "burst_type": "combined",
  "metrics": {
    "volume_multiplier": 3.5,
    "sentiment_change": 0.45
  },
  "significance": "high"
}
```

---

## Error Recovery Patterns

| Error Type | Recovery Strategy | Fallback |
|------------|-------------------|----------|
| Model loading failure | Retry with CPU device | Keyword-based sentiment |
| Inference timeout | Reduce batch_size by 50% | Continue with partial results |
| Normalization error | Use global baseline | Flag as NaN, document gap |
| Resource exhausted | Escalate to orchestrator | Report memory/GPU requirements |

---

## Quick Reference

- [ ] Model loaded with correct device
- [ ] Sentiment scores in bounds (polarity [-1, 1], confidence [0, 1])
- [ ] Z-scores normalized (mean ~0, std ~1)
- [ ] No raw text stored beyond aggregation
- [ ] Cache size within bounds (<500MB)
