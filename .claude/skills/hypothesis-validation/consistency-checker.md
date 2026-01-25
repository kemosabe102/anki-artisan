---
name: consistency-checker
description: >
  Validates hypothesis-spec alignment for P5 gate in /algo-strategy command. Enforces 4 consistency rules:
  timeframe alignment, signal logic, parameter binding, mechanism soundness.
  Trigger keywords: consistency check, hypothesis validation, spec alignment, P5 gate.
---

# Consistency Checker Skill

*Hypothesis-Spec Alignment Validation for P5 Gate*

## Quick Reference

| Aspect | Requirement |
|--------|-------------|
| Purpose | Validate hypothesis-spec consistency in P5 |
| Rules | 4 (Timeframe, Signal, Parameter, Mechanism) |
| Blocking | TIMEFRAME_ALIGNMENT, SIGNAL_LOGIC, PARAMETER_BINDING |
| Warning | MECHANISM_SOUNDNESS |
| Output | ConsistencyResult with violations list |

---

## The 4 Consistency Rules

### Rule 1: Timeframe Alignment (BLOCKING)

```
hypothesis.timeframe == spec.timeframe
```

| Hypothesis | Spec | Verdict |
|------------|------|---------|
| "4-hour bars" | `timeframe: "4hour"` | PASS |
| "4-hour bars" | `timeframe: "1hour"` | FAIL |
| "daily" | `timeframe: "daily"` | PASS |

**Violation Message**:
> Timeframe mismatch: Hypothesis specifies "{hypothesis.timeframe}" but spec uses "{spec.timeframe}".

---

### Rule 2: Signal Logic (BLOCKING)

Entry conditions MUST use indicators mentioned in hypothesis.

```
for indicator in hypothesis.mentioned_indicators:
    assert indicator in spec.get_all_indicators()
```

| Hypothesis Indicator | Spec Entry | Verdict |
|---------------------|------------|---------|
| RSI > 70 | `rsi_14 > 70` | PASS |
| RSI > 70 | `macd_crossover` | FAIL |
| EMA crossover | `ema_20 > ema_50` | PASS |

**Violation Message**:
> Signal logic mismatch: Hypothesis mentions "{indicator}" but spec entry uses [{spec_indicators}].

---

### Rule 3: Parameter Binding (BLOCKING)

Locked parameters MUST appear unchanged in spec.

```
for param_name, param_value in hypothesis.params_locked.items():
    assert spec.get_param(param_name) == param_value["value"]
```

| Locked Param | Spec Value | Verdict |
|--------------|------------|---------|
| `ema_fast: 20` | `ema_period: 20` | PASS |
| `ema_fast: 20` | `ema_period: 25` | FAIL |
| `rsi_period: 14` | `rsi_period: 14` | PASS |

**Violation Message**:
> Parameter binding violation: "{param_name}" locked at {locked_value} but spec uses {spec_value}.

---

### Rule 4: Mechanism Soundness (WARNING)

Strategy type SHOULD align with hypothesis mechanism.

```
hypothesis.mechanism_type ~= spec.strategy_type
```

| Hypothesis Mechanism | Spec Type | Verdict |
|---------------------|-----------|---------|
| momentum continuation | `momentum` | PASS |
| momentum continuation | `mean_reversion` | WARN |
| oversold reversal | `mean_reversion` | PASS |

**Violation Message**:
> Mechanism mismatch: Hypothesis describes "{mechanism_type}" but spec is "{strategy_type}".

---

## Validation Function Signature

```python
def validate_hypothesis_spec_consistency(
    hypothesis: HypothesisBundle, 
    spec: StrategySpec
) -> ConsistencyResult:
    """
    Validate alignment between hypothesis and generated strategy spec.
    
    Args:
        hypothesis: HypothesisBundle from P2 (hypothesis formulation phase)
        spec: StrategySpec from P4 (delegation phase output)
    
    Returns:
        ConsistencyResult with valid flag and violations list
    """
    violations = []
    
    # Rule 1: Timeframe alignment
    if hypothesis.timeframe != spec.timeframe:
        violations.append(ConsistencyViolation(
            rule="TIMEFRAME_ALIGNMENT",
            severity="BLOCKING",
            hypothesis_value=hypothesis.timeframe,
            spec_value=spec.timeframe,
            message=f"Timeframe mismatch: Hypothesis specifies '{hypothesis.timeframe}' "
                    f"but spec uses '{spec.timeframe}'"
        ))
    
    # Rule 2: Signal logic
    for indicator in hypothesis.mentioned_indicators:
        if indicator not in spec.get_all_indicators():
            violations.append(ConsistencyViolation(
                rule="SIGNAL_LOGIC",
                severity="BLOCKING",
                hypothesis_value=indicator,
                spec_value=spec.get_all_indicators(),
                message=f"Signal logic mismatch: Hypothesis mentions '{indicator}' "
                        f"but spec entry uses {spec.get_all_indicators()}"
            ))
    
    # Rule 3: Parameter binding
    for param_name, param_value in hypothesis.params_locked.items():
        spec_value = spec.get_param(param_name)
        if spec_value != param_value["value"]:
            violations.append(ConsistencyViolation(
                rule="PARAMETER_BINDING",
                severity="BLOCKING",
                hypothesis_value=param_value["value"],
                spec_value=spec_value,
                message=f"Parameter binding violation: '{param_name}' locked at "
                        f"{param_value['value']} but spec uses {spec_value}"
            ))
    
    # Rule 4: Mechanism soundness
    if hypothesis.mechanism_type != spec.strategy_type:
        violations.append(ConsistencyViolation(
            rule="MECHANISM_SOUNDNESS",
            severity="WARNING",
            hypothesis_value=hypothesis.mechanism_type,
            spec_value=spec.strategy_type,
            message=f"Mechanism mismatch: Hypothesis describes '{hypothesis.mechanism_type}' "
                    f"but spec is '{spec.strategy_type}'"
        ))
    
    return ConsistencyResult(
        valid=len([v for v in violations if v.severity == "BLOCKING"]) == 0,
        violations=violations
    )
```

---

## ConsistencyViolation Schema

```python
{
    "rule": str,  # TIMEFRAME_ALIGNMENT | SIGNAL_LOGIC | PARAMETER_BINDING | MECHANISM_SOUNDNESS
    "severity": str,  # BLOCKING | WARNING
    "hypothesis_value": Any,  # Value from hypothesis
    "spec_value": Any,  # Value from spec
    "message": str  # Human-readable error message
}
```

### ConsistencyResult Schema

```python
{
    "valid": bool,  # True if no BLOCKING violations
    "violations": List[ConsistencyViolation]  # All violations (BLOCKING + WARNING)
}
```

---

## Error Response Templates

### TIMEFRAME_ALIGNMENT Violation

```
CONSISTENCY CHECK FAILED (P5)

Rule: TIMEFRAME_ALIGNMENT
Severity: BLOCKING

Hypothesis timeframe: "4-hour bars"
Spec timeframe: "1-hour"

Action: Regenerate spec with correct timeframe or revise hypothesis.
```

### SIGNAL_LOGIC Violation

```
CONSISTENCY CHECK FAILED (P5)

Rule: SIGNAL_LOGIC
Severity: BLOCKING

Hypothesis indicator: RSI
Spec entry indicators: [MACD, EMA]

Action: Spec must use indicators from hypothesis. Regenerate or revise.
```

### PARAMETER_BINDING Violation

```
CONSISTENCY CHECK FAILED (P5)

Rule: PARAMETER_BINDING
Severity: BLOCKING

Locked parameter: ema_fast = 20
Spec value: ema_period = 25

Action: Locked parameters cannot be changed. Regenerate spec with locked values.
```

### MECHANISM_SOUNDNESS Violation

```
CONSISTENCY CHECK WARNING (P5)

Rule: MECHANISM_SOUNDNESS
Severity: WARNING

Hypothesis mechanism: momentum continuation
Spec strategy type: mean_reversion

Action: Review if strategy type aligns with hypothesis reasoning. Proceed with caution.
```

---

## P5 Gate Integration

### How P5 Gate Calls This Checker

```python
# In /algo-strategy command P5 phase
def p5_validate(hypothesis_bundle, strategy_spec, qc_skeleton):
    """P5 Validation Gate - Schema + Syntax + Consistency"""
    
    # Step 1: Schema validation
    schema_result = validate_spec_schema(strategy_spec)
    if not schema_result.valid:
        return P5Result(passed=False, error="ALGO_ERR_006", details=schema_result)
    
    # Step 2: QC skeleton syntax check
    syntax_result = validate_qc_syntax(qc_skeleton)
    if not syntax_result.valid:
        return P5Result(passed=False, error="ALGO_ERR_007", details=syntax_result)
    
    # Step 3: Hypothesis-spec consistency (THIS CHECKER)
    consistency_result = validate_hypothesis_spec_consistency(
        hypothesis=hypothesis_bundle,
        spec=strategy_spec
    )
    
    if not consistency_result.valid:
        return P5Result(
            passed=False, 
            error="ALGO_ERR_008",
            details=consistency_result.violations
        )
    
    # Step 4: Pass with warnings if any
    warnings = [v for v in consistency_result.violations if v.severity == "WARNING"]
    return P5Result(passed=True, warnings=warnings)
```

### P5 Gate Decision Matrix

| Schema | Syntax | Consistency | Result |
|--------|--------|-------------|--------|
| PASS | PASS | PASS (no blocking) | Proceed to P6 |
| PASS | PASS | WARN only | Proceed with warnings |
| PASS | PASS | BLOCKING | HALT, return ALGO_ERR_008 |
| PASS | FAIL | - | HALT, return ALGO_ERR_007 |
| FAIL | - | - | HALT, return ALGO_ERR_006 |

---

## Examples

### Valid Case: All Rules Pass

**Hypothesis:**
```json
{
  "hypothesis_id": "H001",
  "timeframe": "daily",
  "mentioned_indicators": ["RSI", "SMA"],
  "params_locked": {
    "rsi_period": {"value": 14, "locked": true},
    "sma_period": {"value": 200, "locked": true}
  },
  "mechanism_type": "mean_reversion"
}
```

**Spec:**
```json
{
  "timeframe": "daily",
  "entry": {"conditions": ["rsi_14 < 30", "close > sma_200"]},
  "strategy_type": "mean_reversion",
  "indicators": ["RSI", "SMA"],
  "params": {"rsi_period": 14, "sma_period": 200}
}
```

**Result:** `ConsistencyResult(valid=True, violations=[])`

---

### Invalid Case: Multiple Violations

**Hypothesis:**
```json
{
  "hypothesis_id": "H002",
  "timeframe": "4hour",
  "mentioned_indicators": ["RSI"],
  "params_locked": {
    "rsi_period": {"value": 14, "locked": true}
  },
  "mechanism_type": "momentum"
}
```

**Spec:**
```json
{
  "timeframe": "1hour",
  "entry": {"conditions": ["macd_crossover"]},
  "strategy_type": "mean_reversion",
  "indicators": ["MACD"],
  "params": {"rsi_period": 21}
}
```

**Result:**
```python
ConsistencyResult(
    valid=False,
    violations=[
        ConsistencyViolation(
            rule="TIMEFRAME_ALIGNMENT",
            severity="BLOCKING",
            hypothesis_value="4hour",
            spec_value="1hour",
            message="Timeframe mismatch: Hypothesis specifies '4hour' but spec uses '1hour'"
        ),
        ConsistencyViolation(
            rule="SIGNAL_LOGIC",
            severity="BLOCKING",
            hypothesis_value="RSI",
            spec_value=["MACD"],
            message="Signal logic mismatch: Hypothesis mentions 'RSI' but spec entry uses ['MACD']"
        ),
        ConsistencyViolation(
            rule="PARAMETER_BINDING",
            severity="BLOCKING",
            hypothesis_value=14,
            spec_value=21,
            message="Parameter binding violation: 'rsi_period' locked at 14 but spec uses 21"
        ),
        ConsistencyViolation(
            rule="MECHANISM_SOUNDNESS",
            severity="WARNING",
            hypothesis_value="momentum",
            spec_value="mean_reversion",
            message="Mechanism mismatch: Hypothesis describes 'momentum' but spec is 'mean_reversion'"
        )
    ]
)
```

---

## Reference Documentation

| Reference | Purpose |
|-----------|---------|
| `.claude/skills/hypothesis-formulation/SKILL.md` | Hypothesis structure |
| `.claude/skills/strategy-specification/SKILL.md` | Spec schema, 7-element framework |
| `.claude/skills/hypothesis-tracking/SKILL.md` | Lifecycle, graveyard |
