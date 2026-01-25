# Context Readiness Assessor - Frameworks

## Hermeneutic Assessment Approach

**When to Apply**: Complex context gathering (CQ < 0.85), multi-component features (3+ files), architectural changes, new patterns without examples.

**Skip for**: Simple single-file changes, pattern-matching tasks, well-understood domains.

### Three Fore-Structures (Heidegger)

1. **Fore-having**: Total situation/context you're operating within
   - Current domain knowledge, mental models, constraints
   - Example: "Python codebase using Pydantic for data validation"

2. **Fore-sight**: Specific aspect or angle being examined
   - Which particular problem/component is the focus?
   - Example: "Focusing on error handling in auth module"

3. **Fore-conception**: Preliminary understanding or hypothesis
   - Initial interpretation before deep investigation
   - Example: "Hypothesis: validation error propagation issue"

### Iterative Refinement Process

1. **Initial scan** → Form provisional understanding (fore-conception)
2. **Examine details** → How do specifics challenge whole-view?
3. **Revise whole** → Update context model based on contradictions
4. **Re-examine details** → With new view, what details now matter?
5. **Stabilize** → Continue until understanding converges (CQ >= 0.85)

### Practical Questions
- "Does this detail fit my context model, or does the model need updating?"
- "What assumptions am I bringing that these findings contradict?"
- "Have I iterated enough, or am I forcing closure?"

---

## Iteration Management

### Iteration 1: Initial Assessment
1. Calculate baseline Context_Quality (all 4 components)
2. Identify all gaps with severity ratings
3. Coordinate research agents (prioritize critical gaps)
4. Synthesize findings into context improvements
5. Recalculate CQ → delta = iteration1 - baseline

### Iteration 2: Refinement (if CQ < 0.85)
1. Identify remaining gaps (focus on high-severity)
2. Coordinate targeted research (fewer agents, more focused)
3. Synthesize findings
4. Recalculate CQ → delta = iteration2 - iteration1
5. **Diminishing Returns Check**: If delta < 0.1, escalate early

### Iteration 3: Final Attempt (if still < 0.85)
1. Identify critical blocking gaps only
2. Coordinate minimal research (essential agents only)
3. Synthesize findings
4. Recalculate CQ → Final score
5. **Gate Decision**: PASS (>=0.85) or BLOCKED (escalate to user)

---

## Gate Logic

```
IF Context_Quality >= 0.85:
  gate_status = "PASS"
  ready_for_implementation = true
  recommendation = "PROCEED_TO_DECIDE"

ELSE IF iteration_count < 3:
  gate_status = "GATHER_MORE_CONTEXT"
  ready_for_implementation = false
  recommendation = "CONTINUE_ORIENT (iteration N+1)"

ELSE (CQ < 0.85 AND iteration_count = 3):
  gate_status = "BLOCKED"
  ready_for_implementation = false
  recommendation = "ESCALATE_TO_USER (manual intervention)"
```

---

## Improvement Tracking Metrics

| Metric | Description |
|--------|-------------|
| `iteration_count` | Iterations executed (0-3) |
| `baseline_score` | Initial CQ (iteration 0) |
| `current_score` | Latest CQ |
| `delta_per_iteration` | Array [delta1, delta2, delta3] |
| `diminishing_returns` | Boolean: delta < 0.1 detected |

### Escalation Triggers
- CQ < 0.85 after 3 iterations → BLOCKED
- Delta < 0.1 after any iteration → Early escalation warning
- No viable research agents for gaps → BLOCKED
- 5-minute timeout exceeded → BLOCKED

---

## Related Documentation

- [Domain Expertise & Scoring Rubrics](domain-expertise.md) - Component scoring, gap-to-agent mapping
- [Assessment Examples](../examples/assessment-examples.md) - 3 worked scenarios
- [Schema Contract](../schemas/context-readiness-assessor.schema.json) - Input/output validation
- [Main Agent Definition](../context-readiness-assessor.md) - Core behavior and workflow
