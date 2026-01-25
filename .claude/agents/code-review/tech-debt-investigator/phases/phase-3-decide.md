# Phase 3: DECIDE - Prioritization & Planning

**OODA Stage**: DECIDE | **Time Allocation**: 10-15%

**Purpose**: Rank findings, group into sprints, calculate ROI, identify dependencies

**Deliverable**: Prioritized remediation plan with sprint groupings and ROI projections

---

## Workflow Steps

### Step 3.1: Finding Prioritization

**Input**: Impact/Effort matrix from Phase 2

**Process**:
1. Rank findings by composite score: `(impact_score * 2) - effort_score`
2. Apply tiebreaker: higher churn files first
3. Validate P1 items are truly quick wins (effort < 4 hours each)

**Output**: Ordered list of findings by priority

### Step 3.1.5: Conflict Resolution

**When findings compete for Sprint 1 resources, apply this priority order:**

| Priority | Condition | Rationale |
|----------|-----------|-----------|
| 1 | Hotspots >7.0 | Critical risk, blocks other work |
| 2 | P1 in `critical_modules` | Business-critical quick wins |
| 3 | P1 in non-critical modules | Regular quick wins |
| 4 | P2 strategic items | Planned capacity |
| 5 | P4 opportunistic | Fill remaining capacity |

**Tie-Breaking Rules**:
- Equal priority → higher churn file wins
- Equal churn → lower effort wins
- Still tied → alphabetical by file path (deterministic)

**Resource Constraint Handling**:
- If Sprint 1 capacity < total P1 effort: split P1 across Sprint 1+2
- Never defer hotspots >7.0 (escalate if capacity insufficient)
- Document deferred items with justification

### Step 3.2: Sprint Grouping

**Input**: Prioritized findings, hotspot flags

**Process**:
1. **Sprint 1**: All P1_quick_wins + urgent hotspots (score >7.0)
2. **Sprint 2**: P2_strategic items with dependencies resolved
3. **Sprint 3+**: Remaining P2 items + P4_opportunistic
4. P3_defer items: Document but exclude from active sprints

**Output**: Sprint assignments with effort estimates

### Step 3.3: ROI Projection

**Input**: Sprint groupings, effort estimates, impact scores

**Process**:
1. Calculate per-sprint metrics:
   - Total effort hours
   - Cumulative impact reduction
   - Debt score improvement projection
2. Apply Principal/Interest model:
   - Principal: one-time remediation cost
   - Interest: ongoing maintenance burden if not fixed
3. Calculate break-even timeline for each sprint

**Output**: ROI projections per sprint, payback period estimates

### Step 3.4: Dependency Identification

**Input**: All findings with file references

**Process**:
1. Identify shared dependencies between findings
2. Flag items that must be fixed before others
3. Document blocking relationships
4. Adjust sprint order if dependencies cross sprints

**Output**: Dependency graph, adjusted sprint sequence

---

## Quick Checklist

Before advancing to Phase 4 (ACT):

- [ ] Findings ranked by priority score
- [ ] Sprint 1 contains only quick wins and urgent hotspots
- [ ] ROI calculated for each sprint
- [ ] Dependencies mapped and addressed
- [ ] P3_defer items documented but excluded

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| P2 items in Sprint 1 | Sprint 1 is only P1 + urgent hotspots |
| Missing dependencies | Check file references for shared modules |
| No ROI justification | Calculate payback period for stakeholder buy-in |
| Ignoring urgency flags | Hotspots >7.0 override normal prioritization |

---

## Exit Criteria

**Approval required to proceed**

| Criterion | Weight | Check |
|-----------|--------|-------|
| Priority ranking complete | 0.30 | All findings ordered |
| Sprint groupings defined | 0.25 | Items assigned to sprints |
| ROI calculated | 0.25 | Payback periods documented |
| Dependencies resolved | 0.20 | No cross-sprint blockers |

---

**Previous Phase**: [Phase 2: ORIENT](phase-2-orient.md)
**Next Phase**: [Phase 4: ACT](phase-4-act.md)
