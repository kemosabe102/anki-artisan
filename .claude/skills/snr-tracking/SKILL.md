---
name: snr-tracking
description: >
  Signal-to-Noise Ratio tracking for pattern confidence sustainability.
  Monitors pattern quality degradation and generates sustainability metrics.
  Trigger keywords: SNR, signal noise, pattern quality, degradation tracking, pattern sustainability.
---

# SNR Tracking Skill

*Measuring pattern signal strength relative to market noise*

## Purpose

Track pattern quality over time using Signal-to-Noise Ratio (SNR) metrics. Identifies when patterns are degrading (becoming more noise than signal) and recommends position sizing adjustments.

## Core Philosophy

> "More noise than signal in markets. Be skeptical first."

Patterns can degrade over time due to:
- Crowding (too many traders exploiting the pattern)
- Regime changes (pattern no longer fits market conditions)
- Capacity exhaustion (pattern collapses under capital weight)


## SNR Formulas

### Basic SNR
```
SNR = Mean(Pattern Return) / StdDev(Pattern Return)
```

### SNR in dB (Decibel Scale)
```
SNR_dB = 10 × log10(signal_power / noise_power)
```

### Rolling SNR
```
Rolling_SNR_20 = SNR calculated over last 20 trades
```

## Metrics Tracked

| Metric | Formula | Healthy Threshold | Degradation Trigger |
|--------|---------|-------------------|---------------------|
| Current SNR | Mean/StdDev of returns | >= 1.0 | < 1.0 |
| Rolling SNR (20) | 20-trade rolling window | >= 1.0 | < 1.0 for 3 periods |
| SNR Decay Rate | (SNR_t - SNR_t-n) / n | > -0.05/month | < -0.1/month |
| Confidence CV | StdDev(conf) / Mean(conf) | < 0.3 | > 0.5 |


## Degradation Status Classification

| Status | Criteria | Action |
|--------|----------|--------|
| **STABLE** | SNR >= 1.0, decay rate > -0.05 | Continue normal sizing |
| **DEGRADING** | SNR < 1.0 for 3+ periods OR decay < -0.1 | Reduce position sizing by 25% |
| **CRITICAL** | SNR < 0.5 OR decay < -0.2 | Reduce sizing by 50%, flag for review |
| **EXPIRED** | SNR < 0.3 for 5+ periods | Suspend pattern, move to graveyard |

## Recommendations by Status

| Status | Position Sizing Adjustment | Review Frequency |
|--------|---------------------------|------------------|
| STABLE | Full confidence scaling | Monthly |
| DEGRADING | × 0.75 multiplier | Weekly |
| CRITICAL | × 0.50 multiplier | Daily |
| EXPIRED | × 0.00 (no trading) | Immediate |


## Integration

### Upstream (Inputs)
- Pattern detector confidence scores
- Trade entry/exit prices and timestamps
- Regime classification

### Downstream (Outputs)
- Sustainability metrics for pattern detector output
- Degradation alerts to hypothesis tracking
- Position sizing adjustments to risk management

## Usage

### Calculate SNR for Pattern
```
Input: {pattern_type, ticker, trades[]}
Output: {
  current_snr: number,
  rolling_snr_20: number,
  snr_decay_rate_monthly: number,
  degradation_status: STABLE|DEGRADING|CRITICAL|EXPIRED,
  recommendation: CONTINUE|REDUCE_SIZING|SUSPEND|RETIRE
}
```


### Check Pattern Sustainability
```
Input: {pattern_type, ticker, lookback_days: 90}
Output: {
  sustainability_score: 0-100,
  historical_snr: number[],
  trend: IMPROVING|STABLE|DECLINING,
  degradation_risk: LOW|MEDIUM|HIGH
}
```

## Anti-Patterns

| Anti-Pattern | Why Problematic | Correct Approach |
|--------------|-----------------|------------------|
| Ignoring SNR degradation | Continued trading on dying patterns | Monitor and reduce sizing |
| Short lookback windows | Insufficient data for trend | Use 20+ trades minimum |
| Ignoring regime context | SNR varies by regime | Calculate SNR within regime |

## Related Skills

- `hypothesis-formulation` - Cause→Effect→Why structure
- `hypothesis-tracking` - Trial management and graveyard
- `regime-classifier` - Market regime detection

## Schema

See `schemas/pattern-sustainability.schema.json` for detailed output schema.
