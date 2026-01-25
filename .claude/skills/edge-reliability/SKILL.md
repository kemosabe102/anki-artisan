---
name: edge-reliability
description: >
  Graph Theorist reliability review for edge boundaries. Evaluates temporal edges
  (timeouts, race conditions, backpressure), semantic edges (schema evolution,
  idempotency), failure propagation (retry storms, bulkheading), and monolith-specific
  patterns (transactional edges, shared resources). Use for: integration boundary
  reliability analysis. Trigger keywords: edge reliability, timeout review, race
  condition, backpressure, bulkhead.
allowed-tools: Read, Glob, Grep
---

# Edge Reliability Skill

**Purpose**: Systematic checklist for evaluating reliability at integration edges (Graph Theorist hat).

**Use Cases**:
- Timeout budget validation
- Race condition detection
- Backpressure mechanism verification
- Retry storm prevention
- Bulkhead pattern compliance
- Monolith transactional safety

## Source Documents

This skill derives its checklists from:
- `.claude/docs/01-guides/review/system-edge-reliability.md`
- `.claude/docs/01-guides/review/monolith-edge-reliability.md`

---

## Checklist Categories

### 1. Temporal Edge (Dynamics & Latency)

| Check | Severity | Evidence Pattern |
|-------|----------|------------------|
| Cross-component call has timeout < upstream timeout | HIGH | Look for `timeout=` or HTTP client config |
| Race condition guards present | CRITICAL | Check for locks, atomic ops, or event ordering |
| Backpressure mechanism exists | MEDIUM | Look for queue limits, flow control, or rate limiting |


### 2. Semantic Edge (Contracts & Compatibility)

| Check | Severity | Evidence Pattern |
|-------|----------|------------------|
| Schema evolution strategy exists | HIGH | Look for version fields, unknown field handling |
| Implicit assumptions documented | MEDIUM | Check comments, type hints, contracts |
| Idempotent message handling | HIGH | Look for dedup keys, at-least-once handling |

### 3. Failure Propagation Edge (Blast Radius)

| Check | Severity | Evidence Pattern |
|-------|----------|------------------|
| Exponential backoff + jitter for retries | MEDIUM | Check retry logic, backoff config |
| Thread/connection bulkheading | HIGH | Look for pool isolation, circuit breakers |
| Default fallback when edges fail | MEDIUM | Check error handling, degraded modes |

### 4. Transactional Edge (Monolith-Specific)

| Check | Severity | Evidence Pattern |
|-------|----------|------------------|
| Sandwich rule compliance (txn as meat not bread) | HIGH | Check @Transactional scope |
| No external API calls inside transaction | CRITICAL | Look for HTTP/gRPC calls in txn blocks |
| Component update ordering prevents deadlocks | CRITICAL | Check lock ordering consistency |

### 5. Shared Resource Edge (Monolith-Specific)

| Check | Severity | Evidence Pattern |
|-------|----------|------------------|
| Thread pool isolation (bulkheading) | HIGH | Check executor config, pool separation |
| Memory bounds on loads | HIGH | Look for findAll(), unbounded queries |
| Static cache eviction policy | MEDIUM | Check cache config, TTL settings |

---

## Reference Files

- `reference/system-edge-checklist.md` - Detailed system edge checks
- `reference/monolith-edge-checklist.md` - Monolith-specific edge checks

## Related Skills

- `node-reliability` - Lawyer hat (node contracts)
- `operational-reliability` - Operator + Historian hats
