# Crisis Stress Tester Examples

## Overview

This directory contains delegation and usage examples for the crisis-stress-tester agent.

## Contents

| File | Description |
|------|-------------|
| `delegation-examples.md` | Examples of delegating to/from this agent |

## Quick Usage Examples

### Full Crisis Suite

```
Task(crisis-stress-tester): {
  "hypothesis_id": "HYP-001",
  "mode": "full_crisis_suite",
  "strategy_spec": { ... },
  "backtest_passed": true,
  "request": "Run full crisis stress test suite"
}
```

### Single Crisis Test

```
Task(crisis-stress-tester): {
  "hypothesis_id": "HYP-001",
  "mode": "single_crisis",
  "crisis_period": "GFC_2008",
  "strategy_spec": { ... },
  "request": "Test strategy against 2008 GFC period"
}
```

### Tail Risk Analysis

```
Task(crisis-stress-tester): {
  "hypothesis_id": "HYP-001",
  "mode": "tail_analysis",
  "returns_data": [...],
  "confidence_levels": [0.95, 0.99],
  "request": "Calculate VaR and CVaR metrics"
}
```

## Expected Outputs

See `delegation-examples.md` for complete output examples.
