---
title: "Quality Scoring Algorithms: Concrete Measurement Framework"
date: 2025-11-08
status: ACTIVE
tags: [claude-docs]
---
# Quality Scoring Algorithms: Concrete Measurement Framework

## Overview

This framework provides concrete, mathematical algorithms for quality assessment in software development, replacing subjective metrics with objective, calculable scores. All agents should use these algorithms for consistent quality evaluation.

**Quality Philosophy:** Measurable, reproducible quality assessment that provides actionable feedback and enables continuous improvement.

## Core Quality Algorithms

### 1. Pain Point Alignment Score

**Purpose:** Measure how well a feature addresses documented customer pain points

**Algorithm:**

```
Pain Point Alignment Score = Σ(Weight × Coverage × Impact) / Σ(Weight)

Where for each pain point:
- Weight = Customer frequency score (1-5)
- Coverage = Feature coverage of pain point (0.0-1.0)
- Impact = Expected impact on pain point (1-5)

Target Score: ≥ 0.4 (minimum acceptable)
Good Score: ≥ 0.6 (well-aligned)
Excellent Score: ≥ 0.8 (highly aligned)
```

**Example Calculation:**

```
Pain Points:
- Analysis Paralysis (Weight: 5, Coverage: 0.8, Impact: 4) = 5 × 0.8 × 4 = 16
- Time Constraints (Weight: 4, Coverage: 0.6, Impact: 3) = 4 × 0.6 × 3 = 7.2
- Quality Concerns (Weight: 3, Coverage: 0.4, Impact: 2) = 3 × 0.4 × 2 = 2.4

Score = (16 + 7.2 + 2.4) / (5 + 4 + 3) = 25.6 / 12 = 0.53 (Medium alignment)
```

### 2. MVP Complexity Score

**Purpose:** Assess whether feature complexity aligns with MVP stage constraints

**Algorithm:**

```
MVP Complexity Score = (Technical Complexity + Integration Complexity + Resource Complexity) / 3

Technical Complexity = (Dependencies + Novel Technologies + Custom Logic) / 15
Integration Complexity = (External APIs + Data Sources + System Boundaries) / 15
Resource Complexity = (Team Skills Gap + Time Investment + Maintenance Overhead) / 15

Target Score: ≤ 0.3 (MVP appropriate)
Acceptable Score: ≤ 0.5 (manageable complexity)
High Complexity: > 0.5 (requires simplification or staging)
```

**Scoring Components (1-5 scale each):**

- **Dependencies:** Number and complexity of external dependencies
- **Novel Technologies:** Use of unproven or new technologies
- **Custom Logic:** Amount of business logic complexity
- **External APIs:** Number and complexity of external integrations
- **Data Sources:** Number and variety of data sources
- **System Boundaries:** Interfaces with other systems
- **Team Skills Gap:** Learning curve for required skills
- **Time Investment:** Expected development time
- **Maintenance Overhead:** Ongoing operational complexity

### 3. Requirements Completeness Score

**Purpose:** Measure completeness and quality of functional requirements

**Algorithm:**

```
Completeness Score = (Testable Requirements + Traced Requirements + Detailed Requirements) / (3 × Total Requirements)

Testable Requirements = Count of requirements with clear acceptance criteria
Traced Requirements = Count of requirements linked to business goals
Detailed Requirements = Count of requirements with implementation detail
```

**Quality Thresholds:**

- **Excellent:** ≥ 0.9 (90%+ complete)
- **Good:** ≥ 0.8 (80%+ complete)
- **Acceptable:** ≥ 0.7 (70%+ complete)
- **Poor:** < 0.7 (needs improvement)

### 4. Technical Debt Risk Score

**Purpose:** Quantify potential technical debt accumulation

**Algorithm:**

```
Technical Debt Risk = (Shortcuts × Urgency + Complexity × Maintainability + Knowledge × Documentation) / 300

Shortcuts (0-10): Number of known technical shortcuts
Urgency (0-10): Pressure to deliver quickly
Complexity (0-10): Solution complexity level
Maintainability (0-10): Code maintainability challenges
Knowledge (0-10): Team knowledge concentration
Documentation (0-10): Documentation completeness gaps

Risk Levels:
- Low Risk: ≤ 0.3
- Medium Risk: 0.3-0.6
- High Risk: 0.6-0.8
- Critical Risk: > 0.8
```

### 5. Implementation Readiness Score

**Purpose:** Assess whether requirements are ready for implementation

**Algorithm:**

```
Implementation Readiness = Σ(Category Weight × Category Score) / Σ(Category Weight)

Categories and Weights:
- Requirement Clarity (Weight: 0.3): Clear, unambiguous requirements
- Technical Approach (Weight: 0.25): Defined implementation approach
- Dependency Resolution (Weight: 0.2): All dependencies identified and available
- Resource Availability (Weight: 0.15): Required skills and time available
- Risk Mitigation (Weight: 0.1): Major risks identified and mitigated

Each category scored 0.0-1.0 based on completion percentage
```

**Readiness Thresholds:**

- **Ready:** ≥ 0.8 (can start implementation)
- **Nearly Ready:** ≥ 0.6 (minor gaps to address)
- **Not Ready:** < 0.6 (significant preparation needed)

## Quality Gate Algorithms

### 1. SPEC Quality Gate

**Purpose:** Determine if specification is ready for planning phase

**Algorithm:**

```
SPEC Quality Score = (0.4 × Pain Point Alignment) + (0.3 × Requirements Completeness) + (0.2 × MVP Complexity) + (0.1 × Technical Debt Risk)

Where:
- Pain Point Alignment: 0.0-1.0 (target ≥ 0.4)
- Requirements Completeness: 0.0-1.0 (target ≥ 0.7)
- MVP Complexity: 0.0-1.0 (target ≤ 0.3, inverted for scoring)
- Technical Debt Risk: 0.0-1.0 (target ≤ 0.3, inverted for scoring)

Gate Thresholds:
- PASS: ≥ 0.7
- CONDITIONAL: 0.5-0.69 (with mitigation plan)
- FAIL: < 0.5
```

### 2. PLAN Quality Gate

**Purpose:** Determine if technical plans are ready for implementation

**Algorithm:**

```
PLAN Quality Score = (0.35 × Implementation Readiness) + (0.25 × Technical Completeness) + (0.2 × Risk Assessment) + (0.2 × Resource Planning)

Technical Completeness = (Architecture Decisions + Technology Choices + Integration Design) / 3
Risk Assessment = 1.0 - (Average Risk Score / 125)  // Invert P×I×E scores
Resource Planning = (Effort Estimates + Skill Requirements + Timeline) / 3

Gate Thresholds:
- PASS: ≥ 0.75
- CONDITIONAL: 0.6-0.74 (with enhancement plan)
- FAIL: < 0.6
```

### 3. Sprint Readiness Gate

**Purpose:** Determine if tasks are ready for sprint execution

**Algorithm:**

```
Sprint Readiness Score = (0.4 × Task Clarity) + (0.3 × Dependency Resolution) + (0.2 × Acceptance Criteria) + (0.1 × Resource Allocation)

Task Clarity = (Clear Goals + Defined Approach + Specific Deliverables) / 3
Dependency Resolution = Resolved Dependencies / Total Dependencies
Acceptance Criteria = Tasks with Criteria / Total Tasks
Resource Allocation = Assigned Tasks / Total Tasks

Gate Thresholds:
- READY: ≥ 0.8
- NEEDS PREPARATION: 0.6-0.79
- NOT READY: < 0.6
```

## Continuous Quality Metrics

### 1. Quality Trend Analysis

**Purpose:** Track quality improvements over time

**Algorithm:**

```
Quality Velocity = (Current Period Quality Score - Previous Period Quality Score) / Previous Period Quality Score

Trend Categories:
- Improving: > 0.05 (5%+ improvement)
- Stable: -0.05 to 0.05 (within 5%)
- Declining: < -0.05 (more than 5% decline)
```

### 2. Quality Debt Accumulation

**Purpose:** Track accumulation of quality shortcuts

**Algorithm:**

```
Quality Debt Score = Σ(Shortcut Impact × Time Since Shortcut) / Total Features

Shortcut Impact (1-5):
- 1: Minor documentation gap
- 2: Missing test cases
- 3: Technical debt accumulation
- 4: Architecture compromise
- 5: Critical quality bypass

Time Weight = sqrt(Days Since Shortcut / 30)  // Increases over time
```

### 3. Stakeholder Confidence Index

**Purpose:** Measure stakeholder confidence in quality processes

**Algorithm:**

```
Confidence Index = (Process Adherence × Outcome Predictability × Communication Quality) / 3

Process Adherence = Gates Followed / Total Gates
Outcome Predictability = Actual vs Estimated Quality Scores correlation
Communication Quality = Quality Reports Completeness Score

Target: ≥ 0.8 (high confidence)
```

## Implementation Guidelines

### For /spec Command

```python
# Example implementation
def calculate_pain_point_alignment(feature_coverage, pain_points):
    total_weighted_score = 0
    total_weight = 0

    for pain_point in pain_points:
        weight = pain_point.customer_frequency  # 1-5
        coverage = feature_coverage.get(pain_point.id, 0.0)  # 0.0-1.0
        impact = pain_point.expected_impact  # 1-5

        total_weighted_score += weight * coverage * impact
        total_weight += weight

    return total_weighted_score / total_weight if total_weight > 0 else 0.0

# Include in Planning Recommendations
planning_recommendations = {
    "quality_scoring": {
        "pain_point_alignment": calculate_pain_point_alignment(feature, pain_points),
        "mvp_complexity": calculate_mvp_complexity(technical_requirements),
        "requirements_completeness": calculate_completeness(functional_requirements),
        "overall_spec_quality": calculate_spec_quality_gate(scores)
    }
}
```

### For architecture Agent

```python
def calculate_plan_quality_score(plans):
    implementation_readiness = assess_implementation_readiness(plans)
    technical_completeness = assess_technical_completeness(plans)
    risk_assessment = 1.0 - (calculate_average_risk_score(plans) / 125)
    resource_planning = assess_resource_planning(plans)

    return (0.35 * implementation_readiness +
            0.25 * technical_completeness +
            0.2 * risk_assessment +
            0.2 * resource_planning)
```

### For planning Agent

```python
def validate_quality_scoring(business_review):
    # Validate pain point alignment calculation
    alignment_score = recalculate_pain_point_alignment(business_review)

    # Check quality gate thresholds
    quality_gates = {
        "spec_quality": alignment_score >= 0.4,
        "requirements_complete": requirements_completeness >= 0.7,
        "mvp_appropriate": mvp_complexity <= 0.3
    }

    return quality_gates
```

## Quality Scoring Standards

### Mandatory Quality Checks

All agents must include these quality scores:

- [ ] Pain Point Alignment Score calculated and ≥ 0.4
- [ ] MVP Complexity Score calculated and ≤ 0.3
- [ ] Requirements Completeness Score calculated and ≥ 0.7
- [ ] Technical Debt Risk Score calculated and ≤ 0.3
- [ ] Implementation Readiness Score calculated when applicable
- [ ] Quality gate thresholds applied and documented
- [ ] Trend analysis included for ongoing projects

### Quality Score Reporting Template

```markdown
## Quality Self-Assessment

### Core Quality Metrics

- **Pain Point Alignment:** 0.65 (Target: ≥0.4) ✅ PASS
- **MVP Complexity:** 0.28 (Target: ≤0.3) ✅ PASS
- **Requirements Completeness:** 0.82 (Target: ≥0.7) ✅ PASS
- **Technical Debt Risk:** 0.25 (Target: ≤0.3) ✅ PASS

### Quality Gate Status

- **SPEC Quality Gate:** 0.73 ✅ PASS (≥0.7 required)
- **Overall Quality Score:** Good (all metrics within targets)
- **Recommendations:** Continue with current approach
```

---

**This framework provides concrete, mathematical quality assessment that enables consistent, objective evaluation across all development activities.**
