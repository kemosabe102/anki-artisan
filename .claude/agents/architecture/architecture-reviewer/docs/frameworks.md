# Architecture Reviewer Frameworks

## Review Workflow (5 Phases)

### Phase 1: Input Analysis & Technical Assessment (30-60s)
1. Load and parse PLAN.md files + source SPEC.md
2. Load Component Almanac (`docs/00-project/COMPONENT_ALMANAC.md`)
3. Technical Placeholder Census - scan for `[Architecture.*]`, `[Technology.*]`, etc.
4. Code Reuse Analysis - check "Existing Code Analysis" section

### Phase 1.5: Critical Concept Research (MANDATORY - 180-300s)

**NO EXCEPTIONS - Research 3 critical concepts before ANY scoring**

1. **Extract 3 Critical Concepts**: Prioritize by (Impact×0.5) + (Complexity×0.3) + (Risk×0.2)
2. **Classify Each**:
   - TECHNICAL (library/API) → Context7
   - ABSTRACT (pattern/principle) → Perplexity
   - HYBRID → Context7 FIRST, then Perplexity
3. **Execute Research**:
   - Context7: 5000-8000 tokens per concept
   - Perplexity: Variable depth for trade-offs
4. **Document Findings**: Source attribution, confidence scoring

### Phase 2: Traceability & Quality Analysis (60-90s)
1. Extract all FR_IDs from SPEC.md
2. Map FR_IDs → plan components → implementation tasks
3. Calculate coverage (target: 95%+)
4. Apply stage-specific quality gates


### Phase 3: Integration & Risk Analysis (120-180s)
1. Apply Quality Matrix (8 criteria with research-backed evidence)
2. Interface Analysis - compare definitions across plans
3. Dependency Mapping - identify conflicts
4. Latency Budget Analysis - validate allocations
5. Risk Assessment - P×I×E scoring with mitigations

### Phase 4: Report Generation (60-120s)
1. Generate Technical Review Report (schema-compliant)
2. Create Technical Edit Plan with unified diff patches
3. Document research findings with sources
4. Synthesize top 5 recommendations

### Phase 5: Validation (30s)
1. Schema validation for both outputs
2. Zero mutation verification
3. SLO/SLI compliance tracking

---

## Research Protocol

### Decision Matrix

| Need | Tool | Cost |
|------|------|------|
| Library/framework standards | Context7 FIRST | Free |
| Context7 quality (trust≥7) | Context7 ONLY | Free |
| Architectural trade-offs | Perplexity | $0.003-0.005 |
| Industry best practices | Perplexity | $0.005-0.010 |

**Target Ratio**: Context7:Perplexity = 3:1 (75%/25%)
**Avg Cost Per Review**: < $0.02


### Concept Classification Examples

| Concept | Type | Tool | Query Pattern |
|---------|------|------|---------------|
| "Kafka event streaming" | TECHNICAL | Context7 | "[library] best practices" |
| "CQRS with event sourcing" | ABSTRACT | Perplexity | "[pattern] trade-offs 2025" |
| "Multi-tenant isolation" | HYBRID | Both | Context7 first, then Perplexity |

---

## Framework Visibility Modes

### Explicit Mode (Default)
Show framework annotations in output:
```markdown
**[FRAMEWORK: Quality Matrix - Architecture Soundness]**
- Score: 4.0/5.0
- Evidence: Context7 validated Kafka partition strategy
- Finding: Recommend LZ4 compression for 40% throughput gain
```

### Silent Mode
Show results only:
```markdown
## Architecture Soundness: 4.0/5.0
Kafka partition strategy validated. Recommend LZ4 compression.
```

---

## Error Recovery Protocol

| Error Type | Retry Strategy | Fallback |
|------------|----------------|----------|
| File access | 3x with 1s/2s/4s delays | Escalate to orchestrator |
| Context7 timeout | 2x with 2s/5s delays | Fallback to Perplexity |
| Perplexity rate limit | Wait 10s, retry 1x | Defer to manual phase |
| Schema validation | Log, continue best-effort | Flag as incomplete |

### Circuit Breaker Thresholds
- Research API: 3 consecutive failures → skip remaining, use cached
- File reads: 5 consecutive errors → abort with FAILURE
