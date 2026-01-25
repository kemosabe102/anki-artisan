# Architecture Integration Patterns

## Overview

Integration patterns for pattern-detector agent including DataConnector protocol specification, OODA loop implementation, Fact Object mapping, output schema design, and testing strategies.

## Core Frameworks

### 1. DataConnector Protocol Specification

**Purpose**: Standardized interface for data ingestion across all agents

**When to Use**: All agent data access, external system integration, data source abstraction

**Protocol Definition**:

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import pandas as pd

class DataConnector(ABC):
    """Abstract base class for data connectors"""

    @abstractmethod
    async def fetch_ohlcv(
        self,
        symbol: str,
        timeframe: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Fetch OHLCV data for given symbol and timeframe

        Returns:
            DataFrame with columns: ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        """
        pass

    @abstractmethod
    async def fetch_fundamental(
        self,
        symbol: str,
        data_type: str,  # 'earnings', 'financials', etc.
    ) -> Dict[str, Any]:
        """Fetch fundamental data"""
        pass

    @abstractmethod
    def validate_connection(self) -> bool:
        """Test connection health"""
        pass

    @abstractmethod
    def get_rate_limit_status(self) -> Dict[str, Any]:
        """Return current rate limit status"""
        pass
```

**Pattern Detector Usage**:

```python
class PatternDetector:
    def __init__(self, data_connector: DataConnector):
        self.data_connector = data_connector

    async def detect_patterns(self, symbol: str, timeframe: str = '1d'):
        """Main entry point for pattern detection"""
        # Fetch data via connector
        df = await self.data_connector.fetch_ohlcv(
            symbol=symbol,
            timeframe=timeframe,
            limit=200  # Sufficient for most indicators
        )

        # Validate data
        if len(df) < 50:
            raise InsufficientDataError(f"Need 50+ bars, got {len(df)}")

        # Process patterns
        patterns = self._process_patterns(df)
        return patterns
```

**Error Handling Requirements**:

1. **Connection Failures**:

   ```python
   class CircuitBreaker:
       def __init__(self, failure_threshold=5, timeout=60):
           self.failure_count = 0
           self.failure_threshold = failure_threshold
           self.timeout = timeout
           self.last_failure_time = None

       def call(self, func, *args, **kwargs):
           if self.failure_count >= self.failure_threshold:
               if time.time() - self.last_failure_time < self.timeout:
                   raise CircuitBreakerOpen("Circuit breaker open, retry later")
               else:
                   self.failure_count = 0  # Reset after timeout

           try:
               result = func(*args, **kwargs)
               self.failure_count = 0  # Success resets counter
               return result
           except Exception as e:
               self.failure_count += 1
               self.last_failure_time = time.time()
               raise
   ```

2. **Rate Limit Handling**:

   ```python
   async def fetch_with_rate_limit(connector, symbol, timeframe):
       """Respect rate limits with exponential backoff"""
       max_retries = 3
       for attempt in range(max_retries):
           rate_limit = connector.get_rate_limit_status()
           if rate_limit['remaining'] == 0:
               wait_time = rate_limit['reset_time'] - time.time()
               await asyncio.sleep(wait_time)

           try:
               return await connector.fetch_ohlcv(symbol, timeframe)
           except RateLimitError:
               if attempt == max_retries - 1:
                   raise
               await asyncio.sleep(2 ** attempt)  # Exponential backoff
   ```

3. **Data Validation**:

   ```python
   def validate_ohlcv_dataframe(df):
       """Validate DataConnector output"""
       required_cols = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
       if not all(col in df.columns for col in required_cols):
           raise ValueError(f"Missing columns: {set(required_cols) - set(df.columns)}")

       # Type validation
       numeric_cols = ['open', 'high', 'low', 'close', 'volume']
       for col in numeric_cols:
           if not pd.api.types.is_numeric_dtype(df[col]):
               raise TypeError(f"Column {col} must be numeric")

       # Logical validation
       if (df['high'] < df['low']).any():
           raise ValueError("Invalid OHLC: high < low")
       if (df['volume'] < 0).any():
           raise ValueError("Invalid volume: negative values")

       return True
   ```

---

### 2. OODA Loop Implementation Patterns

**Purpose**: 6-phase workflow for systematic pattern detection

**When to Use**: All agent operations, complex multi-step analysis, decision-making workflows

**6-Phase Workflow**:

1. **OBSERVE** (Data Collection):

   ```python
   async def observe(self, symbol: str, timeframe: str):
       """Gather data and context"""
       # Fetch OHLCV
       df = await self.data_connector.fetch_ohlcv(symbol, timeframe, limit=200)

       # Fetch optional context (earnings, sentiment)
       try:
           fundamentals = await self.data_connector.fetch_fundamental(symbol, 'earnings')
       except NotImplementedError:
           fundamentals = None

       return {
           'ohlcv': df,
           'fundamentals': fundamentals,
           'symbol': symbol,
           'timeframe': timeframe
       }
   ```

2. **ORIENT** (Context Assessment):

   ```python
   def orient(self, observation):
       """Assess market regime and context quality"""
       df = observation['ohlcv']

       # Calculate regime indicators
       adx = talib.ADX(df['high'].values, df['low'].values, df['close'].values, 14)
       atr_pct = (df['atr'] / df['close']) * 100

       regime = self._classify_regime(adx[-1], atr_pct.iloc[-1])

       # Context quality score
       context_quality = self._assess_context_quality(observation)

       return {
           'regime': regime,
           'context_quality': context_quality,
           'observation': observation
       }
   ```

3. **DECIDE** (Pattern Selection):

   ```python
   def decide(self, orientation):
       """Select patterns to detect based on regime"""
       regime = orientation['regime']
       context_quality = orientation['context_quality']

       if context_quality < 0.5:
           return {'patterns_to_detect': [], 'skip_reason': 'insufficient_context'}

       # Regime-specific pattern selection
       if regime == 'trending':
           patterns = ['breakout', 'pullback', 'hidden_divergence']
       elif regime == 'ranging':
           patterns = ['regular_divergence', 'support_resistance']
       else:  # volatile
           patterns = ['pead']  # News-driven only

       return {
           'patterns_to_detect': patterns,
           'regime': regime,
           'orientation': orientation
       }
   ```

4. **ACT** (Pattern Detection):

   ```python
   def act(self, decision):
       """Execute pattern detection"""
       patterns_to_detect = decision['patterns_to_detect']
       df = decision['orientation']['observation']['ohlcv']

       results = []
       for pattern_type in patterns_to_detect:
           try:
               pattern_result = self._detect_pattern(df, pattern_type)
               results.append(pattern_result)
           except Exception as e:
               results.append({
                   'pattern': pattern_type,
                   'status': 'failed',
                   'error': str(e)
               })

       return results
   ```

5. **VALIDATE** (Confidence Scoring):

   ```python
   def validate(self, action_results):
       """Validate and score pattern detections"""
       validated_results = []

       for result in action_results:
           if result.get('status') == 'failed':
               continue

           # Multi-indicator confirmation
           confidence = self._calculate_confidence(result)

           # Apply minimum threshold
           if confidence >= 0.5:
               result['confidence'] = confidence
               validated_results.append(result)

       return validated_results
   ```

6. **REFLECT** (Output Generation):

   ```python
   def reflect(self, validated_results, decision):
       """Generate final output with metadata"""
       regime = decision['regime']
       context_quality = decision['orientation']['context_quality']

       return {
           'status': 'SUCCESS' if validated_results else 'SUCCESS',  # Empty is valid
           'patterns_detected': validated_results,
           'metadata': {
               'regime': regime,
               'context_quality': context_quality,
               'patterns_evaluated': decision['patterns_to_detect'],
               'timestamp': pd.Timestamp.now().isoformat()
           }
       }
   ```

**Full Workflow Integration**:

```python
async def run_ooda_loop(self, symbol: str, timeframe: str):
    """Complete OODA loop execution"""
    # 1. OBSERVE
    observation = await self.observe(symbol, timeframe)

    # 2. ORIENT
    orientation = self.orient(observation)

    # 3. DECIDE
    decision = self.decide(orientation)

    # 4. ACT
    action_results = self.act(decision)

    # 5. VALIDATE
    validated_results = self.validate(action_results)

    # 6. REFLECT
    output = self.reflect(validated_results, decision)

    return output
```

---

### 3. Fact Object Integration

**Purpose**: Map pattern detections to standardized Fact objects for downstream processing

**Fact Object Schema**:

```python
from dataclasses import dataclass
from typing import Dict, Any, Optional
from datetime import datetime

@dataclass
class Fact:
    """Standardized fact object"""
    category: str  # Pattern type: 'breakout', 'pullback', 'pead', 'divergence'
    confidence: float  # 0.0-1.0
    timestamp: datetime
    symbol: str
    timeframe: str
    metadata: Dict[str, Any]  # Pattern-specific details
    source_agent: str = 'pattern-detector'

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary"""
        return {
            'category': self.category,
            'confidence': self.confidence,
            'timestamp': self.timestamp.isoformat(),
            'symbol': self.symbol,
            'timeframe': self.timeframe,
            'metadata': self.metadata,
            'source_agent': self.source_agent
        }
```

**Pattern → Fact Mapping**:

```python
def pattern_to_fact(pattern_result, symbol, timeframe):
    """Convert pattern detection to Fact object"""
    pattern_type = pattern_result['pattern']
    confidence = pattern_result['confidence']

    # Pattern-specific metadata extraction
    if pattern_type == 'breakout':
        metadata = {
            'direction': pattern_result.get('direction', 'unknown'),
            'channel_high': pattern_result.get('channel_high'),
            'channel_low': pattern_result.get('channel_low'),
            'volume_multiplier': pattern_result.get('volume_multiplier'),
            'adx': pattern_result.get('adx')
        }
    elif pattern_type == 'pullback':
        metadata = {
            'ema_fast': pattern_result.get('ema_fast'),
            'ema_slow': pattern_result.get('ema_slow'),
            'rsi': pattern_result.get('rsi'),
            'adx': pattern_result.get('adx')
        }
    elif pattern_type == 'pead':
        metadata = {
            'sue': pattern_result.get('sue'),
            'gap_pct': pattern_result.get('gap_pct'),
            'sentiment_score': pattern_result.get('sentiment_score'),
            'drift_days': pattern_result.get('drift_days')
        }
    elif pattern_type == 'divergence':
        metadata = {
            'divergence_type': pattern_result.get('divergence_type'),  # 'regular' or 'hidden'
            'indicator': pattern_result.get('indicator'),  # 'rsi', 'macd'
            'price_peaks': pattern_result.get('price_peaks'),
            'indicator_peaks': pattern_result.get('indicator_peaks')
        }
    else:
        metadata = {}

    return Fact(
        category=pattern_type,
        confidence=confidence,
        timestamp=datetime.now(),
        symbol=symbol,
        timeframe=timeframe,
        metadata=metadata
    )
```

**Batch Fact Generation**:

```python
def generate_facts(validated_results, symbol, timeframe):
    """Convert all pattern results to Facts"""
    facts = []
    for pattern_result in validated_results:
        fact = pattern_to_fact(pattern_result, symbol, timeframe)
        facts.append(fact)
    return facts
```

---

### 4. Output Schema Design

**Purpose**: Standardized SUCCESS/FAILURE response format

**Schema Definition**:

```python
from typing import List, Optional
from pydantic import BaseModel, Field

class PatternDetectionMetadata(BaseModel):
    regime: str
    context_quality: float = Field(ge=0.0, le=1.0)
    patterns_evaluated: List[str]
    timestamp: str

class PatternDetectionOutput(BaseModel):
    """Agent-specific output for pattern-detector"""
    patterns_detected: List[Dict[str, Any]]
    facts: List[Dict[str, Any]]  # Serialized Fact objects
    metadata: PatternDetectionMetadata

class SuccessResponse(BaseModel):
    status: str = 'SUCCESS'
    agent: str = 'pattern-detector'
    task_id: str
    operation_type: str = 'detect_patterns'
    summary: str
    confidence: float = Field(ge=0.0, le=1.0)
    execution_timestamp: str
    agent_specific_output: PatternDetectionOutput

class FailureDetails(BaseModel):
    failure_type: str  # 'insufficient_data', 'connection_error', 'validation_error'
    reasons: List[str]
    partial_results: Optional[PatternDetectionOutput] = None
    recovery_suggestions: List[str]
    next_steps: str

class FailureResponse(BaseModel):
    status: str = 'FAILURE'
    agent: str = 'pattern-detector'
    task_id: str
    operation_type: str = 'detect_patterns'
    summary: str
    confidence: float = Field(ge=0.0, le=1.0)
    execution_timestamp: str
    failure_details: FailureDetails
```

**Usage Example**:

```python
def generate_success_response(patterns, facts, metadata, task_id):
    """Generate SUCCESS response"""
    output = PatternDetectionOutput(
        patterns_detected=patterns,
        facts=[fact.to_dict() for fact in facts],
        metadata=metadata
    )

    return SuccessResponse(
        task_id=task_id,
        summary=f"Detected {len(patterns)} patterns with avg confidence {sum(p['confidence'] for p in patterns) / len(patterns):.2f}",
        confidence=0.85,  # Overall agent confidence
        execution_timestamp=datetime.now().isoformat(),
        agent_specific_output=output
    )

def generate_failure_response(error_type, reasons, task_id, partial_results=None):
    """Generate FAILURE response"""
    failure_details = FailureDetails(
        failure_type=error_type,
        reasons=reasons,
        partial_results=partial_results,
        recovery_suggestions=[
            "Check DataConnector health",
            "Verify symbol validity",
            "Increase data limit if insufficient history"
        ],
        next_steps='escalate_to_orchestrator'
    )

    return FailureResponse(
        task_id=task_id,
        summary=f"Pattern detection failed: {error_type}",
        confidence=0.0,
        execution_timestamp=datetime.now().isoformat(),
        failure_details=failure_details
    )
```

---

### 5. Integration Testing Strategies

**Purpose**: Validate end-to-end integration with mocked dependencies

**Test Structure**:

```python
import pytest
from unittest.mock import AsyncMock, MagicMock
import pandas as pd

@pytest.fixture
def mock_data_connector():
    """Mock DataConnector for testing"""
    connector = AsyncMock(spec=DataConnector)

    # Mock OHLCV data
    mock_df = pd.DataFrame({
        'timestamp': pd.date_range('2024-01-01', periods=100),
        'open': [100 + i for i in range(100)],
        'high': [105 + i for i in range(100)],
        'low': [95 + i for i in range(100)],
        'close': [102 + i for i in range(100)],
        'volume': [1000000] * 100
    })
    connector.fetch_ohlcv.return_value = mock_df

    # Mock rate limit status
    connector.get_rate_limit_status.return_value = {'remaining': 100, 'reset_time': time.time() + 3600}

    return connector

@pytest.fixture
def pattern_detector(mock_data_connector):
    """Pattern detector with mocked dependencies"""
    return PatternDetector(data_connector=mock_data_connector)

@pytest.mark.asyncio
async def test_ooda_loop_success(pattern_detector):
    """Test successful OODA loop execution"""
    result = await pattern_detector.run_ooda_loop('AAPL', '1d')

    assert result['status'] == 'SUCCESS'
    assert 'patterns_detected' in result
    assert 'metadata' in result
    assert result['metadata']['context_quality'] >= 0.0

@pytest.mark.asyncio
async def test_insufficient_data_handling(pattern_detector, mock_data_connector):
    """Test handling of insufficient data"""
    # Mock insufficient data
    short_df = pd.DataFrame({
        'timestamp': pd.date_range('2024-01-01', periods=10),
        'open': [100] * 10,
        'high': [105] * 10,
        'low': [95] * 10,
        'close': [102] * 10,
        'volume': [1000000] * 10
    })
    mock_data_connector.fetch_ohlcv.return_value = short_df

    with pytest.raises(InsufficientDataError):
        await pattern_detector.detect_patterns('AAPL', '1d')

@pytest.mark.asyncio
async def test_fact_object_generation(pattern_detector):
    """Test Fact object creation from patterns"""
    result = await pattern_detector.run_ooda_loop('AAPL', '1d')
    facts = result['agent_specific_output']['facts']

    assert len(facts) > 0
    for fact in facts:
        assert 'category' in fact
        assert 'confidence' in fact
        assert 'timestamp' in fact
        assert 'symbol' in fact
        assert 'metadata' in fact

@pytest.mark.asyncio
async def test_circuit_breaker_trigger(pattern_detector, mock_data_connector):
    """Test circuit breaker activation"""
    # Simulate repeated failures
    mock_data_connector.fetch_ohlcv.side_effect = ConnectionError("API down")

    circuit_breaker = CircuitBreaker(failure_threshold=3, timeout=60)

    for i in range(5):
        try:
            circuit_breaker.call(mock_data_connector.fetch_ohlcv, 'AAPL', '1d')
        except (ConnectionError, CircuitBreakerOpen):
            pass

    # Should raise CircuitBreakerOpen after threshold
    with pytest.raises(CircuitBreakerOpen):
        circuit_breaker.call(mock_data_connector.fetch_ohlcv, 'AAPL', '1d')
```

**Integration Test Coverage Goals**:

- OODA loop phases: 100%
- DataConnector error paths: 100%
- Fact object generation: 100%
- Schema validation: 100%
- Circuit breaker logic: 100%

---

## Anti-Patterns

### 1. Tight Coupling to DataConnector Implementation

**Problem**: Agent breaks when connector implementation changes
**Alternative**: Depend on abstract DataConnector protocol, use dependency injection

### 2. Skipping OODA Phases

**Problem**: Jumping straight to pattern detection without context assessment
**Alternative**: Always execute full OODA loop, skip only when context_quality gate fails

### 3. Ignoring Partial Results

**Problem**: Failing entire operation if one pattern detection fails
**Alternative**: Collect all results, return partial success with warnings

### 4. Hardcoded Thresholds

**Problem**: Magic numbers scattered throughout code
**Alternative**: Configuration-driven thresholds, regime-adaptive parameters

### 5. No Telemetry

**Problem**: Cannot diagnose failures in production
**Alternative**: Log OODA phase transitions, emit metrics (latency, pattern counts, confidence distribution)

---

## Integration Points

### Pattern Detection Framework

- Implements pattern detection algorithms
- Outputs feed Fact objects
- See: `domain-knowledge-pattern-detection.md`

### Multi-Indicator Coordination

- Coordinates indicator signals before Fact generation
- Provides confidence scores for pattern validation
- See: `development-multi-indicator-coordination.md`

### TA-Lib Integration

- DataConnector feeds OHLCV to TA-Lib computation
- Indicator outputs used in pattern detection
- See: `development-talib-integration.md`

### Error Recovery

- Circuit breaker protects DataConnector calls
- Validation checkpoints in OODA loop
- See: `development-error-recovery.md`

### Downstream Systems

- Facts consumed by trading strategy agents
- Patterns feed alerting/notification systems
- Metadata used for backtesting/analysis

---

## Sources

1. **Boyd, John** (1976). "The Essence of Winning and Losing" (OODA Loop). Unpublished briefing.
   - OODA loop methodology, decision-making framework

2. **Gamma, Erich et al.** (1994). _Design Patterns: Elements of Reusable Object-Oriented Software_. Addison-Wesley. ISBN: 978-0201633610
   - Abstract interface pattern, dependency injection

3. **Fowler, Martin** (2002). _Patterns of Enterprise Application Architecture_. Addison-Wesley. ISBN: 978-0321127426
   - Data access patterns, circuit breaker

4. **Nygard, Michael T.** (2007). _Release It!: Design and Deploy Production-Ready Software_. Pragmatic Bookshelf. ISBN: 978-0978739218
   - Circuit breaker pattern, bulkhead isolation, rate limiting

5. **Evans, Eric** (2003). _Domain-Driven Design: Tackling Complexity in the Heart of Software_. Addison-Wesley. ISBN: 978-0321125217
   - Fact object pattern, domain model

6. **Pydantic Documentation** (2024). <https://docs.pydantic.dev/>
   - Schema validation, type safety

7. **pytest Documentation** (2024). <https://docs.pytest.org/>
   - Testing patterns, fixtures, mocking

---

**Version**: 1.0
**Last Updated**: 2025-11-16
**Agent**: pattern-detector
