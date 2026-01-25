# Data Validator - Documentation

## Overview

The **data-validator** agent audits daily news collection quality from the `attention_daily` Postgres table. It validates completeness across 5 risk categories, confidence thresholds, source diversity, and escalation tracking.

## Purpose

Ensure the news collection pipeline produces reliable data for downstream impact analysis. Identify gaps before they affect trading decisions.

## Key Capabilities

1. **Category Coverage** - Validates all 5 risk categories have events
2. **Confidence Validation** - Checks minimum thresholds (>=40, >=70 high)
3. **Source Diversity** - Verifies multi-source confirmation (>2 sources)
4. **Severity Range** - Confirms all values within 0-100
5. **Escalation Tracking** - Checks narrative risks have escalation_history

## Output

Returns a `data_quality_score` (0-100) with:
- 5-dimension breakdown (each 0-20 points)
- Letter grade (A/B/C/D/F)
- Specific issues found with recommendations
- Actionable improvement suggestions

## Documentation Index

| Document | Purpose |
|----------|---------|
| [quality-metrics.md](quality-metrics.md) | Scoring formulas and calculation examples |
| [category-requirements.md](category-requirements.md) | 5-category coverage rules |
| [validation-rules.md](validation-rules.md) | Confidence, source, escalation checks |

## Integration

- **Invoked by**: `/analyze-news` command
- **Runs with**: `news-impact-analyzer` (parallel)
- **Feeds into**: Collection pipeline improvement

## Quick Reference

```
Input:  { "date": "2026-01-04" }  // Optional, defaults to today

Output: {
  "status": "SUCCESS",
  "data_quality_score": 85,
  "grade": "B",
  "breakdown": { ... },
  "recommendations": [ ... ]
}
```
