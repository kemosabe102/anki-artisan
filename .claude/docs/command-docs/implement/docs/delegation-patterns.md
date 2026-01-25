# Delegation Patterns for /implement Command

**CRITICAL**: Use these EXACT Task() call patterns. The orchestrator NEVER implements directly.

---

## Task Type to Agent Mapping

| Task Type | Agent | Retry Policy |
|-----------|-------|--------------|
| Implementation | development | 1 retry |
| Test Creation | code-quality | 1 retry |
| Test Execution | code-quality | 1 retry |
| Review Checkpoint | Multi-agent (3-5 parallel) | 3 retries |
| Fix after Review | debugger or development | Per iteration |

---

## Implementation Task Delegation

```
Task(
  subagent_type="development",
  prompt="Implement task {task_id}: {task.description}

    Context:
    - File: {task.file_path}
    - Dependencies: {task.dependencies}
    - Artifacts: {task.artifact_refs}
    - Spec reference: {meta.spec_file} (DO NOT LOAD - reference only)
    - Plan reference: {meta.plan_file} (DO NOT LOAD - reference only)

    Requirements:
    - Follow existing patterns in codebase
    - Maintain <500 token implementation summary
    - Return task_status: in_progress | completed | blocked

    Return: {
      implementation_summary: <500 tokens,
      task_status: completed | blocked,
      files_modified: [],
      error_details: null | string
    }"
)
```

**Expected Output**:
```json
{
  "implementation_summary": "Added ConfigMap mounting...",
  "task_status": "completed",
  "files_modified": ["k8s/local/api.yaml"],
  "error_details": null
}
```

---

## Test Creation Delegation

```
Task(
  subagent_type="code-quality",
  prompt="Create tests for task {task_id}: {task.description}

    Context:
    - Code files: {task.code_files}
    - Coverage requirements: {task.coverage_reqs}
    - Test patterns: Follow existing test patterns in tests/

    Requirements:
    - AAA pattern (Arrange-Act-Assert)
    - Mock external dependencies
    - Target >80% coverage for new code

    Return: {
      test_creation_summary: <300 tokens,
      task_status: completed | blocked,
      tests_generated: [],
      coverage_achieved: percentage
    }"
)
```

---

## Test Execution Delegation

```
Task(
  subagent_type="code-quality",
  prompt="Execute tests for task {task_id}

    Context:
    - Test suite: {task.test_suite}
    - Code files: {task.code_files}
    - Previous failures: {task.previous_failures}

    Requirements:
    - Run specified test suite
    - Categorize failures: APPLICATION_BUG | TEST_BUG | ENVIRONMENT | FLAKY
    - Attempt fixes (max 3 per test)

    Return: {
      test_execution_summary: <300 tokens,
      task_status: completed | blocked,
      failures: [],
      failure_categories: {}
    }"
)
```

---

## Review Checkpoint Delegation (Multi-Agent)

Review checkpoints use parallel multi-agent delegation. See `review-framework.md` for full details.

### Launch Pattern (Single Message)

```
# Launch ALL review agents in parallel (single message, multiple Task calls)

Task(
  subagent_type="code-quality",
  prompt="Code quality review for group {group_id}:
    Files: {review_group.files_in_scope}
    Focus: Code patterns, conventions, maintainability
    Return: {review_status, findings: [], blocking_issues: []}"
)

Task(
  subagent_type="architectureer",
  prompt="Architecture review for group {group_id}:
    Files: {review_group.files_in_scope}
    Focus: Integration, scalability, reliability
    Return: {review_status, findings: [], blocking_issues: []}"
)

Task(
  subagent_type="tech-debt-investigator",
  prompt="Tech debt review for group {group_id}:
    Files: {review_group.files_in_scope}
    Focus: Duplication, complexity, cleanup validation
    Return: {debt_score, findings: [], blocking_issues: []}"
)

# Dynamic agents (0-2 based on confidence >0.8)
# See review-framework.md for selection criteria
```

### Synthesis After Parallel Return

```
# Combine findings with weighted scoring
core_weight = 0.75 / 3  # Split among 3 core agents
dynamic_weight = 0.25 / N  # Split among N dynamic agents

# Categorize issues
critical_issues = [f for f in all_findings if f.severity == "critical"]
improvements = [f for f in all_findings if f.severity in ["high", "medium"]]
future_work = [f for f in all_findings if f.severity == "low"]

# Determine outcome
if len(critical_issues) > 0:
    proceed_to_fix_loop()
else:
    approve_checkpoint()
```

---

## Fix Agent Delegation (After Review Failure)

**Issue Type → Agent Selection**:

| Issue Type | Agent | Focus |
|------------|-------|-------|
| Test failures | debugger | Investigation, root cause |
| Pattern violations | development | Apply correct patterns |
| Security vulnerabilities | development | Security-focused fixes |
| Performance issues | development | Optimization |

```
Task(
  subagent_type="debugger",  # or development
  prompt="Fix critical issues from review {group_id}:

    Critical Issues:
    {formatted_critical_issues}

    Files: {review_group.files_in_scope}
    
    Iteration: {iteration_number} of 3
    
    Previous Fix Attempts (if iteration > 1):
    {formatted_iteration_history}
    # Format: "- Iteration N: {fix_attempted} → {outcome}\n  Issues: {issues_found}\n  Introduced: {new_issues}"
    
    Constraints:
    - Address ONLY critical blockers (not improvements)
    - Maintain existing functionality
    - Document what was changed
    - Do NOT revert changes from iteration {iteration_number - 1} unless explicitly required
    - Do NOT reintroduce patterns that were previously removed
    - If you detect conflicting requirements (fix A breaks B, fix B breaks A), return fix_status: 'ARCHITECTURAL_CONFLICT'

    Return: {
      fix_summary: <300 tokens,
      fix_status: 'resolved' | 'partial' | 'blocked' | 'ARCHITECTURAL_CONFLICT',
      issues_resolved: [],
      files_modified: [],
      new_issues_introduced: []  # Track for oscillation detection
    }"
)
```

---

## Progress Reporting Pattern

The orchestrator reports progress every 5 tasks OR 2 minutes OR at review checkpoints.

**Progress Report Format**:
```
📊 Implementation Progress: {plan_name}
Phase {N}: ✅ T001-T006 complete | 🔍 T007 in_progress [{agent}]
Status: {completed}/{total} tasks ({blocked} blocked) | Next: {next_task} | ETA: {estimate}
```

**State Tracking**:
```json
{
  "current_plan": "001-infrastructure-foundation",
  "completed_tasks": ["T001", "T002", "T003"],
  "in_progress_tasks": ["T004"],
  "blocked_tasks": [],
  "failed_review_groups": {},
  "elapsed_hours": 4.5
}
```

---

## Anti-Patterns

| ❌ NEVER | ✅ ALWAYS |
|----------|----------|
| Load full SPEC.md into prompt | Reference by path only |
| Implement code in orchestrator | Delegate to development |
| Run tests directly | Delegate to code-quality |
| Single reviewer for checkpoints | Multi-agent parallel review |
| Skip retry policy | 1x tasks, 3x reviews |
