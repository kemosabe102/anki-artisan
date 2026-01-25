---
title: "Debugger: fix_failing_tests Operation"
date: 2025-01-18
status: ACTIVE
tags: [debugger, testing, ooda, research]
---

# fix_failing_tests Operation

**Purpose**: Per-test fix loop with 3-attempt OODA cycle for persistent test failures

**Parent Agent**: [debugger.md](../../../agents/debugger.md)

**Operation Type**: Per-test debugging with progressive research escalation

---

## Quick Reference

| Attribute | Value |
|-----------|-------|
| **Max Attempts per Test** | 3 attempts (OODA cycle) |
| **Timing** | 25-35 minutes per test |
| **WebSearch Escalation** | Attempt 3 (if confidence < 0.8 OR 2 failures) |
| **Success Criteria** | All tests pass OR unfixable tests documented |
| **Unfixable Handling** | Mark unfixable, continue to next test |
| **Flaky Test Detection** | Verify repeatability (1-3 runs) after each successful fix |

---

## Goal

Fix individual failing tests through isolated debugging with progressive research escalation

**Key Principle**: One test at a time, 3 attempts per test with OODA cycle (OBSERVE → ORIENT → DECIDE → ACT), WebSearch research on attempt 3

---

## When to Use This Operation

**Primary Triggers**:

- Multiple tests failing in pre-commit validation after Iteration 2
- Test suite with mix of failures needing individual attention
- Complex test failures requiring focused debugging per test
- Orchestrator needs granular test-by-test progress tracking

**NOT for**:

- Single test failure (use standard debugging workflow)
- Test failures requiring architecture changes (escalate to orchestrator)
- Tests failing due to missing dependencies (fix dependencies first)

---

## Timing Rationale

**debugger.fix_failing_tests**: 25-35 min per test (comprehensive debugging)

- 5-8 min: Attempt 1 (hypothesis-driven debugging)
- 8-12 min: Attempt 2 (refined hypothesis with additional evidence)
- 12-15 min: Attempt 3 (WebSearch research + informed fix)

**When to Choose debugger**:

- Complex logic bugs requiring 5 Whys RCA
- Multi-component failures
- Architecture or design issues
- Async/concurrency problems
- After code-quality exhausted 3 attempts

**Alternative**: code-quality.fix_failing_tests (~11 min/test) for simple failures with clear categorization (assertion mismatches, type errors, simple logic bugs).

---

## 3-Attempt OODA Cycle (Per Test)

**Pattern**: Fix → Verify → Research → Fix (progressive escalation)

```
TEST: path/to/test.py::test_specific_case

ATTEMPT 1 (Standard Fix - 5-8 min):
├─ OBSERVE: Run isolated test, collect failure evidence
│  Command: pytest path/to/test.py::test_specific_case -v --tb=short
├─ ORIENT: Form hypothesis from error message, stack trace
├─ DECIDE: Apply standard debugging (hypothesis → minimal fix)
├─ ACT: Apply single focused change using Edit tool
├─ VERIFY: Re-run isolated test
│  ├─ IF PASS → Verify repeatability (run test 1-2 more times)
│  │  ├─ IF all PASS → Test fixed successfully, move to next test
│  │  └─ IF any FAIL → FLAKY_TEST detected, mark unfixable with flaky evidence
│  └─ IF FAIL → Continue to Attempt 2
└─ NEXT: Proceed to Attempt 2 if verification failed

ATTEMPT 2 (Hypothesis Refinement - 8-12 min):
├─ OBSERVE: Re-run test, collect additional evidence (logs, debug output)
├─ ORIENT: Refine hypothesis based on new evidence, check related code
├─ DECIDE: Apply refined fix (may involve multiple files)
├─ ACT: Apply refined fix (may involve multiple files)
├─ VERIFY: Re-run isolated test + related tests
│  ├─ IF PASS → Verify repeatability (run test 1-2 more times)
│  │  ├─ IF all PASS → Test fixed successfully, move to next test
│  │  └─ IF any FAIL → FLAKY_TEST detected, mark unfixable with flaky evidence
│  └─ IF FAIL → Continue to Attempt 3
└─ NEXT: Proceed to Attempt 3 if verification failed

ATTEMPT 3 (Research Escalation - 12-15 min):
├─ OBSERVE: Comprehensive evidence collection (test context, dependencies)
├─ ORIENT: WebSearch research for similar patterns/issues
│  Research Strategy:
│  - Search: "[test framework] [error pattern] debugging"
│  - Search: "[library name] [specific error] troubleshooting"
│  - Extract: Root cause patterns, fix examples, edge cases
├─ DECIDE: Apply research-informed fix
├─ ACT: Apply research-informed change
├─ VERIFY: Re-run isolated test comprehensively
│  ├─ IF PASS → Verify repeatability (run test 2-3 more times)
│  │  ├─ IF all PASS → Test fixed successfully, move to next test
│  │  └─ IF any FAIL → FLAKY_TEST detected, mark unfixable with flaky evidence
│  └─ IF FAIL → Mark unfixable, continue to next test
└─ NEXT: Mark test unfixable if verification failed after research

UNFIXABLE TEST:
└─ Document: Test name, attempts made, evidence collected, recommended action
```

---

## Test Isolation Pattern

**CRITICAL**: Use pytest's test selection to run ONE test at a time:

```bash
# ✅ CORRECT: Isolated test execution
AGENT_NAME=debugger pytest path/to/test.py::test_specific_name -v --tb=short

# ❌ WRONG: Running entire test file
AGENT_NAME=debugger pytest path/to/test.py

# ❌ WRONG: Running test suite
AGENT_NAME=debugger pytest tests/
```

**Why Isolation**:

- Eliminates test interdependencies affecting results
- Faster feedback loop (5-10 sec vs 2-5 min)
- Clear pass/fail signal per attempt
- Prevents cascading failures from obscuring root cause

---

## WebSearch Research Strategy (Attempt 3)

**When to Research**: Only on Attempt 3 after 2 failed fix attempts

**Research Queries** (prioritized):

1. **Error Pattern Search**:
   - Query: `"[exact error message]" [test framework] debugging`
   - Extract: Root cause explanations, fix examples
   - Time: 2-3 min

2. **Library-Specific Search**:
   - Query: `[library name] [error type] troubleshooting best practices`
   - Extract: Known issues, version-specific bugs, workarounds
   - Time: 2-3 min

3. **Stack Overflow Pattern Search**:
   - Query: `site:stackoverflow.com [error pattern] [language]`
   - Extract: Community solutions, edge case handling
   - Time: 1-2 min

**Research Output Requirements**:

- Cite sources in evidence (WebSearch-[timestamp])
- Document applied pattern/solution from research
- Note if research contradicts initial hypothesis

**Research Budget**: Max 6-8 min per test on Attempt 3

---

## Tracking Unfixable Tests

**Unfixable Definition**: Test still fails after 3 attempts (15-20 min investment)

**Documentation Requirements**:

```json
{
  "test_name": "path/to/test.py::test_failing_case",
  "attempts": [
    {
      "attempt": 1,
      "hypothesis": "Missing null check in handler",
      "action": "Added validation guard",
      "result": "FAIL - Different error: KeyError"
    },
    {
      "attempt": 2,
      "hypothesis": "KeyError from missing config",
      "action": "Added config initialization",
      "result": "FAIL - Timeout error"
    },
    {
      "attempt": 3,
      "hypothesis": "Async timeout issue per research",
      "research_sources": ["WebSearch-async-timeout-patterns"],
      "action": "Increased timeout + added retry logic",
      "result": "FAIL - Persistent timeout"
    }
  ],
  "recommendation": "Requires architecture change - async event loop may be blocked. Escalate to development for async refactoring."
}
```

**Escalation Triggers**:

- Test requires design/architecture changes (not bug fix)
- Test depends on external service/resource not available
- Test failure is intermittent (flaky test issue)
- Fix would require breaking changes to public API

---

## Workflow Integration

**Orchestrator Pattern** (task delegation):

```python
# Orchestrator receives multiple test failures from validate_pre_commit
failing_tests = [
    "tests/unit/test_auth.py::test_jwt_validation",
    "tests/unit/test_api.py::test_rate_limiting",
    "tests/unit/test_db.py::test_transaction_rollback"
]

# Delegate to fix_failing_tests operation
response = await call_agent(
    agent="debugger",
    operation="fix_failing_tests",
    tests=failing_tests,
    max_attempts_per_test=3
)

# Process results
if response.status == "SUCCESS":
    print(f"Fixed {len(response.agent_specific_output.tests_fixed)} tests")

    # Handle unfixable tests
    if response.agent_specific_output.unfixable_tests:
        for test in response.agent_specific_output.unfixable_tests:
            print(f"Unfixable: {test.test_name} - {test.recommendation}")
            # Escalate to appropriate agent based on recommendation
else:
    # Operation failed entirely
    handle_failure(response.failure_details)
```

---

## Output Schema

```json
{
  "status": "SUCCESS" | "FAILURE",

  "agent_specific_output": {
    "tests_fixed": [
      {
        "test_name": "path/to/test.py::test_case",
        "attempts_needed": {
          "type": "integer",
          "minimum": 1,
          "maximum": 3,
          "description": "Number of OODA attempts required to fix"
        },
        "fix_description": "Added null validation guard",
        "files_modified": ["path/to/module.py"],
        "research_used": {
          "type": "boolean",
          "description": "Whether WebSearch research was used"
        },
        "research_sources": ["WebSearch-pattern-name"]
      }
    ],

    "unfixable_tests": [
      {
        "test_name": "path/to/test.py::test_failing",
        "attempts": [ /* detailed attempt log */ ],
        "recommendation": "Escalation guidance with rationale",
        "evidence": {
          "error_patterns": ["TimeoutError", "ConnectionRefused"],
          "research_findings": ["Requires async refactoring per WebSearch-async-patterns"]
        }
      }
    ],

    "summary": {
      "total_tests": 5,
      "fixed": 3,
      "unfixable": 2,
      "total_duration_seconds": 420,
      "research_triggered": 2
    }
  },

  "failure_details": {
    "reason": "Operation failed before test processing",
    "recovery_suggestions": [
      "Check test file paths are valid",
      "Ensure pytest is available",
      "Verify working directory is correct"
    ]
  }
}
```

---

## Safety Constraints

**SAFE Operations** (per-test loop):

- ✅ Running isolated tests via pytest path::test_name
- ✅ WebSearch research on Attempt 3
- ✅ Fixing code to make test pass (standard debugging)
- ✅ Tracking unfixable tests for escalation
- ✅ Comprehensive evidence collection per attempt

**FORBIDDEN Operations**:

- ❌ Skipping tests to make suite pass
- ❌ Disabling tests instead of fixing
- ❌ Running full test suite (defeats isolation)
- ❌ Attempting >3 fixes per test (exceeds budget)
- ❌ Delegating to other agents (sub-agents cannot delegate)

---

## Integration with validate_pre_commit

**Handoff Pattern**: When validate_pre_commit hits persistent test failures in Iteration 2:

```
validate_pre_commit (Iteration 2):
├─ Run validation script
├─ Detect: 5 test failures persist after auto-fixes
├─ Extract test names from failure output
├─ Decision: Delegate to fix_failing_tests operation
└─ Return: Partial fix status with unfixable tests

fix_failing_tests (Called by orchestrator):
├─ Process 5 tests with 3-attempt OODA cycle each
├─ Fix 3 tests successfully
├─ Mark 2 tests unfixable with escalation guidance
└─ Return: SUCCESS with unfixable_tests list

orchestrator:
├─ Receives fix_failing_tests results
├─ Re-run validate_pre_commit to verify 3 fixed tests
├─ Escalate 2 unfixable tests based on recommendations
└─ Final validation: PASS (fixed tests) or BLOCK (unfixable critical tests)
```

**Note**: This operation is designed for orchestrator coordination. The validate_pre_commit operation focuses on auto-fixable issues (linting, formatting, simple test failures). Complex test failures requiring per-test OODA cycles are handled here.

---

## Schema Reference

See `.claude/docs/schemas/debugger.schema.json` → `agent_specific_output.fix_failing_tests`

---

## Parent Agent

This operation is part of the [debugger](../../../agents/debugger.md) agent. See parent for:
- Core 8-step debugging methodology
- Research tool selection (Context7 first, Perplexity escalation)
- File operation protocol
- Pre-flight checklist
- Complete agent capabilities and boundaries
