# Phase 3: DECIDE - Implementation Strategy (Test-Driven)

**OODA Stage**: DECIDE | **Time Allocation**: 5% of project

**Purpose**: Plan test-driven implementation, define test cases, identify risks before production code.

**Deliverable**: Test-Driven Implementation Plan with test cases, mocking strategies, effort estimates, and risk mitigation.

---

## Agent Delegation

| Step | Agent | Purpose |
|------|-------|---------|
| Test case generation | `Task(code-quality)` | Generate unit/integration/E2E test specs |
| Risk assessment | `Task(tech-debt-investigator)` | Identify technical risks and mitigation |

**Sequential execution**: Test specs inform risk assessment.

---

## Workflow Steps

### Step 3.1: Test-Driven Approach

**Test Pyramid (by count)**:
- **Unit Tests (75%)**: Single function/class in isolation - fast, deterministic
- **Integration Tests (20%)**: Module + mocked external services - moderate speed
- **E2E Tests (5%)**: Full system with real dependencies - slow, valuable for critical paths

### Step 3.2: Unit Test Cases (Target: 50+ tests)

**Coverage areas**:
- Core business logic (happy path + edge cases)
- Input validation and boundary conditions
- Error handling and exception paths
- State transitions and invariants

### Step 3.3: Integration Test Cases (Target: 15+ tests)

**Focus areas**:
- Component collaboration and data flow
- External service interactions (mocked)
- Database transactions and consistency
- Cache behavior and invalidation

### Step 3.4: End-to-End Test Cases (Target: 5+ tests)

**Critical paths only**:
- Happy path with real dependencies
- Error recovery and retry scenarios
- Idempotency and duplicate handling
- Failure modes and graceful degradation

### Step 3.5: Mocking & Test Fixtures

**Required artifacts**:
- Mock clients for external APIs (deterministic behavior queues)
- Test data builders (fluent interface pattern)
- Shared fixtures in `conftest.py`
- In-memory substitutes for Redis/database

### Step 3.6: Risk Identification & Mitigation

**Risk Register Format**:

| Risk | Likelihood | Impact | Mitigation | Effort |
|------|------------|--------|------------|--------|
| Race condition in concurrent operations | Medium | Critical | Pessimistic locking | Medium |
| External service timeout | Medium | High | Circuit breaker, fail-fast | Low |
| Connection pool exhaustion | Low | High | Pooling, monitoring, auto-scale | Medium |
| Data inconsistency on crash | Low | Critical | Write-ahead logging | Low |


### Step 3.7: Effort Estimation

**Estimate per task** (engineering hours, not calendar time):
- Data classes + schema: 4h
- External integrations: 6-8h each
- Unit tests (50+): 12h
- Integration tests (15+): 8h
- E2E tests (5+): 6h
- Documentation + runbook: 4h

---

## Quick Checklist

Before advancing to Phase 4 (ACT):

- [ ] Tests designed BEFORE implementation code
- [ ] 50+ unit tests covering edge cases specified
- [ ] 15+ integration tests for component interaction
- [ ] 5+ E2E tests for critical user flows
- [ ] Mock objects designed for external dependencies
- [ ] 5+ risks identified with mitigation strategies
- [ ] Effort estimated for each implementation task
- [ ] Coverage target: >90% line, >80% branch

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Writing tests after code | Test specs FIRST, implementation second |
| Insufficient unit tests | Aim for 50+ covering all edge cases |
| Missing integration tests | Verify component collaboration explicitly |
| Ignoring risk register | Document at least 5 risks with mitigations |
| No effort estimates | Break down and estimate each task |
| Skipping mocking design | Plan mock behavior before implementation |


---

## Exit Criteria

**Plan approval required to proceed to ACT**

| Criterion | Weight | Check |
|-----------|--------|-------|
| Test pyramid defined | 0.25 | Unit/Integration/E2E breakdown documented |
| Unit test specs | 0.25 | 50+ test cases with expected behavior |
| Integration test specs | 0.20 | 15+ tests for component interaction |
| Risk register | 0.15 | 5+ risks with mitigation strategies |
| Effort estimates | 0.15 | Per-task breakdown with total hours |

---

## Reference Documentation

- [development-pytest-framework.md](../../../docs/00-core/development-pytest-framework.md) - Pytest best practices
- [testing-failure-categorization.md](../../../docs/01-guides/testing/testing-failure-categorization.md) - Test failure taxonomy

---

**Previous Phase**: [Phase 2: ORIENT - Architecture Design](phase-2-orient.md)

**Next Phase**: [Phase 4: ACT - Implementation](phase-4-act.md)
