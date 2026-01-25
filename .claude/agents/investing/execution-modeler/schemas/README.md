# Execution Modeler - Schemas

This directory contains JSON schemas for the execution-modeler agent.

## Schema Files

| File | Purpose |
|------|---------|
| `execution-modeler.schema.json` | Input/output contract for execution cost estimates |

## Output Schema Summary

### SUCCESS Response

```json
{
  "status": "VIABLE|MARGINAL|NOT_VIABLE",
  "execution_cost_bps": 25,
  "cost_breakdown": {
    "slippage_estimate_bps": 15,
    "market_impact_bps": 8,
    "commission_bps": 2
  },
  "impact_model_used": "linear|square_root|almgren_chriss",
  "sharpe_analysis": {
    "sharpe_before_costs": 1.20,
    "sharpe_after_costs": 0.95,
    "degradation_pct": 20.8
  },
  "sensitivity_analysis": {
    "base_case": {"slippage_bps": 15, "sharpe": 0.95},
    "stress_case": {"slippage_bps": 23, "sharpe": 0.85}
  },
  "gates_passed": ["SLIPPAGE_ESTIMATE", "MARKET_IMPACT_MODEL", "SENSITIVITY_PASS"],
  "recommendations": [],
  "assumptions": [],
  "confidence": 0.85
}
```

### FAILURE Response

```json
{
  "status": "FAILURE",
  "error": "Missing required input: strategy_params",
  "required_fields": ["strategy_params", "universe", "target_capital_usd"],
  "recovery_guidance": "Provide strategy parameters including annual_trades and avg_position_size_usd"
}
```

## Validation Requirements

- `status` must be one of: VIABLE, MARGINAL, NOT_VIABLE, FAILURE
- `execution_cost_bps` must be non-negative integer
- `confidence` must be between 0.0 and 1.0
- `gates_passed` must contain all required gates for VIABLE status
- `sensitivity_analysis` must include `stress_case` for viability verdict

## Base Schema Extension

This schema extends `base-agent.schema.json` with execution-modeler-specific fields.
