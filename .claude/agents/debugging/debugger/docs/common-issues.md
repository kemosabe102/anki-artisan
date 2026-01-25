# Common Issues & Solutions

Troubleshooting guide for frequent debugging challenges.

---

## Issue 1: Fix Causes Regressions

**Symptoms**: Fix resolves original issue but breaks other tests

**Root Cause**: Narrow hypothesis that doesn't account for side effects

**Solution**:
1. Re-run full test suite (not just failing test) after fix
2. Use `git diff` to review all changes for unintended modifications
3. Expand hypothesis: "Fix X without breaking Y"
4. Apply 5 Whys to regression to find shared dependencies

---

## Issue 2: Cannot Reproduce After 3 Attempts

**Symptoms**: Test passes locally but fails in CI, or failure is intermittent

**Root Cause**: Environment differences, timing issues, or test isolation

**Solution**:
1. Check environment: Python version, dependencies, OS, timezone
2. Look for timing issues: Add `asyncio.sleep(0)` to yield control
3. Verify test isolation: Run test alone vs in suite
4. Review CI logs for environment variable differences
5. Mark as flaky if confidence < 0.5: `pytest.mark.flaky(reruns=3)`

---

## Issue 3: Interdependent Tests (Isolation Failure)

**Symptoms**: Test passes alone but fails in suite

**Root Cause**: Shared state (globals, database, filesystem, cached imports)

**Solution**:
1. Run tests in different orders to identify polluting test
2. Add teardown: Use pytest fixtures with `yield` for cleanup
3. Database: Wrap tests in transactions that rollback
4. Filesystem: Use `tmp_path` fixture instead of hardcoded paths
5. Clear caches: `importlib.reload()` between tests

---

## Issue 4: Research Yields No Results

**Symptoms**: Escalated to Perplexity but no useful results

**Root Cause**: Error message too specific or too vague

**Solution**:
1. Try Context7 first for framework errors
2. Generalize search: Strip local paths, UUIDs, timestamps
3. Search for innermost exception in chained exceptions
4. Search by symptoms, not error text
5. Check `git diff main` for recent breaking changes

---

## Issue 5: Validation Script Timeout

**Symptoms**: validate_pre_commit times out

**Root Cause**: Slow tests, infinite loop, or hanging process

**Solution**:
1. Add timeout: `AGENT_NAME=debugger timeout 300 pytest`
2. Use fast mode: `scripts/prepare-code-review.py --fast`
3. Profile script with `time` command
4. Parallelize: `pytest -n auto`
5. Skip slow tests: `pytest -m "not slow"`

---

## Issue 6: Fix Ineffective Despite Confirmed Hypothesis

**Symptoms**: Experiment validated, fix applied, test still fails

**Root Cause**: Hypothesis was incomplete (symptom, not root cause)

**Solution**:
1. Deepen 5 Whys: Ask "Why?" 2 more times
2. Check for multiple independent causes
3. Verify fix applied: `git diff` - did Edit actually modify file?
4. Re-run experiment with fix applied
5. Expand scope: Is there a second location with same bug?

---

## Issue 7: Missing Dependencies or External Services

**Symptoms**: Test requires unavailable database, API key, or service

**Root Cause**: External dependencies can't be mocked or unavailable in CI

**Solution**:
1. Mark as unfixable with evidence
2. Mock external dependencies: `unittest.mock` or `pytest-mock`
3. Skip in CI: `pytest.mark.skipif(not has_db())`
4. Use test doubles: In-memory database or fake service
5. Document requirements in test docstring

---

## Escalation Path

If issue persists after troubleshooting:
1. Document all attempted solutions in `hypotheses_attempted`
2. Capture evidence (logs, screenshots, environment details)
3. Return FAILURE with `failure_type` and `recovery_suggestions`
4. Orchestrator will escalate to user or specialized agent
