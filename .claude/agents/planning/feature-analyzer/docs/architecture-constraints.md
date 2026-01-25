# Architecture Constraint Enforcement

## Framework Integration

This document supports **Phase 7 (ACT - Validation)** of the agent workflow.

**Primary Framework**: Pre-Mortem - Anticipate how recommendation could fail
**Secondary Framework**: Cynefin - Re-assess complexity after analysis

**Tool Sequence**: Read SPEC.md -> Check constraints -> Apply Pre-Mortem -> Calculate alignment -> Perplexity (if unclear)

---

## Pre-Mortem Validation

**Before finalizing recommendation, apply Pre-Mortem:**

"Assume this [MERGE/SEPARATE/REFACTOR] recommendation failed in 6 months. What went wrong?"

### Failure Mode Checklist

| Failure Mode | Check | Mitigation If Found |
|--------------|-------|---------------------|
| Scope creep | Did combined feature exceed 70 FR limit? | Split into sub-features |
| Integration complexity | Does architecture require >3 new interfaces? | Simplify or phase implementation |
| Team friction | Do distinct teams need to merge codebases? | Define clear ownership boundaries |
| Performance degradation | Does combined feature have conflicting NFRs? | Separate hot paths |
| Maintenance burden | Does separation create duplicate code? | Extract shared library |

### Pre-Mortem Output
```json
{
  "pre_mortem_risks": [
    "Risk 1: [Description] - Mitigation: [Action]",
    "Risk 2: [Description] - Mitigation: [Action]",
    "Risk 3: [Description] - Mitigation: [Action]"
  ],
  "residual_risk_level": "low|medium|high"
}
```

---

## Constraint 1: Hook Isolation

**Rule**: Hooks cannot access agent reasoning or modify agent state

| Status | Condition |
|--------|-----------|
| VIOLATION | Features proposing hook-based decision logic or reasoning |
| ALIGNED | Hooks limited to pre/post-processing, validation, monitoring |

**Directive Steps**:
1. List all hooks mentioned in both specs
2. Check each hook for: state modification, reasoning access, cross-agent calls
3. IF violation found -> Document in `alignment_assessment.risks[]`
4. IF unclear about hook behavior -> `mcp__perplexity__search("best practices for [hook type] isolation")`

**Pass/Fail Criteria**:
- PASS: All hooks are pure (input -> output, no side effects)
- FAIL: Any hook modifies agent state or accesses reasoning

**Example Violation**: "Checkpoint hook analyzes context to decide when to checkpoint"
**Example Aligned**: "Checkpoint hook executes orchestrator's checkpoint decision"
**Mitigation**: Move decision logic to orchestrator, hook executes only

---

## Constraint 2: Context Offloading

**Rule**: 10:1 compression for context management

| Status | Condition |
|--------|-----------|
| RED FLAG | Features adding >1K tokens without 10:1 compression |
| CAUTION | Features adding 500-1K tokens with <5:1 compression |
| ALIGNED | Features adding <500 tokens OR providing >10:1 compression |

**Directive Steps**:
1. Estimate combined feature's context size (FR count x 50 tokens average)
2. Check for context offloading strategy (external docs, schemas, references)
3. Calculate compression: `external_tokens / total_tokens`
4. IF compression < 10:1 -> Document in risks with remediation

**Pass/Fail Criteria**:
- PASS: Compression ratio >= 10:1
- WARN: Compression ratio 5:1 to 10:1 (document improvement plan)
- FAIL: Compression ratio < 5:1

**Calculation**: `context_impact = (merged_feature_FRs x 50 tokens/FR) - compression_benefit`

**Example Violation**: 120-FR merge adds 6K tokens, no compression
**Mitigation**: Extract compression layer OR separate to reduce context

---

## Constraint 3: No Unjustified State Machines

**Rule**: Code-based state machines require explicit justification

| Status | Condition |
|--------|-----------|
| VIOLATION | Explicit FSM code (switch statements, state enums) without justification |
| JUSTIFIED | Workflow phase tracking (limited states: pending/in_progress/completed) |
| PREFERRED | Conversation-based state management via prompt/response |

**Directive Steps**:
1. Search specs for state machine patterns: "state:", "transition:", "FSM", "workflow states"
2. For each state machine, check for justification (why not simpler approach)
3. IF no justification -> Document as risk

**Pass/Fail Criteria**:
- PASS: No state machines OR all justified
- WARN: State machines without clear justification

**Example Violation**: "15-state FSM for checkpoint lifecycle"
**Example Justified**: "3-state phase tracker (pending/active/done)"
**Mitigation**: Justify necessity OR recommend conversation-based alternative

---

## Constraint 4: Simplicity First

**Rule**: Maximum 70 functional requirements per feature

| Status | Condition |
|--------|-----------|
| VIOLATION | Merged feature exceeds 70 FRs |
| VIOLATION | Refactored foundation has >3 shared dependencies |
| ALIGNED | Clear boundaries, single responsibilities |

**Directive Steps**:
1. Count FRs in each spec: `Grep("^FR-|^- FR|functional requirement")`
2. IF MERGE: Sum FR counts from both specs
3. IF combined > 70 -> FAIL or require scope reduction
4. Check for complexity indicators: deep nesting, many integrations, >10 entities

**Pass/Fail Criteria**:
- PASS: FR count <= 70 AND complexity indicators <= 3
- WARN: FR count 50-70 OR complexity indicators 3-5
- FAIL: FR count > 70 OR complexity indicators > 5

---

## System Goals Alignment (from SPEC.md)

**Directive Steps**:
1. `Read("docs/00-project/SPEC.md")` - Extract system goals
2. For each goal, assess recommendation alignment
3. Score: aligned (1.0), partial (0.5), misaligned (0.0)
4. Calculate overall: `sum(goal_scores) / goal_count`

**Goal Assessment Template**:

| Goal | Recommendation Impact | Score | Rationale |
|------|----------------------|-------|-----------|
| Simplicity First | Supports/Neutral/Hinders | 0.0-1.0 | [Why] |
| Confidence-Based Decisions | Supports/Neutral/Hinders | 0.0-1.0 | [Why] |
| Context Offloading | Supports/Neutral/Hinders | 0.0-1.0 | [Why] |
| Operational Reliability | Supports/Neutral/Hinders | 0.0-1.0 | [Why] |
| Continuous Learning | Supports/Neutral/Hinders | 0.0-1.0 | [Why] |

**5 System Goals**:
1. **Simplicity First** - Start simple, add complexity only when proven necessary
2. **Confidence-Based Decisions** - Quantify uncertainty, act on thresholds
3. **Context Offloading** - Move complexity from orchestrator to sub-agents
4. **Operational Reliability** - Graceful degradation, recovery paths
5. **Continuous Learning** - Improve from feedback, track patterns

**IF SPEC.md unavailable**:
- Set `alignment_assessment.overall_alignment_score = null`
- Add to risks: "System goals not validated - SPEC.md inaccessible"
- Reduce confidence by 0.10

---

## Overall Alignment Score

**Formula**:
```
alignment_score = (
  constraint_pass_rate x 0.40 +
  goal_alignment_avg x 0.40 +
  pre_mortem_residual_risk x 0.20
)
```

**Where**:
- `constraint_pass_rate` = (constraints passed / 4)
- `goal_alignment_avg` = average of goal scores
- `pre_mortem_residual_risk` = 1.0 (low), 0.7 (medium), 0.3 (high)

**Thresholds**:

| Score | Status | Action |
|-------|--------|--------|
| >= 0.85 | Strong Alignment | Proceed with confidence |
| 0.70-0.84 | Partial Alignment | Proceed with documented risks |
| < 0.70 | Weak Alignment | Reconsider recommendation or add mitigations |

---

## Enforcement Protocol

1. **Check** all 4 constraints using directive steps
2. **Assess** goal alignment using Goal Assessment Template
3. **Apply** Pre-Mortem to identify failure modes
4. **Calculate** overall alignment score using formula
5. **Document** violations in `alignment_assessment.risks`
6. **Mitigate** each violation with specific recommendation
7. **Override** if score < 0.70 (reconsider recommendation)

---

## Constraint Summary Table

| Constraint | Pass Threshold | Impact on Score |
|------------|----------------|-----------------|
| Hook Isolation | All hooks pure | -0.25 per violation |
| Context Offloading | >= 10:1 compression | -0.20 per violation |
| No Unjustified FSM | All FSMs justified | -0.15 per violation |
| Simplicity First | <= 70 FRs | -0.25 per violation |
