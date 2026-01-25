# Feature Plan - Quick Reference Card

Print this or bookmark for quick lookup while planning/executing features.

---

## Feature Object Structure (Copy-Paste Template)

```json
{
  "id": "PREFIX_NNN",
  "category": "functional|infrastructure|testing|performance|documentation|bug_fix",
  "description": "Human-readable one-liner describing the feature",
  "steps": [
    "Step 1: Concrete action with specifics",
    "Step 2: Next action",
    "Step 3: Verification step"
  ],
  "acceptance_criteria": [
    "Criterion 1: Measurable outcome",
    "Criterion 2: Verifiable result",
    "Criterion 3: Testable state"
  ],
  "passes": false,
  "estimated_hours": 1.5
}
```

---

## ID Naming Convention

| Feature Type | Prefix | Examples |
|--------------|--------|----------|
| Infrastructure | `INFRA_` | INFRA_SETUP_001, INFRA_CI_002 |
| Data pipeline | `DATA_` | DATA_IMPORT_001, DATA_TRANSFORM_002 |
| Authentication | `AUTH_` | AUTH_LOGIN_001, AUTH_2FA_002 |
| API endpoints | `API_` | API_USERS_001, API_ORDERS_002 |
| UI components | `UI_` | UI_CHART_001, UI_FORM_002 |
| Testing | `TEST_` | TEST_SUITE_001, TEST_E2E_002 |
| Database | `DB_` | DB_SCHEMA_001, DB_MIGRATION_002 |
| Documentation | `DOC_` | DOC_API_001, DOC_GUIDE_002 |
| Bug fixes | `BUG_` | BUG_CRASH_001, BUG_PERF_002 |

**Always use**: PREFIX_DESCRIPTION_NNN (zero-padded numbers)

---

## Category Reference

| Category | When to Use | Examples |
|----------|------------|----------|
| **functional** | Core feature implementation | User signup, payment processing, report generation |
| **infrastructure** | Setup, frameworks, tooling | Docker, Kubernetes, CI/CD, database setup |
| **testing** | Tests, validation, verification | Unit tests, integration tests, E2E tests |
| **performance** | Optimization, caching | Database tuning, query optimization, memory reduction |
| **documentation** | Guides, API docs, comments | API documentation, user guides, runbooks |
| **bug_fix** | Defect resolution | Fix crash, fix calculation error, fix UI bug |

---

## Steps - Good vs Bad

### ❌ BAD STEPS (Too Vague)
```json
"steps": [
  "Implement authentication",
  "Add tests",
  "Make it work"
]
```

### ✅ GOOD STEPS (Concrete & Specific)
```json
"steps": [
  "Create User model with email, username, password_hash fields",
  "Implement POST /api/auth/signup endpoint",
  "Hash passwords using bcrypt with salt factor 12",
  "Validate email format using regex ^[...]+@[...]+\\.[...]+$",
  "Check for duplicate email in database",
  "Return JWT token on success (exp: 24 hours)",
  "Write unit test for valid signup",
  "Write unit test for duplicate email error",
  "Verify all tests pass"
]
```

### Key: Each step should be a 15-30 minute task

---

## Acceptance Criteria - Good vs Bad

### ❌ BAD CRITERIA (Vague)
```json
"acceptance_criteria": [
  "Works correctly",
  "No errors",
  "Tests pass"
]
```

### ✅ GOOD CRITERIA (Measurable)
```json
"acceptance_criteria": [
  "POST /api/auth/signup returns 201 on valid input",
  "Returns 400 with error message on invalid email format",
  "Returns 409 if email already exists",
  "Password minimum 8 characters, 1 uppercase, 1 number, 1 special",
  "Password never stored in plain text (verified in database)",
  "JWT token valid for 24 hours from creation",
  "Unit test coverage >90%",
  "Integration test: full signup → login flow works",
  "Load test: handles 1000 concurrent signups",
  "No console errors or security warnings"
]
```

### Key: Each criterion is verifiable by inspection or test

---

## Time Estimation Guide

| Hours | Size | Features | When to Split |
|-------|------|----------|----------------|
| 0.5 | Tiny | Config change, simple test | Never |
| 1.0 | Small | Basic feature, some tests | If >50% is one task |
| 1.5 | Small-Med | Feature + testing + docs | If >50% is one task |
| 2.0 | Medium | Full feature, good coverage | If >2.5 hours |
| 2.5 | Medium | Complex logic + tests | If >2.5 hours |
| 3.0 | Medium-Large | Large module with integration | **SPLIT** |
| 3.5+ | Large | Multiple components | **SPLIT** |

**Rule: Max 3 hours per feature, prefer 1-2 hours**

---

## Testing Checklist

✓ **Unit Tests**
- Test individual functions/methods
- Use mocks for external dependencies
- Test valid inputs, invalid inputs, edge cases
- All tests pass locally

✓ **Integration Tests**
- Test components working together
- Test with real (or realistic) data
- Test database interactions
- Verify data consistency

✓ **End-to-End Tests**
- Test as user would use it
- Full workflow from start to finish
- Browser automation for UI features
- Manual testing / screenshot proof

**Feature NOT complete until all three levels pass**

---

## Git Commit Message Template

```
Implement FEATURE_NNN: Brief description of what was done

- Specific change 1 (e.g., "Added POST /api/users endpoint")
- Specific change 2 (e.g., "Implemented password validation")
- Specific change 3 (e.g., "Added database migration")

All acceptance criteria verified:
✓ Criterion 1
✓ Criterion 2
✓ Criterion 3

Test results:
- Unit: 8/8 passing
- Integration: 4/4 passing
- E2E: Manual testing complete

Time: Estimated 2.0h, Actual 1.9h
```

**Always include:**
- Feature ID and description
- Specific changes made
- All acceptance criteria ✓
- Test results
- Time estimate vs actual

---

## WORKFLOW_STATUS.md Template

```markdown
# Feature Plan Progress - PROJECT_NAME

## Current Status
Phase: Phase 1 (Description)
Progress: 3/7 complete (43%)
Last Updated: YYYY-MM-DD HH:MM UTC

## Completed This Session
- [x] FEATURE_001 (2h estimated, 1.9h actual)
- [x] FEATURE_002 (1.5h estimated, 1.7h actual)
- [x] FEATURE_003 (2h estimated, 2.1h actual)

## In Progress
- [ ] FEATURE_004 (50% done, estimated 1h remaining)

## Not Started
- [ ] FEATURE_005
- [ ] FEATURE_006
- [ ] FEATURE_007

## Blockers
None currently.

## Quality Metrics
- Test coverage: 87% (target: >85%)
- All tests passing: YES
- Production bugs: 0
```

**Update after EVERY feature completion**

---

## Common Mistakes - Prevention

| Mistake | Prevention |
|---------|-----------|
| Feature too large | Estimate >3h? Split it. |
| Vague acceptance criteria | Ask: "How do I test this?" If unsure, too vague. |
| Skip testing | Test at 3 levels before marking complete. |
| Work on 2 features simultaneously | Work on ONE only. Finish before starting next. |
| Mark done without verification | All criteria must pass = true |
| No progress tracking | Update WORKFLOW_STATUS.md after each feature |
| Ambiguous steps | Ask: Can junior dev follow? If not, too vague. |
| Wrong time estimate | Track actual hours, improve estimation next time |

---

## When to Break a Feature

**You need to split if:**
- Estimated >3.5 hours
- Multiple unrelated components
- Can't test independently
- Multiple developers needed
- Depends on unfinished feature

**How to split:**
1. Break by component (UI + backend = 2 features)
2. Break by scope (MVP + nice-to-have = 2 features)
3. Break by risk (risky part first, then safe part)
4. Renumber remaining features

**Always update JSON, commit, communicate**

---

## Acceptance Criteria Keywords

### Must-Have Keywords
- **"Returns"** (for API endpoints)
- **"Handles"** (for edge cases)
- **"Validates"** (for input checking)
- **"Prevents"** (for errors/security)
- **"Verified in tests"** (for automation)

### Measurable Keywords
- **"<500ms"** (performance)
- **">85%"** (coverage)
- **"0 errors"** (quality)
- **"All X passing"** (test results)
- **"Deterministic"** (consistency)

### Bad Keywords (Vague)
- ❌ "Works well"
- ❌ "Looks good"
- ❌ "Should be"
- ❌ "Probably"
- ❌ "Somehow"

---

## Feature Plan Validation Checklist

Before marking `passes: true`:

- [ ] All steps completed?
- [ ] All acceptance criteria met?
- [ ] Unit tests written and passing?
- [ ] Integration tests written and passing?
- [ ] End-to-end test completed?
- [ ] Code reviewed (if team environment)?
- [ ] No console errors or warnings?
- [ ] Performance acceptable?
- [ ] Security reviewed (if applicable)?
- [ ] Documented (comments, if complex)?
- [ ] Git committed with message?
- [ ] WORKFLOW_STATUS.md updated?

**All items ✓ = feature complete**

---

## Phase Completion Checklist

Before closing a phase:

- [ ] All features marked `passes: true`
- [ ] Test coverage >85%
- [ ] No critical bugs
- [ ] Code reviewed
- [ ] Ready to deploy (works in staging)?
- [ ] Documentation complete?
- [ ] WORKFLOW_STATUS.md updated?

**All items ✓ = phase ready to launch**

---

## Emergency: Feature Blocked?

**What to do:**
1. Document blocker in WORKFLOW_STATUS.md
2. Note expected resolution date
3. Switch to DIFFERENT feature (not blocked)
4. Don't stay idle waiting

**If many features blocked:**
- Re-prioritize: unblock others first
- Parallel work: work on Phase 2 prep
- Communicate: team needs to know

**Keep momentum - never let blockers stop progress**

---

## Numbers to Remember

- **30-90 min**: Ideal feature size
- **1-2 weeks**: Ideal phase length
- **3-7**: Ideal features per phase
- **3 levels**: Testing (unit, integration, E2E)
- **85%+**: Minimum test coverage
- **±25%**: Acceptable estimation error
- **<3.5h**: Maximum feature time (else split)
- **100%**: Acceptance criteria pass rate (not 80%)

---

**Print this. Keep it handy. Reference while planning and executing features.**
