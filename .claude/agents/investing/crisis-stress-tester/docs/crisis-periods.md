# Historical Crisis Periods

## Purpose

Defines historical market crisis periods used for stress testing strategies. Each period represents a distinct type of market stress that strategies must survive.

---

## GFC 2008 (Global Financial Crisis)

### Period Definition
- **Start**: 2008-09-01 (pre-Lehman)
- **End**: 2009-03-31 (market bottom + initial recovery)
- **Duration**: 7 months

### Market Characteristics
- **Trigger**: Lehman Brothers bankruptcy (Sept 15, 2008)
- **Type**: Credit/liquidity crisis
- **VIX Peak**: 89.53 (Nov 20, 2008)
- **Correlation**: Spike to 0.9+ across asset classes
- **Liquidity**: Severe dislocation, wide spreads

### Benchmark Performance
- **S&P 500 Drawdown**: -57% (peak to trough)
- **Recovery Time**: ~4 years to previous highs
- **Worst Month**: October 2008 (-16.9%)

### Gate Threshold
```
CRISIS_2008_SURVIVE: Strategy DD < 2x S&P DD (-114%)
```

**Rationale**: A strategy that loses more than 2x the market in a crisis has unacceptable tail risk. The 2x multiplier allows for leveraged or concentrated strategies while setting a hard ceiling.

---

## COVID 2020 (Fastest Bear Market)

### Period Definition
- **Start**: 2020-02-19 (all-time high)
- **End**: 2020-03-23 (market bottom)
- **Duration**: 33 calendar days (22 trading days)

### Market Characteristics
- **Trigger**: Global pandemic, lockdowns, economic shutdown
- **Type**: Exogenous shock, liquidity crisis
- **VIX Peak**: 82.69 (March 16, 2020)
- **Speed**: Fastest 30% decline in history
- **Recovery**: V-shaped, new highs by August 2020

### Benchmark Performance
- **S&P 500 Drawdown**: -34% (peak to trough)
- **Recovery Time**: ~6 months to previous highs
- **Worst Week**: March 16-20 (-15%)

### Gate Threshold
```
CRISIS_2020_SURVIVE: Strategy DD < 50%
```

**Rationale**: The 50% threshold accounts for the unprecedented speed of the decline. Strategies that lost more than 50% in 33 days likely have structural vulnerabilities to rapid drawdowns.

---

## Rate Hike 2022 (Fed Tightening Cycle)

### Period Definition
- **Start**: 2022-01-01 (pre-tightening)
- **End**: 2022-10-31 (market bottom)
- **Duration**: 10 months

### Market Characteristics
- **Trigger**: Aggressive Fed rate hikes (0% to 4%)
- **Type**: Monetary policy shock, multiple compression
- **VIX Average**: ~25-30 (elevated but not panic)
- **Rotation**: Growth to value, tech devastation
- **Bond Correlation**: Unusual positive stock-bond correlation

### Benchmark Performance
- **S&P 500 Drawdown**: -27% (peak to trough)
- **Nasdaq Drawdown**: -38%
- **Bond Index (AGG)**: -18%
- **60/40 Portfolio**: Worst year since 1937

### Gate Threshold
```
CRISIS_2022_SURVIVE: Strategy Sharpe > 0 OR DD < 30%
```

**Rationale**: This was a grinding bear market, not a crash. Strategies should either maintain positive risk-adjusted returns (Sharpe > 0) or limit losses to slightly worse than the index. The OR condition allows different strategy types to pass.

---

## Flash Crash 2010 (Optional)

### Period Definition
- **Date**: 2010-05-06 (single day)
- **Duration**: Intraday event (~36 minutes)

### Market Characteristics
- **Trigger**: Algorithmic trading cascade
- **Type**: Technical/liquidity event
- **S&P 500 Intraday**: -9% then recovery
- **Individual Stocks**: Some dropped 99%+ briefly

### Usage
- **Optional**: Only for intraday strategies
- **Gate**: Strategy must not trigger stop-losses on false prices

---

## Period Selection Guidelines

### For Full Crisis Suite
Test ALL three major periods (2008, 2020, 2022) because:
1. Each represents different crisis type (credit, exogenous, monetary)
2. Different market dynamics (crash vs grind)
3. Different correlation/rotation patterns

### For Single Crisis Testing
Use when:
- Initial validation (start with 2008 as most severe)
- Debugging a specific failure mode
- Strategy designed for specific regime

### For Synthetic Scenarios
Use AFTER historical crises pass to test:
- Scenarios worse than historical
- Custom combinations
- Strategy-specific stress points
