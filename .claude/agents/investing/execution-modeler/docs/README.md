# Execution Modeler - Domain Expertise

This directory contains domain knowledge for the execution-modeler agent.

## Documents

| File | Purpose |
|------|---------|
| `slippage-models.md` | Slippage estimation methodology and formulas |
| `market-impact-models.md` | Linear, square-root, and Almgren-Chriss models |
| `viability-thresholds.md` | Gate thresholds and rationale |

## Key Concepts

### Execution Costs Components

1. **Slippage**: Cost from bid-ask spread and adverse price movement
2. **Market Impact**: Price movement caused by order flow
3. **Commission**: Explicit broker fees per trade

### Model Selection Criteria

- **Linear**: Simple, conservative, for small orders (<1% ADV)
- **Square-Root**: Standard for medium orders (1-5% ADV)
- **Almgren-Chriss**: Sophisticated, for institutional-size orders (>5% ADV)

### Viability Gates

All gates must pass for VIABLE verdict:
- SLIPPAGE_ESTIMATE: Slippage quantified in bps
- MARKET_IMPACT_MODEL: Appropriate model selected and applied
- SENSITIVITY_PASS: Strategy survives +50% slippage stress test

## Related Agents

- `market-data-specialist`: Provides ADV data for impact calculations
- `backtester`: Provides raw metrics for cost adjustment
- `strategy-builder`: Provides strategy parameters for analysis
