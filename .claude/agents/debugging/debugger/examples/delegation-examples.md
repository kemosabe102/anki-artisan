# Debugger Delegation Examples

How the orchestrator invokes the debugger agent.

---

## Standard Debugging

```python
# Single failing test investigation
Task(debugger, """
Debug failing test: pytest tests/unit/test_auth.py::test_login_expired_token

Error: AssertionError: Expected 401, got 200

Context:
- Test worked before commit abc123
- Related to token validation changes

Apply 8-step scientific debugging methodology.
Return RCA Record with root cause and fix.
""")
```

---

## Pre-Commit Validation

```python
# Autonomous validation with self-correcting loop
Task(debugger, """
Operation: validate_pre_commit

Validate changes before commit using:
  scripts/prepare-code-review.py --fast

Modified files:
- packages/core/auth/handler.py
- tests/unit/test_auth.py

Max iterations: 3
Auto-fix: linting, formatting, simple test failures
Document any unfixable issues.
""")
```

---

## Multiple Failing Tests

```python
# Fix multiple tests with per-test OODA loop
Task(debugger, """
Operation: fix_failing_tests

Failing tests:
- tests/unit/test_auth.py::test_login_success
- tests/unit/test_auth.py::test_login_expired
- tests/integration/test_api.py::test_protected_route

Apply per-test OODA cycle (max 3 attempts each).
Escalate to research on attempt 3.
Mark unfixable tests with evidence.
""")
```

---

## OpenTelemetry Debugging

```python
# Application-layer telemetry issues
Task(debugger, """
Debug missing spans in Jaeger for auth service.

Symptoms:
- telemetrygen traces appear (infra OK)
- Application spans not visible
- TracerProvider configured in main.py

Focus on application instrumentation, not infrastructure.
Reference: docs/04-guides/debugger/opentelemetry-instrumentation.md
""")
```

---

## Context Metadata

When delegating, orchestrator should include:

```yaml
context:
  bug_description: "Login fails for expired tokens"
  failing_test: "tests/unit/test_auth.py::test_login_expired"
  error_message: "AssertionError: Expected 401, got 200"
  reproduction_steps:
    - "Create token with past expiry"
    - "Call login endpoint"
    - "Assert 401 response"
  affected_files:
    - "packages/core/auth/validator.py"
  recent_changes: "commit abc123 modified token validation"
  
operation_type: debug  # or validate_pre_commit, fix_failing_tests

constraints:
  max_iterations: 3
  research_allowed: true
  research_on_attempt: 3
```

---

## Delegation Decision Matrix

| Scenario | Delegate To | Reason |
|----------|-------------|--------|
| Failing test, unknown cause | debugger | RCA needed |
| Simple known fix | python-code-implementer | No investigation needed |
| Pre-commit validation | debugger (validate_pre_commit) | Self-correcting loop |
| Multiple test failures | debugger (fix_failing_tests) | Per-test OODA |
| Infrastructure telemetry | k8s-deployment | Not app code |
| Design change needed | refactorer | Outside debugger scope |
