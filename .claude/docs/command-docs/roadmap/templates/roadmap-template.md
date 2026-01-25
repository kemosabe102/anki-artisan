# ROADMAP: [Product Name]

**Version:** 1.0  
**Status:** Locked  
**Created:** [Date]  
**Owner:** [Name/Team]  

---

## Strategic Overview

This roadmap translates the Project Spec into executable phases. Each phase contains 4-6 features sorted by ICE score (highest impact/confidence/ease first). Build features top-to-bottom within each phase.

**Key principle:** Do not start Phase 2 until Phase 1 is complete.

---

## Phase 1: [Phase Name] ([Timeline])

**Goal:** [1 sentence on what Phase 1 achieves]

### Features (in build order by ICE score)

- [ ] **1.1 [Feature Name]** (ICE: ###)
  - **Impact:** _ | **Confidence:** _ | **Ease:** _
  - **User Story:** [From project spec]
  - **Spec:** [ ] To create
  - **Plan:** [ ] To create
  - **Tasks:** [ ] To create
  - **Building:** [ ] In progress

- [ ] **1.2 [Feature Name]** (ICE: ###)
  - **Impact:** _ | **Confidence:** _ | **Ease:** _
  - **User Story:** [From project spec]
  - **Spec:** [ ] To create
  - **Plan:** [ ] To create
  - **Tasks:** [ ] To create
  - **Building:** [ ] In progress

- [ ] **1.3 [Feature Name]** (ICE: ###)
  - **Impact:** _ | **Confidence:** _ | **Ease:** _
  - **User Story:** [From project spec]
  - **Spec:** [ ] To create
  - **Plan:** [ ] To create
  - **Tasks:** [ ] To create
  - **Building:** [ ] In progress

- [ ] **1.4 [Feature Name]** (ICE: ###)
  - **Impact:** _ | **Confidence:** _ | **Ease:** _
  - **User Story:** [From project spec]
  - **Spec:** [ ] To create
  - **Plan:** [ ] To create
  - **Tasks:** [ ] To create
  - **Building:** [ ] In progress

- [ ] **1.5 [Feature Name]** (ICE: ###)
  - **Impact:** _ | **Confidence:** _ | **Ease:** _
  - **User Story:** [From project spec]
  - **Spec:** [ ] To create
  - **Plan:** [ ] To create
  - **Tasks:** [ ] To create
  - **Building:** [ ] In progress

### Phase 1 Success Criteria
- [ ] All 5 features complete and tested
- [ ] [Metric from project spec]
- [ ] [Metric from project spec]
- [ ] Deployed to staging

**Definition of Done:** All checkboxes checked. Phase 1 is production-ready (or staging-ready).

---

## Phase 2: [Phase Name] ([Timeline])

**Goal:** [1 sentence on what Phase 2 achieves]

**Prerequisites:** Phase 1 complete

### Features (in build order by ICE score)

- [ ] **2.1 [Feature Name]** (ICE: ###)
  - **Impact:** _ | **Confidence:** _ | **Ease:** _
  - **User Story:** [From project spec]
  - **Spec:** [ ] To create
  - **Plan:** [ ] To create
  - **Tasks:** [ ] To create
  - **Building:** [ ] In progress

[Add more features...]

### Phase 2 Success Criteria
- [ ] All features complete
- [ ] [Metric from project spec]
- [ ] Ready for production

---

## Phase 3: [Phase Name] ([Timeline])

**Goal:** [1 sentence on what Phase 3 achieves]

**Prerequisites:** Phase 2 complete

### Features
[Same structure as phases 1-2]

---

## How to Use This Roadmap

### Weekly Workflow
1. Open ROADMAP.md
2. Find the first unchecked feature
3. Run: `/spec [Feature Name]`
4. Review spec (5 min)
5. Check: `[x] Spec`
6. Run: `/plan [Feature Name] --phase [X]`
7. Review plan (5 min)
8. Check: `[x] Plan`
9. Run: `/tasks [Feature Name] --phase [X]`
10. Review tasks (5 min)
11. Check: `[x] Tasks`
12. In Claude Code: "Execute Task 1.1"
13. After all tasks done: Check `[x] Building`
14. Move to next feature

### Estimated Time Per Feature
- Spec: 5 min
- Plan: 10 min
- Tasks: 5 min
- Building: 4-8 hours (depends on complexity)

### Tracking Progress
- **Week 1:** Generate all specs for Phase 1 (4-5 features = 20-25 min of planning)
- **Week 2-3:** Generate plans and tasks, start building
- **Week 4:** Phase 1 complete, evaluate Phase 2
- **Week 5-8:** Phase 2-3 execution

---

## Deferred Features (Backlog)

These are P1/P2 features from the Project Spec with ICE < 200. Revisit after Phase 1 is shipped.

- [ ] [Feature Name] (P1) - Why deferred: [reason]
- [ ] [Feature Name] (P1) - Why deferred: [reason]

---

## Success Metrics (Project-Level)

From Project Spec, Section 4:

### Primary Metrics
1. **[Metric 1]**
   - Target: [value]
   - Current: [value]
   - Status: [ ] Not started, [ ] In progress, [ ] Achieved

2. **[Metric 2]**
   - Target: [value]
   - Current: [value]
   - Status: [ ] Not started, [ ] In progress, [ ] Achieved

### Anti-Metrics (Watch for These)
- [ ] [Anti-metric from project spec]
- [ ] [Anti-metric from project spec]

---

## Risk Register

From Project Spec, Section 12:

| Risk | Likelihood | Impact | Mitigation | Status |
|:---|:---:|:---:|:---|:---|
| [Risk 1] | Low/Med/High | Low/Med/High | [Action] | [ ] Mitigated |
| [Risk 2] | Low/Med/High | Low/Med/High | [Action] | [ ] Mitigated |

---

## Notes & Decisions

- **Date:** [Decision]
  - Context: [What was being decided]
  - Decision: [What was chosen]
  - Why: [Rationale]

---

## Appendix: ICE Score Reference

**ICE = Impact x Confidence x Ease** (each 1-10)

### Impact (Does this matter?)
- 10: Foundational feature, nothing works without it
- 8-9: Core value prop, high priority
- 6-7: Important but optional
- 3-5: Nice-to-have
- 1-2: Can skip

### Confidence (Will it work?)
- 10: Proven tech, low risk
- 8-9: Proven tech, simple integration
- 6-7: Proven tech, moderate complexity
- 4-5: New or unproven tech
- 1-3: High technical risk

### Ease (How hard to build?)
- 10: <1 hour
- 8-9: <4 hours
- 6-7: <1 day (4-8 hours)
- 4-5: 1-2 days
- 1-3: >2 days (complex)

### Decision Rules

> **Canonical Source**: [orchestrator-thresholds.md](../../../00-core/orchestrator-thresholds.md#ice-score-thresholds)

- **ICE ≥ 500:** Build Phase 1 (high priority)
- **ICE 300-499:** Build Phase 1-2 (medium priority)
- **ICE 200-299:** Build Phase 2+ (lower priority)
- **ICE < 200:** Defer to backlog (P1/P2)

---

**END ROADMAP**

This roadmap is your execution plan. Check it weekly. Update features as you progress.
