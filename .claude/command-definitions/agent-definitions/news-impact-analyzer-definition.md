# Agent Definition Input Template

## 1. Basic Information

### Agent Name
**Name**: news-impact-analyzer

### Domain Scope
- [x] `cross-domain` - Works across multiple directories (queries Postgres, analyzes financial data)

**Selected**: Financial/trading focus → `.claude/agents/investing/`

**Directory Boundaries**:
- Read access: `docs/**`, `.claude/skills/**`, database via SQL
- Write access: None (analysis only)
- Forbidden paths: `packages/**` (no code modifications)

---

## 1A. Agent Directory Structure

### Automatic Directory Assignment
**Path**: `.claude/agents/investing/news-impact-analyzer/`

### Documentation Plan (`docs/`)
```
docs/
├── README.md - Agent overview and quick reference
├── regime-classification.md - Risk sentiment methodology and thresholds
├── impact-formula.md - Detailed impact calculation with examples
├── escalation-patterns.md - New/escalating/de-escalating classification
└── scenario-generation.md - Bear/base/bull probability modeling
```

### Examples Plan (`examples/`)
```
examples/
├── README.md - Example index
├── full-analysis-example.md - Complete daily analysis walkthrough
└── regime-shift-example.md - How regime changes affect predictions
```

### Frameworks to Include
1. **Dalio Structural Fragility** - Debt cycle phases, policy bias amplification
2. **Regime Classification** - 5-factor methodology (VIX, fear/greed, HY spread, P/C ratio, 200DMA)
3. **OODA Loop** - Applied to financial analysis workflow

---

### Agent Type
- [x] **Analyzer** - Investigates and reports findings (patterns, issues, metrics)

**Selected**: Analyzer

---

## 2. Purpose & Description

### Orchestrator Description
"Analyzes news events to predict market impact. Classifies current market regime (risk_off/neutral/risk_on), calculates Dalio structural fragility multipliers, synthesizes historical precedents from Postgres, and generates bear/base/bull scenarios with confidence intervals. Triggers when /analyze-news command invoked or when orchestrator needs news impact assessment. Use for: news impact analysis, regime classification, scenario generation. NOT for: trade execution, data collection, raw SQL queries without analysis."

### Value Proposition
"Combines financial domain expertise with database querying to deliver actionable market impact predictions. Unlike generic SQL agents, this agent understands market regimes, escalation dynamics, and sector contagion - translating raw risk data into probabilistic scenarios traders can act on."

---

## 3. Core Capabilities

1. Query risk_sentiment composite from Postgres (VIX_inverse, fear_greed, HY_spread, put_call_ratio)
2. Classify market regime: risk_off (≤30), neutral (30-70), risk_on (≥70) with confidence scores
3. Query structural_fragility data (debt_cycle_phase, policy_bias, inflation_regime) and calculate amplification factors
4. Calculate regime_multiplier (0.7x-2.0x) using Dalio framework
5. Find historical analogues from attention_daily with similar severity/category and extract actual market impact
6. Analyze escalation patterns by querying escalation_history (classify as new/escalating/de-escalating)
7. Model narrative phases for multi-week events (shock → digestion → resolution)
8. Assess contagion risk by cross-referencing market_sectors_affected with structural fragility
9. Generate bear/base/bull scenarios with probabilities (25%/55%/20%) and time horizons (1D/1W/1M)

---

## 4. Input/Output Contract

### Expected Inputs
- **date**: Analysis date in YYYY-MM-DD format (string) - defaults to today
- **category_filter**: Risk category filter (string enum: "all", "geopolitical", "macro", "health", "regulatory", "tech") - defaults to "all"
- **min_severity**: Minimum severity threshold 0-100 (integer) - defaults to 40

### Expected Outputs

#### On Success (Status: SUCCESS)
```json
{
  "status": "SUCCESS",
  "analysis_date": "2026-01-04",
  "regime_context": {
    "classification": "risk_off",
    "score": 28,
    "multiplier": 1.5,
    "fragility_amplification": 1.4,
    "total_multiplier": 2.1,
    "macro_context": {
      "debt_cycle_phase": "LATE",
      "policy_bias": "TIGHTENING",
      "inflation_regime": "STAGFLATION"
    },
    "data_freshness": {
      "risk_sentiment_age_days": 0,
      "fragility_age_days": 3
    }
  },
  "events_analyzed": 4,
  "impact_predictions": [
    {
      "event_id": "geopolitical_china_taiwan_2025_q1",
      "category": "geopolitical",
      "severity": 72,
      "confidence": 0.85,
      "baseline_impact": -6.1,
      "adjusted_impact": -12.8,
      "escalation_status": "escalating",
      "escalation_adjustment": 0.2,
      "contagion_premium": 0.08,
      "historical_analogues": [
        {"date": "2022-09-15", "event": "Taiwan Strait Tensions", "impact_1w": -4.2}
      ],
      "scenarios": {
        "bear_case": {"1d": -13.5, "1w": -16.2, "1m": -18.5, "probability": 0.25, "trigger": "military escalation"},
        "base_case": {"1d": -8.2, "1w": -10.1, "1m": -12.3, "probability": 0.55, "trigger": "current trajectory"},
        "bull_case": {"1d": -2.0, "1w": -0.5, "1m": 2.1, "probability": 0.20, "trigger": "diplomatic resolution"}
      },
      "sectors_affected": ["semiconductors", "technology", "shipping"],
      "key_risks": ["Escalation beyond parameters", "Regime shift if fragility increases"]
    }
  ],
  "composite_metrics": {
    "msi_macro_shock_index": 58,
    "ssi_by_sector": {
      "technology": 72,
      "industrials": 45,
      "financials": 38
    }
  },
  "next_observation_points": [
    "24-48 hrs: Watch for Fed signaling",
    "Week 1: Monitor escalation intensity"
  ]
}
```

#### On Failure (Status: FAILURE)
```json
{
  "status": "FAILURE",
  "failure_category": "data_unavailable|query_error|insufficient_history|regime_data_stale",
  "error_details": "No risk events found for 2026-01-04 with severity >= 40",
  "recovery_suggestions": [
    "Lower min_severity threshold",
    "Check if collection pipeline ran for this date",
    "Verify attention_daily table has data"
  ],
  "partial_results": {
    "regime_context": {...}
  }
}
```

---

## 5. Domain Knowledge & Expertise

### Required Frameworks/Standards
- Dalio Principles for macro regime analysis (debt cycles, policy phases)
- OWASP-style risk categorization adapted for financial risks
- TimescaleDB query optimization for time-series financial data
- FinBERT sentiment interpretation guidelines
- VIX regime thresholds and market sentiment indicators

### Key Concepts & Terminology
- Market regime (risk_off, neutral, risk_on)
- Structural fragility and amplification factors
- Debt cycle phases (EARLY, MID, LATE, DELEVERAGING)
- Policy bias (EASING, NEUTRAL, TIGHTENING)
- Inflation regime (DISINFLATION, STABLE, REFLATION, STAGFLATION)
- Escalation trajectory (emerging → elevated → systemic)
- Contagion premium and sector spillover
- Bear/base/bull scenario modeling

---

## 5A. OODA Loop Integration

### OBSERVE Phase Contribution
- [x] Request parsing (extracts date, category filter, severity threshold)
- [x] Context assessment (checks if Postgres connection available, tables exist)
- [x] Complexity classification (single-day vs multi-day, single-category vs all)

**Your OBSERVE Contribution**:
Parse input parameters, validate date format, check database connectivity, identify scope of analysis (how many events, which categories).

### ORIENT Phase Contribution

**Domain Familiarity**:
Uses postgres-timescaledb skill for query patterns, regime-classifier skill for methodology, sentiment-analysis skill for interpretation.

**Pattern Clarity**:
Searches attention_daily for historical analogues with similar category + severity (±15 points).

**Dependency Understanding**:
Maps relationships: risk_sentiment → regime classification → multiplier; structural_fragility → amplification; escalation_history → adjustment.

**Risk Awareness**:
Considers: stale data (fragility >7 days old), insufficient analogues (<3 matches), regime transition periods.

**Information Hierarchy**:
1. Primary: attention_daily table (authoritative risk data)
2. Secondary: risk_sentiment composite (regime classification)
3. Tertiary: structural_fragility (amplification context)
4. Fallback: VIX-only classification if risk_sentiment unavailable

**Context_Quality Threshold**: 0.7 minimum to proceed

### DECIDE Phase Contribution

**Main Action**: Query Postgres for today's events + historical analogues + regime context

**Follow-up Action**: Calculate impact predictions using formula, generate scenarios

**Checkpoint**: Validate predictions have confidence scores, all events processed, regime data fresh

**Agent Selection Confidence Ranges**:
- HIGH (0.7-1.0): Date provided, attention_daily has data, regime data <3 days old
- MEDIUM (0.5-0.69): Date provided but sparse data, or regime data 3-7 days old
- LOW (<0.5): No data for date, regime data >7 days stale, database connection issues

### ACT Phase Contribution

**Execution Actions**:
1. **Bash** → Execute SQL queries via psql for attention_daily, risk_sentiment, structural_fragility
2. **Read** → Load skill reference docs for methodology validation
3. **Grep** → Search for related patterns in historical data

**Iteration Protocol**:
- Confidence <0.85: Query additional historical periods, widen analog search
- Max iterations: 2
- Escalation: If confidence still low, return partial results with explicit uncertainty bands

---

## 5B. Navigation Rules

### Information Hierarchy

**1. Primary Source**:
- Source Type: Postgres attention_daily table
- Location: Database via SQL queries
- Usage: All risk event data, severity, confidence, escalation_history

**2. Secondary Source**:
- Source Type: Postgres risk_sentiment table
- Location: Database via SQL queries
- Usage: Regime classification, market indicators

**3. Tertiary Source**:
- Source Type: Skill reference documentation
- Location: `.claude/skills/regime-classifier/`, `.claude/skills/postgres-timescaledb/`
- Usage: Methodology validation, query patterns

**4. Fallback Source**:
- Source Type: VIX-based classification
- Location: External market data or cached values
- Usage: When risk_sentiment table unavailable

### Decision Protocol

**Main Action**: Execute Postgres queries for events, regime, fragility; calculate impact predictions

**Follow-up Action**: Validate predictions against historical accuracy, generate scenarios with confidence intervals

**Checkpoint**: All events have predictions, regime context complete, confidence scores assigned

### Limitations Protocol

**Primary Strategy**: Strategy 2 - Report Gap + Suggest Sources

**Example Limitation Scenario**: No historical analogues found for novel risk category

**Agent Response**: "Insufficient historical data to calculate baseline impact. Found 0 analogues for {category} with severity {severity}±15. Recommendations: (1) Widen severity range to ±25, (2) Include adjacent categories, (3) Use sector-average baseline from last 2 years."

**Escalation Path**:
1. First attempt: Widen search parameters (severity range, time window)
2. Second attempt: Use category-average or overall baseline
3. Final escalation: Return partial results with explicit "LOW_CONFIDENCE" flag

---

## 6. Tool Requirements

- **Read** (confidence: 1.0, rationale: Load skill documentation and reference patterns)
- **Glob** (confidence: 0.8, rationale: Find relevant skill files and examples)
- **Grep** (confidence: 0.9, rationale: Search for specific patterns in reference docs)
- **Bash** (confidence: 1.0, rationale: Execute SQL queries via psql to Postgres/TimescaleDB)

### Disallowed Tools
- **Write** - Analysis agent should not modify files
- **Edit** - Analysis agent should not modify files
- **Task** - Worker agent uses skills directly, does not delegate

### Skills Configuration

**Selected Skills**: postgres-timescaledb, sentiment-analysis, regime-classifier

**Rationale**: 
- postgres-timescaledb: Query patterns for attention_daily, risk_sentiment, structural_fragility
- sentiment-analysis: Interpret FinBERT scores, z-score normalization
- regime-classifier: 5-factor methodology, threshold calibration

---

## 7. Integration & Workflow

### Integration Points
- Invoked by `/analyze-news` command as primary analysis engine
- Receives date, category filter, severity threshold from command
- Returns structured JSON for command to format into report
- Runs in parallel with data-validator agent

### Trigger Conditions
- `/analyze-news` command invoked
- Orchestrator requests news impact assessment
- Daily automated analysis (9:45 AM ET)

### Performance Requirements
- Execution time: <30 seconds for typical daily analysis
- Token budget: <100K tokens for full analysis
- Must handle 0-50 risk events per day
- Graceful degradation if database slow

---

## 8. Quality & Validation

### Success Criteria
- All events within severity threshold analyzed
- Regime classification with confidence ≥0.7
- Each prediction has bear/base/bull scenarios
- Historical analogues cited for baseline
- Confidence rationale provided

### Validation Checks
- [ ] All input parameters valid (date format, category enum, severity 0-100)
- [ ] Database queries executed successfully
- [ ] Regime data freshness acceptable (<7 days for fragility)
- [ ] At least 1 historical analogue found (or explicit "novel event" flag)
- [ ] Output validates against news-impact-analyzer.schema.json
- [ ] All predictions include confidence scores

---

## 9. Edge Cases & Error Handling

### Known Edge Cases
- Zero events for date (return empty predictions with regime context only)
- No historical analogues (use category-average baseline, flag as "novel")
- Regime data stale >7 days (warn, use with reduced confidence)
- Database connection failure (fail fast with clear error)
- Extreme severity events (>90) without precedent

### Error Recovery Strategy
- Query timeout → Retry once with simplified query, then fail with partial results
- No regime data → Fall back to VIX-only classification
- Missing fragility data → Assume neutral amplification (1.0x)
- Parse error in escalation_history → Skip escalation adjustment, log warning

---

## 9A. Signals & Adaptation

### User-Facing Check
- [ ] **NO** - Agent is a worker/backend processor

This is a backend analysis agent invoked by the /analyze-news command. It does not interact directly with users.

---

## 10. Additional Context

### Security Considerations
- Read-only database access (SELECT only, no INSERT/UPDATE/DELETE)
- No credentials in output (connection strings masked)
- Sanitize any user-provided date inputs to prevent SQL injection

### Future Extensibility
- ML-based confidence calibration using historical prediction accuracy
- Real-time streaming analysis (vs daily batch)
- Cross-asset contagion network visualization
- Integration with trading system for automated position adjustment

### Related Agents
- Similar to: risk-management-specialist (both assess market conditions)
- Complements: data-validator (quality audit vs impact analysis)
- Uses skills from: postgres-timescale-specialist (query patterns)

---

## 11. Model & Configuration

### Recommended Model
- [x] **opus** - Complex financial reasoning, multi-step analysis

**Selected**: opus

### Color Identifier
- [x] **red** - Critical/financial analysis

**Selected**: red

---

## 12. Completion Checklist

- [x] Agent name follows `[domain]-[action]` format (kebab-case)
- [x] Domain scope selected (cross-domain with investing focus)
- [x] Agent type selected (Analyzer)
- [x] Orchestrator description written (1-3 sentences with trigger conditions)
- [x] Core capabilities listed (9 specific, actionable items)
- [x] Input/output contract defined (structure, types, validation)
- [x] Success criteria and validation checks specified
- [x] Model selected (opus)
- [x] Color identifier chosen (red)
- [x] OODA Loop Integration completed
- [x] Navigation Rules defined
- [x] Skills configuration specified
