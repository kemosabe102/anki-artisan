# Pattern Detection Reference

Detailed specifications for 4 trading pattern detection frameworks with confidence scoring.

---

## 1. Breakout Detection

**Purpose**: Identify price breaks through established ranges with conviction.

**Primary Method: Donchian Channel**
- Calculate N-period high/low channels (default N=20)
- Breakout signal: Close > channel_high OR Close < channel_low
- Volume confirmation: Volume > 1.5x 20-day average

**Alternative: Clenow Momentum**
- Price > exponential regression upper band (20-day)
- ADX > 25 (trending regime)
- Volume > 1.5x average

### Confidence Scoring

| Factor | Contribution |
|--------|--------------|
| Base (pattern detected) | 0.6 |
| Volume > 1.5x avg | +0.1 |
| ADX > 25 | +0.1 |
| Gap > 2% ATR | +0.1 |
| **Max** | **0.9** |

### Code Pattern

```python
def detect_breakout(df, period=20, volume_multiplier=1.5):
    breakout_up = (
        (df['close'] > df['donchian_upper_20']) &
        (df['volume'] > volume_multiplier * df['volume'].rolling(period).mean())
    )
    return breakout_up
```

---

## 2. Pullback Detection

**Purpose**: Identify retracements in established trends for entry opportunities.

**EMA Reclaim Pattern**
- Establish trend: EMA(20) > EMA(50) for uptrend
- Pullback: Price touches EMA(20) from above
- Confirmation: Close back above EMA(20) within 5 bars
- ADX > 20 (trend strength maintained)

### Confidence Scoring

| Factor | Contribution |
|--------|--------------|
| Base (pattern detected) | 0.5 |
| ADX > 25 (strong trend) | +0.15 |
| Volume confirmation | +0.1 |
| RSI confirmation (> 40) | +0.1 |
| Gap within 1 ATR | +0.05 |
| **Max** | **0.9** |

### Code Pattern

```python
def detect_pullback(df, ema_fast=20, ema_slow=50):
    uptrend = df['ema_20'] > df['ema_50']
    pullback_touch = (df['low'] <= df['ema_20']) & (df['low'].shift(1) > df['ema_20'].shift(1))
    reclaim = (df['close'] > df['ema_20']) & pullback_touch.rolling(5).max()
    valid = uptrend & reclaim & (df['adx_14'] > 20) & (df['rsi_14'] > 40)
    return valid
```

---

## 3. PEAD/News Drift Detection

**Purpose**: Capture post-earnings announcement drift and news-driven momentum.

**SUE Formula (Standardized Unexpected Earnings)**
```
SUE = (Actual EPS - Expected EPS) / StdDev(EPS surprises)
```
- Threshold: |SUE| > 2.0 for significant surprise

**Gap + Sentiment Confirmation**
- Gap > 3% at open (news reaction)
- Sentiment score (zS) > 0.6 (positive) or < -0.6 (negative)
- Volume > 2x average on gap day

**Drift Confirmation**
- Price continues in gap direction for 3+ days
- Volume remains elevated (> 1.2x average)

### Confidence Scoring

| Factor | Contribution |
|--------|--------------|
| Base (pattern detected) | 0.5 |
| Per SUE unit above 2.0 | +0.1 (max +0.3) |
| Sentiment alignment | +0.2 |
| Drift continuation 3+ days | +0.1 |
| Volume persistence | +0.05 |
| **Max** | **0.95** |

---

## 4. Divergence Detection

**Purpose**: Identify price-indicator disagreement signaling potential reversals.

### Regular Divergence (Reversal Signal)
- **Bullish**: Price lower low, RSI/MACD higher low
- **Bearish**: Price higher high, RSI/MACD lower high

### Hidden Divergence (Continuation Signal)
- **Bullish**: Price higher low, RSI/MACD lower low
- **Bearish**: Price lower high, RSI/MACD higher high

### Peak/Trough Algorithm
1. Identify local extrema: `peaks = argrelmax(price, order=5)`
2. Compare consecutive peaks/troughs in price vs indicator
3. Require minimum 2 peaks/troughs for divergence

### Confidence Scoring

| Factor | Contribution |
|--------|--------------|
| Base (divergence detected) | 0.4 |
| Multiple indicator agreement | +0.2 |
| Volume confirmation | +0.1 |
| Overbought/oversold extreme | +0.1 |
| Clean peak/trough structure | +0.1 |
| **Max** | **0.9** |

---

## Multi-Pattern Confirmation

**Strategy**: Combine pattern signals to increase confidence.

| Combination | Confidence Formula |
|-------------|-------------------|
| Breakout + PEAD | max(breakout_conf, pead_conf) + 0.1 |
| Pullback + Divergence | (pullback_conf + div_conf) / 2 + 0.15 |
| Breakout + Hidden Divergence | min(0.95, breakout_conf + 0.15) |

**Conflict Resolution**:
- Contradictory signals: Use highest confidence, discount by 0.2
- Time-weighted: Recent patterns (< 5 bars) weighted 2x
