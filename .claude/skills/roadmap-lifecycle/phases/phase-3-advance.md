# Phase 3: ADVANCE - Stage Transition Planning

**OODA Phase**: DECIDE → ACT
**Operation**: Advance
**Purpose**: Plan and track transition from current stage to next stage

---

## Overview

The Advance operation analyzes the gap between current state and next stage requirements, generates remediation tasks, and creates a transition checklist.

**Input**: 
- Current stage (from Assess or user input)
- Target stage (typically next stage: MVP→Alpha, Alpha→Beta, etc.)
- Assessment results (if available from prior Assess)

**Output**: Transition Checklist (see `templates/transition-checklist.template.md`)

---

## Prerequisites

Before running Advance:
- [ ] Current stage known
- [ ] Target stage confirmed (usually next in sequence)
- [ ] Assessment results available (recommended) or will gather fresh

---

## Workflow Steps

### Step 3.1: Load Stage Criteria

**Action**: Load exit and entry criteria from stage definitions

**Sources**:
- `stages/{current_stage}-stage.md` → Exit Criteria
- `stages/{target_stage}-stage.md` → Entry Criteria

```python
transition_criteria = {
    "exit_criteria": [...],  # From current stage
    "entry_criteria": [...],  # From target stage
    "quality_delta": {
        "overall": target_min - current_min,
        "by_dimension": {...}
    }
}
```

---

### Step 3.2: Assess Current Completion

**Option A**: Use existing assessment (if recent)
- Load from prior Assess operation results
- Verify assessment is still current (<7 days old)

**Option B**: Gather fresh data
- Delegate to `researcher-codebase` for current state
- Quick validation against exit criteria

**For each exit criterion**:
```python
def check_criterion(criterion, project_state):
    # Check if criterion is met
    evidence = find_evidence(criterion, project_state)
    if evidence:
        return {"status": "✅", "evidence": evidence}
    else:
        return {"status": "❌", "gap": criterion.requirement}
```

---

### Step 3.3: Identify Gaps

**Logic** (skill performs):

```python
gaps = []

# Check exit criteria
for criterion in exit_criteria:
    if not criterion.met:
        gaps.append({
            "type": "exit_criterion",
            "criterion": criterion.description,
            "current": criterion.current_state,
            "required": criterion.requirement,
            "priority": criterion.priority
        })

# Check quality dimension gaps
for dimension, scores in dimension_scores.items():
    gap = target_scores[dimension] - scores.current
    if gap > 0:
        gaps.append({
            "type": "quality_dimension",
            "dimension": dimension,
            "current": scores.current,
            "target": target_scores[dimension],
            "gap": gap,
            "priority": "critical" if gap > 2 else "standard"
        })
```

**Priority Classification**:
- **Critical**: Must address before transition (exit criteria, large gaps)
- **Standard**: Should address for smooth transition
- **Nice-to-have**: Would improve transition but not blocking

---

### Step 3.4: Generate Remediation Tasks

**Delegate to**: `planning`
**Execution**: Sequential

**For each gap, generate task with**:
- Clear description (actionable)
- Acceptance criteria (testable)
- Effort estimate (S/M/L)
- Dependencies
- Recommended agent for implementation

**Group into work streams** (max 5):

| Stream | Focus | Example Tasks |
|--------|-------|---------------|
| Infrastructure | Deployment, CI/CD | Add staging env, set up CD |
| Quality | Testing, coverage | Add integration tests, increase coverage |
| Security | Auth, compliance | Add security scans, secrets management |
| Operations | Monitoring, docs | Set up logging, write runbooks |
| Features | Core functionality | Complete critical features |

---

### Step 3.5: Determine Execution Order

**Logic** (skill performs):

```python
def order_tasks(tasks):
    # Build dependency graph
    graph = build_dependency_graph(tasks)
    
    # Topological sort for execution order
    ordered = topological_sort(graph)
    
    # Identify parallel opportunities
    parallel_groups = find_independent_groups(ordered)
    
    return {
        "sequence": ordered,
        "parallel_groups": parallel_groups
    }
```

**Parallel Opportunities**:
- Tasks with no dependencies on each other
- Different work streams that don't conflict
- Read-only analysis tasks

---

### Step 3.6: Create Transition Checklist

**Output**: Transition Checklist document

Use template: `templates/transition-checklist.template.md`

Fill sections:
- Transition overview (stages, completion %, effort)
- Exit criteria with status
- Entry criteria with evidence requirements
- Work streams with tasks
- Execution order and parallel opportunities
- Validation plan
- Approval requirements

---

### Step 3.7: Integration with Planning Workflow

**For complex gaps**, integrate with /spec workflow:

```
Identified Gap
    ↓
Is gap complex? (requires design)
    ├─ Yes → /spec [gap-feature]
    │         ↓
    │        /plan
    │         ↓
    │        /tasks
    │         ↓
    │        /implement
    │
    └─ No → Direct task in transition checklist
```

**Complexity indicators**:
- Requires architectural changes
- Affects multiple components
- Needs external research
- Estimated effort > M

---

### Step 3.8: Present to User

**Output summary**:
```
Transition Plan: {current_stage} → {target_stage}

Exit Criteria: {exit_met}/{exit_total} complete ({exit_percent}%)
Tasks Generated: {task_count}
Estimated Effort: {total_effort}

Work Streams:
1. {stream_1}: {task_count_1} tasks
2. {stream_2}: {task_count_2} tasks
...

Output: {checklist_path}

Ready to begin transition? (Yes / Modify / Re-assess)
```

---

## Quick Checklist

- [ ] Exit criteria loaded from current stage
- [ ] Entry criteria loaded from target stage
- [ ] Current completion assessed
- [ ] Gaps identified and prioritized
- [ ] Remediation tasks generated
- [ ] Execution order determined
- [ ] Transition checklist created
- [ ] Complex gaps routed to /spec workflow

---

## Exit Criteria

Phase 3 complete when:
- Transition checklist created with all sections
- All gaps have remediation tasks
- Execution order determined
- User reviewed and accepted plan

---

## Error Handling

| Error | Recovery |
|-------|----------|
| No gaps found | Confirm ready for transition, verify assessment |
| Too many gaps (>20) | Prioritize critical only, defer others |
| Circular dependencies | Flag to user, suggest breaking points |
| planning fails | Generate simplified task list manually |

---

## Post-Transition Actions

After transition tasks complete:

1. **Re-assess**: Run Assess to confirm new stage
2. **Update artifacts**:
   - PROJECT-SPEC.md stage field
   - ROADMAP.md stage milestone
3. **Archive checklist**: Move to completed transitions
4. **Communicate**: Announce stage transition to stakeholders

---

## Stage Transition Approval Matrix

| Transition | Approvers Required |
|------------|-------------------|
| MVP → Alpha | Technical Lead, Product Owner |
| Alpha → Beta | Architecture Review Board |
| Beta → GA | ARB + Product Management |
| GA → Next Release | Executive Sponsor + Operations |

---

## Previous/Next Phases

- **Previous**: [phase-2-generate.md](phase-2-generate.md) (Generate roadmap)
- **Previous**: [phase-1-assess.md](phase-1-assess.md) (Assess stage)
- **After Transition**: Return to phase-1-assess.md to confirm new stage
