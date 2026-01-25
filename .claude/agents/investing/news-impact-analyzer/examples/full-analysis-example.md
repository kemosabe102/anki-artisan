# Full Analysis Example

Complete walkthrough of a daily news impact analysis.

## Input

```json
{
  "date": "2026-01-04",
  "category_filter": "all",
  "min_severity": 40
}
```

## Step 1: Regime Classification

Query risk_sentiment table:
```sql
SELECT composite_score, vix_inverse, fear_greed_index, 
       hy_spread_normalized, put_call_ratio, recorded_at
FROM risk_sentiment
WHERE recorded_at <= '2026-01-04'
ORDER BY recorded_at DESC LIMIT 1;
```

Result: composite_score = 28 (risk_off)

## Step 2: Structural Fragility

Query structural_fragility table:
```sql
SELECT debt_cycle_phase, policy_bias, inflation_regime, recorded_at
FROM structural_fragility
WHERE recorded_at <= '2026-01-04'
ORDER BY recorded_at DESC LIMIT 1;
```

Result: LATE cycle, TIGHTENING policy, STAGFLATION
Fragility amplification: 1.3 * 1.3 * 1.4 = 2.366 (capped at 1.8)


## Step 3: Query Risk Events

```sql
SELECT event_id, category, severity, confidence, 
       escalation_status, sectors_affected
FROM attention_daily
WHERE recorded_at = '2026-01-04'
  AND severity >= 40
ORDER BY severity DESC;
```

Result: 4 events found

## Step 4: Historical Analogues

For top event (severity 72, geopolitical):
```sql
SELECT event_date, event_name, market_impact_1w
FROM attention_daily
WHERE category = 'geopolitical'
  AND severity BETWEEN 57 AND 87
  AND recorded_at < '2026-01-04'
ORDER BY recorded_at DESC LIMIT 10;
```

Result: 5 analogues, avg impact = -6.1%

## Step 5: Impact Calculation

```
baseline_impact = -6.1%
regime_base = 1.5 (risk_off)
fragility_amp = 1.4 (capped)
regime_multiplier = 1.5 * 1.4 = 2.1
escalation_adj = 1.2 (escalating)
contagion_premium = 0.08 (3 sectors)

adjusted_impact = -6.1 * 2.1 * 1.2 * 1.08 = -16.6%
```


## Step 6: Scenario Generation

Base probabilities adjusted for risk_off + escalating:
- Bear: 25% + 10% + 10% = 45%
- Base: 55% - 5% - 5% = 45%
- Bull: 20% - 5% - 5% = 10%

## Complete Output

```json
{
  "status": "SUCCESS",
  "analysis_date": "2026-01-04",
  "regime_context": {
    "classification": "risk_off",
    "score": 28,
    "multiplier": 1.5,
    "fragility_amplification": 1.4,
    "total_multiplier": 2.1,
    "macro_context": {
      "debt_cycle_phase": "LATE",
      "policy_bias": "TIGHTENING",
      "inflation_regime": "STAGFLATION"
    },
    "data_freshness": {
      "risk_sentiment_age_days": 0,
      "fragility_age_days": 3
    }
  },
  "events_analyzed": 4,
  "impact_predictions": [
    {
      "event_id": "geopolitical_china_taiwan_2025_q1",
      "category": "geopolitical",
      "severity": 72,
      "confidence": 0.85,
      "baseline_impact": -6.1,
      "adjusted_impact": -16.6,
      "escalation_status": "escalating",
      "escalation_adjustment": 0.2,
      "contagion_premium": 0.08,
      "historical_analogues": [
        {"date": "2022-09-15", "event": "Taiwan Strait Tensions", "impact_1w": -4.2},
        {"date": "2023-04-10", "event": "China Military Exercises", "impact_1w": -3.8}
      ],
      "scenarios": {
        "bear_case": {
          "1d": -10.0,
          "1w": -16.6,
          "1m": -20.0,
          "probability": 0.45,
          "trigger": "military escalation"
        },
        "base_case": {
          "1d": -8.0,
          "1w": -14.1,
          "1m": -12.5,
          "probability": 0.45,
          "trigger": "current trajectory"
        },
        "bull_case": {
          "1d": -5.0,
          "1w": -5.0,
          "1m": -1.7,
          "probability": 0.10,
          "trigger": "diplomatic resolution"
        }
      },
      "sectors_affected": ["semiconductors", "technology", "shipping"],
      "key_risks": ["Escalation beyond parameters", "Regime shift if fragility increases"]
    }
  ],
  "composite_metrics": {
    "msi_macro_shock_index": 58,
    "ssi_by_sector": {
      "technology": 72,
      "industrials": 45,
      "financials": 38
    }
  },
  "next_observation_points": [
    "24-48 hrs: Watch for diplomatic signaling",
    "Week 1: Monitor escalation intensity"
  ]
}
```
