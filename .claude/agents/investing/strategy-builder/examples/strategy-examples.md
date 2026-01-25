# Strategy Examples

Complete examples showing natural language -> JSON specification -> Python skeleton transformation for each strategy type.

**Schema Reference**: `../schemas/strategy-builder.schema.json`

---

## Example 1: Momentum Strategy (Donchian Breakout)

### Natural Language Request

> "Build a momentum strategy that buys stocks breaking out of 20-day highs with volume confirmation. Use ATR-based stops. Only trade in uptrending markets."

### Classification

- **Strategy Type**: `momentum`
- **Classification Confidence**: 0.92
- **Key Signals**: "breaking out", "20-day highs", "uptrending markets"

### JSON Specification

```json
{
  "strategy_name": "DonchianBreakoutMomentum",
  "strategy_type": "momentum",
  "universe": {
    "type": "manual",
    "symbols": ["SPY", "QQQ", "IWM"],
    "description": "Large-cap ETFs for liquidity"
  },
  "entry": {
    "condition": "price >= donchian_high(20) AND volume > 1.5 * sma(volume, 20)",
    "trigger": "breakout",
    "description": "Price breaks 20-day high with 50% above-average volume"
  },
  "exit": {
    "stop_loss": {
      "method": "atr_multiple",
      "value": 2,
      "period": 14
    },
    "take_profit": {
      "method": "atr_multiple",
      "value": 4,
      "period": 14
    },
    "trailing_stop": null
  },
  "position_sizing": {
    "method": "fixed_risk",
    "risk_per_trade": 0.01,
    "description": "Risk 1% of portfolio per trade"
  },
  "risk_management": {
    "max_positions": 5,
    "max_portfolio_risk": 0.05,
    "max_sector_exposure": 0.30
  },
  "timeframe": "daily",
  "regime_filters": {
    "indicator": "SPY_200DMA",
    "conditions": {
      "above": {
        "multiplier": 1.0,
        "action": "trade",
        "description": "Full position size in uptrend"
      },
      "below": {
        "multiplier": 0.5,
        "action": "reduce_size",
        "description": "Half position size in downtrend"
      }
    }
  }
}
```

### Python Skeleton Excerpt

```python
from AlgorithmImports import *

class DonchianBreakoutMomentum(QCAlgorithm):
    """Momentum strategy: Donchian breakout with volume confirmation."""
    
    def initialize(self) -> None:
        self.set_start_date(2020, 1, 1)
        self.set_cash(100000)
        
        # Universe
        self.symbols = ["SPY", "QQQ", "IWM"]
        for symbol in self.symbols:
            self.add_equity(symbol, Resolution.DAILY)
        
        # Regime filter: SPY 200-day SMA
        self.spy = self.add_equity("SPY", Resolution.DAILY).symbol
        self.sma200 = self.sma(self.spy, 200, Resolution.DAILY)
        self.regime_multiplier = 1.0
        
        # Indicators per symbol
        self.donchian = {}
        self.atr = {}
        self.volume_sma = {}
        for symbol in self.symbols:
            sym = self.securities[symbol].symbol
            self.donchian[sym] = self.dch(sym, 20, Resolution.DAILY)
            self.atr[sym] = self.atr(sym, 14, Resolution.DAILY)
            self.volume_sma[sym] = self.sma(sym, 20, Resolution.DAILY, Field.VOLUME)
        
        # Risk parameters
        self.risk_per_trade = 0.01
        self.max_positions = 5

    def on_data(self, data: Slice) -> None:
        self._update_regime_multiplier()
        
        for symbol in self.symbols:
            sym = self.securities[symbol].symbol
            if not data.contains_key(sym):
                continue
            
            if self.portfolio[sym].invested:
                self._check_exit(sym, data)
            else:
                self._check_entry(sym, data)
    
    def _update_regime_multiplier(self) -> None:
        """Update position size multiplier based on market regime."""
        if not self.sma200.is_ready:
            self.regime_multiplier = 0.5  # Conservative until data ready
            return
        
        spy_price = self.securities[self.spy].price
        if spy_price > self.sma200.current.value:
            self.regime_multiplier = 1.0  # Full size in uptrend
        else:
            self.regime_multiplier = 0.5  # Half size in downtrend
    
    def _check_entry(self, symbol, data) -> None:
        """Check for breakout entry with volume confirmation."""
        if not self.donchian[symbol].is_ready:
            return
        
        price = data[symbol].close
        volume = data[symbol].volume
        
        # Entry: Price breaks 20-day high with volume confirmation
        breakout = price >= self.donchian[symbol].upper_band.current.value
        volume_confirmed = volume > 1.5 * self.volume_sma[symbol].current.value
        
        if breakout and volume_confirmed:
            self._execute_entry(symbol)
    
    def _execute_entry(self, symbol) -> None:
        """Execute entry with regime-adjusted position sizing."""
        if self._count_positions() >= self.max_positions:
            return
        
        # Calculate position size with regime multiplier
        portfolio_value = self.portfolio.total_portfolio_value
        risk_dollars = portfolio_value * self.risk_per_trade
        stop_distance = 2 * self.atr[symbol].current.value
        
        base_shares = int(risk_dollars / stop_distance)
        shares = int(base_shares * self.regime_multiplier)  # Apply regime filter
        
        if shares > 0:
            self.market_order(symbol, shares)
            self.log(f"ENTRY: {symbol} | Shares: {shares} | Regime: {self.regime_multiplier}")
```

---

## Example 2: Mean-Reversion Strategy (RSI Oversold)

### Natural Language Request

> "Create a mean-reversion strategy that buys when RSI drops below 30 and sells when it rises above 70. Use tighter sizing during high volatility periods."

### Classification

- **Strategy Type**: `mean_reversion`
- **Classification Confidence**: 0.95
- **Key Signals**: "mean-reversion", "RSI", "oversold", "overbought"

### JSON Specification

```json
{
  "strategy_name": "RSIMeanReversion",
  "strategy_type": "mean_reversion",
  "universe": {
    "type": "manual",
    "symbols": ["SPY", "QQQ"],
    "description": "Liquid ETFs with mean-reverting behavior"
  },
  "entry": {
    "condition": "RSI(14) < 30",
    "trigger": "oversold",
    "description": "Enter when RSI indicates oversold conditions"
  },
  "exit": {
    "condition": "RSI(14) > 70",
    "stop_loss": {
      "method": "percentage",
      "value": 0.03
    },
    "take_profit": null,
    "description": "Exit when RSI indicates overbought or 3% stop hit"
  },
  "position_sizing": {
    "method": "fixed_risk",
    "risk_per_trade": 0.02,
    "description": "Risk 2% of portfolio per trade"
  },
  "risk_management": {
    "max_positions": 3,
    "max_portfolio_risk": 0.06,
    "max_drawdown_halt": 0.10
  },
  "timeframe": "daily",
  "regime_filters": {
    "indicator": "VIX_LEVEL",
    "conditions": {
      "low": {
        "threshold": 15,
        "multiplier": 1.0,
        "description": "Full size when VIX < 15"
      },
      "normal": {
        "threshold": 25,
        "multiplier": 0.75,
        "description": "75% size when VIX 15-25"
      },
      "high": {
        "threshold": 35,
        "multiplier": 0.5,
        "description": "50% size when VIX 25-35"
      },
      "extreme": {
        "threshold": 50,
        "multiplier": 0.25,
        "description": "25% size when VIX > 35"
      }
    }
  }
}
```

### Python Skeleton Excerpt

```python
from AlgorithmImports import *

class RSIMeanReversion(QCAlgorithm):
    """Mean-reversion strategy: RSI oversold/overbought with VIX regime filter."""
    
    def initialize(self) -> None:
        self.set_start_date(2020, 1, 1)
        self.set_cash(100000)
        
        # Universe
        self.spy = self.add_equity("SPY", Resolution.DAILY).symbol
        self.qqq = self.add_equity("QQQ", Resolution.DAILY).symbol
        self.symbols = [self.spy, self.qqq]
        
        # VIX for regime filter
        self.vix = self.add_data(CBOE, "VIX", Resolution.DAILY).symbol
        self.regime_multiplier = 1.0
        
        # RSI indicators
        self.rsi = {}
        for sym in self.symbols:
            self.rsi[sym] = self.rsi(sym, 14, Resolution.DAILY)
        
        # Risk parameters
        self.risk_per_trade = 0.02
        self.rsi_oversold = 30
        self.rsi_overbought = 70
        self.stop_loss_pct = 0.03
        self.entry_prices = {}
    
    def on_data(self, data: Slice) -> None:
        self._update_regime_multiplier(data)
        
        for symbol in self.symbols:
            if not data.contains_key(symbol):
                continue
            
            if self.portfolio[symbol].invested:
                self._check_exit(symbol, data)
            else:
                self._check_entry(symbol, data)
    
    def _update_regime_multiplier(self, data: Slice) -> None:
        """Update position size multiplier based on VIX level."""
        if not data.contains_key(self.vix):
            self.regime_multiplier = 0.5  # Conservative default
            return
        
        vix_level = data[self.vix].close
        
        if vix_level < 15:
            self.regime_multiplier = 1.0   # Low vol: full size
        elif vix_level < 25:
            self.regime_multiplier = 0.75  # Normal vol: 75%
        elif vix_level < 35:
            self.regime_multiplier = 0.5   # High vol: 50%
        else:
            self.regime_multiplier = 0.25  # Extreme vol: 25%
    
    def _check_entry(self, symbol, data) -> None:
        """Check for RSI oversold entry."""
        if not self.rsi[symbol].is_ready:
            return
        
        if self.rsi[symbol].current.value < self.rsi_oversold:
            self._execute_entry(symbol, data[symbol].close)
    
    def _check_exit(self, symbol, data) -> None:
        """Check for RSI overbought exit or stop loss."""
        current_price = data[symbol].close
        entry_price = self.entry_prices.get(symbol, current_price)
        
        # RSI overbought exit
        if self.rsi[symbol].current.value > self.rsi_overbought:
            self.liquidate(symbol, "RSI Overbought")
            return
        
        # Stop loss exit
        if current_price < entry_price * (1 - self.stop_loss_pct):
            self.liquidate(symbol, "Stop Loss")
    
    def _execute_entry(self, symbol, price) -> None:
        """Execute entry with VIX-adjusted position sizing."""
        portfolio_value = self.portfolio.total_portfolio_value
        risk_dollars = portfolio_value * self.risk_per_trade
        stop_distance = price * self.stop_loss_pct
        
        base_shares = int(risk_dollars / stop_distance)
        shares = int(base_shares * self.regime_multiplier)  # Apply VIX regime filter
        
        if shares > 0:
            self.market_order(symbol, shares)
            self.entry_prices[symbol] = price
            self.log(f"ENTRY: {symbol} | Shares: {shares} | VIX Mult: {self.regime_multiplier}")
```

---

## Example 3: Event-Driven Strategy (Earnings Surprise)

### Natural Language Request

> "Build a strategy that trades earnings surprises. Long on positive surprises >5%, short on negative surprises. Only trade when market sentiment is neutral."

### Classification

- **Strategy Type**: `event_driven`
- **Classification Confidence**: 0.88
- **Key Signals**: "earnings surprises", "positive surprises", "negative surprises", "sentiment"

### JSON Specification

```json
{
  "strategy_name": "EarningsSurpriseTrader",
  "strategy_type": "event_driven",
  "universe": {
    "type": "scheduled_earnings",
    "filters": {
      "market_cap_min": 10000000000,
      "avg_volume_min": 1000000
    },
    "description": "Large-cap stocks with upcoming earnings"
  },
  "entry": {
    "long_condition": "earnings_surprise_pct > 5",
    "short_condition": "earnings_surprise_pct < -5",
    "trigger": "post_earnings_announcement",
    "hold_period_days": 5,
    "description": "Trade post-earnings based on surprise magnitude"
  },
  "exit": {
    "time_based": {
      "hold_days": 5
    },
    "stop_loss": {
      "method": "percentage",
      "value": 0.05
    },
    "take_profit": {
      "method": "percentage",
      "value": 0.10
    }
  },
  "position_sizing": {
    "method": "equal_weight",
    "max_position_pct": 0.05,
    "description": "Equal weight positions, max 5% per trade"
  },
  "risk_management": {
    "max_positions": 10,
    "max_long_exposure": 0.50,
    "max_short_exposure": 0.30,
    "earnings_blackout_days": 1
  },
  "timeframe": "daily",
  "regime_filters": {
    "indicator": "MARKET_SENTIMENT",
    "conditions": {
      "bullish": {
        "vix_below": 18,
        "spy_above_sma50": true,
        "multiplier": 1.0,
        "long_only": false,
        "description": "Full trading in bullish sentiment"
      },
      "neutral": {
        "vix_range": [18, 28],
        "multiplier": 1.0,
        "description": "Normal trading in neutral sentiment"
      },
      "bearish": {
        "vix_above": 28,
        "spy_below_sma50": true,
        "multiplier": 0.5,
        "short_bias": true,
        "description": "Reduced size, short bias in bearish sentiment"
      }
    }
  }
}
```

### Python Skeleton Excerpt

```python
from AlgorithmImports import *
from datetime import timedelta

class EarningsSurpriseTrader(QCAlgorithm):
    """Event-driven strategy: Earnings surprise trading with sentiment regime filter."""
    
    def initialize(self) -> None:
        self.set_start_date(2020, 1, 1)
        self.set_cash(100000)
        
        # Sentiment regime indicators
        self.spy = self.add_equity("SPY", Resolution.DAILY).symbol
        self.vix = self.add_data(CBOE, "VIX", Resolution.DAILY).symbol
        self.sma50 = self.sma(self.spy, 50, Resolution.DAILY)
        
        self.regime_multiplier = 1.0
        self.sentiment = "neutral"
        
        # Earnings tracking
        self.earnings_universe = []
        self.active_trades = {}  # symbol -> (entry_date, direction, entry_price)
        
        # Parameters
        self.surprise_threshold = 0.05  # 5% surprise threshold
        self.hold_days = 5
        self.stop_loss_pct = 0.05
        self.take_profit_pct = 0.10
        self.max_position_pct = 0.05
        
        # Schedule earnings check
        self.schedule.on(self.date_rules.every_day(),
                        self.time_rules.after_market_open(self.spy, 30),
                        self._check_earnings_events)
    
    def _update_regime_multiplier(self, data: Slice) -> None:
        """Update regime based on market sentiment (VIX + trend)."""
        if not self.sma50.is_ready or not data.contains_key(self.vix):
            self.regime_multiplier = 0.5
            self.sentiment = "unknown"
            return
        
        vix_level = data[self.vix].close
        spy_price = self.securities[self.spy].price
        spy_above_sma = spy_price > self.sma50.current.value
        
        if vix_level < 18 and spy_above_sma:
            self.sentiment = "bullish"
            self.regime_multiplier = 1.0
        elif vix_level > 28 or not spy_above_sma:
            self.sentiment = "bearish"
            self.regime_multiplier = 0.5
        else:
            self.sentiment = "neutral"
            self.regime_multiplier = 1.0
    
    def _check_earnings_events(self) -> None:
        """Check for earnings surprises and execute trades."""
        # NOTE: Actual earnings data would come from data provider
        # This is a skeleton showing the pattern
        pass
    
    def _execute_earnings_trade(self, symbol, surprise_pct: float, price: float) -> None:
        """Execute trade based on earnings surprise with sentiment-adjusted sizing."""
        direction = 1 if surprise_pct > self.surprise_threshold else -1
        
        # Adjust for bearish sentiment (favor shorts)
        if self.sentiment == "bearish" and direction == 1:
            self.regime_multiplier *= 0.5  # Reduce long exposure in bearish
        
        portfolio_value = self.portfolio.total_portfolio_value
        position_value = portfolio_value * self.max_position_pct * self.regime_multiplier
        shares = int(position_value / price) * direction
        
        if shares != 0:
            self.market_order(symbol, shares)
            self.active_trades[symbol] = (self.time, direction, price)
            self.log(f"EARNINGS: {symbol} | Surprise: {surprise_pct:.1%} | "
                    f"Dir: {'LONG' if direction > 0 else 'SHORT'} | Sentiment: {self.sentiment}")
```

---

## Example 4: Multi-Factor Strategy (Value + Momentum + Quality)

### Natural Language Request

> "Create a multi-factor strategy combining value (P/E), momentum (12-month return), and quality (ROE). Reduce exposure during bear markets."

### Classification

- **Strategy Type**: `multi_factor`
- **Classification Confidence**: 0.90
- **Key Signals**: "multi-factor", "value", "momentum", "quality", "P/E", "ROE"

### JSON Specification

```json
{
  "strategy_name": "ValueMomentumQuality",
  "strategy_type": "multi_factor",
  "universe": {
    "type": "fundamental_screen",
    "source": "sp500",
    "filters": {
      "market_cap_min": 5000000000,
      "avg_volume_min": 500000,
      "exclude_sectors": ["Financials", "Utilities"]
    },
    "description": "S&P 500 ex-Financials/Utilities, >$5B market cap"
  },
  "factors": {
    "value": {
      "metric": "pe_ratio",
      "weight": 0.30,
      "direction": "low_is_good",
      "zscore_cap": 3.0,
      "description": "Lower P/E = higher score"
    },
    "momentum": {
      "metric": "return_12m_1m",
      "weight": 0.40,
      "direction": "high_is_good",
      "zscore_cap": 3.0,
      "description": "12-month return excluding last month"
    },
    "quality": {
      "metric": "roe",
      "weight": 0.30,
      "direction": "high_is_good",
      "zscore_cap": 3.0,
      "description": "Higher ROE = higher score"
    }
  },
  "entry": {
    "condition": "composite_score in top_decile",
    "rebalance_frequency": "monthly",
    "description": "Buy top 10% by composite factor score"
  },
  "exit": {
    "condition": "composite_score drops below top_quintile OR rebalance",
    "description": "Sell when score drops to bottom 80%"
  },
  "position_sizing": {
    "method": "factor_weighted",
    "base_weight": "equal",
    "tilt_by_score": true,
    "max_position_pct": 0.05,
    "description": "Equal weight with slight tilt toward higher scores"
  },
  "risk_management": {
    "max_positions": 30,
    "max_sector_weight": 0.25,
    "max_turnover_monthly": 0.30
  },
  "timeframe": "monthly",
  "regime_filters": {
    "indicator": "COMPOSITE_REGIME",
    "components": {
      "trend": {
        "indicator": "SPY_200DMA",
        "weight": 0.5
      },
      "volatility": {
        "indicator": "VIX_PERCENTILE_1Y",
        "weight": 0.3
      },
      "breadth": {
        "indicator": "NYSE_ADVANCE_DECLINE",
        "weight": 0.2
      }
    },
    "conditions": {
      "bull_market": {
        "composite_score_above": 0.6,
        "multiplier": 1.0,
        "factor_tilt": "momentum",
        "description": "Full exposure, favor momentum in bull markets"
      },
      "bear_market": {
        "composite_score_below": 0.4,
        "multiplier": 0.5,
        "factor_tilt": "quality",
        "description": "Half exposure, favor quality in bear markets"
      },
      "transition": {
        "composite_score_range": [0.4, 0.6],
        "multiplier": 0.75,
        "factor_tilt": "value",
        "description": "Reduced exposure, favor value in transitions"
      }
    }
  }
}
```

### Python Skeleton Excerpt

```python
from AlgorithmImports import *
import numpy as np

class ValueMomentumQuality(QCAlgorithm):
    """Multi-factor strategy: Value + Momentum + Quality with composite regime filter."""
    
    def initialize(self) -> None:
        self.set_start_date(2020, 1, 1)
        self.set_cash(100000)
        
        # Regime indicators
        self.spy = self.add_equity("SPY", Resolution.DAILY).symbol
        self.vix = self.add_data(CBOE, "VIX", Resolution.DAILY).symbol
        self.sma200 = self.sma(self.spy, 200, Resolution.DAILY)
        
        self.regime_multiplier = 1.0
        self.regime = "transition"
        self.factor_tilt = "value"
        
        # Factor weights (adjusted by regime)
        self.base_weights = {"value": 0.30, "momentum": 0.40, "quality": 0.30}
        self.active_weights = self.base_weights.copy()
        
        # Universe and holdings
        self.universe_symbols = []
        self.holdings = {}
        self.max_positions = 30
        self.max_position_pct = 0.05
        
        # VIX history for percentile calculation
        self.vix_history = []
        self.vix_lookback = 252  # 1 year
        
        # Schedule monthly rebalance
        self.schedule.on(self.date_rules.month_start(5),
                        self.time_rules.after_market_open(self.spy, 30),
                        self._rebalance)
    
    def _update_regime_multiplier(self, data: Slice) -> None:
        """Update regime based on composite indicator (trend + vol + breadth)."""
        if not self.sma200.is_ready:
            self.regime_multiplier = 0.5
            self.regime = "unknown"
            return
        
        # Trend component (50% weight)
        spy_price = self.securities[self.spy].price
        trend_score = 1.0 if spy_price > self.sma200.current.value else 0.0
        
        # Volatility component (30% weight) - lower VIX percentile = higher score
        vix_percentile = self._calculate_vix_percentile(data)
        vol_score = 1.0 - vix_percentile  # Invert: low VIX = high score
        
        # Breadth component simplified (20% weight)
        # In production, use NYSE A/D line data
        breadth_score = 0.5  # Placeholder
        
        # Composite score
        composite = (trend_score * 0.5) + (vol_score * 0.3) + (breadth_score * 0.2)
        
        # Determine regime and adjust
        if composite > 0.6:
            self.regime = "bull_market"
            self.regime_multiplier = 1.0
            self._tilt_factors("momentum")
        elif composite < 0.4:
            self.regime = "bear_market"
            self.regime_multiplier = 0.5
            self._tilt_factors("quality")
        else:
            self.regime = "transition"
            self.regime_multiplier = 0.75
            self._tilt_factors("value")
    
    def _tilt_factors(self, favored_factor: str) -> None:
        """Adjust factor weights based on regime."""
        self.active_weights = self.base_weights.copy()
        # Add 10% to favored factor, reduce others proportionally
        tilt_amount = 0.10
        self.active_weights[favored_factor] += tilt_amount
        
        # Reduce other factors proportionally
        other_factors = [f for f in self.base_weights if f != favored_factor]
        reduction_each = tilt_amount / len(other_factors)
        for factor in other_factors:
            self.active_weights[factor] -= reduction_each
        
        self.factor_tilt = favored_factor
    
    def _calculate_vix_percentile(self, data: Slice) -> float:
        """Calculate current VIX percentile over trailing year."""
        if not data.contains_key(self.vix):
            return 0.5
        
        current_vix = data[self.vix].close
        self.vix_history.append(current_vix)
        
        if len(self.vix_history) > self.vix_lookback:
            self.vix_history = self.vix_history[-self.vix_lookback:]
        
        if len(self.vix_history) < 20:
            return 0.5
        
        return sum(1 for v in self.vix_history if v < current_vix) / len(self.vix_history)
    
    def _rebalance(self) -> None:
        """Monthly rebalance with regime-adjusted position sizing."""
        self._update_regime_multiplier(self.current_slice)
        
        # Score universe (simplified - actual would use fundamental data)
        scores = self._calculate_factor_scores()
        
        # Select top decile
        sorted_symbols = sorted(scores.keys(), key=lambda s: scores[s], reverse=True)
        top_decile = sorted_symbols[:max(1, len(sorted_symbols) // 10)]
        
        # Calculate target weights with regime adjustment
        target_weight = (1.0 / len(top_decile)) * self.regime_multiplier
        target_weight = min(target_weight, self.max_position_pct)
        
        # Execute rebalance
        for symbol in self.portfolio.keys():
            if symbol not in top_decile:
                self.liquidate(symbol)
        
        for symbol in top_decile[:self.max_positions]:
            self.set_holdings(symbol, target_weight)
        
        self.log(f"REBALANCE: Regime={self.regime} | Mult={self.regime_multiplier} | "
                f"Tilt={self.factor_tilt} | Positions={len(top_decile)}")
```

---

## Key Takeaways

### 1. Every Strategy MUST Include `regime_filters`

This is enforced by **ALGO_GATE_001** (Regime Awareness Gate):

- **No strategy passes validation without regime awareness**
- The schema requires `regime_filters` as a mandatory field
- Default implementation uses SPY 200 DMA if no regime specified

### 2. Position Sizing Uses `regime_multiplier`

The universal pattern for all strategy types:

```python
base_shares = int(risk_dollars / stop_distance)
shares = int(base_shares * self.regime_multiplier)  # Apply regime filter
```

This ensures position size automatically adjusts based on market conditions.

### 3. Common Regime Indicators

| Indicator | Best For | Description |
|-----------|----------|-------------|
| `SPY_200DMA` | Trend strategies | Price vs 200-day SMA |
| `VIX_LEVEL` | Vol-sensitive strategies | Absolute VIX thresholds |
| `VIX_PERCENTILE` | Relative vol strategies | VIX rank over trailing period |
| `SECTOR_RS` | Sector rotation | Relative strength vs benchmark |
| `MARKET_SENTIMENT` | Event-driven | Composite of trend + vol |
| `COMPOSITE_REGIME` | Multi-factor | Weighted combination of indicators |

### 4. Default Regime Logic

When no custom regime is specified, the default is applied:

```python
def _update_regime_multiplier(self) -> None:
    """Default regime logic: SPY above/below 200 DMA."""
    if not self.sma200.is_ready:
        self.regime_multiplier = 0.5  # Conservative until ready
        return
    
    spy_price = self.securities[self.spy].price
    if spy_price > self.sma200.current.value:
        self.regime_multiplier = 1.0  # Full size in uptrend
    else:
        self.regime_multiplier = 0.5  # Half size in downtrend
```

### 5. Strategy Type to Regime Mapping

| Strategy Type | Recommended Regime | Rationale |
|---------------|-------------------|-----------|
| `momentum` | SPY_200DMA | Momentum works best in trends |
| `mean_reversion` | VIX_LEVEL | Mean reversion sensitive to vol |
| `event_driven` | MARKET_SENTIMENT | Events react to market mood |
| `multi_factor` | COMPOSITE_REGIME | Factors rotate by regime |

---

## Validation Checklist

Before submitting a strategy specification, verify:

- [ ] `strategy_name` is PascalCase and descriptive
- [ ] `strategy_type` matches one of: momentum, mean_reversion, event_driven, multi_factor
- [ ] `regime_filters` is present with `indicator` and `conditions`
- [ ] `entry` conditions are specific and testable
- [ ] `exit` includes stop_loss (mandatory for risk management)
- [ ] `position_sizing` method is defined
- [ ] `risk_management` includes max_positions
- [ ] `timeframe` is specified (daily, weekly, monthly)

---

## See Also

- **Templates**: `../templates/README.md` - Template placeholder documentation
- **Schema**: `../schemas/strategy-builder.schema.json` - Full JSON schema with all required fields
- **Agent Docs**: `../strategy-builder.md` - Agent documentation with modes and workflows
- **Development**: `../docs/development_guide.md` - Development best practices
- **Iteration**: `../docs/iteration_framework.md` - HDD iteration workflow

---

## Appendix: Quick Reference

### Minimum Viable Specification

```json
{
  "strategy_name": "MinimalExample",
  "strategy_type": "momentum",
  "universe": {"type": "manual", "symbols": ["SPY"]},
  "entry": {"condition": "price > sma(20)"},
  "exit": {"stop_loss": {"method": "percentage", "value": 0.02}},
  "position_sizing": {"method": "fixed_risk", "risk_per_trade": 0.01},
  "risk_management": {"max_positions": 1},
  "timeframe": "daily",
  "regime_filters": {
    "indicator": "SPY_200DMA",
    "conditions": {"above": {"multiplier": 1.0}, "below": {"multiplier": 0.5}}
  }
}
```

### Regime Multiplier Quick Reference

| Market Condition | Multiplier | Position Size |
|------------------|------------|---------------|
| Strong uptrend (SPY > 200 DMA) | 1.0 | 100% of base |
| Weak uptrend / transition | 0.75 | 75% of base |
| Downtrend (SPY < 200 DMA) | 0.5 | 50% of base |
| High volatility (VIX > 35) | 0.25-0.5 | 25-50% of base |
| Extreme volatility (VIX > 50) | 0.0-0.25 | Minimal or no new positions |

### Strategy Type Keywords

Use these keywords in natural language requests for accurate classification:

| Strategy Type | Keywords |
|---------------|----------|
| `momentum` | breakout, trend, moving average crossover, highs, strength |
| `mean_reversion` | oversold, overbought, RSI, revert, bounce, pullback |
| `event_driven` | earnings, news, announcement, surprise, catalyst |
| `multi_factor` | value, momentum, quality, combined, scoring, factors, P/E, ROE |
