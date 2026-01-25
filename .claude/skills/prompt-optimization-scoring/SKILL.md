---
name: prompt-optimization-scoring
description: >
  7-framework weighted scoring for prompt optimization. Use when grading prompt
  quality, calculating optimization scores, or generating improvement recommendations.
  Trigger keywords: prompt score, optimization, grading, A-F grade, token optimization.
---

# Prompt Optimization Scoring

> **7-framework weighted scoring system for evaluating and optimizing prompt quality.**

---

## When to Use This Skill

**Trigger Keywords**: "prompt score", "optimization", "grading", "A-F grade", "token optimization", "prompt quality score", "evaluation score"

**Use For**:
- Calculating overall prompt quality scores (A+ through F)
- Generating prioritized improvement recommendations
- Token optimization opportunity analysis
- Comparing prompt versions quantitatively

**NOT For**:
- Structural validation only (use `prompt-structural-analysis`)
- Creating/modifying agents (use claude-code-ecosystem)
- Full evaluation workflow (use claude-code-ecosystem agent)

---

## Core Methodology

### 7-Framework Evaluation System

Each framework assesses a different dimension of prompt quality:

| Framework | Weight | Assessment Type | Output |
|-----------|--------|-----------------|--------|
| F1: Structural Quality | 0.20 | 17-criteria pass/fail | X/17 score |
| F2: Anthropic Prompt Engineering | 0.25 | 9 weighted principles | A-F grade |
| F3: Token Optimization | 0.15 | Quantitative analysis | Savings % |
| F4: Testing Strategy | 0.10 | Risk-based match | Gap analysis |
| F5: Progressive Disclosure | 0.10 | 4-factor analysis | A-F grade |
| F6: Token Density | 0.10 | 6-metric analysis | A-F grade |
| F7: Framework Alignment | 0.10 | Phase-aware evaluation | A-F grade |

**Total Weight**: 1.00

---

## Weighted Scoring Formula

### Overall Grade Calculation

```
overall_score = (F1 x 0.20) + (F2 x 0.25) + (F3 x 0.15) + 
                (F4 x 0.10) + (F5 x 0.10) + (F6 x 0.10) + (F7 x 0.10)
```

### Score Normalization

All framework scores must be normalized to 0-5 scale before weighting:

| Framework Type | Normalization |
|----------------|---------------|
| Pass/Fail (F1) | `(pass_count / total_criteria) * 5` |
| Letter Grade (F2, F5, F6, F7) | A=5, B=4, C=3, D=2, F=1 |
| Quantitative (F3, F4) | Direct 0-5 calculation |


---

## Grade Thresholds

### Letter Grade Mapping

| Grade | Score Range | Status |
|-------|-------------|--------|
| A+ | >= 4.75 | Exceptional |
| A | 4.50 - 4.74 | Excellent - Production ready |
| A- | 4.25 - 4.49 | Very Good |
| B+ | 4.00 - 4.24 | Good |
| B | 3.75 - 3.99 | Above Average |
| B- | 3.50 - 3.74 | Satisfactory |
| C+ | 3.25 - 3.49 | Acceptable |
| C | 3.00 - 3.24 | Average |
| C- | 2.75 - 2.99 | Below Average |
| D+ | 2.50 - 2.74 | Poor |
| D | 2.25 - 2.49 | Very Poor |
| D- | 2.00 - 2.24 | Failing threshold |
| F | < 2.00 | Failing - Redesign needed |

### Action Thresholds

| Grade | Action Required |
|-------|-----------------|
| A (>= 4.5) | Production ready |
| B (3.5-4.49) | Minor fixes then deploy |
| C (2.5-3.49) | Significant work needed |
| D (1.5-2.49) | Major rework required |
| F (< 1.5) | Full redesign needed |

---

## Priority Calculation for Recommendations

### Priority Score Formula

```
Priority = (Impact x 0.4) + (Effort_Inverse x 0.3) + (Risk_Reduction x 0.3)
```

### Component Scoring

**Impact (0.0-1.0)**:
| Level | Score | Examples |
|-------|-------|----------|
| Critical | 1.0 | Schema non-compliance, security gaps |
| Major | 0.6 | Token bloat >500, missing error recovery |
| Minor | 0.3 | Inconsistent XML, missing examples |

**Effort Inverse (0.0-1.0)**:
| Effort | Score | Time |
|--------|-------|------|
| Low | 1.0 | <30 min |
| Medium | 0.5 | 1-3 hrs |
| High | 0.2 | >3 hrs |

**Risk (0.0-1.0)**:
| Level | Score | Tools |
|-------|-------|-------|
| High | 1.0 | Write + Bash + External APIs |
| Medium | 0.5 | Edit OR single heavy tool |
| Low | 0.2 | Read-only operations |

### Priority Classification

| Score | Classification | Timeline |
|-------|----------------|----------|
| > 0.7 | Immediate | Fix within current sprint |
| 0.4 - 0.7 | Short-term | Next maintenance cycle |
| < 0.4 | Long-term | Backlog for future |


---

## Framework Summaries

### F1: Structural Quality (Weight: 0.20)

17 criteria evaluating agent architecture and design patterns.

**Categories**:
- Single Responsibility & Boundaries (3 criteria)
- Schema & Pattern Compliance (4 criteria)
- Tool & Workflow Architecture (3 criteria)
- Communication Quality (3 criteria)
- Integration Patterns (4 criteria)

**Cross-reference**: `prompt-structural-analysis` skill for detailed criteria.

### F2: Anthropic Prompt Engineering (Weight: 0.25)

9 principles with weighted scoring:

| Principle | Weight |
|-----------|--------|
| Role Assignment | 1.2x |
| Clarity & Directness | 1.3x |
| Data-Instruction Separation | 1.1x |
| Output Formatting | 1.0x |
| Step-by-Step Thinking | 1.2x |
| Example Usage | 1.0x |
| Hallucination Prevention | 1.1x |
| XML Tag Structure | 0.9x |
| Layered Complexity | 1.0x |

**Calculation**: `Weighted_Average = Sum(Score x Weight) / Sum(Weights)`


### F3: Token Optimization (Weight: 0.15)

Quantitative analysis of token savings opportunities:

| Technique | Savings | Effort |
|-----------|---------|--------|
| Base pattern inheritance | ~1,150 tokens | Low |
| Documentation references | 100-300/section | Low |
| Compression (10:1) | Variable | Medium |
| Tool description optimization | 50-150 tokens | Low |
| Example consolidation | 100-500 tokens | Low |

**Formula**: `Optimization_% = (Potential_Savings / Current_Tokens) x 100`

### F4: Testing Strategy (Weight: 0.10)

Risk-based testing strategy match:

| Risk Level | Required Testing |
|------------|------------------|
| CRITICAL | Schema + Regression + Adversarial + CI/CD |
| HIGH | Schema + Regression + Quality Matrix |
| MEDIUM | Schema + Quality Matrix + LLM-as-judge |
| LOW | Quality Matrix + Schema + Spot checks |

### F5: Progressive Disclosure (Weight: 0.10)

4-factor analysis:
- **Semantic Description** (0.25): <200 chars, keyword-rich
- **Hierarchical Structure** (0.30): 5 sections in order
- **Size Compliance** (0.25): <500 lines
- **Context Efficiency** (0.20): External refs, no bloat

**Size Formula**: `Size_Score = max(0.0, 1.0 - ((Line_Count - 500) / 500))`


### F6: Token Density (Weight: 0.10)

6-metric analysis:

| Dimension | Weight | Target |
|-----------|--------|--------|
| Filler Word Density | 0.15 | <5% |
| Active Voice Ratio | 0.20 | >80% |
| Structured Data Usage | 0.15 | Lists > Prose |
| XML Tag Efficiency | 0.15 | >30% savings |
| Example Efficiency | 0.20 | <=3 examples, <20% tokens |
| Reference Inheritance | 0.15 | >60% reuse |

### F7: Framework Alignment (Weight: 0.10)

Domain-framework matching:

| Agent Category | Expected Framework |
|----------------|-------------------|
| Research | ReACT |
| Implementation | CAGEERF |
| Analysis/Review | ReACT + DMAIC |
| Planning | CAGEERF or OKR |
| Debugging | ReACT + 5 Whys |
| Optimization | SCAMPER + DMAIC |

**Integration Depth**: `phases_with_framework / total_phases`

---

## Scoring Workflow

### Step 1: Collect Framework Scores
1. Run structural validation (F1) - get X/17
2. Apply prompt engineering principles (F2) - get weighted average
3. Calculate token optimization potential (F3) - get savings %
4. Assess testing strategy match (F4) - get gap score
5. Evaluate progressive disclosure (F5) - get PD score
6. Analyze token density (F6) - get TD score
7. Check framework alignment (F7) - get integration depth


### Step 2: Normalize Scores
Convert all scores to 0-5 scale using normalization rules.

### Step 3: Calculate Overall Score
Apply weighted formula:
```
overall = (F1_norm x 0.20) + (F2_norm x 0.25) + (F3_norm x 0.15) + 
          (F4_norm x 0.10) + (F5_norm x 0.10) + (F6_norm x 0.10) + (F7_norm x 0.10)
```

### Step 4: Map to Grade
Use grade thresholds to convert numeric score to letter grade.

### Step 5: Generate Recommendations
1. Identify gaps (scores below 4.0)
2. Calculate priority for each improvement
3. Sort by priority descending
4. Classify as Immediate/Short-term/Long-term

---

## Output Format

### Score Report Structure

```json
{
  "overall_score": 3.85,
  "overall_grade": "B",
  "framework_scores": {
    "F1_structural": {"raw": "14/17", "normalized": 4.12},
    "F2_prompt_engineering": {"raw": "B+", "normalized": 4.25},
    "F3_token_optimization": {"raw": "22%", "normalized": 3.50},
    "F4_testing_strategy": {"raw": "gaps: 2", "normalized": 3.00},
    "F5_progressive_disclosure": {"raw": "B", "normalized": 4.00},
    "F6_token_density": {"raw": "B-", "normalized": 3.50},
    "F7_framework_alignment": {"raw": "C+", "normalized": 3.25}
  },
  "recommendations": [
    {"priority": 0.82, "classification": "immediate", "issue": "...", "fix": "..."},
    {"priority": 0.65, "classification": "short-term", "issue": "...", "fix": "..."}
  ],
  "confidence": 0.85
}
```


### Markdown Report Template

```markdown
## Prompt Quality Score: {agent_name}

**Overall Grade**: {grade} ({score}/5.0)
**Confidence**: {confidence}

### Framework Breakdown

| Framework | Raw Score | Normalized | Weight |
|-----------|-----------|------------|--------|
| F1: Structural | {raw} | {norm}/5 | 0.20 |
| F2: Prompt Engineering | {raw} | {norm}/5 | 0.25 |
| F3: Token Optimization | {raw} | {norm}/5 | 0.15 |
| F4: Testing Strategy | {raw} | {norm}/5 | 0.10 |
| F5: Progressive Disclosure | {raw} | {norm}/5 | 0.10 |
| F6: Token Density | {raw} | {norm}/5 | 0.10 |
| F7: Framework Alignment | {raw} | {norm}/5 | 0.10 |

### Prioritized Recommendations

| Priority | Classification | Issue | Fix |
|----------|----------------|-------|-----|
| 0.82 | Immediate | ... | ... |
| 0.65 | Short-term | ... | ... |
```

---

## References

- **Framework Rubrics**: [references/framework-rubrics.md](references/framework-rubrics.md)
- **Grade Thresholds**: [references/grade-thresholds.md](references/grade-thresholds.md)
- **Related Skill**: `prompt-structural-analysis` for structural validation
- **Source Agent**: `.claude/agents/claude-code/claude-code-ecosystem/`
