# Documentation-First Strategy Example

This example demonstrates the `/algo-strategy` command parsing an existing strategy document.

---

## User Input

```
/algo-strategy --from-doc docs/investing/MVP-ARCHITECTURE-PLAN.md
```

---

## Document Analysis

The command scans the document and extracts strategy components:

```yaml
extracted:
  universe: ["SPY"]
  entry:
    signal: "EMA crossover"
    params: {fast: 20, slow: 50}
  risk:
    max_drawdown: "2%"
    
missing:
  - exit_rules
  - position_sizing
  - timeframe
  
confidence: 0.65
```

---

## Clarifying Questions Generated

The system identifies gaps and generates targeted questions:

1. **Exit Rules**: "What triggers position close? Options: profit target, trailing stop, time-based, signal reversal"
2. **Position Sizing**: "What sizing method? Options: fixed percentage, volatility-adjusted, Kelly criterion"
3. **Timeframe**: "Daily or intraday resolution?"

---

## User Answers

```
Exit: trailing stop at 2x ATR
Sizing: fixed 10% per position
Timeframe: daily
```

---

## Completed Hypothesis

```yaml
hypothesis_id: HYP-002
cause: "EMA(20) crosses above EMA(50) on daily timeframe"
effect: "Trend continuation captured with controlled downside"
why: "Document specifies momentum-based approach with strict risk limits"
testability_score: 0.90
params_locked:
  ema_fast: 20
  ema_slow: 50
  atr_multiplier: 2.0
  position_size: 0.10
  resolution: "daily"
trial_number: 0
source_doc: "docs/investing/MVP-ARCHITECTURE-PLAN.md"
```

---

## Next Steps

1. **Validate extraction**: Confirm parsed values match document intent
2. **Generate spec**: Creates full strategy specification from hypothesis
3. **Backtest**: `/backtest HYP-002` with source document as reference
