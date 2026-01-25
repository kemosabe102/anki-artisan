# Execution Modeler - Examples

This directory contains delegation examples and usage patterns for the execution-modeler agent.

## Documents

| File | Purpose |
|------|---------|
| `delegation-examples.md` | How to delegate to and from this agent |

## Quick Reference

### Delegating TO execution-modeler

```
Task(execution-modeler): {
  "request": "validate_viability",
  "strategy_params": {
    "annual_trades": 200,
    "avg_position_size_usd": 10000
  },
  "backtest_sharpe": 1.2,
  "universe": ["AAPL", "MSFT"],
  "target_capital_usd": 100000
}
```

### Expected Response

```json
{
  "status": "VIABLE",
  "execution_cost_bps": 25,
  "sharpe_after_costs": 0.95,
  "recommendations": []
}
```

## Common Use Cases

1. **Pre-deployment viability check**: Validate strategy before live trading
2. **Capacity analysis**: Determine maximum tradeable capital
3. **Sensitivity analysis**: Stress test under adverse conditions
4. **Cost comparison**: Compare execution costs across universes
