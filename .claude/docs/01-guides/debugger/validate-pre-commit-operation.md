---
title: "Debugger: validate_pre_commit Operation"
date: 2025-01-18
status: ACTIVE
tags: [debugger, pre-commit, validation]
---

# validate_pre_commit Operation

**Purpose**: Autonomous pre-commit validation with built-in error recovery for /git workflow

**Parent Agent**: [debugger.md](../../../agents/debugger.md)

**Operation Type**: Autonomous validation with fix loop

---

## Quick Reference

| Attribute | Value |
|-----------|-------|
| **Max Iterations** | 3 attempts |
| **Timing** | 8-15 minutes typical |
| **WebSearch Escalation** | Not applicable (handled by fix_failing_tests operation) |
| **Success Criteria** | All checks pass OR all failures documented |
| **Delegation Path** | Complex test failures → fix_failing_tests operation |

---

## Goal

Make validation script pass - run script, fix issues, re-run, repeat until success (max 3 attempts)

**Key Principle**: The debugger handles the ENTIRE validation + fix + retry loop autonomously. The orchestrator just calls this operation and trusts the SUCCESS/FAILURE result.

---

## ABSOLUTE CONSTRAINTS (MANDATORY)

**Commands Allowed**:

- ✅ `uv run python scripts/prepare-code-review.py --fast` - The ONLY validation command

- ✅ `ruff check --fix <files>` - For auto-fixing linting (if needed)

- ✅ `ruff format <files>` - For auto-formatting (if needed)

- ✅ File operations: Read, Edit, Write, Grep, Glob - For fixing code

**Commands FORBIDDEN**:

- ❌ `cd` to any directory - NEVER change directories

- ❌ `pytest` directly - NEVER run pytest outside validation script

- ❌ Any `timeout` wrapper commands - Use validation script only

- ❌ Manual test commands - Use validation script only

**Fix Strategy**:

1. Run validation script: `uv run python scripts/prepare-code-review.py --fast`

2. If fails: Read error output, identify issues

3. Fix code using Edit/Write tools (never run tests manually)

4. Re-run validation script (same command as step 1)

5. Repeat until pass or max 3 attempts

---

## Why Debugger (Not Test-Executor)?

The debugger is perfect for this because:

- ✅ **Fixes issues** (test failures, import errors, syntax errors)

- ✅ **Iterates autonomously** (retry loop built into the agent)

- ✅ **Makes things pass** (goal-oriented: achieve passing validation)

The code-quality would just report failures - it doesn't fix things.

---

## Workflow

**The debugger manages this entire loop internally:**

**CRITICAL CONSTRAINTS**:

- ❌ **NEVER cd to directories** - all commands run from current working directory

- ❌ **NEVER run pytest directly** - ONLY use the validation script

- ❌ **NEVER run individual test commands** - ONLY use the validation script

- ✅ **ONLY command allowed**: `uv run python scripts/prepare-code-review.py --fast`

```
ITERATION 1:
├─ Run: uv run python scripts/prepare-code-review.py --fast
├─ Parse output (DO NOT run any other commands)
├─ IF SUCCESS → Return SUCCESS
└─ IF FAILURE → Fix issues and continue to Iteration 2

ITERATION 2:
├─ Fix linting/formatting issues (auto-fixable with ruff)
├─ Fix test failures (edit code only, DO NOT run pytest directly)
├─ Fix import errors (analyze dependencies)
├─ Re-run validation script: uv run python scripts/prepare-code-review.py --fast
├─ IF SUCCESS → Return SUCCESS
└─ IF FAILURE → Continue to Iteration 3

ITERATION 3:
├─ Fix remaining complex issues (edit code only)
├─ Re-run validation script: uv run python scripts/prepare-code-review.py --fast
├─ IF SUCCESS → Return SUCCESS
└─ IF FAILURE → Return FAILURE with blockers for orchestrator
```

---

## Actions Per Iteration

**Iteration 1**: Initial validation attempt

- Run `uv run python scripts/prepare-code-review.py --fast` (ONLY this command)

- If passes → SUCCESS, done

- If fails → Analyze failures from script output, proceed to Iteration 2

**Iteration 2**: Auto-fix common issues

- Apply ruff auto-fixes for linting: `ruff check --fix <files>`

- Apply ruff format for formatting: `ruff format <files>`

- Fix simple test failures by editing code (DO NOT run pytest manually)

- Re-run validation script: `uv run python scripts/prepare-code-review.py --fast`

- If passes → SUCCESS, done

- If fails → Proceed to Iteration 3

**Iteration 3**: Fix complex issues

- Debug remaining test failures by editing code (DO NOT run pytest manually)

- Fix import/dependency errors by editing code

- Fix syntax errors by editing code

- Re-run validation script: `uv run python scripts/prepare-code-review.py --fast`

- If passes → SUCCESS, done

- If still fails → Return FAILURE with blockers

**CRITICAL**: The validation script already runs all tests. DO NOT run pytest separately.

**Test Failure Delegation**: For persistent test failures after Iteration 2, consider delegating to fix_failing_tests operation for per-test OODA loop with research escalation.

---

## Output Schema

```json
{
  "status": {
    "type": "string",
    "enum": ["SUCCESS", "FAILURE"],
    "description": "Operation outcome status"
  },

  "agent_specific_output": {
    "validation_status": {
      "type": "string",
      "enum": ["PASS", "FAIL"],
      "description": "Final validation script outcome"
    },

    "fixes_applied": [
      {
        "type": {
          "type": "string",
          "enum": ["linting", "formatting", "test_failure", "import_error", "syntax_error"],
          "description": "Category of fix applied"
        },

        "files": ["path/to/file.py"],

        "description": "Fixed unused import in auth.py"
      }
    ],

    "iteration_count": {
      "type": "integer",
      "minimum": 1,
      "maximum": 3,
      "description": "Number of validation iterations executed"
    },

    "duration_seconds": 120
  },

  "failure_details": {
    "unfixable_issues": [
      "Test failure: test_auth.py::test_jwt_validation (complex logic bug)",

      "Import error: missing external dependency 'some_package'"
    ],

    "recovery_suggestions": [
      "Manual fix needed for test_jwt_validation - requires understanding auth logic",

      "Install missing dependency: uv add some_package"
    ]
  }
}
```

---

## Integration with /git Command

**Orchestrator Pattern** (simple delegation, trust the result):

```python
# Orchestrator calls debugger
response = await call_agent(
    agent="debugger",

    operation="validate_pre_commit",

    files=modified_files
)

# Trust the agent's SUCCESS/FAILURE
if response.status == "SUCCESS":
    # Validation passed after agent's autonomous fixes
    proceed_to_phase_2()
else:
    # Agent couldn't fix after 3 attempts
    report_blockers_to_user(response.failure_details)
    stop_workflow()
```

**NO orchestrator retry loop needed** - the agent handles it internally!

---

## Safety Constraints

**SAFE Operations** (debugger may use):

- ✅ Running validation script multiple times

- ✅ Auto-fixing linting/formatting (ruff)

- ✅ Debugging test failures (hypothesis-driven)

- ✅ Reading git status/diff

- ✅ Analyzing error messages

- ✅ Fixing code to make tests pass

**FORBIDDEN Operations** (debugger will NEVER use):

- ❌ `git reset --hard` (discards changes)

- ❌ `git clean -fd` (deletes untracked files)

- ❌ `git checkout -- <file>` (discards file changes)

- ❌ `git stash` (hides changes)

- ❌ Deleting user's code to make tests pass

**Core Principle**: Fix CODE to make validation pass, never discard git changes.

---

## Schema Reference

See `.claude/docs/schemas/debugger.schema.json` → `agent_specific_output.validate_pre_commit`

---

## Parent Agent

This operation is part of the [debugger](../../../agents/debugger.md) agent. See parent for:
- Core 8-step debugging methodology
- Research tool selection (Context7 first, Perplexity escalation)
- File operation protocol
- Pre-flight checklist
- Complete agent capabilities and boundaries
