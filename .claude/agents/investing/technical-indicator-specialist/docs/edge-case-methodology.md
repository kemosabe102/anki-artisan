# Edge Case Handling Methodology

**Purpose**: Comprehensive edge case detection and handling strategies for technical indicator computation

**Audience**: technical-indicator-specialist agent, python-code-implementer (implementation), test-creator (validation coverage)

**Version**: 1.0

**Last Updated**: 2025-11-16

---

## Overview

Technical indicator computation must handle real-world market data edge cases gracefully while maintaining data integrity. This guide defines a **fail-gracefully philosophy** with best-effort computation and transparent warning mechanisms across 5 critical edge case categories.

**Core Philosophy**: Preserve data integrity > Produce potentially misleading values. Skip periods when data quality is uncertain, compute with available data when possible, degrade gracefully under resource pressure.

---

## Core Principles

1. **No Data Fabrication**: Never forward/backward fill missing price/volume data (introduces bias in technical signals)
2. **Best-Effort Computation**: Compute with available data when insufficient history, annotate with confidence penalty
3. **Transparent Warnings**: Log all edge cases with structured warning format for downstream review
4. **Graceful Degradation**: Reduce precision/caching before failing completely under resource pressure
5. **Fail-Safe Defaults**: Return NaN for uncomputable periods rather than stale/fabricated values

---

## Edge Case Categories

### 1. Missing Data

**Description**: Gaps in OHLCV (Open/High/Low/Close/Volume) time series data due to market closures, data feed issues, or delisted securities.

**Detection Logic**:
```python
if pd.isna(df[['open', 'high', 'low', 'close', 'volume']]).any(axis=1).any():
    missing_indices = df[pd.isna(df[['open', 'high', 'low', 'close', 'volume']]).any(axis=1)].index
```

**Handling Strategy**: **SKIP PERIOD** (no forward/backward fill)

**Implementation**:
```python
# For each missing data point
for idx in missing_indices:
    indicators.loc[idx] = np.nan
    warnings.append({
        "type": "MISSING_DATA",
        "index": idx,
        "timestamp": df.loc[idx, 'timestamp'] if 'timestamp' in df.columns else None,
        "message": f"Missing OHLCV data at index {idx}, skipping indicator computation",
        "severity": "WARNING"
    })
```

**Warning Format**:
```json
{
  "type": "MISSING_DATA",
  "index": 42,
  "timestamp": "2024-03-15T14:30:00Z",
  "message": "Missing OHLCV data at index 42, skipping indicator computation",
  "severity": "WARNING"
}
```

**Test Coverage Requirements**:
- Single missing value (middle of series)
- Multiple consecutive missing values (gap detection)
- Missing data at start/end of series
- All OHLCV fields missing vs partial field missing

**Rationale**: Forward/backward fill creates artificial price continuity, distorting momentum indicators (RSI, MACD), trend indicators (moving averages), and volume indicators (OBV). Better to acknowledge data gap than introduce phantom signals.

---

### 2. Insufficient History

**Description**: Available data periods less than indicator lookback requirement (e.g., 10 periods available, RSI requires 14).

**Detection Logic**:
```python
required_periods = indicator_params.get('lookback', 14)
available_periods = len(df)

if available_periods < required_periods:
    # Insufficient history detected
    confidence_penalty = available_periods / required_periods
```

**Handling Strategy**: **BEST-EFFORT COMPUTATION + WARNING**

**Implementation**:
```python
def compute_with_insufficient_history(df, indicator, required_periods):
    available = len(df)

    if available < required_periods:
        # Compute with available data
        result = indicator.compute(df, period=available)

        # Apply confidence penalty
        confidence_penalty = available / required_periods

        warnings.append({
            "type": "INSUFFICIENT_HISTORY",
            "indicator": indicator.name,
            "required": required_periods,
            "available": available,
            "confidence_penalty": round(confidence_penalty, 2),
            "message": f"Insufficient history: {available} periods available, {required_periods} required. Results may be less accurate.",
            "severity": "WARNING"
        })

        return result, confidence_penalty

    return indicator.compute(df, period=required_periods), 1.0
```

**Warning Format**:
```json
{
  "type": "INSUFFICIENT_HISTORY",
  "indicator": "RSI",
  "required": 14,
  "available": 10,
  "confidence_penalty": 0.71,
  "message": "Insufficient history: 10 periods available, 14 required. RSI values may be less stable.",
  "severity": "WARNING"
}
```

**Test Coverage Requirements**:
- Exactly 50% required periods (confidence = 0.5)
- <25% required periods (severe penalty)
- Edge case: 1 period available (minimal computation)
- Multiple indicators with different lookback requirements

**Example**: RSI(14) with 10 periods → Compute RSI(10), apply 0.71 confidence multiplier, warn about reduced stability.

---

### 3. Zero Volume

**Description**: Trading periods with zero volume (market closed, illiquid securities, data feed error).

**Detection Logic**:
```python
zero_volume_mask = df['volume'] == 0
zero_volume_indices = df[zero_volume_mask].index
```

**Handling Strategy**: **SKIP PERIOD** (volume-based indicators) OR **CARRY FORWARD** (cumulative indicators like OBV)

**Affected Indicators**: OBV, RVOL, VWAP, MFI (all volume-dependent)

**Implementation**:
```python
def handle_zero_volume(df, indicator_type):
    zero_vol_idx = df[df['volume'] == 0].index

    for idx in zero_vol_idx:
        if indicator_type in ['VWAP', 'RVOL', 'MFI']:
            # Skip period (return NaN)
            indicators.loc[idx] = np.nan
            action = "skipped"

        elif indicator_type == 'OBV':
            # Carry forward prior value (OBV is cumulative)
            if idx > 0:
                indicators.loc[idx] = indicators.loc[idx - 1]
                action = "carried_forward"
            else:
                indicators.loc[idx] = 0
                action = "initialized_to_zero"

        warnings.append({
            "type": "ZERO_VOLUME",
            "index": idx,
            "indicator": indicator_type,
            "action": action,
            "message": f"Zero volume at index {idx}, {action} for {indicator_type}",
            "severity": "INFO"
        })
```

**Warning Format**:
```json
{
  "type": "ZERO_VOLUME",
  "index": 87,
  "indicator": "OBV",
  "action": "carried_forward",
  "message": "Zero volume at index 87, carried_forward for OBV",
  "severity": "INFO"
}
```

**Test Coverage Requirements**:
- Single zero volume period (middle of series)
- Multiple consecutive zero volume periods
- Zero volume at start of series (OBV initialization)
- Mixed indicators (OBV vs VWAP) in same computation

---

### 4. Extreme Values

**Description**: Outlier price movements or volume spikes indicating potential data quality issues (flash crash, bad tick, feed error).

**Detection Logic**:
```python
# Price change threshold: >20% single-period move
price_change_pct = df['close'].pct_change().abs()
price_outliers = df[price_change_pct > 0.20].index

# Volume threshold: >10x rolling 20-period average
avg_volume = df['volume'].rolling(20).mean()
volume_ratio = df['volume'] / avg_volume
volume_outliers = df[volume_ratio > 10].index
```

**Handling Strategy**: **LOG WARNING + PROCEED WITH COMPUTATION**

**Implementation**:
```python
def detect_extreme_values(df):
    extreme_warnings = []

    # Price outliers
    price_change = df['close'].pct_change().abs()
    price_outliers = df[price_change > 0.20]

    for idx, row in price_outliers.iterrows():
        extreme_warnings.append({
            "type": "EXTREME_VALUE",
            "category": "PRICE",
            "index": idx,
            "price_change_pct": round(price_change.loc[idx] * 100, 2),
            "message": f"Extreme price movement: {price_change.loc[idx]:.2%} at index {idx}. Verify data quality.",
            "severity": "WARNING",
            "action": "computed_with_flag"
        })

    # Volume outliers
    avg_vol = df['volume'].rolling(20, min_periods=5).mean()
    vol_ratio = df['volume'] / avg_vol
    volume_outliers = df[vol_ratio > 10]

    for idx, row in volume_outliers.iterrows():
        extreme_warnings.append({
            "type": "EXTREME_VALUE",
            "category": "VOLUME",
            "index": idx,
            "volume_ratio": round(vol_ratio.loc[idx], 2),
            "message": f"Extreme volume spike: {vol_ratio.loc[idx]:.2f}x average at index {idx}. Verify data quality.",
            "severity": "WARNING",
            "action": "computed_with_flag"
        })

    return extreme_warnings
```

**Warning Format**:
```json
{
  "type": "EXTREME_VALUE",
  "category": "PRICE",
  "index": 142,
  "price_change_pct": 23.5,
  "message": "Extreme price movement: 23.5% at index 142. Verify data quality.",
  "severity": "WARNING",
  "action": "computed_with_flag"
}
```

**Test Coverage Requirements**:
- Single flash crash (>20% down, immediate recovery)
- Sustained price movement (>20% over 2-3 periods)
- Volume spike without price movement (block trade)
- Combined price + volume extreme event

**Rationale**: Extreme values may be real market events (earnings surprises, macro shocks) or data errors. Flag for review but still compute indicators to avoid missing legitimate signals.

---

### 5. Performance Degradation

**Description**: Resource pressure (memory >90% limit, computation time >10x expected) requiring graceful degradation strategies.

**Detection Logic**:
```python
import psutil
import time

def monitor_resources(df, expected_time_ms):
    process = psutil.Process()
    current_memory_mb = process.memory_info().rss / (1024 ** 2)
    memory_limit_mb = 200  # Agent limit

    memory_usage_pct = current_memory_mb / memory_limit_mb

    start_time = time.time()
    # ... computation ...
    elapsed_time_ms = (time.time() - start_time) * 1000

    timeout_threshold = expected_time_ms * 10

    return {
        "memory_usage_pct": memory_usage_pct,
        "current_memory_mb": current_memory_mb,
        "computation_time_ms": elapsed_time_ms,
        "timeout_exceeded": elapsed_time_ms > timeout_threshold
    }
```

**Handling Strategy**: **CHUNKING → PRECISION REDUCTION → CACHE DISABLE → PARTIAL RESULTS**

**Implementation (Progressive Degradation)**:
```python
def apply_degradation_strategies(df, indicators_list, resources):
    strategies_applied = []

    # Strategy 1: Chunking (memory >90%)
    if resources['memory_usage_pct'] > 0.90:
        chunk_size = len(df) // 4  # Process in 4 chunks
        strategies_applied.append({
            "strategy": "CHUNKING",
            "chunk_size": chunk_size,
            "reason": f"Memory usage {resources['memory_usage_pct']:.1%} exceeds 90% threshold"
        })
        results = process_in_chunks(df, indicators_list, chunk_size)

    # Strategy 2: Precision Reduction (memory >85%)
    elif resources['memory_usage_pct'] > 0.85:
        df = df.astype('float32')  # float64 → float32 (50% memory reduction)
        strategies_applied.append({
            "strategy": "PRECISION_REDUCTION",
            "dtype": "float32",
            "memory_saved_pct": 50,
            "reason": f"Memory usage {resources['memory_usage_pct']:.1%} exceeds 85% threshold"
        })
        results = compute_indicators(df, indicators_list)

    # Strategy 3: Cache Disable (computation time >10x)
    elif resources['timeout_exceeded']:
        disable_caching()
        strategies_applied.append({
            "strategy": "CACHE_DISABLE",
            "reason": f"Computation time {resources['computation_time_ms']}ms exceeds 10x expected threshold"
        })
        results = compute_indicators(df, indicators_list)

    # Strategy 4: Partial Results (timeout persists)
    else:
        results = compute_partial_indicators(df, indicators_list)
        strategies_applied.append({
            "strategy": "PARTIAL_RESULTS",
            "successful_indicators": len(results),
            "total_indicators": len(indicators_list),
            "reason": "Computation timeout after degradation strategies applied"
        })

    return results, strategies_applied
```

**Warning Format (Degradation Applied)**:
```json
{
  "type": "PERFORMANCE_DEGRADATION",
  "strategy": "PRECISION_REDUCTION",
  "memory_usage_pct": 87.3,
  "dtype": "float32",
  "memory_saved_pct": 50,
  "message": "Applied precision reduction (float64 → float32) due to 87.3% memory usage. Expect minor rounding differences (<0.01%).",
  "severity": "INFO"
}
```

**Warning Format (Partial Results)**:
```json
{
  "type": "PERFORMANCE_DEGRADATION",
  "strategy": "PARTIAL_RESULTS",
  "successful_indicators": 8,
  "total_indicators": 12,
  "failed_indicators": ["ATR", "ADX", "STOCH_K", "STOCH_D"],
  "message": "Computation timeout: 8/12 indicators completed successfully. Partial results available.",
  "severity": "ERROR"
}
```

**Test Coverage Requirements**:
- Gradual memory increase (trigger 85%, 90%, 95% thresholds)
- Computation timeout scenarios (5x, 10x, 20x expected time)
- Chunking correctness (results match non-chunked computation)
- Precision reduction impact (<0.01% deviation from float64)

---

## Decision Tree

```
Input: Market data edge case detected
│
├─ Missing OHLCV data?
│  └─ YES → SKIP PERIOD (return NaN) + log WARNING
│
├─ Insufficient history (<required lookback)?
│  └─ YES → COMPUTE with available data + apply confidence_penalty + log WARNING
│
├─ Zero volume?
│  ├─ Volume-based (VWAP/RVOL/MFI) → SKIP PERIOD (return NaN) + log INFO
│  └─ Cumulative (OBV) → CARRY FORWARD prior value + log INFO
│
├─ Extreme value (price >20% OR volume >10x avg)?
│  └─ YES → LOG WARNING + PROCEED with computation (flag for review)
│
├─ Resource pressure?
│  ├─ Memory >90% → CHUNKING + log INFO
│  ├─ Memory >85% → PRECISION REDUCTION (float32) + log INFO
│  ├─ Timeout >10x → CACHE DISABLE + log WARNING
│  └─ Timeout persists → PARTIAL RESULTS + log ERROR
│
└─ No edge case → STANDARD COMPUTATION
```

---

## Golden Dataset Validation

**How Edge Cases Affect Validation**:

1. **Missing Data Periods**: Golden dataset must include NaN values for periods with missing OHLCV (validate skip behavior)
2. **Insufficient History**: First N periods (where N < lookback) will have lower confidence scores (validate penalty calculation)
3. **Zero Volume**: Volume-based indicators will have NaN for zero-volume periods (validate skip vs carry-forward logic)
4. **Extreme Values**: Indicators still computed for outliers, warnings present in metadata (validate flag-and-compute behavior)
5. **Performance Degradation**: Float32 results may differ from float64 by <0.01% (validate acceptable tolerance)

**Validation Tolerance Thresholds**:
- Standard computation: `abs(result - expected) < 1e-6` (exact match)
- Float32 degradation: `abs(result - expected) < 1e-4` (0.01% tolerance)
- Insufficient history: `confidence_score >= (available / required)`
- Missing data: `pd.isna(result) == True` (exact NaN match)

**Golden Dataset Structure**:
```json
{
  "symbol": "AAPL",
  "data": [...],
  "edge_cases": [
    {"type": "MISSING_DATA", "indices": [42, 87]},
    {"type": "INSUFFICIENT_HISTORY", "first_N_periods": 13},
    {"type": "ZERO_VOLUME", "indices": [101, 102, 103]},
    {"type": "EXTREME_VALUE", "price_outliers": [156], "volume_outliers": [234]}
  ],
  "expected_warnings": [...],
  "expected_results": {...}
}
```

---

## Performance Impact Analysis

### Latency Impact (per 1,000 periods)

| Edge Case | Detection Overhead | Handling Overhead | Total Added Latency |
|-----------|-------------------|-------------------|---------------------|
| Missing Data | ~5ms (isna check) | ~2ms (skip logic) | **~7ms** |
| Insufficient History | ~1ms (len check) | ~3ms (penalty calc) | **~4ms** |
| Zero Volume | ~3ms (equality check) | ~2ms (skip/carry) | **~5ms** |
| Extreme Values | ~15ms (rolling stats) | ~1ms (logging) | **~16ms** |
| Chunking (memory >90%) | ~50ms (chunk split) | ~200ms (4x overhead) | **~250ms** |
| Precision Reduction | ~30ms (dtype conversion) | ~0ms (compute faster) | **~30ms** |

**Total Overhead (all edge cases active)**: ~32ms per 1,000 periods (3.2% of 1s baseline computation)

### Memory Impact

| Strategy | Memory Footprint | Reduction vs Baseline |
|----------|------------------|----------------------|
| Standard (float64) | 100% (baseline) | 0% |
| Precision Reduction (float32) | 50% | -50% |
| Chunking (4 chunks) | 25% peak | -75% peak |
| Cache Disable | +0% (no cache overhead) | Variable |

---

## Related References

1. **TA-Lib Documentation**: [https://ta-lib.org/function.html](https://ta-lib.org/function.html) - Canonical indicator definitions, edge case handling notes
2. **pandas Best Practices**: [https://pandas.pydata.org/docs/user_guide/missing_data.html](https://pandas.pydata.org/docs/user_guide/missing_data.html) - Missing data strategies, NaN propagation rules
3. **Base Agent Pattern**: `.claude/docs/01-guides/agents/base-agent-pattern.md` - Error recovery patterns, graceful degradation philosophy
4. **Python Code Review Guidelines**: `docs/04-guides/code-review/coding-guidelines.md` - Performance optimization standards, memory management
5. **Technical Indicator Specialist**: `.claude/agents/technical-indicator-specialist.md` - Primary agent definition, complete capability matrix

---

**Version History**:
- 1.0 (2025-11-16): Initial externalization from technical-indicator-specialist.md (lines 424-502)

**Token Budget**: ~1,200 tokens (AI-readable, progressive disclosure, structured sections)

**Maintenance**: Update when new edge cases discovered via production usage or golden dataset validation failures
