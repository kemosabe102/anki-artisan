# Gate Thresholds Reference

**Purpose**: Consolidated reference for all validation gate thresholds used by backtester.

---

## Standard Validation Gates

| Gate | Threshold | Severity | Notes |
|------|-----------|----------|-------|
| Trade Count | >= 100 | HARD | Ensures statistical significance |
| Sharpe (deflated) | >= 0.3 | HARD | After trial penalty applied |
| Sharpe (raw) | >= 0.5 | SOFT | Before deflation |
| Max Drawdown | <= 25% | SOFT | Maximum acceptable peak-to-trough |
| OOS/IS Ratio | >= 0.5 | HARD | Out-of-sample vs in-sample performance |

---

## Regime-Adjusted Thresholds

| Regime | Sharpe Min | Max DD | Trade Count |
|--------|------------|--------|-------------|
| HIGH_RISK | 0.20 | 35% | 60 |
| ELEVATED | 0.25 | 30% | 80 |
| NORMAL | 0.30 | 25% | 100 |
| LOW_RISK | 0.35 | 20% | 100 |

---

## Tier-Specific Gates

| Tier | Additional Gates |
|------|------------------|
| Tier 1-2 | Standard gates only |
| Tier 3 | + Capacity Score >= 70 (SOFT) |
| Tier 4 | + Monte Carlo p-value < 0.05 (HARD), + Capacity Score >= 75 (HARD) |

---

## Deflated Sharpe Ratio (DSR)

Applied at Tier 4 only:

```
DSR = SR × sqrt(1 - gamma × T)

Where:
- SR = Raw Sharpe Ratio  
- gamma = 0.08 (trial penalty factor, from tier-config.json)
- T = trials_on_dataset (cumulative trials)
```

| Trials | Deflation Factor | SR=1.0 → DSR |
|--------|------------------|---------------|
| 1 | 0.960 | 0.960 |
| 2 | 0.917 | 0.917 |
| 3 | 0.871 | 0.871 |
| 4 | 0.822 | 0.822 |
| 5 | 0.775 | 0.775 |

---

## Gate Evaluation Order

1. Trade Count (HARD) - First check
2. Sharpe Deflated (HARD)
3. OOS/IS Ratio (HARD)
4. Max Drawdown (SOFT)
5. Sharpe Raw (SOFT)
6. Monte Carlo (Tier 4 only, HARD)
7. Capacity Score (Tier 3+ only)

**Rule**: First HARD failure = NOT_DEPLOYABLE. All SOFT failures = NEEDS_REVIEW.
