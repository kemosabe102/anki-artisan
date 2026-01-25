# Delegation Examples for Python Code Implementer

## Standard Feature Implementation

```markdown
Task(python-code-implementer,
  "Implement the user authentication middleware for the FastAPI application.
  
  **Context**:
  - Location: packages/api/middleware/
  - Pattern: Follow existing middleware patterns in packages/api/middleware/logging.py
  - Tests: tests/unit/api/test_auth_middleware.py already exists
  
  **Acceptance Criteria**:
  1. Validate JWT tokens from Authorization header
  2. Extract user_id and roles into request.state
  3. Return 401 for invalid/missing tokens
  4. Return 403 for insufficient roles
  
  **Constraints**:
  - Use existing JWTValidator from packages/core/auth/
  - Follow error response format in packages/api/errors.py")
```

---

## Bug Fix (Scoped Modification)

```markdown
Task(python-code-implementer,
  "Fix the race condition in packages/core/cache/redis_cache.py:45-67.
  
  **Problem**: Concurrent writes can overwrite each other when updating cached user sessions.
  
  **Expected Behavior**: Use Redis WATCH/MULTI/EXEC for atomic updates.
  
  **Tests**: tests/unit/core/test_redis_cache.py has failing test_concurrent_updates.
  
  **Constraints**:
  - Minimal changes - only fix the race condition
  - Do not refactor surrounding code")
```

---

## Integration Task

```markdown
Task(python-code-implementer,
  "Integrate the new payment provider SDK into packages/billing/providers/.
  
  **Context**:
  - New SDK: stripe-python v8.0
  - Existing pattern: packages/billing/providers/paypal.py
  - Interface: Must implement PaymentProvider protocol from packages/billing/interfaces.py
  
  **Deliverables**:
  1. packages/billing/providers/stripe.py implementing PaymentProvider
  2. Tests in tests/unit/billing/test_stripe_provider.py
  
  **Research Needed**: Use Context7 for stripe-python v8 API patterns")
```

---

## TDD-First New Feature

```markdown
Task(python-code-implementer,
  "Implement rate limiting for API endpoints.
  
  **Note**: No existing tests for this feature.
  
  **TDD Requirement**: Create tests FIRST in tests/unit/api/test_rate_limiter.py before implementation.
  
  **Specification**:
  - 100 requests per minute per user
  - Return 429 with Retry-After header when exceeded
  - Use Redis for distributed state
  
  **Location**: packages/api/middleware/rate_limiter.py")
```

---

## Expected Output Format

All implementations return structured output per `schemas/python-code-implementer.schema.json`:

### SUCCESS Example

```json
{
  "status": "SUCCESS",
  "agent": "python-code-implementer",
  "operation_type": "feature_implementation",
  "agent_specific_output": {
    "tdd_evidence": {
      "existing_tests_found": ["tests/unit/api/test_auth_middleware.py::test_valid_token", "tests/unit/api/test_auth_middleware.py::test_invalid_token"],
      "tests_created": [],
      "pre_impl_test_run": "FAILED: 2 tests failed (expected before implementation)",
      "post_impl_test_run": "PASSED: 4 tests passed in 0.23s"
    },
    "declared_scope": {
      "files_to_modify": ["packages/api/middleware/auth.py"],
      "files_read_only": ["packages/core/auth/jwt_validator.py", "packages/api/errors.py", "packages/api/middleware/logging.py"],
      "rationale": "Creating new auth middleware following existing patterns, reusing JWTValidator"
    },
    "almanac_check": {
      "checked": true,
      "existing_components_found": ["packages/core/auth/JWTValidator", "packages/api/middleware/BaseMiddleware"],
      "reuse_decision": "extend",
      "justification": "Extending BaseMiddleware pattern and reusing JWTValidator for token validation"
    },
    "files_modified": [
      {
        "path": "packages/api/middleware/auth.py",
        "change_type": "created",
        "lines_changed": 87,
        "description": "JWT authentication middleware with role validation"
      }
    ],
    "implementation_summary": "Implemented auth middleware using existing JWTValidator from packages/core/auth/. Middleware validates JWT tokens from Authorization header, extracts user_id and roles into request.state, returns 401 for invalid/missing tokens, and 403 for insufficient roles.",
    "pre_flight_checks_passed": true,
    "standards_compliance": {
      "coding_guidelines_validated": true,
      "context7_patterns_applied": ["fastapi-middleware", "jwt-validation"],
      "adr_compliance": ["ADR-004"],
      "existing_components_leveraged": ["packages/core/auth/JWTValidator", "packages/api/middleware/BaseMiddleware"]
    },
    "security_verification": {
      "path_validation": {
        "applied": false,
        "evidence": "N/A: no user-supplied file paths"
      },
      "subprocess_safety": {
        "applied": false,
        "evidence": "N/A: no subprocess calls"
      },
      "regex_safety": {
        "applied": false,
        "evidence": "N/A: no regex patterns"
      },
      "input_validation": {
        "applied": true,
        "evidence": "Lines 23-31: Authorization header validated before processing"
      },
      "secret_handling": {
        "applied": true,
        "evidence": "Verified: JWT secret loaded from environment, not hardcoded"
      }
    },
    "self_review_results": {
      "correctness": {
        "passed": true,
        "evidence": "Verified by tests: test_valid_token, test_invalid_token, test_missing_token, test_insufficient_roles"
      },
      "readability": {
        "passed": true,
        "evidence": "All functions <20 lines, clear naming (validate_token, extract_roles), Google-style docstrings"
      },
      "maintainability": {
        "passed": true,
        "evidence": "HTTP status codes as constants, single responsibility per method, no magic strings"
      },
      "security": {
        "passed": true,
        "evidence": "See security_verification: input validation applied, secrets from environment"
      },
      "performance": {
        "passed": true,
        "evidence": "No regex compilation needed, O(1) role lookup via set, no N+1 queries"
      },
      "standards": {
        "passed": true,
        "evidence": "Ruff passed (0 errors), 100% type hint coverage, async/await pattern per ADR-004"
      }
    },
    "next_actions": [
      {
        "action": "Run integration tests",
        "agent": "test-executor",
        "rationale": "Validate middleware works with full request cycle"
      },
      {
        "action": "Update API documentation",
        "agent": "doc-writer",
        "rationale": "Document new authentication requirements for API consumers"
      }
    ]
  }
}
```

### FAILURE Example

```json
{
  "status": "FAILURE",
  "agent": "python-code-implementer",
  "operation_type": "feature_implementation",
  "failure_details": {
    "failure_type": "standards_conflict",
    "reasons": ["ADR-004 requires async middleware but task specified sync"],
    "recovery_suggestions": [
      {
        "approach": "Clarify with architect whether async is required",
        "rationale": "ADR-004 conflicts with task specification"
      }
    ],
    "delegation_needed": "none"
  }
}
```

### FAILURE Example: scope_boundary_violation

```json
{
  "status": "FAILURE",
  "agent": "python-code-implementer",
  "operation_type": "feature_implementation",
  "failure_details": {
    "failure_type": "scope_boundary_violation",
    "reasons": ["Attempted to modify packages/api/middleware.py which was not in declared_scope"],
    "partial_results": {
      "files_modified": ["packages/api/auth.py"],
      "completed_phases": ["analysis", "research", "todo_creation"]
    },
    "recovery_suggestions": [
      {
        "approach": "Request scope expansion from orchestrator",
        "rationale": "middleware.py integration discovered during implementation"
      },
      {
        "approach": "Create separate task for middleware changes",
        "rationale": "Maintain scope boundaries, defer to new task"
      }
    ]
  }
}
```

### FAILURE Example: ambiguous_requirements

```json
{
  "status": "FAILURE",
  "agent": "python-code-implementer",
  "operation_type": "feature_implementation",
  "failure_details": {
    "failure_type": "ambiguous_requirements",
    "reasons": ["Acceptance criterion 'handle errors gracefully' scored clarity 2/5"],
    "ambiguous_criteria": [
      {
        "criterion": "handle errors gracefully",
        "clarity_score": 2,
        "interpretations": ["log and continue", "retry with backoff", "fail fast"],
        "question": "Which error handling strategy is required?"
      }
    ],
    "recovery_suggestions": [
      {
        "approach": "Clarify with orchestrator/user",
        "rationale": "Multiple valid interpretations require explicit choice"
      }
    ]
  }
}
```

### FAILURE Example: tdd_gate_violation

```json
{
  "status": "FAILURE",
  "agent": "python-code-implementer",
  "operation_type": "feature_implementation",
  "failure_details": {
    "failure_type": "tdd_gate_violation",
    "reasons": ["Implementation attempted before test creation"],
    "pre_flight_failures": [
      {
        "pattern": "TDD-First",
        "violation": "No tests found and tests_created array empty",
        "guideline_reference": "TDD-First Gate requires tests BEFORE implementation"
      }
    ],
    "recovery_suggestions": [
      {
        "approach": "Create test file first",
        "rationale": "TDD workflow: Red (failing test) → Green (implementation) → Refactor"
      }
    ]
  }
}
```

### FAILURE Example: almanac_check_missing

```json
{
  "status": "FAILURE",
  "agent": "python-code-implementer",
  "operation_type": "feature_implementation",
  "failure_details": {
    "failure_type": "almanac_check_missing",
    "reasons": ["New utility class created without COMPONENT_ALMANAC.md verification"],
    "recovery_suggestions": [
      {
        "approach": "Read COMPONENT_ALMANAC.md and search for existing validators",
        "rationale": "May duplicate existing functionality"
      }
    ],
    "delegation_needed": "researcher-codebase"
  }
}
```
