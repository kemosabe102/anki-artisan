# ICE Scoring Guide

**Purpose**: Examples and guidance for calculating ICE scores in roadmap planning.

**Canonical Thresholds**: [orchestrator-thresholds.md](../../../00-core/orchestrator-thresholds.md#ice-score-thresholds)

---

## Formula

```
ICE Score = Impact × Confidence × Ease
```

Each factor scored 1-10, yielding a total score of 1-1000.

---

## Factor Definitions

| Factor | Question | Low (1-3) | Medium (4-6) | High (7-10) |
|--------|----------|-----------|--------------|-------------|
| **Impact** | How much does this move the needle? | Nice to have | Supports core value | Core differentiator |
| **Confidence** | How confident are we it will work? | Unknown tech, first attempt | Some precedent | Proven patterns |
| **Ease** | How easy is it to build? | Multiple unknowns, complex integration | Moderate complexity | Well-understood scope |

---

## Calculation Examples

| Feature | Impact | Confidence | Ease | ICE | Priority |
|---------|--------|------------|------|-----|----------|
| Decision Logging | 10 (foundation) | 9 (simple form) | 7 (form+API+DB) | 630 | Build 1st |
| Decision Search | 9 (core value) | 8 (proven tech) | 8 (built-in FTS) | 576 | Build 2nd |
| PDF Export | 8 (nice to have) | 7 (pdfkit stable) | 6 (pagination) | 336 | Phase 2 |
| Pattern Detection | 9 (differentiator) | 5 (AI complexity) | 4 (unknown scope) | 180 | Backlog |

### Rationale by Example

**Decision Logging (ICE: 630)**
- Impact 10: Foundation for entire system - nothing works without it
- Confidence 9: Simple CRUD form, well-understood pattern
- Ease 7: Requires form + API + database schema, but straightforward
- Priority: Phase 1, build first

**Pattern Detection (ICE: 180)**
- Impact 9: Would be a major differentiator if successful
- Confidence 5: AI/ML complexity, uncertain outcomes
- Ease 4: Unknown scope, potential rabbit holes
- Priority: Backlog - high risk, defer until foundation stable

---

## Phase Assignment

| ICE Score | Phase | Rationale |
|-----------|-------|-----------|
| >= 500 | Phase 1 | High value, high confidence - schedule immediately |
| 300-499 | Phase 1-2 | Moderate value - plan for current or next sprint |
| 200-299 | Phase 2+ | Lower priority - plan for future |
| < 200 | Backlog | Too risky or too little value - defer, require user confirmation |

---

## Common Scoring Pitfalls

1. **Impact inflation**: "Everything is critical" - use relative comparison within project scope
2. **Confidence optimism**: First-time tech should rarely exceed 6
3. **Ease underestimation**: Include testing, documentation, integration time
4. **Score manipulation**: Don't adjust scores to get desired phase - trust the formula

---

## When to Re-Score

- After prototype reveals unexpected complexity (adjust Ease)
- After research reduces uncertainty (adjust Confidence)
- After scope changes affect feature importance (adjust Impact)
- During phase transitions - validate ICE still reflects reality
