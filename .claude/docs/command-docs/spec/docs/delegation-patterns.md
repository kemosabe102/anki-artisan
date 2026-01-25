# Spec Command Delegation Patterns

Task patterns and review agent delegation in the `/spec` workflow.

---

## Quick Reference

| Phase | Agent/Action | Task Type | Key Parameters |
|-------|--------------|-----------|----------------|
| 5 | /spec command | feature-specification | specFilePath, specification, validationRequirements |
| 7 | /spec command | spec-validation-fixes | validationIssues, fixType |
| 10 | planning | spec_review | spec_file_path, review_focus, output_path |
| 10 | planning | spec_review | operation_type, spec_file_path, review_focus |
| 10 | architecture | spec_review | operation_type, spec_file_path, review_focus |
| 11 | /spec command | spec-refinement | reviewFindings, fixPriority |
| 13 | /spec command | spec-section-refinement | section, userFeedback |

---

## Phase 5: Initial Spec Generation

The /spec command generates specifications with the following context:

**Context Requirements**:
- Comprehensive multi-line context from Phases 1-3
- Spec File Path: docs/01-planning/specifications/XXX-[feature-name]/SPEC.md

**Specification Requirements**:
- Business Goals: [extracted from roadmap/guide/context]
- Constraints: MVP maturity, existing architecture, timeline
- Related Features: [identified during context loading]

**Validation Requirements**:
- Pain Point Alignment: minimum score 0.4
- Maturity Alignment: MVP stage, complexity threshold 0.3
- Requirements Completeness: minimum 0.7

**Reference Guide Context** (if file: input):
- Guide Path: [path to guide file]
- Guide Type: technical_implementation_guide
- Extracted Goals: [goals from guide]
- Technical Patterns: [approaches, tools, workflows from guide]
- Performance Targets: [targets from guide]
- Preserve for Planning: true

**Generation Steps**:
1. Read the initialized SPEC.md at the specified path
2. Populate all sections following spec-template.md structure
3. Ensure pain point alignment score calculated
4. Include ROI analysis with monthly time savings
5. All functional requirements must have acceptance criteria
6. Preserve technical context for planning phase

---

## Phase 7: Validation Fixes

The /spec command applies validation fixes:

**Spec File Path**: docs/01-planning/specifications/XXX-[feature-name]/SPEC.md

**Validation Issues**:
- Missing Sections: [list of missing sections]
- Incomplete Metrics: [list of incomplete calculations]
- Requirements Issues: [list of requirements without acceptance criteria]

**Fix Type**: validation_corrections
**Max Iterations**: 1

**Fix Steps**:
1. Add all missing required sections
2. Calculate missing metrics (pain point alignment, ROI)
3. Add acceptance criteria to requirements missing them
4. Establish traceability links (requirements -> pain points)
5. Do NOT change content that already passes validation

---

## Phase 10: Parallel Review (3 Agents)

**CRITICAL**: Launch all 3 in SINGLE message.

### Task(planning, quality_completeness)

```markdown
Task(planning, "Review specification quality and completeness

**Spec File Path**: docs/01-planning/specifications/XXX-[feature-name]/SPEC.md

**Review Focus**: quality_completeness_how_avoidance

**Output Path**: docs/01-planning/specifications/XXX-[feature-name]/review/planning-report.md

**Review Criteria**:
1. Completeness: All required sections present and populated
2. Quality: Clear, unambiguous language
3. HOW Avoidance: No implementation details (WHAT/WHY only)
4. Testability: Acceptance criteria are measurable
5. Progressive Disclosure: Appropriate detail level

**Output Format**:
- Overall Status: PASS/WARN/FAIL
- Section Scores: 0-100 per section
- Critical Issues: Must address before planning
- Recommendations: Improvements for quality")
```

### Task(planning, business_alignment)

```markdown
Task(planning, "Review specification business alignment

**Operation Type**: spec_review

**Spec File Path**: docs/01-planning/specifications/XXX-[feature-name]/SPEC.md

**Review Focus**: business_alignment_roi_validation

**Output Path**: docs/01-planning/specifications/XXX-[feature-name]/review/planning-report.md

**Review Criteria**:
1. Pain Point Alignment: Score ≥0.4, coverage of priority items
2. ROI Analysis: Credible time savings, reasonable cost estimates
3. Business Value: Clear value proposition
4. User Scenarios: Cover primary use cases
5. Budget Compliance: Within $100/month limit (or justified)

**Output Format**:
- Overall Status: PASS/WARN/FAIL
- Business Alignment Score: 0-5
- ROI Validation: PASS/FAIL with reasoning
- Critical Issues: Business blockers
- Recommendations: Business improvements")
```

### Task(architecture, technical_feasibility)

```markdown
Task(architecture, "Review specification technical constraints

**Operation Type**: spec_review

**Spec File Path**: docs/01-planning/specifications/XXX-[feature-name]/SPEC.md

**Review Focus**: technical_constraints_not_implementation

**Output Path**: docs/01-planning/specifications/XXX-[feature-name]/review/architecture-report.md

**Review Criteria**:
1. Technical Feasibility: Achievable with current architecture
2. Constraint Validation: Constraints are realistic and complete
3. Architecture Alignment: Fits system patterns
4. Dependency Analysis: Dependencies identified and reasonable
5. NOT Implementation: No architecture design (that's planning phase)

**Output Format**:
- Overall Status: PASS/WARN/FAIL
- Technical Feasibility: HIGH/MEDIUM/LOW
- Constraint Completeness: 0-100%
- Critical Issues: Technical blockers
- Recommendations: Constraint clarifications")
```

---

## Phase 11: Post-Review Refinement

The /spec command applies review fixes:

**Spec File Path**: docs/01-planning/specifications/XXX-[feature-name]/SPEC.md

**Review Findings**:
- Critical Issues: [aggregated from all 3 reviews]
- Important Issues: [aggregated from all 3 reviews]
- Consensus Items: [issues flagged by 2+ reviewers]

**Fix Priority**: critical_and_important_only
**Iteration Mode**: auto-apply
**Max Iterations**: 1

**Refinement Steps**:
1. Address ALL critical issues (must fix)
2. Address ALL important issues (high-impact)
3. Do NOT apply minor/P3 recommendations (preserve for user)
4. Track what was changed for transparency
5. Maintain specification quality score

---

## Phase 13: Section Refinement

The /spec command refines sections based on user feedback:

**Spec File Path**: docs/01-planning/specifications/XXX-[feature-name]/SPEC.md

**Section**: [section name, e.g., "Business Value & Pain Points"]

**User Feedback**: [captured feedback from interactive walkthrough]

**Refinement Type**: modify|add|remove|clarify

**Iteration Mode**: single-section

**Refinement Steps**:
1. Apply user feedback to the specified section only
2. Preserve all other sections unchanged
3. Maintain quality standards
4. Re-validate section after changes

---

## Parallel Execution Pattern

**Phase 10 requires launching 3 agents in a SINGLE message**:

```markdown
[Agent 1: planning]
Task(planning, "[full prompt]")

[Agent 2: planning]
Task(planning, "[full prompt]")

[Agent 3: architecture]
Task(architecture, "[full prompt]")
```

**Benefits**:
- 3x speedup vs sequential execution
- Zero file conflicts (separate output files)
- Comprehensive multi-perspective validation
