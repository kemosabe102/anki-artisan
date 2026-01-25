# Stakeholder Summary Reference

Executive summary format for non-technical stakeholders.

---

## When to Include Stakeholder Summary

Include `stakeholder_summary` when:
- Report audience includes non-technical leadership
- Executive briefing requested
- Sprint review presentations
- Budget/resource allocation discussions

---

## Required Fields

### overall_health

Plain-language health assessment.

| Value | Criteria |
|-------|----------|
| Excellent | debt_score >85, SQALE grade A |
| Good | debt_score 70-85, SQALE grade B |
| Needs Improvement | debt_score 50-70, SQALE grade C-D |
| Critical | debt_score <50, SQALE grade D-E |

---

### top_recommendations

Array of 3-5 actionable recommendations in plain language.

**Format Rules**:
- Start with action verb
- No technical jargon
- Include business impact
- Max 1 sentence each

**Examples**:
```json
{
  "top_recommendations": [
    "Prioritize payment processing reliability to reduce customer support tickets",
    "Add automated testing to prevent bugs from reaching production",
    "Update security dependencies to maintain compliance requirements",
    "Simplify checkout code to enable faster feature development",
    "Document API contracts to reduce onboarding time for new developers"
  ]
}
```

---

### roi_estimate

Return on investment calculation for debt remediation.

| Field | Description |
|-------|-------------|
| `investment_hours` | Total hours to remediate (principal) |
| `monthly_savings_hours` | Time saved per month after paydown (interest) |
| `break_even_months` | Months to recoup investment |

**Formula**:
```
break_even_months = investment_hours / monthly_savings_hours
```

**Example**:
```json
{
  "roi_estimate": {
    "investment_hours": 120,
    "monthly_savings_hours": 30,
    "break_even_months": 4
  }
}
```

Interpretation: "Investing 120 developer hours now will save 30 hours monthly, paying back the investment in 4 months."

---

## Executive Summary Format

Structure the stakeholder-facing output as follows:

### 1-Paragraph Overview

Template:
```
The codebase health is [overall_health]. The technical debt score is [debt_score]/100 
([debt_classification] classification) with a maintainability grade of [sqale_grade]. 
[Top hotspot count] areas require immediate attention. Addressing the top 3 priorities 
would improve the score by approximately [expected_improvement] points.
```

### Key Metrics Table

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Debt Score | 67/100 | >80 | Below target |
| SQALE Grade | C | B or better | Below target |
| Test Coverage | 72% | >80% | Below target |
| Critical Hotspots | 3 | 0 | Action needed |

### Recommended Actions (Top 3)

1. **[Action 1]** - [Business impact] - [Effort estimate]
2. **[Action 2]** - [Business impact] - [Effort estimate]
3. **[Action 3]** - [Business impact] - [Effort estimate]

### Risk Assessment

Map technical findings to business impact:

| Technical Issue | Business Risk |
|-----------------|---------------|
| Low test coverage in payments | Customer-facing bugs, refund costs |
| High complexity in checkout | Slow feature delivery, dev frustration |
| Outdated dependencies | Security vulnerabilities, compliance risk |

### Trend Direction (if baseline available)

- **Improving**: "Debt is decreasing. Continue current practices."
- **Stable**: "Debt is holding steady. Consider targeted remediation."
- **Worsening**: "Debt is accumulating. Immediate intervention recommended."

---

## Complete Example

```json
{
  "stakeholder_summary": {
    "overall_health": "Needs Improvement",
    "top_recommendations": [
      "Prioritize payment reliability to reduce support tickets",
      "Add testing to checkout flow to catch bugs earlier",
      "Update security libraries to maintain compliance"
    ],
    "roi_estimate": {
      "investment_hours": 80,
      "monthly_savings_hours": 25,
      "break_even_months": 3.2
    }
  }
}
```

---

## Language Guidelines

**DO**:
- Use business terms (reliability, velocity, risk)
- Quantify impact when possible
- Focus on outcomes, not technical details
- Provide clear action items

**DO NOT**:
- Use jargon (cyclomatic complexity, coupling)
- List technical violations
- Include code snippets
- Use acronyms without explanation
