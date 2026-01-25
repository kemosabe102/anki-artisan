# Business Frameworks

Detailed business analysis frameworks used by the technical-pm agent for ROI validation, cost-benefit analysis, risk assessment, and timeline realism evaluation.

---

## Code Reuse ROI Validation

**Critical Business Assessment Dimensions**:

### Development Time Savings
Calculate hours saved by reusing vs building new components:
- **Reuse Savings** = (Hours to Build New) - (Hours to Integrate Existing)
- **Extension Savings** = (Hours to Build New) - (Hours to Extend Existing + Migration Hours)
- **Replacement Savings** = (Maintenance Hours Saved Over Project Lifetime) - (Migration Hours + Cleanup Hours)

**Target Threshold**: Reuse/Extension must save >50% development hours to justify new implementation

### Assessment Checklist
- [ ] Development time savings calculated
- [ ] Maintenance burden reduction assessed
- [ ] Technical debt reduction value quantified
- [ ] Business risk of replacing vs extending evaluated
- [ ] Team productivity impact analyzed (familiarity, learning curve)

---

## Cost-Benefit Analysis Validation

**Framework Reference**: `cost-analysis-framework.md`

### Validation Points
1. **Budget Constraint**: Validate estimates against $100/month operational limit
2. **Cost Optimization**: Ensure strategies align with business priorities
3. **ROI Timeline**: Review business justification for costs >$50/month
4. **Free Tier Maximization**: Verify optimization where business impact acceptable
5. **Code Reuse Integration**: Include time savings in cost-benefit calculations

### Cost Categories to Validate
| Category | Validation Criteria |
|----------|---------------------|
| Infrastructure | Within $100/month, free tier maximized |
| Third-party Services | ROI justified, alternatives evaluated |
| Development Time | Reuse opportunities identified |
| Maintenance | Long-term burden assessed |

---

## Risk-Adjusted Planning Review

**Framework Reference**: `risk-assessment-matrix.md`

### P x I x E Scoring Methodology

**Formula**: Risk Score = Probability x Impact x Exposure

| Factor | Scale | Description |
|--------|-------|-------------|
| Probability (P) | 0.1-1.0 | Likelihood of occurrence |
| Impact (I) | 1-5 | Severity if occurs |
| Exposure (E) | 0.1-1.0 | Vulnerability window |

### Risk Categories for Business Context
1. **Scope Risks**: Requirements creep, unclear boundaries
2. **Requirements Risks**: Missing/incomplete specifications
3. **Market Risks**: Competitive pressure, timing
4. **Resource Risks**: Team availability, skill gaps
5. **Technical Risks**: Integration complexity, dependencies

### Validation Checklist
- [ ] P x I x E scores calculated for all identified risks
- [ ] Risk-adjusted timelines validated for feasibility
- [ ] Mitigation resource allocation aligned with priorities
- [ ] Business risk coverage comprehensive (scope, requirements, market)
- [ ] Business impact assessments included in risk calculations

---

## Timeline Realism Assessment

**Framework Reference**: `quality-scoring-algorithms.md`

### Complexity vs Estimation Analysis

**Realism Score Formula**:
```
Timeline_Realism = 1 - |Estimated_Effort - Calculated_Complexity| / Calculated_Complexity
```

| Score Range | Assessment |
|-------------|------------|
| >= 0.85 | Realistic |
| 0.70-0.84 | Acceptable with monitoring |
| 0.50-0.69 | Concerning, review assumptions |
| < 0.50 | Unrealistic, recommend adjustment |

### Validation Points
1. **Sprint Allocation**: Points align with business delivery expectations
2. **Phased Delivery**: Feasibility from stakeholder perspective
3. **Resource Allocation**: Matches complexity and priorities
4. **Quality Gates**: Timing aligns with business milestones
5. **Dependencies**: External blockers identified and mitigated

### Red Flags
- Complexity vs estimation mismatch > 40%
- No buffer for unknowns in timeline
- Critical path dependencies unmitigated
- Resource over-allocation (>80% utilization assumed)

---

## Framework Integration Instructions

**For all business review operations**:

1. **Citation Requirements**
   - Always cite which framework and specific methodology used
   - Include framework compliance validation in assessments
   - Reference specific guide file paths when applicable

2. **Validation Sequence**
   - Cost-benefit: MUST apply `cost-analysis-framework.md`
   - Risk: MUST validate `risk-assessment-matrix.md` coverage
   - Timeline: MUST apply `quality-scoring-algorithms.md`
   - Quality: MUST align with framework thresholds

3. **Deviation Handling**
   - Flag framework deviations with business impact assessment
   - Provide justification for any deviation
   - Escalate critical deviations (budget overruns, high risks, timeline conflicts)

4. **Report Standards**
   - Include framework-based validation in all Business Review Reports
   - Document framework-aligned recommendations in Business Edit Plans
   - Apply cost constraints consistently across analysis
   - Provide framework-backed evidence for all recommendations
   - Maintain traceability between business goals and framework requirements
