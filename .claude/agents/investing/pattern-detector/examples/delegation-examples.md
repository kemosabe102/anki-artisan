# Pattern Detector Delegation Examples

## 1. Pattern Detection Workflow

```markdown
Task(pattern-detector,
  "Detect breakout and pullback patterns for AAPL 1d timeframe.
   Data source: packages/core/data/outputs/AAPL_1d_ohlcv.parquet.
   Pattern types: [breakout, pullback].
   Detection sensitivity: balanced.")
```

**Expected Output**:
```json
{
  "status": "SUCCESS",
  "patterns_detected": [
    {
      "pattern": "breakout",
      "timestamp": "2025-11-15T14:30:00Z",
      "confidence": 0.82,
      "direction": "up",
      "evidence_bundle": {
        "volume_multiplier": 2.3,
        "adx": 28.5,
        "channel_high": 148.50
      }
    }
  ],
  "metadata": {
    "regime": "trending",
    "context_quality": 0.89
  }
}
```

## 2. Detector Validation Workflow

```markdown
Task(pattern-detector,
  "Validate breakout detector against golden dataset.
   Golden dataset: tests/fixtures/patterns/golden_breakout_labels.parquet.
   Metrics: [precision, recall, f1_score, mcc].
   Confidence thresholds: [0.5, 0.7, 0.9].")
```

**Expected Output**:
```json
{
  "status": "SUCCESS",
  "validation_metrics": {
    "precision": 0.78,
    "recall": 0.85,
    "f1_score": 0.81,
    "mcc": 0.72
  },
  "recommended_threshold": 0.7,
  "confusion_matrix": {"TP": 85, "FP": 24, "TN": 156, "FN": 15}
}
```

## 3. Pattern Explanation Workflow

```markdown
Task(pattern-detector,
  "Explain the breakout pattern detected for AAPL at 2025-11-15T14:30:00Z.
   Explanation depth: detailed.")
```

**Expected Output**:
```json
{
  "status": "SUCCESS",
  "evidence_bundle": {
    "detection_logic": [
      "1. Volume 2.3x > 1.5x threshold (PASS)",
      "2. Close $150.25 > Donchian high $148.50 (PASS)",
      "3. ADX 28.5 > 25 threshold (PASS)"
    ],
    "confidence_factors": [
      {"factor": "volume_confirmation", "contribution": 0.1},
      {"factor": "adx_trending", "contribution": 0.1},
      {"factor": "base_breakout", "contribution": 0.6}
    ],
    "total_confidence": 0.8
  }
}
```

## 4. Multi-Pattern Conflict Resolution

```markdown
Task(pattern-detector,
  "Detect all patterns for TSLA 1h timeframe with conflict resolution.
   Pattern types: [breakout, pullback, divergence].
   Conflict strategy: hierarchical_priority.")
```

**When breakout and pullback conflict at same timestamp**:
- Hierarchical priority applies regime-based ranking
- Trending regime: breakout wins
- Conflict penalty reduces final confidence
- Audit log captures resolution path

## 5. PEAD Detection with Sentiment Delegation

```markdown
Task(pattern-detector,
  "Detect PEAD patterns for NVDA around earnings_date 2025-10-20.
   Include sentiment integration from sentiment-nlp-specialist.")
```

**Internal Delegation Chain**:
1. pattern-detector receives task
2. Delegates to technical-indicator-specialist for ATR, volume indicators
3. Delegates to sentiment-nlp-specialist for zS sentiment score
4. Combines SUE formula + sentiment + gap detection
5. Returns PEAD pattern with full evidence bundle
