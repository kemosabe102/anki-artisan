# Threshold Calibration

**Purpose**: Document the empirical basis for regime classification thresholds.

---

## Threshold Summary

| Factor | RED | NEUTRAL | GREEN | Source |
|--------|-----|---------|-------|--------|
| VIX percentile | > 75th | 50-75th | < 50th | 1990-2023 distribution |
| Correlation | > 0.7 | 0.5-0.7 | < 0.5 | Crisis correlation analysis |
| Credit spread | > 80th | 50-80th | < 50th | HYG-LQD spread history |
| Sentiment | < -15% | -15% to +15% | > +15% | AAII historical extremes |
| Trend | Below 200DMA | - | Above 200DMA | Binary classification |

---

## VIX Percentile Thresholds

**Data**: VIX daily closes 1990-01-02 to 2023-12-31

| Percentile | VIX Level | Regime Signal |
|------------|-----------|---------------|
| 25th | 12.8 | GREEN zone |
| 50th | 17.2 | Neutral boundary |
| 75th | 23.5 | RED zone entry |
| 90th | 30.2 | Elevated stress |
| 95th | 35.8 | Crisis territory |

**Rationale**: 75th percentile (~24 VIX) historically corresponds to market corrections. Below 50th percentile indicates complacency or genuine low-risk environment.

---

## Correlation Thresholds

**Data**: S&P 500 top 50 stocks pairwise correlation, 2000-2023

| Regime | Avg Correlation | Events |
|--------|-----------------|--------|
| Normal | 0.35-0.55 | Typical trading |
| Elevated | 0.55-0.70 | Sector rotations, mild stress |
| Crisis | > 0.70 | 2008, 2011, 2020 (everything sells together) |

**Rationale**: Correlation > 0.7 indicates panic selling where diversification fails. This is a leading indicator of regime stress.

---

## Credit Spread Thresholds

**Data**: HYG-LQD yield spread, 2007-2023

| Percentile | Spread (bps) | Interpretation |
|------------|--------------|----------------|
| 25th | 280 | Credit optimism |
| 50th | 350 | Normal spreads |
| 80th | 480 | Stress emerging |
| 95th | 650+ | Crisis (2008, 2020) |

**Rationale**: Credit spreads widen before equity markets fully price in distress. 80th percentile provides early warning.


---

## Sentiment Thresholds

**Data**: AAII Bull-Bear spread, 1987-2023

| Spread | Interpretation | Historical Frequency |
|--------|----------------|---------------------|
| > +30% | Euphoria (contrarian sell) | 5% of weeks |
| +15% to +30% | Healthy optimism | 25% of weeks |
| -15% to +15% | Neutral | 50% of weeks |
| -15% to -30% | Pessimism | 15% of weeks |
| < -30% | Extreme fear (contrarian buy) | 5% of weeks |

**Rationale**: -15% Bull-Bear spread indicates meaningful pessimism. Below -30% often marks bottoms, but we use -15% for regime classification (not timing).

---

## Trend Thresholds

**Binary Classification**:
- **Below 200DMA**: Bear market territory (RED)
- **Above 200DMA**: Bull market territory (GREEN)

**Historical performance**:
- SPY above 200DMA: Average annual return +12.8%
- SPY below 200DMA: Average annual return -4.2%

**No neutral zone**: Trend is binary for regime classification purposes.


---

## Threshold Stability

These thresholds are calibrated on long-term data and should remain stable. Review annually for:

1. **Regime shift**: If VIX baseline permanently rises (e.g., new normal = 20), adjust percentile calculation window
2. **Market structure**: ETF growth, algo trading may affect correlation dynamics
3. **Credit market evolution**: New instruments may require spread recalibration

**Last calibration**: 2024-01-15
**Next review**: 2025-01-15

---

## Sensitivity Analysis

Impact of threshold changes on regime classification frequency (2020-2023):

| Threshold Change | HIGH_RISK Days | Impact |
|-----------------|----------------|--------|
| VIX 75th → 70th | +12% | More false positives |
| VIX 75th → 80th | -8% | Slower detection |
| Corr 0.7 → 0.65 | +15% | Catches more stress |
| Corr 0.7 → 0.75 | -18% | Misses mild stress |

**Recommendation**: Maintain current thresholds. They balance sensitivity and specificity.
