# CI/CD Integration

Push and CI monitoring workflows for the `/git` command.

---

## Push & CI Monitoring

**NOT part of main workflow** - these are separate user requests.

### Push to Remote

**Usage:** User manually runs `git push` OR asks Claude to push

**Claude Code handles directly:**
```bash
git push origin [current-branch]
```

### Monitor CI

**Usage:** User asks "check CI status" OR "why did CI fail"

**Delegate to:** `[source-control]` agent - `monitor_ci` operation

**Actions:**
- Run `gh run list --branch [branch]` to find recent runs
- Run `gh run view [run_id]` to get status
- If failed: Parse logs and provide actionable recommendations

---

## CI Status Output Examples

### Success Output
```text
CI Status for commit abc123

Workflow: CI/CD Pipeline (run #7891234567)
Status: PASSED (4.5 minutes)

Jobs:
- lint-format (45s) PASSED
- run-tests (2m 0s) PASSED
- security-scan (1m 30s) PASSED

All checks passed!
```

### Failure Output
```text
CI Status for commit abc123

Workflow: CI/CD Pipeline (run #7891234567)
Status: FAILED (3.2 minutes)

Failed Jobs:
- run-tests (1m 35s) FAILED
  Failed Step: Run pytest
  Error: 3 test failures

Test Failures:
1. tests/test_auth.py::test_jwt_validation
   AssertionError: Expected valid=True

2. tests/test_auth.py::test_token_expiry
   KeyError: 'exp'

3. tests/test_user.py::test_create_user
   ValidationError: email format invalid

Recommended Actions:
1. Delegate to debugger to fix test_jwt_validation
2. Delegate to debugger to fix test_token_expiry
3. Delegate to debugger to fix test_create_user
4. Re-run validation after fixes

Full logs: gh run view 7891234567 --log
```

---

## CI Failure Recovery Workflow

```text
User: git push
|
... time passes ...
|
User: Check CI status
|
Claude: [Delegates to source-control monitor_ci]
# Reports test failures with details
|
User: Fix those test failures
|
Claude: [Delegates to debugger, fixes tests]
|
User: /git prepare
# Re-validates the fixes
|
User: /git commit
# Commits the fix
|
User: git push
|
User: Monitor CI
|
Claude: [Watches CI, reports success]
```

---

## Pre-Commit Validation vs CI

| Check | Pre-Commit (Phase 1) | CI Pipeline |
|-------|---------------------|-------------|
| Linting | Yes (ruff check) | Yes |
| Formatting | Yes (ruff format) | Yes |
| Unit Tests | Yes (affected files) | Yes (all tests) |
| Integration Tests | No | Yes |
| Security Scan | Yes (Phase 3) | Yes |
| Build | No | Yes |

**Philosophy:** Pre-commit catches most issues locally; CI provides final validation.
