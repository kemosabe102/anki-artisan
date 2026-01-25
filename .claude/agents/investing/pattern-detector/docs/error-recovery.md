# Error Recovery & Performance Patterns

## Overview

Comprehensive error recovery strategies including decision trees for retry vs fail vs partial results, validation checkpoint templates, edge case handling, performance optimization, and confidence scoring formulas.

## Core Frameworks

### 1. Error Recovery Decision Trees

**Purpose**: Systematic decision-making for error handling based on error type and severity

**When to Use**: All error conditions, exception handling, resilience planning

**Decision Tree Structure**:

```text
Error Detected
├─ Connection Error
│  ├─ Transient (timeout, 5xx) → Retry with exponential backoff (max 3)
│  ├─ Authentication (401, 403) → Fail immediately, log credentials issue
│  └─ Rate limit (429) → Wait for reset_time, then retry
├─ Data Quality Error
│  ├─ Missing columns → Fail, log schema mismatch
│  ├─ Insufficient history (<50 bars) → Fail, recommend longer period
│  ├─ Short gaps (<3 bars) → Impute (forward-fill), continue with warning
│  └─ Long gaps (≥3 bars) → Fail, request data repair
├─ Computation Error
│  ├─ Indicator failure (single) → Skip indicator, continue with remaining (partial result)
│  ├─ Pattern detection failure (single) → Skip pattern, continue (partial result)
│  └─ Multiple failures (>50%) → Fail, insufficient computation coverage
└─ Validation Error
   ├─ Confidence below threshold → Return empty result (SUCCESS with no patterns)
   ├─ Invalid OHLC relationships → Fail, log data corruption
   └─ Schema validation failure → Fail, log schema violation
```

**Implementation**:

```python
from enum import Enum
from typing import Optional

class ErrorType(Enum):
    CONNECTION = 'connection'
    DATA_QUALITY = 'data_quality'
    COMPUTATION = 'computation'
    VALIDATION = 'validation'

class RecoveryAction(Enum):
    RETRY = 'retry'
    FAIL = 'fail'
    PARTIAL_RESULT = 'partial_result'
    CONTINUE_WITH_WARNING = 'continue_with_warning'

def determine_recovery_action(error: Exception, context: dict) -> RecoveryAction:
    """Decision tree for error recovery"""

    # Connection errors
    if isinstance(error, (TimeoutError, ConnectionError)):
        if context.get('retry_count', 0) < 3:
            return RecoveryAction.RETRY
        else:
            return RecoveryAction.FAIL

    if isinstance(error, RateLimitError):
        if context.get('can_wait', True):
            return RecoveryAction.RETRY  # With wait
        else:
            return RecoveryAction.FAIL

    if isinstance(error, AuthenticationError):
        return RecoveryAction.FAIL  # No retry for auth issues

    # Data quality errors
    if isinstance(error, InsufficientDataError):
        return RecoveryAction.FAIL

    if isinstance(error, DataGapError):
        gap_size = context.get('gap_size', 0)
        if gap_size < 3:
            return RecoveryAction.CONTINUE_WITH_WARNING  # Impute
        else:
            return RecoveryAction.FAIL

    # Computation errors
    if isinstance(error, IndicatorComputationError):
        failed_indicators = context.get('failed_indicators', [])
        total_indicators = context.get('total_indicators', 1)
        failure_rate = len(failed_indicators) / total_indicators

        if failure_rate < 0.5:
            return RecoveryAction.PARTIAL_RESULT  # Continue with remaining
        else:
            return RecoveryAction.FAIL  # Too many failures

    # Validation errors
    if isinstance(error, ConfidenceBelowThresholdError):
        return RecoveryAction.PARTIAL_RESULT  # Empty result is valid

    if isinstance(error, (SchemaValidationError, DataCorruptionError)):
        return RecoveryAction.FAIL

    # Unknown error type
    return RecoveryAction.FAIL  # Conservative default
```

**Retry Strategy with Exponential Backoff**:

```python
import asyncio
from typing import Callable, Any

async def retry_with_backoff(
    func: Callable,
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
    exponential_base: float = 2.0
) -> Any:
    """Execute function with exponential backoff retry"""
    for attempt in range(max_retries):
        try:
            return await func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise  # Last attempt, propagate error

            # Determine if retryable
            action = determine_recovery_action(e, {'retry_count': attempt})
            if action != RecoveryAction.RETRY:
                raise

            # Calculate delay
            delay = min(base_delay * (exponential_base ** attempt), max_delay)
            await asyncio.sleep(delay)

    raise RuntimeError("Retry exhausted")  # Should not reach here
```

---

### 2. Validation Checkpoint Templates

**Purpose**: Standardized validation gates at critical workflow points

**When to Use**: Before/after computation, data ingestion, output generation

**Checkpoint Locations**:

1. **Pre-Computation Checkpoint** (before OODA ACT phase):

   ```python
   def validate_pre_computation(observation):
       """Validate inputs before pattern detection"""
       df = observation['ohlcv']

       # Check 1: Minimum data requirement
       if len(df) < 50:
           raise InsufficientDataError(f"Need 50+ bars, got {len(df)}")

       # Check 2: Required columns
       required_cols = ['open', 'high', 'low', 'close', 'volume']
       missing_cols = set(required_cols) - set(df.columns)
       if missing_cols:
           raise SchemaValidationError(f"Missing columns: {missing_cols}")

       # Check 3: Data types
       for col in required_cols[:-1]:  # OHLC
           if not pd.api.types.is_numeric_dtype(df[col]):
               raise TypeError(f"Column {col} must be numeric")

       # Check 4: Logical consistency
       if (df['high'] < df['low']).any():
           raise DataCorruptionError("Invalid OHLC: high < low")
       if (df['high'] < df['close']).any():
           raise DataCorruptionError("Invalid OHLC: high < close")
       if (df['low'] > df['close']).any():
           raise DataCorruptionError("Invalid OHLC: low > close")
       if (df['volume'] < 0).any():
           raise DataCorruptionError("Negative volume detected")

       # Check 5: Missing values
       null_counts = df[required_cols].isnull().sum()
       if null_counts.any():
           total_nulls = null_counts.sum()
           null_pct = (total_nulls / (len(df) * len(required_cols))) * 100
           if null_pct > 5:  # >5% missing is too much
               raise DataQualityError(f"Too many nulls: {null_pct:.1f}%")

       return True
   ```

2. **Post-Computation Checkpoint** (after OODA ACT phase):

   ```python
   def validate_post_computation(pattern_results):
       """Validate pattern detection outputs"""
       # Check 1: Results structure
       if not isinstance(pattern_results, list):
           raise ValidationError("Pattern results must be list")

       for i, result in enumerate(pattern_results):
           # Check 2: Required fields
           if 'pattern' not in result:
               raise ValidationError(f"Result {i} missing 'pattern' field")
           if 'confidence' not in result:
               raise ValidationError(f"Result {i} missing 'confidence' field")

           # Check 3: Confidence range
           conf = result['confidence']
           if not (0.0 <= conf <= 1.0):
               raise ValidationError(f"Invalid confidence {conf}, must be [0,1]")

           # Check 4: Pattern type validity
           valid_patterns = ['breakout', 'pullback', 'pead', 'divergence']
           if result['pattern'] not in valid_patterns:
               raise ValidationError(f"Unknown pattern: {result['pattern']}")

       return True
   ```

3. **Output Schema Checkpoint** (before OODA REFLECT phase):

   ```python
   from pydantic import ValidationError as PydanticValidationError

   def validate_output_schema(output):
       """Validate against Pydantic schema"""
       try:
           if output['status'] == 'SUCCESS':
               validated = SuccessResponse(**output)
           else:
               validated = FailureResponse(**output)
           return validated
       except PydanticValidationError as e:
           raise SchemaValidationError(f"Schema validation failed: {e}")
   ```

**Checkpoint Integration in OODA Loop**:

```python
async def run_ooda_loop_with_checkpoints(self, symbol, timeframe):
    """OODA loop with validation checkpoints"""
    try:
        # 1. OBSERVE
        observation = await self.observe(symbol, timeframe)

        # CHECKPOINT: Pre-computation
        validate_pre_computation(observation)

        # 2. ORIENT
        orientation = self.orient(observation)

        # 3. DECIDE
        decision = self.decide(orientation)

        # 4. ACT
        action_results = self.act(decision)

        # CHECKPOINT: Post-computation
        validate_post_computation(action_results)

        # 5. VALIDATE
        validated_results = self.validate(action_results)

        # 6. REFLECT
        output = self.reflect(validated_results, decision)

        # CHECKPOINT: Output schema
        validated_output = validate_output_schema(output)

        return validated_output

    except Exception as e:
        # Error recovery decision tree
        action = determine_recovery_action(e, {
            'retry_count': 0,
            'can_wait': True
        })

        if action == RecoveryAction.RETRY:
            return await retry_with_backoff(
                lambda: self.run_ooda_loop_with_checkpoints(symbol, timeframe)
            )
        elif action == RecoveryAction.FAIL:
            return self._generate_failure_response(e)
        elif action == RecoveryAction.PARTIAL_RESULT:
            return self._generate_partial_success_response(e)
```

---

### 3. Edge Case Handling

**Purpose**: Robust handling of unusual but valid scenarios

**When to Use**: Data anomalies, market conditions, boundary cases

**Edge Cases & Solutions**:

#### A. Missing Data (Gaps in OHLCV)

**Problem**: Data provider has gaps due to holidays, trading halts, API failures

**Detection**:

```python
def detect_data_gaps(df):
    """Identify gaps in timestamp sequence"""
    df = df.sort_values('timestamp')
    df['time_diff'] = df['timestamp'].diff()

    # Expected frequency (e.g., 1 day for daily data)
    expected_freq = pd.Timedelta(days=1)  # Adjust based on timeframe

    gaps = df[df['time_diff'] > expected_freq * 1.5]  # 50% tolerance
    return gaps
```

**Solution**:

```python
def handle_data_gaps(df, max_gap_size=3):
    """Forward-fill short gaps, fail on long gaps"""
    gaps = detect_data_gaps(df)

    if gaps.empty:
        return df

    for idx, gap_row in gaps.iterrows():
        gap_size = (gap_row['time_diff'] / pd.Timedelta(days=1)).days

        if gap_size <= max_gap_size:
            # Forward-fill short gaps
            df.loc[idx, ['open', 'high', 'low', 'close']] = df.loc[idx - 1, 'close']
            df.loc[idx, 'volume'] = 0  # No volume on filled bars
        else:
            # Fail on long gaps
            raise DataGapError(f"Gap too large: {gap_size} bars at {gap_row['timestamp']}")

    return df
```

#### B. Insufficient History

**Problem**: Requested timeframe doesn't have enough bars for indicators

**Solution**:

```python
def handle_insufficient_history(df, min_required=50, current_operation='pattern_detection'):
    """Graceful degradation based on available history"""
    available_bars = len(df)

    if available_bars < min_required:
        # Calculate what's possible with available data
        if available_bars >= 20:
            # Can do simple patterns (20-bar Donchian)
            return 'simple_patterns_only'
        elif available_bars >= 10:
            # Can do basic indicators (10-bar SMA)
            return 'indicators_only'
        else:
            # Not enough for any analysis
            raise InsufficientDataError(
                f"Need {min_required}+ bars for {current_operation}, got {available_bars}"
            )

    return 'full_analysis'

# Usage
analysis_level = handle_insufficient_history(df)
if analysis_level == 'simple_patterns_only':
    patterns_to_detect = ['breakout']  # Skip complex patterns
elif analysis_level == 'indicators_only':
    patterns_to_detect = []  # Skip all patterns
```

#### C. Zero Volume Bars

**Problem**: After-hours trading, low liquidity stocks, data errors

**Solution**:

```python
def handle_zero_volume(df):
    """Handle zero-volume bars"""
    zero_vol_mask = df['volume'] == 0

    if zero_vol_mask.sum() == 0:
        return df  # No zero-volume bars

    zero_vol_pct = (zero_vol_mask.sum() / len(df)) * 100

    if zero_vol_pct > 20:
        # Too many zero-volume bars, likely data issue
        raise DataQualityError(f"{zero_vol_pct:.1f}% of bars have zero volume")

    # For small percentage, flag but continue
    df['zero_volume_flag'] = zero_vol_mask

    # Disable volume-based signals for these bars
    df.loc[zero_vol_mask, 'volume_confirmation'] = False

    return df
```

#### D. Extreme Values (Flash Crashes, Errors)

**Problem**: Price spikes due to data errors or genuine market events

**Detection**:

```python
def detect_extreme_values(df, z_threshold=5.0):
    """Detect statistical outliers using z-score"""
    df['returns'] = df['close'].pct_change()

    # Z-score of returns
    mean_return = df['returns'].mean()
    std_return = df['returns'].std()
    df['z_score'] = (df['returns'] - mean_return) / (std_return + 1e-9)

    # Flag extreme values
    extreme_mask = abs(df['z_score']) > z_threshold

    return df[extreme_mask]
```

**Solution**:

```python
def handle_extreme_values(df, z_threshold=5.0, action='flag'):
    """Handle extreme value outliers"""
    extreme_rows = detect_extreme_values(df, z_threshold)

    if extreme_rows.empty:
        return df

    if action == 'flag':
        # Flag but keep data
        df['extreme_value_flag'] = False
        df.loc[extreme_rows.index, 'extreme_value_flag'] = True

    elif action == 'cap':
        # Cap at threshold
        df.loc[extreme_rows.index, 'returns'] = df['returns'].clip(
            lower=df['returns'].quantile(0.01),
            upper=df['returns'].quantile(0.99)
        )

    elif action == 'remove':
        # Remove outlier bars
        df = df.drop(extreme_rows.index)

    return df
```

#### E. Regime Changes (Trending → Ranging)

**Problem**: Pattern detection optimized for one regime fails in another

**Solution**:

```python
def detect_regime_change(df, window=20):
    """Detect regime transitions"""
    # ADX for trend strength
    adx = talib.ADX(df['high'].values, df['low'].values, df['close'].values, window)
    df['adx'] = adx

    # Bollinger Band width for volatility
    upper, middle, lower = talib.BBANDS(df['close'].values, window)
    df['bb_width'] = (upper - lower) / middle

    # Classify regimes
    df['regime'] = 'transitional'  # Default
    df.loc[df['adx'] > 25, 'regime'] = 'trending'
    df.loc[(df['adx'] < 20) & (df['bb_width'] < df['bb_width'].quantile(0.2)), 'regime'] = 'ranging'

    # Detect transitions
    df['regime_change'] = df['regime'] != df['regime'].shift(1)

    return df

def handle_regime_change(df, orientation):
    """Adjust pattern selection on regime change"""
    df = detect_regime_change(df)

    if df['regime_change'].iloc[-1]:
        # Regime just changed, reduce confidence
        orientation['context_quality'] *= 0.8
        orientation['regime_change_detected'] = True

    return orientation
```

---

### 4. Performance Optimization Patterns

**Purpose**: Minimize latency and resource usage

**When to Use**: Production environments, high-frequency analysis, batch processing

**Optimization Techniques**:

#### A. Exponential Backoff with Jitter

**Purpose**: Prevent thundering herd on retry

```python
import random

def exponential_backoff_with_jitter(attempt, base_delay=1.0, max_delay=30.0):
    """Calculate backoff delay with jitter"""
    delay = min(base_delay * (2 ** attempt), max_delay)
    jitter = random.uniform(0, delay * 0.1)  # ±10% jitter
    return delay + jitter
```

#### B. Circuit Breaker (Detailed Implementation)

**Purpose**: Prevent cascade failures by failing fast

```python
from enum import Enum
import time

class CircuitState(Enum):
    CLOSED = 'closed'  # Normal operation
    OPEN = 'open'      # Failing fast
    HALF_OPEN = 'half_open'  # Testing recovery

class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60, success_threshold=2):
        self.failure_threshold = failure_threshold
        self.timeout = timeout  # Seconds before trying again
        self.success_threshold = success_threshold  # Successes needed to close circuit

        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED

    def call(self, func, *args, **kwargs):
        """Execute function with circuit breaker protection"""
        if self.state == CircuitState.OPEN:
            # Check if timeout expired
            if time.time() - self.last_failure_time >= self.timeout:
                self.state = CircuitState.HALF_OPEN
                self.success_count = 0
            else:
                raise CircuitBreakerOpen(
                    f"Circuit breaker open, retry after {self.timeout - (time.time() - self.last_failure_time):.1f}s"
                )

        try:
            result = func(*args, **kwargs)

            # Success handling
            if self.state == CircuitState.HALF_OPEN:
                self.success_count += 1
                if self.success_count >= self.success_threshold:
                    self.state = CircuitState.CLOSED
                    self.failure_count = 0

            elif self.state == CircuitState.CLOSED:
                self.failure_count = 0  # Reset on success

            return result

        except Exception as e:
            # Failure handling
            self.failure_count += 1
            self.last_failure_time = time.time()

            if self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN

            if self.state == CircuitState.HALF_OPEN:
                self.state = CircuitState.OPEN  # Immediate reopen on failure

            raise
```

#### C. Memory-Aware Chunking

**Purpose**: Process large datasets without OOM errors

```python
def memory_aware_chunking(df, max_memory_mb=500):
    """Calculate optimal chunk size based on memory limit"""
    # Estimate memory per row (rough)
    sample_size = min(1000, len(df))
    sample_memory = df.head(sample_size).memory_usage(deep=True).sum()
    bytes_per_row = sample_memory / sample_size

    # Calculate chunk size
    max_bytes = max_memory_mb * 1024 * 1024
    chunk_size = int(max_bytes / bytes_per_row)

    # Ensure minimum chunk size
    chunk_size = max(chunk_size, 1000)

    return chunk_size
```

---

### 5. Confidence Scoring Formulas

**Purpose**: Quantify reliability of pattern detections

**Formulas**:

#### A. Base Confidence (Pattern-Specific)

See `domain-knowledge-pattern-detection.md` for detailed formulas per pattern type.

#### B. Context Quality Adjustment

```python
def adjust_confidence_for_context(base_confidence, context_quality):
    """Adjust pattern confidence based on context quality"""
    # Context quality from ORIENT phase (0.0-1.0)
    adjusted = base_confidence * (0.5 + 0.5 * context_quality)
    return min(adjusted, 1.0)
```

#### C. Multi-Pattern Consensus Boost

```python
def consensus_boost(pattern_confidences, agreement_threshold=0.7):
    """Boost confidence when multiple patterns agree"""
    if len(pattern_confidences) < 2:
        return max(pattern_confidences)

    # Calculate agreement (all same direction)
    directions = [p['direction'] for p in pattern_confidences]
    agreement = directions.count(directions[0]) / len(directions)

    if agreement >= agreement_threshold:
        # Boost highest confidence
        max_conf = max(p['confidence'] for p in pattern_confidences)
        boost = min(0.15, 0.05 * (len(pattern_confidences) - 1))
        return min(max_conf + boost, 1.0)
    else:
        # No consensus, return highest individual
        return max(p['confidence'] for p in pattern_confidences)
```

#### D. Regime Mismatch Penalty

```python
def regime_penalty(confidence, pattern_type, regime):
    """Penalize confidence if pattern-regime mismatch"""
    # Optimal pattern-regime pairs
    optimal_pairs = {
        'breakout': ['trending', 'volatile'],
        'pullback': ['trending'],
        'divergence': ['ranging', 'transitional'],
        'pead': ['volatile']
    }

    if regime in optimal_pairs.get(pattern_type, []):
        return confidence  # No penalty
    else:
        return confidence * 0.7  # 30% penalty for mismatch
```

---

## Anti-Patterns

### 1. Swallowing Errors Silently

**Problem**: Errors caught but not logged, impossible to diagnose
**Alternative**: Always log errors with context, use structured logging

### 2. Retry Without Backoff

**Problem**: Hammering failed service, exacerbating load
**Alternative**: Exponential backoff with jitter, circuit breaker

### 3. No Partial Results

**Problem**: One failure causes total failure, wasting valid work
**Alternative**: Collect partial results, return what succeeded with warnings

### 4. Fixed Thresholds Across Regimes

**Problem**: Confidence thresholds optimized for trending fail in ranging markets
**Alternative**: Regime-adaptive thresholds, dynamic adjustment

### 5. No Telemetry on Error Paths

**Problem**: Cannot measure error rates, recovery effectiveness
**Alternative**: Emit metrics (error_count, retry_count, circuit_breaker_state)

---

## Integration Points

### OODA Loop Framework

- Validation checkpoints at phase transitions
- Error recovery integrated into loop execution
- See: `development-architecture-integration.md`

### Pattern Detection

- Confidence formulas applied to pattern results
- Regime mismatch penalties
- See: `domain-knowledge-pattern-detection.md`

### DataConnector Protocol

- Circuit breaker protects connector calls
- Retry logic for transient failures
- See: `development-architecture-integration.md`

### Multi-Indicator Coordination

- Handles missing indicator gracefully
- Partial results when subset fails
- See: `development-multi-indicator-coordination.md`

---

## Sources

1. **Nygard, Michael T.** (2007). _Release It!: Design and Deploy Production-Ready Software_. Pragmatic Bookshelf. ISBN: 978-0978739218
   - Circuit breaker pattern, bulkhead isolation, fail-fast

2. **Kleppmann, Martin** (2017). _Designing Data-Intensive Applications_. O'Reilly Media. ISBN: 978-1449373320
   - Retry strategies, partial failures, data quality

3. **Newman, Sam** (2015). _Building Microservices_. O'Reilly Media. ISBN: 978-1491950357
   - Resilience patterns, cascading failures

4. **Humble, Jez & Farley, David** (2010). _Continuous Delivery_. Addison-Wesley. ISBN: 978-0321601919
   - Validation gates, quality checkpoints

5. **AWS Architecture Blog** (2024). "Exponential Backoff and Jitter". <https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/>
   - Backoff algorithms, retry best practices

6. **Google SRE Book** (2016). _Site Reliability Engineering_. O'Reilly Media. ISBN: 978-1491929124
   - Error budgets, graceful degradation, SLO management

7. **Fowler, Martin** (2004). "CircuitBreaker". <https://martinfowler.com/bliki/CircuitBreaker.html>
   - Circuit breaker pattern documentation

---

**Version**: 1.0
**Last Updated**: 2025-11-16
**Agent**: pattern-detector
