# Output Templates

Sample Business Review Report and Business Edit Plan structures for technical-pm agent outputs.

---

## Business Review Report Template

```markdown
# Business Review Report

**Specification**: [Feature Name]
**Review Date**: [ISO 8601 timestamp]
**Agent**: technical-pm
**Operation**: business_review

---

## Executive Summary

[1-3 sentence overview of findings and overall assessment]

**Overall Alignment Score**: [0.00-1.00]
**Recommendation**: [PROCEED / PROCEED WITH CHANGES / HALT FOR REVIEW]

---

## Business Goals Alignment

**Score**: [0.00-1.00]

| Business Goal | Plan Coverage | Gap Analysis |
|---------------|---------------|--------------|
| [Goal 1] | [Fully/Partially/Not Covered] | [Gap description or "None"] |
| [Goal 2] | [Coverage level] | [Gap description] |

**Evidence**: [Specific plan sections demonstrating alignment]

---

## NFR Assessment

| Category | Coverage | Key Risks | Mitigation Status |
|----------|----------|-----------|-------------------|
| Performance | [Low/Medium/High] | [Risk summary] | [Addressed/Partial/Missing] |
| Security | [Coverage] | [Risk summary] | [Status] |
| Operational | [Coverage] | [Risk summary] | [Status] |
| Integration | [Coverage] | [Risk summary] | [Status] |

**Critical Gaps**: [List any "Low" coverage areas requiring immediate attention]

---

## Requirements Traceability

**Coverage**: [X]% ([N] of [M] requirements traced)

| FR-ID | Description | Traced To | Status |
|-------|-------------|-----------|--------|
| FR-001 | [Requirement] | [Plan section] | [Traced/Gap] |
| FR-002 | [Requirement] | [Plan section] | [Status] |

**Unmapped Requirements**: [List any requirements without traceability]

---

## Placeholder Census

| Priority | Count | Examples |
|----------|-------|----------|
| Critical | [N] | [TBD: authentication method], [TBD: rate limits] |
| Important | [N] | [Example placeholders] |
| Nice-to-have | [N] | [Example placeholders] |

**Total Placeholders**: [N]

---

## Framework Compliance

| Framework | Applied | Findings |
|-----------|---------|----------|
| cost-analysis-framework.md | Yes/No | [Budget status, ROI assessment] |
| risk-assessment-matrix.md | Yes/No | [Risk coverage assessment] |
| quality-scoring-algorithms.md | Yes/No | [Timeline realism score] |

---

## Recommendations

### P1 (Critical)
1. **[Category]**: [Recommendation]
   - Rationale: [Why this matters]
   - Effort: [Low/Medium/High]
   - Business Impact: [Critical/High/Medium/Low]

### P2 (Important)
1. **[Category]**: [Recommendation]
   - Rationale: [Why]
   - Effort: [Estimate]

### P3 (Nice-to-have)
1. **[Category]**: [Recommendation]

---

## Zero Mutation Verification

- [x] No source files modified during review
- [x] All analysis performed via Read operations only
- [x] Report written to review/ directory only
```

---

## Business Edit Plan Template

```json
{
  "edit_plan": {
    "target_files": [
      {
        "path": "docs/01-planning/specifications/XXX-feature/PLAN.md",
        "edits": [
          {
            "section": "Business Context",
            "pattern": "[TBD: business justification]",
            "replacement": "Specific business justification text",
            "priority": "P1",
            "rationale": "Missing critical business context blocks stakeholder approval"
          },
          {
            "section": "Success Metrics",
            "pattern": "[Placeholder: metrics]",
            "replacement": "1. Response time <200ms\n2. 99.9% uptime\n3. <$50/month operational cost",
            "priority": "P2",
            "rationale": "Quantified metrics enable objective success validation"
          }
        ]
      }
    ],
    "enhancement_sequence": [
      "1. Address P1 business context gaps",
      "2. Add quantified success metrics",
      "3. Complete NFR specifications",
      "4. Resolve remaining placeholders"
    ],
    "target_agent": "plan-enhancer",
    "validation_criteria": [
      "business_goals_alignment_score >= 0.75",
      "All P1 placeholders resolved",
      "NFR coverage >= Medium across all categories"
    ]
  }
}
```

---

## SUCCESS Output Structure

```json
{
  "status": "SUCCESS",
  "agent": "technical-pm",
  "task_id": "tpm-20240115-001",
  "operation_type": "plan_file_enhancement",
  "summary": "Business review completed. Alignment score 0.72, 3 P1 gaps identified, NFR coverage adequate.",
  "validation_checklist": {
    "checks_performed": [
      "business_alignment_analysis",
      "nfr_coverage_assessment",
      "traceability_mapping",
      "placeholder_census"
    ],
    "all_checks_passed": true,
    "check_details": [
      {
        "check_name": "business_alignment",
        "status": "passed",
        "evidence": "4 of 5 business goals fully traced to plan components",
        "validation_method": "business_context_validation",
        "score": 0.72
      }
    ]
  },
  "success_evidence": {
    "operation_result": {
      "plan_enhancements": { "..." },
      "files_enhanced": [],
      "handoff_package": {
        "architecture_handoff_ready": true,
        "business_context_preserved": true
      }
    },
    "recommendations": [
      {
        "category": "business_strategy",
        "priority": "critical",
        "recommendation": "Add explicit ROI timeline to justify $75/month infrastructure cost",
        "rationale": "Costs >$50/month require business justification per cost framework",
        "business_impact": "high",
        "implementation_effort": "low"
      }
    ],
    "next_actions": [
      "Delegate Business Edit Plan to plan-enhancer",
      "Re-review after P1 gaps addressed"
    ],
    "changes": []
  },
  "confidence": 0.85,
  "severity": "Minor",
  "execution_timestamp": "2024-01-15T10:30:00Z"
}
```

---

## FAILURE Output Structure

```json
{
  "status": "FAILURE",
  "agent": "technical-pm",
  "task_id": "tpm-20240115-002",
  "operation_type": "plan_file_enhancement",
  "summary": "Review failed: SPEC.md not found in specification directory",
  "validation_checklist": {
    "checks_performed": ["file_discovery"],
    "all_checks_passed": false,
    "failed_checks": [
      {
        "check_name": "spec_file_exists",
        "status": "failed",
        "reason": "SPEC.md not found at expected path",
        "evidence": "Glob returned 0 results for docs/01-planning/specifications/XXX/*.md",
        "expected_criteria": "SPEC.md present in specification directory",
        "actual_result": "No markdown files found"
      }
    ]
  },
  "failure_details": {
    "failure_type": "plan_file_not_found",
    "reasons": [
      "Specification directory does not contain SPEC.md",
      "Path may be incorrect or specification not yet created"
    ],
    "missing": ["SPEC.md", "PLAN.md"],
    "recovery_suggestions": [
      {
        "strategy": "verify_path",
        "description": "Confirm specification directory path is correct",
        "estimated_effort": "low",
        "success_probability": 0.8
      },
      {
        "strategy": "create_spec",
        "description": "Create SPEC.md using spec-creator agent before review",
        "estimated_effort": "medium",
        "success_probability": 0.95
      }
    ]
  },
  "confidence": 0.95,
  "severity": "Major",
  "execution_timestamp": "2024-01-15T10:35:00Z"
}
```
