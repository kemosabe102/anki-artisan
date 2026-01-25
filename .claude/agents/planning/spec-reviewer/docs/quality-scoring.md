# Quality Scoring Framework

**Purpose**: Dimension breakdowns for SPEC quality assessment

---

## Completeness Score (0-1.0)

| Component | Weight | Criteria |
|-----------|--------|----------|
| Functional requirements | 0.30 | All FR-XXX present and clear |
| Non-functional requirements | 0.20 | NFR specs with measurable targets |
| Acceptance scenarios | 0.20 | Clear pass/fail criteria |
| Planning Recommendations | 0.15 | Section present (from /spec command) |
| Technical architecture | 0.15 | Component breakdown defined |

---

## Testability Score (0-1.0)

| Component | Weight | Criteria |
|-----------|--------|----------|
| Measurable criteria | 0.40 | Requirements have quantifiable metrics |
| Verifiable scenarios | 0.30 | Acceptance tests can be automated |
| Quantifiable success | 0.30 | Success metrics are numeric/observable |

---

## Clarity Score (0-1.0)

| Component | Weight | Criteria |
|-----------|--------|----------|
| Unambiguous language | 0.40 | No vague terms (see Ambiguity Index) |
| Defined terms | 0.30 | Technical terms explained |
| Consistent references | 0.30 | Internal links valid, terminology consistent |

---

## Ambiguity Index (0-10)

| Score | Rating | Description |
|-------|--------|-------------|
| 0-2 | Excellent | Clear, precise language throughout |
| 3-5 | Acceptable | Minor ambiguities, easily resolved |
| 6-8 | Significant | Multiple unclear requirements |
| 9-10 | Critical | Pervasive ambiguity, needs rewrite |

**Vague Terms to Flag**: "improve", "enhance", "optimize", "better", "faster", "more efficient", "user-friendly", "seamless", "robust"

---

## Progressive Disclosure Score (0-1.0)

| Component | Weight | Criteria |
|-----------|--------|----------|
| Visibility | 0.25 | Core requirements in main overview |
| Structure | 0.25 | Proper hierarchy (Overview -> Core -> Details) |
| Size | 0.20 | Main SPEC <500 lines |
| Scent | 0.15 | Descriptive headings, preview hints |
| Depth | 0.15 | Maximum 2 disclosure levels |

---

## Overall Grade Calculation

```
Overall_Score = (Completeness × 0.25) + (Testability × 0.25) + 
                (Clarity × 0.25) + ((10 - Ambiguity) / 10 × 0.15) + 
                (Progressive_Disclosure × 0.10)

Grade Mapping:
  A: 0.90 - 1.00  (Excellent - ready for implementation)
  B: 0.80 - 0.89  (Good - minor improvements recommended)
  C: 0.70 - 0.79  (Acceptable - several issues to address)
  D: 0.60 - 0.69  (Poor - significant rework needed)
  F: < 0.60       (Failing - major rewrite required)
```

---

## Quick Reference Checklist

- [ ] All FR-XXX requirements present?
- [ ] NFRs have measurable targets?
- [ ] Acceptance scenarios verifiable?
- [ ] No vague terms used?
- [ ] Technical terms defined?
- [ ] Cross-references consistent?
- [ ] SPEC < 500 lines?
- [ ] Proper heading hierarchy?
