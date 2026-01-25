---
title: "Research Patterns Guide"
date: 2025-11-08
status: ACTIVE
tags: [claude-docs]
---
# Research Patterns Guide

**Purpose**: Research strategies and patterns from Anthropic Multi-Agent Research System for efficient, high-quality research orchestration

**Referenced by**: researcher-lead, researcher-codebase, researcher-external

## Query Classification

### Breadth-First

**Pattern**: Multiple parallel research streams
**Example**: "Analyze all S&P 500 tech companies board members"
**Approach**: Deploy many workers (10+), each handling independent subtask
**Benefits**: Massive parallelization, 90% time reduction

### Depth-First

**Pattern**: Multiple perspectives on single issue
**Example**: "Investigate semiconductor shortage from government, industry, expert perspectives"
**Approach**: 3-5 workers, each exploring different angle
**Benefits**: Comprehensive understanding, diverse viewpoints

### Straightforward

**Pattern**: Focused, well-defined question
**Example**: "What's the current JWT best practice?"
**Approach**: 1-2 workers, direct research
**Benefits**: Simple, fast, efficient

## Explicit Scaling Rules

**Simple (1 worker, 3-10 tool calls)**:

- Fact-finding from known sources
- Single-source verification
- Straightforward queries

**Moderate (3-5 workers, 10-15 calls each)**:

- Direct comparisons
- Multi-source validation
- Moderate complexity research

**Complex (10+ workers, clearly divided)**:

- Breadth-first exploration
- Multiple independent streams
- Large-scale analysis

## Search Strategy: Start Wide, Then Narrow

**Phase 1 - Broad Discovery** (<5 word queries):

- "authentication patterns"
- "microservices architecture"
- "API design"

**Phase 2 - Evaluate Landscape**:

- Assess available sources
- Identify authoritative content
- Note information gaps

**Phase 3 - Progressive Narrowing**:

- "JWT refresh token implementation"
- "saga pattern microservices"
- "REST vs GraphQL tradeoffs"

**Phase 4 - Targeted Deep-Dive**:

- Specific file/URL investigation
- Detailed analysis
- Gap filling

## Four-Component Delegation

Every worker delegation MUST include:

**1. Specific Objective** - One core goal

- ❌ BAD: "Research semiconductor shortage"
- ✅ GOOD: "Investigate US government response: check CHIPS Act at commerce.gov, focus on funding allocation, timeline, projected capacity increases"

**2. Output Format** - Exact return structure

- List of entities with attributes
- Dense report with findings
- Question answer with confidence
- **Always compressed essentials**

**3. Tool & Source Guidance** - Preferences and reliability

- Authoritative sources over SEO farms
- Academic PDFs over blog posts
- Official docs over tutorials
- Start broad, narrow progressively

**4. Task Boundaries** - Clear scope limits

- What to avoid
- Time/depth constraints
- Related topics to exclude
- Prevents duplication and drift

## Orchestrator-to-researcher-lead Contract

**Critical Invocation Pattern**:

- **Phrase**: "CREATE A RESEARCH PLAN for [objective]"
- **Not**: "Investigate" or "Research" (triggers execution mode)
- **Purpose**: Ensure researcher-lead returns plan, not executes research

**Expected Flow**:

```
1. Orchestrator → researcher-lead: "CREATE A RESEARCH PLAN..."
2. researcher-lead → Orchestrator: {delegation_plans: [...]}
3. Orchestrator spawns workers from delegation_plans (parallel Task calls)
4. Workers → Orchestrator: {findings with iteration_support}
5. Orchestrator synthesizes findings
6. IF gaps detected → GOTO step 1 with iteration_context
7. Present synthesized findings to user
```

**Concrete Example**:

```markdown
❌ WRONG INVOCATION:
Task(
agent="researcher-lead",
prompt="Research async validation patterns in Pydantic v2"
)
→ researcher-lead executes research (99.4k tokens, 3m 53s)
→ No worker delegation, all work done by lead

✅ CORRECT INVOCATION:
Task(
agent="researcher-lead",
prompt="CREATE A RESEARCH PLAN for researching async validation patterns in Pydantic v2"
)
→ researcher-lead returns plan: {delegation_plans: [web_1, web_2, library_1]}
→ Orchestrator spawns 3 workers in parallel (single message, multiple Task calls)
→ Workers execute research (5-10k tokens each, 2-3 min parallel)
→ Orchestrator synthesizes 3 worker findings into comprehensive answer
→ Total: 15-30k tokens, 2-3 minutes (vs 99.4k, 3m 53s with wrong invocation)
```

**Output Contract**:

```typescript
researcher-lead returns:
  status: "SUCCESS"
  agent_specific_output:
    research_plan:
      delegation_plans: Array<{
        worker_type: "researcher-external" | "researcher-codebase"
        worker_id: string
        specific_objective: string
        output_format: string
        tool_guidance: {...}
        task_boundaries: {...}
      }>
      execution_guidance:
        parallel_execution: boolean
        synthesis_approach: string

Orchestrator processes:
  1. Parse delegation_plans array
  2. Spawn workers with single message (multiple Task calls)
  3. Wait for all workers to complete
  4. Synthesize using execution_guidance.synthesis_approach
  5. Check iteration_support.open_questions and confidence
  6. If gaps → Call researcher-lead again with iteration_context
```

**Token Efficiency**:

- researcher-lead planning: 5-10k tokens, <30 seconds
- Workers (parallel): 5-10k tokens each, 2-3 minutes total
- Wrong invocation (lead executes): 99.4k tokens, 3m 53s
- **Savings**: 70-90% token reduction, similar execution time (parallel workers)

## Compression Patterns

**Worker-Level Compression** (10:1 ratio):

- 200k codebase analysis → 20k key findings
- Extract patterns, not exhaustive lists
- Representative examples (1-2, not all)
- High-confidence insights prioritized

**Lead-Level Compression** (5:1 additional):

- 100k worker findings → 20k synthesized report
- Remove redundancy across workers
- Consolidate overlapping insights
- Actionable conclusions only

**Overall Target**: 50:1 for complex multi-agent research

## Source Quality Heuristics

**Authoritative (Highest Priority)**:

- Official documentation
- Academic papers (.edu)
- Government sources (.gov)
- Framework maintainer content

**Supporting (Medium)**:

- Established technical authors
- Conference talks
- Well-known tech blogs
- GitHub from maintainers

**Reject (Ignore)**:

- SEO content farms
- Unverified tutorials
- Outdated content
- No clear authorship

## Anti-Patterns to Avoid

**Resource Misallocation**:

- ❌ 50 workers for simple query
- ❌ Endless searching for nonexistent sources
- ❌ Vague delegation causing duplication

**Search Quality Issues**:

- ❌ Overly specific queries returning nothing
- ❌ SEO farms over authoritative sources
- ❌ Accepting first results without quality check

**Parallelization Failures**:

- ❌ Tight dependencies between workers
- ❌ Shared context requirements
- ❌ Coding tasks (fewer parallel opportunities)

## Memory Management for Long Research

**When to Use Memory Tool**:

- Research >200k tokens expected
- Multiple session continuation
- Complex multi-phase investigation

**What to Store**:

- Research plan before worker deployment
- Intermediate findings from workers
- Compression decisions
- Phase summaries

**Retrieval Strategy**:

- Load plan when approaching context limits
- Retrieve specific findings as needed
- Maintain continuity across fresh contexts

## Token Economics

**Trade-offs**:

- Agents: 4x tokens vs chat
- Multi-agent: 15x tokens vs chat
- **Value Justification**: Use for high-value tasks only

**Performance**:

- Token usage explains 80% variance
- Latest models = efficiency multipliers
- sonnet for coordination, Sonnet for workers = cost optimization

---

**Reference**: `docs/04-guides/domain-specific/Anthropic Multi-Agent Research System.md`
