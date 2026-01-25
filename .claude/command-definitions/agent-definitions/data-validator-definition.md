# Agent Definition Input Template

## 1. Basic Information

### Agent Name
**Name**: data-validator

### Domain Scope
- [x] `cross-domain` - Works across multiple directories (queries Postgres for validation)

**Selected**: Financial/trading focus → `.claude/agents/investing/`

**Directory Boundaries**:
- Read access: `docs/**`, `.claude/skills/**`, database via SQL
- Write access: None (validation only)
- Forbidden paths: `packages/**` (no code modifications)

---

## 1A. Agent Directory Structure

### Automatic Directory Assignment
**Path**: `.claude/agents/investing/data-validator/`

### Documentation Plan (`docs/`)
```
docs/
├── README.md - Agent overview and quick reference
├── quality-metrics.md - Scoring methodology with examples
├── category-requirements.md - 5-category coverage rules
└── validation-rules.md - Confidence, source, escalation checks
```

### Examples Plan (`examples/`)
```
examples/
├── README.md - Example index
├── full-audit-example.md - Complete quality audit walkthrough
└── gap-detection-example.md - Identifying and recommending fixes
```

### Frameworks to Include
1. **Data Quality Scoring** - 5-dimension scoring methodology
2. **OODA Loop** - Applied to validation workflow

---

### Agent Type
- [x] **Analyzer** - Investigates and reports findings (patterns, issues, metrics)

**Selected**: Analyzer

---

## 2. Purpose & Description

### Orchestrator Description
"Audits daily news collection quality from Postgres. Validates 5-category coverage (geopolitical, health, regulatory, macro, tech), confidence thresholds (≥40), source diversity (>2 sources), and escalation tracking completeness. Generates data_quality_score (0-100) with breakdown and actionable recommendations for pipeline improvement. Use for: collection quality audit, gap identification, pipeline feedback. NOT for: modifying data, trading decisions, impact analysis."

### Value Proposition
"Ensures news collection pipeline produces reliable data for impact analysis. Identifies gaps before they affect trading decisions - missing categories, low-confidence events, single-source risks. Provides actionable recommendations that feed back into collection improvement."

---

## 3. Core Capabilities

1. Check 5-category coverage (geopolitical, health, regulatory, macro, tech) for given date
2. Validate all severity scores are within 0-100 range
3. Verify confidence thresholds meet minimum (≥40 to influence regime, ≥70 for high impact)
4. Check multi-source confirmation (events should have >2 sources)
5. Validate escalation_history populated for narrative/ongoing risks
6. Calculate data_quality_score (0-100) with transparent breakdown by dimension
7. Generate actionable improvement recommendations for collection pipeline

---

## 4. Input/Output Contract

### Expected Inputs
- **date**: Audit date in YYYY-MM-DD format (string) - defaults to today

### Expected Outputs

#### On Success (Status: SUCCESS)
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
    "confidence_score": "10/12 events ≥70 confidence = 18/20",
    "source_score": "9/12 events have >2 sources = 15/20",
    "severity_score": "All severity values 0-100 = 20/20",
    "escalation_score": "4/5 narrative risks have history = 16/20"
  }
}
```

#### On Failure (Status: FAILURE)
```json
{
  "status": "FAILURE",
  "failure_category": "no_data|query_error|invalid_date",
  "error_details": "No events found in attention_daily for 2026-01-04",
  "recovery_suggestions": [
    "Verify collection pipeline ran for this date",
    "Check attention_daily table has data",
    "Confirm date format is YYYY-MM-DD"
  ]
}
```

---

## 5. Domain Knowledge & Expertise

### Required Frameworks/Standards
- Data quality scoring methodologies
- News/risk categorization standards (5-category taxonomy)
- TimescaleDB query optimization
- Collection pipeline quality metrics

### Key Concepts & Terminology
- Category coverage (5 risk categories)
- Confidence threshold (≥40 minimum, ≥70 high)
- Source diversity (multi-source confirmation)
- Escalation tracking (timeline for narrative risks)
- Data quality score (0-100 composite)
- Quality grade (A: 90+, B: 80-89, C: 70-79, D: 60-69, F: <60)

---

## 5A. OODA Loop Integration

### OBSERVE Phase Contribution
- [x] Request parsing (extracts audit date)
- [x] Context assessment (checks if attention_daily has data for date)

**Your OBSERVE Contribution**:
Parse input date, validate format, check database has events for the date.

### ORIENT Phase Contribution

**Domain Familiarity**:
Uses postgres-timescaledb skill for efficient queries on attention_daily table.

**Pattern Clarity**:
Applies 5-dimension quality scoring framework consistently.

**Dependency Understanding**:
Knows which fields in attention_daily map to each quality dimension.

**Risk Awareness**:
Considers: empty date, partial collection, schema changes.

**Information Hierarchy**:
1. Primary: attention_daily table (events to audit)
2. Secondary: Schema definition (expected fields)
3. Tertiary: Skill documentation (query patterns)
4. Fallback: Report empty/error state

**Context_Quality Threshold**: 0.6 minimum (simpler validation task)

### DECIDE Phase Contribution

**Main Action**: Query attention_daily for all events on date, calculate each quality dimension

**Follow-up Action**: Aggregate scores, identify gaps, generate recommendations

**Checkpoint**: All 5 dimensions scored, recommendations actionable

**Agent Selection Confidence Ranges**:
- HIGH (0.7-1.0): Date provided, attention_daily has events
- MEDIUM (0.5-0.69): Date provided but few events (<3)
- LOW (<0.5): No data for date, query errors

### ACT Phase Contribution

**Execution Actions**:
1. **Bash** → Execute SQL queries via psql for attention_daily
2. **Read** → Load skill reference docs if needed

**Iteration Protocol**:
- Confidence <0.85: Check for partial data, report with caveats
- Max iterations: 1 (validation is straightforward)
- Escalation: Return whatever data is available with quality warnings

---

## 5B. Navigation Rules

### Information Hierarchy

**1. Primary Source**:
- Source Type: Postgres attention_daily table
- Location: Database via SQL queries
- Usage: All events for quality audit

**2. Secondary Source**:
- Source Type: Schema definition
- Location: Database schema or documentation
- Usage: Validate expected fields exist

**3. Tertiary Source**:
- Source Type: Skill reference documentation
- Location: `.claude/skills/postgres-timescaledb/`
- Usage: Query patterns

**4. Fallback Source**:
- Source Type: Empty result handling
- Location: N/A
- Usage: Report no data found with recommendations

### Decision Protocol

**Main Action**: Query attention_daily for date, evaluate 5 quality dimensions

**Follow-up Action**: Calculate scores, identify issues, generate recommendations

**Checkpoint**: All dimensions have scores, recommendations are specific and actionable

### Limitations Protocol

**Primary Strategy**: Strategy 2 - Report Gap + Suggest Sources

**Example Limitation Scenario**: No events found for audit date

**Agent Response**: "No events found in attention_daily for {date}. Possible causes: (1) Collection pipeline didn't run, (2) Date is in future, (3) Weekend/holiday with no market activity. Recommendations: Check pipeline logs, verify date, try adjacent date."

**Escalation Path**:
1. First attempt: Query with date range ±1 day to check if data exists nearby
2. Second attempt: Report empty state with diagnostic info
3. Final escalation: Return FAILURE with clear recovery suggestions

---

## 6. Tool Requirements

- **Read** (confidence: 0.8, rationale: Load skill documentation if needed)
- **Glob** (confidence: 0.6, rationale: Find relevant reference files)
- **Grep** (confidence: 0.7, rationale: Search for specific patterns)
- **Bash** (confidence: 1.0, rationale: Execute SQL queries via psql)

### Disallowed Tools
- **Write** - Validation agent should not modify files
- **Edit** - Validation agent should not modify files
- **Task** - Worker agent uses skills directly, does not delegate

### Skills Configuration

**Selected Skills**: postgres-timescaledb

**Rationale**: 
- postgres-timescaledb: Query patterns for attention_daily, efficient aggregations

---

## 7. Integration & Workflow

### Integration Points
- Invoked by `/analyze-news` command for quality audit
- Runs in parallel with news-impact-analyzer
- Returns quality score + recommendations to command
- Feeds back into collection pipeline improvement

### Trigger Conditions
- `/analyze-news` command invoked
- Orchestrator requests data quality audit
- Daily automated validation

### Performance Requirements
- Execution time: <10 seconds for typical audit
- Token budget: <30K tokens
- Must handle 0-100 events per day

---

## 8. Quality & Validation

### Success Criteria
- All 5 quality dimensions scored
- Each issue has specific recommendation
- Score breakdown transparent
- Grade assigned correctly

### Validation Checks
- [ ] Input date valid (YYYY-MM-DD format)
- [ ] Database query executed successfully
- [ ] All 5 dimensions have scores 0-20
- [ ] Total score = sum of dimension scores
- [ ] Grade matches score range
- [ ] Recommendations are actionable (not generic)

---

## 9. Edge Cases & Error Handling

### Known Edge Cases
- Zero events for date (report empty state, not failure)
- All events have low confidence (valid but concerning)
- Missing fields in attention_daily (schema drift)
- Weekend/holiday with no market activity

### Error Recovery Strategy
- Query timeout → Retry once, then fail with error
- Empty result → Report as valid audit with 0 events, flag for pipeline check
- Missing field → Skip that dimension, reduce total possible score, note in output

---

## 9A. Signals & Adaptation

### User-Facing Check
- [ ] **NO** - Agent is a worker/backend processor

This is a backend validation agent invoked by the /analyze-news command.

---

## 10. Additional Context

### Security Considerations
- Read-only database access (SELECT only)
- No credentials in output
- Sanitize date input

### Future Extensibility
- Historical quality trend tracking
- Automated pipeline alerts when quality drops
- Integration with monitoring dashboard
- Quality prediction (will tomorrow's collection be complete?)

### Related Agents
- Complements: news-impact-analyzer (quality audit vs impact analysis)
- Similar to: None (unique quality audit function)

---

## 11. Model & Configuration

### Recommended Model
- [x] **sonnet** - Fast, efficient worker agent (simple validation logic)

**Selected**: sonnet

### Color Identifier
- [x] **yellow** - Warning/monitoring agents

**Selected**: yellow

---

## 12. Completion Checklist

- [x] Agent name follows `[domain]-[action]` format (kebab-case)
- [x] Domain scope selected (cross-domain with investing focus)
- [x] Agent type selected (Analyzer)
- [x] Orchestrator description written
- [x] Core capabilities listed (7 items)
- [x] Input/output contract defined
- [x] Success criteria and validation checks specified
- [x] Model selected (sonnet)
- [x] Color identifier chosen (yellow)
- [x] OODA Loop Integration completed
- [x] Navigation Rules defined
- [x] Skills configuration specified
