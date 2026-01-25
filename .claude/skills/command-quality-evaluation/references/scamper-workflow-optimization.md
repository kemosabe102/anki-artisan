# SCAMPER Workflow Optimization

Creative problem-solving framework applied to slash command workflow optimization.

---

## Purpose

Generate optimization candidates for command workflows using the 7 SCAMPER techniques, then rank by weighted criteria.

---

## The 7 SCAMPER Techniques

| Letter | Technique | Question for Commands |
|--------|-----------|----------------------|
| **S** | Substitute | What phases/agents can be replaced? |
| **C** | Combine | What phases can be merged? |
| **A** | Adapt | What patterns from other commands apply? |
| **M** | Modify | What can be scaled up/down/changed? |
| **P** | Put to other use | Can this workflow serve other purposes? |
| **E** | Eliminate | What phases/steps can be removed? |
| **R** | Reverse/Rearrange | What if we reorder the workflow? |

---

## Application to Command Workflows

### Substitute

**Question**: What agents or phases can be replaced with better alternatives?

**Applications**:
- Replace slow agent with faster specialist
- Substitute sequential phases with parallel execution
- Replace manual gate with automated validation
- Swap heavy model (opus) for lighter (sonnet) where appropriate

**Example**:
```
Before: Task(general-researcher, "Analyze codebase patterns")
After:  Task(researcher-codebase, "Analyze patterns") // Specialist agent
```

### Combine

**Question**: What phases or operations can be merged?

**Applications**:
- Merge validation phases into single pass
- Combine related agent tasks into one delegation
- Unify error handling across phases
- Consolidate similar output formats

**Example**:
```
Before: P1:VALIDATE_SYNTAX -> P2:VALIDATE_SCHEMA -> P3:VALIDATE_DEPS
After:  P1:VALIDATE_ALL (single validation agent)
```


### Adapt

**Question**: What patterns from other successful commands apply here?

**Applications**:
- Borrow multi-agent pattern from analyze-agent
- Apply progressive disclosure from review command
- Use error code pattern from git command
- Adapt gate structure from spec command

**Example**:
```
Before: Ad-hoc error messages
After:  Structured error codes (adapted from /analyze-agent)
        | Code | Meaning | Recovery |
        |------|---------|----------|
        | CMD_ERR_001 | Not found | Suggest alternatives |
```

### Modify

**Question**: What can be scaled, expanded, or adjusted?

**Applications**:
- Increase parallelization (2 agents -> 4 agents)
- Reduce timeout for fast-fail
- Expand output detail levels
- Adjust confidence thresholds

**Example**:
```
Before: Gate: confidence >= 0.9 (too strict, frequent failures)
After:  Gate: confidence >= 0.75 (balanced threshold)
```


### Put to Other Use

**Question**: Can this workflow serve additional purposes?

**Applications**:
- Extend analysis command to support batch mode
- Repurpose validation workflow for CI integration
- Use command output as input to another command
- Enable command as skill for other agents

**Example**:
```
Before: /analyze-agent researcher-codebase (single agent)
After:  /analyze-agent --all (batch mode, ecosystem analysis)
```

### Eliminate

**Question**: What phases or complexity can be removed?

**Applications**:
- Remove redundant validation (already done upstream)
- Eliminate unused agent in delegation
- Remove over-complicated gate conditions
- Strip unnecessary output fields

**Example**:
```
Before: 9 phases with 5 conditional branches
After:  6 phases with 2 conditional branches (cleaner flow)
```


### Reverse/Rearrange

**Question**: What if we reorder the workflow?

**Applications**:
- Move validation earlier (fail-fast)
- Defer expensive operations until needed
- Reverse dependency order for efficiency
- Rearrange output for progressive disclosure

**Example**:
```
Before: P1:COLLECT -> P2:VALIDATE -> P3:ANALYZE (late validation)
After:  P1:VALIDATE -> P2:COLLECT -> P3:ANALYZE (fail-fast)
```

---

## Optimization Ranking Criteria

After generating candidates, rank by weighted score:

| Criterion | Weight | Question |
|-----------|--------|----------|
| **Minimality** | 40% | Is this the smallest possible change? |
| **Risk** | 35% | What could go wrong? (lower = better) |
| **Maintainability** | 25% | Will future maintainers understand this? |

### Scoring Scale

- **Minimality**: 0.0 (massive change) to 1.0 (single-line change)
- **Risk**: 0.0 (high risk) to 1.0 (no risk)
- **Maintainability**: 0.0 (obscure) to 1.0 (crystal clear)


### Score Calculation

```
Final_Score = (Minimality x 0.40) + ((1 - Risk) x 0.35) + (Maintainability x 0.25)
```

Note: Risk is inverted because lower risk is better.

---

## Output Format

```json
{
  "command": "/analyze-agent",
  "candidates": [
    {
      "approach": "Combine P1+P2 validation phases",
      "technique": "Combine",
      "minimality": 0.7,
      "risk": 0.2,
      "maintainability": 0.9,
      "score": 0.785,
      "implementation": "Merge validate-syntax and validate-schema into single phase"
    },
    {
      "approach": "Move validation before collection",
      "technique": "Reverse",
      "minimality": 0.9,
      "risk": 0.1,
      "maintainability": 0.95,
      "score": 0.913,
      "implementation": "Swap P1:COLLECT and P0:VALIDATE order"
    }
  ],
  "recommended": "Move validation before collection"
}
```


---

## Technique Selection Guide

| Symptom | Recommended Techniques |
|---------|----------------------|
| Too many phases | Combine, Eliminate |
| Slow execution | Substitute, Modify (parallelize) |
| Frequent failures | Reverse (fail-fast), Modify (thresholds) |
| Hard to maintain | Adapt (proven patterns), Eliminate |
| Limited reusability | Put to Other Use, Adapt |
| Complex dependencies | Reverse, Combine |

---

## Workflow Optimization Process

1. **Identify Pain Points**: What's slow, brittle, or confusing?
2. **Apply SCAMPER**: Generate 2-3 candidates per technique
3. **Score Candidates**: Use Minimality/Risk/Maintainability weights
4. **Select Top 3**: Highest scoring candidates
5. **Validate**: Check against workflow-patterns-checklist
6. **Implement**: Apply changes incrementally

---

## Integration with Quality Matrix

SCAMPER optimizations target specific quality criteria:

| Technique | Primary Criteria Improved |
|-----------|--------------------------|
| Substitute | Subagent Validity, Tool Permissions |
| Combine | Workflow Correctness, State Management |
| Adapt | Error Recovery, Documentation |
| Modify | Gate Coverage, Parallelization Safety |
| Put to Other Use | Orchestrator Integration |
| Eliminate | Workflow Correctness, Maintainability |
| Reverse | Workflow Correctness, Error Recovery |
