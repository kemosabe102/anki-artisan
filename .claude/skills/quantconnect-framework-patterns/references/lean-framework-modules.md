# LEAN Framework Modules

*Detailed patterns for each of the 5 pluggable modules in QuantConnect's LEAN Algorithm Framework.*

---

## 1. Universe Selection Module

**Purpose**: Define which securities your algorithm trades.

### Pre-Built Models
| Model | Use Case |
|-------|----------|
| `FundamentalUniverseSelectionModel` | Filter by fundamentals |
| `ManualUniverseSelectionModel` | Fixed symbol list |
| `ScheduledUniverseSelectionModel` | Time-based rebalancing |

### Implementation Pattern
```python
def Initialize(self):
    self.UniverseSettings.Resolution = Resolution.Daily
    self.AddUniverse(self.CoarseFilter, self.FineFilter)

def CoarseFilter(self, coarse):
    # First pass: liquidity
    return [x.Symbol for x in coarse
            if x.Price > 5 and x.DollarVolume > 1e6][:500]

def FineFilter(self, fine):
    # Second pass: fundamentals
    return [f.Symbol for f in fine
            if f.CompanyReference.MarketCap > 1e9
            and f.ValuationRatios.PERatio < 40][:100]
```

---

## 2. Alpha Model

**Purpose**: Generate trading signals (Insights).

### Insight Object Structure
```python
Insight.Price(
    symbol,                    # Security
    timedelta(days=5),         # Prediction horizon
    InsightDirection.Up,       # Up/Down/Flat
    magnitude=0.05,            # Expected move (5%)
    confidence=0.8             # Signal confidence
)
```

### Custom AlphaModel Pattern
```python
class MyAlphaModel(AlphaModel):
    def __init__(self):
        self.symbol_data = {}
    
    def Update(self, algorithm, data):
        insights = []
        
        for symbol in algorithm.ActiveSecurities.Keys:
            if not data.ContainsKey(symbol):
                continue
            
            # Your signal logic here
            if self.is_bullish(symbol):
                insights.append(Insight.Price(
                    symbol,
                    timedelta(days=5),
                    InsightDirection.Up,
                    confidence=0.8))
        
        return insights
```

### Registration
```python
def Initialize(self):
    self.AddAlpha(MyAlphaModel())
```

---

## 3. Portfolio Construction Model

**Purpose**: Convert Insights into position targets (sizing).

### Pre-Built Optimizers
| Optimizer | Strategy |
|-----------|----------|
| `MaximumSharpeRatioPortfolioOptimizer` | Maximize risk-adjusted return |
| `MinimumVariancePortfolioOptimizer` | Minimize volatility |
| `EqualWeightingPortfolioConstructionModel` | Equal allocation |
| `InsightWeightingPortfolioConstructionModel` | Weight by confidence |

### Implementation Pattern
```python
def Initialize(self):
    # Option 1: Equal weighting
    self.SetPortfolioConstruction(
        EqualWeightingPortfolioConstructionModel())
    
    # Option 2: Insight-weighted
    self.SetPortfolioConstruction(
        InsightWeightingPortfolioConstructionModel(
            resolution=Resolution.Daily))
    
    # Option 3: Optimization-based
    optimizer = MaximumSharpeRatioPortfolioOptimizer(
        minimum_weight=-0.05,  # Allow 5% short
        maximum_weight=0.10)   # Max 10% per position
    
    self.SetPortfolioConstruction(
        MeanVarianceOptimizationPortfolioConstructionModel(
            optimizer=optimizer))
```

### Position Constraints
- `minimum_weight`: Floor per position (negative = shorts allowed)
- `maximum_weight`: Ceiling per position
- `rebalancing_func`: When to rebalance

---

## 4. Risk Management Model

**Purpose**: Protect portfolio from excessive losses.

### Pre-Built Models
| Model | Protection |
|-------|------------|
| `MaximumDrawdownPercentPerSecurity` | Per-position loss limit |
| `MaximumDrawdownPercentPortfolio` | Total portfolio loss limit |
| `TrailingStopRiskManagementModel` | Dynamic trailing stop |
| `MaximumSectorExposureRiskManagementModel` | Sector concentration |

### Implementation Pattern
```python
def Initialize(self):
    # Per-position: 5% max loss
    self.AddRiskManagement(
        MaximumDrawdownPercentPerSecurity(0.05))
    
    # Portfolio: 10% max loss
    self.AddRiskManagement(
        MaximumDrawdownPercentPortfolio(0.10))
    
    # Trailing stop: 10%
    self.AddRiskManagement(
        TrailingStopRiskManagementModel(0.10))
```

### Composite Risk
Multiple risk models can be stacked—first triggered wins.

---

## 5. Execution Model

**Purpose**: Convert targets into orders efficiently.

### Pre-Built Models
| Model | Strategy |
|-------|----------|
| `ImmediateExecutionModel` | Market orders immediately |
| `VolumeWeightedAveragePriceExecutionModel` | Split by volume (VWAP) |
| `StandardDeviationExecutionModel` | Volatility-based timing |

### Implementation Pattern
```python
def Initialize(self):
    # Simple: immediate fill
    self.SetExecution(ImmediateExecutionModel())
    
    # Advanced: VWAP execution
    self.SetExecution(
        VolumeWeightedAveragePriceExecutionModel())
```

### When to Use Each
| Scenario | Model |
|----------|-------|
| Small positions, liquid stocks | `ImmediateExecutionModel` |
| Large positions, minimize impact | `VolumeWeightedAveragePriceExecutionModel` |
| Volatile markets | `StandardDeviationExecutionModel` |

---

## Complete Framework Setup

```python
class FrameworkAlgorithm(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2020, 1, 1)
        self.SetCash(100000)
        
        # 1. Universe
        self.AddUniverse(self.CoarseFilter, self.FineFilter)
        
        # 2. Alpha (YOUR CODE)
        self.AddAlpha(MyAlphaModel())
        
        # 3. Portfolio Construction
        self.SetPortfolioConstruction(
            InsightWeightingPortfolioConstructionModel())
        
        # 4. Risk Management
        self.AddRiskManagement(
            MaximumDrawdownPercentPerSecurity(0.05))
        
        # 5. Execution
        self.SetExecution(
            VolumeWeightedAveragePriceExecutionModel())
        
        self.SetWarmUp(250)
```

**Result**: OnData() is eliminated—framework handles the entire flow.
