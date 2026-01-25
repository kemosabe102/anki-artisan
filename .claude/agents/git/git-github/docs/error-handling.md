# Error Handling for Git and GitHub Operations

**Purpose**: Error classification framework, retry patterns, and circuit breaker logic

**MANDATORY**: Classify errors BEFORE retrying any git/gh command.

---

## Error Classification Overview

| Category | Retry? | Max Attempts | Action |
|----------|--------|--------------|--------|
| PERMANENT | No | 0 | Return FAILURE with recovery suggestions |
| TRANSIENT | Yes | 3 | Exponential backoff, then FAILURE |
| FATAL | No | 0 | Escalate to orchestrator immediately |

---

## Git Command Errors

### PERMANENT (No Retry)

| Error Pattern | Example Message | Recovery Suggestion |
|---------------|-----------------|---------------------|
| Merge conflict | "Merge conflict in CLAUDE.md" | Resolve conflict manually, run git status |
| Pre-commit hook failure | "Linting failed", "Tests failed" | Fix issues, re-stage files |
| Invalid commit format | "commit-msg hook rejected" | Fix commit message format |
| Detached HEAD + uncommitted | "HEAD detached at..." | Create branch or stash changes |

### TRANSIENT (Retry with Backoff)

| Error Pattern | Example Message | Backoff |
|---------------|-----------------|---------|
| Lock file busy | ".git/index.lock already exists" | 1s, 2s, 4s |
| Network timeout | "Connection timeout", "EOF" | 2s, 4s, 8s |
| File system delay | "Temporary file error" | 1s, 2s, 4s |
| SSH key timeout | "git-agent not responding" | 2s, 4s, 8s |

### FATAL (Escalate Immediately)

| Error Pattern | Example Message | Action |
|---------------|-----------------|--------|
| Repository corruption | "Cannot recover objects" | Escalate to orchestrator |
| Force push blocked | "protected branch" | Escalate - never override |
| Pack file corruption | "Invalid pack file" | Escalate to orchestrator |

---

## GitHub MCP Errors

### PERMANENT (No Retry)

| HTTP Code | Error | Recovery |
|-----------|-------|----------|
| 404 | Repository/resource not found | Verify owner/repo via `git remote -v` |
| 403 | Insufficient permissions | Check token scopes |
| 422 | Validation failed | Check parameters, often wrong repo name |
| 401 | Authentication expired | Suggest `/mcp` for re-auth |

### TRANSIENT (Retry with Circuit Breaker)

| HTTP Code | Error | Backoff |
|-----------|-------|---------|
| 429 | Rate limiting | Check Retry-After header, else 5s, 10s, 20s |
| 500 | Internal server error | 5s, 10s, 20s with jitter |
| 502 | Bad gateway | 5s, 10s, 20s with jitter |
| 503 | Service unavailable | 5s, 10s, 20s with jitter |
| 504 | Gateway timeout | 5s, 10s, 20s with jitter |

---

## Circuit Breaker Pattern

**Purpose**: Prevent overwhelming GitHub API during outages.

### States

```
CLOSED (normal) --[5 failures]--> OPEN (blocked)
OPEN --[60s wait]--> HALF-OPEN (testing)
HALF-OPEN --[3 successes]--> CLOSED
HALF-OPEN --[1 failure]--> OPEN
```

### Configuration

| Parameter | Value |
|-----------|-------|
| Failure threshold | 5 consecutive 5xx errors |
| Open duration | 60 seconds |
| Half-open test requests | 3 |
| Tracked tuple | `(mcp_tool, error_pattern)` |

### During OPEN State

1. Return cached data if available
2. Otherwise return "GitHub MCP unavailable" message
3. Include recovery suggestions with wait time

---

## Retry Configuration by Operation

### Git Commands (add, commit)

```
max_retries: 3
backoff: exponential (1s, 2s, 4s)
retry_on: lock file issues ONLY
no_retry: merge conflicts, hook failures
```

### GitHub MCP Tools

```
max_retries: 3
backoff: exponential with jitter (5s, 10s, 20s)
retry_on: 429 (honor Retry-After), 5xx errors
no_retry: 401, 403, 404, 422
circuit_breaker: enabled
```

### GitHub CLI (gh run commands)

```
max_retries: 3
backoff: exponential with jitter (5s, 10s, 20s)
retry_on: 429, 5xx errors
circuit_breaker: enabled
auth: via gh auth (separate from MCP OAuth)
```

### FileGrouper Operations (git status, git diff)

```
max_retries: 2
backoff: linear (2s, 4s)
retry_on: concurrent operation conflicts
no_retry: repository corruption, invalid repository
```

---

## Failure Output Schema Enhancement

When returning FAILURE, always include error classification context:

```json
{
  "status": "FAILURE",
  "agent": "git-github",
  "failure_details": {
    "failure_type": "git_transient_error",
    "error_classification": "TRANSIENT",
    "retry_attempts": 3,
    "last_error": "fatal: Unable to create '.git/index.lock'",
    "recovery_suggestions": [
      "Lock file persisted after 3 retries",
      "Check for concurrent git operations: ps aux | grep git",
      "Manually remove stale lock: rm -f .git/index.lock (CAUTION)"
    ]
  }
}
```

---

## Anti-Patterns

- Retrying PERMANENT errors (merge conflicts, validation failures)
- Skipping error classification
- Ignoring Retry-After headers
- Continuing after circuit breaker OPEN
- Retrying without backoff (causes thundering herd)

---

## External References

- `.claude/docs/00-core/error-classification-framework.md` - Complete framework
- `.claude/docs/01-guides/github-integration-guide.md` - GitHub-specific patterns
