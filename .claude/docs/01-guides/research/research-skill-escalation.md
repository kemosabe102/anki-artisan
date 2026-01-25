# Research Skill Escalation Reference

**Purpose**: Decision framework for escalating through codebase → library → web research chain

**Version**: 1.0.0 | **Last Updated**: 2025-12-13

---

## Escalation Chain

```
researcher-codebase → researcher-external
     (local)              (external: official + community)
```

**Cost Optimization**: Context7 (free) before Perplexity (paid). Target ratio: 4:1.

---

## Query Type Decision Tree

### Type 1: Implementation Details
**Signals**: "how does X work", "find existing implementation", "locate code for Y"
**Primary Skill**: `researcher-codebase` (ASC: 0.95)
**Escalation**: None unless not found locally

### Type 2: API/Library Usage
**Signals**: "official docs", "API reference", "library parameters", "method signature"
**Primary Skill**: `researcher-external` (ASC: 0.90)
**Escalation**: None (unified agent handles Context7 first, then Perplexity)

### Type 3: Best Practices
**Signals**: "best practice", "recommended pattern", "industry standard", "common approach"
**Primary Skill**: `researcher-external` (ASC: 0.85)
**Escalation**: None (unified agent handles both library docs and community patterns)

### Type 4: Hybrid (Multi-Skill)
**Signals**: Multiple domains, comparison queries, architecture decisions
**Primary Skill**: ALL THREE in parallel via researcher-lead
**Pattern**: researcher-lead creates delegation plan → orchestrator spawns workers

---

## Handoff Protocol

### Codebase → External Escalation
**Trigger**: Local search returns 0 results, or implementation references external library
**Context to Pass**:
- Search patterns attempted (file globs, grep queries)
- Library/framework name identified
- Specific API/method being researched

**Example**:
```
Task(
  agent="researcher-external",
  prompt="Search for Pydantic async validators (Context7 first, then Perplexity if needed). Codebase search found 0 results. Need official API reference for async_validator decorator usage."
)
```

### External → Codebase Validation
**Trigger**: External pattern found, need to verify local compatibility
**Context to Pass**:
- Pattern/approach discovered
- Source URLs (authoritative only)
- Compatibility concerns

**Example**:
```
Task(
  agent="researcher-codebase",
  prompt="Verify codebase compatibility with FastAPI dependency injection pattern from docs.fastapi.org. Check existing Depends() usage in packages/core/api/"
)
```

---

## Combined Confidence Scoring

### Single-Skill Confidence
```
Skill_CQ = (Result_Quality × 0.50) + (Source_Authority × 0.30) + (Completeness × 0.20)
```

**Factors**:
- **Result_Quality**: Relevance to query, actionability
- **Source_Authority**: Official docs > maintainer content > community
- **Completeness**: All aspects of query addressed

### Multi-Skill Consolidated CQ
```
Research_CQ = (Codebase × 0.60) + (External × 0.40)
```

**Weights Rationale**:
- **Codebase (0.60)**: Ground truth, existing patterns, direct applicability
- **External (0.40)**: Official docs + community validation, best practices (unified researcher-external)

---

## Escalation Thresholds

| Skill CQ | Action |
|----------|--------|
| ≥0.85 | Sufficient, no escalation |
| 0.70-0.84 | Consider escalation for validation |
| <0.70 | MUST escalate to next skill |

**Research_CQ Gate**: ≥0.85 to proceed to DECIDE phase (from `.claude/docs/00-core/orchestrator-thresholds.md`)

---

## Parallel vs Sequential

### Sequential (Default)
**Pattern**: Codebase FIRST → External IF needed (auto-routes Context7 vs Perplexity)
**Use When**:
- Query type clearly matches one skill (ASC ≥ 0.85)
- Cost optimization priority
- Low urgency

### Parallel (Multi-Agent)
**Pattern**: ALL THREE simultaneously via researcher-lead
**Use When**:
- Hybrid query type (ASC < 0.80 for all skills)
- High urgency, time-critical
- Comprehensive research required (depth-first pattern)
**Trade-off**: 3x token cost, 90% time reduction

**Launch Pattern** (from `research-patterns.md`):
```
1. Task(researcher-lead, "CREATE A RESEARCH PLAN for [query]")
2. researcher-lead returns {delegation_plans: [codebase_1, library_1, web_1]}
3. Orchestrator spawns 3 workers (single message, multiple Task calls)
4. Synthesize findings with Research_CQ formula
```

---

## Cost Optimization Rules

### Context7 First (Free)
- researcher-external auto-routes library docs queries to Context7
- Libraries: Python (pypi.org), JavaScript (npm), Go (pkg.go.dev)
- Frameworks: Django, FastAPI, React, Next.js

### Perplexity Second (Paid)
- researcher-external escalates to Perplexity when Context7 returns 0 results
- Focus on: best practices, community patterns, version-specific issues
- Broad queries (≤5 words) for discovery, narrow for deep-dive

**Target Ratio**: 4 Context7 calls : 1 Perplexity call

---

## Research Depth by CQ

**From CLAUDE.md orchestrator research strategy**:

| Initial CQ | Research Depth | Agent Count |
|-----------|----------------|-------------|
| ≥0.80 | Light verification | 1 agent (highest ASC) |
| 0.50-0.79 | Standard depth | 2-3 agents (sequential) |
| <0.50 | Deep investigation | 3-5 agents (parallel via researcher-lead) |

---

## Quick Reference

**Decision Ladder**:
1. Classify query type (implementation/API/best-practice/hybrid)
2. Calculate ASC for each skill
3. If ASC ≥ 0.85: Use primary skill
4. If ASC < 0.85 all skills: Parallel via researcher-lead
5. Execute research, calculate Skill_CQ
6. If Skill_CQ < 0.70: Escalate to next skill
7. Calculate Research_CQ, gate at 0.85

**Handoff Checklist**:
- [ ] Pass search patterns attempted
- [ ] Include library/version info
- [ ] Specify API/feature researched
- [ ] Note source authority level

---

**See Also**:
- `.claude/docs/00-core/orchestrator-thresholds.md` - CQ formulas
- `.claude/docs/00-core/research-patterns.md` - Multi-agent patterns
- `.claude/docs/01-guides/orchestration/orient-research-coordination.md` - Research coordination
