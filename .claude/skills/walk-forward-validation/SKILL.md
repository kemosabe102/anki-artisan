---
name: walk-forward-validation
description: >
  Walk-forward validation protocol for strategy backtesting. Enforces IS/OOS/Holdout splits and rolling window validation.
  Trigger keywords: walk-forward, out-of-sample, holdout, validation, curve-fit detection.
---

# Walk-Forward Validation Skill

*Preventing curve-fitting through rigorous out-of-sample validation*

## Quick Reference

### Data Split Requirements

| Period | % of Data | Usage |
|--------|-----------|-------|
| In-Sample (IS) | 60-70% | Hypothesis testing (max 5 trials) |
| Out-of-Sample (OOS) | 20-30% | Single validation (NO iteration) |
| Holdout | 10% | Final deployment gate |

---

## Walk-Forward Protocol

The walk-forward protocol ensures strategies generalize beyond their training data:

```
1. Train on IS → Validate on OOS (single pass)
2. If OOS Sharpe < 0.5 × IS Sharpe → REJECT (curve-fit)
3. Roll window forward, repeat (min 3 windows required)
4. Calculate average OOS performance across windows
5. Final holdout test only after all windows pass
```

### Protocol Flow

```
┌─────────────────────────────────────────────────────┐
│                  WALK-FORWARD FLOW                   │
│                                                      │
│   Window 1: [IS₁ 60%][OOS₁ 30%]    → OOS₁ Sharpe    │
│   Window 2:    [IS₂ 60%][OOS₂ 30%] → OOS₂ Sharpe    │
│   Window 3:       [IS₃ 60%][OOS₃ 30%] → OOS₃ Sharpe │
│                                                      │
│   All windows pass? ────────YES────────> Holdout    │
│         │                                   │        │
│         NO                              PASS/FAIL    │
│         │                                   │        │
│         v                                   v        │
│      REJECT                        DEPLOY / ARCHIVE  │
└─────────────────────────────────────────────────────┘
```

---

## Curve-Fit Detection

Curve-fitting occurs when a strategy is over-optimized to historical data and fails on new data.

### Detection Thresholds

| Indicator | Threshold | Interpretation |
|-----------|-----------|----------------|
| OOS/IS Sharpe Ratio | < 0.5 | Severe curve-fit |
| OOS/IS Sharpe Ratio | 0.5-0.7 | Moderate curve-fit |
| OOS/IS Sharpe Ratio | > 0.7 | Acceptable degradation |
| OOS Win Rate vs IS Win Rate | > 20% drop | Signal instability |

### Curve-Fit Severity Levels

| Level | OOS/IS Ratio | Action |
|-------|--------------|--------|
| SEVERE | < 0.5 | REJECT immediately, archive to graveyard |
| MODERATE | 0.5-0.7 | WARNING, investigate parameters |
| ACCEPTABLE | > 0.7 | PASS, proceed to next window |

---

## Window Configuration

### Minimum Requirements

| Requirement | Value | Rationale |
|-------------|-------|-----------|
| Minimum windows | 3 | Statistical significance |
| Minimum trades per window | 30 | Law of large numbers |
| Market condition coverage | Bull + Bear + Sideways | Regime robustness |

### Window Sizing Guidelines

```
Total Data: 5 years (2019-2024)
├── Window 1: 2019-2021 (IS) → 2021-2022 (OOS)
├── Window 2: 2020-2022 (IS) → 2022-2023 (OOS)
├── Window 3: 2021-2023 (IS) → 2023-2024 (OOS)
└── Holdout: 2024 (10% reserved, NEVER touched until final)
```

### Market Condition Verification

Each window should ideally span different market regimes:

| Window | Required Conditions |
|--------|---------------------|
| Window 1 | Must include at least 1 regime type |
| Window 2 | Must differ from Window 1 regime |
| Window 3 | Should span regime transition |

---

## Holdout Rules

The holdout set is the final gatekeeper before deployment.

### Sacred Principles

| Rule | Description | Violation Consequence |
|------|-------------|----------------------|
| NEVER touch until ready | Holdout remains sealed during all IS/OOS work | Data leakage, invalid results |
| Single test only | ONE evaluation, no iteration | Burns the holdout |
| No parameter changes | Use exact parameters from OOS validation | Curve-fitting |
| Holdout failure = ARCHIVE | No second chances | Graveyard entry |

### Holdout Protocol

```
1. Confirm ALL OOS windows passed (OOS/IS Sharpe > 0.5)
2. Calculate average OOS Sharpe across windows
3. Document final parameters (locked, no changes)
4. Run SINGLE holdout backtest
5. Compare holdout Sharpe to average OOS Sharpe
6. If Holdout/OOS Sharpe > 0.7 → DEPLOY
7. If Holdout/OOS Sharpe < 0.7 → ARCHIVE to graveyard
```

### Holdout Metrics Required

| Metric | Passing Threshold |
|--------|-------------------|
| Holdout Sharpe | > 0.5 |
| Holdout/OOS Sharpe Ratio | > 0.7 |
| Holdout Max Drawdown | < 1.5 × OOS Max Drawdown |
| Holdout Trade Count | >= 10 (statistical minimum) |

---

## Anti-Patterns

| Anti-Pattern | Why Wrong | Correct Approach |
|--------------|-----------|------------------|
| Peek at OOS during development | Data leakage invalidates validation | Train on IS only, OOS is sealed |
| Multiple OOS iterations | Burns validation data, curve-fits to OOS | Single pass per window |
| Skip holdout | No final deployment gate | Always reserve 10% |
| Short windows | Insufficient trades for significance | Min 30 trades per window |
| Reuse holdout after failure | Contaminated data | Archive strategy, start fresh |
| Optimize on combined IS+OOS | Entire dataset leaked | Strict separation enforced |
| Cherry-pick best window | Selection bias | Report ALL windows, use average |

---

## Validation Checklist

Before proceeding to each stage, verify:

### Pre-OOS Checklist
- [ ] IS training complete with locked parameters
- [ ] Trial count documented (max 5 trials on IS)
- [ ] OOS data has NOT been viewed or analyzed
- [ ] Single parameter set selected (no ensembles)

### Pre-Holdout Checklist
- [ ] Minimum 3 OOS windows completed
- [ ] ALL windows have OOS/IS Sharpe > 0.5
- [ ] Average OOS Sharpe calculated
- [ ] Parameters locked (no further changes)
- [ ] Holdout data has NEVER been touched

---

## Workflow Integration

```
User: "Validate momentum strategy"
           ↓
1. Verify IS training complete (from hypothesis-tracking)
           ↓
2. Split data: IS (60-70%) | OOS (20-30%) | Holdout (10%)
           ↓
3. Run walk-forward on Window 1
   - Train on IS₁ → Test on OOS₁
   - Calculate OOS₁/IS₁ Sharpe ratio
           ↓
4. If OOS/IS < 0.5 → REJECT (curve-fit detected)
   If OOS/IS >= 0.5 → Continue to Window 2
           ↓
5. Repeat for Windows 2, 3 (minimum)
           ↓
6. All windows pass? → Calculate average OOS metrics
           ↓
7. Run SINGLE holdout test
           ↓
8. Holdout passes? → DEPLOY
   Holdout fails? → ARCHIVE to graveyard
```

---

## Reference Documentation

| Reference | Purpose |
|-----------|---------|
| `.claude/skills/hypothesis-tracking/SKILL.md` | Trial counting, graveyard management |
| `.claude/skills/failure-analyzer/SKILL.md` | Failure mode analysis for rejected strategies |
| `.claude/skills/strategy-specification/SKILL.md` | 7-element strategy framework |
