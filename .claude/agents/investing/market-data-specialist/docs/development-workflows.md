# Market Data Specialist - Development Workflows & Patterns

**Category**: Development Workflows & Patterns
**Domain**: Market Data Integration & API Resilience
**Confidence**: 0.95 (extracted from production codebase patterns)
**Last Updated**: 2025-11-14T00:00:00Z
**Agent**: market-data-specialist

---

## Overview

This documentation provides production-ready patterns for implementing resilient market data connectors following the DataConnector Protocol, circuit breaker patterns, and multi-provider fallback chains. All patterns are extracted from the Gauntlet Agents codebase and represent battle-tested implementations.

**Key Concepts**:

- **DataConnector Protocol**: Unified interface for all external market data ingestion with standardized error handling
- **Circuit Breaker Pattern**: Fault tolerance mechanism preventing cascade failures across API providers
- **Multi-Provider Fallback Chain**: Sequential or concurrent orchestration pattern (Alpaca → Polygon → Yahoo)

---

## Core Frameworks

### Framework 1: DataConnector Protocol Compliance

**Purpose**: Standardize all market data integrations with consistent error handling, observability, and type safety following ADR-004 protocol requirements.

**When to Use**:

- Integrating any new market data provider (quotes, fundamentals, sentiment)
- Implementing custom data sources for technical analysis
- Building connectors for alternative data providers

**Components**:

1. **Protocol Interface**: Abstract contract defining `name`, `source_name`, `timeout_seconds`, `enabled` properties and `fetch()`, `health_check()` methods
2. **ConnectorInput**: Standardized input model with ticker symbol and optional parameters
3. **ConnectorResult**: Enhanced output with facts, status, error message, and comprehensive observability metrics (execution_time_ms, api_calls, cache_hit)
4. **ConnectorStatus Enum**: Standardized status codes (SUCCESS, PARTIAL_SUCCESS, NO_DATA, API_ERROR, TIMEOUT_ERROR, RATE_LIMITED, CONFIG_ERROR)

**How to Apply**:

1. Implement DataConnector protocol interface with all required properties and methods
2. **NEVER raise exceptions for predictable failures** (API errors, timeouts, rate limits) - return ConnectorResult with appropriate status
3. Include comprehensive observability metadata in every ConnectorResult (execution_time_ms, api_calls, cache_hit)
4. Implement health_check() for pre-flight validation without expensive API calls
5. Return ConnectorStatus.NO_DATA for valid queries with no results (not an error condition)

**Example from Codebase**:

```python
from packages.core.connectors.protocol import (
    DataConnector,
    ConnectorInput,
    ConnectorResult,
    ConnectorStatus,
)
from domain.models.facts import Fact
import asyncio


class AlpacaQuoteConnector(DataConnector):
    """Alpaca market data connector following DataConnector Protocol."""

    def __init__(self, api_key: str, api_secret: str, timeout: float = 10.0):
        self._api_key = api_key
        self._api_secret = api_secret
        self._timeout = timeout
        self._enabled = True

    @property
    def name(self) -> str:
        return "alpaca_quote"

    @property
    def source_name(self) -> str:
        return "Alpaca Markets"

    @property
    def timeout_seconds(self) -> float:
        return self._timeout

    @property
    def enabled(self) -> bool:
        return self._enabled

    async def fetch(self, input: ConnectorInput) -> ConnectorResult:
        """
        Fetch market data from Alpaca API.

        NEVER raises exceptions for operational failures - returns ConnectorResult
        with appropriate status code for all predictable failures.
        """
        start_time = time.monotonic()

        try:
            # Use timeout from protocol
            async with asyncio.timeout(self.timeout_seconds):
                # API call implementation
                response = await self._call_alpaca_api(input.ticker)

            elapsed_ms = (time.monotonic() - start_time) * 1000

            # Check for business logic failures (not exceptions)
            if response.status_code == 429:
                return ConnectorResult(
                    status=ConnectorStatus.RATE_LIMITED,
                    facts=[],
                    error_message="Alpaca rate limit exceeded",
                    source_name=self.source_name,
                    execution_time_ms=elapsed_ms,
                    api_calls=1,
                )

            if response.status_code == 404:
                return ConnectorResult(
                    status=ConnectorStatus.NO_DATA,
                    facts=[],
                    error_message=f"No data found for ticker {input.ticker}",
                    source_name=self.source_name,
                    execution_time_ms=elapsed_ms,
                    api_calls=1,
                )

            # Parse response and create facts
            data = response.json()
            facts = [
                Fact(
                    category="market_data",
                    key="current_price",
                    value=data["latest_quote"]["price"],
                    confidence=0.95,
                    source=self.source_name,
                )
            ]

            return ConnectorResult(
                status=ConnectorStatus.SUCCESS,
                facts=facts,
                source_name=self.source_name,
                execution_time_ms=elapsed_ms,
                api_calls=1,
                confidence_note="Real-time quote from Alpaca API",
            )

        except asyncio.TimeoutError:
            # Timeout is NOT an exception - return status
            elapsed_ms = (time.monotonic() - start_time) * 1000
            return ConnectorResult(
                status=ConnectorStatus.TIMEOUT_ERROR,
                facts=[],
                error_message=f"Alpaca API timeout after {self.timeout_seconds}s",
                source_name=self.source_name,
                execution_time_ms=elapsed_ms,
                api_calls=1,
            )

        except Exception as e:
            # Catch unexpected errors and return API_ERROR status
            elapsed_ms = (time.monotonic() - start_time) * 1000
            return ConnectorResult(
                status=ConnectorStatus.API_ERROR,
                facts=[],
                error_message=f"Alpaca API error: {str(e)}",
                source_name=self.source_name,
                execution_time_ms=elapsed_ms,
                api_calls=1,
            )

    async def health_check(self) -> bool:
        """Verify connector can operate (credentials valid, API reachable)."""
        try:
            # Lightweight check without consuming quota
            response = await self._call_alpaca_health_endpoint()
            return response.status_code == 200
        except Exception:
            return False  # NEVER raise exceptions from health_check
```

**Source**: `C:/Users/kemos/Repos/gauntlet-agents/packages/core/connectors/protocol.py` (lines 1-254)

---

### Framework 2: Circuit Breaker Resilience Pattern

**Purpose**: Prevent cascade failures and automatic API degradation by tracking failures, opening circuits after thresholds, and providing recovery periods.

**When to Use**:

- Wrapping all external API calls with failure tracking
- Multi-provider fallback chains requiring automatic skip logic
- Any service integration requiring fault tolerance (databases, cache, third-party APIs)

**Components**:

1. **CircuitBreakerConfig**: Configurable thresholds (failure_threshold=5, reset_timeout=60s, success_threshold=3)
2. **AsyncCircuitBreaker**: Async-aware wrapper around pybreaker with manual success/failure recording
3. **Circuit States**: CLOSED (healthy) → OPEN (failing) → HALF_OPEN (testing recovery) → CLOSED
4. **Manual Recording**: Explicit `record_success()` and `record_failure()` calls based on business logic evaluation

**How to Apply**:

1. Create AsyncCircuitBreaker instance with CircuitBreakerConfig for each external dependency
2. Wrap async operations with `circuit_breaker.call(async_operation, *args, **kwargs)`
3. **Manually record success/failure** after evaluating business logic (e.g., HTTP 200 but invalid data = failure)
4. Monitor circuit breaker state via `is_open`, `is_closed`, `is_half_open` properties
5. Configure thresholds based on SLO requirements and failure patterns

**Example from Codebase**:

```python
from packages.core.resilience import AsyncCircuitBreaker, CircuitBreakerConfig
import asyncio


class AlpacaConnectorWithCircuitBreaker:
    """Alpaca connector with circuit breaker protection."""

    def __init__(self, api_key: str, logger):
        self._api_key = api_key
        self._logger = logger

        # Configure circuit breaker
        cb_config = CircuitBreakerConfig(
            failure_threshold=5,  # Open after 5 consecutive failures
            reset_timeout=60,  # Wait 60s before testing recovery
            success_threshold=3,  # Need 3 successes to fully recover
        )

        # Create circuit breaker instance
        self._circuit_breaker = AsyncCircuitBreaker(
            name="alpaca_api", config=cb_config, logger=logger
        )

    async def fetch(self, ticker: str) -> ConnectorResult:
        """Fetch data with circuit breaker protection."""
        start_time = time.monotonic()

        try:
            # Check circuit state before calling (skip if fully open)
            if self._circuit_breaker.is_open and not self._circuit_breaker.is_half_open:
                self._logger.warning(
                    f"Circuit breaker OPEN for Alpaca - skipping call",
                    extra={"circuit_state": self._circuit_breaker.state},
                )
                return ConnectorResult(
                    status=ConnectorStatus.API_ERROR,
                    facts=[],
                    error_message="Circuit breaker open - Alpaca API unavailable",
                    source_name="Alpaca Markets",
                    execution_time_ms=0,
                    api_calls=0,
                )

            # Execute through circuit breaker
            async def api_call():
                async with asyncio.timeout(10.0):
                    return await self._call_alpaca_api(ticker)

            response = await self._circuit_breaker.call(api_call)

            # Business logic evaluation (NOT automatic success recording)
            if response.status_code == 200:
                data = response.json()

                # Check for valid data (business logic check)
                if "latest_quote" in data and data["latest_quote"]["price"] > 0:
                    # SUCCESS - manually record
                    await self._circuit_breaker.record_success()

                    facts = [
                        Fact(
                            category="market_data",
                            key="current_price",
                            value=data["latest_quote"]["price"],
                            confidence=0.95,
                            source="Alpaca Markets",
                        )
                    ]

                    elapsed_ms = (time.monotonic() - start_time) * 1000
                    return ConnectorResult(
                        status=ConnectorStatus.SUCCESS,
                        facts=facts,
                        source_name="Alpaca Markets",
                        execution_time_ms=elapsed_ms,
                        api_calls=1,
                    )
                else:
                    # Invalid data - manually record FAILURE
                    await self._circuit_breaker.record_failure(
                        Exception("Invalid quote data from Alpaca")
                    )

                    elapsed_ms = (time.monotonic() - start_time) * 1000
                    return ConnectorResult(
                        status=ConnectorStatus.API_ERROR,
                        facts=[],
                        error_message="Invalid quote data structure",
                        source_name="Alpaca Markets",
                        execution_time_ms=elapsed_ms,
                        api_calls=1,
                    )

            elif response.status_code == 429:
                # Rate limited - record FAILURE
                await self._circuit_breaker.record_failure(
                    Exception(f"Alpaca rate limited: {response.status_code}")
                )

                elapsed_ms = (time.monotonic() - start_time) * 1000
                return ConnectorResult(
                    status=ConnectorStatus.RATE_LIMITED,
                    facts=[],
                    error_message="Alpaca rate limit exceeded",
                    source_name="Alpaca Markets",
                    execution_time_ms=elapsed_ms,
                    api_calls=1,
                )

            else:
                # API error - record FAILURE
                await self._circuit_breaker.record_failure(
                    Exception(f"Alpaca API error: {response.status_code}")
                )

                elapsed_ms = (time.monotonic() - start_time) * 1000
                return ConnectorResult(
                    status=ConnectorStatus.API_ERROR,
                    facts=[],
                    error_message=f"HTTP {response.status_code}",
                    source_name="Alpaca Markets",
                    execution_time_ms=elapsed_ms,
                    api_calls=1,
                )

        except asyncio.TimeoutError:
            # Timeout - record FAILURE
            await self._circuit_breaker.record_failure(TimeoutError("API timeout"))

            elapsed_ms = (time.monotonic() - start_time) * 1000
            return ConnectorResult(
                status=ConnectorStatus.TIMEOUT_ERROR,
                facts=[],
                error_message="Alpaca API timeout after 10s",
                source_name="Alpaca Markets",
                execution_time_ms=elapsed_ms,
                api_calls=1,
            )

        except Exception as e:
            # Unexpected error - record FAILURE
            await self._circuit_breaker.record_failure(e)

            elapsed_ms = (time.monotonic() - start_time) * 1000
            return ConnectorResult(
                status=ConnectorStatus.API_ERROR,
                facts=[],
                error_message=f"Unexpected error: {str(e)}",
                source_name="Alpaca Markets",
                execution_time_ms=elapsed_ms,
                api_calls=1,
            )
```

**Source**: `C:/Users/kemos/Repos/gauntlet-agents/packages/core/resilience/async_circuit_breaker.py` (lines 1-428)

---

### Framework 3: Multi-Provider Fallback Chain Architecture

**Purpose**: Implement intelligent failover orchestration across multiple market data providers (Alpaca → Polygon → Yahoo) with circuit breaker integration, global timeout protection, and health-based routing.

**When to Use**:

- Multi-provider market data integration requiring automatic fallback
- SLO enforcement requiring global timeout guarantees
- Concurrent provider racing (early winner pattern) for latency optimization
- Health-based provider prioritization

**Components**:

1. **MultiAPIOrchestrator**: Orchestration layer managing provider lifecycle, circuit breakers, and health tracking
2. **OrchestratorConfig**: Configuration for global timeout, circuit breaker thresholds, concurrent providers, health checks
3. **ProviderHealth**: Health status tracking (is_healthy, consecutive_failures, success_rate_24h, average_latency_ms, circuit_breaker_state)
4. **Fallback Strategies**: Sequential (max_concurrent_providers=1) or concurrent (max_concurrent_providers>1) with early winner pattern

**How to Apply**:

1. Instantiate MultiAPIOrchestrator with ordered list of DataConnector providers (primary first, fallbacks last)
2. Configure OrchestratorConfig with global_timeout_seconds, circuit_breaker_failure_threshold, max_concurrent_providers
3. Call `fetch_with_fallback(input, timeout_seconds)` for orchestrated data retrieval
4. Orchestrator automatically:
   - Routes to healthy providers first via `_get_ordered_providers()`
   - Skips providers with OPEN circuit breakers
   - Tracks provider health and circuit breaker states
   - Returns first successful result with enhanced metadata
5. Monitor fallback chain via `get_orchestrator_metrics()`, `get_provider_health_status()`, `get_circuit_breaker_status()`

**Example from Codebase**:

```python
from packages.core.connectors.orchestrator import (
    MultiAPIOrchestrator,
    OrchestratorConfig,
    create_simple_orchestrator,
)
from packages.core.connectors.protocol import ConnectorInput


# Create provider instances (order matters: primary → secondary → tertiary)
alpaca_connector = AlpacaQuoteConnector(api_key="...", api_secret="...")
polygon_connector = PolygonQuoteConnector(api_key="...")
yahoo_connector = YahooFinanceConnector()

# Option 1: Simple orchestrator with defaults (sequential fallback)
orchestrator = create_simple_orchestrator(
    providers=[alpaca_connector, polygon_connector, yahoo_connector],
    global_timeout=30.0,
    circuit_breaker_threshold=5,
)

# Option 2: Custom configuration (concurrent providers with early winner)
config = OrchestratorConfig(
    global_timeout_seconds=30.0,
    circuit_breaker_failure_threshold=5,
    circuit_breaker_reset_timeout=60,
    circuit_breaker_success_threshold=3,
    max_concurrent_providers=2,  # Race Alpaca vs Polygon, Yahoo as fallback
    enable_detailed_logging=True,
    enable_metrics_collection=True,
)

orchestrator = MultiAPIOrchestrator(
    providers=[alpaca_connector, polygon_connector, yahoo_connector], config=config
)

# Fetch with automatic fallback
input = ConnectorInput(ticker="AAPL")
result = await orchestrator.fetch_with_fallback(input, timeout_seconds=30.0)

# Result includes enhanced metadata with fallback chain details
if result.is_successful:
    print(f"Data from: {result.source_name}")
    print(f"Facts collected: {len(result.facts)}")
    print(f"Execution time: {result.execution_time_ms}ms")
    print(f"Fallback attempts: {result.partial_failure_details}")
else:
    print(f"All providers failed: {result.error_message}")
    print(f"Fallback chain: {result.partial_failure_details}")

# Monitor orchestrator health
metrics = orchestrator.get_orchestrator_metrics()
print(f"Success rate: {metrics['success_rate']:.2%}")
print(f"Fallback activations: {metrics['fallback_activations']}")
print(f"Healthy providers: {metrics['healthy_providers']}/{metrics['total_providers']}")

# Check provider health
health_status = orchestrator.get_provider_health_status()
for provider_name, health in health_status.items():
    print(
        f"{provider_name}: healthy={health.is_healthy}, "
        f"failures={health.consecutive_failures}, "
        f"latency={health.average_latency_ms:.2f}ms, "
        f"circuit={health.circuit_breaker_state}"
    )

# Get circuit breaker status
cb_status = orchestrator.get_circuit_breaker_status()
for provider_name, status in cb_status.items():
    print(
        f"{provider_name}: state={status['state']}, "
        f"failures={status['failure_count']}/{status['failure_threshold']}, "
        f"successes={status['success_count']}/{status['success_threshold']}"
    )
```

**Source**: `C:/Users/kemos/Repos/gauntlet-agents/packages/core/connectors/orchestrator.py` (lines 1-1299)

---

## Processes & Workflows

### Workflow 1: New Market Data Provider Integration

**Trigger Conditions**:

- Adding new market data source (fundamentals, sentiment, alternative data)
- Replacing existing provider due to cost/reliability/coverage
- Implementing custom data connectors for proprietary sources

**Steps**:

1. **Implement DataConnector Protocol**:
   - **Input**: API credentials, provider documentation, timeout requirements
   - **Output**: Fully compliant DataConnector implementation
   - **Rationale**: Ensures consistent error handling, observability, and type safety across all providers

2. **Configure Circuit Breaker Thresholds**:
   - **Input**: Provider SLA, expected failure modes, recovery time requirements
   - **Output**: CircuitBreakerConfig with tuned failure_threshold, reset_timeout, success_threshold
   - **Rationale**: Prevents cascade failures while allowing appropriate recovery windows

3. **Add to Fallback Chain**:
   - **Input**: Provider priority (primary/secondary/tertiary), data coverage, latency requirements
   - **Output**: Updated MultiAPIOrchestrator with ordered provider list
   - **Rationale**: Enables automatic failover and health-based routing

4. **Implement Unit Tests**:
   - **Input**: Provider mock responses, error scenarios, timeout cases
   - **Output**: Test suite covering SUCCESS, NO_DATA, API_ERROR, TIMEOUT_ERROR, RATE_LIMITED paths
   - **Rationale**: Validates protocol compliance and error handling without consuming API quota

5. **Deploy with Health Monitoring**:
   - **Input**: Orchestrator configuration, observability dashboards
   - **Output**: Production deployment with health checks, circuit breaker metrics, fallback chain monitoring
   - **Rationale**: Enables real-time monitoring and automatic degradation

**Success Criteria**:

- ✅ All ConnectorResult responses include execution_time_ms, api_calls, cache_hit metadata
- ✅ No exceptions raised for predictable failures (API errors, timeouts, rate limits)
- ✅ Health check implementation validates credentials without consuming quota
- ✅ Circuit breaker properly records success/failure based on business logic evaluation
- ✅ Fallback chain automatically skips OPEN circuit breakers

**Failure Handling**:

- If protocol compliance fails, consult `packages/core/connectors/protocol.py` for reference implementation
- If circuit breaker not triggering, verify manual `record_success()` and `record_failure()` calls after business logic evaluation
- If fallback chain not activating, check provider ordering via `get_provider_health_status()`

**Example Execution**:

```python
# Step 1: Implement DataConnector Protocol
class CustomDataConnector(DataConnector):
    @property
    def name(self) -> str:
        return "custom_provider"

    @property
    def source_name(self) -> str:
        return "Custom Data Provider"

    @property
    def timeout_seconds(self) -> float:
        return 15.0

    @property
    def enabled(self) -> bool:
        return True

    async def fetch(self, input: ConnectorInput) -> ConnectorResult:
        # Implementation with NEVER raising exceptions for operational failures
        pass

    async def health_check(self) -> bool:
        # Lightweight validation without expensive API calls
        pass


# Step 2: Configure circuit breaker (integrated into orchestrator)

# Step 3: Add to fallback chain
orchestrator = MultiAPIOrchestrator(
    providers=[
        primary_connector,
        custom_data_connector,  # New provider as secondary fallback
        tertiary_connector,
    ],
    config=OrchestratorConfig(
        circuit_breaker_failure_threshold=5,
        circuit_breaker_reset_timeout=60,
    ),
)

# Step 4: Unit tests (see Anti-Patterns section for testing examples)

# Step 5: Deploy with monitoring
result = await orchestrator.fetch_with_fallback(ConnectorInput(ticker="AAPL"))
metrics = orchestrator.get_orchestrator_metrics()
```

---

### Workflow 2: Circuit Breaker Threshold Tuning

**Trigger Conditions**:

- Circuit breaker opening too frequently (false positives during transient failures)
- Circuit breaker not opening fast enough (allowing too many failed requests)
- Provider SLA changes requiring threshold adjustments

**Steps**:

1. **Analyze Current Metrics**:
   - **Input**: Circuit breaker status, provider health history, orchestrator metrics
   - **Output**: Baseline failure rates, average latency, circuit open frequency
   - **Rationale**: Data-driven tuning based on observed behavior

2. **Calculate New Thresholds**:
   - **Input**: Target SLO, acceptable failure rate, recovery time requirements
   - **Output**: Updated CircuitBreakerConfig parameters
   - **Rationale**: Balance between fault tolerance and operational efficiency

3. **Apply Configuration Updates**:
   - **Input**: New CircuitBreakerConfig
   - **Output**: Updated orchestrator configuration
   - **Rationale**: Non-disruptive configuration changes without code deployment

4. **Monitor Impact**:
   - **Input**: Updated metrics after threshold changes
   - **Output**: Validation that circuit behavior matches expectations
   - **Rationale**: Verify tuning effectiveness before production rollout

**Success Criteria**:

- ✅ Circuit breaker opens before cascade failures occur
- ✅ Circuit breaker closes appropriately after recovery period
- ✅ False positive rate (circuit opens during transient failures) <5%
- ✅ Mean time to recovery (MTTR) within SLO requirements

**Failure Handling**:

- If circuit opens too frequently, increase failure_threshold or decrease reset_timeout
- If circuit not opening fast enough, decrease failure_threshold or increase success_threshold
- If circuit not closing after recovery, decrease success_threshold or increase reset_timeout

**Example Execution**:

```python
# Step 1: Analyze current metrics
metrics = orchestrator.get_orchestrator_metrics()
cb_status = orchestrator.get_circuit_breaker_status()

print(f"Circuit breaker trips: {metrics['circuit_breaker_trips']}")
print(f"Circuit breaker skips: {metrics['circuit_breaker_skips']}")
print(f"Success rate: {metrics['success_rate']:.2%}")

for provider_name, status in cb_status.items():
    print(
        f"{provider_name}: state={status['state']}, "
        f"failures={status['failure_count']}/{status['failure_threshold']}"
    )

# Step 2: Calculate new thresholds based on analysis
# Example: Provider has transient failures but recovers quickly
# Current: failure_threshold=5, reset_timeout=60s
# Tuning: Increase failure_threshold to tolerate more transient failures
#         Decrease reset_timeout for faster recovery testing

# Step 3: Apply configuration updates
new_config = OrchestratorConfig(
    circuit_breaker_failure_threshold=8,  # Increased from 5
    circuit_breaker_reset_timeout=45,  # Decreased from 60s
    circuit_breaker_success_threshold=3,  # Unchanged
)

# Recreate orchestrator with new config
orchestrator = MultiAPIOrchestrator(providers=providers, config=new_config)

# Step 4: Monitor impact
# ... collect metrics over 24-48 hours ...
# Compare: circuit_breaker_trips, success_rate, average_latency_ms
```

---

## Decision Trees

### Decision 1: Which Fallback Strategy to Use (Sequential vs Concurrent)

```
IF latency_requirement < 500ms AND provider_latency_variance > 200ms
  THEN use concurrent providers (max_concurrent_providers >= 2)
  BECAUSE early winner pattern reduces tail latency by racing providers

ELSE IF api_quota_constraints = tight OR cost_per_request = high
  THEN use sequential fallback (max_concurrent_providers = 1)
  BECAUSE minimizes API quota consumption and cost

ELSE IF provider_count <= 2
  THEN use sequential fallback
  BECAUSE overhead of concurrent orchestration not justified for small provider sets

ELSE
  THEN use sequential fallback (default)
  BECAUSE simpler failure analysis and more predictable cost
```

**Example Scenarios**:

1. **Scenario**: Real-time trading dashboard requiring <500ms latency, providers average 300-800ms → **Decision**: Concurrent with max_concurrent_providers=3 (race all providers)
2. **Scenario**: Background batch job with tight API quota limits → **Decision**: Sequential fallback to minimize quota usage
3. **Scenario**: Free-tier Yahoo Finance as primary, paid Polygon as fallback → **Decision**: Sequential to avoid unnecessary paid API calls

---

### Decision 2: When to Record Circuit Breaker Failure

```
IF response.status_code IN [500, 502, 503, 504]
  THEN record_failure()
  BECAUSE server-side errors indicate provider health issues

ELSE IF response.status_code = 429
  THEN record_failure()
  BECAUSE rate limiting indicates capacity exhaustion requiring circuit protection

ELSE IF response.status_code = 401 OR response.status_code = 403
  THEN record_failure()
  BECAUSE authentication failures indicate configuration issues requiring investigation

ELSE IF asyncio.TimeoutError raised
  THEN record_failure()
  BECAUSE timeouts indicate provider unavailability or network issues

ELSE IF response.status_code = 404
  THEN record_success()  # Controversial but intentional
  BECAUSE no data found is NOT a provider failure (valid response)

ELSE IF response.status_code = 200 BUT business_logic_validation_fails
  THEN record_failure()
  BECAUSE invalid data structure indicates provider API changes or degradation

ELSE IF response.status_code = 200 AND business_logic_validation_passes
  THEN record_success()
  BECAUSE valid data received as expected

ELSE
  THEN record_failure()  # Conservative default
  BECAUSE unknown status codes should trigger circuit protection
```

**Example Scenarios**:

1. **Scenario**: Alpaca returns HTTP 200 with `{"latest_quote": null}` → **Decision**: record_failure() because quote data is required
2. **Scenario**: Polygon returns HTTP 404 for unknown ticker "INVALID_SYMBOL" → **Decision**: record_success() because this is valid API behavior, not provider failure
3. **Scenario**: Yahoo Finance times out after 10s → **Decision**: record_failure() to protect against continued timeouts

---

## Best Practices

### Practice 1: Manual Success/Failure Recording Based on Business Logic

**Principle**: Circuit breaker success/failure should be determined by business logic evaluation, not just HTTP status codes. HTTP 200 with invalid data = failure. HTTP 404 for unknown ticker = success.

**Implementation**:

- Always call `circuit_breaker.call(async_operation)` to execute through circuit breaker
- **Never rely on automatic success recording** - explicitly evaluate response
- Call `await circuit_breaker.record_success()` after validating business logic requirements
- Call `await circuit_breaker.record_failure(exception)` when business logic validation fails

**Benefits**:

- ✅ Circuit breaker reflects actual provider health (data quality), not just network connectivity
- ✅ Prevents false positives (circuit opens due to business logic failures like unknown tickers)
- ✅ Enables intelligent failover based on provider data quality, not just uptime

**Trade-offs**:

- ⚠️ Requires explicit business logic validation in every connector implementation
- ⚠️ More complex than automatic HTTP-based success/failure determination

**Example**:

```python
async def fetch(self, input: ConnectorInput) -> ConnectorResult:
    """Fetch with business logic-based circuit breaker recording."""

    try:
        # Execute through circuit breaker
        response = await self._circuit_breaker.call(self._call_api, input.ticker)

        # Business logic validation (NOT automatic success)
        if response.status_code == 200:
            data = response.json()

            # Validate data structure and content
            if "latest_quote" in data and data["latest_quote"]["price"] > 0:
                # Valid data - record SUCCESS
                await self._circuit_breaker.record_success()
                return ConnectorResult(
                    status=ConnectorStatus.SUCCESS, facts=[...], ...
                )
            else:
                # Invalid data structure - record FAILURE
                await self._circuit_breaker.record_failure(
                    Exception("Invalid quote data structure")
                )
                return ConnectorResult(
                    status=ConnectorStatus.API_ERROR, facts=[], ...
                )

        elif response.status_code == 404:
            # No data found for ticker - record SUCCESS (valid API behavior)
            await self._circuit_breaker.record_success()
            return ConnectorResult(status=ConnectorStatus.NO_DATA, facts=[], ...)

        else:
            # API error - record FAILURE
            await self._circuit_breaker.record_failure(
                Exception(f"HTTP {response.status_code}")
            )
            return ConnectorResult(status=ConnectorStatus.API_ERROR, facts=[], ...)

    except asyncio.TimeoutError:
        # Timeout - record FAILURE
        await self._circuit_breaker.record_failure(TimeoutError("API timeout"))
        return ConnectorResult(status=ConnectorStatus.TIMEOUT_ERROR, facts=[], ...)
```

---

### Practice 2: Comprehensive Observability Metadata in Every ConnectorResult

**Principle**: Every ConnectorResult must include execution_time_ms, api_calls, cache_hit metadata to enable performance monitoring, quota tracking, and cache effectiveness analysis.

**Implementation**:

- Track execution time using `time.monotonic()` at start/end of fetch operation
- Count API calls made during fetch operation (including retries)
- Set cache_hit=True when serving from cache, cache_hit=False when fetching fresh data
- Include confidence_note explaining data source and quality assessment
- Populate partial_failure_details for partial success scenarios

**Benefits**:

- ✅ Enables real-time performance monitoring and alerting on slow providers
- ✅ Tracks API quota consumption for cost optimization
- ✅ Measures cache effectiveness for performance tuning
- ✅ Provides debugging context for failure analysis

**Trade-offs**:

- ⚠️ Minimal overhead (~50 bytes per result for metadata)
- ⚠️ Requires discipline to populate all fields consistently

**Example**:

```python
async def fetch(self, input: ConnectorInput) -> ConnectorResult:
    """Fetch with comprehensive observability metadata."""
    start_time = time.monotonic()
    api_calls_made = 0

    try:
        # Make API call
        response = await self._call_api(input.ticker)
        api_calls_made += 1

        # Check cache (hypothetical cache layer)
        if response.headers.get("X-Cache") == "HIT":
            cache_hit = True
        else:
            cache_hit = False

        # Calculate execution time
        execution_time_ms = (time.monotonic() - start_time) * 1000

        # Parse data
        data = response.json()
        facts = [
            Fact(
                category="market_data",
                key="current_price",
                value=data["price"],
                confidence=0.95,
                source=self.source_name,
            )
        ]

        return ConnectorResult(
            status=ConnectorStatus.SUCCESS,
            facts=facts,
            source_name=self.source_name,
            # Comprehensive observability metadata
            execution_time_ms=execution_time_ms,
            api_calls=api_calls_made,
            cache_hit=cache_hit,
            confidence_note=f"Real-time quote from {self.source_name} API",
            timestamp=datetime.now(timezone.utc),
        )

    except asyncio.TimeoutError:
        execution_time_ms = (time.monotonic() - start_time) * 1000
        return ConnectorResult(
            status=ConnectorStatus.TIMEOUT_ERROR,
            facts=[],
            error_message=f"Timeout after {self.timeout_seconds}s",
            source_name=self.source_name,
            execution_time_ms=execution_time_ms,
            api_calls=api_calls_made,
            cache_hit=False,
        )
```

---

## Anti-Patterns

### Anti-Pattern 1: Raising Exceptions for Predictable Failures

**Problem**: Raising exceptions for API errors, timeouts, rate limits violates DataConnector Protocol and breaks fallback chains.

**Detection**:

- 🔴 Code contains `raise HTTPError(...)` or `raise TimeoutError(...)` in fetch() method
- 🔴 Unit tests expect exceptions for API failures instead of ConnectorResult with error status
- 🔴 Orchestrator logs show "Unexpected error" for common failure modes

**Consequences**:

- ❌ Fallback chain breaks because exceptions are not caught by orchestrator
- ❌ Circuit breaker cannot distinguish between operational failures and programming errors
- ❌ Observability metrics incomplete because execution_time_ms not populated on exception path

**Better Approach**:

```python
✅ Preferred Pattern:
async def fetch(self, input: ConnectorInput) -> ConnectorResult:
    """NEVER raise exceptions for operational failures."""
    start_time = time.monotonic()

    try:
        response = await self._call_api(input.ticker)

        # API error - return status, DO NOT raise exception
        if response.status_code >= 400:
            elapsed_ms = (time.monotonic() - start_time) * 1000
            return ConnectorResult(
                status=ConnectorStatus.API_ERROR,
                facts=[],
                error_message=f"HTTP {response.status_code}",
                source_name=self.source_name,
                execution_time_ms=elapsed_ms,
                api_calls=1,
            )

        # Success case
        return ConnectorResult(status=ConnectorStatus.SUCCESS, facts=[...], ...)

    except asyncio.TimeoutError:
        # Timeout - return status, DO NOT raise exception
        elapsed_ms = (time.monotonic() - start_time) * 1000
        return ConnectorResult(
            status=ConnectorStatus.TIMEOUT_ERROR,
            facts=[],
            error_message="Timeout",
            source_name=self.source_name,
            execution_time_ms=elapsed_ms,
            api_calls=1,
        )


❌ Anti-Pattern:
async def fetch(self, input: ConnectorInput) -> ConnectorResult:
    """WRONG - raises exceptions for operational failures."""
    response = await self._call_api(input.ticker)

    # WRONG - raises exception instead of returning ConnectorResult
    if response.status_code >= 400:
        raise HTTPError(f"API error: {response.status_code}")

    # WRONG - timeout exception propagates instead of being caught
    # No try/except around asyncio.timeout() call
```

**Migration Strategy**:

1. Audit all DataConnector implementations for `raise` statements in fetch() method
2. Replace exception raising with ConnectorResult returns using appropriate ConnectorStatus
3. Add try/except blocks to catch asyncio.TimeoutError and return TIMEOUT_ERROR status
4. Update unit tests to assert ConnectorResult.status instead of expecting exceptions

---

### Anti-Pattern 2: Skipping Circuit Breaker for "Simple" API Calls

**Problem**: Implementing DataConnector without circuit breaker protection because "this provider is reliable" or "it's just one API call" leads to cascade failures.

**Detection**:

- 🔴 DataConnector implementation calls provider API directly without AsyncCircuitBreaker.call()
- 🔴 No circuit breaker instance created for external dependency
- 🔴 Manual success/failure recording missing

**Consequences**:

- ❌ Single provider failure causes repeated timeouts without automatic degradation
- ❌ Fallback chain cannot skip unhealthy providers because circuit state unknown
- ❌ No automatic recovery testing (half-open state) after provider comes back online

**Better Approach**:

```python
✅ Preferred Pattern:
class MarketDataConnector:
    """ALL external API calls protected by circuit breaker."""

    def __init__(self, api_key: str, logger):
        self._api_key = api_key

        # Circuit breaker for ALL external dependencies
        cb_config = CircuitBreakerConfig(
            failure_threshold=5, reset_timeout=60, success_threshold=3
        )
        self._circuit_breaker = AsyncCircuitBreaker(
            name=f"{self.__class__.__name__}_api", config=cb_config, logger=logger
        )

    async def fetch(self, input: ConnectorInput) -> ConnectorResult:
        """Fetch with circuit breaker protection."""

        # Check circuit state before calling
        if self._circuit_breaker.is_open and not self._circuit_breaker.is_half_open:
            return ConnectorResult(
                status=ConnectorStatus.API_ERROR,
                facts=[],
                error_message="Circuit breaker open",
                source_name=self.source_name,
                execution_time_ms=0,
                api_calls=0,
            )

        try:
            # Execute through circuit breaker
            response = await self._circuit_breaker.call(self._call_api, input.ticker)

            # Evaluate business logic and record success/failure
            if response.status_code == 200:
                await self._circuit_breaker.record_success()
                return ConnectorResult(status=ConnectorStatus.SUCCESS, facts=[...], ...)
            else:
                await self._circuit_breaker.record_failure(
                    Exception(f"HTTP {response.status_code}")
                )
                return ConnectorResult(
                    status=ConnectorStatus.API_ERROR, facts=[], ...
                )

        except Exception as e:
            await self._circuit_breaker.record_failure(e)
            return ConnectorResult(status=ConnectorStatus.API_ERROR, facts=[], ...)


❌ Anti-Pattern:
class MarketDataConnector:
    """WRONG - no circuit breaker protection."""

    async def fetch(self, input: ConnectorInput) -> ConnectorResult:
        """Direct API call without circuit breaker - WRONG."""

        # WRONG - direct API call without circuit breaker
        response = await self._call_api(input.ticker)

        # No automatic failure tracking or degradation
        if response.status_code == 200:
            return ConnectorResult(status=ConnectorStatus.SUCCESS, facts=[...], ...)
        else:
            return ConnectorResult(status=ConnectorStatus.API_ERROR, facts=[], ...)
```

**Migration Strategy**:

1. Identify all DataConnector implementations without circuit breaker protection
2. Add AsyncCircuitBreaker instance to `__init__()` method with appropriate configuration
3. Wrap all external API calls with `circuit_breaker.call(async_operation)`
4. Add manual success/failure recording based on business logic evaluation
5. Add circuit breaker state check before API calls to skip when OPEN

---

### Anti-Pattern 3: Treating NO_DATA as API_ERROR

**Problem**: Returning ConnectorStatus.API_ERROR when no data found for valid ticker query instead of ConnectorStatus.NO_DATA. This causes circuit breaker to open for valid API behavior.

**Detection**:

- 🔴 Circuit breaker opens frequently during off-market hours when no quotes available
- 🔴 HTTP 404 responses trigger circuit breaker failures
- 🔴 Unknown tickers cause provider to be marked unhealthy

**Consequences**:

- ❌ Circuit breaker false positives (opens for valid API responses)
- ❌ Fallback chain activates unnecessarily (wastes API quota)
- ❌ Provider health metrics inaccurate (legitimate no-data scenarios counted as failures)

**Better Approach**:

```python
✅ Preferred Pattern:
async def fetch(self, input: ConnectorInput) -> ConnectorResult:
    """Distinguish between API errors and no data found."""

    try:
        response = await self._circuit_breaker.call(self._call_api, input.ticker)

        if response.status_code == 404:
            # No data found - record SUCCESS (valid API behavior)
            await self._circuit_breaker.record_success()
            return ConnectorResult(
                status=ConnectorStatus.NO_DATA,  # NOT API_ERROR
                facts=[],
                error_message=f"No data found for ticker {input.ticker}",
                source_name=self.source_name,
                execution_time_ms=elapsed_ms,
                api_calls=1,
            )

        elif response.status_code == 200:
            data = response.json()

            # Check for empty result (valid API response)
            if not data or len(data.get("quotes", [])) == 0:
                # Empty result - record SUCCESS (valid API behavior)
                await self._circuit_breaker.record_success()
                return ConnectorResult(
                    status=ConnectorStatus.NO_DATA,  # NOT API_ERROR
                    facts=[],
                    error_message=f"No quotes available for {input.ticker}",
                    source_name=self.source_name,
                    execution_time_ms=elapsed_ms,
                    api_calls=1,
                )

            # Valid data - record SUCCESS
            await self._circuit_breaker.record_success()
            return ConnectorResult(status=ConnectorStatus.SUCCESS, facts=[...], ...)

        else:
            # Actual API error - record FAILURE
            await self._circuit_breaker.record_failure(
                Exception(f"HTTP {response.status_code}")
            )
            return ConnectorResult(
                status=ConnectorStatus.API_ERROR, facts=[], ...
            )

    except Exception as e:
        # Unexpected error - record FAILURE
        await self._circuit_breaker.record_failure(e)
        return ConnectorResult(status=ConnectorStatus.API_ERROR, facts=[], ...)


❌ Anti-Pattern:
async def fetch(self, input: ConnectorInput) -> ConnectorResult:
    """WRONG - treats NO_DATA as API_ERROR."""

    response = await self._call_api(input.ticker)

    # WRONG - treats 404 as API error instead of NO_DATA
    if response.status_code == 404:
        await self._circuit_breaker.record_failure(
            Exception("404 Not Found")
        )  # WRONG
        return ConnectorResult(
            status=ConnectorStatus.API_ERROR,  # Should be NO_DATA
            facts=[],
            error_message="API error: 404",
            source_name=self.source_name,
            execution_time_ms=elapsed_ms,
            api_calls=1,
        )
```

**Migration Strategy**:

1. Audit all DataConnector implementations for HTTP 404 handling
2. Replace ConnectorStatus.API_ERROR with ConnectorStatus.NO_DATA for legitimate no-data scenarios
3. Update circuit breaker recording: `record_success()` for NO_DATA cases (valid API behavior)
4. Add business logic checks for empty result sets (e.g., `len(data.get("quotes", [])) == 0`)
5. Update unit tests to verify NO_DATA status for unknown tickers and empty results

---

## Integration Points

### Integration 1: DataConnector Protocol → MultiAPIOrchestrator

**Relationship**: All DataConnector implementations are consumed by MultiAPIOrchestrator for fallback chain orchestration with circuit breaker integration.

**Coordination Pattern**:

- DataConnector implements protocol interface (name, source_name, timeout_seconds, enabled, fetch, health_check)
- MultiAPIOrchestrator wraps each DataConnector with AsyncCircuitBreaker instance
- Orchestrator routes requests to healthy providers first via `_get_ordered_providers()`
- Orchestrator skips providers with OPEN circuit breakers automatically
- Orchestrator enhances ConnectorResult with fallback chain metadata

**Example Usage**:

```python
# DataConnector implementation
class AlpacaConnector(DataConnector):
    @property
    def name(self) -> str:
        return "alpaca_quote"

    @property
    def timeout_seconds(self) -> float:
        return 10.0

    async def fetch(self, input: ConnectorInput) -> ConnectorResult:
        # Implementation following protocol
        pass


# MultiAPIOrchestrator consumption
orchestrator = MultiAPIOrchestrator(
    providers=[AlpacaConnector(), PolygonConnector(), YahooConnector()],
    config=OrchestratorConfig(circuit_breaker_failure_threshold=5),
)

# Orchestrator automatically:
# 1. Creates circuit breaker for each provider
# 2. Routes to healthy providers first
# 3. Skips OPEN circuit breakers
# 4. Enhances results with fallback metadata
result = await orchestrator.fetch_with_fallback(ConnectorInput(ticker="AAPL"))
```

**Dependencies**:

- DataConnector depends on: packages.core.connectors.protocol.DataConnector protocol interface
- MultiAPIOrchestrator depends on: DataConnector implementations, AsyncCircuitBreaker, ConnectorInput/ConnectorResult models

---

### Integration 2: AsyncCircuitBreaker → DataConnector Implementations

**Relationship**: Every DataConnector implementation should integrate AsyncCircuitBreaker for automatic failure tracking and degradation.

**Coordination Pattern**:

- DataConnector creates AsyncCircuitBreaker instance in `__init__()` with CircuitBreakerConfig
- DataConnector wraps API calls with `circuit_breaker.call(async_operation)`
- DataConnector manually records success/failure based on business logic evaluation
- Circuit breaker state influences fetch() behavior (skip when OPEN)

**Example Usage**:

```python
class PolygonConnector(DataConnector):
    """Polygon connector with integrated circuit breaker."""

    def __init__(self, api_key: str, logger):
        self._api_key = api_key

        # Integrate circuit breaker
        cb_config = CircuitBreakerConfig(
            failure_threshold=5, reset_timeout=60, success_threshold=3
        )
        self._circuit_breaker = AsyncCircuitBreaker(
            name="polygon_api", config=cb_config, logger=logger
        )

    async def fetch(self, input: ConnectorInput) -> ConnectorResult:
        """Fetch with circuit breaker integration."""

        # Check circuit state before calling
        if self._circuit_breaker.is_open and not self._circuit_breaker.is_half_open:
            return ConnectorResult(
                status=ConnectorStatus.API_ERROR,
                facts=[],
                error_message="Circuit breaker open",
                source_name=self.source_name,
                execution_time_ms=0,
                api_calls=0,
            )

        try:
            # Execute through circuit breaker
            response = await self._circuit_breaker.call(self._call_polygon_api, input.ticker)

            # Business logic evaluation
            if response.status_code == 200 and valid_data(response.json()):
                await self._circuit_breaker.record_success()
                return ConnectorResult(status=ConnectorStatus.SUCCESS, facts=[...], ...)
            else:
                await self._circuit_breaker.record_failure(Exception("Invalid data"))
                return ConnectorResult(status=ConnectorStatus.API_ERROR, facts=[], ...)

        except Exception as e:
            await self._circuit_breaker.record_failure(e)
            return ConnectorResult(status=ConnectorStatus.API_ERROR, facts=[], ...)
```

**Dependencies**:

- AsyncCircuitBreaker depends on: pybreaker library, CircuitBreakerConfig, AsyncCircuitBreakerListener
- DataConnector depends on: AsyncCircuitBreaker for fault tolerance

---

## Validation & Quality Checks

### Check 1: DataConnector Protocol Compliance

**What to Validate**: All DataConnector implementations comply with protocol requirements and ADR-004 standards.

**Validation Method**:

1. Verify all required properties implemented: `name`, `source_name`, `timeout_seconds`, `enabled`
2. Verify fetch() method signature matches protocol: `async def fetch(self, input: ConnectorInput) -> ConnectorResult`
3. Verify health_check() implemented: `async def health_check(self) -> bool`
4. Verify fetch() NEVER raises exceptions for operational failures (only programming errors)
5. Verify ConnectorResult includes observability metadata: `execution_time_ms`, `api_calls`, `cache_hit`

**Pass Criteria**: All protocol requirements satisfied, no exceptions for operational failures, comprehensive observability metadata

**Fail Criteria**: Missing required properties, fetch() raises exceptions for API errors/timeouts, missing observability metadata

**Remediation**:

```python
# Example unit test for protocol compliance
import pytest
from packages.core.connectors.protocol import DataConnector, ConnectorInput, ConnectorResult


@pytest.mark.asyncio
async def test_connector_protocol_compliance(connector: DataConnector):
    """Validate DataConnector protocol compliance."""

    # Check required properties
    assert hasattr(connector, "name")
    assert hasattr(connector, "source_name")
    assert hasattr(connector, "timeout_seconds")
    assert hasattr(connector, "enabled")
    assert connector.timeout_seconds > 0

    # Check fetch() signature
    assert callable(connector.fetch)
    input = ConnectorInput(ticker="AAPL")
    result = await connector.fetch(input)

    # Check ConnectorResult compliance
    assert isinstance(result, ConnectorResult)
    assert hasattr(result, "status")
    assert hasattr(result, "facts")
    assert hasattr(result, "execution_time_ms")
    assert hasattr(result, "api_calls")
    assert hasattr(result, "cache_hit")
    assert result.execution_time_ms >= 0
    assert result.api_calls >= 0

    # Check health_check() signature
    assert callable(connector.health_check)
    health_result = await connector.health_check()
    assert isinstance(health_result, bool)


@pytest.mark.asyncio
async def test_connector_never_raises_exceptions_for_operational_failures(
    connector: DataConnector,
):
    """Verify fetch() returns ConnectorResult for all failure modes."""

    # Test timeout scenario (should return TIMEOUT_ERROR status, not raise exception)
    input = ConnectorInput(ticker="AAPL", params={"force_timeout": True})
    result = await connector.fetch(input)
    assert isinstance(result, ConnectorResult)
    # Timeout should return TIMEOUT_ERROR status, not raise exception

    # Test API error scenario (should return API_ERROR status, not raise exception)
    input = ConnectorInput(ticker="AAPL", params={"force_error": True})
    result = await connector.fetch(input)
    assert isinstance(result, ConnectorResult)
    # API error should return API_ERROR status, not raise exception
```

---

### Check 2: Circuit Breaker Integration Validation

**What to Validate**: DataConnector implementations properly integrate AsyncCircuitBreaker with manual success/failure recording.

**Validation Method**:

1. Verify AsyncCircuitBreaker instance created in `__init__()` with CircuitBreakerConfig
2. Verify all external API calls wrapped with `circuit_breaker.call(async_operation)`
3. Verify manual `record_success()` called after business logic validation passes
4. Verify manual `record_failure()` called when business logic validation fails OR operational failures occur
5. Verify circuit breaker state checked before API calls (skip when OPEN)

**Pass Criteria**: Circuit breaker properly tracks failures, opens after threshold, skips calls when OPEN, records success/failure based on business logic

**Fail Criteria**: No circuit breaker integration, automatic success/failure recording, circuit state not checked before calls

**Remediation**:

```python
# Example unit test for circuit breaker integration
import pytest
from packages.core.connectors.protocol import ConnectorInput, ConnectorStatus


@pytest.mark.asyncio
async def test_circuit_breaker_opens_after_threshold(connector_with_circuit_breaker):
    """Verify circuit breaker opens after failure threshold."""

    # Trigger failures to open circuit breaker
    for i in range(6):  # failure_threshold = 5
        input = ConnectorInput(ticker="AAPL", params={"force_error": True})
        result = await connector_with_circuit_breaker.fetch(input)
        assert result.status == ConnectorStatus.API_ERROR

    # Verify circuit breaker is OPEN
    assert connector_with_circuit_breaker._circuit_breaker.is_open

    # Next call should be skipped (circuit OPEN)
    input = ConnectorInput(ticker="AAPL")
    result = await connector_with_circuit_breaker.fetch(input)
    assert result.error_message == "Circuit breaker open"
    assert result.api_calls == 0  # No API call made


@pytest.mark.asyncio
async def test_circuit_breaker_manual_recording(connector_with_circuit_breaker):
    """Verify manual success/failure recording based on business logic."""

    # Success case - valid data
    input = ConnectorInput(ticker="AAPL")
    result = await connector_with_circuit_breaker.fetch(input)
    assert result.status == ConnectorStatus.SUCCESS

    # Verify success recorded (circuit breaker success counter incremented)
    assert connector_with_circuit_breaker._circuit_breaker.success_counter > 0

    # Failure case - invalid data (HTTP 200 but business logic fails)
    input = ConnectorInput(ticker="AAPL", params={"invalid_data": True})
    result = await connector_with_circuit_breaker.fetch(input)
    assert result.status == ConnectorStatus.API_ERROR

    # Verify failure recorded (circuit breaker failure counter incremented)
    assert connector_with_circuit_breaker._circuit_breaker.fail_counter > 0
```

---

## Common Pitfalls & Solutions

| Pitfall                                                             | Detection                                                                                               | Solution                                                                                                     |
| ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| Raising exceptions for API errors/timeouts                          | Unit tests fail with unhandled exceptions, fallback chain breaks                                        | Return ConnectorResult with appropriate status (API_ERROR, TIMEOUT_ERROR), never raise for operational failures |
| Treating NO_DATA as API_ERROR                                       | Circuit breaker opens during off-market hours, false positive failures                                  | Return ConnectorStatus.NO_DATA for legitimate no-data scenarios, record_success() for valid API responses    |
| Skipping circuit breaker for "simple" API calls                     | Repeated timeouts without degradation, fallback chain cannot skip unhealthy providers                   | Integrate AsyncCircuitBreaker for ALL external dependencies, check circuit state before calls               |
| Automatic success/failure recording (not based on business logic)   | Circuit opens for valid API responses (e.g., HTTP 404), invalid data counted as success                | Manually record success/failure after business logic evaluation, validate data structure/content            |
| Missing observability metadata in ConnectorResult                   | Cannot measure performance, quota usage, cache effectiveness                                            | Populate execution_time_ms, api_calls, cache_hit for every result (including failures)                      |
| Sequential fallback when concurrent would reduce latency            | High tail latency, slow response times                                                                  | Use max_concurrent_providers >= 2 for early winner pattern when latency requirements tight                  |
| Concurrent providers when quota constraints tight                   | Excessive API quota consumption, high cost                                                              | Use max_concurrent_providers = 1 for sequential fallback to minimize quota usage                            |
| Not implementing health_check() method                              | Cannot validate credentials/configuration without consuming quota, missing pre-flight validation        | Implement lightweight health_check() without expensive API calls                                             |
| Global timeout too short for provider chain                         | TimeoutError before fallback chain exhausted                                                            | Set global_timeout_seconds >= sum(provider.timeout_seconds) for sequential fallback                        |
| Circuit breaker thresholds not tuned for provider SLA               | Too many false positives (circuit opens during transient failures) or too slow to detect failures      | Analyze metrics, tune failure_threshold/reset_timeout/success_threshold based on observed behavior          |

---

## Tools & Resources

### Recommended Tools

1. **AsyncCircuitBreaker**
   - **Purpose**: Fault tolerance and automatic degradation for external API integrations
   - **When to Use**: ALL external API calls in DataConnector implementations
   - **Documentation**: `C:/Users/kemos/Repos/gauntlet-agents/packages/core/resilience/async_circuit_breaker.py`

2. **MultiAPIOrchestrator**
   - **Purpose**: Multi-provider fallback chain orchestration with circuit breaker integration
   - **When to Use**: Market data integrations requiring automatic failover across multiple providers
   - **Documentation**: `C:/Users/kemos/Repos/gauntlet-agents/packages/core/connectors/orchestrator.py`

3. **DataConnector Protocol**
   - **Purpose**: Standardized interface for all external data ingestion with consistent error handling
   - **When to Use**: ALL new market data provider integrations
   - **Documentation**: `C:/Users/kemos/Repos/gauntlet-agents/packages/core/connectors/protocol.py`

### Learning Resources

1. **ADR-004: The DataConnector Protocol**: Internal documentation (not URL)
   - **Topic**: DataConnector Protocol architecture, versioning, cross-cutting concerns
   - **Quality**: High

2. **ADR-002: Multi-API Fallback Strategy**: Internal documentation (not URL)
   - **Topic**: Fallback chain orchestration patterns, health-based routing
   - **Quality**: High

3. **ADR-003: Resilient Data Provider**: Internal documentation (not URL)
   - **Topic**: Circuit breaker patterns, fault tolerance, cascade failure prevention
   - **Quality**: High

---

## Glossary

- **DataConnector Protocol**: Unified interface for all external data ingestion with standardized error handling, observability, and type safety following ADR-004
- **Circuit Breaker**: Fault tolerance mechanism that tracks failures, opens circuit after threshold, provides recovery period, and gradually tests if service recovered
- **ConnectorStatus**: Standardized status enum (SUCCESS, PARTIAL_SUCCESS, NO_DATA, API_ERROR, TIMEOUT_ERROR, RATE_LIMITED, CONFIG_ERROR) for consistent error handling
- **ConnectorResult**: Enhanced output model with facts, status, error message, and comprehensive observability metadata (execution_time_ms, api_calls, cache_hit)
- **Multi-Provider Fallback Chain**: Sequential or concurrent orchestration pattern across multiple market data providers (Alpaca → Polygon → Yahoo) with automatic failover
- **Early Winner Pattern**: Concurrent provider racing where first successful result returned, remaining tasks cancelled (reduces tail latency)
- **Health-Based Routing**: Provider ordering based on health status (is_healthy, consecutive_failures, circuit_breaker_state) with healthy providers prioritized
- **Manual Success/Failure Recording**: Explicit circuit breaker recording based on business logic evaluation (not automatic HTTP status codes)
- **Global Timeout**: Maximum total execution time across all providers to maintain SLO requirements and prevent cascade failures

---

## Sources & References

1. DataConnector Protocol Implementation: `C:/Users/kemos/Repos/gauntlet-agents/packages/core/connectors/protocol.py`
   - Accessed: 2025-11-14
   - Confidence: 0.95
   - Pattern: DataConnector interface, ConnectorInput/ConnectorResult models, ConnectorStatus enum

2. AsyncCircuitBreaker Implementation: `C:/Users/kemos/Repos/gauntlet-agents/packages/core/resilience/async_circuit_breaker.py`
   - Accessed: 2025-11-14
   - Confidence: 0.95
   - Pattern: Circuit breaker configuration, manual success/failure recording, state management

3. MultiAPIOrchestrator Implementation: `C:/Users/kemos/Repos/gauntlet-agents/packages/core/connectors/orchestrator.py`
   - Accessed: 2025-11-14
   - Confidence: 0.95
   - Pattern: Fallback chain orchestration, health-based routing, early winner pattern, global timeout protection

---

## Changelog

- **2025-11-14**: Initial documentation created (confidence: 0.95)
  - Extracted from production codebase patterns (protocol.py, async_circuit_breaker.py, orchestrator.py)
  - Documented DataConnector Protocol compliance, circuit breaker integration, multi-provider fallback chains
  - Added workflows for new provider integration and circuit breaker tuning
  - Documented anti-patterns, best practices, integration points, validation checks

---

## Related Documentation

- ADR-004: The DataConnector Protocol (internal documentation)
- ADR-002: Multi-API Fallback Strategy (internal documentation)
- ADR-003: Resilient Data Provider (internal documentation)
- `.claude/docs/guides/market-data-specialist/domain-knowledge.md` (if exists - domain-specific market data concepts)
- `.claude/docs/guides/market-data-specialist/testing-patterns.md` (if exists - testing strategies for connectors)
