# Phase 1: OBSERVE - Context Gathering & Validation

**OODA Stage**: OBSERVE | **Time Allocation**: 15-20%

**Purpose**: Gather task requirements, search for existing tests, sync with standards, identify ambiguities

**Deliverable**: Task analysis with test baseline, clarity scores, ALMANAC check status

---

## Pre-Flight Standards Sync

**MANDATORY first action before any task analysis**:

1. Read `docs/04-guides/code-review/coding-guidelines.md` - Prevention patterns
2. Read `docs/00-project/COMPONENT_ALMANAC.md` - Existing components
3. Confirm standards loaded: `standards_synced: true`

---

## Workflow Steps

### Step 1.1: Parse Task Requirements

**Input**: Task from orchestrator (goal, file paths, constraints)

**Process**:
1. Extract acceptance criteria from task description
2. Identify target files/modules
3. Note explicit constraints (dependencies, deadlines)

**Output**: Parsed requirements object


### Step 1.2: TDD-First Gate - Test Search

**Trigger**: Before ANY production code modification

**Process**:
1. Search for existing tests: `Grep("test.*<module_name>", path="tests/")`
2. Document findings:
   - `existing_tests_found`: List of test files/functions discovered
   - `tests_needed`: true if no tests exist for target functionality
3. If no tests exist, mark `tests_needed: true` for Phase 4 creation

**Output**:
```json
{
  "existing_tests_found": ["tests/unit/test_auth.py:45-67"],
  "tests_needed": false,
  "test_coverage_estimate": "partial"
}
```

---

### Step 1.3: COMPONENT_ALMANAC Check

**Trigger**: Before creating ANY new module, class, or utility function

**Process**:
1. Read `docs/00-project/COMPONENT_ALMANAC.md`
2. Search for existing functionality matching intended creation
3. Document reuse decision

**Output**:
```json
{
  "almanac_check": {
    "checked": true,
    "existing_components_found": ["packages/core/validators.py:InputValidator"],
    "reuse_decision": "extend" | "new_required",
    "justification": "Existing validator lacks async support needed"
  }
}
```

**HALT Condition**: Creating new component without `almanac_check.checked: true`


---

### Step 1.4: Ambiguity Detection Protocol

**Trigger**: During analysis for each acceptance criterion

**Clarity Scoring (1-5)**:
| Score | Meaning | Action |
|-------|---------|--------|
| 5 | Fully testable (specific inputs, outputs, error cases) | Proceed |
| 4 | Mostly testable (minor assumptions acceptable) | Document assumptions |
| 3 | Partially testable (significant assumptions required) | Document assumptions |
| 2 | Vague (requires interpretation) | HALT - request clarification |
| 1 | Ambiguous (contradictory or undefined) | HALT - request clarification |

**Process**:
1. Score each acceptance criterion
2. Document assumptions for scores 3-4
3. For scores <=2, identify specific ambiguities

**HALT Threshold**: ANY criterion scoring <=2:
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

**Resume**: Orchestrator provides clarification -> re-score -> proceed if all >=3


---

## Quick Checklist

Before advancing to Phase 2 (ORIENT):

- [ ] Standards synced (coding-guidelines.md, COMPONENT_ALMANAC.md)
- [ ] Task requirements parsed and understood
- [ ] Existing tests searched (TDD-First Gate)
- [ ] ALMANAC checked for existing components
- [ ] All criteria clarity score >= 3

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Skipping standards sync | ALWAYS read coding-guidelines.md first |
| Implementing before finding tests | Search tests/ directory first |
| Creating duplicate utilities | Check COMPONENT_ALMANAC.md |
| Assuming vague requirements | Score clarity, HALT if <= 2 |

---

## Exit Criteria

**CQ (Context Quality) >= 0.70 required to proceed**

| Criterion | Weight | Check |
|-----------|--------|-------|
| Standards synced | 0.20 | coding-guidelines.md read |
| Tests baseline established | 0.30 | existing_tests_found documented |
| ALMANAC checked | 0.20 | almanac_check.checked: true |
| Requirements clear | 0.30 | All clarity scores >= 3 |

---

## Reference Documentation

- coding-guidelines.md - Prevention patterns
- COMPONENT_ALMANAC.md - Existing components
- base-agent-pattern.md - Inherited patterns

---

**Next Phase**: [Phase 2: ORIENT](phase-2-orient.md)
