# Context Readiness Assessor - Assessment Examples

## Example 1: High Context_Quality (Immediate PASS)

**Input**:
```json
{
  "task_description": "Add JWT authentication to existing auth service (packages/core/auth/service.py)",
  "domain_scope": ["packages/core/auth/"],
  "requirements": "Use PyJWT library, implement token expiration"
}
```

**Assessment**:
- Domain: packages/core/auth/ (well-documented, existing auth patterns)
- Technology: JWT (standard, well-known)
- Patterns: Existing auth service (clear integration point)

**Context_Quality Calculation**:
| Component | Score | Rationale |
|-----------|-------|-----------|
| Domain_Familiarity | 0.90 | Existing auth service, clear domain |
| Pattern_Clarity | 0.90 | JWT is standard pattern, examples exist |
| Dependency_Understanding | 0.85 | PyJWT library well-documented |
| Risk_Awareness | 0.80 | Security considerations documented |

**Overall CQ**: (0.90 x 0.4) + (0.90 x 0.3) + (0.85 x 0.2) + (0.80 x 0.1) = **0.880**

**Output**: SUCCESS, gate_status = PASS (>= 0.85), no research needed

---

## Example 2: Moderate Context_Quality (1 Iteration)

**Input**:
```json
{
  "task_description": "Implement distributed caching layer using Redis",
  "domain_scope": ["packages/api/", "packages/core/"],
  "requirements": "Reduce API response time from 500ms to <100ms"
}
```

**Iteration 1 - Baseline**:
| Component | Score | Gap Identified |
|-----------|-------|----------------|
| Domain_Familiarity | 0.40 | No existing Redis usage |
| Pattern_Clarity | 0.35 | No caching patterns documented |
| Dependency_Understanding | 0.50 | Redis integration unclear |
| Risk_Awareness | 0.45 | Cache invalidation risks unknown |

**Baseline CQ**: 0.410 (< 0.85, requires research)

**Research Coordinated** (3 agents parallel):
- researcher-external: Redis client docs, TTL patterns
- researcher-codebase: Found 2 in-memory cache examples
- tech-debt-investigator: Cache invalidation patterns

**After Research**:
| Component | Score | Delta |
|-----------|-------|-------|
| Domain_Familiarity | 0.65 | +0.25 |
| Pattern_Clarity | 0.60 | +0.25 |
| Dependency_Understanding | 0.70 | +0.20 |
| Risk_Awareness | 0.70 | +0.25 |

**Updated CQ**: 0.650 (< 0.85, requires additional iteration)

**Output**: gate_status = GATHER_MORE_CONTEXT, continue to iteration 2

---

## Example 3: Low Context_Quality (BLOCKED)

**Input**:
```json
{
  "task_description": "Improve the system",
  "domain_scope": [],
  "requirements": ""
}
```

**All Iterations**:
| Component | Score | Issue |
|-----------|-------|-------|
| Domain_Familiarity | 0.10 | No domain specified |
| Pattern_Clarity | 0.15 | No patterns identifiable |
| Dependency_Understanding | 0.10 | No dependencies specified |
| Risk_Awareness | 0.10 | No context for risks |

**CQ**: 0.115 (no improvement possible without domain context)

**Research Attempted**: Unable to coordinate (no domain = cannot select agents)

**Output**: FAILURE after 3 iterations
```json
{
  "status": "FAILURE",
  "failure_details": {
    "failure_type": "insufficient_context",
    "reasons": [
      "Task description too vague",
      "No domain scope provided",
      "Cannot improve CQ without domain context"
    ],
    "recovery_suggestions": [
      "Request user clarification: Which system? What improvement?",
      "Escalate: Cannot proceed without minimum context"
    ]
  }
}
```

---

## Edge Case Scenarios

### Scenario 4: Timeout During Research (Error Recovery)

**Input**:
- task_description: "Implement OAuth2 flow with PKCE for mobile app"
- Research agents spawned: researcher-external
- researcher-external times out after 5 minutes

**Assessment Process**:
1. Initial CQ: 0.42 (Domain: 0.3, Pattern: 0.5, Dependency: 0.4, Risk: 0.6)
2. researcher-external returns (confidence: 0.82), partial TIMEOUT
3. **Error Recovery**: Exclude timed-out agent, recalculate with available findings
4. Adjusted CQ: 0.58 (improved Domain to 0.55 from web research)

**Output**:
```json
{
  "gate_status": "GATHER_MORE_CONTEXT",
  "context_quality_score": 0.58,
  "research_summary": "Partial research: OAuth2 PKCE patterns gathered from web sources. Library-specific implementation details unavailable (timeout). Recommend retry or manual context injection.",
  "information_gaps": [
    {"component": "pattern_clarity", "gap": "Library-specific PKCE implementation patterns", "severity": "high"}
  ]
}
```

### Scenario 5: Research Agent Conflict (Conflict Resolution)

**Input**:
- task_description: "Add caching layer to API responses"
- researcher-codebase finds: "Existing pattern uses in-memory LRU cache"
- researcher-external finds: "Redis recommended for distributed caching"

**Assessment Process**:
1. Conflict detected: Pattern recommendations differ by >0.30 in approach
2. **Conflict Resolution**: Flag as moderate conflict, check task scope
3. Task is single-service (not distributed) → in-memory pattern preferred
4. Confidence-weighted: researcher-codebase (local context) weighted higher

**Output**:
```json
{
  "gate_status": "PASS",
  "context_quality_score": 0.87,
  "research_summary": "CONFLICT RESOLVED: researcher-codebase recommends LRU cache (local pattern), researcher-external recommends Redis (distributed). Resolution: Task scope is single-service, existing LRU pattern preferred. Redis noted for future scaling consideration.",
  "component_scores": {
    "pattern_clarity": {"score": 0.85, "rationale": "Existing LRU pattern identified, conflict resolved in favor of local consistency"}
  }
}
```

### Scenario 6: Catastrophic Context Collapse (All Components <0.3)

**Input**:
- task_description: "Implement quantum-resistant encryption for data at rest"
- domain_scope: ["packages/crypto/"]
- No existing quantum crypto in codebase

**Assessment Process**:
1. Initial CQ: 0.18 (Domain: 0.1, Pattern: 0.2, Dependency: 0.25, Risk: 0.15)
2. **Catastrophic Collapse Detected**: All components <0.3
3. Gap triage: Prioritize Domain (0.40 weight) and Pattern (0.30 weight) first
4. Spawn max 5 agents on highest-impact gaps
5. Iteration 1: CQ improved to 0.35 (delta +0.17)
6. Iteration 2: CQ improved to 0.48 (delta +0.13)
7. Iteration 3: CQ improved to 0.55 (delta +0.07) - diminishing returns

**Output**:
```json
{
  "gate_status": "BLOCKED",
  "context_quality_score": 0.55,
  "iteration_count": 3,
  "research_summary": "Novel domain: quantum-resistant encryption not present in codebase. After 3 iterations, CQ reached 0.55 (<0.85 threshold). Diminishing returns detected at iteration 3 (delta 0.07).",
  "recovery_suggestions": [
    "Manual context injection: Provide quantum crypto library preferences (e.g., liboqs, PQClean)",
    "Scope reduction: Start with single algorithm (e.g., Kyber-768) before full suite",
    "Domain expert escalation: Consult cryptography specialist for threat model validation"
  ],
  "improvement_tracking": {
    "baseline_score": 0.18,
    "iteration_deltas": [0.17, 0.13, 0.07],
    "total_improvement": 0.37,
    "diminishing_returns_detected": true,
    "diminishing_returns_iteration": 3
  }
}
```

---

## Related Documentation

- [Domain Expertise & Scoring Rubrics](../docs/domain-expertise.md) - Component scoring details
- [Frameworks & Iteration Management](../docs/frameworks.md) - Hermeneutic assessment
- [Schema Contract](../schemas/context-readiness-assessor.schema.json) - Input/output validation
- [Main Agent Definition](../context-readiness-assessor.md) - Core behavior and workflow
