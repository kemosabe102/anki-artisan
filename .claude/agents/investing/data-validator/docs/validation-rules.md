# Validation Rules - Confidence, Source, Escalation Checks

## Overview

Beyond category coverage, the data-validator checks three key data quality dimensions:
1. Confidence thresholds
2. Source diversity
3. Escalation history completeness

---

## 1. Confidence Threshold Validation

### Thresholds

| Level | Threshold | Description |
|-------|-----------|-------------|
| Minimum | >= 40 | Below this, events are too uncertain to influence |
| High | >= 70 | Target for majority of events |

### Validation Logic

```sql
SELECT 
  risk_id,
  confidence,
  CASE 
    WHEN confidence < 40 THEN 'CRITICAL'
    WHEN confidence < 70 THEN 'LOW'
    ELSE 'OK'
  END as status
FROM attention_daily 
WHERE date = :audit_date;
```

### Flagging Rules

- **CRITICAL** (< 40): Flag with specific recommendation to verify or remove
- **LOW** (40-69): Flag for additional source confirmation
- **OK** (>= 70): No flag needed

### Recommendations by Confidence Issue

| Issue | Recommendation |
|-------|----------------|
| Single source, low confidence | "Add [category-specific] source for confirmation" |
| Old data, low confidence | "Verify event still active, refresh sources" |
| Conflicting reports | "Flag for manual review, increase source diversity" |

---

## 2. Source Diversity Validation

### Threshold

Events should have **> 2 sources** for reliable confirmation.

### Validation Logic

```sql
SELECT 
  risk_id,
  source_count,
  CASE 
    WHEN source_count <= 1 THEN 'SINGLE_SOURCE'
    WHEN source_count = 2 THEN 'LOW_DIVERSITY'
    ELSE 'OK'
  END as status
FROM attention_daily 
WHERE date = :audit_date;
```

### Flagging Rules

- **SINGLE_SOURCE** (1): Critical flag - unreliable without confirmation
- **LOW_DIVERSITY** (2): Warning flag - borderline acceptable
- **OK** (> 2): Adequate source diversity

### Recommendations by Source Issue

| Category | Single-Source Recommendation |
|----------|------------------------------|
| geopolitical | "Add Reuters or AP wire confirmation" |
| health | "Add CDC or WHO official source" |
| regulatory | "Add Federal Register or agency release" |
| macro | "Add financial news wire confirmation" |
| tech | "Add industry publication confirmation" |

---

## 3. Escalation History Validation

### Purpose

Narrative/ongoing risks must have `escalation_history` populated to track evolution over time.

### Identifying Narrative Risks

Narrative risks are ongoing events that evolve (vs. point-in-time events):
- Conflicts escalating/de-escalating
- Disease outbreaks spreading/contained
- Regulatory investigations progressing
- Trade disputes evolving

### Validation Logic

```sql
SELECT 
  risk_id,
  stage,
  escalation_history,
  CASE 
    WHEN stage IN ('elevated', 'critical', 'ongoing') 
      AND (escalation_history IS NULL OR escalation_history = '[]')
    THEN 'MISSING'
    ELSE 'OK'
  END as status
FROM attention_daily 
WHERE date = :audit_date;
```

### Flagging Rules

- **MISSING**: Narrative risk without escalation history - critical gap
- **OK**: Either not a narrative risk, or has escalation history populated

### Expected Escalation History Format

```json
[
  {"date": "2026-01-01", "stage": "emerging", "severity": 45},
  {"date": "2026-01-02", "stage": "elevated", "severity": 65},
  {"date": "2026-01-04", "stage": "elevated", "severity": 72}
]
```

### Recommendations for Missing Escalation

| Stage | Recommendation |
|-------|----------------|
| elevated | "Populate escalation timeline from first observation" |
| critical | "URGENT: Add historical severity progression" |
| ongoing | "Track stage transitions since event began" |

---

## Combined Validation Summary

All three validations run in parallel and contribute to the overall quality score:

| Validation | Weight | Impact |
|------------|--------|--------|
| Confidence | 20 pts | Affects reliability of impact predictions |
| Source | 20 pts | Affects confidence in event accuracy |
| Escalation | 20 pts | Affects scenario generation quality |
