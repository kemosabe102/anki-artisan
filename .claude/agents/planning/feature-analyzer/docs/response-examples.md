# Feature Analyzer - Response Structure Examples

**Purpose**: Complete SUCCESS and FAILURE JSON response structures with full nested JSON for all scenarios.

**Usage**: Reference this guide when constructing feature-analyzer outputs. All responses must validate against `../schemas/feature-analyzer.schema.json`.

---

## SUCCESS Response Structure

### Complete Example (Refactor Recommendation)

```json
{
  "status": "SUCCESS",
  "agent": "feature-analyzer",
  "task_id": "analyze_features_012_013",
  "operation_type": "analyze_features",
  "summary": "Analyzed 2 features: 42.76% overlap detected, recommend REFACTOR to extract shared checkpoint foundation, keep distinct value propositions separate.",
  "confidence": 0.85,
  "execution_timestamp": "2025-10-12T14:30:00Z",
  "agent_specific_output": {
    "comparison_matrix": {
      "features": [
        {
          "name": "Feature A",
          "core_responsibility": "Progressive validation with checkpointing",
          "entities": ["Checkpoint", "ValidationState", "ProgressTracker"],
          "workflows": ["checkpoint_creation", "state_recovery", "validation_progression"],
          "success_metrics": [">=98% workflow completion", "<=5min recovery time"]
        },
        {
          "name": "Feature B",
          "core_responsibility": "Context monitoring with size alerts",
          "entities": ["ContextMonitor", "SizeTracker", "AlertConfig"],
          "workflows": ["context_measurement", "threshold_alerting", "size_optimization"],
          "success_metrics": ["<=10K token orchestrator context", ">=95% alert accuracy"]
        }
      ],
      "overlap_analysis": {
        "responsibility_overlap_pct": 25,
        "requirement_overlap_pct": 18,
        "infrastructure_overlap_pct": 65,
        "conflict": false,
        "synergy": true,
        "synergy_type": "complementary_layers"
      }
    },
    "separation_report": {
      "overlapping_responsibilities": [
        {
          "area": "State persistence",
          "solution": "Extract shared StateManager component, both features depend on it"
        },
        {
          "area": "Progress tracking",
          "solution": "Feature A owns checkpoint creation, Feature B owns size monitoring (clear boundaries)"
        }
      ],
      "clear_boundaries": [
        {
          "owner": "Feature A",
          "responsibility": "Validation workflow checkpointing and recovery"
        },
        {
          "owner": "Feature B",
          "responsibility": "Context size monitoring and optimization alerts"
        }
      ],
      "recommended_structure": "REFACTOR: Extract shared StateManager foundation (Phase 0), implement Feature A (Phase 1), implement Feature B (Phase 2) with shared foundation"
    },
    "integration_architecture": {
      "strategy": "refactor",
      "shared_foundation": {
        "component": "StateManager",
        "responsibilities": ["State persistence", "Progress tracking", "Recovery coordination"],
        "interface": "state_manager.py with save_state(), load_state(), track_progress() methods",
        "implementation_phase": "Phase 0 (foundation)"
      },
      "feature_separation": [
        {
          "feature": "Feature A",
          "phase": "Phase 1",
          "dependencies": ["StateManager"],
          "integration_tests": ["Checkpoint creation", "State recovery", "Validation progression"]
        },
        {
          "feature": "Feature B",
          "phase": "Phase 2",
          "dependencies": ["StateManager"],
          "integration_tests": ["Context monitoring", "Threshold alerting", "Size optimization"]
        }
      ],
      "rationale": "30-70% overlap indicates refactor: extract shared infrastructure (StateManager), keep distinct value propositions (checkpointing vs monitoring) separate for clarity and maintainability."
    },
    "alignment_assessment": {
      "goals": [
        {
          "goal": "Simplicity First",
          "status": "PASS",
          "rationale": "Refactor creates single shared foundation vs duplicate state management, reduces complexity"
        },
        {
          "goal": "Context Offloading",
          "status": "PASS",
          "rationale": "Feature B directly addresses context optimization goal, Feature A supports reliability"
        },
        {
          "goal": "Operational Reliability",
          "status": "PASS",
          "rationale": "Feature A checkpointing improves reliability, Feature B prevents context blowup failures"
        },
        {
          "goal": "Confidence-Based Decisions",
          "status": "WARN",
          "rationale": "Features don't directly address DCS framework, but checkpointing enables confidence calibration via audit trails",
          "mitigation": "Add confidence logging to checkpoint metadata"
        },
        {
          "goal": "Continuous Learning",
          "status": "PASS",
          "rationale": "Checkpoint audit trails enable decision learning, context metrics enable optimization learning"
        }
      ],
      "risks": [
        {
          "risk": "StateManager becomes coupling point if not well-abstracted",
          "severity": "medium",
          "mitigation": "Define clear interface contracts, limit responsibilities to persistence only"
        }
      ],
      "overall_alignment_score": 0.9
    },
    "recommended_action": {
      "action": "refactor",
      "confidence": 0.85,
      "rationale": "30-70% overlap triggers refactor decision. Shared infrastructure (65% overlap) justifies StateManager extraction. Distinct value propositions (checkpointing vs monitoring) justify keeping features separate after foundation. Architecture alignment strong (0.90) with minor confidence-based decision enhancement needed.",
      "alternatives_considered": [
        {
          "alternative": "merge",
          "rejected_because": "Responsibility overlap only 25%, merging would create bloated single-purpose feature"
        },
        {
          "alternative": "separate",
          "rejected_because": "Infrastructure overlap 65%, separation would duplicate state management code"
        }
      ]
    }
  }
}
```

---

## FAILURE Response Structure

### Complete Example (Missing Context)

```json
{
  "status": "FAILURE",
  "agent": "feature-analyzer",
  "task_id": "analyze_features_012_013",
  "operation_type": "analyze_features",
  "summary": "Analysis failed: Feature A specification missing success metrics, Feature B has circular dependency on Feature A.",
  "confidence": 0.7,
  "execution_timestamp": "2025-10-12T14:30:00Z",
  "failure_details": {
    "failure_type": "missing_context",
    "reasons": [
      "Feature A missing quantitative success criteria (no baseline or target metrics)",
      "Feature B dependency graph shows circular dependency: B requires A, A requires B (checkpointing vs monitoring integration)",
      "Unclear scope boundaries: both features mention 'state management' but don't define ownership"
    ],
    "recovery_suggestions": [
      {
        "suggestion": "Delegate to technical-pm agent to enhance Feature A specification with success metrics",
        "effort_estimate": "30 minutes",
        "confidence": 0.85
      },
      {
        "suggestion": "Delegate to architecture-review agent to resolve circular dependency and define clear interface contracts",
        "effort_estimate": "1 hour",
        "confidence": 0.9
      },
      {
        "suggestion": "Request orchestrator to coordinate specification enhancement before retrying analysis",
        "effort_estimate": "1.5 hours total",
        "confidence": 0.95
      }
    ],
    "partial_results": {
      "comparison_matrix": {
        "features_loaded": 2,
        "responsibility_mapping": "completed",
        "overlap_detection": "blocked (missing metrics)",
        "integration_decision": "not_started"
      }
    },
    "research_attempted": [
      "Read Feature A specification from docs/01-planning/specifications/012-feature-a/spec.md",
      "Read Feature B specification from docs/01-planning/specifications/013-feature-b/spec.md",
      "Grep for 'success criteria' across both specifications (found in B only)",
      "Grep for 'dependencies' across both specifications (found circular reference)"
    ],
    "next_steps": [
      "Orchestrator should delegate specification enhancement to technical-pm",
      "After enhancement, retry feature-analyzer with same feature_paths",
      "If circular dependency persists, escalate to architecture-review for design consultation"
    ]
  }
}
```

---

## Response Components

### Comparison Matrix

Always includes:
- **features**: Array of feature objects with core_responsibility, entities, workflows, success_metrics
- **overlap_analysis**: Percentages (0-100) for responsibility, requirement, infrastructure overlap + conflict/synergy flags

### Separation Report

Always includes:
- **overlapping_responsibilities**: Array of overlap areas with solutions
- **clear_boundaries**: Array of owner-responsibility pairs
- **recommended_structure**: Single-sentence integration recommendation

### Integration Architecture

**For MERGE**:
- `strategy: "merge"`
- `merged_feature`: { name, combined_scope, phased_implementation, unified_success_criteria }

**For SEPARATE**:
- `strategy: "separate"`
- `feature_separation`: Array of features with phase, dependencies, integration_tests
- `interface_contracts`: Description of shared interfaces (or "No shared interfaces needed")

**For REFACTOR**:
- `strategy: "refactor"`
- `shared_foundation`: { component, responsibilities, interface, implementation_phase }
- `feature_separation`: Array of features with phase, dependencies, integration_tests

### Alignment Assessment

Always includes:
- **goals**: Array of 5 goal objects (Simplicity First, Confidence-Based Decisions, Context Offloading, Operational Reliability, Continuous Learning)
  - Each goal: { goal, status (PASS/WARN/FAIL), rationale, mitigation (if WARN/FAIL) }
- **risks**: Array of risk objects with { risk, severity, mitigation }
- **overall_alignment_score**: 0.0-1.0

### Recommended Action

Always includes:
- **action**: "merge" | "separate" | "refactor"
- **confidence**: 0.0-1.0
- **rationale**: Multi-sentence explanation with overlap breakdown, decision factors, architecture alignment
- **alternatives_considered**: Array of { alternative, rejected_because }

---

## Usage Guidelines

### When to Use SUCCESS

- All 7 phases completed successfully
- Overlap percentages calculated for all 3 dimensions (responsibility, requirement, infrastructure)
- Decision matrix applied with rationale
- Architecture alignment validated against all 5 goals
- Confidence >=0.70

### When to Use FAILURE

- Missing context blocks analysis (no metrics, circular dependencies, access errors)
- Overlap calculation impossible (insufficient data)
- Confidence <0.70 (insufficient data quality)
- File access failures prevent specification loading

### Confidence Bands

- **0.90-1.00**: High certainty, proceed with implementation
- **0.80-0.89**: Good certainty, proceed with minor validation
- **0.70-0.79**: Moderate certainty, proceed with caution and enhanced validation
- **<0.70**: Insufficient data, recommendation not actionable without enhancement -> FAILURE mode

---

**See Also**:
- `../examples/simulation-examples.md` for complete walkthrough examples
- `./verification-protocol.md` for orchestrator validation commands
- `../feature-analyzer.md` for 7-phase methodology
