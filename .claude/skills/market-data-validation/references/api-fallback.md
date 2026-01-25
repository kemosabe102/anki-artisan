# API Fallback Reference

Data connector resilience patterns with circuit breaker implementation.

---

## Fallback Chain: Alpaca -> Polygon -> Yahoo

### Priority Order

| Priority | Provider | Use Case | Rate Limits |
|----------|----------|----------|-------------|
| 1 | **Alpaca** | Primary (free tier available) | 200 req/min |
| 2 | **Polygon** | Secondary (paid, higher quality) | 5 req/min (free) |
| 3 | **Yahoo** | Tertiary (fallback only) | Unofficial limits |

### Fallback Logic

```python
def fetch_ohlcv(symbol: str, start: str, end: str) -> ConnectorResult:
    providers = [alpaca_connector, polygon_connector, yahoo_connector]
    
    for provider in providers:
        if provider.circuit_breaker.is_open:
            continue  # Skip failed providers
        
        result = provider.fetch(symbol, start, end)
        if result.status == 'SUCCESS':
            return result
        
        provider.circuit_breaker.record_failure()
    
    return ConnectorResult(status='PROVIDER_EXHAUSTED')
```

---

## Circuit Breaker Pattern

### States

```
CLOSED (normal) --[3 failures]--> OPEN (blocking)
                                      |
                                 [30s timeout]
                                      |
                                      v
                                 HALF_OPEN (testing)
                                      |
                          [success]--> CLOSED
                          [failure]--> OPEN
```

### Configuration Profiles

| Profile | failure_threshold | reset_timeout | half_open_max | Use Case |
|---------|-------------------|---------------|---------------|----------|
| **Conservative** | 3 | 30s | 1 | Critical paths, backtesting |
| **Balanced** | 5 | 60s | 2 | Standard production |
| **Aggressive** | 8 | 90s | 3 | High-throughput, fault-tolerant |

### Implementation

```python
class CircuitBreaker:
    def __init__(self, failure_threshold=3, reset_timeout=30):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'CLOSED'
    
    @property
    def is_open(self) -> bool:
        if self.state == 'OPEN':
            if time.time() - self.last_failure_time > self.reset_timeout:
                self.state = 'HALF_OPEN'
                return False
            return True
        return False
    
    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = 'OPEN'
    
    def record_success(self):
        self.failure_count = 0
        self.state = 'CLOSED'
```

---

## Partial Failure Handling

When 2/3 providers fail:

1. Return `PARTIAL_SUCCESS` with data from working provider
2. Set `degraded_mode=True` in response metadata
3. Include `failed_providers` list for monitoring
4. Log warning for ops alerting

### Response Structure

```python
ConnectorResult(
    status='PARTIAL_SUCCESS',
    data=df,
    metadata={
        'degraded_mode': True,
        'provider': 'yahoo',
        'failed_providers': ['alpaca', 'polygon'],
        'execution_time_ms': 1250
    }
)
```
