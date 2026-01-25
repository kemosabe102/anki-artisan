# Delegation Examples: Technical Indicator Specialist

**Purpose**: How orchestrator invokes this agent for indicator computation tasks

---

## Trigger Conditions

The orchestrator delegates to `technical-indicator-specialist` when:

1. **Keywords detected**: "compute indicators", "calculate RSI/ATR/EMA", "engineer features", "multi-timeframe"
2. **File paths involved**: `packages/core/features/indicators/*.py`, `tests/fixtures/indicators/`
3. **Data type**: OHLCV Parquet files requiring technical analysis
4. **NOT for**: Market data acquisition, pattern detection, ML feature engineering

---

## Example 1: Basic Indicator Computation

**User Request**: "Compute RSI, ATR, and EMA for AAPL daily data"

**Orchestrator Delegation**:
```
Task(technical-indicator-specialist,
  "Compute indicators [RSI, ATR, EMA] for ticker AAPL, timeframe 1D.
   Data source: packages/core/data/ohlcv/AAPL_1D.parquet
   Output format: wide-format Parquet with OHLCV + indicator columns.")
```

**Expected Output**:
```json
{
  "status": "SUCCESS",
  "agent": "technical-indicator-specialist",
  "confidence": 0.92,
  "agent_specific_output": {
    "indicators_computed": ["RSI", "ATR", "EMA"],
    "output_location": "packages/core/features/outputs/AAPL_1D_indicators.parquet",
    "performance_metrics": {
      "computation_time_seconds": 0.34,
      "memory_peak_mb": 45.2,
      "vectorization_ratio": 0.98
    }
  }
}
```

---

## Example 2: Multi-Timeframe Feature Engineering

**User Request**: "Create multi-timeframe features for SPY across 1min, 5min, 1H"

**Orchestrator Delegation**:
```
Task(technical-indicator-specialist,
  "Engineer multi-timeframe features for SPY.
   Timeframes: [1min, 5min, 1H]
   Indicators: [ATR, RSI, EMA, VWAP]
   Data source: packages/core/data/ohlcv/SPY_1min.parquet
   Enable multi_timeframe aggregation.")
```

**Expected Output**: Wide-format Parquet with columns like `ATR_14_1min`, `ATR_14_5min`, `ATR_14_1H`

---

## Example 3: Golden Dataset Validation

**User Request**: "Validate our ATR implementation against the golden dataset"

**Orchestrator Delegation**:
```
Task(technical-indicator-specialist,
  "Validate indicators [ATR] against golden dataset.
   Test fixture: tests/fixtures/indicators/golden_ATR.parquet
   Enable validation_mode=true.
   Report MAE, correlation coefficient, and max error.")
```

**Expected Output**:
```json
{
  "status": "SUCCESS",
  "agent_specific_output": {
    "validation_results": {
      "indicators_validated": ["ATR"],
      "accuracy_vs_golden": {
        "mean_absolute_error": 0.0023,
        "max_absolute_error": 0.0089,
        "correlation_coefficient": 0.9987
      }
    }
  }
}
```

---

## Example 4: Handling Edge Cases

**User Request**: "Compute volume indicators for illiquid ticker with gaps"

**Orchestrator Delegation**:
```
Task(technical-indicator-specialist,
  "Compute volume indicators [OBV, RVOL, MFI] for ticker XYZ.
   Data source: packages/core/data/ohlcv/XYZ_1D.parquet
   Note: Data has known gaps and zero-volume periods.")
```

**Expected Output** (with warnings):
```json
{
  "status": "SUCCESS",
  "confidence": 0.78,
  "agent_specific_output": {
    "indicators_computed": ["OBV", "RVOL", "MFI"],
    "warnings": [
      {
        "indicator": "MFI",
        "warning_type": "zero_volume",
        "rows_affected": 12,
        "message": "Zero volume at 12 periods, skipping MFI computation"
      },
      {
        "indicator": "RVOL",
        "warning_type": "missing_data",
        "rows_affected": 5,
        "message": "Missing OHLCV data at 5 indices, returning NaN"
      }
    ]
  }
}
```

---

## Pipeline Integration

### Sequential Pipeline
```
market-data-specialist → technical-indicator-specialist → Feature Factory
        (OHLCV)                  (wide-format)              (ML features)
```

### Parallel Validation
```
                    ┌─ python-code-reviewer (implementation quality)
technical-indicator │
                    └─ test-executor (golden dataset validation)
```

---

## Context Metadata Template

When delegating, include:
```yaml
ticker: "AAPL"
timeframe: "1D"
indicators: ["RSI", "ATR", "EMA"]
data_source:
  type: "parquet"
  path: "packages/core/data/ohlcv/AAPL_1D.parquet"
options:
  lookback_period: 14  # optional, uses defaults
  multi_timeframe: false
  validation_mode: false
  optimization_level: "standard"
```
