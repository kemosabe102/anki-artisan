# Example: Simple Fact-Finding - Web Research Skill

**Scenario:** Quick research on Python 3.12 new features

**Research Question:** What are the key new features in Python 3.12?

---

## Context

**CQ (Context Quality):** 0.90 (High - simple factual query)

**Research Depth:** Light (single Perplexity search sufficient)

**Expected Time:** <1 minute

---

## Tool Selection

**Selected Tool:** Perplexity `search`

**Rationale:**
- Simple factual query (not complex reasoning)
- Well-documented topic (official Python docs exist)
- Single concept (Python version features)
- No comparative analysis needed

**Rejected Tools:**
- `reason`: Overkill for facts (no multi-step logic)
- `deep_research`: Cost-inefficient for simple lookup
- WebSearch: Perplexity provides better synthesis + citations

---

## Query Formulation

**Optimized Query:** `"Python 3.12 new features and improvements"`

**Optimization Decisions:**
- Added "improvements" to capture enhancements (not just new features)
- Used version number explicitly (3.12, not "latest")
- No year needed (version implies recency)
- Single-concept query (no compound questions)

---

## Execution

```
Tool: Perplexity Search
Query: "Python 3.12 new features and improvements"
Execution Time: 22 seconds
Sources Retrieved: 4
```

---

## Findings

### Key Features

1. **PEP 701: F-String Improvements**
   - Arbitrary nesting of quotes and expressions
   - Improved error messages for invalid f-strings
   - Source: [Python Docs - What's New 3.12]

2. **Per-Interpreter GIL (PEP 684)**
   - Experimental support for subinterpreters with independent GILs
   - Enables true parallelism for CPU-bound tasks
   - Source: [PEP 684]

3. **Type System Enhancements**
   - `type` keyword for type aliases (PEP 695)
   - Generic classes syntax simplification
   - Source: [Python Docs - What's New 3.12]

4. **Performance Improvements**
   - 5% faster than Python 3.11 (comprehensions, overhead reduction)
   - Source: [Python Release Notes]

---

## Source Citations

### Source 1: Python Official Documentation - What's New in 3.12
- **URL:** https://docs.python.org/3.12/whatsnew/3.12.html
- **Authority Tier:** 1 (Official Documentation)
- **Authority Score:** 1.00
- **Date Accessed:** 2025-12-13
- **Relevance:** Primary source for Python version features

### Source 2: PEP 684 - Per-Interpreter GIL
- **URL:** https://peps.python.org/pep-0684/
- **Authority Tier:** 1 (Official Standards)
- **Authority Score:** 1.00
- **Date Accessed:** 2025-12-13
- **Relevance:** Technical specification for GIL changes

### Source 3: PEP 701 - Syntactic Formalization of F-strings
- **URL:** https://peps.python.org/pep-0701/
- **Authority Tier:** 1 (Official Standards)
- **Authority Score:** 1.00
- **Date Accessed:** 2025-12-13
- **Relevance:** F-string enhancement details

### Source 4: Python 3.12.0 Release Notes
- **URL:** https://www.python.org/downloads/release/python-3120/
- **Authority Tier:** 1 (Official Release)
- **Authority Score:** 1.00
- **Date Accessed:** 2025-12-13
- **Relevance:** Official performance benchmarks

---

## Validation

**Source Quality Check:**
- All sources are Tier 1 (official Python documentation)
- No conflicting information found
- Recency: Python 3.12 released Oct 2023 (within relevance window)

**Completeness:**
- 4 major feature categories covered
- Sufficient depth for high-level overview
- No follow-up research needed

**Confidence Score:** 0.95 (High - all Tier 1 sources, comprehensive coverage)

---

## Output Summary

**Research Completed:** Python 3.12 features identified with official citations

**Key Findings:**
1. F-string improvements (PEP 701)
2. Per-interpreter GIL (PEP 684)
3. Type system enhancements (PEP 695)
4. 5% performance boost

**Sources:** 4 Tier 1 official Python sources

**Time Elapsed:** <1 minute

**Next Steps:** None (query fully answered)

---

## Lessons Learned

**What Worked:**
- Perplexity `search` was appropriate tool choice (fast, accurate)
- Query optimization yielded focused results
- All sources were Tier 1 (no validation overhead)

**Optimization Opportunities:**
- Could have included "PEP" in query for more technical depth
- Future queries: add "official" to prioritize primary sources

---

## Template Mapping

This example demonstrates:
- Tool selection (Perplexity search for simple facts)
- Query optimization (concise, version-specific)
- Source authority validation (all Tier 1)
- Citation formatting (URL, tier, score, date)
- Confidence scoring (0.95 based on source quality)

**See:** `templates/findings-template.md` for full output format
