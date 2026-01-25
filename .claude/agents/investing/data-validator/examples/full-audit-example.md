# Full Audit Example

## Scenario

Daily quality audit for 2026-01-04 with good collection quality but minor gaps.

## Input

```json
{
  "date": "2026-01-04"
}
```

## Output

```json
{
  "status": "SUCCESS",
  "audit_date": "2026-01-04",
  "data_quality_score": 85,
  "grade": "B",
  "category_coverage": {
    "geopolitical": true,
    "health": true,
    "regulatory": false,
    "macro": true,
    "tech": true
  },
  "categories_covered": 4,
  "categories_total": 5,
  "missing_categories": ["regulatory"],
  "events_audited": 12,
  "low_confidence_risks": [
    {
      "risk_id": "health_outbreak_xyz",
      "confidence": 35,
      "reason": "single source",
      "recommendation": "Add CDC or WHO source"
    }
  ],
  "single_source_events": [
    {
      "risk_id": "macro_fed_policy_123",
      "sources": 1,
      "recommendation": "Add financial news wire confirmation"
    }
  ],
  "missing_escalation_history": [
    {
      "risk_id": "geopolitical_conflict_456",
      "stage": "elevated",
      "recommendation": "Populate escalation timeline"
    }
  ],
  "recommendations": [
    "Add regulatory news sources (missing category)",
    "Increase source diversity for health_outbreak_xyz",
    "Populate escalation_history for ongoing geopolitical events"
  ],
  "breakdown": {
    "category_score": 16,
    "confidence_score": 18,
    "source_score": 15,
    "severity_score": 20,
    "escalation_score": 16
  },
  "breakdown_details": {
    "category_score": "4/5 categories covered = 16/20",
    "confidence_score": "10/12 events >= 70 confidence = 18/20 (rounded)",
    "source_score": "9/12 events have >2 sources = 15/20",
    "severity_score": "All severity values 0-100 = 20/20",
    "escalation_score": "4/5 narrative risks have history = 16/20"
  }
}
```

## Analysis

### Score Breakdown

| Dimension | Score | Explanation |
|-----------|-------|-------------|
| Category | 16/20 | Missing regulatory category |
| Confidence | 18/20 | Most events have high confidence |
| Source | 15/20 | 3 events need more sources |
| Severity | 20/20 | All values valid |
| Escalation | 16/20 | 1 narrative risk missing history |
| **Total** | **85/100** | **Grade: B** |

### Issues Found

1. **Missing Category**: No regulatory events collected
2. **Low Confidence**: 1 health event below minimum threshold
3. **Single Source**: 1 macro event needs confirmation
4. **Missing Escalation**: 1 geopolitical conflict lacks timeline

### Recommendations Priority

1. **High**: Add regulatory news sources (entire category missing)
2. **Medium**: Verify health_outbreak_xyz or add sources
3. **Low**: Populate escalation history for tracking
