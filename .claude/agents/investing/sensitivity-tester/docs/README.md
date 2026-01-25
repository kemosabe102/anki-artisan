# Sensitivity Tester Documentation

## Overview

The sensitivity-tester agent validates strategy robustness through three primary mechanisms:

1. **Noise Injection**: Perturbs parameters ±10% to detect curve-fitting
2. **Walk-Forward Analysis**: Rolling window out-of-sample validation
3. **Parameter Stability**: Identifies cliff-edge parameters

## Quick Reference

| Gate | Threshold | Severity |
|------|-----------|----------|
| NOISE_ROBUST | <30% Sharpe degradation | HARD |
| WALK_FORWARD_VALID | OOS/IS ratio >= 0.50 | HARD |
| PARAMETER_STABLE | No cliff-edges (>50% drop at ±5%) | SOFT |

## When to Use

- After initial backtest passes validation gates
- Before holdout/final validation
- When strategy shows suspiciously good performance
- As part of P9 in the 10-phase algo-strategy workflow

## Integration

```
strategy-builder -> backtester -> sensitivity-tester -> holdout/archive
```

## Key Concepts

### Robustness Score (0-100)

Weighted combination of three factors:
- Noise stability (40%)
- Walk-forward efficiency (40%)
- Parameter stability (20%)

### Verdict Mapping

| Score | Verdict | Action |
|-------|---------|--------|
| 80-100 | ROBUST | Proceed to holdout |
| 60-79 | MARGINAL | Proceed with monitoring |
| 40-59 | FRAGILE | Return for refinement |
| 0-39 | OVERFIT | Archive |

## Files in This Directory

- `sensitivity-methodology.md` - Theory and calculations
- `../examples/delegation-examples.md` - Usage patterns
