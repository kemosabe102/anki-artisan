---
name: backtest-rca
description: >
  Deep root cause analysis of backtest results using multiple thinking frameworks.
  Explains WHY results occurred and generates actionable recommendations.
  Trigger keywords: analyze backtest, why did strategy fail, backtest RCA,
  root cause analysis, explain results, deep analysis, why did it work.
---

# Backtest Root Cause Analysis Skill

*Deep causal analysis of backtest outcomes using structured thinking frameworks*

## Quick Reference

| Aspect | Value |
|--------|-------|
| **Purpose** | Explain WHY backtest results occurred (successes AND failures) |
| **Input** | Backtest metrics, failure-analyzer classification (optional), regime context |
| **Output** | Root cause chain, SCAMPER recommendations, statistical evidence, confidence |
| **Invoked By** | `backtester` agent (deep analysis mode), orchestrator (post-mortem) |
| **Outputs To** | `hypothesis-tracking` (audit trail), strategy-builder (recommendations) |

---

## Integration with HDD Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│                        HDD Backtest Pipeline                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  backtester ─────► failure-analyzer ─────► backtest-rca            │
│  (executes)        (classifies)            (explains WHY)           │
│                          │                       │                  │
│                          │                       ▼                  │
│                          │              SCAMPER recommendations     │
│                          │                       │                  │
│                          ▼                       ▼                  │
│                   hypothesis-tracking ◄──────────┘                  │
│                   (audit trail)                                     │
│                          │                                          │
│                          ▼                                          │
│                   strategy-builder                                  │
│                   (implements fixes)                                │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Relationship with failure-analyzer

| Skill | Purpose | When Invoked |
|-------|---------|--------------|
| `failure-analyzer` | Quick classification (BAD_LUCK/BAD_PROCESS/UNDETERMINED) | After every failed backtest |
| `backtest-rca` | Deep causal analysis with multiple frameworks | On request, for deep analysis mode, or post-mortems |

**backtest-rca USES failure-analyzer output as input** - it does not replace it.

---

## Framework Application Sequence

Apply frameworks IN ORDER. Each builds on prior analysis.

```
1. ReACT Loop (gather context)
   │
   ▼
2. 5 Whys (drill to root cause)
   │
   ▼
3. Luck vs Process (statistical significance)
   │
   ▼
4. SCAMPER (generate recommendations)
   │
   ▼
5. Synthesize Output
```



---

## Framework 1: ReACT Loop

*Reason -> Act -> Observe -> Refine until confidence >= 0.85*

### Protocol

| Step | Action | Output |
|------|--------|--------|
| **Reason** | Form hypothesis about result driver | "Sharpe degraded due to regime mismatch" |
| **Act** | Gather supporting evidence | Query regime breakdown, parameter sensitivity |
| **Observe** | Analyze evidence patterns | "62% of losses occurred in HIGH_RISK regime" |
| **Refine** | Update hypothesis or conclude | Confidence score + refined hypothesis |

### Iteration Limits

| Condition | Action |
|-----------|--------|
| Confidence >= 0.85 | Proceed to 5 Whys |
| Confidence < 0.85 after 3 iterations | Flag UNDETERMINED, proceed with caveats |
| Missing data | Document gaps, request from backtester |

### Evidence Categories

| Category | Sources | Weight |
|----------|---------|--------|
| Performance Metrics | Sharpe, drawdown, win rate, profit factor | 0.30 |
| Regime Breakdown | Performance by volatility/trend/correlation | 0.25 |
| Trade Distribution | Entry/exit timing, holding periods, clustering | 0.20 |
| Parameter Sensitivity | How small changes affect outcomes | 0.15 |
| Market Structure | Liquidity, spreads, correlation shifts | 0.10 |



---

## Framework 2: 5 Whys (Trading-Specific)

*Drill past symptoms to actionable root cause*

### Trading-Specific Why Categories

| Category | Example Questions |
|----------|-------------------|
| **Regime** | Why did strategy perform differently across volatility regimes? |
| **Parameters** | Why were these parameter values chosen? Why do they fail now? |
| **Market Structure** | Why did liquidity/spreads/correlations change? |
| **Data Quality** | Why did the signal behave unexpectedly? Data issues? |
| **Hypothesis Validity** | Why did we believe this cause-effect relationship existed? |

### 5 Whys Protocol

```
WHY #1: Why did the backtest [succeed/fail]?
→ Evidence-based answer (from ReACT)

WHY #2: Why did [answer to #1] occur?
→ Drill into mechanism

WHY #3: Why did [answer to #2] occur?
→ Examine assumptions

WHY #4: Why did [answer to #3] occur?
→ Check historical context

WHY #5: Why did [answer to #4] occur?
→ Reach actionable root cause

STOP when: Further "why" leads to external/market factors beyond control
```



### Example: Failed Momentum Strategy

```
Problem: Momentum strategy Sharpe dropped from 1.2 (IS) to 0.3 (OOS)

WHY #1: Why did Sharpe degrade in OOS period?
→ Win rate dropped from 58% to 41%

WHY #2: Why did win rate drop?
→ Strategy entered trades during HIGH_RISK regime that didn't exist in IS

WHY #3: Why was there no HIGH_RISK regime in IS?
→ IS period (2019-2021) was predominantly LOW_RISK/NORMAL; OOS (2022) included rate hike volatility

WHY #4: Why didn't we test across multiple regime types?
→ Single historical period used; no synthetic regime stress testing

WHY #5: Why was regime-aware testing not part of protocol?
→ Initial hypothesis didn't consider regime as a confounding variable

ROOT CAUSE: Missing regime filter in hypothesis formulation
ACTIONABLE FIX: Add regime classification to entry conditions; reformulate hypothesis with regime awareness
```

---

## Framework 3: Luck vs Process (Statistical Significance)

*Distinguish random variance from systematic issues*

### Monte Carlo Significance Testing

| Test | Purpose | Threshold |
|------|---------|-----------|
| Monte Carlo Simulation | Is performance distinguishable from random? | p-value < 0.05 |
| Sigma from Regime Mean | How far from expected performance? | abs(sigma) < 2 |
| Bootstrap Confidence | Stability of Sharpe estimate | 95% CI width < 0.5 |



### Classification Matrix

| Evidence | Sigma from Mean | Monte Carlo p-value | Classification |
|----------|-----------------|---------------------|----------------|
| Within expectations | < 1 | > 0.10 | **GOOD_LUCK** (if success) or **BAD_LUCK** (if failure) |
| Slightly anomalous | 1-2 | 0.05-0.10 | **UNDETERMINED** - flag for review |
| Significantly anomalous | > 2 | < 0.05 | **GOOD_PROCESS** (if success) or **BAD_PROCESS** (if failure) |

### Calculation Protocol

```python
# Sigma from regime mean
sigma = (observed_sharpe - regime_mean_sharpe) / regime_std_sharpe

# Monte Carlo simulation
def monte_carlo_test(trade_returns, n_simulations=1000):
    observed_sharpe = calculate_sharpe(trade_returns)
    random_sharpes = []
    for _ in range(n_simulations):
        shuffled = np.random.permutation(trade_returns)
        random_sharpes.append(calculate_sharpe(shuffled))
    p_value = np.mean(random_sharpes >= observed_sharpe)  # for success
    return p_value

# Bootstrap confidence interval
def bootstrap_sharpe_ci(trade_returns, n_bootstrap=1000):
    sharpes = []
    for _ in range(n_bootstrap):
        sample = np.random.choice(trade_returns, size=len(trade_returns), replace=True)
        sharpes.append(calculate_sharpe(sample))
    return np.percentile(sharpes, [2.5, 97.5])
```



### Interpretation Guidelines

| Classification | Confidence Required | Recommended Action |
|----------------|--------------------|--------------------|
| **GOOD_PROCESS** | >= 0.85 | Document success factors, consider scaling |
| **GOOD_LUCK** | >= 0.70 | Caution - success may not repeat; extend test period |
| **BAD_LUCK** | >= 0.70 | May retry (uses trial budget); document and proceed |
| **BAD_PROCESS** | >= 0.85 | Do NOT retry - fix process first via SCAMPER |
| **UNDETERMINED** | < 0.70 | Flag for human review with all evidence |

---

## Framework 4: SCAMPER (Trading-Specific Recommendations)

*Generate actionable improvement candidates*

### Trading-Adapted SCAMPER

| Letter | Technique | Trading Application | Example |
|--------|-----------|---------------------|---------|
| **S** | Substitute | Replace indicator/signal | Substitute RSI(14) with RSI(21) for less noise |
| **C** | Combine | Merge signals for confirmation | Combine momentum with volume confirmation |
| **A** | Adapt | Borrow from other strategies | Adapt mean-reversion exit to trending strategy |
| **M** | Modify | Adjust thresholds/parameters | Modify stop-loss from 2% to ATR-based |
| **P** | Put to use | Apply to different markets | Put momentum strategy to sector ETFs instead of individual stocks |
| **E** | Eliminate | Remove complexity | Eliminate redundant filters that add curve-fit risk |
| **R** | Reverse | Invert logic | Reverse entry/exit (exit on entry signal, enter on exit signal) |



### Impact/Effort Scoring

Each SCAMPER recommendation receives:

| Dimension | Scale | Description |
|-----------|-------|-------------|
| **Impact** | 1-5 | Expected improvement in target metric (Sharpe, drawdown, etc.) |
| **Effort** | 1-5 | Implementation complexity (1=trivial, 5=major refactor) |
| **Risk** | 1-5 | Probability of unintended consequences |
| **Priority Score** | Calculated | (Impact × 2) - Effort - Risk |

### SCAMPER Recommendation Template

```json
{
  "technique": "Substitute",
  "recommendation": "Replace fixed stop-loss with ATR-based dynamic stop",
  "rationale": "5 Whys revealed losses concentrated during high-volatility periods where fixed 2% stop was too tight",
  "impact": 4,
  "effort": 2,
  "risk": 2,
  "priority_score": 4,
  "implementation_notes": "Use 2x ATR(14) as stop distance; requires ATR indicator addition",
  "addresses_root_cause": true,
  "root_cause_link": "WHY #3: Stop-loss not adaptive to volatility regime"
}
```

---

## Output Schema

### Complete RCA Output Structure

```json
{
  "rca_id": "RCA-2025-001",
  "hypothesis_id": "HYP-001",
  "analysis_timestamp": "2025-01-15T14:30:00Z",
  "backtest_outcome": "FAILURE|SUCCESS",
  "confidence": 0.87,
  

  "react_analysis": {
    "iterations": 2,
    "final_hypothesis": "Strategy fails in HIGH_RISK regime due to tight stop-loss",
    "evidence_summary": [
      "62% of losses occurred in HIGH_RISK regime",
      "Average stop-out distance: 1.8% vs 2.0% threshold",
      "Regime-stratified Sharpe: LOW_RISK=1.4, NORMAL=0.9, HIGH_RISK=-0.3"
    ],
    "confidence": 0.87
  },
  
  "five_whys": {
    "chain": [
      {
        "level": 1,
        "question": "Why did the backtest fail?",
        "answer": "Sharpe degraded from 1.2 (IS) to 0.3 (OOS)",
        "evidence": "OOS period metrics"
      },
      {
        "level": 2,
        "question": "Why did Sharpe degrade?",
        "answer": "Win rate dropped from 58% to 41%",
        "evidence": "Trade-level analysis"
      },
      {
        "level": 3,
        "question": "Why did win rate drop?",
        "answer": "Stop-losses triggered prematurely in volatile periods",
        "evidence": "62% of losses in HIGH_RISK regime"
      },
      {
        "level": 4,
        "question": "Why were stop-losses premature?",
        "answer": "Fixed 2% stop too tight for HIGH_RISK regime volatility",
        "evidence": "ATR analysis shows 3.5% average daily range in HIGH_RISK vs 1.2% in NORMAL"
      },
      {
        "level": 5,
        "question": "Why was stop-loss not regime-adaptive?",
        "answer": "Original hypothesis did not consider regime as a variable",
        "evidence": "Hypothesis documentation review"
      }
    ],
    "root_cause": "Fixed stop-loss not adapted to volatility regime",
    "actionable_fix": "Implement ATR-based dynamic stop-loss"
  },
  

  "luck_vs_process": {
    "classification": "BAD_PROCESS",
    "confidence": 0.90,
    "evidence": {
      "sigma_from_mean": -2.3,
      "monte_carlo_pvalue": 0.02,
      "bootstrap_ci": [0.15, 0.45],
      "regime_breakdown": {
        "LOW_RISK": {"sharpe": 1.4, "trades": 45},
        "NORMAL": {"sharpe": 0.9, "trades": 120},
        "HIGH_RISK": {"sharpe": -0.3, "trades": 35}
      }
    },
    "interpretation": "Performance 2.3 sigma below regime mean with p=0.02 indicates systematic issue, not random variance"
  },
  
  "scamper_recommendations": [
    {
      "rank": 1,
      "technique": "Modify",
      "recommendation": "Replace fixed 2% stop with 2x ATR(14) dynamic stop",
      "impact": 4,
      "effort": 2,
      "risk": 2,
      "priority_score": 4,
      "addresses_root_cause": true
    },
    {
      "rank": 2,
      "technique": "Adapt",
      "recommendation": "Add regime filter - reduce position size 50% in HIGH_RISK",
      "impact": 3,
      "effort": 2,
      "risk": 1,
      "priority_score": 3,
      "addresses_root_cause": true
    },
    {
      "rank": 3,
      "technique": "Eliminate",
      "recommendation": "Remove trades entirely during HIGH_RISK regime",
      "impact": 3,
      "effort": 1,
      "risk": 3,
      "priority_score": 2,
      "addresses_root_cause": true
    }
  ],
  

  "next_steps": [
    {
      "action": "REVISE_HYPOTHESIS",
      "description": "Formulate new hypothesis with ATR-based stop-loss",
      "route_to": "hypothesis-formulation",
      "priority": "HIGH"
    },
    {
      "action": "UPDATE_AUDIT_TRAIL",
      "description": "Record RCA in hypothesis tracking",
      "route_to": "hypothesis-tracking",
      "priority": "REQUIRED"
    }
  ]
}
```

---

## Anti-Patterns

| Anti-Pattern | Why Wrong | Correct Approach |
|--------------|-----------|------------------|
| Skip ReACT, jump to 5 Whys | Missing evidence leads to speculation | Always gather evidence first |
| Accept first "why" answer | Symptom treated as cause | Drill 5 levels minimum |
| Ignore statistical tests | Confuse luck with skill | Always run Monte Carlo |
| Generate SCAMPER without root cause | Recommendations don't address problem | Link each recommendation to root cause |
| Single SCAMPER recommendation | Miss alternative solutions | Generate minimum 3 options |
| Skip audit trail update | Lose institutional memory | Always route to hypothesis-tracking |
| Analyze only failures | Miss success factors | Analyze both successes and failures |

---



## Invocation Patterns

### From backtester Agent (Deep Analysis Mode)

```markdown
Task(backtest-rca): {
  "hypothesis_id": "HYP-001",
  "backtest_metrics": { ... },
  "failure_classification": "BAD_PROCESS",  // from failure-analyzer
  "regime_context": { ... },
  "request": "Deep RCA with SCAMPER recommendations"
}
```

### From Orchestrator (Post-Mortem)

```markdown
Task(backtest-rca): {
  "hypothesis_id": "HYP-001",
  "request": "Full post-mortem analysis of hypothesis journey",
  "include_all_trials": true
}
```

### For Successful Backtest

```markdown
Task(backtest-rca): {
  "hypothesis_id": "HYP-002",
  "backtest_metrics": { ... },
  "backtest_outcome": "SUCCESS",
  "request": "Analyze success factors - is this skill or luck?"
}
```

---

## Knowledge Base

| Document | Purpose |
|----------|---------|
| `.claude/skills/failure-analyzer/SKILL.md` | Failure classification (input to RCA) |
| `.claude/skills/hypothesis-tracking/SKILL.md` | Audit trail management |
| `.claude/skills/hypothesis-formulation/SKILL.md` | New hypothesis requirements |
| `.claude/skills/debugging-methodology/reference/five-whys-rca.md` | General 5 Whys framework |
| `.claude/skills/debugging-methodology/reference/scamper-solutions.md` | General SCAMPER framework |
| `.claude/agents/investing/backtester/backtester.md` | Backtester agent (invokes this skill) |



---

## Error Recovery

| Scenario | Action |
|----------|--------|
| Missing backtest metrics | Request from backtester, HALT until received |
| No failure-analyzer classification | Run classification inline, proceed |
| Insufficient trade count for Monte Carlo | WARN, use bootstrap only, note in output |
| Cannot reach 0.85 confidence | Output with UNDETERMINED, list gaps |
| 5 Whys leads to external factors | Stop at last actionable level, document |

---

## Quality Standards

- All RCA outputs MUST include confidence score (0.0-1.0)
- 5 Whys chain MUST have evidence for each level
- SCAMPER recommendations MUST link to root cause
- Monte Carlo MUST use minimum 1000 simulations
- Audit trail update is MANDATORY (route to hypothesis-tracking)
- Minimum 3 SCAMPER recommendations required

---

## See Also

- **Failure Analyzer**: Quick classification before deep RCA
- **Hypothesis Tracking**: Trial limits, graveyard, audit trail
- **Hypothesis Formulation**: Cause-Effect-Why framework for new hypotheses
- **Debugging Methodology**: General debugging frameworks (non-trading)
- **Backtester**: Executes backtests, invokes RCA for deep analysis

