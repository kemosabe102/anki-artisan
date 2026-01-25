# Freeform Strategy Example

This example demonstrates the `/algo-strategy` command with a natural language strategy description.

---

## User Input

```
/algo-strategy "momentum strategy buying SPY when EMA(20) crosses above EMA(50), with ATR trailing stop"
```

---

## Generated Hypothesis

```yaml
hypothesis_id: HYP-001
cause: "EMA(20) crosses above EMA(50)"
effect: "Price continues upward for days/weeks"
why: "Short-term momentum exceeding medium-term indicates trend strength"
testability_score: 0.85
params_locked:
  ema_fast: 20
  ema_slow: 50
  atr_multiplier: 2.0
trial_number: 0
```

---

## Generated Spec (abbreviated)

```json
{
  "strategy_id": "momentum-ema-crossover",
  "universe": ["SPY"],
  "entry": {
    "signal": "ema_crossover",
    "params": {"fast": 20, "slow": 50}
  },
  "exit": {
    "trailing_stop": {"type": "atr", "multiplier": 2.0}
  },
  "risk": {
    "max_position_pct": 0.10
  }
}
```

---

## Generated Skeleton (abbreviated)

```python
class MomentumEmaCrossover(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2020, 1, 1)
        self.SetCash(100000)
        self.symbol = self.AddEquity("SPY", Resolution.Daily).Symbol
        
        self.ema_fast = self.EMA(self.symbol, 20)
        self.ema_slow = self.EMA(self.symbol, 50)
        self.atr = self.ATR(self.symbol, 14)
        
    def OnData(self, data):
        if not self.ema_fast.IsReady or not self.ema_slow.IsReady:
            return
            
        if self.ema_fast.Current.Value > self.ema_slow.Current.Value:
            if not self.Portfolio[self.symbol].Invested:
                self.SetHoldings(self.symbol, 0.10)
```

---

## Next Steps

1. **Review hypothesis** - Validate assumptions about EMA crossover effectiveness
2. **Backtest**: `/backtest HYP-001` - Run initial backtest with locked parameters
3. **Revise**: `/algo-strategy --revise "add RSI filter above 50"` - Refine strategy
4. **Optimize**: After validation, unlock parameters for optimization
