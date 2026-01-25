# Non-Functional Requirements (NFR) Framework

> 8-category assessment with stage-appropriate targets for production readiness.

---

## Overview

Non-functional requirements define system qualities beyond features. This framework
provides stage-appropriate targets for 8 key NFR categories.

| Category | Focus | Key Metric |
|----------|-------|------------|
| Performance | Speed | Response time (ms) |
| Scalability | Growth | Concurrent users/requests |
| Reliability | Uptime | Availability % |
| Security | Protection | Vulnerability count |
| Maintainability | Code health | Technical debt ratio |
| Usability | User experience | Task success rate |
| Compatibility | Integration | API compatibility % |
| Testability | Quality assurance | Code coverage % |

---

## 1. Performance

> System responsiveness under normal load.

### Stage-Appropriate Targets

| Stage | P95 Response Time | Throughput | Rationale |
|-------|-------------------|------------|-----------|
| MVP | < 500ms | Baseline measured | Functional, not optimized |
| Alpha | < 500ms | Baseline + 20% | Stable performance |
| Beta | < 200ms | 2x baseline | Optimized for scale |
| RC | < 150ms | 5x baseline | Production simulation |
| GA | < 150ms + optimization | 10x baseline | Full production |


### Assessment Questions

1. Are response time SLOs defined?
2. Is performance monitoring in place?
3. Are there performance tests in CI/CD?
4. Have bottlenecks been identified and addressed?
5. Is there capacity planning documentation?

### Scoring Rubric

| Score | Criteria |
|-------|----------|
| 5 | Exceeds targets, proactive optimization, APM in place |
| 4 | Meets all targets, monitoring active |
| 3 | Meets minimum, some gaps in monitoring |
| 2 | Below targets, reactive only |
| 1 | No performance consideration |

---

## 2. Scalability

> System ability to handle growth.

### Stage-Appropriate Targets

| Stage | Scale Target | Approach | Rationale |
|-------|--------------|----------|-----------|
| MVP | Conceptual only | Document scaling strategy | Validate approach |
| Alpha | 10k users mapped | Horizontal scaling designed | Architecture validated |
| Beta | 10x tested | Load testing complete | Scale verified |
| RC | Auto-scaling | Dynamic scaling operational | Production-ready |
| GA | 100x proven | Multi-region capable | Full production |


### Assessment Questions

1. Is there a documented scaling strategy?
2. Are stateless components designed for horizontal scaling?
3. Has load testing been performed?
4. Is auto-scaling configured?
5. Are there bottleneck components that limit scale?

### Scoring Rubric

| Score | Criteria |
|-------|----------|
| 5 | Proven at 100x, auto-scaling, multi-region |
| 4 | Load tested at 10x, auto-scaling ready |
| 3 | Scaling strategy documented, basic testing |
| 2 | Limited scaling consideration |
| 1 | Monolithic, no scaling path |

---

## 3. Reliability

> System availability and fault tolerance.

### Stage-Appropriate Targets

| Stage | Availability | Recovery | Rationale |
|-------|--------------|----------|-----------|
| MVP | Tracked | Manual recovery OK | Baseline established |
| Alpha | > 95% | Documented procedures | Basic reliability |
| Beta | > 99% | Automated recovery | Production-like |
| RC | > 99.5% | < 15 min RTO | Near-production |
| GA | > 99.9% | < 5 min RTO, tested | Full SLA |


### Assessment Questions

1. Are SLOs/SLIs defined and monitored?
2. Is there redundancy for critical components?
3. Are failure modes documented?
4. Is there a disaster recovery plan?
5. Has chaos engineering been performed?

### Scoring Rubric

| Score | Criteria |
|-------|----------|
| 5 | > 99.9%, chaos tested, automated recovery |
| 4 | > 99%, redundancy, documented recovery |
| 3 | > 95%, basic monitoring |
| 2 | Uptime tracked, manual recovery |
| 1 | No reliability measures |

---

## 4. Security

> System protection against threats.

### Stage-Appropriate Targets

| Stage | Requirement | Validation | Rationale |
|-------|-------------|------------|-----------|
| MVP | Basic auth/authz | Code review | Minimal protection |
| Alpha | OWASP Top 10 mapped | Security review | Known vulnerabilities |
| Beta | Pen tested | External audit | Professional validation |
| RC | Remediation complete | Re-test | Issues addressed |
| GA | Continuous scanning | Automated | Ongoing protection |


### Assessment Questions

1. Is authentication/authorization implemented?
2. Are secrets properly managed?
3. Is data encrypted at rest and in transit?
4. Has OWASP Top 10 been reviewed?
5. Is there a security incident response plan?

### Scoring Rubric

| Score | Criteria |
|-------|----------|
| 5 | Continuous scanning, zero critical, SOC2/ISO27001 |
| 4 | Pen tested, issues remediated |
| 3 | OWASP mapped, basic protections |
| 2 | Auth implemented, gaps exist |
| 1 | No security consideration |

---

## 5. Maintainability

> Ease of system modification and support.

### Stage-Appropriate Targets

| Stage | Requirement | Metric | Rationale |
|-------|-------------|--------|-----------|
| MVP | Exists | Debt tracked | Acknowledge debt |
| Alpha | Style enforced | Linting active | Consistent code |
| Beta | Debt tracked | < 30% ratio | Managed debt |
| RC | Debt prioritized | < 25% ratio | Reduction plan |
| GA | Debt < 20% | Continuous improvement | Sustainable |


### Assessment Questions

1. Is code following consistent style guidelines?
2. Is technical debt tracked and prioritized?
3. Are there automated code quality checks?
4. Is documentation maintained alongside code?
5. Is the codebase modular and decoupled?

### Scoring Rubric

| Score | Criteria |
|-------|----------|
| 5 | < 20% debt, continuous improvement, excellent docs |
| 4 | < 25% debt, tracked, good documentation |
| 3 | < 30% debt, linting active |
| 2 | Debt acknowledged, some standards |
| 1 | No maintainability consideration |

---

## 6. Usability

> User experience quality.

### Stage-Appropriate Targets

| Stage | Requirement | Metric | Rationale |
|-------|-------------|--------|-----------|
| MVP | Core tested | Task completion | Basic usability |
| Alpha | > 80% success | User testing done | Validated UX |
| Beta | Feedback integrated | NPS > 20 | Improved UX |
| RC | Polish complete | NPS > 25 | Production-ready |
| GA | NPS > 30 | Continuous feedback | Excellent UX |


### Assessment Questions

1. Has user testing been conducted?
2. Are accessibility standards (WCAG) considered?
3. Is there a feedback mechanism?
4. Are error messages user-friendly?
5. Is the interface consistent across features?

### Scoring Rubric

| Score | Criteria |
|-------|----------|
| 5 | NPS > 30, WCAG AA, continuous feedback |
| 4 | NPS > 25, user tested, accessible |
| 3 | > 80% task success, basic testing |
| 2 | Core flows tested |
| 1 | No usability consideration |

---

## 7. Compatibility

> Integration with other systems.

### Stage-Appropriate Targets

| Stage | Requirement | Validation | Rationale |
|-------|-------------|------------|-----------|
| MVP | Defined | API contracts | Clear interfaces |
| Alpha | > 95% | Integration tests | Verified integration |
| Beta | > 99% | Consumer tests | Stable contracts |
| RC | Backward tested | Version compatibility | Safe upgrades |
| GA | Full compatibility | Continuous testing | Production stable |


### Assessment Questions

1. Are API contracts documented (OpenAPI, etc.)?
2. Is there versioning strategy?
3. Are breaking changes managed?
4. Is there consumer-driven contract testing?
5. Are third-party integrations abstracted?

### Scoring Rubric

| Score | Criteria |
|-------|----------|
| 5 | Full backward compatibility, CDC testing |
| 4 | > 99% compatibility, versioned APIs |
| 3 | > 95% compatibility, documented contracts |
| 2 | Contracts defined |
| 1 | No compatibility consideration |

---

## 8. Testability

> Ease of validating system behavior.

### Stage-Appropriate Targets

| Stage | Coverage | Test Types | Rationale |
|-------|----------|------------|-----------|
| MVP | > 50% | Unit tests | Basic coverage |
| Alpha | > 70% | Unit + integration | Comprehensive |
| Beta | > 80% | Full pyramid | Production-like |
| RC | > 85% | + performance | Pre-production |
| GA | > 85% + chaos | Full suite | Production proven |


### Assessment Questions

1. Is code designed for testability (DI, interfaces)?
2. Is test coverage measured and enforced?
3. Are tests part of CI/CD pipeline?
4. Is there a test pyramid (unit > integration > e2e)?
5. Are edge cases and error paths tested?

### Scoring Rubric

| Score | Criteria |
|-------|----------|
| 5 | > 85%, chaos tested, mutation testing |
| 4 | > 80%, full pyramid, CI integrated |
| 3 | > 70%, unit + integration |
| 2 | > 50%, unit tests only |
| 1 | No testing strategy |

---

## Scoring Methodology

### Per-Category Scoring

1. Evaluate against stage-appropriate targets
2. Score 1-5 based on rubric
3. Document evidence and confidence

### Aggregate NFR Score

```
NFR_Score = Sum(Category_Scores) / 8
```

### Weighted Scoring (Domain-Specific)

| Category | Default | API Focus | User Focus | Data Focus |
|----------|---------|-----------|------------|------------|
| Performance | 0.15 | 0.20 | 0.10 | 0.15 |
| Scalability | 0.10 | 0.15 | 0.05 | 0.15 |
| Reliability | 0.15 | 0.15 | 0.10 | 0.20 |
| Security | 0.15 | 0.15 | 0.15 | 0.20 |
| Maintainability | 0.15 | 0.10 | 0.10 | 0.10 |
| Usability | 0.10 | 0.05 | 0.30 | 0.05 |
| Compatibility | 0.10 | 0.15 | 0.10 | 0.10 |
| Testability | 0.10 | 0.05 | 0.10 | 0.05 |


### Grade Mapping

| Score Range | Grade | Interpretation |
|-------------|-------|----------------|
| 4.5 - 5.0 | A | Excellent, exceeds requirements |
| 4.0 - 4.4 | A- | Very good, meets all requirements |
| 3.5 - 3.9 | B+ | Good, minor gaps |
| 3.0 - 3.4 | B- | Adequate, some improvement needed |
| 2.5 - 2.9 | C+ | Below standard, significant gaps |
| 2.0 - 2.4 | C | Poor, major improvement required |
| < 2.0 | F | Critical, redesign needed |

---

## Assessment Template

```markdown
## NFR Assessment

**Project**: [name]
**Date**: [date]
**Stage**: [MVP/Alpha/Beta/RC/GA]

### Category Scores

| Category | Score | Grade | Confidence | Key Findings |
|----------|-------|-------|------------|--------------|
| Performance | X/5 | X | HIGH/MED/LOW | [notes] |
| Scalability | X/5 | X | HIGH/MED/LOW | [notes] |
| Reliability | X/5 | X | HIGH/MED/LOW | [notes] |
| Security | X/5 | X | HIGH/MED/LOW | [notes] |
| Maintainability | X/5 | X | HIGH/MED/LOW | [notes] |
| Usability | X/5 | X | HIGH/MED/LOW | [notes] |
| Compatibility | X/5 | X | HIGH/MED/LOW | [notes] |
| Testability | X/5 | X | HIGH/MED/LOW | [notes] |

### Aggregate Score: X.X/5 (Grade: X)

### Stage Readiness: [PASS/WARN/FAIL]

### Priority Improvements
1. [category]: [action]
2. [category]: [action]
3. [category]: [action]
```
