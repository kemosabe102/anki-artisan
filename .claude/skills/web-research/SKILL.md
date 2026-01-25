---
name: web-research
description: >
  Use this skill when researching external best practices, industry standards,
  or current documentation. Provides Perplexity-first workflow with progressive
  tool escalation and source quality scoring (0.70-0.90+ thresholds).
  Keywords: web research, best practices, industry standards, external docs, trade-off analysis.
---

# Web Research

*Execute focused external research with progressive tool escalation and source quality scoring.*

---

## Contents

1. [Tool Escalation Strategy](#tool-escalation-strategy)
2. [Mode Detection](#mode-detection)
3. [Source Quality Scoring](#source-quality-scoring)
4. [Tool Priority](#tool-priority)
5. [Compression Guidelines](#compression-guidelines)
6. [Termination Rules](#termination-rules)
7. [Security Patterns](#security-patterns)
8. [Error Recovery](#error-recovery)
9. [Anti-Patterns](#anti-patterns)
10. [Thinking Frameworks](#thinking-frameworks)
11. [Quick Reference](#quick-reference)

---

## Tool Escalation Strategy

Select tools based on query complexity and response time needs.

| Tool | Response Time | Use Case |
|------|---------------|----------|
| `perplexity_search` | 2-3s | Quick facts, error messages, simple lookups |
| `perplexity_ask` | 3-5s | Follow-up questions, clarifications |
| `perplexity_research` | 10-20s | Best practices, deep research, comprehensive analysis |
| `perplexity_reason` | 8-15s | Trade-offs, comparisons, architectural decisions |

### Escalation Flow

```
perplexity_search (quick) → perplexity_ask (follow-up) → perplexity_research (deep)
                                                      ↘ perplexity_reason (decisions)
```

**Rule**: Start with lightest tool. Escalate only if insufficient results.

---

## Mode Detection

| User Says | Mode | Start With |
|-----------|------|------------|
| "best practices", "industry standards" | web_research | perplexity_research |
| "quick facts", "error message" | quick_lookup | perplexity_search |
| "trade-off", "comparison", "decision" | analysis | perplexity_reason |
| "library docs", "API reference" | library_fallback | Context7 first |

**Do not announce the mode. Execute the appropriate tool directly.**

---

## Source Quality Scoring

Assess all sources and filter based on authority level.

| Authority Level | Score | Source Types | Action |
|-----------------|-------|--------------|--------|
| Authoritative | 0.90+ | Official docs, RFC, IEEE, peer-reviewed | Primary citation |
| Supporting | 0.70-0.89 | Reputable blogs, Stack Overflow (high votes) | Secondary citation |
| Reject | <0.70 | Unverified forums, outdated posts, anonymous | Do not cite |

### Scoring Factors

- **Recency**: Prefer sources <2 years old (technology topics)
- **Domain Authority**: Official domains (.gov, .edu, vendor docs) score higher
- **Citation Count**: Well-referenced sources indicate authority

---

## Tool Priority

### Library Documentation

**Context7 FIRST** (free, authoritative):
```
mcp__context7__resolve-library-id(libraryName="react")
mcp__context7__get-library-docs(context7CompatibleLibraryID="/facebook/react")
```

**Fallback to Perplexity** only if Context7 returns no results.

### All Other Web Research

**Perplexity** (comprehensive):
- Use progressive escalation (search → ask → research/reason)
- Target cost ratio: 4 Context7 calls : 1 Perplexity call

---

## Compression Guidelines

| Metric | Target |
|--------|--------|
| Compression Ratio | 10:1 minimum |
| Example | 25 sources → 2.5 pages synthesized |
| Output Format | Structured findings, not raw citations |

### Compression Techniques

- **Summarize consensus**: "3/4 authoritative sources recommend X approach"
- **Extract patterns**: Common recommendations across sources
- **Prioritize actionable**: Keep concrete recommendations, drop theory
- **Cite selectively**: 1-2 key sources per finding

---

## Termination Rules

### Stop When ANY Condition is True

1. 3+ authoritative sources with consensus = "good enough"
2. Confidence >= 0.85 for primary finding
3. MAX 5 iterations reached
4. MAX 30 seconds elapsed
5. All queries returning same results (stagnation)

---

## Security Patterns

### SSRF Prevention

**Domain Whitelist**: 177 approved domains across categories:
- **Financial**: Bloomberg, Reuters, Yahoo Finance, SEC.gov
- **Development**: GitHub, GitLab, Stack Overflow, MDN
- **Technical Docs**: Official language/framework documentation
- **Academic**: arXiv, PubMed, IEEE, ACM
- **Security**: OWASP, NIST, CVE databases

### Domain Validation Rules

1. **Whitelist check**: URL domain must be in approved list
2. **IP validation**: Block internal IPs (10.x, 172.16-31.x, 192.168.x, 169.254.x)
3. **Protocol check**: HTTPS required (HTTP rejected)
4. **Path validation**: No suspicious patterns (../, metadata endpoints)

### Request Limits

| Limit | Value |
|-------|-------|
| Response size | 5MB max |
| Request timeout | 30s max |
| Redirect chain | 3 hops max |

### Prohibited Actions

- Never execute fetched code
- Never follow redirect chains > 3 hops
- Never access file:// or internal protocols
- Never fetch from internal/private IPs

### OWASP LLM Compliance

| Risk | Mitigation |
|------|------------|
| Prompt Injection | Input sanitization on queries |
| Insecure Output | Content sanitization (HTML -> Markdown) |
| Training Poisoning | Trusted sources only (domain whitelist) |
| Model DoS | Response size + timeout limits |

---

## Error Recovery

| Issue | Recovery Sequence |
|-------|-------------------|
| Rate limited (520/429) | Wait 30s → Try lighter tool → Retry |
| Insufficient results | Escalate tool (search → ask → research) |
| Context7 not found | Switch to Perplexity for library docs |
| Security violation | Return FAILURE immediately (no retry) |
| Timeout | Return partial results with gaps noted |

### Retry Limits

- **Per-tool retries**: 2 maximum
- **Tool escalation**: 3 levels maximum
- **Total attempts**: 5 per research session

---

## Anti-Patterns

### NEVER DO

- Return raw search results (compress first)
- Cite sources below 0.70 quality score
- Exceed 30 seconds total research time
- Use Perplexity for library docs (Context7 first)
- Continue after security violation
- Fabricate missing citations

### Efficiency Anti-Patterns

- Starting with perplexity_research for simple questions
- Multiple searches with identical queries
- Ignoring Context7 for known libraries
- Returning 10+ sources when 3 authoritative suffice

---

## Thinking Frameworks

Apply these frameworks for systematic research.

| Framework | When to Use |
|-----------|-------------|
| OODA | Research cycle: Observe sources → Orient findings → Decide relevance → Act on synthesis |
| ReACT | Error recovery: Reason about failure → Act with recovery → Observe result → Refine |

> **Selection Tip**: research cycle → OODA, error recovery → ReACT

---

## Quick Reference

```
TOOL PRIORITY:
  Library docs → Context7 FIRST
  All other   → Perplexity (start light, escalate)

ESCALATION:
  perplexity_search (2-3s) → perplexity_ask (3-5s) → perplexity_research (10-20s)
                                                   ↘ perplexity_reason (8-15s)

SOURCE QUALITY:
  0.90+     Authoritative (cite as primary)
  0.70-0.89 Supporting (cite as secondary)
  <0.70     Reject (do not cite)

TERMINATION:
  - 3+ authoritative with consensus
  - Confidence >= 0.85
  - MAX 5 iterations OR 30 seconds

COMPRESSION:
  - 10:1 minimum ratio
  - 25 sources → 2.5 pages synthesized

SECURITY:
  - 177-domain whitelist
  - No internal URLs
  - FAILURE on violation (no retry)
```

---

## Validation Checklist

Before completing research:

- [ ] Tool escalation followed (light → heavy)
- [ ] Source quality scored (reject <0.70)
- [ ] Compression ratio 10:1 achieved
- [ ] Confidence >= 0.85 OR gaps documented
- [ ] Termination rules checked
- [ ] Security patterns verified
- [ ] Context7 used for library docs (if applicable)

---

## Cross-References

### Skill-Specific Documentation

| Document | Purpose |
|----------|---------|
| [Tool Patterns](./reference/tool-patterns.md) | Perplexity modes, WebSearch, WebFetch patterns |
| [Source Authority](./reference/source-authority.md) | Domain scoring tiers, credibility assessment |
| [Common Docs](./reference/common-docs.md) | Links to shared documentation |
| [Simple Example](./examples/example-simple.md) | "Python 3.12 features" - quick search |
| [Findings Template](./templates/findings-template.md) | Output format with citations |

### Shared Documentation

| Document | Purpose |
|----------|---------|
| [Perplexity Usage Guide](/docs/shared/mcp/perplexity-mcp-usage-guide.md) | Complete Perplexity MCP reference |
| [Research Skill Escalation](/.claude/docs/01-guides/research/research-skill-escalation.md) | Cross-skill handoff protocols |
| [Orchestrator Thresholds](/.claude/docs/00-core/orchestrator-thresholds.md) | CQ formulas and confidence scoring |
| [Research Patterns](/.claude/docs/00-core/research-patterns.md) | General research methodology |

### Related Skills

| Skill | Escalate When |
|-------|---------------|
| [codebase-research](../codebase-research/SKILL.md) | Need to check local implementation patterns |
| [library-research](../library-research/SKILL.md) | Need official API documentation (Context7 first) |
