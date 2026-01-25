# Framework Rubrics for Prompt Optimization Scoring

> **Detailed scoring criteria for each of the 7 evaluation frameworks**

---

## Framework 1: Structural Quality (Weight: 0.20)

**Assessment Type**: Pass/Fail | **Output**: X/17 score

### Scoring Conversion
```
normalized_score = (pass_count / 17) * 5
```

### Criteria Reference
Structural criteria are evaluated in `prompt-structural-analysis` skill.
Reference: `.claude/skills/prompt-structural-analysis/SKILL.md`

---

## Framework 2: Anthropic Prompt Engineering (Weight: 0.25)

**Assessment Type**: Weighted 0-5 scale | **Output**: A-F grade

### 9 Principles with Weights

| Principle | Weight | Description |
|-----------|--------|-------------|
| Role Assignment | 1.2x | Clear agent identity and purpose |
| Clarity & Directness | 1.3x | Unambiguous instructions |
| Data-Instruction Separation | 1.1x | Context vs directives |
| Output Formatting | 1.0x | Structured JSON, XML tags |
| Step-by-Step Thinking | 1.2x | Reasoning approach documented |
| Example Usage | 1.0x | Few-shot demonstrations |
| Hallucination Prevention | 1.1x | Fact-checking, confidence scoring |
| XML Tag Structure | 0.9x | Consistent section hierarchy |
| Layered Complexity | 1.0x | Progressive detail levels |

### Scoring Scale (per principle)

| Score | Criteria |
|-------|----------|
| 5 | Excellent - Comprehensive implementation |
| 4 | Good - Clear with minor gaps |
| 3 | Acceptable - Basic implementation |
| 2 | Poor - Significant gaps |
| 1 | Failing - Major issues |
| 0 | Missing - Not implemented |

### Calculation Formula
```
Weighted_Average = Sum(Score x Weight) / Sum(Weights)
Letter_Grade = Map(Weighted_Average, Grade_Scale)
```

---

## Framework 3: Token Optimization (Weight: 0.15)

**Assessment Type**: Quantitative | **Output**: Savings percentage

### Optimization Techniques

| Technique | Potential Savings | Effort |
|-----------|------------------|--------|
| Base pattern inheritance | ~1,150 tokens | Low |
| Documentation references | 100-300/section | Low |
| Compression (10:1 ratio) | Variable | Medium |
| Tool description optimization | 50-150 tokens | Low |
| Example consolidation | 100-500 tokens | Low |
| Workflow compression | 200-400 tokens | Low |
| Redundant section removal | 100-300/section | Low |

### Scoring Formula
```
Optimization_Potential = Sum(Applicable_Technique_Savings)
Optimization_Score = min(5.0, Optimization_Potential / Current_Tokens * 20)
```


---

## Framework 4: Testing & Validation (Weight: 0.10)

**Assessment Type**: Risk-based strategy match | **Output**: Gap analysis

### Risk Level Classification

| Level | Score | Tools Present | Testing Required |
|-------|-------|---------------|------------------|
| CRITICAL | 1.0 | Write + Bash + External APIs | Schema + Regression + Adversarial + CI/CD |
| HIGH | 0.75 | Write OR Bash OR External APIs | Schema + Regression + Quality Matrix |
| MEDIUM | 0.5 | Edit + Read + Complex logic | Schema + Quality Matrix + LLM-as-judge |
| LOW | 0.25 | Read-only operations | Quality Matrix + Schema + Spot checks |

### Scoring Formula
```
Test_Gap_Score = Current_Coverage_Meets_Risk_Level ? 5 : (Current_Coverage / Required_Coverage) * 5
```

---

## Framework 5: Progressive Disclosure (Weight: 0.10)

**Assessment Type**: 4-factor analysis | **Output**: A-F grade

### Evaluation Factors

| Factor | Weight | Target | Scoring |
|--------|--------|--------|---------|
| Semantic Description | 0.25 | <200 chars, keyword-rich | 1.0/0.5/0.0 |
| Hierarchical Structure | 0.30 | 5 sections in order | 1.0/0.5/0.0 |
| Size Compliance | 0.25 | <500 lines | Formula below |
| Context Efficiency | 0.20 | External refs, no bloat | 1.0/0.5/0.0 |

### Size Score Formula
```
Size_Score = max(0.0, 1.0 - ((Line_Count - 500) / 500))
```


### Overall Formula
```
PD_Score = (Semantic x 0.25) + (Hierarchical x 0.30) + (Size x 0.25) + (Efficiency x 0.20)
Normalized_Score = PD_Score * 5
```

---

## Framework 6: Token Density (Weight: 0.10)

**Assessment Type**: 6-metric analysis | **Output**: A-F grade

### Scoring Dimensions

| Dimension | Weight | Target | Scoring |
|-----------|--------|--------|---------|
| Filler Word Density | 0.15 | <5% | 1.0 if <5%, 0.5 if 5-10%, 0.0 if >10% |
| Active Voice Ratio | 0.20 | >80% | 1.0 if >80%, 0.5 if 60-80%, 0.0 if <60% |
| Structured Data Usage | 0.15 | Lists > Prose | Optimized/Mixed/Verbose |
| XML Tag Efficiency | 0.15 | >30% savings | 1.0 if >40%, 0.5 if 30-40%, 0.0 if <30% |
| Example Efficiency | 0.20 | <=3, <20% tokens | Combined count + ratio score |
| Reference Inheritance | 0.15 | >60% reuse | 1.0 if >60%, 0.5 if 40-60%, 0.0 if <40% |

### Filler Words to Detect
```
"just", "very", "really", "quite", "simply", "basically", 
"in order to", "proceed to", "you should", "please"
```

### Overall Formula
```
TD_Score = (Filler x 0.15) + (Active x 0.20) + (Structured x 0.15) + 
           (XML x 0.15) + (Examples x 0.20) + (Inheritance x 0.15)
Normalized_Score = TD_Score * 5
```


---

## Framework 7: Framework Alignment (Weight: 0.10)

**Assessment Type**: Phase-aware evaluation | **Output**: A-F grade

### Domain-Framework Mapping

| Agent Category | Primary Framework Expected |
|----------------|---------------------------|
| Research | ReACT |
| Implementation | CAGEERF or Build-Measure-Learn |
| Analysis/Review | ReACT + DMAIC |
| Planning | CAGEERF or OKR |
| Debugging | ReACT + 5 Whys |
| Optimization | SCAMPER + DMAIC |
| Agent Lifecycle | CAGEERF + SCAMPER |

### Integration Depth Calculation
```
integration_depth = phases_with_framework_applied / total_phases
```

### Scoring Rubric

| Grade | Integration Depth | Framework Match |
|-------|------------------|-----------------|
| A (5) | >=0.75 | Optimal - Framework in 4+ workflow steps |
| B (4) | 0.50-0.74 | Good - Framework in 2-3 steps |
| C (3) | 0.25-0.49 | Acceptable - Framework in 1 step |
| D (2) | <0.25 | Mismatch - Framework mentioned not applied |
| F (1) | 0.0 | Missing - No framework when required |

---

## References

- **Source**: `.claude/agents/claude-code/claude-code-ecosystem/docs/evaluation-frameworks.md`
- **Related**: `.claude/skills/prompt-structural-analysis/SKILL.md` for structural criteria
