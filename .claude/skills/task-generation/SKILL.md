---
name: task-generation
description: >
  Use this skill when generating tasks from synthesized context. Applies TDD 
  pairing, assigns agents via 2-tier matrix, identifies parallel opportunities.
  Requires context from task-context-synthesis. Trigger keywords: generate 
  tasks, TDD pairing, agent assignment, parallel identification.
---

# Task Generation

*Thin orchestration layer for Steps 4-5 of /tasks workflow: generate tasks and collect results.*

**Key Design**: This skill orchestrates task generation by referencing `generating-tasks` for ALL algorithms. It does NOT duplicate algorithm logic.

---

## Contents

1. [Task Generation Protocol](#task-generation-protocol)
2. [Algorithm Reference Table](#algorithm-reference-table)
3. [Review Checkpoint Placement](#review-checkpoint-placement)
4. [Parallel Group Formation](#parallel-group-formation)
5. [Output Contract](#output-contract)
6. [Anti-Patterns](#anti-patterns)
7. [Quick Reference](#quick-reference)

---

## Task Generation Protocol

### Prerequisites

- **Required Input**: Synthesized context from `task-context-synthesis` skill
- **Required Data**: PLAN.md parsed sections, file discovery results, dependency map

### Step 4: Generate Tasks

Execute task generation by applying algorithms from `generating-tasks`:

```
FOR each implementation_item in synthesized_context.plan_sections:

  1. APPLY T-ID Numbering Convention
     -> See: generating-tasks#t-id-numbering-convention
     
  2. APPLY TDD Pairing Algorithm (if packages/** or scripts/**)
     -> See: generating-tasks#tdd-pairing-algorithm
     
  3. APPLY 2-Tier Agent Assignment Matrix
     -> See: generating-tasks#2-tier-agent-assignment-matrix
     
  4. APPLY Dependency Detection
     -> See: generating-tasks#dependency-detection
     
  5. APPLY Parallel Eligibility Rules
     -> See: generating-tasks#parallel-eligibility-rules
     
  6. CALCULATE effort via Effort Estimation Model
     -> See: generating-tasks/references/effort-estimation.md

  7. VALIDATE via Validation Gates
     -> See: generating-tasks#validation-gates
```

### Step 5: Collect Results


Aggregate generated tasks into output structure:

```
1. GROUP tasks into parallel batches
   - Tasks with no dependencies -> Batch 1
   - Tasks depending on Batch 1 -> Batch 2
   - Continue until all tasks assigned

2. INSERT review checkpoints (see Review Checkpoint Placement)

3. CALCULATE quality score
   -> See: generating-tasks#quality-score-formula
   
4. FORMAT output per Output Contract
```

---

## Algorithm Reference Table

**CRITICAL**: This skill does NOT implement these algorithms. It references `generating-tasks` for ALL algorithm logic.

| Algorithm | Reference | When Applied |
|-----------|-----------|--------------|
| T-ID Numbering | [generating-tasks#t-id-numbering-convention](../generating-tasks/SKILL.md#t-id-numbering-convention) | Every task creation |
| TDD Pairing | [generating-tasks#tdd-pairing-algorithm](../generating-tasks/SKILL.md#tdd-pairing-algorithm) | Tasks targeting packages/** or scripts/** |
| Agent Assignment | [generating-tasks#2-tier-agent-assignment-matrix](../generating-tasks/SKILL.md#2-tier-agent-assignment-matrix) | Every task |
| Dependency Detection | [generating-tasks#dependency-detection](../generating-tasks/SKILL.md#dependency-detection) | After task creation |
| Parallel Eligibility | [generating-tasks#parallel-eligibility-rules](../generating-tasks/SKILL.md#parallel-eligibility-rules) | Batch grouping |
| Effort Estimation | [generating-tasks/references/effort-estimation.md](../generating-tasks/references/effort-estimation.md) | Final calculation |
| Quality Score | [generating-tasks#quality-score-formula](../generating-tasks/SKILL.md#quality-score-formula) | Validation |
| Validation Gates | [generating-tasks#validation-gates](../generating-tasks/SKILL.md#validation-gates) | Before output |

---

## Review Checkpoint Placement

Insert review checkpoints strategically based on task complexity and risk.

### Checkpoint Triggers

| Trigger | Checkpoint Type | Placement |
|---------|-----------------|-----------|
| 3-5 tasks completed | Standard Review | After batch |
| High-complexity task (score >= 4) | Focused Review | Immediately after |
| Cross-module changes | Integration Review | After related batch |
| TDD pair completion | TDD Verification | After T###I task |

### Checkpoint Structure

```markdown
### Review Checkpoint {N}
Components: {component_list} | Complexity: {low/moderate/high} | Coverage: {unit/integration/e2e}
```

### Review Group Formation

```
1. IDENTIFY completed tasks since last checkpoint
2. GROUP by component/module
3. ASSESS complexity (avg of task complexity scores)
4. DETERMINE coverage type needed
5. FORMAT checkpoint entry
```

---

## Parallel Group Formation

Form parallel batches to maximize execution efficiency while respecting dependencies.

### Batch Formation Algorithm

```
parallel_batches = []
remaining_tasks = all_tasks.copy()
batch_number = 1

WHILE remaining_tasks is not empty:
  eligible = []
  
  FOR task in remaining_tasks:
    IF all task.depends_on are in completed_tasks:
      IF task passes Parallel Eligibility Rules:
        eligible.append(task)
  
  IF len(eligible) > 5:
    eligible = prioritize_by_critical_path(eligible)[:5]
  
  parallel_batches.append({
    "batch": batch_number,
    "tasks": eligible,
    "parallel": len(eligible) > 1
  })
  
  completed_tasks.extend(eligible)
  remaining_tasks.remove(eligible)
  batch_number += 1

RETURN parallel_batches
```

### Batch Naming Convention

| Batch Type | Name Format | Example |
|------------|-------------|---------|
| Parallel (2+ tasks) | `Batch {N} (Parallel)` | `Batch 1 (Parallel)` |
| Sequential (1 task) | `Batch {N} (Sequential)` | `Batch 2 (Sequential)` |
| Review | `Review Checkpoint {N}` | `Review Checkpoint 1` |

---

## Output Contract

### Success Response

```json
{
  "status": "SUCCESS",
  "tasks": [
    {
      "id": "T001T",
      "operation": "C",
      "parallel": true,
      "action": "Write tests for AuthService",
      "file_path": "tests/unit/test_auth.py",
      "agent": "code-quality",
      "agent_confidence": 0.95,
      "depends_on": [],
      "acceptance_criteria": "All test cases pass",
      "batch": 1
    }
  ],
  "parallel_batches": [
    {
      "batch": 1,
      "tasks": ["T001T", "T002T"],
      "parallel": true,
      "estimated_time": "10-15 min"
    }
  ],
  "review_groups": [
    {
      "checkpoint": 1,
      "components": ["auth", "models"],
      "complexity": "moderate",
      "coverage": "unit"
    }
  ],
  "effort": {
    "total_tasks": 15,
    "parallel_batches": 4,
    "critical_path_tasks": 6,
    "estimated_wall_clock": "25-35 min",
    "confidence": 0.80,
    "breakdown": {
      "execution": "15-20 min",
      "reviews": "10-15 min",
      "orchestration": "5 min"
    }
  },
  "quality_score": 0.87,
  "metadata": {
    "feature": "feature-name",
    "generated_at": "2025-12-17T10:30:00Z",
    "plan_source": "path/to/PLAN.md",
    "algorithms_applied": [
      "t-id-numbering",
      "tdd-pairing",
      "agent-assignment",
      "dependency-detection",
      "parallel-eligibility",
      "effort-estimation"
    ]
  }
}
```

### Failure Response

```json
{
  "status": "FAILURE",
  "error": {
    "code": "VALIDATION_GATE_FAILED",
    "gate": "tdd_compliance",
    "message": "T003I missing corresponding T003T test task",
    "suggestion": "Add T003T before T003I"
  },
  "partial_tasks": [],
  "quality_score": 0.62
}
```

---

## Anti-Patterns

### NEVER DO

| Anti-Pattern | Why It's Wrong | Correct Approach |
|--------------|----------------|------------------|
| Duplicate algorithm logic | Maintenance burden, drift risk | Reference `generating-tasks` |
| Skip TDD pairing for packages/** | Violates project standards | Always apply TDD Pairing Algorithm |
| Assign agents by keyword only | Low confidence, wrong assignments | Use 2-Tier Agent Assignment Matrix |
| Ignore dependency detection | Parallel failures, race conditions | Always apply Dependency Detection |
| Output without validation | Quality score unknown | Run all Validation Gates |
| Manual parallel grouping | Error-prone, inconsistent | Use Batch Formation Algorithm |

### Algorithm Duplication Check

Before adding ANY algorithm logic to this skill, verify:

```
1. Does generating-tasks already have this algorithm?
   -> YES: Reference it, DO NOT duplicate
   -> NO: Consider adding to generating-tasks first

2. Is this orchestration-only logic?
   -> YES: Can add here (e.g., checkpoint placement)
   -> NO: Add to generating-tasks
```

---

## Quick Reference

```
TASK GENERATION PROTOCOL:
  Step 4: Generate Tasks
    1. Apply T-ID Numbering        -> generating-tasks#t-id-numbering-convention
    2. Apply TDD Pairing           -> generating-tasks#tdd-pairing-algorithm
    3. Apply Agent Assignment      -> generating-tasks#2-tier-agent-assignment-matrix
    4. Apply Dependency Detection  -> generating-tasks#dependency-detection
    5. Apply Parallel Eligibility  -> generating-tasks#parallel-eligibility-rules
    6. Calculate Effort            -> generating-tasks/references/effort-estimation.md
    7. Validate                    -> generating-tasks#validation-gates
  
  Step 5: Collect Results
    1. Group into parallel batches (max 5 per batch)
    2. Insert review checkpoints
    3. Calculate quality score     -> generating-tasks#quality-score-formula
    4. Format output per contract

REVIEW CHECKPOINTS:
  - Every 3-5 tasks
  - After high-complexity tasks (score >= 4)
  - After cross-module changes
  - After TDD pair completion

PARALLEL BATCH RULES:
  - Max 5 tasks per batch
  - All dependencies must be satisfied
  - Apply Parallel Eligibility Rules from generating-tasks

OUTPUT:
  SUCCESS: tasks[], parallel_batches[], review_groups[], effort{}, quality_score
  FAILURE: error{}, partial_tasks[], quality_score

ALGORITHM REFERENCE (DO NOT DUPLICATE):
  All algorithms live in generating-tasks SKILL.md
  This skill ONLY orchestrates their application
```

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| `generating-tasks` | **Source of all algorithms** - reference, never duplicate |
| `task-context-synthesis` | Upstream - provides synthesized context input |
| `validating-specifications` | Upstream - validates PLAN.md quality |

---

## Cross-References

- **Algorithm Source**: [generating-tasks/SKILL.md](../generating-tasks/SKILL.md)
- **Effort Model**: [generating-tasks/references/effort-estimation.md](../generating-tasks/references/effort-estimation.md)
- **/tasks Command**: [../../commands/tasks.md](../../commands/tasks.md)
