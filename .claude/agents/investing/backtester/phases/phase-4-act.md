# Phase 4: ACT - Execution, Aggregation, Gates, and Routing

**OODA Stage**: ACT | **Time Allocation**: 55-65%

**Purpose**: Execute backtest, aggregate metrics, evaluate gates, route verdict

**Deliverable**: Backtest result with verdict (DEPLOYABLE/NOT_DEPLOYABLE) and next_action

---

## Error Classification (MANDATORY)

**Before attempting fixes, classify error type:**

| Error Pattern | Classification | Action |
|---------------|----------------|--------|
| "unauthorized", "forbidden", 401, 403 | AUTH_ERROR | BLOCKED - credential refresh needed |
| "syntax error", "compilation failed", "invalid syntax" | COMPILE_ERROR | Local fix allowed (max 3 attempts) |
| "timeout", "connection refused", "ETIMEDOUT" | NETWORK_ERROR | Retry with backoff (max 2 attempts) |
| "project not found", "invalid project", "no such directory" | PROJECT_ERROR | BLOCKED - project setup needed |
| "rate limit", "too many requests", 429 | RATE_LIMIT_ERROR | Wait and retry (exponential backoff) |
| "insufficient data", "no trades" | DATA_ERROR | BLOCKED - data range adjustment needed |

**Classification Rules**:
1. AUTH_ERROR and PROJECT_ERROR are NEVER auto-fixable -> always BLOCKED
2. COMPILE_ERROR allows max 3 fix attempts before BLOCKED
3. NETWORK_ERROR allows max 2 retries with exponential backoff
4. RATE_LIMIT_ERROR follows QC API rate limit guidelines

**NEVER** treat AUTH_ERROR as COMPILE_ERROR - they require different remediation.

---

## Mode Execution Overview

### single_run Mode

Execute ONE backtest per hypothesis submission.

**Steps**:
1. VALIDATE hypothesis_id exists
2. VERIFY trial_number <= 5
3. EXECUTE single backtest run via Lean CLI
4. CALCULATE raw metrics (Sharpe, drawdown, trade_count)
5. APPLY deflation (see DSR calculation)
6. EVALUATE validation gates
7. RETURN verdict with next_action

**Command**:
```bash
lean backtest Algorithms/{algorithm_name} --output {run_id}
```

---

### tier_test Mode

Execute backtests across all periods defined for a tier.


**Steps**:
1. LOAD tier configuration from tier-config.json
2. EXTRACT period list for specified tier
3. FOR EACH period:
   a. INJECT start_date/end_date into algorithm
   b. EXECUTE: `lean backtest Algorithms/{name}`
   c. PARSE: `{id}-summary.json` for metrics
   d. SAVE: period result to checkpoint
4. AGGREGATE metrics across periods
5. APPLY deflation (Tier 4 only)
6. EVALUATE tier-specific gates
7. RETURN tier verdict with period breakdown

---

### regime_test Mode

Test strategy across volatility regimes.

**Steps**:
1. DELEGATE to `Task(regime-classifier, "Classify regime for test period")`
2. EXECUTE backtest on each regime (HIGH_RISK, ELEVATED, NORMAL, LOW_RISK)
3. COMPARE performance across regimes
4. CALCULATE regime_consistency_score
5. FLAG regime_mismatch if Sharpe variance > 50%
6. RETURN consolidated verdict with regime breakdown

---

### walk_forward Mode

Rolling window out-of-sample validation.

**Steps**:
1. DEFINE window boundaries (min 3 windows, IS:OOS = 3:1)
2. FOR EACH window:
   a. TRAIN on in-sample (IS) period
   b. TEST on out-of-sample (OOS) period
   c. CLASSIFY regime via regime-classifier
   d. RECORD window metrics and regime
3. AGGREGATE metrics across windows
4. CALCULATE OOS/IS ratio
5. REJECT if OOS/IS < 0.5 (curve_fit indicator)
6. RETURN walk-forward results with regime consistency


---

### capacity_test Mode

Test strategy scalability at multiple capital levels.

**Steps**:
1. VALIDATE hypothesis has passed prior tier gates
2. RUN baseline backtest at baseline_capital
3. FOR EACH scale_factor in [2, 5, 10]:
   a. Scale position sizes proportionally
   b. Apply slippage model (volume_proportional)
   c. Calculate Sharpe with slippage-adjusted returns
   d. Calculate degradation_pct vs baseline
4. CALCULATE capacity_score = (Sharpe_max_scale / Sharpe_baseline) x 100
5. ESTIMATE capacity_ceiling (where degradation = 30%)
6. RETURN verdict based on tier threshold

---

### final_validation Mode

Holdout test before deployment approval.

**Steps**:
1. VERIFY walk_forward passed previously
2. LOAD holdout period (never seen during development)
3. EXECUTE single backtest on holdout
4. APPLY all validation gates
5. RETURN final DEPLOYABLE/NOT_DEPLOYABLE verdict

---

## Aggregation Logic

### Metric Aggregation (aggregate mode)

**Input**: Period results array from tier_test

**Calculations**:

| Metric | Formula |
|--------|---------|
| avg_sharpe | Mean of period Sharpe ratios |
| worst_dd | Most negative drawdown across periods |
| total_trades | Sum of period trade counts |
| avg_win_rate | Mean of period win rates |
| regime_cv | CV of Sharpe by regime type |

### Deflated Sharpe Ratio (DSR)

Applied at Tier 4 only:

```
DSR = SR x sqrt(1 - gamma x T)

Where:
- SR = Raw Sharpe Ratio
- gamma = 0.08 (trial penalty factor)
- T = trials_on_dataset (cumulative trials)
```

**Deflation Table**:

| Trials | Factor | SR=1.0 -> DSR |
|--------|--------|---------------|
| 1 | 0.960 | 0.960 |
| 2 | 0.917 | 0.917 |
| 3 | 0.871 | 0.871 |
| 4 | 0.822 | 0.822 |
| 5 | 0.775 | 0.775 |

---

## Gate Evaluation

### Gate Evaluation Order

Gates are evaluated IN ORDER. First HARD failure determines verdict.

See [gate-thresholds.md](../docs/gate-thresholds.md) for complete threshold definitions.


**Gate Evaluation Logic**:
```
FOR each gate IN validation_gates:
    IF gate.check(metrics) == FAIL:
        IF gate.severity == HARD:
            RETURN NOT_DEPLOYABLE with failure_mode
        ELSE:
            ADD to verdict_reasons
            CONTINUE

IF no HARD failures:
    IF any SOFT failures:
        RETURN NEEDS_REVIEW with reasons
    ELSE:
        RETURN DEPLOYABLE
```

### Failure Mode Classification

| Failure Mode | Trigger | Next Action |
|--------------|---------|-------------|
| `curve_fit` | OOS/IS < 0.5 | failure-analyzer -> likely archive |
| `regime_mismatch` | Regime variance > 50% | Suggest regime filter |
| `insufficient_trades` | Trade count < threshold | failure-analyzer -> expand universe |
| `sharpe_too_low` | Deflated Sharpe < threshold | failure-analyzer -> new hypothesis |
| `drawdown_excessive` | Max DD > threshold | failure-analyzer -> risk adjustment |

---

## Failure Routing

### Delegation to failure-analyzer

When verdict is NOT_DEPLOYABLE:

```
Task(failure-analyzer): {
  "hypothesis_id": "HYP-001",
  "failure_mode": "curve_fit",
  "metrics": { ... },
  "validation_gates": { ... },
  "request": "Analyze failure and generate NEW hypothesis or ARCHIVE"
}
```


### Expected Response from failure-analyzer

| Recommendation | Action |
|----------------|--------|
| NEW_HYPOTHESIS | Generate new hypothesis for strategy-builder |
| ARCHIVE | Move to hypothesis graveyard with lessons |
| ADJUST_UNIVERSE | Suggest universe expansion/contraction |
| REGIME_FILTER | Suggest regime-specific entry conditions |

---

## Verdict and next_action Routing

### Verdict Outcomes

| Verdict | Meaning | Next Action |
|---------|---------|-------------|
| DEPLOYABLE | Passed all gates | Suggest walk_forward or final_validation |
| NOT_DEPLOYABLE | Failed HARD gate | Route to failure-analyzer |
| NEEDS_REVIEW | Failed SOFT gate(s) | Present warnings, request decision |

### next_action Routing Table

| Current Mode | Verdict | next_action |
|--------------|---------|-------------|
| single_run | DEPLOYABLE | tier_test (if Tier 1-3) or walk_forward (Tier 4) |
| tier_test | DEPLOYABLE | Next tier or walk_forward |
| regime_test | DEPLOYABLE | walk_forward |
| walk_forward | DEPLOYABLE | final_validation |
| final_validation | DEPLOYABLE | READY_FOR_DEPLOYMENT |
| Any | NOT_DEPLOYABLE | failure-analyzer |

---

## Exit Criteria

**All criteria must pass to return SUCCESS**:

| Criterion | Check |
|-----------|-------|
| Execution completed | All mode steps finished |
| Metrics calculated | Required metrics populated |
| Gates evaluated | All gates checked in order |
| Verdict assigned | DEPLOYABLE/NOT_DEPLOYABLE/NEEDS_REVIEW |
| next_action set | Clear routing for next step |
| Failure routed | failure-analyzer invoked if NOT_DEPLOYABLE |


---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Skipping deflation | ALWAYS apply DSR at Tier 4 |
| Wrong gate order | Evaluate gates in defined order |
| Missing failure routing | ALWAYS route NOT_DEPLOYABLE to failure-analyzer |
| Reporting raw Sharpe | Report both raw and deflated |
| Ignoring SOFT failures | Include in verdict_reasons |

---

## Output Reference

See [output-examples.md](../examples/output-examples.md) for complete output schemas:
- Backtest Result Schema
- tier_test Output
- walk_forward Output
- Failure Output

---

**Previous Phase**: [Phase 3: DECIDE](phase-3-decide.md)
**Complete**: Return to [backtester.md](../backtester.md)


---

## Advanced Analytics

### Regime Stratification

> **P8 Risk Management Integration**: Accept regime configuration and stratify all backtest results by regime factors.

**Regime Configuration Input**:
When `regime_config.enabled = true`, accept regime configuration from P8 (Risk Management phase):

| Field | Type | Description |
|-------|------|-------------|
| `regime_config.enabled` | boolean | Enable regime stratification |
| `regime_config.factors` | array | Factors to stratify by (volatility, trend, correlation, credit, sentiment) |
| `regime_config.stratify_results` | boolean | Whether to break down results by regime |
| `regime_classification` | object | Current regime state per factor |

**Trade-Level Regime Classification**:
```
FOR each trade IN backtest_results:
    1. LOOKUP regime_state at trade.entry_date
    2. TAG trade with regime factors
    3. STORE tagged trade for stratification
```

**Regime Consistency Score**:
```
regime_consistency_score = 100 x (1 - normalized_variance)

Thresholds:
- >= 75: CONSISTENT (pass)
- 50-74: VARIABLE (warn)
- < 50: UNSTABLE (fail regime_consistency gate)
```

---


### CDAP Metrics

> **Source**: Samir Varma's CDAP framework for drawdown-coherent risk adjustment.

**CDAP Ratio Calculation**:
```
CDAP_Ratio = CAGR / (Max_Drawdown x Recovery_Time_Factor)

Where:
- Recovery_Time_Factor = sqrt(avg_recovery_days / 252)

Interpretation:
- > 1.5: Excellent drawdown-adjusted performance
- 1.0-1.5: Good performance
- 0.5-1.0: Acceptable
- < 0.5: Poor drawdown characteristics
```

**Drawdown-Adjusted Sharpe**:
```
DD_Adjusted_Sharpe = Sharpe_Ratio x (1 - Drawdown_Penalty)
Drawdown_Penalty = min(0.5, Max_Drawdown / 0.25)
```

**Regime-Weighted Sharpe**:
```
Regime_Weighted_Sharpe = Sum(regime_weight[r] x sharpe[r]) for r in regimes

Default Regime Weights:
- LOW_RISK: 0.30
- NORMAL: 0.40
- ELEVATED: 0.20
- HIGH_RISK: 0.10
```

**Recovery Factor**:
```
Recovery_Factor = Net_Profit / Max_Drawdown

- > 3.0: Excellent
- 2.0-3.0: Good
- 1.0-2.0: Acceptable
- < 1.0: Poor
```

---


### 200DMA Stratification

> **Insight**: Price position relative to 200-day moving average is a powerful regime filter.

**DMA Classification Logic**:
```
FOR each trading day IN backtest_period:
    price = close_price[day]
    dma_200 = SMA(close_price, 200)[day]
    
    IF price > dma_200:
        regime = "above_200dma"
    ELSE:
        regime = "below_200dma"
    
    TAG all trades entered on this day with dma_regime
```

**DMA Efficiency Ratio**:
```
DMA_Efficiency_Ratio = (return_above / time_above) / (return_below / time_below)

- Ratio > 1.0: Strategy more efficient above 200DMA
- Ratio > 1.5: Consider DMA filter (reduce exposure below)
```

**Asymmetry Score**:
```
Asymmetry_Score = (return_pct_above - risk_pct_above) / 100

- > 0.20: Strong positive asymmetry
- 0.00-0.20: Mild positive asymmetry
- < 0.00: Negative asymmetry (WARNING)
```

**DMA-Based Recommendations**:

| DMA Profile | Recommendation |
|-------------|----------------|
| Efficiency > 2.0, Asymmetry > 0.30 | Consider DMA filter |
| Efficiency > 1.5, Asymmetry > 0.15 | DMA filter optional |
| Efficiency 1.0-1.5, Asymmetry 0-0.15 | DMA filter marginal benefit |
| Efficiency < 1.0, Asymmetry < 0 | Do NOT add DMA filter |
