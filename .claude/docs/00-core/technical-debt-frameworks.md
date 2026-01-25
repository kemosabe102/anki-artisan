---
title: "Technical Debt Assessment Frameworks"
date: 2025-11-08
status: ACTIVE
tags: [claude-docs]
---
# Technical Debt Assessment Frameworks

**Purpose**: Reference guide for technical debt evaluation methodologies used by tech-debt-investigator agent

**Auto-Load**: Referenced by tech-debt-investigator during ORIENT phase

---

## 1. Debt Category Taxonomy (SQALE-Inspired)

**Orthogonal Classification Principle**: Each debt item counted once in exactly one category to prevent double-counting.

### Six Debt Categories

1. **Code Quality Debt**
   - Code smells (long methods, deep nesting, magic numbers)
   - High cyclomatic complexity
   - Code duplication
   - Coding standard violations
   - Poor naming, lack of comments

2. **Architectural Debt**
   - Tight coupling between components
   - Monolithic structures requiring modularization
   - Scalability bottlenecks
   - Dependency hell (outdated libraries, circular dependencies)
   - Poor separation of concerns

3. **Testing Debt**
   - Low test coverage (<80% target)
   - Missing unit/integration tests for critical paths
   - Fragile/flaky tests
   - Over-reliance on manual testing
   - Outdated or broken tests

4. **Documentation Debt**
   - Missing or outdated documentation
   - Lack of inline code comments
   - Missing docstrings
   - Tribal knowledge concentration
   - Outdated README files

5. **Infrastructure Debt**
   - Hard-coded configurations
   - Deprecated Kubernetes API versions
   - Unpatched dependencies with CVEs
   - Manual CI/CD steps
   - Missing monitoring/observability

6. **Design/UI Debt**
   - UX inconsistencies
   - Duplicated UI code
   - Accessibility gaps
   - Inconsistent design patterns
   - Poor responsive design

---

## 2. SQALE Methodology (Remediation Cost Approach)

**Source**: SonarQube standard, used by 50,000+ companies

### Core Principles

1. **Atomic Requirements**: Each quality rule is verifiable (e.g., "cyclomatic complexity ≤10")
2. **Additive Debt**: Sum remediation costs, don't average scores
3. **Orthogonal Categories**: Each violation counted once

### Technical Debt Ratio (TDR)

```
TDR = (Total Remediation Cost) / (Development Cost)

Where:
- Remediation Cost = Sum of hours to fix all violations
- Development Cost = Total hours invested in codebase
```

**Default Estimation**: 30 minutes per line of code (SQALE standard)

### Rating Scale

| Grade | TDR Range | Interpretation |
|-------|-----------|----------------|
| **A** | ≤5% | Excellent maintainability |
| **B** | 6-10% | Good maintainability |
| **C** | 11-20% | Moderate debt |
| **D** | 21-50% | High debt |
| **E** | >50% | Severe debt |

**Target**: Keep TDR <5% for healthy codebases

### Remediation Cost Estimates (Per Violation Type)

| Violation Type | Fix Time | Example |
|----------------|----------|---------|
| Code smell (minor) | 5-15 min | Magic number, short variable name |
| Code smell (major) | 30-60 min | Long method, deep nesting |
| High complexity | 1-2 hours | Refactor complex function |
| Duplication | 30-45 min | Extract duplicated logic |
| Missing test | 30-60 min | Write unit test |
| Missing docs | 15-30 min | Add docstrings |
| Deprecated dependency | 2-4 hours | Update library, fix breaking changes |
| Architecture issue | 4-8 hours | Decouple modules |

---

## 3. SIG Maintainability Model (Benchmark-Driven)

**Source**: Software Improvement Group, ISO/IEC 25010 standard

### Five-Star Rating System

Based on percentile benchmarking against 200+ billion lines of code:

| Rating | Percentile | Interpretation | Business Impact |
|--------|-----------|----------------|-----------------|
| **5★** | Top 5% | Excellent | Lowest maintenance costs |
| **4★** | Next 30% | Above average | 2× lower costs vs 2★ |
| **3★** | Average | Industry standard | Baseline |
| **2★** | Below average | High debt | 2× higher costs vs 4★ |
| **1★** | Bottom 5% | Critical debt | 4× slower development |

### Key Metrics (ISO 25010 Attributes)

1. **Analysability**: Ease of diagnosing issues
   - Metric: Code complexity, module coupling

2. **Changeability**: Effort to modify code
   - Metric: Duplication %, unit size (LOC per function)

3. **Testability**: Ease of writing tests
   - Metric: Test coverage %, cyclomatic complexity

4. **Modularity**: Component independence
   - Metric: Afferent/efferent coupling

5. **Reusability**: Component generality
   - Metric: Code duplication, abstraction level

### Low-Risk Thresholds (Delta Maintainability Model)

| Metric | Low Risk | Moderate Risk | High Risk |
|--------|----------|---------------|-----------|
| **Unit Size** | ≤15 LOC | 16-50 LOC | >50 LOC |
| **Cyclomatic Complexity** | ≤5 | 6-10 | >10 |
| **Parameters** | ≤2 | 3-4 | >4 |
| **Nesting Depth** | ≤3 | 4-5 | >5 |
| **Duplication** | <5% | 5-10% | >10% |

---

## 4. Quantitative Metrics & Thresholds

### Complexity Metrics

**Cyclomatic Complexity** (McCabe)
- **Target**: ≤10 per function (industry standard)
- **SIG Low-Risk**: ≤5
- **Calculation**: Count independent paths (branches, loops)
- **Git detection**: `git grep -E '\b(if|else|elif|switch|case|while|for|foreach)\b' | wc -l`

**Nesting Depth**
- **Target**: ≤3 levels
- **Detection**: Count indentation levels

### Duplication Metrics

**Code Duplication Percentage**
- **Target**: <5% (SQALE/SIG standard)
- **Red Flag**: >10%
- **Calculation**: (Duplicated LOC / Total LOC) × 100
- **Detection**: Compare file similarity, function signatures

### Coverage Metrics

**Test Coverage**
- **Target**: >80% line coverage
- **Minimum**: 60% for non-critical code
- **Critical Paths**: 100% coverage
- **Calculation**: (Tested LOC / Total LOC) × 100

### Historical Metrics (Git-Based)

**Code Churn**
- **Definition**: Files changed frequently (hotspots)
- **High Churn**: >10 commits in 3 months
- **Calculation**: `git log --since="3 months ago" --name-only --format="" | sort | uniq -c | sort -rn`
- **Risk**: High churn + high complexity = top priority debt

**Ownership Dispersion**
- **Definition**: Number of contributors per module
- **High Risk**: >5 minor contributors (<10% commits each)
- **Calculation**: `git shortlog -sn --since="6 months ago" <file>`
- **Research**: Microsoft study shows low ownership = more defects

**Change Cohesion**
- **Definition**: Commits spanning unrelated modules
- **High Risk**: Commits touching >3 unrelated areas
- **Detection**: Analyze git commit file patterns
- **Indicator**: Weak module boundaries

**Recurrent Churn**
- **Definition**: Files changed month-over-month
- **High Risk**: Same file modified in 3+ consecutive months
- **Research**: Most bug-prone indicator (Microsoft study)

### Dependency Metrics

**Dependency Staleness**
- **Calculation**: Months since latest version
- **High Risk**: >12 months outdated
- **Critical**: Known CVEs (security vulnerabilities)
- **Detection**: Check requirements.txt, package.json, Cargo.toml against latest versions

---

## 5. Principal vs Interest Framework

**Financial Debt Analogy**: Technical debt has upfront cost (principal) and ongoing cost (interest)

### Principal (Fix Cost Now)

- **Definition**: Effort to remediate debt immediately
- **Estimation**: Sum of remediation hours per violation
- **Example**: 5 days to refactor messy legacy module

### Interest (Ongoing Cost if Unfixed)

- **Definition**: Recurring cost of not fixing debt
- **Forms**:
  - Extra development time per sprint
  - Bug fix overhead
  - Performance degradation
  - Lost business opportunities
- **Example**: 1 day extra effort per release due to messy code

### Interest Rate Calculation

```
Interest_Rate = (Maintenance_Hours / Development_Hours) × Debt_Percentage × 100

Example:
- Module takes 2 hours to modify (should take 1 hour) = 100% overhead
- Debt_Percentage = 20% of module is problematic
- Interest_Rate = (2/1 - 1) × 20% × 100 = 20% annual interest
```

**Prioritization Rule**: High-interest debt (>10% annual rate) = top priority

---

## 6. Impact/Effort Prioritization Matrix

**Purpose**: Classify debt items into actionable quadrants

### Four Priority Quadrants

```
        High Impact
            │
  P1: Quick Wins   │  P2: Strategic
  (Do Immediately) │  (Plan & Resource)
────────────────────┼────────────────────
  P4: Opportunistic│  P3: Defer
  (Boy Scout Rule) │  (Low Priority)
            │
        Low Impact

    Low Effort          High Effort
```

### Quadrant Definitions

**P1: Quick Wins (High Impact, Low Effort)**
- **Action**: Do immediately
- **Examples**:
  - Fix critical security issue in config (1 hour)
  - Add tests to frequently-failing module (2 hours)
  - Update deprecated API usage (30 min)
- **ROI**: Immediate payoff, minimal investment

**P2: Strategic (High Impact, High Effort)**
- **Action**: Plan, schedule, allocate resources
- **Examples**:
  - Strangler pattern refactor of monolith (6 weeks)
  - Add comprehensive test suite (2 weeks)
  - Architectural redesign for scalability (1 month)
- **ROI**: High long-term value, requires project commitment

**P3: Defer (Low Impact, High Effort)**
- **Action**: Deprioritize unless business context changes
- **Examples**:
  - Refactor rarely-used legacy script
  - Optimize performance of infrequent batch job
  - Rewrite deprecated but stable component
- **ROI**: Poor investment, opportunity cost too high

**P4: Opportunistic (Low Impact, Low Effort)**
- **Action**: Fix when touching nearby code (Boy Scout Rule)
- **Examples**:
  - Rename variable for clarity
  - Add missing docstring
  - Extract magic number to constant
- **ROI**: Incremental improvement, zero dedicated effort

### Impact Scoring Criteria (0-10 scale)

| Factor | Weight | High Score (7-10) | Low Score (0-3) |
|--------|--------|-------------------|-----------------|
| **Business Criticality** | 35% | User-facing, payment flow | Internal tool, rarely used |
| **Usage Frequency** | 25% | 1000 req/min, daily changes | Once/month, stable |
| **Defect Risk** | 20% | High bug density, frequent incidents | No recent bugs |
| **Churn** | 10% | Changed weekly, many contributors | Untouched for months |
| **Downstream Impact** | 10% | Blocks other work, cascading failures | Isolated component |

### Effort Scoring Criteria (0-10 scale)

| Factor | Weight | High Score (7-10) | Low Score (0-3) |
|--------|--------|-------------------|-----------------|
| **Complexity** | 40% | Architectural change, 100+ files | Single function, 1 file |
| **Testing Needs** | 25% | Requires integration tests, mocks | Simple unit test |
| **Risk** | 20% | Breaking change, migration required | Backward compatible |
| **Expertise** | 15% | Specialized domain knowledge | Common pattern |

---

## 7. Composite Debt Score (0-100 Scale)

**Purpose**: Single metric for stakeholder communication and trend tracking

### Weighted Formula

```
Debt_Score = (Code_Quality × 0.40)
           + (Testing_Health × 0.20)
           + (Architecture × 0.15)
           + (Documentation × 0.10)
           + (Infrastructure × 0.10)
           + (Historical_Factors × 0.05)

Where each component is 0-100 (100 = excellent, 0 = critical)
```

### Component Calculations

**Code Quality (40%)**
```
Code_Quality = 100 - (
  (Complexity_Violations × 2)
  + (Duplication_Pct × 5)
  + (Coding_Violations × 0.5)
)
```

**Testing Health (20%)**
```
Testing_Health = (Coverage_Pct × 0.7) + (Test_Quality × 0.3)

Where:
- Coverage_Pct = Test coverage percentage
- Test_Quality = 100 - (Flaky_Tests × 10) - (Missing_Assertions × 5)
```

**Architecture (15%)**
```
Architecture = 100 - (
  (Coupling_Score × 3)
  + (Cyclic_Dependencies × 10)
  + (Outdated_Dependencies × 2)
)
```

**Documentation (10%)**
```
Documentation = (Documented_Functions_Pct × 0.6) + (README_Quality × 0.4)
```

**Infrastructure (10%)**
```
Infrastructure = 100 - (
  (Deprecated_APIs × 5)
  + (Missing_Configs × 3)
  + (Security_Issues × 10)
)
```

**Historical Factors (5%)**
```
Historical = 100 - (
  (High_Churn_Files × 2)
  + (Low_Ownership_Modules × 3)
  + (Recurrent_Bug_Areas × 5)
)
```

### Classification Thresholds

| Score Range | Classification | Interpretation | Action |
|-------------|---------------|----------------|--------|
| **81-100** | Low Debt | Excellent maintainability | Maintain current practices |
| **61-80** | Moderate Debt | Acceptable, room for improvement | Allocate 10% sprint time to debt |
| **41-60** | High Debt | Significant maintenance burden | Allocate 20% sprint time, prioritize |
| **0-40** | Severe Debt | Critical risk to velocity | Dedicated debt paydown sprint |

---

## 8. Hotspot Identification

**Definition**: High-churn + high-complexity files = highest risk areas

### Hotspot Formula

```
Hotspot_Score = (Churn_Frequency × 0.4)
              + (Cyclomatic_Complexity × 0.3)
              + (Defect_Density × 0.2)
              + (Business_Criticality × 0.1)

Threshold: Score >7.0 = Critical Hotspot
```

### CodeScene Research Validation

- **Hotspots = 2-3% of codebase**
- **Generate 11-16% of commits** (disproportionate churn)
- **Alert-level code has 15× more defects**
- **124% longer resolution time** for hotspot bugs

### Detection Strategy

1. **Identify high-churn files**: `git log --since="6 months ago" --name-only --format="" | sort | uniq -c | sort -rn | head -20`
2. **Calculate complexity**: Cyclomatic complexity for each high-churn file
3. **Correlate with bugs**: Cross-reference with bug tracker (GitHub Issues, Jira)
4. **Score business impact**: User-facing? Critical path?

**Prioritization**: Hotspots always Priority 1 (regardless of effort)

---

## 9. Trend Tracking & Regression Detection

**Purpose**: Monitor debt direction (improving vs accumulating)

### Key Trend Metrics

**Debt Score Delta**
```
Trend = (Current_Score - Baseline_Score) / Baseline_Score × 100

Example:
- Baseline: 62 → Current: 78
- Trend: (78-62)/62 × 100 = +25.8% improvement
```

**Category-Level Deltas**
- Track each category independently
- Identify regressions (e.g., testing health drops 10%)

**Regression Alerts** (Threshold-Based)

| Metric | Threshold | Action |
|--------|-----------|--------|
| TDR increase | >2% absolute | Investigate recent commits |
| Coverage drop | >5% | Block merges, add tests |
| Complexity spike | >15% average | Code review required |
| Duplication rise | >3% | Refactoring needed |
| New hotspots | +2 files | Priority investigation |

### Dashboard Visualization

**Recommended Charts**:
1. Debt Score trend line (3-6 month history)
2. Category breakdown (stacked bar: current vs baseline)
3. Hotspot heatmap (churn × complexity)
4. TDR gauge (with A-E grade zones)

---

## 10. Real-World Case Study

**Source**: Michael Eakins, 2-year technical debt paydown

### Starting Point (Baseline)
- **Debt Score**: 41/100 (Critical)
- **TDR**: ~25%
- **Bug Backlog**: 500+ open issues
- **Key Hotspot**: PaymentProcessor (347 complexity, 0% tests, 23 bugs/6mo)

### Intervention Strategy
1. **Priority Matrix**: Classified 200+ debt items
2. **Strangler Pattern**: Gradual rewrite of PaymentProcessor
3. **Boy Scout Rule**: Leave code cleaner than found
4. **Sprint Allocation**: 20% time to debt paydown

### Results After 2 Years
- **Debt Score**: 78/100 (+90% improvement)
- **TDR**: <5% (A grade)
- **Feature Throughput**: 3× increase
- **Production Incidents**: 91% reduction
- **PaymentProcessor**: 93% complexity reduction, near-zero bugs

**ROI**: $3.2M technical debt eliminated, measurable business impact

---

## Usage Guidelines for tech-debt-investigator

1. **OBSERVE Phase**: Parse artifacts using 6-category taxonomy
2. **ORIENT Phase**: Calculate quantitative metrics, apply thresholds
3. **DECIDE Phase**: Use Impact/Effort matrix, compute composite scores
4. **ACT Phase**: Generate findings with TDR, debt_score, hotspot flags
5. **Iterate**: Track trends, detect regressions, measure improvement

**Reference Sections**: Link to specific sections (e.g., "§4 Quantitative Metrics" for threshold lookup)

---

**Document Status**: Production-ready reference
**Last Updated**: 2025-01-20
**Maintenance**: Update thresholds annually based on codebase evolution
