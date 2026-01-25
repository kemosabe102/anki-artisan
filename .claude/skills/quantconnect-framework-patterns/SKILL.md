---
name: quantconnect-framework-patterns
description: >
  Professional quant framework patterns for QuantConnect LEAN Algorithm Framework.
  Covers 5-module composition (Universe, Alpha, Portfolio, Risk, Execution),
  modular thinking mental models, and Stage Analysis methodology.
  Trigger: QC framework, LEAN algorithm, modular trading, alpha model,
  portfolio construction, Stage Analysis, composability, framework integration.
---

# QuantConnect Framework Patterns

*Professional quant patterns for composing trading systems from reusable LEAN Framework modules.*

---

## Quick Reference

### The Core Philosophy
> "Alpha is precious, everything else is plumbing."

| Time Allocation | Focus |
|-----------------|-------|
| **80%** | Alpha research (your signal) |
| **20%** | Infrastructure (use framework) |

### Code Reduction with Framework
| Approach | Lines of Code | Timeline |
|----------|---------------|----------|
| Build everything custom | 1,000+ lines | 8+ weeks |
| Use LEAN Framework | ~60 lines | 1 week |

---

## LEAN Framework 5-Module Architecture

```
┌─────────────────────────────────────────┐
│  1. UNIVERSE SELECTION                  │  ← Which securities to trade
│     FundamentalUniverseSelectionModel   │
└────────────────┬────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│  2. ALPHA MODEL                         │  ← Your signal (proprietary)
│     Emit Insights (direction, confidence)│
└────────────────┬────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│  3. PORTFOLIO CONSTRUCTION              │  ← Position sizing (commodity)
│     MaxSharpeOptimizer, MeanVariance    │
└────────────────┬────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│  4. RISK MANAGEMENT                     │  ← Protection (commodity)
│     MaxDrawdown, TrailingStop           │
└────────────────┬────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│  5. EXECUTION MODEL                     │  ← Order placement (commodity)
│     VWAP, ImmediateExecution            │
└─────────────────────────────────────────┘
```

### Module Summary

| Module | Your Code | Framework Handles |
|--------|-----------|-------------------|
| Universe | Filter criteria | Selection mechanics |
| Alpha | Signal logic | Insight routing |
| Portfolio | Risk params | Optimization math |
| Risk | Thresholds | Stop management |
| Execution | Model choice | Order splitting |

---

## Professional Quant Mental Models

### 1. Separation of Concerns
Each module does ONE thing well. Modules talk through clean interfaces.

### 2. Composability Over Customization
```python
# Bad: Monolithic
def my_strategy():
    # 500 lines of intertwined logic

# Good: Composed
system = TradingSystem(
    alpha=MyAlpha(),           # Your edge
    portfolio=MaxSharpe(),     # Framework
    risk=DrawdownManager(),    # Framework
    execution=VWAPExecutor())  # Framework
```

### 3. Interface-First Design
Define contracts BEFORE implementation:
```python
class AlphaModel(ABC):
    @abstractmethod
    def generate_insights(self, data) -> List[Insight]:
        pass
```

### 4. Configuration Over Code
Parameters in config files, not hardcoded:
```yaml
alpha:
  type: "StageMachine"
  params: { adx_threshold: 25 }
portfolio:
  type: "MaxSharpe"
  params: { max_position: 0.10 }
```

---

## Phase Progression Pattern

| Phase | Focus | Outcome |
|-------|-------|---------|
| **Phase 1** | Core logic (manual) | Working strategy |
| **Phase 2** | Data integration | Real data sources |
| **Phase 3** | Framework wrapping | 5-module composition |
| **Phase 4** | Validation | Backtest, paper, live |

---

## Anti-Patterns (NEVER DO)

| Anti-Pattern | Why Bad | Instead |
|--------------|---------|---------|
| Monolithic code | Hard to test/modify | Separate modules |
| Custom everything | Reinventing wheels | Use framework |
| Hardcoded params | Can't iterate | Config files |
| Research ≠ Production | Translation bugs | Same code path |
| Row-by-row iteration | Slow | Vectorized ops |

---

## Reference Documentation

| Document | Purpose |
|----------|---------|
| [lean-framework-modules.md](references/lean-framework-modules.md) | Detailed 5-module patterns |
| [stage-analysis-methodology.md](references/stage-analysis-methodology.md) | Example alpha implementation |
| [modular-composition-patterns.md](references/modular-composition-patterns.md) | Compose vs build patterns |
| [phase-3-integration-example.md](examples/phase-3-integration-example.md) | Complete code example |

---

## Cross-Skill Dependencies

| Dependency | Skill | Purpose |
|------------|-------|---------|
| Strategy spec | `strategy-specification` | JSON schema for strategies |
| Indicators | `technical-indicators` | ADX, EMA, RSI computation |
| Risk sizing | `risk-management` | Van Tharp R-multiples |

---

## Validation Checklist

Before completing framework integration:
- [ ] Alpha wrapped in AlphaModel interface
- [ ] Insights emitted with direction + confidence
- [ ] Portfolio optimizer configured with constraints
- [ ] Risk models added (at least MaxDrawdown)
- [ ] Execution model selected
- [ ] OnData() simplified (framework handles flow)
