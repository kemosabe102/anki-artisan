---
title: "Error Classification Framework"
date: 2025-11-08
status: ACTIVE
tags: [claude-docs]
---
# Error Classification Framework

**Purpose**: Universal error classification taxonomy for all agents to determine retry strategies, circuit breaker behavior, and escalation paths

**Audience**: All agents (orchestrator, implementation, research, review), sub-agent developers

**Referenced by**: deployment-release, development, debugger, researcher-external, source-control

## Error Taxonomy

### Transient Errors (Retryable with Backoff)

**Definition**: Temporary failures that resolve automatically with time, safe to retry with exponential backoff

**HTTP Status Codes**:

- `408 Request Timeout` - Server processing timeout
- `429 Too Many Requests` - Rate limiting, retry after cooldown
- `500 Internal Server Error` - Generic server-side failure
- `502 Bad Gateway` - Upstream service temporarily unavailable
- `503 Service Unavailable` - Server overloaded or maintenance
- `504 Gateway Timeout` - Upstream service timeout

**Network Errors**:

- Connection timeouts (socket timeout, read timeout)
- DNS resolution failures (temporary DNS issues)
- Connection refused (service restarting)
- Network unreachable (routing flap)
- SSL handshake failures (certificate rotation)

**Kubernetes-Specific**:

- `pod eviction` - Node pressure, pod rescheduling
- `ImagePullBackOff` (temporary registry issues) - Registry rate limit, network blip
- `CrashLoopBackOff` (initial startup) - Dependencies not ready, startup race condition
- `ContainerCreating` timeout - Image pull delays, volume mount delays

**File System Errors**:

- File locked by another process (Windows file locking)
- Disk I/O timeout (storage latency spike)
- Temporary permission errors (ACL propagation delay)

**Retry Strategy**: Exponential backoff with jitter, 3 attempts max, 20s max delay

**Circuit Breaker Behavior**: Count towards failure threshold, trigger OPEN state if sustained

---

### Permanent Errors (Non-Retryable, Requires Code/Config Fix)

**Definition**: Errors indicating request is fundamentally invalid, retrying will not succeed without intervention

**HTTP Status Codes**:

- `400 Bad Request` - Malformed syntax, invalid JSON, schema violation
- `401 Unauthorized` - Missing or invalid credentials
- `403 Forbidden` - Valid credentials but insufficient permissions
- `404 Not Found` - Resource doesn't exist
- `405 Method Not Allowed` - HTTP verb not supported for endpoint
- `409 Conflict` - Request conflicts with current state (duplicate key)
- `422 Unprocessable Entity` - Semantic validation failure

**Authentication/Authorization**:

- Invalid API key (expired, revoked, wrong format)
- OAuth token expired (requires refresh)
- Certificate validation failure (wrong CA, expired cert)
- Role-based access denial (user lacks permission)

**Schema/Validation**:

- JSON schema validation failure
- Missing required fields
- Type mismatch (string instead of integer)
- Constraint violation (value out of range)

**Kubernetes-Specific**:

- `immutability error` - Cannot modify immutable field (selector, namespace)
- `namespace not found` - Namespace doesn't exist
- `invalid resource definition` - YAML syntax error, invalid field
- `admission webhook denial` - Policy violation (security policy, resource quota)

**Code/Logic Errors**:

- Division by zero
- Null pointer dereference
- Array index out of bounds
- Type casting failure

**Retry Strategy**: NEVER retry, immediate failure escalation

**Circuit Breaker Behavior**: Do NOT count towards failure threshold (not service health indicator)

---

### Fatal Errors (Never Retry, Escalate Immediately)

**Definition**: Critical system failures requiring immediate human intervention, continuing operation would cause data corruption or cascading failures

**Database/Storage**:

- Database item doesn't exist (logical deletion, data loss)
- Data corruption detected (checksum mismatch)
- Transaction deadlock (cannot resolve automatically)
- Storage quota exceeded (no space available)

**Service Crashes**:

- Out of memory (OOM kill)
- Segmentation fault
- Unhandled exception in critical path
- Panic/fatal error in service

**Security Violations**:

- Cryptographic signature validation failure
- Tampered configuration detected
- Unauthorized system access attempt
- Security policy violation (SSRF attempt blocked)

**Kubernetes-Specific**:

- Node failure (kubelet stopped, node NotReady)
- Control plane unavailable (API server down)
- etcd cluster failure (quorum lost)
- Persistent volume claim failure (storage backend unavailable)

**Data Integrity**:

- Checksum verification failure
- Duplicate primary key insertion
- Foreign key constraint violation
- Data consistency violation

**Retry Strategy**: NEVER retry, immediate escalation to human

**Circuit Breaker Behavior**: Trigger OPEN state immediately, do NOT count attempts

---

## Classification Decision Tree

**Step 1 - Check Error Category**:

```
Is error a 5xx HTTP status OR network timeout?
  YES → Likely TRANSIENT (proceed to Step 2)
  NO → Proceed to Step 3

Is error a 4xx HTTP status?
  YES → Check specific code:
    - 408, 429 → TRANSIENT
    - 400, 401, 403, 404, 405, 422 → PERMANENT
  NO → Proceed to Step 4
```

**Step 2 - Assess Service Health Pattern**:

```
Is this the first failure for this operation?
  YES → TRANSIENT (single failure, likely transient)
  NO → Check failure pattern:
    - Intermittent (50% success rate) → TRANSIENT
    - Consistent (100% failure) → PERMANENT (likely config/code issue)
```

**Step 3 - Check Error Message Keywords**:

```
Contains "immutable", "invalid", "malformed", "unauthorized"?
  YES → PERMANENT
  NO → Proceed to Step 4

Contains "timeout", "unavailable", "connection refused"?
  YES → TRANSIENT
  NO → Proceed to Step 4
```

**Step 4 - Kubernetes-Specific Classification**:

```
Error type:
  - ImagePullBackOff (first occurrence) → TRANSIENT
  - ImagePullBackOff (persisting >5min) → PERMANENT (wrong image tag)
  - Immutability error → PERMANENT
  - Pod eviction → TRANSIENT
  - Admission webhook denial → PERMANENT
```

**Step 5 - Default to Conservative Classification**:

```
If unable to classify → Treat as PERMANENT
  - Log error for human review
  - Do NOT retry (safer than retry loop)
  - Escalate with full error context
```

---

## Integration with Agent Workflows (OODA Loop)

### OBSERVE Phase

- **Error Detection**: Capture full error context (status code, message, stack trace, operation details)
- **Pattern Recognition**: Check if error matches known transient/permanent patterns
- **Initial Classification**: Apply decision tree for preliminary classification

### ORIENT Phase

- **Context Gathering**: Query recent error history for same operation (circuit breaker state)
- **Service Health Check**: Assess if service is experiencing widespread issues
- **Confidence Scoring**: Calculate classification confidence (0.0-1.0)
- **Research Trigger**: If confidence <0.7 → delegate to researcher-external for error pattern research

### DECIDE Phase

- **Retry Decision**: TRANSIENT with confidence ≥0.7 → exponential backoff retry
- **Escalation Decision**: PERMANENT or FATAL → immediate escalation
- **Circuit Breaker Decision**: Check failure threshold, decide if should trip circuit breaker

### ACT Phase

- **Execute Retry**: Apply exponential backoff with jitter for transient errors
- **Apply Fallback**: Use degraded functionality if circuit breaker OPEN
- **Escalate**: Report permanent/fatal errors with full context and recovery guidance

---

## Examples with Classification Rationale

### Example 1: Kubernetes Immutability Error

```yaml
Error: 'error: the namespace of the provided object cannot be changed'
HTTP Status: 422 Unprocessable Entity

Classification: PERMANENT
Rationale:
  - Contains keyword "cannot be changed" (immutability)
  - HTTP 422 (semantic validation failure)
  - Kubernetes immutability constraint violation
  - Requires manifest fix (update strategy, not namespace change)

Action: Immediate failure, escalate to user with fix guidance
```

### Example 2: Network Timeout

```
Error: "dial tcp 10.96.0.1:443: i/o timeout"
Operation: kubectl get pods

Classification: TRANSIENT
Rationale:
  - Network timeout (temporary connectivity issue)
  - Intermittent (previous kubectl commands succeeded)
  - No indication of permanent failure

Action: Retry with exponential backoff (1s, 2s, 4s), max 3 attempts
```

### Example 3: Invalid Credentials

```
Error: "401 Unauthorized: invalid API key"
HTTP Status: 401

Classification: PERMANENT
Rationale:
  - HTTP 401 (authentication failure)
  - "invalid API key" (credential issue, not temporary)
  - Retrying will not succeed without credential fix

Action: Immediate failure, escalate to user to check API key configuration
```

### Example 4: Database Item Doesn't Exist

```
Error: "DynamoDB item not found: user_id=12345"
Operation: GetItem

Classification: FATAL
Rationale:
  - Data integrity issue (expected item missing)
  - Possible data loss or logical deletion
  - Continuing operation would cause cascading failures

Action: NEVER retry, immediate escalation to human for investigation
```

### Example 5: ImagePullBackOff (Transient)

```
Error: "Failed to pull image 'myregistry/app:v1.2.3': rpc error: code = Unknown desc = Error response from daemon: Get https://myregistry/v2/: net/http: request canceled"
Duration: 30 seconds
Previous pulls: Successful

Classification: TRANSIENT
Rationale:
  - First occurrence (previous pulls worked)
  - Network error during image pull (temporary registry issue)
  - "request canceled" suggests timeout, not permanent failure

Action: Retry with exponential backoff, monitor for sustained failure
```

### Example 6: ImagePullBackOff (Permanent)

```
Error: "Failed to pull image 'myregistry/app:v1.2.3': manifest unknown: manifest unknown"
Duration: 5 minutes, persisting
Previous pulls: Never succeeded

Classification: PERMANENT
Rationale:
  - "manifest unknown" (image tag doesn't exist)
  - Persisting failure (not transient)
  - No successful pulls in history

Action: Immediate failure, escalate to user to check image tag
```

---

## Decision Flow Summary

**When to Retry** (TRANSIENT only):

- Single occurrence of 5xx or network timeout
- Intermittent failures (50% success rate)
- Rate limiting (429) with retry-after header
- Apply exponential backoff with jitter
- Max 3 attempts, 20s max delay

**When to Escalate** (PERMANENT):

- 4xx errors (except 408, 429)
- Schema validation failures
- Authentication/authorization failures
- Kubernetes immutability errors
- Configuration errors
- Immediate failure, no retry

**When to Apply Circuit Breaker**:

- Sustained transient failures (50% failure rate over 10+ calls)
- Protects against cascading failures
- Allows service recovery time
- See `.claude/docs/01-guides/circuit-breaker-pattern.md`

**When to Escalate to Human** (FATAL):

- Data integrity violations
- Service crashes (OOM, segfault)
- Security violations
- Storage failures
- Control plane unavailable
- NEVER retry, immediate escalation

---

## Related Documentation

- **Circuit Breaker Pattern**: `.claude/docs/01-guides/circuit-breaker-pattern.md` - Automatic failure detection and recovery
- **Retry Strategies**: `.claude/docs/01-guides/retry-strategies.md` - Exponential backoff, jitter, retry budgets
- **deployment-release Agent**: `.claude/agents/deployment-release.md` - Kubernetes-specific error handling
- **debugger Agent**: `.claude/agents/debugger.md` - Debugging permanent errors

---

**Key Principle**: Conservative classification prevents retry loops. When in doubt, classify as PERMANENT and escalate for human review.
