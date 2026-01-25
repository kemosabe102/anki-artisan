---
title: QC Memory Optimization Guide
date: 2025-01-16
status: ACTIVE
tags: [backtester, memory, quantconnect]
---

# QC Memory Optimization Guide

**Purpose**: Comprehensive reference for estimating memory requirements and optimizing QuantConnect backtests to avoid out-of-memory failures.

---

## Section 1: Memory Estimation Fundamentals

### Base Memory Formula

```
Total Memory = Σ (Asset Memory × Resolution Multiplier × History Factor)
```

### Per-Asset Base Memory

| Asset Type | Base Memory | Notes |
|------------|-------------|-------|
| Equity | 5-10 MB | Single ticker, daily resolution |
| Forex | 3-5 MB | Currency pair |
| Futures | 8-15 MB | Single contract |
| Options | 15-30 MB | Per underlying × chain depth |
| Crypto | 5-10 MB | Single pair |


### Resolution Multipliers

| Resolution | Multiplier | Bars/Day (Equity) | Use Case |
|------------|------------|-------------------|----------|
| Daily | 1x | 1 | Screening, portfolio rebalance |
| Hour | 2.5x | 7 | Swing trading |
| Minute | 8x | 390 | Intraday execution |
| Second | 50x | 23,400 | High-frequency |
| Tick | 200x | Variable | Full order book |

### History Factor

```
History Memory = 2 MB/year/asset × Resolution Factor
```

| Resolution | History Factor | 10Y Single Stock |
|------------|----------------|------------------|
| Daily | 1x | 20 MB |
| Minute | 8x | 160 MB |
| Second | 50x | 1 GB |

### Example Calculation

```python
# 100 stocks, minute resolution, 5 years history
base_memory = 100 * 7.5  # avg 7.5 MB per stock
resolution_mult = 8      # minute
history = 100 * 2 * 5 * 8  # 2 MB/year × 5 years × resolution factor

total = base_memory + history  # ~8.75 GB estimated
```


---

## Section 2: Universe Sizing Strategies

### Coarse Universe Filter Pattern

```python
def CoarseSelectionFunction(self, coarse):
    # Stage 1: Basic filters (fast, reduces search space)
    filtered = [x for x in coarse 
                if x.Price > 5 
                and x.DollarVolume > 10_000_000
                and x.HasFundamentalData]
    
    # Stage 2: Sort and cap
    sorted_stocks = sorted(filtered, 
                           key=lambda x: x.DollarVolume, 
                           reverse=True)
    
    return [x.Symbol for x in sorted_stocks[:self.universe_size]]
```

### Hard Caps by Resolution

| Resolution | Max Universe | Reason |
|------------|--------------|--------|
| Daily | 2000-5000 | Low memory per asset |
| Hour | 500-1000 | Moderate multiplier |
| Minute | 200-500 | 8x multiplier |
| Second | 50-100 | 50x multiplier |
| Tick | 10-20 | Extreme memory |


### Two-Stage Selection Pattern

```python
class TwoStageUniverse(QCAlgorithm):
    def Initialize(self):
        self.coarse_size = 500  # First pass
        self.fine_size = 100    # Final portfolio
        self.AddUniverse(self.CoarseFilter, self.FineFilter)
    
    def CoarseFilter(self, coarse):
        """Stage 1: Price/volume filters (cheap)"""
        return [x.Symbol for x in sorted(
            [c for c in coarse if c.Price > 5 and c.DollarVolume > 1e6],
            key=lambda x: x.DollarVolume, reverse=True
        )[:self.coarse_size]]
    
    def FineFilter(self, fine):
        """Stage 2: Fundamental filters (expensive)"""
        return [x.Symbol for x in sorted(
            [f for f in fine if f.ValuationRatios.PERatio > 0],
            key=lambda x: x.MarketCap, reverse=True
        )[:self.fine_size]]
```

> **Anti-Pattern**: Subscribing to 1000+ minute-resolution assets. Memory will exceed 16GB and backtest will fail.

---

## Section 3: Resolution Selection

### Resolution Trade-offs

| Resolution | Pros | Cons | Best For |
|------------|------|------|----------|
| Daily | Accurate closes, low memory, fast backtests | Miss intraday moves, fill timing imprecise | Portfolio screening, monthly rebalance |
| Hour | Balance accuracy/memory | Still misses quick moves | Swing strategies (2-5 day holds) |
| Minute | Accurate fills, entry/exit timing | 8x memory, slower backtests | Intraday, execution-sensitive |
| Second | Precise execution | 50x memory, very slow | High-frequency |
| Tick | Full order book | Extreme memory | Market microstructure |


### Resolution Selection Decision Tree

```
IF strategy rebalances weekly+ 
   → Resolution.Daily

ELIF strategy needs intraday entry/exit timing
   → Resolution.Minute

ELIF strategy is HFT or market-making
   → Resolution.Second or Tick
   → WARN: Requires L1 or L2 node

ELSE
   → Resolution.Daily (default safest)
```

### Mixed Resolution Pattern

```python
def Initialize(self):
    # Daily for screening universe
    self.AddUniverse(self.CoarseFilter, Resolution.Daily)
    
    # Minute only for active positions
    self.SetSecurityInitializer(lambda security: 
        security.SetDataNormalizationMode(DataNormalizationMode.Adjusted))
    
def OnSecuritiesChanged(self, changes):
    for security in changes.AddedSecurities:
        # Upgrade to minute when entering position
        if self.ShouldTrade(security.Symbol):
            self.AddEquity(security.Symbol, Resolution.Minute)
```

---

## Section 4: History() and Warmup Patterns

### RollingWindow Pattern (Preferred)

```python
class EfficientHistory(QCAlgorithm):
    def Initialize(self):
        self.lookback = 20
        self.windows = {}
        
    def OnSecuritiesChanged(self, changes):
        for security in changes.AddedSecurities:
            # Initialize rolling window once
            self.windows[security.Symbol] = RollingWindow[TradeBar](self.lookback)
            # Warmup with history
            history = self.History(security.Symbol, self.lookback, Resolution.Daily)
            for bar in history.itertuples():
                self.windows[security.Symbol].Add(TradeBar(...))
    
    def OnData(self, data):
        for symbol, window in self.windows.items():
            if symbol in data.Bars:
                window.Add(data.Bars[symbol])  # O(1) update
```


### WarmUpIndicator Pattern

```python
class IndicatorWarmup(QCAlgorithm):
    def Initialize(self):
        self.SetWarmUp(50, Resolution.Daily)  # Framework handles warmup
        self.sma = {}
        
    def OnSecuritiesChanged(self, changes):
        for security in changes.AddedSecurities:
            self.sma[security.Symbol] = self.SMA(security.Symbol, 20, Resolution.Daily)
            # Indicator auto-warms during SetWarmUp period
    
    def OnData(self, data):
        if self.IsWarmingUp:
            return  # Framework populates indicators
        
        for symbol, indicator in self.sma.items():
            if indicator.IsReady:
                # Use indicator value
                pass
```

> **Anti-Pattern**: Calling `History()` on every bar to recalculate. This creates massive memory churn.

```python
# BAD - O(n) memory allocation per bar
def OnData(self, data):
    for symbol in self.Securities.Keys:
        history = self.History(symbol, 20, Resolution.Daily)  # AVOID
        sma = history['close'].mean()

# GOOD - O(1) update
def OnData(self, data):
    for symbol, window in self.windows.items():
        if symbol in data.Bars:
            window.Add(data.Bars[symbol])
            sma = sum([w.Close for w in window]) / len(window)
```


---

## Section 5: Options Chain Optimization

### OptionChainProvider Pattern

```python
class EfficientOptions(QCAlgorithm):
    def Initialize(self):
        self.equity = self.AddEquity("SPY", Resolution.Minute)
        # Don't subscribe to full chain
        # self.AddOption("SPY")  # AVOID - subscribes to ALL contracts
        
    def OnData(self, data):
        # Query chain on-demand
        contracts = self.OptionChainProvider.GetOptionContractList(
            self.equity.Symbol, self.Time
        )
        
        # Filter before subscribing
        filtered = [c for c in contracts 
                    if abs(c.ID.StrikePrice - self.equity.Price) < 10
                    and (c.ID.Date - self.Time).days < 30]
        
        # Subscribe only to needed contracts
        for contract in filtered[:5]:
            self.AddOptionContract(contract, Resolution.Minute)
```

### SetFilter Pattern

```python
def Initialize(self):
    option = self.AddOption("SPY", Resolution.Minute)
    
    # Filter chain at subscription time
    option.SetFilter(
        minStrike=-5,      # 5 strikes below ATM
        maxStrike=5,       # 5 strikes above ATM
        minExpiry=timedelta(days=7),
        maxExpiry=timedelta(days=45)
    )
```


### Options Memory Estimation

| Chain Depth | Contracts | Memory Estimate |
|-------------|-----------|-----------------|
| Narrow (±3 strikes, 2 expiries) | ~24 | 50-100 MB |
| Medium (±5 strikes, 4 expiries) | ~80 | 200-400 MB |
| Wide (±10 strikes, 8 expiries) | ~320 | 800 MB - 1.5 GB |
| Full chain | 500+ | 2-5 GB |

> **Anti-Pattern**: Using `AddOption()` without `SetFilter()`. This subscribes to the entire options chain (500+ contracts per underlying).

---

## Section 6: Collection Management

### Extract Only Needed Values

```python
# BAD - stores full TradeBar objects
class BadCollection(QCAlgorithm):
    def Initialize(self):
        self.all_bars = []  # Will grow indefinitely
    
    def OnData(self, data):
        for symbol in data.Bars.Keys:
            self.all_bars.append(data.Bars[symbol])  # Full object retained

# GOOD - extract only needed values
class GoodCollection(QCAlgorithm):
    def Initialize(self):
        self.price_history = {}  # Symbol -> list of (time, close)
    
    def OnData(self, data):
        for symbol, bar in data.Bars.items():
            if symbol not in self.price_history:
                self.price_history[symbol] = []
            # Store only what's needed
            self.price_history[symbol].append((bar.EndTime, bar.Close))
            # Cap history length
            if len(self.price_history[symbol]) > 252:
                self.price_history[symbol].pop(0)
```


### Python Explicit Cleanup

```python
def OnSecuritiesChanged(self, changes):
    for security in changes.RemovedSecurities:
        symbol = security.Symbol
        
        # Explicit cleanup
        if symbol in self.windows:
            del self.windows[symbol]
        if symbol in self.indicators:
            del self.indicators[symbol]
        if symbol in self.price_history:
            del self.price_history[symbol]
```

### Avoiding Long-Lived Objects

| Object Type | Retain? | Alternative |
|-------------|---------|-------------|
| Full Slice | NEVER | Extract needed symbols |
| TradeBar | Only in RollingWindow | Store (time, OHLCV) tuple |
| OptionChain | NEVER | Query OptionChainProvider |
| DataFrame (full) | NEVER | Store aggregated metrics |

> **Anti-Pattern**: Storing `self.slice = data` or appending `Slice` objects to a list. Each `Slice` contains ALL subscribed data.

---

## Section 7: Subscription Management

### RemoveSecurity Pattern

```python
def OnSecuritiesChanged(self, changes):
    for security in changes.RemovedSecurities:
        # Clean up algorithm state
        symbol = security.Symbol
        if symbol in self.signals:
            del self.signals[symbol]
        
        # Explicitly remove if needed
        self.RemoveSecurity(symbol)
```


### Custom Data Cleanup

```python
class CustomDataCleanup(QCAlgorithm):
    def Initialize(self):
        self.custom_data = {}
        
    def OnData(self, data):
        for symbol in list(self.custom_data.keys()):
            if symbol not in self.ActiveSecurities:
                del self.custom_data[symbol]
                self.Debug(f"Cleaned up {symbol}")
```

### Security Changed Events Handling

```python
def OnSecuritiesChanged(self, changes):
    # Added securities - initialize state
    for security in changes.AddedSecurities:
        self.InitializeSecurityState(security.Symbol)
    
    # Removed securities - cleanup state
    for security in changes.RemovedSecurities:
        self.CleanupSecurityState(security.Symbol)
        
def CleanupSecurityState(self, symbol):
    """Centralized cleanup for all security-related state"""
    cleanup_targets = [
        self.windows, self.indicators, self.signals,
        self.positions, self.pending_orders
    ]
    for target in cleanup_targets:
        if symbol in target:
            del target[symbol]
```

---

## Section 8: Results and Logging Limits

### Plot Quotas

| Metric | Limit | Impact |
|--------|-------|--------|
| Charts | 10 total | Per backtest |
| Series per chart | 10 | Per chart |
| Data points | ~4000 per series | Total across backtest |
| Updates/second | 2 | Rate limited |


### Efficient Plotting

```python
def OnData(self, data):
    # BAD - plots every bar
    self.Plot("Signals", "SMA", self.sma.Current.Value)
    
    # GOOD - sample at lower frequency
    if self.Time.hour == 16 and self.Time.minute == 0:
        self.Plot("Signals", "SMA", self.sma.Current.Value)
```

### Logging Rate Limits

| Log Type | Limit | Recommendation |
|----------|-------|----------------|
| Debug() | 10,000/backtest | Use sparingly |
| Log() | 10,000/backtest | Key events only |
| Total lines | ~100,000 | Aggregate messages |
| Result size | ~700 MB | Minimize plot data |

### Efficient Logging

```python
def OnData(self, data):
    # BAD - logs every bar
    self.Debug(f"Processing {self.Time}")
    
    # GOOD - log daily summary
    if self.Time.hour == 16 and self.Time.minute == 0:
        self.Log(f"EOD {self.Time.date()}: Portfolio={self.Portfolio.TotalPortfolioValue:.2f}")
    
    # GOOD - log only significant events
    if abs(signal) > self.threshold:
        self.Log(f"SIGNAL: {symbol} = {signal:.4f}")
```


> **Anti-Pattern**: Using `self.Debug()` or `self.Log()` inside `OnData()` without rate limiting. A 10-year minute backtest = ~9.8M bars = exceeded quota.

---

## Section 9: Python-Specific Considerations

### pandas DataFrame Overhead

```python
# BAD - DataFrame for small operations
def OnData(self, data):
    prices = pd.DataFrame({s: [d.Close] for s, d in data.Bars.items()})
    mean = prices.mean()  # Massive overhead for simple calc

# GOOD - use native Python
def OnData(self, data):
    closes = [d.Close for d in data.Bars.values()]
    mean = sum(closes) / len(closes)
```

### NumPy Array Efficiency

```python
# Use NumPy for large numerical operations
import numpy as np

class NumpyEfficient(QCAlgorithm):
    def Initialize(self):
        self.returns = {}  # Symbol -> np.array
        
    def UpdateReturns(self, symbol, price):
        if symbol not in self.returns:
            self.returns[symbol] = np.zeros(252)  # Pre-allocate
            self.returns_idx = {symbol: 0}
        
        idx = self.returns_idx[symbol]
        if idx > 0:
            self.returns[symbol][idx % 252] = price / self.last_price[symbol] - 1
        self.returns_idx[symbol] = idx + 1
```


### Python GC Hints

```python
import gc

class GCOptimized(QCAlgorithm):
    def Initialize(self):
        self.gc_interval = 1000  # Bars between GC
        self.bar_count = 0
        
    def OnData(self, data):
        self.bar_count += 1
        
        if self.bar_count % self.gc_interval == 0:
            collected = gc.collect()
            self.Debug(f"GC collected {collected} objects")
```

### Memory-Efficient Data Structures

| Task | Avoid | Use Instead |
|------|-------|-------------|
| Price tracking | list of floats | collections.deque(maxlen=N) |
| Symbol lookup | list iteration | dict or set |
| Sorted data | sorted() repeatedly | heapq or bisect |
| Large arrays | Python list | numpy.ndarray |

---

## Section 10: Node Sizing Guidance

### Memory Decision Matrix

| Estimated Memory | Node | RAM | Action |
|------------------|------|-----|--------|
| < 4 GB | S1 | 8 GB | PROCEED |
| 4-8 GB | S2 | 16 GB | WARN_MEDIUM |
| 8-16 GB | L1 | 32 GB | WARN_HIGH |
| > 16 GB | L2 | 64 GB | WARN_CRITICAL |
| > 32 GB | Optimize | - | MUST_OPTIMIZE |


### Node Selection Logic

```python
def estimate_node(universe_size: int, resolution: str, history_years: int, has_options: bool) -> dict:
    """Estimate memory and recommend node"""
    
    resolution_mult = {
        "daily": 1, "hour": 2.5, "minute": 8, "second": 50, "tick": 200
    }[resolution.lower()]
    
    base_mb = universe_size * 7.5  # avg per asset
    history_mb = universe_size * 2 * history_years * resolution_mult
    options_mb = 500 if has_options else 0  # per underlying
    
    total_gb = (base_mb + history_mb + options_mb) / 1024
    
    if total_gb < 4:
        return {"node": "S1", "action": "PROCEED", "memory_gb": total_gb}
    elif total_gb < 8:
        return {"node": "S2", "action": "WARN_MEDIUM", "memory_gb": total_gb}
    elif total_gb < 16:
        return {"node": "L1", "action": "WARN_HIGH", "memory_gb": total_gb}
    elif total_gb < 32:
        return {"node": "L2", "action": "WARN_CRITICAL", "memory_gb": total_gb}
    else:
        return {"node": "OPTIMIZE", "action": "MUST_OPTIMIZE", "memory_gb": total_gb}
```

### Optimization Strategies by Warning Level

| Warning Level | Primary Action | Secondary Action |
|---------------|----------------|------------------|
| PROCEED | None required | - |
| WARN_MEDIUM | Reduce universe by 25% | Lower resolution |
| WARN_HIGH | Reduce universe by 50% | Switch to daily |
| WARN_CRITICAL | Multi-pass backtest | Universe segmentation |
| MUST_OPTIMIZE | Complete redesign | Streaming approach |


---

## Section 11: Object Store for Disk Persistence

### Fundamentals

| Aspect | Details |
|--------|---------|
| Storage Type | Key-value store |
| Max Object Size | 50 MB |
| Scope | Organization-wide |
| Access Speed | Local network in backtests (fast), slower in live |
| Persistence | Survives algorithm restarts |

### When to Use Object Store

| Use Case | Object Store | Logs/Debug |
|----------|--------------|------------|
| Trade records | YES | NO |
| Model weights | YES | NO |
| State snapshots | YES | NO |
| Debug messages | NO | YES |
| Streaming data | NO | YES |

### Basic Operations

```python
# Save data
self.ObjectStore.Save("my_key", "string_data")
self.ObjectStore.SaveBytes("binary_key", bytes_data)
self.ObjectStore.SaveJson("json_key", {"data": [1, 2, 3]})

# Read data
data = self.ObjectStore.Read("my_key")
binary = self.ObjectStore.ReadBytes("binary_key")
obj = self.ObjectStore.ReadJson("json_key")

# Check existence
if self.ObjectStore.ContainsKey("my_key"):
    data = self.ObjectStore.Read("my_key")

# Delete
self.ObjectStore.Delete("my_key")
```


### Key Prefixing for Collision Prevention

```python
class ObjectStoreOrganized(QCAlgorithm):
    def Initialize(self):
        # Use project ID as prefix to prevent collisions
        self.store_prefix = f"{self.ProjectId}"
        
    def SaveTrades(self, trades):
        key = f"{self.store_prefix}/trades"
        self.ObjectStore.SaveJson(key, trades)
        
    def SaveSnapshot(self, snapshot_data):
        key = f"{self.store_prefix}/snapshots/{self.Time.strftime('%Y%m%d')}"
        self.ObjectStore.SaveJson(key, snapshot_data)
        
    def LoadTrades(self):
        key = f"{self.store_prefix}/trades"
        if self.ObjectStore.ContainsKey(key):
            return self.ObjectStore.ReadJson(key)
        return []
```

### Cache Management

```python
def Initialize(self):
    # Clear stale data when sharing storage between projects
    if self.GetParameter("clear_cache") == "true":
        keys_to_clear = [
            f"{self.ProjectId}/trades",
            f"{self.ProjectId}/snapshots"
        ]
        for key in keys_to_clear:
            if self.ObjectStore.ContainsKey(key):
                self.ObjectStore.Delete(key)
                self.Debug(f"Cleared cache: {key}")
```


### Large Data Compression

```python
import gzip
import json

class CompressedStorage(QCAlgorithm):
    def SaveCompressed(self, key, data):
        """Save large data with gzip compression"""
        json_str = json.dumps(data)
        compressed = gzip.compress(json_str.encode('utf-8'))
        self.ObjectStore.SaveBytes(f"{key}.gz", compressed)
        
    def LoadCompressed(self, key):
        """Load gzip-compressed data"""
        if self.ObjectStore.ContainsKey(f"{key}.gz"):
            compressed = self.ObjectStore.ReadBytes(f"{key}.gz")
            json_str = gzip.decompress(compressed).decode('utf-8')
            return json.loads(json_str)
        return None
```

> **Anti-Pattern**: Saving to Object Store on every bar. Save once at end or at scheduled intervals.

---

## Section 12: Trade Recording Best Practices

### Accumulate-Then-Save Pattern

```python
class TradeRecorder(QCAlgorithm):
    def Initialize(self):
        self.trades = []  # Accumulate in memory
        
    def OnOrderEvent(self, order_event):
        if order_event.Status == OrderStatus.Filled:
            self.trades.append({
                "time": str(order_event.UtcTime),
                "symbol": str(order_event.Symbol),
                "quantity": order_event.FillQuantity,
                "price": order_event.FillPrice,
                "direction": "BUY" if order_event.FillQuantity > 0 else "SELL",
                "order_id": order_event.OrderId
            })
    
    def OnEndOfAlgorithm(self):
        # Save once at the end
        if self.trades:
            self.ObjectStore.SaveJson(f"{self.ProjectId}/trades", self.trades)
            self.Log(f"Saved {len(self.trades)} trades to Object Store")
```


### Serialization Formats

| Data Type | Format | Method |
|-----------|--------|--------|
| Trade records | JSON | SaveJson() |
| DataFrames | CSV | Save() with df.to_csv() |
| Large arrays | Compressed JSON | gzip + SaveBytes() |
| ML models | Pickle bytes | SaveBytes() |
| Binary data | Raw bytes | SaveBytes() |

### Periodic Snapshot Pattern

```python
class PeriodicSnapshot(QCAlgorithm):
    def Initialize(self):
        self.snapshots = []
        self.Schedule.On(
            self.DateRules.MonthEnd(),
            self.TimeRules.BeforeMarketClose("SPY", 5),
            self.SaveMonthlySnapshot
        )
        
    def SaveMonthlySnapshot(self):
        snapshot = {
            "date": str(self.Time.date()),
            "portfolio_value": self.Portfolio.TotalPortfolioValue,
            "holdings": {str(k): v.Quantity for k, v in self.Portfolio.items() if v.Invested}
        }
        self.snapshots.append(snapshot)
        
    def OnEndOfAlgorithm(self):
        self.ObjectStore.SaveJson(f"{self.ProjectId}/monthly_snapshots", self.snapshots)
```


### Research Notebook Retrieval

```python
# In QuantBook research environment
from QuantConnect import *
from QuantConnect.Research import QuantBook

qb = QuantBook()

# Retrieve trades from Object Store
project_id = 12345678  # Your project ID
trades = qb.ObjectStore.ReadJson(f"{project_id}/trades")

# Convert to DataFrame for analysis
import pandas as pd
df = pd.DataFrame(trades)
df['time'] = pd.to_datetime(df['time'])
df.set_index('time', inplace=True)

# Analyze
print(f"Total trades: {len(df)}")
print(f"Unique symbols: {df['symbol'].nunique()}")
print(df.groupby('direction')['quantity'].sum())
```

### Trade Recording Anti-Patterns

| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| Save per bar | I/O overhead, quota limits | Accumulate, save at end |
| Store full Slice | Massive memory growth | Extract only needed fields |
| Store TradeBar objects | Object overhead | Store (time, OHLCV) tuples |
| No key prefixing | Cross-project collisions | Use `{ProjectId}/key` pattern |
| No compression | 50MB limit hit faster | gzip for large data |


### Complete Trade Recording Example

```python
from AlgorithmImports import *
import json
import gzip

class CompleteTradeRecorder(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2020, 1, 1)
        self.SetEndDate(2024, 1, 1)
        self.SetCash(100000)
        
        self.AddEquity("SPY", Resolution.Daily)
        
        # Trade accumulator
        self.trades = []
        self.daily_equity = []
        
    def OnData(self, data):
        if not self.Portfolio.Invested:
            self.MarketOrder("SPY", 100)
            
    def OnOrderEvent(self, order_event):
        if order_event.Status == OrderStatus.Filled:
            self.trades.append({
                "time": str(order_event.UtcTime),
                "symbol": str(order_event.Symbol),
                "quantity": order_event.FillQuantity,
                "price": order_event.FillPrice,
                "fees": order_event.OrderFee.Value.Amount,
                "order_id": order_event.OrderId
            })
    
    def OnEndOfDay(self, symbol):
        # Daily equity curve (lightweight)
        self.daily_equity.append({
            "date": str(self.Time.date()),
            "equity": self.Portfolio.TotalPortfolioValue
        })
    
    def OnEndOfAlgorithm(self):
        prefix = f"{self.ProjectId}"
        
        # Save trades as JSON
        self.ObjectStore.SaveJson(f"{prefix}/trades", self.trades)
        self.Log(f"Saved {len(self.trades)} trades")
        
        # Save equity curve
        self.ObjectStore.SaveJson(f"{prefix}/equity_curve", self.daily_equity)
        self.Log(f"Saved {len(self.daily_equity)} equity points")
        
        # Save summary metrics
        summary = {
            "total_trades": len(self.trades),
            "final_equity": self.Portfolio.TotalPortfolioValue,
            "start_date": str(self.StartDate),
            "end_date": str(self.EndDate)
        }
        self.ObjectStore.SaveJson(f"{prefix}/summary", summary)

---

## Quick Reference: Memory Optimization Checklist


### Pre-Backtest Checklist

- [ ] Estimated memory < node RAM (with 50% buffer)
- [ ] Universe size within resolution limits
- [ ] Resolution matches strategy requirements (not over-specified)
- [ ] History/warmup uses RollingWindow pattern
- [ ] Options use SetFilter() or OptionChainProvider
- [ ] No unbounded collections (lists with no max length)
- [ ] Logging rate-limited (not per-bar)
- [ ] Plot count within quota (10 charts, 4000 points/series)

### During-Backtest Monitoring

- [ ] Watch memory usage in QC console
- [ ] Check for "memory pressure" warnings
- [ ] Monitor log line count

### Post-Backtest Validation

- [ ] Trades saved to Object Store
- [ ] Results retrieved successfully in Research
- [ ] No truncated data due to quotas

---

## Related Documentation

| Document | Purpose |
|----------|---------|
| [gate-thresholds.md](gate-thresholds.md) | Validation gate definitions |
| [../backtester.md](../backtester.md) | Main backtester agent reference |
| [../phases/phase-2-orient.md](../phases/phase-2-orient.md) | ORIENT phase with memory assessment |

