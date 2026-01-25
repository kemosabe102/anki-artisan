# Test Failure Categorization Methodology

**Category**: testing
**Domain**: Automated failure classification and root cause analysis
**Confidence**: 0.92
**Last Updated**: 2025-10-26T00:00:00Z
**Agent**: code-quality

---

## Overview

Test failure categorization enables automated agents to classify failures into actionable categories (TEST_BUG, APPLICATION_BUG, ENVIRONMENT) for intelligent delegation to appropriate fix agents. Using pytest result codes, exception patterns, stack trace analysis, and message heuristics, code-quality can automatically route failures without manual triage.

**Key Concepts**:

- **TEST_BUG**: Failures in test code itself (fixture errors, assertion logic, test data issues)
- **APPLICATION_BUG**: Failures in application code under test (business logic, runtime exceptions)
- **ENVIRONMENT**: Infrastructure issues (missing dependencies, configuration, imports)

---

## Core Frameworks

### Framework 1: Failure Category Definitions

**Purpose**: Provide clear semantic definitions for each failure category to enable consistent classification

**When to Use**:

- When analyzing test failure details for categorization
- When documenting failure patterns for knowledge base
- When explaining categorization decisions to users

**Components**:

1. **TEST_BUG (Test Code Failures)**
   - Fixture setup/teardown failures
   - Assertion logic errors (wrong expected values)
   - Test data generation issues
   - Mocking/patching configuration errors
   - Test isolation problems

2. **APPLICATION_BUG (Application Code Failures)**
   - Business logic failures (incorrect behavior)
   - Runtime exceptions in application code
   - Unexpected return values or state
   - Algorithm errors
   - Data validation failures in app code

3. **ENVIRONMENT (Infrastructure Failures)**
   - Import errors (missing modules)
   - Missing dependencies or libraries
   - Configuration file issues
   - Database connection failures
   - External service unavailability

**How to Apply**:

1. Examine failure details (exception type, message, stack trace)
2. Identify origin of failure (test file vs application file)
3. Match characteristics to category definition
4. Assign category with confidence score

**Example from Codebase**:

```python
from enum import Enum
from typing import Literal

class FailureCategory(str, Enum):
    """Test failure categories for automated classification."""
    TEST_BUG = "TEST_BUG"          # Failure in test code
    APPLICATION_BUG = "APPLICATION_BUG"  # Failure in app code
    ENVIRONMENT = "ENVIRONMENT"    # Infrastructure/config issue
    UNKNOWN = "UNKNOWN"            # Cannot determine category

def categorize_by_definition(exception_type: str, origin_file: str) -> FailureCategory:
    """Categorize failure based on exception type and origin."""
    # Environment issues
    if exception_type in ["ImportError", "ModuleNotFoundError"]:
        return FailureCategory.ENVIRONMENT

    # Test code issues
    if origin_file.startswith("tests/") and exception_type in ["FixtureNotFound", "ScopeMismatch"]:
        return FailureCategory.TEST_BUG

    # Application code issues
    if origin_file.startswith("packages/") and exception_type in ["ValueError", "RuntimeError"]:
        return FailureCategory.APPLICATION_BUG

    return FailureCategory.UNKNOWN
```

**Source**: Research synthesis from pytest failure analysis patterns

---

### Framework 2: Automated Categorization Decision Tree

**Purpose**: Provide step-by-step algorithm for automated failure categorization using multiple signals

**When to Use**:

- After test execution when failures detected
- When implementing categorization logic in code-quality
- When validating categorization accuracy

**Components**:

1. **Step 1: Check pytest result code** - E (Error) vs F (Failure) provides first signal
2. **Step 2: Exception type pattern matching** - Map exception types to categories
3. **Step 3: Stack trace origin analysis** - Determine where failure originated
4. **Step 4: Message pattern recognition** - Scan error messages for keywords
5. **Step 5: Manual reproduction fallback** - If automated categorization fails

**How to Apply**:

1. Parse pytest JSON report to extract failure details
2. Execute decision tree steps sequentially
3. Assign category when confidence threshold reached (>0.7)
4. Return UNKNOWN if no confident match after all steps

**Example from Codebase**:

```python
from typing import Dict, Tuple

def categorize_failure_automated(failure: Dict) -> Tuple[FailureCategory, float]:
    """
    Apply decision tree to categorize failure automatically.

    Returns:
        (category, confidence_score)
    """
    confidence = 0.0

    # Step 1: Check pytest result code
    if "setup" in failure and failure["setup"]["outcome"] == "failed":
        # Setup failures typically TEST_BUG (fixture issues)
        return (FailureCategory.TEST_BUG, 0.85)

    # Step 2: Exception type pattern matching
    longrepr = failure.get("call", {}).get("longrepr", "")
    if "ImportError" in longrepr or "ModuleNotFoundError" in longrepr:
        return (FailureCategory.ENVIRONMENT, 0.95)
    elif "FixtureNotFound" in longrepr:
        return (FailureCategory.TEST_BUG, 0.90)

    # Step 3: Stack trace origin analysis
    if "nodeid" in failure:
        test_path = failure["nodeid"]
        if test_path.startswith("tests/"):
            # Failure originated in test file
            if "AssertionError" in longrepr:
                # Need to check assertion origin
                if "packages/" in longrepr:
                    return (FailureCategory.APPLICATION_BUG, 0.80)
                else:
                    return (FailureCategory.TEST_BUG, 0.75)

    # Step 4: Message pattern recognition
    if any(keyword in longrepr for keyword in ["connection refused", "no module", "import"]):
        return (FailureCategory.ENVIRONMENT, 0.85)

    # Step 5: Unable to categorize confidently
    return (FailureCategory.UNKNOWN, 0.0)
```

**Source**: Research synthesis from industry failure categorization best practices

---

### Framework 3: Heuristic Pattern Library (12 Patterns)

**Purpose**: Provide concrete pattern matching rules for common failure scenarios

**When to Use**:

- When implementing exception type classification
- When building message pattern recognition
- When validating categorization logic

**Components**:

**Exception Type Patterns**:

1. `ImportError`, `ModuleNotFoundError` → ENVIRONMENT (0.95 confidence)
2. `FixtureNotFound`, `ScopeMismatch` → TEST_BUG (0.90 confidence)

3. **`AssertionError` (Context-Dependent)**
   - **Base Confidence**: 0.60 (REDUCED from 0.75 - context-dependent)

   **High Confidence Conditions** (0.75+):
   - Stack trace shows assertion in `packages/**` (not `tests/**`)
   - Recent code changes in failing function (git log shows commits)
   - Test previously passed (regression indicator)

   **Low Confidence Conditions** (<0.60):
   - Stack trace in both test and app code (unclear boundary)
   - Test recently created (may have wrong expected value)
   - No recent app code changes (suggests test error)

   **Disambiguation**: Use git history to determine likely source (application vs test)

4. `RuntimeError` in app code → APPLICATION_BUG (0.75 confidence)

5. **`ValueError`, `TypeError` (Context-Dependent)**
   - **Base Confidence**: 0.55 (REDUCED from 0.80 - highly context-dependent)

   **High Confidence Conditions** (0.70+):
   - Stack trace clearly in application code (not test setup)
   - Error message shows business logic failure (e.g., "invalid customer ID")
   - Type error on function parameter (not pytest fixture)

   **Low Confidence Conditions** (<0.55):
   - Error in test fixture setup (indicates test configuration issue)
   - Type error on mock/patch objects (test framework issue)
   - Unclear whether test or app is source

   **Disambiguation**: Check if error occurs during test setup (TEST_BUG) or business logic execution (APPLICATION_BUG)

**Stack Trace Origin Patterns**: 6. Failure in `test_*.py` with no app code in trace → TEST_BUG (0.85 confidence) 7. Failure in `packages/**/*.py` → APPLICATION_BUG (0.85 confidence) 8. Failure in fixture function → TEST_BUG (0.90 confidence)

**Message Pattern Patterns**: 9. "connection refused", "timeout", "unreachable" → ENVIRONMENT (0.85 confidence) 10. "fixture not found", "wrong scope" → TEST_BUG (0.90 confidence) 11. "expected X but got Y" + origin in app → APPLICATION_BUG (0.80 confidence) 12. "no module named", "cannot import" → ENVIRONMENT (0.95 confidence)

---

### Confidence Calibration Methodology

**Purpose**: Provide guidance for adjusting confidence scores based on contextual factors

**When to Use**:

- When automated categorization returns ambiguous results
- When implementing context-dependent pattern matching
- When validating categorization accuracy

**Context-Dependent Patterns**:

- **Pattern 3 (AssertionError)**: 0.60 baseline, adjust ±0.15 based on conditions
- **Pattern 5 (TypeError/ValueError)**: 0.55 baseline, adjust ±0.15 based on conditions

**Calibration Factors**:

1. **Stack Trace Location** (+0.15 if clearly in app code, -0.10 if in test code)
2. **Git History** (+0.10 if recent app changes, +0.05 if test changes)
3. **Test Age** (-0.10 if test created <1 week ago)
4. **Previous Pass Rate** (+0.15 if test passed before, indicates regression)

**Confidence Ranges & Actions**:

- **0.80-1.0** (Very Confident): Categorize immediately, proceed with delegation
- **0.60-0.79** (Confident): Categorize with explanatory notes, proceed cautiously
- **0.40-0.59** (Uncertain): Provide both candidate categories, escalate to user
- **0.00-0.39** (Very Uncertain): Flag as MANUAL_REVIEW_NEEDED, do not auto-categorize

**Example Calibration**:

```python
# Base pattern match: AssertionError → 0.60 confidence
base_confidence = 0.60

# Apply calibration factors
if "packages/" in stack_trace and "tests/" not in stack_trace:
    base_confidence += 0.15  # Clear app code origin
if recent_git_changes_in_app_code():
    base_confidence += 0.10  # Recent changes suggest regression
if test_previously_passed():
    base_confidence += 0.15  # Regression indicator

# Final confidence: 0.60 + 0.15 + 0.10 + 0.15 = 1.00 (capped)
final_confidence = min(1.0, base_confidence)
# Result: APPLICATION_BUG with 1.00 confidence
```

**Validation Strategy**:

1. Track categorization accuracy by confidence bucket
2. Adjust calibration factors if bucket accuracy diverges >10% from confidence midpoint
3. Review MANUAL_REVIEW_NEEDED cases to identify missing patterns

---

**How to Apply**:

1. Extract exception type, stack trace, and message from failure
2. Check patterns in order of confidence (highest first)
3. Return first pattern match with confidence >0.7
4. Combine multiple weak signals if single pattern insufficient

**Example from Codebase**:

```python
import re
from typing import Dict, Optional, Tuple

class FailureCategorizer:
    """Apply heuristic patterns for failure categorization."""

    # Exception type patterns (pattern → category, confidence)
    EXCEPTION_PATTERNS = {
        r"ImportError|ModuleNotFoundError": (FailureCategory.ENVIRONMENT, 0.95),
        r"FixtureNotFound|ScopeMismatch": (FailureCategory.TEST_BUG, 0.90),
        r"ValueError|TypeError": (FailureCategory.APPLICATION_BUG, 0.70),  # Context-dependent
    }

    # Message patterns (pattern → category, confidence)
    MESSAGE_PATTERNS = {
        r"connection refused|timeout|unreachable": (FailureCategory.ENVIRONMENT, 0.85),
        r"fixture not found|wrong scope": (FailureCategory.TEST_BUG, 0.90),
        r"no module named|cannot import": (FailureCategory.ENVIRONMENT, 0.95),
    }

    def categorize(self, failure: Dict) -> Tuple[FailureCategory, float]:
        """Apply heuristic patterns to categorize failure."""
        longrepr = failure.get("call", {}).get("longrepr", "")

        # Check exception type patterns
        for pattern, (category, confidence) in self.EXCEPTION_PATTERNS.items():
            if re.search(pattern, longrepr, re.IGNORECASE):
                # Check stack trace origin for context-dependent patterns
                if category == FailureCategory.APPLICATION_BUG:
                    if "packages/" in longrepr:
                        return (category, confidence + 0.1)  # Boost confidence
                    elif "test_" in longrepr:
                        return (FailureCategory.TEST_BUG, 0.70)
                return (category, confidence)

        # Check message patterns
        for pattern, (category, confidence) in self.MESSAGE_PATTERNS.items():
            if re.search(pattern, longrepr, re.IGNORECASE):
                return (category, confidence)

        return (FailureCategory.UNKNOWN, 0.0)
```

**Source**: Research synthesis from pytest failure analysis patterns, industry best practices

---

## Processes & Workflows

### Workflow 1: End-to-End Failure Categorization

**Trigger Conditions**:

- Test execution completed with failures (exit code 1)
- pytest JSON report available for parsing

**Steps**:

1. **Parse Failure Details**
   - **Input**: pytest JSON report path
   - **Output**: List of failure dictionaries with exception, stack trace, nodeid
   - **Rationale**: Extract structured information for analysis

   ```python
   failures = parse_pytest_json_report("results.json")
   ```

2. **Apply Decision Tree**
   - **Input**: Failure details dictionary
   - **Output**: (FailureCategory, confidence_score)
   - **Rationale**: Use multi-step algorithm for robust categorization

   ```python
   for failure in failures:
       category, confidence = categorize_failure_automated(failure)
   ```

3. **Validate Confidence**
   - **Input**: Confidence score
   - **Output**: Accept (≥0.7) or Reject (<0.7) categorization
   - **Rationale**: Only use categorization if sufficiently confident

   ```python
   if confidence >= 0.7:
       accepted_categories.append((failure, category))
   else:
       manual_review_required.append(failure)
   ```

4. **Group by Category**
   - **Input**: List of (failure, category) tuples
   - **Output**: Dictionary mapping category → failures
   - **Rationale**: Enable batch delegation to appropriate agents

   ```python
   grouped = {
       FailureCategory.TEST_BUG: [],
       FailureCategory.APPLICATION_BUG: [],
       FailureCategory.ENVIRONMENT: []
   }
   for failure, category in accepted_categories:
       grouped[category].append(failure)
   ```

5. **Generate Delegation Plan**
   - **Input**: Grouped failures
   - **Output**: Delegation instructions for orchestrator
   - **Rationale**: Route each category to appropriate fix agent
   ```python
   delegations = []
   if grouped[FailureCategory.APPLICATION_BUG]:
       delegations.append({
           "agent": "debugger",
           "failures": grouped[FailureCategory.APPLICATION_BUG]
       })
   if grouped[FailureCategory.TEST_BUG]:
       delegations.append({
           "agent": "code-quality",
           "failures": grouped[FailureCategory.TEST_BUG]
       })
   ```

**Success Criteria**:

- ✅ All failures categorized with confidence ≥0.7
- ✅ Delegation plan generated for all categories
- ✅ No uncategorized failures

**Failure Handling**:

- If confidence <0.7, add to manual review queue
- If categorization contradicts multiple heuristics, escalate to user
- If unknown failure pattern, log for knowledge base expansion

**Example Execution**:

```
Input: results.json with 5 test failures
→ Step 1: Parse → 5 failure dictionaries extracted
→ Step 2: Categorize:
   - test_auth_flow: APPLICATION_BUG (0.85)
   - test_fixture_setup: TEST_BUG (0.90)
   - test_import_module: ENVIRONMENT (0.95)
   - test_validation: APPLICATION_BUG (0.80)
   - test_complex_scenario: UNKNOWN (0.45)
→ Step 3: Validate → 4 accepted, 1 manual review
→ Step 4: Group → {APP_BUG: 2, TEST_BUG: 1, ENV: 1}
→ Step 5: Delegate → debugger (2), code-quality (1), orchestrator (1)
```

---

### Workflow 2: Heuristic Pattern Application

**Trigger Conditions**:

- Single failure needs categorization
- Automated decision tree requires pattern matching

**Steps**:

1. **Extract Signals**
   - **Input**: Failure dictionary from pytest JSON
   - **Output**: Extracted signals (exception_type, stack_trace, message, origin_file)
   - **Rationale**: Isolate key information for pattern matching

   ```python
   longrepr = failure.get("call", {}).get("longrepr", "")
   exception_type = extract_exception_type(longrepr)
   stack_trace = extract_stack_trace(longrepr)
   origin_file = failure.get("nodeid", "").split("::")
   ```

2. **Apply Exception Patterns**
   - **Input**: Exception type
   - **Output**: Optional (category, confidence)
   - **Rationale**: Exception type is strongest signal

   ```python
   for pattern, (category, confidence) in EXCEPTION_PATTERNS.items():
       if re.match(pattern, exception_type):
           return (category, confidence)
   ```

3. **Apply Stack Trace Patterns**
   - **Input**: Stack trace, origin file
   - **Output**: Optional (category, confidence)
   - **Rationale**: Origin location provides context

   ```python
   if origin_file.startswith("packages/"):
       return (FailureCategory.APPLICATION_BUG, 0.85)
   elif origin_file.startswith("tests/"):
       return (FailureCategory.TEST_BUG, 0.80)
   ```

4. **Apply Message Patterns**
   - **Input**: Error message
   - **Output**: Optional (category, confidence)
   - **Rationale**: Message keywords provide additional context

   ```python
   for pattern, (category, confidence) in MESSAGE_PATTERNS.items():
       if re.search(pattern, longrepr, re.IGNORECASE):
           return (category, confidence)
   ```

5. **Combine Weak Signals**
   - **Input**: Multiple weak matches (confidence 0.5-0.69)
   - **Output**: Combined (category, confidence)
   - **Rationale**: Multiple weak signals can form strong conclusion
   ```python
   if len(weak_matches) >= 2 and all(m[0] == weak_matches[0][0] for m in weak_matches):
       # All weak signals agree on category
       combined_confidence = min(0.75, sum(m[1] for m in weak_matches) / len(weak_matches) + 0.1)
       return (weak_matches[0][0], combined_confidence)
   ```

**Success Criteria**:

- ✅ At least one pattern match with confidence ≥0.7
- ✅ Pattern application order optimized (highest confidence first)
- ✅ Consistent categorization across similar failures

**Failure Handling**:

- If no pattern match, return (UNKNOWN, 0.0)
- If conflicting patterns, return highest confidence match
- If weak signals don't combine to ≥0.7, return (UNKNOWN, max_weak_confidence)

**Example Execution**:

```
Failure: test_database_connection failed with "connection refused"
→ Step 1: Extract → exception="ConnectionError", message="connection refused"
→ Step 2: Exception pattern → No strong match
→ Step 3: Stack trace → origin="tests/test_db.py" → TEST_BUG (0.60)
→ Step 4: Message pattern → "connection refused" → ENVIRONMENT (0.85)
→ Step 5: Skip (have strong signal)
→ Result: ENVIRONMENT (0.85)
```

---

## Decision Trees

### Decision 1: Primary Categorization Logic

```
IF pytest_result_code == "E" (Error in setup/teardown)
  THEN category = TEST_BUG
  BECAUSE setup/teardown failures indicate test infrastructure issues
  CONFIDENCE = 0.85

ELSE IF exception_type IN ["ImportError", "ModuleNotFoundError"]
  THEN category = ENVIRONMENT
  BECAUSE import failures are infrastructure issues
  CONFIDENCE = 0.95

ELSE IF exception_type == "FixtureNotFound"
  THEN category = TEST_BUG
  BECAUSE fixture issues are test code problems
  CONFIDENCE = 0.90

ELSE IF origin_file.startswith("packages/") AND exception_type IN ["ValueError", "RuntimeError"]
  THEN category = APPLICATION_BUG
  BECAUSE runtime exceptions in app code are application bugs
  CONFIDENCE = 0.80

ELSE IF origin_file.startswith("tests/") AND exception_type == "AssertionError"
  THEN analyze_assertion_origin()
    IF assertion_on_app_behavior
      THEN category = APPLICATION_BUG
      CONFIDENCE = 0.75
    ELSE
      THEN category = TEST_BUG
      CONFIDENCE = 0.70

ELSE IF message_contains(["connection", "timeout", "unreachable"])
  THEN category = ENVIRONMENT
  BECAUSE connectivity issues are infrastructure
  CONFIDENCE = 0.85

ELSE
  THEN category = UNKNOWN
  CONFIDENCE = 0.0
  ACTION = escalate_to_manual_review()
```

**Example Scenarios**:

1. **Scenario**: pytest returns "E" for fixture setup failure → **Decision**: TEST_BUG (0.85) - fixture issues are test code problems
2. **Scenario**: ImportError raised in packages/core/auth.py → **Decision**: ENVIRONMENT (0.95) - missing dependency
3. **Scenario**: AssertionError in test_auth.py asserting app behavior → **Decision**: APPLICATION_BUG (0.75) - app not behaving as expected
4. **Scenario**: ValueError raised in packages/core/validator.py → **Decision**: APPLICATION_BUG (0.80) - app logic error

---

### Decision 2: Assertion Origin Analysis

```
IF exception_type == "AssertionError"
  THEN extract_assertion_details()

  IF stack_trace_includes("packages/")
    THEN category = APPLICATION_BUG
    BECAUSE failure is in application code behavior
    CONFIDENCE = 0.80

  ELSE IF assertion_message_contains(["expected", "but got", "should be"])
    THEN analyze_expected_vs_actual()
      IF expected_value_from_app_code
        THEN category = APPLICATION_BUG
        BECAUSE app returning wrong value
        CONFIDENCE = 0.75
      ELSE IF expected_value_hardcoded_in_test
        THEN category = TEST_BUG
        BECAUSE test expectation may be wrong
        CONFIDENCE = 0.65

  ELSE IF assertion_on_mock_call
    THEN category = TEST_BUG
    BECAUSE mock assertions are test code validation
    CONFIDENCE = 0.70

  ELSE
    THEN category = UNKNOWN
    CONFIDENCE = 0.40
    ACTION = require_manual_review()
```

**Example Scenarios**:

1. **Scenario**: AssertionError on `assert result.status == "active"` where result from app → **Decision**: APPLICATION_BUG (0.75) - app returning wrong status
2. **Scenario**: AssertionError on `mock_api.assert_called_once()` → **Decision**: TEST_BUG (0.70) - mock validation in test
3. **Scenario**: AssertionError with unclear context → **Decision**: UNKNOWN (0.40) - needs manual review

---

## Best Practices

### Practice 1: Confidence Threshold Enforcement

**Principle**: Only use automated categorization when confidence ≥0.7 to maintain accuracy

**Implementation**:

- Set explicit confidence threshold constant
- Return UNKNOWN for low-confidence categorizations
- Track categorization accuracy metrics
- Escalate low-confidence cases to manual review

**Benefits**:

- ✅ Prevents incorrect delegations
- ✅ Maintains system reliability
- ✅ Identifies edge cases for pattern expansion

**Trade-offs**:

- ⚠️ May require manual review for complex cases
- ⚠️ Some failures remain uncategorized initially
- ⚠️ Need human feedback loop for learning

**Example**:

```python
# ✅ Correct: Enforce confidence threshold
CONFIDENCE_THRESHOLD = 0.7

category, confidence = categorize_failure(failure)
if confidence >= CONFIDENCE_THRESHOLD:
    delegate_to_agent(category, failure)
else:
    manual_review_queue.append(failure)

# ❌ Wrong: Use categorization regardless of confidence
category, confidence = categorize_failure(failure)
delegate_to_agent(category, failure)  # May be wrong!
```

---

### Practice 2: Multi-Signal Combination

**Principle**: Combine multiple weak signals to reach confident categorization

**Implementation**:

- Collect all pattern matches with confidence scores
- If multiple weak signals agree on category, combine confidence
- Apply weighted combination formula: `combined = min(0.75, average(confidences) + 0.1)`
- Require at least 2 agreeing signals for combination

**Benefits**:

- ✅ Reduces UNKNOWN categorizations
- ✅ Leverages complementary information
- ✅ More robust than single-signal decisions

**Trade-offs**:

- ⚠️ More complex logic
- ⚠️ Risk of false confidence boost
- ⚠️ Requires validation of combination formula

**Example**:

```python
# ✅ Preferred: Combine weak signals
weak_matches = []
if exception_type == "AssertionError":  # Confidence: 0.60
    weak_matches.append((FailureCategory.APPLICATION_BUG, 0.60))
if "packages/" in stack_trace:  # Confidence: 0.65
    weak_matches.append((FailureCategory.APPLICATION_BUG, 0.65))

if len(weak_matches) >= 2 and all(m[0] == weak_matches[0][0] for m in weak_matches):
    avg_conf = sum(m[1] for m in weak_matches) / len(weak_matches)
    combined_confidence = min(0.75, avg_conf + 0.1)  # 0.725 → 0.72
    if combined_confidence >= 0.7:
        category = weak_matches

# ❌ Anti-Pattern: Ignore weak signals
if confidence < 0.7:
    return UNKNOWN  # Loses valuable information!
```

---

## Anti-Patterns

### Anti-Pattern 1: Exception Type Only Categorization

**Problem**: Relying solely on exception type without context leads to misclassification

**Detection**:

- 🔴 AssertionError always categorized as TEST_BUG
- 🔴 ValueError always categorized as APPLICATION_BUG
- 🔴 No stack trace or message analysis

**Consequences**:

- ❌ AssertionErrors on app behavior marked as TEST_BUG
- ❌ ValueErrors in test fixtures marked as APPLICATION_BUG
- ❌ High false positive rate in categorization

**Better Approach**:

```python
✅ Preferred Pattern:
# Context-aware categorization
if exception_type == "AssertionError":
    # Check stack trace for origin
    if "packages/" in stack_trace:
        category = APPLICATION_BUG  # App behavior assertion
    else:
        category = TEST_BUG  # Test logic assertion

❌ Anti-Pattern:
# Exception type only
if exception_type == "AssertionError":
    category = TEST_BUG  # Always! Wrong!
```

**Migration Strategy**:

1. Audit existing categorization logic for context-free decisions
2. Add stack trace analysis to exception type patterns
3. Implement assertion origin analysis for AssertionError
4. Validate accuracy with historical failure data

---

### Anti-Pattern 2: Ignoring Confidence Scores

**Problem**: Using categorization results without checking confidence leads to incorrect delegations

**Detection**:

- 🔴 No confidence threshold checks
- 🔴 UNKNOWN category treated same as confident categories
- 🔴 Low-confidence results used for delegation

**Consequences**:

- ❌ Incorrect delegations waste agent time
- ❌ Fixes applied to wrong areas
- ❌ User trust eroded by wrong categorizations

**Better Approach**:

```python
✅ Preferred Pattern:
category, confidence = categorize_failure(failure)
if confidence >= 0.7:
    delegate_to_agent(category, failure)
elif confidence >= 0.5:
    suggest_category_to_user(category, failure, confidence)
else:
    require_manual_categorization(failure)

❌ Anti-Pattern:
category, confidence = categorize_failure(failure)
delegate_to_agent(category, failure)  # No confidence check!
```

**Migration Strategy**:

1. Add CONFIDENCE_THRESHOLD constant to codebase
2. Insert confidence checks before all delegation decisions
3. Create manual review queue for low-confidence cases
4. Track categorization accuracy by confidence bucket

---

## Integration Points

### Integration 1: debugger Agent

**Relationship**: code-quality categorizes APPLICATION_BUG failures and delegates to debugger

**Coordination Pattern**:

- code-quality runs tests → detects failures → categorizes as APPLICATION_BUG
- code-quality extracts failure details (file, function, error, stack trace)
- code-quality delegates to debugger with structured failure information
- debugger applies hypothesis-driven debugging → fixes app code
- debugger returns to code-quality for re-validation

**Example Usage**:

```python
# code-quality categorization and delegation
failures = parse_pytest_json_report("results.json")
for failure in failures:
    category, confidence = categorize_failure(failure)
    if category == FailureCategory.APPLICATION_BUG and confidence >= 0.7:
        debugger.fix_application_bug(
            file=extract_file_from_trace(failure),
            function=extract_function_from_trace(failure),
            error_message=failure["call"]["longrepr"],
            stack_trace=failure["call"]["traceback"]
        )
```

**Dependencies**:

- debugger depends on accurate APPLICATION_BUG categorization
- code-quality depends on debugger's fix quality for re-validation
- Both share failure detail schema (file, function, error, stack_trace)

---

### Integration 2: code-quality Agent

**Relationship**: code-quality categorizes TEST_BUG failures and delegates to code-quality

**Coordination Pattern**:

- code-quality runs tests → detects failures → categorizes as TEST_BUG
- code-quality identifies test redesign needs (fixture issues, assertion logic)
- code-quality delegates to code-quality with test improvement recommendations
- code-quality redesigns test code → returns improved tests
- code-quality re-runs to validate improvements

**Example Usage**:

```python
# code-quality categorization and delegation
for failure in failures:
    category, confidence = categorize_failure(failure)
    if category == FailureCategory.TEST_BUG and confidence >= 0.7:
        if "FixtureNotFound" in failure["longrepr"]:
            test_creator.fix_fixture_issue(
                test_file=failure["nodeid"].split("::")[0],
                fixture_name=extract_fixture_name(failure),
                error=failure["longrepr"]
            )
        elif "AssertionError" in failure["longrepr"] and "mock" in failure["longrepr"]:
            test_creator.fix_assertion_logic(
                test_file=failure["nodeid"].split("::")[0],
                test_function=failure["nodeid"].split("::")[1],
                assertion=extract_assertion(failure)
            )
```

**Dependencies**:

- code-quality depends on accurate TEST_BUG categorization
- code-quality depends on code-quality's redesign quality
- Both share test file schema and fixture conventions

---

### Integration 3: Orchestrator (ENVIRONMENT Failures)

**Relationship**: code-quality categorizes ENVIRONMENT failures and escalates to orchestrator

**Coordination Pattern**:

- code-quality runs tests → detects failures → categorizes as ENVIRONMENT
- code-quality identifies infrastructure needs (missing deps, config)
- code-quality escalates to orchestrator with installation/configuration instructions
- orchestrator installs dependencies or fixes configuration
- orchestrator returns to code-quality for re-validation

**Example Usage**:

```python
# code-quality categorization and escalation
for failure in failures:
    category, confidence = categorize_failure(failure)
    if category == FailureCategory.ENVIRONMENT and confidence >= 0.7:
        if "ModuleNotFoundError" in failure["longrepr"]:
            module_name = extract_module_name(failure)
            orchestrator.install_dependency(
                module=module_name,
                error=failure["longrepr"]
            )
        elif "connection refused" in failure["longrepr"]:
            orchestrator.check_infrastructure(
                service=extract_service_name(failure),
                error=failure["longrepr"]
            )
```

**Dependencies**:

- orchestrator depends on accurate ENVIRONMENT categorization
- code-quality depends on orchestrator's fix capability
- Both share dependency and configuration schemas

---

## Validation & Quality Checks

### Check 1: Categorization Accuracy Validation

**What to Validate**: Categorization results match ground truth for known failures

**Validation Method**:

1. Create labeled dataset of 50+ historical failures with known categories
2. Run categorization logic on labeled dataset
3. Calculate accuracy: `correct_categorizations / total_failures`
4. Analyze false positives and false negatives by category

**Pass Criteria**: Accuracy ≥90% for confidence ≥0.7 categorizations
**Fail Criteria**: Accuracy <80% or high false positive rate in any category

**Remediation**: Adjust heuristic patterns, add missing patterns, retrain on failures

---

### Check 2: Confidence Calibration Validation

**What to Validate**: Confidence scores accurately reflect categorization correctness

**Validation Method**:

1. Group categorizations by confidence bucket (0.7-0.79, 0.8-0.89, 0.9-1.0)
2. Calculate accuracy within each bucket
3. Compare bucket accuracy to expected accuracy (should match confidence)
4. Identify overconfident or underconfident patterns

**Pass Criteria**: Bucket accuracy within 5% of confidence midpoint
**Fail Criteria**: Any bucket with >10% accuracy divergence from confidence

**Remediation**: Adjust confidence scores for patterns, recalibrate combination formula

---

## Common Pitfalls & Solutions

| Pitfall                                            | Detection                                         | Solution                                                          |
| -------------------------------------------------- | ------------------------------------------------- | ----------------------------------------------------------------- |
| AssertionError always marked TEST_BUG              | Check categorization without stack trace analysis | Add assertion origin analysis to distinguish app vs test failures |
| Low confidence categorizations used for delegation | No threshold checks before delegation             | Enforce 0.7 confidence threshold, create manual review queue      |
| Ignoring pytest result code (E vs F)               | Only using exception type for categorization      | Add result code as first signal in decision tree                  |
| Single-signal categorization                       | Only checking exception type or only stack trace  | Implement multi-signal combination for weak matches               |
| Not tracking categorization accuracy               | No validation metrics                             | Create labeled dataset and measure accuracy by category           |

---

## Tools & Resources

### Recommended Tools

1. **pytest-json-report**
   - **Purpose**: Provides structured failure details for categorization
   - **When to Use**: All test executions requiring categorization
   - **Documentation**: https://pypi.org/project/pytest-json-report/

2. **Confusion Matrix Analysis**
   - **Purpose**: Validate categorization accuracy with precision/recall metrics
   - **When to Use**: When building or improving categorization logic
   - **Documentation**: scikit-learn metrics

### Learning Resources

1. **Google Testing Blog - Test Categorization**: https://testing.googleblog.com/
   - **Topic**: Industry practices for test failure analysis
   - **Quality**: High

2. **pytest Failure Analysis Patterns**: https://docs.pytest.org/en/stable/how-to/failures.html
   - **Topic**: Understanding pytest failure modes and result codes
   - **Quality**: High

---

## Glossary

- **TEST_BUG**: Failure in test code itself (fixtures, assertions, test data)
- **APPLICATION_BUG**: Failure in application code under test (business logic, runtime exceptions)
- **ENVIRONMENT**: Infrastructure failure (dependencies, configuration, connectivity)
- **Confidence Score**: Float 0.0-1.0 indicating certainty of categorization
- **Heuristic Pattern**: Regex or condition matching failure characteristics to categories
- **Stack Trace Origin**: Source file location where failure originated

---

## Sources & References

1. pytest Result Codes Documentation: https://docs.pytest.org/en/stable/how-to/failures.html
   - Accessed: 2025-10-26
   - Confidence: 0.95

2. Google Testing Blog - Test Flakiness: https://testing.googleblog.com/
   - Accessed: 2025-10-26
   - Confidence: 0.90

3. Industry Best Practices - Failure Categorization: Research synthesis
   - Accessed: 2025-10-26
   - Confidence: 0.85

---

## Changelog

- **2025-10-26**: Initial documentation created (confidence: 0.92)

---

## Related Documentation

- `.claude/docs/guides/code-quality/development-pytest-framework.md`: pytest execution and exit codes
- `.claude/docs/guides/code-quality/testing-flaky-detection.md`: Flaky test detection techniques
- `.claude/docs/guides/code-quality/development-delegation-patterns.md`: Agent delegation decision trees
