# Feature Analyzer - Simulation Examples

**Purpose**: Complete walkthrough examples demonstrating the 7-phase methodology for merge, separate, refactor, and failure scenarios.

**Usage**: Reference these examples to understand expected behavior and output structure for different overlap patterns.

---

## Example 1: Merge Recommendation (High Overlap >70%)

### Input Features

**Feature A**: Progressive validation with checkpointing (every 5 agents)
**Feature B**: Checkpoint-based state recovery after failures

### Simulation Process

**Phase 1: Inventory (Responsibility Mapping)**
- Feature A core responsibility: "Create checkpoints every 5 agents for validation progress tracking"
- Feature B core responsibility: "Recover validation state from checkpoints after failures"
- Entities:
  - Feature A: [Checkpoint, ValidationState, ProgressTracker]
  - Feature B: [CheckpointStore, RecoveryHandler, StateLoader]
  - Shared: [Checkpoint, ValidationState] (2/4 shared = 50% entity overlap)

**Phase 2: Overlap Detection**
- Responsibility overlap: 85% (both focused on checkpoint management)
- Requirement overlap: 75% (duplicate checkpoint creation, state persistence)
- Infrastructure overlap: 90% (shared StateManager, CheckpointConfig, RecoveryHandler)
- Overall overlap: (0.85 x 0.40) + (0.75 x 0.30) + (0.90 x 0.30) = 0.34 + 0.225 + 0.27 = **82.5%**

**Phase 3: Conflicts**
- No competing objectives found
- No circular dependencies
- Timeline aligned (both target Phase 1 implementation)

**Phase 4: Synergies**
- High amplification: Checkpointing enables recovery (Feature A -> Feature B pipeline)
- Foundation layer: Feature A provides infrastructure, Feature B builds on it
- Synergy type: Foundational + Application

**Phase 5: Decision**
- Overall overlap: 82.5% > 70% -> **MERGE decision**
- No critical conflicts to override
- Architecture constraints checked:
  - Combined FRs: 45 + 38 = 83 FRs (exceeds <=70 target by 19%) -> CAUTION
  - Mitigation: Phase implementation to manage scope
- Relationship type: Type 1 (Foundational + Application)

**Phase 6: Integration Architecture**
```json
{
  "strategy": "merge",
  "merged_feature": {
    "name": "Checkpoint Management & Recovery",
    "combined_scope": "Progressive validation checkpoints + failure recovery",
    "phased_implementation": [
      "Phase 0: StateManager foundation",
      "Phase 1: Checkpoint creation",
      "Phase 2: Recovery workflows",
      "Phase 3: Integration tests"
    ],
    "unified_success_criteria": [
      ">=98% workflow completion with recovery",
      "<=5min recovery time",
      "<=2% checkpoint overhead"
    ]
  }
}
```

**Phase 7: Architecture Alignment**
- Simplicity First: WARN (83 FRs exceeds target, mitigated by phasing)
- Operational Reliability: PASS (checkpointing + recovery improves reliability)
- Context Offloading: PASS (state compression reduces orchestrator context)
- Overall alignment score: 0.88

### Expected Output

```json
{
  "status": "SUCCESS",
  "recommended_action": {
    "action": "merge",
    "confidence": 0.95,
    "rationale": ">70% overlap across all dimensions. Shared objective: checkpoint-based reliability. Separation would duplicate 90% of infrastructure. Merge into unified 'Checkpoint Management & Recovery' feature.",
    "alternatives_considered": [
      {
        "alternative": "separate",
        "rejected_because": "Would duplicate 90% of infrastructure (StateManager, CheckpointConfig), violating DRY principle"
      },
      {
        "alternative": "refactor",
        "rejected_because": "Overlap too high (82.5%) - features are fundamentally the same concern"
      }
    ]
  }
}
```


---

## Example 2: Separate Recommendation (Low Overlap <30%)

### Input Features

**Feature A**: Context size monitoring with alerts
**Feature B**: Test dataset generation for algorithm validation

### Simulation Process

**Phase 1: Inventory**
- Feature A: "Monitor orchestrator context size and alert on threshold breaches"
- Feature B: "Generate diverse test datasets from git history for algorithm validation"
- Entities:
  - Feature A: [ContextMonitor, SizeTracker, AlertConfig]
  - Feature B: [DatasetGenerator, GitMiner, DiversitySampler]
  - Shared: None (0/6 = 0% entity overlap)

**Phase 2: Overlap Detection**
- Responsibility overlap: 5% (completely different domains: monitoring vs test data)
- Requirement overlap: 0% (no duplicate requirements)
- Infrastructure overlap: 10% (both use config files, that's all)
- Overall overlap: (0.05 x 0.40) + (0.00 x 0.30) + (0.10 x 0.30) = 0.02 + 0.00 + 0.03 = **5%**

**Phase 3: Conflicts**
- No conflicts (orthogonal concerns)

**Phase 4: Synergies**
- No amplification effects
- No foundation layers
- No sequential dependencies
- Synergy type: Independent Modules (Type 4)

**Phase 5: Decision**
- Overall overlap: 5% < 30% -> **SEPARATE decision**
- Relationship type: Type 4 (Independent Modules)
- Architecture constraints: PASS All passed (clear boundaries, no coupling)

**Phase 6: Integration Architecture**
```json
{
  "strategy": "separate",
  "feature_separation": [
    {
      "feature": "Feature A: Context Monitoring",
      "phase": "Phase 1",
      "dependencies": [],
      "integration_tests": ["Context size measurement", "Threshold alerting"]
    },
    {
      "feature": "Feature B: Test Dataset Generator",
      "phase": "Phase 2 (parallel with A)",
      "dependencies": [],
      "integration_tests": ["Dataset generation", "Algorithm validation"]
    }
  ],
  "interface_contracts": "No shared interfaces needed (independent modules)"
}
```

**Phase 7: Architecture Alignment**
- Simplicity First: PASS (clear separation, no coupling)
- Confidence-Based Decisions: PASS (Feature A supports decision audit, Feature B enables validation)
- All goals: PASS
- Overall alignment score: 0.95

### Expected Output

```json
{
  "status": "SUCCESS",
  "recommended_action": {
    "action": "separate",
    "confidence": 0.98,
    "rationale": "<30% overlap across all dimensions. Orthogonal concerns: context monitoring vs test data generation. No amplification effects. Clean separation optimal.",
    "alternatives_considered": [
      {
        "alternative": "merge",
        "rejected_because": "Only 5% overlap - merging would create artificial coupling between unrelated features"
      }
    ]
  }
}
```

---

## Example 3: Refactor Recommendation (Medium Overlap 30-70%)

### Input Features

**Feature A**: Multi-agent checkpointing (every 5 agents, save state)
**Feature B**: Context size monitoring (measure tokens, alert on thresholds)

### Simulation Process

**Phase 1: Inventory**
- Feature A: "Progressive checkpointing for multi-agent workflows"
- Feature B: "Context size monitoring with threshold alerting"
- Entities:
  - Feature A: [CheckpointManager, StateStore, ProgressCounter]
  - Feature B: [ContextMonitor, SizeTracker, AlertConfig]
  - Shared: [StateStore] (1/6 = 17% entity overlap)

**Phase 2: Overlap Detection**
- Responsibility overlap: 25% (both track state, different purposes)
- Requirement overlap: 18% (some shared state persistence requirements)
- Infrastructure overlap: 65% (shared StateManager, ProgressTracker)
- Overall overlap: (0.25 x 0.40) + (0.18 x 0.30) + (0.65 x 0.30) = 0.10 + 0.054 + 0.195 = **34.9%**

**Phase 3: Conflicts**
- No conflicts

**Phase 4: Synergies**
- Complementary layers: Checkpointing for reliability, monitoring for optimization
- Shared foundation: StateManager component used by both
- Synergy type: Type 3 (Complementary Layers)

**Phase 5: Decision**
- Overall overlap: 34.9% (30-70% range) -> **REFACTOR decision**
- Tie-breaker analysis:
  - Infrastructure overlap 65% -> Bias toward refactor (extract shared foundation)
  - Distinct value propositions -> Keep features separate after foundation extraction
- Architecture constraints: PASS All passed

**Phase 6: Integration Architecture**
```json
{
  "strategy": "refactor",
  "shared_foundation": {
    "component": "StateManager",
    "responsibilities": ["State persistence", "Progress tracking", "Recovery coordination"],
    "interface": "state_manager.py with save_state(), load_state(), track_progress() methods",
    "implementation_phase": "Phase 0"
  },
  "feature_separation": [
    {
      "feature": "Feature A: Checkpointing",
      "phase": "Phase 1",
      "dependencies": ["StateManager"],
      "integration_tests": ["Checkpoint creation", "State recovery"]
    },
    {
      "feature": "Feature B: Context Monitoring",
      "phase": "Phase 2",
      "dependencies": ["StateManager"],
      "integration_tests": ["Context measurement", "Threshold alerting"]
    }
  ]
}
```

**Phase 7: Architecture Alignment**
- Simplicity First: PASS (Single shared foundation vs duplicate state management)
- Context Offloading: PASS (StateManager provides compression layer)
- All goals: PASS
- Overall alignment score: 0.90

### Expected Output

```json
{
  "status": "SUCCESS",
  "recommended_action": {
    "action": "refactor",
    "confidence": 0.85,
    "rationale": "30-70% overlap triggers refactor. Shared infrastructure (65%) justifies StateManager extraction. Distinct value propositions (checkpointing vs monitoring) justify keeping features separate after foundation.",
    "alternatives_considered": [
      {
        "alternative": "merge",
        "rejected_because": "Responsibility overlap only 25% - features serve different purposes"
      },
      {
        "alternative": "separate",
        "rejected_because": "Infrastructure overlap 65% - separation would duplicate state management code"
      }
    ]
  }
}
```

---

## Example 4: Failure - Missing Context

### Input Features

**Feature A**: Missing success criteria (no metrics defined)
**Feature B**: Circular dependency on Feature A (B requires A, A requires B)

### Simulation Process

**Phase 1: Inventory**
- Feature A: Core responsibility extracted PASS
- Feature A: Success metrics -> **BLOCKED** (no quantitative criteria found)
- Feature B: Core responsibility extracted PASS
- Feature B: Dependencies -> **CIRCULAR DEPENDENCY DETECTED** (A->B, B->A)

**Phase 2: Overlap Detection**
- **BLOCKED** (cannot calculate overlap without Feature A metrics)

**Phase 3: Conflicts**
- **CRITICAL CONFLICT**: Circular dependency unresolvable without architecture redesign

**Halt Condition Triggered**:
- Missing context prevents analysis continuation
- Confidence <0.70 threshold violated (estimated 0.60 due to missing data)

### Expected Output

```json
{
  "status": "FAILURE",
  "failure_details": {
    "failure_type": "missing_context",
    "reasons": [
      "Feature A missing quantitative success criteria (no baseline or target metrics)",
      "Feature B dependency graph shows circular dependency: B requires A, A requires B",
      "Unclear scope boundaries: both features mention 'state management' but don't define ownership"
    ],
    "recovery_suggestions": [
      {
        "suggestion": "Delegate to technical-pm to enhance Feature A with success metrics",
        "effort_estimate": "30 minutes",
        "confidence": 0.85
      },
      {
        "suggestion": "Delegate to architecture-review to resolve circular dependency with interface contracts",
        "effort_estimate": "1 hour",
        "confidence": 0.9
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
    "next_steps": [
      "Orchestrator should delegate specification enhancement to technical-pm",
      "After enhancement, retry feature-analyzer with same feature_paths"
    ]
  }
}
```

---

## Common Patterns Across Examples

### Decision Matrix Application

1. **Calculate overall overlap**: (Responsibility x 0.40) + (Requirement x 0.30) + (Infrastructure x 0.30)
2. **Apply primary rules**:
   - >70% -> MERGE
   - <30% -> SEPARATE
   - 30-70% -> REFACTOR
3. **Check overrides**: Conflicts or architecture violations can override decision
4. **Apply tie-breakers**: For borderline cases (28-32%, 68-72%)

### Confidence Calibration

- **Start with data completeness**: All 3 dimensions measured = 0.90-1.00 base
- **Adjust for decision clarity**:
  - Clear boundary (>5% margin) = +0.05 to +0.10
  - Borderline (within 2%) = -0.05 to -0.10
- **Adjust for architecture alignment**:
  - Strong (0.90+ score) = +0.05
  - Weak (<0.70 score) = -0.10 to -0.15

### Architecture Constraint Enforcement

Always check 4 constraints in Phase 7:
1. Hooks cannot access agent reasoning
2. Context Offloading Principle (10:1 compression target)
3. No code-based state machines (unless justified)
4. Simplicity First (<=70 FRs, <=3 shared dependencies)


---

## Usage Guidelines

### When to Merge
- Overlap >70% across all dimensions
- Shared core objective
- Separation would duplicate infrastructure
- Combined FRs <=70 (or phased to manage scope)

### When to Separate
- Overlap <30%
- Orthogonal concerns (independent value)
- No amplification effects
- Clear boundaries possible

### When to Refactor
- Overlap 30-70%
- Shared infrastructure (>50%) but distinct value propositions
- Complementary layers or foundation + application pattern
- Extract shared components, keep features separate

### When to FAIL
- Missing context blocks analysis (no metrics, circular dependencies)
- Confidence <0.70
- File access failures
- Validation errors

---

**See Also**:
- `../docs/response-examples.md` for complete JSON response structures
- `../docs/verification-protocol.md` for orchestrator validation commands
- `../feature-analyzer.md` for 7-phase methodology details
