# Enforcement Gates Reference

5 blocking gates enforced during Python implementation. Gates are checked in priority order.

---

## Gate 1: Ambiguity Detection (Priority 1 - Highest)

**Trigger**: During analysis for each acceptance criterion

### Clarity Scoring (1-5)

| Score | Meaning | Action |
|-------|---------|--------|
| 5 | Fully testable (specific inputs, outputs, error cases) | Proceed |
| 4 | Mostly testable (minor assumptions acceptable) | Document assumptions |
| 3 | Partially testable (significant assumptions required) | Document assumptions |
| 2 | Vague (requires interpretation) | **HALT** - request clarification |
| 1 | Ambiguous (contradictory or undefined) | **HALT** - request clarification |

### HALT Condition
ANY criterion scoring <= 2:

```json
{
  "status": "FAILURE",
  "failure_type": "ambiguous_requirements",
  "ambiguous_criteria": [
    {
      "criterion": "handle errors gracefully",
      "clarity_score": 2,
      "interpretations": ["log and continue", "retry with backoff", "fail fast"],
      "question": "Which error handling strategy is required?"
    }
  ]
}
```

---

## Gate 2: Scope Boundary Enforcement (Priority 2)

**Trigger**: Before ANY file modification

### Process
1. Declare scope explicitly before modifications
2. Separate files into modify vs read-only categories
3. Verify file is in declared scope before any Edit operation

### Output Format
```json
{
  "declared_scope": {
    "files_to_modify": ["packages/api/auth.py", "tests/unit/test_auth.py"],
    "files_read_only": ["packages/core/base.py"],
    "rationale": "Auth feature requires auth.py changes and new tests"
  }
}
```

### HALT Condition
Attempting to modify undeclared file -> `failure_type: "scope_boundary_violation"`

---

## Gate 3: COMPONENT_ALMANAC Check (Priority 3)

**Trigger**: Before creating ANY new module, class, or utility function

### Process
1. Read `docs/00-project/COMPONENT_ALMANAC.md`
2. Search for existing functionality matching intended creation
3. Document reuse decision

### Output Format
```json
{
  "almanac_check": {
    "checked": true,
    "existing_components_found": ["packages/core/validators.py:InputValidator"],
    "reuse_decision": "extend | new_required",
    "justification": "Existing validator lacks async support needed"
  }
}
```

### HALT Condition
Creating new component without `almanac_check.checked: true`

---

## Gate 4: TDD-First Gate (Priority 4)

**Trigger**: Before ANY production code modification

### Protocol
1. If `tests_needed: true`: Create test file FIRST with failing test
2. Run test to confirm failure (proves test is meaningful)
3. Implement production code to pass tests
4. Run full test suite to verify pass

### Evidence Required
```json
{
  "tdd_evidence": {
    "existing_tests_found": ["tests/unit/test_auth.py:45-67"],
    "tests_created": ["tests/unit/test_new_feature.py"],
    "pre_impl_test_run": "1 failed (expected)",
    "post_impl_test_run": "5 passed in 0.3s"
  }
}
```

### HALT Conditions
- `tdd_evidence` missing -> `failure_type: "tdd_gate_violation"`
- `post_impl_test_run` shows failures -> `failure_type: "tests_failing"`

---

## Gate 5: Defensive Programming Gate (Priority 5)

**Trigger**: Before returning implementation results

### Verification Protocol

| Check | Detection | Fix |
|-------|-----------|-----|
| DP-02: No Mutable Defaults | Grep for `=[]`, `={}`, `=set()` | Use `None` sentinel |
| DP-03: No Bare Exceptions | No `except Exception:` without re-raise | Specific exceptions only |
| DP-10: Input Validation | Public functions validate inputs | Add validation at entry points |

### Evidence Required
```json
{
  "defensive_checks": {
    "mutable_defaults": "none found | lines X, Y fixed",
    "exception_handling": "specific exceptions only",
    "input_validation": "validated at lines X, Y | N/A: internal function"
  }
}
```

### HALT Condition
Mutable default found and not fixed -> `failure_type: "mutable_default_violation"`

---

## Gate Resolution Priority

When multiple gates trigger, resolve in priority order:

**Ambiguity (1) > Scope (2) > ALMANAC (3) > TDD (4) > Defensive (5)**

Report highest-priority HALT as primary `failure_type`.
