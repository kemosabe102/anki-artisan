# Orchestrator Thresholds

**Purpose**: Single source of truth for all quantitative thresholds used in orchestration decisions.

---

## Threshold Reference Table

| Metric | Threshold | Action |
|--------|-----------|--------|
| **CQ (Context Quality)** | >=0.85 | Proceed to DECIDE |
| **CQ** | <0.85 | Research first (max 3 iterations) |
| **CQ** | <0.70 | Spawn exploration agents |
| **ASC (Agent Selection)** | >=0.80 | Use ALL agents >=0.80 (max 5) |
| **ASC** | 0.50-0.79 | Use highest confidence agent |
| **ASC** | <0.50 | ESCALATE to user, recommend agent creation |
| **DCS (Delegation)** | >=0.70 | MUST delegate |
| **DCS** | 0.50-0.69 | SHOULD delegate |
| **DCS** | <0.50 | ESCALATE to user |
| **Consensus** | +/-0.10 | Strong consensus |
| **Conflict** | >0.30 | Escalate to user |
| **Synthesis Overlap** | >0.70 | Trigger synthesis framework |

---

## Formulas

### Context Quality (CQ)
```
CQ = (Domain × 0.4) + (Pattern × 0.3) + (Dependency × 0.2) + (Risk × 0.1)
```

**Factors**:
- **Domain**: How well the orchestrator understands the problem domain
- **Pattern**: Recognition of similar past problems/solutions
- **Dependency**: Understanding of code/system dependencies
- **Risk**: Assessment of potential impact

### Agent Selection Confidence (ASC)
```
ASC = (Domain × 0.60) + (Work_Type × 0.30) + (Track_Record × 0.10)
```

**Factors**:
- **Domain**: Agent's expertise match to task domain
- **Work_Type**: Match between task type (create/review/debug) and agent capabilities
- **Track_Record**: Historical success rate of agent on similar tasks



### Delegation Confidence Score (DCS)
```
DCS = (Task_Complexity × 0.40) + (Agent_Fit × 0.30) + (CQ × 0.20) + (Cost_Benefit × 0.10)
```

**Factors**:
- **Task_Complexity**: How complex is the task (simple lookup vs. multi-file refactor)
- **Agent_Fit**: How well the best available agent matches the task
- **CQ**: Current context quality score
- **Cost_Benefit**: Token/time cost of delegation vs. direct execution

---

## CQ Consolidation (Multi-Agent ORIENT)

When multiple agents contribute to context gathering:

```
Consolidated_CQ = (CRA × 0.50) + (Domain_Specialists_Avg × 0.35) + (Researcher_Lead × 0.15)
```

**Weights**:
- **context-readiness-assessor (CRA)**: 0.50 - Primary assessment weight
- **Domain specialists average**: 0.35 - Combined domain expertise
- **researcher-lead**: 0.15 - Research coordination contribution

---

## Quick Reference

**Gates**:
- CQ >= 0.85: Proceed
- CQ < 0.70: More research needed
- ASC >= 0.80: High-confidence delegation
- ASC < 0.50: Escalate to user

**See also**: `.claude/docs/01-guides/orchestration/orient-research-coordination.md`

---

## ICE Score Thresholds

ICE Score = Impact × Confidence × Ease (each factor 1-10, total 1-1000)

### Priority Classification

| ICE Score | Priority | Phase Assignment | Action |
|-----------|----------|------------------|--------|
| >= 500 | High | Build Phase 1 | Schedule immediately |
| 300-499 | Medium | Build Phase 1-2 | Plan for current/next sprint |
| 200-299 | Lower | Build Phase 2+ | Plan for future sprint |
| < 200 | Backlog | Defer | User confirmation required |

### Quality Gate

| Threshold | Gate | Action |
|-----------|------|--------|
| ICE < 200 | WARN | Recommend backlog, require user override |
| ICE >= 500 | PASS | Auto-approve for Phase 1 |

### Factor Scales

| Factor | Question | Scale |
|--------|----------|-------|
| **Impact** | How much does this move the needle? | 1-10 |
| **Confidence** | How confident are we it will work? | 1-10 |
| **Ease** | How easy is it to build? | 1-10 |

### Usage

Reference this section from commands/skills that use ICE scoring:
- `/roadmap` - Feature prioritization
- `/spec` - Feature validation
- `validating-specifications` skill - Spec quality assessment
