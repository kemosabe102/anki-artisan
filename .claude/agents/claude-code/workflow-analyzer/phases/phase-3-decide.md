# Phase 3: DECIDE - Decision & Planning

**OODA Stage**: DECIDE | **Time Allocation**: 10-15%

**Purpose**: Determine workflow complexity, select analysis depth, plan validation sequence, assess parallelization opportunities

**Deliverable**: Analysis plan with depth selection and risk assessment

---

## Workflow Steps

### Step 3.1: Complexity Classification

**Input**: Findings from Phase 2

**Process**:
1. Count workflow dimensions:
   - Number of phases/steps
   - Number of Task() calls
   - Number of conditional branches
   - Number of gates
2. Calculate complexity score:

| Complexity | Steps | Task() Calls | Branches | Gates |
|------------|-------|--------------|----------|-------|
| **Simple** | 1-3 | 0-2 | 0 | 0-1 |
| **Moderate** | 4-7 | 3-5 | 1-2 | 2-3 |
| **Complex** | 8+ | 6+ | 3+ | 4+ |

**Output**: `{ complexity: "simple" | "moderate" | "complex", factors: object }`

### Step 3.2: Analysis Depth Selection

**Input**: Complexity classification, user request mode

**Process**:
Select analysis depth based on complexity and mode:

| Mode | Simple | Moderate | Complex |
|------|--------|----------|---------|
| VALIDATE | Quick check | Standard | Deep |
| ANALYZE | Standard | Deep | Exhaustive |
| OPTIMIZE | Standard + SCAMPER | Deep + SCAMPER | Exhaustive + SCAMPER |


**Depth Definitions**:
- **Quick**: Frontmatter + critical path only
- **Standard**: All 7 dimensions, basic scoring
- **Deep**: All dimensions + evidence + recommendations
- **Exhaustive**: Deep + pattern research + cross-references

**Output**: `{ depth: string, dimensions_to_check: string[] }`

### Step 3.3: Validation Sequence Planning

**Input**: Workflow structure, depth selection

**Process**:
1. Order dimensions by priority for this workflow:
   - If parallel operations: Parallelization Safety first
   - If many agents: Subagent Validation first
   - If multi-phase: State Management first
2. Plan gate checkpoints in analysis
3. Define early exit conditions (critical failures)

**Validation Order Template**:
```
1. Workflow Correctness (always first - blocks all else)
2. [Context-dependent priority]
3. [Context-dependent priority]
4. Integration Alignment (always last - depends on others)
```

**Output**: `{ validation_sequence: string[], early_exit_conditions: string[] }`

### Step 3.4: Parallelization Opportunity Assessment

**Input**: Workflow steps, current parallel groupings

**Process**:
1. Identify steps that could run in parallel
2. Check for shared state or dependencies
3. Calculate potential efficiency gain
4. Note current parallel/sequential classification

**Opportunity Criteria**:
- No shared file writes
- No output->input dependency
- No shared agent state
- Independent error handling

**Output**: `{ opportunities: Opportunity[], efficiency_potential: float }`


### Step 3.5: Risk Assessment

**Input**: All findings from Phase 1-2

**Process**:
Identify risks in workflow design:

| Risk Category | Indicators | Impact |
|---------------|------------|--------|
| Missing agents | Task() to non-existent agent | CRITICAL |
| Circular dependency | Cycle in step DAG | CRITICAL |
| Unsafe parallelization | Shared state in parallel | HIGH |
| Missing gates | No exit criteria at decision points | MEDIUM |
| Poor error handling | No retry/fallback defined | MEDIUM |
| Weak state management | No checkpoints in multi-phase | LOW |

**Output**: `{ risks: Risk[], critical_count: int, blocking: boolean }`

---

## Exit Criteria

**Plan required to proceed to ACT**

| Criterion | Weight | Check |
|-----------|--------|-------|
| Complexity classified | 0.25 | Simple/Moderate/Complex determined |
| Depth selected | 0.25 | Analysis depth matches complexity |
| Sequence planned | 0.25 | Validation order defined |
| Risks assessed | 0.25 | Risk register populated |

**Blocking**: If critical_count > 0, report immediately before full analysis.

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Wrong depth for complexity | Match depth to complexity level |
| Ignoring critical risks | Report CRITICAL risks immediately |
| Static validation order | Adapt order to workflow characteristics |
| Skipping parallelization check | Always assess parallel opportunities |

---

**Previous Phase**: [Phase 2: ORIENT](phase-2-orient.md)
**Next Phase**: [Phase 4: ACT](phase-4-act.md)
