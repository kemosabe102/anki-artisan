# Memory Optimization Patterns

*Code examples for reducing QuantConnect algorithm memory footprint.*

---

## Pattern 1: RollingWindow vs History()

### Problem

`History()` allocates a new DataFrame on each call, causing memory churn.

### Anti-Pattern (High Memory)

```python
def OnData(self, data):
    # BAD: Allocates new DataFrame every bar
    history = self.History(self.symbol, 20, Resolution.Daily)
    sma = history['close'].mean()
```

### Optimized Pattern (Low Memory)

```python
def Initialize(self):
    self.close_window = RollingWindow[float](20)
    
def OnData(self, data):
    if self.symbol in data.Bars:
        self.close_window.Add(data.Bars[self.symbol].Close)
        
    if self.close_window.IsReady:
        # GOOD: Fixed memory allocation, O(1) updates
        sma = sum(self.close_window) / self.close_window.Count
```

### Memory Savings

| Approach | Memory Per Symbol | For 500 Symbols |
|----------|-------------------|-----------------|
| `History()` per bar | ~2 MB (repeated allocation) | 1 GB churn/bar |
| `RollingWindow` | ~2 KB (fixed) | 1 MB total |

---


## Pattern 2: Universe Size Limiting with CoarseFundamental

### Problem

Unfiltered universes subscribe to 8000+ securities.

### Anti-Pattern (High Memory)

```python
def Initialize(self):
    # BAD: No filtering, subscribes to entire universe
    self.AddUniverse(self.CoarseSelectionFunction)
    
def CoarseSelectionFunction(self, coarse):
    return [x.Symbol for x in coarse]  # 8000+ symbols!
```

### Optimized Pattern (Low Memory)

```python
def Initialize(self):
    self.UniverseSettings.Resolution = Resolution.Daily  # Not Minute!
    self.AddUniverse(self.CoarseSelectionFunction)
    
def CoarseSelectionFunction(self, coarse):
    # GOOD: Filter by liquidity and price
    filtered = [x for x in coarse 
                if x.HasFundamentalData 
                and x.Price > 10 
                and x.DollarVolume > 1000000]
    
    # GOOD: Limit universe size
    sorted_by_volume = sorted(filtered, 
                              key=lambda x: x.DollarVolume, 
                              reverse=True)
    return [x.Symbol for x in sorted_by_volume[:100]]  # Max 100 symbols
```

### Memory Savings

| Universe Size | Daily Resolution | Minute Resolution |
|---------------|------------------|-------------------|
| 8000 (unfiltered) | 64 GB | 512 GB |
| 500 (filtered) | 4 GB | 32 GB |
| 100 (optimized) | 0.8 GB | 6.4 GB |

---


## Pattern 3: Options Chain Filtering with SetFilter

### Problem

Wide strike/expiry ranges load thousands of contracts.

### Anti-Pattern (High Memory)

```python
def Initialize(self):
    option = self.AddOption("SPY")
    # BAD: Massive chain - 10,000+ contracts
    option.SetFilter(-50, 50, timedelta(-180), timedelta(180))
```

### Optimized Pattern (Low Memory)

```python
def Initialize(self):
    option = self.AddOption("SPY")
    # GOOD: Focused chain - ~80 contracts
    option.SetFilter(-5, 5, timedelta(0), timedelta(30))
    
# For dynamic filtering based on strategy needs:
def Initialize(self):
    option = self.AddOption("SPY")
    option.SetFilter(self.OptionFilterFunction)
    
def OptionFilterFunction(self, universe):
    # GOOD: Only ATM options expiring in 2-4 weeks
    return universe.Strikes(-2, 2) \
                   .Expiration(timedelta(14), timedelta(30)) \
                   .IncludeWeeklys()
```

### Memory Savings

| Filter | Contracts | Memory |
|--------|-----------|--------|
| `(-50, 50, -180, 180)` | ~10,000 | 5 GB |
| `(-10, 10, 0, 60)` | ~336 | 168 MB |
| `(-5, 5, 0, 30)` | ~80 | 40 MB |
| `(-2, 2, 14, 30)` | ~20 | 10 MB |

---


## Pattern 4: Subscription Cleanup with RemoveSecurity

### Problem

Universe rotations accumulate zombie subscriptions.

### Anti-Pattern (High Memory)

```python
def OnSecuritiesChanged(self, changes):
    for security in changes.AddedSecurities:
        self.active_symbols.append(security.Symbol)
    # BAD: Never removes securities - memory grows forever
```

### Optimized Pattern (Low Memory)

```python
def OnSecuritiesChanged(self, changes):
    for security in changes.AddedSecurities:
        self.active_symbols.append(security.Symbol)
        
    for security in changes.RemovedSecurities:
        if security.Symbol in self.active_symbols:
            self.active_symbols.remove(security.Symbol)
        # GOOD: Clean up subscription
        self.RemoveSecurity(security.Symbol)
```

### Scheduled Cleanup

```python
def Initialize(self):
    # Monthly cleanup of stale subscriptions
    self.Schedule.On(
        self.DateRules.MonthStart(),
        self.TimeRules.AfterMarketOpen("SPY", 30),
        self.CleanupSubscriptions
    )
    
def CleanupSubscriptions(self):
    for symbol in list(self.Securities.Keys):
        if symbol not in self.active_symbols:
            self.RemoveSecurity(symbol)
```

---


## Pattern 5: Object Store for Disk Offload

### Problem

Large cached datasets consume memory throughout backtest.

### Anti-Pattern (High Memory)

```python
def Initialize(self):
    # BAD: 500MB DataFrame held in memory entire backtest
    self.fundamentals_cache = self.load_fundamentals()
```

### Optimized Pattern (Low Memory)

```python
def Initialize(self):
    # GOOD: Store large data in Object Store, load on demand
    if not self.ObjectStore.ContainsKey("fundamentals"):
        data = self.load_fundamentals()
        self.ObjectStore.SaveBytes("fundamentals", pickle.dumps(data))
    
def OnData(self, data):
    # Load only when needed, can be garbage collected
    if self.need_fundamentals:
        fundamentals = pickle.loads(
            self.ObjectStore.ReadBytes("fundamentals")
        )
        self.process_fundamentals(fundamentals)
        del fundamentals  # Explicit cleanup
```

### When to Use Object Store

| Data Size | Frequency of Access | Recommendation |
|-----------|---------------------|----------------|
| < 10 MB | Every bar | Keep in memory |
| 10-100 MB | Daily | Object Store + cache |
| > 100 MB | Weekly/Monthly | Object Store only |

---

## Optimization Decision Tree

```
START
  │
  ├─ Universe > 500 symbols?
  │   └─ YES → Apply Pattern 2 (CoarseFundamental filters)
  │
  ├─ Using History() in OnData?
  │   └─ YES → Apply Pattern 1 (RollingWindow)
  │
  ├─ Trading options?
  │   └─ YES → Apply Pattern 3 (SetFilter optimization)
  │
  ├─ Universe rotates monthly?
  │   └─ YES → Apply Pattern 4 (RemoveSecurity)
  │
  └─ Large static datasets?
      └─ YES → Apply Pattern 5 (Object Store)
```

