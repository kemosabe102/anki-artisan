# TA-Lib Wrapper Reference

Integration patterns for TA-Lib with pandas-ta fallback.

---

## Library Priority

1. **TA-Lib** (primary): C-based, fastest, industry standard
2. **pandas-ta** (fallback): Pure Python, portable, slower

---

## Fallback Detection

```python
try:
    import talib
    USE_TALIB = True
except ImportError:
    import pandas_ta as ta
    USE_TALIB = False
```

---

## Function Mapping

| Indicator | TA-Lib Function | pandas-ta Equivalent |
|-----------|-----------------|---------------------|
| EMA | `talib.EMA(close, timeperiod)` | `ta.ema(close, length)` |
| RSI | `talib.RSI(close, timeperiod)` | `ta.rsi(close, length)` |
| ATR | `talib.ATR(high, low, close, timeperiod)` | `ta.atr(high, low, close, length)` |
| ADX | `talib.ADX(high, low, close, timeperiod)` | `ta.adx(high, low, close, length)` |
| OBV | `talib.OBV(close, volume)` | `ta.obv(close, volume)` |
| MFI | `talib.MFI(high, low, close, volume, timeperiod)` | `ta.mfi(high, low, close, volume, length)` |


---

## Indicator Formulas

### EMA (Exponential Moving Average)

```
EMA_t = (Price_t * k) + (EMA_{t-1} * (1-k))
k = 2 / (n + 1)
```

- **Default lookback**: 20
- **Range**: 5-200

### RSI (Relative Strength Index)

```
RSI = 100 - (100 / (1 + RS))
RS = AvgGain / AvgLoss
```

- **Default lookback**: 14
- **Overbought**: > 70
- **Oversold**: < 30

### ATR (Average True Range)

```
ATR = SMA(TrueRange, n)
TrueRange = max(H-L, abs(H-C_prev), abs(L-C_prev))
```

- **Default lookback**: 14
- **Use**: Position sizing, stop-loss placement


### ADX (Average Directional Index)

```
ADX = SMA(DX, n)
DX = abs(+DI - -DI) / (+DI + -DI)
```

- **Default lookback**: 14
- **Strong trend**: > 25
- **Weak trend**: < 20

### OBV (On-Balance Volume)

```
OBV_t = OBV_{t-1} + (Volume if Close > Close_prev else -Volume)
```

- **Cumulative indicator** (no lookback)
- **Use**: Accumulation/distribution flow

### MFI (Money Flow Index)

```
MFI = 100 - (100 / (1 + MF_Ratio))
MF_Ratio = Positive_MF / Negative_MF
```

- **Default lookback**: 14
- **Volume-weighted RSI**

---

## Default Lookback Periods

| Indicator | Default | Range |
|-----------|---------|-------|
| RSI | 14 | 7-21 |
| ATR | 14 | 10-20 |
| ADX | 14 | 10-20 |
| EMA | 20 | 5-200 |
| MFI | 14 | 10-20 |
