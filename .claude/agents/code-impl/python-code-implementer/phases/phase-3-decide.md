# Phase 3: DECIDE - Strategy Selection & Gate Resolution

**OODA Stage**: DECIDE | **Time Allocation**: 10-15%

**Purpose**: Select implementation mode, resolve gate priorities, prepare execution plan

**Deliverable**: Selected strategy, gate resolution order, execution plan ready for ACT

---

## Workflow Steps

### Step 3.1: Mode Detection (Auto-Select)

**Input**: Task requirements from Phase 1, scope from Phase 2

**Process**:
Match user intent to implementation mode:

| User Says | Mode | Start With |
|-----------|------|------------|
| "implement", "add feature", "create" | feature_implementation | Pre-flight + TDD |
| "fix this function", "update" | modification | Find existing tests first |
| "integrate", "connect" | integration | Map dependencies + tests |

**Output**: Selected mode with rationale

---

### Step 3.2: Gate Resolution Protocol

**When**: Multiple enforcement gates may trigger during execution

**Priority Order** (higher priority gates block lower):

| Priority | Gate | Blocks If |
|----------|------|-----------|
| 1 | Ambiguity Detection | ANY criterion clarity <= 2 |
| 2 | Scope Boundary Enforcement | File not in declared_scope |
| 3 | COMPONENT_ALMANAC Gate | Creating component without check |
| 4 | TDD-First Gate | No tests before implementation |
| 5 | Defensive Programming Gate | Violations in final code |

**Resolution Rules**:
- Report highest-priority HALT as primary `failure_type`
- Include `halted_gates` array listing all triggered gates
- Defer lower-priority checks until higher-priority resolved

**Multiple HALT Example**:
```json
{
  "status": "FAILURE",
  "failure_type": "ambiguous_requirements",
  "halted_gates": ["ambiguity_detection", "tdd_gate"],
  "details": {
    "primary_halt": "Ambiguity must be resolved before TDD can begin",
    "deferred_checks": ["tdd_gate will run after clarification"]
  }
}
```

---

### Step 3.3: CQ Threshold Decision

**Input**: CQ score from Phase 2

**Decision Matrix**:
| CQ Score | Decision |
|----------|----------|
| >= 0.85 | Proceed to ACT |
| 0.70 - 0.84 | One more research iteration, then proceed |
| < 0.70 | HALT with `insufficient_context` |

**HALT Protocol** (CQ < 0.70 after research):
```json
{
  "status": "FAILURE",
  "failure_type": "insufficient_context",
  "details": {
    "cq_score": 0.65,
    "research_attempted": ["Context7: pydantic validation", "Perplexity: async patterns"],
    "gaps_remaining": ["error handling strategy unclear", "retry policy undefined"]
  }
}
```

---

### Step 3.4: Execution Plan Preparation

**Process**:
1. Sequence file operations (tests first if TDD mode)
2. Plan tool usage order
3. Identify validation checkpoints

**Output**: Ordered execution plan for Phase 4


---

## Quick Checklist

Before advancing to Phase 4 (ACT):

- [ ] Implementation mode selected
- [ ] Gate resolution order understood
- [ ] CQ >= 0.85 confirmed
- [ ] Execution plan sequenced
- [ ] All higher-priority gates clear

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Ignoring gate priority | Always resolve highest-priority gate first |
| Proceeding with low CQ | HALT if CQ < 0.70 after research |
| Modifying before tests | TDD mode requires test-first |
| Skipping scope check | Verify file is in declared_scope before Edit |

---

## Exit Criteria

**All gates clear + CQ >= 0.85 required**

| Criterion | Weight | Check |
|-----------|--------|-------|
| Mode selected | 0.20 | feature/modification/integration chosen |
| Gates clear | 0.30 | No priority 1-2 gates triggered |
| CQ sufficient | 0.30 | CQ >= 0.85 |
| Plan ready | 0.20 | Execution sequence defined |

---

## Reference Documentation

- base-agent-pattern.md - Inherited gate patterns
- escalation-protocol.md - When to escalate

---

**Previous Phase**: [Phase 2: ORIENT](phase-2-orient.md)
**Next Phase**: [Phase 4: ACT](phase-4-act.md)
