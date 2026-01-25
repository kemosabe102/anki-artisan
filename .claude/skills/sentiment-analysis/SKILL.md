---
name: sentiment-analysis
description: >
  Analyzes financial sentiment using FinBERT with z-score normalization and burst detection.
  Use when classifying news sentiment, aggregating sentiment scores, or detecting sentiment bursts.
  Trigger keywords: sentiment analysis, FinBERT, z-score, sentiment burst, PEAD.
---

# Sentiment Analysis

Transform news headlines into quantitative sentiment signals using FinBERT, statistical normalization, and burst detection.

---

## Quick Reference

### FinBERT Classification

| Output | Range | Description |
|--------|-------|-------------|
| polarity | positive/negative/neutral | Sentiment class |
| confidence | 0.0 - 1.0 | Classification confidence |

**Minimum confidence threshold**: 0.6 for accepted classifications.

### Device Detection

```python
# Priority: CUDA -> MPS -> CPU
device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
```

| Device | Batch Size | Timeout |
|--------|------------|---------|
| GPU (CUDA) | 32 | 30s |
| GPU (MPS) | 16 | 30s |
| CPU | 8 | 60s |

---

## Output Format

Aggregated sentiment features (Parquet export):

| Column | Type | Description |
|--------|------|-------------|
| symbol | string | Stock ticker |
| time_bucket | datetime | Bucket start time |
| zS | float | Normalized sentiment (z-score) |
| zΔS | float | Sentiment momentum (z-score of change) |
| volume | int | Headline count in bucket |
| confidence | float | Average classification confidence |

---

## Workflow

1. **Load Model** - Lazy load FinBERT on first inference (not session start)
2. **Batch Inference** - Process headlines with device-appropriate batch size
3. **Aggregate** - Group by symbol and time bucket
4. **Normalize** - Apply z-score using rolling baselines
5. **Detect Bursts** - Identify volume spikes and sentiment momentum
6. **Export** - Output features for downstream consumption

---

## Reference Documentation

Detailed specifications (read when relevant):

- **Model Lifecycle** -> [references/finbert-lifecycle.md](references/finbert-lifecycle.md)
  - Lazy loading, device detection, batch adaptation, memory management
  
- **Normalization** -> [references/normalization.md](references/normalization.md)
  - Z-score formula, rolling baselines, lookback windows, outlier handling
  
- **Burst Detection** -> [references/burst-detection.md](references/burst-detection.md)
  - Volume spike detection, sentiment momentum, PEAD boost (+0.2)

---

## Integration Points

### PEAD Enhancement

- Provide `sentiment_score` field for PEAD detector
- Apply +0.2 boost on positive earnings surprise with positive sentiment
- Ensure temporal alignment with PEAD event windows

### Fallback Strategy

When FinBERT fails:
1. Switch to keyword-based sentiment (positive/negative word counts)
2. Mark results as `fallback_method: keyword`
3. Continue processing with degraded confidence

---

## Anti-Patterns

**NEVER:**
- Store raw news text beyond processing (aggregated scores only)
- Generate trading recommendations (sentiment signals only)
- Skip device detection (always check GPU/CPU availability)
- Use static batch sizes (adapt to device type)
- Ignore confidence thresholds (filter low-confidence results)

**ALWAYS:**
- Lazy-load model (first inference, not session start)
- Apply z-score normalization with rolling baselines
- Include confidence scores with all classifications
- Cache results by headline hash
- Provide fallback when FinBERT fails
