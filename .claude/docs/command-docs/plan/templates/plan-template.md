# LEAN FEATURE PLAN: [Feature Name]

> **Status:** Draft | Locked
> **Owner:** [Your Name]
> **Date:** [YYYY-MM-DD]
> **Spec Reference:** `docs/01-planning/specifications/XXX-[feature-name]/SPEC.md`

---

## 1. Solution Design (High-Level Architecture)

*How will you actually build this? 5-7 bullets. No code.*

- User clicks [action] → Frontend calls [endpoint/event]
- Backend [queries/computes/transforms] [data source]
- [System/Service] returns [result type]
- Frontend displays [result] to user
- Result is persisted in [storage]

**Key Technology Choices:**
- Use [Library/Framework] for [component]
- Constraint: Must support [scaling requirement]

---

## 2. Implementation Phases

### Phase 1: [Foundation] (~[X] days)

**What:** [Specific deliverable]

**Acceptance:**
- [ ] [Testable outcome 1]
- [ ] [Testable outcome 2]
- [ ] No console errors

**Testing:** [How you'll verify this phase works]

---

### Phase 2: [Integration] (~[X] days)

**What:** [Next logical step]

**Acceptance:**
- [ ] [Testable outcome]
- [ ] Works with Phase 1

---

### Phase 3: [Polish] (~[X] days)

**What:** Edge cases, error handling, performance

**Acceptance:**
- [ ] Handles all edge cases from spec
- [ ] Error messages are user-friendly
- [ ] Response time < [spec constraint]

---

## 3. Data Model / API Changes (if applicable)

### Database Changes
```
No schema changes needed.
OR
New table: [table_name]
  - id (primary key)
  - [field] ([type])
  - created_at (timestamp)
```

### API Endpoints
```
POST /api/[resource]
  Input: {key: value}
  Output: {response}
  Status: 200 OK | 400 Bad Request
```

---

## 4. Technical Risks & Mitigations

| Risk | Mitigation |
|:-----|:-----------|
| [Risk 1: Component X fails] | Test locally first, use fallback [approach] |
| [Risk 2: Performance degrades] | Implement [optimization], measure with profiler |

---

## 5. Definition of Done

- [ ] All acceptance criteria from spec met
- [ ] All phases completed
- [ ] Tested locally with edge cases
- [ ] No console errors/warnings
- [ ] Code is committed
- [ ] Ready for demo

---

## 6. Open Questions / Blockers

- [ ] [Question that might delay you]
- [ ] [Dependency on another feature]

---

**Next:** Once status is "Locked", run `/tasks` to generate implementation tasks.
