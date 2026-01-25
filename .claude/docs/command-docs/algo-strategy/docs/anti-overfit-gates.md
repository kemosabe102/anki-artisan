# Anti-Overfit Gates

**Purpose**: Prevent curve-fitting and parameter p-hacking in strategy development.

**When to Reference**: P2 hypothesis phase (hard constraints) | P6 validation (soft constraints) | Constraint violations

---

## Core Principle

> **Statistical rigor before optimization.** Every additional parameter, trial, or data point reduces degrees of freedom.

Overfitting occurs when a strategy learns noise instead of signal. These gates enforce discipline.

---

## Overview

| ID | Constraint | Type | Phase | Threshold | Action |
|----|------------|------|-------|-----------|--------|
| HC-1 | Parameter Count | Hard | P2 | < 10 params | BLOCK |
| HC-2 | Parameter Ranges | Hard | P2 | < 3x span | BLOCK |
| HC-3 | Max Trials | Hard | P2, P6 | < 30 trials | BLOCK |
| SC-1 | Trade Count | Soft | P6 | >= 100 trades | WARN |
| SC-2 | IS/OOS Delta | Soft | P6 | < 30% delta | WARN |
| SC-3 | Plateau Rule | Soft | P6 | Required | WARN |


---

## Hard Constraints

Hard constraints BLOCK strategy creation. Violations prevent hypothesis formation.

### HC-1: Parameter Count Limit

| Attribute | Value |
|-----------|-------|
| **Threshold** | `PARAM_COUNT < 10` |
| **Check Phase** | P2 (Hypothesis Formation) |
| **Error Code** | `OVERFIT_PARAM_COUNT` |

**Rationale**: Each parameter consumes one degree of freedom. Strategies with 10+ parameters almost always overfit to historical noise. The classic rule: `n_params < sqrt(n_trades)`.

**User-Facing Block Message**:

```
PARAMETER COUNT EXCEEDED

Your hypothesis specifies 12 parameters. Maximum allowed: 9

Current parameters:
  1. entry_rsi_period (14)
  2. entry_rsi_threshold (30)
  3. exit_rsi_period (14)
  4. exit_rsi_threshold (70)
  5. stop_loss_pct (2.0)
  6. take_profit_pct (4.0)
  7. position_size_pct (10.0)
  8. lookback_days (20)
  9. volume_threshold (1.5)
  10. volatility_filter (0.02)    <-- LIMIT
  11. trend_filter_period (50)    <-- EXCEEDS
  12. momentum_threshold (0.01)   <-- EXCEEDS

YOUR OPTIONS:
1. REMOVE 3 parameters - Simplify to core signal logic
2. COMBINE parameters - Use derived metrics (e.g., ATR-based stops)
3. FIX parameters - Lock some values as constants (not optimizable)

Command: /algo-strategy --simplify HYP-001
```


---

### HC-2: Parameter Range Limit

| Attribute | Value |
|-----------|-------|
| **Threshold** | `PARAM_RANGE < 3x span` |
| **Check Phase** | P2 (Hypothesis Formation) |
| **Error Code** | `OVERFIT_PARAM_RANGE` |

**Rationale**: Wide parameter ranges (e.g., RSI 5-50) create massive search spaces that guarantee finding spurious patterns. A 3x span ensures parameters stay within economically meaningful bounds.

**Calculation**: `span = max_value / min_value` (for each parameter)

**User-Facing Block Message**:

```
PARAMETER RANGE TOO WIDE

Parameter "rsi_period" has excessive range:
  Specified: 5 to 50 (span = 10x)
  Maximum allowed: 3x span

Wide ranges enable curve-fitting by testing thousands of combinations.

YOUR OPTIONS:
1. NARROW the range based on economic rationale
   Example: RSI(10-21) for 2-4 week momentum
   Command: /algo-strategy --narrow-param rsi_period 10 21

2. FIX the parameter to a single value
   Example: RSI(14) as industry standard
   Command: /algo-strategy --fix-param rsi_period 14

3. JUSTIFY the wide range (requires documented rationale)
   Command: /algo-strategy --justify-range rsi_period "[rationale]"
```


---

### HC-3: Maximum Trials Limit

| Attribute | Value |
|-----------|-------|
| **Threshold** | `MAX_TRIALS < 30` |
| **Check Phase** | P2 (Formation), P6 (Validation) |
| **Error Code** | `OVERFIT_TRIAL_LIMIT` |

**Rationale**: With 30 independent trials, there's a 78% probability of finding a "significant" result by chance (p=0.05). Trial count is tracked per hypothesis_id and resets only with new hypothesis.

**User-Facing Block Message**:

```
TRIAL LIMIT EXCEEDED

Hypothesis HYP-001 has exhausted its trial budget.
  Trials used: 30/30
  Unique parameter combinations tested: 30

Continuing to test exhausts statistical significance.
At 30 trials with p=0.05, false discovery probability = 78%

YOUR OPTIONS:
1. ARCHIVE this hypothesis - Document learnings, move to graveyard
   Command: /algo-strategy --archive HYP-001 "[learnings]"

2. CREATE NEW HYPOTHESIS - Fresh rationale required
   This resets the trial counter to 0
   Command: /algo-strategy --new "[new hypothesis with different rationale]"

BLOCKED: Further trials on HYP-001 are not permitted.
```


---

## Soft Constraints

Soft constraints generate WARNINGS but allow continuation. User must acknowledge risk.

### SC-1: Minimum Trade Count

| Attribute | Value |
|-----------|-------|
| **Threshold** | `TRADE_COUNT >= 100` |
| **Check Phase** | P6 (Validation) |
| **Warning Code** | `WARN_LOW_SAMPLE` |

**Rationale**: Statistical significance requires sufficient sample size. With <100 trades, confidence intervals are too wide for reliable conclusions. Standard error of Sharpe ratio: `SE = sqrt((1 + 0.5*SR^2) / n)`.

**Warning Behavior**: Display warning, require user acknowledgment, log to hypothesis audit trail.

**User-Facing Warn Message**:

```
WARNING: INSUFFICIENT TRADE COUNT

Backtest generated only 47 trades. Minimum recommended: 100

Statistical implications:
  - Sharpe ratio confidence interval: +/- 0.45 (very wide)
  - Win rate estimate: 62% +/- 14% (unreliable)
  - Results may not generalize to live trading

OPTIONS:
[1] EXTEND TIMEFRAME - Add more historical data
    Command: /algo-strategy --extend 2005-2024

[2] REDUCE HOLDING PERIOD - Generate more trades
    Requires NEW hypothesis (parameter change)

[3] ACKNOWLEDGE and CONTINUE (not recommended)
    Command: /algo-strategy --acknowledge-low-sample

Proceeding without acknowledgment? [y/N]
```


---

### SC-2: In-Sample/Out-of-Sample Delta

| Attribute | Value |
|-----------|-------|
| **Threshold** | `IS_OOS_DELTA < 30%` |
| **Check Phase** | P6 (Validation) |
| **Warning Code** | `WARN_OVERFIT_DELTA` |

**Rationale**: Large performance degradation between in-sample and out-of-sample periods indicates overfitting. A strategy that achieves Sharpe 2.0 in-sample but 0.8 out-of-sample (60% delta) has learned noise, not signal.

**Calculation**: `delta = abs(IS_sharpe - OOS_sharpe) / IS_sharpe * 100`

**Warning Behavior**: Highlight degradation, recommend additional validation, suggest regime analysis.

**User-Facing Warn Message**:

```
WARNING: SIGNIFICANT IN-SAMPLE/OUT-OF-SAMPLE DEGRADATION

Performance comparison:
  In-Sample (2010-2020):   Sharpe 1.85 | CAGR 18.2% | MaxDD -12%
  Out-of-Sample (2021-24): Sharpe 0.92 | CAGR 8.4%  | MaxDD -22%

  Delta: 50% degradation (threshold: <30%)

This pattern suggests overfitting to in-sample characteristics.

DIAGNOSTIC QUESTIONS:
- Did market regime change between periods?
- Are key parameters at boundary values?
- Is signal frequency consistent across periods?

OPTIONS:
[1] RUN REGIME ANALYSIS - Identify structural differences
    Command: /algo-strategy --regime-analysis HYP-001

[2] WALK-FORWARD VALIDATION - Test robustness across rolling windows
    Command: /algo-strategy --walk-forward HYP-001

[3] ACKNOWLEDGE and CONTINUE (with caution flag)
    Command: /algo-strategy --acknowledge-delta

Strategy will be flagged as HIGH_OVERFIT_RISK in production.
```


---

### SC-3: Plateau Rule

| Attribute | Value |
|-----------|-------|
| **Threshold** | Plateau detection required |
| **Check Phase** | P6 (Validation) |
| **Warning Code** | `WARN_NO_PLATEAU` |

**Rationale**: Robust parameters exist in "plateau" regions where small changes don't dramatically affect performance. Parameters at local maxima (peaks) are fragile and likely overfit.

**Detection**: Performance variance within +/- 10% parameter change should be < 15%.

**Warning Behavior**: Display sensitivity analysis, recommend parameter adjustment, flag fragile params.

**User-Facing Warn Message**:

```
WARNING: PARAMETER SENSITIVITY DETECTED (NO PLATEAU)

Parameter "rsi_period" shows high sensitivity:

  RSI(12): Sharpe 0.89  |  -18% from optimal
  RSI(13): Sharpe 1.02  |  -6% from optimal
  RSI(14): Sharpe 1.09  |  SELECTED (optimal)
  RSI(15): Sharpe 0.78  |  -28% from optimal
  RSI(16): Sharpe 0.65  |  -40% from optimal

  Variance within +/-10%: 34% (threshold: <15%)

This parameter is at a LOCAL PEAK, not a plateau.
Small market changes could significantly degrade performance.

OPTIONS:
[1] FIND PLATEAU - Search for stable parameter region
    Command: /algo-strategy --find-plateau rsi_period

[2] FIX TO STANDARD - Use industry-standard value (less optimal but robust)
    Command: /algo-strategy --fix-param rsi_period 14 --rationale "industry standard"

[3] ACKNOWLEDGE sensitivity (production will include monitoring)
    Command: /algo-strategy --acknowledge-sensitivity rsi_period
```


---

## Gate Enforcement Matrix

| Gate | P1 Universe | P2 Hypothesis | P3 Backtest | P4 Analysis | P5 Execution | P6 Validation |
|------|-------------|---------------|-------------|-------------|--------------|---------------|
| HC-1 | - | **BLOCK** | - | - | - | - |
| HC-2 | - | **BLOCK** | - | - | - | - |
| HC-3 | - | **CHECK** | - | - | - | **BLOCK** |
| SC-1 | - | - | - | - | - | **WARN** |
| SC-2 | - | - | - | - | - | **WARN** |
| SC-3 | - | - | - | - | - | **WARN** |

**Legend**:
- **BLOCK**: Prevents phase completion, requires resolution
- **CHECK**: Verifies counter state, blocks if exceeded
- **WARN**: Displays warning, requires acknowledgment to proceed
- **-**: Not applicable in this phase


---

## Violation Flow

### Hard Constraint Violation

```python
def check_hard_constraints(hypothesis: HypothesisBundle) -> GateResult:
    violations = []
    
    # HC-1: Parameter count
    if len(hypothesis.params_locked) >= 10:
        violations.append(GateViolation(
            code="OVERFIT_PARAM_COUNT",
            severity="HARD",
            message=f"Parameter count {len(hypothesis.params_locked)} exceeds limit 9",
            resolution_options=["simplify", "combine", "fix_params"]
        ))
    
    # HC-2: Parameter ranges
    for param_name, param_def in hypothesis.params_locked.items():
        if "range" in param_def:
            span = param_def["range"]["max"] / param_def["range"]["min"]
            if span >= 3.0:
                violations.append(GateViolation(
                    code="OVERFIT_PARAM_RANGE",
                    severity="HARD",
                    message=f"Parameter '{param_name}' span {span:.1f}x exceeds 3x limit",
                    resolution_options=["narrow_range", "fix_param", "justify"]
                ))
    
    # HC-3: Trial count
    if hypothesis.trial_count >= 30:
        violations.append(GateViolation(
            code="OVERFIT_TRIAL_LIMIT",
            severity="HARD",
            message=f"Trial count {hypothesis.trial_count} reached limit 30",
            resolution_options=["archive", "new_hypothesis"]
        ))
    
    # BLOCK if any hard violations
    if violations:
        return GateResult(
            passed=False,
            violations=violations,
            action="BLOCK",
            display_message=format_block_message(violations)
        )
    
    return GateResult(passed=True, violations=[], action="PROCEED")
```


### Soft Constraint Violation

```python
def check_soft_constraints(backtest_result: BacktestResult) -> GateResult:
    warnings = []
    
    # SC-1: Trade count
    if backtest_result.trade_count < 100:
        warnings.append(GateViolation(
            code="WARN_LOW_SAMPLE",
            severity="SOFT",
            message=f"Trade count {backtest_result.trade_count} below minimum 100",
            requires_acknowledgment=True
        ))
    
    # SC-2: IS/OOS delta
    if backtest_result.is_sharpe and backtest_result.oos_sharpe:
        delta = abs(backtest_result.is_sharpe - backtest_result.oos_sharpe) 
        delta_pct = delta / backtest_result.is_sharpe * 100
        if delta_pct >= 30:
            warnings.append(GateViolation(
                code="WARN_OVERFIT_DELTA",
                severity="SOFT",
                message=f"IS/OOS delta {delta_pct:.0f}% exceeds 30% threshold",
                requires_acknowledgment=True
            ))
    
    # SC-3: Plateau rule
    if not backtest_result.plateau_detected:
        warnings.append(GateViolation(
            code="WARN_NO_PLATEAU",
            severity="SOFT",
            message="No parameter plateau detected (high sensitivity)",
            requires_acknowledgment=True
        ))
    
    # WARN but allow continuation with acknowledgment
    if warnings:
        return GateResult(
            passed=True,  # Soft = can proceed
            violations=warnings,
            action="WARN",
            requires_user_acknowledgment=True,
            display_message=format_warning_message(warnings)
        )
    
    return GateResult(passed=True, violations=[], action="PROCEED")
```


---

## Summary

| Constraint | Type | Threshold | Phase | Violation Action |
|------------|------|-----------|-------|------------------|
| HC-1 Parameter Count | Hard | < 10 | P2 | BLOCK |
| HC-2 Parameter Ranges | Hard | < 3x span | P2 | BLOCK |
| HC-3 Max Trials | Hard | < 30 | P2, P6 | BLOCK |
| SC-1 Trade Count | Soft | >= 100 | P6 | WARN + acknowledge |
| SC-2 IS/OOS Delta | Soft | < 30% | P6 | WARN + acknowledge |
| SC-3 Plateau Rule | Soft | Required | P6 | WARN + acknowledge |

---

**Related**: [HDD Methodology](./hdd-methodology.md) | [Revision Guard Rails](./revision-guard-rails.md) | [Workflow Phases](./workflow-phases.md)

