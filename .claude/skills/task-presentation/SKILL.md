---
name: task-presentation
description: >
  Use this skill when formatting and presenting task generation results.
  Creates tasks.md and TASKS.json outputs, generates summary reports.
  Trigger keywords: present tasks, task output, tasks.md, TASKS.json, 
  task summary.
---

# Task Presentation Skill

**Domain**: Planning  
**Responsibility**: Format and present task generation results (Step 7 of /tasks workflow)  
**Triggers**:
  - Task list ready for output
  - Generate tasks.md file
  - Generate TASKS.json file
  - Create task summary report
  - Prepare for /implement handoff

---

## Overview

Owns the methodology and operations for:
- Formatting tasks.md human-readable output
- Generating TASKS.json machine-readable output
- Creating summary reports with metrics
- Providing execution instructions for /implement workflow

**Does NOT own**:
- Task generation logic (see `generating-tasks` skill)
- TDD pairing algorithm (see `generating-tasks` skill)
- Agent assignment (see `generating-tasks` skill)
- Task execution (see /implement command)

---

## Output Contract

```json
{
  "status": "SUCCESS|FAILURE",
  "output_files": {
    "tasks_md": "/path/to/tasks.md",
    "tasks_json": "/path/to/TASKS.json"
  },
  "summary": {
    "total_tasks": 15,
    "test_tasks": 6,
    "impl_tasks": 6,
    "standalone_tasks": 3,
    "parallel_batches": 4,
    "review_checkpoints": 2,
    "estimated_effort": "25-35 min"
  }
}
```

---

## Output Format Specification

### tasks.md Structure

> **Reference**: Full schema defined in [generating-tasks SKILL.md](../generating-tasks/SKILL.md#output-format)

```markdown
# Tasks: [Feature Name]

## Summary
- **Total Tasks**: X
- **Test Tasks**: Y (T###T)
- **Implementation Tasks**: Z (T###I)
- **Standalone Tasks**: W (T5XX-T9XX)
- **Parallel Batches**: N
- **Review Checkpoints**: M
- **Estimated Time**: A-B min

## Task List

### Batch 1 (Parallel)
- T001T [C] [P] Write tests for AuthService in tests/unit/test_auth.py
- T002T [C] [P] Write tests for UserModel in tests/unit/test_user.py

### Batch 2 (Sequential - depends on Batch 1)
- T001I [C] Implement AuthService in packages/auth/service.py
- T002I [C] Implement UserModel in packages/models/user.py

### Review Checkpoint 1
Components: auth, models | Complexity: moderate | Coverage: unit

## Execution Instructions
[See Execution Instructions section below]
```

### Batch Organization Rules

| Batch Type | Criteria | Marker |
|------------|----------|--------|
| Parallel | All tasks have [P] flag, no inter-dependencies | `### Batch N (Parallel)` |
| Sequential | Tasks depend on previous batch | `### Batch N (Sequential - depends on Batch M)` |
| Review Checkpoint | After complex batch or milestone | `### Review Checkpoint N` |

**Batch Sizing**:
- Max 5 tasks per parallel batch
- Review checkpoint every 3-5 batches or after complex component
- Group related TDD pairs (T###T, T###I) in consecutive batches

---

## TASKS.json Schema

> **Reference**: Full schema defined in [generating-tasks SKILL.md](../generating-tasks/SKILL.md#output-format)

```json
{
  "metadata": {
    "feature": "feature-name",
    "generated_at": "ISO-8601",
    "plan_source": "path/to/PLAN.md",
    "quality_score": 0.85,
    "skill_version": "1.0.0"
  },
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
  "batches": [
    {
      "id": 1,
      "type": "parallel",
      "tasks": ["T001T", "T002T"],
      "depends_on": []
    },
    {
      "id": 2,
      "type": "sequential",
      "tasks": ["T001I", "T002I"],
      "depends_on": [1]
    }
  ],
  "effort": {
    "total_tasks": 15,
    "test_tasks": 6,
    "impl_tasks": 6,
    "standalone_tasks": 3,
    "parallel_batches": 4,
    "review_checkpoints": 2,
    "estimated_wall_clock": "25-35 min"
  }
}
```

---

## Summary Report Generation

### Summary Calculation Algorithm

```
FOR task_list:
  total_tasks = len(tasks)
  test_tasks = count(tasks WHERE id ENDS_WITH "T")
  impl_tasks = count(tasks WHERE id ENDS_WITH "I")
  standalone_tasks = total_tasks - test_tasks - impl_tasks
  
  parallel_batches = count(batches WHERE type = "parallel")
  review_checkpoints = count(batches WHERE type = "review")
  
  # Effort from generating-tasks skill
  estimated_effort = calculate_wall_clock(tasks, batches)
```

### Summary Template

```markdown
## Task Generation Summary

| Metric | Value |
|--------|-------|
| Total Tasks | {total_tasks} |
| Test Tasks (T###T) | {test_tasks} |
| Implementation Tasks (T###I) | {impl_tasks} |
| Standalone Tasks | {standalone_tasks} |
| Parallel Batches | {parallel_batches} |
| Review Checkpoints | {review_checkpoints} |
| Estimated Effort | {estimated_effort} |
| Quality Score | {quality_score} |

### TDD Compliance
- Paired: {paired_count} (T###T + T###I pairs)
- Unpaired: {unpaired_count} (standalone implementation)
- Compliance Rate: {compliance_rate}%

### Agent Distribution
| Agent | Task Count | Confidence |
|-------|------------|------------|
| {agent_name} | {count} | {avg_confidence} |
```

---

## Execution Instructions

### How to Use Output with /implement

Include these instructions in every tasks.md output:

```markdown
## Execution Instructions

### Option 1: Full Execution
```
/implement --tasks tasks.md --mode sequential
```
Executes all batches in order with review checkpoints.

### Option 2: Batch-by-Batch
```
/implement --tasks tasks.md --batch 1
```
Executes single batch, pauses for review.

### Option 3: Single Task
```
/implement --task T001T
```
Executes individual task by ID.

### Review Checkpoint Protocol
At each review checkpoint:
1. Verify tests pass: `uv run pytest tests/unit/`
2. Check coverage: `uv run pytest --cov=packages`
3. Lint check: `uv run ruff check .`
4. Approve to continue or halt for fixes
```

### Handoff Checklist

Before presenting output to user, verify:

- [ ] tasks.md file written to expected location
- [ ] TASKS.json file written to expected location
- [ ] Quality score >= 0.85 (or WARN if 0.70-0.84)
- [ ] All TDD pairs validated (T###T precedes T###I)
- [ ] Execution instructions included
- [ ] Estimated effort range provided

---

## Anti-Patterns (NEVER DO)

| Anti-Pattern | Why It's Wrong | Correct Approach |
|--------------|----------------|------------------|
| Duplicate schema definitions | Creates drift with generating-tasks | Reference generating-tasks skill |
| Output without quality score | User cannot assess reliability | Always include quality_score |
| Missing batch organization | /implement cannot parallelize | Group tasks into batches |
| No execution instructions | User unsure how to proceed | Include /implement usage |
| Single-number estimates | Hides uncertainty | Use ranges (e.g., "25-35 min") |
| tasks.md without TASKS.json | Loses machine-readability | Always output both files |
| Skipping review checkpoints | No validation gates | Insert checkpoints every 3-5 batches |
| Presenting failed validation | Low-quality output | Regenerate if quality_score < 0.70 |

---

## Output File Locations

### Default Locations

```
{project_root}/
├── docs/01-planning/
│   └── {feature}/
│       ├── PLAN.md          # Input (from plan-generation)
│       ├── tasks.md         # Output (human-readable)
│       └── TASKS.json       # Output (machine-readable)
```

### Path Resolution

```
IF feature_name provided:
  output_dir = docs/01-planning/{feature_name}/
ELSE IF PLAN.md path provided:
  output_dir = dirname(PLAN.md)
ELSE:
  output_dir = docs/01-planning/
```

---

## Quick Reference

```
Output Contract:
  status: SUCCESS | FAILURE
  output_files: { tasks_md, tasks_json }
  summary: { total, test, impl, standalone, batches, checkpoints, effort }

tasks.md Structure:
  # Tasks: [Feature Name]
  ## Summary (metrics table)
  ## Task List (batched)
  ## Execution Instructions

TASKS.json Structure:
  metadata: { feature, generated_at, plan_source, quality_score }
  tasks: [ { id, operation, parallel, action, file_path, agent, ... } ]
  batches: [ { id, type, tasks, depends_on } ]
  effort: { total_tasks, parallel_batches, estimated_wall_clock }

Quality Gates (from generating-tasks):
  >= 0.85 = PASS (output ready)
  0.70-0.84 = WARN (output with warnings)
  < 0.70 = FAIL (regenerate)

Handoff to /implement:
  /implement --tasks tasks.md --mode sequential  # Full execution
  /implement --tasks tasks.md --batch 1          # Single batch
  /implement --task T001T                        # Single task
```

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [generating-tasks](../generating-tasks/SKILL.md) | Source of task data and schemas |
| [effort-estimation](../generating-tasks/references/effort-estimation.md) | Effort calculation model |
| [plan-validation](../plan-validation/SKILL.md) | Validates PLAN.md before task generation |

---

## Thinking Frameworks

**Full Catalog**: [Thinking Frameworks README](../../docs/00-core/frameworks/README.md)

**Most Relevant for Task Presentation**:

| Framework | When to Use |
|-----------|-------------|
| [Pre-Mortem](../../docs/00-core/frameworks/strategy.md) | Validate output before delivery |
| [SCAMPER](../../docs/00-core/frameworks/creative.md) | Optimize batch organization |

> **Selection Tip**: output validation -> Pre-Mortem, optimization -> SCAMPER
