# Debugger Operations Guide

Detailed workflows for each debugger operation mode.

**Self-Contained Principle**: The debugger either solves the problem or returns FAILURE with evidence. No mid-task delegation to other agents.

---

## 1. debug (Standard Debugging)

**Purpose**: Hypothesis-driven debugging using 8-step scientific method

**Workflow**: See `docs/04-guides/debugger/hypothesis-driven-debugging.md` for complete methodology

**Quick Reference**:
1. Reproduce & Baseline - Make bug fail reliably, collect evidence
2. Formulate Hypothesis - Specific, testable statement (no edits yet)
3. Design Experiment - Test harness, instrumentation, or log analysis
4. Execute & Observe - Run experiment, capture outputs objectively
5. 5 Whys Analysis - Find root cause, not symptom
6. SCAMPER Solution - Generate 2-3 candidate fixes, select minimal
7. Minimal Fix - One change at a time, only after confirmation
8. Verify & Guard - Original test passes, no regressions, add guard test
9. Document RCA - Emit RCA record for audit trail

---

## 2. validate_pre_commit (Autonomous Pre-Commit Validation)

**Purpose**: Autonomous validation with self-correcting retry loop

**Timing**: 8-15 minutes typical
**Max Iterations**: 3 attempts
**Success Criteria**: All checks pass OR FAILURE with documented unfixable issues


### Workflow

```
Iteration 1:
  Run validation -> Parse failures -> Apply autonomous fixes -> Re-run

Iteration 2 (if still failing):
  Analyze remaining failures -> Apply targeted fixes -> Re-run

Iteration 3 (if still failing):
  Research via Context7/Perplexity -> Apply research-informed fixes -> Re-run
  If still failing -> Return FAILURE with unfixable issues documented
```

### Fix Categories (Auto-Applied)

| Category | Auto-Fix Strategy |
|----------|-------------------|
| Linting (ruff) | `ruff check --fix` |
| Formatting | `ruff format` |
| Import errors | Add missing imports |
| Type errors | Add type annotations or casts |
| Test failures | Apply debug methodology |

### Unfixable Handling

When issues persist after 3 iterations:
- Document each unfixable issue with evidence
- Provide recovery suggestions
- Return FAILURE with `unfixable_issues` array

---

## 3. fix_failing_tests (Per-Test OODA Fix Loop)

**Purpose**: Fix multiple failing tests with systematic per-test approach

**Timing**: 25-35 minutes per test
**Max Attempts per Test**: 3 (OODA cycle)
**Success Criteria**: All tests pass OR FAILURE with unfixable tests documented


### Per-Test OODA Cycle

```
Attempt 1 (OBSERVE -> ORIENT):
  Run test -> Capture failure -> Form initial hypothesis -> Apply fix -> Verify

Attempt 2 (ORIENT -> DECIDE):
  Analyze why fix failed -> Refine hypothesis -> Apply adjusted fix -> Verify

Attempt 3 (DECIDE -> ACT + Research):
  Escalate to research (Context7 first, Perplexity if needed)
  Apply research-informed fix -> Verify
  If still failing -> Return as unfixable with evidence
```

### Research Escalation Protocol

**Trigger**: Attempt 3 OR confidence < 0.8 OR 2+ failed fixes

**Tool Selection**:
1. **Context7 FIRST** (free, authoritative) - Framework/library errors
2. **Perplexity** (paid) - Only if Context7 insufficient or returns FAILURE
   - `perplexity_search`: Quick error lookups
   - `perplexity_research`: Deep investigation (use `strip_thinking=true`)
   - `perplexity_reason`: Multi-factor RCA

### Flaky Test Detection

When test passes sometimes, fails others:
- Re-run 3+ times with different orders
- Check for timing issues, shared state, environment differences
- Mark as flaky with statistical evidence if confirmed

### Unfixable Test Categorization

| Category | Evidence Required | FAILURE Response |
|----------|-------------------|------------------|
| Missing dependencies | Import errors, API key requirements | FAILURE(missing_dependencies) |
| External service failures | Connection errors, timeout traces | FAILURE(blocked) |
| Environment-specific | Works locally, fails in CI (document differences) | FAILURE(blocked) |
| Requires architectural change | Root cause analysis shows design issue | FAILURE(out_of_scope) |


---

## Experiment Toolkit

### Test Harness Pattern
```python
# .claude/debug/test_harness.py
from my_app.module import function_under_test

print("normal:", function_under_test(valid_input))
print("edge:", function_under_test(edge_case))
try:
    print("error:", function_under_test(invalid_input))
except Exception as e:
    print(f"Exception: {e}")
```

### Dynamic Instrumentation
```python
# Monkey-patch for debugging
original = module.function
def instrumented(*args, **kwargs):
    print(f"DEBUG: {args}, {kwargs}")
    result = original(*args, **kwargs)
    print(f"DEBUG: result = {result}")
    return result
module.function = instrumented
```

### Log Analysis
```bash
# Count occurrences
grep "ERROR" logs/*.log | wc -l

# Context around errors
grep -B 5 -A 5 "ERROR" logs/app.log
```

---

## Bash Command Standards

All Bash commands MUST use agent name prefix for traceability:

```bash
AGENT_NAME=debugger pytest tests/unit/test_module.py -v --tb=short
AGENT_NAME=debugger python .claude/debug/test_harness.py
```
