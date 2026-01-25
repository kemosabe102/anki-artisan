# CI Monitoring Reference

**Purpose**: GitHub Actions workflow monitoring with UV-aware failure analysis

---

## Overview

The monitor_ci operation provides:
- Real-time GitHub Actions workflow status
- UV package manager failure detection and diagnosis
- Actionable recommendations for CI failures
- Structured output for orchestrator consumption

---

## GitHub Actions Query Commands

### List Recent Runs
```bash
AGENT_NAME=github gh run list --limit 10
AGENT_NAME=github gh run list --limit 10 --branch main
AGENT_NAME=github gh run list --limit 10 --workflow ci.yml
```

### View Specific Run
```bash
AGENT_NAME=github gh run view <run-id>
AGENT_NAME=github gh run view <run-id> --log
AGENT_NAME=github gh run view <run-id> --log-failed
```

### Wait for Completion
```bash
AGENT_NAME=github gh run watch <run-id>
```

---

## UV Failure Patterns

The following 6 UV-specific failure patterns are detected and diagnosed:

### 1. UV Sync Failure

**Symptom**: "No matching distribution found", "Could not find a version"

**Detection Pattern**:
```
error: no matching distribution found for <package>
error: Could not find a version that satisfies the requirement
```

**Root Causes**:
- Package version constraint too strict in pyproject.toml
- Package not available for Python version
- Private package without proper credentials

**Recommendations**:
- Check pyproject.toml version constraints
- Verify package exists on PyPI
- Check Python version compatibility
- If private: verify UV_EXTRA_INDEX_URL or credentials

---

### 2. Command Not Found

**Symptom**: "uv: command not found", "bash: uv: command not found"

**Detection Pattern**:
```
uv: command not found
bash: uv: command not found
/bin/sh: uv: not found
```

**Root Causes**:
- UV not installed in workflow
- UV install step missing or failed
- Path not configured after install

**Recommendations**:
- Add UV install step to workflow:
  ```yaml
  - name: Install UV
    uses: astral-sh/setup-uv@v3
  ```
- Verify install step runs before uv commands

---

### 3. Lockfile Conflict

**Symptom**: "Lock file out of sync", "uv.lock is outdated"

**Detection Pattern**:
```
error: The lockfile is outdated
error: Lock file out of sync
uv.lock needs to be regenerated
```

**Root Causes**:
- pyproject.toml changed without updating uv.lock
- Merge conflict in uv.lock
- Different UV versions between local and CI

**Recommendations**:
- Run `uv lock` locally and commit uv.lock
- Ensure UV version in CI matches local
- Check for merge conflicts in uv.lock

---

### 4. Virtual Environment Issues

**Symptom**: "No module named...", "ModuleNotFoundError"

**Detection Pattern**:
```
ModuleNotFoundError: No module named
ImportError: cannot import name
No module named
```

**Root Causes**:
- Venv not activated before running tests
- Dependencies not installed into venv
- Wrong Python interpreter selected

**Recommendations**:
- Use `uv run` prefix for commands:
  ```yaml
  - run: uv run pytest
  ```
- Verify venv activation in workflow
- Check UV_PROJECT_ENVIRONMENT variable

---

### 5. Python Version Mismatch

**Symptom**: "Python version X.Y required", "Requires-Python"

**Detection Pattern**:
```
requires-python does not match
Python version .* is not supported
This project requires Python
```

**Root Causes**:
- Workflow Python version differs from pyproject.toml
- System Python used instead of setup-python version
- UV using wrong Python discovery

**Recommendations**:
- Align workflow python-version with pyproject.toml
- Use setup-python before UV commands:
  ```yaml
  - uses: actions/setup-python@v5
    with:
      python-version: "3.11"
  ```
- Set UV_PYTHON_PREFERENCE=only-system if needed

---

### 6. Test Failures

**Symptom**: pytest errors, assertion failures, collection errors

**Detection Pattern**:
```
FAILED tests/
=== .* failed ===
AssertionError
collection error
```

**Root Causes**:
- Actual test failures (logic errors)
- Missing test fixtures or setup
- Environment-specific failures

**Recommendations**:
- Delegate to debugging agent for analysis
- Check test fixtures and conftest.py
- Review environment variables in workflow

---

## Output Schema

```json
{
  "status": "SUCCESS",
  "workflow_status": "completed",
  "conclusion": "failure",
  "workflow_runs": [
    {
      "id": "12345678901",
      "name": "CI",
      "status": "completed",
      "conclusion": "failure",
      "started_at": "2025-01-15T10:30:00Z",
      "completed_at": "2025-01-15T10:35:00Z",
      "jobs": [
        {
          "name": "test",
          "status": "completed",
          "conclusion": "failure"
        }
      ]
    }
  ],
  "summary": "CI failed: UV sync failure detected",
  "recommended_actions": [
    "Check pyproject.toml version constraints",
    "Run uv lock locally to regenerate lockfile"
  ],
  "uv_failure_detected": true,
  "uv_failure_type": "sync_failure"
}
```

---

## Related References

| Document | Purpose |
|----------|---------|
| error-handling.md | HTTP error handling for gh CLI |
| actions-workflows.md | Workflow dispatch patterns |
| ../../../docs/01-guides/github-integration-guide.md | Complete UV CI troubleshooting |
