---
argument-hint: '[plan-json-path] [--phase=1-N]'
description: 'Generate machine-executable task list from PLAN.json. Delegates to task-creator agent.'
allowed-tools: Task, Read
model: sonnet
---

# Tasks Command

*Delegate task generation to task-creator agent*

---

## Your Role

You are a **thin orchestrator** that:
1. Receives user request with plan path and optional --phase flag
2. Validates input via INPUT_GATE
3. Delegates to task-creator agent with timeout
4. Validates output via OUTPUT_GATE
5. Returns results

**DO NOT** implement task generation logic - that lives in task-creator agent and its skills.

---

## Workflow

```
USER: /tasks path/to/PLAN.json --phase=1
  |
  v
Parse arguments (path, --phase flag where N = number of phases in plan)
  |
  v
INPUT_GATE: path exists AND file readable AND extension is .json
  |-- FAIL: Return error with specific gate failure
  |-- PASS: Continue
  |
  v
Task(task-creator, 
     prompt="Generate tasks from {plan_path}. Phase filter: {phase}",
     timeout=120000)
  |-- FAIL: Retry once after 30s delay
  |-- FAIL again: Return task-creator error
  |
  v
OUTPUT_GATE: task-creator returns SUCCESS with valid schema
  |-- FAIL: Return error with validation details
  |-- PASS: Continue
  |
  v
Return task-creator output verbatim
```

### Review State Management

When task-creator returns with `review_groups`:

**Review Checkpoint Processing**:
```
FOR each review_group RG in output.review_groups:
  RG.status = "PENDING"
  
  # Link blocked tasks
  FOR each task_id in RG.blocks_tasks:
    task.blocked_by = RG.group_id
```

**Output includes**:
- `review_checkpoints_generated`: Count of review groups
- `blocked_task_count`: Total tasks blocked by reviews
- `deferred_findings`: Array (initially empty, populated during execution)

### Fix-Then-Proceed Workflow

During task execution, at each review checkpoint:

```
WHEN review checkpoint RG completes:
  findings = RG.review_results

  IF findings.critical > 0 OR findings.high > 0:
    # Generate fix task
    fix_task = {
      id: "T{next_id}",
      type: "fix",
      description: "Fix CRITICAL/HIGH findings from {RG.group_id}",
      agent: determine_agent(findings, RG.fix_agents),
      blocks: RG.blocks_tasks
    }
    
    # Execute fix and re-review (max 3 iterations)
    iteration = 0
    WHILE iteration < 3 AND has_critical_or_high(findings):
      execute(fix_task)
      findings = re_run_review(RG)
      iteration++
    
    IF iteration >= 3 AND has_critical_or_high(findings):
      ESCALATE to user with findings summary

  # Defer MEDIUM/LOW/NIT findings
  FOR each finding in findings WHERE severity IN ["MEDIUM", "LOW", "NIT"]:
    deferred_findings.append({
      from_checkpoint: RG.group_id,
      severity: finding.severity,
      finding_id: finding.id,
      description: finding.description,
      file_path: finding.file_path,
      deferred_at: now()
    })

  # Unblock downstream tasks
  FOR each task_id in RG.blocks_tasks:
    task.blocked_by = null
```

### Multi-Reviewer Parallel Execution

At each `code_review` checkpoint, 3 reviewers execute in parallel:

```
FOR each review_group RG WHERE RG.execution_mode == "parallel":
  
  # Launch all reviewers in single Task() message (parallel)
  reviewer_results = parallel(
    Task(RG.reviewers[0].agent, files=RG.files_in_scope, focus=RG.reviewers[0].focus),
    Task(RG.reviewers[1].agent, files=RG.files_in_scope, focus=RG.reviewers[1].focus),
    Task(RG.reviewers[2].agent, files=RG.files_in_scope, focus=RG.reviewers[2].focus)
  )
  
  # Aggregate findings using configured strategy
  aggregated_findings = aggregate_findings(
    results=reviewer_results,
    strategy=RG.aggregation.strategy,
    dedup_threshold=RG.aggregation.dedup_threshold,
    conflict_resolution=RG.aggregation.conflict_resolution
  )
  
  # Apply success criteria
  IF aggregated_findings.critical > 0 OR aggregated_findings.high > RG.success_criteria.max_high:
    generate_fix_task(findings=aggregated_findings.blocking)
  ELSE:
    RG.deferred_findings.extend(aggregated_findings.non_blocking)
```

### Finding Aggregation Strategy

**Severity Normalization**:
| Source Agent | Original Severity | Normalized |
|--------------|------------------|------------|
| python-code-reviewer | Critical | CRITICAL |
| python-code-reviewer | Major | HIGH |
| python-code-reviewer | Minor | MEDIUM |
| python-code-reviewer | Nit | LOW |
| architecture-reviewer | fails gate (<3.5) | CRITICAL |
| architecture-reviewer | near gate (3.5-3.7) | HIGH |
| architecture-reviewer | passes (>3.7) | n/a |
| tech-debt-investigator | Severe (<40) | HIGH |
| tech-debt-investigator | High (40-60) | MEDIUM |
| tech-debt-investigator | Moderate (60-80) | LOW |

**Deduplication**:
- Same file:line with >85% finding text similarity = merge
- Keep finding from highest-weighted reviewer
- Preserve all unique evidence citations

### Review Checkpoint Routing (Updated)

| review_type | Reviewers | Execution |
|-------------|-----------|-----------|
| `code_review` | python-code-reviewer, architecture-reviewer, tech-debt-investigator | **Parallel** |
| `integration_review` | integration-boundary-reviewer | Sequential |
| `final_review` | integration-boundary-reviewer + deferred findings | Sequential |

### Final Review Checkpoint

At end of task list, the `final_review` checkpoint:

1. Reviews ALL `deferred_findings` accumulated during execution
2. Performs full integration check via integration-boundary-reviewer
3. Gate: Must resolve or explicitly accept remaining findings

```
final_review_input = {
  deferred_findings: [...accumulated],
  scope: "full_integration",
  gate_criteria: {
    accept_remaining: user_confirmation_required
  }
}
```

---

## Agent Delegation

| Agent | Purpose |
|-------|---------|
| task-creator | Complete task generation workflow using generating-tasks skill |

---

## Error Handling

| Error | Action |
|-------|--------|
| Plan path doesn't exist | Return error: "Plan file not found: {path}. Verify path exists." |
| Plan file not readable | Return error: "Cannot read plan file: {path}. Check permissions." |
| Invalid file extension | Return error: "Expected .json file, got: {ext}" |
| Invalid --phase value | Return error: "Invalid phase. Valid range: 1 to {max_phases} (based on plan sections)" |
| task-creator timeout | Retry once after 30s delay, then return timeout error |
| task-creator fails | Return failure with task-creator's error message and recovery suggestions |
| Schema validation fails | Return error with specific validation violations |

---

## Output

Return task-creator output verbatim. Do not add additional formatting.

**Schema**: See `.claude/agents/planning/task-creator/schemas/task-creator.schema.json`
- `review_groups[].reviewers[]` - Multi-reviewer array (NEW)
- `review_groups[].execution_mode` - "parallel" or "sequential" (NEW)
- `review_groups[].aggregation` - Finding consolidation config (NEW)
- `review_type`, `fix_agents`, `success_criteria`, `deferred_findings` (existing)

---

## Examples

### SUCCESS Case
```json
{
  "status": "SUCCESS",
  "agent": "task-creator",
  "confidence": 0.92,
  "tasks_generated": 15,
  "review_groups": 3,
  "tdd_compliance": true,
  "parallel_eligible": 8,
  "output_files": ["tasks.md", "TASKS.json"]
}
```

### FAILURE Case
```json
{
  "status": "FAILURE",
  "agent": "task-creator",
  "error_code": "PARSE_ERROR",
  "error_message": "PLAN.json schema validation failed",
  "recovery_suggestions": ["Verify PLAN.json conforms to schema", "Check plan format against template"]
}
```

---

## Knowledge Base

| Resource | Path |
|----------|------|
| task-creator agent | `.claude/agents/planning/task-creator/task-creator.md` |
| generating-tasks skill | `.claude/skills/generating-tasks/SKILL.md` |
| Output schema | `.claude/agents/planning/task-creator/schemas/task-creator.schema.json` |

---

## Orchestrator Integration

**Trigger Keywords**: generate tasks, create tasks, task list, break down plan

**Delegation Pattern**:
```
User: "Generate tasks from the auth plan"
Claude Code (OBSERVE): Parse request -> Identify /tasks trigger
Claude Code (ORIENT): PLAN.json exists with 4 phases
Claude Code (DECIDE): ASC = 0.91 -> Delegate to /tasks
Claude Code (ACT): SlashCommand(command="/tasks docs/01-planning/features/auth/PLAN.json")
```

**Integration Points**:
- Upstream: `/plan` (creates PLAN.json)
- Downstream: `/implement` (executes tasks from TASKS.json)
