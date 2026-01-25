# Spec Review: [Feature Name]

**Document**: [Path to SPEC.md] | **Reviewer**: planning | **Date**: [YYYY-MM-DD]

---

## Executive Summary

[2-3 sentences: Overall assessment, key strengths, critical blockers if any.]

---

## Section Assessment

| Section | Status | Notes |
|---------|--------|-------|
| 1. User Story | [Pass/Issues] | [As a/I want/So that complete? Specific user type?] |
| 2. ICE Score | [Pass/Issues] | [Total: XXX, Threshold: <200 Backlog / 200-500 Discuss / >500 Build] |
| 3. Acceptance Criteria | [Pass/Issues] | [Observable behaviors? Testable? Edge cases?] |
| 4. Constraints & Out of Scope | [Pass/Issues] | [Requirements vs HOW? Scope clear?] |
| 5. Dependencies | [Pass/Issues] | [Blockers identified? External reqs?] |
| 6. Open Questions | [Pass/Issues] | [Actionable? Scope-affecting?] |

---

## ICE Score Validation

> **ICE Thresholds**: See `.claude/docs/00-core/orchestrator-thresholds.md#ice-score-thresholds`

| Factor | Score | Rationale Present |
|--------|-------|-------------------|
| Impact | [1-10] | [Yes/No] |
| Confidence | [1-10] | [Yes/No] |
| Ease | [1-10] | [Yes/No] |
| **Total** | **[XXX]** | Formula: I x C x E |

**Threshold**: [Below 200 - WARN] | [200-500 - OK] | [Above 500 - GOOD]

---

## HOW Violation Check

**Count**: [0] | **Severity**: [PASS (0) / WARNING (1-2) / CRITICAL (3+)]

| Location | Violation | Suggested Fix |
|----------|-----------|---------------|
| - | - | - |

---

## Quality Metrics

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| User Story Complete | As a/I want/So that | - | [Y/N] |
| ICE Score Valid | >= 200 | [XXX] | [Y/W/N] |
| Acceptance Criteria Testable | Observable behaviors | - | [Y/N] |
| HOW Violations | 0 | [X] | [Y/W/N] |
| Line Count | < 70 | [X] | [Y/W] |

---

## Verdict

| Field | Value |
|-------|-------|
| **Status** | [READY / CONDITIONAL / NOT_READY] |
| **Confidence** | [0.XX] |

### Conditions (if applicable)
- [ ] [Required fix before /plan]

---

## Next Steps

- **READY**: `/plan [path-to-SPEC.md]`
- **CONDITIONAL**: Address conditions above, then proceed or re-review
- **NOT_READY**: Fix blocking issues, update SPEC.md, re-run review

---

## Machine-Readable Output

```json
{
  "status": "SUCCESS",
  "agent": "planning",
  "verdict": "READY|CONDITIONAL|NOT_READY",
  "ice_score": {"impact": 0, "confidence": 0, "ease": 0, "total": 0, "threshold_met": true},
  "quality_metrics": {
    "user_story_complete": true,
    "ice_score_valid": true,
    "acceptance_criteria_testable": true,
    "how_violations": 0,
    "line_count": 0
  },
  "issues": [],
  "confidence": 0.00
}
```