# QuantConnect Development Guide
## Iteration, Common Issues, Troubleshooting & Best Practices

**Date**: January 2, 2026  
**Purpose**: Help you avoid common pitfalls and accelerate algorithm development

---

## TABLE OF CONTENTS

1. [Development Workflow](#development-workflow)
2. [Common Pitfalls & How to Avoid](#common-pitfalls--how-to-avoid)
3. [Debugging Strategies](#debugging-strategies)
4. [Data Quality & Validation](#data-quality--validation)
5. [Backtesting Biases](#backtesting-biases)
6. [Performance Optimization](#performance-optimization)
7. [Troubleshooting FAQ](#troubleshooting-faq)
8. [Testing Checklist](#testing-checklist)

---

## DEVELOPMENT WORKFLOW

### Phase 1: Design (Pre-Code)
**Time**: 4-8 hours
**Goal**: Clear specification before coding

- [ ] Define entry criteria with mathematical precision
- [ ] Define exit criteria (profit target, stop loss, time-based)
- [ ] Identify failure cases (what could go wrong?)
- [ ] Sketch indicator timing (which indicators, periods)
- [ ] Document assumptions (market efficiency, liquidity, fees)
- [ ] Estimate expected outcomes (win rate %, avg P&L)

**Deliverable**: 1-2 page design document

---

### Phase 2: MVP (Minimal Viable Algorithm)
**Time**: 20-30 hours
**Goal**: Core logic working end-to-end

Start with SIMPLEST possible version:

**Deliverable**: Algorithm that backtests without errors

---

### Phase 3: Refinement (Iterations)
**Time**: 40-60 hours
**Goal**: Improve signal quality, add risk controls

Iterate through these improvements:

1. **Signal Refinement** (Week 1)
   - Add indicators to improve entries
   - Test different parameter combinations
   - Measure signal accuracy (wins vs losses)

2. **Risk Management** (Week 2)
   - Implement regime detection (VIX multiplier)
   - Add circuit breaker logic
   - Test drawdown management

3. **Observability** (Week 2)
   - Add logging, charting, metrics
   - Validate each trade decision
   - Track P&L attribution

4. **Optimization** (Week 3)
   - Parameter optimization (careful!)
   - Walk-forward testing
   - Out-of-sample validation

---

### Phase 4: Validation (Pre-Live)
**Time**: 20-30 hours
**Goal**: Confidence in backtest results

- [ ] Backtest on original time period
- [ ] Walk-forward test (train on 2020-2021, test 2022)
- [ ] Out-of-sample test (train on 2022, test 2023)
- [ ] Stress test (market crashes, volatility spikes)
- [ ] Paper trading (live data, simulated orders)
- [ ] Risk assessment (max drawdown, Sharpe ratio acceptable?)

---

## COMMON PITFALLS & HOW TO AVOID

### ❌ PITFALL #1: Look-Ahead Bias

**What it is**: Using future information in past analysis

**Example - WRONG**:
```python
def OnData(self, data):
    current_price = data[symbol].Close  # OK
    
    # WRONG - using TOMORROW's data today:
    tomorrow_price = self.History(symbol, 1, Resolution.Daily)[symbol].Close
```

**How to detect**:
- Backtest results way too good (>50% win rate, Sharpe > 3)
- Live trading results much worse than backtest
- Performance degrades sharply after backtest period

**How to fix**:
- ✅ Only use data available at current time
- ✅ Use `OnData()` with bars as they arrive (no future lookups)
- ✅ If using History(), request data BEFORE current time
- ✅ Always lag indicators by 1 bar minimum
- ✅ For daily data, make decisions AFTER close
- ✅ For minute data, make decisions same bar (OK if bar is closed)

---

### ❌ PITFALL #2: Survivorship Bias

**What it is**: Backtest using only stocks that exist today, ignoring delisted ones

**How to detect**:
- Backtest improves over time (survivorship getting better)
- Results include stocks that crashed/delisted during period
- Live trading returns worse than backtest (dead stocks killed you)

**How to fix**:
- ✅ Use point-in-time universe (constituents as they were then)
- ✅ QuantConnect provides this: `UniverseSettings.Asynchronous = False`
- ✅ Only include stocks that existed at that date (filtered coarse universe)
- ✅ Test on diverse time periods (crashes, bull markets, bear markets)

---

### ❌ PITFALL #3: Data Quality Issues

**What it is**: Bad data ruins backtest results

**Examples**:
- Extreme price movements (splits not adjusted)
- Missing bars (gaps in data)
- Incorrect timestamps
- Corporate actions not adjusted (splits, dividends)

**How to fix**:
- ✅ QuantConnect handles splits/dividends automatically (adjusted close)
- ✅ BUT: Check for "Adjusted Close" vs "Raw Close"
- ✅ Verify data quality by comparing 2-3 charts
- ✅ For custom data: Validate before using
- ✅ Check Data Issues tab in QuantConnect

---

### ❌ PITFALL #4: Indicator Not Ready

**What it is**: Using indicator before it has enough data

**Example - WRONG**:
```python
self.ema200 = EMA(200)
self.RegisterIndicator(symbol, self.ema200, Resolution.Daily)

# Day 50: EMA200 not ready yet!
if self.ema200.Current.Value > 100:  # Crash if None!
    pass
```

**How to fix**:
```python
# CORRECT - check if ready before using
if self.ema200.IsReady:
    if self.ema200.Current.Value > 100:
        pass
else:
    return  # Skip this bar
```

---

### ❌ PITFALL #5: Overfitting / Curve Fitting

**What it is**: Optimizing parameters too much to past data

**Example - WRONG**:
```python
# Tested 10,000 parameter combinations
# Found: EMA=73, RSI=62, ADX=18 works best on 2020-2022
# Backtest: 75% win rate!
# Live: 15% win rate (parameters only worked for that specific period)
```

**How to fix**:
- ✅ Limit parameter combinations (test 10-20, not 10,000)
- ✅ Use round numbers (20, 50, not 73)
- ✅ Use walk-forward testing (train on Period A, test on Period B, repeat)
- ✅ Use out-of-sample testing (train 2020-2021, test 2022-2023)
- ✅ Manual parameter selection based on logic, not optimization

---

### ❌ PITFALL #6: Universe Selection Too Broad

**What it is**: Trading illiquid stocks causes slippage and failures

**How to fix**:
```python
# CORRECT - filter for liquidity
def CoarseSelectionFunction(self, coarse):
    return [
        c for c in coarse
        if c.Price >= 10
        and c.Volume * c.Price >= 10e6  # At least $10M volume
    ][:100]  # Limit to 100 stocks max
```

---

### ❌ PITFALL #7: Incorrect Position Sizing

**What it is**: Risking wrong amount per trade

**Example - WRONG**:
```python
# Every trade: 100 shares regardless of price
# Stock A: $50 → $5,000 risk (2% portfolio)
# Stock B: $500 → $50,000 risk (50% portfolio!)
```

**How to fix**:
```python
# CORRECT - size based on portfolio value
def CalculatePositionSize(self, symbol, risk_per_trade=0.01):
    """Size position to risk only X% of portfolio per trade"""
    portfolio_value = self.Portfolio.TotalPortfolioValue
    risk_amount = portfolio_value * risk_per_trade
    
    stop_distance = self.Securities[symbol].ATR * 1.5
    shares = int(risk_amount / stop_distance)
    
    return shares
```

---

### ❌ PITFALL #8: No Warm-Up Period

**What it is**: Using indicators before they're ready

**How to fix**:
```python
# In Initialize()
self.SetWarmupPeriod(250)  # Skip first 250 bars
```

---

## DEBUGGING STRATEGIES

### Strategy 1: Log-Based Debugging

**When to use**: Most common - see what algorithm is doing

```python
# Add strategic logging throughout algorithm

# In stage_alpha_model.py:
def Update(self, algorithm, data) -> List[Insight]:
    insights = []
    
    for symbol, indicators in self._indicators.items():
        if symbol not in data.Bars:
            continue
        
        snapshot = self._build_snapshot(symbol, data)
        current_stage = self._classify_stage(snapshot)
        
        # DEBUG: Log every stage transition
        if current_stage != self._prev_stage.get(symbol, Stage.UNKNOWN):
            algorithm.Debug(
                f"[STAGE] {symbol}: Stage {self._prev_stage.get(symbol, 0)} → "
                f"Stage {current_stage} | Price={snapshot.price:.2f} ADX={snapshot.adx:.1f}"
            )
        
        self._prev_stage[symbol] = current_stage

# In main.py:
def OnOrderEvent(self, order_event: OrderEvent):
    if order_event.Status == OrderStatus.Filled:
        self.Log(
            f"[FILL] {order_event.Symbol} | {order_event.Direction} | "
            f"Qty={order_event.Quantity} | Price={order_event.FillPrice:.2f}"
        )
```

---

### Strategy 2: Assertion-Based Debugging

**When to use**: Verify assumptions are true

```python
def _build_snapshot(self, symbol: str, data: Slice):
    """Build snapshot with validation"""
    
    bar = data[symbol]
    
    # Assert data is valid
    assert bar.Close > 0, f"{symbol} price <= 0"
    assert bar.High >= bar.Low, f"{symbol} high < low"
    assert bar.Volume >= 0, f"{symbol} negative volume"
    
    # Assert indicators are ready
    indicators = self._indicators[symbol]
    assert indicators["ema20"].IsReady, f"{symbol} EMA20 not ready"
```

---

### Strategy 3: Charting for Visual Debugging

**When to use**: See trends, validate logic

```python
def OnEndOfDay(self, symbol: Symbol):
    for symbol in self.Portfolio:
        pos = self.Portfolio[symbol]
        if pos.Invested:
            self.Plot(f"Debug_{symbol}", "Quantity", pos.Quantity)
            self.Plot(f"Debug_{symbol}", "UnrealizedProfit", pos.UnrealizedProfit)
```

---

### Strategy 4: Reduced Universe Testing

**When to use**: Isolate problems to specific symbols

```python
# Test with just 1-2 symbols to debug faster

def Initialize(self):
    self.debug_symbols = ["AAPL", "MSFT"]  # Test just these
    
    if self.debug_mode:
        self.AddUniverse(self.SelectDebugUniverse)
    else:
        self.AddUniverse(self.SelectFullUniverse)

def SelectDebugUniverse(self, coarse):
    return self.debug_symbols  # Just 2 stocks
```

**Benefits**:
- Backtest runs in seconds (not minutes)
- Easier to see what each symbol is doing
- Can trace each decision

---

## DATA QUALITY & VALIDATION

### Validation Checklist

```python
def validate_data(self, symbol, data):
    """Validate OHLCV data quality"""
    
    bar = data[symbol]
    issues = []
    
    # Price checks
    if bar.Close <= 0:
        issues.append(f"Invalid close: {bar.Close}")
    if bar.High < bar.Low:
        issues.append(f"High < Low: {bar.High} < {bar.Low}")
    if bar.Close > bar.High or bar.Close < bar.Low:
        issues.append(f"Close outside High/Low range")
    
    # Volume checks
    if bar.Volume < 0:
        issues.append(f"Negative volume: {bar.Volume}")
    if bar.Volume == 0:
        issues.append(f"Zero volume (no trading)")
    
    # Extreme movement checks
    prev_close = self.Securities[symbol].Price
    pct_change = abs((bar.Close - prev_close) / prev_close)
    if pct_change > 0.50:
        issues.append(f"Extreme move: {pct_change:.1%}")
    
    if issues:
        self.Log(f"[DATA_ISSUE] {symbol}: {'; '.join(issues)}")
        return False
    
    return True
```

---

## BACKTESTING BIASES

### Bias #1: Look-Ahead Bias
**How to avoid**: Use only current/past data, not future
**Check**: Are results way too good?

### Bias #2: Survivorship Bias
**How to avoid**: Use point-in-time universe, include delisted stocks
**Check**: Do results improve over time?

### Bias #3: Optimization Bias
**How to avoid**: Don't optimize parameters, use round numbers
**Check**: Do live results match backtest?

### Bias #4: Data Snooping Bias
**How to avoid**: Test on out-of-sample period
**Check**: Walk-forward test (train 2020, test 2021, train 2021, test 2022)

### Testing Methodology

```python
# CORRECT: Walk-forward testing

# Train on Period 1, test on Period 2
SetStartDate(2020, 1, 1)
SetEndDate(2021, 12, 31)  # Train on 2020-2021
backtest_1_result = Run()

# Now test on fresh data
SetStartDate(2022, 1, 1)
SetEndDate(2023, 12, 31)  # Test on 2022-2023
backtest_2_result = Run()

# Did results hold up out-of-sample?
if backtest_2_result.SharpeRatio > 1.5:
    print("Strategy likely robust")
else:
    print("Strategy only worked on train period - likely overfit")
```

---

## PERFORMANCE OPTIMIZATION

### Identify Bottlenecks

```python
# Common Performance Issues

| Issue | Symptom | Fix |
|-------|---------|-----|
| Too many symbols | Backtest takes >10 min | Reduce universe to <50 stocks |
| History() calls | Each call is 1-2 seconds | Don't call History() in OnData |
| Indicator updates | Hundreds of indicators | Limit to < 20 per symbol |
| Loop operations | Nested loops in OnData | Pre-compute in Initialize |
| Inefficient data access | Frequent dictionary lookups | Cache results |
```

### Optimization Best Practices

```python
# BAD - called every bar
def OnData(self, data):
    history = self.History(symbol, 250, Resolution.Daily)  # 1-2 second delay!
    ma200 = history.Close.mean()

# GOOD - computed once during setup
def Initialize(self):
    self.ema200 = EMA(200)
    self.RegisterIndicator(symbol, self.ema200)

def OnData(self, data):
    ma200 = self.ema200.Current.Value  # Instant
```

---

## TROUBLESHOOTING FAQ

### Q: "NoneType cannot be compared with float"

**Cause**: Indicator not ready yet

**Fix**:
```python
if not self.indicator.IsReady:
    return

if self.indicator.Current.Value > 100:  # Now safe
    pass
```

---

### Q: Indicator values look wrong

**Cause**: Different calculation method or warming period

**Fix**:
```python
# Verify calculation manually
# Compare to 2-3 external sources
# If still different: might be correct (different SMA method)

# Use QuantConnect indicator (most common)
self.sma = SimpleMovingAverage(20)
```

---

### Q: Backtest runs but results are 0 (no trades)

**Cause**: Entry conditions never met

**Debug**:
```python
def OnData(self, data):
    self.Log(f"EMA20 ready: {self.ema20.IsReady}")
    self.Log(f"EMA20: {self.ema20.Current.Value}")
    self.Log(f"EMA50: {self.ema50.Current.Value}")
    
    if self.ema20.IsReady and self.ema20.Current.Value > self.ema50.Current.Value:
        self.Log(f"Entry condition MET for {symbol}!")
```

---

### Q: Live trading performance much worse than backtest

**Causes**:
- Look-ahead bias
- Survivorship bias
- Overfitting
- Slippage not accounted for
- Universe changed

**Fix**:
```python
# Compare backtest vs live
backtest_sharpe = 1.8
live_sharpe = 0.5

# Red flag! Investigate:
# 1. Run backtest on recent period (2024)
# 2. Compare to live results from same period
# 3. If backtest > live: likely overfitting or slippage

# Recalibrate with:
# - Wider stops
# - More conservative entry signals
# - Smaller position sizes
```

---

### Q: "Insufficient buying power" errors

**Cause**: Trying to buy more shares than capital allows

**Fix**:
```python
# Size positions correctly
def CalculateQuantity(self, symbol):
    portfolio_value = self.Portfolio.TotalPortfolioValue
    
    # Risk only 1% per trade
    risk_amount = portfolio_value * 0.01
    
    # Determine stop distance
    stop_distance = self.Securities[symbol].Price * 0.02
    
    # Calculate shares
    shares = int(risk_amount / stop_distance)
    
    # Verify buying power
    cost = shares * self.Securities[symbol].Price
    if cost > self.Portfolio.GetBuyingPower():
        shares = int(self.Portfolio.GetBuyingPower() / self.Securities[symbol].Price)
    
    return shares
```

---

### Q: Algorithm is too slow (>10 min per backtest)

**Cause**: Too much computation per bar

**Fix**:
```python
# Profile to find bottleneck
# Typical issues:
# - Universe selection too broad (>100 stocks)
# - Calling History() in OnData
# - Too many indicators per stock
# - Complex calculations on every bar

# Solutions:
# 1. Reduce universe
self.AddUniverse(lambda coarse: [c for c in coarse if c.Price > 5][:50])

# 2. Don't call History in OnData
# Use RegisterIndicator instead

# 3. Pre-compute complex logic
def Initialize(self):
    self._complex_calc = self.ComputeOnce()

def OnData(self, data):
    result = self._complex_calc  # Just lookup
```

---

## TESTING CHECKLIST

Before deploying to live trading:

### Data Validation
- [ ] Compare backtest prices to external sources (Yahoo, TradingView)
- [ ] Check for gaps in data (missing dates)
- [ ] Verify OHLCV ranges make sense
- [ ] Check for extreme outliers (likely data errors)

### Backtest Validation
- [ ] Initial backtest on 3+ years of data
- [ ] Walk-forward test (train period separate from test)
- [ ] Out-of-sample test (completely fresh data)
- [ ] Stress test (crash period like 2008 or 2020)
- [ ] Different symbol sets (test universality)

### Logic Validation
- [ ] Every entry logged with criteria met
- [ ] Every exit logged with reason
- [ ] Position sizes verified (risk <= 2% per trade)
- [ ] No look-ahead bias (only current data used)
- [ ] All indicators ready before use

### Metrics Validation
- [ ] Win rate > 40% (at least break-even on trades)
- [ ] Average trade > 0 (positive expectancy)
- [ ] Sharpe ratio > 1.0 (acceptable risk-adjusted return)
- [ ] Max drawdown < 25% (risk management working)
- [ ] Number of trades > 50 (enough sample size)

### Risk Validation
- [ ] Max positions limit enforced
- [ ] Stop losses placed on all entries
- [ ] Profit targets defined
- [ ] Circuit breaker active
- [ ] Portfolio heat tracked
- [ ] Margin never exceeded

### Observability Validation
- [ ] All entries/exits logged
- [ ] Charts update daily
- [ ] Metrics tracked (win rate, P&L, etc.)
- [ ] Object Store working (state persistence)
- [ ] Live dashboard shows expected data

### Live Trading Validation (Paper Trading First!)
- [ ] Run paper trading 1-4 weeks
- [ ] Results within 80% of backtest Sharpe ratio
- [ ] No crashes or errors
- [ ] Fills within expected slippage
- [ ] Position sizing correct
- [ ] Risk limits working

---

## ITERATION TEMPLATE

### Week 1: MVP
```
Day 1-2: Design
  Entry criteria (Stage 2)
  Exit criteria (ATR-based)
  Risk limits (10% portfolio heat)

Day 3-4: Core Algorithm
  Universe selection (top 100 liquid)
  Alpha model (EMA 20/50/200)
  Basic position sizing
  First backtest

Deliverable: 1-year backtest, 20+ trades, no crashes
```

### Week 2: Refinement
```
Day 1-2: Signal Quality
  Add ADX filter (trend strength)
  Add RSI filter (overbought/oversold)
  Tune hysteresis (prevent whipsaws)
  Measure win rate improvement

Day 3-4: Risk Management
  Implement regime detection (VIX)
  Add circuit breaker
  Implement portfolio heat tracking
  Test drawdown reduction

Deliverable: Win rate >50%, Sharpe > 1.0
```

### Week 3: Validation
```
Day 1-2: Bias Testing
  Walk-forward test (2 periods)
  Out-of-sample test (fresh period)
  Stress test (market crash period)
  Parameter sensitivity

Day 3-4: Observability
  Full logging/charting
  Trade tracking
  Risk monitoring
  Post-backtest analysis

Deliverable: Confidence in strategy robustness
```

### Week 4: Pre-Live
```
Day 1-2: Paper Trading
  2-4 weeks live data simulation
  Compare to backtest
  Verify fills/slippage
  Check for surprises

Day 3-4: Production Setup
  Final parameter review
  Document assumptions
  Set up alerts
  Plan live monitoring

Deliverable: Live trading ready
```

---

## SUMMARY

**Before Coding**: Design algorithm clearly (4-8h)

**During Development**:
- Start with MVP (20-30h)
- Iterate through improvements (40-60h)
- Add observability (20h)
- Validate thoroughly (20-30h)

**Common Pitfalls to Avoid**:
1. Look-ahead bias (use only current data)
2. Survivorship bias (include delisted stocks)
3. Data quality issues (validate inputs)
4. Indicators not ready (check IsReady)
5. Overfitting (don't optimize, use round numbers)
6. Universe too broad (limit to liquid stocks)
7. Wrong position sizing (risk-based sizing)
8. No warm-up (set warm-up period)

**Debugging Approach**:
1. Log everything (use tags for filtering)
2. Validate data (compare to external sources)
3. Test in parts (isolate to 1-2 symbols)
4. Chart intermediate values (visual debugging)
5. Assert assumptions (catch bugs early)

**Before Going Live**:
- ✅ Data validated
- ✅ Backtest robust (walk-forward tested)
- ✅ Biases addressed
- ✅ Observability complete
- ✅ Paper traded 2-4 weeks
- ✅ Ready for production
