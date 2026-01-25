---
title: "Retry Strategies"
date: 2025-11-08
status: ACTIVE
tags: [claude-docs]
---
# Retry Strategies

**Purpose**: Robust retry mechanisms for transient failures using exponential backoff, jitter, and retry budgets to prevent thundering herd and ensure system stability

**Audience**: All agents performing external operations (network requests, file I/O, service calls), sub-agent developers

**Referenced by**: deployment-release, researcher-external, development, source-control, debugger

## Overview

**What is a Retry Strategy?**
Systematic approach to re-attempting failed operations with increasing delays, preventing overwhelming failing services while maximizing success probability.

**Why Use Retry Strategies?**

- **Transient failure recovery**: Automatically recover from temporary issues (network blips, service restarts)
- **Avoid thundering herd**: Prevent simultaneous retries overwhelming recovering service
- **Resource efficiency**: Space out attempts to avoid wasting compute on rapid failures
- **User experience**: Automatic recovery without manual intervention

**When to Use**:

- TRANSIENT errors only (see `.claude/docs/guides/error-classification-framework.md`)
- Network operations (WebFetch, API calls)
- File operations with temporary locking (Windows file system)
- Kubernetes operations (kubectl, API server calls)
- Database queries (connection timeouts, deadlocks)

**When NOT to Use**:

- PERMANENT errors (4xx except 408/429, schema violations, auth failures)
- FATAL errors (data corruption, security violations)
- Idempotency-unsafe operations without idempotency keys (POST without key)

---

## Exponential Backoff

### Formula

**Standard Formula**:

```
wait_time = min(max_delay, base_delay * 2^attempt)
```

**Components**:

- `base_delay`: Initial retry delay (recommend 1 second for general purpose)
- `attempt`: Current retry attempt number (0-indexed: 0, 1, 2, ...)
- `max_delay`: Maximum wait time cap (recommend 20 seconds)
- `min()`: Prevents unbounded growth

**Concrete Example**:

```python
base_delay = 1  # 1 second
max_delay = 20  # 20 seconds

Attempt 0 (first retry):  wait_time = min(20, 1 * 2^0) = 1 second
Attempt 1 (second retry): wait_time = min(20, 1 * 2^1) = 2 seconds
Attempt 2 (third retry):  wait_time = min(20, 1 * 2^2) = 4 seconds
Attempt 3 (fourth retry): wait_time = min(20, 1 * 2^3) = 8 seconds
Attempt 4 (fifth retry):  wait_time = min(20, 1 * 2^4) = 16 seconds
Attempt 5 (sixth retry):  wait_time = min(20, 1 * 2^5) = 20 seconds (capped)
```

---

### Configuration Recommendations

**Base Delay Selection**:

- **Fast operations** (file I/O, local services): 100ms - 500ms
- **General purpose** (HTTP requests, kubectl): 1 second (RECOMMENDED)
- **Heavy operations** (large file transfers, database migrations): 2 seconds

**Max Delay Selection**:

- **Interactive operations** (user-initiated requests): 10 seconds
- **General purpose** (background tasks, research): 20 seconds (RECOMMENDED)
- **Batch operations** (data processing, bulk updates): 60 seconds

**Why These Values?**:

- AWS Builders Library recommendations (battle-tested at scale)
- Balance between recovery time and user experience
- Prevent overwhelming recovering services
- Industry standard (Google Cloud, Azure, Kubernetes use similar values)

**Example Configuration**:

```python
# General purpose retry configuration (RECOMMENDED)
RETRY_CONFIG = {
    "base_delay": 1.0,      # 1 second initial delay
    "max_delay": 20.0,      # 20 seconds maximum
    "max_attempts": 3,      # 3 retry attempts
    "jitter_type": "full"   # Full jitter (AWS preferred)
}

# Fast operations (file I/O, local services)
FAST_RETRY_CONFIG = {
    "base_delay": 0.5,      # 500ms initial delay
    "max_delay": 10.0,      # 10 seconds maximum
    "max_attempts": 5,      # More attempts for transient issues
    "jitter_type": "full"
}

# Heavy operations (large transfers, migrations)
HEAVY_RETRY_CONFIG = {
    "base_delay": 2.0,      # 2 second initial delay
    "max_delay": 60.0,      # 60 seconds maximum
    "max_attempts": 3,      # Fewer attempts (expensive operations)
    "jitter_type": "equal"  # Equal jitter (predictable timing)
}
```

---

## Jitter Implementation

### Why Jitter?

**Problem**: Without jitter, all clients retry at exact same intervals

```
10 clients fail simultaneously at t=0
All retry at t=1s, t=2s, t=4s (thundering herd)
→ Overwhelm recovering service with synchronized load
```

**Solution**: Add randomness to break synchronization

```
10 clients fail simultaneously at t=0
Retry at t=0.3s, t=0.7s, t=1.2s, t=1.8s, t=2.1s, ... (distributed load)
→ Gradual load increase, service has time to recover
```

---

### Full Jitter (AWS Preferred)

**Formula**:

```python
import random

wait_time = random.uniform(0, min(max_delay, base_delay * 2^attempt))
```

**Characteristics**:

- Most aggressive jitter (0 to full calculated delay)
- Best for distributed systems with many clients
- Fastest average recovery time
- AWS recommendation from Builders Library

**Concrete Example**:

```python
base_delay = 1
max_delay = 20
attempt = 2

calculated_delay = min(20, 1 * 2^2) = 4 seconds
jitter_range = [0, 4]

Possible wait times:
  - 0.5 seconds (random)
  - 1.8 seconds (random)
  - 3.2 seconds (random)
  - 2.7 seconds (random)

Average: ~2 seconds (50% of calculated delay)
```

**Implementation**:

```python
def exponential_backoff_full_jitter(base_delay, max_delay, attempt):
    """Full jitter exponential backoff (AWS preferred)"""
    calculated = min(max_delay, base_delay * (2 ** attempt))
    return random.uniform(0, calculated)

# Usage example
for attempt in range(3):
    try:
        result = operation()
        break  # Success
    except TransientError:
        wait = exponential_backoff_full_jitter(1.0, 20.0, attempt)
        print(f"Retry {attempt+1} after {wait:.2f}s")
        time.sleep(wait)
```

---

### Equal Jitter (Predictable)

**Formula**:

```python
calculated_delay = min(max_delay, base_delay * 2^attempt)
wait_time = (calculated_delay / 2) + random.uniform(0, calculated_delay / 2)
```

**Characteristics**:

- Moderate jitter (50% to 100% of calculated delay)
- More predictable timing than full jitter
- Good for operations with timing requirements
- Middle ground between no jitter and full jitter

**Concrete Example**:

```python
base_delay = 1
max_delay = 20
attempt = 2

calculated_delay = min(20, 1 * 2^2) = 4 seconds
base_wait = 4 / 2 = 2 seconds
jitter_range = [0, 2]

Possible wait times:
  - 2.0 + 0.3 = 2.3 seconds (random)
  - 2.0 + 1.5 = 3.5 seconds (random)
  - 2.0 + 0.8 = 2.8 seconds (random)

Average: ~3 seconds (75% of calculated delay)
Range: [2s, 4s] (guaranteed at least 50% of calculated)
```

**Implementation**:

```python
def exponential_backoff_equal_jitter(base_delay, max_delay, attempt):
    """Equal jitter exponential backoff (predictable timing)"""
    calculated = min(max_delay, base_delay * (2 ** attempt))
    base = calculated / 2
    jitter = random.uniform(0, calculated / 2)
    return base + jitter

# Usage example
for attempt in range(3):
    try:
        result = operation()
        break
    except TransientError:
        wait = exponential_backoff_equal_jitter(1.0, 20.0, attempt)
        print(f"Retry {attempt+1} after {wait:.2f}s (range: [{calculated/2:.1f}s, {calculated:.1f}s])")
        time.sleep(wait)
```

---

### Decorrelated Jitter (Advanced)

**Formula**:

```python
wait_time = min(max_delay, random.uniform(base_delay, previous_wait * 3))
```

**Characteristics**:

- Uses previous wait time as input (not attempt number)
- Most aggressive de-correlation
- Best for highly synchronized clients
- Recommended for distributed systems with synchronized failures

**Concrete Example**:

```python
base_delay = 1
max_delay = 20
previous_wait = 0

Attempt 0: wait = random.uniform(1, 1 * 3) = [1, 3] seconds → 2.1s chosen
Attempt 1: wait = random.uniform(1, 2.1 * 3) = [1, 6.3] seconds → 4.7s chosen
Attempt 2: wait = random.uniform(1, 4.7 * 3) = [1, 14.1] seconds → 9.2s chosen
Attempt 3: wait = random.uniform(1, 9.2 * 3) = [1, 20] seconds (capped) → 15.8s chosen
```

**Implementation**:

```python
def exponential_backoff_decorrelated_jitter(base_delay, max_delay, previous_wait):
    """Decorrelated jitter (advanced de-synchronization)"""
    if previous_wait == 0:
        return random.uniform(base_delay, base_delay * 3)

    return min(max_delay, random.uniform(base_delay, previous_wait * 3))

# Usage example
previous_wait = 0
for attempt in range(3):
    try:
        result = operation()
        break
    except TransientError:
        wait = exponential_backoff_decorrelated_jitter(1.0, 20.0, previous_wait)
        previous_wait = wait
        print(f"Retry {attempt+1} after {wait:.2f}s")
        time.sleep(wait)
```

---

### Jitter Selection Guide

**Use Full Jitter When**:

- Distributed system with many clients
- Clients likely to fail simultaneously (service outage)
- Fastest recovery time desired
- **RECOMMENDED for most use cases**

**Use Equal Jitter When**:

- Timing predictability important
- Need guaranteed minimum delay (SLA requirements)
- User-facing operations with expected response times

**Use Decorrelated Jitter When**:

- Highly synchronized client failures (cascading failures)
- Advanced distributed systems (microservices, multi-region)
- Maximum de-correlation needed

---

## Retry Budgets

### Per-Request Budget

**Definition**: Maximum number of retry attempts per individual request

**Recommendation**: 3 attempts maximum

- Initial attempt + 3 retries = 4 total attempts
- Rationale: Balance recovery probability with wasted resources

**Why 3 Attempts?**:

- 1st retry: ~50% transient issues resolve
- 2nd retry: ~30% additional recovery
- 3rd retry: ~15% additional recovery
- Beyond 3: Diminishing returns (<5% recovery, high cost)

**Example**:

```python
MAX_RETRIES = 3

for attempt in range(MAX_RETRIES):
    try:
        result = operation()
        return result  # Success
    except TransientError as e:
        if attempt == MAX_RETRIES - 1:
            raise  # Exhausted retries, escalate

        wait = exponential_backoff_full_jitter(1.0, 20.0, attempt)
        time.sleep(wait)

# If we reach here, all retries exhausted
raise MaxRetriesExceededError(f"Failed after {MAX_RETRIES} attempts")
```

**Adjustment Guidelines**:

- **Increase to 5** for: File operations (Windows file locking), low-cost operations
- **Decrease to 2** for: Expensive operations (large file transfers), user-initiated requests
- **Decrease to 1** for: Time-sensitive operations, real-time systems

---

### Per-Client Budget

**Definition**: Maximum ratio of retries to total requests across all operations

**Recommendation**: 10% retry ratio

- Formula: `retry_ratio = retry_count / (success_count + failure_count)`
- If ratio exceeds 10%, throttle or escalate

**Rationale**:

- Prevents client from overwhelming service with retries
- Google SRE Book recommendation
- Industry standard for distributed systems

**Example**:

```python
class RetryBudgetTracker:
    def __init__(self, budget_threshold=0.1):
        self.success_count = 0
        self.retry_count = 0
        self.budget_threshold = budget_threshold

    def can_retry(self):
        """Check if retry budget available"""
        total_attempts = self.success_count + self.retry_count

        if total_attempts == 0:
            return True  # No attempts yet, allow retry

        retry_ratio = self.retry_count / total_attempts

        return retry_ratio < self.budget_threshold

    def record_success(self):
        self.success_count += 1

    def record_retry(self):
        self.retry_count += 1

# Usage
budget = RetryBudgetTracker(budget_threshold=0.1)

def operation_with_budget():
    for attempt in range(3):
        try:
            result = operation()
            budget.record_success()
            return result
        except TransientError:
            if not budget.can_retry():
                raise RetryBudgetExceededError("10% retry budget exceeded")

            budget.record_retry()
            wait = exponential_backoff_full_jitter(1.0, 20.0, attempt)
            time.sleep(wait)
```

**Concrete Example**:

```
Client statistics over 1 hour:
  - 100 total requests
  - 90 successes (first attempt)
  - 10 initial failures
  - 8 retries (attempts 2-4)
  - 2 final failures (exhausted retries)

Retry ratio: 8 / 100 = 8% < 10% threshold
→ Within budget, continue normal operations

Alternative scenario:
  - 100 total requests
  - 50 successes
  - 50 initial failures
  - 45 retries
  - 5 final failures

Retry ratio: 45 / 100 = 45% > 10% threshold
→ Budget exceeded, throttle retries or escalate to circuit breaker
```

---

## Idempotency Considerations

### Safe-to-Retry Operations (Idempotent)

**HTTP Methods** (naturally idempotent):

- `GET` - Read operation, no side effects
- `PUT` - Replace operation, same result on repeated calls
- `DELETE` - Remove operation, idempotent (deleting nonexistent returns same result)
- `HEAD` - Metadata only, no side effects
- `OPTIONS` - Query supported methods, no side effects

**Example**:

```python
# Safe to retry without idempotency key
def get_deployment_status(namespace):
    """GET request, naturally idempotent"""
    for attempt in range(3):
        try:
            return kubectl_get_deployments(namespace)
        except TransientError:
            wait = exponential_backoff_full_jitter(1.0, 20.0, attempt)
            time.sleep(wait)
```

---

### Unsafe Operations (Require Idempotency Keys)

**HTTP Methods** (NOT naturally idempotent):

- `POST` - Create operation, may create duplicates on retry
- `PATCH` - Partial update, may apply changes multiple times

**Solution**: Use idempotency keys

```python
import uuid

def create_resource_with_idempotency(data):
    """POST request with idempotency key"""
    idempotency_key = str(uuid.uuid4())  # Generate once, reuse on retries

    for attempt in range(3):
        try:
            return api_post(
                url="/resources",
                data=data,
                headers={"Idempotency-Key": idempotency_key}
            )
        except TransientError:
            wait = exponential_backoff_full_jitter(1.0, 20.0, attempt)
            time.sleep(wait)
            # Reuse same idempotency_key on retry
```

**How Idempotency Keys Work**:

1. Client generates unique key (UUID) before first attempt
2. Server stores key with result on success
3. On retry with same key, server returns cached result (doesn't re-execute)
4. Prevents duplicate resource creation

**Example**:

```
POST /api/deployments (idempotency_key=123e4567-e89b-12d3-a456-426614174000)
  - Creates deployment "app-v1"
  - Server stores: {key: 123e4567, result: deployment_id_789}

Retry (network timeout before response received):
POST /api/deployments (idempotency_key=123e4567-e89b-12d3-a456-426614174000)
  - Server checks key: Found cached result
  - Returns deployment_id_789 (doesn't create duplicate)
```

---

## Integration with Error Classification

**See**: `.claude/docs/guides/error-classification-framework.md`

**Retry Decision Logic**:

```python
from error_classification import classify_error, ErrorType

def operation_with_retry():
    for attempt in range(3):
        try:
            return operation()
        except Exception as e:
            error_type = classify_error(e)

            if error_type == ErrorType.TRANSIENT:
                # Safe to retry
                wait = exponential_backoff_full_jitter(1.0, 20.0, attempt)
                time.sleep(wait)
                continue

            elif error_type == ErrorType.PERMANENT:
                # Do NOT retry, immediate failure
                raise PermanentError(f"Non-retryable error: {e}")

            elif error_type == ErrorType.FATAL:
                # NEVER retry, escalate immediately
                escalate_to_human(f"Fatal error: {e}")
                raise

    raise MaxRetriesExceededError("Exhausted retries")
```

**Example**:

```python
# Classify errors and apply appropriate retry strategy

try:
    result = kubectl_apply("deployment.yaml")
except Exception as e:
    error_type = classify_error(e)

    if "immutable field" in str(e):
        # PERMANENT error (immutability constraint)
        # Do NOT retry
        raise PermanentError("Cannot modify immutable field, fix manifest")

    elif "i/o timeout" in str(e):
        # TRANSIENT error (network timeout)
        # Retry with exponential backoff
        for attempt in range(3):
            wait = exponential_backoff_full_jitter(1.0, 20.0, attempt)
            time.sleep(wait)
            try:
                return kubectl_apply("deployment.yaml")
            except Exception:
                if attempt == 2:
                    raise  # Exhausted retries

    elif "etcd cluster failure" in str(e):
        # FATAL error (control plane down)
        # NEVER retry, escalate immediately
        escalate_to_human("Control plane failure, manual intervention required")
        raise
```

---

## Complete Retry Pattern Implementation

**Production-Ready Example**:

```python
import time
import random
from enum import Enum

class ErrorType(Enum):
    TRANSIENT = "transient"
    PERMANENT = "permanent"
    FATAL = "fatal"

class RetryStrategy:
    def __init__(
        self,
        base_delay=1.0,
        max_delay=20.0,
        max_attempts=3,
        jitter_type="full"
    ):
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.max_attempts = max_attempts
        self.jitter_type = jitter_type

    def calculate_wait(self, attempt, previous_wait=0):
        """Calculate wait time with jitter"""
        calculated = min(self.max_delay, self.base_delay * (2 ** attempt))

        if self.jitter_type == "full":
            return random.uniform(0, calculated)
        elif self.jitter_type == "equal":
            base = calculated / 2
            return base + random.uniform(0, calculated / 2)
        elif self.jitter_type == "decorrelated":
            if previous_wait == 0:
                return random.uniform(self.base_delay, self.base_delay * 3)
            return min(self.max_delay, random.uniform(self.base_delay, previous_wait * 3))
        else:
            return calculated  # No jitter

    def execute_with_retry(self, operation, classify_error_fn):
        """Execute operation with retry logic"""
        previous_wait = 0

        for attempt in range(self.max_attempts):
            try:
                result = operation()
                return result  # Success

            except Exception as e:
                error_type = classify_error_fn(e)

                # Check if should retry
                if error_type == ErrorType.PERMANENT:
                    raise PermanentError(f"Non-retryable error: {e}")

                if error_type == ErrorType.FATAL:
                    escalate_to_human(f"Fatal error requires intervention: {e}")
                    raise

                # Last attempt exhausted
                if attempt == self.max_attempts - 1:
                    raise MaxRetriesExceededError(
                        f"Failed after {self.max_attempts} attempts: {e}"
                    )

                # TRANSIENT error, retry with backoff
                wait = self.calculate_wait(attempt, previous_wait)
                previous_wait = wait

                print(f"Attempt {attempt + 1} failed ({error_type.value}), "
                      f"retrying in {wait:.2f}s: {e}")

                time.sleep(wait)

        raise MaxRetriesExceededError("Retry loop exhausted")

# Usage example
def classify_kubectl_error(error):
    """Classify kubectl errors"""
    error_msg = str(error).lower()

    if "timeout" in error_msg or "unavailable" in error_msg:
        return ErrorType.TRANSIENT
    elif "immutable" in error_msg or "invalid" in error_msg:
        return ErrorType.PERMANENT
    elif "etcd" in error_msg or "control plane" in error_msg:
        return ErrorType.FATAL
    else:
        return ErrorType.PERMANENT  # Conservative default

# Execute kubectl with retry
strategy = RetryStrategy(
    base_delay=1.0,
    max_delay=20.0,
    max_attempts=3,
    jitter_type="full"
)

result = strategy.execute_with_retry(
    operation=lambda: kubectl_get_pods("default"),
    classify_error_fn=classify_kubectl_error
)
```

---

## Examples with Integration

### Example 1: WebFetch with Full Retry Strategy

**Scenario**: researcher-external fetching documentation with transient 503 errors

```python
def fetch_documentation(url):
    """Fetch documentation with exponential backoff and error classification"""

    def classify_http_error(error):
        if hasattr(error, 'status_code'):
            if error.status_code in [408, 429, 500, 502, 503, 504]:
                return ErrorType.TRANSIENT
            elif error.status_code in [400, 401, 403, 404]:
                return ErrorType.PERMANENT
        return ErrorType.PERMANENT  # Default to permanent

    strategy = RetryStrategy(base_delay=1.0, max_delay=20.0, max_attempts=3)

    return strategy.execute_with_retry(
        operation=lambda: requests.get(url, timeout=10),
        classify_error_fn=classify_http_error
    )

# Usage
result = fetch_documentation("https://docs.python.org/3/library/asyncio.html")
```

**Execution Flow**:

```
Attempt 1: 503 Service Unavailable
  - Classify: TRANSIENT
  - Wait: 0.7s (full jitter, 0-1s range)

Attempt 2: 503 Service Unavailable
  - Classify: TRANSIENT
  - Wait: 1.8s (full jitter, 0-2s range)

Attempt 3: 200 OK
  - Success, return result
```

---

### Example 2: Kubernetes Operations with Idempotency

**Scenario**: deployment-release applying manifests with network timeouts

```python
import uuid

def kubectl_apply_with_retry(manifest_path):
    """Apply Kubernetes manifest with retry and idempotency"""

    # Generate idempotency key (reused on retries)
    operation_id = str(uuid.uuid4())

    def classify_kubectl_error(error):
        error_msg = str(error).lower()
        if "timeout" in error_msg or "connection refused" in error_msg:
            return ErrorType.TRANSIENT
        elif "immutable" in error_msg:
            return ErrorType.PERMANENT
        elif "etcd" in error_msg:
            return ErrorType.FATAL
        return ErrorType.PERMANENT

    def apply_operation():
        # kubectl apply is idempotent (PUT-like behavior)
        return kubectl_apply(manifest_path, idempotency_key=operation_id)

    strategy = RetryStrategy(base_delay=1.0, max_delay=20.0, max_attempts=3)

    return strategy.execute_with_retry(
        operation=apply_operation,
        classify_error_fn=classify_kubectl_error
    )

# Usage
result = kubectl_apply_with_retry("deployment.yaml")
```

---

### Example 3: File Operations with Windows File Locking

**Scenario**: development editing .claude/ files with high failure rates

```python
def safe_file_edit_with_retry(file_path, old_string, new_string):
    """Edit file with retry for Windows file locking"""

    def classify_file_error(error):
        error_msg = str(error).lower()
        if "permission denied" in error_msg or "locked" in error_msg:
            return ErrorType.TRANSIENT  # Temporary file lock
        elif "not found" in error_msg:
            return ErrorType.PERMANENT  # File doesn't exist
        return ErrorType.PERMANENT

    # Use shorter delays for file operations (faster recovery)
    strategy = RetryStrategy(
        base_delay=0.5,    # 500ms initial delay
        max_delay=10.0,    # 10s maximum
        max_attempts=5,    # More attempts for transient locking
        jitter_type="full"
    )

    return strategy.execute_with_retry(
        operation=lambda: edit_file(file_path, old_string, new_string),
        classify_error_fn=classify_file_error
    )

# Usage
result = safe_file_edit_with_retry(
    ".claude/agents/test-agent.md",
    "old text",
    "new text"
)
```

---

## Anti-Patterns to Avoid

**Infinite Retries** (Don't):

```python
# ❌ BAD: No retry limit
while True:
    try:
        return operation()
    except Exception:
        time.sleep(1)
        continue  # Retry forever
```

**Problem**: Wastes resources on unrecoverable errors

**Solution**: Max 3 attempts, classify errors

---

**Fixed Delay Retries** (Don't):

```python
# ❌ BAD: Fixed 1s delay
for attempt in range(3):
    try:
        return operation()
    except Exception:
        time.sleep(1)  # Same delay every time
```

**Problem**: Thundering herd (all clients retry simultaneously)

**Solution**: Exponential backoff with jitter

---

**No Error Classification** (Don't):

```python
# ❌ BAD: Retry all errors
for attempt in range(3):
    try:
        return operation()
    except Exception:
        time.sleep(2 ** attempt)
        continue  # Retry permanent errors
```

**Problem**: Wastes retries on non-retryable errors

**Solution**: Classify errors, only retry TRANSIENT

---

**No Idempotency for Unsafe Operations** (Don't):

```python
# ❌ BAD: Retry POST without idempotency key
for attempt in range(3):
    try:
        return api_post("/resources", data)  # Creates duplicate on retry
    except Exception:
        time.sleep(2 ** attempt)
```

**Problem**: Creates duplicate resources

**Solution**: Use idempotency keys for POST/PATCH

---

## Related Documentation

- **Error Classification Framework**: `.claude/docs/guides/error-classification-framework.md` - Determine which errors to retry
- **Circuit Breaker Pattern**: `.claude/docs/01-guides/circuit-breaker-pattern.md` - Prevent cascading failures
- **deployment-release Agent**: `.claude/agents/deployment-release.md` - Kubernetes-specific retry patterns
- **researcher-external Agent**: `.claude/agents/research/researcher-external/researcher-external.md` - WebFetch retry implementation

---

**Key Principle**: Retry strategies maximize success probability for transient failures while preventing resource waste on unrecoverable errors. Always combine with error classification and circuit breakers for production systems.
