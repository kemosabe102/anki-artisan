# Fallback Strategies Guide

**Purpose**: Framework for generating 2-3 fallback strategies per failure mode with agent recommendations

**Audience**: contingency-planner agent (DECIDE phase component)

**Scope**: Multi-tier fallback approaches (retry same, switch agent, escalate) with success probability scoring

---

## Fallback Strategy Generation

### Core Principle

Generate **2-3 fallback strategies** per failure mode covering different recovery approaches:

1. **Tier 1 (Retry/Optimize)**: Same agent, adjusted approach
2. **Tier 2 (Switch Agent)**: Different agent with complementary expertise
3. **Tier 3 (Escalate)**: Human intervention or user decision

### Systematic Generation Process

**For each failure mode**:

1. Identify 2-3 recovery approaches using multi-tier framework
2. Recommend appropriate agent for each fallback
3. Specify context enhancement needed (research, clarification)
4. Estimate effort (time, complexity)
5. Assess success probability (0.0-1.0)
6. Document rationale and trade-offs

---

## Fallback Strategy Template

```json
{
  "strategy_id": "FB001-1",
  "approach": "Concrete recovery action with clear steps",
  "tier": "retry|agent_switch|context_enhancement|scope_reduction|optimization|escalation",
  "fallback_agent": "agent-name",
  "agent_rationale": "Why this agent is appropriate for fallback",
  "context_enhancement": {
    "research_needed": "Specific research topics or clarification needed",
    "research_agent": "researcher-external|researcher-codebase",
    "estimated_research_time": "30 minutes - 2 hours"
  },
  "effort_estimate": {
    "time_hours": "2-3",
    "complexity": "simple|moderate|complex",
    "sprint_points": 3
  },
  "success_probability": 0.85,
  "success_rationale": "Evidence-based justification for probability",
  "trade_offs": "Key tradeoffs vs original hypothesis (speed/quality/complexity)"
}
```

---

## Multi-Tier Fallback Framework

### Tier 1: Retry/Optimize (Same Agent, Adjusted Approach)

**When to Use**:
- Original approach fundamentally sound
- Issue is configuration, tuning, or missing context
- Agent has capability to resolve with additional information

**Agent Selection**: Same agent as original hypothesis

**Examples**:
- Retry implementation with better Redis configuration
- Optimize algorithm parameters after profiling
- Adjust caching strategy based on performance data

**Success Probability**: Typically **0.7-0.9** (high, since core approach valid)

```json
{
  "strategy_id": "FB001-1",
  "approach": "Research Redis setup best practices and retry original approach",
  "tier": "context_enhancement",
  "fallback_agent": "researcher-external",
  "agent_rationale": "Gather external setup guides before retry with python-code-implementer",
  "context_enhancement": {
    "research_needed": "OWASP Redis security patterns, Docker compose setup, connection pooling",
    "research_agent": "researcher-external",
    "estimated_research_time": "1 hour"
  },
  "effort_estimate": {
    "time_hours": "5-6",
    "complexity": "moderate",
    "sprint_points": 5
  },
  "success_probability": 0.7,
  "success_rationale": "Addresses root cause (proper setup), higher quality outcome",
  "trade_offs": "More effort vs better long-term maintainability"
}
```

---

### Tier 2: Switch Agent (Different Agent, Alternative Approach)

**When to Use**:
- Original agent lacks capability for recovery
- Different expertise needed (debugging vs implementation)
- Alternative technical approach required

**Agent Selection**: Choose agent with complementary expertise from CLAUDE.md

**Agent Mapping**:
- Implementation failure → debugger (hypothesis-driven bug fixing)
- Performance failure → debugger (profiling and optimization)
- Integration failure → researcher-codebase (pattern analysis)
- Security failure → researcher-external (OWASP best practices)
- Test failure → test-creator (test strategy redesign)
- Architecture failure → architecture-enhancer (design improvement)

**Examples**:
- Switch from Redis to in-memory cache (python-code-implementer, simpler approach)
- Engage debugger for performance bottleneck analysis
- Use researcher-external for alternative library investigation

**Success Probability**: Typically **0.6-0.85** (moderate-high, depends on alternative viability)

```json
{
  "strategy_id": "FB001-2",
  "approach": "Switch to in-memory LRU cache implementation",
  "tier": "agent_switch",
  "fallback_agent": "python-code-implementer",
  "agent_rationale": "Same agent, different approach (simpler implementation, no external dependency)",
  "context_enhancement": {
    "research_needed": "Gather in-memory cache patterns from codebase",
    "research_agent": "researcher-codebase",
    "estimated_research_time": "30 minutes"
  },
  "effort_estimate": {
    "time_hours": "2-3",
    "complexity": "simple",
    "sprint_points": 3
  },
  "success_probability": 0.85,
  "success_rationale": "Removes external dependency, uses proven in-memory patterns in codebase",
  "trade_offs": "Lower scalability vs higher reliability, acceptable for MVP"
}
```

---

### Tier 3: Escalate (Human Intervention)

**When to Use**:
- Task exceeds agent capabilities
- Infrastructure provisioning required
- Business/product decision needed
- Ambiguity requires user clarification

**Escalation Reasons**:
- Infrastructure setup outside agent scope (Redis server provisioning)
- Architectural decision requires stakeholder input
- Budget/resource constraints need approval
- Requirements clarification from user

**Examples**:
- Escalate for Redis infrastructure provisioning
- Request user decision on performance vs complexity tradeoff
- Seek architecture review for distributed system design

**Success Probability**: Typically **0.9-1.0** (very high, human resolves blocker)

```json
{
  "strategy_id": "FB001-3",
  "approach": "Escalate to human for Redis infrastructure provisioning",
  "tier": "escalation",
  "escalation_reason": "Infrastructure setup outside agent scope",
  "required_human_action": "Install and configure Redis server with proper security",
  "effort_estimate": {
    "time_hours": "0.5-1",
    "complexity": "simple",
    "sprint_points": 1
  },
  "success_probability": 1.0,
  "success_rationale": "Human handles infrastructure, agent retries implementation with proper setup"
}
```

---

## Success Probability Scoring

### Rubric (0.0-1.0)

**0.9-1.0 - Very High**:
- Human intervention resolves blocker
- Proven fallback in codebase
- Eliminates root cause completely

**0.7-0.89 - High**:
- Strong evidence of success (similar patterns work)
- Removes major risk factor
- Robust error handling

**0.5-0.69 - Medium**:
- Reasonable alternative but untested
- Reduces risk but doesn't eliminate
- Some unknowns remain

**0.3-0.49 - Low**:
- Speculative approach
- Limited evidence of viability
- High residual risk

**0.0-0.29 - Very Low**:
- Unlikely to succeed
- Major blockers remain
- Last resort option

### Calculation Factors

**Evidence of Success** (40% weight):
- Proven in codebase: +0.4
- External examples available: +0.3
- Theoretical viability: +0.2
- No evidence: 0.0

**Risk Reduction** (30% weight):
- Eliminates root cause: +0.3
- Mitigates major risk: +0.2
- Reduces some risk: +0.1
- No risk reduction: 0.0

**Agent Capability** (20% weight):
- Perfect agent fit: +0.2
- Good agent fit: +0.15
- Acceptable fit: +0.1
- Poor fit: 0.0

**Effort Reasonableness** (10% weight):
- Low effort: +0.1
- Medium effort: +0.07
- High effort: +0.05
- Excessive effort: 0.0

---

## Context Enhancement Specification

### Purpose

Define research needed before fallback execution to increase success probability.

### Research Agents

**researcher-external**:
- Use for: Industry best practices, OWASP patterns, external tutorials, library documentation, API references
- Example: "OWASP Redis security patterns, Docker compose setup guides, Redis client library invalidation APIs"
- Estimated time: 30 minutes - 2 hours

**researcher-codebase**:
- Use for: Internal patterns, existing implementations, component analysis
- Example: "Analyze existing cache patterns, identify in-memory implementations"
- Estimated time: 15 minutes - 1 hour

### Template

```json
{
  "context_enhancement": {
    "research_needed": "Specific topics, patterns, or APIs to investigate",
    "research_agent": "researcher-external|researcher-codebase",
    "estimated_research_time": "30 minutes - 2 hours",
    "success_probability_increase": "+0.15 to +0.25"
  }
}
```

---

## Effort Estimation

### Time Estimates (Hours)

**Simple (1-3 hours)**:
- Single file changes
- Configuration adjustments
- Minor logic fixes
- Sprint points: 1-3

**Moderate (3-8 hours)**:
- Multi-file changes
- Integration work
- Research + implementation
- Sprint points: 3-5

**Complex (8+ hours)**:
- Architecture changes
- Cross-module refactoring
- Novel implementations
- Sprint points: 5-8

### Complexity Classification

**Simple**:
- Proven patterns available
- Single agent, single pass
- Clear requirements

**Moderate**:
- Some unknowns
- May require research first
- Integration dependencies

**Complex**:
- Novel approach
- Multiple agents needed
- Significant unknowns

---

## Trade-Off Analysis

### Key Trade-Offs to Document

1. **Speed vs Quality**
   - Fast fallback: Lower quality, technical debt
   - Slow fallback: Higher quality, better long-term

2. **Simplicity vs Scalability**
   - Simple: In-memory cache, limited scale
   - Complex: Distributed cache, higher scale

3. **Risk vs Reward**
   - Safe: Proven approach, lower upside
   - Risky: Novel approach, higher upside

4. **Effort vs Impact**
   - Low effort: Quick win, limited improvement
   - High effort: Major improvement, more risk

### Template

```
"trade_offs": "Lower scalability (in-memory only) vs higher reliability (no external dependency), acceptable for MVP phase"
```

---

## Agent Selection for Fallbacks

### From CLAUDE.md (Best-Fit Patterns)

**Implementation Tasks**:
- Primary: python-code-implementer (packages/**)
- Fallback: Same agent, different approach

**Debugging Tasks**:
- Primary: debugger (hypothesis-driven, 8-step scientific method)
- Context: researcher-codebase (gather patterns first)

**Research Tasks**:
- External: researcher-external (best practices, tutorials, API docs, official guides)
- Codebase: researcher-codebase (internal patterns)

**Testing Tasks**:
- Creation: test-creator (AAA pattern, coverage analysis)
- Execution: test-executor (run tests, categorize failures)
- Fixing: debugger (test failures, bug investigation)

**Architecture Tasks**:
- Review: architecture-review (production readiness, traceability)
- Enhancement: architecture-enhancer (technical specifications)

**Documentation Tasks**:
- Creation: /spec command (SPEC.md generation)
- Enhancement: plan-enhancer (business context)
- Review: spec-reviewer (quality validation)

---

## Complete Fallback Strategy Example

**Failure Mode**: Redis connection failure during implementation

**Fallback Strategies**:

```json
{
  "failure_mode_id": "FM001",
  "fallback_strategies": [
    {
      "strategy_id": "FB001-1",
      "approach": "Switch to in-memory LRU cache implementation",
      "tier": "agent_switch",
      "fallback_agent": "python-code-implementer",
      "agent_rationale": "Same agent, different approach (simpler implementation)",
      "context_enhancement": {
        "research_needed": "Gather in-memory cache patterns from codebase",
        "research_agent": "researcher-codebase",
        "estimated_research_time": "30 minutes"
      },
      "effort_estimate": {
        "time_hours": "2-3",
        "complexity": "simple",
        "sprint_points": 3
      },
      "success_probability": 0.85,
      "success_rationale": "Removes external dependency, uses proven in-memory patterns in codebase",
      "trade_offs": "Lower scalability vs higher reliability"
    },
    {
      "strategy_id": "FB001-2",
      "approach": "Research Redis setup best practices and retry original approach",
      "tier": "context_enhancement",
      "fallback_agent": "researcher-external",
      "agent_rationale": "Gather external setup guides before retry with python-code-implementer",
      "context_enhancement": {
        "research_needed": "OWASP Redis security patterns, Docker compose setup, connection pooling",
        "research_agent": "researcher-external",
        "estimated_research_time": "1 hour"
      },
      "effort_estimate": {
        "time_hours": "5-6",
        "complexity": "moderate",
        "sprint_points": 5
      },
      "success_probability": 0.7,
      "success_rationale": "Addresses root cause (proper setup), higher quality outcome",
      "trade_offs": "More effort vs better long-term maintainability"
    },
    {
      "strategy_id": "FB001-3",
      "approach": "Escalate to human for Redis infrastructure provisioning",
      "tier": "escalation",
      "escalation_reason": "Infrastructure setup outside agent scope",
      "required_human_action": "Install and configure Redis server with proper security",
      "effort_estimate": {
        "time_hours": "0.5-1",
        "complexity": "simple",
        "sprint_points": 1
      },
      "success_probability": 1.0,
      "success_rationale": "Human handles infrastructure, agent retries implementation"
    }
  ]
}
```

---

## Best Practices

1. **Always generate 2-3 fallback strategies** - Provide options for orchestrator decision-making
2. **Use multi-tier framework** - Cover retry, switch, and escalate tiers
3. **Match agents to capabilities** - Use CLAUDE.md agent selection patterns
4. **Specify context enhancement** - Define research needed for success
5. **Estimate effort realistically** - Time, complexity, sprint points
6. **Score success probability** - Evidence-based assessment (0.0-1.0)
7. **Document trade-offs** - Clear comparison with original hypothesis
8. **Justify agent selection** - Explain why this agent is appropriate

---

**Related Guides**:
- `../contingency-planner.md` - Agent definition and workflow integration
- `failure-mode-analysis.md` - Identifying 3-5 failure modes per hypothesis
- `retry-plans.md` - Defining adaptive retry plans with escalation triggers
- `../examples/contingency-examples.md` - Complete examples with failure modes and fallback strategies
