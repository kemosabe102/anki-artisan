# Crisis Stress Tester Schemas

## Overview

This directory contains JSON schemas for crisis-stress-tester input/output validation.

## Schema Files

| File | Purpose |
|------|---------|
| `crisis-stress-tester.schema.json` | Main agent input/output schema |

## Schema Structure

The crisis-stress-tester schema extends `base-agent.schema.json` with:

### Input Schema

```json
{
  "type": "object",
  "required": ["hypothesis_id", "mode"],
  "properties": {
    "hypothesis_id": {
      "type": "string",
      "pattern": "^HYP-[0-9]{3}"
    },
    "mode": {
      "type": "string",
      "enum": ["full_crisis_suite", "single_crisis", "tail_analysis", "synthetic_test"]
    },
    "strategy_spec": {
      "type": "object"
    },
    "backtest_passed": {
      "type": "boolean"
    },
    "crisis_period": {
      "type": "string",
      "enum": ["GFC_2008", "COVID_2020", "RATE_HIKE_2022", "FLASH_CRASH_2010"]
    }
  }
}
```

### Output Schema

```json
{
  "type": "object",
  "required": ["status", "hypothesis_id", "overall_status", "overall_score", "crisis_results", "verdict"],
  "properties": {
    "status": {
      "type": "string",
      "enum": ["SUCCESS", "FAILURE"]
    },
    "overall_status": {
      "type": "string",
      "enum": ["CRISIS_PROOF", "VULNERABLE", "FRAGILE"]
    },
    "overall_score": {
      "type": "number",
      "minimum": 0,
      "maximum": 100
    },
    "crisis_results": {
      "type": "object",
      "properties": {
        "gfc_2008": { "$ref": "#/definitions/crisis_result" },
        "covid_2020": { "$ref": "#/definitions/crisis_result" },
        "rate_hike_2022": { "$ref": "#/definitions/crisis_result" }
      }
    },
    "tail_metrics": {
      "type": "object",
      "properties": {
        "var_95": { "type": "number" },
        "var_99": { "type": "number" },
        "cvar_99": { "type": "number" },
        "max_consecutive_losses": { "type": "integer" }
      }
    },
    "verdict": {
      "type": "string",
      "enum": ["CRISIS_PROOF", "VULNERABLE", "FRAGILE"]
    },
    "recommendations": {
      "type": "array",
      "items": { "type": "string" }
    }
  }
}
```

### Crisis Result Definition

```json
{
  "definitions": {
    "crisis_result": {
      "type": "object",
      "required": ["max_dd", "benchmark_dd", "gate_status"],
      "properties": {
        "max_dd": { "type": "number" },
        "benchmark_dd": { "type": "number" },
        "dd_ratio": { "type": "number" },
        "recovery_days": { "type": ["integer", "null"] },
        "period_sharpe": { "type": "number" },
        "gate_status": {
          "type": "string",
          "enum": ["PASS", "FAIL"]
        },
        "gate_threshold": { "type": "string" },
        "gate_reason": { "type": "string" }
      }
    }
  }
}
```

## Validation

All agent outputs are validated against this schema before returning to the orchestrator.
