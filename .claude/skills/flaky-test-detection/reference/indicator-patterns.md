# Indicator Patterns: 15 Flakiness Signals

Reference for identifying flaky test indicators in code and behavior.

---

## Timing-Related Indicators (1-5)

### Indicator 1: Hardcoded Sleep
**Risk Level**: HIGH
**Pattern**:
```python
time.sleep(0.5)  # Wait for async operation
await asyncio.sleep(1)
```
**Why Flaky**: Sleep duration may be insufficient under load.
**Fix**: Use explicit waits with conditions.

### Indicator 2: Timestamp Comparison
**Risk Level**: HIGH
**Pattern**:
```python
assert result.timestamp == datetime.now()
```
**Why Flaky**: Microsecond differences cause intermittent failures.
**Fix**: Use time ranges or freeze time.

### Indicator 3: Timeout-Based Assertions
**Risk Level**: MEDIUM
**Pattern**:
```python
with pytest.raises(TimeoutError):
    slow_operation(timeout=0.1)
```
**Why Flaky**: Timeouts race against system load.
**Fix**: Use longer timeouts or mock time.

### Indicator 4: Race Condition Setup
**Risk Level**: HIGH
**Pattern**:
```python
thread.start()
assert shared_state.ready  # May not be ready yet
```
**Why Flaky**: Thread scheduling is non-deterministic.
**Fix**: Use synchronization primitives.

### Indicator 5: Event Loop Timing
**Risk Level**: MEDIUM
**Pattern**:
```python
asyncio.create_task(background_work())
assert result_available()  # Task may not be done
```
**Why Flaky**: Task completion not guaranteed.
**Fix**: Await task completion explicitly.

---

## State-Related Indicators (6-10)

### Indicator 6: Shared Mutable State
**Risk Level**: HIGH
**Pattern**:
```python
class TestSuite:
    data = []  # Shared across tests
    
    def test_add(self):
        self.data.append(1)
```
**Why Flaky**: Test order affects results.
**Fix**: Use fixtures with proper scope.

### Indicator 7: Global Variable Dependency
**Risk Level**: HIGH
**Pattern**:
```python
import config
def test_feature():
    config.DEBUG = True
    # ... test ...
    # Missing: config.DEBUG = False
```
**Why Flaky**: State leaks between tests.
**Fix**: Use fixtures for setup/teardown.

### Indicator 8: Database State Assumption
**Risk Level**: MEDIUM
**Pattern**:
```python
def test_query():
    result = db.query("SELECT * FROM users")
    assert len(result) == 3  # Assumes specific DB state
```
**Why Flaky**: Other tests may modify data.
**Fix**: Use transactions with rollback.

### Indicator 9: File System State
**Risk Level**: MEDIUM
**Pattern**:
```python
def test_read():
    data = open("/tmp/test_file.txt").read()
```
**Why Flaky**: File may not exist or have expected content.
**Fix**: Create file in fixture, clean up after.

### Indicator 10: Cache State
**Risk Level**: MEDIUM
**Pattern**:
```python
def test_cached_value():
    result = cached_function()
    assert result == expected  # Cache may be warm or cold
```
**Why Flaky**: Cache state varies.
**Fix**: Clear cache in setup.

---

## External Dependency Indicators (11-13)

### Indicator 11: Network Call
**Risk Level**: HIGH
**Pattern**:
```python
def test_api():
    response = requests.get("https://api.example.com")
    assert response.status_code == 200
```
**Why Flaky**: Network is unreliable.
**Fix**: Mock external calls.

### Indicator 12: System Resource Dependency
**Risk Level**: MEDIUM
**Pattern**:
```python
def test_port():
    server = start_server(port=8080)
```
**Why Flaky**: Port may be in use.
**Fix**: Use dynamic port allocation.

### Indicator 13: Environment Variable
**Risk Level**: MEDIUM
**Pattern**:
```python
def test_config():
    assert os.environ["API_KEY"] == expected
```
**Why Flaky**: Environment varies.
**Fix**: Set explicitly in fixture.

---

## Randomness Indicators (14-15)

### Indicator 14: Unseeded Random
**Risk Level**: HIGH
**Pattern**:
```python
def test_shuffle():
    result = random.shuffle(items)
    assert result[0] == expected  # Random order!
```
**Why Flaky**: Random is non-deterministic.
**Fix**: Seed random in tests.

### Indicator 15: UUID/Hash Comparison
**Risk Level**: MEDIUM
**Pattern**:
```python
def test_id():
    obj = create_object()
    assert obj.id == "abc123"  # Generated ID
```
**Why Flaky**: IDs are generated fresh.
**Fix**: Mock ID generation or check format only.

---

## Detection Algorithm

```python
INDICATOR_PATTERNS = {
    "time.sleep": ("timing", "HIGH"),
    "datetime.now()": ("timing", "HIGH"),
    "random.": ("randomness", "HIGH"),
    "uuid.uuid": ("randomness", "MEDIUM"),
    "requests.": ("network", "HIGH"),
    "urllib": ("network", "HIGH"),
    "os.environ": ("environment", "MEDIUM"),
    "threading.": ("concurrency", "HIGH"),
    "asyncio.": ("concurrency", "MEDIUM"),
    "global ": ("state", "HIGH"),
    ".append(": ("state", "MEDIUM"),  # On class variable
}

def detect_flakiness_indicators(test_code: str) -> list[tuple[str, str]]:
    """Return list of (indicator, risk_level) tuples."""
    found = []
    for pattern, (category, risk) in INDICATOR_PATTERNS.items():
        if pattern in test_code:
            found.append((category, risk))
    return found
```

---

## Risk Level Summary

| Risk | Count | Categories |
|------|-------|------------|
| HIGH | 7 | timing(2), state(2), network(1), randomness(1), concurrency(1) |
| MEDIUM | 8 | timing(2), state(3), environment(2), randomness(1) |

---

## Quick Detection Checklist

Static analysis (before running):
- [ ] Search for `time.sleep`, `asyncio.sleep`
- [ ] Check for `datetime.now()` in assertions
- [ ] Find `random.` without seed
- [ ] Locate `requests.`, `urllib` calls
- [ ] Identify shared class variables
- [ ] Check for global variable modifications

Behavioral analysis (after running):
- [ ] Test passes/fails inconsistently
- [ ] Different results in CI vs local
- [ ] Fails only under load
- [ ] Fails when run with other tests
- [ ] Timing-sensitive failures

---

## Flakiness Score Calculation

```
Flakiness_Score = Σ (indicator_weight × risk_multiplier)

risk_multiplier:
  HIGH = 1.0
  MEDIUM = 0.5
  LOW = 0.25

indicator_weight:
  Each indicator = 1.0

Score interpretation:
  0-1: Low flakiness risk
  1-3: Medium risk, review recommended
  3+: High risk, refactoring required
```
