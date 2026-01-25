# Phase 2: ORIENT - Score Calculation & Analysis

**OODA Stage**: ORIENT | **Time Allocation**: 25-30%

**Purpose**: Calculate category scores, apply SQALE methodology, build Impact/Effort matrix

**Deliverable**: Weighted scores, TDR ratio, hotspot rankings, prioritized findings

---

## Workflow Steps

### Step 2.1: Category Score Calculation

**Input**: Raw patterns from Phase 1

**Process**:
1. Calculate 6-category scores using SQALE weights:
   - Code Quality: 40%
   - Testing: 20%
   - Architecture: 15%
   - Documentation: 10%
   - Infrastructure: 10%
   - Design: 5%
2. Apply industry thresholds:
   - Cyclomatic complexity: >10 = high
   - Code duplication: >5% = warning, >10% = severe
   - Test coverage: <80% = gap
3. Generate category breakdown with evidence references

**Output**: `category_ratings` object with scores (0-5 stars), evidence arrays, remediation_hours

### Step 2.1.5: Business Context Integration

**Input**: `business_context` from orchestrator (optional)

**Process**:
1. If `critical_modules` provided:
   - Apply 1.5x impact multiplier to findings in listed paths
   - Example: Finding in `packages/payments.py` with base impact 6 → adjusted impact 9
2. If `usage_frequency` provided:
   - High traffic modules: +2 impact score
   - Medium traffic: +1 impact score
   - Low traffic: no adjustment
3. If `team_ownership` provided:
   - Flag ownership dispersion (>3 teams touching same file)
   - Weight by team capacity in sprint planning
4. If `incident_files` provided:
   - Auto-flag as P0 priority (override normal prioritization)
   - Add incident correlation to evidence

**Output**: Business-weighted impact scores for all findings

**Note**: If no business_context provided, use technical metrics only (default behavior)

### Step 2.2: SQALE TDR Calculation

**Input**: Category scores, estimated remediation hours

**Process**:
1. Calculate Technical Debt Ratio: `remediation_cost / development_cost`
2. Map to SQALE grade (A-E):
   - A: TDR < 5%
   - B: TDR 5-10%
   - C: TDR 10-20%
   - D: TDR 20-50%
   - E: TDR > 50%
3. Calculate composite `debt_score` (0-100, lower = more debt)

**Output**: `tdr_ratio`, `sqale_grade`, `debt_score`, `debt_classification`

### Step 2.3: Impact/Effort Matrix

**Input**: Individual findings from categories

**Process**:
1. Score each finding:
   - `impact_score` (0-10): business/technical severity
   - `effort_score` (0-10): remediation complexity
2. Assign priority quadrant:
   - P1_quick_wins: High impact, low effort (do first)
   - P2_strategic: High impact, high effort (plan carefully)
   - P3_defer: Low impact, high effort (deprioritize)
   - P4_opportunistic: Low impact, low effort (do when convenient)
3. Calculate `principal_cost_hours` for each item

**Output**: `impact_effort_matrix` array with all findings prioritized

### Step 2.4: Hotspot Identification

**Input**: Git metrics from Phase 1, complexity scores

**Process**:
1. Apply hotspot formula: `churn x complexity x defects x criticality`
2. Normalize to 0-10 scale
3. Flag items with score >7.0 as urgent hotspots
4. Identify patterns across findings (clustering)

**Output**: `hotspots` array with ranked files and urgency flags

---

## Quick Checklist

Before advancing to Phase 3 (DECIDE):

- [ ] All 6 categories scored with evidence
- [ ] SQALE TDR calculated, grade assigned
- [ ] Composite debt_score computed (0-100)
- [ ] All findings mapped to Impact/Effort matrix
- [ ] Hotspots identified and flagged (>7.0 threshold)

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Missing category weights | Always apply 6-category SQALE weights |
| Quadrant without scores | Calculate impact AND effort before assigning |
| Hotspot without churn | Requires git history for meaningful scores |
| No evidence arrays | Every category needs file:line references |

---

## Exit Criteria

**CQ (Context Quality) >= 0.85 required to proceed**

| Criterion | Weight | Check |
|-----------|--------|-------|
| Categories scored | 0.30 | All 6 categories have scores + evidence |
| TDR calculated | 0.25 | SQALE grade A-E assigned |
| Matrix populated | 0.20 | All findings in quadrants P1-P4 |
| Hotspots ranked | 0.15 | Formula applied, >7.0 flagged |
| Patterns identified | 0.10 | Clustering analysis complete |

---

**Previous Phase**: [Phase 1: OBSERVE](phase-1-observe.md)
**Next Phase**: [Phase 3: DECIDE](phase-3-decide.md)
