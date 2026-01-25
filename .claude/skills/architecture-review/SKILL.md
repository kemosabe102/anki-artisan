---
name: architecture-review
description: >
  Use this skill when reviewing architecture using formal frameworks (TOGAF ACMM, SOLID, NFRs),
  conducting ARB reviews, prioritizing technical debt with ICE scoring, or applying stage-appropriate
  quality gates. Trigger keywords: architecture review, TOGAF, ACMM, SOLID principles, NFR assessment,
  ARB review, technical debt prioritization, ICE scoring, stage gates, maturity assessment.
---

# Architecture Review Skill

> **Domain knowledge for /review-architecture command. Apply formal frameworks with stage-appropriate rigor.**

---

## Contents

1. [Purpose](#purpose)
2. [Quick Reference Tables](#quick-reference-tables)
3. [Framework Summaries](#framework-summaries)
4. [Stage Application](#stage-application)
5. [Scoring Methodology](#scoring-methodology)
6. [References](#references)

---

## Purpose

This skill provides domain knowledge for conducting architecture reviews using industry-standard
frameworks. It enables systematic evaluation of architecture maturity, design quality, and
production readiness with stage-appropriate rigor.

**Primary Use Cases**:
- Architecture maturity assessment (TOGAF ACMM)
- Design quality validation (SOLID principles)
- Non-functional requirements verification (NFR framework)
- Architecture Review Board preparation (ARB process)
- Technical debt prioritization (ICE scoring)
- Stage gate validation (MVP/Alpha/Beta/RC/GA)

---

## Quick Reference Tables

### Framework Selection Matrix

| Need | Framework | Reference |
|------|-----------|-----------|
| Maturity assessment | TOGAF ACMM | [togaf-acmm-assessment.md](references/togaf-acmm-assessment.md) |
| Design quality | SOLID Principles | [solid-principles-checklist.md](references/solid-principles-checklist.md) |
| Production readiness | NFR Framework | [nfr-framework.md](references/nfr-framework.md) |
| Review governance | ARB Process | [arb-process.md](references/arb-process.md) |
| Debt prioritization | ICE Scoring | [ice-prioritization.md](references/ice-prioritization.md) |
| Stage requirements | Stage Matrix | [stage-framework-matrix.md](references/stage-framework-matrix.md) |

### Stage Minimum Thresholds

| Stage | ACMM Level | SOLID Score | NFR Grade | ARB Gate |
|-------|------------|-------------|-----------|----------|
| MVP | L2 | 3.0+ (SRP, DIP) | C+ | ARB1 (optional) |
| Alpha | L3 | 3.5+ (all 5) | B- | ARB1-2 |
| Beta | L3-4 | 4.0+ | B+ | ARB2-3 |
| RC | L4 | 4.2+ | A- | ARB3 |
| GA | L5 | 4.5+ | A | ARB4 |


### Composite Architecture Score

```
Architecture_Score = (ACMM × 0.25) + (SOLID × 0.25) + (NFR × 0.30) + (ARB × 0.20)
```

| Score Range | Rating | Action |
|-------------|--------|--------|
| 4.5+ | Excellent | Proceed to next stage |
| 4.0-4.4 | Good | Minor improvements, proceed |
| 3.5-3.9 | Adequate | Address gaps before proceeding |
| 3.0-3.4 | Poor | Significant rework required |
| < 3.0 | Critical | Architecture redesign needed |

---

## Framework Summaries

### TOGAF ACMM (Architecture Capability Maturity Model)

Evaluates organizational architecture maturity across 9 domains on a 0-5 scale.

**Key Domains**: Process, Development, Business Linkage, Governance, IT Investment,
Communication, Security, Senior Management, Operating Unit Participation

**Stage Mapping**: MVP (L2) -> Alpha (L3) -> Beta (L3-4) -> RC (L4) -> GA (L5)

**Details**: [references/togaf-acmm-assessment.md](references/togaf-acmm-assessment.md)


### SOLID Principles

Design quality checklist validating 5 core OOP principles.

| Principle | Question |
|-----------|----------|
| **S**ingle Responsibility | Does each class/module have exactly one reason to change? |
| **O**pen/Closed | Can components be extended without modifying existing code? |
| **L**iskov Substitution | Are all subclasses substitutable for base classes? |
| **I**nterface Segregation | Are interfaces focused (not forcing unused dependencies)? |
| **D**ependency Inversion | Do high-level modules depend on abstractions? |

**Stage Application**: MVP (SRP, DIP only) -> Alpha+ (full 5 principles)

**Details**: [references/solid-principles-checklist.md](references/solid-principles-checklist.md)

### NFR Framework (Non-Functional Requirements)

8-category assessment with stage-appropriate targets.

**Categories**: Performance, Scalability, Reliability, Security, Maintainability,
Usability, Compatibility, Testability

**Key Metrics**:
- Performance: MVP (<500ms) -> GA (<150ms optimized)
- Reliability: MVP (tracked) -> GA (>99.9%)
- Security: MVP (basic auth) -> GA (continuous scanning)

**Details**: [references/nfr-framework.md](references/nfr-framework.md)


### ARB Process (Architecture Review Board)

4-stage governance process with defined gates and deliverables.

| Stage | Focus | Key Deliverables |
|-------|-------|------------------|
| ARB1 | Pre-Development | Problem statement, requirements, tech stack |
| ARB2 | Pre-Alpha | Architecture doc, ADRs, threat model |
| ARB3 | Alpha->Beta | Code review, monitoring, test results |
| ARB4 | Beta->Production | Operational readiness, SLA/SLO |

**Details**: [references/arb-process.md](references/arb-process.md)

### ICE Prioritization (Technical Debt)

Scoring formula for prioritizing technical debt items.

```
ICE = Impact (1-10) x Confidence (1-10) x Ease (1-10)
```

| ICE Score | Priority | Action |
|-----------|----------|--------|
| 800+ | P1 Must Do | Blocks scalability/security |
| 300-799 | P2 Should Do | Significant improvement |
| 100-299 | P3 Could Do | Nice-to-have |
| < 100 | P4 Won't Do | Low priority |

**Details**: [references/ice-prioritization.md](references/ice-prioritization.md)

---

## Stage Application

### Progressive Framework Application

| Stage | Required Frameworks | Optional | Focus |
|-------|---------------------|----------|-------|
| MVP | SOLID (SRP, DIP), NFR (basic) | ACMM | Speed, core functionality |
| Alpha | Full SOLID, NFR, ARB1-2 | ACMM L3 | Stability, architecture validation |
| Beta | All frameworks | ICE prioritization | Resilience, scale testing |
| RC | All frameworks, full rigor | - | Production simulation |
| GA | All frameworks, continuous | - | Full production readiness |

### Risk Tolerance by Stage

| Stage | Technical Debt | Documentation Gaps | Test Coverage |
|-------|----------------|-------------------|---------------|
| MVP | High tolerance | Acceptable | >50% |
| Alpha | Medium tolerance | Tracked | >70% |
| Beta | Low tolerance | Addressed | >80% |
| RC | Minimal | Complete | >85% |
| GA | Zero new debt | Comprehensive | >85% + chaos |

---

## Scoring Methodology

### Evidence Requirements

Each framework score MUST include supporting evidence:

| Confidence | Evidence Required |
|------------|-------------------|
| HIGH (0.85+) | Code analysis + documentation + test results |
| MEDIUM (0.70-0.84) | Code analysis + partial documentation |
| LOW (<0.70) | Inference only, flag for follow-up |


### Aggregation Formula

```
Framework_Score = Sum(Criterion_Score × Weight) / Sum(Weights)
```

All scores normalized to 1-5 scale before aggregation.

### Output Format

```markdown
## Architecture Review Summary

| Framework | Score | Confidence | Key Findings |
|-----------|-------|------------|--------------|
| TOGAF ACMM | X.X/5 | HIGH/MED/LOW | [summary] |
| SOLID | X.X/5 | HIGH/MED/LOW | [summary] |
| NFR | X.X/5 | HIGH/MED/LOW | [summary] |
| ARB Readiness | X.X/5 | HIGH/MED/LOW | [summary] |

**Composite Score**: X.X/5
**Stage Readiness**: [PASS/WARN/FAIL] for [stage]
**Top 3 Recommendations**: [prioritized list]
```

---

## References

Detailed framework documentation:

- [TOGAF ACMM Assessment](references/togaf-acmm-assessment.md) - Maturity model evaluation
- [SOLID Principles Checklist](references/solid-principles-checklist.md) - Design quality validation
- [NFR Framework](references/nfr-framework.md) - Non-functional requirements assessment
- [ARB Process](references/arb-process.md) - Architecture Review Board governance
- [ICE Prioritization](references/ice-prioritization.md) - Technical debt scoring
- [Stage Framework Matrix](references/stage-framework-matrix.md) - Complete stage-to-framework mapping
