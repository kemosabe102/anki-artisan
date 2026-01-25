# Delegation Examples

## Delegating TO execution-modeler

### From algo-strategy command (P6 phase)

```
Task(execution-modeler): {
  "request": "validate_viability",
  "strategy_params": {
    "annual_trades": 200,
    "avg_position_size_usd": 10000,
    "avg_holding_period_days": 5
  },
  "backtest_sharpe": 1.2,
  "backtest_annual_return_pct": 15.0,
  "universe": ["AAPL", "MSFT", "GOOGL", "AMZN"],
  "target_capital_usd": 100000
}
```

### From strategy-builder

```
Task(execution-modeler): {
  "request": "estimate_costs",
  "strategy_params": {
    "annual_trades": 500,
    "avg_position_size_usd": 5000,
    "avg_holding_period_days": 2
  },
  "universe": ["IWM", "VTI", "QQQ"],
  "target_capital_usd": 250000,
  "commission_per_trade_usd": 0.0
}
```

### From backtester (capacity check)

```
Task(execution-modeler): {
  "request": "analyze_capacity",
  "strategy_params": {
    "annual_trades": 150,
    "avg_position_size_usd": 20000
  },
  "universe": ["SPY", "QQQ"],
  "max_impact_bps": 25,
  "capital_increments": [100000, 500000, 1000000, 5000000]
}
```

### Inbound: Sensitivity Analysis Request

**From**: Orchestrator
**Operation**: Run sensitivity analysis across multiple scenarios

```
Task(execution-modeler): {
  "operation": "sensitivity_analysis",
  "strategy_params": {
    "annual_trades": 200,
    "avg_position_size_usd": 10000,
    "avg_holding_period_days": 5
  },
  "scenarios": ["base", "elevated", "stress", "crisis"],
  "backtest_sharpe": 1.2,
  "universe": ["AAPL", "MSFT", "GOOGL"],
  "target_capital_usd": 100000
}
```

**Expected Response**:
```json
{
  "status": "SUCCESS",
  "stress_test_performed": true,
  "scenario_results": {
    "base": { "slippage_multiplier": 1.0, "total_cost_bps": 25, "sharpe": 0.95 },
    "elevated": { "slippage_multiplier": 1.25, "total_cost_bps": 31, "sharpe": 0.88 },
    "stress": { "slippage_multiplier": 1.5, "total_cost_bps": 38, "sharpe": 0.78 },
    "crisis": { "slippage_multiplier": 2.0, "total_cost_bps": 50, "sharpe": 0.62 }
  },
  "breakeven_slippage_multiplier": 2.4,
  "sharpe_waterfall": {
    "before_costs": 1.20,
    "base_case": 0.95,
    "stress_case": 0.78,
    "degradation_base_pct": 20.8,
    "degradation_stress_pct": 35.0
  },
  "confidence": 0.88
}
```

---

## Delegating FROM execution-modeler

### To market-data-specialist (ADV request)

```
Task(market-data-specialist): {
  "request": "Get ADV for symbols",
  "symbols": ["AAPL", "MSFT", "GOOGL"],
  "lookback_days": 20
}
```

**Expected Response**:
```json
{
  "status": "SUCCESS",
  "data": {
    "AAPL": {
      "adv_shares": 75000000,
      "adv_usd": 12500000000,
      "data_date": "2024-01-15"
    },
    "MSFT": {
      "adv_shares": 25000000,
      "adv_usd": 8000000000,
      "data_date": "2024-01-15"
    }
  }
}
```

## Full Workflow Example

### P6 Execution Modeling in algo-strategy --full

**Step 1**: Receive strategy from backtester

```json
{
  "hypothesis_id": "HYP-001",
  "backtest_sharpe": 1.35,
  "annual_return_pct": 18.5,
  "annual_trades": 180,
  "avg_position_size_usd": 8500,
  "universe": ["AAPL", "MSFT", "NVDA", "GOOGL"]
}
```

**Step 2**: Delegate ADV request

```
Task(market-data-specialist): {
  "request": "Get ADV for symbols",
  "symbols": ["AAPL", "MSFT", "NVDA", "GOOGL"],
  "lookback_days": 20
}
```

**Step 3**: Calculate execution costs

```
- Slippage: 12 bps (spread + volatility)
- Market Impact: 5 bps (square-root model, order/ADV < 0.1%)
- Commission: 2 bps (retail broker)
- Total: 19 bps per trade
```

**Step 4**: Run sensitivity analysis

```json
{
  "base_case": {"slippage_bps": 12, "sharpe": 1.15},
  "stress_case": {"slippage_bps": 18, "sharpe": 1.02}
}
```

**Step 5**: Render verdict

```json
{
  "status": "VIABLE",
  "execution_cost_bps": 19,
  "sharpe_after_costs": 1.15,
  "stress_sharpe": 1.02,
  "gates_passed": ["SLIPPAGE_ESTIMATE", "MARKET_IMPACT_MODEL", "SENSITIVITY_PASS"],
  "recommendations": [],
  "next_action": "proceed_to_P7"
}
```
