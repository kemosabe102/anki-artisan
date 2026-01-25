# Frameworks & Methodologies for Researcher-Web

**Purpose**: Tool selection strategies, error handling, and research workflows

---

## Tool Selection Guide (Perplexity-First Exception)

**researcher-web is the ONLY agent with Perplexity-first strategy** (exception to system-wide Context7-first protocol).

| Situation | Tool | Timing | Cost |
|-----------|------|--------|------|
| Library docs, API reference | Context7 FIRST | 3-5s | Free |
| Quick facts, error messages | perplexity_search | 2-3s | Low |
| General questions, patterns | perplexity_ask | 3-5s | Low-Med |
| Deep research, multi-source | perplexity_research | 10-20s | High |
| Trade-offs, complex decisions | perplexity_reason | 8-15s | Med-High |
| Context7 library not found | perplexity_research | 10-20s | High |

---

## Primary Framework: Progressive Tool Escalation

### What It Is

Start with lightest tool, escalate only when insufficient results or errors.

### The Steps

1. **Select initial tool**: Match query type to tool (see table above)
2. **Execute with timeout**: Respect timing limits
3. **Evaluate results**: Check source count, quality, confidence
4. **Escalate if needed**: Lighter tool failed -> heavier Perplexity tool (search -> ask -> research -> reason)

### Fallback Chain Diagram

```
Library docs needed?
    |
    YES -> Context7 (resolve-library-id -> get-library-docs)
    |          |
    |          v (insufficient coverage)
    NO ------> Perplexity (PRIMARY)
                  |
                  +-- perplexity_search (quick facts, 2-3s)
                  +-- perplexity_ask (general questions, 3-5s)
                  +-- perplexity_research (deep analysis, 10-20s)
                  +-- perplexity_reason (trade-offs, 8-15s)
                  |
                  v (520/429 errors)
               Wait 30s -> Retry with lighter Perplexity tool
                  |
                  v (max retries reached)
               Return with confidence score < 0.85
```

---

## Secondary Framework: Sufficiency Checking

### What It Is

Mandatory check before EVERY tool call to prevent over-research.

### When to Use

- Before each search query
- After receiving results
- Before returning output

### The Checklist

| Question | YES Action |
|----------|------------|
| Do I have 3+ authoritative sources with consensus? | STOP, compress, return |
| Is confidence >= 0.85 on answering objective? | STOP, compress, return |
| Have I exceeded 50% of tool budget? | STOP, compress, return |
| Have I exceeded 5 iterations? | STOP, compress, return |
| Has research exceeded 30 seconds? | STOP, compress, return |

---

## Error Handling

### Perplexity API Errors (PRIMARY TOOL)

| Error | Classification | Strategy | Fallback |
|-------|---------------|----------|----------|
| **520** (rate limiting) | TRANSIENT | Wait 30-60s, retry lighter tool | Return with low confidence |
| **429** (quota exceeded) | TRANSIENT | Wait 30s, retry once | Return with low confidence |
| **500** (server error) | TRANSIENT | Retry once immediately | Return with low confidence |
| **401/403** (auth) | PERMANENT | Escalate to orchestrator | N/A |
| **Insufficient results** | OPERATIONAL | Escalate tool (search->ask->research->reason) | Return with confidence score |

**Progressive Degradation Pattern**:
```
perplexity_research -> (520) -> wait 30s -> perplexity_ask -> (520) -> perplexity_search -> return with confidence
```

### Context7 MCP Errors

| Error | Classification | Strategy | Fallback |
|-------|---------------|----------|----------|
| **Library not found** | PERMANENT | Immediate fallback | perplexity_research |
| **Timeout** | TRANSIENT | Max 3 retries (2s, 4s, 8s) | Perplexity (research for lib docs) |
| **MCP unavailable** | FATAL | Return FAILURE | Document in failure_details |

### Circuit Breaker Pattern

**Per-Tool Tracking**: Track failures per Perplexity tool (e.g., `perplexity_research`)

| State | Condition | Behavior |
|-------|-----------|----------|
| CLOSED | <6 failures | Normal operation |
| OPEN | 6+ consecutive TRANSIENT failures | Skip domain 60s, use cache if available |
| HALF-OPEN | After 60s | Allow 3 test requests |

---

## Security Errors (FATAL - Never Retry)

| Error | Source | Response |
|-------|--------|----------|
| SSRF attempt | security-validate-url.py | Return FAILURE, log violation |
| Secrets detected | security-sanitize-content.py | Strip content, return FAILURE |
| Content too large (>5MB) | Any tool | Reject source, continue with others |

**FATAL Response Template**:
```json
{
  "status": "FAILURE",
  "agent": "researcher-web",
  "confidence": 0.0,
  "failure_details": {
    "failure_type": "security_violation",
    "error_classification": "FATAL",
    "security_hook": "validate_url.py",
    "recovery_suggestions": ["NEVER retry security violations"]
  }
}
```

---

## Termination Rules ("Good Enough" Criteria)

| Criterion | Threshold | Action |
|-----------|-----------|--------|
| Source Quality | 5+ authoritative AND confidence >= 0.85 | STOP |
| Iteration Limit | >5 search iterations | STOP |
| Time Estimate | >30 seconds | STOP |
| Diminishing Returns | <2 new insights last iteration | STOP |
| Token Budget | Findings approaching 10K tokens | STOP |

---

## Iteration Support

**When to Populate**: confidence < 0.85 OR questions discovered during research

### Structure

```json
{
  "iteration_support": {
    "open_questions": [
      {
        "question": "Specific unanswered question",
        "context": "Why it arose, what was found",
        "priority": "high|medium|low",
        "suggested_approach": "Which agent/tool for follow-up"
      }
    ],
    "confidence_breakdown": {
      "overall_confidence": 0.72,
      "confidence_factors": {
        "source_quality": 0.85,
        "coverage_completeness": 0.60,
        "pattern_consensus": 0.75
      },
      "low_confidence_rationale": ["Specific reasons"],
      "confidence_improvement_actions": ["Specific steps"]
    }
  }
}
```

---

## Quick Reference

### Tool Decision Tree

```
Request type?
    |
    +-- Library/API docs? -> Context7 (fallback: perplexity_research)
    |
    +-- Quick fact/error? -> perplexity_search
    |
    +-- General question? -> perplexity_ask
    |
    +-- Deep analysis? -> perplexity_research
    |
    +-- Trade-off/decision? -> perplexity_reason
    |
    +-- All tools exhausted? -> Return with confidence score < 0.85
```

### External References

- **Perplexity details**: `perplexity-mcp-usage-guide.md`
- **Research patterns**: `.claude/docs/00-core/research-patterns.md`
- **Error taxonomy**: `.claude/docs/00-core/error-classification-framework.md`
- **Circuit breaker**: `.claude/docs/01-guides/circuit-breaker-pattern.md`
