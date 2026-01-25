# [Review Type] Report: [Feature Name]

**Document**: [Path to SPEC.md]
**Reviewer**: [agent-name]
**Date**: [YYYY-MM-DD]
**SPEC Hash**: [git hash or commit date]

---

## Executive Summary

[1-2 paragraph summary of review findings. Include overall assessment and key takeaways.]

---

## Compliance Assessment

### Specification Focus

**WHAT Requirements** (Business outcomes and user needs):

- **Status**: [PASS / CONCERNS / FAIL]
- **Details**: [Explanation of how well spec defines WHAT users need]

**WHY Rationale** (Business justification and value):

- **Status**: [PASS / CONCERNS / FAIL]
- **Details**: [Explanation of how well spec justifies WHY this feature matters]

**HOW Avoidance** (Implementation details should NOT be present):

- **Status**: [PASS / CONCERNS / FAIL]
- **Details**: [Explanation of whether spec stays focused on requirements vs implementation]

### Quality Metrics

| Metric                   | Target | Actual            | Status     |
| ------------------------ | ------ | ----------------- | ---------- |
| Testable Requirements    | >90%   | [X%]              | [✅/⚠️/❌] |
| Requirements with FR-IDs | 100%   | [X%]              | [✅/⚠️/❌] |
| Ambiguity Level          | Low    | [Low/Medium/High] | [✅/⚠️/❌] |
| Completeness Score       | >0.7   | [X.XX]            | [✅/⚠️/❌] |
| HOW Details Found        | 0      | [X items]         | [✅/⚠️/❌] |

---

## Detailed Findings

### ✅ Strengths

**What the spec does well**:

1. [Strength 1 - specific example]
2. [Strength 2 - specific example]
3. [Strength 3 - specific example]

**Good Examples of WHAT/WHY Focus**:

- [Quote or reference to well-written requirement]
- [Quote or reference to clear business rationale]

### ⚠️ Issues Requiring Attention

#### CRITICAL Issues

[Issues that MUST be fixed before planning]

- **[ISSUE-001]**: [Brief description]
  - **Location**: Line [X] or Section [Y]
  - **Problem**: [What's wrong]
  - **Impact**: [Why this blocks planning]
  - **Recommendation**: [Specific fix needed]

#### IMPORTANT Issues

[Issues that SHOULD be addressed]

- **[ISSUE-002]**: [Brief description]
  - **Location**: Line [X] or Section [Y]
  - **Problem**: [What's wrong]
  - **Impact**: [Why this matters]
  - **Recommendation**: [Specific fix needed]

#### MINOR Issues

[Issues to consider improving]

- **[ISSUE-003]**: [Brief description]
  - **Location**: Line [X] or Section [Y]
  - **Problem**: [What could be better]
  - **Recommendation**: [Suggestion for improvement]

### 🔄 Recommendations

**Priority Order**:

1. **[P1]**: [Most important recommendation with rationale]
2. **[P2]**: [Second priority recommendation with rationale]
3. **[P3]**: [Third priority recommendation with rationale]

---

## Implementation Details Found (Should Be Removed)

[List any HOW details that leaked into the spec - these belong in PLAN.md, not SPEC.md]

| Location    | Implementation Detail                       | Should Be Replaced With       |
| ----------- | ------------------------------------------- | ----------------------------- |
| Line [X]    | [Specific algorithm/class/method mentioned] | [Outcome-focused requirement] |
| FR-[XXX]    | [Data structure or code pattern specified]  | [What needs to be achieved]   |
| Section [Y] | [Technical solution prescribed]             | [Business requirement]        |

**Examples**:

```markdown
❌ Line 142: "Use breadth-first search algorithm for dependency traversal"
✅ Replace with: "System MUST detect circular dependencies and report specific paths"

❌ FR-008: "Implement TaskGenerator class with generateFromPlan() method"
✅ Replace with: "System MUST generate task list from technical plan within 10 minutes"
```

**Total HOW Details Found**: [X items]
**Severity**: [CRITICAL / IMPORTANT / MINOR]

---

## Review Verdict

### Overall Assessment

- **Ready for Planning**: [YES / NO / CONDITIONAL]
- **Confidence Level**: [High / Medium / Low]

### Conditions (if CONDITIONAL)

**Must fix before proceeding to /plan**:

1. [Specific condition 1]
2. [Specific condition 2]

**Should address for quality**:

1. [Recommended improvement 1]
2. [Recommended improvement 2]

### Next Steps

**If YES (Ready)**:

```bash
/plan docs/01-planning/specifications/[XXX-feature-name]/SPEC.md
```

**If CONDITIONAL**:

1. Address CRITICAL issues listed above
2. Optionally address IMPORTANT issues
3. Re-run review or proceed with caution

**If NO (Not Ready)**:

1. Major revisions needed - see CRITICAL issues
2. Update SPEC.md
3. Re-run review process

---

## Appendix: Review Checklist

### Requirement Quality

- [ ] All requirements have FR-XXX, TC-XXX, or NFR-XXX identifiers
- [ ] Requirements use MUST/SHOULD/MAY language clearly
- [ ] Requirements are testable (observable outcomes)
- [ ] Ambiguous terms are defined or avoided

### Scenario Quality

- [ ] User scenarios use Given/When/Then format
- [ ] Scenarios focus on outcomes, not implementation
- [ ] Edge cases covered with specific scenarios
- [ ] Acceptance criteria concrete and measurable

### Implementation Avoidance

- [ ] No code structure specified (classes, functions, methods)
- [ ] No algorithms detailed (search, sort, traversal)
- [ ] No data schemas specified (tables, JSON formats)
- [ ] No API implementations described

### Business Alignment (if applicable)

- [ ] Pain points clearly identified
- [ ] ROI calculations present (hours-based)
- [ ] Business value quantified
- [ ] Success metrics business-focused

### Technical Constraints (if applicable)

- [ ] Platform choice justified
- [ ] Technical constraints are genuine requirements
- [ ] NFRs measurable (not vague)
- [ ] Integration points identified

---

## Machine-Readable Review Data

**Purpose**: Structured output for orchestrator parsing and review aggregation

```json
{
  "status": "SUCCESS",
  "agent": "planning",
  "task_id": "spec-review-[timestamp]",
  "operation_type": "spec_quality_review",
  "summary": "Brief executive summary of review findings and quality assessment",
  "validation_checklist": {
    "checks_performed": [
      "file_exists",
      "structure_valid",
      "requirements_assessed",
      "testability_checked"
    ],
    "all_checks_passed": true,
    "check_details": [
      "All functional requirements have FR-XXX identifiers",
      "95% of requirements are testable"
    ],
    "failed_checks": []
  },
  "success_evidence": {
    "quality_assessment": {
      "completeness_score": 0.85,
      "testability_score": 0.9,
      "clarity_score": 0.8,
      "ambiguity_index": 3.5,
      "pain_point_alignment": 0.75,
      "overall_grade": "B"
    },
    "review_findings": {
      "strengths": [
        "Clear functional requirements with specific acceptance criteria",
        "Well-defined user scenarios with Given/When/Then format"
      ],
      "weaknesses": [
        "Missing non-functional requirements for performance",
        "Some ambiguous terms in FR-007 need clarification"
      ],
      "recommendations": [
        {
          "priority": "High",
          "category": "requirements",
          "finding": "NFR-001 lacks measurable performance criteria",
          "recommendation": "Add specific latency thresholds (e.g., '<100ms p95')",
          "location": "Section 3.2 Non-Functional Requirements"
        },
        {
          "priority": "Medium",
          "category": "clarity",
          "finding": "Ambiguous term 'improve' used in FR-007",
          "recommendation": "Replace with measurable criteria (e.g., 'reduce by 50%')",
          "location": "FR-007"
        }
      ]
    },
    "validation_results": {
      "requirements_complete": true,
      "planning_metadata_present": true,
      "quality_threshold_met": true,
      "testability_validated": true,
      "pain_point_aligned": true
    },
    "ambiguity_analysis": {
      "ambiguous_terms": ["improve", "enhance", "optimize"],
      "unclear_requirements": ["FR-003", "FR-007"],
      "missing_specifications": [
        "error handling for edge case X",
        "performance targets for scenario Y"
      ]
    },
    "testability_analysis": {
      "testable_requirements": 12,
      "non_testable_requirements": 3,
      "specific_concerns": [
        "FR-005 lacks measurable criteria",
        "NFR-002 uses vague success criteria"
      ]
    }
  },
  "confidence": 0.92,
  "severity": "Minor",
  "execution_timestamp": "2025-10-06T12:34:56Z"
}
```

**Usage Notes**:

- Orchestrator parses this section to aggregate review findings
- `status` field indicates review completion (SUCCESS) vs failure (FAILURE)
- `quality_assessment` scores drive automated quality gates
- `recommendations` array enables priority-based fix workflows
- `validation_results` flags trigger downstream actions (e.g., proceed to /plan)

---

**Review Completed**: [Date]
**Reviewer Signature**: [agent-name]
**Review Guidelines**: `.claude/docs/guides/spec-review-guidelines.md`
