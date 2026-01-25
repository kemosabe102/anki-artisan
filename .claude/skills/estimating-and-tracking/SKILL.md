---
name: estimating-and-tracking
description: >
  Use this skill when estimating effort, calibrating velocity, tracking
  burn-down/burn-up, or applying estimation techniques. Covers story points,
  three-point estimation (O/L/P), planning poker, and velocity calibration.
  Integrates with managing-roadmaps sprint capacity (37h/sprint).
  NOT for: task breakdown (use generating-tasks), sprint operations (use
  managing-roadmaps), timeline realism scoring (use assessing-business-alignment).
  Keywords: estimation, velocity, burn-down, story points, planning poker.
---

# Estimating and Tracking

*Effort estimation techniques, velocity calibration, and progress tracking*

---

## Contents

1. [Estimation Techniques Matrix](#estimation-techniques-matrix)
2. [Story Points Framework](#story-points-framework)
3. [Three-Point Estimation](#three-point-estimation)
4. [Planning Poker](#planning-poker)
5. [Velocity Calculation](#velocity-calculation)
6. [Velocity Calibration](#velocity-calibration)
7. [Burn-Down & Burn-Up Charts](#burn-down--burn-up-charts)
8. [Capacity Planning Integration](#capacity-planning-integration)
9. [Estimation Accuracy Tracking](#estimation-accuracy-tracking)
10. [Re-Estimation Triggers](#re-estimation-triggers)
11. [Relationship to Other Skills](#relationship-to-other-skills)
12. [Anti-Patterns](#anti-patterns-never-do)
13. [Quick Reference](#quick-reference)

---

## Estimation Techniques Matrix

| Technique | Best For | Accuracy | Effort |
|-----------|----------|----------|--------|
| **Story Points** | Relative sizing, sprint planning | Medium-High | Low |
| **Three-Point** | Uncertain scope, risk quantification | High | Medium |
| **T-Shirt Sizing** | Quick prioritization, roadmaps | Low-Medium | Very Low |
| **Planning Poker** | Team consensus, diverse perspectives | Medium-High | Medium |
| **Historical Comparison** | Repeat work, similar tasks | High | Low |

### Technique Selection Guide

| Context | Recommended Technique |
|---------|----------------------|
| Sprint planning | Story Points + Planning Poker |
| Quarterly roadmap | T-Shirt Sizing |
| High-risk features | Three-Point Estimation |
| Repeated work | Historical Comparison |
| New domain (unfamiliar) | Planning Poker + spike first |

---

## Story Points Framework

### Fibonacci Scale with Reference Stories

| Points | Complexity | Example Reference |
|--------|------------|-------------------|
| **1** | Trivial | Fix typo, update config value |
| **2** | Simple | Add validation rule, simple UI tweak |
| **3** | Moderate | New API endpoint (CRUD), form field |
| **5** | Complex | Feature with multiple components |
| **8** | Large | Cross-system integration |
| **13** | Very Large | Major feature, consider splitting |
| **21+** | Epic | Must be decomposed before sprint |

### Estimation Factors

When sizing, consider:

| Factor | Lower Estimate | Higher Estimate |
|--------|---------------|-----------------|
| Familiarity | Done this before | First time |
| Dependencies | Self-contained | External APIs/teams |
| Testing | Well-defined cases | Edge case exploration |
| Risk | Known technology | New library/pattern |
| Scope clarity | Clear requirements | Ambiguous needs |

### The Cone of Uncertainty

| Project Phase | Estimate Range |
|---------------|----------------|
| Initial concept | 0.25x - 4x |
| Approved spec | 0.5x - 2x |
| Design complete | 0.8x - 1.25x |
| Code complete | 0.9x - 1.1x |

**Key Insight**: Estimates improve as you learn more. Re-estimate at phase transitions.

---

## Three-Point Estimation

### Formula (PERT)

```
Expected = (Optimistic + 4×Most_Likely + Pessimistic) / 6
Standard_Deviation = (Pessimistic - Optimistic) / 6
```

### Example

| Task | O | M | P | Expected | SD |
|------|---|---|---|----------|-----|
| Auth integration | 3h | 5h | 12h | 5.8h | 1.5h |
| UI component | 2h | 4h | 6h | 4h | 0.67h |

### Confidence Intervals

| Confidence | Formula |
|------------|---------|
| 68% | Expected ± 1 SD |
| 95% | Expected ± 2 SD |
| 99.7% | Expected ± 3 SD |

### When to Use Three-Point

- High uncertainty tasks
- Stakeholder deadline commitments
- Risk quantification needed
- Budget/resource planning

---

## Planning Poker

### Facilitation Rules

1. **Present item**: PO/author explains the story (2 min max)
2. **Q&A**: Team asks clarifying questions (3 min max)
3. **Private vote**: Everyone selects a card, keeps hidden
4. **Reveal**: All cards shown simultaneously
5. **Discuss**: If spread >2 levels, high/low explain reasoning
6. **Re-vote**: Repeat until consensus (max 3 rounds)
7. **Record**: Log final estimate with any notes


### Card Values

Standard deck: 0, 1, 2, 3, 5, 8, 13, 21, ?, ☕

- **?** = "I need more information"
- **☕** = "I need a break" or "Too complex to estimate"

### Handling Disagreement

| Spread | Action |
|--------|--------|
| 1 level (e.g., 5 vs 8) | Take higher, note concern |
| 2 levels (e.g., 3 vs 8) | Discuss, re-vote once |
| 3+ levels | Spike needed, defer estimate |

---

## Velocity Calculation

### Basic Formula

```
Velocity = Sum of story points completed in sprint
```

### Rolling Average (Recommended)

```
Velocity_avg = (V_sprint-1 + V_sprint-2 + V_sprint-3) / 3
```

Use 3-sprint rolling average for stability. First 3 sprints are "learning period."

### Velocity Factors

| Factor | Adjustment |
|--------|------------|
| Team member added | -20% for 2 sprints |
| Team member left | -15% for 1 sprint |
| Holiday/PTO | Pro-rate capacity |
| New technology | -30% initially |
| Technical debt sprint | Velocity not applicable |

---

## Velocity Calibration

### Healthy Velocity Patterns

| Pattern | Interpretation | Action |
|---------|----------------|--------|
| Stable (±15%) | Well-calibrated team | Maintain |
| Increasing | Team improving, or inflation | Audit estimates |
| Decreasing | Burnout, scope creep, or debt | Investigate |
| Erratic (±40%) | Poor estimation or external factors | Improve process |

### Calibration Techniques

1. **Reference story anchoring**: Keep 1-2 reference stories per point level
2. **Retrospective review**: Compare actual vs estimated each sprint
3. **Cross-team calibration**: Periodically sync with other teams
4. **Estimate decay**: Re-estimate items >2 sprints old

### First 3 Sprints (Learning Period)

| Sprint | Expectation |
|--------|-------------|
| Sprint 1 | Establish baseline (may miss target) |
| Sprint 2 | Adjust based on learnings |
| Sprint 3 | Velocity stabilizing |
| Sprint 4+ | Use rolling average for planning |

---

## Burn-Down & Burn-Up Charts

### Burn-Down Chart

Tracks remaining work over time.

```
Points
Remaining
   |  ╲ Ideal
   |   ╲
   |    ╲____  Actual
   |         ╲
   +----------→ Time
   Day 1    Day N
```

### Interpretation Patterns

| Pattern | Meaning | Action |
|---------|---------|--------|
| Tracking ideal | On track | Continue |
| Above ideal (flat) | Behind, blockers | Investigate, reduce scope |
| Below ideal | Ahead | Verify quality, pull forward |
| Late drop | Last-minute push | Unsustainable, adjust process |
| Steps (flat then drop) | Large items, poor breakdown | Smaller stories |

### Burn-Up Chart (Preferred for Scope Changes)

Shows completed work + total scope over time.

```
Points
   |        ___Total Scope
   |   ____/
   |  /    ___Completed
   | /____/
   +----------→ Time
```

**Advantage**: Scope changes are visible (total line moves).

---

## Capacity Planning Integration

### Integration with managing-roadmaps

This skill's velocity feeds into `managing-roadmaps` sprint capacity model:

| managing-roadmaps | This Skill Provides |
|-------------------|---------------------|
| 3+2 streams model (37h/sprint) | Velocity → story points per sprint |
| Sprint allocation | Historical velocity for forecasting |
| Capacity validation | Velocity variance for buffer |

### Capacity Calculation

```
Available_Capacity = Team_Size × Sprint_Days × Focus_Factor × Hours_Per_Day
Story_Point_Capacity = Available_Capacity / Avg_Hours_Per_Point
```

**Focus Factor**: 0.6-0.8 (accounts for meetings, admin, interrupts)

### Buffer Allocation

| Context | Buffer |
|---------|--------|
| Stable team, known work | 15% |
| New team or technology | 25% |
| High-risk features | 30% |
| External dependencies | 25-40% |

---

## Estimation Accuracy Tracking

### Accuracy Metrics

```
Accuracy = Actual_Points / Estimated_Points × 100
```

| Accuracy | Rating | Action |
|----------|--------|--------|
| 85-115% | Good | Maintain process |
| 70-84% or 116-130% | Acceptable | Minor adjustments |
| <70% or >130% | Poor | Process review needed |

### Tracking Template

```markdown
## Sprint Estimation Accuracy: Sprint [N]

| Story | Estimated | Actual | Accuracy | Notes |
|-------|-----------|--------|----------|-------|
| S-001 | 5 | 5 | 100% | - |
| S-002 | 8 | 13 | 62% | Unexpected API complexity |

**Sprint Accuracy**: 83%
**Rolling 3-Sprint**: 87%
**Improvement Actions**: [Document learnings]
```

---

## Re-Estimation Triggers

### When to Re-Estimate

| Trigger | Action |
|---------|--------|
| Scope clarification reveals complexity | Re-estimate with new info |
| Technical spike complete | Re-estimate with findings |
| Item >2 sprints in backlog | Refresh before planning |
| Team composition change | Review affected items |
| Major dependency change | Assess impact, re-estimate |

### Re-Estimation Rules

1. **Document reason**: Why did the estimate change?
2. **Compare to original**: Track delta for learning
3. **Communicate**: Notify stakeholders if timeline impacted
4. **Don't re-estimate completed work**: Track as variance instead

---

## Relationship to Other Skills

| Skill | Relationship |
|-------|--------------|
| `generating-tasks` | Task breakdown AFTER estimation; tasks inherit parent estimate |
| `managing-roadmaps` | Velocity feeds sprint capacity; this skill provides input |
| `assessing-business-alignment` | Timeline realism uses estimates; this skill provides raw data |
| `feature-design-workflow` | Estimation happens in Phase 3 (DECIDE) |

---

## Anti-Patterns (NEVER DO)

| Anti-Pattern | Why Problematic | Correct Approach |
|--------------|-----------------|------------------|
| Estimate by deadline | Works backward from date, not reality | Estimate scope, then fit to timeline |
| Solo estimation | Single perspective, bias | Team estimation (planning poker) |
| Padding secretly | Hidden buffers distort velocity | Explicit buffers, transparent |
| Ignoring history | Repeat past mistakes | Track accuracy, calibrate |
| Precise hours for unknowns | False precision | Ranges or points for uncertainty |
| Velocity as target | Pressure causes point inflation | Velocity is diagnostic, not goal |
| Never re-estimating | Stale estimates mislead | Refresh backlog regularly |

---

## Quick Reference

### Story Point Scale

| Points | Complexity | Reference |
|--------|------------|-----------|
| 1 | Trivial | Config change |
| 2 | Simple | Validation rule |
| 3 | Moderate | API endpoint |
| 5 | Complex | Multi-component |
| 8 | Large | Integration |
| 13+ | Split it | Epic |

### Three-Point Formula

```
E = (O + 4M + P) / 6
SD = (P - O) / 6
```

### Velocity Guidelines

- Use 3-sprint rolling average
- First 3 sprints = learning period
- New team member = -20% for 2 sprints
- Buffer: 15-30% depending on risk

### Accuracy Targets

- Good: 85-115%
- Acceptable: 70-130%
- Poor: <70% or >130%

---

## Thinking Frameworks

When facing estimation challenges, these frameworks guide systematic problem-solving.

**Full Catalog**: [Thinking Frameworks README](../../docs/00-core/frameworks/README.md)

**Most Relevant for Estimation**:

| Framework | When to Use |
|-----------|-------------|
| [Pre-Mortem](../../docs/00-core/frameworks/strategy.md) | Identifying why estimates might fail |
| [CAGEERF](../../docs/00-core/frameworks/structured-execution.md) | Multi-phase effort breakdown |

> **Selection Tip**: risk identification→Pre-Mortem, complex breakdown→CAGEERF
