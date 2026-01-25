# Phase 3: DECIDE - Planning and Mode Selection

**OODA Stage**: DECIDE | **Time Allocation**: 10-15%

**Purpose**: Generate execution plan, select apply mode, assess risks, create todo breakdown

**Deliverable**: Structured task plan with dependencies, risk register, apply mode decision

---

## Mode Selection

### Step 3.1: Select Apply Mode

**Input**: Operation type, risk assessment, user preferences

**Mode Decision Matrix**:

| Condition | Apply Mode | Rationale |
|-----------|------------|-----------|
| First-time operation | `dry_run` | Validate without side effects |
| Modifying critical files | `dry_run` | Preview changes before commit |
| User explicitly requests | `commit` | Trust user judgment |
| Routine sync operation | `commit` | Low risk, high frequency |
| Pre-mortem/analysis | N/A | Read-only operations |

**Output**: Selected apply mode with rationale


---

## Task Planning

### Step 3.2: Generate Task Breakdown

**Input**: Operation type, research findings, CQ assessment

**Process**:
1. Decompose operation into discrete tasks
2. Identify dependencies between tasks
3. Assign completion criteria per task
4. Estimate effort/complexity

**Todo Structure**:
```json
{
  "todo_items": [
    {
      "id": "step_1",
      "description": "Clear, actionable step",
      "completion_criteria": "Specific validation criteria",
      "dependencies": ["prerequisite_step_ids"],
      "status": "pending"
    }
  ],
  "unclear_items": [
    {
      "id": "unclear_1",
      "description": "Ambiguous requirement",
      "impact": "How this affects execution",
      "resolution_needed": "What clarification is required"
    }
  ]
}
```

**Output**: TodoWrite-ready task breakdown


---

## Risk Assessment

### Step 3.3: Identify Risks

**Input**: Operation scope, file targets, integration points

**Risk Categories**:

| Category | Examples | Mitigation |
|----------|----------|------------|
| File modification | Overwriting existing content | Dry-run first, read-back verify |
| Path errors | Invalid paths, missing files | Validate all paths before write |
| Integration break | Breaking cross-references | Check dependencies before modify |
| Schema violation | Invalid output format | Validate against schema |

**Risk Scoring**:
- **High** (3): Could break ecosystem, data loss
- **Medium** (2): Degraded functionality, fixable
- **Low** (1): Minor issues, easily reversible

**Output**: Risk register with scores and mitigations

### Step 3.4: Define Rollback Strategy

**Input**: Identified risks, file targets

**Process**:
1. Document current state of target files
2. Define rollback steps for each risk
3. Identify point-of-no-return (if any)

**Output**: Rollback plan (or confirmation that operation is reversible)


---

## Quick Checklist

Before advancing to Phase 4 (ACT):

- [ ] Apply mode selected with rationale
- [ ] Task breakdown complete with dependencies
- [ ] All tasks have completion criteria
- [ ] Risks identified and scored
- [ ] Mitigations defined for high/medium risks
- [ ] Rollback strategy documented (if applicable)

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Skipping dry-run | Always dry-run first for new operations |
| Vague task descriptions | Each task must be specific and actionable |
| Missing dependencies | Map task ordering explicitly |
| Ignoring risks | Document at least 3 potential failure modes |

---

## Exit Criteria

**Plan approval required to proceed**

| Criterion | Weight | Check |
|-----------|--------|-------|
| Mode selected | 0.20 | dry_run or commit with rationale |
| Tasks defined | 0.30 | All steps with completion criteria |
| Dependencies mapped | 0.20 | Execution order clear |
| Risks assessed | 0.20 | High/medium risks mitigated |
| Rollback ready | 0.10 | Recovery plan documented |

---

## Reference Documentation

- [workflow-operations.md](../docs/workflow-operations.md) - Operation-specific task patterns
- [file-operation-protocol.md](../../../../docs/01-guides/file-ops/file-operation-protocol.md) - File operation rules
- [escalation-protocol.md](../../../../docs/00-core/escalation-protocol.md) - When to escalate

---

**Previous Phase**: [Phase 2: ORIENT](phase-2-orient.md)
**Next Phase**: [Phase 4: ACT](phase-4-act.md)
