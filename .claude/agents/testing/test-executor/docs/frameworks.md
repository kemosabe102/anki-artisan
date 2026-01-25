# Test Executor Frameworks

**Purpose**: Methodologies applied by test-executor for fix loops, confidence scoring, and research

---

## 3-Attempt OODA Fix Loop

### Overview

Each failing test gets up to 3 fix attempts using OODA methodology before being marked unfixable.

### Timing Estimate

- ~3 min: Attempt 1 (categorization + standard fix)
- ~3 min: Attempt 2 (refined categorization + alternative fix)
- ~5 min: Attempt 3 (Context7/Perplexity research + informed fix)
- **Total: ~11 min max per test**

---

### Attempt 1: Initial OODA Evaluation & Fix

**Observe** (30 sec):
- Run failing test in isolation: `AGENT_NAME=test-executor pytest tests/path/test_file.py::test_name -v`
- Capture error message, traceback, assertion details
- Check test file context (fixtures, parametrization)

**Orient** (1 min):
- Categorize failure (APPLICATION_BUG, TEST_BUG, ENVIRONMENT, FLAKY)
- Identify root cause from traceback
- Form fix hypothesis

**Decide** (30 sec):
- Choose fix strategy: Update assertion, fix logic, adjust mock, update test data
- Identify file to modify
- Plan minimal change (no refactoring)

**Act** (1 min):
- Apply fix using Edit tool
- Rerun ONLY the specific failing test
- **If PASS**: Verify repeatability (run 1-2 more times)
- **If FAIL**: Proceed to Attempt 2

---

### Attempt 2: Re-Evaluate & New Fix

**Observe** (30 sec):
- Analyze NEW error output (may differ from attempt 1)
- Check if fix caused regression
- Read related code files for broader context

**Orient** (1 min):
- Re-categorize failure (category may change)
- Identify why first fix failed
- Form NEW hypothesis

**Decide** (30 sec):
- Choose different fix strategy
- Consider alternative approaches (mock vs data change)

**Act** (1 min):
- Apply NEW fix (may revert attempt 1)
- Rerun isolated test
- **If PASS**: Verify repeatability
- **If FAIL**: Proceed to Attempt 3

---

### Attempt 3: Research-Informed Fix

**Observe** (30 sec):
- Capture persistent error pattern
- Note attempt 1 & 2 approaches that failed
- Extract key error messages for search

**Orient** (2-3 min):
- **Research Protocol** (Context7 FIRST):
  1. `resolve_library_id("pytest")` -> Get library metadata
  2. `get_library_docs(library_id, topic="error_pattern")` -> Fetch docs
  3. IF trust>=7 AND snippets>=100 -> Use Context7 solution
  4. IF insufficient -> Perplexity: `perplexity_search("pytest {error_type}")`
- Synthesize research into fix strategy

**Decide** (1 min):
- Apply research findings to specific test context
- Choose fix informed by external knowledge
- Verify fix aligns with project patterns

**Act** (1 min):
- Apply research-informed fix
- Rerun isolated test
- **If PASS**: Note research source in output
- **If FAIL**: Mark unfixable, move to next test

---

### After 3 Attempts: Mark Unfixable

- Do NOT attempt further fixes
- Record all 3 attempts (hypotheses, fixes applied, errors observed)
- Move to next failing test immediately
- At end: Report unfixable tests with full history

---

## Confidence Scoring Formula

```
Confidence = (Pattern_Match_Strength × 0.6) + (Context_Clarity × 0.3) + (Historical_Accuracy × 0.1)
```

### Components

| Component | Description | Range |
|-----------|-------------|-------|
| Pattern_Match_Strength | How well error matches heuristic pattern | 0.0-1.0 |
| Context_Clarity | Clarity of error message and traceback | 0.0-1.0 |
| Historical_Accuracy | Success rate of similar categorizations | 0.0-1.0 (default 0.8) |

### Example Calculation

```
AssertionError in packages/core/auth.py:
- Pattern_Match_Strength: 0.75 (AssertionError + app code origin)
- Context_Clarity: 0.90 (clear traceback, specific line)
- Historical_Accuracy: 0.80 (default)

Confidence = (0.75 × 0.6) + (0.90 × 0.3) + (0.80 × 0.1)
           = 0.45 + 0.27 + 0.08
           = 0.80 -> APPLICATION_BUG (confident)
```

---

## Research Tool Selection Protocol

### Context7 First (Free, Authoritative)

**Use for**:
- Testing framework errors (pytest, jest, go test)
- Fixture issues, parametrization errors
- Test execution configuration
- Version-specific behavior

**Process**:
1. `resolve_library_id("pytest")`
2. `get_library_docs(library_id, topic="error_pattern", tokens=5000)`
3. IF trust>=7 AND snippets>=100 -> STOP, use solution
4. IF insufficient -> Escalate to Perplexity

### Perplexity Escalation (Paid)

**Use ONLY when**:
- Confidence < 0.8 (unclear failure cause)
- Context7 insufficient
- Test execution failed 2+ times
- Complex CI/CD environment issues

**Tool Selection**:
- `perplexity_search`: Quick error lookups (~$0.003)
- `perplexity_reason`: Root cause analysis (~$0.008-0.015)

---

## Loop Protection

### Maximum Iterations

- 3 attempts per test
- Same category delegated >3 times -> MANUAL_REVIEW_NEEDED

### Confidence Degradation

| Iteration | Adjustment |
|-----------|------------|
| 1 | Use calculated confidence |
| 2 | Reduce by 0.1 |
| 3 | Reduce by 0.2 |
| 4+ | Escalate (confidence too low) |

### Tracking Format

```json
{
  "delegation_history": [
    {"iteration": 1, "category": "TEST_BUG", "confidence": 0.75, "timestamp": "..."},
    {"iteration": 2, "category": "TEST_BUG", "confidence": 0.65, "timestamp": "..."},
    {"iteration": 3, "category": "TEST_BUG", "confidence": 0.55, "timestamp": "..."}
  ],
  "escalation_triggered": true,
  "next_step": "Manual investigation required"
}
```

---

## Multi-Agent Integration

### Upstream Dependencies

| Agent | Relationship |
|-------|--------------|
| test-creator | Creates tests -> test-executor runs them |
| python-code-implementer | Implements features -> test-executor validates |
| debugger | Fixes bugs -> test-executor confirms fix |

### Downstream Integration

| Category | Next Step |
|----------|-----------|
| APPLICATION_BUG | Investigate and fix logic error in app code |
| TEST_BUG | Fix test assertions, fixtures, or mocks |
| ENVIRONMENT | Environment setup (escalate for user intervention) |
| FLAKY_TEST | Fix test isolation and timing dependencies |
| Coverage gaps | Generate unit tests for uncovered functions |
