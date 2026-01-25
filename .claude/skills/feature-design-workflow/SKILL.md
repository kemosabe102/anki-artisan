---
name: feature-design-workflow
description: >
  OODA-based feature design workflow using Task() delegation to specialist agents.
  Use when designing new features, planning implementations, or architecting solutions.
  Follows test-driven development with phased delivery and validation checkpoints.
  Trigger terms: "design feature", "plan implementation", "architect solution", 
  "new feature workflow", "TDD planning".
---

# Feature Design Workflow Skill

*Four-phase, OODA-aligned, delegation-focused feature design*

## Quick Start

| User Says | Action |
|-----------|--------|
| "design a new feature for X" | Run full workflow (Phases 1-4) |
| "help me plan X implementation" | Start at Phase 2 (ORIENT) |
| "review my architecture for X" | Jump to Phase 2 validation |
| "I have requirements, help me implement" | Start at Phase 3 (DECIDE) |

---

## Delegation Model: You Orchestrate, Agents Execute

**CRITICAL**: This skill is an ORCHESTRATOR. You do NOT edit files directly.

```
┌─────────────────────────────────────────────────────────────────┐
│  YOU (Skill)                      AGENTS (via Task)             │
│  ─────────────                    ─────────────────             │
│  • Guide the workflow             • Research codebase           │
│  • Make decisions                 • Validate architecture       │
│  • Coordinate phases              • Create test specs           │
│  • Synthesize outputs             • Write production code       │
│  • Track progress                 • Run tests & fix issues      │
└─────────────────────────────────────────────────────────────────┘
```

### Delegation Rule (MANDATORY)

**ALL work requires Task() delegation. You coordinate, agents execute.**

| Operation | Delegate To | You NEVER Do |
|-----------|-------------|--------------|
| Explore codebase | `Task(researcher-codebase)` | Grep/Read files yourself |
| Research patterns | `Task(researcher-external)` | WebSearch yourself |
| Validate architecture | `Task(architectureer)` | Analyze design yourself |
| Review specs | `Task(planning)` | Read specs yourself |
| Create tests | `Task(code-quality)` | Write tests yourself |
| Write code | `Task(development)` | Edit files yourself |
| Review code | `Task(code-quality)` | Analyze code yourself |
| Run tests | `Task(code-quality)` | Run pytest yourself |
| Fix bugs | `Task(debugger)` | Debug yourself |

See [delegation/patterns.md](delegation/patterns.md) for Task() templates.

---

## EXECUTION CONTRACT (MANDATORY)

**This contract MUST be enforced. Skipping phases without explicit flags is a WORKFLOW VIOLATION.**

### Phase Completion Requirements

Before advancing to next phase, orchestrator MUST complete ALL steps:

| Phase | Required Steps | Skip Flag | Exit Criteria |
|-------|---------------|-----------|---------------|
| 1. OBSERVE | Research + Requirements | `--skip-research` | Problem statement clear |
| 2. ORIENT | Design + Architecture | None (required) | Architecture approved |
| 3. DECIDE | Test specs + Risk analysis | `--skip-tests` | Implementation plan approved |
| 4. ACT | Implement + Validate | None (required) | All tests passing |

**BLOCKED**: Advancing without completing prior phase is a WORKFLOW VIOLATION.

### Human Review Gates

| Phase | Gate | Approval Required Before |
|-------|------|-------------------------|
| Phase 1 → 2 | Requirements Review | Starting architecture design |
| Phase 2 → 3 | Architecture Approval | Starting implementation planning |
| Phase 3 → 4 | Implementation Plan Approval | Writing any code |


---

## Workflow Overview: 4 Phases (OODA)

```
OBSERVE (Phase 1)          ORIENT (Phase 2)           DECIDE (Phase 3)          ACT (Phase 4)
─────────────────          ────────────────           ────────────────          ─────────────
Problem Definition    →    Architecture Design    →   Implementation Plan   →   Execute & Validate
Requirements              Pattern Selection          Test Specifications       Write Code
Edge Cases                Trade-off Analysis         Risk Identification       Run Tests
Constraints               Data Structures            Effort Estimation         Fix Issues
                                                                               Optimize

⚡ parallel research       🔗 sequential design       ⚡ parallel test specs    🔗 sequential impl
```

### Time Allocation

| Phase | % of Effort | Focus |
|-------|-------------|-------|
| OBSERVE | 15% | Gather requirements, explore codebase |
| ORIENT | 25% | Design architecture, evaluate trade-offs |
| DECIDE | 5% | Finalize plan, get approval |
| ACT | 55% | Implement, test, validate, optimize |

---

## Phase 1: OBSERVE - Problem Definition

**Goal**: Nail down exactly what you're solving before any design or implementation.

**Deliverable**: Problem Statement & Requirements Report ([template](templates/problem-statement.template.md))


### Steps

1. **Research existing patterns** → `Task(researcher-codebase)`
2. **Research best practices** → `Task(researcher-external)` 
3. **Define problem statement** (one sentence)
4. **Document I/O, constraints, edge cases**
5. **Identify success criteria**

### Quick Checklist

- [ ] Problem is clear in one sentence
- [ ] All constraints explicit (performance, reliability, compliance)
- [ ] 5+ edge cases identified
- [ ] Success criteria measurable
- [ ] Integration points documented

**Detailed guide**: [phases/phase-1-observe.md](phases/phase-1-observe.md)

**Reference docs**: 
- [thinking-frameworks-catalog.md](../../docs/00-core/frameworks/README.md) (5W1H framework)
- [ooda-loop-framework.md](../../docs/00-core/ooda-loop-framework.md)

---

## Phase 2: ORIENT - Architecture Design

**Goal**: Decompose the problem, evaluate approaches, and select architecture.

**Deliverable**: Architecture & Design Report ([template](templates/architecture-report.template.md))

### Steps

1. **Decompose problem** into sub-problems
2. **Evaluate approaches** (2-3 per sub-problem)
3. **Select design patterns** with justification
4. **Validate architecture** → `Task(architectureer)`
5. **Review specifications** → `Task(planning)`
6. **Design data structures & interfaces**

### Quick Checklist

- [ ] All sub-problems have evaluated approaches
- [ ] Architecture diagram created
- [ ] Design patterns justified (not just applied)
- [ ] Data structures designed (immutable, typed)
- [ ] Trade-offs explicitly documented

**Detailed guide**: [phases/phase-2-orient.md](phases/phase-2-orient.md)

**Reference docs**:
- [architecture-scoring-rubric.md](../../docs/01-guides/architecture/architecture-scoring-rubric.md)
- [tool-design-patterns.md](../../docs/01-guides/architecture/tool-design-patterns.md)

---

## Phase 3: DECIDE - Implementation Strategy

**Goal**: Plan test-driven implementation, define test cases, identify risks.

**Deliverable**: Implementation Strategy Report ([template](templates/implementation-plan.template.md))

### Steps

1. **Define test pyramid** (75% unit / 20% integration / 5% E2E)
2. **Create test specifications** → `Task(code-quality)`
3. **Analyze complexity** → `Task(tech-debt-investigator)`
4. **Identify risks and mitigations**
5. **Estimate effort per component**
6. **Get implementation plan approval**

### Quick Checklist

- [ ] 50+ unit test cases designed
- [ ] 15+ integration test cases designed
- [ ] Risk register created with mitigations
- [ ] Effort estimated per task
- [ ] Implementation sequence defined
- [ ] User approval obtained

**Detailed guide**: [phases/phase-3-decide.md](phases/phase-3-decide.md)

**Reference docs**:
- [development-pytest-framework.md](../../docs/00-core/development-pytest-framework.md)
- [testing-failure-categorization.md](../../docs/01-guides/testing/testing-failure-categorization.md)

---

## Phase 4: ACT - Execute & Validate

**Goal**: Write clean, testable code that passes all tests.

**Deliverable**: Production-ready code with >90% test coverage

### Steps

1. **Implement in sequence**: exceptions → interfaces → logic → integrations
2. **Write code** → `Task(development)` (one file at a time)
3. **Review code** → `Task(code-quality)`
4. **Run tests** → `Task(code-quality)`
5. **Fix issues** → `Task(debugger)`
6. **Validate edge cases**
7. **Analyze performance** (if needed)

### Quick Checklist

- [ ] All tests passing (100%)
- [ ] Code coverage >90%
- [ ] No critical issues from code review
- [ ] Edge cases validated
- [ ] Performance within constraints

**Detailed guide**: [phases/phase-4-act.md](phases/phase-4-act.md)

**Reference docs**:
- [agent-design-best-practices.md](../../docs/01-guides/agents/agent-design-best-practices.md)
- [golden-agent-standards.md](../../docs/01-guides/agents/golden-agent-standards.md)


---

## Agent Delegation Matrix

| Phase | Agent | Purpose | Parallel? |
|-------|-------|---------|-----------|
| OBSERVE | `researcher-codebase` | Explore existing patterns | ⚡ Yes |
| OBSERVE | `researcher-external` | Research best practices | ⚡ Yes |
| ORIENT | `architectureer` | Validate design decisions | 🔗 No |
| ORIENT | `planning` | Review requirements completeness | ⚡ Yes |
| ORIENT | `tech-debt-investigator` | Assess complexity | ⚡ Yes |
| DECIDE | `code-quality` | Generate test specifications | 🔗 No |
| ACT | `development` | Write production code | 🔗 No |
| ACT | `code-quality` | Review code quality | 🔗 After impl |
| ACT | `code-quality` | Run test suites | 🔗 After review |
| ACT | `debugger` | Fix failing tests/issues | 🔗 After tests |

**Parallel Legend**: ⚡ = can run in parallel | 🔗 = must run sequentially

---

## Quality Gates

| Phase | Exit Gate | Confidence Required |
|-------|-----------|---------------------|
| OBSERVE → ORIENT | Requirements complete | CQ ≥ 0.85 |
| ORIENT → DECIDE | Architecture approved | User approval |
| DECIDE → ACT | Implementation plan approved | User approval |
| ACT → Complete | All tests passing | 100% green |

---

## State Management

Track progress through the workflow:

```python
feature_workflow_state = {
    "current_phase": "OBSERVE",  # OBSERVE | ORIENT | DECIDE | ACT | COMPLETE
    "phase_status": {
        "observe": {"research_done": False, "requirements_doc": None},
        "orient": {"architecture_done": False, "design_doc": None},
        "decide": {"tests_planned": False, "impl_plan": None},
        "act": {"code_complete": False, "tests_passing": False}
    },
    "skip_flags": [],  # ["--skip-research", "--skip-tests"]
    "deliverables": []  # List of output document paths
}
```

---

## Anti-Patterns (NEVER DO)

- Execute phases directly (ALWAYS use Task() delegation)
- Read/analyze files yourself (delegate to researcher-codebase)
- Write code yourself (delegate to development)
- Skip ORIENT phase (architecture must be validated)
- Implement before tests are designed (TDD required)
- Optimize before measuring (premature optimization)
- Assume requirements (always validate with user)

---

## Error Recovery

| Error Type | Recovery | Framework |
|------------|----------|-----------|
| Research finds no patterns | Delegate to researcher-external for external best practices | ReACT (iterative discovery) |
| Architecture review fails | Return to ORIENT, address findings, re-validate | Pre-Mortem (identify what went wrong) |
| Test creation blocked | Clarify requirements with user, return to OBSERVE | First Principles (re-examine assumptions) |
| Implementation fails | Delegate to debugger, iterate until tests pass | ReACT (observe→refine loop) |
| Tests fail after implementation | Fix bugs before proceeding, do not skip | ReACT (systematic debugging) |

> **Recovery Tip**: When stuck, apply First Principles to break through constraints, or Pre-Mortem to identify root causes.

---

## Success Criteria

The workflow is complete when:

- [ ] Problem statement approved by user
- [ ] Architecture validated by architectureer
- [ ] Test specifications created (50+ unit, 15+ integration)
- [ ] Implementation complete with >90% coverage
- [ ] All tests passing (100% green)
- [ ] Code review completed with no critical issues
- [ ] User approves final deliverables

---

## Reference Documentation

- **TDD Chunking Guide** -> [reference/tdd-chunking.md](reference/tdd-chunking.md)

---

## Documentation References

| Topic | Document |
|-------|----------|
| Thinking Frameworks | [thinking-frameworks-catalog.md](../../docs/00-core/frameworks/README.md) |
| OODA Loop | [ooda-loop-framework.md](../../docs/00-core/ooda-loop-framework.md) |
| Architecture Review | [architecture-scoring-rubric.md](../../docs/01-guides/architecture/architecture-scoring-rubric.md) |
| Test Framework | [development-pytest-framework.md](../../docs/00-core/development-pytest-framework.md) |
| Code Quality | [agent-design-best-practices.md](../../docs/01-guides/agents/agent-design-best-practices.md) |
| Agent Selection | [agent-selection-guide.md](../../docs/01-guides/agents/agent-selection-guide.md) |
| Skill Delegation | [skill-delegation-model.md](../../docs/01-guides/skills/skill-delegation-model.md) |

---

## Phase Navigation

| From Current Phase | User Says | Navigate To |
|-------------------|-----------|-------------|
| Any | "start over" | Phase 1 (OBSERVE) |
| OBSERVE | "requirements done" | Phase 2 (ORIENT) |
| ORIENT | "architecture approved" | Phase 3 (DECIDE) |
| DECIDE | "ready to implement" | Phase 4 (ACT) |
| ACT | "all tests passing" | COMPLETE |
| Any | "go back" | Previous phase |

---

## Thinking Frameworks

When facing complex design challenges, these frameworks guide systematic problem-solving.

**Full Catalog**: [Thinking Frameworks README](../../docs/00-core/frameworks/README.md)

**Most Relevant for Feature Design**:

| Framework | When to Use |
|-----------|-------------|
| [CAGEERF](../../docs/00-core/frameworks/structured-execution.md) | Large feature planning, multi-phase execution |
| [First Principles](../../docs/00-core/frameworks/creative.md) | Breaking through design constraints |
| [Pre-Mortem](../../docs/00-core/frameworks/strategy.md) | Risk identification before implementation |
| [ReACT](../../docs/00-core/frameworks/analysis.md) | Research gaps, iterative discovery |

> **Selection Tip**: large projects→CAGEERF, innovation→First Principles, risk→Pre-Mortem, research→ReACT
