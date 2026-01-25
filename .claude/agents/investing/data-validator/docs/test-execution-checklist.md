# Test Execution Checklist - Data Validator Agent

Quick reference for validating test execution against the three required scenarios.

---

## Scenario 1: Happy Path - Full Audit

### Pre-Test Setup
- [ ] Database contains exactly 15 events
- [ ] All 5 categories represented (geopolitical, health, regulatory, macro, tech)
- [ ] Average confidence >= 87
- [ ] All events have > 2 sources
- [ ] All severity values in 0-100 range
- [ ] Narrative risks have escalation_history populated

### Input
```json
{ "date": "2026-01-04" }
```

### Output Validation Checklist
- [ ] `status` equals `"SUCCESS"`
- [ ] `audit_date` equals `"2026-01-04"`
- [ ] `data_quality_score` >= 90 and <= 100
- [ ] `grade` equals `"A"`
- [ ] `categories_covered` equals 5
- [ ] `missing_categories` is empty array
- [ ] `events_audited` equals 15
- [ ] `low_confidence_risks` is empty array
- [ ] `single_source_events` is empty array
- [ ] `missing_escalation_history` is empty array

### Score Breakdown Validation
- [ ] `breakdown.category_score` equals 20
- [ ] `breakdown.confidence_score` >= 18 and <= 20
- [ ] `breakdown.source_score` >= 18 and <= 20
- [ ] `breakdown.severity_score` equals 20
- [ ] `breakdown.escalation_score` >= 18 and <= 20
- [ ] Sum of all 5 scores equals `data_quality_score`

### Category Coverage Validation
- [ ] `category_coverage.geopolitical` equals true
- [ ] `category_coverage.health` equals true
- [ ] `category_coverage.regulatory` equals true
- [ ] `category_coverage.macro` equals true
- [ ] `category_coverage.tech` equals true

### Recommendations Validation
- [ ] `recommendations` is array
- [ ] `recommendations.length` <= 2 (minimal suggestions for excellent audit)
- [ ] Each recommendation is non-empty string

### Schema Compliance
- [ ] Response validates against `data-validator.schema.json`
- [ ] All required fields present
- [ ] No extra fields that violate schema
- [ ] All field types match schema

---

## Scenario 2: Edge Case - Partial Coverage with Low Confidence

### Pre-Test Setup
- [ ] Database contains exactly 10 events
- [ ] Only 3 categories present (geopolitical, health, macro)
- [ ] Regulatory and tech categories MISSING
- [ ] 5-6 events have confidence < 70 (between 40-70)
- [ ] 4-5 events have <= 2 sources (single-source)
- [ ] All severity values valid (0-100)
- [ ] Only ~50% of narrative risks have escalation_history

### Input
```json
{ "date": "2026-01-04" }
```

### Output Validation Checklist
- [ ] `status` equals `"SUCCESS"`
- [ ] `audit_date` equals `"2026-01-04"`
- [ ] `data_quality_score` >= 60 and <= 69
- [ ] `grade` equals `"D"`
- [ ] `categories_covered` equals 3
- [ ] `missing_categories` contains exactly ["regulatory", "tech"] (any order)
- [ ] `events_audited` equals 10
- [ ] `low_confidence_risks.length` >= 5
- [ ] `single_source_events.length` >= 4
- [ ] `missing_escalation_history.length` >= 3

### Score Breakdown Validation
- [ ] `breakdown.category_score` equals 12 (3/5 * 4 = 12)
- [ ] `breakdown.confidence_score` >= 8 and <= 10
- [ ] `breakdown.source_score` >= 8 and <= 10
- [ ] `breakdown.severity_score` equals 20
- [ ] `breakdown.escalation_score` >= 8 and <= 10
- [ ] Sum of all 5 scores equals `data_quality_score`
- [ ] Total is between 60-69

### Issue Details Validation
- [ ] All items in `low_confidence_risks` have `confidence` < 70
- [ ] All items in `low_confidence_risks` have `risk_id`, `reason`, `recommendation` fields
- [ ] All items in `single_source_events` have `sources` <= 2
- [ ] All items in `single_source_events` have `risk_id`, `recommendation` fields
- [ ] All items in `missing_escalation_history` are narrative risk types
- [ ] All items in `missing_escalation_history` have `risk_id`, `stage`, `recommendation` fields

### Category Coverage Validation
- [ ] `category_coverage.geopolitical` equals true
- [ ] `category_coverage.health` equals true
- [ ] `category_coverage.regulatory` equals false
- [ ] `category_coverage.macro` equals true
- [ ] `category_coverage.tech` equals false

### Recommendations Validation
- [ ] `recommendations.length` >= 3
- [ ] At least one recommendation addresses missing regulatory category
- [ ] At least one recommendation addresses missing tech category
- [ ] At least one recommendation addresses low confidence
- [ ] At least one recommendation addresses source diversity
- [ ] Each recommendation is specific and actionable

### Schema Compliance
- [ ] Response validates against `data-validator.schema.json`
- [ ] All required fields present
- [ ] All issue arrays properly typed

---

## Scenario 3: Error Handling - Invalid Date Format

### Input
```json
{ "date": "01/04/2026" }
```

### Output Validation Checklist
- [ ] `status` equals `"FAILURE"`
- [ ] `failure_category` equals `"invalid_date"`
- [ ] `error_details` is non-empty string
- [ ] `error_details` mentions "YYYY-MM-DD" or "expected format"
- [ ] `error_details` mentions "01/04/2026" or "received format"
- [ ] `recovery_suggestions` is non-empty array
- [ ] `recovery_suggestions[0]` provides correct format example
- [ ] `recovery_suggestions.length` >= 1

### Invalid Fields Check
- [ ] Response does NOT contain `audit_date`
- [ ] Response does NOT contain `data_quality_score`
- [ ] Response does NOT contain `grade`
- [ ] Response does NOT contain `breakdown`
- [ ] Response does NOT contain `events_audited`
- [ ] Response does NOT contain `category_coverage`

### Schema Compliance
- [ ] Response validates against `data-validator.schema.json` FailureResponse
- [ ] `failure_category` in enum: ['no_data', 'query_error', 'invalid_date', 'connection_failure', 'schema_drift']
- [ ] No SuccessResponse fields present

---

## Scenario 4: Error Handling - Database Connection Failure

### Pre-Test Setup
- [ ] Database is unavailable or connection times out
- [ ] Query does NOT execute successfully

### Input
```json
{ "date": "2026-01-04" }
```

### Output Validation Checklist
- [ ] `status` equals `"FAILURE"`
- [ ] `failure_category` equals `"connection_failure"`
- [ ] `error_details` is non-empty string
- [ ] `error_details` mentions "database" or "connection"
- [ ] `error_details` may mention "timeout" or specific error
- [ ] `recovery_suggestions` is non-empty array
- [ ] `recovery_suggestions.length` >= 2
- [ ] At least one suggestion addresses connectivity check
- [ ] At least one suggestion addresses credentials/hostname

### Invalid Fields Check
- [ ] Response does NOT contain `events_audited`
- [ ] Response does NOT contain `data_quality_score`
- [ ] Response does NOT contain `category_coverage`
- [ ] No partial audit data returned

### Sample Recovery Suggestions
- "Verify database is running and accessible"
- "Check connection credentials (hostname, port, username)"
- "Verify network connectivity to database host"

### Schema Compliance
- [ ] Response validates against `data-validator.schema.json` FailureResponse
- [ ] `failure_category` equals `connection_failure`
- [ ] No SuccessResponse fields present

---

## Scenario 5: Error Handling - No Events (Valid Empty State)

### Pre-Test Setup
- [ ] Database query succeeds (connection healthy)
- [ ] Query returns 0 rows
- [ ] No errors in execution

### Input
```json
{ "date": "2026-01-04" }
```

### Output Validation Checklist
- [ ] `status` equals `"SUCCESS"` (NOT "FAILURE")
- [ ] `audit_date` equals `"2026-01-04"`
- [ ] `data_quality_score` equals 0
- [ ] `grade` equals `"F"`
- [ ] `events_audited` equals 0
- [ ] `categories_covered` equals 0
- [ ] `missing_categories` has length 5
- [ ] `missing_categories` contains all: ["geopolitical", "health", "regulatory", "macro", "tech"]
- [ ] `low_confidence_risks` is empty array
- [ ] `single_source_events` is empty array
- [ ] `missing_escalation_history` is empty array

### Score Breakdown Validation
- [ ] `breakdown.category_score` equals 0
- [ ] `breakdown.confidence_score` equals 0
- [ ] `breakdown.source_score` equals 0
- [ ] `breakdown.severity_score` equals 0
- [ ] `breakdown.escalation_score` equals 0
- [ ] Sum of all 5 scores equals 0

### Category Coverage Validation
- [ ] `category_coverage.geopolitical` equals false
- [ ] `category_coverage.health` equals false
- [ ] `category_coverage.regulatory` equals false
- [ ] `category_coverage.macro` equals false
- [ ] `category_coverage.tech` equals false

### Recommendations Validation
- [ ] `recommendations` is non-empty array
- [ ] At least one recommendation mentions "no events" or "no data"
- [ ] At least one recommendation mentions "weekend/holiday" or "collection pipeline"

### Schema Compliance
- [ ] Response validates against `data-validator.schema.json`
- [ ] All required fields present
- [ ] Status is SUCCESS (not FAILURE)

---

## Cross-Scenario Validation

### Schema Validation (All Scenarios)
- [ ] All responses validate against `schemas/data-validator.schema.json`
- [ ] All JSON is valid and well-formed
- [ ] All required fields present in each response

### Risk ID Format Validation
- [ ] All risk_ids follow pattern: `{category}_{type}_{id}`
- [ ] Categories are one of: geopolitical, health, regulatory, macro, tech
- [ ] No duplicate risk_ids within single response

### Response Structure Validation
- [ ] Happy path: SuccessResponse schema
- [ ] Edge case: SuccessResponse schema
- [ ] Invalid date: FailureResponse schema
- [ ] Connection failure: FailureResponse schema
- [ ] No events: SuccessResponse schema (not failure)

### Timestamp Validation (All Scenarios)
- [ ] All dates in YYYY-MM-DD format
- [ ] All audit_date fields match input date parameter

---

## Test Execution Summary

### Passing Criteria (ALL must be met)
- [ ] Happy path: Score >= 90, Grade A, 0 issues, all categories covered
- [ ] Edge case: Score 60-69, Grade D, 5-6 low confidence, 4-5 single-source, 3-4 missing escalation
- [ ] Invalid date: FAILURE status, invalid_date category, format guidance
- [ ] Connection failure: FAILURE status, connection_failure category, recovery suggestions
- [ ] No events: SUCCESS status, score 0, grade F, all categories missing

### Documentation Requirements
- [ ] Each scenario has input/output examples
- [ ] Success criteria documented in test-scenarios.json
- [ ] Validation rules specified for each dimension
- [ ] Scoring formulas referenced and verified
- [ ] Recovery suggestions provided for all failures

---

**Last Updated**: 2026-01-04
**Test Scenarios Version**: 1.0
**Schema Version**: data-validator.schema.json
