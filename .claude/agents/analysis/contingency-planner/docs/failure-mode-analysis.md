# Failure Mode Analysis Guide

**Purpose**: Comprehensive framework for identifying and scoring failure modes in hypothesis evaluation

**Audience**: contingency-planner agent (DECIDE phase component)

**Scope**: 3-5 failure modes per hypothesis with probability×impact risk scoring (0.0-1.0 scales)

---

## Failure Mode Enumeration

### Core Principle

Generate **3-5 distinct failure modes** per hypothesis covering:

- **Technical failures**: Implementation bugs, integration issues, performance problems
- **Resource failures**: Missing dependencies, capacity constraints, timeout issues
- **Assumption failures**: Incorrect estimates, misunderstood requirements, invalid constraints
- **Integration failures**: Cross-module conflicts, API mismatches, data inconsistencies

### Systematic Enumeration Process

**For each hypothesis**:

1. Identify 3-5 distinct ways the hypothesis could fail
2. Classify each failure by type (technical/resource/assumption/integration)
3. Document specific triggers for each failure mode
4. Calculate probability and impact scores
5. Generate risk_score = probability × impact

### Failure Mode Template

```json
{
  "mode_id": "FM001",
  "description": "Specific failure scenario with concrete triggers",
  "failure_type": "technical|resource|assumption|integration",
  "triggers": [
    "Concrete condition 1 that causes failure",
    "Concrete condition 2 that causes failure",
    "Concrete condition 3 that causes failure"
  ],
  "probability": 0.4,
  "probability_rationale": "Explanation using rubric",
  "impact": 0.6,
  "impact_rationale": "Explanation using rubric",
  "risk_score": 0.24
}
```

---

## Probability Scoring Rubric (0.0-1.0)

### Assessment Criteria

**1.0 - Certain**: Failure will definitely occur
- Examples: Missing critical dependency, undefined API, blocking constraint

**0.7 - High**: Failure very likely
- Examples: Complex integration, known instability, tight coupling, novel pattern

**0.5 - Medium**: Failure somewhat likely
- Examples: Moderate complexity, some unknowns, external dependencies

**0.3 - Low**: Failure unlikely
- Examples: Simple logic, well-tested patterns, clear requirements

**0.1 - Very Low**: Failure rare
- Examples: Proven approach, minimal dependencies, robust error handling

### Domain-Specific Adjustments

Apply these adjustments to base probability score:

**External Dependencies**: +0.2
- APIs, network calls, third-party libraries
- Example: Redis integration adds +0.2 to base probability

**Security-Critical**: +0.1
- Authentication, authorization, data protection
- Example: JWT implementation adds +0.1

**Novel Patterns**: +0.15
- No codebase examples, new technology, unproven approach
- Example: First distributed cache implementation adds +0.15

**Established Patterns**: -0.2
- Proven in codebase, well-documented, multiple examples
- Example: Standard CRUD operation subtracts -0.2

### Calculation Example

```
Base probability: 0.0 (starting point)
+ External dependency (Redis): +0.2
+ Moderate complexity: +0.2
= Final probability: 0.4
```

---

## Impact Scoring Rubric (0.0-1.0)

### Assessment Criteria

**1.0 - Critical**: Complete task failure, no recovery possible without major rework
- Examples: System-wide breaking changes, data loss, security breach

**0.8 - High**: Significant setback, requires substantial effort to recover
- Examples: Multi-day rework, architecture changes, major refactoring

**0.6 - Medium**: Moderate setback, recoverable with reasonable effort
- Examples: Several hours of debugging, fallback to simpler approach

**0.4 - Low**: Minor setback, quick recovery with simple fix
- Examples: Configuration adjustment, dependency update, small refactor

**0.2 - Very Low**: Negligible impact, trivial to work around
- Examples: Code style fix, minor logic adjustment, documentation update

### Impact Dimensions

Assess impact across 4 dimensions:

**1. Time Impact**: How much delay does failure cause?
- 1.0: Weeks of delay
- 0.8: Days of delay
- 0.6: Hours of delay
- 0.4: Minutes of delay
- 0.2: Immediate recovery

**2. Scope Impact**: How many components affected?
- 1.0: System-wide changes required
- 0.8: Multiple modules affected
- 0.6: Single module, multiple files
- 0.4: Single file
- 0.2: Isolated function/method

**3. Quality Impact**: How severe is degradation?
- 1.0: Security vulnerability, data loss
- 0.8: Functional regression
- 0.6: Performance degradation
- 0.4: UX degradation
- 0.2: Cosmetic issue

**4. Recovery Effort**: How difficult to fix?
- 1.0: Architecture redesign
- 0.8: Major refactoring
- 0.6: Moderate debugging
- 0.4: Simple fix
- 0.2: Trivial adjustment

### Calculation Example

```json
{
  "impact": 0.6,
  "impact_breakdown": {
    "time_impact": 0.5,
    "scope_impact": 0.4,
    "quality_impact": 0.3,
    "recovery_effort": 0.6,
    "average": 0.45,
    "rounded_up": 0.6,
    "rationale": "Medium setback - recoverable with fallback to in-memory cache (2-3 hour pivot)"
  }
}
```

---

## Risk Score Calculation

### Formula

```
risk_score = probability × impact
```

### Risk Thresholds

**HIGH RISK (risk_score ≥ 0.7)**:
- Action: Plan 3 fallback strategies
- Retry: Max 1 retry before escalation
- Escalation: Rapid (immediate after first failure)
- Example: Probability 0.9 × Impact 0.8 = 0.72

**MEDIUM RISK (0.4 ≤ risk_score < 0.7)**:
- Action: Plan 2 fallback strategies
- Retry: Max 2 retries before escalation
- Escalation: Conditional (after 2 failures)
- Example: Probability 0.5 × Impact 0.6 = 0.30

**LOW RISK (risk_score < 0.4)**:
- Action: Plan 1 fallback strategy
- Retry: Max 3 retries before escalation
- Escalation: Standard (after exhausting retries)
- Example: Probability 0.3 × Impact 0.4 = 0.12

---

## Domain-Specific Failure Mode Catalogs

### .claude/** (Agent/Workflow Development)

**Common Failure Modes**:
1. Schema validation failures (probability: 0.4, impact: 0.7)
2. Tool permission violations (probability: 0.3, impact: 0.6)
3. Integration with orchestrator breaks (probability: 0.2, impact: 0.8)

### packages/** (Python Implementation)

**Common Failure Modes**:
1. Dependency conflicts (probability: 0.3, impact: 0.5)
2. Test coverage gaps (probability: 0.5, impact: 0.6)
3. Type annotation errors (probability: 0.4, impact: 0.3)
4. Performance targets not met (probability: 0.3, impact: 0.7)

### tests/** (Testing)

**Common Failure Modes**:
1. Flaky tests (probability: 0.4, impact: 0.5)
2. Mock complexity (probability: 0.5, impact: 0.4)
3. Integration test dependencies (probability: 0.6, impact: 0.7)

### docs/** (Documentation)

**Common Failure Modes**:
1. Outdated examples (probability: 0.6, impact: 0.3)
2. Inconsistent formatting (probability: 0.4, impact: 0.2)
3. Missing cross-references (probability: 0.5, impact: 0.4)

---

## Usage Example

**Input Hypothesis**:
```json
{
  "hypothesis_id": "H001",
  "strategy": "Redis-backed distributed cache with TTL",
  "agent": "python-code-implementer",
  "dcs_score": 0.68
}
```

**Failure Mode Analysis Output**:
```json
{
  "failure_modes": [
    {
      "mode_id": "FM001",
      "description": "Redis connection failure during implementation",
      "failure_type": "technical",
      "triggers": [
        "Redis not installed locally",
        "Connection string misconfigured",
        "Network connectivity issues"
      ],
      "probability": 0.4,
      "probability_breakdown": {
        "base_probability": 0.0,
        "external_dependency_adjustment": 0.2,
        "complexity_adjustment": 0.2,
        "rationale": "External dependency increases likelihood, moderate setup complexity"
      },
      "impact": 0.6,
      "impact_breakdown": {
        "time_impact": 0.5,
        "scope_impact": 0.4,
        "quality_impact": 0.3,
        "recovery_effort": 0.6,
        "rationale": "Medium setback - recoverable with fallback to in-memory cache (2-3 hour pivot)"
      },
      "risk_score": 0.24,
      "risk_classification": "medium"
    },
    {
      "mode_id": "FM002",
      "description": "Cache invalidation logic complexity exceeds estimate",
      "failure_type": "assumption",
      "triggers": [
        "TTL patterns unclear for different data types",
        "Invalidation edge cases (concurrent writes, stale reads)",
        "Race conditions between cache update and invalidation"
      ],
      "probability": 0.5,
      "probability_rationale": "Novel pattern (+0.15), moderate complexity (+0.2), base 0.0 = 0.35 → rounded 0.5",
      "impact": 0.8,
      "impact_rationale": "High setback - significant debugging required, multiple edge cases",
      "risk_score": 0.40,
      "risk_classification": "medium"
    },
    {
      "mode_id": "FM003",
      "description": "Performance targets not met (response time >100ms vs target <100ms)",
      "failure_type": "integration",
      "triggers": [
        "Redis network latency higher than expected",
        "Serialization overhead for complex objects",
        "Cache miss ratio higher than predicted"
      ],
      "probability": 0.3,
      "impact": 0.7,
      "risk_score": 0.21,
      "risk_classification": "low"
    }
  ],
  "total_failure_modes": 3,
  "highest_risk_score": 0.40,
  "risk_distribution": {
    "high": 0,
    "medium": 2,
    "low": 1
  }
}
```

---

## Best Practices

1. **Always identify 3-5 failure modes** - Insufficient coverage (<3) or excessive detail (>5) reduces value
2. **Use concrete triggers** - Avoid vague descriptions like "might fail" - specify exact conditions
3. **Apply domain catalogs** - Leverage domain-specific failure patterns for faster enumeration
4. **Document probability rationale** - Show calculation with adjustments for transparency
5. **Consider all 4 impact dimensions** - Time, scope, quality, recovery effort
6. **Calculate risk_score** - Always multiply probability × impact for threshold-based decisions
7. **Classify by risk level** - Use thresholds to determine fallback strategy count and retry limits

---

**Related Guides**:
- `../contingency-planner.md` - Agent definition and workflow integration
- `fallback-strategies.md` - Generating 2-3 fallback strategies per failure mode
- `retry-plans.md` - Defining adaptive retry plans with escalation triggers
- `../examples/contingency-examples.md` - Complete examples with failure modes and fallback strategies
