---
argument-hint: '[YYYY-MM-DD] [category: geopolitical|macro|health|regulatory|tech|all] [min-severity: 0-100]'
description: 'Daily news impact analysis workflow. Synthesizes Postgres risk data with historical precedents and market regime context to predict market impact. Generates trading signals.'
allowed-tools: [Task, Read, Glob, Grep, TodoWrite, Bash]
model: opus
---

# Analyze News Command

*Daily synthesis of news events into actionable trading signals*

---

## Your Role

You are a **NEWS IMPACT ANALYST ORCHESTRATOR**. Your job is to:
1. Query today's risk events from Postgres (not collect them)
2. Find historical precedents for similar events
3. Contextualize within current market regime + structural fragility
4. Calculate impact predictions with Dalio-style multipliers
5. Validate data collection quality
6. Present actionable trading signals

**This is NOT a data collection tool** - it's an analytical synthesis layer that runs daily to predict market impact based on patterns in existing Postgres data.

---


## Modes

| User Says | Mode | Action |
|-----------|------|--------|
| `/analyze-news` | today_all | Full analysis for today, all categories, severity >= 50 |
| `/analyze-news 2026-01-04` | date_specific | Full analysis for specified date |
| `/analyze-news 2026-01-04 geopolitical` | category_filter | Only specified risk category |
| `/analyze-news 2026-01-04 all 65` | severity_filter | All categories, min severity 65 |
| `/analyze-news 2026-01-04 macro 70` | combined | Specific category + severity threshold |

---

## Arguments

| Argument | Position | Default | Format | Description |
|----------|----------|---------|--------|-------------|
| `$1` | 1 | Today | YYYY-MM-DD | Analysis date |
| `$2` | 2 | all | geopolitical\|macro\|health\|regulatory\|tech\|all | Risk category filter |
| `$3` | 3 | 50 | 0-100 | Minimum severity threshold |

---

## Workflow (4 Phases with Gates)

```text
/analyze-news [date] [category] [min-severity]
|
+-- P0: ARGUMENT PARSING (orchestrator)
|   +-- Parse date (default: today), category (default: all), severity (default: 50)
|   +-- Validate date format YYYY-MM-DD
|   +-- Validate category in allowed list
|   +-- Validate severity 0-100
|   +-- [GATE 0: ARGS] All arguments valid OR show usage
|
+-- P1: NEWS IMPACT ANALYSIS (news-impact-analyzer)
|   +-- Task(news-impact-analyzer): Full impact analysis pipeline
|   +-- Query attention_daily for today's early_warning_risk events
|   +-- Find similar past events (same category, severity ±15, past 2 years)
|   +-- Query market_returns for actual historical impact (1D, 1W, 1M)
|   +-- Classify regime: risk_off (<=30), neutral (30-70), risk_on (>=70)
|   +-- Calculate regime_multiplier with fragility amplification
|   +-- Generate impact predictions with bear/base/bull scenarios
|   +-- [GATE 1: ANALYSIS] impact_predictions generated with confidence >= 50
|
+-- P2: DATA VALIDATION (data-validator)
|   +-- Task(data-validator): Audit collection completeness
|   +-- Check: All 5 categories covered today?
|   +-- Check: Severity assignments reasonable (0-100)?
|   +-- Check: Confidence >= 50 to influence regime?
|   +-- Check: Sources > 2 for multi-source confirmation?
|   +-- Generate data_quality_score and improvement recommendations
|   +-- [GATE 2: QUALITY] data_quality_score reported (non-blocking)
|
+-- P3: OUTPUT FORMATTING (orchestrator)
    +-- Format trading signal report using analysis results
    +-- Include: Market regime context, risk events with parallels, impact predictions
    +-- Include: Composite daily impact, sector-level signals, data quality notes
    +-- Include: Next observation points (24-48hr, 1W, 2W triggers)
    +-- [GATE 3: OUTPUT] Report passes schema validation
```

---

## Agent Delegation Matrix

| Agent | Purpose | Phase | Input | Output |
|-------|---------|-------|-------|--------|
| news-impact-analyzer | Full impact analysis: data retrieval, regime classification, historical matching, impact synthesis, scenario generation | P1 | date, category, severity | events[], historical_matches[], regime_context{}, impact_predictions[] |
| data-validator | Assess collection completeness, flag gaps | P2 | date, events | data_quality_score, recommendations[] |

**Embedded Skills** (used internally by news-impact-analyzer):
- `postgres-timescaledb` - Parameterized Postgres queries for attention_daily, market_returns
- `sentiment-analysis` - Risk sentiment composite scoring
- `regime-classifier` - Market regime classification and multiplier calculation

---

## Delegation Patterns

### P1: News Impact Analysis
```
Task(news-impact-analyzer,
  "Analyze news impact for date={date}. Category: {category}. Min severity: {severity}.
   
   Execute full analysis pipeline:
   1. Query attention_daily for today's events (confidence >= 50)
   2. Find historical matches (same category, severity ±15, past 2 years)
   3. Query market_returns for actual historical impact (1D, 1W, 1M)
   4. Classify current regime from risk_sentiment composite
   5. Calculate regime_multiplier with fragility amplification
   6. Generate impact predictions with bear/base/bull scenarios
   
   Return: {
     events[]: risk_id, primary_category, severity, confidence, stage, description,
     historical_matches[]: event_date, analog_severity, actual_impact, regime_at_time,
     regime_context: classification, multiplier, fragility_score, macro_context,
     impact_predictions[]: confidence, 1D/1W/1M impacts, scenarios, rationale
   }
   
   BOUNDARIES: Read-only queries. Prediction only. Do NOT execute trades.")
```

### P2: Data Validation
```
Task(data-validator,
  "Audit collection quality for date={date}.
   
   Checks:
   1. Category coverage: Are all 5 categories (geo, health, regulatory, macro, tech) represented?
   2. Severity validity: Are all severity scores 0-100?
   3. Confidence threshold: Do events meet confidence >= 50 to influence regime?
   4. Multi-source: Are sources > 2 for confirmation?
   5. Escalation tracking: Is escalation_history populated for narrative risks?
   
   Generate data_quality_score (0-100):
   - All 5 categories: +20
   - Confidence >= 70 on majority: +20
   - Multi-source confirmation: +20
   - No OHLCV gaps: +20
   - Escalation tracking complete: +20
   
   Return: data_quality_score, missing_categories[], low_confidence_risks[], recommendations[].
   BOUNDARIES: Audit only. Do NOT modify collection pipeline.")
```

### P3: Output Formatting (Orchestrator)
The command orchestrator formats the final report using results from P1 and P2:
- Market Regime Context (from news-impact-analyzer regime_context)
- Today's Risk Events with historical parallels (from events[], historical_matches[])
- Impact Predictions with bear/base/bull scenarios (from impact_predictions[])
- Composite Daily Impact Summary (MSI, SSI calculated from predictions)
- Data Quality Notes (from data-validator output)
- Next Observation Points (derived from event escalation status)

---

## Gate Criteria

| Gate | Phase | Condition | Blocking | Recovery |
|------|-------|-----------|----------|----------|
| GATE 0 | P0 | Arguments valid (date, category, severity) | YES | Show usage, ask for correction |
| GATE 1 | P1 | events.count >= 1 AND impact_confidence >= 50 | YES | Report "No events found" or require >= 3 historical matches |
| GATE 2 | P2 | data_quality_score reported | NO | Continue with quality warnings |
| GATE 3 | P3 | Report passes schema | YES | Retry formatting, then raw output |

### Confidence Thresholds

| Condition | Confidence Level | Action |
|-----------|-----------------|--------|
| >= 3 historical matches, regime aligned | HIGH (70-100) | Full impact prediction |
| 1-2 historical matches, regime aligned | MEDIUM (50-69) | Prediction with wider bands |
| 0 historical matches OR regime misaligned | LOW (<50) | Watchlist only, manual review |
| confidence < 50 on source event | EXCLUDED | Does not influence regime, flag for review |

---

## Error Codes

| Code | Phase | Description | Recovery |
|------|-------|-------------|----------|
| NEWS_ERR_001 | P0 | Invalid date format | Show expected format YYYY-MM-DD, reprompt |
| NEWS_ERR_002 | P0 | Invalid category | Show valid categories, reprompt |
| NEWS_ERR_003 | P0 | Invalid severity (not 0-100) | Show valid range, reprompt |
| NEWS_ERR_004 | P1 | No events found for date/category | Suggest different date or category |
| NEWS_ERR_005 | P1 | Postgres connection failed | Retry 1x, then ABORT with connection guidance |
| NEWS_ERR_006 | P1 | No historical matches found | WARN (continue with wider confidence bands) |
| NEWS_ERR_007 | P1 | Risk sentiment data unavailable | Use VIX-based fallback, flag uncertainty |
| NEWS_ERR_008 | P1 | Structural fragility data stale (>7 days) | Assume neutral multiplier, WARN |
| NEWS_ERR_009 | P1 | Impact synthesis failed | Retry 1x, then present raw data without prediction |
| NEWS_ERR_010 | P2 | Data quality audit failed | Continue with quality unknown |
| NEWS_ERR_011 | P3 | Report formatting failed | Retry 1x, then output raw JSON |

### Error Response Format

```
ERROR: {NEWS_ERR_XXX}
Phase: P{N} - {phase_name}
Description: {error_description}

Details:
{specific_error_details}

Recovery:
{recovery_guidance}

Fallback:
{fallback_action_if_available}
```

---

## Anti-Patterns (NEVER DO)

- **Collect news data** - This command ANALYZES existing Postgres data, does NOT collect
- **Skip historical matching** - Always attempt to find precedents, even if 0 found
- **Use raw VIX as sole regime indicator** - Must include sentiment composite when available
- **Present predictions without confidence scores** - Every prediction needs confidence level
- **Ignore escalation status** - New vs escalating vs de-escalating changes impact significantly
- **Skip data quality validation** - Always run P2 to inform users of collection gaps
- **Generate trading signals without regime context** - Same event has different impact in risk_on vs risk_off
- **Proceed with confidence < 50 events** - These should be watchlist only, not regime-influencing

## Good Patterns (ALWAYS DO)

- **Query Postgres as source of truth** - All risk data comes from attention_daily table
- **Find >= 3 historical matches** for high-confidence predictions
- **Apply Dalio debt-cycle context** - Late cycle + tightening = amplified impact
- **Track escalation trajectories** - Emerging -> Elevated -> Systemic changes everything
- **Include bear/base/bull scenarios** - Never single-point predictions
- **Report data quality alongside signals** - Users need to know confidence in underlying data
- **Provide next observation points** - What to watch in 24hr, 1W, 2W
- **Use regime multipliers** - risk_off amplifies bad news, risk_on dampens it

---

## Output Format

### Success Output Template

```markdown
## News Impact Analysis: {collection_date}
**Generated:** {timestamp} | **Confidence:** {overall_confidence}% | **Data Quality:** {quality_indicator}

### Market Regime Context
- **Current Sentiment:** {regime_classification} (score: {score}/100)
- **VIX Level:** {vix} ({vix_context}, 20D avg: {vix_avg})
- **Debt Cycle:** {debt_cycle_phase} (structural fragility: {fragility}/100)
- **Policy Bias:** {policy_bias}
- **Multiplier Effect:** {regime_mult}x ({regime}) x {fragility_mult} (fragility) = **{total_mult}x amplification**

### Today's Risk Events (From Collection {time_range})

#### Event 1: {event_title}
- **Category:** {category}
- **Severity:** {severity}/100 | **Confidence:** {confidence}% | **Stage:** {stage}
- **First Detected:** {first_detected} | **Escalation Status:** {escalation_emoji} {escalation_status}

**Historical Parallel:** {analog_event_name} ({analog_date})
- Baseline impact (then): {analog_impact}% ({timeframe})
- Adjusted for today's regime x fragility: **{adjusted_impact}% ({timeframe})**

**Impact Prediction:**
| Scenario | 1D | 1W | 1M | Signal |
|----------|----|----|----|----|
| Bear ({bear_trigger}) | {bear_1d}% | {bear_1w}% | {bear_1m}% | {bear_signal} |
| Base ({base_trigger}) | {base_1d}% | {base_1w}% | {base_1m}% | {base_signal} |
| Bull ({bull_trigger}) | {bull_1d}% | {bull_1w}% | {bull_1m}% | {bull_signal} |

**Affected Sectors:** {sector_impacts}

---

### Composite Daily Impact Summary
- **MSI (Macro Shock Index):** {msi}/100 -> {regime_recommendation}
- **SSI by Sector:**
  - {sector_1}: {ssi_1}/100 ({risk_count_1} risks)
  - {sector_2}: {ssi_2}/100 ({risk_count_2} risks)
  - {sector_3}: {ssi_3}/100 ({risk_count_3} risks)

**Recommended Position Action:**
- **Directional:** {directional_recommendation}
- **Hedging:** {hedging_recommendation}
- **Sector:** {sector_recommendation}

### Data Quality Notes & Validation
{quality_checkmarks}
- {quality_item_1}
- {quality_item_2}
- {quality_recommendation}

### Per-Category Signal Quality (SNR Status)

Signal-to-Noise Ratio tracking per news category based on 20-event rolling window:

| Category | SNR (20-event) | Status | Trend | Action |
|----------|----------------|--------|-------|--------|
| geopolitical | {snr} | STABLE/DEGRADING/CRITICAL | ↑↓→ | {action} |
| macro | {snr} | STABLE/DEGRADING/CRITICAL | ↑↓→ | {action} |
| health | {snr} | STABLE/DEGRADING/CRITICAL | ↑↓→ | {action} |
| regulatory | {snr} | STABLE/DEGRADING/CRITICAL | ↑↓→ | {action} |
| tech | {snr} | STABLE/DEGRADING/CRITICAL | ↑↓→ | {action} |

**SNR Thresholds**:
- **STABLE** (SNR ≥ 1.0): Predictions reliable, normal weighting
- **DEGRADING** (SNR 0.5-1.0): Predictions less reliable, consider reduced weight
- **CRITICAL** (SNR < 0.5): High noise, significant impact reduction recommended

**Formula**: `SNR = Mean(actual_impact) / StdDev(prediction_error)` over rolling 20 events per category.

### Next Observation Points
- **24-48 hrs:** {short_term_watch}
- **Week 1:** {week1_watch}
- **Week 2:** {week2_watch}

---

**Data Sources:** Postgres attention_daily ({tables_queried} tables queried), Historical market_returns aligned
**Backtest Validation:** {backtest_status}
```

### Failure Output Template

```markdown
# News Impact Analysis Failed

## Error
Code: {NEWS_ERR_XXX}
Phase: P{N} - {phase_name}

## Issue
{error_description}

## Details
{specific_details}

## Recovery Options
1. {option_1}
2. {option_2}

## Partial Results (if available)
{partial_data}
```

---

## Impact Calculation Reference

### Formula
```
impact_score = (baseline_impact x regime_multiplier x fragility_amplification x confidence_scaling) 
              + (escalation_adjustment x escalation_fatigue_factor)
              + contagion_premium

Where:
  baseline_impact = historical_analog_impact x (today_severity / analog_severity)
  regime_multiplier = f(risk_sentiment, debt_cycle, policy_bias)
    - risk_on (>=70): 0.7x (bad news absorbed better)
    - neutral (30-70): 1.0x (baseline)
    - risk_off (<=30): 1.5-2.0x (bad news hits harder)
  fragility_amplification = 1 + 0.5 x (amplification_factor - 1)
  confidence_scaling = min(1.3, confidence / 0.75)
    - confidence 0.50 (floor): 0.67x impact (skeptical)
    - confidence 0.75 (reference): 1.00x impact (baseline)
    - confidence 0.95: 1.27x impact (high conviction)
  escalation_adjustment = {
    new_event: 0% (baseline only)
    escalating: +30-50% (momentum effect)
    de-escalating: -20-40% (relief rally pattern)
  }
  escalation_fatigue_factor = max(0.7, 1.0 - 0.1 × consecutive_false_escalations)
    - 0 false escalations: 1.00x (full escalation weight)
    - 2 false escalations: 0.80x (20% reduction)
    - 3+ false escalations: 0.70x (floor - maximum skepticism)
    
    A "false escalation" is when an event was classified as "escalating" 
    but actual_impact < predicted_impact × 0.5 (predicted over 2x the actual).
    Resets when a correct escalation prediction occurs (actual ≥ predicted × 0.8).
  contagion_premium = {
    high_correlation + high_fragility: +10-15%
    else: 0%
  }
```

### Scenario Probability Distribution
- **Bear Case:** 25% probability - worst plausible outcome
- **Base Case:** 55% probability - current trajectory continues
- **Bull Case:** 20% probability - favorable resolution

---

## Knowledge Base

### Agent Definitions
- `.claude/agents/investing/news-impact-analyzer/` - Full impact analysis agent with embedded skills
- `.claude/agents/investing/data-validator/` - Collection quality audit agent

### Embedded Skills (internal to news-impact-analyzer)
- `postgres-timescaledb` - Parameterized Postgres queries for attention_daily, market_returns
- `sentiment-analysis` - Risk sentiment composite scoring and interpretation
- `regime-classifier` - Market regime classification and Dalio-style multiplier calculation

### Documentation
- `.claude/docs/command-docs/analyze-news/docs/workflow-phases.md` - Detailed phase documentation
- `.claude/docs/command-docs/analyze-news/docs/postgres-schema.md` - Database schema reference
- `.claude/docs/command-docs/analyze-news/docs/regime-classification.md` - Regime rules
- `.claude/docs/command-docs/analyze-news/docs/impact-formula.md` - Calculation details

### Schemas
- `.claude/docs/command-docs/analyze-news/schemas/analyze-news.schema.json` - Input/output schema
- `.claude/docs/command-docs/analyze-news/schemas/impact-prediction.schema.json` - Prediction format

### Examples
- `.claude/docs/command-docs/analyze-news/examples/geopolitical-example.md`
- `.claude/docs/command-docs/analyze-news/examples/macro-example.md`
- `.claude/docs/command-docs/analyze-news/examples/multi-event-example.md`

---

## Integration

**Upstream**: 
- Daily risk collection pipeline (populates attention_daily table)
- SPEC-14 early warning risk framework (data structure)

**Downstream**:
- Trading decision support
- Risk dashboard
- Alert generation

**Trigger Keywords**: analyze news, news impact, risk analysis, daily analysis, trading signals

**Execution Schedule**: Recommended daily at 9:45 AM ET (15 min after market open)
- Analyzes news collected 6:00-9:30 AM ET
- Compares to historical patterns
- Outputs trading signals + data quality alerts

---

## Examples

### Example A: Full Analysis for Today
```
User: /analyze-news

P0: Parse args -> date=today, category=all, severity=50
P1: Task(news-impact-analyzer) -> 6 events, 15 historical matches, regime=risk_off (28/100), 
    multiplier=1.7x, impact predictions generated
P2: Task(data-validator) -> data quality = 85/100 (missing regulatory coverage)
P3: Format and present report
```

### Example B: Filtered Analysis
```
User: /analyze-news 2026-01-04 geopolitical 65

P0: Parse args -> date=2026-01-04, category=geopolitical, severity=65
P1: Task(news-impact-analyzer) -> 2 events, 8 historical matches (Taiwan tensions 2022, etc.),
    regime=neutral (45/100), multiplier=1.0x, focused impact predictions
P2: Task(data-validator) -> data quality = 90/100
P3: Format and present report
```

---

**Version**: 2.0
**Dependencies**: news-impact-analyzer, data-validator
