# Phase 2: ORIENT - Architecture Design

**OODA Stage**: ORIENT | **Time Allocation**: 25% of project

**Purpose**: Decompose problems, evaluate approaches, select architecture balancing complexity, performance, and maintainability.

**Deliverable**: Architecture & Design Report with ADR and implementation roadmap.

---

## Agent Delegation

| Step | Agent | Purpose |
|------|-------|---------|
| Architecture review | `Task(architectureer)` | Validate patterns, identify risks |
| Spec validation | `Task(planning)` | Ensure requirements completeness |
| Debt assessment | `Task(tech-debt-investigator)` | Surface existing debt affecting design |

**Sequential execution**: Architecture review depends on spec validation output.

---

## Workflow Steps

### Step 2.1: Problem Decomposition

**Input**: Problem Statement & Requirements Report (Phase 1)

**Process**:
1. **Identify major functional components** - Core responsibilities, decoupling opportunities, boundaries
2. **List sub-problems for each component** - Idempotency, retries, consistency, observability
3. **Prioritize by criticality and coupling** - Which block others? Which are independent?

**Output**: Hierarchical breakdown of sub-problems with dependencies mapped.

### Step 2.2: Approach Evaluation

**For each sub-problem, create comparison matrix**:

| Approach | Implementation | Pros | Cons | Use Case |
|----------|----------------|------|------|----------|
| Option A | Brief description | Benefits | Trade-offs | When to use |
| Option B | Brief description | Benefits | Trade-offs | When to use |

**Output**: Recommendation with rationale for each sub-problem.

### Step 2.3: Design Patterns & OOP

**Pattern Selection Criteria**:
- Does it reduce complexity or add unnecessary abstraction?
- Is it reusable across the codebase?
- What's the maintenance cost?

**Common Patterns**: Strategy (pluggable algorithms), Repository (data access), Circuit Breaker (fault tolerance), Builder (complex objects)

**Output**: Patterns chosen with trade-off justification.

### Step 2.4: Architecture Decision Record (ADR)

```markdown
# ADR: [Decision Title]

## Status: Accepted

## Context
[Problem requiring decision]

## Decision
[Chosen approach]

## Rationale
[Why this approach over alternatives]

## Alternatives Considered
[Options rejected and why]

## Consequences
- (+) Positive impacts
- (-) Trade-offs and costs
```

### Step 2.5: Data Structures & Interfaces

**Define**:
- **Data classes**: Immutable, serializable, validated
- **Interfaces**: Abstract contracts for major components
- **Enums**: Typed states and categories

**Output**: Python dataclasses, ABCs, and type definitions.

### Step 2.6: Implementation Order & Roadmap

**Sequence by dependency order**:
1. Foundation (data structures, migrations)
2. Core logic (primary algorithms, interfaces)
3. Integration (external services, storage)
4. Observability (logging, metrics, tracing)
5. Hardening (testing, chaos, load)

**Output**: Phased roadmap with effort estimates.

---

## Quick Checklist

- [ ] Problem decomposed into independent sub-problems
- [ ] 2-3 approaches evaluated per major sub-problem
- [ ] Trade-offs documented for each approach
- [ ] Design patterns justified (not over-engineered)
- [ ] ADR captures key decisions with rationale
- [ ] Data structures and interfaces defined
- [ ] Implementation sequenced in dependency order
- [ ] Risks identified with mitigations

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Jumping to implementation | Complete decomposition first |
| Over-engineering patterns | Justify each pattern's value |
| Missing trade-off analysis | Document pros AND cons |
| Vague ADRs | Include specific consequences |
| Ignoring existing code | Check COMPONENT_ALMANAC.md |
| Monolithic design | Decompose into testable units |

---

## Exit Criteria

**CQ (Context Quality) >= 0.85 required to proceed**

| Criterion | Weight | Check |
|-----------|--------|-------|
| Decomposition complete | 0.25 | All sub-problems identified |
| Approaches evaluated | 0.25 | Comparison matrices exist |
| ADR documented | 0.20 | Decisions with rationale |
| Interfaces defined | 0.15 | Contracts specified |
| Roadmap sequenced | 0.15 | Implementation order clear |

---

## Reference Documentation

- [architecture-scoring-rubric.md](../../../docs/01-guides/architecture/architecture-scoring-rubric.md)
- [tool-design-patterns.md](../../../docs/01-guides/architecture/tool-design-patterns.md)

---

**Previous**: [Phase 1: OBSERVE - Problem Definition](phase-1-observe.md)
**Next**: [Phase 3: DECIDE - Implementation Planning](phase-3-decide.md)
