# Stage-to-Framework Mapping Matrix

> Complete matrix showing which frameworks apply at each development stage.

---

## Overview

This matrix defines which architecture review frameworks are required, optional,
or not applicable at each development stage. It provides minimum thresholds,
required validations, and risk tolerance levels for progressive quality gates.

---

## Framework Application Matrix

### TOGAF ACMM (Architecture Capability Maturity Model)

| Stage | Status | Minimum Level | Domains Required | Focus |
|-------|--------|---------------|------------------|-------|
| MVP | Optional | L2 | Process, Development | Basic structure |
| Alpha | Required | L3 | Core 5 domains | Formal practices |
| Beta | Required | L3-4 | All 9 domains | Measurement begins |
| RC | Required | L4 | All 9 domains | Optimization |
| GA | Required | L5 | All 9 domains | Excellence |

### SOLID Principles

| Stage | Status | Principles | Minimum Score | Focus |
|-------|--------|------------|---------------|-------|
| MVP | Required | SRP, DIP only | 3.0 | Foundation |
| Alpha | Required | All 5 | 3.5 | Full validation |
| Beta | Required | All 5 | 4.0 | Quality |
| RC | Required | All 5 | 4.2 | Polish |
| GA | Required | All 5 | 4.5 | Excellence |


### NFR Framework

| Stage | Status | Categories | Minimum Grade | Focus |
|-------|--------|------------|---------------|-------|
| MVP | Required | Basic 4 | C+ | Functional |
| Alpha | Required | All 8 | B- | Comprehensive |
| Beta | Required | All 8 | B+ | Scale-ready |
| RC | Required | All 8 | A- | Production-like |
| GA | Required | All 8 | A | Production |

**Basic 4**: Performance, Reliability, Security, Testability

### ARB Process

| Stage | Status | Required Gates | Focus |
|-------|--------|----------------|-------|
| MVP | Optional | ARB1 | Validate approach |
| Alpha | Required | ARB1, ARB2 | Architecture |
| Beta | Required | ARB2, ARB3 | Implementation |
| RC | Required | ARB3 | Readiness |
| GA | Required | ARB4 | Production |

### ICE Prioritization

| Stage | Status | Application | Focus |
|-------|--------|-------------|-------|
| MVP | Optional | Track debt | Awareness |
| Alpha | Optional | Score debt | Prioritization |
| Beta | Required | Active reduction | P1/P2 focus |
| RC | Required | Aggressive reduction | Clear P1s |
| GA | Required | Maintenance | Continuous |

---


## Minimum Thresholds Summary

### Composite Score Requirements

| Stage | ACMM | SOLID | NFR | ARB | Composite Min |
|-------|------|-------|-----|-----|---------------|
| MVP | 2.0 | 3.0 | 2.5 (C+) | N/A | 3.0 |
| Alpha | 3.0 | 3.5 | 3.0 (B-) | 3.5 | 3.5 |
| Beta | 3.5 | 4.0 | 3.5 (B+) | 4.0 | 3.8 |
| RC | 4.0 | 4.2 | 4.0 (A-) | 4.0 | 4.0 |
| GA | 4.5 | 4.5 | 4.5 (A) | 4.5 | 4.5 |

### Stage Transition Gates

| Transition | Required Frameworks | Must Pass |
|------------|---------------------|-----------|
| MVP → Alpha | SOLID, NFR basic | All minimums |
| Alpha → Beta | All + ARB2 | ARB2 approval |
| Beta → RC | All + ARB3 | ARB3 approval |
| RC → GA | All + ARB4 | ARB4 GO decision |

---

## Required Validations by Stage

### MVP Stage

| Framework | Required Validation |
|-----------|---------------------|
| SOLID | SRP + DIP code review |
| NFR | Performance baseline, basic security |
| ARB | Problem statement documented |
| ICE | Debt items identified |


### Alpha Stage

| Framework | Required Validation |
|-----------|---------------------|
| ACMM | 9-domain assessment |
| SOLID | Full 5-principle review |
| NFR | All 8 categories assessed |
| ARB | ARB1 + ARB2 completed |
| ICE | Debt scored and prioritized |

### Beta Stage

| Framework | Required Validation |
|-----------|---------------------|
| ACMM | L3-4 across all domains |
| SOLID | No score below 3.5 |
| NFR | Scale testing complete |
| ARB | ARB3 scheduled |
| ICE | P1 items addressed |

### RC Stage

| Framework | Required Validation |
|-----------|---------------------|
| ACMM | L4 minimum |
| SOLID | No score below 4.0 |
| NFR | Production simulation |
| ARB | ARB3 approved |
| ICE | Zero P1, P2 plan |

### GA Stage

| Framework | Required Validation |
|-----------|---------------------|
| ACMM | L5 target |
| SOLID | 4.5+ average |
| NFR | SLOs defined and proven |
| ARB | ARB4 GO |
| ICE | Maintenance mode |


---

## Risk Tolerance Levels

### By Stage

| Stage | Technical Debt | Documentation | Test Coverage | Security |
|-------|----------------|---------------|---------------|----------|
| MVP | High (50%+) | Minimal | > 50% | Basic auth |
| Alpha | Medium (30-50%) | Key decisions | > 70% | OWASP mapped |
| Beta | Low (20-30%) | Comprehensive | > 80% | Pen tested |
| RC | Minimal (10-20%) | Complete | > 85% | Remediated |
| GA | Zero new (< 10%) | Maintained | > 85% | Continuous |

### Risk Escalation

| Risk Level | Allowed At | Action |
|------------|------------|--------|
| Critical | Never | Block release, immediate fix |
| High | MVP only | Track, plan remediation |
| Medium | MVP, Alpha | Address before Beta |
| Low | Any | Address opportunistically |

---

## Stage Transition Criteria

### MVP to Alpha

- [ ] SOLID score >= 3.0 (SRP, DIP)
- [ ] NFR basic assessment complete
- [ ] Core functionality working
- [ ] Architecture approach validated
- [ ] Major risks identified

### Alpha to Beta

- [ ] ACMM L3 achieved
- [ ] SOLID full 5 >= 3.5
- [ ] NFR all 8 >= B-
- [ ] ARB2 approved
- [ ] All P1 debt addressed


### Beta to RC

- [ ] ACMM L4 achieved
- [ ] SOLID >= 4.2 average
- [ ] NFR >= A-
- [ ] ARB3 approved
- [ ] Scale testing passed
- [ ] Security remediation complete

### RC to GA

- [ ] ACMM L5 target
- [ ] SOLID >= 4.5 average
- [ ] NFR A grade
- [ ] ARB4 GO decision
- [ ] SLOs proven in production simulation
- [ ] Zero P1 debt, P2 plan in place
- [ ] Operational readiness confirmed

---

## Quick Reference Card

```
+-------+-------+-------+-------+-------+-------+
| Stage | ACMM  | SOLID | NFR   | ARB   | ICE   |
+-------+-------+-------+-------+-------+-------+
| MVP   | L2?   | 3.0*  | C+    | ARB1? | Track |
| Alpha | L3    | 3.5   | B-    | ARB2  | Score |
| Beta  | L3-4  | 4.0   | B+    | ARB3  | Fix   |
| RC    | L4    | 4.2   | A-    | ARB3+ | Clear |
| GA    | L5    | 4.5   | A     | ARB4  | Maint |
+-------+-------+-------+-------+-------+-------+

? = Optional   * = SRP+DIP only at MVP
```
