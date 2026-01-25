# Phase 4: ACT - Execute & Validate

**OODA Stage**: ACT | **Time Allocation**: 55% of project

**Purpose**: Write production code, validate with tests, and verify performance meets requirements.

**Deliverable**: Production-ready code with passing tests and performance analysis

---

## Agent Delegation

| Step | Agent | Purpose |
|------|-------|---------|
| Write code | `Task(development)` | Implement components |
| Review code | `Task(code-quality)` | Quality validation |
| Run tests | `Task(code-quality)` | Execute test suite |
| Fix issues | `Task(debugger)` | Debug failures, fix issues |

**File-scoped delegation**: One file per Task() for retryability and parallelization.

---

## Workflow Steps

### Step 4.1: Implementation Sequence

**Order** (dependencies flow downward):
1. **Exceptions & Models** - Exception hierarchy, data classes (immutable)
2. **Interfaces** - Abstract base classes defining contracts
3. **Core Logic** - Business rules, retry strategies, validation
4. **Integrations** - External APIs, databases, caches
5. **Orchestration** - Main processor tying components together
6. **Observability** - Logging, metrics, tracing

### Step 4.2: Code Quality Standards

Apply these 7 categories during implementation:

| Category | Key Checks |
|----------|------------|
| **Readability** | Descriptive names, no magic numbers, comments explain *why* |
| **Maintainability** | DRY principle, config externalized, constants in one place |
| **Testability** | Dependency injection, explicit side effects, mockable interfaces |
| **Defensive** | Input validation, null checks, type hints, logging with context |
| **Error Handling** | Specific exception types, no silent failures, graceful degradation |
| **Performance** | Avoid O(n^2) when O(n) possible, prevent N+1 queries |
| **Documentation** | Type hints on all signatures, docstrings with examples |

### Step 4.3: Write Code

Delegate implementation to `development`:

```
Task(development):
  Goal: Implement {component} per design in {design-doc}
  Map: [target-file-path]
  Constraints: Follow quality standards, include type hints
```

### Step 4.4: Code Review

Delegate review to `code-quality`:
- All tests passing (unit, integration, e2e)
- Coverage >90% line, >80% branch
- No code duplication, no hardcoded secrets
- Error handling is specific, logging includes context

### Step 4.5: Run Tests & Validate

Delegate test execution to `code-quality`:
- **Happy path**: Verify normal operation, check side effects
- **Edge cases**: Input boundaries, idempotency, retry logic, race conditions
- **Output validation**: Response matches schema, serialization round-trips

### Step 4.6: Fix Issues (OODA Loop)

If tests fail, delegate to `debugger`:
1. **OBSERVE**: Gather failure evidence (logs, stack trace)
2. **ORIENT**: Trace through code, identify root cause
3. **DECIDE**: Plan fix approach
4. **ACT**: Apply fix, re-run tests

Repeat until all tests green.

### Step 4.7: Complexity Analysis (If Needed)

For performance-critical features, analyze:

| Analysis | Questions |
|----------|-----------|
| **Time Complexity** | Big-O for each function? Meets latency requirements? |
| **Space Complexity** | Memory per request? Within pod limits? |
| **Bottlenecks** | Where is time spent? (measure, don't guess) |
| **Optimization ROI** | Benefit vs complexity trade-off? |

**Key principle**: Accept external constraints (API latency), optimize what you control.

---

## Quick Checklist

Before completing Phase 4:

- [ ] All tests passing (100% test suite)
- [ ] Code coverage >90% line, >80% branch
- [ ] Code is testable (dependency injection, no hidden side effects)
- [ ] Error handling is specific with contextual logging
- [ ] Type hints on all public APIs
- [ ] Performance meets requirements (p95 latency, throughput)
- [ ] Edge cases handled (empty input, nulls, race conditions)
- [ ] Ready for deployment

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Direct file edits | Always delegate via Task() |
| Bare `except:` clauses | Catch specific exception types |
| Missing edge case tests | Apply edge case matrix from Phase 1 |
| Premature optimization | Measure bottlenecks first, then optimize |
| Skipping code review | Quality gate before marking complete |

---

## Exit Criteria

**All criteria must pass to complete**

| Criterion | Weight | Check |
|-----------|--------|-------|
| Tests passing | 0.30 | 100% test suite green |
| Code coverage | 0.25 | >90% line, >80% branch |
| Quality review | 0.20 | Code review approved |
| Performance | 0.15 | Meets latency/throughput requirements |
| Documentation | 0.10 | Type hints + docstrings complete |

---

## Reference Documentation

- [agent-design-best-practices.md](../../../docs/01-guides/agents/agent-design-best-practices.md)
- [golden-agent-standards.md](../../../docs/01-guides/agents/golden-agent-standards.md)

---

**Previous Phase**: [Phase 3: DECIDE - Implementation Planning](phase-3-decide.md)

**Complete**: Return to [SKILL.md](../SKILL.md)
