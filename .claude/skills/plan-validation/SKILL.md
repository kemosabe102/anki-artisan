---
name: plan-validation
description: >
  Use this skill when validating generated plans through 4 blocking gates.
  Calculates quality scores and identifies violations.
  Trigger keywords: validate plan, quality gates, plan quality, FR coverage.
---

# Plan Validation

*Validate generated plans through 4 sequential blocking gates, calculate quality score, identify violations*

## Contents

- [Validation Pipeline Overview](#validation-pipeline-overview)
- [Gate 1: Schema Compliance](#gate-1-schema-compliance)
- [Gate 2: FR Coverage](#gate-2-fr-coverage)
- [Gate 3: Phase Structure](#gate-3-phase-structure)
- [Gate 4: Acceptance Criteria](#gate-4-acceptance-criteria)
- [Quality Score Formula](#quality-score-formula)
- [Threshold Definitions](#threshold-definitions)
- [Output Contract](#output-contract)
- [Anti-Patterns](#anti-patterns)
- [Quick Reference](#quick-reference)

---


## Validation Pipeline Overview

**All 4 gates execute in sequence. Failure at any gate is BLOCKING.**

```
INPUT: {
  plan: PLAN.json (generated plan object),
  spec_metadata: {
    functional_requirements: FR[],
    acceptance_criteria_source: Map<FR_ID, string[]>
  }
}

PROCESS:
  1. Gate 1: Schema Compliance   -> Validate JSON structure matches schema
  2. Gate 2: FR Coverage         -> Verify all FRs from SPEC have features
  3. Gate 3: Phase Structure     -> Check phase constraints and balance
  4. Gate 4: Acceptance Criteria -> Ensure criteria exist and match SPEC

  IF any gate FAILS:
    STOP and return FAIL with violations
  
  Calculate quality_score from all dimensions
  Return status based on thresholds

OUTPUT: ValidationResult (see Output Contract below)
```

### Validation Flow Diagram

```
Plan Input
    ↓
┌─────────────────────────────────────┐
│  Gate 1: Schema Compliance          │
│  -> Check: project, description,    │
│     total_features, phases, summary │
│  -> BLOCKING if any field missing   │
└─────────────────────────────────────┘
    ↓ (pass)
┌─────────────────────────────────────┐
│  Gate 2: FR Coverage                │
│  -> Check: Every FR-ID in SPEC.md   │
│     has corresponding feature.id    │
│  -> BLOCKING if coverage < 100%     │
└─────────────────────────────────────┘
    ↓ (pass)
┌─────────────────────────────────────┐
│  Gate 3: Phase Structure            │
│  -> Check: Phase 1 has >= 1 Must    │
│  -> Check: Each phase <= 8 features │
│  -> Check: Feature hours in range   │
│  -> BLOCKING if constraints violated│
└─────────────────────────────────────┘
    ↓ (pass)
┌─────────────────────────────────────┐
│  Gate 4: Acceptance Criteria        │
│  -> Check: Every feature has >= 1   │
│  -> Check: Criteria from SPEC       │
│  -> BLOCKING if criteria missing    │
└─────────────────────────────────────┘
    ↓ (pass)
Calculate Quality Score
    ↓
Return PASS/WARN/FAIL
```


---

## Gate 1: Schema Compliance

**Purpose**: Ensure plan JSON structure matches `feature_plan_blank.json` schema.

**Reference**: Schema template at `.claude/docs/command-docs/plan/templates/feature_plan_blank.json`

### Required Fields by Level

| Level | Required Fields | Type |
|-------|-----------------|------|
| Root | `project` | string |
| Root | `description` | string |
| Root | `total_features` | number |
| Root | `phases` | object |
| Root | `summary` | object |
| Phase | `name` | string |
| Phase | `duration_weeks` | number |
| Phase | `target_completion` | string |
| Phase | `features` | array |
| Feature | `id` | string (FR-XXX pattern) |
| Feature | `category` | enum: functional, testing, infrastructure, documentation, performance |
| Feature | `description` | string |
| Feature | `steps` | array (2-5 items) |
| Feature | `acceptance_criteria` | array (1+ items) |
| Feature | `passes` | boolean |
| Feature | `estimated_hours` | number (0.5-3.0) |
| Summary | `total_features` | number |
| Summary | `total_estimated_hours` | number |
| Summary | `phases_total` | number |
| Summary | `implementation_timeline` | string |
| Summary | `critical_path` | array |
| Summary | `launch_readiness_gates` | array |


### Validation Logic

```
FUNCTION validate_schema(plan):
  violations = []
  
  # Root-level fields
  required_root = ['project', 'description', 'total_features', 'phases', 'summary']
  FOR field IN required_root:
    IF field NOT IN plan:
      violations.append({
        level: 'root',
        field: field,
        message: f"Missing required root field: {field}"
      })
  
  # Phase-level fields
  IF 'phases' IN plan:
    FOR phase_key, phase IN plan['phases'].items():
      required_phase = ['name', 'duration_weeks', 'target_completion', 'features']
      FOR field IN required_phase:
        IF field NOT IN phase:
          violations.append({
            level: 'phase',
            phase: phase_key,
            field: field,
            message: f"Phase {phase_key} missing field: {field}"
          })
      
      # Feature-level fields
      IF 'features' IN phase:
        FOR idx, feature IN enumerate(phase['features']):
          required_feature = [
            'id', 'category', 'description', 'steps',
            'acceptance_criteria', 'passes', 'estimated_hours'
          ]
          FOR field IN required_feature:
            IF field NOT IN feature:
              violations.append({
                level: 'feature',
                phase: phase_key,
                feature_index: idx,
                feature_id: feature.get('id', f'index_{idx}'),
                field: field,
                message: f"Feature {feature.get('id', idx)} missing field: {field}"
              })
  
  # Summary-level fields
  IF 'summary' IN plan:
    required_summary = [
      'total_features', 'total_estimated_hours', 'phases_total',
      'implementation_timeline', 'critical_path', 'launch_readiness_gates'
    ]
    FOR field IN required_summary:
      IF field NOT IN plan['summary']:
        violations.append({
          level: 'summary',
          field: field,
          message: f"Summary missing field: {field}"
        })
  
  RETURN {
    passed: len(violations) == 0,
    violations: violations,
    schema_score: 1.0 IF len(violations) == 0 ELSE 0.0
  }
```


### Gate 1 Result Example

```json
{
  "passed": false,
  "violations": [
    {
      "level": "feature",
      "phase": "phase_1",
      "feature_id": "FR-003",
      "field": "estimated_hours",
      "message": "Feature FR-003 missing field: estimated_hours"
    },
    {
      "level": "summary",
      "field": "critical_path",
      "message": "Summary missing field: critical_path"
    }
  ],
  "schema_score": 0.0
}
```

---

## Gate 2: FR Coverage

**Purpose**: Verify every FR-ID from SPEC.md has a corresponding feature in the plan.

**Reference**: See [generating-plans#validation-gates](../generating-plans/SKILL.md#validation-gates) for FR coverage algorithm.


### Coverage Calculation

```
coverage = mapped_fr_count / total_spec_fr_count

WHERE:
  mapped_fr_count = count of unique FR-IDs found in plan features
  total_spec_fr_count = count of FRs in SPEC.md (excluding Won't priority)

THRESHOLD:
  coverage < 1.0 = FAIL (all FRs must be covered)
```

### FR Coverage Validation Logic

```
FUNCTION validate_fr_coverage(plan, spec_metadata):
  # Extract FRs from SPEC metadata (excluding Won't)
  spec_frs = [
    fr.id FOR fr IN spec_metadata.functional_requirements
    IF fr.priority != "Won't"
  ]
  spec_fr_set = set(spec_frs)
  
  # Extract feature IDs from plan
  plan_frs = set()
  FOR phase IN plan['phases'].values():
    FOR feature IN phase.get('features', []):
      feature_id = feature.get('id', '')
      
      # Handle split features (FR-001-A -> FR-001)
      base_id = extract_base_fr_id(feature_id)
      plan_frs.add(base_id)
      
      # Also check description for FR references
      desc_refs = extract_fr_references(feature.get('description', ''))
      plan_frs.update(desc_refs)
  
  # Calculate coverage
  covered_frs = spec_fr_set.intersection(plan_frs)
  missing_frs = spec_fr_set - plan_frs
  
  coverage = len(covered_frs) / len(spec_fr_set) IF spec_fr_set ELSE 1.0
  
  RETURN {
    passed: len(missing_frs) == 0,
    coverage: coverage,
    missing_frs: sorted(list(missing_frs)),
    covered_count: len(covered_frs),
    total_count: len(spec_fr_set),
    message: f"FR Coverage: {coverage:.1%} ({len(covered_frs)}/{len(spec_fr_set)})"
  }

FUNCTION extract_base_fr_id(feature_id):
  # FR-001-A -> FR-001
  # FR-015 -> FR-015
  match = re.match(r'(FR-\d+)', feature_id)
  RETURN match.group(1) IF match ELSE feature_id

FUNCTION extract_fr_references(text):
  # Find all FR-XXX patterns in text
  RETURN set(re.findall(r'FR-\d+', text))
```


### Gate 2 Result Example

```json
{
  "passed": false,
  "coverage": 0.875,
  "missing_frs": ["FR-007", "FR-012"],
  "covered_count": 14,
  "total_count": 16,
  "message": "FR Coverage: 87.5% (14/16)"
}
```

---

## Gate 3: Phase Structure

**Purpose**: Validate phase organization, feature distribution, and effort estimates.

**Reference**: See [generating-plans#validation-gates](../generating-plans/SKILL.md#validation-gates) for phase structure rules.

### Phase Structure Rules

| Rule | Constraint | Validation |
|------|------------|------------|
| Must in Phase 1 | All Must-priority features MUST be in Phase 1 | BLOCKING |
| Feature Limit | Each phase <= 8 features | BLOCKING |
| Feature Minimum | Each phase >= 1 feature | BLOCKING |
| Hour Range | Each feature 0.5-3.0 hours | BLOCKING |
| No Duplicates | No duplicate feature IDs | BLOCKING |
| Phase Count | 1-4 phases | WARNING |
| Balance | 3-7 features per phase | WARNING |


### Phase Structure Validation Logic

```
FUNCTION validate_phase_structure(plan):
  violations = []
  warnings = []
  all_feature_ids = []
  
  phases = list(plan.get('phases', {}).items())
  
  # Rule: 1-4 phases
  IF len(phases) < 1:
    violations.append({
      rule: 'PHASE_COUNT',
      message: "Plan must have at least 1 phase"
    })
  IF len(phases) > 4:
    warnings.append({
      rule: 'PHASE_COUNT',
      message: f"Plan has {len(phases)} phases (recommended: 1-4)"
    })
  
  FOR phase_idx, (phase_key, phase) IN enumerate(phases):
    features = phase.get('features', [])
    feature_count = len(features)
    
    # Rule: Each phase >= 1 feature
    IF feature_count < 1:
      violations.append({
        rule: 'FEATURE_MINIMUM',
        phase: phase_key,
        message: f"Phase {phase_key} has no features"
      })
    
    # Rule: Each phase <= 8 features
    IF feature_count > 8:
      violations.append({
        rule: 'FEATURE_LIMIT',
        phase: phase_key,
        count: feature_count,
        message: f"Phase {phase_key} has {feature_count} features (max: 8)"
      })
    
    # Warning: 3-7 features optimal
    IF feature_count < 3:
      warnings.append({
        rule: 'FEATURE_BALANCE',
        phase: phase_key,
        message: f"Phase {phase_key} under-loaded ({feature_count} features)"
      })
    ELSE IF feature_count > 7:
      warnings.append({
        rule: 'FEATURE_BALANCE',
        phase: phase_key,
        message: f"Phase {phase_key} over-loaded ({feature_count} features)"
      })
    
    FOR feature IN features:
      feature_id = feature.get('id', '')
      all_feature_ids.append(feature_id)
      
      # Rule: Hour range 0.5-3.0
      hours = feature.get('estimated_hours', 0)
      IF hours < 0.5 OR hours > 3.0:
        violations.append({
          rule: 'HOUR_RANGE',
          feature_id: feature_id,
          phase: phase_key,
          hours: hours,
          message: f"Feature {feature_id} has {hours} hours (valid: 0.5-3.0)"
        })
      
      # Rule: Must features only in Phase 1
      IF feature.get('priority') == 'Must' AND phase_idx > 0:
        violations.append({
          rule: 'MUST_IN_PHASE_1',
          feature_id: feature_id,
          phase: phase_key,
          message: f"Must-priority feature {feature_id} not in Phase 1"
        })
  
  # Rule: No duplicate feature IDs
  seen_ids = set()
  FOR fid IN all_feature_ids:
    IF fid IN seen_ids:
      violations.append({
        rule: 'NO_DUPLICATES',
        feature_id: fid,
        message: f"Duplicate feature ID: {fid}"
      })
    seen_ids.add(fid)
  
  # Calculate structure score
  structure_score = calculate_structure_score(violations, warnings)
  
  RETURN {
    passed: len(violations) == 0,
    violations: violations,
    warnings: warnings,
    structure_score: structure_score
  }

FUNCTION calculate_structure_score(violations, warnings):
  IF len(violations) > 0:
    RETURN 0.0
  
  # Deduct for warnings (0.1 per warning, min 0.5)
  warning_penalty = len(warnings) * 0.1
  RETURN max(0.5, 1.0 - warning_penalty)
```


### Gate 3 Result Example

```json
{
  "passed": false,
  "violations": [
    {
      "rule": "MUST_IN_PHASE_1",
      "feature_id": "FR-002",
      "phase": "phase_2",
      "message": "Must-priority feature FR-002 not in Phase 1"
    },
    {
      "rule": "HOUR_RANGE",
      "feature_id": "FR-005",
      "phase": "phase_1",
      "hours": 4.5,
      "message": "Feature FR-005 has 4.5 hours (valid: 0.5-3.0)"
    }
  ],
  "warnings": [
    {
      "rule": "FEATURE_BALANCE",
      "phase": "phase_3",
      "message": "Phase phase_3 under-loaded (2 features)"
    }
  ],
  "structure_score": 0.0
}
```

---

## Gate 4: Acceptance Criteria

**Purpose**: Ensure every feature has acceptance criteria that match SPEC.md.

**Reference**: See [generating-plans#validation-gates](../generating-plans/SKILL.md#validation-gates) for criteria validation.


### Acceptance Criteria Rules

| Rule | Constraint | Validation |
|------|------------|------------|
| Minimum Criteria | Every feature has >= 1 acceptance criterion | BLOCKING |
| Source Validation | Criteria copied from SPEC (not invented) | BLOCKING |
| Measurability | Criteria should be testable/verifiable | WARNING |

### Acceptance Criteria Validation Logic

```
FUNCTION validate_acceptance_criteria(plan, spec_metadata):
  violations = []
  warnings = []
  criteria_stats = { total: 0, from_spec: 0, invented: 0 }
  
  # Build lookup of SPEC acceptance criteria
  spec_criteria_map = build_spec_criteria_map(spec_metadata)
  
  FOR phase IN plan.get('phases', {}).values():
    FOR feature IN phase.get('features', []):
      feature_id = feature.get('id', '')
      criteria = feature.get('acceptance_criteria', [])
      
      # Rule: >= 1 criterion per feature
      IF len(criteria) < 1:
        violations.append({
          rule: 'MINIMUM_CRITERIA',
          feature_id: feature_id,
          message: f"Feature {feature_id} has no acceptance criteria"
        })
        CONTINUE
      
      criteria_stats.total += len(criteria)
      
      FOR criterion IN criteria:
        # Rule: Criteria from SPEC (not invented)
        source_check = check_criterion_source(
          criterion, 
          feature_id, 
          spec_criteria_map
        )
        
        IF source_check.from_spec:
          criteria_stats.from_spec += 1
        ELSE:
          criteria_stats.invented += 1
          violations.append({
            rule: 'SOURCE_VALIDATION',
            feature_id: feature_id,
            criterion: criterion[:50] + '...' IF len(criterion) > 50 ELSE criterion,
            message: f"Criterion not found in SPEC.md for {feature_id}"
          })
        
        # Warning: Check measurability
        IF NOT is_measurable(criterion):
          warnings.append({
            rule: 'MEASURABILITY',
            feature_id: feature_id,
            criterion: criterion[:50] + '...',
            message: f"Criterion may not be measurable: '{criterion[:30]}...'"
          })
  
  # Calculate criteria score
  criteria_score = calculate_criteria_score(violations, warnings, criteria_stats)
  
  RETURN {
    passed: len(violations) == 0,
    violations: violations,
    warnings: warnings,
    criteria_stats: criteria_stats,
    criteria_score: criteria_score
  }
```


### Helper Functions

```
FUNCTION build_spec_criteria_map(spec_metadata):
  """
  Build a map of FR-ID -> list of acceptance criteria from SPEC.md
  """
  criteria_map = {}
  
  FOR fr_id, criteria_list IN spec_metadata.acceptance_criteria_source.items():
    # Normalize criteria for comparison
    normalized = [normalize_criterion(c) FOR c IN criteria_list]
    criteria_map[fr_id] = normalized
  
  RETURN criteria_map

FUNCTION check_criterion_source(criterion, feature_id, spec_criteria_map):
  """
  Check if criterion exists in SPEC.md for this FR-ID
  """
  normalized_criterion = normalize_criterion(criterion)
  base_fr_id = extract_base_fr_id(feature_id)
  
  # Check exact FR match
  IF base_fr_id IN spec_criteria_map:
    spec_criteria = spec_criteria_map[base_fr_id]
    FOR spec_criterion IN spec_criteria:
      IF fuzzy_match(normalized_criterion, spec_criterion):
        RETURN { from_spec: True, match: spec_criterion }
  
  # Check all FRs for similar criterion (may be shared)
  FOR fr_id, spec_criteria IN spec_criteria_map.items():
    FOR spec_criterion IN spec_criteria:
      IF fuzzy_match(normalized_criterion, spec_criterion):
        RETURN { from_spec: True, match: spec_criterion, source_fr: fr_id }
  
  RETURN { from_spec: False }

FUNCTION normalize_criterion(text):
  """
  Normalize criterion text for comparison
  """
  # Lowercase, remove extra whitespace
  normalized = ' '.join(text.lower().split())
  # Remove common prefixes
  normalized = re.sub(r'^(the\s+|a\s+|an\s+)', '', normalized)
  RETURN normalized

FUNCTION fuzzy_match(criterion1, criterion2, threshold=0.8):
  """
  Check if two criteria are similar enough to be considered a match
  """
  # Use token-based similarity
  tokens1 = set(criterion1.split())
  tokens2 = set(criterion2.split())
  
  intersection = len(tokens1 & tokens2)
  union = len(tokens1 | tokens2)
  
  jaccard = intersection / union IF union > 0 ELSE 0
  
  RETURN jaccard >= threshold

FUNCTION is_measurable(criterion):
  """
  Check if criterion contains measurable/testable indicators
  """
  measurable_patterns = [
    r'\d+',                          # Contains numbers
    r'\b(pass|fail|success|error)\b', # Pass/fail conditions
    r'\b(return|output|display|show|render)\b',  # Observable actions
    r'\b(within|under|above|below|at least|at most)\b',  # Thresholds
    r'\b(complete|exist|contain|include|have)\b',  # State verification
    r'\b(valid|invalid|correct|incorrect)\b',  # Validation states
    r'\b(when|if|given|then)\b',     # Conditional logic
  ]
  
  RETURN any(re.search(p, criterion, re.I) FOR p IN measurable_patterns)

FUNCTION calculate_criteria_score(violations, warnings, stats):
  IF len(violations) > 0:
    # Partial credit based on how many criteria are valid
    IF stats.total > 0:
      RETURN stats.from_spec / stats.total
    RETURN 0.0
  
  # Deduct for warnings (0.05 per warning, min 0.7)
  warning_penalty = len(warnings) * 0.05
  RETURN max(0.7, 1.0 - warning_penalty)
```


### Gate 4 Result Example

```json
{
  "passed": false,
  "violations": [
    {
      "rule": "MINIMUM_CRITERIA",
      "feature_id": "FR-008",
      "message": "Feature FR-008 has no acceptance criteria"
    },
    {
      "rule": "SOURCE_VALIDATION",
      "feature_id": "FR-003",
      "criterion": "System performs well under load...",
      "message": "Criterion not found in SPEC.md for FR-003"
    }
  ],
  "warnings": [
    {
      "rule": "MEASURABILITY",
      "feature_id": "FR-005",
      "criterion": "User experience is good...",
      "message": "Criterion may not be measurable: 'User experience is good...'"
    }
  ],
  "criteria_stats": {
    "total": 24,
    "from_spec": 22,
    "invented": 2
  },
  "criteria_score": 0.92
}
```

---

## Quality Score Formula

**Purpose**: Calculate overall plan quality from gate results.

**Reference**: See [generating-plans#quality-score-formula](../generating-plans/SKILL.md#quality-score-formula) for base formula.


### Formula

```
quality_score = (
  schema_score    × 0.25 +    # Gate 1: Schema Compliance
  coverage_score  × 0.30 +    # Gate 2: FR Coverage
  structure_score × 0.25 +    # Gate 3: Phase Structure
  criteria_score  × 0.20      # Gate 4: Acceptance Criteria
)
```

### Weight Rationale

| Dimension | Weight | Rationale |
|-----------|--------|-----------|
| Schema Compliance | 0.25 | Foundational structure required for downstream processing |
| FR Coverage | 0.30 | Highest weight - missing FRs mean incomplete implementation |
| Phase Structure | 0.25 | Execution order and parallelization depend on structure |
| Acceptance Criteria | 0.20 | Quality of verification, but can be refined during implementation |

### Quality Score Calculation

```
FUNCTION calculate_quality_score(gate_results):
  # Extract scores from each gate
  schema_score = gate_results.gate_1_schema.schema_score
  coverage_score = gate_results.gate_2_fr_coverage.coverage
  structure_score = gate_results.gate_3_phase_structure.structure_score
  criteria_score = gate_results.gate_4_acceptance_criteria.criteria_score
  
  # Apply weights
  quality_score = (
    schema_score    * 0.25 +
    coverage_score  * 0.30 +
    structure_score * 0.25 +
    criteria_score  * 0.20
  )
  
  RETURN {
    total: round(quality_score, 3),
    dimensions: {
      schema: schema_score,
      coverage: coverage_score,
      structure: structure_score,
      criteria: criteria_score
    },
    weights: {
      schema: 0.25,
      coverage: 0.30,
      structure: 0.25,
      criteria: 0.20
    }
  }
```

### Calculation Example

```
Gate Results:
  Gate 1 (Schema):    1.00 (all fields present)
  Gate 2 (Coverage):  0.94 (15/16 FRs covered)
  Gate 3 (Structure): 0.90 (1 warning for under-loaded phase)
  Gate 4 (Criteria):  0.85 (3 measurability warnings)

Quality Score:
  = (1.00 × 0.25) + (0.94 × 0.30) + (0.90 × 0.25) + (0.85 × 0.20)
  = 0.25 + 0.282 + 0.225 + 0.17
  = 0.927

Result: PASS (>= 0.85)
```

---

## Threshold Definitions

**Purpose**: Define pass/warn/fail boundaries and corresponding actions.


### Gate Thresholds (Per-Gate)

**CRITICAL**: Each gate MUST meet its individual minimum threshold. Aggregate scoring alone is insufficient.

| Gate | Minimum Score | Rationale |
|------|--------------|-----------|
| schema_validity | 1.0 | Schema must be 100% valid - no partial compliance |
| section_coverage | 0.6 | At least 60% sections mapped to ensure plan usability |
| step_completeness | 0.6 | At least 60% steps have details for execution clarity |
| fr_traceability | 0.5 | At least 50% FRs traced - baseline requirement tracking |
| effort_estimation | 0.4 | Effort can be estimated/refined later in process |

### Blocking Rules

1. **Schema Validation First**: schema_validity gate MUST pass (1.0) before other gates are evaluated
2. **No Bypass**: All gates must meet their individual minimums - no exceptions allowed
3. **Early Exit**: Validation stops at first failing gate (ordered by importance: schema -> coverage -> structure -> criteria)
4. **No Aggregate Override**: A passing aggregate score (>= 0.6) does NOT override individual gate failures

### Threshold Table

| Score Range | Status | Action | Downstream Impact |
|-------------|--------|--------|-------------------|
| >= 0.85 | **PASS** | Plan ready for task generation | Proceed to `/tasks` |
| 0.70 - 0.84 | **WARN** | Plan usable with review | Manual review before `/tasks` |
| < 0.70 | **FAIL** | Plan must be regenerated | Block `/tasks`, return to `/plan` |

### Status Determination Algorithm

```
FUNCTION determine_status(gate_results, quality_score):
  # Per-gate minimum thresholds (FM-003 fix: prevents aggregate bypass)
  GATE_MINIMUMS = {
    'schema_validity': 1.0,      # Schema must be 100% valid
    'section_coverage': 0.6,     # At least 60% sections mapped
    'step_completeness': 0.6,    # At least 60% steps have details
    'fr_traceability': 0.5,      # At least 50% FRs traced
    'effort_estimation': 0.4     # Effort can be estimated later
  }
  
  # Map gate results to threshold keys
  gate_score_map = {
    'schema_validity': gate_results.gate_1_schema.schema_score,
    'section_coverage': gate_results.gate_2_fr_coverage.coverage,
    'step_completeness': gate_results.gate_3_phase_structure.structure_score,
    'fr_traceability': gate_results.gate_2_fr_coverage.coverage,
    'effort_estimation': gate_results.gate_4_acceptance_criteria.criteria_score
  }
  
  # STEP 1: Check per-gate minimum thresholds (ordered by importance)
  failing_gates = []
  gate_order = ['schema_validity', 'section_coverage', 'step_completeness', 
                'fr_traceability', 'effort_estimation']
  
  FOR gate_name IN gate_order:
    gate_score = gate_score_map[gate_name]
    minimum = GATE_MINIMUMS[gate_name]
    
    IF gate_score < minimum:
      failing_gates.append({
        gate: gate_name,
        score: gate_score,
        minimum: minimum,
        gap: minimum - gate_score
      })
      # Early exit on first failure (ordered validation)
      RETURN {
        status: 'FAIL',
        reason: f'Gate {gate_name} below minimum threshold',
        failing_gates: failing_gates,
        action: f'Raise {gate_name} from {gate_score:.2f} to >= {minimum:.2f}'
      }
  
  # STEP 2: Check boolean gate pass/fail status
  blocking_gates = []
  
  IF NOT gate_results.gate_1_schema.passed:
    blocking_gates.append('gate_1_schema')
  IF NOT gate_results.gate_2_fr_coverage.passed:
    blocking_gates.append('gate_2_fr_coverage')
  IF NOT gate_results.gate_3_phase_structure.passed:
    blocking_gates.append('gate_3_phase_structure')
  IF NOT gate_results.gate_4_acceptance_criteria.passed:
    blocking_gates.append('gate_4_acceptance_criteria')
  
  IF len(blocking_gates) > 0:
    RETURN {
      status: 'FAIL',
      reason: 'Gate failure',
      blocking_gates: blocking_gates,
      failing_gates: [],
      action: 'Address gate violations before proceeding'
    }
  
  # STEP 3: Score-based determination (only if all per-gate minimums pass)
  IF quality_score >= 0.85:
    RETURN {
      status: 'PASS',
      reason: 'All gates passed, high quality',
      failing_gates: [],
      action: 'Plan ready for task generation'
    }
  
  ELSE IF quality_score >= 0.70:
    RETURN {
      status: 'WARN',
      reason: 'All gates passed, quality below optimal',
      failing_gates: [],
      action: 'Review warnings before proceeding',
      recommendations: generate_recommendations(gate_results)
    }
  
  ELSE:
    RETURN {
      status: 'FAIL',
      reason: 'Quality score below threshold',
      failing_gates: [],
      action: 'Regenerate plan with improvements',
      recommendations: generate_recommendations(gate_results)
    }
```

### Recommendation Generation

```
FUNCTION generate_recommendations(gate_results):
  recommendations = []
  
  # Schema recommendations
  IF gate_results.gate_1_schema.schema_score < 1.0:
    violations = gate_results.gate_1_schema.violations
    recommendations.append({
      gate: 'schema',
      priority: 'HIGH',
      action: f"Add {len(violations)} missing fields to plan structure",
      details: [v.message FOR v IN violations[:3]]  # Top 3
    })
  
  # Coverage recommendations
  IF gate_results.gate_2_fr_coverage.coverage < 1.0:
    missing = gate_results.gate_2_fr_coverage.missing_frs
    recommendations.append({
      gate: 'fr_coverage',
      priority: 'HIGH',
      action: f"Add features for {len(missing)} missing FRs",
      details: missing[:5]  # Top 5
    })
  
  # Structure recommendations
  IF gate_results.gate_3_phase_structure.structure_score < 0.85:
    violations = gate_results.gate_3_phase_structure.violations
    warnings = gate_results.gate_3_phase_structure.warnings
    
    IF violations:
      recommendations.append({
        gate: 'phase_structure',
        priority: 'HIGH',
        action: 'Fix phase structure violations',
        details: [v.message FOR v IN violations[:3]]
      })
    IF warnings:
      recommendations.append({
        gate: 'phase_structure',
        priority: 'MEDIUM',
        action: 'Address phase balance warnings',
        details: [w.message FOR w IN warnings[:3]]
      })
  
  # Criteria recommendations
  IF gate_results.gate_4_acceptance_criteria.criteria_score < 0.85:
    violations = gate_results.gate_4_acceptance_criteria.violations
    
    IF violations:
      recommendations.append({
        gate: 'acceptance_criteria',
        priority: 'HIGH',
        action: 'Add/fix acceptance criteria from SPEC.md',
        details: [v.message FOR v IN violations[:3]]
      })
  
  # Sort by priority
  priority_order = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}
  recommendations.sort(key=lambda r: priority_order.get(r.priority, 99))
  
  RETURN recommendations
```

---

## Output Contract

**Purpose**: Define validation result structure for consumers.


### Input Contract

```json
{
  "plan": {
    "project": "string",
    "description": "string",
    "total_features": "number",
    "phases": {
      "phase_N": {
        "name": "string",
        "duration_weeks": "number",
        "target_completion": "string",
        "features": [
          {
            "id": "FR-XXX",
            "category": "functional|testing|infrastructure|documentation|performance",
            "description": "string",
            "steps": ["string"],
            "acceptance_criteria": ["string"],
            "passes": "boolean",
            "estimated_hours": "number"
          }
        ]
      }
    },
    "summary": {
      "total_features": "number",
      "total_estimated_hours": "number",
      "phases_total": "number",
      "implementation_timeline": "string",
      "critical_path": ["string"],
      "launch_readiness_gates": ["string"]
    }
  },
  "spec_metadata": {
    "functional_requirements": [
      {
        "id": "FR-XXX",
        "description": "string",
        "priority": "Must|Should|Could|Won't"
      }
    ],
    "acceptance_criteria_source": {
      "FR-XXX": ["criterion 1", "criterion 2"]
    }
  }
}
```


### Output Contract

```json
{
  "status": "PASS | WARN | FAIL",
  "quality_score": 0.87,
  "validation_result": {
    "passed": true,
    "aggregate_score": 0.87,
    "failing_gates": [],
    "per_gate_status": {
      "schema_validity": { "score": 1.0, "minimum": 1.0, "passed": true },
      "section_coverage": { "score": 0.85, "minimum": 0.6, "passed": true },
      "step_completeness": { "score": 0.9, "minimum": 0.6, "passed": true },
      "fr_traceability": { "score": 0.85, "minimum": 0.5, "passed": true },
      "effort_estimation": { "score": 0.75, "minimum": 0.4, "passed": true }
    }
  },
  "gate_results": {
    "gate_1_schema": {
      "passed": true,
      "violations": [],
      "schema_score": 1.0
    },
    "gate_2_fr_coverage": {
      "passed": true,
      "coverage": 1.0,
      "missing_frs": [],
      "covered_count": 16,
      "total_count": 16
    },
    "gate_3_phase_structure": {
      "passed": true,
      "violations": [],
      "warnings": [],
      "structure_score": 0.9
    },
    "gate_4_acceptance_criteria": {
      "passed": true,
      "violations": [],
      "warnings": [],
      "criteria_stats": {
        "total": 32,
        "from_spec": 32,
        "invented": 0
      },
      "criteria_score": 0.95
    }
  },
  "recommendations": [
    {
      "gate": "phase_structure",
      "priority": "MEDIUM",
      "action": "Consider rebalancing phase_3 (2 features)",
      "details": ["Phase phase_3 under-loaded (2 features)"]
    }
  ],
  "metadata": {
    "validated_at": "2025-12-17T10:30:00Z",
    "plan_source": "PLAN.json",
    "spec_source": "SPEC.md",
    "validator_version": "1.1.0"
  }
}
```

### Success Response Example

```json
{
  "status": "PASS",
  "quality_score": 0.927,
  "gate_results": {
    "gate_1_schema": {
      "passed": true,
      "violations": [],
      "schema_score": 1.0
    },
    "gate_2_fr_coverage": {
      "passed": true,
      "coverage": 1.0,
      "missing_frs": [],
      "covered_count": 12,
      "total_count": 12
    },
    "gate_3_phase_structure": {
      "passed": true,
      "violations": [],
      "warnings": [
        {
          "rule": "FEATURE_BALANCE",
          "phase": "phase_3",
          "message": "Phase phase_3 under-loaded (2 features)"
        }
      ],
      "structure_score": 0.9
    },
    "gate_4_acceptance_criteria": {
      "passed": true,
      "violations": [],
      "warnings": [],
      "criteria_stats": {
        "total": 28,
        "from_spec": 28,
        "invented": 0
      },
      "criteria_score": 1.0
    }
  },
  "recommendations": [],
  "metadata": {
    "validated_at": "2025-12-17T10:30:00Z",
    "plan_source": "docs/01-planning/specifications/auth-system/PLAN.json",
    "spec_source": "docs/01-planning/specifications/auth-system/SPEC.md",
    "validator_version": "1.0.0"
  }
}
```


### Per-Gate Failure Response Example (FM-003 Fix)

This example shows how per-gate validation prevents aggregate bypass:

```json
{
  "status": "FAIL",
  "quality_score": 0.67,
  "validation_result": {
    "passed": false,
    "aggregate_score": 0.67,
    "failing_gates": [
      {
        "gate": "section_coverage",
        "score": 0.3,
        "minimum": 0.6,
        "gap": 0.3
      }
    ],
    "per_gate_status": {
      "schema_validity": { "score": 1.0, "minimum": 1.0, "passed": true },
      "section_coverage": { "score": 0.3, "minimum": 0.6, "passed": false },
      "step_completeness": { "score": 0.9, "minimum": 0.6, "passed": true },
      "fr_traceability": { "score": 0.8, "minimum": 0.5, "passed": true },
      "effort_estimation": { "score": 0.75, "minimum": 0.4, "passed": true }
    },
    "recommendations": [
      "Increase section_coverage from 0.30 to >= 0.60",
      "Add NFR section coverage"
    ]
  },
  "reason": "Gate section_coverage below minimum threshold (0.3 < 0.6)",
  "note": "Aggregate 0.67 would pass 0.6 threshold but individual gate failure blocks"
}
```

### Failure Response Example

```json
{
  "status": "FAIL",
  "quality_score": 0.62,
  "validation_result": {
    "passed": false,
    "aggregate_score": 0.62,
    "failing_gates": [],
    "per_gate_status": {
      "schema_validity": { "score": 1.0, "minimum": 1.0, "passed": true },
      "section_coverage": { "score": 0.75, "minimum": 0.6, "passed": true },
      "step_completeness": { "score": 0.0, "minimum": 0.6, "passed": false },
      "fr_traceability": { "score": 0.75, "minimum": 0.5, "passed": true },
      "effort_estimation": { "score": 1.0, "minimum": 0.4, "passed": true }
    }
  },
  "gate_results": {
    "gate_1_schema": {
      "passed": true,
      "violations": [],
      "schema_score": 1.0
    },
    "gate_2_fr_coverage": {
      "passed": false,
      "coverage": 0.75,
      "missing_frs": ["FR-009", "FR-010", "FR-011", "FR-012"],
      "covered_count": 12,
      "total_count": 16
    },
    "gate_3_phase_structure": {
      "passed": false,
      "violations": [
        {
          "rule": "MUST_IN_PHASE_1",
          "feature_id": "FR-002",
          "phase": "phase_2",
          "message": "Must-priority feature FR-002 not in Phase 1"
        }
      ],
      "warnings": [],
      "structure_score": 0.0
    },
    "gate_4_acceptance_criteria": {
      "passed": true,
      "violations": [],
      "warnings": [],
      "criteria_stats": {
        "total": 24,
        "from_spec": 24,
        "invented": 0
      },
      "criteria_score": 1.0
    }
  },
  "recommendations": [
    {
      "gate": "fr_coverage",
      "priority": "HIGH",
      "action": "Add features for 4 missing FRs",
      "details": ["FR-009", "FR-010", "FR-011", "FR-012"]
    },
    {
      "gate": "phase_structure",
      "priority": "HIGH",
      "action": "Move Must-priority features to Phase 1",
      "details": ["Must-priority feature FR-002 not in Phase 1"]
    }
  ],
  "metadata": {
    "validated_at": "2025-12-17T10:30:00Z",
    "plan_source": "docs/01-planning/specifications/auth-system/PLAN.json",
    "spec_source": "docs/01-planning/specifications/auth-system/SPEC.md",
    "validator_version": "1.0.0"
  }
}
```

---

## Anti-Patterns

**NEVER DO**:

| Anti-Pattern | Why It's Wrong | Correct Approach |
|--------------|----------------|------------------|
| Skip gates on "simple" plans | All plans need validation | Run all 4 gates always |
| Override FAIL with WARN | Masks quality issues | Respect thresholds strictly |
| Accept partial coverage | Missing FRs = incomplete plan | Require 100% FR coverage |
| Invent acceptance criteria | Criteria must trace to SPEC | Copy from SPEC.md only |
| Ignore gate order | Later gates assume earlier passed | Execute gates sequentially |
| Validate without spec_metadata | Cannot verify FR coverage or criteria | Always require spec_metadata |
| Return partial results on error | Consumers expect complete contract | Return full structure with error details |
| Auto-fix violations | May break intentional design | Report and recommend, don't modify |


### Schema Validation Anti-Patterns

```
# WRONG: Validating only root fields
validate_schema(plan):
  check('project' in plan)
  check('phases' in plan)
  # Missing feature-level and summary validation!

# CORRECT: Validate all levels
validate_schema(plan):
  check_root_fields(plan)
  check_phase_fields(plan.phases)
  check_feature_fields(plan.phases.*.features)
  check_summary_fields(plan.summary)
```

### Coverage Validation Anti-Patterns

```
# WRONG: Counting features instead of FR coverage
coverage = len(plan_features) / expected_features  # Wrong metric!

# CORRECT: Check FR-ID mapping
coverage = len(spec_frs.intersection(plan_fr_ids)) / len(spec_frs)
```

### Criteria Validation Anti-Patterns

```
# WRONG: Accepting any criteria text
FOR feature IN features:
  IF len(feature.acceptance_criteria) > 0:
    PASS  # Not checking source!

# CORRECT: Verify criteria from SPEC
FOR feature IN features:
  FOR criterion IN feature.acceptance_criteria:
    IF NOT exists_in_spec(criterion, feature.id, spec_criteria_map):
      FAIL("Criterion not from SPEC.md")
```

---

## Quick Reference

```
VALIDATION GATES (sequential, all BLOCKING):
  Gate 1: Schema Compliance   -> JSON structure matches template
  Gate 2: FR Coverage         -> Every FR-ID has a feature
  Gate 3: Phase Structure     -> Must in Phase 1, limits enforced
  Gate 4: Acceptance Criteria -> Criteria exist and from SPEC

QUALITY SCORE FORMULA:
  schema(0.25) + coverage(0.30) + structure(0.25) + criteria(0.20)

THRESHOLDS:
  >= 0.85 = PASS (ready for /tasks)
  0.70-0.84 = WARN (review recommended)
  < 0.70 = FAIL (regenerate plan)

PER-GATE MINIMUMS (FM-003 fix - prevents aggregate bypass):
  schema_validity:   1.0  (must be 100% valid)
  section_coverage:  0.6  (at least 60% sections)
  step_completeness: 0.6  (at least 60% steps)
  fr_traceability:   0.5  (at least 50% FRs)
  effort_estimation: 0.4  (can be refined later)

VALIDATION ORDER:
  1. Per-gate minimums (early exit on first failure)
  2. Gate pass/fail boolean checks
  3. Aggregate score threshold

BLOCKING RULES:
  - Missing schema fields = FAIL
  - FR coverage < 100% = FAIL
  - Must features not in Phase 1 = FAIL
  - Features > 8 per phase = FAIL
  - Features with hours outside 0.5-3.0 = FAIL
  - Features without acceptance criteria = FAIL
  - Invented criteria (not from SPEC) = FAIL

WARNING RULES:
  - Phase count > 4 = WARN
  - Features per phase < 3 or > 7 = WARN
  - Criteria may not be measurable = WARN

INPUT CONTRACT:
  {
    plan: PLAN.json object,
    spec_metadata: {
      functional_requirements: FR[],
      acceptance_criteria_source: Map<FR_ID, string[]>
    }
  }

OUTPUT CONTRACT:
  {
    status: PASS|WARN|FAIL,
    quality_score: 0.XX,
    gate_results: { gate_1..4 },
    recommendations: [...]
  }

GATE EXECUTION ORDER:
  1. Schema -> 2. Coverage -> 3. Structure -> 4. Criteria
  (stop on first FAIL)

CROSS-REFERENCES:
  -> generating-plans SKILL.md (validation gate definitions)
  -> plan-generation SKILL.md (plan output contract)
  -> generating-tasks SKILL.md (downstream consumer)
```

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [generating-plans](../generating-plans/SKILL.md) | Source of validation gate algorithms |
| [plan-generation](../plan-generation/SKILL.md) | Produces plans that this skill validates |
| [generating-tasks](../generating-tasks/SKILL.md) | Consumes validated plans |
| [task-validation](../task-validation/SKILL.md) | Parallel validation skill for tasks |

---

## Thinking Frameworks

**Full Catalog**: [Thinking Frameworks README](../../docs/00-core/frameworks/README.md)

**Most Relevant for Plan Validation**:

| Framework | When to Use |
|-----------|-------------|
| [Pre-Mortem](../../docs/00-core/frameworks/strategy.md) | Anticipate validation failures |
| [OODA](../../docs/00-core/frameworks/decision.md) | Iterate through validation gates |
| [Systems Thinking](../../docs/00-core/frameworks/analysis.md) | Understand gate interdependencies |

> **Selection Tip**: gate failures -> Pre-Mortem, iteration -> OODA, dependencies -> Systems

