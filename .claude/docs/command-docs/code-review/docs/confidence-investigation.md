# Confidence-Driven Investigation Protocol

Phase 4 of the /code-review workflow - increasing finding confidence via delegated research.

---

## Overview

**Purpose**: Ensure all reported findings have confidence >= 0.75 through research delegation.

**Key Difference from /review**: Instead of direct MCP tool calls, all research is delegated to:
- `researcher-external` (replaces mcp__context7__* and mcp__perplexity__*, auto-routes)

**Principle**: NO LOW-CONFIDENCE FINDINGS reported as facts.

---

## Confidence Bands & Actions

| Confidence | Band | Action Required |
|------------|------|-----------------|
| >= 0.90 | HIGH | Report as-is, no investigation |
| 0.75-0.89 | MEDIUM | Optional Task(researcher-external) |
| < 0.75 | LOW | MANDATORY Task(researcher-external) |
| < 0.50 after research | UNRESOLVABLE | Escalate to "Open Questions" |

---

## Step 4.1: Confidence Assessment

For EACH finding from all agents:

```yaml
initial_confidence_check:
  - Extract finding confidence score (0.0-1.0)
  - Extract source_agent (for conflict tracking)
  - Route based on confidence band:
    - >= 0.90: HIGH -> No investigation needed
    - 0.75-0.89: MEDIUM -> Optional library research
    - < 0.75: LOW -> MANDATORY investigation
```


---

## Step 4.2: Library Research (Delegated)

**Trigger**: Finding confidence 0.75-0.89 OR < 0.75

**Delegation Pattern**:

```
Task(
  subagent_type="researcher-external",
  description="Validate finding against library documentation",
  prompt="Validate code review finding:
    
    Finding ID: {finding.finding_id}
    Finding Message: {finding.message}
    Location: {finding.location}
    Current Confidence: {finding.confidence}
    
    Extract and research:
    - Library/framework mentioned (e.g., 'fastapi', 'sqlalchemy')
    - Specific topic (e.g., 'async dependency injection')
    
    Steps:
    1. Resolve library to documentation source
    2. Find relevant documentation section
    3. Validate finding against official docs
    
    Return JSON:
    {
      library: string,
      topic: string,
      validation_result: 'confirmed' | 'contradicted' | 'ambiguous',
      confidence_delta: float,  # +0.10 if confirmed, -0.20 if contradicted
      source_citation: string,
      evidence_summary: string
    }"
)
```

**Confidence Update Rules**:
- Docs confirm issue: `confidence += 0.10` (cap at 0.95)
- Docs contradict: downgrade to "Open Question" (`confidence < 0.50`)
- Docs ambiguous: maintain confidence, note uncertainty


---

## Step 4.3: Web Research (Delegated)

**Trigger**: Finding confidence < 0.75 after library research

**Delegation Pattern**:

```
Task(
  subagent_type="researcher-external",
  description="Deep research on low-confidence finding",
  prompt="Research code review finding via web sources:
    
    Finding ID: {finding.finding_id}
    Finding Message: {finding.message}
    Context: {finding.problem}
    Current Confidence: {finding.confidence}
    
    Library Research Result: {library_research_result}
    
    Research Query: Convert finding to question form
    Example: 'Is using requests.get() in async Python blocking?'
    
    Cross-reference with:
    - OWASP standards (for security findings)
    - PEP guidelines (for Python style/patterns)
    - RFC specifications (for protocol issues)
    - Community best practices
    
    Return JSON:
    {
      query_used: string,
      consensus_level: 'strong' | 'moderate' | 'none',
      recommended_confidence: float,
      sources: [
        {url: string, title: string, trust_score: float}
      ],
      synthesis: string,
      standards_referenced: string[]
    }"
)
```

**Confidence Update Rules**:
- Strong consensus: `confidence = 0.80-0.90`
- Moderate consensus: `confidence = 0.70-0.79`
- No consensus: `confidence` remains < 0.70 -> ESCALATE


---

## Step 4.4: User Escalation

**Trigger**: Confidence remains < 0.50 after both research phases

**Action**: Move to "Open Questions" section

```yaml
escalate_to_open_questions:
  finding_id: {finding.finding_id}
  original_message: {finding.message}
  initial_confidence: {finding.initial_confidence}
  
  research_attempts:
    researcher_library:
      result: {validation_result}
      evidence: {evidence_summary}
    researcher_web:
      result: {consensus_level}
      sources_count: {len(sources)}
  
  why_unresolvable: |
    Conflicting information from sources OR
    No authoritative documentation found OR
    Novel pattern not covered in standards
  
  recommendation: "Manual code review required"
  flag: "NEEDS VERIFICATION"
```

**Example Output**:
```
Open Question (Escalated):
- Issue: "Potential race condition in cache invalidation"
- Initial Confidence: 0.45
- Research Trail:
  - researcher-external: Ambiguous (Redis docs unclear on threading, 3 web sources conflicting)
- Gap: Cannot determine safety without:
  - Understanding thread model
  - Reviewing cache access patterns
  - Load testing under concurrency
- Recommendation: Manual review + load testing
- DO NOT assume this is a bug
```


---

## Investigation Trail Schema

Every investigated finding includes:

```json
{
  "finding_id": "AUTH-001",
  "source_agent": "python-code-reviewer",
  "investigation_trail": {
    "initial_confidence": 0.72,
    "researcher_library_result": {
      "library": "pydantic",
      "topic": "Optional field validation",
      "validation_result": "confirmed",
      "confidence_delta": 0.15,
      "source_citation": "Pydantic v2 Field Validation Guide"
    },
    "researcher_web_result": null,
    "final_confidence": 0.87,
    "sources": [
      "researcher-external: Pydantic Field Validation (trust: 9/10)"
    ]
  }
}
```

---

## Cost Optimization

**Target Ratio**: 4:1 Context7:Perplexity (managed internally by researcher-external)

- `researcher-external`: Uses Context7 (free, authoritative) and Perplexity (paid, synthesis) with auto-routing

**Strategy**:
1. ALWAYS delegate to researcher-external (auto-routes Context7 first, Perplexity if needed)
3. Track ratio in Investigation Summary section

**Investigation Summary Example**:
```
Investigation Summary:
- Total Findings Investigated: 8
- researcher-external calls: 8 (Context7: 6/75%, Perplexity: 2/25%)
- Ratio: 3:1 (target: 4:1) - ACCEPTABLE
- Confidence Boosts: 5 findings improved
- Escalated to Open Questions: 1 finding
```

---

## Critical Severity Override

**Rule**: Critical findings ALWAYS get full investigation regardless of initial confidence.

```yaml
critical_severity_override:
  trigger: finding.severity == "Critical"
  action: |
    ALWAYS run BOTH:
    1. Task(researcher-external, ...)
    
    Even if initial confidence >= 0.90
    
  rationale: Security issues require validation regardless of agent confidence
```
