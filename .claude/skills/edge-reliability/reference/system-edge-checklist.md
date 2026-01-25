# System Edge Reliability Checklist

**Source**: `.claude/docs/01-guides/review/system-edge-reliability.md`

## Temporal Edge (Dynamics & Latency)

### TE-001: Timeout Budget
- **Check**: Every cross-component call has timeout < upstream timeout
- **Severity**: HIGH
- **Evidence**: Look for `timeout=`, `httpx.Timeout`, `asyncio.wait_for`
- **Pass**: Explicit timeout configured, value < caller's timeout
- **Fail**: No timeout, or timeout >= upstream timeout

### TE-002: Race Condition Guards
- **Check**: Concurrent access to shared state is protected
- **Severity**: CRITICAL
- **Evidence**: Look for locks, atomic operations, event ordering
- **Pass**: Threading primitives or async coordination present
- **Fail**: Shared mutable state without synchronization

### TE-003: Backpressure Handling
- **Check**: Flow control mechanism exists for high-load scenarios
- **Severity**: MEDIUM
- **Evidence**: Queue limits, rate limiters, circuit breakers
- **Pass**: Explicit backpressure mechanism documented
- **Fail**: Unbounded buffering, no flow control

## Semantic Edge (Contracts & Compatibility)

### SE-001: Schema Evolution
- **Check**: Unknown fields are handled gracefully
- **Severity**: HIGH
- **Evidence**: Pydantic `extra='ignore'`, version fields
- **Pass**: Forward/backward compatibility strategy present
- **Fail**: Strict parsing that breaks on new fields

### SE-002: Idempotency
- **Check**: Retries don't cause duplicate side effects
- **Severity**: HIGH
- **Evidence**: Deduplication keys, idempotency tokens
- **Pass**: At-least-once delivery is safe
- **Fail**: Duplicate messages cause duplicate effects

## Failure Propagation Edge (Blast Radius)

### FP-001: Retry Strategy
- **Check**: Exponential backoff with jitter
- **Severity**: MEDIUM
- **Evidence**: `tenacity`, custom retry logic
- **Pass**: Backoff multiplier + randomization present
- **Fail**: Fixed delays or immediate retries

### FP-002: Bulkheading
- **Check**: Downstream failures don't exhaust resources
- **Severity**: HIGH
- **Evidence**: Thread pool isolation, connection limits
- **Pass**: Separate pools per downstream
- **Fail**: Shared pool, no isolation

### FP-003: Graceful Degradation
- **Check**: Default fallback when edges fail
- **Severity**: MEDIUM
- **Evidence**: Try/except with fallback, feature flags
- **Pass**: Degraded mode returns sensible default
- **Fail**: Failure propagates without mitigation
