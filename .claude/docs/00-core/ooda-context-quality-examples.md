# OODA Context_Quality Assessment Examples

**Purpose**: Dimension scoring guide for Context_Quality calculation during ORIENT phase

**Formula**: Context_Quality = (Domain×0.4 + Pattern×0.3 + Dependency×0.2 + Risk×0.1)

**Threshold**: ≥0.5 PROCEED to implementation | <0.5 RESEARCH FIRST (delegate to researcher-lead)

---

## Example 1: Bug Fix in packages/auth/jwt.py

**Scenario**: User reports JWT token validation failing intermittently

**Dimension Scores**:
- **Domain**: 0.9 (familiar auth patterns in codebase)
- **Pattern**: 0.8 (existing JWT implementation to reference)
- **Dependency**: 0.6 (requires understanding token validation flow)
- **Risk**: 0.4 (security-critical, requires careful testing)

**Calculation**:
- CQ = (0.9×0.4) + (0.8×0.3) + (0.6×0.2) + (0.4×0.1) = **0.73**

**Decision**: ✅ **PROCEED** → Delegate to debugger (high confidence, familiar domain)

---

## Example 2: New Feature - Sentiment Analysis Integration

**Scenario**: User requests adding FinBERT sentiment analysis to news pipeline

**Dimension Scores**:
- **Domain**: 0.3 (unfamiliar ML domain)
- **Pattern**: 0.2 (no existing sentiment analysis in codebase)
- **Dependency**: 0.8 (clear integration points via existing data pipeline)
- **Risk**: 0.6 (medium risk - experimental feature)

**Calculation**:
- CQ = (0.3×0.4) + (0.2×0.3) + (0.8×0.2) + (0.6×0.1) = **0.38**

**Decision**: ❌ **RESEARCH FIRST** → Delegate to researcher-lead (gather ML/NLP context) → RETRY ORIENT

**Action**: researcher-lead → researcher-external (FinBERT best practices, sentiment analysis libraries) → Synthesize → Return to ORIENT with CQ >0.5

---

## Example 3: Update .claude/docs Formatting Standards

**Scenario**: User wants to standardize markdown formatting across .claude/docs/**

**Dimension Scores**:
- **Domain**: 1.0 (complete familiarity with .claude directory)
- **Pattern**: 0.9 (established formatting patterns in docs)
- **Dependency**: 0.3 (cross-document sync required, affects 20+ files)
- **Risk**: 0.2 (low risk - documentation changes)

**Calculation**:
- CQ = (1.0×0.4) + (0.9×0.3) + (0.3×0.2) + (0.2×0.1) = **0.75**

**Decision**: ✅ **PROCEED** → Delegate to documentation (documentation structure specialist)

---

## Example 4: Add Observability to k8s Deployment

**Scenario**: User requests Prometheus/Grafana/Loki integration for Kubernetes cluster

**Dimension Scores**:
- **Domain**: 0.5 (moderate K8s familiarity)
- **Pattern**: 0.6 (some observability patterns exist in other services)
- **Dependency**: 0.7 (integration with Prometheus/Grafana/Loki stack)
- **Risk**: 0.8 (high risk - production infrastructure changes)

**Calculation**:
- CQ = (0.5×0.4) + (0.6×0.3) + (0.7×0.2) + (0.8×0.1) = **0.60**

**Decision**: ✅ **PROCEED** (borderline - monitor closely) → Delegate to deployment-release

**Note**: CQ 0.5-0.7 = borderline confidence. Proceed but verify outputs carefully, consider follow-up research if initial attempt fails.

---

## Example 5: Implement Trading Strategy Backtesting Framework

**Scenario**: User requests building backtesting system for trading strategies

**Dimension Scores**:
- **Domain**: 0.4 (some financial domain knowledge)
- **Pattern**: 0.1 (no existing backtesting framework in codebase)
- **Dependency**: 0.9 (requires integration with market data, patterns, risk modules)
- **Risk**: 0.9 (critical - affects trading decisions)

**Calculation**:
- CQ = (0.4×0.4) + (0.1×0.3) + (0.9×0.2) + (0.9×0.1) = **0.46**

**Decision**: ❌ **RESEARCH FIRST** → Multi-source research required

**Action**:
1. researcher-external (industry best practices for backtesting frameworks)
2. researcher-codebase (existing market data patterns, risk management patterns)
3. Synthesize findings → RETRY ORIENT with enhanced context

---

## Dimension Scoring Guidelines

### Domain (Weight: 0.4 - Highest Impact)
**Score 0.0-0.3**: Unfamiliar territory, no prior experience
**Score 0.4-0.6**: Some knowledge, but gaps exist
**Score 0.7-0.9**: Familiar patterns, confident understanding
**Score 1.0**: Complete mastery, can teach others

### Pattern (Weight: 0.3)
**Score 0.0-0.3**: No existing code patterns to reference
**Score 0.4-0.6**: Some patterns exist but adaptation required
**Score 0.7-0.9**: Clear patterns exist, straightforward application
**Score 1.0**: Identical pattern exists, copy/adapt workflow

### Dependency (Weight: 0.2)
**Score 0.0-0.3**: Complex dependencies, unclear integration points
**Score 0.4-0.6**: Moderate dependencies, some integration clarity
**Score 0.7-0.9**: Clear dependencies, well-defined interfaces
**Score 1.0**: No dependencies or trivial integration

### Risk (Weight: 0.1 - Lowest Impact)
**Score 0.0-0.3**: Low risk (docs, tests, non-critical features)
**Score 0.4-0.6**: Medium risk (user-facing features, data processing)
**Score 0.7-0.9**: High risk (security, auth, payment, production infra)
**Score 1.0**: Critical risk (data loss potential, financial impact)

**Note**: Higher risk score = MORE research needed (inverse relationship to "proceed" confidence)

---

## Edge Cases & Special Scenarios

### Borderline CQ (0.45-0.55)
**Decision Strategy**:
- IF Risk ≥0.7 (high risk) → RESEARCH FIRST (err on side of caution)
- IF Risk <0.7 AND Domain ≥0.6 → PROCEED with monitoring
- IF Risk <0.7 AND Domain <0.6 → RESEARCH FIRST

### Maximum Research (All Dimensions Low)
**Example**: CQ <0.3 with Domain <0.4, Pattern <0.3
**Action**: researcher-lead with ALL workers (researcher-external, researcher-codebase) → Comprehensive context gathering → RETRY ORIENT (may take 3+ iterations)

### Iteration Limit
**Rule**: MAX 3 ORIENT iterations
**If CQ still <0.5 after 3 research cycles** → ESCALATE to user:
- "Insufficient context gathered after 3 research attempts"
- "Recommend: user provides additional requirements/constraints"
- "Alternative: create new specialist agent for this domain"

---

**Last Updated**: 2025-11-21
**Used By**: Orchestrator ORIENT phase (OODA Loop)
**Auto-loaded**: Via startup-eval.py hook
