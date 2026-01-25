---
name: reviewing-architecture
description: >
  Use this skill when validating PLAN.md architecture, applying stage-specific quality gates 
  (MVP/Alpha/Beta/GA), calculating 8-criterion quality matrix, or assessing FR_ID traceability. 
  Trigger keywords: architecture review, stage gates, quality matrix, traceability, production readiness.
---

# Reviewing Architecture Skill

> **Read-only technical analysis. Generate reports - never modify source files.**

---

## Contents

1. [Disney Creative Strategy - DREAMER to REALIST Lens](#disney-creative-strategy---dreamer-to-realist-lens)
2. [8-Criterion Quality Matrix](#8-criterion-quality-matrix)
3. [Stage-Specific Quality Thresholds](#stage-specific-quality-thresholds)
4. [FR_ID Traceability Calculation](#fr_id-traceability-calculation)
5. [5-Phase Review Workflow](#5-phase-review-workflow)
6. [Research Protocol](#research-protocol)
7. [Confidence Scoring](#confidence-scoring)
8. [5W1H Review Framework](#5w1h-review-framework)
9. [Anti-Patterns](#anti-patterns-never-do)
10. [Quick Reference](#quick-reference)

---

## Disney Creative Strategy - DREAMER to REALIST Lens

Apply the Disney Creative Strategy framework during architecture reviews.


### Mindset Transition

| Phase | Focus | Key Question |
|-------|-------|--------------|
| **Dreamer** | Technical Vision | What's the best possible architecture? |
| **Dreamer** | Innovation | Are we leveraging optimal patterns? |
| **Realist** | Feasibility | Can we build this with current stack? |
| **Realist** | Constraints | What technical limits apply? |
| **Bridge** | Trade-offs | What compromises balance vision vs reality? |

### Application Process

1. **First (Dreamer)**: What's the ideal technical vision?
2. **Then (Realist)**: Is this vision technically feasible?
3. **Bridge**: How do we achieve the vision within constraints?

**Output Tone**: Aspirational but grounded. Start with what's ideal, then validate against reality.

---

## 8-Criterion Quality Matrix

Evaluate architecture using 8 weighted criteria. Each score is 1-5 scale.

**Detailed Rubric**: [Scoring Rubric](references/scoring-rubric-summary.md)

### Criteria Weights

| Criterion | Weight | Confidence Source |
|-----------|--------|-------------------|
| **Architecture Soundness** | 0.25 | Pattern analysis depth + research hits |
| **Implementation Readiness** | 0.20 | Code coverage + task decomposition clarity |
| **Production Readiness** | 0.15 | NFR validation + monitoring evidence |

| **Code Reuse Effectiveness** | 0.15 | Almanac cross-reference completeness |
| **Integration Coherence** | 0.10 | Interface documentation + data flow analysis |
| **Cleanup & Debt** | 0.07 | Debt tracking + deprecation plan presence |
| **Risk Mitigation** | 0.05 | Risk register completeness + mitigation quality |
| **Standards Compliance** | 0.03 | Compliance checklist coverage |

### Overall Score Formula

```
Overall Score = (Architecture × 0.25) + (Implementation × 0.20) + (Production × 0.15) 
              + (Reuse × 0.15) + (Integration × 0.10) + (Cleanup × 0.07) 
              + (Risk × 0.05) + (Standards × 0.03)
```

**Score Range**: 1.0 - 5.0

---

## Stage-Specific Quality Thresholds

Different development stages require different minimum scores.

| Stage | Min Score | Key Focus Areas |
|-------|-----------|-----------------|
| **MVP** | 3.5+ | Speed & Feasibility - core functionality works |
| **Alpha** | 3.7+ | Stabilize Core - major bugs addressed |
| **Beta** | 3.8+ | Resilience & Scale - handles load, recovers from failures |
| **GA** | 4.2+ | Full Rigor - production-ready, comprehensive coverage |


### Stage Detection

```
IF request contains "MVP" THEN stage=MVP
IF request contains "Alpha" THEN stage=Alpha
IF request contains "Beta" THEN stage=Beta
IF request contains "GA" OR "production ready" THEN stage=GA
DEFAULT: ASK user OR stage=MVP
```

---

## FR_ID Traceability Calculation

Measure how well the PLAN.md maps to SPEC.md requirements.

### FR_ID Pattern

```regex
FR-[A-Z]{2,4}-\d{3,4}
```

**Examples**: `FR-AUTH-001`, `FR-DATA-0012`, `FR-API-123`

### Calculation Process

```
1. Extract all FR_IDs from SPEC.md → spec_fr_ids
2. Extract all FR_IDs from PLAN.md → plan_fr_ids
3. Traceability = |plan_fr_ids ∩ spec_fr_ids| / |spec_fr_ids| × 100
```

### Traceability Thresholds

| Coverage | Status | Action |
|----------|--------|--------|
| ≥95% | **PASS** | Excellent traceability |
| 80-94% | **WARN** | Review unmapped requirements |
| <80% | **FAIL** | Significant gaps, recommend enhancement |


**Special Case**: If SPEC.md missing, cap traceability at 60% and add WARNING to report.

---

## 5-Phase Review Workflow

### Phase 1: Input Analysis (30-60s)

1. Load and parse PLAN.md files + source SPEC.md
2. Load Component Almanac (`docs/00-project/COMPONENT_ALMANAC.md`)
3. Technical Placeholder Census - scan for `[Architecture.*]`, `[Technology.*]`
4. Code Reuse Analysis - check "Existing Code Analysis" section

### Phase 1.5: Critical Concept Research (MANDATORY - 180-300s)

**NO EXCEPTIONS - Research 3 critical concepts before ANY scoring**

1. **Extract 3 Critical Concepts**: Prioritize by `(Impact×0.5) + (Complexity×0.3) + (Risk×0.2)`
2. **Classify Each**:
   - TECHNICAL (library/API) → Context7
   - ABSTRACT (pattern/principle) → Perplexity
   - HYBRID → Context7 FIRST, then Perplexity
3. **Execute Research**: Context7 5000-8000 tokens per concept
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
2. Zero mutation verification (confirm no source files modified)
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


### Target Ratio

**Context7:Perplexity = 3:1 (75% Context7 / 25% Perplexity)**

- Context7 is FREE - use first for all technical queries
- Perplexity is PAID - reserve for abstract patterns and trade-offs
- Average cost per review: < $0.02

### Concept Classification Examples

| Concept | Type | Tool | Query Pattern |
|---------|------|------|---------------|
| "Kafka event streaming" | TECHNICAL | Context7 | "[library] best practices" |
| "CQRS with event sourcing" | ABSTRACT | Perplexity | "[pattern] trade-offs 2025" |
| "Multi-tenant isolation" | HYBRID | Both | Context7 first, then Perplexity |

---

## Confidence Scoring

Each criterion score MUST include a confidence level based on evidence quality.

### Confidence Thresholds

| Confidence | Threshold | Meaning | Evidence Basis |
|------------|-----------|---------|----------------|
| **HIGH** | ≥0.85 | Strong evidence | Code analysis + research validation |
| **MEDIUM** | 0.70-0.84 | Partial evidence | Pattern inference, partial coverage |
| **LOW** | <0.70 | Limited evidence | Assumptions, flag for follow-up |

### Output Rules

- All scores with LOW confidence (<0.70) MUST include `[NEEDS_REVIEW]` flag
- HIGH confidence requires both code analysis AND research validation
- MEDIUM confidence acceptable for non-critical criteria


---

## 5W1H Review Framework

Apply structured analysis to every architecture review.

| Dimension | Question | Focus Area |
|-----------|----------|------------|
| **What** | What is being built? | Components, boundaries, scope |
| **Why** | Why this architecture? | Rationale, alternatives considered |
| **Where** | Where does it fit? | Integration points, system context |
| **When** | When are milestones? | Timeline, dependencies, blockers |
| **Who** | Who owns what? | Responsibilities, expertise required |
| **How** | How will it work? | Implementation approach, patterns |

### Application

1. Answer each question during Phase 1 (Input Analysis)
2. Identify gaps where questions cannot be answered
3. Flag unanswered questions in the review report

---

## Anti-Patterns (NEVER DO)

| Anti-Pattern | Why It's Wrong | Correct Approach |
|--------------|----------------|------------------|
| Skip mandatory research phase | Scores become opinion-based | ALWAYS research 3 concepts |
| Opinion-based scoring | No evidence = unreliable | MUST cite research sources |
| Modify source files | Violates read-only boundary | Generate report/edit plan only |
| Spawn other agents | Worker agent, not orchestrator | Return results to caller |
| Score without confidence | Hides uncertainty | Include confidence per criterion |


---

## Quick Reference

### Metrics Summary

| Metric | Formula/Target |
|--------|----------------|
| **Overall Score** | Sum(Criterion × Weight) across 8 criteria |
| **Traceability** | FR_IDs_mapped / FR_IDs_total × 100 → Target: ≥95% |
| **Research Coverage** | decisions_researched / total_decisions × 100 → Target: ≥80% |
| **Review SLO** | P95 < 600s (10 min), research phase 300s standard |

### Stage Gates (Min Scores)

| MVP | Alpha | Beta | GA |
|-----|-------|------|-----|
| 3.5+ | 3.7+ | 3.8+ | 4.2+ |

### Pre-Flight Checklist

| Check | Condition | Action |
|-------|-----------|--------|
| PLAN.md exists | IF missing | ABORT with guidance |
| Stage specified | IF missing | ASK user OR DEFAULT to MVP |
| SPEC.md check | IF missing | WARN, cap traceability at 60% |
| File count | IF >10 files | WARN about extended review time |

### Error Recovery

| Error Type | Retry Strategy | Fallback |
|------------|----------------|----------|
| File access | 3x with 1s/2s/4s delays | Escalate to orchestrator |
| Context7 timeout | 2x with 2s/5s delays | Fallback to Perplexity |
| Perplexity rate limit | Wait 10s, retry 1x | Defer to manual phase |
| Schema validation | Log, continue best-effort | Flag as incomplete |

### Circuit Breaker Thresholds

- Research API: 3 consecutive failures → skip remaining, use cached
- File reads: 5 consecutive errors → abort with FAILURE
