# Documentation Reference Optimization Report

**Agent Analyzed**: {{agent_name}}
**Current Size**: {{current_lines}} lines / {{current_tokens}} tokens
**Analysis Date**: {{date}}

---

## Analysis Summary

| Metric | Current | Optimized | Savings | Confidence |
|--------|---------|-----------|---------|------------|
| **Total Tokens** | {{current_tokens}} | {{optimized_tokens}} | {{savings}} ({{percentage}}%) | {{confidence}} |
| **Workflow Section** | {{workflow_tokens}} | {{workflow_optimized}} | {{workflow_savings}} | {{workflow_confidence}} |
| **Methodology Section** | {{methodology_tokens}} | {{methodology_optimized}} | {{methodology_savings}} | {{methodology_confidence}} |

---

## Priority 1: High-Impact Optimizations (>1000 token savings)

### 1. {{recommendation_1_title}}

**Current**: {{current_state_1}}
**Issue**: {{issue_description_1}}
**Recommendation**: **{{strategy_1}}** → {{reference_path_1}}

**Optimization Strategy**:
```markdown
❌ BEFORE ({{before_tokens_1}} tokens):
{{before_example_1}}

✅ AFTER ({{after_tokens_1}} tokens):
{{after_example_1}}
```

**Token Savings**: {{savings_1}} tokens ({{percentage_1}}% reduction)
**Confidence**: {{confidence_1}}
**Value Score**: {{value_score_1}}

---

## Priority 2: Medium-Impact Optimizations (500-1000 token savings)

[Similar structure for P2 recommendations]

---

## Priority 3: Token Density Improvements (<500 token savings)

[Similar structure for P3 recommendations]

---

## Consolidated Recommendations

### Summary by Strategy

| Strategy | Opportunities | Token Savings | Avg Confidence | Highest Value Score |
|----------|---------------|---------------|----------------|---------------------|
| **reference_existing** | {{ref_count}} | {{ref_savings}} tokens | {{ref_confidence}} | {{ref_value_score}} |
| **compress_examples** | {{compress_count}} | {{compress_savings}} tokens | {{compress_confidence}} | {{compress_value_score}} |
| **keep_inline** | {{keep_count}} | 0 tokens | N/A | N/A |

---

**Report Generated**: {{timestamp}}
**Agent**: documentation ({{version}})
**Status**: ✅ SUCCESS with actionable recommendations
