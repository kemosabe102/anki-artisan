# Regime-Adaptive Pattern Selection Reference

Market regime classification using ADX and pattern selection guidelines per regime.

---

## Regime Classification

### ADX-Based Classification

| Regime | ADX Condition | Secondary | Description |
|--------|---------------|-----------|-------------|
| **Trending** | ADX > 25 | - | Strong directional movement |
| **Ranging** | ADX < 20 | BB width < 20th pct | Sideways, low volatility |
| **Volatile** | Any | ATR > 80th percentile | High volatility, news-driven |
| **Transitional** | 20-25 | - | Regime uncertain |

### Classification Code

```python
def classify_regime(adx, atr_percentile, bb_width_percentile):
    if atr_percentile > 80:
        return 'volatile'
    if adx > 25:
        return 'trending'
    if adx < 20 and bb_width_percentile < 20:
        return 'ranging'
    return 'transitional'
```

---

## Pattern Selection by Regime

### Trending Regime (ADX > 25)

| Pattern | Priority | Rationale |
|---------|----------|-----------|
| Breakout | HIGH | Momentum continuation likely |
| Pullback | HIGH | Entry on retracement |
| Hidden Divergence | MEDIUM | Confirms trend strength |
| Regular Divergence | LOW | Counter-trend, higher risk |

**Indicator Weights**:
- Trend indicators (ADX, EMA): 0.4
- Momentum (RSI, MACD): 0.3
- Volume: 0.2
- Volatility: 0.1

### Ranging Regime (ADX < 20)

| Pattern | Priority | Rationale |
|---------|----------|-----------|
| Regular Divergence | HIGH | Mean reversion signal |
| Support/Resistance | HIGH | Price oscillates between levels |
| Breakout | LOW | High false positive rate |
| Pullback | DISABLED | No clear trend |

**Indicator Weights**:
- Oscillators (RSI, Stochastic): 0.4
- Volume: 0.3
- Trend indicators: 0.2
- Volatility: 0.1

### Volatile Regime (ATR > 80th percentile)

| Pattern | Priority | Rationale |
|---------|----------|-----------|
| PEAD | HIGH | News-driven, momentum follows |
| Breakout | MEDIUM | Volume confirms direction |
| All others | LOW | High noise, low reliability |

**Indicator Weights**:
- Sentiment: 0.4
- Volume: 0.3
- Price action: 0.2
- Oscillators: 0.1

---

## Regime Transition Handling

### Detection

```python
def detect_regime_change(df, lookback=20):
    current_regime = classify_regime(df['adx_14'].iloc[-1], ...)
    prev_regime = classify_regime(df['adx_14'].iloc[-lookback], ...)
    return current_regime != prev_regime
```

### Transition Rules

| From | To | Action |
|------|-----|--------|
| Trending | Ranging | Disable breakout, enable divergence |
| Ranging | Trending | Enable breakout, disable S/R |
| Any | Volatile | Enable PEAD, apply 0.8x confidence penalty |

### Confidence Penalty

```python
if regime_change_detected:
    confidence *= 0.8  # 20% penalty
    output['flags'].append('regime_change_mid_analysis')
```

---

## ADX Calculation Reference

### Formula
```
DI+ = 100 * EMA(+DM) / ATR
DI- = 100 * EMA(-DM) / ATR
DX = 100 * |DI+ - DI-| / (DI+ + DI-)
ADX = EMA(DX, period=14)
```

### Interpretation

| ADX Value | Trend Strength |
|-----------|----------------|
| 0-25 | Absent or weak |
| 25-50 | Strong |
| 50-75 | Very strong |
| 75-100 | Extremely strong (rare) |

---

## Configuration Defaults

```python
REGIME_CONFIG = {
    'trending': {
        'adx_threshold': 25,
        'patterns': ['breakout', 'pullback', 'hidden_divergence'],
        'coordination': 'weighted_voting'
    },
    'ranging': {
        'adx_threshold': 20,
        'patterns': ['regular_divergence', 'support_resistance'],
        'coordination': 'consensus_threshold'
    },
    'volatile': {
        'atr_percentile': 80,
        'patterns': ['pead'],
        'coordination': 'dempster_shafer'
    }
}
```

---

## Anti-Patterns

| Anti-Pattern | Why Wrong | Correct Approach |
|--------------|-----------|------------------|
| Static regime assumption | Markets change | Re-classify every N bars |
| ADX-only classification | Misses volatility | Include ATR percentile |
| No transition penalty | False confidence | Apply 0.8x on regime change |
| Same weights all regimes | Sub-optimal signals | Regime-adaptive weighting |
