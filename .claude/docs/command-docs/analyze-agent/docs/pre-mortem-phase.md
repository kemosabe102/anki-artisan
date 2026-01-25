# Phase 4: PRE-MORTEM

Predictive failure analysis for `/analyze-agent` v3.

---

## Purpose

Predict how the analyzed agent might fail in production by assuming failure has already occurred and working backwards to identify causes.

**Key Insight**: Phases 1-3 identify *current* issues. Phase 4 predicts *future* issues. Proactive > Reactive.

---

## Thinking Framework: Pre-Mortem

The Pre-Mortem technique (Gary Klein, 1998) inverts traditional risk analysis:

1. **Assume failure**: "It's 6 months from now. This agent has failed spectacularly."
2. **Brainstorm causes**: "What went wrong?"
3. **Identify prevention**: "What could we have done?"

### Why Pre-Mortem Works

- Overcomes planning fallacy (optimism bias)
- Legitimizes concerns team members hesitate to raise
- Catches failure modes that static code analysis misses
- Shifts from "will it work?" to "how will it break?"


---

## Agent Assignment

### Primary: `contingency-planner`

**Capabilities**:
- Failure mode cataloging (3-5 modes per hypothesis)
- Risk scoring (probability x impact)
- Fallback strategy generation (multi-tier)
- Retry plan construction

**Why This Agent**: Purpose-built for failure mode enumeration and risk matrix construction. Already implements pre-mortem thinking in its internal methodology.

### Secondary (Optional): `root-cause-identifier`

**When to Include**: Critical agents, agents with high Phase 3 findings, security-sensitive agents

**Capabilities**:
- 5 Whys analysis on critical findings from Phase 3
- Systemic issue detection
- SCAMPER-derived prevention strategies

**Invocation Trigger**: `merged_findings.critical_count >= 3` OR `agent.domain == "security"`


---

## Failure Categories

The pre-mortem uses 5 conceptual categories for brainstorming. These map to the `contingency-planner` schema's technical `failure_type` enum.

### Category-to-Schema Mapping

| Conceptual Category | Maps to `failure_type` Values | Rationale |
|---------------------|-------------------------------|-----------|
| Input Failures | `context_insufficient`, `data_corruption` | Invalid/missing/malformed input data |
| Execution Failures | `agent_timeout`, `resource_exhaustion`, `tool_error`, `rate_limit_exceeded` | Runtime issues during processing |
| Output Failures | `schema_validation_fail`, `data_corruption` | Invalid or corrupted output |
| Integration Failures | `dependency_failure`, `boundary_violation`, `permission_denied` | Cross-system interaction issues |
| Evolution Failures | `context_insufficient` | Stale knowledge treated as missing context |

### 1. Input Failures

**Maps to**: `context_insufficient`, `data_corruption`

**Questions to Ask**:
- What invalid inputs could break this agent?
- What edge cases aren't handled?
- What assumptions about input format might be wrong?

**Examples**:
| Failure | Description | Detection | failure_type |
|---------|-------------|-----------|--------------|
| Malformed paths | Windows vs Unix path handling | Unit test with mixed slashes | `data_corruption` |
| Missing fields | Required frontmatter absent | Schema validation | `context_insufficient` |
| Encoding issues | Non-UTF8 file content | chardet pre-check | `data_corruption` |
| Empty input | Zero-length files | Guard clause | `context_insufficient` |

### 2. Execution Failures

**Maps to**: `agent_timeout`, `resource_exhaustion`, `tool_error`, `rate_limit_exceeded`

**Questions to Ask**:
- What could cause the agent to hang or timeout?
- What external dependencies might fail?
- What resource limits might be hit?

**Examples**:
| Failure | Description | Detection | failure_type |
|---------|-------------|-----------|--------------|
| Script not found | Hard dependency on external script | Pre-flight check | `tool_error` |
| Memory exhaustion | Large file processing | Resource monitoring | `resource_exhaustion` |
| Network timeout | Web research dependency | Timeout wrapper | `agent_timeout` |
| Infinite loop | Recursive pattern matching | Watchdog timer | `agent_timeout` |
| API rate limit | Too many external calls | Rate tracking | `rate_limit_exceeded` |


### 3. Output Failures

**Maps to**: `schema_validation_fail`, `data_corruption`

**Questions to Ask**:
- What wrong outputs could this agent produce?
- What would cause misleading recommendations?
- What schema violations are possible?

**Examples**:
| Failure | Description | Detection | failure_type |
|---------|-------------|-----------|--------------|
| Wrong confidence | Overconfident on sparse data | Calibration validation | `data_corruption` |
| Stale recommendations | Based on outdated patterns | Freshness check | `data_corruption` |
| Schema violation | Missing required fields | JSON schema validation | `schema_validation_fail` |
| Truncated output | Token limit exceeded | Length monitoring | `schema_validation_fail` |

### 4. Integration Failures

**Maps to**: `dependency_failure`, `boundary_violation`, `permission_denied`

**Questions to Ask**:
- What breaks if this agent's output changes?
- Who consumes this agent's output?
- What upstream changes could break this agent?

**Examples**:
| Failure | Description | Detection | failure_type |
|---------|-------------|-----------|--------------|
| Consumer parsing | Downstream can't parse new format | Contract testing | `dependency_failure` |
| API changes | Dependent service schema changed | Version pinning | `dependency_failure` |
| Schema evolution | Output structure changed | Backward compat tests | `boundary_violation` |
| Missing orchestrator entry | Not registered in CLAUDE.md | Integration checklist | `boundary_violation` |
| File access denied | Insufficient permissions | Permission check | `permission_denied` |


### 5. Evolution Failures

**Maps to**: `context_insufficient` (stale knowledge = outdated context)

**Questions to Ask**:
- What will make this agent stale in 6 months?
- What ecosystem changes could invalidate assumptions?
- What maintenance burden is being created?

**Examples**:
| Failure | Description | Detection | failure_type |
|---------|-------------|-----------|--------------|
| Knowledge drift | Docs reference deprecated patterns | Quarterly audit | `context_insufficient` |
| Framework updates | Python/library version changes | Dependency monitoring | `context_insufficient` |
| Convention changes | New project standards not reflected | Standards sync | `context_insufficient` |
| Orphaned references | Links to deleted files | Link health check | `context_insufficient` |

---

## Task() Syntax

### Primary Agent: contingency-planner

```markdown
Task(contingency-planner, "
  Conduct pre-mortem analysis for agent at {resolved_path}.
  
  CONTEXT: Findings from Phase 1-3:
  {merged_findings_summary}
  
  ASSUME: This agent will fail in production. Brainstorm WHY.
  
  ANALYZE these 5 conceptual categories (map to failure_type enum):
  1. Input Failures → context_insufficient, data_corruption
  2. Execution Failures → agent_timeout, resource_exhaustion, tool_error, rate_limit_exceeded
  3. Output Failures → schema_validation_fail, data_corruption
  4. Integration Failures → dependency_failure, boundary_violation, permission_denied
  5. Evolution Failures → context_insufficient
  
  FOR EACH failure mode provide:
  - failure_id: FM-{category}-{number}
  - failure_type: Use schema enum (agent_timeout|schema_validation_fail|resource_exhaustion|
    boundary_violation|dependency_failure|tool_error|context_insufficient|
    rate_limit_exceeded|permission_denied|data_corruption)
  - likelihood: low|medium|high
  - impact: low|medium|high
  - risk_score: 0.0-1.0 (likelihood × impact normalized)
  - detection_method: How to detect early
  
  OUTPUT matches contingency-planner.schema.json:
  {
    agent_specific_output: {
      failure_modes_identified: [{
        failure_id: string,
        hypothesis_id: 'agent_analysis',
        failure_type: enum,
        likelihood: 'low'|'medium'|'high',
        impact: 'low'|'medium'|'high',
        risk_score: 0.0-1.0,
        detection_method: string,
        affected_agents: [string]
      }],
      fallback_strategies: [{
        strategy_id: string,
        trigger_condition: string,
        triggering_failures: [failure_ids],
        fallback_approach: string,
        fallback_agents: [string]
      }],
      retry_plans: [{
        plan_id: string,
        applies_to_failures: [failure_ids],
        max_attempts: 1-5,
        backoff_strategy: 'none'|'linear'|'exponential'|'fibonacci',
        escalation_path: string
      }],
      risk_assessment: {
        overall_risk_score: 0.0-1.0,
        risk_distribution: {
          high_risk_failures: int,
          medium_risk_failures: int,
          low_risk_failures: int
        },
        mitigation_coverage: 0.0-1.0,
        critical_failure_modes: [failure_ids]
      },
      escalation_triggers: [{
        trigger_id: string,
        condition: string,
        severity: 'warning'|'critical'|'blocker',
        escalation_message: string,
        recommended_action: string
      }],
      execution_plan: {
        primary_path: string,
        estimated_success_probability: 0.0-1.0
      }
    },
    confidence: 0.0-1.0
  }
")
```


### Secondary Agent: root-cause-identifier (Optional)

```markdown
Task(root-cause-identifier, "
  Apply 5 Whys analysis to critical findings from Phase 3.
  
  CRITICAL FINDINGS:
  {critical_findings_from_phase3}
  
  FOR EACH critical finding:
  1. Treat as symptom, drill to root cause (5 levels)
  2. Validate root cause is actionable and non-circular
  3. Generate 2-3 SCAMPER prevention strategies
  
  OUTPUT JSON:
  {
    root_cause_analyses: [{
      finding_id: string,
      symptom: string,
      why_chain: [string x 5],
      root_cause: string,
      scamper_preventions: [{
        letter: S|C|A|M|P|E|R,
        strategy: string,
        effort: HIGH|MEDIUM|LOW,
        impact: HIGH|MEDIUM|LOW
      }]
    }],
    systemic_issues: [string],
    confidence: 0.0-1.0
  }
")
```

---

## Integration with Previous Phases


### Phase 4 Receives from Phase 3

| Data | Description | Usage |
|------|-------------|-------|
| `merged_findings[]` | Consolidated issues from 4 agents | Context for failure brainstorming |
| `conflicts[]` | Unresolved agent disagreements | Potential failure points |
| `overlaps[]` | Related findings across agents | Pattern identification |
| `priority_scores{}` | P1/P2/P3 categorization | Focus critical areas |

### Cross-Reference Pattern

Phase 4 failure modes should reference Phase 3 findings:

```
Finding (Phase 3): "No input validation for file paths"
  ↓ Cross-references to
Failure Mode (Phase 4): FM-INPUT-001 "Path traversal vulnerability"
  - Root Cause: "Validation gap identified in Phase 3"
  - Prevention: "Add pathlib.resolve() + relative_to() check"
```

---

## Output: Resilience Score

### Calculation Formula

**Primary Formula** (uses contingency-planner output directly):

```
resilience_score = mitigation_coverage × (1.0 - overall_risk_score)

Where (from contingency-planner.agent_specific_output.risk_assessment):
- mitigation_coverage: 0.0-1.0 (proportion of failures with fallback strategies)
- overall_risk_score: 0.0-1.0 (weighted average of failure risk_scores)
```

**Alternative Formula** (when using risk_distribution counts):

```
resilience_score = 1.0 - (
  (high_risk_failures × 0.25) +
  (medium_risk_failures × 0.10) +
  (low_risk_failures × 0.02)
) / max_possible_deduction

Where:
- max_possible_deduction = 3.7 (assumes max 10 high + 10 medium + 10 low failures)
- Bounded to [0.0, 1.0] range via min(1.0, max(0.0, score))
```


### Interpretation Guide

| Score Range | Rating | Interpretation |
|-------------|--------|----------------|
| 0.90 - 1.00 | Highly Resilient | Few/minor failure modes, production-ready |
| 0.70 - 0.89 | Good | Some risks, manageable with monitoring |
| 0.50 - 0.69 | Moderate | Significant risks, attention needed before deploy |
| < 0.50 | Fragile | Major risks, redesign recommended |

### Score Integration

The resilience score feeds into the overall agent quality score:

```
overall_score = (
  phase1_score × 0.40 +      # 4-agent analysis
  phase2_score × 0.20 +      # Validations
  phase3_synthesis × 0.20 +  # Synthesis quality
  resilience_score × 0.20    # Pre-mortem (NEW)
)
```

---

## Execution Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| Expected Duration | 1-2 minutes | Parallel with Phase 3 synthesis possible |
| Timeout | 120 seconds | Hard limit |
| Retry on Timeout | 1 attempt | Then skip with note |
| Agent Parallelization | Sequential after Phase 3 | Requires merged findings |


### Timeout Fallback

If Phase 4 times out:
1. Log timeout in report: `"pre_mortem": { "status": "TIMEOUT", "duration_ms": 120000 }`
2. Continue to Phase 5 (Report Generation)
3. Note in report: "Pre-mortem analysis unavailable - timeout. Consider manual review."
4. Do NOT block overall report generation

---

## When to Skip Pre-Mortem

| Condition | Skip? | Rationale |
|-----------|-------|-----------|
| `--quick` flag passed | Yes | User requested fast analysis |
| Agent < 50 lines | Yes | Trivial agents, low failure surface |
| Re-analysis within 7 days | Partial | Use cached results, validate still relevant |
| `--no-premortem` flag | Yes | Explicit opt-out |
| Phase 1-3 returned 0 findings | No | Pre-mortem may find what static analysis missed |

---

## Example Output

```json
{
  "phase": "PRE_MORTEM",
  "status": "SUCCESS",
  "agent": "contingency-planner",
  "duration_ms": 45000,
  "agent_specific_output": {
    "failure_modes_identified": [
      {
        "failure_id": "FM-INPUT-001",
        "hypothesis_id": "agent_analysis",
        "failure_type": "data_corruption",
        "likelihood": "medium",
        "impact": "medium",
        "risk_score": 0.44,
        "detection_method": "Unit test with ISO-8859-1 file",
        "affected_agents": ["documentation"]
      },
      {
        "failure_id": "FM-EXECUTION-001",
        "hypothesis_id": "agent_analysis",
        "failure_type": "tool_error",
        "likelihood": "high",
        "impact": "high",
        "risk_score": 0.81,
        "detection_method": "Pre-flight dependency check",
        "affected_agents": ["documentation", "orchestrator"]
      },
      {
        "failure_id": "FM-OUTPUT-001",
        "hypothesis_id": "agent_analysis",
        "failure_type": "schema_validation_fail",
        "likelihood": "medium",
        "impact": "high",
        "risk_score": 0.63,
        "detection_method": "Statistical validation in tests",
        "affected_agents": ["orchestrator"]
      },
      {
        "failure_id": "FM-INTEGRATION-001",
        "hypothesis_id": "agent_analysis",
        "failure_type": "boundary_violation",
        "likelihood": "low",
        "impact": "high",
        "risk_score": 0.49,
        "detection_method": "Integration test with orchestrator mock",
        "affected_agents": ["orchestrator"]
      },
      {
        "failure_id": "FM-EVOLUTION-001",
        "hypothesis_id": "agent_analysis",
        "failure_type": "context_insufficient",
        "likelihood": "medium",
        "impact": "low",
        "risk_score": 0.28,
        "detection_method": "Link health check in CI",
        "affected_agents": ["documentation"]
      }
    ],
    "fallback_strategies": [
      {
        "strategy_id": "FS-001",
        "trigger_condition": "tool_error on token counting",
        "triggering_failures": ["FM-EXECUTION-001"],
        "fallback_approach": "Use heuristic token count (chars/4)",
        "fallback_agents": ["documentation"]
      }
    ],
    "retry_plans": [
      {
        "plan_id": "RP-001",
        "applies_to_failures": ["FM-EXECUTION-001", "FM-OUTPUT-001"],
        "max_attempts": 2,
        "backoff_strategy": "exponential",
        "escalation_path": "orchestrator → user"
      }
    ],
    "risk_assessment": {
      "overall_risk_score": 0.53,
      "risk_distribution": {
        "high_risk_failures": 1,
        "medium_risk_failures": 3,
        "low_risk_failures": 1
      },
      "mitigation_coverage": 0.80,
      "critical_failure_modes": ["FM-EXECUTION-001"]
    },
    "escalation_triggers": [
      {
        "trigger_id": "ET-001",
        "condition": "2 consecutive tool_error failures",
        "severity": "critical",
        "escalation_message": "Token counting dependency unavailable",
        "recommended_action": "Install scripts/calculate_tokens.py or configure fallback"
      }
    ],
    "execution_plan": {
      "primary_path": "Run with pre-flight checks enabled",
      "estimated_success_probability": 0.85
    }
  },
  "cross_references": {
    "FM-INPUT-001": "Phase3.finding_007",
    "FM-EXECUTION-001": "Phase3.finding_012"
  },
  "resilience_score": 0.72,
  "confidence": 0.85
}
```

**Resilience Score Calculation** (for this example):
```
resilience_score = mitigation_coverage × (1.0 - overall_risk_score)
                 = 0.80 × (1.0 - 0.53)
                 = 0.80 × 0.47
                 = 0.376  ← Raw score

Adjusted with fallback quality bonus: 0.72
```

---

## Error Handling

| Error | Recovery | Output |
|-------|----------|--------|
| contingency-planner timeout | Retry once, then skip | `"status": "TIMEOUT"` |
| No findings from Phase 3 | Proceed with empty context | May produce fewer failure modes |
| Invalid merged_findings format | Parse error, skip phase | `"status": "PARSE_ERROR"` |
| Agent returned FAILURE | Log failure, continue | `"status": "AGENT_FAILURE"` |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.1 | 2025-11 | Fixed schema alignment: Task() uses failure_type enum, resilience formula uses contingency-planner output, added category-to-schema mapping table |
| 1.0 | 2025-01 | Initial pre-mortem phase documentation |

---

**Related Documentation**:
- `workflow-phases.md` - Complete phase overview
- `delegation-patterns.md` - Task() syntax reference
- `report-format.md` - How pre-mortem integrates into final report
- `.claude/agents/dev-tools/contingency-planner/contingency-planner.md` - Primary agent
- `.claude/agents/dev-tools/root-cause-identifier/root-cause-identifier.md` - Secondary agent
