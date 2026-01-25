# Delegation Examples

## Four-Component Delegation Pattern

Every delegation from researcher-lead should include:

1. **Specific Objective**: What to research
2. **Output Format**: How to structure findings
3. **Tool & Source Guidance**: Which tools and token budget
4. **Task Boundaries**: Scope and exclusions

### Example Delegation

```
Task(researcher-library,
  "Research Pydantic v2 async validation patterns.
   Return API signatures, key patterns, 1-2 code examples.
   Use Context7, focus on async validators, 5000 tokens.
   Scope: Async validation only. Exclude: Sync validators, serialization.")
```

**Parsed Components**:
- **Objective**: "Pydantic v2 async validation patterns"
- **Output Format**: "API signatures, key patterns, 1-2 code examples"
- **Tool Guidance**: "Context7, focus on async validators, 5000 tokens"
- **Boundaries**: "Scope: Async validation only. Exclude: Sync validators, serialization"

---

## SUCCESS State Example

```json
{
  "status": "SUCCESS",
  "agent": "researcher-library",
  "confidence": 0.92,
  "execution_timestamp": "2025-10-06T12:00:00Z",
  "agent_specific_output": {
    "findings": {
      "library_info": {
        "library_id": "/pydantic/pydantic",
        "version": "v2.x",
        "trust_score": 9,
        "snippet_count": 542
      },
      "api_signatures": [
        "async def validate_field(value: str, *, context: ValidationContext) -> str",
        "Model.model_validate(data: dict) -> Self",
        "@field_validator('field_name', mode='after') async def validate(cls, v) -> str"
      ],
      "key_patterns": [
        "Use model_validate() not parse_obj() in v2",
        "Async validators require 'mode=after' decorator",
        "ValidationContext provides access to other field values"
      ],
      "code_examples": [
        {
          "description": "Async field validation pattern",
          "code": "from pydantic import BaseModel, field_validator\n\nclass User(BaseModel):\n    email: str\n    \n    @field_validator('email', mode='after')\n    @classmethod\n    async def validate_email(cls, v: str) -> str:\n        # async validation logic\n        return v",
          "source": "/pydantic/pydantic/docs/async-validation"
        }
      ],
      "version_notes": [
        "Breaking change: parse_obj() deprecated in v2.0",
        "New feature: model_validate_json() added in v2.1"
      ]
    },
    "compression_stats": {
      "tokens_retrieved": 15000,
      "findings_returned": 1000,
      "compression_ratio": "15:1"
    },
    "context7_performance": {
      "query_count": 2,
      "total_duration_seconds": 8
    },
    "research_boundaries": {
      "termination_reason": "found_sufficient",
      "topic_coverage": ["async validation", "field validators", "model methods"],
      "gaps": ["Serialization patterns not covered (excluded by scope)"]
    }
  }
}
```

---

## FAILURE State Example

```json
{
  "status": "FAILURE",
  "agent": "researcher-library",
  "confidence": 0.3,
  "execution_timestamp": "2025-10-06T12:05:00Z",
  "failure_details": {
    "failure_type": "library_not_found",
    "reasons": [
      "Library 'custom-internal-lib' not indexed in Context7",
      "No matching libraries found with trust >= 7"
    ],
    "research_attempted": {
      "resolve_queries": ["custom-internal-lib", "custom_internal_lib", "internal-lib"],
      "libraries_found": [],
      "tokens_used": 0
    },
    "partial_results": null,
    "recovery_suggestions": [
      {
        "approach": "Delegate to researcher-web",
        "rationale": "Library not in Context7, use web search for unofficial docs",
        "delegation": {
          "worker_type": "researcher-web",
          "query_refinement": "Search 'custom-internal-lib documentation API reference'"
        }
      },
      {
        "approach": "Delegate to researcher-codebase",
        "rationale": "If this is an internal library, check local codebase for usage patterns",
        "delegation": {
          "worker_type": "researcher-codebase",
          "query_refinement": "Search for custom-internal-lib imports and usage in packages/"
        }
      }
    ]
  }
}
```

---

## Iteration Support Example

When confidence is below 0.85 threshold:

```json
{
  "status": "SUCCESS",
  "confidence": 0.78,
  "agent_specific_output": {
    "findings": { "..." },
    "iteration_support": {
      "open_questions": [
        {
          "question": "How does FastAPI handle WebSocket reconnection with authentication?",
          "context": "Official docs cover basic WebSocket usage but production reconnection with auth not documented",
          "priority": "high",
          "suggested_approach": "researcher-web for production WebSocket patterns and community examples"
        }
      ],
      "confidence_breakdown": {
        "overall_confidence": 0.78,
        "confidence_factors": {
          "documentation_completeness": 0.85,
          "version_accuracy": 0.90,
          "example_quality": 0.60
        },
        "low_confidence_rationale": [
          "WebSocket reconnection not covered in official FastAPI docs",
          "Authentication integration with WebSockets only has basic example"
        ],
        "confidence_improvement_actions": [
          "Search for FastAPI WebSocket production patterns (researcher-web)",
          "Find community examples of authenticated WebSocket reconnection"
        ]
      }
    }
  }
}
```

---

## Quality Threshold Failure Example

```json
{
  "status": "FAILURE",
  "agent": "researcher-library",
  "confidence": 0.4,
  "failure_details": {
    "failure_type": "quality_threshold_not_met",
    "reasons": [
      "Trust score 6.5 below minimum threshold 7.0",
      "Insufficient curation quality for authoritative research"
    ],
    "research_attempted": {
      "resolve_queries": ["obscure-framework"],
      "libraries_found": ["/obscure/framework"],
      "tokens_used": 100
    },
    "recovery_suggestions": [
      {
        "approach": "Delegate to researcher-web",
        "rationale": "Borderline trust scores indicate incomplete Context7 coverage"
      }
    ]
  }
}
```

---

## Rate Limit Exceeded Example

```json
{
  "status": "FAILURE",
  "agent": "researcher-library",
  "confidence": 0.0,
  "failure_details": {
    "failure_type": "context7_unavailable",
    "reasons": [
      "Context7 MCP rate limit reached after 3 attempts"
    ],
    "research_attempted": {
      "attempts": 3,
      "backoff_used": "exponential (2s, 4s)",
      "total_wait_time_seconds": 6
    },
    "recovery_suggestions": [
      {
        "approach": "Retry after 60 seconds",
        "rationale": "Context7 rate limits typically reset within 60s"
      },
      {
        "approach": "Delegate to researcher-web",
        "rationale": "Alternative source while waiting for rate limit reset"
      }
    ]
  }
}
```

---

## Parallel Execution Context

researcher-library can run alongside other researchers for multi-source research:

```
# Parallel delegation from researcher-lead
Task(researcher-library, "Pydantic v2 async validation - official patterns")
Task(researcher-codebase, "How async validation is used in packages/core/")
Task(researcher-web, "Industry best practices for async validation")

# Orchestrator synthesizes: official (0.90) + local (0.85) + community (0.85)
```
