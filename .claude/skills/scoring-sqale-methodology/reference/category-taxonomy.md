# Category Taxonomy Reference

6-category orthogonal classification for technical debt scoring.

---

## Orthogonal Classification Principle

Each issue is counted **ONCE** in exactly one category. No double-counting.

**Assignment Rule**: Classify by primary impact, not secondary effects.

---

## Category Definitions

### 1. Code Quality (Weight: 40%)

**Focus**: Internal code characteristics affecting maintainability.

| Sub-Category | Metrics | Thresholds |
|--------------|---------|------------|
| Complexity | Cyclomatic complexity | <10 per function |
| Duplication | Clone detection % | <5% of codebase |
| Violations | Linter/SAST findings | 0 critical, <10 major |
| Readability | Naming, structure | Subjective review |

**Scoring Formula**:
```
code_quality_score = 100 - (complexity_penalty + duplication_penalty + violation_penalty)
```


### 2. Testing (Weight: 20%)

**Focus**: Test quality and coverage gaps.

| Sub-Category | Metrics | Thresholds |
|--------------|---------|------------|
| Coverage | Line/branch coverage | >80% lines, >70% branches |
| Flakiness | Flaky test rate | <2% of test suite |
| Missing tests | Untested critical paths | 0 for core modules |
| Test quality | Assertion density | >1.5 assertions/test |

### 3. Architecture (Weight: 15%)

**Focus**: Structural qualities affecting evolution.

| Sub-Category | Metrics | Thresholds |
|--------------|---------|------------|
| Coupling | Afferent/efferent coupling | Ca/Ce ratio balanced |
| Cohesion | LCOM (Lack of Cohesion) | LCOM < 0.5 |
| Dependencies | Circular deps, depth | 0 cycles, depth <5 |
| Modularity | Component boundaries | Clear interfaces |

### 4. Documentation (Weight: 10%)

**Focus**: Knowledge capture and accessibility.

| Sub-Category | Metrics | Thresholds |
|--------------|---------|------------|
| Missing docs | Public API coverage | 100% public methods |
| Outdated READMEs | Staleness score | Updated within 90 days |
| Inline comments | Comment density | 10-20% for complex code |
| Architecture docs | ADR presence | Key decisions documented |


### 5. Infrastructure (Weight: 10%)

**Focus**: External dependencies and tooling.

| Sub-Category | Metrics | Thresholds |
|--------------|---------|------------|
| Deprecated APIs | Usage count | 0 deprecated calls |
| Outdated deps | Age, CVEs | <6 months old, 0 CVEs |
| Build system | Build time, reliability | <5 min, >99% success |
| CI/CD health | Pipeline failures | <5% failure rate |

### 6. Design (Weight: 5%)

**Focus**: User-facing patterns and accessibility.

| Sub-Category | Metrics | Thresholds |
|--------------|---------|------------|
| UX patterns | Consistency score | Follows design system |
| Accessibility | WCAG compliance | Level AA minimum |
| API ergonomics | Usability heuristics | Intuitive interfaces |
| Error handling | User-facing messages | Clear, actionable |

---

## Composite Score Formula

```
debt_score = (code_quality x 0.40) + 
             (testing x 0.20) + 
             (architecture x 0.15) + 
             (documentation x 0.10) + 
             (infrastructure x 0.10) + 
             (design x 0.05)
```

**Score Range**: 0-100 (higher = healthier codebase)


---

## Classification Table

| Score | Classification | Interpretation |
|-------|----------------|----------------|
| 81-100 | Low debt | Healthy codebase |
| 61-80 | Moderate debt | Normal maintenance |
| 41-60 | High debt | Active remediation needed |
| 0-40 | Severe debt | Critical intervention |

---

## Example Calculation

**Scenario**: Web application assessment

| Category | Raw Score | Weight | Weighted |
|----------|-----------|--------|----------|
| Code Quality | 70 | 0.40 | 28.0 |
| Testing | 85 | 0.20 | 17.0 |
| Architecture | 60 | 0.15 | 9.0 |
| Documentation | 50 | 0.10 | 5.0 |
| Infrastructure | 75 | 0.10 | 7.5 |
| Design | 80 | 0.05 | 4.0 |

**Composite Score**: 28 + 17 + 9 + 5 + 7.5 + 4 = **70.5**

**Classification**: Moderate debt - Normal maintenance cycle
