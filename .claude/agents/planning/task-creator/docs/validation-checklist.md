# Task-Creator Validation Checklist

> **Single authoritative quality gate for task generation.**

**Extends**: `base-agent-pattern.md` (Validation Checklist)

---

## Pre-Generation Gate (Phase 1)

**Purpose**: Validate input before processing begins.

| Check | Rule | Severity |
|-------|------|----------|
| Input exists | PLAN.md file found at specified path | BLOCKING |
| Input readable | PLAN.md parses without errors | BLOCKING |
| Sections present | >=3 of 5 required sections found | BLOCKING |

**Required Sections** (need 3+): Technical Debt, Implementation Plan, Dependencies, Success Criteria, Risk Assessment


---

## Task Quality Gate (Phase 4)

**Purpose**: Validate each generated task meets quality standards.

| Check | Rule | Severity |
|-------|------|----------|
| Specificity | All 4 components present (ACTION_VERB, SCOPE, FILE_PATH, CRITERIA) | BLOCKING |
| Operation Type | Each task has [C]/[M]/[D] | BLOCKING |
| Agent Assignment | Each task has valid agent (Tier 1 or Tier 2 match) | BLOCKING |
| T-ID Format | Follows T###[T/I] convention | BLOCKING |
| Dependencies | All dependencies use valid T-IDs | WARNING |

### Task Anatomy (All 4 Required)

| Component | Check | Example |
|-----------|-------|---------|
| ACTION_VERB | Imperative verb present | Create, Implement, Add, Fix, Update, Refactor, Delete, Test |
| SCOPE | Bounded change description | "calculate_metrics() function", "MetricResult dataclass" |
| FILE_PATH | Target file(s) specified | "packages/metrics/engine.py" |
| ACCEPTANCE_CRITERIA | Measurable done condition | "tests pass", "schema validates", "lint clean" |

### File Operation Validation

| Operation | Symbol | Prerequisite Check | If Fails |
|-----------|--------|-------------------|----------|
| CREATE | [C] | Parent directory exists? | Add mkdir task as dependency |
| MODIFY | [M] | File exists? | Change to [C] or flag error |
| DELETE | [D] | File exists? | Skip task or flag warning |

---

## TDD Gate (Phase 4.3)

**Purpose**: Structural enforcement of test-first development.

| Check | Rule | Severity |
|-------|------|----------|
| Pair Complete | Every T###I has T###T | BLOCKING |
| Order Correct | T###T.order < T###I.order | BLOCKING |
| Dependency Link | T###I.dependencies includes T###T | BLOCKING |

### TDD Validation Algorithm

```
FOR each task in task_list:
  IF task.id matches pattern T[0-4]XX[I]:
    base_id = extract_base(task.id)  # T001I -> T001
    test_id = base_id + "T"          # T001T
    
    ASSERT test_id EXISTS in task_list
      ELSE FAIL: "Missing test task {test_id} for {task.id}"
    
    ASSERT task_list.index(test_id) < task_list.index(task.id)
      ELSE FAIL: "Order violation: {test_id} must precede {task.id}"
    
    ASSERT test_id IN task.depends_on
      ELSE FAIL: "Dependency missing: {task.id}.depends_on must include {test_id}"
```

### TDD Validation Examples

| Scenario | Input | Result | Reason |
|----------|-------|--------|--------|
| Valid pair | T001T, T001I (depends_on: [T001T]) | PASS | All rules satisfied |
| Missing test | T001I (no T001T exists) | FAIL | Pair completeness violated |
| Wrong order | T001I, T001T | FAIL | Order correctness violated |
| Missing dependency | T001T, T001I (depends_on: []) | FAIL | Dependency link violated |
| Valid standalone | T501 (documentation task) | PASS | T5XX range, no pairing required |


---

## Output Quality Gate (Phase 5)

**Purpose**: Validate generated outputs before delivery.

| Check | Rule | Severity |
|-------|------|----------|
| File Created | tasks.md exists at output path | BLOCKING |
| JSON Valid | TASKS.json parses without errors | BLOCKING |
| Schema Valid | TASKS.json matches task-creator.schema.json | BLOCKING |

### Output File Requirements

**tasks.md**:
- [ ] All tasks listed with T-ID, operation type, description
- [ ] Review checkpoints every 5-8 tasks
- [ ] Parallel groups marked with [P] flags
- [ ] Agent assignments included for each task

**TASKS.json**:
- [ ] tasks_generated array populated
- [ ] review_groups structured with component metadata
- [ ] dependency_graph includes all dependencies
- [ ] parallel_execution_groups identified
- [ ] Validates against task-creator.schema.json


---

## Validation Summary

| Gate | BLOCKING Checks | Status |
|------|-----------------|--------|
| Pre-Generation | 3 | Must all pass |
| Task Quality | 5 | Must all pass |
| TDD | 3 | Must all pass |
| Output Quality | 3 | Must all pass |

**TOTAL**: 14 BLOCKING checks, 1 WARNING check

**PASS CRITERIA**: All BLOCKING checks pass

---

## Quick Reference: Validation Execution Order

```
Phase 1: Pre-Generation Gate
  └─ Input validation (3 BLOCKING)
  
Phase 4: Task Quality Gate  
  └─ Per-task validation (5 BLOCKING)
  └─ Phase 4.3: TDD validation (3 BLOCKING)
  
Phase 5: Output Quality Gate
  └─ Output validation (3 BLOCKING)
```

**On BLOCKING Failure**: STOP, report error, do not proceed to next phase.

**On WARNING**: Log issue, continue processing, include in final report.

