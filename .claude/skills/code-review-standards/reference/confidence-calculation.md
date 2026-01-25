# Confidence Calculation Reference

## Formula

```
Confidence = (Evidence_Strength × 0.40) + (Pattern_Match × 0.30) + (Context_Clarity × 0.30)
```

---

## Component Definitions

### Evidence Strength (0.0-1.0)
How directly observable is the issue?

| Score | Criteria |
|-------|----------|
| 1.0 | Direct observation (test failure, crash log) |
| 0.8 | Strong inference (type mismatch, null dereference) |
| 0.6 | Pattern match (code smell, anti-pattern) |
| 0.4 | Weak inference (style issue, naming) |
| 0.2 | Speculation (might cause issues) |

### Pattern Match (0.0-1.0)
How well does this match known issue patterns?

| Score | Criteria |
|-------|----------|
| 1.0 | Exact match to documented vulnerability |
| 0.8 | Strong match to common bug pattern |
| 0.6 | Partial match, some conditions met |
| 0.4 | Weak match, many conditions missing |
| 0.2 | No known pattern, novel issue |

### Context Clarity (0.0-1.0)
How clear is the surrounding code context?

| Score | Criteria |
|-------|----------|
| 1.0 | Full understanding of module purpose and dependencies |
| 0.8 | Good understanding, minor unknowns |
| 0.6 | Partial understanding, some dependencies unclear |
| 0.4 | Limited understanding, significant unknowns |
| 0.2 | Minimal context, unfamiliar codebase |

---

## Post-Validation Adjustments

After initial calculation, apply adjustments:

| Validation | Adjustment |
|------------|------------|
| Context7 confirms pattern | +0.10 |
| Context7 contradicts pattern | -0.15 |
| Recent similar bug found | +0.10 |
| Author confirms intent | +0.15 / -0.20 |
| Static analysis confirms | +0.10 |

---

## Example Calculation

**Finding**: Potential SQL injection in query builder

```
Evidence_Strength: 0.8 (string concatenation visible)
Pattern_Match: 0.9 (classic SQL injection pattern)
Context_Clarity: 0.7 (query builder module, user input unclear)

Confidence = (0.8 × 0.40) + (0.9 × 0.30) + (0.7 × 0.30)
           = 0.32 + 0.27 + 0.21
           = 0.80

Post-validation: Context7 confirms parameterized queries required
Adjusted: 0.80 + 0.10 = 0.90

Final Confidence: 0.90 → CRITICAL severity eligible
```
