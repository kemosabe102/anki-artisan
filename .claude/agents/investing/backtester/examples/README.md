# Backtester Examples

This directory contains example inputs/outputs for the backtester agent.

## Example: Successful Backtest

### Input
```json
{
  "mode": "single_run",
  "hypothesis_id": "HYP-001",
  "trial_number": 2,
  "trials_on_dataset": 8,
  "strategy_spec": {
    "strategy_name": "EMA Momentum",
    "strategy_type": "momentum",
    "universe": {"symbols": ["SPY"]},
    "entry": {"condition": "EMA(20) > EMA(50)"},
    "exit": {"condition": "ATR trailing stop"}
  },
  "backtest_params": {
    "start_date": "2020-01-01",
    "end_date": "2023-12-31",
    "initial_capital": 100000
  }
}
```

### Output
```json
{
  "status": "SUCCESS",
  "hypothesis_id": "HYP-001",
  "trial_number": 2,
  "trials_on_dataset": 8,
  "metrics": {
    "sharpe_raw": 0.92,
    "sharpe_deflated": 0.74,
    "deflation_factor": 0.80,
    "trade_count": 156,
    "max_drawdown": 0.18,
    "win_rate": 0.54,
    "profit_factor": 1.42
  },
  "validation_gates": {
    "trade_count": {"passed": true, "value": 156, "threshold": 100},
    "sharpe_raw": {"passed": true, "value": 0.92, "threshold": 0.5},
    "sharpe_deflated": {"passed": true, "value": 0.74, "threshold": 0.3},
    "max_drawdown": {"passed": true, "value": 0.18, "threshold": 0.25}
  },
  "verdict": "DEPLOYABLE",
  "verdict_reasons": ["All gates passed"],
  "next_action": "walk_forward",
  "failure_mode": null
}
```

## Example: Failed Backtest (Curve Fit)

### Output
```json
{
  "status": "SUCCESS",
  "hypothesis_id": "HYP-002",
  "trial_number": 4,
  "metrics": {
    "sharpe_raw": 1.85,
    "sharpe_deflated": 1.48,
    "trade_count": 45,
    "oos_is_ratio": 0.32
  },
  "validation_gates": {
    "trade_count": {"passed": false, "value": 45, "threshold": 100},
    "oos_is_ratio": {"passed": false, "value": 0.32, "threshold": 0.5}
  },
  "verdict": "NOT_DEPLOYABLE",
  "verdict_reasons": [
    "Trade count below minimum (45 < 100)",
    "OOS/IS ratio indicates curve fitting (0.32 < 0.5)"
  ],
  "next_action": "failure_analyzer",
  "failure_mode": "curve_fit"
}
```

## Example: Delegation to failure-analyzer

When verdict is NOT_DEPLOYABLE, the backtester routes to failure-analyzer:

```
Task(failure-analyzer): {
  "hypothesis_id": "HYP-002",
  "failure_mode": "curve_fit",
  "metrics": {
    "sharpe_raw": 1.85,
    "trade_count": 45,
    "oos_is_ratio": 0.32
  },
  "request": "Analyze failure and recommend NEW hypothesis or ARCHIVE"
}
```
