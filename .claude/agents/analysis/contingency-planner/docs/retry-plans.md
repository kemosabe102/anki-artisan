# Adaptive Retry Plans Guide

**Purpose**: Framework for defining retry plans with max attempts, exponential backoff, escalation triggers, and confidence decay

**Audience**: contingency-planner agent (DECIDE phase component)

**Scope**: Adaptive retry logic for resilient orchestrator execution planning

---

## Retry Plan Definition

### Core Components

Every retry plan must specify:

1. **Max Attempts**: 1-3 retries based on risk score
2. **Backoff Strategy**: Exponential timing (1s, 2s, 4s)
3. **Escalation Triggers**: Conditions for human intervention
4. **Confidence Decay Model**: How failures reduce confidence
5. **Termination Conditions**: When to abandon hypothesis

---

## Max Attempts Determination

### Risk-Based Retry Limits

**HIGH RISK (risk_score ≥ 0.7)**:
- Max attempts: **1**
- Rationale: High-impact failures require rapid escalation
- Example: Critical security vulnerability, data loss risk

**MEDIUM RISK (0.4 ≤ risk_score < 0.7)**:
- Max attempts: **2**
- Rationale: Moderate risk allows automated recovery attempts
- Example: Integration complexity, performance issues

**LOW RISK (risk_score < 0.4)**:
- Max attempts: **3**
- Rationale: Low risk enables full retry sequence
- Example: Configuration errors, minor logic bugs

### Formula

```python
def calculate_max_attempts(highest_risk_score: float) -> int:
    """
    Calculate max retry attempts based on highest risk score across all failure modes.

    Args:
        highest_risk_score: Highest risk_score (probability × impact) from failure modes

    Returns:
        Max attempts: 1-3 retries
    """
    if highest_risk_score >= 0.7:
        return 1  # High risk → rapid escalation
    elif highest_risk_score >= 0.4:
        return 2  # Medium risk → moderate retries
    else:
        return 3  # Low risk → full retry sequence
```

### Template

```json
{
  "max_attempts": 2,
  "max_attempts_rationale": "Highest risk_score is 0.40 (medium) → allows 2 retries before escalation"
}
```

---

## Backoff Strategy

### Exponential Backoff

**Purpose**: Prevent tight retry loops, allow transient issues to resolve

**Formula**: `backoff_interval = base_interval × 2^(attempt - 1)`

**Standard Intervals**:
- Attempt 1: 1 second
- Attempt 2: 2 seconds
- Attempt 3: 4 seconds

**Rationale**: Short intervals appropriate for automated agent retries (not user-facing operations)

### Template

```json
{
  "backoff_strategy": "exponential",
  "backoff_intervals": ["1s", "2s", "4s"],
  "backoff_rationale": "Short intervals (seconds) - automated agent retries, not user-facing"
}
```

### Alternative: Linear Backoff

**When to Use**: Predictable timing requirements, testing scenarios

**Formula**: `backoff_interval = base_interval × attempt`

**Intervals**: 1s, 2s, 3s

---

## Escalation Triggers

### Core Triggers (Always Include)

**1. Max Retries Exhausted**:
```json
{
  "trigger": "retry_count >= max_attempts",
  "threshold": 2,
  "action": "Escalate to human with failure analysis"
}
```

**2. Execution Time Limit**:
```json
{
  "trigger": "execution_time > time_limit",
  "threshold": "10 minutes",
  "action": "Pause execution, return to ORIENT for context enhancement"
}
```

**3. Critical Failure (High Risk)**:
```json
{
  "trigger": "critical_failure",
  "threshold": "risk_score >= 0.7",
  "action": "Immediate escalation, skip retries"
}
```

**4. Confidence Below Threshold**:
```json
{
  "trigger": "confidence_below_threshold",
  "threshold": 0.3,
  "action": "Escalate with low-confidence warning"
}
```

### Template

```json
{
  "escalation_triggers": [
    {
      "trigger": "retry_count >= max_attempts",
      "threshold": 2,
      "action": "Escalate to human with failure analysis"
    },
    {
      "trigger": "execution_time > time_limit",
      "threshold": "10 minutes",
      "action": "Pause execution, return to ORIENT for context enhancement"
    },
    {
      "trigger": "critical_failure",
      "threshold": "risk_score >= 0.7",
      "action": "Immediate escalation, skip retries"
    },
    {
      "trigger": "confidence_below_threshold",
      "threshold": 0.3,
      "action": "Escalate with low-confidence warning"
    }
  ]
}
```

---

## Confidence Decay Model

### Purpose

Model how repeated failures erode confidence in hypothesis, informing escalation decisions.

### Core Parameters

**Initial Confidence**: Starting confidence from orchestrator-provided hypothesis (confidence_score field)

**Decay Per Failure**: Reduction amount per retry failure
- Standard: 0.15 per failure (moderate decay for medium-risk scenarios)
- High-risk: 0.20 per failure (aggressive decay)
- Low-risk: 0.10 per failure (gentle decay)

**Escalation Threshold**: Confidence level triggering human intervention
- Standard: 0.30 (escalate when confidence drops below 30%)

**Confidence Trajectory**: Predicted confidence after each attempt

### Formula

```python
def calculate_confidence_trajectory(
    initial_confidence: float,
    decay_per_failure: float,
    max_attempts: int
) -> list:
    """
    Calculate confidence trajectory across retry attempts.

    Args:
        initial_confidence: Starting confidence (confidence_score from orchestrator)
        decay_per_failure: Confidence reduction per failure (0.10-0.20)
        max_attempts: Maximum retry attempts

    Returns:
        List of confidence values at each attempt
    """
    trajectory = [
        {
            "attempt": 0,
            "confidence": initial_confidence,
            "status": "initial"
        }
    ]

    for attempt in range(1, max_attempts + 1):
        new_confidence = trajectory[-1]["confidence"] - decay_per_failure
        status = "below_threshold_escalate" if new_confidence < 0.30 else f"attempt_{attempt}_failure"

        trajectory.append({
            "attempt": attempt,
            "confidence": new_confidence,
            "status": status
        })

    return trajectory
```

### Template

```json
{
  "confidence_decay_model": {
    "initial_confidence": 0.68,
    "decay_per_failure": 0.15,
    "decay_rationale": "Each failure reduces confidence by 0.15 (moderate decay for medium-risk scenarios)",
    "escalation_threshold": 0.3,
    "confidence_trajectory": [
      { "attempt": 0, "confidence": 0.68, "status": "initial" },
      { "attempt": 1, "confidence": 0.53, "status": "first_failure" },
      { "attempt": 2, "confidence": 0.38, "status": "second_failure" },
      { "attempt": 3, "confidence": 0.23, "status": "below_threshold_escalate" }
    ]
  }
}
```

---

## Termination Conditions

### Purpose

Define when to abandon hypothesis vs continue retrying.

### Standard Conditions

**1. All Fallback Strategies Exhausted**:
- Attempted all 2-3 fallback approaches
- No remaining recovery options
- Action: Escalate to user, mark hypothesis as failed

**2. Confidence Drops Below Threshold**:
- Confidence < 0.30 after repeated failures
- Low probability of success even with retries
- Action: Escalate to user, recommend alternative hypothesis

**3. User Requests Termination**:
- User explicitly cancels execution
- Business priorities changed
- Action: Stop immediately, document progress

**4. Critical System Error Detected**:
- Unrecoverable error (file system, network, security)
- Agent incapable of resolution
- Action: Immediate escalation to user

### Template

```json
{
  "termination_conditions": [
    "All fallback strategies exhausted",
    "Confidence drops below 0.30",
    "User requests termination",
    "Critical system error detected"
  ]
}
```

---

## Escalation Paths

### Risk-Based Escalation Strategy

**HIGH RISK (risk_score ≥ 0.7)**:
```json
{
  "high_risk_scenario": {
    "condition": "risk_score >= 0.7",
    "path": "Immediate human escalation, skip automated retries",
    "rationale": "High-impact failures require human judgment"
  }
}
```

**MEDIUM RISK (0.4 ≤ risk_score < 0.7)**:
```json
{
  "medium_risk_scenario": {
    "condition": "0.4 <= risk_score < 0.7",
    "path": "Attempt 2 retries with fallback strategies, escalate if unsuccessful",
    "rationale": "Moderate risk allows automated recovery attempts"
  }
}
```

**LOW RISK (risk_score < 0.4)**:
```json
{
  "low_risk_scenario": {
    "condition": "risk_score < 0.4",
    "path": "Standard retry with exponential backoff, escalate after max_attempts",
    "rationale": "Low risk enables full retry sequence"
  }
}
```

### Template

```json
{
  "escalation_paths": {
    "high_risk_scenario": {
      "condition": "risk_score >= 0.7",
      "path": "Immediate human escalation, skip automated retries",
      "rationale": "High-impact failures require human judgment"
    },
    "medium_risk_scenario": {
      "condition": "0.4 <= risk_score < 0.7",
      "path": "Attempt 2 retries with fallback strategies, escalate if unsuccessful",
      "rationale": "Moderate risk allows automated recovery attempts"
    },
    "low_risk_scenario": {
      "condition": "risk_score < 0.4",
      "path": "Standard retry with exponential backoff, escalate after max_attempts",
      "rationale": "Low risk enables full retry sequence"
    }
  }
}
```

---

## Complete Retry Plan Example

**Context**: Redis cache implementation with highest risk_score = 0.40 (medium)

```json
{
  "retry_plan": {
    "max_attempts": 2,
    "max_attempts_rationale": "Highest risk_score is 0.40 (medium) → allows 2 retries before escalation",
    "backoff_strategy": "exponential",
    "backoff_intervals": ["1s", "2s"],
    "backoff_rationale": "Short intervals (seconds) - automated agent retries, not user-facing",
    "escalation_triggers": [
      {
        "trigger": "retry_count >= max_attempts",
        "threshold": 2,
        "action": "Escalate to human with failure analysis"
      },
      {
        "trigger": "execution_time > time_limit",
        "threshold": "10 minutes",
        "action": "Pause execution, return to ORIENT for context enhancement"
      },
      {
        "trigger": "critical_failure",
        "threshold": "risk_score >= 0.7",
        "action": "Immediate escalation, skip retries"
      },
      {
        "trigger": "confidence_below_threshold",
        "threshold": 0.3,
        "action": "Escalate with low-confidence warning"
      }
    ],
    "confidence_decay_model": {
      "initial_confidence": 0.68,
      "decay_per_failure": 0.15,
      "decay_rationale": "Each failure reduces confidence by 0.15 (moderate decay for medium-risk scenarios)",
      "escalation_threshold": 0.3,
      "confidence_trajectory": [
        { "attempt": 0, "confidence": 0.68, "status": "initial" },
        { "attempt": 1, "confidence": 0.53, "status": "first_failure" },
        { "attempt": 2, "confidence": 0.38, "status": "second_failure" },
        { "attempt": 3, "confidence": 0.23, "status": "below_threshold_escalate" }
      ]
    },
    "termination_conditions": [
      "All fallback strategies exhausted",
      "Confidence drops below 0.30",
      "User requests termination",
      "Critical system error detected"
    ],
    "escalation_paths": {
      "high_risk_scenario": {
        "condition": "risk_score >= 0.7",
        "path": "Immediate human escalation, skip automated retries",
        "rationale": "High-impact failures require human judgment"
      },
      "medium_risk_scenario": {
        "condition": "0.4 <= risk_score < 0.7",
        "path": "Attempt 2 retries with fallback strategies, escalate if unsuccessful",
        "rationale": "Moderate risk allows automated recovery attempts"
      },
      "low_risk_scenario": {
        "condition": "risk_score < 0.4",
        "path": "Standard retry with exponential backoff, escalate after max_attempts",
        "rationale": "Low risk enables full retry sequence"
      }
    }
  }
}
```

---

## Execution Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│ Hypothesis Execution Starts                                     │
│ Initial Confidence: 0.68                                        │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│ Attempt 1: Execute Hypothesis                                   │
└──────┬──────────────────────────────────────────┬───────────────┘
       │ SUCCESS                                   │ FAILURE
       ▼                                           ▼
┌──────────────┐                    ┌──────────────────────────────┐
│ Complete     │                    │ Confidence Decay: 0.68→0.53  │
│              │                    │ Backoff: Wait 1s             │
└──────────────┘                    └─────────┬────────────────────┘
                                              │
                                              ▼
                                   ┌──────────────────────────────┐
                                   │ Attempt 2: Try Fallback      │
                                   └─────┬────────────────┬───────┘
                                         │ SUCCESS        │ FAILURE
                                         ▼                ▼
                                   ┌────────────┐ ┌──────────────────┐
                                   │ Complete   │ │ Confidence: 0.38 │
                                   │            │ │ Backoff: Wait 2s │
                                   └────────────┘ └─────┬────────────┘
                                                        │
                                                        ▼
                                         ┌──────────────────────────┐
                                         │ Check Escalation Trigger │
                                         │ - Max retries? YES       │
                                         │ - Confidence <0.3? NO    │
                                         │ - Time >10min? NO        │
                                         └─────┬────────────────────┘
                                               │
                                               ▼
                                         ┌─────────────────────┐
                                         │ ESCALATE TO HUMAN   │
                                         │ Provide failure log │
                                         └─────────────────────┘
```

---

## Best Practices

1. **Risk-based max attempts** - Use formula to determine 1-3 retries
2. **Exponential backoff** - Standard 1s, 2s, 4s intervals for agents
3. **Multiple escalation triggers** - Max retries, time limit, confidence, critical failure
4. **Confidence decay modeling** - Track hypothesis viability across attempts
5. **Clear termination conditions** - Define when to abandon vs escalate
6. **Risk-specific escalation paths** - High/medium/low risk strategies
7. **Document rationale** - Explain why max attempts, decay rate chosen

---

**Related Guides**:
- `../contingency-planner.md` - Agent definition and workflow integration
- `failure-mode-analysis.md` - Calculating risk scores that drive retry limits
- `fallback-strategies.md` - Generating 2-3 fallback strategies to execute during retries
- `../examples/contingency-examples.md` - Complete examples with retry plans
