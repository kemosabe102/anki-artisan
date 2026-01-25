# Plan Command Usage Examples

Complete workflow examples with expected output.

---

## Basic Usage

### Simple Feature Planning

**Input:**
```bash
/plan docs/01-planning/specifications/015-auth-system/SPEC.md
```

**Expected Workflow:**

```
Phase 1: Input Validation
✅ SPEC.md found at docs/01-planning/specifications/015-auth-system/SPEC.md
✅ Structure validated: 5 FR-IDs, business goals present

Phase 2: SPEC Validation & Component Analysis
Delegating to planning + feature-analyzer (parallel)...
✅ SPEC validated: completeness_score 92/100
✅ 2 components identified:
   - core-authentication (FR-001, FR-002, FR-003)
   - oauth-integration (FR-004, FR-005)

Phase 3: File Creation
Creating plan files...
✅ Created: docs/01-planning/specifications/015-auth-system/plans/core-authentication-PLAN.md
✅ Created: docs/01-planning/specifications/015-auth-system/plans/oauth-integration-PLAN.md

Phase 4: Enhancement Pipelines (Parallel)
Launching 2 parallel pipelines...
  Pipeline 1: core-authentication-PLAN.md
    → planning: Business sections populated ✅
    → architecture: Technical sections populated ✅
  Pipeline 2: oauth-integration-PLAN.md
    → planning: Business sections populated ✅
    → architecture: Technical sections populated ✅
✅ All pipelines complete (2 min 15 sec)

Phase 5: Task-Creator Readiness Validation
Validating Implementation Plans...
✅ core-authentication-PLAN.md: 4 phases, 12 tasks, 0 placeholders - PASS
✅ oauth-integration-PLAN.md: 3 phases, 8 tasks, 1 placeholder - PASS

Phase 6: Architecture Review
Delegating to architectureer...
✅ Architecture Score: 4.2/5
✅ Integration Analysis: Complete (2 integration points validated)
✅ Security Assessment: Approved
✅ Production Readiness: Ready

Phase 7: Present Results
## Planning Complete ✅

### Plan Files Created:
- core-authentication-PLAN.md - Ready for implementation ✅
- oauth-integration-PLAN.md - Ready for implementation ✅

### Quality Metrics:
- Requirements Coverage: 100% (5/5 FR-IDs) ✅
- Architecture Score: 4.2/5 ✅

Next Step: /tasks docs/01-planning/specifications/015-auth-system/
```

---

## Review Mode

### Analyzing Existing Plans

**Input:**
```bash
/plan docs/01-planning/specifications/015-auth-system/SPEC.md --mode=review
```

**Expected Workflow:**
```
Review Mode: Analyzing existing plans...

Found Plans:
- core-authentication-PLAN.md (last modified: 2025-01-15)
- oauth-integration-PLAN.md (last modified: 2025-01-15)

Delegating to architectureer...

### Review Results:

| Plan File | Score | Status | Issues |
|-----------|-------|--------|--------|
| core-authentication-PLAN.md | 4.2/5 | PASS | None |
| oauth-integration-PLAN.md | 3.8/5 | PASS | Minor: Consider adding retry logic |

### SPEC → Plan Alignment:
- FR-001: ✅ Mapped to core-authentication Phase 1
- FR-002: ✅ Mapped to core-authentication Phase 2
- FR-003: ✅ Mapped to core-authentication Phase 3
- FR-004: ✅ Mapped to oauth-integration Phase 1
- FR-005: ✅ Mapped to oauth-integration Phase 2

Overall: Plans are well-aligned with SPEC.md
```

---

## Quick Mode

### Fast Planning Without Human Review

**Input:**
```bash
/plan docs/01-planning/specifications/015-auth-system/SPEC.md --mode=quick
```

**Expected Workflow:**
```
Quick Mode: Skipping human review checkpoints...

[Phases 1-6 execute automatically]

## Planning Complete ✅ (Quick Mode)

Plan files created and validated.
Architecture Score: 4.1/5 ✅

Plans ready at: docs/01-planning/specifications/015-auth-system/plans/

Run /tasks to generate implementation tasks.
```

---

## Custom Output Directory

### Override Default Location

**Input:**
```bash
/plan docs/01-planning/specifications/015-auth-system/SPEC.md --output-dir=custom/plans/auth/
```

**Expected Workflow:**
```
Output directory override: custom/plans/auth/

Creating directory: custom/plans/auth/ ✅

[Workflow proceeds with custom output location]

Plan files created at:
- custom/plans/auth/core-authentication-PLAN.md
- custom/plans/auth/oauth-integration-PLAN.md
```

---

## Error Scenario Examples

### SPEC.md Not Found

**Input:**
```bash
/plan docs/01-planning/specifications/999-nonexistent/SPEC.md
```

**Expected Output:**
```
❌ Phase 1 Failed: Input Validation

SPEC.md not found at: docs/01-planning/specifications/999-nonexistent/SPEC.md

Recovery Options:
1. Verify the path is correct
2. Run /spec to generate a new specification
3. Check if the file was moved or renamed
```

### Architecture Review Below Threshold

**Expected Output:**
```
⚠️ Phase 6 Warning: Architecture Review

Architecture Score: 3.2/5 (Target: ≥3.5)

Issues Found:
- oauth-integration-PLAN.md: Missing error handling strategy
- oauth-integration-PLAN.md: Token refresh flow not documented

Recommendations:
1. Add error handling section to oauth-integration plan
2. Document token refresh flow in Implementation Plan

Options:
- [Proceed Anyway] Accept technical debt
- [Refine Plans] Address issues before proceeding
- [Cancel] Return to /spec for requirements clarification
```
