# Delegation Examples for spec-reviewer

**Purpose**: How orchestrator delegates to spec-reviewer and expected responses

---

## Comprehensive Review

**Orchestrator Delegation**:
```
Task(spec-reviewer, 
  "Review SPEC quality for docs/01-planning/specifications/015-feature-name/SPEC.md. 
   Assess completeness, testability, clarity, and progressive disclosure. 
   Generate review report with quality grades and recommendations.")
```

**Expected Output Location**: `docs/01-planning/specifications/015-feature-name/review/spec-review-report.md`

---

## Focused Review (Testability)

**Orchestrator Delegation**:
```
Task(spec-reviewer,
  "Focused review on TESTABILITY for docs/01-planning/specifications/015-feature-name/SPEC.md.
   Deep-dive on measurable criteria and verifiable acceptance scenarios.")
```

---

## Ambiguity Detection

**Orchestrator Delegation**:
```
Task(spec-reviewer,
  "Find ambiguous requirements in docs/01-planning/specifications/015-feature-name/SPEC.md.
   Flag vague terms, unclear success criteria, and missing specifications.")
```

---

## Multi-Agent Workflow Context

### Upstream: /spec command
spec-reviewer runs AFTER /spec command creates/updates SPEC files.

### Downstream: Remediation
If review returns CONDITIONAL or NOT READY:
- Orchestrator may use /spec command for improvements
- Or present findings to user for manual resolution

---

## Response Structure

```json
{
  "status": "SUCCESS",
  "agent": "spec-reviewer",
  "summary": "SPEC quality assessment complete. Grade: B (0.82)",
  "success_evidence": {
    "quality_assessment": {
      "completeness_score": 0.85,
      "testability_score": 0.78,
      "clarity_score": 0.88,
      "ambiguity_index": 3,
      "progressive_disclosure_score": 0.80,
      "overall_grade": "B"
    },
    "review_findings": {
      "strengths": ["Clear FR definitions", "Well-structured acceptance criteria"],
      "weaknesses": ["NFR-002 missing performance targets"],
      "recommendations": [...]
    }
  },
  "confidence": 0.88
}
```

---

## Failure Scenarios

### File Not Found
```json
{
  "status": "FAILURE",
  "agent": "spec-reviewer",
  "failure_details": {
    "error_type": "missing_file",
    "error_message": "SPEC.md not found at specified path",
    "recovery_suggestions": ["Verify path", "Check if /spec command completed"]
  }
}
```

### Invalid Structure
```json
{
  "status": "FAILURE", 
  "agent": "spec-reviewer",
  "failure_details": {
    "error_type": "invalid_structure",
    "error_message": "SPEC missing required sections",
    "recovery_suggestions": ["Ensure Overview section exists", "Add FR-XXX requirements"]
  }
}
```
