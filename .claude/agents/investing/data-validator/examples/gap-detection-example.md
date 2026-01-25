# Gap Detection Example

## Scenario

Daily quality audit for 2026-01-03 with significant collection gaps requiring immediate attention.

## Input

```json
{
  "date": "2026-01-03"
}
```

## Output

```json
{
  "status": "SUCCESS",
  "audit_date": "2026-01-03",
  "data_quality_score": 62,
  "grade": "D",
  "category_coverage": {
    "geopolitical": true,
    "health": false,
    "regulatory": false,
    "macro": true,
    "tech": true
  },
  "categories_covered": 3,
  "categories_total": 5,
  "missing_categories": ["health", "regulatory"],
  "events_audited": 8,
  "low_confidence_risks": [
    {
      "risk_id": "tech_cyber_incident_001",
      "confidence": 32,
      "reason": "unverified social media report",
      "recommendation": "Verify with CISA advisory or security vendor"
    },
    {
      "risk_id": "macro_trade_policy_002",
      "confidence": 38,
      "reason": "conflicting reports",
      "recommendation": "Wait for official announcement or add Reuters wire"
    },
    {
      "risk_id": "geopolitical_sanctions_003",
      "confidence": 42,
      "reason": "single government source",
      "recommendation": "Add independent news confirmation"
    }
  ],
  "single_source_events": [
    {
      "risk_id": "tech_cyber_incident_001",
      "sources": 1,
      "recommendation": "Add CISA or security vendor source"
    },
    {
      "risk_id": "macro_trade_policy_002",
      "sources": 1,
      "recommendation": "Add Reuters or Bloomberg confirmation"
    },
    {
      "risk_id": "geopolitical_sanctions_003",
      "sources": 1,
      "recommendation": "Add AP or Reuters wire"
    },
    {
    {
      "risk_id": "tech_ai_regulation_004",
      "sources": 2,
      "recommendation": "Add industry publication for diversity"
    }
  ],
  "missing_escalation_history": [
    {
      "risk_id": "geopolitical_conflict_ongoing",
      "stage": "critical",
      "recommendation": "URGENT: Add historical severity progression"
    },
    {
      "risk_id": "macro_inflation_trend",
      "stage": "elevated",
      "recommendation": "Populate escalation timeline from Q3 2025"
    }
  ],
  "recommendations": [
    "CRITICAL: Add health news sources (WHO, CDC) - missing entire category",
    "CRITICAL: Add regulatory news sources (SEC, Federal Register) - missing entire category",
    "HIGH: Verify tech_cyber_incident_001 - confidence below minimum (32)",
    "HIGH: Add sources for 4 single-source events",
    "MEDIUM: Populate escalation_history for 2 narrative risks"
  ],
  "breakdown": {
    "category_score": 12,
    "confidence_score": 10,
    "source_score": 10,
    "severity_score": 20,
    "escalation_score": 10
  },
  "breakdown_details": {
    "category_score": "3/5 categories covered = 12/20",
    "confidence_score": "4/8 events >= 70 confidence = 10/20",
    "source_score": "4/8 events have >2 sources = 10/20",
    "severity_score": "All severity values 0-100 = 20/20",
    "escalation_score": "2/4 narrative risks have history = 10/20"
  }
}
```

## Analysis

### Score Breakdown

| Dimension | Score | Explanation |
|-----------|-------|-------------|
| Category | 12/20 | Missing 2 categories (health, regulatory) |
| Confidence | 10/20 | Only half events meet high threshold |
| Source | 10/20 | Half events are single-source |
| Severity | 20/20 | All values valid |
| Escalation | 10/20 | Half narrative risks missing history |
| **Total** | **62/100** | **Grade: D** |

### Critical Issues

1. **Missing Categories** (2): No health or regulatory events
2. **Below-Minimum Confidence** (2): tech_cyber_incident_001 (32), macro_trade_policy_002 (38)
3. **Single-Source Events** (4): High risk of inaccuracy
4. **Missing Escalation** (2): Cannot track risk evolution

### Recommended Actions

**Immediate (Before Next Analysis)**:
1. Add WHO/CDC feeds for health category
2. Add SEC/Federal Register feeds for regulatory category
3. Verify or remove tech_cyber_incident_001 (32 confidence)

**Short-Term (This Week)**:
1. Increase source diversity across all categories
2. Populate escalation_history for ongoing risks
3. Review collection pipeline for systematic gaps
