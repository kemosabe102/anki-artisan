# Phase 1: OBSERVE - Problem Definition

**OODA Stage**: OBSERVE | **Time Allocation**: 15% of project

**Purpose**: Nail down exactly what you're solving before design or implementation.

**Deliverable**: Problem Statement & Requirements Report

---

## Agent Delegation

| Step | Agent | Purpose |
|------|-------|---------|
| Research codebase | `Task(researcher-codebase)` | Find existing patterns, dependencies |
| Research best practices | `Task(researcher-external)` | Industry standards, external solutions |

**Parallel execution**: Both research tasks can run simultaneously ⚡

---

## Workflow Steps

### Step 1.1: Problem Statement Definition

**Questions to answer**:
- What is the core problem? (one sentence)
- Who is the user/consumer?
- Why does it matter? (business value)
- What triggered this work?

**Output**: One-sentence problem + executive summary

### Step 1.2: Inputs, Outputs & Side Effects

**Document**:
- **Inputs**: Format, range, source (JSON, Protobuf, SQL)
- **Outputs**: Schema, destination (HTTP, database, event stream)
- **Side Effects**: DB writes, API calls, logs, metrics, cache

### Step 1.3: Constraints & Requirements

**Categories**:
- **Performance**: Latency (p50/p95/p99), throughput (QPS), availability (99.9%?)
- **Reliability**: Idempotency, consistency, durability, retry semantics
- **Compliance**: Security, data residency, audit logging
- **Resources**: Memory limits, CPU constraints, storage budget

### Step 1.4: Edge Cases & Failure Modes

**Identify 5+ edge cases across categories**:
- **Input boundaries**: Empty, max size, malformed, encoding
- **System failures**: Network timeout, dependency down, disk full
- **Concurrency**: Race conditions, duplicate requests, ordering
- **Degradation**: Partial outages, circuit breaker triggers

### Step 1.5: Integration Points & Data Flow

**Document**:
- External dependencies and their SLAs
- Data persistence layer(s)
- Observability: logs, metrics, traces
- Backwards compatibility requirements

---

## Quick Checklist

Before advancing to Phase 2 (ORIENT):

- [ ] Problem is clear in one sentence
- [ ] All constraints explicit and measurable
- [ ] 5+ edge cases identified with expected behavior
- [ ] Success criteria defined and measurable
- [ ] Integration points documented with SLAs
- [ ] User/stakeholder approved requirements

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Vague problem statement | Use "verb + object + constraint" format |
| Missing edge cases | Apply edge case matrix systematically |
| Unclear constraints | Assign numbers to performance requirements |
| Assuming requirements | Validate with user before proceeding |
| Skipping this phase | NEVER proceed to ORIENT without clear requirements |

---

## Output Template

See [problem-statement.template.md](../templates/problem-statement.template.md)

---

## Reference Documentation

- [thinking-frameworks-catalog.md](../../../docs/00-core/frameworks/README.md) - 5W1H framework
- [ooda-loop-framework.md](../../../docs/00-core/ooda-loop-framework.md) - OBSERVE stage details

---

## Exit Criteria

**CQ (Context Quality) ≥ 0.85 required to proceed**

| Criterion | Weight | Check |
|-----------|--------|-------|
| Problem clarity | 0.30 | One-sentence statement exists |
| Constraints defined | 0.25 | All categories have values |
| Edge cases | 0.20 | 5+ documented with behavior |
| Success criteria | 0.15 | Measurable metrics defined |
| User approval | 0.10 | Stakeholder sign-off obtained |

**Next Phase**: [Phase 2: ORIENT - Architecture Design](phase-2-orient.md)
