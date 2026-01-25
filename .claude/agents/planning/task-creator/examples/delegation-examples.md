# Task Creator Delegation Examples

How the orchestrator invokes task-creator with proper context.

---

## Example 1: Single Component Task Generation

**Orchestrator delegation**:
```
Task(task-creator,
  "Generate tasks from docs/01-planning/specifications/015-deepeval/plans/agent-evaluation-PLAN.md
   with spec at docs/01-planning/specifications/015-deepeval/SPEC.md.
   Component: agent-evaluation, Sprint points: 8")
```

**Expected output**:
- `docs/01-planning/specifications/015-deepeval/tasks/agent-evaluation/tasks.md`
- `docs/01-planning/specifications/015-deepeval/tasks/agent-evaluation/TASKS.json`

---

## Example 2: Multi-Component Parallel Invocation

**Orchestrator launches 3 instances in parallel**:
```
# Instance 1
Task(task-creator, "Generate tasks from .../plans/component-a-PLAN.md ...")

# Instance 2
Task(task-creator, "Generate tasks from .../plans/component-b-PLAN.md ...")

# Instance 3
Task(task-creator, "Generate tasks from .../plans/component-c-PLAN.md ...")
```

**Directory isolation ensures no conflicts**:
```
tasks/
├── component-a/    # Instance 1 writes here
├── component-b/    # Instance 2 writes here
└── component-c/    # Instance 3 writes here
```

---

## Example 3: With Task ID Offset

**When continuing from previous task generation**:
```
Task(task-creator,
  "Generate tasks from .../plans/phase-2-PLAN.md
   with task_id_offset=50 to continue numbering from T050")
```


---

## Example 4: Full Context Delegation

**Complete orchestrator context**:
```json
{
  "task_id": "orch-2024-001",
  "execution_timestamp": "2024-01-15T10:30:00Z",
  "plan_file_path": "docs/01-planning/specifications/015-deepeval/plans/metrics-PLAN.md",
  "spec_file_path": "docs/01-planning/specifications/015-deepeval/SPEC.md",
  "task_id_offset": 0,
  "component_context": {
    "component_name": "metrics-engine",
    "sprint_points": 5,
    "requirements_covered": ["FR-001", "FR-002", "FR-003"]
  }
}
```

---

## Output Structure

**tasks.md format**:
```markdown
# Tasks: metrics-engine

## Cleanup Tasks (T9XX)
- T901 [python-code-implementer] Remove deprecated imports in packages/metrics/old.py [C]

## Investigation Tasks (T8XX)
- T801 [tech-debt-investigator] Analyze metrics calculation patterns [I]

## Implementation Tasks
- T001 [test-creator] Create unit tests for MetricsEngine in tests/unit/test_metrics.py [P]
- T002 [test-creator] Create unit tests for MetricsCollector in tests/unit/test_collector.py [P]
- T003 [python-code-implementer] Implement MetricsEngine in packages/metrics/engine.py
- T004 [python-code-implementer] Implement MetricsCollector in packages/metrics/collector.py
- T005 [test-executor] Run and validate all metrics tests
- T006 [REVIEW] Review checkpoint for T001-T005

## Review Groups
- RG001: T001-T005 -> T006 (blocks T007+)
```

---

## Key Points

1. **One plan per invocation** - task-creator processes single PLAN.md
2. **Orchestrator aggregates** - Multiple instances, orchestrator combines results
3. **Component isolation** - Each instance writes to separate directory
4. **No cross-talk** - Instances do not communicate with each other
