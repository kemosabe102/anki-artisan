# Data Validator - Test Scenarios

**File**: `test-scenarios.json`

Comprehensive test specifications for the data-validator agent covering happy path, edge case, and error handling scenarios.

---

## Overview

The test scenarios validate the data-validator agent's ability to:
1. Audit 5-category coverage (geopolitical, health, regulatory, macro, tech)
2. Score confidence levels, source diversity, severity validity, and escalation completeness
3. Generate actionable recommendations
4. Handle errors gracefully with specific recovery guidance

---

## Scenario 1: Happy Path - Full Audit with Excellent Quality

**Scenario ID**: `happy_path_full_audit`

### Input
```json
{
  "date": "2026-01-04"
}
```

### Database State
- **15 events** across **all 5 categories**
- Average confidence: **87** (well above 70 threshold)
- Average sources: **3.7** (exceeds >2 requirement)
- 93% of events have confidence >= 70
- 100% of events have >2 sources
- 100% of severity values in 0-100 range
- 95% of narrative risks have escalation history

### Expected Output
```
Status: SUCCESS
Grade: A (90-100)
data_quality_score: 90-100

Breakdown:
- category_score: 20 (5/5 categories)
- confidence_score: 18-20 (93% high confidence)
- source_score: 18-20 (100% multi-source)
- severity_score: 20 (100% valid)
- escalation_score: 18-20 (95% complete)

Issues: None or minimal (0-1 low-confidence risks)
Recommendations: 0-2 minor suggestions
```

### Success Criteria
- All 5 categories present in coverage
- No issues flagged in low_confidence_risks, single_source_events, or missing_escalation_history
- Total score sums to breakdown dimensions
- Grade assignment correct (A = 90-100)

---

## Scenario 2: Edge Case - Partial Coverage with Low Confidence

**Scenario ID**: `edge_case_partial_coverage`

### Input
```json
{
  "date": "2026-01-04"
}
```

### Database State
- **10 events** across **3 categories only** (geopolitical, health, macro)
- **Missing**: regulatory, tech
- Average confidence: **56** (below high threshold)
- Average sources: **1.8** (below >2 requirement)
- Only 20% of events have confidence >= 70
- Only 40% of events have >2 sources
- 100% of severity values valid
- Only 50% of narrative risks have escalation history

### Expected Output
```
Status: SUCCESS
Grade: D (60-69)
data_quality_score: 60-69

Breakdown:
- category_score: 12 (3/5 categories = 60% * 4 = 12)
- confidence_score: 8-10 (20% events >= 70)
- source_score: 8-10 (40% events >2 sources)
- severity_score: 20 (100% valid)
- escalation_score: 8-10 (50% narrative with history)

Issues Flagged:
- low_confidence_risks: 5-6 events
- single_source_events: 4-5 events
- missing_escalation_history: 3-4 risks
- missing_categories: regulatory, tech

Recommendations:
- "Add regulatory news sources (missing category)"
- "Increase source diversity for [specific events]"
- "Populate escalation_history for narrative risks"
```

### Success Criteria
- Only 3 categories in coverage (regulatory and tech marked false)
- 5-6 events flagged in low_confidence_risks
- 4-5 events flagged in single_source_events
- 3-4 risks flagged in missing_escalation_history
- Total score 60-69
- Recommendations address specific gaps

---

## Scenario 3: Error Handling - Invalid Date Format

**Scenario ID**: `error_invalid_date_format`

### Input
```json
{
  "date": "01/04/2026"
}
```

### Expected Output
```
Status: FAILURE
failure_category: "invalid_date"

error_details: "Date format must be YYYY-MM-DD. Received: 01/04/2026"

recovery_suggestions: [
  "Use format YYYY-MM-DD (e.g., 2026-01-04)",
  "Ensure year is 4 digits, month and day are 2 digits",
  "Refer to the /analyze-news endpoint documentation"
]
```

### Success Criteria
- Status is FAILURE (not SUCCESS)
- failure_category is "invalid_date"
- Error message mentions expected format (YYYY-MM-DD)
- Recovery suggestions provide format example
- No audit_date, data_quality_score, or breakdown in response

---

## Scenario 4: Error Handling - Database Connection Failure

**Scenario ID**: `error_connection_failure`

### Input
```json
{
  "date": "2026-01-04"
}
```

### Database State
- Connection timeout or unavailable
- Error: "Connection timeout after 30s"

### Expected Output
```
Status: FAILURE
failure_category: "connection_failure"

error_details: "Failed to connect to database: Connection timeout after 30s"

recovery_suggestions: [
  "Verify database is running and accessible",
  "Check connection credentials (hostname, port, username)",
  "Verify network connectivity to database host",
  "Check database logs for errors"
]
```

### Success Criteria
- Status is FAILURE
- failure_category is "connection_failure"
- Error mentions database or connection issue
- Recovery suggestions include connectivity and credentials checks
- >= 2 recovery suggestions provided
- No partial audit data in response

---

## Scenario 5: Error Handling - No Events (Valid Empty State)

**Scenario ID**: `error_no_events_valid_state`

### Input
```json
{
  "date": "2026-01-04"
}
```

### Database State
- Query succeeds
- Returns 0 events
- Connection healthy

### Expected Output
```
Status: SUCCESS (NOT FAILURE - empty data is valid)
Grade: F
audit_date: "2026-01-04"
data_quality_score: 0
events_audited: 0
categories_covered: 0

missing_categories: [
  "geopolitical", "health", "regulatory", "macro", "tech"
]

Breakdown (all zeros):
- category_score: 0
- confidence_score: 0
- source_score: 0
- severity_score: 0
- escalation_score: 0

Issues: None
Recommendations: [
  "No events collected for this date. Check if it's a weekend/holiday.",
  "Verify news collection pipeline is running."
]
```

### Success Criteria
- Status is SUCCESS (not FAILURE)
- All breakdown scores equal 0
- Total score = 0
- Grade = F (0-59 range)
- All category_coverage values are false
- All 5 categories in missing_categories
- Recommendations mention no data collection

---

## Scoring Formula Reference

### Category Score (0-20)
```
category_score = 4 * (categories_covered / 5)

5/5 categories → 20
4/5 categories → 16
3/5 categories → 12
2/5 categories → 8
1/5 categories → 4
0/5 categories → 0
```

### Confidence Score (0-20)
```
confidence_score = 20 * (events_with_confidence_gte_70 / total_events)

Minimum acceptable: 40
High threshold: 70
```

### Source Score (0-20)
```
source_score = 20 * (events_with_sources_gt_2 / total_events)

Requirement: >2 sources per event
```

### Severity Score (0-20)
```
severity_score = 20 * (events_with_severity_0_to_100 / total_events)

Valid range: 0-100
```

### Escalation Score (0-20)
```
escalation_score = 20 * (narrative_risks_with_escalation_history / total_narrative_risks)

Applies only to narrative risk types
```

### Total Score (0-100)
```
data_quality_score = category_score + confidence_score + source_score + severity_score + escalation_score
```

---

## Grade Assignment

| Grade | Score Range | Interpretation |
|-------|-------------|-----------------|
| A | 90-100 | Excellent - Collection pipeline healthy |
| B | 80-89 | Good - Minor gaps, acceptable for analysis |
| C | 70-79 | Fair - Some issues need attention |
| D | 60-69 | Poor - Significant gaps affecting reliability |
| F | 0-59 | Failing - Critical issues, pipeline needs repair |

---

## Test Execution Guide

### Happy Path
- **Purpose**: Verify Grade A output with optimized dimensions
- **Setup**: Mock database with 15 quality events across all 5 categories
- **Key Assertion**: Score >= 90, all issue arrays empty

### Edge Case
- **Purpose**: Verify partial coverage detection and proportional scoring
- **Setup**: 10 events, 3 categories, low confidence/source metrics
- **Key Assertion**: Score 60-69, specific issues flagged

### Error Handling (Format)
- **Purpose**: Validate input format validation
- **Setup**: Invalid date format input
- **Key Assertion**: FAILURE with invalid_date category

### Error Handling (Connection)
- **Purpose**: Validate database error handling
- **Setup**: Database timeout or unavailable
- **Key Assertion**: FAILURE with connection_failure category

### Error Handling (Empty)
- **Purpose**: Distinguish 'no data' (valid) from connection errors
- **Setup**: Query succeeds, 0 results
- **Key Assertion**: SUCCESS with score 0, grade F

---

## Integration Notes

- Test scenarios validate against the agent's output schema: `schemas/data-validator.schema.json`
- All timestamps are in YYYY-MM-DD format (ISO 8601)
- Risk IDs follow naming convention: `{category}_{type}_{id}`
- Recommendations must be specific and actionable
- No test should modify database (SELECT-only validation)

---

## File Location

**Primary**: `C:/Users/kemos/Repos/gauntlet-agents/.claude/agents/investing/data-validator/docs/test-scenarios.json`

**Format**: JSON with comprehensive test metadata, success criteria, and validation rules.

---
