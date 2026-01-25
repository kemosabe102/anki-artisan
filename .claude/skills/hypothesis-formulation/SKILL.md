---
name: hypothesis-formulation
description: >
  Guides hypothesis formulation for HDD workflow. Requires Cause→Effect→Why 
  structure before strategy specification. Locks parameters and defines fail 
  conditions BEFORE trial #1 begins.
  
  Use for: "I have an idea for...", "structure hypothesis", "define fail condition".
  Trigger keywords: hypothesis formulation, cause effect why, trading hypothesis.
  
  NOT for: Trial tracking or lifecycle management (hypothesis-tracking), 
  graveyard maintenance (hypothesis-tracking), mid-hypothesis constraint 
  changes (requires new hypothesis).
---

# Hypothesis Formulation Skill

*Structured hypothesis creation for Hypothesis-Driven Development*

## Quick Reference

| Aspect | Requirement |
|--------|-------------|
| Structure | Cause→Effect→Why (all three required) |
| Specificity | Measurable cause, testable effect |
| Fail condition | Must define BEFORE backtest |
| Min trades | 100 for statistical significance |
| Testable params | ONE per hypothesis |

---

## Hypothesis Template (REQUIRED)

"I believe that **[CAUSE: specific market signal/condition]** 
will lead to **[EFFECT: price movement/pattern]** 
because **[WHY: economic/behavioral mechanism]**."

### Components Explained

| Component | Definition | Requirement |
|-----------|------------|-------------|
| CAUSE | Specific market signal or condition | Measurable indicator + threshold |
| EFFECT | Expected price movement or pattern | Testable target + time horizon |
| WHY | Economic or behavioral mechanism | Grounded rationale (not curve-fit) |

---

## Example Hypothesis

```
CAUSE:  RSI(14) crosses below 30 while Price > SMA(200)
EFFECT: Price reverses upward within 5 bars
WHY:    Oversold conditions in an uptrend trigger value buyers
        who view the dip as a buying opportunity
```

**Formatted statement:**
"I believe that RSI(14) crossing below 30 while Price > SMA(200) 
will lead to price reversing upward within 5 bars 
because oversold conditions in an uptrend trigger value buyers."

---

## Constraints (MANDATORY)

### Fail Condition (Define A Priori)

| Metric | Threshold | Action |
|--------|-----------|--------|
| fail_condition | Define BEFORE backtest | e.g., "Sharpe < 0.5" |
| min_trades | 100 required | REJECT if < 100 trades |
| max_trials | 5 per hypothesis | HALT at 5, require NEW |

**Example fail conditions:**
- Sharpe ratio < 0.5
- Win rate < 40%
- Max drawdown > 25%
- Trade count < 100

### Parameter Locking

| Rule | Requirement |
|------|-------------|
| locked_parameters | List ALL params at hypothesis creation |
| testable_parameter | Mark exactly ONE as testable |
| single_change | Only ONE param may vary per trial |

**Example parameter specification:**
```json
{
  "locked_parameters": [
    "rsi_period: 14",
    "rsi_threshold: 30",
    "sma_period: 200",
    "exit_bars: 5"
  ],
  "testable_parameter": "rsi_threshold",
  "test_rationale": "Testing if 30 vs 25 threshold captures better entry timing"
}
```

---

## Quality Checklist

Before proceeding to strategy specification, verify:

- [ ] CAUSE is measurable (specific indicator/condition)
- [ ] EFFECT is testable (price target, time horizon)
- [ ] WHY is grounded (economic mechanism, not curve-fit)
- [ ] Fail condition defined before backtest
- [ ] Single testable parameter identified
- [ ] All other parameters locked
- [ ] Min trades requirement acknowledged (100)

---

## Anti-Patterns

| Anti-Pattern | Why Wrong | Correct Approach |
|--------------|-----------|------------------|
| Vague cause | Untestable hypothesis | Specific indicator + threshold |
| Multiple WHYs | Confounded causality | Single mechanism per hypothesis |
| No fail condition | Goalpost shifting | Define before backtest |
| Results-first | P-hacking risk | Hypothesis before code |
| Vague effect | Cannot measure success | Specific target + timeframe |
| Post-hoc WHY | Narrative fallacy | WHY must predict, not explain |
| Multiple testable params | Confounds results | ONE testable parameter only |

### Anti-Pattern Examples

**BAD - Vague cause:**
> "When the market looks oversold..."

**GOOD - Specific cause:**
> "When RSI(14) crosses below 30..."

**BAD - Multiple WHYs:**
> "Because of mean reversion AND momentum exhaustion AND institutional buying..."

**GOOD - Single WHY:**
> "Because oversold conditions trigger value buyers"

**BAD - No fail condition:**
> "Let's see how it performs"

**GOOD - Defined fail condition:**
> "FAIL if Sharpe < 0.5 after 100+ trades"

---

## Workflow Integration

```
User: "Build momentum strategy"
           |
           v
1. REQUIRE Cause->Effect->Why statement
           |
           v
2. VALIDATE each component (measurable, testable, grounded)
           |
           v
3. DEFINE fail_condition before any code
           |
           v
4. LOCK all parameters, mark ONE testable
           |
           v
5. PASS to strategy-specification skill
           |
           v
6. Track via hypothesis-tracking skill
```

---

## Reference Documentation

| Reference | Purpose |
|-----------|---------|
| `.claude/skills/hypothesis-tracking/SKILL.md` | Lifecycle management, graveyard |
| `.claude/skills/strategy-specification/SKILL.md` | 7-element framework, QC patterns |
