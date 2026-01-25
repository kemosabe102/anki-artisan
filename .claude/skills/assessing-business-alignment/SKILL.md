---
name: assessing-business-alignment
description: >
  Use this skill when validating business alignment, calculating ROI, assessing NFR coverage, 
  or applying P×I×E risk scoring. Trigger keywords: business review, alignment score, risk 
  assessment, cost-benefit, NFR validation, traceability.
---

# Assessing Business Alignment

> **Executive-level pragmatism for validating plans against business goals, ROI, and feasibility.**

---

## Contents

1. [Disney Creative Strategy - REALIST Lens](#disney-creative-strategy---realist-lens)
2. [Alignment Score Formula](#alignment-score-formula)
3. [Cost-Benefit Analysis](#cost-benefit-analysis)
4. [P×I×E Risk Scoring](#pie-risk-scoring)
5. [Timeline Realism Assessment](#timeline-realism-assessment)
6. [NFR Categories](#nfr-categories-4-required)
7. [Scoring Thresholds](#scoring-thresholds)
8. [FR Traceability Calculation](#fr-traceability-calculation)
9. [Review Checklist](#review-checklist)
10. [Anti-Patterns](#anti-patterns-never-do)
11. [Quick Reference](#quick-reference)

---

## Disney Creative Strategy - REALIST Lens

You operate as the REALIST in the Disney Creative Strategy framework.

**Realist Mindset**:
- Is this achievable with current resources?
- Does the ROI justify the effort?
- Are timelines and constraints realistic?
- What practical trade-offs are needed?

**Focus Areas**:

| Area | Realist Question |
|------|------------------|
| ROI Validation | Does benefit outweigh cost? |
| Pain Point Alignment | Does this address real user pain? |
| Scope Feasibility | Can this be delivered in stated constraints? |
| Resource Reality | Are dependencies and integrations accounted for? |
| Business Alignment | Does this fit strategic priorities? |

**Output Tone**: Pragmatically grounded. Validate feasibility with specific evidence.

---

## Alignment Score Formula

**Formula**:
```
Alignment = (GoalCoverage × 0.4) + (NFRCoverage × 0.3) + (Traceability × 0.3)
```

**Component Definitions**:
- **GoalCoverage**: Percentage of business goals addressed by plan components (0.0-1.0)
- **NFRCoverage**: Categories_assessed / 4 (target: 100%)
- **Traceability**: FR_IDs_mapped / FR_IDs_total (target: >= 70%)

**Targets**:
| Component | Target | Weight |
|-----------|--------|--------|
| Goal Coverage | >= 0.80 | 40% |
| NFR Coverage | 100% (4/4 categories) | 30% |
| Traceability | >= 70% | 30% |

---

## Cost-Benefit Analysis

**Budget Constraint**: $100/month operational limit (hard cap)

**Validation Points**:
1. Validate estimates against $100/month operational limit
2. Ensure strategies align with business priorities
3. Review business justification for costs >$50/month
4. Verify free tier maximization where business impact acceptable

**Cost Categories**:

| Category | Validation Criteria |
|----------|---------------------|
| Infrastructure | Within $100/month, free tier maximized |
| Third-party Services | ROI justified, alternatives evaluated |
| Development Time | Reuse opportunities identified |
| Maintenance | Long-term burden assessed |

**Code Reuse ROI**:
- **Reuse Savings** = (Hours to Build New) - (Hours to Integrate Existing)
- **Extension Savings** = (Hours to Build New) - (Hours to Extend Existing + Migration Hours)
- **Target**: Reuse/Extension must save >50% development hours to justify new implementation

---

## P×I×E Risk Scoring

**Formula**: `Risk Score = Probability × Impact × Exposure`

**Factor Scales**:

| Factor | Scale | Description |
|--------|-------|-------------|
| Probability (P) | 0.1-1.0 | Likelihood of occurrence |
| Impact (I) | 1-5 | Severity if occurs |
| Exposure (E) | 0.1-1.0 | Vulnerability window |

**Risk Categories**:
1. **Scope Risks**: Requirements creep, unclear boundaries
2. **Requirements Risks**: Missing/incomplete specifications
3. **Market Risks**: Competitive pressure, timing
4. **Resource Risks**: Team availability, skill gaps
5. **Technical Risks**: Integration complexity, dependencies

**Risk Validation Checklist**:
- [ ] P×I×E scores calculated for all identified risks
- [ ] Risk-adjusted timelines validated for feasibility
- [ ] Mitigation resource allocation aligned with priorities
- [ ] Business risk coverage comprehensive (scope, requirements, market)
- [ ] Business impact assessments included in risk calculations

---

## Timeline Realism Assessment

**Formula**:
```
Timeline_Realism = 1 - |Estimated_Effort - Calculated_Complexity| / Calculated_Complexity
```

**Score Interpretation**:

| Score Range | Assessment | Action |
|-------------|------------|--------|
| >= 0.85 | Realistic | Proceed |
| 0.70-0.84 | Acceptable | Monitor closely |
| 0.50-0.69 | Concerning | Review assumptions |
| < 0.50 | Unrealistic | Recommend adjustment |

**Target**: Timeline_Realism >= 0.85

**Red Flags**:
- Complexity vs estimation mismatch > 40%
- No buffer for unknowns in timeline
- Critical path dependencies unmitigated
- Resource over-allocation (>80% utilization assumed)

**Validation Points**:
1. Sprint Allocation: Points align with business delivery expectations
2. Phased Delivery: Feasibility from stakeholder perspective
3. Resource Allocation: Matches complexity and priorities
4. Quality Gates: Timing aligns with business milestones
5. Dependencies: External blockers identified and mitigated

---

## NFR Categories (4 Required)

All business reviews MUST assess these four NFR categories:

| # | Category | Assessment Focus |
|---|----------|------------------|
| 1 | **Performance** | Response time, throughput, scalability |
| 2 | **Security** | Authentication, authorization, data protection |
| 3 | **Availability/Reliability** | Uptime, disaster recovery, backup |
| 4 | **Compliance** | Regulatory, audit, data governance |

**Coverage Calculation**: `NFR_Coverage = Categories_Assessed / 4`

**Target**: 100% (all 4 categories assessed)

**Business Impact Perspective**:
- Performance → User experience
- Security → Risk mitigation
- Availability → Business continuity
- Compliance → Operational cost

---

## Scoring Thresholds

**Universal scoring scale for business alignment assessments**:

| Score | Assessment | Priority | Action |
|-------|------------|----------|--------|
| < 0.30 | Critical | HALT | Escalate to orchestrator, stop work |
| 0.30-0.50 | Needs Work | P1 | Flag critical, require remediation |
| 0.50-0.70 | Acceptable | P2 | Flag important, recommend improvements |
| > 0.70 | Good | P3 | Proceed, note optional enhancements |

**Escalation Triggers**:
- Alignment score < 0.30 → P1: HALT, escalate
- NFR coverage "low" in 3+ categories → P2: Flag, recommend human review
- Traceability < 50% → P2: Document gaps, prioritize in edit plan
- Budget overrun > 150% → P2: Flag critical, include mitigation options

---

## FR Traceability Calculation

**Formula**:
```
Traceability = FR_IDs_mapped / FR_IDs_total
```

**Target**: >= 70%

**Process**:
1. Identify all FR-IDs in SPEC.md
2. Map each FR-ID to plan components
3. Calculate coverage percentage
4. Document unmapped FR-IDs as gaps

**Gap Documentation Format**:
```
| FR-ID | Status | Gap Description |
|-------|--------|-----------------|
| FR-001 | Mapped | Covered in PLAN-001 |
| FR-002 | Unmapped | No plan component addresses this requirement |
```

---

## Review Checklist

**Pre-Review Validation**:
- [ ] SPEC.md exists and contains business goals
- [ ] PLAN files exist and are readable
- [ ] Business goals section defined in SPEC

**Analysis Checklist**:
- [ ] Business goals alignment score calculated with evidence
- [ ] All 4 NFR categories assessed from business impact perspective
- [ ] Traceability coverage % computed with gap identification
- [ ] Cost-benefit analysis applied (budget constraint validated)
- [ ] P×I×E risk scores calculated for identified risks
- [ ] Timeline realism assessed (target >= 0.85)

**Output Validation**:
- [ ] Framework citations included for all scoring methodologies
- [ ] Zero-mutation verification confirmed
- [ ] Report written to correct location

---

## Anti-Patterns (NEVER DO)

- Mutating ANY source files (SPEC.md, PLAN.md, etc.)
- Skipping alignment scoring dimensions
- Producing reports without framework citations
- Making architectural recommendations (defer to architecture)
- Ignoring budget constraints ($100/month limit)
- Calculating alignment without all three components (Goal, NFR, Traceability)
- Proceeding with alignment score < 0.30 without escalation
- Accepting NFR coverage < 100% without justification

---

## Quick Reference

**Core Formulas**:

| Metric | Formula | Target |
|--------|---------|--------|
| Alignment Score | (Goal×0.4) + (NFR×0.3) + (Trace×0.3) | >= 0.70 |
| Traceability | FR_IDs_mapped / FR_IDs_total | >= 70% |
| NFR Coverage | Categories_assessed / 4 | 100% |
| Timeline Realism | 1 - \|Est - Calc\| / Calc | >= 0.85 |
| Risk Score | P × I × E | Varies |

**Budget Constraints**:
- Operational limit: $100/month
- ROI review threshold: >$50/month

**Scoring Actions**:
- < 0.30 → HALT
- 0.30-0.50 → P1 remediation
- 0.50-0.70 → P2 improvements
- > 0.70 → P3 proceed
