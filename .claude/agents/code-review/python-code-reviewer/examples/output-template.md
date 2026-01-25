# Sample Review Output

## Open Questions & Missing Context

- `packages/core/auth/validator.py:45` - What is the expected behavior when `token` is None? Missing: `AuthConfig` definition
- `packages/api/routes.py:123` - Is this endpoint rate-limited? Missing: Rate limiting middleware config

## Summary Verdict

**Changes Requested** - Found 2 Critical and 3 Major issues requiring attention before merge. Primary concerns are unhandled async exceptions and missing input validation.

## Review Scope

**Files Reviewed**: 5 files from git diff
- `packages/core/auth/validator.py` (87 lines changed) - HIGH priority
- `packages/api/routes.py` (45 lines changed) - HIGH priority
- `tests/unit/test_validator.py` (32 lines changed) - MEDIUM priority

**Surfaces Affected**: APIs, authentication flow, data validation

---

## Should-Do Changes

### Critical (2)

* **packages/core/auth/validator.py:67** | **Severity:** Critical | **Confidence:** 0.95
  * **Problem:** Async function `validate_token()` not awaited, returns coroutine instead of result
  * **Why (Principle):** Invariant violation - async functions must be awaited [coding-guidelines.md §async]
  * **Missing Context:** None
  * **Verification:**
    * *Wrong signature:* `result = validate_token(token)`
    * *Correct signature:* `result = await validate_token(token)`
    * *Quick check:* `rg -n "validate_token\s*\(" | grep -v "await"`
  * **Fix:** Add `await` keyword before `validate_token()` call

* **packages/api/routes.py:89** | **Severity:** Critical | **Confidence:** 0.92
  * **Problem:** User input passed directly to SQL query without sanitization
  * **Why (Principle):** Unsafe pattern - SQL injection vulnerability [python-security-patterns.md §injection]
  * **Missing Context:** None
  * **Verification:**
    * *Wrong signature:* `query = f"SELECT * FROM users WHERE id = {user_id}"`
    * *Correct signature:* `query = "SELECT * FROM users WHERE id = :id"` with parameterized binding
    * *Quick check:* `rg "f\"SELECT.*\{" packages/`
  * **Fix:** Use parameterized queries with SQLAlchemy

### Major (3)

* **packages/core/auth/validator.py:34** | **Severity:** Major | **Confidence:** 0.87
  * **Problem:** Missing type hints on public function `verify_credentials()`
  * **Why (Principle):** Type safety requirement [python-type-safety.md §public-api]
  * **Missing Context:** None
  * **Verification:**
    * *Quick check:* `mypy packages/core/auth/validator.py --check-untyped-defs`
  * **Fix:** Add type hints: `def verify_credentials(username: str, password: str) -> bool:`

---

## Optional / Later

### Nits (1)

* **tests/unit/test_validator.py:15** | **Severity:** Nit | **Confidence:** 0.75
  * **Problem:** Test name `test_thing()` is not descriptive
  * **Why (Principle):** Test clarity [python-testing-standards.md §naming]
  * **Fix:** Rename to `test_validate_token_returns_false_for_expired_token()`

---

## Tests & Coverage

- Missing: Test for `validate_token()` with expired token
- Missing: Test for `verify_credentials()` with SQL injection attempt
- Missing: Edge case test for empty username

## Security Notes

- **SQL Injection Risk** at `routes.py:89` - See Critical finding above
- Consider adding rate limiting to `/api/auth/login` endpoint

## Performance Notes

No performance concerns identified in this change set.

## Context7 Research Summary

**Libraries Researched**: fastapi, pydantic, sqlalchemy
**Validation Results**:
- fastapi: 3 findings validated (async patterns)
- sqlalchemy: 1 finding validated (parameterized queries)
**Fallback to WebSearch**: No

---

## Rate Limit Compliance

| Severity | Count | Limit |
|----------|-------|-------|
| Critical | 2 | ≤3 ✅ |
| Major | 3 | ≤5 ✅ |
| Minor | 0 | ≤5 ✅ |
| Nits | 1 | ≤2 ✅ |
