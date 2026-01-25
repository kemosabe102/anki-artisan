# Test Executor Delegation Examples

**Purpose**: Show orchestrator how to delegate to test-executor

---

## Example 1: Basic Test Execution

### Delegation

```
Task(test-executor, "Run tests in tests/unit/ and categorize any failures")
```

### Context Provided

```json
{
  "operation_type": "execute_tests",
  "test_paths": ["tests/unit/"],
  "execution_timestamp": "2025-10-27T10:00:00Z"
}
```

### Expected Output

```json
{
  "status": "SUCCESS",
  "agent": "test-executor",
  "confidence": 0.92,
  "agent_specific_output": {
    "execution_summary": {
      "total_tests": 47,
      "passed": 45,
      "failed": 2,
      "exit_code": 1
    },
    "framework_detected": "pytest",
    "command_executed": "AGENT_NAME=test-executor pytest tests/unit/ -v",
    "failures": [
      {
        "test_name": "tests/unit/test_auth.py::test_login",
        "category": "APPLICATION_BUG",
        "confidence": 0.85,
        "error_message": "AssertionError: expected 'active' but got 'pending'"
      },
      {
        "test_name": "tests/unit/test_auth.py::test_logout",
        "category": "TEST_BUG",
        "confidence": 0.78,
        "error_message": "FixtureNotFound: mock_session"
      }
    ],
    "delegation_summary": {
      "primary_category": "APPLICATION_BUG",
      "failure_count": 2,
      "delegation_confidence": 0.82
    },
    "delegation_recommendations": [
      {
        "category": "APPLICATION_BUG",
        "next_step": "Investigate and fix logic error in auth module",
        "priority": "high",
        "rationale": "Login status not being set correctly",
        "affected_tests": ["tests/unit/test_auth.py::test_login"]
      },
      {
        "category": "TEST_BUG",
        "next_step": "Fix missing fixture definition",
        "priority": "medium",
        "rationale": "mock_session fixture not defined in conftest",
        "affected_tests": ["tests/unit/test_auth.py::test_logout"]
      }
    ]
  }
}
```

---

## Example 2: Fix Failing Tests

### Delegation

```
Task(test-executor, "Fix failing tests in tests/unit/test_auth.py using 3-attempt OODA loop")
```

### Context Provided

```json
{
  "operation_type": "fix_failing_tests",
  "test_paths": ["tests/unit/test_auth.py::test_login", "tests/unit/test_auth.py::test_logout"],
  "execution_timestamp": "2025-10-27T10:05:00Z"
}
```

### Expected Output

```json
{
  "status": "SUCCESS",
  "agent": "test-executor",
  "confidence": 0.88,
  "agent_specific_output": {
    "execution_summary": {
      "total_tests": 2,
      "fixed": 1,
      "unfixable": 1
    },
    "fixed_tests": [
      {
        "test_name": "tests/unit/test_auth.py::test_login",
        "attempts": 1,
        "fix_type": "assertion_update",
        "fix_description": "Updated expected status from 'active' to 'pending' to match new auth flow"
      }
    ],
    "unfixable_tests": [
      {
        "test_name": "tests/unit/test_auth.py::test_logout",
        "attempts": 3,
        "attempt_history": [
          {"attempt": 1, "action": "Created mock_session fixture", "result": "New error: AttributeError"},
          {"attempt": 2, "action": "Fixed fixture scope", "result": "Same error persists"},
          {"attempt": 3, "action": "Researched via Context7", "result": "Complex dependency issue"}
        ],
        "final_error": "AttributeError: 'NoneType' object has no attribute 'invalidate'",
        "research_tried": true,
        "recommendation": "Manual investigation required - complex session lifecycle issue"
      }
    ],
    "delegation_recommendations": [
      {
        "category": "TEST_BUG",
        "next_step": "Manual investigation of session lifecycle in logout test",
        "priority": "high",
        "rationale": "3 fix attempts failed, complex dependency issue",
        "affected_tests": ["tests/unit/test_auth.py::test_logout"]
      }
    ]
  }
}
```

---

## Example 3: Coverage Analysis

### Delegation

```
Task(test-executor, "Run tests with coverage and identify gaps in packages/core/")
```

### Context Provided

```json
{
  "operation_type": "analyze_coverage",
  "test_paths": ["tests/"],
  "coverage_target": "packages/core/",
  "execution_timestamp": "2025-10-27T10:10:00Z"
}
```

### Expected Output

```json
{
  "status": "SUCCESS",
  "agent": "test-executor",
  "confidence": 0.95,
  "agent_specific_output": {
    "execution_summary": {
      "total_tests": 120,
      "passed": 120,
      "failed": 0,
      "exit_code": 0
    },
    "coverage_gaps": [
      {
        "file": "packages/core/auth/session.py",
        "functions": ["refresh_token", "validate_expiry"],
        "lines": [45, 46, 47, 52, 53],
        "severity": "critical"
      },
      {
        "file": "packages/core/utils/helpers.py",
        "functions": ["format_error"],
        "lines": [23, 24],
        "severity": "low"
      }
    ],
    "delegation_recommendations": [
      {
        "category": "COVERAGE_GAP",
        "next_step": "Generate unit tests for refresh_token and validate_expiry functions",
        "priority": "critical",
        "rationale": "Core auth functions have no test coverage",
        "affected_tests": []
      }
    ]
  }
}
```

---

## Example 4: Multi-Failure Categorization

### Delegation

```
Task(test-executor, "Execute full test suite and categorize all failures for delegation")
```

### Expected Output (Multiple Categories)

```json
{
  "status": "SUCCESS",
  "agent": "test-executor",
  "confidence": 0.87,
  "agent_specific_output": {
    "execution_summary": {
      "total_tests": 200,
      "passed": 192,
      "failed": 8,
      "exit_code": 1
    },
    "failures": [
      {"test_name": "test_api_response", "category": "APPLICATION_BUG", "confidence": 0.88},
      {"test_name": "test_data_transform", "category": "APPLICATION_BUG", "confidence": 0.82},
      {"test_name": "test_fixture_setup", "category": "TEST_BUG", "confidence": 0.91},
      {"test_name": "test_mock_config", "category": "TEST_BUG", "confidence": 0.75},
      {"test_name": "test_db_connection", "category": "ENVIRONMENT", "confidence": 0.95},
      {"test_name": "test_timing_sensitive", "category": "FLAKY_TEST", "confidence": 0.78},
      {"test_name": "test_race_condition", "category": "FLAKY_TEST", "confidence": 0.85},
      {"test_name": "test_unclear_failure", "category": "MANUAL_REVIEW_NEEDED", "confidence": 0.42}
    ],
    "delegation_summary": {
      "primary_category": "APPLICATION_BUG",
      "failure_count": 8,
      "delegation_confidence": 0.80
    },
    "delegation_recommendations": [
      {
        "category": "APPLICATION_BUG",
        "next_step": "Investigate and fix logic errors in API and data transform modules",
        "priority": "high",
        "affected_tests": ["test_api_response", "test_data_transform"]
      },
      {
        "category": "TEST_BUG",
        "next_step": "Fix test fixture and mock configuration issues",
        "priority": "medium",
        "affected_tests": ["test_fixture_setup", "test_mock_config"]
      },
      {
        "category": "ENVIRONMENT",
        "next_step": "Database connection setup required",
        "priority": "critical",
        "affected_tests": ["test_db_connection"]
      },
      {
        "category": "FLAKY_TEST",
        "next_step": "Fix test isolation and timing dependencies",
        "priority": "medium",
        "affected_tests": ["test_timing_sensitive", "test_race_condition"]
      },
      {
        "category": "MANUAL_REVIEW_NEEDED",
        "next_step": "Manual investigation required - automated categorization inconclusive",
        "priority": "low",
        "affected_tests": ["test_unclear_failure"]
      }
    ]
  }
}
```

---

## Failure Output Example

### When Test Execution Fails

```json
{
  "status": "FAILURE",
  "agent": "test-executor",
  "confidence": 0.0,
  "failure_details": {
    "failure_type": "FRAMEWORK_NOT_FOUND",
    "reasons": [
      "No pytest, jest, or go test framework detected",
      "pyproject.toml missing [tool.pytest] section",
      "No package.json found"
    ],
    "recovery_suggestions": [
      "Add pytest configuration to pyproject.toml",
      "Install pytest: uv add pytest",
      "Specify framework override in request"
    ]
  }
}
```
