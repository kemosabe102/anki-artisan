# Phase 2: GENERATE - Stage-Aware Roadmap

**OODA Phase**: ORIENT
**Operation**: Generate
**Purpose**: Create or update ROADMAP.md with stage-appropriate constraints

---

## Overview

The Generate operation creates a stage-aware roadmap that respects the current stage's quality thresholds, defers inappropriate features, and sets stage transition milestones.

**Input**: 
- Current stage (from Assess operation or user specification)
- Project spec path (PROJECT-SPEC.md or equivalent)

**Output**: Updated ROADMAP.md at `docs/00-project/roadmaps/`

---

## Prerequisites

Before running Generate:
- [ ] Current stage known (via Assess or user input)
- [ ] PROJECT-SPEC.md exists or project requirements documented
- [ ] User has confirmed stage (if from Assess)

---

## Workflow Steps

### Step 2.1: Load Stage Definition

**Action**: Read stage constraints from stage definition file

**Source**: `stages/{current_stage}-stage.md`

**Extract**:
- Quality thresholds (minimum scores)
- Risk tolerance level
- Stage-specific focus areas
- Anti-patterns to avoid
- Features to defer

```python
stage_constraints = {
    "quality_minimums": {...},
    "risk_tolerance": "...",
    "do_at_stage": [...],
    "defer_to_later": [...],
    "anti_patterns": [...]
}
```

---

### Step 2.2: Load Project Requirements

**Delegate to**: `researcher-codebase`
**Execution**: Parallel

**Gather**:
- PROJECT-SPEC.md or equivalent
- Existing ROADMAP.md (if any)
- Feature backlog or requirements docs

**Output**:
```json
{
    "project_spec_path": "...",
    "existing_roadmap_path": "..." or null,
    "features_documented": [...],
    "project_context": {...}
}
```

---

### Step 2.3: Filter Features by Stage

**Logic** (skill performs):

For each feature in project spec:
```python
def is_stage_appropriate(feature, current_stage):
    # Check if feature complexity matches stage
    if feature.complexity > stage_max_complexity[current_stage]:
        return False, "Defer: complexity exceeds stage"
    
    # Check if feature type is in anti-patterns
    if feature.type in stage_anti_patterns[current_stage]:
        return False, f"Defer: {feature.type} is anti-pattern for {current_stage}"
    
    # Check if dependencies are met
    if not all(dep.complete for dep in feature.dependencies):
        return False, "Defer: dependencies not met"
    
    return True, "Include in roadmap"
```

**Stage Complexity Limits**:

| Stage | Max Complexity | Feature Types to Defer |
|-------|----------------|------------------------|
| MVP | Low-Medium | Microservices, multi-region, complex auth |
| Alpha | Medium | Performance optimization, chaos engineering |
| Beta | Medium-High | Multi-region, advanced compliance |
| GA | High | None - all appropriate |

---

### Step 2.4: Apply ICE Scoring

> **Base Thresholds**: `.claude/docs/00-core/orchestrator-thresholds.md#ice-score-thresholds`

**Logic** (skill performs or delegates to planning):

ICE scoring adjusted for stage context:
- **Impact**: 1-10 (business value)
- **Confidence**: 1-10 (adjusted by stage - MVP has lower confidence ceiling)
- **Ease**: 1-10 (adjusted by stage complexity limits)

```python
def stage_adjusted_ice(feature, stage):
    # MVP: conservative confidence, favor easy wins
    if stage == "MVP":
        confidence = min(feature.confidence, 7)  # Cap confidence
        ease_weight = 1.5  # Favor easy features
    # GA: full confidence, balanced scoring
    elif stage == "GA":
        confidence = feature.confidence
        ease_weight = 1.0
    
    return feature.impact * confidence * (feature.ease * ease_weight)
```

---

### Step 2.5: Generate Roadmap

**Delegate to**: `planning`
**Execution**: Sequential

**Prompt includes**:
- Current stage and constraints
- Filtered feature list with ICE scores
- Stage exit criteria as phase success gates
- Deferred features with rationale

**Roadmap Structure**:
```markdown
# Product Roadmap: {project_name}

## Current Stage: {stage}

### Phase 1: {stage} Core
**Goal**: {stage_focus_from_definition}
**Success Criteria**: {stage_exit_criteria}

#### Features (ICE-prioritized)
- [ ] Feature 1 (ICE: XXX)
- [ ] Feature 2 (ICE: XXX)
...

### Stage Transition Milestone
**From**: {current_stage}
**To**: {next_stage}
**Criteria**: {exit_criteria_checklist}

### Deferred Features (for {next_stage}+)
- Feature X: {deferral_reason}
- Feature Y: {deferral_reason}
```

---

### Step 2.6: Validate Roadmap Scope

**Checks** (skill performs):

- [ ] Features per phase <= 6 (avoid overcommitment)
- [ ] All features pass stage-appropriateness filter
- [ ] ICE scores calculated with stage context
- [ ] Stage exit criteria included as milestone
- [ ] Deferred features documented with reasons
- [ ] No anti-patterns in roadmap

---

### Step 2.7: Save and Confirm

**Action**: Write roadmap to `docs/00-project/roadmaps/`

**Naming**: `ROADMAP-{project}.md` or update existing `ROADMAP.md`

**User confirmation**:
```
Roadmap generated:
- Stage: {stage}
- Features included: {count}
- Features deferred: {deferred_count}
- Output: {file_path}

Review the roadmap. Ready to proceed?
```

---

## Quick Checklist

- [ ] Stage definition loaded
- [ ] Project requirements gathered
- [ ] Features filtered by stage
- [ ] ICE scoring applied
- [ ] Roadmap generated via planning
- [ ] Scope validated
- [ ] User confirmed output

---

## Exit Criteria

- ROADMAP.md created/updated with stage context
- All features are stage-appropriate
- Stage exit criteria documented as milestone
- Deferred features listed with rationale

---

## Error Handling

| Error | Recovery |
|-------|----------|
| No project spec | Ask user for requirements source |
| Existing roadmap conflict | Backup existing, generate fresh or merge |
| All features deferred | Alert user - may need to revisit stage assessment |
| planning fails | Retry with simplified prompt |

---

## Next Phase

After Generate completes, user can:
- **Advance**: Plan transition to next stage -> [phase-3-advance.md](phase-3-advance.md)
- **Re-assess**: Update stage assessment -> [phase-1-assess.md](phase-1-assess.md)
