# Data Validator Agent - Testing Overview

Complete test specification suite for validating the data-validator agent's audit functionality.

---

## Quick Summary

**3 Required Test Scenarios Generated**:

1. **Happy Path** - Full audit with all 5 categories, high quality metrics → Grade A (90+)
2. **Edge Case** - Partial coverage (3/5 categories), low confidence, single-source issues → Grade D (60-69)
3. **Error Handling** - Invalid date format, connection failure, empty database state → FAILURE or SUCCESS with 0 score

**Files Created**:
- `test-scenarios.json` - Comprehensive test specification with all scenarios, inputs, expected outputs, and validation rules
- `test-scenarios-README.md` - Detailed narrative guide with examples for each scenario
- `test-execution-checklist.md` - Quick-reference validation checklist for test execution

---

## Test Files Location

```
C:/Users/kemos/Repos/gauntlet-agents/.claude/agents/investing/data-validator/docs/
├── test-scenarios.json               # Primary test specifications
├── test-scenarios-README.md          # Detailed scenario guide
├── test-execution-checklist.md       # Execution validation checklist
└── TESTING-OVERVIEW.md              # This file
```

---

## Scenario Details at a Glance

### Scenario 1: Happy Path - Full Audit

**What It Tests**: Agent correctly audits high-quality data collection

| Dimension | Value |
|-----------|-------|
| Input | `{"date": "2026-01-04"}` |
| Database | 15 events, all 5 categories, avg confidence 87 |
| Expected Grade | A (90-100) |
| Expected Issues | None |
| Key Assertions | All dimensions optimized, no gaps |

**Database Requirements**:
- 15 events total
- Categories: geopolitical (2), health (3), regulatory (2), macro (3), tech (2+)
- Confidence: 87-95 (all >= 70)
- Sources: 3-5 per event (all > 2)
- Severity: All 0-100 valid
- Escalation: Narrative risks populated

**Success Criteria**:
```
✓ status = SUCCESS
✓ data_quality_score >= 90
✓ grade = A
✓ categories_covered = 5
✓ missing_categories = []
✓ low_confidence_risks = []
✓ single_source_events = []
✓ missing_escalation_history = []
✓ breakdown.category_score = 20
✓ breakdown.confidence_score >= 18
✓ breakdown.source_score >= 18
✓ breakdown.severity_score = 20
✓ breakdown.escalation_score >= 18
✓ recommendations.length <= 2
```

---

### Scenario 2: Edge Case - Partial Coverage with Low Confidence

**What It Tests**: Agent correctly identifies and scores partial coverage scenarios

| Dimension | Value |
|-----------|-------|
| Input | `{"date": "2026-01-04"}` |
| Database | 10 events, 3 categories only, avg confidence 56 |
| Expected Grade | D (60-69) |
| Expected Issues | 5-6 low confidence, 4-5 single-source, 3-4 missing escalation |
| Key Assertions | Proportional scoring reflects quality gaps |

**Database Requirements**:
- 10 events total
- Categories: geopolitical (3), health (4), macro (3) - **MISSING**: regulatory, tech
- Confidence: 41-72 (40-60% below high threshold)
- Sources: 1-3 per event (40% have <=2 sources)
- Severity: All 0-100 valid
- Escalation: ~50% of narrative risks have history

**Success Criteria**:
```
✓ status = SUCCESS
✓ data_quality_score >= 60 and <= 69
✓ grade = D
✓ categories_covered = 3
✓ missing_categories = [regulatory, tech]
✓ events_audited = 10
✓ low_confidence_risks.length >= 5
✓ single_source_events.length >= 4
✓ missing_escalation_history.length >= 3
✓ breakdown.category_score = 12 (3/5 * 4)
✓ breakdown.confidence_score = 8-10 (20-30% high confidence)
✓ breakdown.source_score = 8-10 (40-50% multi-source)
✓ breakdown.severity_score = 20 (100% valid)
✓ breakdown.escalation_score = 8-10 (50% with history)
✓ recommendations.length >= 3 (specific action items)
```

---

### Scenario 3: Error Handling - Three Sub-Cases

#### 3a. Invalid Date Format

**Input**: `{"date": "01/04/2026"}` (MM/DD/YYYY instead of YYYY-MM-DD)

**Expected Output**:
```
status: FAILURE
failure_category: invalid_date
error_details: "Date format must be YYYY-MM-DD. Received: 01/04/2026"
recovery_suggestions: [
  "Use format YYYY-MM-DD (e.g., 2026-01-04)",
  "Ensure year is 4 digits, month and day are 2 digits",
  ...
]
```

**Success Criteria**:
```
✓ status = FAILURE
✓ failure_category = invalid_date
✓ error_details mentions YYYY-MM-DD format
✓ recovery_suggestions.length >= 1
✓ recovery_suggestions[0] provides example
✓ No audit_date, data_quality_score, or breakdown
```

---

#### 3b. Database Connection Failure

**Input**: `{"date": "2026-01-04"}`

**Database State**: Connection timeout or unavailable

**Expected Output**:
```
status: FAILURE
failure_category: connection_failure
error_details: "Failed to connect to database: Connection timeout after 30s"
recovery_suggestions: [
  "Verify database is running and accessible",
  "Check connection credentials (hostname, port, username)",
  "Verify network connectivity to database host",
  ...
]
```

**Success Criteria**:
```
✓ status = FAILURE
✓ failure_category = connection_failure
✓ error_details mentions database/connection
✓ recovery_suggestions.length >= 2
✓ Suggests connectivity check
✓ Suggests credentials/hostname check
✓ No partial audit data
```

---

#### 3c. No Events (Valid Empty State)

**Input**: `{"date": "2026-01-04"}` (e.g., weekend/holiday)

**Database State**: Query succeeds, returns 0 rows

**Expected Output**:
```
status: SUCCESS (NOT FAILURE - empty is valid)
audit_date: "2026-01-04"
data_quality_score: 0
grade: F
events_audited: 0
categories_covered: 0
missing_categories: [geopolitical, health, regulatory, macro, tech]
breakdown: {
  category_score: 0,
  confidence_score: 0,
  source_score: 0,
  severity_score: 0,
  escalation_score: 0
}
recommendations: [
  "No events collected for this date. Check if weekend/holiday.",
  "Verify news collection pipeline is running."
]
```

**Success Criteria**:
```
✓ status = SUCCESS (not FAILURE)
✓ data_quality_score = 0
✓ grade = F
✓ events_audited = 0
✓ categories_covered = 0
✓ All breakdown scores = 0
✓ missing_categories.length = 5 (all categories)
✓ All category_coverage = false
✓ Recommendations mention no events/weekend
```

---

## Scoring Formulas Reference

All formulas are validated in the test suite:

### Category Score (0-20)
```
category_score = 4 * (categories_covered / 5)

Example:
- 5/5 categories → 20 points
- 3/5 categories → 12 points (3/5 * 4 = 12)
- 0/5 categories → 0 points
```

### Confidence Score (0-20)
```
confidence_score = 20 * (events_with_confidence_gte_70 / total_events)

Thresholds:
- Minimum acceptable: 40 (events below flagged)
- High threshold: 70 (target for majority)

Example:
- 10/10 events >= 70 → 20 points
- 2/10 events >= 70 → 4 points
```

### Source Score (0-20)
```
source_score = 20 * (events_with_sources_gt_2 / total_events)

Requirement: Each event must have >2 sources

Example:
- 9/10 events >2 sources → 18 points
- 4/10 events >2 sources → 8 points
```

### Severity Score (0-20)
```
severity_score = 20 * (events_with_severity_0_to_100 / total_events)

Valid range: 0-100 (any other value indicates schema drift)

Example:
- 10/10 events valid → 20 points (all valid)
- 8/10 events valid → 16 points (2 invalid severity)
```

### Escalation Score (0-20)
```
escalation_score = 20 * (narrative_risks_with_escalation_history / total_narrative_risks)

Applies only to narrative risk types
If no narrative risks: escalation_score = 20 (default)

Example:
- 4/5 narrative risks with history → 16 points
- 0/5 narrative risks with history → 0 points
```

### Total Score (0-100)
```
data_quality_score = category_score + confidence_score + source_score + severity_score + escalation_score

All 5 dimensions summed
```

---

## Grade Assignment

| Grade | Score | Interpretation |
|-------|-------|-----------------|
| **A** | 90-100 | Excellent - Collection pipeline healthy |
| **B** | 80-89 | Good - Minor gaps, acceptable for analysis |
| **C** | 70-79 | Fair - Some issues need attention |
| **D** | 60-69 | Poor - Significant gaps affecting reliability |
| **F** | 0-59 | Failing - Critical issues, pipeline needs repair |

---

## Key Validation Rules

### All Scenarios Must Validate Against Schema
- File: `schemas/data-validator.schema.json`
- SuccessResponse for happy path and empty cases
- FailureResponse for error cases

### Consistent Field Requirements

**SuccessResponse fields**:
- status, audit_date, data_quality_score, grade
- category_coverage, categories_covered, categories_total
- events_audited, missing_categories
- low_confidence_risks, single_source_events, missing_escalation_history
- breakdown, breakdown_details, recommendations

**FailureResponse fields**:
- status, failure_category, error_details, recovery_suggestions

### Risk ID Format
- Pattern: `{category}_{type}_{id}`
- Categories: geopolitical, health, regulatory, macro, tech
- No duplicate risk_ids within response

### Timestamp Format
- All dates: YYYY-MM-DD (ISO 8601)
- audit_date matches input date parameter

---

## Test Execution Flow

### Step 1: Set Up Database Mock
- Happy path: 15 quality events across all 5 categories
- Edge case: 10 events with gaps (3 categories only)
- Error scenarios: Connection failure or 0 events

### Step 2: Execute Agent
- Call data-validator with input date
- Capture full JSON response

### Step 3: Validate Against Schema
- Verify JSON structure matches schema
- Check all required fields present
- Verify field types and value constraints

### Step 4: Run Success Criteria
- Check each assertion in test-execution-checklist.md
- Verify scoring calculations
- Validate recommendations specificity

### Step 5: Report Results
- Log pass/fail for each scenario
- Provide detailed failure explanations
- Reference validation rules for failures

---

## Integration Notes

### Database Queries
- Agent uses SELECT-only queries
- No INSERT/UPDATE/DELETE operations
- Queries against `attention_daily` table
- Validates using postgres-timescaledb skill

### Output Format
- All outputs are valid JSON
- Matches data-validator.schema.json
- Human-readable breakdown_details for all scores
- Specific, actionable recommendations

### Error Recovery
- Invalid date: Return FAILURE with format guidance
- Connection failure: Return FAILURE with recovery steps
- No events: Return SUCCESS with 0 score (valid state)
- Query timeout: Retry once, then FAILURE

---

## Files and Locations

**Primary Test Specification**:
```
C:/Users/kemos/Repos/gauntlet-agents/.claude/agents/investing/data-validator/docs/test-scenarios.json
```
- 320 lines of comprehensive test metadata
- Input/output specifications
- Success criteria and validation rules
- Scoring formula references

**Detailed Scenario Guide**:
```
C:/Users/kemos/Repos/gauntlet-agents/.claude/agents/investing/data-validator/docs/test-scenarios-README.md
```
- Narrative explanations for each scenario
- Example JSON inputs/outputs
- Scoring calculations with examples
- Integration notes

**Execution Checklist**:
```
C:/Users/kemos/Repos/gauntlet-agents/.claude/agents/investing/data-validator/docs/test-execution-checklist.md
```
- Field-by-field validation checklist
- Quick pass/fail verification
- Cross-scenario validation rules
- Summary passing criteria

---

## Coverage Summary

**5 Test Scenarios**:
1. ✓ Happy path (Grade A)
2. ✓ Edge case (Grade D)
3. ✓ Invalid date error
4. ✓ Connection error
5. ✓ Empty database (valid 0 score)

**5-Dimension Scoring Coverage**:
- ✓ Category score (0-20)
- ✓ Confidence score (0-20)
- ✓ Source score (0-20)
- ✓ Severity score (0-20)
- ✓ Escalation score (0-20)

**Error Handling Coverage**:
- ✓ Input validation (invalid date format)
- ✓ Database errors (connection failure)
- ✓ Valid empty states (0 events)

**Schema Validation**:
- ✓ SuccessResponse structure
- ✓ FailureResponse structure
- ✓ All required fields
- ✓ Type constraints

---

## Next Steps

To execute these tests:

1. **Set up test fixtures** for database mock (15 quality events, 10 partial events, error states)
2. **Run Happy Path** against test-scenarios.json Scenario 1
3. **Run Edge Case** against test-scenarios.json Scenario 2
4. **Run Error Tests** against test-scenarios.json Error Scenarios
5. **Validate outputs** using test-execution-checklist.md
6. **Generate report** with pass/fail for each scenario

---

**Status**: Test specifications generated and ready for test execution
**Created**: 2026-01-04
**Specification Version**: 1.0
**Schema**: data-validator.schema.json
**Total Scenarios**: 5 (2 functional + 3 error handling)
