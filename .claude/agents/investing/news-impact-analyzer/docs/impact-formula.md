# Impact Calculation Formula

## Core Formula

```
adjusted_impact = baseline_impact * regime_multiplier * confidence_scaling * escalation_adjustment * (1 + contagion_premium)
```

## Component Breakdown

### 1. Baseline Impact

Historical average impact from analogous events:
- Query attention_daily for events with similar category AND severity (+-15 points)
- Calculate average 1-week market impact from historical data
- Minimum 3 analogues required, else flag as "novel"

```sql
SELECT AVG(market_impact_1w) as baseline
FROM attention_daily
WHERE category = $category
  AND severity BETWEEN $severity - 15 AND $severity + 15
  AND recorded_at < $analysis_date
ORDER BY recorded_at DESC
LIMIT 20;
```

### 2. Regime Multiplier

Combined regime and structural fragility:

```
regime_multiplier = regime_base * fragility_amplification
```

**Regime Base**:
| Classification | Base Multiplier |
|----------------|-----------------|
| risk_off | 1.5 |
| neutral | 1.0 |
| risk_on | 0.7 |


**Fragility Amplification** (Dalio framework):

| Dimension | Value | Amplification |
|-----------|-------|---------------|
| debt_cycle_phase | EARLY | 0.8x |
| debt_cycle_phase | MID | 1.0x |
| debt_cycle_phase | LATE | 1.3x |
| debt_cycle_phase | DELEVERAGING | 1.5x |
| policy_bias | EASING | 0.85x |
| policy_bias | NEUTRAL | 1.0x |
| policy_bias | TIGHTENING | 1.3x |
| inflation_regime | DISINFLATION | 0.9x |
| inflation_regime | STABLE | 1.0x |
| inflation_regime | REFLATION | 1.1x |
| inflation_regime | STAGFLATION | 1.4x |

Combined: `fragility = debt_amp * policy_amp * inflation_amp`

### 3. Escalation Adjustment

Based on event trajectory classification:

| Status | Adjustment | Logic |
|--------|------------|-------|
| new | 1.0 | No history to compare |
| escalating | 1.2 (+20%) | Severity increasing over time |
| stable | 1.0 | No change in trajectory |
| de-escalating | 0.85 (-15%) | Severity decreasing |

### 4. Contagion Premium

Cross-sector spillover risk (0.0 to 0.15):

```python
contagion = base_contagion * sector_exposure_factor
```

Where:
- `base_contagion`: 0.05 per major sector affected beyond primary
- `sector_exposure_factor`: 1.0-1.5 based on current portfolio exposure

### 5. Confidence Scaling (Skepticism-First)

Scales impact based on event confidence to prevent overreaction to low-quality signals:

```
confidence_scaling = min(1.3, event_confidence / 0.75)
```

| Event Confidence | Scaling Factor | Rationale |
|------------------|----------------|-----------|
| 0.50 (floor) | 0.67x | Minimum executable, high skepticism |
| 0.60 | 0.80x | Below reference, reduced weight |
| 0.75 (reference) | 1.00x | Baseline - standard confidence |
| 0.90 | 1.20x | High confidence, amplified weight |
| 0.95 | 1.27x | Maximum confidence (capped at 1.3x) |

**Why 0.75 as reference?** The skepticism-first framework assumes moderate skepticism by default. An event must demonstrate high confidence (>0.75) to have amplified impact.

## Worked Example

**Input**:
- Event: China-Taiwan tensions
- Category: geopolitical
- Severity: 72
- Event Confidence: 0.72
- Regime: risk_off (score: 28)
- Fragility: LATE cycle, TIGHTENING, STAGFLATION

**Step 1: Baseline Impact**
- 5 historical analogues found: avg impact = -6.1%

**Step 2: Regime Multiplier**
- regime_base = 1.5 (risk_off)
- debt_amp = 1.3 (LATE)
- policy_amp = 1.3 (TIGHTENING)
- inflation_amp = 1.4 (STAGFLATION)
- fragility = 1.3 * 1.3 * 1.4 = 2.366
- regime_multiplier = 1.5 * 2.366 = 3.55 (capped at 2.7)

**Step 3: Escalation**
- Status: escalating (third week of tensions)
- escalation_adjustment = 1.2

**Step 4: Contagion**
- Sectors: semiconductors, technology, shipping (3 sectors)
- contagion_premium = 0.05 * 2 = 0.10 (2 beyond primary)

**Step 5: Confidence Scaling**
- confidence_scaling = min(1.3, 0.72 / 0.75) = 0.96

**Final Calculation**:
```
adjusted_impact = -6.1 * 2.7 * 0.96 * 1.2 * 1.10 = -20.9%
```
