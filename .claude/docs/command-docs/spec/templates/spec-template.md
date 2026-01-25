# SPEC: [Feature/Project Name]

> **Status:** Draft | Locked
> **Owner:** [Name]
> **Date:** [YYYY-MM-DD]
> **ICE Score:** [XXX]

---

## 1. Context & Vision

**Problem Statement:** What user/business problem does this solve?

**Purpose:** What does this feature accomplish?

**Target Audience:** Who benefits from this?

---

## 2. User Stories

**Primary:**
As a [user type], I want [goal], so that [benefit].

**Scenarios:** (optional for small features)
- Scenario A: [description]
- Scenario B: [description]

---

## 3. Scope

**In Scope:**
- [What WILL be included]

**Out of Scope:**
- [What will NOT be included]
- [Future enhancements - explicitly deferred]

---

## 4. Goals & ICE Score

**Success Metrics:**
| Metric | Target | Measurement |
|--------|--------|-------------|
| [KPI 1] | [value] | [how measured] |

**ICE Score:**
| Metric | Score (1-10) | Rationale |
|--------|:------------:|-----------|
| Impact | [X] | [How much does this move success metrics?] |
| Confidence | [X] | [How sure are we about impact/effort?] |
| Ease | [X] | [How fast can we build this?] |
| **TOTAL** | **[XXX]** | *(Impact × Confidence × Ease)* |

> Threshold: <200 (Backlog) | 200-500 (Discuss) | >500 (Build)

---

## 5. Functional Requirements

| ID | Requirement | Priority | Testable? |
|----|-------------|----------|-----------|
| FR-001 | [description] | Must | Yes |
| FR-002 | [description] | Should | Yes |
| FR-003 | [description] | Could | Yes |

**Priority Key:** Must (required for MVP) | Should (expected) | Could (nice-to-have) | Won't (explicitly excluded)

---

## 6. Acceptance Criteria

**Given/When/Then Format:**
```gherkin
Given [initial context]
When [action occurs]
Then [expected outcome]
```

**Or Checklist Format:**
- [ ] User can [action] and see [result]
- [ ] System handles [edge case] by [behavior]
- [ ] [Performance requirement]

---

## 7. Non-Functional Requirements

> [OPTIONAL: Skip for small features]

| Category | Requirement | Target |
|----------|-------------|--------|
| Performance | Response time | < 500ms p95 |
| Scalability | Concurrent users | 1000 |
| Security | [requirement] | [target] |
| Availability | Uptime | 99.9% |

---

## 8. Constraints & Assumptions

**Constraints (must follow):**
- [Technical limit]
- [Resource limit]
- [Regulatory requirement]

**Assumptions (believe true, not verified):**
- [Technical assumption]
- [Business assumption]

---

## 9. Dependencies

| Dependency | Owner | Status | Impact if Delayed |
|------------|-------|--------|-------------------|
| [Component/Service] | [team/person] | [status] | [impact] |

---

## 10. Open Questions & Risks

**Open Questions:**
- [ ] [Question needing resolution]

**Risks:**
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| [risk] | High/Med/Low | High/Med/Low | [strategy] |

---

**Next:** Once status is "Locked", run `/plan` to create implementation plan.
