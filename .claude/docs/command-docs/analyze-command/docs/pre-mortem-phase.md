# Phase 4: Pre-Mortem

Predictive failure analysis for command workflows in `/analyze-command`.

**Version**: 1.0.0 | **Last Updated**: 2025-12-21

---

## Purpose

Predict how the analyzed command might fail in production by assuming failure has already occurred and working backwards to identify causes.

**Key Insight**: Phases 1-3 identify *current* issues. Phase 4 predicts *future* issues. Proactive > Reactive.

---

## Thinking Framework: Pre-Mortem

The Pre-Mortem technique (Gary Klein, 1998) inverts traditional risk analysis:

1. **Assume failure**: "It's 6 months from now. This command has failed spectacularly."
2. **Brainstorm causes**: "What went wrong?"
3. **Identify prevention**: "What could we have done?"

### Why Pre-Mortem Works

- Overcomes planning fallacy (optimism bias)
- Legitimizes concerns team members hesitate to raise
- Catches failure modes that static analysis misses
- Shifts from "will it work?" to "how will it break?"

---

## Agent Assignment

### Primary: `contingency-planner`

**Capabilities**:
- Failure mode cataloging (3-5 modes per category)
- Risk scoring (probability x impact)
- Prevention strategy generation
- Detection method specification

**Why This Agent**: Purpose-built for failure mode enumeration and risk matrix construction. Already implements pre-mortem thinking in its internal methodology.

---

## 5 Failure Categories for Commands

### Category 1: Input Failures

**Description**: Failures related to invalid, missing, or malformed input data.

| Failure Mode | Description | Detection Method |
|--------------|-------------|------------------|
| Invalid arguments | Required args missing or malformed | Argument validation in P0 |
| Missing files | Referenced paths don't exist | Path existence check |
| Malformed paths | Windows/Unix path format mismatch | Path normalization validation |
| Encoding issues | Non-UTF8 file content | Encoding detection pre-check |
| Empty input | Zero-length files or args | Guard clause validation |

**Prevention Strategies**:
- Strict argument schema validation
- Path existence verification before processing
- Encoding detection with fallback handling
- Guard clauses for empty input

**Example Failure Mode**:
```json
{
  "failure_id": "FM-INPUT-001",
  "category": "INPUT",
  "description": "Windows path with backslashes fails on Unix processing",
  "likelihood": "MEDIUM",
  "impact": "HIGH",
  "risk_score": 0.56,
  "root_cause": "Path normalization not applied before file operations",
  "prevention": "Apply pathlib.resolve() before all file operations",
  "detection": "Unit test with mixed slash paths"
}
```

---

### Category 2: Execution Failures

**Description**: Failures that occur during command execution.

| Failure Mode | Description | Detection Method |
|--------------|-------------|------------------|
| Agent timeout | Delegated agent doesn't respond | Timeout wrapper with monitoring |
| Tool unavailable | Required MCP tool not available | Pre-flight tool availability check |
| Skill not found | Referenced skill doesn't exist | Skill registry validation |
| Resource exhaustion | Memory or API limits exceeded | Resource monitoring |
| Rate limit exceeded | Too many API calls | Rate tracking with backoff |

**Prevention Strategies**:
- Pre-flight dependency checks
- Graceful degradation on tool failure
- Resource budgeting per phase
- Exponential backoff for rate limits

**Example Failure Mode**:
```json
{
  "failure_id": "FM-EXECUTION-001",
  "category": "EXECUTION",
  "description": "Documentation agent times out on large command file",
  "likelihood": "MEDIUM",
  "impact": "MEDIUM",
  "risk_score": 0.44,
  "root_cause": "No timeout handling for token counting on large files",
  "prevention": "Implement streaming token count for files > 1000 lines",
  "detection": "Performance test with 2000+ line command file"
}
```

---

### Category 3: Workflow Failures

**Description**: Failures in the command's workflow structure.

| Failure Mode | Description | Detection Method |
|--------------|-------------|------------------|
| Step ordering errors | Phases execute out of dependency order | Dependency graph validation |
| Parallelization conflicts | Race conditions in parallel agents | Conflict detection in synthesis |
| Missing gates | No validation between phases | Gate coverage analysis |
| Timeout cascade | One timeout triggers subsequent timeouts | Cascade detection monitoring |
| Infinite loops | Retry logic without termination | Retry counter enforcement |

**Prevention Strategies**:
- Explicit phase dependency declarations
- Idempotent agent operations
- Mandatory gate validation between phases
- Circuit breaker patterns for cascading failures

**Example Failure Mode**:
```json
{
  "failure_id": "FM-WORKFLOW-001",
  "category": "WORKFLOW",
  "description": "P3 synthesis runs before P1 agents complete",
  "likelihood": "LOW",
  "impact": "HIGH",
  "risk_score": 0.49,
  "root_cause": "Missing explicit wait for parallel agent completion",
  "prevention": "Implement Promise.all pattern for P1 agents",
  "detection": "Timing test with slow agent simulation"
}
```

---

### Category 4: Output Failures

**Description**: Failures in command output generation.

| Failure Mode | Description | Detection Method |
|--------------|-------------|------------------|
| Schema violations | Output doesn't match expected schema | JSON schema validation |
| Truncated output | Incomplete results due to limits | Output completeness check |
| Wrong format | Output structure unexpected | Format assertion tests |
| Missing fields | Required fields absent | Required field validation |
| Stale data | Output contains outdated information | Freshness timestamp check |

**Prevention Strategies**:
- JSON schema validation on all outputs
- Output size monitoring with warnings
- Required field assertions
- Timestamp validation for data freshness

**Example Failure Mode**:
```json
{
  "failure_id": "FM-OUTPUT-001",
  "category": "OUTPUT",
  "description": "Report truncated due to token limit in P6",
  "likelihood": "MEDIUM",
  "impact": "HIGH",
  "risk_score": 0.63,
  "root_cause": "Report generation doesn't chunk large findings arrays",
  "prevention": "Implement progressive report generation with chunking",
  "detection": "Test with 50+ findings to verify complete output"
}
```

---

### Category 5: Integration Failures

**Description**: Failures in command integration with the ecosystem.

| Failure Mode | Description | Detection Method |
|--------------|-------------|------------------|
| Orchestrator mismatch | Command not registered in CLAUDE.md | Registry scan |
| Registry inconsistency | Metadata out of sync with implementation | Cross-reference validation |
| Version drift | Dependencies updated incompatibly | Dependency version check |
| Permission issues | Command attempts out-of-scope operations | Scope boundary enforcement |
| Downstream breaks | Changes break consuming commands | Consumer impact analysis |

**Prevention Strategies**:
- Automated registry synchronization
- Semantic versioning for dependencies
- Scope validation in P0
- Consumer contract testing

**Example Failure Mode**:
```json
{
  "failure_id": "FM-INTEGRATION-001",
  "category": "INTEGRATION",
  "description": "Command references deprecated agent that was removed",
  "likelihood": "MEDIUM",
  "impact": "HIGH",
  "risk_score": 0.56,
  "root_cause": "No validation of agent existence in delegation patterns",
  "prevention": "Pre-flight agent availability check before delegation",
  "detection": "CI job scanning for broken agent references"
}
```

---

## Resilience Score Calculation

### Formula

```
resilience_score = 1.0 - weighted_risk_average

Where:
weighted_risk_average = sum(risk_score_i * weight_i) / sum(weight_i)

Weights by category:
- INPUT: 0.15
- EXECUTION: 0.25
- WORKFLOW: 0.25
- OUTPUT: 0.20
- INTEGRATION: 0.15
```

### Alternative Formula (Risk Distribution)

```
resilience_score = 1.0 - (
  (critical_count x 0.30) +
  (high_count x 0.15) +
  (medium_count x 0.05) +
  (low_count x 0.01)
) / max_possible_deduction

Where:
max_possible_deduction = 5.1 (assumes max 10 critical + 10 high + 10 medium + 10 low)
Bounded to [0.0, 1.0]
```

### Interpretation Guide

| Score Range | Rating | Interpretation |
|-------------|--------|----------------|
| 0.90 - 1.00 | Highly Resilient | Few/minor failure modes, production-ready |
| 0.70 - 0.89 | Good | Some risks, manageable with monitoring |
| 0.50 - 0.69 | Moderate | Significant risks, address before deploy |
| < 0.50 | Fragile | Major risks, redesign recommended |

---

## Integration with Other Phases

### Phase 4 Receives from Phase 3

| Data | Description | Usage |
|------|-------------|-------|
| `merged_findings[]` | Consolidated issues from 4 agents | Context for failure brainstorming |
| `conflicts[]` | Unresolved disagreements | Potential failure points |
| `overlaps[]` | Related findings | Pattern identification |
| `priority_scores{}` | P1/P2/P3 categorization | Focus critical areas |

### Phase 4 Outputs to Phase 5

| Data | Description | Usage |
|------|-------------|-------|
| `resilience_score` | 0.0-1.0 | Component of overall_score (5% weight) |
| `failure_modes[]` | Complete failure catalog | Report generation |
| `top_3_risks[]` | Highest priority risks | Executive summary |

---

## Execution Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| Expected Duration | 1-2 minutes | Sequential after P3 |
| Timeout | 120 seconds | Hard limit |
| Retry on Timeout | 1 attempt | Then skip with note |
| Minimum Failure Modes | 3 | Less suggests incomplete analysis |

### Timeout Fallback

If Phase 4 times out:
1. Log timeout in report: `"pre_mortem": { "status": "TIMEOUT" }`
2. Set `resilience_score = null`
3. Continue to Phase 5 (use 0 for resilience weight)
4. Note in report: "Pre-mortem analysis unavailable - timeout"

---

## When to Skip Pre-Mortem

| Condition | Skip? | Rationale |
|-----------|-------|-----------|
| `--quick` flag | Yes | User requested fast analysis |
| Command < 50 lines | Yes | Trivial commands, low failure surface |
| Re-analysis within 7 days | Partial | Use cached results if available |
| `--no-premortem` flag | Yes | Explicit opt-out |
| P1-P3 returned 0 findings | No | Pre-mortem may find what static missed |

---

## Related Documentation

- `workflow-phases.md` - Complete phase overview
- `delegation-patterns.md` - Task() syntax reference
- `../schemas/command-analysis.schema.json` - Output schema
- `.claude/agents/dev-tools/contingency-planner/contingency-planner.md` - Primary agent
