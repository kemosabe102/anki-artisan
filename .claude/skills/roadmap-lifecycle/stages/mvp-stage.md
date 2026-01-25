# MVP Stage Definition

## Overview

- **Score Range**: 1.0 - 3.4
- **Focus**: Speed & Feasibility - prove core concept works, validate with early adopters
- **Risk Tolerance**: Medium
- **Business Context**: Proof of concept, market validation, early feedback collection

## Entry Criteria

What must be true to BE at MVP stage:

- [ ] Project concept defined and documented
- [ ] Core problem statement clear and validated
- [ ] Target users identified
- [ ] Initial team/owner assigned
- [ ] Success metrics defined (top 3 pain points to address)
- [ ] Basic technology stack selected
- [ ] Development environment established

## Exit Criteria

What must be true to LEAVE MVP and enter Alpha:

- [ ] Core functionality working end-to-end
- [ ] Basic error handling implemented
- [ ] Top 3 customer pain points addressed
- [ ] Deployment process documented
- [ ] Cost per operation measured
- [ ] Technical debt documented (acceptable if planned for resolution)
- [ ] Basic security review completed (no critical vulnerabilities)
- [ ] 95% of functional requirements traced
- [ ] Ready for internal team testing

## Quality Thresholds

### Minimum Scores

| Metric | Minimum | Notes |
|--------|---------|-------|
| Overall Score | 3.5 | Architecture review overall |
| Weighted Score | 3.4 | Weighted by criteria importance |
| Required Grade | C | Minimum passing grade |
| Architecture Soundness | 3.0 | Core structure adequate |
| Implementation Readiness | 3.5 | Code ready for basic use |
| Production Readiness | 2.5 | Local/dev deployment OK |

### Dimension Requirements

| Dimension | Score Range | Evidence Required |
|-----------|-------------|-------------------|
| Architecture | 1-3 | Minimal viable modules, simplest schemas, monolith OK |
| Data & Migrations | 1-3 | v0 schemas, manual migrations OK, SQLite acceptable |
| Observability | 1-3 | Console logs, basic errors logged, manual monitoring |
| Testing | 1-3 | Unit tests for critical paths, smoke tests, 40% coverage OK |
| Release & Deployment | 1-3 | Manual deployment, local/dev only, git tags for versions |
| Security | 1-3 | Secrets in env vars, basic auth OK, HTTPS only, no PII logging |
| Capacity & Cost | 1-3 | Local estimates, single instance, manual scaling |
| Documentation | 1-3 | README basics, inline comments, single owner OK |
| LLM Integration | 1-3 | Single model, basic prompts, no versioning, manual testing |

### Risk Limits

| Risk Level | Allowed Count | Notes |
|------------|---------------|-------|
| Critical | 0 | No critical risks permitted |
| High | Up to 2 | Must have documented mitigation plan |
| Medium | Acceptable | Track and monitor |
| Low | Acceptable | Document for awareness |

**Technical Debt**: Acceptable if documented and planned for resolution in later stages.

## Stage-Specific Focus Areas

### DO at MVP

- Prove core concept works with real users
- Validate problem-solution fit with early adopters
- Ship fast, learn fast, iterate quickly
- Accept technical debt (must be documented)
- Focus on working software that solves pain points
- Use simplest possible architecture (monolith OK)
- Hard-coded configs acceptable
- Manual processes acceptable

### DEFER to Later Stages

- Microservices architecture (defer to Beta+)
- Complex abstractions and design patterns
- Auto-scaling infrastructure
- Comprehensive documentation and wikis
- Performance optimization
- Distributed tracing and APM tools
- Complex CI/CD pipelines
- Multiple environments
- Online migrations and sharding
- Multi-model LLM orchestration
- Complex agent workflows

## Anti-Patterns (NEVER at MVP)

| Anti-Pattern | Why It's Wrong | Do This Instead |
|--------------|----------------|-----------------|
| Building for scale before proving value | Wastes resources on unvalidated concept | Prove concept first, scale later |
| Microservices for simple problems | Unnecessary complexity | Use monolith until boundaries clear |
| Extensive documentation before stable interfaces | Documentation will be outdated immediately | Inline comments, basic README |
| Complex CI/CD for single-instance apps | Over-engineering deployment | Manual deployment, git tags |
| Multi-model LLM orchestration | Premature optimization | Single model, basic prompts |
| 100% test coverage goals | Slows velocity without proven value | 40% coverage on critical paths |
| Complex ORMs and multi-DB support | Unnecessary abstraction | Simple queries, single DB type |
| Kubernetes for single instance | Infrastructure over-engineering | Local/dev deployment sufficient |

## Validation Requirements

### Mandatory

- [ ] Basic functionality testing (smoke tests)
- [ ] Core requirement coverage validation
- [ ] Essential security review (no hardcoded secrets, HTTPS)
- [ ] Basic integration testing (critical paths only)

### Optional (defer if needed)

- Performance testing
- Load testing
- Security penetration testing
- Usability testing
- Chaos engineering
- Multi-environment validation

## Traceability Requirements

| Requirement | Threshold | Notes |
|-------------|-----------|-------|
| Coverage Minimum | 95% | Functional requirements traced |
| Missing Link Tolerance | Up to 3 | Non-critical links only |
| Validation Method | Manual OK | Automated preferred but not required |
| Documentation Level | Basic | Requirement descriptions sufficient |

## Checklist Template

Copy this checklist for project use:

```markdown
## MVP Readiness Checklist for [Project Name]

**Assessment Date:** YYYY-MM-DD
**Assessed By:** [Name/Role]

### Entry Validation

- [ ] Problem statement documented
- [ ] Target users identified
- [ ] Success metrics defined (top 3 pain points)
- [ ] Technology stack selected
- [ ] Development environment ready
- [ ] Initial team/owner assigned

### Quality Gate Validation

- [ ] Overall score >= 3.5
- [ ] Architecture soundness >= 3.0
- [ ] Implementation readiness >= 3.5
- [ ] Production readiness >= 2.5
- [ ] 0 critical risks
- [ ] <= 2 high risks (with mitigation documented)

### Exit Validation (Ready for Alpha)

- [ ] Core functionality working end-to-end
- [ ] Basic error handling implemented
- [ ] Top 3 customer pain points addressed
- [ ] Deployment process documented
- [ ] Cost per operation measured
- [ ] Technical debt documented
- [ ] Basic security review passed
- [ ] 95% requirement traceability achieved
- [ ] Ready for internal team testing
```

---

**Related Documents:**
- [MATURITY-MATRIX.md](../../../../docs/00-project/strategy/MATURITY-MATRIX.md) - Full scoring framework
- [architecture-stage-policies.md](../../../docs/01-guides/architecture/architecture-stage-policies.md) - Quality gate policies
