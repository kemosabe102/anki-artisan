# ICE Scoring for Technical Debt Prioritization

> Systematic prioritization of technical debt using Impact, Confidence, and Ease scoring.

---

## Overview

ICE (Impact, Confidence, Ease) is a prioritization framework that helps teams
objectively rank technical debt items for remediation. Each factor is scored
1-10, with the product determining priority.

### Formula

```
ICE Score = Impact (1-10) × Confidence (1-10) × Ease (1-10)
```

**Maximum Score**: 1000 (10 × 10 × 10)
**Minimum Score**: 1 (1 × 1 × 1)

---

## Factor Definitions

### Impact (1-10)

> How much will fixing this improve the system?

| Score | Definition | Examples |
|-------|------------|----------|
| 10 | Critical system improvement | Fixes security vulnerability, unblocks scale |
| 8-9 | Major improvement | Significant performance gain, reliability fix |
| 6-7 | Moderate improvement | Notable quality improvement, reduces incidents |
| 4-5 | Minor improvement | Developer experience, minor efficiency |
| 2-3 | Marginal improvement | Code cleanliness, style consistency |
| 1 | Negligible improvement | Cosmetic only |


### Impact Assessment Questions

1. Does this block scalability or security? (+3)
2. Does this cause production incidents? (+2)
3. Does this slow development velocity? (+2)
4. Does this affect user experience? (+1)
5. Is this purely internal/cosmetic? (-2)

### Confidence (1-10)

> How certain are we about the impact and effort estimates?

| Score | Definition | Evidence Level |
|-------|------------|----------------|
| 10 | Certain | Measured data, proven solution |
| 8-9 | Very confident | Strong evidence, similar past work |
| 6-7 | Moderately confident | Some data, reasonable assumptions |
| 4-5 | Uncertain | Limited data, educated guess |
| 2-3 | Speculative | Minimal evidence, hypothesis |
| 1 | Unknown | No data, pure speculation |

### Confidence Assessment Questions

1. Have we measured the current impact? (+2)
2. Have we done similar work before? (+2)
3. Is the solution well-understood? (+2)
4. Are there known risks or unknowns? (-2)
5. Is this based on assumptions? (-2)


### Ease (1-10)

> How easy is it to implement this fix?

| Score | Definition | Effort Level |
|-------|------------|--------------|
| 10 | Trivial | < 1 hour, single file |
| 8-9 | Easy | 1-4 hours, few files |
| 6-7 | Moderate | 1-2 days, multiple components |
| 4-5 | Difficult | 3-5 days, significant changes |
| 2-3 | Hard | 1-2 weeks, cross-cutting |
| 1 | Very hard | > 2 weeks, major refactoring |

### Ease Assessment Questions

1. Is this a single-file change? (+3)
2. Are there tests already? (+2)
3. Is the code well-understood? (+2)
4. Does this require coordination? (-2)
5. Does this touch critical paths? (-2)

---

## Priority Classification

### ICE Score Ranges

| ICE Score | Priority | Classification | Action |
|-----------|----------|----------------|--------|
| 800-1000 | P1 | Must Do | Immediate sprint, blocks progress |
| 500-799 | P2 | Should Do | Next 2-3 sprints, significant value |
| 300-499 | P3 | Could Do | Backlog, address when convenient |
| 100-299 | P4 | Nice to Have | Low priority, opportunistic |
| < 100 | P5 | Won't Do | Defer indefinitely, may close |


### Priority Characteristics

| Priority | Characteristics |
|----------|-----------------|
| P1 | Blocks scalability, security risk, production incidents |
| P2 | Significant improvement, clear ROI, manageable effort |
| P3 | Quality improvement, moderate effort, good value |
| P4 | Nice-to-have, low impact, or high effort |
| P5 | Cosmetic, speculative, or massive effort |

---

## Scoring Examples

### Example 1: Security Vulnerability (P1)

**Item**: SQL injection in user search endpoint

| Factor | Score | Rationale |
|--------|-------|-----------|
| Impact | 10 | Security vulnerability, data breach risk |
| Confidence | 9 | Confirmed via security scan |
| Ease | 7 | Parameterized query, 2-hour fix |

**ICE Score**: 10 × 9 × 7 = **630** (P2, but security escalates to P1)

**Note**: Security issues may be escalated regardless of ICE score.

### Example 2: Performance Optimization (P2)

**Item**: N+1 query in dashboard loading

| Factor | Score | Rationale |
|--------|-------|-----------|
| Impact | 7 | 3s page load reduced to 200ms |
| Confidence | 8 | Measured, known solution |
| Ease | 6 | Requires ORM changes, 1 day |

**ICE Score**: 7 × 8 × 6 = **336** (P3, but high confidence elevates to P2)


### Example 3: Code Refactoring (P3)

**Item**: Extract service from monolithic controller

| Factor | Score | Rationale |
|--------|-------|-----------|
| Impact | 5 | Improves testability, maintainability |
| Confidence | 6 | Reasonable estimate, some unknowns |
| Ease | 5 | 3-day effort, needs careful testing |

**ICE Score**: 5 × 6 × 5 = **150** (P4)

### Example 4: Style Cleanup (P5)

**Item**: Rename variables to follow naming convention

| Factor | Score | Rationale |
|--------|-------|-----------|
| Impact | 2 | Cosmetic, readability only |
| Confidence | 10 | Simple, well-understood |
| Ease | 8 | Automated refactoring tool |

**ICE Score**: 2 × 10 × 8 = **160** (P4, but low impact keeps at P5)

---

## Sprint Grouping Guidance

### Sprint Planning

| Sprint Type | Priority Mix | Focus |
|-------------|--------------|-------|
| Normal | 1 P1, 2-3 P2, 2-3 P3 | Balanced progress |
| Debt Focus | 2 P1, 4-5 P2 | Aggressive reduction |
| Feature Focus | 0-1 P1, 1-2 P2 | Minimal debt work |


### Capacity Allocation

| Stage | Debt Capacity | Rationale |
|-------|---------------|-----------|
| MVP | 10-15% | Accumulate strategically |
| Alpha | 15-20% | Address blocking debt |
| Beta | 20-25% | Reduce before scale |
| RC | 25-30% | Aggressive reduction |
| GA | 10-15% | Maintenance mode |

### Grouping Strategy

1. **Theme Sprints**: Group related debt items
2. **Risk Reduction**: Address P1s first
3. **Quick Wins**: Include some high-ease items
4. **Balanced**: Mix difficulties to avoid burnout

---

## Assessment Template

```markdown
## Technical Debt ICE Assessment

**Date**: [date]
**Assessor**: [name]

### Debt Item: [name]

**Description**: [what is the technical debt]

**Current Impact**: [how it affects the system now]

| Factor | Score | Rationale |
|--------|-------|-----------|
| Impact | X/10 | [explanation] |
| Confidence | X/10 | [explanation] |
| Ease | X/10 | [explanation] |

**ICE Score**: XXX
**Priority**: PX
**Recommended Sprint**: [sprint/quarter]
**Estimated Effort**: [hours/days]
```
