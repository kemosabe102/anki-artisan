# News Impact Analyzer Documentation

Domain knowledge and methodology documentation for the news-impact-analyzer agent.

## Contents

| Document | Description |
|----------|-------------|
| [regime-classification.md](regime-classification.md) | 5-factor regime methodology and thresholds |
| [impact-formula.md](impact-formula.md) | Impact calculation with worked examples |
| [escalation-patterns.md](escalation-patterns.md) | New/escalating/de-escalating classification |
| [scenario-generation.md](scenario-generation.md) | Bear/base/bull probability modeling |

## Quick Reference

### Core Formula

```
adjusted_impact = baseline_impact * regime_multiplier * escalation_adjustment * (1 + contagion_premium)
```

### Regime Thresholds

| Regime | Score Range | Multiplier |
|--------|-------------|------------|
| risk_off | 0-30 | 1.5x |
| neutral | 31-69 | 1.0x |
| risk_on | 70-100 | 0.7x |

### Default Scenario Probabilities

| Scenario | Probability | Typical Trigger |
|----------|-------------|-----------------|
| Bear | 25% | Escalation, contagion |
| Base | 55% | Current trajectory |
| Bull | 20% | Resolution, containment |

### Key Thresholds

| Parameter | Default | Range |
|-----------|---------|-------|
| Min severity | 50 | 0-100 |
| Stale data warning | 7 days | - |
| Max events/day | 50 | - |
| Confidence floor | 0.50 | 0-1 |
