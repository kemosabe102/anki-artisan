# Scenario Generation

## Overview

Each impact prediction includes three scenarios (bear/base/bull) with probability distributions and trigger conditions. This enables decision-makers to assess risk across different outcome paths.

## Default Probability Distribution

| Scenario | Default Probability | Condition |
|----------|---------------------|-----------|
| Bear | 25% | Adverse developments |
| Base | 55% | Current trajectory continues |
| Bull | 20% | Favorable resolution |

## Probability Adjustment Rules

### Regime-Based Adjustments

| Regime | Bear Adj | Base Adj | Bull Adj |
|--------|----------|----------|----------|
| risk_off | +10% | -5% | -5% |
| neutral | 0% | 0% | 0% |
| risk_on | -5% | -5% | +10% |

### Escalation-Based Adjustments

| Status | Bear Adj | Base Adj | Bull Adj |
|--------|----------|----------|----------|
| escalating | +10% | -5% | -5% |
| stable | 0% | 0% | 0% |
| de-escalating | -10% | 0% | +10% |

### Combined Example

Regime: risk_off, Status: escalating
- Bear: 25% + 10% + 10% = 45%
- Base: 55% - 5% - 5% = 45%
- Bull: 20% - 5% - 5% = 10%


## Time Horizon Modeling

Each scenario includes 1D, 1W, and 1M projections:

### Impact Decay Curve

```python
# Bear case: Impact compounds over time
impact_1d = adjusted_impact * 0.6
impact_1w = adjusted_impact * 1.0
impact_1m = adjusted_impact * 1.2

# Base case: Impact then partial recovery
impact_1d = adjusted_impact * 0.7
impact_1w = adjusted_impact * 0.85
impact_1m = adjusted_impact * 0.75

# Bull case: Quick recovery
impact_1d = adjusted_impact * 0.5
impact_1w = adjusted_impact * 0.3
impact_1m = adjusted_impact * 0.1  # or positive
```

## Trigger Conditions

Each scenario must specify a trigger condition:

### Bear Case Triggers
- "Military escalation"
- "Policy error (rate hike during stress)"
- "Contagion to additional sectors"
- "Key support level broken"
- "Credit event spillover"

### Base Case Triggers
- "Current trajectory continues"
- "Gradual de-escalation"
- "Contained to affected sectors"
- "Policy response as expected"

### Bull Case Triggers
- "Diplomatic resolution"
- "Policy pivot (dovish surprise)"
- "Faster-than-expected containment"
- "Technical oversold bounce"


## Composite Metrics

### Macro Shock Index (MSI)

Aggregate measure of systemic risk (0-100):

```python
msi = sum(event_severity * event_weight for event in events) / total_weight
```

Where `event_weight` = 1 + (regime_multiplier - 1) * 0.5

### Sector Sensitivity Index (SSI)

Per-sector impact exposure:

```python
ssi[sector] = sum(
    adjusted_impact * sector_weight 
    for event in events 
    if sector in event.sectors_affected
)
```

## Validation Rules

1. Probabilities must sum to ~100% (95-105% acceptable due to rounding)
2. Bear case impact must be <= base case impact
3. Bull case impact must be >= base case impact
4. All scenarios must have non-empty trigger strings
5. 1M impact magnitude should be >= 1W impact for bear case
