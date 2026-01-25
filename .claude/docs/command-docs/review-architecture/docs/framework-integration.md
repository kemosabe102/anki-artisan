# Framework Integration Guide

How the 5 frameworks integrate with the `/review-architecture` command.

---

## Framework Overview

| Framework | Purpose | Phase Applied | Weight |
|-----------|---------|---------------|--------|
| TOGAF ACMM | Architecture maturity assessment | P2, P3 | 0.20 |
| SOLID | Code design principles | P2, P3 | 0.25 |
| NFR | Non-functional requirements | P2, P3 | 0.40 |
| ARB | Architecture Review Board readiness | P2, P3 | 0.15 |
| ICE | Prioritization scoring | P5 | N/A (prioritization) |

---

## 1. TOGAF ACMM (Architecture Capability Maturity Model)

### Overview

TOGAF ACMM measures organizational architecture maturity across 5 levels.

### Maturity Levels

| Level | Name | Description | Score |
|-------|------|-------------|-------|
| L1 | Initial | Ad-hoc, no formal architecture | 1.0 |
| L2 | Architecture Vision | Basic architecture vision exists | 2.0 |
| L3 | Information Systems | Defined information architecture | 3.0 |
| L4 | Technology | Full technology architecture | 4.0 |
| L5 | Governance | Complete governance framework | 5.0 |


### Stage-Appropriate Application

| Stage | Required TOGAF Level | Assessment Focus |
|-------|---------------------|------------------|
| MVP | L2 (Vision) | Architecture vision documented |
| Alpha | L3 (Information Systems) | Information architecture defined |
| Beta | L3-4 (Technology) | Technology choices documented |
| RC | L4 (Full Technology) | Complete technology architecture |
| GA | L5 (Governance) | Governance processes in place |

### Assessment Criteria

- Architecture documentation exists
- Component boundaries defined
- Integration patterns documented
- Technology decisions recorded (ADRs)
- Governance processes established

---

## 2. SOLID Principles

### Overview

SOLID measures adherence to object-oriented design principles.

### Principles

| Principle | Name | Description |
|-----------|------|-------------|
| S | Single Responsibility | One reason to change per class/module |
| O | Open/Closed | Open for extension, closed for modification |
| L | Liskov Substitution | Subtypes substitutable for base types |
| I | Interface Segregation | Specific interfaces over general ones |
| D | Dependency Inversion | Depend on abstractions, not concretions |


### Stage-Appropriate Application

| Stage | Required Principles | Rationale |
|-------|--------------------|-----------| 
| MVP | SRP, DIP | Core foundations prevent early debt |
| Alpha | Full SOLID | All principles for stability |
| Beta | Full SOLID | Continued enforcement |
| RC | Full SOLID + patterns | Design patterns validation |
| GA | Complete coverage | No exceptions |

### Scoring

```
SOLID Score = 5.0 - (violation_count × 0.5)
Minimum: 0.0
```

### Common Violations

| Violation | Detection Signal |
|-----------|-----------------|
| SRP | Class >300 lines, >5 public methods |
| OCP | Switch statements on type, frequent modifications |
| LSP | Overridden methods with different behavior |
| ISP | Interfaces with >7 methods |
| DIP | Direct instantiation of concrete classes |

---

## 3. NFR Framework (Non-Functional Requirements)

### Overview

NFR framework assesses 10 quality attribute categories.


### NFR Categories

| # | Category | Key Metrics |
|---|----------|-------------|
| 1 | Performance | Response time, throughput, latency |
| 2 | Security | Authentication, authorization, encryption |
| 3 | Reliability | Uptime, MTBF, error rates |
| 4 | Scalability | Horizontal/vertical scaling, load handling |
| 5 | Maintainability | Code complexity, documentation, modularity |
| 6 | Usability | API ergonomics, developer experience |
| 7 | Portability | Platform independence, containerization |
| 8 | Testability | Test coverage, test isolation, mockability |
| 9 | Observability | Logging, monitoring, tracing |
| 10 | Compliance | Regulatory requirements, standards |

### Stage-Appropriate Categories

| Stage | Required Categories | Count |
|-------|--------------------| ------|
| MVP | Performance, Security, Reliability | 3 |
| Alpha | +Scalability, Maintainability, Usability | 6 |
| Beta | +Portability, Testability | 8 |
| RC | All 10 | 10 |
| GA | All 10 + Compliance verification | 10+ |

### Scoring

```
NFR Score = (categories_passing / categories_required) × 5.0
```


### Category Targets by Stage

| Category | MVP | Alpha | Beta | RC | GA |
|----------|-----|-------|------|----|----|
| Performance | P95 <2s | P95 <1s | P95 <500ms | P95 <200ms | P95 <100ms |
| Security | Basic auth | OWASP Top 10 | Pen tested | Audit passed | Certified |
| Reliability | 95% | 99% | 99.5% | 99.9% | 99.99% |
| Test Coverage | - | 70% | 85% | 90% | 95% |

---

## 4. ARB Framework (Architecture Review Board)

### Overview

ARB framework measures readiness for formal architecture governance.

### ARB Levels

| Level | Name | Description | Score |
|-------|------|-------------|-------|
| - | None | No formal review | 0.0 |
| ARB1 | Initial Review | Basic architecture documented | 1.25 |
| ARB2 | Design Review | Detailed design reviewed | 2.50 |
| ARB3 | Implementation Review | Implementation validated | 3.75 |
| ARB4 | Production Review | Production-ready certified | 5.00 |

### Stage-Appropriate Application

| Stage | Required ARB Level | Gates |
|-------|-------------------|-------|
| MVP | None | - |
| Alpha | ARB1-2 | Architecture documented, design reviewed |
| Beta | ARB2-3 | Implementation validated |
| RC | ARB3 | Full implementation review |
| GA | ARB4 | Production certification |


### ARB Gate Criteria

| Gate | Required Artifacts |
|------|-------------------|
| ARB1 | Architecture vision, component diagram, ADRs |
| ARB2 | Detailed design docs, interface specs, NFR targets |
| ARB3 | Implementation review, test results, performance benchmarks |
| ARB4 | Production runbook, monitoring dashboards, SLA definitions |

---

## 5. ICE Scoring Methodology

### Overview

ICE prioritizes findings by Impact, Confidence, and Ease.

### Dimensions

| Dimension | Question | Scale |
|-----------|----------|-------|
| Impact | How much improvement? | 1-10 (10=transformative) |
| Confidence | How certain is the issue? | 1-10 (10=definite) |
| Ease | How easy to fix? | 1-10 (10=trivial) |

### Calculation

```
ICE Score = (Impact × Confidence × Ease) / 10
Range: 0.1 to 100.0
```

### Priority Mapping

| ICE Score | Priority | Action Urgency |
|-----------|----------|----------------|
| >= 7.0 | P1 (Critical) | Immediate action required |
| 5.0 - 6.9 | P2 (High) | Address in current sprint |
| 3.0 - 4.9 | P3 (Medium) | Plan for next sprint |
| < 3.0 | P4 (Low) | Backlog consideration |


### Override Rules

- Any critical risk -> P1 regardless of ICE score
- Any high risk -> P2 minimum regardless of ICE score

---

## Stage-Framework Summary Matrix

Complete matrix showing framework requirements by stage:

| Stage | SOLID | NFR Count | TOGAF | ARB | Min Score | Grade |
|-------|-------|-----------|-------|-----|-----------|-------|
| MVP | SRP, DIP | 3 | L2 | - | 3.5 | C |
| Alpha | Full | 6 | L3 | ARB1-2 | 3.7 | B- |
| Beta | Full | 8 | L3-4 | ARB2-3 | 3.8 | B |
| RC | Full+patterns | 10 | L4 | ARB3 | 4.0 | B+ |
| GA | Complete | 10+compliance | L5 | ARB4 | 4.2 | A- |

---

## Composite Score Calculation

### Formula

```
Composite = (SOLID × 0.25) + (NFR × 0.40) + (TOGAF × 0.20) + (ARB × 0.15)
```

### Weight Rationale

| Framework | Weight | Rationale |
|-----------|--------|-----------|
| NFR | 0.40 | Highest impact on production quality |
| SOLID | 0.25 | Foundation for maintainability |
| TOGAF | 0.20 | Organizational maturity indicator |
| ARB | 0.15 | Governance readiness |

### Grade Mapping

| Score Range | Grade |
|-------------|-------|
| 4.5 - 5.0 | A |
| 4.0 - 4.49 | B+ |
| 3.5 - 3.99 | B |
| 3.0 - 3.49 | C |
| 2.0 - 2.99 | D |
| < 2.0 | F |
