# Hypothesis-Driven Development for Trading Strategies

**Version**: 1.0.0 | **Last Updated**: 2025-12-31

---

## What is HDD?

Hypothesis-Driven Development (HDD) applies the scientific method to trading strategy development. Instead of curve-fitting parameters to historical data, HDD requires you to:

1. **Form a testable hypothesis** with economic rationale
2. **Lock parameters** before running any backtest
3. **Analyze results** against pre-defined success criteria
4. **Revise or archive** based on evidence, not hope

The goal is **discovery of robust market mechanisms**, not optimization of historical performance.

---

## The Core Loop

```
HYPOTHESIS --> TEST --> ANALYZE --> REVISE or ARCHIVE
     ^                                      |
     |______________________________________|
```

| Phase | Duration | Output |
|-------|----------|--------|
| HYPOTHESIS | 1-2 hours | Documented prediction with rationale |
| TEST | Automated | Backtest results on locked parameters |
| ANALYZE | 30-60 min | Pass/fail against success criteria |
| REVISE/ARCHIVE | 15-30 min | Next hypothesis OR graveyard entry |


---

## Hypothesis Formulation

**Template**: "I believe [CAUSE] leads to [EFFECT] WHEN [REGIME_CONDITION] because [WHY]"

### Good Hypotheses

| Hypothesis | Why It's Good |
|------------|---------------|
| "I believe momentum in large-cap tech leads to 3-day continuation because institutional rebalancing takes multiple days to complete" | Specific cause, measurable effect, economic rationale |
| "I believe VIX mean-reversion above 25 leads to SPY rallies because fear overshoots during panic selling" | Identifies regime, clear mechanism, testable threshold |

### Bad Hypotheses

| Hypothesis | Why It's Bad |
|------------|--------------|
| "Moving averages work for trend following" | No cause, no effect size, no rationale |
| "I think RSI oversold signals good entries" | Vague, no timeframe, no economic theory |
| "This parameter set has good backtest results" | Outcome-based, not theory-based |

---

## Parameter Discipline

### Lock Before Test

**CRITICAL**: All parameters must be documented BEFORE running any backtest.

```yaml
# parameters.yaml - LOCKED before test
entry_threshold: 0.02
exit_threshold: -0.01
lookback_period: 20
position_size: 0.1
stop_loss: 0.03
```

### Single Parameter Change Per Trial

When revising, change **exactly ONE parameter** per trial:
- Trial 1: Base hypothesis (original parameters)
- Trial 2: Adjust entry_threshold only
- Trial 3: Adjust lookback_period only


**NEVER**: Run optimization sweeps, grid searches, or auto-tuning.

### Max 5 Trials Per Hypothesis

| Trial Count | Action |
|-------------|--------|
| 1-3 | Normal iteration |
| 4-5 | Final attempts, consider archiving |
| >5 | STOP - Archive hypothesis, formulate new one |

---

## Failure Analysis (NOT Parameter Tweaking)

When a hypothesis fails, diagnose the ROOT CAUSE:

| Diagnosis | Symptom | Action |
|-----------|---------|--------|
| **Code Bug** | Results don't match expected behavior | Fix implementation, re-run same hypothesis |
| **Regime Failure** | Works in some periods, fails in others | Add regime filter (e.g., VIX < 20) |
| **Invalid Theory** | Consistent failure across all conditions | Archive to graveyard with learnings |
| **Insufficient Sample** | <100 trades, inconclusive statistics | Extend timeframe, add symbols |

### What NOT To Do

- Tweak parameters until backtest looks good
- Add indicators to "fix" losing trades
- Cherry-pick favorable time periods
- Ignore drawdowns that "won't happen again"

---

## Anti-Overfitting Rules

| Metric | Threshold | Rationale |
|--------|-----------|-----------|
| **Parameters** | <10 | Degrees of freedom must be low |
| **Trials** | <30 | Preserve statistical significance |
| **Trades** | >100 | Minimum sample size for inference |
| **IS/OOS Delta** | <30% | In-sample vs out-of-sample performance gap |


### Calculating IS/OOS Delta

```
IS_sharpe = 1.8   (in-sample backtest)
OOS_sharpe = 1.3  (out-of-sample forward test)

Delta = (IS_sharpe - OOS_sharpe) / IS_sharpe
      = (1.8 - 1.3) / 1.8
      = 27.8%  --> ACCEPTABLE (< 30%)
```

---

## When to Create NEW Hypothesis

Create a new hypothesis (not a revision) when:

| Trigger | Example |
|---------|---------|
| **Theory Invalidated** | "Mean reversion doesn't work in trending markets" - need new mechanism |
| **Different Economic Rationale** | Switching from momentum to value - different cause |
| **New Market Mechanism** | "Fed policy drives risk-on/off" - distinct from technical factors |

### New Hypothesis vs Revision

| Revision (Same Hypothesis) | New Hypothesis |
|----------------------------|----------------|
| Adjust lookback from 20 to 30 days | Change from momentum to mean-reversion |
| Add regime filter for high VIX | Target different asset class |
| Refine entry threshold | Different economic theory |

---

## Quick Reference Checklist

Before each test, verify:

- [ ] Hypothesis documented with cause/effect/rationale
- [ ] All parameters locked in version control
- [ ] Success criteria defined before running backtest
- [ ] Trial count < 5 for this hypothesis
- [ ] Total parameters < 10

After each test, document:

- [ ] Pass/fail against pre-defined criteria
- [ ] Root cause if failed (bug/regime/theory/sample)
- [ ] Next action (revise or archive)
- [ ] Learnings for future hypotheses
