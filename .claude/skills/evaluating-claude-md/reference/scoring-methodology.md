# Scoring Methodology

How to apply scoring rubrics consistently across evaluations.

---

## Scoring Principles

### 1. Binary Scoring (Most Criteria)

Most D1-D7 criteria are binary (all-or-nothing):

- **Met (full points)**: Criterion fully satisfied with evidence
- **Not Met (0 points)**: Criterion not satisfied or partially satisfied

**Rationale**: Binary scoring ensures consistency and prevents score inflation.

### 2. Variable-Weight Criteria

Some criteria have higher weight (3 pts) due to importance:

| Dimension | Criterion | Points | Why Higher Weight |
|-----------|-----------|--------|-------------------|
| D2 | One-Read Rule | 4 | Core orchestrator efficiency |
| D2 | Token Budget Strategy | 3 | Context preservation critical |
| D2 | Anti-patterns Listed | 3 | Prevents common failures |
| D5 | Code Truth | 3 | Core quality principle |
| D5 | Code Snippets | 3 | Prevents hallucination |
| D6 | Successfully Tested | 3 | Practical validation critical |

### 3. Evidence Documentation

For every criterion, evaluators must:

1. **Quote evidence**: Extract exact text from CLAUDE.md
2. **Cite location**: Section name or line reference
3. **Justify score**: Brief explanation of why met/not met

**Template**:
```
Criterion: [name]
Score: [X/Y]
Evidence: "[quoted text]" (Section: [name])
Justification: [why this evidence supports the score]
```

---

## Edge Cases

### Implicit vs Explicit

- **Explicit always wins**: If criterion requires explicit statement, implicit compliance = 0 pts
- **Example**: "Read-only coordinator" must be stated explicitly

### Synonyms and Variants

Accept reasonable synonyms for key concepts:

| Concept | Acceptable Variants |
|---------|---------------------|
| "Read-only coordinator" | "Read-only orchestrator", "Project coordinator (never worker)" |
| "One-Read Rule" | "Single strategic read", "One multi-file read" |

### Absence of Evidence

When searching for content that may not exist:

1. Search for multiple keyword variants
2. Check all relevant sections
3. Only score 0 if exhaustive search fails
4. Document search terms used

---

## Aggregation Rules

### Dimension Score

```
dimension_score = SUM(criterion_points_awarded)
```

### Overall Score

```
overall_score = SUM(all_dimension_scores)
```

### Health Status Mapping

| Overall Score | Grade | Health Status |
|---------------|-------|---------------|
| 63-70 | A | Excellent |
| 56-62 | B | Good |
| 49-55 | C | Needs Attention |
| 42-48 | D | Poor |
| <42 | F | Critical |

### Dimension Status

| Dimension Score | Status |
|-----------------|--------|
| 8-10 | Pass (✅) |
| 5-7 | Warning (⚠️) |
| 0-4 | Fail (❌) |

---

## Quality Assurance

### Before Scoring

1. CLAUDE.md is complete (not truncated)
2. All sections are readable
3. Evaluator has access to reference docs

### After Scoring

1. All criteria have evidence (no empty justifications)
2. Scores match rubric thresholds exactly
3. Findings align with recommendations
4. Total score equals sum of criterion scores
