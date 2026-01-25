# Algorithm Iteration Decision Framework
## How to Know What to Work On Next

**Use this to make decisions about what to improve in your algorithm**

---

## THE ITERATION CYCLE

```
Current State → Measure → Analyze → Decide → Implement → Test → Repeat
```

---

## STEP 1: MEASURE YOUR ALGORITHM

Run a backtest and collect metrics:

```python
backtest_metrics = {
    # Trade Statistics
    "total_trades": 45,
    "win_rate": 0.45,
    "avg_win": 450,
    "avg_loss": -380,
    
    # Portfolio Performance
    "total_return": 0.25,
    "annual_return": 0.08,
    "sharpe_ratio": 0.95,
    "max_drawdown": -0.18,
    
    # Risk Metrics
    "avg_trade_duration": 12,
    "largest_consecutive_losses": 3,
    "profit_factor": 1.2,
}
```

---

## STEP 2: ANALYZE YOUR RESULTS

### Ask These Questions

1. **Is the algorithm profitable?**
   - Total Return > 0? If yes, moving in right direction

2. **Is the risk acceptable?**
   - Max Drawdown < 25%? If yes, good

3. **Is there enough sample size?**
   - Trades > 50? If yes, enough data

4. **What's the biggest problem?**
   - Low win rate (< 40%)? → Entry signals weak
   - High drawdown (> 25%)? → Risk management failing
   - Low Sharpe (< 1.0)? → Returns not worth the risk
   - No trades? → Entry conditions too strict

---

## STEP 3: IDENTIFY THE BOTTLENECK

Use this decision tree:

```
Algorithm produces trades?
├─ NO: Entry signals never triggered
│   └─ Action: Loosen entry conditions (add ADX, relax RSI)
│
└─ YES: Getting trades ✓
    │
    │ Win rate > 40%?
    │ ├─ NO: Too many losing trades
    │ │   └─ Action: Improve entry signal quality
    │ │       (add confirmations, improve indicators)
    │ │
    │ └─ YES: ✓ Win rate OK
    │     │
    │     │ Sharpe ratio > 1.0?
    │     │ ├─ NO: Risk too high for returns
    │     │ │   └─ Action: Improve risk management
    │     │ │       (tighter stops, fewer positions)
    │     │ │
    │     │ └─ YES: ✓ Risk-adjusted return OK
    │         │
    │         │ Max drawdown < 25%?
    │         │ ├─ NO: Getting too much loss
    │         │ │   └─ Action: Add circuit breaker
    │         │ │       or position sizing limits
    │         │ │
    │         │ └─ YES: ✓ Algorithm working!
    │             └─ Action: Paper trade or optimize
```

---

## STEP 4: DECIDE WHAT TO FIX

### Priority Matrix: Impact vs Effort

```
              EFFORT (Time to implement)
              Low         Medium       High
IMPACT   High │ DO NOW  │ DO NEXT  │ PLAN   │
(Effect on   ├─────────┼──────────┼────────┤
Results)    Med │ DO NEXT │ MAYBE   │ DEFER  │
             ├─────────┼──────────┼────────┤
            Low │ DEFER   │ DEFER    │ NO     │


Quick Wins (Low Effort, High Impact):
1. Add losing trade logging - see why trades fail (2h)
2. Tighten stops - reduce largest losses (4h)
3. Add position limit - reduce drawdown (3h)
4. Add ADX filter - filter weak trends (4h)

Medium Effort (1-2 days):
5. Implement regime detection (8h)
6. Add circuit breaker (6h)
7. Improve position sizing (8h)
8. Add profit target exits (4h)

Hard Stuff (1+ weeks):
9. New indicator development
10. Complex risk metrics
11. Multi-factor entry signals
12. Advanced order logic
```

---

## COMMON PROBLEMS & SOLUTIONS

### Problem 1: NO TRADES

**Symptoms**:
- Backtest shows 0-5 trades for 1 year
- Entries never triggered

**Root Causes** (in order of likelihood):
1. Indicator not ready (IsReady check missing)
2. Entry conditions too strict
3. Universe filtered out all stocks
4. Market conditions don't match signal

**Quick Fix**:
```python
# Add logging to each entry condition
self.Debug(f"EMA20 ready: {self.ema20.IsReady}")
self.Debug(f"EMA20 > EMA50: {ema20} > {ema50}")
self.Debug(f"ADX ready: {self.adx.IsReady}")
self.Debug(f"ADX > 20: {adx} > 20")

# Loosen filters if needed
# MIN_ADX = 15  (was 20)
# MAX_RSI = 75  (was 70)
```

**Time to Fix**: 2-4 hours

---

### Problem 2: LOW WIN RATE (< 40%)

**Symptoms**:
- Getting many trades
- Too many losses
- Win rate 25-35%

**Root Causes**:
1. Entry signal weak (too many false signals)
2. Exits happening too early
3. Wrong market conditions for strategy
4. Stops too tight (good trades stopped out)

**Quick Fix**:
```python
# Add confirming indicator
# Was: Just EMA alignment
# Now: EMA alignment + ADX > 20 + RSI not extreme

# OR widen stops
# Was: Entry - 1.0*ATR
# Now: Entry - 1.5*ATR

# Log each signal with criteria met
self.Log(f"[SIGNAL] {symbol} | EMA OK: Y | ADX OK: {adx > 20} | RSI OK: Y")
```

**Time to Fix**: 4-8 hours

---

### Problem 3: HIGH DRAWDOWN (> 25%)

**Symptoms**:
- Max drawdown of 30-40%
- Can't tolerate the swings
- Risk too high for return

**Root Causes**:
1. Position sizing too aggressive
2. Stops too far away
3. No circuit breaker
4. Consecutive losses hitting hard

**Quick Fix**:
```python
# Add circuit breaker
if daily_loss > portfolio * 0.03:  # 3% daily loss
    skip_entries = True

# Tighten stops
# Was: Entry - 2.0*ATR
# Now: Entry - 1.5*ATR

# Reduce position size
# Was: Risk 2% per trade
# Now: Risk 1% per trade
```

**Time to Fix**: 4-6 hours

---

### Problem 4: LIVE WORSE THAN BACKTEST

**Symptoms**:
- Backtest: 2.0 Sharpe, 50% win rate
- Live: 0.5 Sharpe, 35% win rate

**Root Causes** (90% of the time):
1. Overfitting (parameters only worked for backtest period)
2. Look-ahead bias (using future data)
3. Slippage not accounted for
4. Universe changed (trading different stocks)

**Quick Fix**:
```python
# Run walk-forward test
# Train on 2020-2021, test on 2022
# Train on 2021-2022, test on 2023
# Do results hold up? If not = overfitting

# Widen stops by 10-20%
# Smaller positions by 20%
# More conservative entries

# Never optimize parameters
# Use logical defaults instead
```

**Time to Fix**: 8-16 hours of analysis + recalibration

---

## ITERATION PLANNING TEMPLATE

### For Each 1-2 Week Sprint

```
SPRINT GOAL: [Pick ONE focus area]
├─ Improve win rate from 35% → 45%
├─ Reduce max drawdown from 28% → 20%
├─ Increase # of trades from 20 → 50
├─ Validate strategy holds in 2022
└─ Make algorithm production-ready

METRICS TO TRACK:
├─ Win rate before: ___%
├─ Win rate target: ___%
├─ Max DD before: ___%
├─ Max DD target: ___%
└─ Trade count: ___

WHAT I'LL CHANGE:
├─ Change #1: Add ADX filter
├─ Change #2: Tighten stop from 2x to 1.5x ATR
├─ Change #3: Reduce position size from 2% to 1% risk
└─ NOT Changing: Entry signal logic

EXPECTED IMPACT:
├─ Win rate should go to: 40%
├─ Max DD should drop to: 22%
└─ Trade count should stay: ~35

HOW I'LL MEASURE SUCCESS:
├─ Win rate > 40%? YES = Sprint success
├─ Max DD < 22%? YES = Sprint success
├─ No new crashes? YES = Sprint success
└─ Live test profitable? YES = Ready for real money

ROLLBACK PLAN:
If changes make things worse:
├─ Revert ADX filter
├─ Go back to 2x ATR stops
├─ Increase position size back to 2%
```

---

## DECISION TREE: WHEN TO MOVE TO LIVE

```
Ready for live trading?
│
├─ Backtest results good?
│  ├─ Win rate > 40%?
│  ├─ Sharpe ratio > 1.0?
│  ├─ Max drawdown < 25%?
│  └─ All YES? ✓ Continue...
│
├─ Validated robustness?
│  ├─ Walk-forward test OK?
│  ├─ Out-of-sample test OK?
│  ├─ Different symbols tested?
│  └─ All YES? ✓ Continue...
│
├─ Observability ready?
│  ├─ All entries logged?
│  ├─ All exits logged?
│  ├─ Charts working?
│  └─ All YES? ✓ Continue...
│
├─ Paper traded 2-4 weeks?
│  ├─ Results similar to backtest?
│  ├─ No major surprises?
│  ├─ Fills within slippage estimate?
│  └─ All YES? ✓ Continue...
│
└─ READY FOR LIVE ✓
   │
   ├─ Start with small position (10% of capital)
   ├─ Monitor closely first month
   ├─ Scale up only if consistent
   └─ Have emergency stop plan
```

---

## METRICS AT EACH STAGE

### Stage 1: Initial Development
```
MINIMUM ACCEPTABLE:
├─ Win rate > 30% (better than coin flip)
├─ Sharpe ratio > 0.5 (some quality returns)
├─ Max drawdown < 40% (not bankrupt)
├─ Trades > 20 (enough sample)
└─ No crashes (runs to completion)

GOAL: Get something working, prove concept
```

### Stage 2: Refinement
```
MINIMUM ACCEPTABLE:
├─ Win rate > 40% (clearly profitable)
├─ Sharpe ratio > 1.0 (good risk-adjusted)
├─ Max drawdown < 25% (manageable)
├─ Profit factor > 1.2 (wins > losses)
└─ Trades > 50 (good sample size)

GOAL: Improve signal quality and risk management
```

### Stage 3: Validation
```
MINIMUM ACCEPTABLE:
├─ Walk-forward: Sharpe > 0.8 (holds up)
├─ Out-of-sample: Win rate > 35% (generalizes)
├─ Stress test: Survives crashes
├─ Different symbols: Works on others too
└─ No look-ahead bias (confirmed)

GOAL: Prove strategy is robust, not lucky
```

### Stage 4: Production Ready
```
MINIMUM ACCEPTABLE:
├─ Paper trading results: ±10% of backtest
├─ All observability working
├─ Risk limits enforced
├─ Logging complete
├─ Emergency procedures documented
└─ 2-4 weeks paper testing completed

GOAL: Safe to deploy real capital
```

---

## 30-SECOND DECISION MAKER

```
Current backtest:
- 35 trades, 38% win rate, 0.8 Sharpe, 22% max DD

Decision: What to do next?

WIN RATE is limiting factor (38% close to 40%)
→ Solution: Add ADX filter to entry signals
→ Expected: Win rate → 42%, Sharpe → 1.1
→ Effort: 4 hours
→ Risk: Low (can always revert)
→ Action: Code it and test

→ If it works: Move to next problem
→ If it doesn't: Revert and try different approach
```

---

## DON'T GET STUCK IN ANALYSIS PARALYSIS

**After you've measured and diagnosed:**
- Pick ONE thing to improve
- Implement it (4-8 hours max)
- Test it (run backtest)
- Did it help? YES → Keep it
- Did it help? NO → Revert
- Move on to next thing

**Don't:**
- Spend weeks researching perfect solution
- Implement 5 things at once
- Tweak parameters endlessly
- Wait for "perfect" backtest

**Timeline:**
- 1 hour to diagnose problem
- 4-8 hours to implement fix
- 1-2 hours to test
- Total: 1 sprint = 1 improvement

**Iterate**: After each sprint, go back to Step 1

Good luck! 🚀
