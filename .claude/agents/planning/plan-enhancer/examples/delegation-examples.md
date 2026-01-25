# Plan Enhancer Delegation Examples

How the orchestrator invokes plan-enhancer for various scenarios.

## Basic Enhancement

```markdown
Task(plan-enhancer,
  "Enhance docs/01-planning/specifications/feature-x/PLAN.md with business context 
   from docs/01-planning/specifications/feature-x/SPEC.md.
   
   Plan metadata:
   - name: DataValidationService
   - requirements: [FR-001, FR-002, FR-003]
   - focus_areas: [data quality, performance]
   
   Populate all business sections. Leave technical sections for architecture-enhancer.")
```

## Requirements Mapping Focus

```markdown
Task(plan-enhancer,
  "Map functional requirements to business value in PLAN.md.
   
   Context:
   - plan_file_path: docs/01-planning/specifications/screening/PLAN.md
   - spec_file_path: docs/01-planning/specifications/screening/SPEC.md
   
   Focus on FR-ID traceability. Each component should map to specific
   functional requirements with clear business value statements.")
```

## Success Metrics Focus

```markdown
Task(plan-enhancer,
  "Add success metrics and KPIs to PLAN.md business sections.
   
   Extract from SPEC.md:
   - Measurable success criteria
   - Business metrics (cost savings, efficiency gains)
   - User satisfaction targets
   
   Ensure all metrics are specific and measurable, not generic placeholders.")
```

## With Code Reuse Analysis

```markdown
Task(plan-enhancer,
  "Enhance PLAN.md with business context including reuse opportunities.
   
   Steps:
   1. Read COMPONENT_ALMANAC.md first
   2. Identify components that can be reused/extended
   3. Include reuse benefits in value propositions
   4. Flag replacement scenarios for cleanup tasks
   
   Plan: docs/01-planning/specifications/new-feature/PLAN.md
   SPEC: docs/01-planning/specifications/new-feature/SPEC.md")
```

## Expected Output Structure

```json
{
  "status": "SUCCESS",
  "agent": "plan-enhancer",
  "confidence": 0.95,
  "agent_specific_output": {
    "enhanced_sections": [
      {
        "section_name": "Business Context & Strategic Alignment",
        "placeholders_replaced": 8,
        "content_source": "SPEC.md",
        "enhancement_type": "business_context"
      }
    ],
    "business_context_added": {
      "business_goals": ["Reduce screening time by 60%"],
      "user_value_propositions": ["Self-service eliminates analyst bottleneck"],
      "success_metrics": ["Processing time <2s (P95)"]
    },
    "requirements_traceability": {
      "functional_requirements_mapped": [
        {
          "fr_id": "FR-001",
          "description": "Validate OHLCV data integrity",
          "business_value": "Prevents costly trading errors"
        }
      ]
    },
    "completion_validation": {
      "total_placeholders_identified": 25,
      "placeholders_replaced": 25,
      "remaining_business_placeholders": 0,
      "validation_passed": true
    }
  }
}
```

## Failure Scenario

```json
{
  "status": "FAILURE",
  "agent": "plan-enhancer",
  "confidence": 0.85,
  "failure_details": {
    "failure_type": "spec_file_not_found",
    "reasons": ["SPEC.md does not exist at specified path"],
    "recovery_suggestions": [
      {
        "approach": "Create SPEC.md first using /spec command",
        "rationale": "Business context requires specification as source of truth",
        "estimated_effort": "medium"
      }
    ]
  }
}
```

## Orchestrator Workflow Integration

### Typical Sequence
1. **/spec command** creates SPEC.md from requirements
2. **spec-reviewer** validates SPEC.md quality
3. **plan-enhancer** populates business sections in PLAN.md
4. **architecture-enhancer** populates technical sections in PLAN.md
5. **architecture-review** validates complete PLAN.md

### Parallel Opportunity
plan-enhancer and architecture-enhancer can run in parallel on the same PLAN.md
since they modify different sections (business vs technical).
