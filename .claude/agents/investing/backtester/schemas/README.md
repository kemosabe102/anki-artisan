# Backtester Schemas

This directory contains JSON Schema definitions for the backtester agent.

## Files

| Schema | Purpose |
|--------|---------|
| `backtester.schema.json` | Input/Output contract for all backtester modes |

## Schema Overview

### Input Requirements

| Field | Required | Description |
|-------|----------|-------------|
| `mode` | Yes | single_run, regime_test, walk_forward, final_validation |
| `hypothesis_id` | Yes | HYP-XXX format identifier |
| `trial_number` | Yes | Current trial (1-5) |
| `strategy_spec` | Yes | Strategy specification from strategy-builder |
| `backtest_params` | No | Date range and capital |
| `locked_parameters` | No | Parameters that cannot change |
| `regime_context` | No | For regime_test mode |
| `walk_forward_params` | No | For walk_forward mode |

### Output Structure

| Field | Always Present | Description |
|-------|----------------|-------------|
| `status` | Yes | SUCCESS or FAILURE |
| `hypothesis_id` | Yes | Echo of input |
| `trial_number` | Yes | Trial executed |
| `metrics` | Yes | Performance metrics with deflated Sharpe |
| `verdict` | Yes | DEPLOYABLE, NOT_DEPLOYABLE, NEEDS_REVIEW |
| `next_action` | Yes | Routing decision |
| `failure_mode` | If failed | Classification of failure |

## Validation Gate Thresholds

Defined as constants in schema:
- `trade_count`: 100 (HARD)
- `sharpe_raw`: 0.5 (SOFT)
- `sharpe_deflated`: 0.3 (HARD)
- `max_drawdown`: 0.25 (SOFT)
- `oos_is_ratio`: 0.5 (HARD)
