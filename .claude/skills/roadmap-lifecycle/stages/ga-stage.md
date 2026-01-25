# GA (General Availability) Stage Definition

## Overview

- **Score Range**: 8.0 - 10.0
- **Focus**: Full Rigor + Continuous Value - production deployment with complete support
- **Risk Tolerance**: Minimal
- **Business Context**: Full commercial release, production support, SLA commitments

## Core Philosophy

**Production is a living scale - there is no "done" - only continuous improvement.**

GA is NOT a destination. It is the entry point to continuous production excellence where the product must evolve with customer needs while maintaining exceptional reliability.

## Entry Criteria

What must be true to ENTER GA from Beta:

### From Beta Exit
- [ ] Beta exit criteria complete (all Beta requirements met)
- [ ] 99.9% uptime demonstrated during beta period
- [ ] Disaster recovery tested and validated
- [ ] Full documentation complete (user, operational, API)
- [ ] Support processes operational and validated
- [ ] Security compliance certified
- [ ] All SLOs consistently met for 30+ days
- [ ] 7+ pain points with measurable improvement

### Quality Gates Passed
- [ ] Overall score minimum: 4.2
- [ ] Architecture soundness: 4.2
- [ ] Implementation readiness: 4.0
- [ ] Production readiness: 4.5
- [ ] Integration coherence: 4.0
- [ ] Performance optimization: 4.0
- [ ] Maintainability: 4.0
- [ ] Standards compliance: 4.0

### Operational Readiness
- [ ] 24/7 support capability demonstrated
- [ ] On-call rotation established and tested
- [ ] Incident response playbooks complete
- [ ] Escalation paths documented
- [ ] Business continuity plan validated

## Ongoing Criteria (No Exit - Continuous)

GA is continuous improvement, not a destination. These criteria must be maintained indefinitely:

### Availability & Reliability
- [ ] 99.9%+ availability maintained
- [ ] SLA commitments met consistently
- [ ] Zero critical incidents per quarter (target)
- [ ] Mean time to recovery (MTTR) within SLA
- [ ] Proactive capacity planning reviews (monthly)

### Security & Compliance
- [ ] Continuous security monitoring active
- [ ] CVE patching within defined SLAs
- [ ] Compliance certifications current
- [ ] Security assessments conducted (annual minimum)
- [ ] Threat modeling updated with feature changes

### Customer Excellence
- [ ] Customer feedback actively integrated
- [ ] Feature evolution based on usage data
- [ ] Support ticket SLAs met
- [ ] Customer satisfaction metrics tracked
- [ ] Emerging needs identified and addressed

### Technical Health
- [ ] Technical debt actively managed (not accumulated)
- [ ] Performance metrics trending stable or improving
- [ ] Team knowledge distributed (no single points of failure)
- [ ] Documentation kept current with changes
- [ ] Operational efficiency continuously improved

## Quality Thresholds

| Dimension | Min Score | GA-Level Requirements |
|-----------|-----------|----------------------|
| Architecture | 9-10 | Fully maintainable, multi-tenant ready, plugin architecture, long-term evolution path |
| Data & Migrations | 9-10 | Online migrations, zero-downtime updates, multi-region data, compliance ready |
| Observability | 9-10 | Full telemetry, custom dashboards, predictive alerts, business KPIs tracked |
| Testing | 9-10 | Chaos engineering, load testing, security testing, mutation testing |
| Release & Deployment | 9-10 | Progressive rollouts, multi-region deploy, zero-downtime, GitOps |
| Security | 9-10 | Zero-trust architecture, compliance certified, security automation, threat modeling |
| Capacity & Cost | 9-10 | Auto-scaling, multi-region, DR tested, FinOps practices |
| Documentation | 9-10 | Self-service docs, video tutorials, clear RACI, knowledge base |
| LLM Integration | 9-10 | Model garden, continuous evaluation, safety rails, bias monitoring |
| Agent Orchestration | 9-10 | Self-organizing, adaptive workflows, full observability, human-in-loop controls |


## Stage-Specific Focus Areas

### DO at GA

- **Maintain 99.9%+ availability** - This is non-negotiable
- **Continuous security monitoring** - Proactive threat detection
- **Proactive capacity planning** - Stay ahead of growth
- **Customer feedback loops** - Systematic collection and action
- **Performance optimization** - Continuous improvement, not stagnation
- **Feature evolution based on data** - Evidence-driven development
- **Support excellence** - 24/7 capability, rapid response

### CONTINUOUSLY IMPROVE

- Security posture (annual assessments, quarterly reviews)
- Performance metrics (monthly trend analysis)
- Customer satisfaction (ongoing measurement)
- Operational efficiency (reduce toil, automate)
- Documentation freshness (review with each release)
- Team knowledge distribution (cross-training, runbook updates)
- Cost optimization (FinOps practices)

## Anti-Patterns (NEVER at GA)

| Anti-Pattern | Why It's Dangerous | What To Do Instead |
|--------------|-------------------|-------------------|
| Considering the product "done" | Stagnation leads to irrelevance | Continuous improvement mindset |
| Stopping innovation for stability | Market passes you by | Balance stability with evolution |
| Ignoring emerging customer needs | Customer churn | Active feedback integration |
| Accumulating technical debt | System becomes unmaintainable | Active debt management |
| Uncontrolled cloud spend | Budget overruns, business impact | FinOps practices, cost monitoring |
| Tribal knowledge | Single points of failure | Documentation, cross-training |
| Unactionable alerts | Alert fatigue, missed incidents | Tune alerts, ensure actionability |
| Ignored CVEs | Security breaches | Patch within SLA, no exceptions |
| Manual operational tasks | Toil, human error | Automate everything possible |
| Skipping post-mortems | Repeat failures | Blameless post-mortems, action items |

## Validation Requirements

### Mandatory (Required for GA Entry)

- [ ] Production certification testing passed
- [ ] High availability validation (99.9%+ demonstrated)
- [ ] Security compliance audit passed
- [ ] Performance certification (SLOs met under load)
- [ ] Scalability validation (proven under expected scale)
- [ ] Support process certification (team trained, processes tested)
- [ ] Business continuity testing (DR drill successful)
- [ ] Regulatory compliance validation (if applicable)

### Ongoing (Required to Maintain GA Status)

- [ ] Independent security assessments (annual minimum)
- [ ] Compliance certification renewals (per certification schedule)
- [ ] Advanced monitoring validation (quarterly review)
- [ ] Disaster recovery drills (semi-annual minimum)
- [ ] Capacity planning reviews (monthly)
- [ ] Performance trend analysis (monthly)

## Risk Management at GA

### Risk Tolerance
- **Level**: Minimal
- **Critical Risks**: 0 allowed above medium severity
- **Technical Debt**: No debt that impacts production operations
- **Change Control**: Production change management with rollback capabilities

### Risk Categories to Monitor

| Category | Monitoring Approach | Response SLA |
|----------|--------------------|--------------| 
| Security vulnerabilities | Continuous scanning, CVE feeds | Critical: 24h, High: 7d |
| Performance degradation | Real-time metrics, anomaly detection | Investigate within 1h |
| Capacity limits | Predictive alerting, trend analysis | 30-day runway minimum |
| Compliance drift | Automated compliance checks | Remediate before audit |
| Customer impact | Error rates, satisfaction metrics | Immediate triage |

## Checklist Template (Copy for Project Use)

```markdown
## GA Readiness Checklist for [Project Name]

**Date**: YYYY-MM-DD
**Reviewer**: [Name/Role]
**Current Stage**: Beta -> GA

### Entry Validation (Beta Complete)
- [ ] 99.9% uptime demonstrated in beta (30+ days)
- [ ] DR tested successfully (date: ___)
- [ ] Full documentation complete
- [ ] Support processes ready and tested
- [ ] Security compliance certified
- [ ] All quality gate scores met (see thresholds)

### GA Launch Validation
- [ ] Production deployment validated
- [ ] Monitoring & alerting active and tuned
- [ ] On-call rotation staffed and trained
- [ ] Customer support ready (24/7 if required)
- [ ] SLAs published and communicated
- [ ] Rollback procedures tested
- [ ] Communication plan ready (status page, notifications)

### Ongoing Excellence (Monthly Review)
- [ ] SLA compliance: ___% (target: 99.9%+)
- [ ] Security posture reviewed (last: ___)
- [ ] Capacity planning reviewed (runway: ___ days)
- [ ] Customer feedback actioned (items: ___)
- [ ] Technical debt status (critical items: ___)
- [ ] Team knowledge gaps addressed
- [ ] Cost optimization reviewed

### Quarterly Health Check
- [ ] Independent security assessment scheduled/complete
- [ ] DR drill scheduled/complete
- [ ] Performance certification renewed
- [ ] Documentation audit complete
- [ ] Compliance status verified
```

## Related Documents

- [MATURITY-MATRIX.md](../../../../../docs/00-project/strategy/MATURITY-MATRIX.md) - Full scoring framework
- [architecture-stage-policies.md](../../../../docs/01-guides/architecture/architecture-stage-policies.md) - Quality gate policies
- [mvp-stage.md](./mvp-stage.md) - MVP stage definition
- [alpha-stage.md](./alpha-stage.md) - Alpha stage definition
- [beta-stage.md](./beta-stage.md) - Beta stage definition
