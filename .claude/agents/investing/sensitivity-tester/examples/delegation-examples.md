# Delegation Examples

## Full Sensitivity Test

### Orchestrator to sensitivity-tester

```
Task(sensitivity-tester, {
  "mode": "full_test",
  "hypothesis_id": "HYP-001",
  "hypothesis_bundle": {
    "strategy_name": "momentum_breakout",
    "parameters": {
      "lookback_period": 20,
      "breakout_threshold": 1.5,
      "atr_multiplier": 2.0
    }
  },
  "baseline_metrics": {
    "sharpe": 1.2,
    "trade_count": 156,
    "max_drawdown": -0.18
  }
})
```

### Expected Response (ROBUST)

```json
{
  "status": "ROBUST",
  "hypothesis_id": "HYP-001",
  "sensitivity_score": 82,
  "noise_test": {
    "base_sharpe": 1.2,
    "noise_sharpe_mean": 1.02,
    "degradation_pct": 15,
    "status": "PASS"
  },
  "walk_forward": {
    "efficiency_ratio": 0.68,
    "status": "PASS"
  },
  "next_action": "holdout_validation"
}
```

## Noise Test Only

### Request

```
Task(sensitivity-tester, {
  "mode": "noise_only",
  "hypothesis_id": "HYP-002",
  "strategy_params": {
    "rsi_period": 14,
    "overbought": 70,
    "oversold": 30
  },
  "baseline_sharpe": 0.95
})
```

### Response (FRAGILE)

```json
{
  "status": "FAIL",
  "base_sharpe": 0.95,
  "noise_sharpe_mean": 0.55,
  "degradation_pct": 42,
  "fragile_parameters": ["rsi_period", "overbought"],
  "recommendation": "RSI period shows cliff-edge at 12 and 16. Consider using adaptive period."
}
```


## sensitivity-tester to backtester

### Noise Test Delegation

```
Task(backtester, {
  "hypothesis_id": "HYP-001",
  "mode": "single_run",
  "strategy_spec": {
    "name": "momentum_breakout",
    "parameters": {
      "lookback_period": 18,  // noised from 20 (-10%)
      "breakout_threshold": 1.5,
      "atr_multiplier": 2.0
    }
  },
  "context": "sensitivity_noise_test",
  "backtest_params": {
    "start_date": "2018-01-01",
    "end_date": "2023-12-31"
  }
})
```

### Walk-Forward Fold Delegation

```
Task(backtester, {
  "hypothesis_id": "HYP-001",
  "mode": "single_run",
  "strategy_spec": {...},
  "context": "sensitivity_walk_forward_fold_3",
  "backtest_params": {
    "start_date": "2020-01-01",  // OOS start
    "end_date": "2020-12-31"     // OOS end
  }
})
```

## Failure Case: OVERFIT

### Response

```json
{
  "status": "OVERFIT",
  "hypothesis_id": "HYP-003",
  "sensitivity_score": 28,
  "noise_test": {
    "degradation_pct": 48,
    "status": "FAIL"
  },
  "walk_forward": {
    "efficiency_ratio": 0.32,
    "status": "FAIL"
  },
  "gate_results": {
    "NOISE_ROBUST": {"passed": false, "value": 48, "threshold": 30},
    "WALK_FORWARD_VALID": {"passed": false, "value": 0.32, "threshold": 0.50}
  },
  "recommendations": [
    "Strategy shows severe curve-fitting (48% degradation under noise)",
    "Walk-forward efficiency of 0.32 indicates poor generalization",
    "Recommend archiving and reformulating hypothesis"
  ],
  "next_action": "archive",
  "failure_mode": "multi_failure"
}
```

## Examples README

This directory contains delegation examples for:
- Orchestrator -> sensitivity-tester requests
- sensitivity-tester -> backtester delegations
- Success and failure response patterns
