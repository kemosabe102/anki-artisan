# Domain Expertise: Technical Indicator Computation

**Purpose**: Core concepts, indicator formulas, and implementation patterns for technical analysis

---

## Technical Analysis Foundations

### Volume as Leading Indicator
- **OBV (On-Balance Volume)**: Price follows volume; accumulation/distribution detection
- Volume confirms price movements; divergence signals potential reversals
- High volume on breakouts validates trend strength

### Momentum Ranking Frameworks
- **ROC (Rate of Change)**: Simple percentage change over N periods
- **Relative Strength**: Compare asset performance vs benchmark (not RSI)
- **Clenow Method**: Momentum portfolio construction using exponential regression

### Statistical Measures
- **Z-scores**: Normalize indicators for cross-asset comparison
- **Percentiles**: Rank current value within historical distribution
- **Standard Deviations**: Define volatility bands and outlier detection

---

## Indicator Specifications

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
| **Donchian** | Upper = max(High, n), Lower = min(Low, n) | 20 | Breakout detection, range boundaries |

### Volume Indicators

| Indicator | Formula | Lookback | Use Case |
|-----------|---------|----------|----------|
| **OBV** | OBV_t = OBV_{t-1} + (Volume if Close > Close_prev else -Volume) | N/A | Accumulation/distribution flow |
| **RVOL** | RVOL = Volume / SMA(Volume, n) | 20 | Relative activity level (>1.5 = high) |
| **VWAP** | VWAP = cumsum(Price * Volume) / cumsum(Volume) | Intraday | Institutional fill quality benchmark |
| **MFI** | MFI = 100 - (100 / (1 + MF_Ratio)), volume-weighted RSI | 14 | Volume-confirmed momentum |

---

## TA-Lib Integration

### Library Priority
1. **TA-Lib** (primary): C-based, fastest, industry standard
2. **pandas-ta** (fallback): Pure Python, portable, slower

### TA-Lib Function Mapping

| Indicator | TA-Lib Function | pandas-ta Equivalent |
|-----------|-----------------|---------------------|
| EMA | `talib.EMA(close, timeperiod)` | `ta.ema(close, length)` |
| RSI | `talib.RSI(close, timeperiod)` | `ta.rsi(close, length)` |
| ATR | `talib.ATR(high, low, close, timeperiod)` | `ta.atr(high, low, close, length)` |
| ADX | `talib.ADX(high, low, close, timeperiod)` | `ta.adx(high, low, close, length)` |
| OBV | `talib.OBV(close, volume)` | `ta.obv(close, volume)` |
| MFI | `talib.MFI(high, low, close, volume, timeperiod)` | `ta.mfi(high, low, close, volume, length)` |

### Fallback Detection
```python
try:
    import talib
    USE_TALIB = True
except ImportError:
    import pandas_ta as ta
    USE_TALIB = False
```

---

## Performance Optimization

### Vectorization Patterns
- **NumPy/pandas native ops**: 100x+ faster than row-by-row loops
- **Avoid apply()**: Use vectorized alternatives (rolling, shift, cumsum)
- **Batch computation**: Compute multiple indicators in single pass

### Memory Management
- **float32 vs float64**: 50% memory reduction with <0.01% precision loss
- **Chunking**: Split datasets >200MB into 50MB chunks
- **Cache intermediate**: Store EMA(T-1) for EMA(T) calculation

### Numba JIT (Advanced)
- Use for hot loops that cannot be vectorized
- 10x+ speedup for custom indicator implementations
- Requires explicit type annotations

---

## Information Hierarchy

### 1. Primary Source (Authoritative)
- **Golden test datasets**: `tests/fixtures/indicators/golden_datasets/`
- Use for: Validation, accuracy benchmarking

### 2. Secondary Source (Reliable)
- **Existing implementations**: `packages/core/features/indicators/*.py`
- Use for: Pattern following, code reuse

### 3. Tertiary Source (Supplementary)
- **TA-Lib documentation**: https://ta-lib.org/function.html
- Use for: Formula verification, parameter defaults

### 4. Fallback Source (Research)
- **researcher-external**: Volume as Leading Indicator theory, Clenow Method
- Use for: Novel indicators, custom aggregation strategies

---

## Quick Reference

### Default Lookback Periods
| Indicator | Default | Range |
|-----------|---------|-------|
| RSI | 14 | 7-21 |
| ATR | 14 | 10-20 |
| ADX | 14 | 10-20 |
| EMA | 20 | 5-200 |
| Donchian | 20 | 10-55 |
| RVOL | 20 | 10-30 |
| MFI | 14 | 10-20 |

### Performance SLA Targets
| Dataset Size | Max Latency | Memory Limit |
|--------------|-------------|--------------|
| 10K rows | 1 second | 200MB |
| 100K rows | 5 seconds | 200MB |
| 1M+ rows | 30 seconds | 200MB (chunked) |
