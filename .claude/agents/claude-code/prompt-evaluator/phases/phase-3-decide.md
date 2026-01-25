# Phase 3: DECIDE - Score Normalization & Grade Calculation

**OODA Stage**: DECIDE | **Time Allocation**: 10-15%

**Purpose**: Normalize framework scores, calculate overall grade, prioritize recommendations

**Deliverable**: Normalized scores, overall grade A-F, prioritized recommendation list

---

## Workflow Steps

### Step 3.1: Score Normalization

**Input**: Raw scores from all 7 frameworks (Phase 2)

**Process**:
1. **Pass/Fail frameworks (F1 Structural)**:
   - `normalized_score = pass_count / 16 * 5`
2. **Letter grade frameworks (F2, F5, F6, F7)**:
   - A=5, B=4, C=3, D=2, F=1
3. **Quantitative frameworks (F3 Token, F4 Testing)**:
   - Use 0-5 scale from methodology in docs/evaluation-frameworks.md

**Output**: Array of 7 normalized scores (0-5 scale each)


### Step 3.2: Overall Grade Calculation

**Input**: 7 normalized scores

**Process**:
1. Apply weights:
   ```
   overall_score = (F1 x 0.20) + (F2 x 0.25) + (F3 x 0.15) + 
                   (F4 x 0.10) + (F5 x 0.10) + (F6 x 0.10) + (F7 x 0.10)
   ```
2. Map to letter grade:
   - A: >= 4.5
   - B: 3.5 - 4.49
   - C: 2.5 - 3.49
   - D: 1.5 - 2.49
   - F: < 1.5

**Output**: `overall_grade` (A-F) with `overall_score` (0-5)

### Step 3.3: Recommendation Priority Scoring

**Input**: All findings, anti-patterns, token opportunities

**Process**:
1. For each recommendation, calculate priority score:
   ```
   priority = (impact x 0.4) + (effort_inverse x 0.3) + (risk_reduction x 0.3)
   ```
2. Classify by score:
   - >0.7: Immediate (fix this sprint)
   - 0.4-0.7: Short-term (next maintenance cycle)
   - <0.4: Long-term (backlog)
3. Sort recommendations by priority descending

**Output**: Prioritized recommendation list with scores and classifications


### Step 3.4: Confidence Assessment

**Input**: Pre-flight results, framework completion status

**Process**:
1. Check for incomplete dimensions (frameworks that couldn't run)
2. Check for reduced-confidence baselines (heuristic token counts)
3. Calculate overall confidence:
   ```
   confidence = (complete_frameworks / 7) x baseline_confidence
   ```

**Output**: `overall_confidence` (0.0-1.0), `incomplete_dimensions` list

---

## Quick Checklist

Before advancing to Phase 4 (ACT):

- [ ] All framework scores normalized to 0-5 scale
- [ ] Overall grade calculated using weight formula
- [ ] Letter grade mapped from overall score
- [ ] Recommendations prioritized with scores
- [ ] Confidence score reflects any gaps

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Raw score aggregation | Normalize all scores to 0-5 before weighting |
| Missing weight application | Always apply formula weights (0.20, 0.25, etc.) |
| Unprioritized recommendations | Calculate priority score for every finding |
| Ignoring incomplete frameworks | Document in incomplete_dimensions, reduce confidence |

---

**Previous Phase**: [Phase 2: ORIENT](phase-2-orient.md)
**Next Phase**: [Phase 4: ACT](phase-4-act.md)
