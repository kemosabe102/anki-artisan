# QuantConnect Algorithm Patterns

## Algorithm Lifecycle

```python
class MyAlgorithm(QCAlgorithm):
    def initialize(self) -> None:
        # 1. Set dates and cash
        # 2. Add securities
        # 3. Initialize indicators
        # 4. Set risk parameters
    
    def on_data(self, data: Slice) -> None:
        # 1. Check indicators ready
        # 2. Check entry conditions
        # 3. Check exit conditions
        # 4. Execute orders
```

## Common Indicator Setup

```python
# Trend
self.ema_fast = self.ema(symbol, 20)
self.ema_slow = self.ema(symbol, 50)

# Momentum
self.rsi = self.rsi(symbol, 14)

# Volatility
self.atr = self.atr(symbol, 22)
self.bb = self.bb(symbol, 20, 2)

# Breakout
self.donchian = self.dch(symbol, 20, 20)
```

## Position Sizing

```python
def calculate_position_size(self, symbol, stop_distance):
    risk_dollars = self.Portfolio.TotalPortfolioValue * self.risk_per_trade
    shares = int(risk_dollars / stop_distance)
    return shares
```
