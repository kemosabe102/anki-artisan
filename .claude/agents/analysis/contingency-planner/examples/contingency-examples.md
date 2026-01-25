# Contingency Planning Examples

**Purpose**: Complete examples demonstrating failure mode analysis, fallback strategies, and retry plans

**Audience**: contingency-planner agent (DECIDE phase component)

**Scope**: End-to-end contingency plan generation with full risk analysis

---

## Example 1: Medium-Risk Implementation Hypothesis

**Context**: Standard JWT authentication implementation

### Input (from orchestrator)

```json
{
  "task_id": "task_001",
  "execution_timestamp": "2025-01-15T10:30:00Z",
  "hypotheses": [
    {
      "hypothesis_id": "H001",
      "approach": "Standard JWT implementation with PyJWT library",
      "confidence_score": 0.72,
      "agents_required": ["python-code-implementer"],
      "complexity": "medium",
      "risk_factors": ["JWT library integration", "Token expiration logic"]
    }
  ],
  "context_quality": 0.85,
  "task_context": {
    "user_request": "Implement JWT authentication for the API",
    "domain": "packages/core/auth/",
    "constraints": ["Must use PyJWT library", "Token expiration required"]
  }
}
```

### Analysis

- Risk level: Low (simple library integration)
- Complexity: Moderate (authentication security-critical)
- Domain: packages/core/auth/ → python-code-implementer
- Expected failure modes: 3 (library integration, token logic, testing)

### Contingency Plan Generated

```json
{
  "hypothesis_id": "H001",
  "contingency_plan": {
    "failure_modes": [
      {
        "mode_id": "FM001",
        "description": "PyJWT library integration issues",
        "failure_type": "technical",
        "triggers": ["Import errors", "Version conflicts", "API mismatches"],
        "probability": 0.3,
        "probability_rationale": "External dependency (+0.2), low complexity (+0.1)",
        "impact": 0.5,
        "impact_rationale": "Medium setback - alternative library available",
        "risk_score": 0.15,
        "risk_classification": "low",
        "fallback_strategies": [
          {
            "strategy_id": "FB001-1",
            "approach": "Research PyJWT documentation and retry",
            "tier": "context_enhancement",
            "fallback_agent": "researcher-external",
            "context_enhancement": {
              "research_needed": "PyJWT API reference, examples",
              "estimated_research_time": "30 minutes"
            },
            "effort_estimate": { "time_hours": "1-2", "sprint_points": 2 },
            "success_probability": 0.9,
            "success_rationale": "Official docs resolve API confusion"
          },
          {
            "strategy_id": "FB001-2",
            "approach": "Switch to alternative JWT library (python-jose)",
            "tier": "agent_switch",
            "fallback_agent": "python-code-implementer",
            "effort_estimate": { "time_hours": "3-4", "sprint_points": 4 },
            "success_probability": 0.75,
            "success_rationale": "Alternative library proven in ecosystem"
          }
        ]
      },
      {
        "mode_id": "FM002",
        "description": "Token expiration edge cases not handled correctly",
        "failure_type": "assumption",
        "triggers": ["Clock skew", "Grace period unclear", "Refresh logic bugs"],
        "probability": 0.4,
        "impact": 0.7,
        "risk_score": 0.28,
        "risk_classification": "medium",
        "fallback_strategies": [
          {
            "strategy_id": "FB002-1",
            "approach": "Add comprehensive test coverage for edge cases",
            "tier": "agent_switch",
            "fallback_agent": "test-creator",
            "effort_estimate": { "time_hours": "2-3", "sprint_points": 3 },
            "success_probability": 0.85
          },
          {
            "strategy_id": "FB002-2",
            "approach": "Research JWT expiration best practices (OWASP)",
            "tier": "context_enhancement",
            "fallback_agent": "researcher-external",
            "effort_estimate": { "time_hours": "1 + 2", "sprint_points": 3 },
            "success_probability": 0.8
          }
        ]
      },
      {
        "mode_id": "FM003",
        "description": "Security review identifies vulnerabilities",
        "failure_type": "integration",
        "probability": 0.25,
        "impact": 0.9,
        "risk_score": 0.225,
        "risk_classification": "low",
        "fallback_strategies": [
          {
            "strategy_id": "FB003-1",
            "approach": "Apply security reviewer recommendations and retry",
            "tier": "retry",
            "fallback_agent": "python-code-implementer",
            "success_probability": 0.95
          }
        ]
      }
    ],
    "retry_plan": {
      "max_attempts": 3,
      "max_attempts_rationale": "Low-medium risk (0.28 highest) allows 3 retries",
      "backoff_strategy": "exponential",
      "backoff_intervals": ["1s", "2s", "4s"],
      "escalation_triggers": [
        { "trigger": "retry_count >= 3" },
        { "trigger": "critical_failure", "threshold": "risk_score >= 0.7" }
      ],
      "confidence_decay_model": {
        "initial_confidence": 0.72,
        "decay_per_failure": 0.10,
        "escalation_threshold": 0.3
      }
    },
    "overall_resilience_score": 0.82,
    "resilience_rationale": "3 failure modes, 5 fallback strategies, clear escalation paths"
  }
}
```

---

## Example 2: High-Risk Multi-Component Hypothesis

**Context**: Distributed cache with cross-module integration

### Input (from orchestrator)

```json
{
  "task_id": "task_002",
  "execution_timestamp": "2025-01-15T11:00:00Z",
  "hypotheses": [
    {
      "hypothesis_id": "H002",
      "approach": "Distributed cache with cross-module integration",
      "confidence_score": 0.82,
      "agents_required": ["python-code-implementer", "architecture-enhancer"],
      "complexity": "high",
      "risk_factors": [
        "Distributed systems complexity",
        "Cross-module coordination",
        "Performance validation"
      ]
    }
  ],
  "context_quality": 0.78,
  "task_context": {
    "user_request": "Implement distributed caching across modules",
    "domain": "packages/**",
    "constraints": ["Must maintain consistency", "Sub-100ms latency"]
  }
}
```

### Analysis

- Risk level: High (distributed systems, multiple modules)
- Complexity: Very high (6+ files, integration points)
- Domain: packages/** (multiple modules)
- Expected failure modes: 5 (integration, coordination, performance, testing, deployment)

### Contingency Plan Generated (Condensed)

```json
{
  "hypothesis_id": "H002",
  "contingency_plan": {
    "failure_modes": [
      {
        "mode_id": "FM001",
        "description": "Cross-module integration failures",
        "probability": 0.6,
        "impact": 0.8,
        "risk_score": 0.48,
        "risk_classification": "medium",
        "fallback_strategies": [
          {
            "strategy_id": "FB001-1",
            "approach": "Implement phased rollout (core first, then API)",
            "tier": "scope_reduction",
            "success_probability": 0.8
          },
          {
            "strategy_id": "FB001-2",
            "approach": "Research integration patterns before retry",
            "tier": "context_enhancement",
            "fallback_agent": "researcher-codebase",
            "success_probability": 0.75
          }
        ]
      },
      {
        "mode_id": "FM002",
        "description": "Distributed cache coordination issues",
        "probability": 0.7,
        "impact": 0.9,
        "risk_score": 0.63,
        "risk_classification": "high",
        "fallback_strategies": [
          {
            "strategy_id": "FB002-1",
            "approach": "Simplify to single-node cache (remove distributed complexity)",
            "tier": "scope_reduction",
            "success_probability": 0.85
          },
          {
            "strategy_id": "FB002-2",
            "approach": "Escalate for architecture review",
            "tier": "escalation",
            "success_probability": 0.95
          }
        ]
      }
    ],
    "retry_plan": {
      "max_attempts": 1,
      "max_attempts_rationale": "High risk (0.63 highest) requires rapid escalation after 1 failure",
      "escalation_triggers": [
        { "trigger": "retry_count >= 1" },
        { "trigger": "risk_score >= 0.6" },
        { "trigger": "execution_time > 10min" }
      ]
    },
    "overall_resilience_score": 0.65
  }
}
```

---

## Example 3: Insufficient Hypothesis Information (FAILURE)

**Context**: Vague hypothesis without agent recommendation or risk assessment

### Input

```json
{
  "hypothesis_id": "H003",
  "strategy": "Improve performance"
}
```

### Analysis

- Missing: agent recommendation, risk assessment, domain scope
- Cannot identify failure modes without domain context
- Cannot generate fallbacks without agent information

### Output (FAILURE)

```json
{
  "status": "FAILURE",
  "agent": "contingency-planner",
  "confidence": 0.2,
  "failure_details": {
    "failure_type": "insufficient_hypothesis_information",
    "reasons": [
      "No agent recommendation provided (required for fallback strategy generation)",
      "No risk assessment provided (required for failure mode identification)",
      "Strategy too vague ('improve performance' lacks specificity)"
    ],
    "required_information": [
      {
        "field": "agent_recommendation",
        "required_in": "Hypothesis object",
        "format": "string (agent name from CLAUDE.md)"
      },
      {
        "field": "risk_assessment",
        "required_in": "Hypothesis object",
        "format": "{ risk_level, key_risks, probability, impact }"
      },
      {
        "field": "domain_scope",
        "required_in": "Hypothesis metadata",
        "format": "array of directory paths"
      }
    ],
    "recovery_suggestions": [
      "Re-submit to orchestrator with complete hypothesis details",
      "Provide specific strategy description (what performance? which component?)",
      "Include agent recommendation and risk assessment"
    ],
    "partial_analysis": {
      "hypotheses_received": 1,
      "hypotheses_analyzable": 0,
      "reason": "Missing required fields prevent failure mode analysis"
    }
  }
}
```

---

## Example 4: Input/Output Transformation Example

**Purpose**: Show contingency density (hypothesis -> comprehensive contingency framework)

### INPUT (hypothesis from orchestrator - ~150 tokens)

```json
{
  "task_id": "task_004",
  "execution_timestamp": "2025-01-15T14:00:00Z",
  "hypotheses": [
    {
      "hypothesis_id": "H001",
      "approach": "Redis-backed distributed cache with TTL",
      "confidence_score": 0.68,
      "agents_required": ["python-code-implementer"],
      "complexity": "medium",
      "risk_factors": ["Redis dependency", "Cache invalidation"]
    }
  ],
  "context_quality": 0.82,
  "task_context": {
    "user_request": "Implement Redis caching with TTL support",
    "domain": "packages/core/cache/"
  }
}
```

### OUTPUT (comprehensive contingency plan - ~550 tokens with full risk analysis)

```json
{
  "hypothesis_id": "H001",
  "contingency_plan": {
    "failure_modes": [
      {
        "mode_id": "FM001",
        "description": "Redis connection failure during implementation",
        "failure_type": "technical",
        "triggers": ["Redis not installed", "Connection string misconfigured", "Network issues"],
        "probability": 0.4,
        "probability_rationale": "External dependency (+0.2), moderate complexity (+0.2), base 0.0",
        "impact": 0.6,
        "impact_rationale": "Medium setback (0.6) - recoverable with fallback to in-memory cache",
        "risk_score": 0.24,
        "fallback_strategies": [
          {
            "strategy_id": "FB001-1",
            "approach": "Switch to in-memory cache implementation",
            "fallback_agent": "python-code-implementer",
            "context_enhancement": "Gather in-memory cache patterns from codebase",
            "effort_estimate": "2-3 hours (simpler than Redis)",
            "success_probability": 0.85,
            "rationale": "Removes external dependency, uses proven in-memory patterns"
          },
          {
            "strategy_id": "FB001-2",
            "approach": "Research Redis setup best practices and retry",
            "fallback_agent": "researcher-external",
            "context_enhancement": "OWASP Redis security patterns, Docker setup guides",
            "effort_estimate": "1 hour research + 4 hours implementation retry",
            "success_probability": 0.70,
            "rationale": "Addresses root cause (setup), higher quality but more effort"
          }
        ]
      },
      {
        "mode_id": "FM002",
        "description": "Cache invalidation logic complexity exceeds estimate",
        "failure_type": "assumption",
        "triggers": ["TTL patterns unclear", "Invalidation edge cases", "Race conditions"],
        "probability": 0.5,
        "impact": 0.8,
        "risk_score": 0.40,
        "fallback_strategies": [
          {
            "strategy_id": "FB002-1",
            "approach": "Simplify to time-based expiration only",
            "fallback_agent": "python-code-implementer",
            "effort_estimate": "1 hour refactor",
            "success_probability": 0.90
          },
          {
            "strategy_id": "FB002-2",
            "approach": "Research cache invalidation patterns before retry",
            "fallback_agent": "researcher-external",
            "context_enhancement": "Redis client library docs, cache invalidation best practices",
            "effort_estimate": "1 hour research + 3 hours retry",
            "success_probability": 0.75
          }
        ]
      },
      {
        "mode_id": "FM003",
        "description": "Performance targets not met (>100ms response time)",
        "failure_type": "integration",
        "probability": 0.3,
        "impact": 0.7,
        "risk_score": 0.21
      }
    ],
    "retry_plan": {
      "max_attempts": 2,
      "max_attempts_rationale": "Medium risk (0.40 highest) allows 2 retries before escalation",
      "backoff_strategy": "exponential",
      "backoff_intervals": ["1s", "2s"],
      "escalation_triggers": [
        "retry_count >= 2",
        "execution_time > 10 minutes",
        "critical_failure (risk_score >= 0.7)"
      ],
      "confidence_decay_model": {
        "initial_confidence": 0.68,
        "decay_per_failure": 0.15,
        "escalation_threshold": 0.30,
        "rationale": "Each failure reduces confidence by 0.15; escalate if drops below 0.30"
      },
      "termination_conditions": [
        "All fallback strategies exhausted",
        "Confidence drops below 0.30",
        "User requests termination"
      ]
    },
    "escalation_paths": {
      "high_risk_path": "Immediate escalation to human for critical failures (risk_score >= 0.7)",
      "medium_risk_path": "Attempt fallback strategies, escalate after 2 failures",
      "low_risk_path": "Standard retry with backoff, escalate after max_attempts exhausted"
    },
    "overall_resilience_score": 0.75,
    "resilience_rationale": "3 failure modes identified, 5 fallback strategies total, clear escalation paths"
  }
}
```

**Note**: Agent expands hypothesis to comprehensive contingency framework (~4.5x expansion)

**Value**: Orchestrator gets execution-ready resilience plan instead of vague risk assessment

---

## Usage Patterns

### Pattern 1: Single Hypothesis Contingency Planning

**When to Use**: Orchestrator provides 1 hypothesis for analysis

**Process**:
1. Receive hypothesis with confidence_score and risk_factors from orchestrator
2. Identify 3-5 failure modes
3. Generate 2-3 fallback strategies per failure mode
4. Define retry plan with escalation triggers
5. Return SUCCESS with contingency plan

### Pattern 2: Multi-Hypothesis Contingency Planning

**When to Use**: Orchestrator provides 2-5 ranked hypotheses

**Process**:
1. Receive ranked hypothesis list
2. For each hypothesis:
   - Identify 3-5 failure modes
   - Generate 2-3 fallback strategies per mode
   - Define retry plan
3. Return SUCCESS with array of contingency plans

### Pattern 3: Insufficient Information (FAILURE)

**When to Use**: Orchestrator input missing required fields

**Process**:
1. Attempt to parse hypotheses from orchestrator input
2. Detect missing fields (agents_required, risk_factors, domain)
3. Return FAILURE with required information and recovery suggestions

---

## Integration with OODA Loop

### OBSERVE Phase (Orchestrator)
- Parse user request, identify task requirements

### ORIENT Phase (Orchestrator + context-readiness-assessor)
- Gather context, assess Context_Quality

### DECIDE Phase (orchestrator -> contingency-planner)
- **Orchestrator**: Provides 1-5 ranked hypotheses with confidence scores and risk factors
- **contingency-planner**: Analyze each hypothesis, identify failure modes, generate fallback strategies, define retry plans
- **Output**: Comprehensive contingency frameworks returned to orchestrator for execution planning

### ACT Phase (Orchestrator)
- Execute top-ranked hypothesis
- Monitor for failures using contingency plan
- Apply fallback strategies as needed
- Escalate based on retry plan triggers

---

**Related Guides**:
- `../contingency-planner.md` - Agent definition and workflow integration
- `../docs/failure-mode-analysis.md` - Detailed probability x impact risk scoring rubrics
- `../docs/fallback-strategies.md` - Multi-tier fallback framework with agent selection
- `../docs/retry-plans.md` - Adaptive retry logic with confidence decay modeling
