# Backtester Documentation

This directory contains domain knowledge and reference documentation for the backtester agent.

## Contents

| Document | Purpose |
|----------|---------|
| `deflated-sharpe.md` | Deflated Sharpe Ratio calculation and rationale |
| `validation-gates.md` | Statistical validation gate definitions |
| `regime-testing.md` | Volatility regime testing methodology |
| `gate-thresholds.md` | Consolidated gate threshold reference |
| `memory-optimization.md` | QC memory estimation and optimization guide |

## Key Concepts

### HDD Compliance

Hypothesis-Driven Development (HDD) prevents overfitting through:
1. Mandatory hypothesis_id before ANY backtest
2. Maximum 5 trials per hypothesis
3. Single parameter change per trial
4. Deflated Sharpe calculation

### Statistical Validation

The backtester enforces gates in order:
1. Trade Count >= 100 (HARD)
2. Sharpe (raw) >= 0.5 (SOFT)
3. Sharpe (deflated) >= 0.3 (HARD)
4. Max Drawdown <= 25% (SOFT)
5. OOS/IS Ratio >= 0.5 (HARD)

## Related Skills

- `hypothesis-tracking` - Trial counting and parameter locking
- `failure-analyzer` - Failure mode classification
- `walk-forward-validation` - Rolling window methodology
