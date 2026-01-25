---
name: code-review-standards
description: >
  Use this skill when reviewing code for quality, security, and maintainability.
  Provides confidence scoring formulas, blast radius analysis, severity classification,
  and finding validation gates. Trigger keywords: code review, review, confidence,
  blast radius, severity, finding, security review, quality check.
---

# Code Review Standards Skill

Systematic code review with confidence-scored findings and blast radius prioritization.

## Reference Documentation

- **Confidence Calculation** -> [reference/confidence-calculation.md](reference/confidence-calculation.md)
- **Blast Radius Analysis** -> [reference/blast-radius-analysis.md](reference/blast-radius-analysis.md)
- **Severity Classification** -> [reference/severity-classification.md](reference/severity-classification.md)
- **Merge Readiness Checklist** -> [reference/merge-readiness-checklist.md](reference/merge-readiness-checklist.md)

---

## Templates

**Finding Template**: [templates/finding-template.md](templates/finding-template.md)

Use this template for documenting code review findings with:
- Severity and confidence scores
- Evidence and risk assessment
- Blast radius calculation
- Gate verification checklist

---

## Quick Reference: Confidence Formula

```
Confidence = (Evidence_Strength × 0.40) + (Pattern_Match × 0.30) + (Context_Clarity × 0.30)
```

| Score Range | Action |
|-------------|--------|
| 0.90-1.0 | Report finding with high confidence |
| 0.70-0.89 | Report with explanatory notes |
| 0.50-0.69 | Research before reporting |
| < 0.50 | Do not report, investigate further |

---

## Quick Reference: Blast Radius

```
Blast_Radius = (Afferent_Coupling × 0.50) + (Change_Frequency × 0.25) + (Business_Criticality × 0.25)
```

| Afferent (Importers) | Priority | Review Depth |
|---------------------|----------|--------------|
| 10+ files | CRITICAL | Full coverage |
| 5-9 files | HIGH | Standard review |
| 2-4 files | MEDIUM | Major issues only |
| 0-1 files | LOW | Critical issues only |

---

## 5 Finding Gates

Before reporting ANY finding, verify:

| Gate | Question | HALT if NO |
|------|----------|------------|
| 1. Invariant | Does it violate a type/contract? | Skip finding |
| 2. Intent | Does behavior contradict intent? | Skip finding |
| 3. Failure Path | Is there a concrete failure scenario? | Skip finding |
| 4. Pattern Match | Does it match known unsafe pattern? | Research first |
| 5. Stack Alignment | Is it inconsistent with SPEC.md? | Verify with user |

---

## Severity Decision Tree

```
Confidence >= 0.90 AND (security_risk OR data_integrity_risk)?
  → CRITICAL (max 3 per review)

Confidence >= 0.90 OR (Confidence >= 0.70 AND public_api)?
  → MAJOR (max 5 per review)

Confidence 0.70-0.89 AND internal_code?
  → MINOR (max 5 per review)

Style/naming only?
  → NIT (max 2 per review)
```

---

## Rate Limits

| Severity | Max Per Review |
|----------|----------------|
| CRITICAL | 3 |
| MAJOR | 5 |
| MINOR | 5 |
| NIT | 2 |

**Total**: 15 findings maximum per review session.
