---
title: "Agent Effectiveness Tracking Framework"
date: 2025-11-18
status: ACTIVE
tags: [agents, effectiveness, metrics, tracking]
---

# Agent Effectiveness Tracking Framework

**Purpose**: Framework for tracking agent performance, confidence calibration, and success rates

**Audience**: Future agent-effectiveness-tracker agent, orchestrator, agent reviewers

**Scope**: Metrics and methodologies for measuring Claude Code agent effectiveness over time

**Status**: FRAMEWORK ONLY - No implementation yet (gap identified in research synthesis)

---

## Quick Reference

| **Metric** | **Formula** | **Target** | **Use Case** |
|------------|-------------|------------|--------------|
| Success Rate | successful_completions / total_delegations | >85% | Agent reliability tracking |
| Confidence Accuracy | correlation(reported_confidence, actual_success) | >0.7 Pearson | Calibration validation |
| Domain Fit Score | (domain × 0.6) + (work_type × 0.3) + (track_record × 0.1) | >0.5 for delegation | Agent selection optimization |
| Average Confidence | mean(confidence_scores) | 0.7-0.85 optimal | Overconfidence/underconfidence detection |
| Iteration Rate | tasks_requiring_retry / total_tasks | <15% | Quality signal (lower = better) |
| Token Efficiency | output_quality_score / tokens_consumed | Benchmark per agent | Cost-effectiveness tracking |

---

## Core Metrics

### 1. Success Rate Tracking

**Definition**: Percentage of agent delegations that complete successfully without escalation.

**Calculation**:
```
success_rate = (successful_completions / total_delegations) × 100

successful_completion = agent returns SUCCESS status AND orchestrator validates output quality
```

**Targets**:
- **Excellent**: >90% success rate
- **Good**: 85-90% success rate
- **Acceptable**: 75-84% success rate (for v0.x MVP agents)
- **Concerning**: <75% success rate (triggers agent review)

**Tracking Period**: Rolling 30-day window, minimum 10 delegations for statistical significance

**Data Collection**:
```json
{
  "agent": "researcher-external",
  "delegation_timestamp": "2025-11-18T12:00:00Z",
  "status": "SUCCESS",
  "orchestrator_validation": "PASS",
  "task_complexity": "medium",
  "confidence_reported": 0.88
}
```

**Use Cases**:
- Identify underperforming agents for review/enhancement
- Validate agent maturity level (v0.x → v1.x → v2.x → v3.x progression)
- Optimize agent selection (prefer high success rate agents for critical tasks)

---

### 2. Confidence Calibration

**Definition**: Correlation between agent's self-reported confidence and actual task success.

**Calculation**:
```
confidence_accuracy = pearson_correlation(reported_confidence[], actual_success[])

where:
- reported_confidence = agent's confidence score (0.0-1.0)
- actual_success = 1.0 if SUCCESS + validated, 0.0 if FAILURE or validation fail
```

**Interpretation**:
- **Well-calibrated**: r > 0.7 (high confidence predicts success, low confidence predicts failure)
- **Overconfident**: High confidence but low success rate (agent overestimates abilities)
- **Underconfident**: Low confidence but high success rate (agent underestimates abilities)
- **Uncalibrated**: r < 0.3 (confidence scores uninformative)

**Example**:
```
Agent A:
confidence: [0.9, 0.9, 0.9, 0.2, 0.3]
success:    [1.0, 1.0, 0.0, 0.0, 0.0]
r = 0.45 (moderate calibration, slightly overconfident)

Agent B:
confidence: [0.9, 0.8, 0.5, 0.3, 0.2]
success:    [1.0, 1.0, 0.0, 0.0, 0.0]
r = 0.95 (excellent calibration)
```

**Calibration Adjustment**:
If agent consistently overconfident (r < 0.5, high confidence + low success):
1. Review agent's confidence scoring logic
2. Adjust thresholds (e.g., reduce confidence by 0.1-0.2)
3. Add uncertainty factors to confidence calculation

**Tracking Period**: Minimum 20 delegations for statistical significance

---

### 3. Domain Fit Score

**Definition**: How well agent's domain expertise matches delegated tasks.

**Calculation**:
```
domain_fit_score = (domain_match × 0.6) + (work_type_match × 0.3) + (track_record × 0.1)

where:
- domain_match = 1.0 if task path in agent's primary domain, 0.5 if adjacent, 0.0 if unrelated
- work_type_match = 1.0 if task type matches agent capabilities, 0.0 if mismatch
- track_record = success_rate for this agent (0.0-1.0)
```

**Example**:
```
Task: "Fix bug in packages/auth/jwt.py"

debugger agent:
- domain_match = 1.0 (packages/** is primary domain)
- work_type_match = 1.0 (bug fixing is core capability)
- track_record = 0.88 (88% success rate)
→ domain_fit_score = (1.0 × 0.6) + (1.0 × 0.3) + (0.88 × 0.1) = 0.988

/spec command:
- domain_match = 0.0 (docs/** domain, not packages/**)
- work_type_match = 0.0 (spec creation, not bug fixing)
- track_record = 0.92 (92% success rate in its domain)
→ domain_fit_score = (0.0 × 0.6) + (0.0 × 0.3) + (0.92 × 0.1) = 0.092
```

**Use Cases**:
- Optimize agent selection (prefer domain_fit_score >0.5)
- Identify task-agent mismatches (low domain fit but delegated anyway)
- Detect domain drift (agent used outside intended scope)

---

### 4. Average Confidence Analysis

**Definition**: Mean confidence score across all delegations to detect systematic over/underconfidence.

**Calculation**:
```
avg_confidence = mean(confidence_scores[])

Optimal range: 0.70-0.85
```

**Interpretation**:
- **avg_confidence > 0.90**: Likely overconfident (or only receives easy tasks)
- **avg_confidence 0.70-0.85**: Well-calibrated (healthy uncertainty acknowledgment)
- **avg_confidence < 0.60**: Likely underconfident (or receives difficult tasks)

**Actionable Insights**:
- High avg_confidence + low success rate → Overconfidence, review confidence logic
- Low avg_confidence + high success rate → Underconfidence, adjust upward
- Appropriate avg_confidence → Monitor for drift over time

---

### 5. Iteration Rate

**Definition**: Percentage of tasks requiring retry or follow-up research before completion.

**Calculation**:
```
iteration_rate = (tasks_requiring_retry / total_tasks) × 100

tasks_requiring_retry = tasks where agent calls iteration_support OR orchestrator requests follow-up
```

**Targets**:
- **Excellent**: <10% iteration rate (high quality first-pass outputs)
- **Good**: 10-15% iteration rate (acceptable for complex domains)
- **Concerning**: >20% iteration rate (agent frequently uncertain or incomplete)

**Use Cases**:
- Quality signal (lower = better first-pass quality)
- Identify agents needing better pre-flight research
- Optimize research coordination (high iteration rate → delegate to researcher-lead first)

---

### 6. Token Efficiency

**Definition**: Output quality per token consumed (cost-effectiveness).

**Calculation**:
```
token_efficiency = output_quality_score / tokens_consumed

where:
- output_quality_score = orchestrator validation score (0-100 scale)
- tokens_consumed = total input + output tokens for agent delegation
```

**Benchmarking**:
Establish baseline per agent type:
- Research agents: Higher token consumption acceptable (10K-20K tokens typical)
- Implementation agents: Moderate consumption (5K-10K tokens)
- Review agents: Lower consumption (2K-5K tokens)

**Use Cases**:
- Cost optimization (prefer high token efficiency for budget-sensitive tasks)
- Detect token bloat (sudden increase in consumption without quality improvement)
- Evaluate progressive disclosure effectiveness (should reduce token usage over time)

---

## Data Collection Schema

**Proposed tracking record structure** (for future agent-effectiveness-tracker):

```json
{
  "delegation_id": "uuid",
  "timestamp": "ISO 8601 UTC",
  "agent": "agent-name",
  "task_type": "implementation | research | review | analysis | planning",
  "task_domain": "file path or domain identifier",
  "task_complexity": "low | medium | high",
  "confidence_reported": 0.0-1.0,
  "status": "SUCCESS | FAILURE | PARTIAL",
  "orchestrator_validation": "PASS | FAIL | PARTIAL",
  "output_quality_score": 0-100,
  "tokens_consumed": {
    "input": 1234,
    "output": 5678,
    "total": 6912
  },
  "iteration_required": true/false,
  "escalation_triggered": true/false,
  "execution_time_seconds": 123.45,
  "domain_fit_score": 0.0-1.0,
  "context_quality": 0.0-1.0
}
```

---

## Effectiveness Reporting

**Dashboard Metrics** (if agent-effectiveness-tracker implemented):

### Per-Agent Report
```
Agent: researcher-external
Period: Last 30 days
Delegations: 45

Success Rate: 91% (41/45) ✅
Confidence Accuracy: r=0.82 (well-calibrated) ✅
Avg Confidence: 0.78 (optimal) ✅
Iteration Rate: 13% (6/45) ✅
Token Efficiency: 12.5 quality/1K tokens (benchmark: 10.0) ✅

Domain Fit Distribution:
- Primary domain (library docs): 38 delegations, 95% success
- Adjacent domain (web research): 5 delegations, 80% success
- Outside domain: 2 delegations, 50% success ⚠️

Recommendation: PASS - Agent performing well within primary domain.
Handles both library docs and web research (auto-routes based on query).
```

### Ecosystem-Wide Trends
```
Top 5 Agents by Success Rate (30 days):
1. /spec command: 96% (48/50)
2. researcher-external: 91% (41/45)
3. claude-code-ecosystem: 89% (32/36)
4. debugger: 87% (78/90)
5. development: 85% (102/120)

Agents Needing Review (success rate <75%):
- experimental-agent-xyz: 62% (15/24) ← v0.x MVP, expected
- pattern-detector: 71% (25/35) ← Needs calibration
```

---

## Gap Identified: No Implementation Yet

**Current State**: This framework documents WHAT to track, but:
- ❌ No agent-effectiveness-tracker agent exists
- ❌ No automated data collection
- ❌ No tracking database or storage
- ❌ No dashboard or reporting

**Recommendation**:
1. Create agent-effectiveness-tracker agent (uses this framework)
2. Implement tracking data collection (hook into orchestrator delegations)
3. Build reporting dashboard (weekly/monthly effectiveness summaries)
4. Establish baseline metrics (first 30-60 days of collection)
5. Iterate on framework based on actual data

**Priority**: P2 (Medium) - Useful for optimization but not blocking current operations

---

## Integration with Agent Analysis

**claude-code-ecosystem.md** references this framework when evaluating agent maturity:
- Success rate → Maturity progression (v0.x <75%, v1.x 75-85%, v2.x 85-90%, v3.x >90%)

**claude-code-ecosystem.md** uses confidence calibration insights:
- Identify agents with poor calibration for prompt engineering review

**tech-debt-investigator.md** tracks iteration rate:
- High iteration rate = signal of documentation debt or unclear requirements

**orchestrator** optimizes agent selection:
- Prefer agents with high domain_fit_score and success_rate
- Adjust confidence thresholds based on calibration data

**See Also**:
- `.claude/docs/01-guides/agents/agent-selection-guide.md` - Domain fit scoring methodology
- `.claude/docs/03-workflows/orchestrator-workflow.md` - Agent coordination patterns
- `docs/01-planning/custom/confidence-based-delegation-framework.md` - Delegation confidence scoring

---

**Version**: 1.0 (Framework Only - No Implementation)
**Source**: Research synthesis gap analysis + agent selection frameworks + OODA loop metrics
