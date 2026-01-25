# Scoring Rubric Summary

> Condensed from `architecture-scoring-rubric.md`. Use for quick reference during reviews.

---

## 5-Point Scale Anchor Definitions

### Score 5 - Excellent (Industry Leading)

- **Performance**: Exceeds all industry standards and stage requirements
- **Quality**: Research-validated patterns, comprehensive documentation, proactive optimization
- **Evidence**: Multiple authoritative sources, peer validation, measurable benefits
- **Business Impact**: Competitive advantage, innovation leadership, risk mitigation
- **Exemplar**: Microservices with full observability, auto-scaling, chaos engineering

### Score 4 - Good (Meets All Standards)

- **Performance**: Meets all standards with minor enhancement opportunities
- **Quality**: Well-documented patterns, adequate coverage, standard compliance
- **Evidence**: Authoritative sources, clear documentation, proven approach
- **Business Impact**: Reliable delivery, acceptable risk, standard industry practice
- **Exemplar**: Monolithic architecture with proper separation of concerns and monitoring

### Score 3 - Adequate (Meets Minimum Requirements)

- **Performance**: Meets minimum requirements for current maturity stage
- **Quality**: Basic documentation, essential patterns, some gaps acceptable
- **Evidence**: Sufficient sources, basic documentation, functional approach
- **Business Impact**: Delivers core value, manageable risk, requires improvement planning
- **Exemplar**: Basic service architecture with fundamental logging and error handling

### Score 2 - Poor (Below Standards)

- **Performance**: Below minimum standards, significant improvements required
- **Quality**: Incomplete documentation, pattern violations, multiple gaps
- **Evidence**: Limited sources, insufficient documentation, questionable approach
- **Business Impact**: Delivery risk, elevated technical debt, requires immediate attention
- **Exemplar**: Tightly coupled architecture with minimal error handling

### Score 1 - Critical (Major Deficiencies)

- **Performance**: Major deficiencies that block stage progression
- **Quality**: Missing documentation, anti-patterns, critical gaps
- **Evidence**: No authoritative backing, inadequate documentation, flawed approach
- **Business Impact**: Delivery failure risk, unacceptable technical debt, requires redesign
- **Exemplar**: Monolithic architecture with no error handling, logging, or separation

---

## Criteria Weights

| Criterion | Weight | Key Focus |
|-----------|--------|-----------|
| Architecture Soundness | 0.30 | Design integrity, pattern compliance, scalability |
| Implementation Readiness | 0.25 | Detail sufficiency, task decomposition, traceability |
| Production Readiness | 0.20 | Cloud readiness, monitoring, security, operational |
| Integration Coherence | 0.10 | Cross-plan consistency, interface design, data flow |
| Risk Mitigation | 0.05 | Risk identification, mitigation strategies, debt management |

---

## Stage Thresholds

| Stage | Min Score | Focus |
|-------|-----------|-------|
| MVP | 3.5+ | Speed & Feasibility |
| Alpha | 3.7+ | Stabilize Core |
| Beta | 3.8+ | Resilience & Scale |
| GA | 4.2+ | Full Rigor |

---

## Inter-Rater Reliability

- **Target**: >= 0.90 Krippendorff's Alpha
- **Variance Threshold**: Trigger review if scores differ by >1 point
- **Calibration**: Quarterly reviewer calibration sessions

**Full rubric**: `.claude/docs/01-guides/architecture/architecture-scoring-rubric.md`
