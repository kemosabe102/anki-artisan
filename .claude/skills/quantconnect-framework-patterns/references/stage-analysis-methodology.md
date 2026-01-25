# Stage Analysis Methodology

*Example alpha implementation using Stan Weinstein's 4-stage model.*

---

## Stage Classification Overview

Stocks cycle through 4 stages. Trade Stage 2 (uptrend), avoid Stage 4 (decline).

| Stage | Name | Characteristics | Action |
|-------|------|-----------------|--------|
| **1** | Basing | Consolidation, ADX < 20 | Watch |
| **2** | Uptrend | EMA aligned, ADX > 20 rising | **BUY** |
| **3** | Distribution | Momentum fading, volume divergence | Exit |
| **4** | Decline | Downtrend, ADX > 20 falling | Avoid |

---

## Stage Decision Tree

```
┌─ Is EMA20 > EMA50 > EMA200?
│  ├─ YES + ADX > 20 + +DI > -DI? → STAGE 2 (BUY)
│  └─ NO → Continue
│
├─ Is ADX < 20 + Price near MA ± 10%?
│  ├─ YES → STAGE 1 (WATCH)
│  └─ NO → Continue
│
├─ Is ADX < 25 + Distribution days ≥ 3?
│  ├─ YES → STAGE 3 (EXIT)
│  └─ NO → Continue
│
└─ Is EMA20 < EMA50 < EMA200 + -DI > +DI?
   ├─ YES → STAGE 4 (AVOID)
   └─ NO → UNKNOWN (WAIT)
```

---

## Indicator Requirements

| Indicator | Period | Stage 1 | Stage 2 | Stage 3 | Stage 4 |
|-----------|--------|---------|---------|---------|---------|
| **ADX** | 14 | <20 | >20↑ | <25↓ | >20↑ |
| **+DI** | 14 | ≈-DI | >-DI | Weak | <-DI |
| **EMA20** | 20 | ≈EMA50 | >EMA50 | →EMA50 | <EMA50 |
| **EMA50** | 50 | ≈EMA200 | >EMA200 | Weak | <EMA200 |
| **RSI** | 14 | 40-60 | 50-70 | 60-80 | 30-50 |

---

## StageMachine Implementation

```python
class StageMachine:
    """Deterministic stage classifier."""
    
    def classify(self, symbol_data):
        adx = symbol_data.ADX.Current.Value
        rsi = symbol_data.RSI.Current.Value
        price = symbol_data.Price
        ema20 = symbol_data.EMA20.Current.Value
        ema50 = symbol_data.EMA50.Current.Value
        ema200 = symbol_data.EMA200.Current.Value
        
        # Stage 2: Strong uptrend
        if (price > ema20 > ema50 > ema200 and
            adx > 25 and 50 < rsi < 70):
            return Stage.STAGE_2
        
        # Stage 4: Downtrend
        elif (price < ema20 < ema50 < ema200 and
              adx > 25 and rsi < 50):
            return Stage.STAGE_4
        
        # Stage 1: Basing
        elif adx < 20 and price > ema200:
            return Stage.STAGE_1
        
        # Stage 3: Distribution
        else:
            return Stage.STAGE_3

class Stage:
    STAGE_1 = 1  # Basing
    STAGE_2 = 2  # Uptrend (buy)
    STAGE_3 = 3  # Distribution
    STAGE_4 = 4  # Decline (avoid)
```

---

## Persistent State Tracking

Track per-symbol state to enable hysteresis and analytics:

```python
self.symbol_stages = {
    'AAPL': {
        'stage': 2,
        'entered_date': datetime(...),
        'entry_price': 150.00,
        'stop_loss': 145.50,
        'target': 165.00,
        'confidence': 85
    }
}
```

### Why Track State
1. **Hysteresis**: Prevent rapid stage flipping on noise
2. **Entry details**: Know where you entered, stop/target levels
3. **Analytics**: Track win rate by stage type

---

## Hysteresis Protocol

Prevent whipsaws by requiring confirmation:

```python
days_in_stage = (today - stage_entered_date).days

# Require 3+ days in new stage before reverting
if days_in_stage < 3:
    return current_stage  # Don't flip back
```

| Day | Condition | Action |
|-----|-----------|--------|
| 1 | Stage 2 triggered | Enter Stage 2 |
| 2 | Stage 3 conditions appear | Stay Stage 2 (< 3 days) |
| 3 | Stage 3 confirmed again | Now flip to Stage 3 |
| 4-5 | Stage 2 re-appears | Require 3+ days in Stage 3 |

---

## Regime Overlay

Position sizing multiplier based on market volatility:

```python
def update_regime(self):
    spy_vol = self.calculate_spy_volatility(30)  # Annualized
    
    if spy_vol < 0.15:
        self.regime_multiplier = 1.25  # Trending: size up
    elif spy_vol < 0.20:
        self.regime_multiplier = 1.0   # Normal
    elif spy_vol < 0.30:
        self.regime_multiplier = 0.75  # Elevated: reduce
    else:
        self.regime_multiplier = 0.0   # Panic: NO ENTRIES
```

### Position Sizing Formula
```
Position_Size = Base_Risk × Regime_Multiplier × Entry_Modifier

Example:
2% × 0.75 (elevated) × 0.9 (Stage 2 momentum) = 1.35% risk
```

---

## Wrapping as AlphaModel

```python
class StageMachineAlphaModel(AlphaModel):
    def __init__(self):
        self.stage_machine = StageMachine()
        self.symbol_data = {}
    
    def Update(self, algorithm, data):
        insights = []
        
        for symbol in algorithm.ActiveSecurities.Keys:
            if symbol not in self.symbol_data:
                self.symbol_data[symbol] = SymbolData(symbol, algorithm)
            
            sd = self.symbol_data[symbol]
            sd.Update(data[symbol])
            
            if not sd.IsReady():
                continue
            
            stage = self.stage_machine.classify(sd)
            
            if stage == Stage.STAGE_2:
                insights.append(Insight.Price(
                    symbol,
                    timedelta(days=5),
                    InsightDirection.Up,
                    confidence=0.8))
            
            elif stage == Stage.STAGE_4:
                insights.append(Insight.Price(
                    symbol,
                    timedelta(days=5),
                    InsightDirection.Down,
                    confidence=0.6))
        
        return insights
```

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Stage 2 win rate | ≥ 60% |
| Stage 1 win rate | ≥ 55% |
| Average win | +3% |
| Average loss | -2% |
| Sharpe ratio | > 1.0 |
| Max drawdown | < 20% |
