---
name: plan-generation
description: >
  Use this skill when generating implementation plans from synthesized context.
  Orchestrates algorithms from generating-plans skill.
  Trigger keywords: generate plan, create plan, plan orchestration.
---

# Plan Generation

*Thin orchestration layer for plan creation: transform SPEC.md into phased implementation plans with MoSCoW prioritization.*

**Key Design**: This skill orchestrates plan generation by referencing `generating-plans` for ALL algorithms. It does NOT duplicate algorithm logic.

---

## Contents

1. [Generation Pipeline Overview](#generation-pipeline-overview)
2. [Algorithm References](#algorithm-references)
3. [Phase Building Logic](#phase-building-logic)
4. [Summary Generation](#summary-generation)
5. [Output Contract](#output-contract)
6. [Anti-Patterns](#anti-patterns)
7. [Quick Reference](#quick-reference)

---

## Generation Pipeline Overview

### Transformation Flow

```
SPEC.md Input
    ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 1: Section Detection                                   │
│   -> Apply: generating-plans#specmd-section-detection       │
│   -> Extract FR table, scenarios, constraints               │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 2: Complexity Classification                           │
│   -> Apply: generating-plans#cynefin-complexity-classification│
│   -> Determine: SIMPLE/COMPLICATED/COMPLEX/CHAOTIC          │
│   -> Output: phase_count, approach                          │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 3: MoSCoW-to-Phase Mapping                            │
│   -> Apply: generating-plans#moscow-to-phase-mapping        │
│   -> Must→Phase1, Should→Phase1-2, Could→Phase2-3          │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 4: FR-to-Feature Conversion                           │
│   -> Apply: generating-plans#fr-to-feature-conversion       │
│   -> Transform FR rows to feature objects                   │
│   -> Split features >3 hours into sub-features              │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 5: Step Generation                                     │
│   -> Apply: generating-plans#step-generation-algorithm      │
│   -> Generate 2-5 concrete steps per feature                │
│   -> Apply: Risk Annotation (if risk assessment available)  │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 6: Critical Path Calculation                          │
│   -> Apply: generating-plans#critical-path-calculation      │
│   -> Identify blocking/foundational features                │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 7: Effort Estimation                                   │
│   -> Apply: generating-plans#effort-estimation-model        │
│   -> Calculate 0.5-3.0 hours per feature                    │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 8: Category Assignment                                 │
│   -> Apply: generating-plans#category-assignment-rules      │
│   -> Assign: functional/testing/infra/docs/performance      │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 9: Validation                                          │
│   -> Apply: generating-plans#validation-gates               │
│   -> Run 4 blocking gates: Schema, Coverage, Structure, AC  │
│   -> Calculate: generating-plans#quality-score-formula      │
└─────────────────────────────────────────────────────────────┘
    ↓
PLAN.json Output (if quality_score >= 0.85)
```

### Prerequisites

- **Required Input**: SPEC.md with Functional Requirements table
- **Required Data**: FR entries with MoSCoW priorities, acceptance criteria
- **Optional**: User scenarios, technical constraints, pain point alignment

### Input from plan-risk-assessment (Optional)

When risk assessment data is available from the upstream `plan-risk-assessment` skill:

```json
{
  "research_recommendations": [
    {
      "step_id": "FR-001-step-2",
      "priority": "MUST",
      "risk_score": 0.85,
      "risk_factors": ["external_api", "no_prior_pattern"],
      "recommendation": "Research JWT best practices before implementation"
    }
  ],
  "summary": {
    "total_steps_assessed": 24,
    "must_research": 3,
    "should_research": 5,
    "could_research": 8,
    "no_research_needed": 8
  }
}
```

**Risk Integration Protocol**:
- If `research_recommendations` is provided, apply risk annotation during Step 5
- If not provided, skip risk annotation (steps will lack risk properties)
- Summary counts are logged but do not affect quality score calculation

---

## Algorithm References

**CRITICAL**: This skill does NOT implement these algorithms. It references `generating-plans` for ALL algorithm logic.

| Algorithm | Reference | When Applied | Output |
|-----------|-----------|--------------|--------|
| Section Detection | [generating-plans#specmd-section-detection](../generating-plans/SKILL.md#specmd-section-detection) | Step 1: Initial parsing | sections{}, fr_entries[] |
| Complexity Classification | [generating-plans#cynefin-complexity-classification](../generating-plans/SKILL.md#cynefin-complexity-classification) | Step 2: After FR extraction | domain, phases, approach |
| MoSCoW-to-Phase Mapping | [generating-plans#moscow-to-phase-mapping-algorithm](../generating-plans/SKILL.md#moscow-to-phase-mapping-algorithm) | Step 3: Phase assignment | phases{} with FRs allocated |
| FR-to-Feature Conversion | [generating-plans#fr-to-feature-conversion-algorithm](../generating-plans/SKILL.md#fr-to-feature-conversion-algorithm) | Step 4: Feature creation | feature objects[] |
| Step Generation | [generating-plans#step-generation-algorithm](../generating-plans/SKILL.md#step-generation-algorithm) | Step 5: Per feature | steps[] (2-5 per feature) |
| Risk Annotation | See [Risk Annotation Protocol](#risk-annotation-protocol) | Step 5: After step generation | steps[] with risk properties |
| Critical Path Calculation | [generating-plans#critical-path-calculation](../generating-plans/SKILL.md#critical-path-calculation) | Step 6: After features built | critical_path[], foundational[] |
| Effort Estimation | [generating-plans#effort-estimation-model](../generating-plans/SKILL.md#effort-estimation-model) | Step 7: Per feature | estimated_hours (0.5-3.0) |
| Category Assignment | [generating-plans#category-assignment-rules](../generating-plans/SKILL.md#category-assignment-rules) | Step 8: Per feature | category string |
| Validation Gates | [generating-plans#validation-gates](../generating-plans/SKILL.md#validation-gates) | Step 9: Before output | gate_results{}, valid boolean |
| Quality Score | [generating-plans#quality-score-formula](../generating-plans/SKILL.md#quality-score-formula) | Step 9: Final check | quality_score (0.0-1.0) |

### Algorithm Application Protocol

```
FOR each step in generation_pipeline:

  1. IDENTIFY required algorithm from table above
  
  2. APPLY algorithm exactly as defined in generating-plans
     -> DO NOT modify algorithm parameters
     -> DO NOT skip validation steps
     
  3. CAPTURE algorithm output for next step
  
  4. IF algorithm returns error:
     -> HALT pipeline
     -> RETURN FAILURE with error details
     -> INCLUDE recovery_action from algorithm
```

### Algorithm Dependencies

```
Section Detection ─────────────────┐
                                   ↓
Complexity Classification ←────────┤
                                   ↓
MoSCoW-to-Phase Mapping ←──────────┤
         ↓                         │
FR-to-Feature Conversion ──────────┘
         ↓
Step Generation ←──────────────────┐
         ↓                         │
Category Assignment ───────────────┤
         ↓                         │
Effort Estimation ─────────────────┤
         ↓                         │
Critical Path Calculation ─────────┘
         ↓
Validation Gates
         ↓
Quality Score
```

### Risk Annotation Protocol

When risk assessment data is available from `plan-risk-assessment`, apply risk annotations during Step 5:

```
FUNCTION annotate_steps_with_risk(steps[], research_recommendations[]):
  
  # Build lookup map for O(1) access
  risk_map = {}
  FOR rec IN research_recommendations:
    risk_map[rec.step_id] = rec
  
  # Annotate each step
  FOR step IN steps:
    IF step.step_id IN risk_map:
      rec = risk_map[step.step_id]
      
      # Add risk properties to step
      step.risk_score = rec.risk_score
      step.research_required = (rec.priority == "MUST")
      step.risk_factors = rec.risk_factors
    ELSE:
      # No risk assessment for this step - use defaults
      step.risk_score = 0.0
      step.research_required = false
      step.risk_factors = []
  
  RETURN steps
```

**Risk Property Definitions**:

| Property | Type | Description |
|----------|------|-------------|
| `risk_score` | float (0.0-1.0) | Aggregated risk score from assessment |
| `research_required` | boolean | True if priority is MUST |
| `risk_factors` | string[] | List of identified risk factors |

**Step ID Matching**:
- Step IDs follow pattern: `{FR-ID}-step-{N}` (e.g., `FR-001-step-2`)
- Match is case-insensitive
- If no match found, step receives default values (score=0, required=false, factors=[])

---

## Phase Building Logic

### Phase Construction Protocol

Phases are constructed by orchestrating MoSCoW mapping results with complexity-derived phase counts.

```
FUNCTION build_phases(mapped_requirements, complexity_result):
  
  phase_count = complexity_result.phases  # From Cynefin classification
  phases = {}
  
  FOR i IN range(1, phase_count + 1):
    phase_key = f"phase_{i}"
    
    phases[phase_key] = {
      "name": generate_phase_name(i, phase_count),
      "duration_weeks": calculate_duration(i, phase_count),
      "target_completion": f"Week {sum_weeks_to_phase(i)}",
      "features": []
    }
  
  # Populate phases from MoSCoW mapping
  FOR req, phase_num IN mapped_requirements:
    feature = convert_fr_to_feature(req)  # From generating-plans
    phases[f"phase_{phase_num}"]["features"].append(feature)
  
  # Validate phase balance (3-7 features per phase optimal)
  balance_warnings = validate_phase_balance(phases)
  
  RETURN phases, balance_warnings
```

### Phase Naming Convention

| Phase | Theme Pattern | Example |
|-------|---------------|---------|
| 1 of 1 | Core Implementation | "Phase 1: Core - Complete Implementation" |
| 1 of 2 | Foundation | "Phase 1: Foundation - Core Infrastructure" |
| 2 of 2 | Integration | "Phase 2: Integration - API and Data Layer" |
| 1 of 3 | Foundation | "Phase 1: Foundation - Core Components" |
| 2 of 3 | Integration | "Phase 2: Integration - Service Layer" |
| 3 of 3 | Enhancement | "Phase 3: Enhancement - Polish and Performance" |
| 1 of 4 | Foundation | "Phase 1: Foundation - MVP Features" |
| 2 of 4 | Integration | "Phase 2: Integration - Core Workflows" |
| 3 of 4 | Enhancement | "Phase 3: Enhancement - Advanced Features" |
| 4 of 4 | Hardening | "Phase 4: Hardening - Security and Monitoring" |

### Phase Duration Calculation

```
FUNCTION calculate_duration(phase_num, total_phases):
  # Base durations by phase position
  duration_patterns = {
    1: {1: 2, 2: 2, 3: 2, 4: 1},  # Phase 1 durations
    2: {2: 2, 3: 2, 4: 2},        # Phase 2 durations
    3: {3: 1, 4: 2},              # Phase 3 durations
    4: {4: 1}                      # Phase 4 durations
  }
  
  base_duration = duration_patterns[phase_num].get(total_phases, 1)
  
  RETURN base_duration  # In weeks
```

### Phase Rebalancing Rules

When phases become unbalanced during construction:

```
TRIGGERS for rebalancing:
  - Phase has <3 features (under-loaded)
  - Phase has >7 features (over-loaded)
  - Adjacent phases differ by >4 features

REBALANCING actions:
  1. Move Could/Should items from over-loaded to under-loaded
  2. Respect dependency constraints (don't move if has dependents)
  3. Preserve Must items in Phase 1 (never move)
  4. Log all moves in balance_warnings[]
```

---

## Summary Generation

### Summary Construction Protocol

The summary section aggregates plan-wide metrics and identifies execution constraints.

```
FUNCTION generate_summary(phases, critical_path_result, spec_source):
  
  # Calculate totals
  total_features = sum(len(phase["features"]) FOR phase IN phases.values())
  total_hours = sum(
    feature["estimated_hours"] 
    FOR phase IN phases.values() 
    FOR feature IN phase["features"]
  )
  phases_total = len(phases)
  
  # Calculate timeline
  total_weeks = sum(phase["duration_weeks"] FOR phase IN phases.values())
  implementation_timeline = f"{total_weeks} weeks"
  
  # Format critical path
  critical_path_formatted = format_critical_path(critical_path_result)
  
  # Generate readiness gates
  launch_readiness_gates = generate_readiness_gates(phases)
  
  RETURN {
    "total_features": total_features,
    "total_estimated_hours": round(total_hours, 1),
    "phases_total": phases_total,
    "implementation_timeline": implementation_timeline,
    "critical_path": critical_path_formatted,
    "launch_readiness_gates": launch_readiness_gates
  }
```

### Critical Path Formatting

```
FUNCTION format_critical_path(critical_path_result):
  formatted = []
  
  FOR feature IN critical_path_result.critical_features:
    blockers = critical_path_result.get_blocked_by(feature.id)
    
    IF blockers:
      blocker_ids = ", ".join(blockers)
      formatted.append(f"{feature.id} (blocks {blocker_ids})")
    ELSE:
      formatted.append(f"{feature.id} (foundational)")
  
  RETURN formatted
```

### Readiness Gate Generation

```
FUNCTION generate_readiness_gates(phases):
  gates = []
  
  FOR phase_key, phase IN phases.items():
    phase_num = extract_phase_number(phase_key)
    
    # Determine gate type based on phase content
    categories = [f["category"] FOR f IN phase["features"]]
    primary_category = most_common(categories)
    
    # Generate gate description
    gate = generate_gate_description(phase_num, primary_category, phase["features"])
    gates.append(gate)
  
  RETURN gates

FUNCTION generate_gate_description(phase_num, category, features):
  gate_templates = {
    "functional": f"Phase {phase_num} Complete: All core features implemented and unit tested",
    "testing": f"Phase {phase_num} Complete: Test coverage meets >80% threshold",
    "infrastructure": f"Phase {phase_num} Complete: Infrastructure deployed and health checks passing",
    "documentation": f"Phase {phase_num} Complete: Documentation reviewed and published",
    "performance": f"Phase {phase_num} Complete: Performance benchmarks meet targets"
  }
  
  RETURN gate_templates.get(category, gate_templates["functional"])
```

### Summary Validation

```
VALIDATION rules for summary:
  - total_features MUST match sum of all phase features
  - total_estimated_hours MUST be within 0.5-3.0 × total_features range
  - phases_total MUST match actual phase count
  - critical_path MUST contain at least 1 feature
  - launch_readiness_gates MUST have exactly phases_total entries
```

---

## Output Contract

### Success Response

```json
{
  "status": "SUCCESS",
  "plan": {
    "project": "Feature Name",
    "description": "High-level description of what this project solves and delivers",
    "total_features": 8,
    "spec_source": "docs/01-planning/specifications/feature-name/SPEC.md",
    "phases": {
      "phase_1": {
        "name": "Phase 1: Foundation - Core Infrastructure",
        "duration_weeks": 2,
        "target_completion": "Week 2",
        "features": [
          {
            "id": "FR-001",
            "category": "functional",
            "description": "Implement user authentication service",
            "priority": "Must",
            "steps": [
              {
                "step_id": "FR-001-step-1",
                "description": "Define AuthService interface and data structures",
                "risk_score": 0.2,
                "research_required": false,
                "risk_factors": []
              },
              {
                "step_id": "FR-001-step-2",
                "description": "Implement JWT token generation and validation",
                "risk_score": 0.85,
                "research_required": true,
                "risk_factors": ["external_api", "security_critical"]
              },
              {
                "step_id": "FR-001-step-3",
                "description": "Add password hashing with bcrypt",
                "risk_score": 0.6,
                "research_required": false,
                "risk_factors": ["security_critical"]
              },
              {
                "step_id": "FR-001-step-4",
                "description": "Write unit tests covering auth scenarios",
                "risk_score": 0.1,
                "research_required": false,
                "risk_factors": []
              }
            ],
            "acceptance_criteria": [
              "AuthService returns valid JWT for correct credentials",
              "Invalid credentials return 401 error",
              "Token expiration enforced at 24 hours"
            ],
            "passes": false,
            "estimated_hours": 2.0
          }
        ]
      },
      "phase_2": {
        "name": "Phase 2: Integration - API Layer",
        "duration_weeks": 2,
        "target_completion": "Week 4",
        "features": []
      }
    },
    "summary": {
      "total_features": 8,
      "total_estimated_hours": 14.5,
      "phases_total": 2,
      "implementation_timeline": "4 weeks",
      "critical_path": [
        "FR-001 (foundational, blocks FR-003, FR-005)",
        "FR-003 (core logic, blocks FR-007)"
      ],
      "launch_readiness_gates": [
        "Phase 1 Complete: All auth and data models pass unit tests",
        "Phase 2 Complete: E2E integration tests pass with >80% coverage"
      ],
      "research_recommendations": [
        {
          "step_id": "FR-001-step-2",
          "priority": "MUST",
          "risk_score": 0.85,
          "risk_factors": ["external_api", "security_critical"],
          "recommendation": "Research JWT best practices and token rotation strategies"
        }
      ]
    }
  },
  "algorithms_applied": [
    "specmd-section-detection",
    "cynefin-complexity-classification",
    "moscow-to-phase-mapping",
    "fr-to-feature-conversion",
    "step-generation",
    "critical-path-calculation",
    "effort-estimation",
    "category-assignment",
    "validation-gates",
    "quality-score"
  ],
  "quality_score": 0.92,
  "validation_results": {
    "schema_compliance": { "valid": true, "errors": [] },
    "fr_coverage": { "valid": true, "coverage_ratio": 1.0, "missing": [] },
    "phase_structure": { "valid": true, "errors": [], "warnings": [] },
    "acceptance_criteria": { "valid": true, "errors": [], "warnings": [] },
    "risk_coverage": { "valid": true, "coverage_ratio": 1.0, "unannotated_steps": [] }
  },
  "metadata": {
    "generated_at": "2025-12-17T10:30:00Z",
    "spec_source": "docs/01-planning/specifications/feature-name/SPEC.md",
    "complexity_classification": "COMPLICATED",
    "phase_count": 2
  }
}
```


### Failure Response

```json
{
  "status": "FAILURE",
  "error": {
    "code": "VALIDATION_GATE_FAILED",
    "gate": "fr_coverage",
    "message": "FR Coverage below threshold: 85% (missing FR-007, FR-012)",
    "suggestion": "Add features for missing FRs or mark them as Won't in SPEC.md"
  },
  "partial_plan": null,
  "quality_score": 0.68,
  "validation_results": {
    "schema_compliance": { "valid": true, "errors": [] },
    "fr_coverage": { "valid": false, "coverage_ratio": 0.85, "missing": ["FR-007", "FR-012"] },
    "phase_structure": { "valid": true, "errors": [], "warnings": [] },
    "acceptance_criteria": { "valid": true, "errors": [], "warnings": [] }
  },
  "recovery_actions": [
    "Add FR-007 feature to Phase 2",
    "Add FR-012 feature to Phase 3 or mark as Won't in SPEC.md"
  ]
}
```

### Error Codes

| Code | Gate | Meaning | Recovery |
|------|------|---------|----------|
| `SCHEMA_INVALID` | Schema Compliance | Missing required fields in plan structure | Add missing fields to plan object |
| `FR_COVERAGE_FAILED` | FR Coverage | Not all FRs mapped to features | Add missing features or mark FRs as Won't |
| `PHASE_STRUCTURE_INVALID` | Phase Structure | Phase constraints violated | Rebalance features across phases |
| `ACCEPTANCE_CRITERIA_MISSING` | Acceptance Criteria | Features lack measurable criteria | Add acceptance criteria to features |
| `QUALITY_BELOW_THRESHOLD` | Quality Score | quality_score < 0.70 | Address highest-weight validation failures |
| `SPEC_PARSE_FAILED` | Section Detection | Cannot parse SPEC.md structure | Verify SPEC.md format and required sections |
| `CIRCULAR_DEPENDENCY` | Critical Path | Dependency cycle detected | Remove circular FR references |
| `RISK_COVERAGE_FAILED` | Risk Coverage | Steps missing risk annotations | Re-run plan-risk-assessment or provide manual annotations |

### Quality Thresholds

| Score Range | Grade | Action |
|-------------|-------|--------|
| >= 0.85 | PASS | Return SUCCESS with full plan |
| 0.70 - 0.84 | WARN | Return SUCCESS with warnings in validation_results |
| < 0.70 | FAIL | Return FAILURE with recovery_actions |

---

## Anti-Patterns

### NEVER DO

| Anti-Pattern | Why It's Wrong | Correct Approach |
|--------------|----------------|------------------|
| Duplicate algorithm logic | Maintenance burden, drift risk | Reference `generating-plans` skill |
| Skip Section Detection | Missing FRs, incomplete plans | Always apply specmd-section-detection first |
| Ignore Complexity Classification | Wrong phase count, poor structure | Apply cynefin-complexity-classification |
| Skip MoSCoW Mapping | Must features not prioritized | Apply moscow-to-phase-mapping |
| Manual phase assignment | Inconsistent, error-prone | Use MoSCoW-to-Phase Mapping algorithm |
| Skip Critical Path | Unknown blocking dependencies | Always calculate critical path |
| Output without validation | Quality unknown, may fail downstream | Run all 4 validation gates |
| Estimate effort manually | Inconsistent estimates | Use effort-estimation-model formula |
| Return partial plan on FAILURE | Downstream consumers expect complete plans | Either SUCCESS or FAILURE, never partial |

### Algorithm Duplication Check

Before adding ANY algorithm logic to this skill, verify:

```
1. Does generating-plans already have this algorithm?
   -> YES: Reference it, DO NOT duplicate
   -> NO: Consider adding to generating-plans first

2. Is this orchestration-only logic?
   -> YES: Can add here (e.g., phase building, summary generation)
   -> NO: Add to generating-plans

3. Does it transform data between algorithms?
   -> YES: Can add here (e.g., format conversion)
   -> NO: Add to generating-plans
```

### Pipeline Anti-Patterns

```
# WRONG: Skipping steps
spec -> FR-to-Feature -> Output  # Missing complexity, MoSCoW, validation

# WRONG: Out-of-order execution
spec -> Effort Estimation -> MoSCoW Mapping  # Effort needs features first

# CORRECT: Full pipeline in order
spec -> Section Detection -> Complexity -> MoSCoW -> FR-to-Feature 
     -> Steps -> Critical Path -> Effort -> Category -> Validation -> Output
```

### Output Anti-Patterns

```
# WRONG: Missing algorithms_applied
{
  "status": "SUCCESS",
  "plan": {...}
  // No algorithms_applied list!
}

# WRONG: Incomplete validation_results
{
  "status": "SUCCESS",
  "plan": {...},
  "validation_results": {
    "schema_compliance": {...}
    // Missing other 3 gates!
  }
}

# CORRECT: All required fields present
{
  "status": "SUCCESS",
  "plan": {...},
  "algorithms_applied": ["specmd-section-detection", ...],
  "quality_score": 0.92,
  "validation_results": {
    "schema_compliance": {...},
    "fr_coverage": {...},
    "phase_structure": {...},
    "acceptance_criteria": {...}
  }
}
```

---

## Quick Reference

```
PLAN GENERATION PROTOCOL:
  
  Pipeline Steps (in order):
    1. Section Detection        -> generating-plans#specmd-section-detection
    2. Complexity Classification -> generating-plans#cynefin-complexity-classification
    3. MoSCoW-to-Phase Mapping  -> generating-plans#moscow-to-phase-mapping-algorithm
    4. FR-to-Feature Conversion -> generating-plans#fr-to-feature-conversion-algorithm
    5. Step Generation          -> generating-plans#step-generation-algorithm
    5b. Risk Annotation         -> Apply risk data from plan-risk-assessment (if available)
    6. Critical Path Calculation -> generating-plans#critical-path-calculation
    7. Effort Estimation        -> generating-plans#effort-estimation-model
    8. Category Assignment      -> generating-plans#category-assignment-rules
    9. Validation (5 gates)     -> generating-plans#validation-gates + risk_coverage
   10. Quality Score            -> Modified formula with risk_coverage weight

PHASE BUILDING:
  - Phase count from Complexity Classification (1-4 phases)
  - Must features -> Phase 1 only
  - Should features -> Phase 1-2
  - Could features -> Phase 2-3
  - Target 3-7 features per phase
  - Rebalance if under/over-loaded

SUMMARY GENERATION:
  - total_features = sum of all phase features
  - total_estimated_hours = sum of feature.estimated_hours
  - critical_path = formatted blocking feature chain
  - launch_readiness_gates = 1 per phase

QUALITY THRESHOLDS:
  >= 0.85  -> PASS (return SUCCESS)
  0.70-0.84 -> WARN (return SUCCESS with warnings)
  < 0.70   -> FAIL (return FAILURE with recovery_actions)

VALIDATION GATES (all must pass for PASS):
  1. Schema Compliance    (0.20 weight)
  2. FR Coverage          (0.25 weight)
  3. Phase Structure      (0.20 weight)
  4. Acceptance Criteria  (0.15 weight)
  5. Risk Coverage        (0.20 weight) - NEW

QUALITY SCORE FORMULA:
  quality_score = schema(0.20) + coverage(0.25) + structure(0.20) + criteria(0.15) + risk_coverage(0.20)
  
  Where risk_coverage = steps_with_risk_annotation / steps_requiring_annotation
  Note: If no risk assessment provided, risk_coverage defaults to 1.0 (not penalized)

OUTPUT CONTRACT:
  SUCCESS: plan{}, algorithms_applied[], quality_score, validation_results{}
  FAILURE: error{}, quality_score, validation_results{}, recovery_actions[]

STEP OBJECT STRUCTURE (with risk data):
  {
    step_id: string,           // Format: {FR-ID}-step-{N}
    description: string,       // Step description
    risk_score: float,         // 0.0-1.0, from risk assessment
    research_required: bool,   // true if priority=MUST
    risk_factors: string[]     // List of risk factors
  }

RESEARCH_RECOMMENDATIONS PASS-THROUGH:
  - If risk_assessment provided, include research_recommendations in plan.summary
  - Enables downstream consumers to access original risk recommendations

ALGORITHM REFERENCE (DO NOT DUPLICATE):
  All algorithms live in generating-plans SKILL.md
  This skill ONLY orchestrates their application

INPUT CONTRACT:
  {
    feature_name: string,
    description: string,
    functional_requirements: FR[],
    complexity_classification: "SIMPLE"|"COMPLICATED"|"COMPLEX"|"CHAOTIC",
    dependencies: string[],
    // Optional - from plan-risk-assessment
    risk_assessment?: {
      research_recommendations: [{
        step_id: string,
        priority: "MUST"|"SHOULD"|"COULD"|"NONE",
        risk_score: float,
        risk_factors: string[],
        recommendation: string
      }],
      summary: {
        total_steps_assessed: int,
        must_research: int,
        should_research: int,
        could_research: int,
        no_research_needed: int
      }
    }
  }
```

---

## TB-Mode Plan Generation

When TB-mode is detected (via plan-creator agent), this skill applies Terminal Bench-specific generation logic.

### TB-Mode Activation

The skill receives `mode="tb"` parameter when invoked in TB-mode. Detection occurs in the plan-creator agent based on:
- File path contains `terminal-bench` or `harbor_tasks`
- Spec file is `plan/TB-SPEC.md`
- Spec contains "HARD Score" or "Tier 2" sections

### Phase Mapping (Terminal Bench Specific)

TB-mode uses a fixed 3-phase structure instead of MoSCoW-derived phases:

| Phase | Steps | Features | Purpose |
|-------|-------|----------|---------|
| `phase_1_create` | 1-2 | Directory setup, configuration | Initial task scaffolding |
| `phase_2_build` | 3-7 | instruction.md, task.toml, Dockerfile, solve.sh, tests | Core implementation |
| `phase_3_validate` | 8-11 | Oracle, agent testing, LLMaJ, verification | Validation and submission |

### Difficulty Validation Section

Extract from TB-SPEC.md and include in output:

```json
{
  "difficulty_validation": {
    "hard_score": 6.2,
    "tier1_factors": [
      "multi_system_interaction",
      "domain_expertise",
      "temporal_stateful_reasoning",
      "extensive_edge_cases"
    ],
    "tier2_factors": [
      "long_range_dependency",
      "consistency_stress"
    ],
    "tier2_highest": 0.85,
    "edge_case_count": 14,
    "exploitation_score": 7,
    "verdict": "HARD_CONFIRMED"
  }
}
```

### Extraction Rules

| Field | Source | Extraction Logic |
|-------|--------|------------------|
| `hard_score` | HARD Score header | Parse numeric value from `## HARD Score: X.X` |
| `tier1_factors` | Tier 1 section | Extract factor names from checklist items |
| `tier2_factors` | Tier 2 section | Extract factor names from `### Tier 2:` subsections |
| `tier2_highest` | Tier 2 scores | Find max value among Tier 2 factor scores |
| `edge_case_count` | Pre-Mortem section | Count items in edge case list |
| `exploitation_score` | Cognitive Exploitation Matrix | Parse value from exploitation rating |

### TB-Mode Pipeline Modifications

```
TB-SPEC.md Input
    |
    +-> STEP 1: Section Detection (standard)
    |
    +-> STEP 2: Difficulty Extraction (TB-specific)
    |     -> Extract hard_score, tier factors, edge cases
    |     -> Validate against HARD thresholds
    |
    +-> STEP 3: Fixed 3-Phase Mapping (TB-specific)
    |     -> No MoSCoW mapping
    |     -> Map features to phase_1_create, phase_2_build, phase_3_validate
    |
    +-> STEP 4-8: (standard with TB categories)
    |
    +-> STEP 9: TB Validation Gates
    |     -> hard_score >= 5.5
    |     -> tier2_highest >= 0.7
    |     -> edge_case_count >= 10
    |     -> exploitation_score >= 5
    |
    +-> Output: TB-PLAN.json
```

### Output Path

Write output to `plan/TB-PLAN.json` relative to task directory (not standard PLAN.json location).

Example paths:
- Input: `tasks/parse-logs/plan/TB-SPEC.md`
- Output: `tasks/parse-logs/plan/TB-PLAN.json`

### TB-Mode Validation

All standard validation gates plus TB-specific thresholds:

| Gate | Threshold | Failure Action |
|------|-----------|----------------|
| HARD Score | >= 5.5 | Return FAILURE with hardening suggestions |
| Tier 2 Highest | >= 0.7 | Return FAILURE with exploitation recommendations |
| Edge Case Count | >= 10 | Return FAILURE with edge case expansion guidance |
| Exploitation Score | >= 5 | Return FAILURE with LLM weakness analysis |
| 3-Phase Structure | All 3 present | Return FAILURE if phases missing |
| Feature-to-FR Mapping | Complete | Return FAILURE with unmapped features |

### TB-Mode Quality Score

Modified formula for TB-mode:

```
TB_Quality_Score = 
  Schema(0.15) + 
  FR_Coverage(0.20) + 
  Phase_Structure(0.20) + 
  Difficulty_Validation(0.25) + 
  Acceptance_Criteria(0.20)
```

### Schema Reference

TB-PLAN output must validate against:
`.claude/agents/terminal-bench/common/templates/TB-PLAN.schema.json`

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| `generating-plans` | **Source of all algorithms** - reference, never duplicate |
| `validating-specifications` | Upstream - validates SPEC.md before plan generation |
| `generating-tasks` | Downstream - PLAN.json becomes input for task generation |
| `task-context-synthesis` | Parallel - builds context that may inform plan generation |

---

## Cross-References

- **Algorithm Source**: [generating-plans/SKILL.md](../generating-plans/SKILL.md)
- **Specification Validation**: [validating-specifications/SKILL.md](../validating-specifications/SKILL.md)
- **Task Generation**: [generating-tasks/SKILL.md](../generating-tasks/SKILL.md)
- **Thinking Frameworks**: [../../docs/00-core/frameworks/README.md](../../docs/00-core/frameworks/README.md)

---

## Thinking Frameworks

**Full Catalog**: [Thinking Frameworks README](../../docs/00-core/frameworks/README.md)

**Most Relevant for Plan Generation**:

| Framework | When to Use |
|-----------|-------------|
| [CAGEERF](../../docs/00-core/frameworks/planning.md) | Multi-phase plan structuring |
| [Systems Thinking](../../docs/00-core/frameworks/analysis.md) | Dependency and critical path analysis |
| [MoSCoW](../../docs/00-core/frameworks/planning.md) | Priority-based phase mapping |
| [Pre-Mortem](../../docs/00-core/frameworks/strategy.md) | Plan validation before output |

> **Selection Tip**: phase structure -> CAGEERF, dependencies -> Systems, priorities -> MoSCoW, validation -> Pre-Mortem
