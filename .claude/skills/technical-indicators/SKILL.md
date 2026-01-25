---
name: technical-indicators
description: >
  Computes technical indicators using TA-Lib with pandas-ta fallback.
  Use when calculating EMA, RSI, ATR, ADX, OBV, MFI or handling indicator edge cases.
  Trigger keywords: technical indicators, TA-Lib, EMA, RSI, ATR, vectorization.
---

# Technical Indicators

Compute technical indicators with high performance and robust edge case handling.

---

## Indicator Catalog

### Trend Indicators

| Indicator | Formula | Lookback | Use Case |
|-----------|---------|----------|----------|
| **EMA** | EMA_t = (Price_t * k) + (EMA_{t-1} * (1-k)), k=2/(n+1) | 20 | Trend direction, support/resistance |
| **ADX** | ADX = SMA(DX, n), DX = abs(+DI - -DI) / (+DI + -DI) | 14 | Trend strength (>25 strong, <20 weak) |

### Momentum Indicators

| Indicator | Formula | Lookback | Use Case |
|-----------|---------|----------|----------|
| **RSI** | RSI = 100 - (100 / (1 + RS)), RS = AvgGain/AvgLoss | 14 | Overbought (>70) / Oversold (<30) |

### Volatility Indicators

| Indicator | Formula | Lookback | Use Case |
|-----------|---------|----------|----------|
| **ATR** | ATR = SMA(TrueRange, n), TR = max(H-L, abs(H-C_prev), abs(L-C_prev)) | 14 | Position sizing, stop-loss placement |


### Volume Indicators

| Indicator | Formula | Lookback | Use Case |
|-----------|---------|----------|----------|
| **OBV** | OBV_t = OBV_{t-1} + (Volume if Close > Close_prev else -Volume) | N/A | Accumulation/distribution flow |
| **MFI** | MFI = 100 - (100 / (1 + MF_Ratio)), volume-weighted RSI | 14 | Volume-confirmed momentum |

---

## Performance SLA

| Dataset Size | Max Latency | Memory Limit |
|--------------|-------------|--------------|
| 10K rows | 1 second | 200MB |
| 100K rows | 5 seconds | 200MB |
| 1M+ rows | 30 seconds | 200MB (chunked) |

---

## Confidence Scoring

**Base Confidence**: 0.90 (deterministic computation)

| Factor | Adjustment |
|--------|------------|
| Data Quality Penalty | -0.05 per 10% missing data |
| History Penalty | -0.10 if insufficient lookback (<50% required) |
| Validation Bonus | +0.05 if golden dataset validation passes |

---

## Workflow

```
1. Load Data → 2. Validate OHLCV Schema → 3. Check Lookback Sufficiency
        ↓                  ↓                        ↓
4. Compute Indicators (batch) → 5. Handle Edge Cases → 6. Return Wide-Format Output
```

---

## Reference Documentation

| Reference | Purpose |
|-----------|---------|
| [references/talib-wrapper.md](references/talib-wrapper.md) | TA-Lib integration, pandas-ta fallback, function mapping |
| [references/edge-cases.md](references/edge-cases.md) | Missing data, insufficient history, zero volume handling |
| [references/vectorization.md](references/vectorization.md) | No row loops, rolling/shift patterns, chunking strategy |

---

## Anti-Patterns

| Anti-Pattern | Why Wrong | Correct Approach |
|--------------|-----------|------------------|
| Forward/backward fill missing data | Introduces bias in technical signals | Skip period, return NaN |
| Row-by-row iteration | 100x+ slower than vectorized ops | Use pandas/numpy vectorization |
| Exceed 200MB without chunking | Memory pressure, OOM risk | Chunk into 50MB segments |
| Return fabricated values | Misleading signals | Return NaN + log warning |
