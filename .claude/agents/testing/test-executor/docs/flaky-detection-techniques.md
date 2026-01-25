# Flaky Test Detection Techniques

**Category**: testing
**Domain**: Test reliability analysis and flakiness detection
**Confidence**: 0.90
**Last Updated**: 2025-10-26T00:00:00Z
**Agent**: test-executor

---

## Overview

Flaky tests (tests that pass/fail inconsistently) undermine test suite reliability and developer confidence. Automated flaky test detection uses repeatability validation, statistical thresholds, and flakiness indicators to identify and quarantine unreliable tests. This enables proactive test improvement and prevents flaky tests from blocking valid deployments.

**Key Concepts**:

- **Flaky Test**: Test that passes/fails inconsistently without code changes
- **Repeatability Validation**: Running tests multiple times to measure failure rate
- **Quarantine**: Isolating flaky tests to prevent blocking CI/CD pipelines

---

## Core Frameworks

### Framework 1: Repeatability Validation Techniques

**Purpose**: Determine if test is flaky through statistical N-run validation

**When to Use**:

- When test fails once but cause unclear
- Before marking test as reliably failing
- After fixing suspected flaky test
- During test suite health audits

**Components**:

1. **N-Run Validation**: Execute test 3-5 times with delays between runs
2. **Failure Rate Calculation**: `failure_rate = failures / total_runs`
3. **Threshold Comparison**: `if failure_rate > 0.15 → FLAKY`
4. **Quarantine Decision**: Isolate if failure rate >15% but <100%

**How to Apply**:

1. Detect test failure in initial run
2. Execute test N=5 times with 1-2s delays
3. Record pass/fail outcome for each run
4. Calculate failure rate: `failures / 5`
5. Decision:
   - 0% failure rate → False alarm, likely environment issue
   - 1-15% failure rate → Likely flaky, monitor
   - 16-99% failure rate → Definitely flaky, quarantine immediately
   - 100% failure rate → Reliably failing, categorize and delegate fix

**Example from Codebase**:

```python
import subprocess
import time
from typing import Tuple, List

def validate_test_repeatability(
    test_path: str,
    n_runs: int = 5,
    delay_seconds: float = 1.5
) -> Tuple[float, List[bool]]:
    """
    Run test N times to calculate failure rate.

    Args:
        test_path: pytest node ID (e.g., "tests/unit/test_auth.py::test_login")
        n_runs: Number of validation runs (default 5)
        delay_seconds: Delay between runs (default 1.5s)

    Returns:
        (failure_rate, outcomes) where outcomes is list of pass/fail bools
    """
    outcomes = []

    for i in range(n_runs):
        result = subprocess.run(
            ["uv", "run", "pytest", test_path, "-v"],
            capture_output=True
        )
        outcomes.append(result.returncode != 0)  # True if failed

        if i < n_runs - 1:  # Don't delay after last run
            time.sleep(delay_seconds)

    failures = sum(outcomes)
    failure_rate = failures / n_runs

    return (failure_rate, outcomes)


def classify_by_failure_rate(failure_rate: float) -> str:
    """Classify test based on failure rate."""
    if failure_rate == 0.0:
        return "PASSING"  # False alarm
    elif failure_rate <= 0.15:
        return "POTENTIALLY_FLAKY"  # Monitor
    elif failure_rate < 1.0:
        return "FLAKY"  # Quarantine
    else:
        return "RELIABLY_FAILING"  # Delegate fix
```

**Source**: Industry best practices, Google Testing Blog - https://testing.googleblog.com/

---

### Framework 2: Flaky Test Indicators (5 Categories)

**Purpose**: Identify flakiness indicators in test code through pattern analysis

**When to Use**:

- During test creation review
- When investigating flaky test root cause
- During test suite refactoring
- In pre-commit test quality checks

**Components**:

**1. Timing Issues**

- `time.sleep()` calls without justification
- Hard-coded timeouts (e.g., `timeout=5`)
- Race conditions in async code
- No synchronization for concurrent operations

**2. Random Data**

- `random.random()` without seed
- `uuid.uuid4()` without mocking
- Non-deterministic data generation
- Timestamp-based test data

**3. Shared State**

- Global variables modified in tests
- Database state not cleaned between tests
- File system persistence without cleanup
- Singleton pattern misuse

**4. Infrastructure Variability**

- Platform-specific assumptions (Windows vs Linux)
- External service dependencies (network calls)
- Hardcoded paths or ports
- Environment variable dependencies without validation

**5. Test Size Correlation**

- Larger tests have exponentially higher flakiness
- Google data: Small tests 0.5% flaky, Large tests 14% flaky
- More dependencies = more flakiness sources

**How to Apply**:

1. Parse test source code
2. Search for indicator patterns using regex or AST analysis
3. Score each test by indicator count
4. Flag tests with high indicator counts (≥3) for review
5. Recommend specific improvements based on indicators found

**Example from Codebase**:

```python
import ast
import re
from typing import List, Dict
from pathlib import Path

class FlakinessIndicatorDetector:
    """Detect flakiness indicators in test code."""

    # Indicator patterns
    TIMING_PATTERNS = [
        r"time\.sleep\(",
        r"timeout\s*=\s*\d+",
        r"\.wait\(",
    ]

    RANDOM_PATTERNS = [
        r"random\.random\(",
        r"uuid\.uuid4\(",
        r"datetime\.now\(",
    ]

    SHARED_STATE_PATTERNS = [
        r"global\s+\w+",
        r"@pytest\.fixture\(scope=[\"']session[\"']\)",
    ]

    def detect_indicators(self, test_file: Path) -> Dict[str, List[str]]:
        """Scan test file for flakiness indicators."""
        source = test_file.read_text()
        indicators = {
            "timing_issues": [],
            "random_data": [],
            "shared_state": [],
            "infrastructure": []
        }

        # Check timing patterns
        for pattern in self.TIMING_PATTERNS:
            matches = re.findall(pattern, source)
            indicators["timing_issues"].extend(matches)

        # Check random data patterns
        for pattern in self.RANDOM_PATTERNS:
            matches = re.findall(pattern, source)
            indicators["random_data"].extend(matches)

        # Check shared state patterns
        for pattern in self.SHARED_STATE_PATTERNS:
            matches = re.findall(pattern, source)
            indicators["shared_state"].extend(matches)

        # Check external dependencies
        if "requests." in source or "httpx." in source:
            indicators["infrastructure"].append("External HTTP calls")

        return indicators

    def score_flakiness_risk(self, indicators: Dict[str, List[str]]) -> float:
        """Calculate flakiness risk score (0.0-1.0)."""
        total_indicators = sum(len(v) for v in indicators.values())
        # Risk increases non-linearly with indicator count
        risk_score = min(1.0, (total_indicators ** 1.5) / 10)
        return risk_score
```

**Source**: Research synthesis from Google Testing Blog, industry patterns

---

### Framework 3: Common Flaky Test Patterns (15 Patterns)

**Purpose**: Catalog of specific flaky test patterns with detection indicators and fixes

**When to Use**:

- When investigating root cause of flaky test
- During test creation review for proactive prevention
- When building automated flakiness detection

**How to Apply**:

1. Match failure symptoms to pattern indicators
2. Verify confidence score meets threshold (≥0.70)
3. Apply recommended fix from pattern
4. Validate fix with N-run repeatability testing

---

## Pattern 1: Hard-Coded Sleep Timeouts

**Indicators**:

- Error messages: "AssertionError" after wait, "condition not met"
- Code patterns: `time.sleep(N)` without retry logic
- Failure timing: Intermittent (depends on system load)

**Confidence**: 0.80 (high if sleep + timing assertion)

**Common Causes**:

- Sleep duration too short for slow systems
- No verification that condition was actually met
- Race condition masked by arbitrary delay

**Recommended Fix**:

- Replace `time.sleep()` with condition polling (wait_until pattern)
- Use `WebDriverWait` for UI testing
- Add explicit synchronization with event/flag checks

---

## Pattern 2: Non-Deterministic Data Generation

**Indicators**:

- Error messages: Assertion failures with different values each run
- Code patterns: `random.random()`, `uuid.uuid4()` without seed/mock
- Failure timing: Random (depends on generated data)

**Confidence**: 0.85 (very high if random + assertion)

**Common Causes**:

- Random data generation without seed control
- UUID generation in test comparisons
- Non-deterministic ordering (dict iteration in Python <3.7)

**Recommended Fix**:

- Add `random.seed(42)` at test start
- Mock `uuid.uuid4()` with fixed value
- Use `pytest.fixture` with deterministic data

---

## Pattern 3: Shared Global State

**Indicators**:

- Error messages: Test order dependent failures, "value already set"
- Code patterns: Global variables, class attributes modified in tests
- Failure timing: Depends on test execution order

**Confidence**: 0.90 (very high if order-dependent)

**Common Causes**:

- Tests modify shared global state without cleanup
- Singleton patterns retain state across tests
- Class-level attributes used for test data

**Recommended Fix**:

- Use function-scoped fixtures instead of globals
- Add tearDown cleanup to reset state
- Use pytest-randomly to detect order dependencies

---

## Pattern 4: File System Persistence

**Indicators**:

- Error messages: "FileExistsError", "PermissionError", "file not found"
- Code patterns: File creation without cleanup, hardcoded paths
- Failure timing: After first test run (files persist)

**Confidence**: 0.85 (high if file operations + cleanup missing)

**Common Causes**:

- Test files not deleted in tearDown
- Hardcoded filenames cause collisions
- Parallel tests write to same file

**Recommended Fix**:

- Use `pytest.tmpdir` fixture for isolated temp directories
- Add file cleanup in tearDown (try/finally)
- Use unique filenames with UUID or timestamp

---

## Pattern 5: Network/External Service Dependencies

**Indicators**:

- Error messages: "ConnectionError", "Timeout", "503 Service Unavailable"
- Code patterns: HTTP requests, database queries, API calls (not mocked)
- Failure timing: Intermittent (depends on network/service)

**Confidence**: 0.90 (very high if network error)

**Common Causes**:

- Tests call real external services
- No mocking of HTTP/API responses
- Service rate limiting or downtime

**Recommended Fix**:

- Mock all external HTTP requests (`responses` library)
- Use pytest-vcr to record/replay interactions
- Mock database queries with in-memory DB or fixtures

---

## Pattern 6: Platform-Specific Assumptions

**Indicators**:

- Error messages: "FileNotFoundError" on Windows, "No such file"
- Code patterns: Hardcoded paths (`/tmp`, `C:\`), platform-specific imports
- Failure timing: Only on specific OS

**Confidence**: 0.75 (moderate-high if path-related)

**Common Causes**:

- Unix paths hardcoded (`/tmp/file`)
- Windows vs Linux path separators
- Platform-specific library availability

**Recommended Fix**:

- Use `pathlib.Path` for cross-platform paths
- Use `pytest.tmpdir` instead of hardcoded temp paths
- Add platform skip markers: `@pytest.mark.skipif(sys.platform == "win32")`

---

## Pattern 7: Session-Scoped Fixture Pollution

**Indicators**:

- Error messages: "IntegrityError", "state mismatch", "unexpected value"
- Code patterns: `@pytest.fixture(scope="session")`, shared database fixtures
- Failure timing: Later tests fail (early tests pollute state)

**Confidence**: 0.85 (high if session fixture + state error)

**Common Causes**:

- Session fixtures modified by tests
- Database state not rolled back
- Cached objects retain old data

**Recommended Fix**:

- Reduce fixture scope to function or module
- Use database transaction rollback in fixture teardown
- Make fixtures immutable (return copies, not references)

---

## Pattern 8: Timing-Based Assertions

**Indicators**:

- Error messages: "AssertionError: expected <1s, got 1.02s"
- Code patterns: Time measurements, duration assertions
- Failure timing: Sporadic (depends on CPU load)

**Confidence**: 0.80 (high if time measurement)

**Common Causes**:

- Exact time comparisons on variable-speed systems
- No tolerance for timing variations
- System load affects execution speed

**Recommended Fix**:

- Add tolerance to timing assertions (`assert duration < 1.1`)
- Mock time measurement functions
- Use relative time comparisons, not absolute

---

## Pattern 9: Uncontrolled Concurrency

**Indicators**:

- Error messages: "Race condition", "concurrent modification"
- Code patterns: `threading.Thread`, multiprocessing without synchronization
- Failure timing: Intermittent (depends on thread scheduling)

**Confidence**: 0.90 (very high if threading + intermittent)

**Common Causes**:

- Threads/processes access shared data without locks
- No synchronization primitives (locks, events)
- Test relies on specific execution order

**Recommended Fix**:

- Add proper synchronization (locks, barriers, queues)
- Avoid testing concurrent code with exact ordering expectations
- Use deterministic concurrency testing tools

---

## Pattern 10: Environment Variable Dependencies

**Indicators**:

- Error messages: "KeyError: 'ENV_VAR'", "None type error"
- Code patterns: `os.environ["VAR"]` without default, env-dependent behavior
- Failure timing: Depends on environment setup

**Confidence**: 0.85 (high if env error)

**Common Causes**:

- Tests assume environment variables are set
- No default values for missing env vars
- Different CI vs local environments

**Recommended Fix**:

- Mock environment variables in test setup
- Use `os.environ.get("VAR", "default")`
- Set required env vars in test fixtures

---

## Pattern 11: Async Race Conditions

**Indicators**:

- Error messages: "RuntimeError: Event loop is closed", "asyncio.TimeoutError"
- Code patterns: `asyncio.gather()`, `asyncio.wait_for()`, concurrent async calls
- Failure timing: Inconsistent (depends on async scheduling)

**Confidence**: 0.75 (high if async + timing issues present)

**Common Causes**:

- Missing await statements
- Race between concurrent async operations
- Improper event loop cleanup

**Recommended Fix**:

- Add explicit `await` for all async calls
- Use `asyncio.timeout()` for async operations
- Ensure event loop cleanup in teardown

---

## Pattern 12: Database State Pollution

**Indicators**:

- Error messages: "IntegrityError: UNIQUE constraint failed", "duplicate key value"
- Code patterns: Database commits in setUp/tearDown, shared DB state
- Failure timing: Test order dependent (fails when run after specific tests)

**Confidence**: 0.80 (high if database + order-dependent)

**Common Causes**:

- Incomplete database rollback in tearDown
- Shared database fixtures without isolation
- Foreign key constraints from previous test data

**Recommended Fix**:

- Use transaction rollback in fixtures
- Add database cleanup in tearDown (DELETE FROM or TRUNCATE)
- Isolate tests with separate database schemas or pytest-randomly

---

## Pattern 13: Time-Sensitive Assertions

**Indicators**:

- Error messages: "AssertionError: datetime mismatch", "timestamp off by 1 second"
- Code patterns: `datetime.now()`, `time.time()`, timestamp comparisons
- Failure timing: Sporadic (depends on execution speed)

**Confidence**: 0.85 (very high if datetime + assertion error)

**Common Causes**:

- Comparing exact datetime.now() values
- Not mocking time-dependent functions
- Timezone-aware vs timezone-naive datetime mismatches

**Recommended Fix**:

- Mock datetime.now() with fixed value (unittest.mock.patch)
- Use time ranges instead of exact matches (within 1 second tolerance)
- Use freezegun library for deterministic time testing

---

## Pattern 14: External Service Timeouts

**Indicators**:

- Error messages: "requests.exceptions.Timeout", "ConnectionTimeout", "ReadTimeout"
- Code patterns: HTTP requests, API calls, external service dependencies
- Failure timing: Intermittent (depends on network/service availability)

**Confidence**: 0.70 (moderate-high if network + timeout)

**Common Causes**:

- Tests depend on external services (not mocked)
- Network latency variability
- Service rate limiting or downtime

**Recommended Fix**:

- Mock all external HTTP requests (responses library)
- Use pytest-vcr to record/replay HTTP interactions
- Add timeout controls (requests.get(url, timeout=5))

---

## Pattern 15: Resource Contention

**Indicators**:

- Error messages: "OSError: [Errno 98] Address already in use", "PermissionError: file in use"
- Code patterns: Port binding, file locking, shared resources
- Failure timing: Parallel test execution failures

**Confidence**: 0.75 (high if parallel + resource conflict)

**Common Causes**:

- Tests bind to same port (e.g., Flask test server on port 5000)
- File locking conflicts in parallel execution
- Shared temporary file names

**Recommended Fix**:

- Use dynamic port allocation (port=0, OS assigns random)
- Use pytest-xdist isolation with unique temp directories
- Add file locking with retry logic or unique filenames (uuid)

---

### Framework 4: pytest-rerunfailures Plugin Configuration

**Purpose**: Automatically retry flaky tests to distinguish transient failures from real bugs

**When to Use**:

- In CI/CD pipelines to handle known flaky tests
- During flakiness validation (N-run testing)
- As temporary mitigation while fixing flaky tests
- NOT as permanent solution - fix flaky tests instead

**Components**:

1. **CLI Usage**: `pytest --reruns 5 --reruns-delay 1.5`
2. **Configuration File**: `pytest.ini` with `[pytest] reruns = 3`
3. **Test Marker**: `@pytest.mark.flaky(reruns=5, reruns_delay=2)`
4. **Best Practices**: 3-5 retries, 1-2s delays, quarantine at >15% failure rate

**How to Apply**:

1. Install plugin: `uv add pytest-rerunfailures`
2. Choose configuration method:
   - **CLI**: For ad-hoc validation or specific test runs
   - **pytest.ini**: For project-wide defaults
   - **Marker**: For specific known-flaky tests
3. Configure retry count (3-5) and delay (1-2s)
4. Monitor retry patterns to identify flaky tests
5. Use retry data to prioritize test fixes

**Example from Codebase**:

```python
# pytest.ini configuration
"""
[pytest]
# Global retry settings (conservative)
reruns = 2
reruns_delay = 1

# Markers for known flaky tests
markers =
    flaky: mark test as flaky (retries automatically)
"""

# Test file with marker
"""
import pytest

@pytest.mark.flaky(reruns=5, reruns_delay=2)
def test_network_dependent_operation():
    # Known flaky due to network variability
    result = make_external_api_call()
    assert result.status_code == 200

def test_reliable_unit_test():
    # No marker needed - reliable test
    result = pure_function(1, 2)
    assert result == 3
"""

# CLI usage for validation
"""
# Validate specific test for flakiness
uv run pytest tests/unit/test_auth.py::test_login --reruns 5 --reruns-delay 1.5 -v

# Run all tests with retry
uv run pytest --reruns 3 --reruns-delay 1
"""

# Python API usage
"""
import subprocess

def run_with_retry_validation(test_path: str) -> dict:
    # Run with retries and capture detailed output
    result = subprocess.run(
        ["uv", "run", "pytest", test_path,
         "--reruns", "5",
         "--reruns-delay", "1.5",
         "-v",
         "--tb=short"],
        capture_output=True,
        text=True
    )

    # Parse output for retry information
    output = result.stdout
    rerun_count = output.count("RERUN")
    final_status = "PASSED" if result.returncode == 0 else "FAILED"

    return {
        "status": final_status,
        "rerun_count": rerun_count,
        "is_flaky": rerun_count > 0 and final_status == "PASSED"
    }
"""
```

**Source**: pytest-rerunfailures documentation - https://pypi.org/project/pytest-rerunfailures/

---

## Processes & Workflows

### Workflow 1: Flakiness Detection on Test Failure

**Trigger Conditions**:

- Test fails in test execution
- Failure category uncertain (not obviously TEST_BUG, APP_BUG, or ENV)
- Need to determine if failure is flaky or reliable

**Steps**:

1. **Initial Failure Detection**
   - **Input**: Test execution result with failure
   - **Output**: Failed test identified
   - **Rationale**: Starting point for flakiness investigation

   ```python
   if test_result.status == "FAILED":
       suspect_test = test_result.nodeid
   ```

2. **Execute N-Run Validation**
   - **Input**: Failed test node ID
   - **Output**: Failure rate and outcome list
   - **Rationale**: Measure consistency of failure

   ```python
   failure_rate, outcomes = validate_test_repeatability(
       test_path=suspect_test,
       n_runs=5,
       delay_seconds=1.5
   )
   ```

3. **Classify by Failure Rate**
   - **Input**: Failure rate
   - **Output**: Classification (PASSING, POTENTIALLY_FLAKY, FLAKY, RELIABLY_FAILING)
   - **Rationale**: Determine appropriate action based on consistency

   ```python
   classification = classify_by_failure_rate(failure_rate)
   ```

4. **Make Decision**
   - **Input**: Classification
   - **Output**: Action (quarantine, monitor, delegate_fix, ignore)
   - **Rationale**: Route to appropriate handler

   ```python
   if classification == "FLAKY":
       quarantine_test(suspect_test)
       delegate_to_test_creator(suspect_test, "FLAKY_TEST")
   elif classification == "RELIABLY_FAILING":
       categorize_failure(test_result)
       delegate_fix(test_result)
   elif classification == "POTENTIALLY_FLAKY":
       add_to_monitoring(suspect_test)
   ```

5. **Detect Flakiness Indicators**
   - **Input**: Test source file
   - **Output**: Indicator dictionary with risk score
   - **Rationale**: Identify root cause patterns
   ```python
   test_file = Path(suspect_test.split("::")[0])
   indicators = detector.detect_indicators(test_file)
   risk_score = detector.score_flakiness_risk(indicators)
   ```

**Success Criteria**:

- ✅ Failure rate accurately measured
- ✅ Classification matches test behavior
- ✅ Flakiness indicators identified for root cause analysis

**Failure Handling**:

- If N-run validation times out, reduce n_runs and retry
- If classification uncertain (failure_rate ~15%), increase n_runs to 10
- If indicators detection fails, proceed with classification only

**Example Execution**:

```
Input: test_auth_flow failed once
→ Step 1: Detect failure → suspect_test = "tests/unit/test_auth.py::test_auth_flow"
→ Step 2: N-run validation → 5 runs → outcomes = [False, True, False, True, False]
→ Step 3: Calculate → failure_rate = 3/5 = 0.60 → classification = "FLAKY"
→ Step 4: Quarantine → Add to .pytest_cache/flaky_tests.json
→ Step 5: Detect indicators → timing_issues: ["time.sleep(0.5)"], random_data: ["uuid.uuid4()"]
→ Result: FLAKY test quarantined, delegate to test-creator with indicator context
```

---

### Workflow 2: Indicator-Based Test Quality Audit

**Trigger Conditions**:

- Pre-commit test quality check
- Test suite health audit
- After adding new tests

**Steps**:

1. **Collect Test Files**
   - **Input**: Test directory path
   - **Output**: List of test file paths
   - **Rationale**: Enumerate all tests for scanning

   ```python
   test_files = list(Path("tests/").rglob("test_*.py"))
   ```

2. **Scan for Indicators**
   - **Input**: Test file path
   - **Output**: Indicators dictionary per file
   - **Rationale**: Identify flakiness patterns

   ```python
   all_indicators = {}
   for test_file in test_files:
       indicators = detector.detect_indicators(test_file)
       all_indicators[test_file] = indicators
   ```

3. **Calculate Risk Scores**
   - **Input**: Indicators per file
   - **Output**: Risk score per file
   - **Rationale**: Prioritize high-risk tests

   ```python
   risk_scores = {}
   for file, indicators in all_indicators.items():
       risk_scores[file] = detector.score_flakiness_risk(indicators)
   ```

4. **Prioritize High-Risk Tests**
   - **Input**: Risk scores
   - **Output**: Sorted list of high-risk tests
   - **Rationale**: Focus improvement efforts

   ```python
   high_risk = [
       (file, score) for file, score in risk_scores.items()
       if score >= 0.7
   ]
   high_risk.sort(key=lambda x: x[1], reverse=True)
   ```

5. **Generate Remediation Plan**
   - **Input**: High-risk tests with indicators
   - **Output**: Improvement recommendations per test
   - **Rationale**: Provide actionable fix guidance
   ```python
   for file, score in high_risk:
       indicators = all_indicators[file]
       recommendations = generate_recommendations(indicators)
       report.append({
           "file": file,
           "risk_score": score,
           "recommendations": recommendations
       })
   ```

**Success Criteria**:

- ✅ All test files scanned successfully
- ✅ Risk scores calculated for all tests
- ✅ Remediation plan generated for high-risk tests

**Failure Handling**:

- If file read fails, skip and log warning
- If indicator parsing fails, mark risk as UNKNOWN
- If no high-risk tests, report suite health summary

**Example Execution**:

```
Input: Audit tests/ directory
→ Step 1: Collect → 47 test files found
→ Step 2: Scan → Indicators detected for all files
→ Step 3: Calculate → Risk scores: 5 high (≥0.7), 12 medium (0.4-0.69), 30 low (<0.4)
→ Step 4: Prioritize → Top 5 high-risk tests identified
→ Step 5: Generate plan:
   - test_integration_flow.py (0.85): Remove time.sleep, mock external API, add fixtures
   - test_database_sync.py (0.78): Clean database state, remove shared fixtures
   - test_async_handler.py (0.72): Add proper async synchronization, remove timeouts
→ Result: Remediation plan with 15 specific recommendations
```

---

## Decision Trees

### Decision 1: Flakiness Classification by Failure Rate

```
IF failure_rate == 0.0
  THEN classification = "PASSING"
  ACTION = ignore_initial_failure()
  BECAUSE initial failure was false alarm or transient environment issue

ELSE IF failure_rate <= 0.15 (1 failure in 5-7 runs)
  THEN classification = "POTENTIALLY_FLAKY"
  ACTION = add_to_monitoring() + run_indicator_detection()
  BECAUSE low failure rate may indicate emerging flakiness

ELSE IF 0.15 < failure_rate < 1.0
  THEN classification = "FLAKY"
  ACTION = quarantine_test() + delegate_to_test_creator(reason="FLAKY_TEST")
  BECAUSE inconsistent failure indicates test needs redesign

ELSE IF failure_rate == 1.0
  THEN classification = "RELIABLY_FAILING"
  ACTION = categorize_failure() + delegate_fix()
  BECAUSE consistent failure indicates real bug (test or app)
```

**Example Scenarios**:

1. **Scenario**: 0 failures in 5 runs → **Decision**: PASSING (ignore initial failure, likely environment)
2. **Scenario**: 1 failure in 5 runs (20%) → **Decision**: FLAKY (quarantine, investigate indicators)
3. **Scenario**: 3 failures in 5 runs (60%) → **Decision**: FLAKY (high priority quarantine)
4. **Scenario**: 5 failures in 5 runs (100%) → **Decision**: RELIABLY_FAILING (categorize and delegate fix)

---

### Decision 2: Indicator-Based Risk Assessment

```
IF timing_issues_count >= 2
  THEN risk_category = "HIGH_TIMING_RISK"
  ACTION = recommend_async_synchronization() + remove_sleep_calls()
  BECAUSE multiple timing dependencies indicate race conditions

ELSE IF random_data_count >= 2
  THEN risk_category = "HIGH_NONDETERMINISM_RISK"
  ACTION = recommend_seeding() + mock_random_generation()
  BECAUSE non-deterministic data causes inconsistent test results

ELSE IF shared_state_count >= 1
  THEN risk_category = "HIGH_ISOLATION_RISK"
  ACTION = recommend_fixture_scope_changes() + add_cleanup()
  BECAUSE shared state between tests causes interference

ELSE IF infrastructure_variability_count >= 1
  THEN risk_category = "HIGH_ENVIRONMENT_RISK"
  ACTION = recommend_mocking_externals() + add_dependency_validation()
  BECAUSE external dependencies introduce failure variability

ELSE IF total_indicators >= 5
  THEN risk_category = "HIGH_COMPLEXITY_RISK"
  ACTION = recommend_test_splitting() + simplify_test()
  BECAUSE test complexity increases flakiness probability

ELSE
  THEN risk_category = "LOW_RISK"
  ACTION = no_immediate_action()
  BECAUSE few indicators detected
```

**Example Scenarios**:

1. **Scenario**: Test has `time.sleep(1)`, `time.sleep(0.5)`, `timeout=10` → **Decision**: HIGH_TIMING_RISK - remove sleep calls, use proper waits
2. **Scenario**: Test uses `random.random()`, `uuid.uuid4()`, `datetime.now()` → **Decision**: HIGH_NONDETERMINISM_RISK - seed random, mock uuid, freeze time
3. **Scenario**: Test modifies global variable, uses session-scoped fixture → **Decision**: HIGH_ISOLATION_RISK - reduce fixture scope, clean state

---

## Best Practices

### Practice 1: Statistical N-Run Validation

**Principle**: Use 5+ runs with delays to reliably detect flakiness

**Implementation**:

- Execute test 5 times minimum (10 for high-confidence)
- Add 1-2 second delays between runs to simulate real conditions
- Record all outcomes for failure rate calculation
- Use 15% failure rate as quarantine threshold

**Benefits**:

- ✅ Distinguishes flaky from reliably failing tests
- ✅ Reduces false positives in flakiness detection
- ✅ Provides statistical confidence in classification

**Trade-offs**:

- ⚠️ Increases test execution time (5x minimum)
- ⚠️ May not catch very rare flakiness (1% failure rate)
- ⚠️ Requires infrastructure for parallel execution

**Example**:

```python
# ✅ Correct: Statistical validation with delays
failure_rate, outcomes = validate_test_repeatability(
    test_path="tests/unit/test_auth.py::test_login",
    n_runs=5,
    delay_seconds=1.5
)

if 0.15 < failure_rate < 1.0:
    # Confidently flaky
    quarantine_test(test_path)

# ❌ Wrong: Single retry without delay
result1 = run_test(test_path)
result2 = run_test(test_path)  # No delay!
if result1 != result2:
    quarantine_test(test_path)  # Not enough evidence!
```

---

### Practice 2: Indicator-Driven Root Cause Analysis

**Principle**: Use flakiness indicators to guide test improvement, not just detection

**Implementation**:

- Scan test code for indicator patterns when flakiness detected
- Generate specific recommendations based on indicators found
- Prioritize fixes by indicator severity and frequency
- Track indicator reduction over time

**Benefits**:

- ✅ Provides actionable fix guidance beyond "test is flaky"
- ✅ Enables proactive prevention during test creation
- ✅ Reduces time to fix flaky tests

**Trade-offs**:

- ⚠️ Requires pattern maintenance as new flakiness types emerge
- ⚠️ May miss subtle flakiness causes not captured by patterns
- ⚠️ Static analysis has limits (can't detect runtime issues)

**Example**:

```python
# ✅ Preferred: Indicator-driven remediation
indicators = detector.detect_indicators(test_file)
if indicators["timing_issues"]:
    recommend("Replace time.sleep with proper async synchronization")
if indicators["random_data"]:
    recommend("Add random.seed() or mock UUID generation")
if indicators["shared_state"]:
    recommend("Change fixture scope from session to function")

# ❌ Anti-Pattern: Generic "test is flaky" message
if failure_rate > 0.15:
    report("Test is flaky, fix it")  # No guidance!
```

---

### Practice 3: Quarantine with Monitoring

**Principle**: Isolate flaky tests while fixing them to prevent CI/CD blocking

**Implementation**:

- Move flaky tests to separate pytest marker or directory
- Configure CI to run quarantined tests but not block on failures
- Monitor quarantined tests for fix validation
- Remove from quarantine after 5+ consecutive passes

**Benefits**:

- ✅ Prevents flaky tests from blocking valid deployments
- ✅ Maintains test coverage visibility
- ✅ Enables gradual test suite improvement

**Trade-offs**:

- ⚠️ Risk of ignoring real bugs if quarantine becomes permanent
- ⚠️ Requires discipline to fix quarantined tests
- ⚠️ May reduce perceived test quality metrics

**Example**:

```python
# ✅ Correct: Quarantine with monitoring
# pytest.ini
"""
[pytest]
markers =
    flaky: mark test as flaky (quarantined)
"""

# Test file
"""
@pytest.mark.flaky
def test_unreliable_operation():
    # Known flaky - quarantined while fixing
    ...
"""

# CI configuration
"""
# Run all tests including flaky
pytest --reruns 3 -m ""

# Also run flaky tests separately (non-blocking)
pytest -m flaky --reruns 5 || echo "Flaky tests failed (expected)"
"""

# Dequarantine validation
"""
def validate_dequarantine(test_path: str) -> bool:
    # Verify 10 consecutive passes
    for _ in range(10):
        result = run_test(test_path)
        if not result.passed:
            return False
        time.sleep(1)
    return True
"""

# ❌ Anti-Pattern: Deleting flaky tests
# Don't do this - loses coverage and masks problems!
```

---

## Anti-Patterns

### Anti-Pattern 1: Immediate Quarantine on Single Failure

**Problem**: Quarantining tests after single failure without validation wastes effort and may hide real bugs

**Detection**:

- 🔴 Test quarantined without N-run validation
- 🔴 No failure rate calculation
- 🔴 Growing quarantine list with no fix tracking

**Consequences**:

- ❌ Reliable tests falsely marked as flaky
- ❌ Quarantine becomes dumping ground
- ❌ Real bugs ignored due to false flaky label

**Better Approach**:

```python
✅ Preferred Pattern:
# Validate before quarantine
if test_failed:
    failure_rate, _ = validate_test_repeatability(test_path, n_runs=5)
    if failure_rate > 0.15 and failure_rate < 1.0:
        quarantine_test(test_path)
    elif failure_rate == 1.0:
        categorize_and_delegate_fix(test_path)

❌ Anti-Pattern:
# Immediate quarantine
if test_failed:
    quarantine_test(test_path)  # No validation!
```

**Migration Strategy**:

1. Audit all quarantined tests with N-run validation
2. Dequarantine tests with 100% failure rate (reliably failing)
3. Dequarantine tests with 0% failure rate (false positives)
4. Keep only 1-99% failure rate tests in quarantine

---

### Anti-Pattern 2: Using pytest-rerunfailures as Permanent Solution

**Problem**: Relying on automatic retries instead of fixing flaky tests masks problems and wastes CI time

**Detection**:

- 🔴 Global `--reruns` in CI configuration
- 🔴 High rerun counts (≥5) used routinely
- 🔴 No tracking of which tests retry frequently

**Consequences**:

- ❌ Flaky tests never fixed
- ❌ Increased CI time and costs
- ❌ False sense of test reliability

**Better Approach**:

```python
✅ Preferred Pattern:
# Temporary mitigation with tracking
@pytest.mark.flaky(reruns=3, reruns_delay=1)
@pytest.mark.xfail(reason="Known flaky - fix in progress: ISSUE-123")
def test_unreliable_operation():
    ...

# CI monitors retry usage
"""
pytest --reruns 3 -v | tee test-output.log
grep "RERUN" test-output.log | wc -l  # Alert if >5 reruns
"""

❌ Anti-Pattern:
# Global retries hide problems
"""
# pytest.ini
[pytest]
reruns = 5  # Every test retries 5 times!
"""

# No tracking of retry patterns
"""
# .github/workflows/ci.yml
- run: pytest --reruns 5  # Just retry everything
"""
```

**Migration Strategy**:

1. Remove global `--reruns` from pytest.ini and CI
2. Add `@pytest.mark.flaky` only to known flaky tests
3. Track retry usage to identify tests needing fixes
4. Create tickets for each flaky test with fix deadline

---

## Integration Points

### Integration 1: test-creator Agent

**Relationship**: test-executor detects flaky tests and delegates redesign to test-creator

**Coordination Pattern**:

- test-executor runs tests → detects inconsistent failures → validates flakiness
- test-executor scans test code for flakiness indicators
- test-executor delegates to test-creator with indicators and recommendations
- test-creator redesigns test for reliability (better isolation, mocking, synchronization)
- test-creator returns improved test → test-executor validates with N-run

**Example Usage**:

```python
# test-executor flakiness detection and delegation
failure_rate, outcomes = validate_test_repeatability(test_path, n_runs=5)
if 0.15 < failure_rate < 1.0:
    # Flaky test detected
    test_file = Path(test_path.split("::")[0])
    indicators = detector.detect_indicators(test_file)

    # Delegate to test-creator with context
    test_creator.fix_flaky_test(
        test_path=test_path,
        failure_rate=failure_rate,
        indicators=indicators,
        recommendations=[
            "Remove time.sleep calls",
            "Mock external API",
            "Add fixture cleanup"
        ]
    )

    # Validate improvement
    new_failure_rate, _ = validate_test_repeatability(test_path, n_runs=10)
    if new_failure_rate <= 0.15:
        dequarantine_test(test_path)
```

**Dependencies**:

- test-creator depends on accurate flakiness detection
- test-executor depends on test-creator's redesign quality
- Both share indicator schema and recommendation format

---

### Integration 2: CI/CD Pipeline

**Relationship**: test-executor provides flakiness metrics for CI/CD quality gates

**Coordination Pattern**:

- CI executes test suite via test-executor
- test-executor tracks retry patterns and failure rates
- test-executor reports flakiness metrics to CI
- CI uses metrics for quality gates and alerts

**Example Usage**:

```yaml
# .github/workflows/ci.yml
- name: Run tests with flakiness detection
  run: |
    uv run pytest --reruns 3 --json-report --json-report-file=results.json
    uv run python scripts/analyze_flakiness.py results.json > flakiness-report.json

- name: Check flakiness threshold
  run: |
    flaky_count=$(jq '.flaky_test_count' flakiness-report.json)
    if [ "$flaky_count" -gt 5 ]; then
      echo "Too many flaky tests: $flaky_count"
      exit 1
    fi

- name: Upload flakiness report
  uses: actions/upload-artifact@v3
  with:
    name: flakiness-report
    path: flakiness-report.json
```

**Dependencies**:

- CI depends on test-executor's flakiness detection accuracy
- test-executor depends on CI's execution environment consistency
- Both share flakiness metrics schema

---

## Validation & Quality Checks

### Check 1: Flakiness Detection Accuracy

**What to Validate**: N-run validation correctly identifies flaky vs reliable tests

**Validation Method**:

1. Create labeled dataset of known flaky and reliable tests
2. Run N-run validation on all tests (n=10 for high confidence)
3. Compare classification to ground truth labels
4. Calculate precision (% of flaky classifications that are correct) and recall (% of true flaky tests detected)

**Pass Criteria**: Precision ≥90%, Recall ≥85%
**Fail Criteria**: Precision <80% or Recall <70%

**Remediation**: Adjust failure rate threshold, increase n_runs, validate delay timing

---

### Check 2: Indicator Detection Completeness

**What to Validate**: Indicator patterns cover all common flakiness sources

**Validation Method**:

1. Collect 50+ flaky test examples from history
2. Manually identify root causes
3. Run indicator detection on all examples
4. Measure: What % of root causes were detected by indicators?

**Pass Criteria**: ≥80% of known root causes detected by indicators
**Fail Criteria**: <70% detection rate

**Remediation**: Add missing indicator patterns, refine regex patterns, expand category coverage

---

## Common Pitfalls & Solutions

| Pitfall                        | Detection                                   | Solution                                                   |
| ------------------------------ | ------------------------------------------- | ---------------------------------------------------------- |
| Single-failure quarantine      | Tests quarantined without N-run validation  | Require 5+ run validation before quarantine                |
| Ignoring failure rate = 100%   | Treating reliably failing tests as flaky    | Check for 100% failure rate → delegate fix instead         |
| No indicator context           | Reporting "test is flaky" without guidance  | Scan code for indicators, provide specific recommendations |
| Permanent pytest-rerunfailures | Global reruns in pytest.ini                 | Use markers for specific tests, track retry usage          |
| No dequarantine validation     | Tests stay quarantined forever              | Require 10+ consecutive passes before dequarantine         |
| Missing delay in N-runs        | Back-to-back execution misses timing issues | Add 1-2s delays between validation runs                    |

---

## Tools & Resources

### Recommended Tools

1. **pytest-rerunfailures**
   - **Purpose**: Automatically retry flaky tests for validation
   - **When to Use**: N-run validation, temporary mitigation while fixing
   - **Documentation**: https://pypi.org/project/pytest-rerunfailures/

2. **pytest-flaky**
   - **Purpose**: Mark and track flaky tests with automatic retry
   - **When to Use**: Known flaky tests needing gradual improvement
   - **Documentation**: https://pypi.org/project/pytest-flaky/

3. **pytest-json-report**
   - **Purpose**: Structured output for retry pattern analysis
   - **When to Use**: CI/CD flakiness metrics and trend analysis
   - **Documentation**: https://pypi.org/project/pytest-json-report/

### Learning Resources

1. **Google Testing Blog - Flaky Tests**: https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html
   - **Topic**: Industry analysis of flaky test causes and solutions
   - **Quality**: High

2. **Google Testing Blog - Test Size**: https://testing.googleblog.com/2010/12/test-sizes.html
   - **Topic**: Correlation between test size and flakiness rates
   - **Quality**: High

3. **pytest Best Practices - Flakiness**: https://docs.pytest.org/en/stable/how-to/flaky.html
   - **Topic**: pytest-specific flakiness mitigation techniques
   - **Quality**: High

---

## Glossary

- **Flaky Test**: Test that produces inconsistent results (pass/fail) without code changes
- **Failure Rate**: Percentage of test runs that fail (failures / total_runs)
- **N-Run Validation**: Running test multiple times to measure failure consistency
- **Quarantine**: Isolating flaky tests to prevent blocking CI/CD while fixing
- **Flakiness Indicator**: Code pattern correlated with flaky behavior
- **Dequarantine**: Removing test from quarantine after validation of fix

---

## Sources & References

1. Google Testing Blog - Flaky Tests: https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html
   - Accessed: 2025-10-26
   - Confidence: 0.95

2. Google Testing Blog - Test Sizes: https://testing.googleblog.com/2010/12/test-sizes.html
   - Accessed: 2025-10-26
   - Confidence: 0.95

3. pytest-rerunfailures Plugin: https://pypi.org/project/pytest-rerunfailures/
   - Accessed: 2025-10-26
   - Confidence: 0.90

4. Industry Best Practices - Flaky Test Detection: Research synthesis
   - Accessed: 2025-10-26
   - Confidence: 0.85

---

## Changelog

- **2025-10-26**: Initial documentation created (confidence: 0.90)

---

## Related Documentation

- `.claude/docs/guides/test-executor/development-pytest-framework.md`: pytest execution and exit codes
- `.claude/docs/guides/test-executor/testing-failure-categorization.md`: Failure categorization methodology
- `.claude/docs/guides/test-executor/development-delegation-patterns.md`: Agent delegation decision trees
