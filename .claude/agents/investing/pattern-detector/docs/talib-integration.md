# TA-Lib Integration Patterns

## Overview

Comprehensive guide for integrating TA-Lib pattern recognition and indicator computation with pandas-ta fallbacks, vectorization strategies, and DataConnector protocol compatibility.

## Core Frameworks

### 1. TA-Lib Pattern Recognition API

**Purpose**: Leverage TA-Lib's 61 candlestick pattern functions for reliable pattern detection

**When to Use**: Candlestick pattern analysis, standardized indicator computation, production environments

**How to Apply**:

1. **Installation**:

   ```bash
   # Linux/MacOS
   conda install -c conda-forge ta-lib
   # or
   pip install TA-Lib

   # Windows (requires binary wheel)
   pip install TA-Lib --find-links https://github.com/cgohlke/talib-build/releases
   ```

2. **CDL Pattern Functions** (61 total):
   - All functions: `talib.CDL*` (e.g., `CDL2CROWS`, `CDL3BLACKCROWS`)
   - Return values: 0 (no pattern), +100 (bullish), -100 (bearish)
   - Common patterns: `CDLDOJI`, `CDLENGULFING`, `CDLHAMMER`, `CDLMORNINGSTAR`

3. **Basic Usage**:

   ```python
   import talib
   import numpy as np

   def detect_candlestick_patterns(df):
       """Scan all TA-Lib candlestick patterns"""
       open_prices = df['open'].values
       high_prices = df['high'].values
       low_prices = df['low'].values
       close_prices = df['close'].values

       pattern_results = {}

       # List of all CDL functions
       cdl_patterns = [
           'CDL2CROWS', 'CDL3BLACKCROWS', 'CDL3INSIDE', 'CDL3LINESTRIKE',
           'CDL3OUTSIDE', 'CDL3STARSINSOUTH', 'CDL3WHITESOLDIERS',
           'CDLABANDONEDBABY', 'CDLADVANCEBLOCK', 'CDLBELTHOLD',
           'CDLBREAKAWAY', 'CDLCLOSINGMARUBOZU', 'CDLCONCEALBABYSWALL',
           'CDLCOUNTERATTACK', 'CDLDARKCLOUDCOVER', 'CDLDOJI',
           'CDLDOJISTAR', 'CDLDRAGONFLYDOJI', 'CDLENGULFING',
           'CDLEVENINGDOJISTAR', 'CDLEVENINGSTAR', 'CDLGAPSIDESIDEWHITE',
           'CDLGRAVESTONEDOJI', 'CDLHAMMER', 'CDLHANGINGMAN',
           'CDLHARAMI', 'CDLHARAMICROSS', 'CDLHIGHWAVE',
           'CDLHIKKAKE', 'CDLHIKKAKEMOD', 'CDLHOMINGPIGEON',
           'CDLIDENTICAL3CROWS', 'CDLINNECK', 'CDLINVERTEDHAMMER',
           'CDLKICKING', 'CDLKICKINGBYLENGTH', 'CDLLADDERBOTTOM',
           'CDLLONGLEGGEDDOJI', 'CDLLONGLINE', 'CDLMARUBOZU',
           'CDLMATCHINGLOW', 'CDLMATHOLD', 'CDLMORNINGDOJISTAR',
           'CDLMORNINGSTAR', 'CDLONNECK', 'CDLPIERCING',
           'CDLRICKSHAWMAN', 'CDLRISEFALL3METHODS', 'CDLSEPARATINGLINES',
           'CDLSHOOTINGSTAR', 'CDLSHORTLINE', 'CDLSPINNINGTOP',
           'CDLSTALLEDPATTERN', 'CDLSTICKSANDWICH', 'CDLTAKURI',
           'CDLTASUKIGAP', 'CDLTHRUSTING', 'CDLTRISTAR',
           'CDLUNIQUE3RIVER', 'CDLUPSIDEGAP2CROWS', 'CDLXSIDEGAP3METHODS'
       ]

       for pattern_name in cdl_patterns:
           pattern_func = getattr(talib, pattern_name)
           result = pattern_func(open_prices, high_prices, low_prices, close_prices)
           pattern_results[pattern_name] = result

       return pattern_results
   ```

4. **Indicator Functions** (150+ total):
   - Overlap: `SMA`, `EMA`, `BBANDS`, `SAR`
   - Momentum: `RSI`, `MACD`, `STOCH`, `ADX`
   - Volume: `OBV`, `AD`, `ADOSC`
   - Volatility: `ATR`, `NATR`, `TRANGE`

**Example - Multi-Indicator Computation**:

```python
def compute_indicators(df):
    """Compute common TA-Lib indicators"""
    close = df['close'].values
    high = df['high'].values
    low = df['low'].values
    volume = df['volume'].values

    # Trend
    df['sma_20'] = talib.SMA(close, timeperiod=20)
    df['ema_50'] = talib.EMA(close, timeperiod=50)
    upper, middle, lower = talib.BBANDS(close, timeperiod=20)
    df['bb_upper'], df['bb_middle'], df['bb_lower'] = upper, middle, lower

    # Momentum
    df['rsi'] = talib.RSI(close, timeperiod=14)
    macd, macd_signal, macd_hist = talib.MACD(close)
    df['macd'], df['macd_signal'], df['macd_hist'] = macd, macd_signal, macd_hist
    df['adx'] = talib.ADX(high, low, close, timeperiod=14)

    # Volume
    df['obv'] = talib.OBV(close, volume)

    # Volatility
    df['atr'] = talib.ATR(high, low, close, timeperiod=14)

    return df
```

---

### 2. pandas-ta Fallback Strategy

**Purpose**: Provide graceful degradation when TA-Lib unavailable or missing indicators

**When to Use**: Development environments, missing TA-Lib patterns, custom indicators

**How to Apply**:

1. **Installation**:

   ```bash
   pip install pandas-ta
   ```

2. **Equivalent Functions**:

   | TA-Lib | pandas-ta | Notes |
   |--------|-----------|-------|
   | `RSI(close, 14)` | `df.ta.rsi(length=14)` | Identical algorithm |
   | `SMA(close, 20)` | `df.ta.sma(length=20)` | Identical |
   | `EMA(close, 50)` | `df.ta.ema(length=50)` | Identical |
   | `BBANDS(close, 20)` | `df.ta.bbands(length=20)` | Returns DataFrame |
   | `MACD(close)` | `df.ta.macd()` | Returns DataFrame |
   | `ADX(h,l,c, 14)` | `df.ta.adx(length=14)` | Returns DataFrame |
   | `ATR(h,l,c, 14)` | `df.ta.atr(length=14)` | Identical |

3. **Fallback Pattern**:

   ```python
   try:
       import talib
       TALIB_AVAILABLE = True
   except ImportError:
       import pandas_ta as ta
       TALIB_AVAILABLE = False

   def compute_rsi(df, period=14):
       """Compute RSI with TA-Lib fallback to pandas-ta"""
       if TALIB_AVAILABLE:
           return talib.RSI(df['close'].values, timeperiod=period)
       else:
           return df.ta.rsi(length=period).values
   ```

4. **Candlestick Pattern Emulation** (pandas-ta lacks CDL functions):

   ```python
   def detect_doji_pandasta(df, doji_threshold=0.1):
       """Emulate CDLDOJI using pandas-ta primitives"""
       body = abs(df['close'] - df['open'])
       total_range = df['high'] - df['low']
       body_ratio = body / (total_range + 1e-9)

       is_doji = body_ratio < doji_threshold
       return is_doji.astype(int) * 100  # Match TA-Lib output format
   ```

**Important**: pandas-ta does NOT have CDL pattern recognition. For production, use TA-Lib.

---

### 3. Vectorization Patterns for Large Datasets

**Purpose**: Maximize performance on large OHLCV datasets (1M+ rows)

**When to Use**: Backtesting, batch pattern detection, multi-timeframe analysis

**How to Apply**:

1. **NumPy Array Inputs** (TA-Lib requirement):

   ```python
   # ✅ CORRECT - NumPy arrays
   close_array = df['close'].values
   rsi = talib.RSI(close_array, timeperiod=14)

   # ❌ WRONG - Pandas Series
   rsi = talib.RSI(df['close'], timeperiod=14)  # Fails!
   ```

2. **Batch Computation** (compute all indicators once):

   ```python
   def compute_all_indicators_vectorized(df):
       """Vectorized computation for 20+ indicators"""
       c, h, l, v = df['close'].values, df['high'].values, df['low'].values, df['volume'].values

       # Trend (vectorized)
       indicators = {
           'sma_20': talib.SMA(c, 20),
           'ema_50': talib.EMA(c, 50),
           'ema_200': talib.EMA(c, 200),
       }

       # Momentum (vectorized)
       indicators['rsi'] = talib.RSI(c, 14)
       indicators['adx'] = talib.ADX(h, l, c, 14)
       macd, signal, hist = talib.MACD(c)
       indicators['macd'], indicators['macd_signal'], indicators['macd_hist'] = macd, signal, hist

       # Volume (vectorized)
       indicators['obv'] = talib.OBV(c, v)

       # Volatility (vectorized)
       indicators['atr'] = talib.ATR(h, l, c, 14)

       # Add all at once (faster than iterative assignment)
       return df.assign(**indicators)
   ```

3. **Chunked Processing** (for datasets >10M rows):

   ```python
   def process_large_dataset_chunked(df, chunk_size=1_000_000, lookback=200):
       """Process large datasets in chunks with lookback overlap"""
       results = []

       for i in range(0, len(df), chunk_size):
           # Include lookback for indicator continuity
           start = max(0, i - lookback)
           end = min(len(df), i + chunk_size)
           chunk = df.iloc[start:end].copy()

           # Compute indicators on chunk
           chunk = compute_all_indicators_vectorized(chunk)

           # Trim lookback from results (keep only new data)
           if i > 0:
               chunk = chunk.iloc[lookback:]

           results.append(chunk)

       return pd.concat(results, ignore_index=True)
   ```

4. **Parallel Processing** (multi-symbol/multi-timeframe):

   ```python
   from concurrent.futures import ProcessPoolExecutor

   def process_symbol_indicators(symbol_df):
       """Worker function for parallel processing"""
       return compute_all_indicators_vectorized(symbol_df)

   def process_multiple_symbols_parallel(symbol_dfs, max_workers=4):
       """Process multiple symbols in parallel"""
       with ProcessPoolExecutor(max_workers=max_workers) as executor:
           results = list(executor.map(process_symbol_indicators, symbol_dfs))
       return results
   ```

---

### 4. Performance Optimization Techniques

**Purpose**: Minimize computation time and memory usage

**When to Use**: Production environments, real-time processing, resource-constrained systems

**Techniques**:

1. **Pre-compute Static Indicators**:
   - Compute once during data loading
   - Cache results in DataFrame
   - Recompute only new bars in live trading

2. **Avoid Redundant Calculations**:

   ```python
   # ❌ BAD - Recomputes SMA twice
   if talib.SMA(close, 20)[-1] > talib.SMA(close, 50)[-1]:
       signal = 'BUY'

   # ✅ GOOD - Compute once, reuse
   sma_20 = talib.SMA(close, 20)
   sma_50 = talib.SMA(close, 50)
   if sma_20[-1] > sma_50[-1]:
       signal = 'BUY'
   ```

3. **Use Numba for Custom Indicators** (if not in TA-Lib):

   ```python
   from numba import jit

   @jit(nopython=True)
   def custom_indicator_numba(close, period):
       """Numba-accelerated custom calculation"""
       result = np.empty_like(close)
       for i in range(period, len(close)):
           result[i] = np.mean(close[i-period:i])  # Example logic
       return result
   ```

4. **Memory-Aware Processing**:

   ```python
   def memory_efficient_indicators(df):
       """Compute indicators in-place to reduce memory"""
       c, h, l = df['close'].values, df['high'].values, df['low'].values

       # In-place assignment
       df['rsi'] = talib.RSI(c, 14)
       df['atr'] = talib.ATR(h, l, c, 14)

       # Delete intermediate arrays
       del c, h, l

       return df
   ```

5. **Benchmarking**:

   ```python
   import time

   def benchmark_indicator_computation(df, iterations=10):
       """Benchmark TA-Lib vs pandas-ta"""
       close = df['close'].values

       # TA-Lib
       start = time.time()
       for _ in range(iterations):
           _ = talib.RSI(close, 14)
       talib_time = time.time() - start

       # pandas-ta
       start = time.time()
       for _ in range(iterations):
           _ = df.ta.rsi(length=14)
       pandasta_time = time.time() - start

       print(f"TA-Lib: {talib_time:.4f}s | pandas-ta: {pandasta_time:.4f}s")
       print(f"Speedup: {pandasta_time / talib_time:.2f}x")
   ```

**Expected Performance**:

- TA-Lib: 5-10x faster than pandas-ta for most indicators
- Vectorized operations: 100x faster than row-by-row iteration
- Numba: 50-200x faster than pure Python for custom logic

---

## DataConnector Protocol Compatibility

### Integration Requirements

**DataConnector Contract**:

- Input: DataFrame with columns `['open', 'high', 'low', 'close', 'volume']`
- Output: DataFrame with additional indicator columns
- Error handling: Graceful degradation on missing data
- Circuit breaker: Skip computation if insufficient history

**Implementation**:

```python
class TALibPatternDetector:
    def __init__(self, min_periods=50):
        self.min_periods = min_periods

    def process(self, df):
        """DataConnector-compatible processing"""
        # Validation
        required_cols = ['open', 'high', 'low', 'close', 'volume']
        if not all(col in df.columns for col in required_cols):
            raise ValueError(f"Missing required columns: {required_cols}")

        # Circuit breaker
        if len(df) < self.min_periods:
            return df  # Return unmodified, insufficient data

        # Compute indicators
        try:
            df = compute_all_indicators_vectorized(df)
        except Exception as e:
            # Graceful degradation
            print(f"Indicator computation failed: {e}")
            return df

        return df
```

### Error Handling Patterns

1. **Missing Data**:

   ```python
   def handle_missing_data(df):
       """Forward-fill short gaps, fail on long gaps"""
       for col in ['open', 'high', 'low', 'close', 'volume']:
           gap_size = df[col].isna().sum()
           if gap_size > 0:
               if gap_size <= 3:  # Short gap
                   df[col].fillna(method='ffill', inplace=True)
               else:  # Long gap
                   raise ValueError(f"Gap too large in {col}: {gap_size} bars")
       return df
   ```

2. **Invalid Values**:

   ```python
   def validate_ohlcv(df):
       """Check for invalid OHLCV relationships"""
       invalid_hl = df['high'] < df['low']
       invalid_hc = df['high'] < df['close']
       invalid_lc = df['low'] > df['close']
       invalid_vol = df['volume'] < 0

       if any([invalid_hl.any(), invalid_hc.any(), invalid_lc.any(), invalid_vol.any()]):
           raise ValueError("Invalid OHLCV data detected")
       return df
   ```

3. **TA-Lib Import Failure**:

   ```python
   try:
       import talib
       TALIB_AVAILABLE = True
   except ImportError:
       TALIB_AVAILABLE = False
       print("TA-Lib not available, falling back to pandas-ta")
   ```

---

## Anti-Patterns

### 1. Pandas Series as TA-Lib Input

**Problem**: TA-Lib requires NumPy arrays, passing Series causes errors
**Alternative**: Always use `.values` to convert: `talib.RSI(df['close'].values, 14)`

### 2. Row-by-Row Iteration

**Problem**: 100x slower than vectorized operations
**Alternative**: Compute all rows at once using NumPy arrays

### 3. Ignoring NaN Handling

**Problem**: TA-Lib functions return NaN for insufficient lookback periods
**Alternative**: Use `.dropna()` or check for NaN before downstream processing

### 4. Over-reliance on pandas-ta for Production

**Problem**: pandas-ta lacks candlestick patterns, slower performance
**Alternative**: Use TA-Lib for production, pandas-ta for development only

### 5. No Benchmarking

**Problem**: Assuming performance without measurement
**Alternative**: Benchmark indicator computation, optimize bottlenecks (see Performance Optimization section)

---

## Integration Points

### Pattern Detection Framework

- TA-Lib CDL outputs feed pattern confidence scoring
- Indicator outputs used for multi-indicator coordination
- See: `domain-knowledge-pattern-detection.md`, `development-multi-indicator-coordination.md`

### DataConnector Protocol

- Implements `process(df)` interface
- Returns DataFrame with added indicator columns
- Handles circuit breaker logic (insufficient history)

### Error Recovery

- Validation checkpoints before/after computation
- Graceful degradation on missing indicators
- See: `development-error-recovery.md`

### Fact Object Output

- Indicator values → Fact.metadata
- Pattern detection results → Fact.category, Fact.confidence
- See: `development-architecture-integration.md`

---

## Sources

1. **TA-Lib Documentation** (2024). <https://ta-lib.org/function.html>
   - Complete function reference, parameter specifications

2. **TA-Lib Python Wrapper** (2024). <https://github.com/mrjbq7/ta-lib>
   - Installation guide, NumPy integration, troubleshooting

3. **pandas-ta Documentation** (2024). <https://github.com/twopirllc/pandas-ta>
   - Function reference, DataFrame integration

4. **Nison, Steve** (1991). _Japanese Candlestick Charting Techniques_. New York Institute of Finance. ISBN: 978-0139316500
   - Candlestick pattern definitions, interpretation

5. **Harris, Larry** (2003). _Trading and Exchanges: Market Microstructure for Practitioners_. Oxford University Press. ISBN: 978-0195144703
   - Technical indicator validation, market mechanics

6. **NumPy Documentation** (2024). <https://numpy.org/doc/stable/>
   - Vectorization techniques, performance optimization

7. **Numba Documentation** (2024). <https://numba.pydata.org/>
   - JIT compilation for custom indicators

---

**Version**: 1.0
**Last Updated**: 2025-11-16
**Agent**: pattern-detector
