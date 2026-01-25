# Delegation Examples: Sentiment NLP Specialist

**Purpose**: Show how the orchestrator invokes this agent for different operations.

---

## Basic Sentiment Analysis

```markdown
Task(sentiment-nlp-specialist, "analyze_sentiment for AAPL and MSFT headlines from last hour.
Headlines: [
  {text: 'Apple announces record iPhone sales', symbol: 'AAPL', timestamp: '2024-01-15T09:30:00Z', source: 'reuters'},
  {text: 'Microsoft cloud revenue disappoints', symbol: 'MSFT', timestamp: '2024-01-15T09:35:00Z', source: 'bloomberg'}
]
Config: {model_name: 'ProsusAI/finbert', batch_size: 16, confidence_threshold: 0.6}")
```

**Expected Output**:
- sentiment_scores array with polarity, confidence, classification per headline
- processing_stats with total_headlines, avg_confidence, processing_time_ms

---

## Aggregation with Normalization

```markdown
Task(sentiment-nlp-specialist, "aggregate_sentiment for symbols ['AAPL', 'MSFT', 'GOOGL'].
Time bucket: 1hour
Normalization: true
Lookback periods: 24
Weighting method: recency")
```

**Expected Output**:
- aggregated_scores array with zS, zΔS, volume per symbol-bucket
- normalization_params with mean, std_dev, lookback_periods

---

## Burst Detection

```markdown
Task(sentiment-nlp-specialist, "detect_bursts for tech sector symbols.
Volume threshold: 2.0 (2x baseline)
Sentiment shift threshold: 0.3
Baseline window: 1day")
```

**Expected Output**:
- bursts_detected array with burst_type (volume_spike/sentiment_shift/combined)
- baseline_stats per symbol (avg_volume, avg_sentiment)
- significance rating (high/medium/low)

---

## Theme Extraction

```markdown
Task(sentiment-nlp-specialist, "extract_themes from 500 tech headlines.
Max themes: 10
Min frequency: 5
Extraction method: keyword")
```

**Expected Output**:
- themes array with label, keywords, headline_count, affected symbols
- extraction_method used
- avg_sentiment per theme

---

## Multi-Operation Workflow

```markdown
Task(sentiment-nlp-specialist, "Full sentiment pipeline for earnings season:
1. analyze_sentiment for all earnings-related headlines
2. aggregate_sentiment with 1hour buckets, z-score normalization
3. detect_bursts with volume_threshold=2.5, sentiment_shift=0.4
4. extract_themes to identify dominant narratives

Export aggregated features to Parquet for PEAD integration.")
```

---

## Error Handling Example

```markdown
Task(sentiment-nlp-specialist, "analyze_sentiment with GPU preference.
If GPU unavailable, fallback to CPU with reduced batch_size.
If model loading fails, use keyword-based fallback and flag in metadata.")
```

**Expected Behavior**:
- Attempts GPU -> MPS -> CPU in order
- Adjusts batch_size per device capability
- Returns results with fallback_method flag if keyword-based used
