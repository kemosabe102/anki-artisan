# Sensitivity Tester Schemas

## Schema Location

**Primary Schema**: `./sensitivity-tester.schema.json` (local to this directory)

**Status**: Active

## Schema Contract

The sensitivity-tester agent extends `base-agent.schema.json` with:

### Input Schema

```json
{
  "hypothesis_id": "string (required)",
  "mode": "full_test|noise_only|walk_forward_only|stability_check",
  "hypothesis_bundle": {
    "strategy_name": "string",
    "parameters": "object"
  },
  "baseline_metrics": {
    "sharpe": "number (required)",
    "trade_count": "number",
    "max_drawdown": "number"
  }
}
```

### Output Schema

```json
{
  "status": "ROBUST|MARGINAL|FRAGILE|OVERFIT",
  "hypothesis_id": "string",
  "sensitivity_score": "number (0-100)",
  "noise_test": {
    "base_sharpe": "number",
    "noise_sharpe_mean": "number",
    "degradation_pct": "number",
    "status": "PASS|FAIL"
  },
  "walk_forward": {
    "in_sample_sharpe": "number",
    "out_sample_sharpe": "number",
    "efficiency_ratio": "number",
    "num_folds": "number",
    "status": "PASS|FAIL"
  },
  "gate_results": "object",
  "recommendations": "array",
  "next_action": "holdout_validation|refinement|archive"
}
```

## Validation

All outputs must validate against the schema before returning to orchestrator.
