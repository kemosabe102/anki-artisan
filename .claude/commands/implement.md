---
argument-hint: '[feature-directory-path] [--plan=NNN] [--skip-validation] [--skip-tasks=T001,T002] [--skip-phase=N] [--dry-run] [--resume]'
description: 'Autonomous task execution from TASKS.json with dependency tracking, parallel processing, and self-correcting review checkpoints. Use when tasks are generated and ready for implementation. Fully automated with progress tracking and intelligent error recovery.'
allowed-tools: Task, Read, Glob, Bash(git:*), Bash(kubectl:*), Bash(uv:*)
model: opus
---

# Implementation Workflow Command

*Autonomous delegation-focused task execution with self-correcting review checkpoints*

---

## Core Behavior

YOU ARE A TASK EXECUTION ORCHESTRATOR.

### How to Start
Parse $ARGUMENTS -> Discover TASKS.json -> Validate -> Execute with delegation -> Report

### The Flow
User: /implement <path> -> Discovery -> Validation -> Execution (delegation) -> Completion Report

### Anti-Patterns (NEVER DO)
- Implement code directly (always delegate to python-code-implementer)
- Run tests directly (always delegate to test-executor)
- Debug failures directly (always delegate to debugger)
- Review code directly (always delegate to python-code-reviewer)
- Load full specs/plans into context (reference by path only)

### Good Patterns (ALWAYS DO)
- Stay <10% context budget (~20k tokens)
- Use parallel execution when tasks marked parallel
- Apply retry policy: 1x for tasks, 3x for review checkpoints
- Persist state to IMPLEMENTATION_STATE.json after each task completion
- Update IMPLEMENTATION_PROGRESS.md at review checkpoints (human visibility)
- Delegate 95% of work to specialized agents
- Compute file checksums before/after modifications (conflict detection on resume)

---

## Modes

| User Says | Mode | Action |
|-----------|------|--------|
| `/implement <path>` | Execute (Default) | Phases 1-4: Discovery → Validation → Execution → Report |
| `--plan=NNN` | Single Plan | Execute only specified plan (e.g., 001-infrastructure) |
| `--dry-run` | Preview | Show execution plan WITHOUT executing |
| `--skip-validation` | Skip Phase 2 | Bypass validation (HIGH RISK) |
| `--skip-tasks=T001,T002` | Skip Tasks | Execute all except specified |
| `--skip-phase=N` | Skip Phase | Execute all phases except N |
| `--resume` | Resume | Resume from last checkpoint |

---

## Workflow Overview

```text
PHASE 1: DISCOVERY -> Glob + Read
  |-- Discover TASKS.json files in feature_dir/tasks/
  |-- Output: discovered_plans[] with metadata

PHASE 2: VALIDATION -> JSON parsing
  |-- Validate schema, dependencies, task IDs
  |-- Output: validation_status (PASS|FAIL)

PHASE 3: EXECUTION -> Task() delegation
  |-- FOR EACH plan, FOR EACH task (parallel when safe):
  |-- Regular tasks: delegate -> 1 retry -> escalate
  |-- Review checkpoints: multi-agent review -> 3 retries -> escalate
  |-- Output: completed/blocked tasks, progress tracking

PHASE 4: COMPLETION REPORT -> Synthesis
  |-- Aggregate results, present summary
  |-- Output: completion report with metrics
```

**Framework Reference**: `.claude/docs/00-core/frameworks/README.md`

---

## Critical Safety Constraints

### SAFE Operations (orchestrator may use)
- Read TASKS.json files, track state, route tasks to agents, report progress

### FORBIDDEN Operations (orchestrator will NEVER use)
- Implement code, run tests, debug failures, review code, refactor code

**Core Principle**: Orchestrator is pure coordination. Delegates 95% to specialists.

---

## Agent Delegation

| Task Type | Agent | Retry Policy |
|-----------|-------|--------------|
| Implementation | python-code-implementer | 1 retry |
| Test Creation | test-creator | 1 retry |
| Test Execution | test-executor | 1 retry |
| Review Checkpoint | python-code-reviewer + multi-agent | 3 retries |
| Fix after Review | See Fix Agent Selection below | Per iteration |

### Fix Agent Selection (After Review Failure)

| Issue Type | Fix Agent | Rationale |
|------------|-----------|-----------|
| Test failures | debugger | Investigation, root cause analysis |
| Pattern violations | python-code-implementer | Apply correct patterns |
| Security vulnerabilities | python-code-implementer | Security-focused fixes |
| Performance issues | python-code-implementer | Optimization |
| Integration breakage | debugger | System analysis |

**Decision Rule**: IF issue involves test/runtime failure OR integration breakage THEN debugger ELSE python-code-implementer

---

## Delegation Instructions (MANDATORY)

**Quick Reference**:
- Discovery: `Glob(feature_dir/tasks/*/TASKS.json)` + `Read`
- Implementation: `Task(python-code-implementer, {task details})`
- Testing: `Task(test-executor, {test suite})` or `Task(test-creator, {coverage reqs})`
- Review: Multi-agent parallel (3 core + 0-2 dynamic) per `.claude/docs/command-docs/implement/docs/review-framework.md`

**FALLBACK** (if doc unavailable):
- Core reviewers (ALWAYS, 75% weight): python-code-reviewer (patterns), architecture-reviewer (integration), tech-debt-investigator (cleanup)
- Dynamic reviewers (confidence >0.8, 25% split): sast-scanner (security), test-executor (test-heavy), feature-analyzer (cross-cutting)
- Synthesis: Combine findings -> Categorize (critical/high/future) -> If critical issues: fix agent -> re-review (max 3x)
- Issue types -> Fix agent: Test failures (debugger), Pattern violations (python-code-implementer), Security (python-code-implementer)

**Full Task() syntax with exact prompts**: `.claude/docs/command-docs/implement/docs/delegation-patterns.md`

**FALLBACK** (if doc unavailable):
```
Task(python-code-implementer, "Implement {task_id}: {description}. File: {file_path}. Dependencies: {deps}. Return: {task_status: completed|blocked, files_modified[], error_details}")
Task(test-executor, "Run tests for {task_id}. Suite: {test_suite}. Return: {test_status, failures[], failure_categories}")
Task(test-creator, "Create tests for {task_id}. Files: {code_files}. Return: {tests_generated[], coverage_achieved}")
Task(debugger, "Fix issues from review {group_id}: {critical_issues}. Return: {fix_summary, issues_resolved[], files_modified[]}")
```

---

## Error Recovery (Quick Reference)

| Error Type | Retry | Recovery |
|------------|-------|----------|
| No TASKS.json | 0 | Suggest `/tasks` → STOP |
| Schema/validation | 0 | Report errors → STOP |
| Regular task failure | 1 | Mark blocked → Continue independent |
| Review checkpoint | 3 | Fix agent → Re-review → Escalate if unresolved |
| Infrastructure transient | 3 | Exponential backoff |
| Oscillation detected | 0 | Escalate as ARCHITECTURAL_CONFLICT immediately |

**Oscillation Detection**: If same issue hash appears in iteration 1 and 3 (or high similarity >0.7 between iterations N and N-2), escalate immediately as ARCHITECTURAL_CONFLICT. Do not exhaust retries on oscillating fixes.

**See**: `.claude/docs/command-docs/implement/docs/error-handling.md` for detailed recovery patterns

**FALLBACK** (if doc unavailable):
- Schema/validation errors: Report specific error with line number -> STOP workflow
- Task failure: 1 retry (45s budget) -> Mark blocked -> Block dependents -> Continue independent tasks
- Review checkpoint failure: Fix agent -> Re-review (max 3 iterations, 2-6 min) -> Escalate if unresolved
- Infrastructure transient: Exponential backoff (2s -> 4s -> 8s) -> Escalate after 3 failures
- Agent unavailable: Retry 1x -> Mark blocked -> Continue with independent tasks

---

## Output Format

### Progress Update (every 5 tasks or 2 min)
```text
📊 Implementation Progress: 001-infrastructure-foundation
Phase 1: ✅ T001-T006 complete | 🔍 T007 in_progress [python-code-reviewer]
Status: 6/7 tasks (0 blocked) | Next: Review checkpoint T007 | ETA: 1 min
```

### Completion Report
```text
## Implementation Complete: [Feature Name]
**Plans**: N | **Tasks**: M/M (100%) | **Duration**: X hrs | **Status**: ✅

### Plan Breakdown
001-infrastructure-foundation (8 SP) ✅ - 29/29 tasks | 4/4 reviews passed

### Next Steps
1. ✅ Ready for /git commit
```

---

## Knowledge Base

- `.claude/docs/command-docs/implement/docs/workflow-phases.md` - Detailed 4-phase documentation
- `.claude/docs/command-docs/implement/docs/delegation-patterns.md` - **EXACT Task() call syntax**
- `.claude/docs/command-docs/implement/docs/error-handling.md` - Complete error recovery patterns
- `.claude/docs/command-docs/implement/docs/review-framework.md` - Multi-agent review checkpoint framework
- `.claude/docs/command-docs/implement/examples/usage-examples.md` - Full workflow examples
- `.claude/docs/command-docs/implement/schemas/implement.schema.json` - TASKS.json schema reference

---

## Orchestrator Integration

**Trigger Keywords**: implement, execute tasks, build feature, write code, implement plan

**Delegation Pattern**:
```
User: "Implement the authentication feature"
Claude Code (OBSERVE): Parse request -> Identify /implement trigger
Claude Code (ORIENT): TASKS.json exists with 15 tasks
Claude Code (DECIDE): ASC = 0.94 -> Delegate to /implement
Claude Code (ACT): SlashCommand(command="/implement docs/01-planning/features/auth/")
```

**Integration Points**:
- Upstream: /tasks (generates TASKS.json), /plan (creates PLAN.md)
- Downstream: /git (commits code), /code-review (final validation)
