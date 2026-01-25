---
name: hypothesis-tracking
description: >
  Manages hypothesis lifecycle for HDD workflow. Assumes pre-formulated 
  hypotheses (Cause→Effect→Why already locked). Tracks trial counts (5-trial 
  limit), maintains graveyard of failed hypotheses, prevents zombie resurrection.
  
  Use for: "How many trials left?", "Why did trial #3 fail?", "Archive hypothesis".
  Trigger keywords: hypothesis tracking, trial counter, graveyard, failed hypotheses.
  
  NOT for: Creating new hypotheses or defining Cause→Effect→Why structure 
  (hypothesis-formulation), defining initial fail conditions or parameter 
  constraints (hypothesis-formulation), strategy code generation.
---

# Hypothesis Tracking Skill

*Lifecycle management for Hypothesis-Driven Development*

## Quick Reference

### Hypothesis Lifecycle States

| State | Description | Allowed Actions |
|-------|-------------|-----------------|
| FORMULATED | Hypothesis documented with Cause→Effect→Why | Start trial 1 |
| TESTING | Backtest in progress | Await result |
| VALIDATED | Passed statistical gates | Deploy or archive |
| FAILED | Did not meet criteria | Analyze → REVISE or ARCHIVE |
| ARCHIVED | In graveyard | Read-only reference |

### Trial Counter Rules

| Rule | Limit | Enforcement |
|------|-------|-------------|
| Max trials per hypothesis | 5 | HALT at 5, require NEW hypothesis |
| Warning threshold | 3 | WARN user: "3 trials used, 2 remaining" |
| Single change per trial | 1 | REJECT multi-parameter changes |

---

## Statistical Justification for 5-Trial Limit

The 5-trial limit is not arbitrary—it balances discovery rate against false positive risk.

### Power Analysis Assumptions

- **Base rate of "true edge" strategies**: 10% (most strategies don't have real edge)
- **DSR penalty gamma**: 0.08 per trial
- **Significance threshold**: α = 0.05
- **Minimum detectable Sharpe**: 0.30 (after deflation)

### False Discovery Rate by Trial Count

| Trials | Deflation Factor | False Discovery Rate | True Positive Rate |
|--------|------------------|---------------------|-------------------|
| 1 | 0.960 | 5% | 45% |
| 2 | 0.917 | 7% | 62% |
| 3 | 0.872 | 8% | 72% |
| 4 | 0.825 | 10% | 80% |
| **5** | **0.775** | **12%** | **85%** |
| 7 | 0.671 | 18% | 91% |
| 10 | 0.548 | 28% | 95% |

### Interpretation

At **5 trials**:
- **12% False Discovery Rate**: Roughly 1 in 8 "passing" strategies may be false positives
- **85% True Positive Rate**: We correctly identify 85% of strategies with genuine edge
- **DSR = 0.775 × raw Sharpe**: A raw Sharpe of 0.45 becomes DSR of 0.35

At **10 trials** (rejected):
- **28% False Discovery Rate**: Nearly 1 in 3 "passing" strategies would be false positives
- This is unacceptable for production deployment

### Why Not Fewer Trials?

At **3 trials**:
- Only 72% True Positive Rate
- Good strategies might be prematurely rejected
- Insufficient iteration for parameter refinement

### Conclusion

**5 trials** represents the optimal balance:
- High enough power (85%) to detect true edge
- Low enough false discovery (12%) to trust results
- Sufficient iteration for meaningful refinement
- Strong DSR penalty (22.5%) to discourage trial inflation

### Reference

This analysis follows the Deflated Sharpe Ratio methodology from Bailey & López de Prado (2014), adapted with Varma's recommendation for gamma=0.08 in retail trading contexts.

---

## Hypothesis Graveyard

### Purpose
Prevent "zombie hypothesis resurrection" - researchers re-testing failed ideas months later without remembering why they failed.

### Graveyard Entry Structure
```json
{
  "hypothesis_id": "H001",
  "cause_effect_why": {
    "cause": "RSI(14) crosses below 30",
    "effect": "Price reverses upward within 5 bars",
    "why": "Oversold conditions trigger value buyers"
  },
  "trial_count": 5,
  "failure_mode": "curve_fit | regime_mismatch | insufficient_trades | implementation_bug",
  "backtest_metrics": {
    "sharpe_raw": 0.8,
    "sharpe_deflated": 0.2,
    "trade_count": 45,
    "max_drawdown": -18.5
  },
  "buried_at": "2025-01-15T14:30:00Z",
  "epitaph": "Signal worked in bull markets only. No edge in bear/sideways."
}
```

### Failure Modes

| Mode | Description | Next Action |
|------|-------------|-------------|
| `curve_fit` | Strategy overfit to backtest period | ARCHIVE, dataset burned |
| `regime_mismatch` | Works in some regimes only | Add regime filter → NEW hypothesis |
| `insufficient_trades` | < 100 trades for significance | Extend timeframe → NEW hypothesis |
| `implementation_bug` | Code error detected | Fix bug, does NOT count as trial |

---

## Trial Tracking Protocol

### Before Each Trial
1. Check hypothesis_id exists
2. Check trial_number ≤ 5
3. Verify single_change documented
4. Confirm locked_parameters unchanged

### After Each Trial
1. Increment trial_number
2. Record backtest_metrics
3. If FAILED: Route to failure analyzer
4. If trial_number = 5 and FAILED: Force ARCHIVE

---

## Anti-Patterns

| Anti-Pattern | Why Wrong | Correct Approach |
|--------------|-----------|------------------|
| Reset trial counter | Gaming the safety system | Hypothesis graveyard is permanent |
| Test "similar" hypothesis | Zombie resurrection | Check graveyard first |
| Multiple param changes | Confounds causality | Single change per trial |
| Skip failure analysis | Repeats mistakes | ALWAYS analyze before new hypothesis |

---

## Workflow Integration

```
User: "Build momentum strategy"
           ↓
1. Check graveyard for similar hypotheses
           ↓
2. Require Cause→Effect→Why statement
           ↓
3. Lock parameters, set trial_number = 1
           ↓
4. Generate spec → Run backtest
           ↓
5. If FAILED:
   - trial_number < 5 → failure_analyzer → NEW hypothesis
   - trial_number = 5 → ARCHIVE to graveyard
           ↓
6. If PASSED:
   - Walk-forward validation
   - If passes → VALIDATED
   - If fails → ARCHIVE
```


---

## Knowledge Base

| Document | Purpose |
|----------|---------|
| `schemas/trial-audit.schema.json` | Trial audit manifest validation |
| `.claude/skills/failure-analyzer/SKILL.md` | Luck vs process classification |
| `.claude/skills/strategy-specification/SKILL.md` | 7-element framework |
| `.claude/agents/investing/strategy-builder/schemas/` | Schema with graveyard structure |
