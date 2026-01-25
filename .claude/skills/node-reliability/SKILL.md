---
name: node-reliability
description: >
  Lawyer reliability review for node contracts and invariants. Evaluates invariant
  core (preconditions, postconditions, class invariants), resource bounds (allocations,
  complexity, regex safety), and failure strategy (typed exceptions, atomic failure).
  Use for: component contract validation. Trigger keywords: node reliability, contract
  validation, invariant, precondition, resource bound.
allowed-tools: Read, Glob, Grep
---

# Node Reliability Skill

**Purpose**: Systematic checklist for evaluating reliability of component contracts (Lawyer hat).

**Use Cases**:
- Precondition validation
- Postcondition guarantees
- Class invariant enforcement
- Resource bound verification
- Exception handling quality

## Source Documents

This skill derives its checklists from:
- `.claude/docs/01-guides/review/system-node-reliability.md`

---

## Checklist Categories

### 1. Invariant Core (Design by Contract)

| Check | Severity | Evidence Pattern |
|-------|----------|------------------|
| Input validation fails immediately (preconditions first) | HIGH | Look for early returns, guard clauses |
| Return value guarantees (never null list, only empty) | MEDIUM | Check return statements, type hints |
| Class invariants enforced (no half-broken states) | HIGH | Check constructor, state mutations |


### 2. Resource Bound (Algorithmic Safety)

| Check | Severity | Evidence Pattern |
|-------|----------|------------------|
| No unbounded allocations based on user input | CRITICAL | Look for list/dict creation from input |
| O(n) complexity (no hidden nested loops) | MEDIUM | Check for nested iterations, recursion |
| Regex safety (no catastrophic backtracking) | HIGH | Look for regex patterns, ReDoS risk |

### 3. Failure Strategy (Exception Hierarchy)

| Check | Severity | Evidence Pattern |
|-------|----------|------------------|
| Typed exceptions (not generic RuntimeException) | MEDIUM | Check exception classes, hierarchy |
| Atomic failure (all-or-nothing, no dirty state) | HIGH | Look for partial updates, cleanup |
| Rich error context in exception messages | LOW | Check exception messages for values |

---

## Reference Files

- `reference/invariant-checklist.md` - Invariant core checks
- `reference/resource-bound-checklist.md` - Resource bound checks
- `reference/failure-strategy-checklist.md` - Failure strategy checks

## Related Skills

- `edge-reliability` - Graph Theorist hat (edge boundaries)
- `operational-reliability` - Operator + Historian hats
