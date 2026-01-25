# Plan Command Workflow Phases

Detailed documentation for each phase of the `/plan` command workflow.

---

## Phase 1: Input Validation

**Actor**: Orchestrator  
**Duration**: ~30 seconds

### Process

1. Parse command arguments:
   - `spec_path`: Direct path to SPEC.md file
   - `mode`: default | quick | review
   - `output_dir`: Target for generated plans (optional override)

2. Validation Steps:
   - Verify SPEC.md exists and is readable
   - For review mode: Verify existing plan files exist in plans/ directory
   - Validate SPEC.md structure and completeness
   - Check for required FR-IDs and business context

### Expected Input

```bash
/plan docs/01-planning/specifications/XXX-auth-system/SPEC.md
/plan docs/01-planning/specifications/XXX-auth-system/SPEC.md --mode=review
/plan docs/01-planning/specifications/XXX-auth-system/SPEC.md --output-dir=custom/path/
```

### Output

- `validated_spec_path`: Confirmed SPEC.md location
- `mode`: Determined workflow mode
- `output_directory`: Target for plan files

### Thinking Framework: Cynefin

Before proceeding, classify the SPEC complexity:
- **SIMPLE**: SPEC is well-formed, patterns exist - Proceed directly
- **COMPLICATED**: SPEC has gaps but structure is clear - May need enhanced context
- **COMPLEX**: SPEC is ambiguous, multiple interpretations - Research first with researcher-lead
- **CHAOTIC**: SPEC is broken/incomplete - Suggest /spec first

Classification determines whether to proceed or gather more context.

---


## Phase 2: SPEC Validation & Component Analysis

**Actors**: planning + feature-analyzer (PARALLEL)  
**Duration**: ~2-3 minutes

### Purpose

Validate SPEC.md quality and determine optimal plan breakdown. Two agents work in parallel:
- **planning**: Validates SPEC.md structure, FR-ID format, required sections, completeness
- **feature-analyzer**: Identifies logical components and maps requirements to components

### SPEC.md Validation Checklist (planning)

| Check | Requirement |
|-------|-------------|
| File exists | Path is valid and readable |
| Business Goals | Contains "## Business Goals" or "## 1. Business" section |
| Functional Requirements | Contains FR-XXX IDs (e.g., FR-001, FR-002) |
| Non-Functional Requirements | Contains "## Non-Functional Requirements" or "## NFRs" |
| Minimum content | File size > 500 characters (not empty/stub) |

### Process

**planning** (parallel):
1. Validate SPEC.md structure against checklist
2. Check FR-ID format consistency (FR-XXX pattern)
3. Verify required sections exist
4. Score completeness (0-100)

**feature-analyzer** (parallel):
1. Analyze SPEC.md structure for logical domains
2. Identify distinct components/domains
3. Map FR-IDs to components
4. Generate component breakdown with rationale

### Expected Output

```json
{
  "validation_report": {
    "validation_status": "PASS",
    "completeness_score": 92,
    "issues": [],
    "missing_sections": []
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

### Thinking Framework: ReACT

Both agents apply iterative reasoning:

**ReACT Loop**:
1. **THINK**: Form hypothesis about SPEC quality / component boundaries
2. **ACT**: Execute validation checks / analyze SPEC structure
3. **OBSERVE**: Collect validation results / identify component patterns
4. **REFINE**: Update understanding, iterate until confidence >=0.85

This ensures systematic analysis rather than single-pass evaluation.

---

## Phase 3: File Creation

**Actor**: Orchestrator  
**Duration**: ~1 minute

### Purpose

Create individual plan files from template based on feature-analyzer output.

### Process

For each component from Phase 2:


```bash
uv run python scripts/planning/create-plan-from-template.py "[output-directory]" "[component-name]-PLAN"
```

### Verification Checkpoint

Confirm all expected plan files exist before proceeding:
- Check file count matches component count
- Verify files are non-empty
- List created files for user visibility

---

## Phase 4: Enhancement Pipelines (PARALLEL BY FILE)

**Actors**: planning, architecture  
**Duration**: ~3-5 minutes (parallel execution)

### Critical Execution Strategy

**PARALLEL BY FILE, SEQUENTIAL PER FILE**

```text
Pipeline 1: planning(core-PLAN.md) → architecture(core-PLAN.md)
Pipeline 2: planning(oauth-PLAN.md) → architecture(oauth-PLAN.md)
Pipeline 3: planning(api-PLAN.md) → architecture(api-PLAN.md)
[All pipelines run simultaneously]
```

### Why This Strategy?

| Approach | Risk | Speed |
|----------|------|-------|
| Sequential all | None | SLOW (6+ min) |
| Parallel all agents | FILE CONFLICTS | FAILS |
| **Parallel by file** | None | FAST (2-3 min) |

### planning (First in Pipeline)

Populates BUSINESS sections:
- Requirements traceability (FR-ID mapping)
- Success criteria and user value propositions
- Business pain point alignment
- Preserves technical sections as placeholders


### architecture (Second in Pipeline)

Populates TECHNICAL sections:
- Implementation plans with concrete phases
- Pydantic models and data structures
- Testing strategies
- Integration points with other components

### Verification After Phase 4

1. All plan files have both business AND technical sections populated
2. Zero placeholder sections remaining (except intentional `[NEEDS VERIFICATION]`)
3. Cross-plan dependencies documented

### Thinking Framework: CAGEERF

Both enhancers apply comprehensive enhancement:

**CAGEERF Stages**:
- **C**ontext: Read SPEC, existing plan, understand domain
- **A**nalysis: Identify gaps between current state and targets
- **G**oals: Define success criteria (business alignment, NFR coverage)
- **E**xecution: Populate sections systematically
- **E**valuation: Verify completeness against goals
- **R**efinement: Iterate if gaps remain, research via Context7 if uncertain
- **F**ramework: Apply OODA for any sub-decisions

This ensures thorough, multi-stage enhancement rather than single-pass population.

---

## Phase 5: Task-Creator Readiness Validation

**Actor**: Orchestrator  
**Duration**: ~30 seconds

### Purpose

Validate Implementation Plan sections are complete enough for `/tasks` command.

### Validation Criteria

| Criterion | Requirement |
|-----------|-------------|
| Implementation Plan Section | Must exist in every plan file |
| Minimum Phases | ≥3 phases defined (e.g., "Phase 1:", "Phase 2:", "Phase 3:") |
| Concrete Tasks | ≥2 tasks per phase with descriptions |
| File Paths | Actual paths specified (packages/, tests/, etc.), not `[file/path]` placeholders |
| Dependencies | Dependencies between phases documented |
| Placeholder Count | ≤3 placeholders per Implementation Plan |
| Architecture Markers | No `[Architecture Review Agent: ...]` remaining |

### Quality Gates

| Status | Condition | Action |
|--------|-----------|--------|
| **PASS** | All criteria met | Proceed to Phase 6 |
| **WARN** | Missing 1-2 items | Suggest re-run architecture |
| **FAIL** | Missing ≥3 items OR <2 phases | BLOCK until enhanced |

### Recovery on FAIL

Re-run architecture with `enhanced_scope: "implementation_detail"` on failed files.

### Thinking Framework: DMAIC (Measure + Analyze)

Readiness validation uses quality measurement methodology:

**MEASURE**:
- Count implementation phases (target: >=3)
- Count tasks per phase (target: >=2)
- Check for file path specifications
- Verify dependency documentation

**ANALYZE**:
- Calculate readiness score from measurements
- Identify specific gaps (which phases incomplete, what's missing)
- Determine PASS/WARN/FAIL based on gap count

This ensures objective, data-driven readiness assessment.

---

## Phase 6: Architecture Review

**Actor**: architectureer agent  
**Duration**: ~3-5 minutes

### Purpose

Comprehensive validation of all plans before human review.

### Validation Scope

- **Technical Completeness**: All required sections present
- **Integration Points**: Cross-plan dependencies validated
- **Production Readiness**: Scalability, security, observability assessed
- **Architecture Decisions**: Key decisions documented with rationale

### Quality Requirements

| Metric | Minimum | Target |
|--------|---------|--------|
| Architecture Score | 3.0 | 3.5+ |
| Integration Analysis | Required | Complete |
| Security Review | Required | Approved |

### Expected Output

- Validation report for all plans
- Integration analysis and dependency matrix
- Production readiness assessment
- Quality scores per plan and overall
- Recommendations for improvements

### Thinking Framework: Disney Creative Strategy

Architecture review uses three-lens validation:

**Lens 1 - DREAMER** (Vision):
- Does this architecture inspire? Is it elegant?
- Does it achieve the business vision?
- Would stakeholders be proud of this design?
- Output: vision_verdict (PASS | NEEDS_WORK) + note

**Lens 2 - REALIST** (Practicality):
- Can this actually be built with available resources?
- Is the timeline achievable?
- Are required skills available?
- Output: practicality_verdict (PASS | NEEDS_WORK) + note

**Lens 3 - CRITIC** (Risk):
- What could go wrong?
- What's missing from the design?
- What assumptions are risky?
- Output: risk_verdict (PASS | NEEDS_WORK) + note

**Consolidated**: Overall verdict based on three lenses + top recommendation

This catches gaps that single-perspective review would miss.

---

## Phase 7: Present Results

**Actor**: Orchestrator  
**Duration**: ~1 minute

### Purpose

Present complete workflow results with verification checklist for human review.

### Presentation Format


```markdown
## Planning Complete ✅

### Workflow Verification Results:
✅ **Phase 1**: Input validation - SPEC.md verified
✅ **Phase 2**: Component breakdown - [X] components identified
✅ **Phase 3**: Plan file creation - [X] files generated
✅ **Phase 4**: Enhancement pipelines - All files enhanced
✅ **Phase 5**: Task-creator readiness - PASS
✅ **Phase 6**: Architecture review - Score: X.X/5

### Plan Files Created:
- [component-1]-PLAN.md - Ready for implementation ✅
- [component-2]-PLAN.md - Ready for implementation ✅

### Architecture Review Results:
- **Quality Score**: X.X/5 (Target: ≥3.5) ✅
- **Integration Analysis**: Complete ✅
- **Security Assessment**: Approved ✅
- **Production Readiness**: Ready ✅

### Quality Metrics Achieved:
- Requirements Coverage: X% (Target: ≥95%) ✅
- Pain Point Alignment: X.X (Target: ≥0.4) ✅

### Next Step:
Would you like to proceed to `/tasks [feature-dir]` to generate implementation tasks?
[Yes / No / Review Plans First]
```

### Human Decision Options

| Option | Description | Next Action |
|--------|-------------|-------------|
| **Approve** | Plans are complete | Proceed to `/tasks` |
| **Refine** | Need adjustments | Provide specific feedback |
| **Reject** | Major issues | Return to /spec or restart |

### Thinking Framework: Pre-Mortem Awareness

When presenting results, especially for REFINE decisions:

**Pre-Mortem Framing**:
- "If we proceed to /tasks without addressing [issue], what could fail?"
- "Assume implementation fails in 2 weeks - which plan gaps would be the cause?"

This helps users make informed refinement decisions by surfacing hidden risks.

**Structured Refinement Options** (informed by Pre-Mortem):
- `refine-technical`: Re-run architecture (risk: technical gaps cause implementation failures)
- `refine-business`: Re-run planning (risk: business misalignment causes rework)
- `refine-all`: Re-run Phase 4 (risk: multiple gaps compound)
- `refine-spec`: Issues in source SPEC (risk: garbage in, garbage out)
