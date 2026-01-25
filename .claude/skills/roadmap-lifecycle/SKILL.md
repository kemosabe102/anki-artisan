---
name: roadmap-lifecycle
description: >
  STRATEGIC stage-based project governance: determines current maturity stage 
  (MVP/Alpha/Beta/GA), assesses 9-dimension quality gaps, plans stage transitions
  with criteria-based progression, and enforces stage gate requirements.
  NOT for: sprint-level operations or capacity tracking (use managing-roadmaps),
  effort estimation (use estimating-and-tracking), generating ROADMAP.md files (use /roadmap command).
  Keywords: what stage, project maturity, advance to alpha, transition to beta, stage assessment.
---

# Roadmap Lifecycle Skill

*Stage-aware project lifecycle management with criteria-based progression*

## Quick Start

| User Says | Action |
|-----------|--------|
| "assess current stage" | Run Assess operation |
| "where are we in lifecycle" | Run Assess operation |
| "what stage is this project" | Run Assess operation |
| "generate roadmap for MVP" | Run Generate operation (stage-specific) |
| "plan transition to Alpha" | Run Advance operation |
| "what's needed for Beta" | Run Assess + show gap to Beta |
| "advance to GA" | Run Advance operation |

---

## Delegation Model: You Orchestrate, Agents Execute

**CRITICAL**: This skill is an ORCHESTRATOR. You do NOT edit files directly.

```
┌─────────────────────────────────────────────────────────────────┐
│  YOU (Skill)                      AGENTS (via Task)             │
│  ─────────────                    ─────────────────             │
│  • Guide the workflow             • Research project artifacts  │
│  • Make decisions                 • Validate stage gates        │
│  • Coordinate operations          • Create/update roadmaps      │
│  • Synthesize outputs             • Generate transition tasks   │
│  • Track progress                 • Research best practices     │
└─────────────────────────────────────────────────────────────────┘
```

### Delegation Rule (MANDATORY)

**ALL work requires Task() delegation. You coordinate, agents execute.**

| Operation | Delegate To | You NEVER Do |
|-----------|-------------|--------------|
| Gather project artifacts | `Task(researcher-codebase)` | Read files yourself |
| Validate stage gates | `Task(architectureer)` | Analyze quality yourself |
| Create/update roadmap | `Task(planning)` | Edit ROADMAP.md yourself |
| Generate transition tasks | `Task(planning)` | Write tasks yourself |
| Research best practices | `Task(researcher-external)` | WebSearch yourself |

See [delegation/patterns.md](delegation/patterns.md) for Task() templates.

---

## Operations (3)

| Operation | OODA Phase | Description | Output |
|-----------|------------|-------------|--------|
| **Assess** | OBSERVE | Determine current stage via 9-dimension scoring | Stage Assessment Report |
| **Generate** | ORIENT | Create stage-aware ROADMAP.md | Updated ROADMAP.md |
| **Advance** | DECIDE/ACT | Plan transition to next stage | Transition Checklist |

---

## Operation Details

### Assess Operation

**Trigger**: "assess", "current stage", "where are we", "lifecycle status"
**Workflow**: [phases/phase-1-assess.md](phases/phase-1-assess.md)
**Agents**: researcher-codebase, architectureer
**Output**: Stage Assessment Report with dimension scores and gaps

**Steps**:
1. Delegate artifact gathering to `researcher-codebase`
2. Delegate quality assessment to `architectureer`
3. Calculate dimension scores (9 dimensions)
4. Determine stage based on score thresholds
5. Identify gaps to next stage
6. Present findings for user confirmation

### Generate Operation

**Trigger**: "generate roadmap", "create roadmap", "roadmap for [stage]"
**Workflow**: [phases/phase-2-generate.md](phases/phase-2-generate.md)
**Agents**: planning
**Output**: Stage-aware ROADMAP.md

**Steps**:
1. Confirm current stage (via Assess if needed)
2. Delegate roadmap generation to `planning`
3. Validate generated roadmap structure
4. Present for user review

### Advance Operation

**Trigger**: "advance to", "transition to", "plan for [next stage]"
**Workflow**: [phases/phase-3-advance.md](phases/phase-3-advance.md)
**Agents**: planning
**Output**: Transition Checklist with remediation tasks

**Steps**:
1. Review current stage assessment
2. Identify exit criteria gaps for target stage
3. Delegate task creation to `planning`
4. Generate prioritized remediation checklist
5. Present transition plan for user approval

---

## Stage Scoring Quick Reference

| Stage | Score Range | Min Quality | Key Focus |
|-------|-------------|-------------|-----------|
| MVP | 1.0 - 3.4 | 3.5 overall | Speed & Feasibility |
| Alpha | 3.5 - 5.4 | 3.7 overall | Stabilize Core |
| Beta | 5.5 - 7.9 | 3.8 overall | Resilience & Scale |
| GA | 8.0 - 10.0 | 4.2 overall | Full Rigor |

See stage definitions: [stages/](stages/)

### 9-Dimension Scoring Model

| Dimension | MVP Weight | Alpha Weight | Beta Weight | GA Weight |
|-----------|------------|--------------|-------------|-----------|
| Testing | 0.08 | 0.10 | 0.12 | 0.15 |
| Documentation | 0.08 | 0.10 | 0.11 | 0.12 |
| Code Quality | 0.10 | 0.12 | 0.12 | 0.13 |
| Architecture | 0.12 | 0.12 | 0.11 | 0.10 |
| Security | 0.08 | 0.10 | 0.12 | 0.13 |
| Performance | 0.08 | 0.09 | 0.11 | 0.12 |
| Observability | 0.06 | 0.08 | 0.10 | 0.10 |
| Operational Readiness | 0.05 | 0.08 | 0.10 | 0.10 |
| Feature Completeness | 0.35 | 0.21 | 0.11 | 0.05 |

---

## Quality Gates

| Operation | Exit Gate | Confidence Required |
|-----------|-----------|---------------------|
| Assess | Dimension scores calculated | CQ >= 0.85 |
| Assess -> Generate | User confirms stage | User approval |
| Generate | ROADMAP.md valid | planning success |
| Generate -> Advance | User requests transition | User approval |
| Advance | Tasks created | planning success |

### Stage Transition Gates

| Transition | Required Score | Additional Criteria |
|------------|----------------|---------------------|
| MVP -> Alpha | >= 3.5 | Core functionality stable |
| Alpha -> Beta | >= 5.5 | No critical bugs, docs complete |
| Beta -> GA | >= 8.0 | Production-ready, SLAs defined |

---

## Integration Points

### With /roadmap Command

- `/roadmap assess` - Invokes Assess operation
- `/roadmap advance` - Invokes Advance operation
- `/roadmap [path] --stage=X` - Generate with stage context

### With Planning Workflow

```
Assess (current stage)
    │
    ▼
Generate (stage-aware roadmap)
    │
    ▼
Advance (identify gaps)
    │
    ▼
/spec (for complex gaps)
    │
    ▼
/plan -> /tasks -> /implement
```

### With Other Skills

| Skill | Integration |
|-------|-------------|
| `feature-design-workflow` | Stage informs design rigor level |
| `spec-generator` | Stage determines spec depth |
| `task-management` | Stage affects task prioritization |

---

## Anti-Patterns (NEVER DO)

- Read files directly (delegate to researcher-codebase)
- Score dimensions yourself (delegate to architectureer)
- Edit ROADMAP.md yourself (delegate to planning)
- Skip user confirmation on stage assessment
- Advance without completing exit criteria
- Assume stage without assessment
- Generate roadmap without knowing current stage
- Create transition tasks without gap analysis

---

## Error Recovery

| Error | Recovery | Framework |
|-------|----------|-----------|
| Artifacts not found | Ask user for project location | - |
| Score ambiguous | Present options, get user confirmation | Cynefin (navigate ambiguity) |
| Stage gate violation | Show gaps, suggest remediation | Pre-Mortem (identify blockers) |
| Roadmap conflict | Backup existing, generate fresh | - |
| Missing dimension data | Request additional context | - |
| Agent delegation fails | Retry once, escalate to user | - |
| Complex transition planning | Run Pre-Mortem before advancing | Pre-Mortem |
| Unclear goal alignment | Map to OKRs, validate priorities | OKR |

> **Tip**: For ambiguous situations, apply Cynefin to classify the problem domain before selecting recovery action.

---

## Phase Navigation

| Current | User Says | Navigate To |
|---------|-----------|-------------|
| Any | "assess stage" | Assess |
| Assess | "generate roadmap" | Generate |
| Generate | "plan transition" | Advance |
| Advance | "start over" | Assess |
| Any | "skip to [operation]" | Specified operation |

---

## State Management

Track progress through the workflow:

```python
roadmap_lifecycle_state = {
    "current_operation": "ASSESS",  # ASSESS | GENERATE | ADVANCE | COMPLETE
    "assessed_stage": None,  # MVP | ALPHA | BETA | GA
    "dimension_scores": {},  # 9-dimension scores
    "target_stage": None,  # Next stage for transition
    "gaps": [],  # List of identified gaps
    "transition_tasks": [],  # Generated remediation tasks
    "deliverables": []  # Output document paths
}
```

---

## Agent Delegation Matrix

| Operation | Agent | Purpose | Parallel? |
|-----------|-------|---------|-----------|
| Assess | `researcher-codebase` | Gather project artifacts | Yes |
| Assess | `architectureer` | Validate quality dimensions | No (after research) |
| Generate | `planning` | Create/update ROADMAP.md | No |
| Advance | `researcher-codebase` | Analyze gap details | Yes |
| Advance | `planning` | Generate remediation tasks | No (after analysis) |

**Parallel Legend**: Yes = can run in parallel | No = must run sequentially

---

## Success Criteria

The workflow is complete when:

- [ ] Stage accurately assessed with user confirmation
- [ ] Dimension scores calculated (9 dimensions)
- [ ] ROADMAP.md generated with stage-appropriate content
- [ ] Gaps to next stage identified
- [ ] Transition tasks created (if advancing)
- [ ] User approves final deliverables

---

## Documentation

| Topic | Document |
|-------|----------|
| MVP Stage | [stages/mvp-stage.md](stages/mvp-stage.md) |
| Alpha Stage | [stages/alpha-stage.md](stages/alpha-stage.md) |
| Beta Stage | [stages/beta-stage.md](stages/beta-stage.md) |
| GA Stage | [stages/ga-stage.md](stages/ga-stage.md) |
| Assess Workflow | [phases/phase-1-assess.md](phases/phase-1-assess.md) |
| Generate Workflow | [phases/phase-2-generate.md](phases/phase-2-generate.md) |
| Advance Workflow | [phases/phase-3-advance.md](phases/phase-3-advance.md) |
| Delegation Patterns | [delegation/patterns.md](delegation/patterns.md) |
| Assessment Template | [templates/stage-assessment.template.md](templates/stage-assessment.template.md) |
| Transition Template | [templates/transition-checklist.template.md](templates/transition-checklist.template.md) |
| Scoring Model | [docs/scoring-model.md](docs/scoring-model.md) |
| Stage Criteria | [docs/stage-criteria.md](docs/stage-criteria.md) |

---

## Thinking Frameworks

When facing complex roadmap challenges, these frameworks guide systematic problem-solving.

**Full Catalog**: [Thinking Frameworks README](../../docs/00-core/frameworks/README.md)

**Most Relevant for Roadmap Lifecycle**:

| Framework | When to Use |
|-----------|-------------|
| [OKR](../../docs/00-core/frameworks/strategy.md) | Goal alignment, quarterly planning |
| [Cynefin](../../docs/00-core/frameworks/strategy.md) | Navigating ambiguous project stages |
| [Pre-Mortem](../../docs/00-core/frameworks/strategy.md) | Risk identification before phase transitions |

> **Selection Tip**: goal setting->OKR, ambiguity->Cynefin, risk mitigation->Pre-Mortem
