# Web Research Findings Template

**Research Question:** [Clear, concise statement of the research objective]

**Date:** [YYYY-MM-DD]

**Researcher:** [Agent/Skill Name]

---

## Executive Summary

[2-3 sentence summary of key findings, confidence score, and source quality]

**Confidence Score:** [0.00-1.00] ([Low/Medium/High])

**Source Quality:** [Average Authority Score] ([Tier distribution])

**Time Elapsed:** [Minutes/seconds]

---

## Research Context

**CQ (Context Quality):** [0.00-1.00] ([Low/Medium/High])

**Research Depth:** [Light/Standard/Deep]

**Tools Used:**
- [Tool 1]: [Query/URL]
- [Tool 2]: [Query/URL]
- [Tool 3]: [Query/URL]

**Constraints:**
- [Time, scope, source availability, etc.]

---

## Key Findings

### Finding 1: [Title]

**Summary:** [1-2 sentence description]

**Details:**
- [Bullet point detail 1]
- [Bullet point detail 2]
- [Bullet point detail 3]

**Sources:** [Source IDs or inline citations]

**Authority Score:** [0.00-1.00]

---

### Finding 2: [Title]

**Summary:** [1-2 sentence description]

**Details:**
- [Bullet point detail 1]
- [Bullet point detail 2]

**Sources:** [Source IDs or inline citations]

**Authority Score:** [0.00-1.00]

---

[Repeat for additional findings]

---

## Source Citations

### Tier 1 Sources (Official Documentation)

**[1] [Source Name/Title]**
- **URL:** [Full URL]
- **Authority Tier:** 1
- **Authority Score:** [0.90-1.00]
- **Date Published:** [YYYY-MM-DD or "Unknown"]
- **Date Accessed:** [YYYY-MM-DD]
- **Relevance:** [Why this source was used]
- **Key Extract:** [Brief quote or paraphrase]

---

### Tier 2 Sources (Vendor/Academic)

**[2] [Source Name/Title]**
- **URL:** [Full URL]
- **Authority Tier:** 2
- **Authority Score:** [0.70-0.89]
- **Date Published:** [YYYY-MM-DD]
- **Date Accessed:** [YYYY-MM-DD]
- **Relevance:** [Why this source was used]
- **Key Extract:** [Brief quote or paraphrase]

---

### Tier 3 Sources (Community/Expert)

**[3] [Source Name/Title]**
- **URL:** [Full URL]
- **Authority Tier:** 3
- **Authority Score:** [0.50-0.69]
- **Date Published:** [YYYY-MM-DD]
- **Date Accessed:** [YYYY-MM-DD]
- **Relevance:** [Why this source was used]
- **Key Extract:** [Brief quote or paraphrase]
- **Validation:** [How this source was cross-referenced]

---

## Validation Summary

**Source Quality Distribution:**
- Tier 1: [Count] sources (Authority Score: [Avg])
- Tier 2: [Count] sources (Authority Score: [Avg])
- Tier 3: [Count] sources (Authority Score: [Avg])

**Cross-Reference Status:**
- [Finding 1]: Confirmed by [X] sources (Tiers [Y, Z])
- [Finding 2]: Confirmed by [X] sources (Tiers [Y, Z])
- [Finding 3]: Single source only (flagged for future validation)

**Recency Check:**
- [X]% sources within relevance window
- [Y]% sources 1-2x window (reduced weight)
- [Z]% sources >2x window (flagged as potentially outdated)

**Contradictions Found:** [None / List any conflicting information]

---

## Confidence Score Breakdown

**Final Confidence Score:** [0.00-1.00]

**Calculation:**
```
Source Quality:   [0.00-1.00] (weight: 0.40)
Completeness:     [0.00-1.00] (weight: 0.30)
Recency:          [0.00-1.00] (weight: 0.20)
Consensus:        [0.00-1.00] (weight: 0.10)
```

**Factors Impacting Score:**
- [Positive factor 1, e.g., "All Tier 1 sources"]
- [Positive factor 2, e.g., "High consensus across sources"]
- [Negative factor 1, e.g., "One finding from single source"]

---

## Gaps and Limitations

**Known Gaps:**
- [Gap 1: e.g., "No production benchmarks found for Framework X"]
- [Gap 2: e.g., "Security considerations not addressed"]

**Limitations:**
- [Limitation 1: e.g., "Sources limited to English language"]
- [Limitation 2: e.g., "Paywall blocked access to 2 academic papers"]

**Recommendations for Follow-Up:**
- [Recommendation 1: e.g., "Run internal benchmark to validate claims"]
- [Recommendation 2: e.g., "Consult security specialist for review"]

---

## Next Steps

**Immediate Actions:**
- [Action 1: e.g., "Implement best practice X from Finding 2"]
- [Action 2: e.g., "Validate claim Y in staging environment"]

**Future Research:**
- [Future topic 1: e.g., "Deep dive on Framework X security model"]
- [Future topic 2: e.g., "Comparative benchmark: X vs Y"]

**Escalation Required:** [Yes/No]
- **Reason:** [If yes, explain why user/specialist input needed]

---

## Appendix: Research Methodology

**Phase 1: [Tool Name]**
- Query: [Exact query text]
- Execution Time: [Seconds]
- Sources Retrieved: [Count]
- Decision: [Proceed/Escalate/Complete]

**Phase 2: [Tool Name]** (if applicable)
- Query: [Exact query text]
- Execution Time: [Seconds]
- Sources Retrieved: [Count]
- Decision: [Proceed/Escalate/Complete]

**Phase 3: [Tool Name]** (if applicable)
- Query: [Exact query text]
- Execution Time: [Seconds]
- Sources Retrieved: [Count]
- Decision: [Complete]

**Total Execution Time:** [Minutes:Seconds]

---

## Related Documents

- **Tool Selection:** `.claude/skills/web-research/reference/tool-patterns.md`
- **Authority Scoring:** `.claude/skills/web-research/reference/source-authority.md`
- **Research Patterns:** `.claude/docs/00-core/research-patterns.md`
- **Thresholds:** `.claude/docs/00-core/orchestrator-thresholds.md`
