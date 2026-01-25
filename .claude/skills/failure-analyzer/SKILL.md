---
name: failure-analyzer
description: >
  Analyzes backtest failures within hypothesis-driven strategy research to 
  classify failure mode (curve_fit, regime_mismatch, insufficient_trades, 
  implementation_bug, no_edge) and determine next action. Routes to hypothesis 
  graveyard (REJECT) or requires new hypothesis formulation (REVISE).
  
  Use for: "analyze backtest failure", "classify failure mode", "curve fit or 
  regime mismatch?", "should we archive this hypothesis?"
  Trigger keywords: failure analysis, backtest failed, why did it fail.
  
  NOT for: Unit test execution failures (test-executor), code debugging and 
  bug fixing (debugger), generic root cause analysis or incident post-mortems 
  (root-cause-identifier), non-backtest contexts.
---

# Failure Analyzer Skill

*Decision tree for analyzing backtest failures and routing to appropriate actions*

## Quick Reference

| Aspect | Value |
|--------|-------|
| Purpose | Classify backtest failure mode, determine next action |
| Outputs | `REJECT` (graveyard) or `REVISE` (new hypothesis required) |
| Related Skills | hypothesis-tracking, hypothesis-formulation |
| Deep Analysis | For framework-based WHY analysis, invoke `backtest-rca` after classification |

---

## Companion Skill: backtest-rca

**failure-analyzer provides CLASSIFICATION. backtest-rca provides EXPLANATION.**

| Skill | Purpose | Output |
|-------|---------|--------|
| `failure-analyzer` | Quick classification of failure mode | BAD_LUCK/BAD_PROCESS/UNDETERMINED + REJECT/REVISE |
| `backtest-rca` | Deep causal analysis using frameworks | Root cause chain, SCAMPER recommendations, evidence |

### When to Use Each

```
Backtest Failed
    │
    ▼
failure-analyzer (ALWAYS first)
    │ → Classification: curve_fit, regime_mismatch, etc.
    │ → Decision: REJECT or REVISE
    │
    ├─── Quick Mode: Stop here, return decision
    │
    └─── Deep Analysis Mode: Continue to backtest-rca
         │
         ▼
    backtest-rca
         │ → 5 Whys root cause drilling
         │ → SCAMPER improvement recommendations  
         │ → Statistical luck vs process evidence
         │
         ▼
    Structured analysis with actionable next steps
```

### Invoking Deep Analysis

After failure-analyzer completes, invoke backtest-rca for deeper understanding:
```
Skill(backtest-rca, "Analyze {hypothesis_id} with classification: {failure_mode}")
```

---

## Decision Tree

```
Backtest Failed
|
+-- Check: Implementation Bug?
|   +-- Yes --> Fix bug, retest (does NOT count as new trial)
|   +-- No  |
|           v
+-- Check: Regime Mismatch?
|   +-- Yes --> Add regime filter, NEW hypothesis required
|   +-- No  |
|           v
+-- Check: Insufficient Trades?
|   +-- Yes --> Extend timeframe, NEW hypothesis required
|   +-- No  |
|           v
+-- Check: Logic Issue?
    +-- Signal too frequent --> Tighten criteria, NEW hypothesis
    +-- Signal too rare     --> Loosen criteria, NEW hypothesis
    +-- No edge detected    --> ARCHIVE to graveyard
    |
    v
Output: REJECT (graveyard) | REVISE (new hypothesis required)
```

---

## Failure Mode Classification

| Mode | Indicators | Root Cause | Next Action |
|------|-----------|-----------|-------------|
| `curve_fit` | OOS Sharpe << IS Sharpe | Overfit to backtest | ARCHIVE |
| `regime_mismatch` | Works in one regime only | Missing market state filter | NEW hypothesis with regime |
| `insufficient_trades` | < 100 trades | Short timeframe or rare signal | NEW hypothesis with extended period |
| `implementation_bug` | Code error, data error | Technical issue | Fix, does NOT count as trial |
| `no_edge` | Random performance | Hypothesis invalid | ARCHIVE |

### Failure Mode Detection Criteria

| Mode | Primary Indicator | Secondary Indicators |
|------|-------------------|---------------------|
| `curve_fit` | OOS Sharpe / IS Sharpe < 0.5 | High parameter sensitivity, narrow profit window |
| `regime_mismatch` | Sharpe varies >1.0 across regimes | Positive only in HIGH or LOW volatility |
| `insufficient_trades` | trade_count < 100 | Wide confidence intervals, unstable metrics |
| `implementation_bug` | Exceptions, NaN values, data gaps | Results don't match expected behavior |
| `no_edge` | Sharpe < 0.5 deflated | Performance indistinguishable from random |

---

## Luck vs Process Classification

When a trial fails, distinguish between random variance (bad luck) and systematic issues (bad process).

### BAD_LUCK (confidence >= 0.7)

**Indicators**:
- Performance within 1 sigma of regime historical mean
- Monte Carlo simulation p-value > 0.05
- No parameter anomalies detected
- Single-variable change between trials

**Evidence to collect**:
- `sigma_from_mean`: How many standard deviations from regime mean
- `monte_carlo_pvalue`: Bootstrap simulation result
- `parameter_validation`: All parameters within historical ranges

**Action**: May retry (counts against 5-trial budget). Document and proceed.

### BAD_PROCESS (confidence >= 0.7)

**Indicators**:
- Performance > 2 sigma below regime mean
- Monte Carlo p-value < 0.01
- Parameter values outside historical ranges
- Multiple parameters changed between trials
- Logic errors detected in strategy

**Evidence to collect**:
- `sigma_from_mean`: Deviation from expected performance
- `monte_carlo_pvalue`: Statistical significance of poor performance
- `parameter_anomalies`: List of out-of-range parameters
- `process_violations`: List of HDD rule violations

**Action**: Route to hypothesis reformulation. Do NOT retry - fix the process first.

### UNDETERMINED (confidence < 0.7)

**Indicators**:
- Mixed signals from statistical tests
- p-value between 0.01 and 0.05
- Performance between 1-2 sigma from mean

**Action**: Flag for human review. Present evidence and request decision.

---

### Classification Algorithm

```
FUNCTION classify_failure(trial_result, regime_stats):
    sigma = (trial_result.sharpe - regime_stats.mean) / regime_stats.std
    pvalue = monte_carlo_test(trial_result, n_simulations=1000)
    
    IF sigma > -1 AND pvalue > 0.05:
        RETURN BAD_LUCK, confidence=0.85
    ELIF sigma < -2 AND pvalue < 0.01:
        RETURN BAD_PROCESS, confidence=0.90
    ELSE:
        RETURN UNDETERMINED, confidence=0.50
```

---

### Output Schema

```json
{
  "failure_classification": {
    "type": "BAD_LUCK|BAD_PROCESS|UNDETERMINED",
    "confidence": 0.85,
    "evidence": [
      "Monte Carlo p-value: 0.12",
      "Within 1 sigma of HIGH_RISK mean",
      "Single parameter change verified"
    ],
    "monte_carlo_pvalue": 0.12,
    "sigma_from_mean": -0.8,
    "recommended_action": "Document and proceed to next trial"
  }
}
```

---

### Integration with hypothesis-tracking

After classification, update the trial audit manifest:
```
Skill(hypothesis-tracking, "Update trial {n} with classification: {type}, confidence: {conf}")
```

This ensures the audit trail captures the luck vs process distinction for post-mortem analysis.

---

## Analysis Protocol

### Step-by-Step Process

1. **Record raw backtest metrics**
   - Sharpe ratio (raw and deflated)
   - Total trades
   - Max drawdown
   - Win rate
   - Profit factor

2. **Compare IS vs OOS Sharpe** (if available)
   - IS (In-Sample): Training period
   - OOS (Out-of-Sample): Validation period
   - Ratio < 0.5 = likely curve fit

3. **Check trade count** (< 100 = insufficient)
   - Minimum 100 trades for statistical significance
   - Prefer 200+ for confidence
   - Fewer trades = wider confidence intervals

4. **Classify by regime performance**
   - LOW volatility (VIX < 15)
   - NORMAL volatility (VIX 15-25)
   - HIGH volatility (VIX > 25)
   - Flag if performance varies significantly across regimes

5. **Assign failure mode**
   - Use classification table above
   - Single mode assignment (pick primary cause)

6. **Generate action recommendation**
   - ARCHIVE: Move to graveyard, hypothesis exhausted
   - REVISE: New hypothesis required with specific changes

---

## NEW Hypothesis Requirements

When analysis outputs `REVISE`, the new hypothesis MUST:

| Requirement | Description |
|-------------|-------------|
| Change CAUSE or WHY | Parameter tweaks alone are insufficient |
| Reference previous | Include `previous_hypothesis_id` field |
| Include failure metrics | Document what failed and why |
| Address failure mode | New hypothesis must specifically address identified issue |

### Valid Revisions by Failure Mode

| Failure Mode | Valid Revision Examples |
|--------------|------------------------|
| `regime_mismatch` | Add VIX filter, market state detection, sector rotation |
| `insufficient_trades` | Extend backtest period, add correlated instruments, lower threshold |
| `curve_fit` | Simplify model, reduce parameters, use walk-forward validation |

### Invalid Revisions (Will Be Rejected)

| Invalid Change | Why It Fails |
|----------------|--------------|
| Same cause, different parameters | Does not address root cause |
| Add complexity to overfit model | Makes curve fitting worse |
| Ignore failure mode classification | Repeats same mistake |

---

## Anti-Patterns

| Anti-Pattern | Why Wrong | Correct Approach |
|--------------|-----------|------------------|
| Parameter tweak after failure | Not addressing root cause | Change cause or mechanism |
| Ignore failure mode | Repeat same mistake | Classify and address |
| Skip to new hypothesis | No learning captured | Analyze first |
| Retry without changes | Definition of insanity | Must change something |
| Multiple changes at once | Confounds causality | Single change per revision |
| Blame data quality | Often excuse | Verify with alternative data |

---

## Implementation Bug Handling

Implementation bugs are special: they do NOT count as hypothesis trials.

### Identification Criteria

| Indicator | Example |
|-----------|---------|
| Code exceptions | IndexError, KeyError, ZeroDivisionError |
| Data anomalies | NaN values, missing bars, duplicate timestamps |
| Logic errors | Wrong comparison operator, off-by-one errors |
| API misuse | Incorrect method calls, wrong parameter types |

### Bug Fix Protocol

1. Identify and document the bug
2. Fix the implementation
3. Re-run backtest with SAME parameters
4. This does NOT increment trial_number
5. Document bug in hypothesis notes for future reference

---

## Workflow Integration

```
Backtest Complete (FAILED)
         |
         v
1. Invoke failure-analyzer skill
         |
         v
2. Collect metrics: Sharpe, trades, drawdown, regime breakdown
         |
         v
3. Walk decision tree (bug? regime? trades? logic?)
         |
         v
4. Classify failure mode
         |
         v
5. Output: REJECT or REVISE
         |
    +----+----+
    |         |
    v         v
REJECT    REVISE
    |         |
    v         v
Archive   Require NEW hypothesis
to        with failure mode
graveyard addressed
```

---

## Output Schema

### Analysis Result Structure

```json
{
  "hypothesis_id": "H001",
  "analysis_timestamp": "2025-01-15T14:30:00Z",
  "failure_mode": "curve_fit | regime_mismatch | insufficient_trades | implementation_bug | no_edge",
  "decision": "REJECT | REVISE",
  "metrics": {
    "sharpe_raw": 0.8,
    "sharpe_deflated": 0.2,
    "sharpe_oos": 0.1,
    "trade_count": 45,
    "max_drawdown": -18.5,
    "regime_breakdown": {
      "low_vol": 1.2,
      "normal_vol": 0.3,
      "high_vol": -0.5
    }
  },
  "reasoning": "OOS Sharpe (0.1) << IS Sharpe (0.8) indicates curve fitting",
  "next_action": {
    "type": "ARCHIVE | NEW_HYPOTHESIS",
    "requirements": ["Must change cause or mechanism", "Address regime sensitivity"]
  }
}
```

---

## Knowledge Base

| Document | Purpose |
|----------|---------|
| `.claude/skills/hypothesis-tracking/SKILL.md` | Hypothesis lifecycle, graveyard structure, trial counting |
| `.claude/skills/hypothesis-tracking/schemas/trial-audit.schema.json` | Trial audit schema for failure records |
| `.claude/skills/regime-classifier/SKILL.md` | Regime context for failure analysis |
| `.claude/skills/hypothesis-formulation/SKILL.md` | Cause-Effect-Why framework, formulation requirements |
| `.claude/agents/investing/strategy-builder/schemas/` | Schema definitions for hypothesis and backtest results |
| `.claude/skills/backtest-rca/SKILL.md` | Deep framework-based analysis (ReACT, 5 Whys, SCAMPER) |

---

## See Also

- **Hypothesis Tracking**: Trial limits, graveyard management
- **Strategy Specification**: 7-element framework for strategy definition
- **Backtest Validation**: Statistical gates and significance testing
