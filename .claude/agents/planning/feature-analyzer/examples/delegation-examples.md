# Feature Analyzer Delegation Examples

## Basic Invocation

```markdown
Task(feature-analyzer,
  "Compare Feature A and Feature B specifications.
   Path A: docs/01-planning/specifications/001-feature-a/SPEC.md
   Path B: docs/01-planning/specifications/002-feature-b/SPEC.md
   Determine if they should merge, separate, or refactor shared components.")
```

## Quick Overlap Check

```markdown
Task(feature-analyzer,
  "Quick overlap analysis for checkpoint-management and phase-tracking specs.
   comparison_scope: quick
   Focus on responsibility overlap only.")
```

## Multi-Feature Comparison

```markdown
Task(feature-analyzer,
  "Analyze overlap between 3 features:
   - docs/01-planning/specifications/003-state-management/SPEC.md
   - docs/01-planning/specifications/004-checkpoint-system/SPEC.md
   - docs/01-planning/specifications/005-recovery-flow/SPEC.md
   Identify foundation layers and recommend architecture.")
```

## Expected Outputs

### SUCCESS Response Contains
- `comparison_matrix`: Overlap %, conflict/synergy indicators per feature pair
- `separation_report`: Responsibility boundaries, ownership recommendations
- `integration_architecture`: Merge strategy OR separation contracts
- `alignment_assessment`: Goal-by-goal validation with risks
- `recommended_action`: "merge" | "separate" | "refactor" with confidence

### FAILURE Response Contains
- `failure_type`: missing_context | access_error | validation_failure | circular_dependency
- `reasons`: Specific blocking issues
- `recovery_suggestions`: Agent delegations with effort estimates
- `partial_results`: Work completed before failure
- `next_steps`: Actionable recommendations

## Orchestrator Processing

1. Receive feature-analyzer output
2. If SUCCESS with confidence ≥0.80: Proceed to implementation planning
3. If SUCCESS with confidence 0.70-0.79: Add technical-pm validation gate
4. If FAILURE: Delegate to suggested agents (technical-pm, architecture-review)
