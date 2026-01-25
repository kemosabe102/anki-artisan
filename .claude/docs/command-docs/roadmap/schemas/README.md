# Roadmap Command Schemas

Schema documentation for the `/roadmap` command.

## Files

| File | Purpose |
|------|---------|
| (none yet) | Output schemas to be added as needed |

## Schema Categories

Potential schemas for future addition:
- `health-report.schema.json` - Structure of health dashboard output
- `dimension-scores.schema.json` - Health dimension scoring format
- `recommendation.schema.json` - Action recommendation structure

## Output Structure (Informal)

### Health Dashboard

```text
Overall Score: 0.0-1.0 (letter grade A-F)
Date: ISO date
Files: count (active count, archive count)

Dimensions:
  - Progressive Disclosure: score (grade)
  - Token Density: score (grade)
  - Cross-Ref Integrity: score (grade)
  - Sprint Compliance: score (grade)
  - Freshness: score (grade)
  - Completeness: score (grade)

Top 5 Actions:
  - Description (impact, effort, confidence) -> suggested command
```

### Dimension Weights

```text
CrossRefIntegrity:  0.20
ProgDisclosure:     0.25
SprintCompliance:   0.15
Completeness:       0.10
Freshness:          0.10
TokenDensity:       0.20
```
