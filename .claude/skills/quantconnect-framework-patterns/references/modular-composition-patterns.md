# Modular Composition Patterns

*How professional quants compose systems from reusable parts instead of building everything custom.*

---

## Monolithic vs Modular Comparison

### Monolithic (Bad)
```python
def my_trading_strategy():
    # 500+ lines of intertwined logic:
    # - Get data
    # - Calculate indicators  
    # - Generate signals
    # - Size positions
    # - Manage risk
    # - Place orders
    # Everything tightly coupled
```

**Problems**:
- Hard to test individual components
- Can't swap implementations
- Bug in one area breaks everything
- Months to build

### Modular (Good)
```python
class TradingSystem:
    def __init__(self):
        self.data = DataModule()
        self.alpha = MyAlpha()       # ← Your edge
        self.portfolio = MaxSharpe() # ← Framework
        self.risk = RiskManager()    # ← Framework
        self.execution = VWAP()      # ← Framework
    
    def run(self):
        data = self.data.get_latest()
        signals = self.alpha.generate(data)
        targets = self.portfolio.construct(signals)
        targets = self.risk.filter(targets)
        self.execution.execute(targets)
```

**Benefits**:
- Test each module in isolation
- Swap implementations without breaking system
- Days to build (reuse infrastructure)
- Clear contracts between modules

---

## Interface-First Design

Define contracts BEFORE implementation:

```python
from abc import ABC, abstractmethod

class AlphaModel(ABC):
    """Every alpha MUST implement this interface."""
    
    @abstractmethod
    def generate_insights(self, data: pd.DataFrame) -> List[Insight]:
        """Generate trading insights from data."""
        pass
    
    @abstractmethod
    def get_required_features(self) -> List[str]:
        """Return required data features."""
        pass
```

### Why This Matters
- Any alpha implementing interface can plug into system
- Portfolio constructor doesn't care HOW signals are generated
- Swap alphas without changing anything else
- This IS the QuantConnect framework approach

---

## Dependency Injection Pattern

### Tight Coupling (Bad)
```python
class TradingStrategy:
    def __init__(self):
        self.data = YahooFinance()      # Hardcoded!
        self.optimizer = MVO()          # Hardcoded!
```

**Problem**: Can't test without real data, can't swap components.

### Loose Coupling (Good)
```python
class TradingStrategy:
    def __init__(self, data_source, optimizer):
        self.data = data_source   # Injected
        self.optimizer = optimizer # Injected

# Testing
strategy = TradingStrategy(
    data_source=MockData(),
    optimizer=TestOptimizer())

# Production
strategy = TradingStrategy(
    data_source=QCData(),
    optimizer=MaxSharpe())
```

**Benefit**: Test with mocks, run with real components.

---

## Configuration Over Code

### Hardcoded (Bad)
```python
class Strategy:
    ADX_THRESHOLD = 25
    MAX_POSITION = 0.10
    STOP_LOSS = 0.05
```

### Externalized (Good)
```yaml
# strategy_config.yaml
strategy:
  name: "StageMomentum"

alpha:
  type: "StageMachine"
  params:
    adx_threshold: 25
    rsi_bounds: [30, 70]

portfolio:
  type: "MaxSharpe"
  params:
    max_position: 0.10
    min_position: 0.01

risk:
  models:
    - type: "MaxDrawdown"
      params: { threshold: 0.05 }
    - type: "TrailingStop"
      params: { distance: 0.10 }
```

### Benefits
- Change parameters without code changes
- Version control configurations
- A/B test different configs
- Roll back quickly

---

## Research-Production Parity

### Bad Practice
```
Research: Jupyter notebooks
    ↓ (manual copy)
Production: Separate codebase
    ↓
Code diverges, bugs in translation
```

### Good Practice
```python
# research_notebook.ipynb
from quant_lib.alphas import MyAlpha
from quant_lib.backtest import BacktestEngine

alpha = MyAlpha(params={'threshold': 30})
engine = BacktestEngine(alpha=alpha)
results = engine.run('2020-01-01', '2024-12-31')

# production_system.py (SAME CODE)
from quant_lib.alphas import MyAlpha
from quant_lib.live import LiveTrading

alpha = MyAlpha(params={'threshold': 30})
system = LiveTrading(alpha=alpha)
system.run()
```

**Both use the SAME alpha implementation.**

---

## The "Write Less Code" Principle

### What's Proprietary vs Commodity

| Type | Your Code | Framework Handles |
|------|-----------|-------------------|
| **Alpha (signal)** | Yes - your edge | No |
| **Data loading** | No | Yes - solved problem |
| **Portfolio optimization** | No | Yes - solved problem |
| **Risk management** | No | Yes - solved problem |
| **Execution** | No | Yes - solved problem |

### Time Allocation
| Activity | Time |
|----------|------|
| Alpha research | 80% |
| Infrastructure | 20% |

---

## Pipeline Thinking

Think in data pipelines:

```
Raw Data → Clean → Features → Signals → Portfolio → Orders → Fills → P&L
   ↓         ↓        ↓         ↓          ↓          ↓        ↓       ↓
Module    Module   Module    Module     Module     Module   Module  Module
```

Each module:
1. Has **clear inputs and outputs**
2. Can be **tested independently**
3. Can be **swapped** without breaking pipeline
4. Has **well-defined failure modes**

---

## The Mental Shift

### Old Thinking
> "I'm building a trading algorithm. I need to write all the code for data, signals, sizing, risk, execution..."

**Result**: 3,000+ lines, months to build, hard to test.

### New Thinking
> "I'm discovering an alpha signal. The framework handles everything else."

**Result**: 200 lines of alpha, days to build, easy to test.

---

## Quick Comparison

| Metric | Build Everything | Use Framework |
|--------|-----------------|---------------|
| Lines of code | 1,000+ | ~60 |
| Development time | 8+ weeks | 1 week |
| Testing difficulty | Hard | Easy |
| Maintenance | Ongoing forever | Framework handles |
| Focus | Scattered | Alpha only |
