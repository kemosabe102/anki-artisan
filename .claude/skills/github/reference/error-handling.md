# GitHub Error Handling Reference

**Purpose**: GitHub-specific error classification, retry patterns, and recovery

---

## Overview

This reference covers errors specific to GitHub operations:
- HTTP API errors (MCP tools and gh CLI)
- Rate limiting
- Authentication failures
- Circuit breaker patterns

**For git command errors**: See source-control skill error-handling.md

---

## HTTP Error Classification

### PERMANENT Errors (No Retry)

| Code | Error | Cause | Recovery |
|------|-------|-------|----------|
| 401 | Unauthorized | Token expired/invalid | Run `gh auth login` |
| 403 | Forbidden | Insufficient permissions | Check token scopes, verify repo access |
| 404 | Not Found | Resource does not exist | Verify owner/repo/resource ID |
| 422 | Validation Failed | Invalid parameters | Check request body, fix inputs |

### TRANSIENT Errors (Retry with Backoff)

| Code | Error | Cause | Backoff |
|------|-------|-------|---------|
| 429 | Rate Limited | Too many requests | Honor Retry-After header, else 5s, 10s, 20s |
| 500 | Internal Server Error | GitHub issue | 5s, 10s, 20s with jitter |
| 502 | Bad Gateway | GitHub issue | 5s, 10s, 20s with jitter |
| 503 | Service Unavailable | GitHub maintenance | 5s, 10s, 20s with jitter |
| 504 | Gateway Timeout | GitHub overload | 5s, 10s, 20s with jitter |

---

## Error Classification Rules

**MANDATORY**: Classify errors BEFORE retrying any GitHub operation.

```
IF error code IN [401, 403, 404, 422]:
  -> PERMANENT: Return FAILURE immediately with recovery suggestions

IF error code IN [429, 500, 502, 503, 504]:
  -> TRANSIENT: Apply retry with exponential backoff

IF circuit breaker OPEN:
  -> Return cached data or "GitHub unavailable" message
```

---

## 401 Unauthorized

**Symptoms**:
- "Bad credentials"
- "Requires authentication"
- "Token has expired"

**Recovery Steps**:
1. Re-authenticate: `gh auth login`
2. Verify token: `gh auth status`
3. Check token expiry in GitHub settings

**MCP-specific**: OAuth token may need refresh. Suggest `/mcp` command.

---

## 403 Forbidden

**Symptoms**:
- "Resource not accessible"
- "Must have push access"
- "API rate limit exceeded" (with 403, not 429)

**Recovery Steps**:
1. Check token scopes: `gh auth status`
2. Verify repository access permissions
3. For organizations: check SSO authorization

**Common Scope Issues**:
| Operation | Required Scope |
|-----------|----------------|
| Read repos | `repo` or `public_repo` |
| Write repos | `repo` |
| Workflows | `workflow` |
| Admin | `admin:repo` |

---

## 404 Not Found

**Symptoms**:
- "Not Found"
- "Repository not found"
- "Pull request not found"

**Recovery Steps**:
1. Verify repository exists: `git remote -v`
2. Check owner/repo spelling (case-sensitive)
3. Verify resource ID (issue number, PR number, etc.)

**Common Causes**:
- Private repo without proper token scope
- Typo in owner or repo name
- Resource was deleted

---

## 422 Validation Failed

**Symptoms**:
- "Validation Failed"
- "Reference already exists"
- "No commits between..."

**Recovery Steps**:
1. Check error message for specific field
2. Verify all required parameters provided
3. Check parameter values are valid

**Common Validation Errors**:
| Message | Cause | Fix |
|---------|-------|-----|
| "No commits between..." | HEAD same as base | Push commits first |
| "Reference already exists" | Tag/branch exists | Use different name |
| "Title is required" | Empty title | Provide title |
| "Body is too long" | Exceeded limit | Shorten body |

---

## 429 Rate Limited

**Symptoms**:
- "API rate limit exceeded"
- "You have exceeded a secondary rate limit"

**Recovery Steps**:
1. Check Retry-After header
2. Apply exponential backoff
3. If persistent, wait longer between requests

**Rate Limits**:
| Type | Limit | Reset |
|------|-------|-------|
| Authenticated | 5000/hour | Rolling window |
| Unauthenticated | 60/hour | Rolling window |
| Secondary | Varies | Retry-After header |

**Backoff Strategy**:
```
If Retry-After header present:
  Wait for specified duration
Else:
  Attempt 1: Wait 5s
  Attempt 2: Wait 10s
  Attempt 3: Wait 20s
  After 3 attempts: Return FAILURE
```

---

## 5xx Server Errors

**Symptoms**:
- "Internal Server Error"
- "Bad Gateway"
- "Service Unavailable"

**Recovery Steps**:
1. Apply exponential backoff with jitter
2. Check GitHub Status page
3. If persistent, circuit breaker activates

**Backoff with Jitter**:
```
base_delay = [5, 10, 20] seconds
jitter = random(0, base_delay * 0.3)
actual_delay = base_delay + jitter
```

---

## Circuit Breaker Pattern

**Purpose**: Prevent overwhelming GitHub API during outages.

### State Machine

```
CLOSED (normal operation)
  |
  v [5 consecutive 5xx errors]
OPEN (requests blocked)
  |
  v [60s wait]
HALF-OPEN (testing)
  |
  +--[3 successes]--> CLOSED
  |
  +--[1 failure]---> OPEN
```

### Configuration

| Parameter | Value |
|-----------|-------|
| Failure threshold | 5 consecutive 5xx errors |
| Open duration | 60 seconds |
| Half-open test requests | 3 |
| Tracked per | (tool_name, error_pattern) |

### During OPEN State

1. Return cached data if available
2. Return status: "GitHub unavailable, retrying in Xs"
3. Include estimated recovery time

---

## Failure Output Schema

All failures must include recovery context:

```json
{
  "status": "FAILURE",
  "failure_details": {
    "failure_type": "github_api_error",
    "error_code": 403,
    "error_message": "Must have push access to repository",
    "error_classification": "PERMANENT",
    "retry_attempted": false,
    "recovery_suggestions": [
      "Verify token has repo scope: gh auth status",
      "Check repository access permissions",
      "For organizations, verify SSO authorization"
    ]
  }
}
```

---

## gh CLI Error Handling

The gh CLI may return different error formats:

### Exit Codes
| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Usage error |
| 4 | Authentication required |

### Parse gh Errors
```bash
# Capture stderr and exit code
output=$(AGENT_NAME=github gh pr create --title "test" 2>&1)
exit_code=$?

if [ $exit_code -ne 0 ]; then
  # Parse error message from output
  # Apply error classification
fi
```

---

## Anti-Patterns

- Retrying PERMANENT errors (401, 403, 404, 422)
- Skipping error classification
- Ignoring Retry-After headers
- Continuing after circuit breaker OPEN
- Retrying without backoff (causes rate limiting)
- Not including recovery suggestions in failures

---

## Related References

| Document | Purpose |
|----------|---------|
| ci-monitoring.md | UV-specific CI failures |
| ../../../docs/00-core/error-classification-framework.md | Full error framework |
| source-control/reference/error-handling.md | Git command errors |
