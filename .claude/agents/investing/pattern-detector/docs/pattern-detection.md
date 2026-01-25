# Trading Pattern Detection Frameworks

## Overview

Comprehensive framework for detecting classical trading patterns (breakout, pullback, PEAD/news drift, divergence) using multi-indicator confirmation and quantitative thresholds.

## Core Frameworks

### 1. Breakout Detection

**Purpose**: Identify when price breaks through established ranges with conviction

**When to Use**: Range-bound markets transitioning to trending phases, volume expansion events

**How to Apply**:

1. **Donchian Channel Method**:
   - Calculate N-period high/low channels (default N=20)
   - Breakout = Close > channel_high OR Close < channel_low
   - Confirmation: Volume > 1.5x average volume

2. **Clenow Momentum Variant**:
   - Price > exponential regression upper band (20-day)
   - ADX > 25 (trending regime)
   - Volume confirmation (>1.5x 20-day avg)

**Example**:

```python
def detect_breakout(df, period=20, volume_multiplier=1.5):
    df['donchian_high'] = df['high'].rolling(period).max()
    df['donchian_low'] = df['low'].rolling(period).min()
    df['avg_volume'] = df['volume'].rolling(period).mean()

    breakout_up = (
        (df['close'] > df['donchian_high']) &
        (df['volume'] > volume_multiplier * df['avg_volume'])
    )
    breakout_down = (
        (df['close'] < df['donchian_low']) &
        (df['volume'] > volume_multiplier * df['avg_volume'])
    )

    return breakout_up, breakout_down
```

**Confidence Scoring**:

- Base confidence: 0.6
- +0.1 for volume confirmation
- +0.1 for ADX > 25
- +0.1 for gap > 2% ATR
- Max confidence: 0.9

---

### 2. Pullback Detection

**Purpose**: Identify retracements in established trends that offer entry opportunities

**When to Use**: After confirmed uptrend/downtrend establishment, during consolidation phases

**How to Apply**:

1. **EMA Reclaim Pattern**:
   - Establish trend: EMA(20) > EMA(50) for uptrend
   - Pullback: Price touches EMA(20) from above
   - Confirmation: Close back above EMA(20) within 5 bars
   - ADX > 20 (trend strength maintained)

2. **RSI Oversold/Overbought**:
   - Uptrend pullback: RSI(14) < 40, then crosses back > 40
   - Downtrend pullback: RSI(14) > 60, then crosses back < 60
   - Volume on reclaim > average

**Example**:

```python
def detect_pullback(df, ema_fast=20, ema_slow=50, rsi_period=14):
    df['ema_fast'] = df['close'].ewm(span=ema_fast).mean()
    df['ema_slow'] = df['close'].ewm(span=ema_slow).mean()
    df['rsi'] = compute_rsi(df['close'], rsi_period)
    df['adx'] = compute_adx(df, period=14)

    uptrend = df['ema_fast'] > df['ema_slow']
    pullback_touch = (df['low'] <= df['ema_fast']) & (df['low'].shift(1) > df['ema_fast'].shift(1))
    reclaim = (df['close'] > df['ema_fast']) & pullback_touch.rolling(5).max()

    valid_pullback = uptrend & reclaim & (df['adx'] > 20) & (df['rsi'] > 40)

    return valid_pullback
```

**Confidence Scoring**:

- Base confidence: 0.5
- +0.15 for ADX > 25 (strong trend)
- +0.1 for volume confirmation
- +0.1 for RSI confirmation
- +0.05 for gap within 1 ATR (controlled pullback)
- Max confidence: 0.9

---

### 3. PEAD/News Drift Detection

**Purpose**: Capture post-earnings announcement drift and news-driven momentum

**When to Use**: After earnings releases, major news events, analyst upgrades/downgrades

**How to Apply**:

1. **SUE Formula (Standardized Unexpected Earnings)**:
   - SUE = (Actual EPS - Expected EPS) / StdDev(EPS surprises)
   - Threshold: |SUE| > 2.0 for significant surprise

2. **Gap Detection + Sentiment**:
   - Gap > 3% at open (news reaction)
   - Sentiment score > 0.6 (positive) or < -0.6 (negative)
   - Volume > 2x average on gap day

3. **Drift Confirmation**:
   - Price continues in gap direction for 3+ days
   - Each day: Close > Open (for positive drift) or Close < Open (for negative drift)
   - Volume remains elevated (> 1.2x average)

**Example**:

```python
def detect_pead(df, earnings_date, actual_eps, expected_eps, eps_std, sentiment_score):
    sue = (actual_eps - expected_eps) / eps_std

    # Gap day detection
    gap_pct = (df.loc[earnings_date, 'open'] - df.loc[earnings_date - 1, 'close']) / df.loc[earnings_date - 1, 'close']
    volume_spike = df.loc[earnings_date, 'volume'] / df['volume'].rolling(20).mean().loc[earnings_date]

    # Drift confirmation (next 5 days)
    drift_days = df.loc[earnings_date:earnings_date + 5]
    drift_continuation = (drift_days['close'] > drift_days['open']).sum() >= 3

    pead_detected = (
        abs(sue) > 2.0 and
        abs(gap_pct) > 0.03 and
        volume_spike > 2.0 and
        drift_continuation and
        abs(sentiment_score) > 0.6
    )

    confidence = min(0.95, 0.5 + 0.1 * abs(sue) + 0.2 * (volume_spike / 2.0) + 0.15 * abs(sentiment_score))

    return pead_detected, confidence
```

**Confidence Scoring**:

- Base confidence: 0.5
- +0.1 per SUE unit above 2.0 (max +0.3)
- +0.2 for sentiment alignment
- +0.1 for drift continuation 3+ days
- +0.05 for volume persistence
- Max confidence: 0.95

---

### 4. Divergence Detection

**Purpose**: Identify price-indicator disagreement signaling potential reversals

**When to Use**: Extended trends showing exhaustion, overbought/oversold conditions

**How to Apply**:

1. **Regular Divergence** (reversal signal):
   - Bullish: Price makes lower low, RSI/MACD makes higher low
   - Bearish: Price makes higher high, RSI/MACD makes lower high

2. **Hidden Divergence** (continuation signal):
   - Bullish: Price makes higher low, RSI/MACD makes lower low
   - Bearish: Price makes lower high, RSI/MACD makes higher high

3. **Peak/Trough Algorithm**:
   - Identify local extrema: peaks = argrelmax(price, order=5)
   - Compare consecutive peaks/troughs in price vs indicator
   - Require minimum 2 peaks/troughs for divergence

**Example**:

```python
from scipy.signal import argrelextrema

def detect_divergence(df, indicator='rsi', lookback=50):
    # Find peaks and troughs
    price_peaks_idx = argrelextrema(df['close'].values, np.greater, order=5)
    price_troughs_idx = argrelextrema(df['close'].values, np.less, order=5)

    ind_peaks_idx = argrelextrema(df[indicator].values, np.greater, order=5)
    ind_troughs_idx = argrelextrema(df[indicator].values, np.less, order=5)

    # Bearish regular divergence
    if len(price_peaks_idx) >= 2 and len(ind_peaks_idx) >= 2:
        last_price_peaks = df.iloc[price_peaks_idx[-2:]]['close']
        last_ind_peaks = df.iloc[ind_peaks_idx[-2:]][indicator]

        bearish_div = (
            last_price_peaks.iloc[-1] > last_price_peaks.iloc[-2] and
            last_ind_peaks.iloc[-1] < last_ind_peaks.iloc[-2]
        )

    # Bullish regular divergence
    if len(price_troughs_idx) >= 2 and len(ind_troughs_idx) >= 2:
        last_price_troughs = df.iloc[price_troughs_idx[-2:]]['close']
        last_ind_troughs = df.iloc[ind_troughs_idx[-2:]][indicator]

        bullish_div = (
            last_price_troughs.iloc[-1] < last_price_troughs.iloc[-2] and
            last_ind_troughs.iloc[-1] > last_ind_troughs.iloc[-2]
        )

    return bearish_div, bullish_div
```

**Confidence Scoring**:

- Base confidence: 0.4 (divergence is weak signal alone)
- +0.2 for multiple indicator agreement (RSI + MACD)
- +0.1 for volume confirmation (declining volume on divergence)
- +0.1 for overbought/oversold extreme (RSI > 70 or < 30)
- +0.1 for clean peak/trough structure (no noise)
- Max confidence: 0.9

---

## Cross-Pattern Integration

### Multi-Pattern Confirmation

**Strategy**: Combine pattern signals to increase confidence

**Example Scenarios**:

1. **Breakout + PEAD**:
   - Earnings gap breakout above Donchian channel
   - Sentiment confirmation
   - Combined confidence: max(breakout_conf, pead_conf) + 0.1

2. **Pullback + Divergence Resolution**:
   - Bullish divergence forms at EMA support
   - Pullback reclaim triggers entry
   - Combined confidence: (pullback_conf + div_conf) / 2 + 0.15

3. **Breakout + Hidden Divergence**:
   - Breakout confirms trend continuation
   - Hidden divergence shows momentum strength
   - Combined confidence: min(0.95, breakout_conf + 0.15)

**Conflict Resolution**:

- Contradictory signals: Use highest confidence pattern, discount by 0.2
- Time-weighted consensus: Recent patterns (< 5 bars) weighted 2x vs older

---

## Anti-Patterns

### 1. Over-Optimization

**Problem**: Fitting parameters to historical data reduces forward performance
**Alternative**: Use industry-standard defaults (20-day Donchian, 14-day RSI), validate on out-of-sample data

### 2. Ignoring Volume

**Problem**: Price patterns without volume confirmation have high false positive rates
**Alternative**: Require volume > 1.5x average for breakouts, > 1.2x for pullbacks

### 3. Single-Indicator Dependence

**Problem**: Relying on one indicator (e.g., only RSI) increases noise sensitivity
**Alternative**: Multi-indicator confirmation (ADX + RSI + volume for pullbacks)

### 4. Ignoring Market Regime

**Problem**: Applying breakout detection in ranging markets generates whipsaws
**Alternative**: Use ADX < 20 filter to disable breakout signals in non-trending regimes

### 5. Delayed Gap Analysis

**Problem**: Analyzing PEAD patterns days after earnings misses optimal entry
**Alternative**: Real-time sentiment integration, pre-computed SUE forecasts

---

## Integration Points

### DataConnector Protocol

- Requires: OHLCV data with minimum 50-bar lookback for pattern context
- Optional: Earnings dates, sentiment scores, analyst estimates
- Error handling: Graceful degradation if optional data missing (lower confidence)

### Fact Object Mapping

- Pattern type → Fact.category
- Confidence score → Fact.confidence
- Pattern metadata → Fact.metadata (thresholds, indicators used)

### Multi-Indicator Coordination

- Feeds pattern signals to coordination frameworks (Dempster-Shafer, Weighted Voting)
- Receives consensus confidence scores
- See: `development-multi-indicator-coordination.md`

### TA-Lib Integration

- Uses TA-Lib CDL* functions for candlestick patterns
- Falls back to pandas-ta for missing indicators
- See: `development-talib-integration.md`

---

## Sources

1. **Clenow, Andreas F.** (2015). _Stocks on the Move: Beating the Market with Hedge Fund Momentum Strategies_. ISBN: 978-1511466950
   - Breakout detection, momentum scoring, exponential regression

2. **Chan, Ernest P.** (2009). _Quantitative Trading: How to Build Your Own Algorithmic Trading Business_. ISBN: 978-0470284889
   - Mean reversion, pullback strategies, statistical arbitrage

3. **Jegadeesh, Narasimhan & Titman, Sheridan** (1993). "Returns to Buying Winners and Selling Losers: Implications for Stock Market Efficiency". _Journal of Finance_, 48(1), 65-91.
   - Momentum persistence, holding periods

4. **Bernard, Victor L. & Thomas, Jacob K.** (1989). "Post-Earnings-Announcement Drift: Delayed Price Response or Risk Premium?". _Journal of Accounting Research_, 27, 1-36.
   - PEAD framework, SUE formula

5. **Bulkowski, Thomas N.** (2005). _Encyclopedia of Chart Patterns_. ISBN: 978-0471668268
   - Breakout patterns, pullback classification, divergence types

6. **Wilder, J. Welles** (1978). _New Concepts in Technical Trading Systems_. ISBN: 978-0894590276
   - RSI calculation, ADX methodology, ATR usage

7. **TA-Lib Documentation** (2024). <https://ta-lib.org/function.html>
   - CDL pattern functions, indicator reference

8. **pandas-ta Documentation** (2024). <https://github.com/twopirllc/pandas-ta>
   - Fallback indicator implementations

---

**Version**: 1.0
**Last Updated**: 2025-11-16
**Agent**: pattern-detector
