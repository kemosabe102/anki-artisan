# Risk Assessment Matrix: P×I×E Scoring Framework

## Overview

This framework provides systematic risk assessment using the **P×I×E scoring formula** (Probability × Impact × Exposure) to evaluate and prioritize risks in software development projects. All features and technical decisions should include comprehensive risk assessment.

**Risk Philosophy:** Proactive identification and mitigation of risks to ensure project success and stakeholder confidence.

## P×I×E Scoring Formula

### Risk Score = P × I × E

Where:

- **P (Probability):** Likelihood of risk occurring (1-5 scale)
- **I (Impact):** Severity of consequences if risk occurs (1-5 scale)
- **E (Exposure):** Duration or scope of exposure to risk (1-5 scale)

**Total Risk Score Range:** 1-125

- **1-25:** Low Risk (Green)
- **26-50:** Medium Risk (Yellow)
- **51-75:** High Risk (Orange)
- **76-125:** Critical Risk (Red)

## Scoring Scales

### Probability (P): Likelihood Scale

- **1 - Very Unlikely (5%):** Historical evidence suggests very low probability
- **2 - Unlikely (15%):** Some possibility but not expected
- **3 - Possible (35%):** Moderate chance based on current conditions
- **4 - Likely (65%):** High probability based on evidence/trends
- **5 - Very Likely (85%):** Almost certain to occur given current trajectory

### Impact (I): Severity Scale

- **1 - Minimal:** Minor inconvenience, easily resolved, <1 day impact
- **2 - Minor:** Some disruption, resolved with known procedures, <1 week impact
- **3 - Moderate:** Significant disruption, requires effort to resolve, 1-4 weeks impact
- **4 - Major:** Serious consequences, substantial recovery effort, 1-3 months impact
- **5 - Severe:** Critical consequences, major recovery effort, >3 months impact

### Exposure (E): Duration/Scope Scale

- **1 - Limited:** Single component, short timeframe, isolated impact
- **2 - Contained:** Few components, defined timeframe, localized impact
- **3 - Extended:** Multiple components, medium timeframe, cross-functional impact
- **4 - Widespread:** Many components, long timeframe, organization-wide impact
- **5 - Enterprise:** All components, indefinite timeframe, external stakeholder impact

## Risk Categories

### Technical Risks

**Definition:** Risks related to technology choices, implementation complexity, and technical debt

**Common Patterns:**

- **Technology Maturity:** New/unproven technologies (P=3, I=4, E=4 = 48)
- **Integration Complexity:** Multiple system integration points (P=4, I=3, E=3 = 36)
- **Performance Bottlenecks:** Scalability limitations (P=3, I=4, E=4 = 48)
- **Technical Debt:** Accumulation of shortcuts (P=4, I=3, E=5 = 60)
- **Dependency Risks:** External library/service dependencies (P=2, I=3, E=4 = 24)

### Resource Risks

**Definition:** Risks related to team capacity, skills, and availability

**Common Patterns:**

- **Skill Gaps:** Team lacks required expertise (P=3, I=4, E=3 = 36)
- **Resource Availability:** Key team members unavailable (P=2, I=4, E=2 = 16)
- **Workload Overcommitment:** Team capacity exceeded (P=4, I=3, E=3 = 36)
- **Knowledge Concentration:** Single points of failure (P=3, I=4, E=4 = 48)
- **Tool/Infrastructure Limitations:** Development environment constraints (P=2, I=2, E=3 = 12)

### Business Risks

**Definition:** Risks related to business goals, market conditions, and stakeholder alignment

**Common Patterns:**

- **Requirement Changes:** Evolving business needs (P=4, I=3, E=4 = 48)
- **Market Timing:** Competitive pressure/market shifts (P=3, I=5, E=3 = 45)
- **Stakeholder Alignment:** Conflicting priorities (P=3, I=3, E=4 = 36)
- **Budget Constraints:** Funding limitations (P=2, I=4, E=4 = 32)
- **Regulatory Changes:** Compliance requirement changes (P=2, I=5, E=4 = 40)

### Operational Risks

**Definition:** Risks related to deployment, monitoring, and ongoing operations

**Common Patterns:**

- **Deployment Complexity:** Complex release processes (P=3, I=3, E=2 = 18)
- **Monitoring Gaps:** Insufficient observability (P=4, I=3, E=4 = 48)
- **Data Loss/Corruption:** Data integrity issues (P=2, I=5, E=4 = 40)
- **Security Vulnerabilities:** Security implementation gaps (P=2, I=5, E=5 = 50)
- **Disaster Recovery:** Inadequate backup/recovery procedures (P=1, I=5, E=5 = 25)

## Risk Assessment Template

### Standard Risk Assessment Table

```markdown
## Risk Assessment Matrix

| Risk ID  | Risk Description                         | Category    | P   | I   | E   | Score | Priority | Mitigation Strategy                       |
| -------- | ---------------------------------------- | ----------- | --- | --- | --- | ----- | -------- | ----------------------------------------- |
| TECH-001 | New framework adoption learning curve    | Technical   | 3   | 3   | 3   | 27    | Medium   | Training plan + prototype                 |
| RES-001  | Key developer availability during sprint | Resource    | 2   | 4   | 2   | 16    | Low      | Cross-training + documentation            |
| BIZ-001  | Requirements change mid-development      | Business    | 4   | 3   | 4   | 48    | Medium   | Agile methodology + stakeholder alignment |
| OPS-001  | Production deployment complexity         | Operational | 3   | 3   | 2   | 18    | Low      | Deployment automation + testing           |

**Risk Summary:**

- Critical (76-125): 0 risks
- High (51-75): 0 risks
- Medium (26-50): 2 risks
- Low (1-25): 2 risks

**Top Priority Mitigation:** BIZ-001 (Score: 48) - Establish weekly stakeholder reviews
```

## Risk Mitigation Strategies

### Critical Risk Response (76-125)

**Immediate Action Required:**

- **Risk Avoidance:** Change approach to eliminate risk
- **Executive Escalation:** Immediate leadership involvement
- **Resource Reallocation:** Shift resources to address risk
- **Contingency Activation:** Execute emergency backup plans
- **Regular Monitoring:** Daily risk status updates

### High Risk Response (51-75)

**Active Management Required:**

- **Risk Reduction:** Implement specific mitigation actions
- **Enhanced Monitoring:** Weekly risk status reviews
- **Contingency Planning:** Develop detailed backup plans
- **Stakeholder Communication:** Regular risk status updates
- **Resource Buffering:** Allocate additional resources

### Medium Risk Response (26-50)

**Managed Monitoring:**

- **Mitigation Planning:** Document specific mitigation actions
- **Regular Monitoring:** Bi-weekly risk status checks
- **Contingency Preparation:** Identify potential responses
- **Team Awareness:** Ensure team understands risk
- **Early Warning Systems:** Set up risk indicators

### Low Risk Response (1-25)

**Standard Monitoring:**

- **Risk Tracking:** Include in regular status reports
- **Basic Mitigation:** Simple preventive measures
- **Awareness Only:** Team knowledge of potential risk
- **Standard Procedures:** Follow normal risk management
- **Periodic Review:** Monthly risk reassessment

## Risk Lifecycle Management

### Risk Identification Phase

1. **Brainstorming Sessions:** Team-based risk identification
2. **Historical Analysis:** Review past project risks
3. **Expert Consultation:** Domain expert risk assessment
4. **Stakeholder Input:** Business and user risk concerns
5. **Technical Analysis:** Architecture and implementation risks

### Risk Analysis Phase

1. **P×I×E Scoring:** Apply quantitative risk assessment
2. **Risk Categorization:** Classify by type and source
3. **Impact Analysis:** Assess potential consequences
4. **Probability Assessment:** Evaluate likelihood factors
5. **Exposure Evaluation:** Determine duration and scope

### Risk Response Planning

1. **Mitigation Strategy:** Define specific risk reduction actions
2. **Contingency Planning:** Prepare backup approaches
3. **Resource Allocation:** Assign responsibility and resources
4. **Timeline Development:** Set mitigation implementation schedule
5. **Success Criteria:** Define measurable mitigation outcomes

### Risk Monitoring & Control

1. **Regular Assessment:** Ongoing P×I×E score updates
2. **Trigger Monitoring:** Watch for risk indicator changes
3. **Mitigation Tracking:** Monitor action effectiveness
4. **New Risk Identification:** Continuous risk discovery
5. **Lessons Learned:** Document risk management outcomes

## Integration with Development Process

### SPEC Creation Requirements

Every specification must include:

```markdown
## Risk Assessment Matrix

[Standard risk assessment table]
**Risk Summary:** [X] Critical, [Y] High, [Z] Medium, [W] Low
**Primary Mitigation Focus:** [Top 2-3 risks with specific mitigation plans]
```

### Technical Planning Integration

- Include risk assessment in technical architecture decisions
- Document risk mitigation in implementation approaches
- Plan risk monitoring as part of development tasks
- Integrate risk response into testing and validation

### Sprint Planning Considerations

- Prioritize high-risk items for early sprints
- Allocate buffer time for risk mitigation
- Assign risk ownership to specific team members
- Include risk review in sprint retrospectives

## Risk Monitoring Metrics

### Risk Health Indicators

- **Risk Trend:** Overall risk score trending up/down
- **Mitigation Effectiveness:** Percentage of risks with decreasing scores
- **Risk Discovery Rate:** New risks identified per sprint
- **Risk Resolution Rate:** Risks closed per sprint

### Early Warning Signals

- **Score Increases:** Existing risks with increasing P×I×E scores
- **New Critical Risks:** Emergence of 76+ score risks
- **Mitigation Delays:** Planned mitigations behind schedule
- **Resource Constraints:** Team capacity affecting risk response

## Implementation Guidelines

### For Architecture Review Agent

- Apply P×I×E scoring to all identified technical risks
- Include risk assessment in Technical Review Reports
- Recommend specific mitigation strategies with effort estimates
- Flag Critical/High risks for immediate attention

### For Technical PM Agent

- Validate business risk assessments in plan reviews
- Ensure risk mitigation is included in project timelines
- Monitor risk trends and escalate Critical/High risks
- Coordinate cross-functional risk response efforts

### For Plan Enhancement Agent

- Include comprehensive risk assessment in all enhanced plans
- Document risk mitigation strategies in implementation approaches
- Ensure risk ownership is clearly assigned
- Validate risk assessment completeness

---

**This framework ensures systematic risk identification, quantitative assessment, and proactive mitigation planning for all development activities.**
