---
name: task-validation
description: >
  Use this skill when validating generated task quality. Runs 4 validation 
  gates, calculates quality score, identifies TDD violations. Requires tasks
  from task-generation. Trigger keywords: validate tasks, task quality, 
  validation gates, quality score, TDD compliance check.
---

# Task Validation

*Validate generated tasks through 4 sequential gates, calculate quality score, identify violations*

## Contents

- [Validation Protocol](#validation-protocol)
- [Gate 1: Task Anatomy](#gate-1-task-anatomy)
- [Gate 2: TDD Compliance](#gate-2-tdd-compliance)
- [Gate 3: Dependency Acyclicity](#gate-3-dependency-acyclicity)
- [Gate 4: Agent Coverage](#gate-4-agent-coverage)
- [Quality Score Calculation](#quality-score-calculation)
- [Pass/Warn/Fail Decision Logic](#passwarnfail-decision-logic)
- [Anti-Patterns](#anti-patterns)
- [Quick Reference](#quick-reference)

---


## Validation Protocol

**All 4 gates execute in sequence. Failure at any gate is BLOCKING.**

```
INPUT: tasks[] from task-generation
       (tasks.md or TASKS.json)

PROCESS:
  1. Gate 1: Task Anatomy      -> Validate each task has 4 components
  2. Gate 2: TDD Compliance    -> Verify T###T/T###I pairing rules
  3. Gate 3: Dependency Graph  -> Check for cycles
  4. Gate 4: Agent Coverage    -> Confirm agent assignments

  IF any gate FAILS:
    STOP and return FAIL with violations
  
  Calculate quality_score from all dimensions
  Return status based on thresholds

OUTPUT: ValidationResult (see Output Contract below)
```

**Output Contract**:
```json
{
  "status": "PASS|WARN|FAIL",
  "quality_score": 0.87,
  "gate_results": {
    "gate_1_anatomy": { "passed": true, "violations": [] },
    "gate_2_tdd": { "passed": true, "violations": [] },
    "gate_3_acyclicity": { "passed": true, "cycles": [] },
    "gate_4_agent_coverage": { "passed": true, "unassigned": [] }
  },
  "recommendations": [...]
}
```

---


## Gate 1: Task Anatomy

**Purpose**: Ensure every task contains all 4 required components.

**Reference**: See [generating-tasks SKILL.md](../generating-tasks/SKILL.md#validation-gates) for Task Anatomy Formula.

### Required Components

| Component | Description | Detection Pattern |
|-----------|-------------|-------------------|
| ACTION_VERB | What operation | Create, Modify, Delete, Add, Update, Remove, Implement, Fix, Write |
| SCOPE | What component/module | Noun phrase after action verb |
| FILE_PATH | Target location | Path pattern (`packages/`, `tests/`, `docs/`, etc.) |
| ACCEPTANCE_CRITERIA | Testable condition | Text after semicolon or "when" clause |

### Validation Logic

```
FOR each task in tasks[]:
  violations = []
  
  IF NOT contains_action_verb(task.action):
    violations.push({ field: "ACTION_VERB", message: "Missing action verb" })
  
  IF NOT extract_scope(task.action):
    violations.push({ field: "SCOPE", message: "Missing scope/component" })
  
  IF NOT task.file_path OR NOT is_valid_path(task.file_path):
    violations.push({ field: "FILE_PATH", message: "Missing or invalid file path" })
  
  IF NOT task.acceptance_criteria:
    violations.push({ field: "ACCEPTANCE_CRITERIA", message: "Missing acceptance criteria" })
  
  IF violations.length > 0:
    gate_1_violations.push({ task_id: task.id, violations })
```

### Gate 1 Result

```json
{
  "passed": false,
  "violations": [
    {
      "task_id": "T003I",
      "violations": [
        { "field": "ACCEPTANCE_CRITERIA", "message": "Missing acceptance criteria" }
      ]
    }
  ]
}
```

---


## Gate 2: TDD Compliance

**Purpose**: Verify all implementation tasks have proper test task pairings.

**Reference**: See [generating-tasks SKILL.md](../generating-tasks/SKILL.md#tdd-pairing-algorithm) for TDD Pairing Rules.

### TDD Pairing Rules

| Rule | Validation Check |
|------|------------------|
| Pair Requirement | Every T###I MUST have corresponding T###T |
| Order Enforcement | T###T.order MUST be < T###I.order |
| Dependency Link | T###I.depends_on MUST include T###T |
| Scope Match | Test file mirrors implementation file |

### Validation Logic

```
FOR each task WHERE task.id ends with "I":
  base_id = task.id.slice(0, -1)  # Remove "I" suffix
  test_task_id = base_id + "T"
  
  # Rule 1: Pair exists
  test_task = find_task(test_task_id)
  IF NOT test_task:
    violations.push({
      task_id: task.id,
      rule: "PAIR_REQUIREMENT",
      message: f"Missing test task {test_task_id} for implementation {task.id}"
    })
    CONTINUE
  
  # Rule 2: Order correct
  IF test_task.order >= task.order:
    violations.push({
      task_id: task.id,
      rule: "ORDER_ENFORCEMENT",
      message: f"{test_task_id} (order={test_task.order}) must precede {task.id} (order={task.order})"
    })
  
  # Rule 3: Dependency link
  IF test_task_id NOT IN task.depends_on:
    violations.push({
      task_id: task.id,
      rule: "DEPENDENCY_LINK",
      message: f"{task.id} must depend on {test_task_id}"
    })
```

### TDD Exemptions

Tasks in these ranges are EXEMPT from TDD pairing:
- T5XX-T7XX: Standalone tasks (documentation, config)
- T8XX: Investigation tasks
- T9XX: Cleanup/debt tasks

---


## Gate 3: Dependency Acyclicity

**Purpose**: Ensure no circular dependencies exist in the task graph.

**Reference**: See [generating-tasks SKILL.md](../generating-tasks/SKILL.md#dependency-detection) for Dependency Types.

### Cycle Detection Algorithm

```
FUNCTION detect_cycles(tasks[]):
  graph = build_adjacency_list(tasks)
  visited = {}
  rec_stack = {}
  cycles = []
  
  FOR each task in tasks:
    IF NOT visited[task.id]:
      cycle = dfs_cycle_detect(task.id, graph, visited, rec_stack, [])
      IF cycle:
        cycles.push(cycle)
  
  RETURN cycles

FUNCTION dfs_cycle_detect(node, graph, visited, rec_stack, path):
  visited[node] = true
  rec_stack[node] = true
  path.push(node)
  
  FOR each neighbor in graph[node]:
    IF NOT visited[neighbor]:
      result = dfs_cycle_detect(neighbor, graph, visited, rec_stack, path)
      IF result: RETURN result
    ELSE IF rec_stack[neighbor]:
      # Cycle found - extract cycle path
      cycle_start = path.indexOf(neighbor)
      RETURN path.slice(cycle_start).concat([neighbor])
  
  rec_stack[node] = false
  path.pop()
  RETURN null
```

### Gate 3 Result

```json
{
  "passed": false,
  "cycles": [
    {
      "path": ["T001I", "T002I", "T003I", "T001I"],
      "suggested_break": "T002I -> T003I",
      "reason": "T003I can be made independent"
    }
  ]
}
```

---


## Gate 4: Agent Coverage

**Purpose**: Verify all tasks have valid agent assignments.

**Reference**: See [generating-tasks SKILL.md](../generating-tasks/SKILL.md#2-tier-agent-assignment-matrix) for Agent Assignment Matrix.

### Valid Agent List

```
valid_agents = [
  "development",
  "code-quality", 
  "documentation",
  "workflow",
  "claude-code-ecosystem",
  "deployment-release",
  "debugger"
]
```

### Validation Logic

```
FOR each task in tasks[]:
  IF task.agent NOT IN valid_agents:
    IF task.agent_confidence >= 0.50:
      # Invalid agent with high confidence = error
      unassigned.push({
        task_id: task.id,
        current_agent: task.agent,
        confidence: task.agent_confidence,
        file_path: task.file_path,
        suggested_agent: suggest_agent(task.file_path)
      })
    ELSE:
      # Low confidence = manual review flagged (acceptable)
      warnings.push({
        task_id: task.id,
        message: "Flagged for manual agent review"
      })
```

### Gate 4 Result

```json
{
  "passed": false,
  "unassigned": [
    {
      "task_id": "T004I",
      "current_agent": "unknown-agent",
      "confidence": 0.80,
      "file_path": "packages/auth/service.py",
      "suggested_agent": "development"
    }
  ]
}
```

---


## Quality Score Calculation

**Reference**: See [generating-tasks SKILL.md](../generating-tasks/SKILL.md#quality-score-formula) for full formula and dimension scoring.

### Formula

```
quality_score = (
  specificity_score    x 0.30 +   # All 4 anatomy components present
  agent_match_score    x 0.30 +   # Tier 1/2 match with confidence
  tdd_compliance_score x 0.20 +   # All T###I have T###T pairs
  parallel_optimization x 0.20    # % of tasks marked [P] correctly
)
```

### Dimension Calculation

| Dimension | Calculation |
|-----------|-------------|
| Specificity | `1.0 - (0.25 * missing_components_per_task_avg)` |
| Agent Match | `sum(task.agent_confidence) / total_tasks` |
| TDD Compliance | `valid_tdd_pairs / total_impl_tasks` |
| Parallel Opt | `correctly_flagged_parallel / eligible_for_parallel` |

### Calculation Example

```
Tasks: 10 total, 4 implementation tasks (T###I)

Specificity:     All tasks have 4 components       -> 1.00
Agent Match:     Avg confidence = 0.88             -> 0.88
TDD Compliance:  4/4 valid pairs                   -> 1.00
Parallel Opt:    5/6 correctly flagged             -> 0.83

quality_score = (1.00 * 0.30) + (0.88 * 0.30) + (1.00 * 0.20) + (0.83 * 0.20)
              = 0.30 + 0.264 + 0.20 + 0.166
              = 0.93 -> PASS
```

---


## Pass/Warn/Fail Decision Logic

### Thresholds

| Score | Status | Action |
|-------|--------|--------|
| >= 0.85 | **PASS** | Output ready for `/implement` |
| 0.70 - 0.84 | **WARN** | Output with warnings, suggest review |
| < 0.70 | **FAIL** | Regenerate with feedback |

### Decision Algorithm

```
FUNCTION determine_status(gate_results, quality_score):
  # Gate failures are BLOCKING regardless of score
  IF any gate_result.passed == false:
    RETURN {
      status: "FAIL",
      reason: "Gate failure",
      blocking_gates: [gates where passed == false]
    }
  
  # Score-based decision
  IF quality_score >= 0.85:
    RETURN { status: "PASS", reason: "All gates passed, high quality" }
  
  ELSE IF quality_score >= 0.70:
    RETURN {
      status: "WARN",
      reason: "All gates passed, quality below optimal",
      recommendations: generate_improvement_suggestions(gate_results)
    }
  
  ELSE:
    RETURN {
      status: "FAIL",
      reason: "Quality score below threshold",
      recommendations: generate_improvement_suggestions(gate_results)
    }
```

### Recommendation Generation

```
FUNCTION generate_improvement_suggestions(gate_results, scores):
  recommendations = []
  
  IF scores.specificity < 0.85:
    recommendations.push("Add missing acceptance criteria to tasks")
  
  IF scores.agent_match < 0.85:
    recommendations.push("Review agent assignments for low-confidence tasks")
  
  IF scores.tdd_compliance < 1.0:
    recommendations.push("Ensure all T###I tasks have matching T###T")
  
  IF scores.parallel_optimization < 0.80:
    recommendations.push("Review parallel flags - some tasks may be parallelizable")
  
  RETURN recommendations
```

---


## Anti-Patterns

**NEVER DO**:

| Anti-Pattern | Why It's Wrong | Correct Approach |
|--------------|----------------|------------------|
| Skip gates on "simple" tasks | All tasks need validation | Run all 4 gates always |
| Ignore low-confidence agents | Creates assignment debt | Flag for manual review |
| Auto-fix TDD violations | May break intentional design | Report and recommend |
| Accept cycles "temporarily" | Cycles block execution | Resolve before proceeding |
| Validate partial task lists | Incomplete data = wrong scores | Require complete task set |
| Override FAIL with WARN | Masks quality issues | Respect thresholds |
| Skip validation for T5XX-T9XX | Still need anatomy/agent checks | Validate all ranges |

---

## Quick Reference

```
VALIDATION GATES (sequential, all BLOCKING):
  Gate 1: Task Anatomy    -> 4 components per task
  Gate 2: TDD Compliance  -> T###T before T###I
  Gate 3: Acyclicity      -> No circular dependencies
  Gate 4: Agent Coverage  -> Valid agent assignments

QUALITY SCORE:
  Specificity(0.30) + AgentMatch(0.30) + TDD(0.20) + Parallel(0.20)

THRESHOLDS:
  >= 0.85 = PASS (ready for /implement)
  0.70-0.84 = WARN (review recommended)
  < 0.70 = FAIL (regenerate)

TDD EXEMPTIONS:
  T5XX-T7XX = Standalone (no pairing needed)
  T8XX = Investigation (no pairing needed)
  T9XX = Cleanup (no pairing needed)

OUTPUT CONTRACT:
  {
    status: PASS|WARN|FAIL,
    quality_score: 0.XX,
    gate_results: { gate_1..4 },
    recommendations: [...]
  }

CROSS-REFERENCES:
  -> generating-tasks SKILL.md (gate definitions, quality formula)
  -> agent-selection-guide.md (valid agent list)
```

---

## Related Skills

- [generating-tasks](../generating-tasks/SKILL.md) - Task generation (provides input)
- [implementing-tasks](../implementing-tasks/SKILL.md) - Task execution (consumes validated output)

