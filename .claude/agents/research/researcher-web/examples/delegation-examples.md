# Delegation Examples for Researcher-Web

**Purpose**: Show orchestrator how to delegate web research tasks

---

## When to Delegate to This Agent

### Trigger Conditions

Delegate to `researcher-web` when:
- User asks about "best practices", "industry standards"
- Need real-time/current information from web
- Trade-off analysis or comparison research needed
- External documentation or framework research

### NOT This Agent

Do NOT delegate when:
- Local codebase analysis needed -> Use `researcher-codebase`
- Library-specific API docs (simple) -> Use `researcher-library` (Context7-first)
- Pure orchestration decisions -> Handle in orchestrator

---

## Basic Delegation Pattern

### Quick Lookup

**Orchestrator says**:
```
Task(researcher-web, "Find current best practices for Python async error handling patterns")
```

**Agent returns**:
```json
{
  "status": "SUCCESS",
  "agent": "researcher-web",
  "confidence": 0.88,
  "agent_specific_output": {
    "findings": {
      "key_patterns": [
        {
          "pattern": "Structured exception hierarchy",
          "description": "Create custom exception classes inheriting from base",
          "confidence": 0.92,
          "sources": ["https://docs.python.org/3/library/asyncio-exceptions.html"]
        }
      ],
      "compressed_synthesis": "Modern async error handling uses structured exception hierarchies with TaskGroup for concurrent error propagation..."
    },
    "source_attribution": {
      "authoritative": [
        {"url": "https://docs.python.org/3/library/asyncio.html", "title": "Python Asyncio Docs", "quality_score": 0.95}
      ],
      "supporting": ["https://realpython.com/async-io-python/"]
    },
    "compression_stats": {
      "sources_evaluated": 12,
      "authoritative_used": 5,
      "patterns_extracted": 4,
      "compression_ratio": "15:1"
    }
  }
}
```

---

## Complex Delegation Pattern

### Deep Research with Context

**Orchestrator says**:
```
Task(researcher-web, "Research OAuth 2.0 vs API key authentication trade-offs.
Context: Enterprise SSO requirement, mobile app support needed.
Constraints: Must support refresh tokens, consider rate limiting implications.
Output format: Pros/cons matrix with recommendation.")
```

**Agent returns** (success):
```json
{
  "status": "SUCCESS",
  "agent": "researcher-web",
  "confidence": 0.91,
  "agent_specific_output": {
    "findings": {
      "key_patterns": [
        {
          "pattern": "OAuth 2.0 for enterprise SSO",
          "description": "Superior for SSO integration, supports SAML bridge",
          "confidence": 0.94,
          "sources": ["https://oauth.net/2/", "https://auth0.com/docs/"]
        },
        {
          "pattern": "API keys for service-to-service",
          "description": "Simpler for backend, but lacks refresh mechanism",
          "confidence": 0.89,
          "sources": ["https://cloud.google.com/docs/authentication"]
        }
      ],
      "compressed_synthesis": "For enterprise SSO + mobile: OAuth 2.0 with PKCE. OAuth handles token refresh natively, supports SSO via SAML/OIDC bridge. API keys lack rotation automation and mobile security..."
    },
    "research_boundaries": {
      "termination_reason": "target_patterns_found",
      "gaps": ["Specific rate limiting benchmarks not found"]
    },
    "security_validations": {
      "urls_validated": 8,
      "ssrf_checks_passed": 8,
      "content_sanitized": true,
      "secrets_detected": false
    }
  }
}
```

**Agent returns** (failure):
```json
{
  "status": "FAILURE",
  "agent": "researcher-web",
  "confidence": 0.3,
  "failure_details": {
    "failure_type": "insufficient_sources",
    "reasons": [
      "Perplexity rate limited (520)",
      "WebSearch returned outdated results (pre-2023)"
    ],
    "research_attempted": {
      "web_searches": ["OAuth 2.0 enterprise SSO 2024", "API key vs OAuth mobile"],
      "url_fetches": [
        {"url": "https://auth0.com/docs/", "error": "timeout"}
      ]
    },
    "partial_results": {
      "patterns_found": 1,
      "sources_accessed": 3
    },
    "recovery_suggestions": [
      {"approach": "Retry in 60s", "rationale": "Perplexity rate limit may clear"},
      {"approach": "Use researcher-library for auth0 docs", "rationale": "Context7 may have cached"}
    ]
  }
}
```

---

## Iteration Support Example

**When confidence < 0.85**:

```json
{
  "status": "SUCCESS",
  "agent": "researcher-web",
  "confidence": 0.72,
  "agent_specific_output": {
    "findings": { "..." },
    "iteration_support": {
      "open_questions": [
        {
          "question": "How does Pydantic v2 handle async validation in nested models?",
          "context": "Found basic patterns but nested model behavior unclear",
          "priority": "high",
          "suggested_approach": "researcher-library for official Pydantic docs"
        }
      ],
      "confidence_breakdown": {
        "overall_confidence": 0.72,
        "confidence_factors": {
          "source_quality": 0.85,
          "coverage_completeness": 0.60,
          "pattern_consensus": 0.75
        },
        "low_confidence_rationale": [
          "Pattern found in only 3 of 10 sources",
          "No official examples for nested async validation"
        ],
        "confidence_improvement_actions": [
          "Search official Pydantic documentation",
          "Find authoritative benchmarks"
        ]
      }
    }
  }
}
```

---

## Multi-Agent Coordination

### Upstream Agents (provide input)

| Agent | Provides | Example |
|-------|----------|---------|
| `researcher-lead` | Research objective, constraints | "Investigate OAuth patterns for mobile" |
| `orchestrator` | Task delegation with context | Direct delegation per examples above |

### Downstream Agents (consume output)

| Agent | Uses | For |
|-------|------|-----|
| `researcher-lead` | compressed_synthesis, key_patterns | Research plan synthesis |
| `python-code-implementer` | key_patterns, sources | Implementation guidance |
| `/spec` command | findings, source_attribution | Specification enrichment |

### Parallel Execution Pattern

```
Launch in parallel (independent research topics):
- Task(researcher-web, "Research async error handling patterns")
- Task(researcher-web, "Research retry/backoff strategies")
- Task(researcher-library, "Get tenacity library docs")

Synthesize results when all complete.
```

---

## Error Handling

### Retry Conditions

Retry delegation when:
- `confidence < 0.5` with refined context
- `failure_type: "insufficient_sources"` with alternative search terms

### Escalation Conditions

Escalate to user when:
- 2+ retries failed
- `failure_type: "security_violation"` (NEVER retry)
- Agent returns `recovery_suggestions` requiring human decision
