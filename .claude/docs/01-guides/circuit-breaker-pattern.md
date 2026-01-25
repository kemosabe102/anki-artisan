---
title: "Circuit Breaker Pattern"
date: 2025-11-08
status: ACTIVE
tags: [claude-docs]
---
# Circuit Breaker Pattern

**Purpose**: Prevent cascading failures through automatic failure detection, fail-fast behavior, and self-healing recovery mechanisms

**Audience**: All agents performing external operations (network requests, file I/O, service calls), sub-agent developers

**Referenced by**: deployment-release, researcher-external, development, source-control

## Overview

**What is a Circuit Breaker?**
A circuit breaker monitors operation failures and automatically "trips" (opens) to prevent further attempts when failure threshold exceeded, allowing failing service time to recover.

**Why Use Circuit Breakers?**

- **Prevent cascading failures**: Stop calling failing services before they bring down entire system
- **Fast failure feedback**: Fail immediately instead of waiting for timeout
- **Automatic recovery**: Self-heal by periodically testing if service recovered
- **Resource protection**: Prevent thread pool exhaustion from blocked calls

**When to Use**:

- External API calls (WebFetch, researcher-external)
- Kubernetes operations (kubectl, deployment-release)
- File system operations with high failure rates
- Database connections
- MCP server calls

---

## Three-State Pattern

Circuit breaker operates in 3 states with automatic transitions:

### CLOSED State (Normal Operation)

**Behavior**: All requests pass through normally

- Monitor failure rate for each operation
- Count consecutive failures
- Track success/failure ratio

**Transition to OPEN**:

```
IF (failure_rate > 50% AND call_count >= 10)
OR (consecutive_failures >= 5)
THEN transition to OPEN state
```

**Example**:

```
10 requests to WebFetch:
  - 6 failures (503 Service Unavailable)
  - 4 successes
  - Failure rate: 60% > 50% threshold
  - Call count: 10 >= minimum calls
→ Transition to OPEN state
```

---

### OPEN State (Fail-Fast)

**Behavior**: All requests fail immediately without attempting operation

- Return cached response if available
- Return degraded functionality response
- Log circuit breaker trip event

**Purpose**: Give failing service time to recover without overwhelming it

**Transition to HALF-OPEN**:

```
AFTER 60 seconds in OPEN state
THEN transition to HALF-OPEN state
```

**Example**:

```
Circuit breaker OPEN for WebFetch to "api.example.com":
  - All requests fail immediately with CircuitBreakerOpenError
  - Return cached documentation if available
  - After 60 seconds → transition to HALF-OPEN
```

---

### HALF-OPEN State (Recovery Testing)

**Behavior**: Allow limited number of test requests to check service recovery

- Permit exactly 10 test requests
- Monitor success rate of test requests
- Decide whether to fully recover or trip again

**Transition from HALF-OPEN**:

```
IF (test_success_rate >= 80% AND test_count >= 10)
THEN transition to CLOSED (service recovered)

ELSE IF (test_failure_rate > 20%)
THEN transition back to OPEN (service still failing)
```

**Example**:

```
Circuit breaker HALF-OPEN for kubectl operations:
  - Allow 10 test kubectl get pods commands
  - 9 successes, 1 failure
  - Success rate: 90% >= 80% threshold
→ Transition to CLOSED (service recovered)

Alternative scenario:
  - 3 successes, 7 failures
  - Failure rate: 70% > 20% threshold
→ Transition back to OPEN (service still failing)
```

---

## Default Configuration

**Failure Rate Threshold**: 50%

- Rationale: Balance between sensitivity and false positives
- Industry standard (Resilience4j, Hystrix)
- Adjust higher (60-70%) for flaky services

**Minimum Calls**: 10

- Rationale: Need sufficient sample size to determine failure rate
- Prevents premature tripping on single failures
- Adjust lower (5) for critical operations, higher (20-100) for high-volume

**Wait Duration in OPEN**: 60 seconds

- Rationale: Allow service recovery time without excessive delay
- Typical service restart time: 30-90 seconds
- Adjust based on service recovery patterns

**Permitted Calls in HALF-OPEN**: 10

- Rationale: Sufficient sample to determine recovery
- Not too many to overwhelm recovering service
- Industry standard (Resilience4j)

**State Transition Summary**:

```
CLOSED → OPEN:
  - failure_rate > 50% AND call_count >= 10
  OR consecutive_failures >= 5

OPEN → HALF-OPEN:
  - After 60 seconds in OPEN state

HALF-OPEN → CLOSED:
  - test_success_rate >= 80% AND test_count >= 10

HALF-OPEN → OPEN:
  - test_failure_rate > 20%
```

---

## Failure Detection Logic

### Per-Operation Tracking

**Track separately for each unique operation**:

- WebFetch: Per domain (api.example.com, docs.python.org)
- kubectl: Per cluster + namespace (local-cluster/default)
- File operations: Per directory (.claude/agents/, packages/core/)

**Why Per-Operation?**: Failure in one service shouldn't affect unrelated services

**Example**:

```python
circuit_breakers = {
    "webfetch:api.example.com": CircuitBreaker(
        failure_threshold=0.5,
        min_calls=10,
        wait_duration=60
    ),
    "kubectl:local-cluster:default": CircuitBreaker(...),
    "file_ops:.claude/agents": CircuitBreaker(...)
}
```

---

### Consecutive Failures Tracking

**Purpose**: Detect rapid failure patterns even with low call volume

**Logic**:

```python
consecutive_failures = 0

def record_failure(operation):
    global consecutive_failures
    consecutive_failures += 1

    if consecutive_failures >= 5:
        trip_circuit_breaker(operation)

def record_success(operation):
    global consecutive_failures
    consecutive_failures = 0  # Reset on any success
```

**Example**:

```
Scenario: Low-volume operation (2-3 calls/minute)
  - Call 1: Failure (timeout)
  - Call 2: Failure (timeout)
  - Call 3: Failure (timeout)
  - Call 4: Failure (timeout)
  - Call 5: Failure (timeout)
  - consecutive_failures = 5 >= threshold
→ Trip circuit breaker (even though total calls < 10)
```

---

### Sliding Window Pattern

**Purpose**: Track failure rate over recent operations, not all-time

**Implementation**:

```python
from collections import deque

class CircuitBreaker:
    def __init__(self, window_size=10):
        self.call_results = deque(maxlen=window_size)  # Sliding window

    def record_call(self, success: bool):
        self.call_results.append(success)

        if len(self.call_results) >= 10:
            failure_rate = 1.0 - (sum(self.call_results) / len(self.call_results))

            if failure_rate > 0.5:
                self.trip()
```

**Example**:

```
Sliding window (size=10):
  [S, S, F, F, F, F, F, F, S, S]
  Failures: 6/10 = 60% > 50% threshold
→ Trip circuit breaker

New call succeeds:
  [S, F, F, F, F, F, F, S, S, S]  # Oldest S removed
  Failures: 5/10 = 50% = threshold
→ Keep monitoring

Next call succeeds:
  [F, F, F, F, F, F, S, S, S, S]
  Failures: 6/10 = 60% > 50%
→ Still tripped (need more successes to recover)
```

---

## Recovery Strategies

### Fallback Responses

**Cached Response** (preferred for research agents):

```python
def fetch_with_circuit_breaker(url):
    if circuit_breaker.is_open():
        cached = get_from_cache(url)
        if cached:
            return {
                "status": "SUCCESS",
                "source": "cache",
                "data": cached,
                "warning": "Circuit breaker OPEN, using cached response"
            }
        else:
            return fallback_response(url)

    return attempt_fetch(url)
```

**Example**:

```
WebFetch to "docs.python.org/library/asyncio.html":
  - Circuit breaker OPEN (503 errors)
  - Check cache: Found cached documentation from 2 hours ago
→ Return cached response with warning
```

---

### Degraded Functionality

**Partial Feature Availability**:

```python
def get_deployment_status(namespace):
    if circuit_breaker.is_open():
        return {
            "status": "DEGRADED",
            "message": "kubectl operations unavailable, showing last known state",
            "last_known_state": load_from_disk(namespace),
            "recovery_estimate": "60 seconds"
        }

    return kubectl_get_deployments(namespace)
```

**Example**:

```
deployment-release agent with circuit breaker OPEN:
  - Cannot run kubectl commands
  - Return last known pod status from local state file
  - Warn user operations are degraded
  - Suggest manual kubectl check if critical
```

---

### Escalation Strategy

**When to Escalate**:

1. Circuit breaker trips 3 times in 10 minutes (service persistently failing)
2. Circuit breaker stays OPEN for >5 minutes (long recovery time)
3. No fallback response available (critical operation)

**Escalation Message Template**:

```
CIRCUIT BREAKER ESCALATION

Operation: WebFetch to api.example.com
State: OPEN (60 seconds)
Failure Pattern: 6/10 failures (60% rate)
Last Error: 503 Service Unavailable

Attempted Recovery:
  - Exponential backoff applied (1s, 2s, 4s)
  - Circuit breaker tripped at 50% threshold
  - Waiting 60s for service recovery

Fallback Status: Cache unavailable

Action Required: Check service health or retry manually in 60 seconds
```

---

## Integration with Retry Strategies

**Complementary Patterns** (use together):

**Circuit Breaker**: Prevent overwhelming failing service
**Exponential Backoff**: Space out retry attempts

**Workflow**:

```
1. Attempt operation
2. IF failure:
   a. Record in circuit breaker
   b. Check if should trip circuit breaker (failure rate > 50%)
   c. IF not tripped: Apply exponential backoff and retry
   d. IF tripped: Return fallback response
3. IF circuit breaker OPEN:
   a. Return fallback immediately (no retry)
4. IF circuit breaker HALF-OPEN:
   a. Allow test request (part of 10 permitted)
   b. Record result for recovery decision
```

**Example**:

```
WebFetch operation sequence:

Attempt 1: Failure (503) → Record in circuit breaker (1/10 failures)
  - Not tripped yet, apply exponential backoff (1s)
Attempt 2: Failure (503) → Record (2/10 failures)
  - Backoff 2s
Attempt 3: Failure (503) → Record (3/10 failures)
  - Backoff 4s
...
Attempt 6: Failure (503) → Record (6/10 failures = 60% > 50%)
  - Circuit breaker trips → OPEN state
  - Return cached response immediately (no further retries)

After 60 seconds:
  - Circuit breaker → HALF-OPEN
  - Allow 10 test requests to determine recovery
```

---

## Integration with Error Classification

**See**: `.claude/docs/guides/error-classification-framework.md`

**Circuit Breaker Counting Rules**:

**Count Towards Threshold** (affects circuit breaker state):

- TRANSIENT errors (5xx, timeouts, network failures)
- Rationale: Indicate service health issues

**Do NOT Count** (ignore for circuit breaker):

- PERMANENT errors (4xx except 408/429)
- Rationale: Client-side errors, not service health indicators
- FATAL errors (data corruption, security violations)
- Rationale: Require immediate escalation, not retry

**Example**:

```
10 requests to kubectl:
  - 5 timeouts (TRANSIENT) → Count towards circuit breaker (5/10 = 50%)
  - 3 "immutable field" errors (PERMANENT) → Do NOT count
  - 2 successes

Circuit breaker decision:
  - Only count TRANSIENT: 5 failures, 2 successes = 5/7 = 71% > 50%
→ Trip circuit breaker

If we incorrectly counted PERMANENT errors:
  - 8 failures, 2 successes = 8/10 = 80%
→ Would trip unnecessarily for client-side errors
```

---

## Examples with Integration

### Example 1: WebFetch Circuit Breaker

**Scenario**: researcher-external fetching documentation during service outage

**Setup**:

```python
circuit_breaker = CircuitBreaker(
    operation="webfetch:docs.python.org",
    failure_threshold=0.5,
    min_calls=10,
    wait_duration=60
)
```

**Execution**:

```
Request 1: docs.python.org/library/asyncio.html
  - 503 Service Unavailable
  - Record failure (1/10), retry with 1s backoff

Request 2: Same URL after 1s
  - 503 Service Unavailable
  - Record failure (2/10), retry with 2s backoff

... (pattern continues)

Request 6: After backoffs
  - 503 Service Unavailable
  - Record failure (6/10 = 60% > 50%)
  - Circuit breaker trips → OPEN state

Request 7: Same URL
  - Circuit breaker OPEN → Immediate failure
  - Check cache: Found documentation from yesterday
  - Return cached response with warning

After 60 seconds:
  - Circuit breaker → HALF-OPEN
  - Allow 10 test requests
  - First test: Success (200 OK)
  - Continue testing... 9/10 successes
  - Circuit breaker → CLOSED (service recovered)
```

---

### Example 2: Kubernetes Operations Circuit Breaker

**Scenario**: deployment-release agent during control plane issues

**Setup**:

```python
circuit_breaker = CircuitBreaker(
    operation="kubectl:local-cluster:default",
    failure_threshold=0.5,
    min_calls=10,
    wait_duration=60
)
```

**Execution**:

```
kubectl get pods -n default:
  - i/o timeout (TRANSIENT)
  - Record failure, retry with backoff

kubectl get deployments -n default:
  - i/o timeout (TRANSIENT)
  - Record failure (2/10)

... (multiple operations fail)

6th operation:
  - i/o timeout
  - Circuit breaker trips (6/10 = 60% > 50%)

kubectl apply -f deployment.yaml:
  - Circuit breaker OPEN → Fail immediately
  - Return degraded response:
    "Cannot apply deployment (kubectl unavailable).
     Last known state: 3 pods running.
     Check control plane health manually."

After 60 seconds:
  - Circuit breaker → HALF-OPEN
  - Test with kubectl get nodes (lightweight operation)
  - Success → Continue testing
  - 8/10 test successes → Circuit breaker CLOSED
```

---

### Example 3: File Operations Circuit Breaker

**Scenario**: Windows file locking causing high failure rates in .claude/ directory

**Setup**:

```python
circuit_breaker = CircuitBreaker(
    operation="file_edit:.claude/agents",
    failure_threshold=0.5,
    min_calls=10,
    wait_duration=10  # Shorter wait for file operations
)
```

**Execution**:

```
Edit .claude/agents/test-agent.md:
  - File locked by another process (TRANSIENT)
  - Record failure, retry with 1s backoff

Edit same file:
  - File locked (TRANSIENT)
  - Record failure (2/10), retry with 2s backoff

... (pattern continues due to Claude Code bug)

6th edit attempt:
  - File locked
  - Circuit breaker trips (6/10 = 60% > 50%)

Next edit request:
  - Circuit breaker OPEN → Switch to Python script fallback
  - Use safe_file_edit.py (99% success rate)
  - Success → Record in circuit breaker

After 10 seconds:
  - Circuit breaker → HALF-OPEN
  - Test with Python script (10 attempts)
  - 10/10 successes → Circuit breaker CLOSED
  - Future edits use Python script (learned fallback)
```

---

## Anti-Patterns to Avoid

**Global Circuit Breaker** (Don't):

```python
# ❌ BAD: Single circuit breaker for all operations
global_circuit_breaker = CircuitBreaker()

def fetch_url(url):
    if global_circuit_breaker.is_open():
        return fallback()
    # ...
```

**Problem**: Failure in one service affects unrelated services

**Solution**: Per-operation circuit breakers

---

**Permanent Errors in Threshold** (Don't):

```python
# ❌ BAD: Count all errors towards failure rate
def record_result(status_code):
    if status_code >= 400:
        circuit_breaker.record_failure()
```

**Problem**: Client-side errors (400, 404) trigger circuit breaker inappropriately

**Solution**: Only count TRANSIENT errors (see error-classification-framework.md)

---

**Infinite OPEN State** (Don't):

```python
# ❌ BAD: No automatic recovery testing
if circuit_breaker.is_open():
    return fallback()  # Never transitions to HALF-OPEN
```

**Problem**: Service recovers but circuit breaker stays OPEN forever

**Solution**: Automatic transition to HALF-OPEN after wait duration

---

**No Fallback Strategy** (Don't):

```python
# ❌ BAD: Circuit breaker OPEN with no fallback
if circuit_breaker.is_open():
    raise CircuitBreakerOpenError("Service unavailable")
```

**Problem**: No degraded functionality, complete operation failure

**Solution**: Implement fallback responses (cache, degraded mode, escalation)

---

## Related Documentation

- **Error Classification Framework**: `.claude/docs/guides/error-classification-framework.md` - Determine which errors count towards circuit breaker
- **Retry Strategies**: `.claude/docs/01-guides/retry-strategies.md` - Exponential backoff integration with circuit breakers
- **deployment-release Agent**: `.claude/agents/deployment-release.md` - Kubernetes-specific circuit breaker patterns
- **researcher-external Agent**: `.claude/agents/research/researcher-external/researcher-external.md` - WebFetch circuit breaker implementation

---

**Key Principle**: Circuit breakers prevent cascading failures by failing fast and allowing services time to recover. Always implement fallback strategies for graceful degradation.
