# Confidence-Driven Investigation Protocol

Phase 4 of the /review workflow - automatically increasing finding confidence through research.

---

## Overview

**Purpose**: Ensure all reported findings have confidence >= 0.75, preventing low-confidence speculation from being reported as fact.

**Key Principle**: NO LOW-CONFIDENCE FINDINGS reported as facts. Auto-investigation ensures quality.

---

## Confidence Bands & Actions

| Confidence | Band | Action Required |
|------------|------|-----------------|
| >= 0.90 | HIGH | Report as-is, no investigation |
| 0.75-0.89 | MEDIUM | Optional Context7 validation |
| < 0.75 | LOW | MANDATORY investigation (Context7 -> Perplexity) |
| < 0.50 after research | UNRESOLVABLE | Escalate to "Open Questions" |

---

## Step 4.1: Confidence Assessment

For EACH finding from all agents:

```yaml
initial_confidence_check:
  - Extract finding confidence score (0.0-1.0)
  - Route based on confidence band:
    - >= 0.90: HIGH -> No investigation needed
    - 0.75-0.89: MEDIUM -> Optional Context7 research
    - < 0.75: LOW -> MANDATORY investigation
```

---

## Step 4.2: Context7 Research (Confidence 0.75-0.89)

**Trigger**: Finding confidence between 0.75-0.89

**Protocol**:

```yaml
context7_validation:
  1_extract_keywords:
    - Parse finding message for library/framework names
    - Example: "FastAPI dependency injection not awaited" -> ["fastapi", "async", "dependency injection"]

  2_resolve_library:
    - Use: resolve-library-id(library_name)
    - Example: resolve-library-id("fastapi") -> "/fastapi/fastapi"

  3_fetch_docs:
    - Use: get-library-docs(library_id, topic)
    - Example: get-library-docs("/fastapi/fastapi", topic="async dependency injection")

  4_update_confidence:
    - Docs confirm issue: confidence += 0.10 (cap at 0.95)
    - Docs contradict: downgrade to "Open Question" (confidence < 0.5)
    - Docs ambiguous: maintain confidence, note uncertainty

  5_cite_sources:
    - Add: "Source: Context7 - FastAPI Official Docs (trust: 9/10)"
```

**Example**:
```
Initial: confidence 0.78, "requests.get() blocks event loop in async function"
Context7: Library "httpx", Topic "async vs sync HTTP calls"
Result: Docs confirm "requests library is synchronous, use httpx for async"
Final: confidence 0.88, Citation: "Context7 - httpx Official Docs (trust: 9/10)"
```


---

## Step 4.3: Perplexity Research (Confidence < 0.75)

**Trigger**: Finding confidence < 0.75 (requires deep synthesis)

**Protocol**:

```yaml
perplexity_escalation:
  1_formulate_query:
    - Convert finding to research question
    - Example: "Is using requests.get() in async Python functions a blocking issue?"

  2_execute_research:
    - Use: perplexity_search(query, focus="comprehensive")
    - Synthesize from multiple authoritative sources

  3_cross_reference:
    - Validate against industry standards (OWASP, PEP, RFC)
    - Check for consensus across sources

  4_update_confidence:
    - Strong consensus: confidence = 0.80-0.90
    - Moderate consensus: confidence = 0.70-0.79
    - No consensus: confidence remains < 0.70 -> ESCALATE

  5_document_trail:
    - Add investigation summary to finding
    - Include Perplexity sources with URLs
    - Show confidence progression (initial -> final)
```

**Example**:
```
Initial: confidence 0.65, "Potential SQL injection in query builder"
Query: "Is string concatenation for SQL queries in SQLAlchemy vulnerable to injection?"
Sources: OWASP A01:2021, SQLAlchemy Security Best Practices, NIST Guidelines
Synthesis: "Confirmed - parameterized queries required, string concat vulnerable"
Final: confidence 0.88, Trail: "Perplexity: OWASP A01, SQLAlchemy security docs"
```

---

## Step 4.4: User Escalation (Confidence < 0.50 After Research)

**Trigger**: Confidence remains < 0.50 after Context7 AND Perplexity research

**Protocol**:

```yaml
escalate_to_user:
  1_document_gap:
    - Finding description
    - Initial confidence
    - Research attempts (Context7 result, Perplexity result)
    - Why confidence couldn't be raised

  2_provide_evidence:
    - Sources consulted
    - Conflicting information found
    - Open questions remaining

  3_recommend_action:
    - Manual review required
    - Subject matter expert consultation
    - Additional testing needed

  4_do_not_report_as_fact:
    - Move to "Open Questions" section
    - Flag as "NEEDS VERIFICATION"
    - Include uncertainty explanation
```

**Example Output**:
```
Open Question (Escalated):
- Issue: "Potential race condition in cache invalidation"
- Initial Confidence: 0.45
- Research Trail:
  - Context7 (Redis docs): Ambiguous on multi-threaded cache access
  - Perplexity (3 sources): Conflicting recommendations (locks vs atomic ops)
- Gap: Cannot determine if current implementation is safe without:
  - Understanding thread model (single vs multi-threaded)
  - Reviewing cache access patterns across codebase
  - Testing under concurrent load
- Recommendation: Manual code review + load testing
- DO NOT assume this is a bug - insufficient evidence
```

---

## Investigation Trail Schema

Every investigated finding includes:

```json
{
  "finding_id": "AUTH-001",
  "investigation_trail": {
    "initial_confidence": 0.72,
    "context7_research": {
      "library": "pydantic",
      "topic": "Optional field validation",
      "result": "Confirmed - Optional fields can be None without explicit check",
      "confidence_delta": 0.15
    },
    "perplexity_research": null,
    "final_confidence": 0.87,
    "sources": [
      "Context7: Pydantic Field Validation (trust: 9/10)"
    ]
  }
}
```

---

## Cost Optimization

**Target Ratio**: 4:1 Context7:Perplexity

- Context7: Free, authoritative (official docs)
- Perplexity: Paid, synthesis (community + standards)

**Strategy**:
1. ALWAYS try Context7 first
2. Escalate to Perplexity only if Context7 insufficient
3. Track ratio in Investigation Summary section
