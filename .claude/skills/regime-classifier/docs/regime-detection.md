# Regime Detection Methodology

**Purpose**: Explain the multi-factor approach to market regime classification.

---

## Why 5 Factors?

Single-factor regime classification (e.g., VIX-only) misses critical market dynamics:

| Crisis | VIX Signal | Missed Signals |
|--------|------------|----------------|
| 2008 GFC | HIGH | Credit spreads blew out BEFORE VIX spiked |
| 2011 Euro Crisis | MODERATE | Correlation spike was the leading indicator |
| 2020 COVID | HIGH | Sentiment collapsed, VIX followed |
| 2022 Rate Hikes | MODERATE | Trend broke, VIX remained subdued |

**Lesson**: Multi-factor consensus provides earlier warning and fewer false positives.

---

## Factor Selection Rationale

### 1. Volatility (VIX)

**Why**: Direct measure of expected market turbulence.

**Calculation**: VIX percentile over trailing 252 trading days.

**Thresholds**:
- RED: > 75th percentile (elevated fear)
- GREEN: < 50th percentile (complacency or calm)

### 2. Correlation

**Why**: During stress, correlations spike as diversification breaks down.

**Calculation**: Average pairwise correlation of top 50 S&P 500 stocks to SPY over 60 days.

**Thresholds**:
- RED: > 0.7 (herd behavior, panic selling)
- GREEN: < 0.5 (healthy dispersion)

### 3. Credit Spreads

**Why**: Credit markets often lead equity markets. Widening spreads signal distress.

**Calculation**: HYG (high yield) minus LQD (investment grade) yield spread, percentile over 252 days.

**Thresholds**:
- RED: > 80th percentile (credit stress)
- GREEN: < 50th percentile (healthy credit)

### 4. Sentiment

**Why**: Extreme sentiment (bullish or bearish) often precedes reversals.

**Calculation**: AAII Bull-Bear spread (% bulls minus % bears).

**Thresholds**:
- RED: < -15% (extreme pessimism)
- GREEN: > +15% (healthy optimism, not euphoria)

### 5. Trend

**Why**: Price above/below 200DMA is a simple but powerful regime indicator.

**Calculation**: SPY close vs 200-day moving average.

**Thresholds**:
- RED: Below 200DMA (bear market territory)
- GREEN: Above 200DMA (bull market territory)

---

## Historical Regime Classification

### March 2020 (COVID Crash)

| Factor | Value | Signal |
|--------|-------|--------|
| VIX | 82.69 (99th) | RED |
| Correlation | 0.89 | RED |
| Credit | 95th | RED |
| Sentiment | -41% | RED |
| Trend | Below | RED |

**Regime**: HIGH_RISK (5/5 RED)
**Confidence**: 0.98

### January 2018 (Volatmageddon)

| Factor | Value | Signal |
|--------|-------|--------|
| VIX | 37 (85th) | RED |
| Correlation | 0.72 | RED |
| Credit | 42nd | GREEN |
| Sentiment | +28% | NEUTRAL |
| Trend | Above | GREEN |

**Regime**: ELEVATED (2/5 RED)
**Confidence**: 0.85

### 2017 (Low Vol Year)

| Factor | Value | Signal |
|--------|-------|--------|
| VIX | 11 (15th) | GREEN |
| Correlation | 0.38 | GREEN |
| Credit | 22nd | GREEN |
| Sentiment | +18% | GREEN |
| Trend | Above | GREEN |

**Regime**: LOW_RISK (5/5 GREEN)
**Confidence**: 0.95

---

## Regime Transition Patterns

Typical sequences observed:

```
LOW_RISK -> NORMAL -> ELEVATED -> HIGH_RISK (gradual stress build)
HIGH_RISK -> ELEVATED -> NORMAL (recovery, often faster than decline)
NORMAL -> HIGH_RISK (shock events, rare but possible)
```

**Average regime duration** (2000-2023):
- HIGH_RISK: 2-4 months
- ELEVATED: 1-3 months
- NORMAL: 6-12 months
- LOW_RISK: 3-6 months

---

## Backtesting Implications

When backtesting across regimes:

1. **Stratify results by regime**: A strategy that works in LOW_RISK but fails in HIGH_RISK is regime-dependent.

2. **Test regime transitions**: Entry/exit behavior during regime changes reveals robustness.

3. **Don't optimize per-regime**: That's curve fitting. Use regime as context, not as a parameter.

4. **Report regime CV**: Coefficient of variation of Sharpe across regimes. CV > 0.5 indicates regime sensitivity.
