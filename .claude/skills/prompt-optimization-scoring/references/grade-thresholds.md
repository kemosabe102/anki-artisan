# Grade Thresholds and Calculation

> **Overall grade formula, thresholds, and priority calculation for prompt optimization scoring**

---

## Overall Grade Calculation

### Weighted Score Formula

```
overall_score = (F1 x 0.20) + (F2 x 0.25) + (F3 x 0.15) + 
                (F4 x 0.10) + (F5 x 0.10) + (F6 x 0.10) + (F7 x 0.10)
```

### Framework Weights Summary

| Framework | Weight | Name |
|-----------|--------|------|
| F1 | 0.20 | Structural Quality |
| F2 | 0.25 | Anthropic Prompt Engineering |
| F3 | 0.15 | Token Optimization |
| F4 | 0.10 | Testing & Validation |
| F5 | 0.10 | Progressive Disclosure |
| F6 | 0.10 | Token Density |
| F7 | 0.10 | Framework Alignment |
| **Total** | **1.00** | |

---

## Grade Thresholds

### Primary Letter Grade Scale

| Grade | Score Range | Description |
|-------|-------------|-------------|
| A+ | >= 4.75 | Exceptional - Industry leading |
| A | 4.50 - 4.74 | Excellent - Follows all best practices |
| A- | 4.25 - 4.49 | Very Good - Minor improvements possible |
| B+ | 4.00 - 4.24 | Good - Solid implementation |
| B | 3.75 - 3.99 | Above Average - Some gaps |
| B- | 3.50 - 3.74 | Satisfactory - Notable gaps |
| C+ | 3.25 - 3.49 | Acceptable - Improvements needed |
| C | 3.00 - 3.24 | Average - Several gaps |
| C- | 2.75 - 2.99 | Below Average - Significant issues |
| D+ | 2.50 - 2.74 | Poor - Many issues |
| D | 2.25 - 2.49 | Very Poor - Major issues |
| D- | 2.00 - 2.24 | Failing threshold |
| F | < 2.00 | Failing - Major redesign needed |

### Simplified Scale (for quick assessment)

| Grade | Score Range | Action Required |
|-------|-------------|-----------------|
| A | >= 4.5 | Production ready |
| B | 3.5 - 4.49 | Minor fixes then deploy |
| C | 2.5 - 3.49 | Significant work needed |
| D | 1.5 - 2.49 | Major rework required |
| F | < 1.5 | Full redesign needed |

---

## Score Normalization

### Converting Framework Scores to 0-5 Scale

**Pass/Fail Frameworks (F1)**:
```
normalized = (pass_count / total_criteria) * 5
```

**Letter Grade Frameworks (F2, F5, F6, F7)**:
| Letter | Numeric |
|--------|---------|
| A | 5.0 |
| B | 4.0 |
| C | 3.0 |
| D | 2.0 |
| F | 1.0 |

**Quantitative Frameworks (F3, F4)**:
- Use calculated 0-5 score from methodology

---

## Priority Calculation for Recommendations

### Priority Score Formula

```
Priority = (Impact x 0.4) + (Effort_Inverse x 0.3) + (Risk_Reduction x 0.3)
```

### Impact Scoring (0.0 - 1.0)

| Level | Score | Examples |
|-------|-------|----------|
| Critical | 1.0 | Schema non-compliance, security gaps, missing testing for high-risk |
| Major | 0.6 | Tool ambiguity, token bloat >500, missing error recovery |
| Minor | 0.3 | Inconsistent XML, missing examples, suboptimal compression |

### Effort Inverse Scoring (0.0 - 1.0)

| Effort | Score | Time | Examples |
|--------|-------|------|----------|
| Low | 1.0 | <30 min | Reference docs, add schema section, remove filler words |
| Medium | 0.5 | 1-3 hrs | Restructure workflow, add examples, externalize framework |
| High | 0.2 | >3 hrs | Full redesign, new testing framework, multi-file refactor |


### Risk Scoring (0.0 - 1.0)

| Level | Score | Tools | Examples |
|-------|-------|-------|----------|
| High | 1.0 | Write + Bash + External APIs | development, deployment-release |
| Medium | 0.5 | Edit OR single heavy tool | claude-code-ecosystem, debugger |
| Low | 0.2 | Read-only operations | claude-code-ecosystem, researcher-codebase |

### Priority Interpretation

| Score | Classification | Timeline |
|-------|----------------|----------|
| > 0.7 | Immediate | Fix within current sprint |
| 0.4 - 0.7 | Short-term | Next maintenance cycle |
| < 0.4 | Long-term | Backlog for future improvement |

---

## Confidence Scoring

### Per-Dimension Formula

```
Confidence = Data_Completeness x Evidence_Quality x Methodology_Soundness
```

| Factor | 1.0 | 0.75 | 0.5 | 0.25 |
|--------|-----|------|-----|------|
| Data Completeness | All required | Minor gaps | Significant gaps | Critical gaps |
| Evidence Quality | Direct citations | Strong indicators | Weak indicators | No evidence |
| Methodology | Established | Adapted | Novel | Ad-hoc |

### Overall Confidence

```
Overall = Sum(Dimension_Confidence x Dimension_Weight) / Sum(Weights)
```


**Dimension Weights for Confidence**:
| Dimension | Weight |
|-----------|--------|
| Structural | 0.25 |
| Prompt Engineering | 0.20 |
| Token Optimization | 0.20 |
| Testing | 0.15 |
| Progressive Disclosure | 0.10 |
| Token Density | 0.10 |

---

## Validation & Accuracy

| Metric | Accuracy | Notes |
|--------|----------|-------|
| Token counts | +/- 10% | tiktoken-based |
| Effort estimates | +/- 50% | Inherent uncertainty |
| Priority scores | +/- 0.1 | Input sensitivity |
| Confidence scores | +/- 0.15 | Subjective components |

---

## References

- **Source**: `.claude/agents/claude-code/claude-code-ecosystem/docs/optimization-calculations.md`
- **Source**: `.claude/agents/claude-code/claude-code-ecosystem/phases/phase-3-decide.md`
