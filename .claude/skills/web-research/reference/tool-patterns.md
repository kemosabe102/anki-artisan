# Tool Patterns - Web Research Skill

**Version**: 1.0.0 | **Last Updated**: 2025-12-13

---

## Overview

This document defines tool selection patterns and query optimization strategies for web research operations.

---

## Perplexity Tool Selection Decision Tree

### Primary Decision Factors

| Factor | search | reason | deep_research |
|--------|--------|--------|---------------|
| **Complexity** | Simple facts | Multi-step logic | Comprehensive analysis |
| **Time Sensitivity** | <30s | <2min | <5min |
| **Source Count** | 3-5 sources | 5-10 sources | 10+ sources |
| **Cost** | Low | Medium | High |
| **Use Frequency** | 80% of queries | 15% of queries | 5% of queries |

---

## Tool 1: Perplexity Search

**When to Use:**
- Quick factual lookups
- Simple "what is X" questions
- Version/release date checks
- Single-concept clarification
- Documentation link discovery

**Query Optimization:**
```
Good: "Python 3.12 release date"
Bad:  "When did Python release version 3.12 and what were the major features?"

Good: "FastAPI async database support"
Bad:  "How do I implement async database connections in FastAPI with proper error handling?"
```

**Pattern:**
1. Use natural language questions (concise)
2. Include version numbers when relevant
3. Add year for recency: "...best practices 2024"
4. Avoid compound questions (split into multiple searches)

**Expected Response Time:** <30 seconds

**Source Quality:** 3-5 authoritative sources with citations

---

## Tool 2: Perplexity Reason

**When to Use:**
- Multi-step reasoning required
- Comparative analysis ("X vs Y")
- Architectural decisions ("best approach for...")
- Debugging complex issues
- Trade-off evaluation

**Query Optimization:**
```
Good: "Compare PostgreSQL vs TimescaleDB for time-series data at 1M inserts/day"
Bad:  "Database comparison"

Good: "Kubernetes HPA vs KEDA for event-driven autoscaling: latency and cost trade-offs"
Bad:  "How to autoscale Kubernetes?"
```

**Pattern:**
1. Frame as decision problem ("Compare A vs B for use case C")
2. Include constraints/metrics ("at scale X", "with requirement Y")
3. Specify evaluation criteria ("latency", "cost", "complexity")
4. Use "why" or "how" for causal reasoning

**Expected Response Time:** 1-2 minutes

**Source Quality:** 5-10 sources with reasoning chains

---

## Tool 3: Perplexity Deep Research

**When to Use:**
- State-of-the-art reviews
- Comprehensive best practices guides
- Security vulnerability analysis
- Technology landscape surveys
- Multi-domain integration research

**Query Optimization:**
```
Good: "State-of-the-art for real-time financial data pipelines: architecture patterns, tools, and trade-offs (2024)"
Bad:  "Financial data pipelines"

Good: "Comprehensive review: Python async frameworks for high-throughput API services (FastAPI, Sanic, Starlette) with benchmarks"
Bad:  "Python async frameworks"
```

**Pattern:**
1. Use "state-of-the-art" or "comprehensive review" prefix
2. Enumerate specific domains/tools to cover
3. Request specific output types ("benchmarks", "case studies")
4. Include year for currency
5. Phrase as research question

**Expected Response Time:** 3-5 minutes

**Source Quality:** 10+ authoritative sources, academic papers preferred

---

## WebSearch Tool

**When to Use:**
- Perplexity unavailable (fallback)
- Need exact URL discovery (not just citations)
- Specific site search ("site:python.org asyncio")
- Open-ended exploration (browsing mode)
- Image/video result needs

**Query Optimization:**
```
Good: "site:kubernetes.io HorizontalPodAutoscaler behavior"
Good: "FastAPI streaming response example github.com"
Good: "TimescaleDB compression benchmarks filetype:pdf"
```

**Pattern:**
1. Use search operators: `site:`, `filetype:`, `-exclude`
2. Include example keywords: "example", "tutorial", "guide"
3. Add platform hints: "github.com", "stackoverflow.com"
4. Quote exact phrases: `"async with"` for Python syntax

**Expected Response Time:** <10 seconds

**Limitation:** No synthesis, raw search results only

---

## WebFetch Tool

**When to Use:**
- Extract content from specific URL (from search/Perplexity results)
- Official documentation reading
- Blog post/article deep-dive
- GitHub README/docs parsing
- Code snippet extraction

**URL Selection Criteria:**
1. **Official docs** > Academic papers > Tech blogs > Forums
2. Check domain authority (see `source-authority.md`)
3. Prefer recent content (<1 year for tools, <3 years for concepts)
4. Avoid paywalls (check free alternatives first)

**Content Extraction Patterns:**

```markdown
# HTML Processing Strategy

1. Identify content region (skip nav/footer/ads)
2. Extract main headings (H1-H3)
3. Capture code blocks with language tags
4. Preserve inline links for citations
5. Strip images unless diagram-critical
```

**Post-Fetch Actions:**
1. Validate content relevance (>70% signal, <30% noise)
2. Extract key quotes with `[source URL]` citation
3. Summarize in 2-3 bullet points
4. Store URL in findings template

**Expected Response Time:** <15 seconds per URL

---

## Tool Selection Flowchart

```
User Query
    |
    v
Is it a simple fact? ─YES─> Perplexity SEARCH
    |
    NO
    v
Multiple sources needed? ─NO─> WebFetch (if URL known)
    |                              |
    YES                           (extract and cite)
    v
Requires reasoning/comparison? ─YES─> Perplexity REASON
    |
    NO
    v
Comprehensive/state-of-art? ─YES─> Perplexity DEEP_RESEARCH
    |
    NO
    v
Fallback: WebSearch + WebFetch
```

---

## Citation Formatting Requirements

### In-Text Citations

**Pattern:** `[Author/Source Year]` or `[Source]` if no date

```markdown
FastAPI supports async database operations natively [FastAPI Docs].
TimescaleDB compression achieves 95% reduction on financial data [Timescale Blog 2024].
```

### Reference List Format

```markdown
## Sources

1. **FastAPI Documentation - Database Integrations**
   - URL: https://fastapi.tiangolo.com/advanced/sql-databases-async/
   - Authority: Official (Tier 1)
   - Date Accessed: 2025-12-13

2. **Timescale Blog - Compression Benchmarks**
   - URL: https://www.timescale.com/blog/compression-benchmarks-2024
   - Authority: Vendor (Tier 2)
   - Date: 2024-06-15
```

---

## Multi-Tool Patterns

### Progressive Depth Pattern

```
1. Start: Perplexity SEARCH (broad orientation)
2. Escalate: Perplexity REASON (if ambiguity found)
3. Deep Dive: Perplexity DEEP_RESEARCH (if critical decision)
4. Validate: WebFetch official docs (confirm findings)
```

### Parallel Validation Pattern

```
1. Perplexity SEARCH (primary research)
2. WebFetch (2-3 top sources in parallel)
3. Cross-reference findings
4. Flag contradictions for REASON escalation
```

---

## Anti-Patterns

**AVOID:**
- Using `deep_research` for simple facts (cost inefficiency)
- Chaining multiple `search` calls without synthesis (use `reason` instead)
- WebFetch without source authority check (garbage in, garbage out)
- Queries without version/year context (stale results)
- Compound questions in `search` (split into atomic queries)

---

## Related Documents

- `source-authority.md` - Domain scoring and credibility assessment
- `common-docs.md` - Shared research methodology documentation
- `docs/shared/mcp/perplexity-mcp-usage-guide.md` - Full Perplexity API reference
