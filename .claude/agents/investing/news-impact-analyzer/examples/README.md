# News Impact Analyzer Examples

Usage examples showing how the orchestrator delegates to news-impact-analyzer.

## Contents

| Example | Description |
|---------|-------------|
| [full-analysis-example.md](full-analysis-example.md) | Complete daily analysis walkthrough |
| [delegation-examples.md](delegation-examples.md) | Orchestrator delegation patterns |

## Quick Example

```python
Task(news-impact-analyzer,
  "Analyze news impact for 2026-01-04. 
   Category: all. Minimum severity: 40.")
```

## Expected Output Format

```json
{
  "status": "SUCCESS",
  "analysis_date": "2026-01-04",
  "regime_context": {
    "classification": "risk_off",
    "score": 28,
    "total_multiplier": 2.1
  },
  "events_analyzed": 4,
  "impact_predictions": [...],
  "composite_metrics": {
    "msi_macro_shock_index": 58,
    "ssi_by_sector": {"technology": 72}
  }
}
```

## Input Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| date | string (YYYY-MM-DD) | today | Analysis date |
| category_filter | enum | "all" | Filter by risk category |
| min_severity | int (0-100) | 40 | Minimum severity threshold |
