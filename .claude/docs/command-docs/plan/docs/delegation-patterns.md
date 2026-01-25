# Delegation Patterns for /plan Command

**CRITICAL**: Use these EXACT Task() call patterns. Phase 4 runs PARALLEL BY FILE.

---

## Framework Directives

**CRITICAL**: Each delegation prompt MUST include the appropriate thinking framework directive. This ensures agents apply structured reasoning rather than ad-hoc processing.

| Phase | Agent(s) | Framework | Directive Prefix |
|-------|----------|-----------|------------------|
| 2 | planning, feature-analyzer | ReACT | "USE REACT FRAMEWORK: THINK -> ACT -> OBSERVE -> REFINE" |
| 4 | planning, architecture | CAGEERF | "USE CAGEERF FRAMEWORK: Context -> Analysis -> Goals -> Execution -> Evaluation -> Refinement" |
| 6 | architectureer | Disney Creative Strategy | "USE DISNEY CREATIVE STRATEGY: DREAMER -> REALIST -> CRITIC" |

**Why Frameworks Matter**:
- Without framework directive: Agent may use single-pass, superficial analysis
- With framework directive: Agent applies structured, iterative reasoning
- Result: Higher quality outputs, fewer missed issues, better confidence scores

---

## Phase-to-Agent Mapping

| Phase | Agent | Operation | Duration |
|-------|-------|-----------|----------|
| 2a | planning | spec_validation | ~1-2 min |
| 2b | feature-analyzer | component_breakdown | ~1-2 min |
| 4a | planning | business_context_enhancement | ~1-2 min/file |
| 4b | architecture | technical_content_population | ~1-2 min/file |
| 6 | architectureer | plan_validation | ~3-5 min |

---

## Phase 2: SPEC Validation & Component Analysis (PARALLEL)

**CRITICAL**: Phase 2 uses TWO agents in PARALLEL for faster execution:
- **planning**: Validates SPEC.md quality and completeness
- **feature-analyzer**: Determines component breakdown from SPEC structure

### planning (Parallel with feature-analyzer)

```
Task(
  subagent_type="planning",
  prompt="Validate SPEC.md at {spec_file_path}:

    Process:
    1. Check FR-ID format (FR-XXX pattern)
    2. Verify required sections exist:
       - Business Goals
       - User Scenarios
       - Functional Requirements
       - Non-Functional Requirements
       - Constraints
    3. Assess completeness and consistency
    4. Score overall quality

    Return: {
      validation_status: PASS|WARN|FAIL,
      issues: [string],
      completeness_score: number (0-100),
      missing_sections: [string]
    }"
)
```

### feature-analyzer (Parallel with planning)

```
Task(
  subagent_type="feature-analyzer",
  prompt="Analyze SPEC.md at {spec_file_path} for component breakdown:

    Process:
    1. Identify logical components from section structure
    2. Group related requirements (FR-IDs) by domain
    3. Determine component boundaries for independent development
    4. Map integration points between components

    Return: {
      components: [{
        name: string,
        description: string,
        fr_ids: [FR-ID list],
        dependencies: [component names]
      }],
      rationale: string
    }"
)
```

**Expected Output (Combined):**

```json
{
  "validation_report": {
    "validation_status": "PASS",
    "completeness_score": 92,
    "issues": []
  },
  "component_breakdown": [
    {
      "name": "core-authentication",
      "description": "Core auth logic and token management",
      "fr_ids": ["FR-001", "FR-002", "FR-003"],
      "dependencies": []
    },
    {
      "name": "oauth-integration",
      "description": "OAuth2 provider integration",
      "fr_ids": ["FR-004", "FR-005"],
      "dependencies": ["core-authentication"]
    }
  ],
  "rationale": "Separated by authentication concern for independent development"
}
```

---

## Phase 4: Enhancement Pipelines (PARALLEL BY FILE)

**CRITICAL EXECUTION PATTERN:**

```python
# Launch ALL pipelines simultaneously (each pipeline is sequential internally)
for plan_file in plan_files:
    # Each pipeline runs in parallel with others
    Pipeline(
        Task(planning, plan_file),  # Step 1
        Task(architecture, plan_file)  # Step 2 (waits for Step 1)
    )
```

### planning (Per File)

```
Task(
  subagent_type="planning",
  prompt="Enhance plan file with business context:

    Input:
    - plan_file_path: {plan_file_path}
    - spec_file_path: {spec_file_path}
    - plan_metadata: {
        name: '{component_name}',
        requirements: {fr_id_list},
        focus_areas: {focus_areas}
      }
    - strategic_requirements: {
        maturity_stage: 'MVP',
        complexity_threshold: 0.3,
        pain_point_targets: {from_spec_analysis}
      }

    Process:
    1. Read SPEC.md for business context
    2. Map assigned requirements to plan sections
    3. Populate business sections (goals, success criteria, value proposition)
    4. Preserve technical sections as placeholders for architecture

    Return: {
      status: SUCCESS|FAILURE,
      sections_populated: [list],
      requirements_mapped: count,
      placeholders_remaining: count
    }"
)
```

### architecture (Per File, After planning)

```
Task(
  subagent_type="architecture",
  prompt="Populate technical sections in plan file:

    Input:
    - plan_file_path: {plan_file_path}
    - spec_file_path: {spec_file_path}
    - component_context: {
        name: '{component_name}',
        requirements: {fr_id_list},
        related_components: {other_component_names}
      }

    Process:
    1. Read existing plan (with business sections from planning)
    2. Research technical implementation approaches via Context7
    3. Populate Implementation Plan with concrete phases (≥3)
    4. Add specific tasks per phase (≥2 per phase)
    5. Include actual file paths, not placeholders
    6. Document integration points with other components

    Return: {
      status: SUCCESS|FAILURE,
      phases_created: count,
      tasks_per_phase: [counts],
      file_paths_added: count,
      placeholders_remaining: count
    }"
)
```

---

## Phase 6: Architecture Review

```
Task(
  subagent_type="architectureer",
  prompt="Validate all plan files for production readiness:

    Input:
    - plans_to_review: [
        {plan_file_path: '{path}', validation_scope: 'comprehensive'}
      ]
    - validation_requirements: {
        check_technical_completeness: true,
        validate_integration_points: true,
        assess_production_readiness: true,
        verify_architecture_decisions: true
      }
    - quality_requirements: {
        architecture_score_minimum: 3.5,
        integration_analysis_required: true,
        security_review_required: true
      }

    Process:
    1. Review each plan for technical completeness
    2. Validate cross-plan integration points
    3. Assess production readiness (scalability, security, observability)
    4. Score architecture quality (1-5 scale)
    5. Generate recommendations for improvements

    Return: {
      overall_status: PASS|WARN|FAIL,
      architecture_score: number,
      per_plan_results: [{
        plan_file: string,
        score: number,
        issues: [],
        recommendations: []
      }],
      integration_analysis: {
        dependencies_validated: boolean,
        missing_integrations: [],
        circular_dependencies: []
      },
      production_readiness: {
        security: PASS|WARN|FAIL,
        scalability: PASS|WARN|FAIL,
        observability: PASS|WARN|FAIL
      }
    }"
)
```

---

## Why Parallel-by-File Strategy?

| Benefit | Explanation |
|---------|-------------|
| **No file conflicts** | Single agent modifies each file at any time |
| **3-5x faster** | 3 files × 2 min/file = 2 min parallel vs 6 min sequential |
| **Deterministic** | Pipeline order per file is always planning → arch-enhancer |
| **Easy recovery** | If one pipeline fails, others complete; retry failed file only |
