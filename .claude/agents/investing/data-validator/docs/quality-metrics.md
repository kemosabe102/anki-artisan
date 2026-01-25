# Quality Metrics - Scoring Methodology

## Overview

The data quality score is a composite of 5 dimensions, each worth 0-20 points, for a total of 0-100.

## Master Formula

```
data_quality_score = category_score + confidence_score + source_score + severity_score + escalation_score
```

---

## Dimension 1: Category Score (0-20)

**Purpose**: Measures coverage across the 5 risk categories.

**Formula**:
```
category_score = 4 * (categories_covered / 5)
```

**Categories**:
- `geopolitical` - International conflicts, sanctions, elections
- `health` - Pandemics, outbreaks, healthcare policy
- `regulatory` - Financial regulations, antitrust, compliance
- `macro` - Central bank policy, employment, GDP
- `tech` - Cybersecurity, AI policy, tech sector disruption

**Examples**:
| Categories Covered | Score |
|-------------------|-------|
| 5/5 | 20 |
| 4/5 | 16 |
| 3/5 | 12 |
| 2/5 | 8 |
| 1/5 | 4 |
| 0/5 | 0 |

---

## Dimension 2: Confidence Score (0-20)

**Purpose**: Validates event confidence meets thresholds.

**Formula**:
```
high_confidence_ratio = events_with_confidence_gte_70 / total_events
confidence_score = 20 * high_confidence_ratio
```

**Thresholds**:
- Minimum acceptable: 40 (events below are flagged)
- High confidence: 70+ (target for majority)

**Examples**:
| Events >= 70 | Total Events | Score |
|--------------|--------------|-------|
| 10/10 | 10 | 20 |
| 8/10 | 10 | 16 |
| 5/10 | 10 | 10 |
| 0/10 | 10 | 0 |

---

## Dimension 3: Source Score (0-20)

**Purpose**: Validates multi-source confirmation for events.

**Formula**:
```
multi_source_ratio = events_with_sources_gt_2 / total_events
source_score = 20 * multi_source_ratio
```

**Threshold**: Events should have >2 sources for confirmation.

**Examples**:
| Events >2 Sources | Total Events | Score |
|-------------------|--------------|-------|
| 12/12 | 12 | 20 |
| 9/12 | 12 | 15 |
| 6/12 | 12 | 10 |
| 0/12 | 12 | 0 |

---

## Dimension 4: Severity Score (0-20)

**Purpose**: Validates severity values are within expected range.

**Formula**:
```
valid_severity_ratio = events_with_severity_0_to_100 / total_events
severity_score = 20 * valid_severity_ratio
```

**Note**: Any severity outside 0-100 indicates data quality issue (schema drift, parsing error).

---

## Dimension 5: Escalation Score (0-20)

**Purpose**: Validates narrative/ongoing risks have escalation_history populated.

**Formula**:
```
narrative_risks = events flagged as ongoing/narrative type
escalation_complete_ratio = risks_with_escalation_history / narrative_risks
escalation_score = 20 * escalation_complete_ratio
```

**Note**: Only applies to events with narrative risk classification. If no narrative risks, score defaults to 20.

---

## Grade Assignment

| Grade | Score Range | Interpretation |
|-------|-------------|----------------|
| A | 90-100 | Excellent - Collection pipeline healthy |
| B | 80-89 | Good - Minor gaps, acceptable for analysis |
| C | 70-79 | Fair - Some issues need attention |
| D | 60-69 | Poor - Significant gaps affecting reliability |
| F | 0-59 | Failing - Critical issues, pipeline needs repair |

---

## Complete Calculation Example

**Scenario**: 10 events on 2026-01-04
- Categories: geopolitical, health, macro, tech (4/5)
- Confidence >= 70: 8/10 events
- Sources > 2: 9/10 events
- Severity 0-100: 10/10 events
- Narrative risks with history: 4/5 risks

**Calculation**:
```
category_score    = 4 * (4/5) = 16
confidence_score  = 20 * (8/10) = 16
source_score      = 20 * (9/10) = 18
severity_score    = 20 * (10/10) = 20
escalation_score  = 20 * (4/5) = 16

total = 16 + 16 + 18 + 20 + 16 = 86
grade = B
```
