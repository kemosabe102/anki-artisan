# Scoring Criteria

Detailed criteria for Impact and Effort scoring in technical debt prioritization.

---

## Impact Scoring (0-10)

Impact measures the business value and risk reduction of remediating a finding.

### Score Definitions

| Score | Category | Criteria | Examples |
|-------|----------|----------|----------|
| 9-10 | Critical | Security, data integrity, core functionality | SQL injection, auth bypass, data corruption |
| 7-8 | High | Performance, reliability, critical path | Memory leaks, race conditions, SLA violations |
| 5-6 | Moderate | Maintainability, testability, DX | High complexity, low coverage, coupling |
| 3-4 | Low | Code clarity, documentation | Naming, comments, minor UX issues |
| 1-2 | Minimal | Cosmetic, style preferences | Formatting, whitespace, ordering |

### Impact Assessment Questions

**Score 9-10 if ANY apply**:
- Could this cause security breach or data loss?
- Does this affect payment processing or PII?
- Would failure cause complete system outage?
- Is this a regulatory compliance issue?

**Score 7-8 if ANY apply**:
- Does this cause noticeable performance degradation?
- Could this lead to intermittent failures?
- Does this block critical user workflows?
- Is this in a high-traffic code path?

**Score 5-6 if ANY apply**:
- Does this make the code harder to modify?
- Does this increase onboarding time for new developers?
- Is test coverage significantly below target?
- Are there circular dependencies?

**Score 3-4 if ANY apply**:
- Is this primarily about code readability?
- Does this only affect developer experience?
- Is the documentation incomplete but code works?

**Score 1-2 if ALL apply**:
- Purely cosmetic or stylistic
- No functional impact
- Existing code works correctly
- No maintainability concerns

---

## Effort Scoring (0-10)

Effort measures the time and complexity to remediate a finding.

### Score Definitions

| Score | Time Estimate | Scope | Examples |
|-------|---------------|-------|----------|
| 9-10 | >2 weeks | Architectural changes, multiple teams | System redesign, platform migration |
| 7-8 | 1-2 weeks | Significant refactoring | Major module rewrite, schema changes |
| 5-6 | 2-5 days | Moderate changes | Cross-file refactoring, API changes |
| 3-4 | 1-2 days | Localized changes | Single module fix, adding tests |
| 1-2 | <1 day | Quick fixes | Config change, simple bug fix |

### Effort Assessment Questions

**Score 9-10 if ANY apply**:
- Does this require changes to system architecture?
- Are multiple teams or services affected?
- Is database migration with downtime required?
- Does this require new infrastructure?

**Score 7-8 if ANY apply**:
- Is significant refactoring needed (>500 LOC)?
- Are there complex dependencies to untangle?
- Is extensive testing required?
- Does this require coordination across modules?

**Score 5-6 if ANY apply**:
- Are changes needed in multiple files?
- Is there moderate complexity in the fix?
- Are new tests needed?
- Is code review likely to require iterations?

**Score 3-4 if ANY apply**:
- Is the fix contained to one module?
- Is the solution straightforward?
- Can existing tests cover the change?

**Score 1-2 if ALL apply**:
- Single file change
- Simple, obvious fix
- Minimal testing needed
- Low risk of side effects

---

## P1 Quick Win Validation

For P1 classification, effort must be <4 hours. Additional validation:

| Check | Requirement |
|-------|-------------|
| Time estimate | <4 hours actual work |
| Dependencies | None or already resolved |
| Testing | Existing tests cover or trivial to add |
| Review | Standard review process sufficient |
| Rollback | Easy to revert if issues arise |

---

## Scoring Examples

### Example 1: SQL Injection Vulnerability
```
Finding: Unsanitized user input in database query
Impact: 10 (security vulnerability, data integrity)
Effort: 2 (parameterized query is simple fix)
Priority Score: (10 x 2) - 2 = 18
Quadrant: P1 Quick Wins
```

### Example 2: Legacy Authentication Module
```
Finding: Outdated auth library with maintenance burden
Impact: 7 (reliability, security updates)
Effort: 8 (significant refactoring, testing)
Priority Score: (7 x 2) - 8 = 6
Quadrant: P2 Strategic
```

### Example 3: Code Style Inconsistency
```
Finding: Mixed naming conventions in utility module
Impact: 2 (cosmetic, style preference)
Effort: 3 (moderate find-and-replace)
Priority Score: (2 x 2) - 3 = 1
Quadrant: P4 Opportunistic
```

---

## Cross-References

- **Quadrant Thresholds**: [quadrant-classification.md](quadrant-classification.md)
- **Priority Formula**: SKILL.md
- **Shared Formulas**: `.claude/skills/tech-debt-shared/FORMULAS.md` section 2
