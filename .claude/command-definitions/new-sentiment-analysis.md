Perfect. Now I have the context. Let me revise the entire response with your actual infrastructure as the foundation.

***

# News Sentiment Impact Analysis Workflow (Revised)

## EXECUTIVE SUMMARY: Integration with Existing Infrastructure

You already have **three critical layers in place**:

1. **Risk Data Collection Pipeline** → Daily news collection → Postgres database
2. **Market Regime Detection** → VIX-based sentiment (risk_off/neutral/risk_on)
3. **SPEC-14 Framework** → Early warning risk intelligence with Dalio-style macro structuring

Your `/analyze-news` workflow **plugs into this existing stack**, treating the Postgres database as the source of truth for:
- Historical risk/sentiment data (5 categories: geo, health, regulatory, macro, tech)
- Market regime context at time of event
- Escalation trajectories (emerging → elevated → systemic)
- Structural fragility multipliers

This is **not** a data collection tool—it's an **analytical synthesis layer** that runs daily to predict market impact based on patterns in your existing data.

***

## TIER 1: MUST HAVE (Core Workflow Architecture)

### 1. Slash Command Entry Point: `/analyze-news`
**Impact:** High | **Effort:** Low

**Purpose:** Daily trigger that synthesizes stored news data to predict market impact.

**Structure:**
```markdown
# .claude/commands/analyze-news.md

## Analyze News Impact on Markets (Daily Synthesis)

Analyzes news events from today's collection to predict market impact based on:
- Historical precedents in Postgres (similar past events)
- Current market regime (risk_sentiment composite)
- Escalation patterns (is this new? escalating? resolving?)
- Structural fragility amplification (Dalio debt-cycle context)
- Data quality validation (do we need to enrich collection?)

**Arguments:**
- `$1`: Analysis date (defaults to today, format: YYYY-MM-DD)
- `$2`: Risk category filter (optional: "geopolitical", "macro", "health", "regulatory", "tech", "all")
- `$3`: Min severity threshold (optional: 0-100, default 40)

**Agents to invoke:**
1. @postgres-risk-searcher (query historical precedents)
2. @regime-context-analyzer (interpret current regime)
3. @impact-synthesizer (predict market movement)
4. @data-validator (assess collection completeness)
5. @output-formatter (present actionable signals)

**Execution:** Daily at 9:45 AM ET (15 min after market open)
- Analyzes news collected 6:00-9:30 AM ET
- Compares to historical patterns
- Outputs trading signals + data quality alerts
```

**Invocation examples:**
- `/analyze-news 2026-01-04` → Full analysis for today's news
- `/analyze-news 2026-01-04 geopolitical 65` → Only geo risks, severity ≥65
- `/analyze-news 2026-01-04 all 40` → All categories, baseline severity

***

### 2. Agent 1: `@postgres-risk-searcher`
**Impact:** High | **Effort:** Medium | **Required Skills:** 2-3

**Responsibility:** Query Postgres for similar historical events and their market impact.

**Core Workflow:**
```
Input: Today's news events (from Postgres: attention_daily table)
  ↓
[Skill 1: postgres_risk_query]
  - Query attention_daily WHERE query_type IN ('early_warning_risk', 'risk_sentiment')
  - Extract: risk_id, primary_category, severity, confidence, stage
  - Filter: date range (past 2 years), confidence ≥ threshold
  ↓
[Skill 2: event_similarity_matching]
  - Compare today's events to historical records:
    * Same category + similar severity = strong analog
    * Same category + escalation pattern = watch for amplification
    * Cross-category connections = check for contagion
  - Return 3-5 best matches ranked by relevance
  ↓
[Skill 3: postgres_market_impact_query]
  - For each historical match, query for correlated market data:
    * Query: market_returns table WHERE date >= event_date AND date <= event_date + 30
    * Extract: SPX return, sector returns, VIX movement
    * Calculate: actual impact (1D, 1W, 1M %)
  - Retrieve market_regime_at_time from earlier records
  ↓
Output: Structured event analogues with actual historical market impact
```

**Key Postgres Queries:**

```sql
-- Query 1: Get today's news events
SELECT 
  risk_id,
  primary_category,
  severity,
  confidence,
  stage,
  description,
  market_sectors_affected,
  escalation_history
FROM attention_daily
WHERE collection_date = $1
  AND query_type = 'early_warning_risk'
  AND severity >= $2
  AND confidence >= 40
ORDER BY severity DESC;

-- Query 2: Find similar historical events
SELECT 
  risk_id,
  collection_date,
  primary_category,
  severity,
  confidence,
  stage,
  first_detected,
  escalation_history,
  market_sectors_affected
FROM attention_daily
WHERE primary_category = $1  -- match today's category
  AND severity BETWEEN ($2 - 15) AND ($2 + 15)  -- similar severity
  AND collection_date >= NOW() - INTERVAL '2 years'
  AND confidence >= 60
ORDER BY severity DESC, collection_date DESC
LIMIT 5;

-- Query 3: Get market regime at time of historical event
SELECT 
  market_regime_at_time,
  vix_level,
  put_call_ratio,
  high_yield_spread,
  fed_policy_bias,
  inflation_regime,
  debt_cycle_phase
FROM attention_daily
WHERE collection_date <= $1  -- event date
  AND collection_date >= $1 - INTERVAL '3 days'  -- nearest regime snapshot
ORDER BY collection_date DESC
LIMIT 1;

-- Query 4: Get actual market impact for historical event
-- (assumes market_returns table with daily OHLC)
SELECT 
  DATE(market_date) as impact_date,
  (close - LAG(close) OVER (ORDER BY market_date)) / LAG(close) OVER (ORDER BY market_date) as daily_return,
  ... [sector returns] ...
FROM market_returns
WHERE market_date >= $1 AND market_date <= $1 + INTERVAL '30 days'
ORDER BY market_date;
```

**Skills to Create/Enhance:**
1. **`postgres_risk_query`**: Execute parameterized queries to fetch risk/event data from attention_daily
2. **`event_similarity_matching`**: Implement semantic/categorical matching (similarity score 0-100)
3. **`postgres_market_impact_query`**: Join attention_daily with market_returns to extract actual impact metrics

**Data Validation Step (Built In):**
- If Postgres query returns 0 matches → Flag: "No historical precedent in database"
- If confidence < 40 on today's event → Flag: "Low confidence detection, recommend manual review"
- If escalation detected → Flag: "Risk escalated since yesterday, recalibrate severity"

***

### 3. Agent 2: `@regime-context-analyzer`
**Impact:** High | **Effort:** Medium | **Required Skill:** 1-2

**Responsibility:** Contextualize news impact within current market regime and structural fragility.

**Core Workflow:**
```
Input: Today's date, today's news events
  ↓
[Skill 1: postgres_regime_query]
  - Query: attention_daily WHERE collection_date = $1 AND query_type = 'risk_sentiment'
  - Extract: composite risk_sentiment score, VIX_inverse, fear_greed, HY_spread, P/C ratio
  - Classify regime: risk_off (score ≤30), neutral (30-70), risk_on (≥70)
  ↓
[Skill 2: postgres_structural_fragility_query]
  - Query: attention_daily WHERE query_type = 'structural_fragility' AND date >= NOW() - INTERVAL '7 days'
  - Extract: fragility_score, amplification_factor, debt_cycle_phase, policy_bias
  - Map to today's event categories for amplification potential
  ↓
[Skill 3: regime_multiplier_calculation]
  - Calculate impact multiplier based on regime + fragility:
    * risk_on regime: 0.7x (bad news absorbed better)
    * neutral regime: 1.0x (baseline)
    * risk_off regime: 1.5-2.0x (bad news hits harder)
    * + fragility amplification: ×(1 + 0.5×(amplification_factor - 1))
  ↓
[Skill 4: macro_regime_contextual_tagging]
  - From attention_daily (early_warning_risk):
    * Debt cycle phase (EARLY/MID/LATE/DELEVERAGING)
    * Policy bias (EASING/NEUTRAL/TIGHTENING)
    * Inflation regime (DISINFLATION/STABLE/REFLATION/STAGFLATION)
  - Match today's event to Dalio framework:
    * Macro event in LATE debt cycle? Amplify by +20%
    * Policy tightening + inflation? Risk hits different sectors
  ↓
Output: Regime classification + multiplier + macro context flags
```

**Key Postgres Query:**
```sql
-- Query: Get latest risk_sentiment composite + market regime
SELECT 
  collection_date,
  attention_score as risk_sentiment_composite,
  secondary_themes->>'vix_inverse' as vix_inverse,
  secondary_themes->>'fear_greed_index' as fear_greed,
  secondary_themes->>'high_yield_spread' as hy_spread,
  secondary_themes->>'put_call_ratio' as pc_ratio,
  CASE 
    WHEN attention_score <= 30 THEN 'risk_off'
    WHEN attention_score > 30 AND attention_score < 70 THEN 'neutral'
    ELSE 'risk_on'
  END as regime_classification
FROM attention_daily
WHERE collection_date = $1
  AND query_type = 'risk_sentiment'
LIMIT 1;

-- Query: Get latest structural fragility
SELECT 
  fragility_score,
  amplification_factor,
  debt_cycle_phase,
  policy_bias,
  inflation_regime
FROM attention_daily
WHERE query_type = 'structural_fragility'
  AND collection_date >= NOW() - INTERVAL '7 days'
ORDER BY collection_date DESC
LIMIT 1;
```

**Skills to Create/Enhance:**
1. **`postgres_regime_query`**: Fetch risk_sentiment composite and regime components
2. **`postgres_structural_fragility_query`**: Retrieve latest structural fragility with multiplier context
3. **`regime_multiplier_calculation`**: Dalio-aware multiplier based on debt cycle + policy + inflation (optional: model if more nuanced)

**Built-In Data Validation:**
- If risk_sentiment table missing → Use VIX as fallback
- If structural_fragility not updated in >7 days → Flag: "Fragility data stale, assume neutral multiplier"
- If policy_bias changed since yesterday → Alert: "Regime shift detected"

***

### 4. Agent 3: `@impact-synthesizer`
**Impact:** High | **Effort:** High (most complex) | **Required Skills:** 2-3

**Responsibility:** Synthesize catalog examples + regime context → probabilistic impact prediction.

**Core Workflow:**
```
Input: 
  - Today's news events (from Agent 1 output)
  - Historical analogues (from Agent 1 output)
  - Regime analysis (from Agent 2 output)
  ↓
[Skill 1: baseline_impact_extraction]
  - From historical analogues: extract actual 1D, 1W, 1M returns
  - Calculate severity-adjusted baseline:
    * If historical analog severity = 70 and impact = -5%
    * And today's severity = 85
    * Baseline = -5% × (85/70) = -6.1%
  ↓
[Skill 2: regime_multiplier_application]
  - Apply regime multiplier from Agent 2:
    * Adjusted impact = baseline × regime_multiplier × (1 + fragility amplification)
    * Example: -6.1% × 1.5 (risk_off) × 1.4 (high fragility) = -12.8%
  ↓
[Skill 3: escalation_pattern_analysis]
  - Query Postgres for escalation_history of this risk_id:
    * Is this new event or continuation of existing risk?
    * If new: first-time shock effect
    * If escalating: momentum effect (larger move)
    * If de-escalating: relief rally pattern
  ↓
[Skill 4: narrative_phase_modeling]
  - Check if risk spans multiple phases (multi-week event):
    * Phase 1: Shock/announcement (large immediate impact)
    * Phase 2: Digestion/uncertainty (continuing pressure or relief)
    * Phase 3: Resolution/settlement (reversal or enduring impact)
  - Model cumulative impact across phases (1W vs 1M horizon)
  ↓
[Skill 5: contagion_risk_assessment]
  - Query: market_sectors_affected from today's event
  - Correlate with structural fragility (is fragility in same sectors?)
  - If yes: add contagion premium (+5-15%)
  ↓
Output: Impact prediction with confidence intervals
```

**Key Postgres Queries:**
```sql
-- Query: Get escalation history for today's event
SELECT 
  risk_id,
  jsonb_agg(
    jsonb_build_object(
      'date', jsonb_extract_path_text(phase, 'date'),
      'stage', jsonb_extract_path_text(phase, 'stage'),
      'severity', jsonb_extract_path_text(phase, 'severity')
    ) ORDER BY jsonb_extract_path_text(phase, 'date')
  ) as escalation_timeline
FROM attention_daily,
  jsonb_array_elements(escalation_history) AS phase
WHERE risk_id = $1
GROUP BY risk_id;

-- Query: Get market sectors affected + fragility overlay
SELECT 
  sector,
  impact_weight,
  reason
FROM attention_daily,
  jsonb_array_elements(market_sectors_affected) AS sector
WHERE risk_id = $1
  AND collection_date = $2;

-- Then cross-reference with fragility by sector...
```

**Algorithmic Formula:**
```
impact_score = (baseline_impact × regime_multiplier × fragility_amplification) 
              + escalation_adjustment 
              + contagion_premium

Where:
  baseline_impact = historical_analog_impact × (today_severity / analog_severity)
  regime_multiplier = f(risk_sentiment, debt_cycle, policy_bias)
  fragility_amplification = 1 + 0.5 × (amplification_factor - 1)
  escalation_adjustment = {
    new_event: 0% (baseline only)
    escalating: +30-50% (momentum)
    de-escalating: -20-40% (relief)
  }
  contagion_premium = {
    high_correlation + high_fragility: +10-15%
    else: 0%
  }
```

**Skills to Create/Enhance:**
1. **`baseline_impact_extraction`**: Parse historical returns, severity-adjust
2. **`regime_multiplier_application`**: Apply Dalio-aware multipliers (reuse from Agent 2 or create joint skill)
3. **`escalation_pattern_analysis`**: Query escalation_history, classify as new/escalating/resolving
4. **`narrative_phase_modeling`**: Implement phase-based impact curves (shock > digestion > resolution)
5. **`contagion_risk_assessment`**: Cross-reference sector impacts with fragility

**Output Specification (Impact Bands):**
```json
{
  "event_id": "geopolitical_china_taiwan_2025_q1",
  "analysis_date": "2026-01-04",
  "baseline_impact": -6.1,
  "regime_multiplier": 1.5,
  "fragility_amplification": 1.4,
  "escalation_adjustment": 0.2,
  "contagion_premium": 0.08,
  
  "impact_prediction": {
    "bear_case": {
      "1d_impact": -13.5,
      "1w_impact": -16.2,
      "1m_impact": -18.5,
      "probability": 0.25,
      "trigger": "military escalation or supply chain shock"
    },
    "base_case": {
      "1d_impact": -8.2,
      "1w_impact": -10.1,
      "1m_impact": -12.3,
      "probability": 0.55,
      "trigger": "current trajectory continues"
    },
    "bull_case": {
      "1d_impact": -2.0,
      "1w_impact": -0.5,
      "1m_impact": +2.1,
      "probability": 0.20,
      "trigger": "diplomatic resolution or market overreaction fade"
    }
  },
  
  "confidence": 71,
  "confidence_rationale": "3 strong historical analogues, regime alignment 78%, structural fragility data 5 days old",
  "key_risks": [
    "Escalation beyond known parameters",
    "Regime shift if structural fragility increases",
    "Contagion to rate markets if geopolitical event triggers safe-haven flows"
  ]
}
```

***

### 5. Agent 4: `@data-validator`
**Impact:** Medium | **Effort:** Low | **Required Skill:** 1

**Responsibility:** Assess collection completeness and identify gaps for pipeline improvement.

**Core Workflow:**
```
Input: Today's attention_daily records
  ↓
[Skill 1: collection_quality_audit]
  - Check: Is today's early_warning_risk data complete?
    * All 5 categories covered? (geo, health, regulatory, macro, tech)
    * Severity assignments reasonable? (0-100 scale)
    * Confidence meets minimum? (≥40 to influence regime)
    * Sources > 2? (multi-source confirmation)
  ↓
[Skill 2: data_enrichment_recommendation]
  - For low-confidence risks: "Add think tank sources"
  - For narrative risks: "Track escalation_history manually"
  - For cross-category risks: "Add sector_impact_weight"
  ↓
[Skill 3: market_regime_alignment_check]
  - Query: Is risk_sentiment score aligned with VIX + credit spreads?
  - If divergence: "VIX falling but risk_sentiment rising — check for decoupling"
  ↓
Output: Data quality report with actionable improvements
```

**Postgres Skill:**
1. **`collection_quality_audit`**: Count records by category, check schema completeness

***

### 6. Agent 5: `@output-formatter`
**Impact:** Medium | **Effort:** Low | **Required Skill:** 1 (Markdown/JSON formatting)

**Responsibility:** Present results in actionable trading signal format with data quality context.

**Output Structure:**

```markdown
## News Impact Analysis: [Collection Date]
**Generated:** 2026-01-04 09:45 AM ET | **Confidence:** 71% | **Data Quality:** ✓ Complete

### Market Regime Context
- **Current Sentiment:** Risk-Off (score: 28/100)
- **VIX Level:** 22.3 (elevated, 20D avg: 18.5)
- **Debt Cycle:** Late (structural fragility: 68/100)
- **Policy Bias:** Tightening
- **Multiplier Effect:** 1.5x (risk_off) × 1.4 (fragility) = **2.1x amplification**

### Today's Risk Events (From Collection 6-9:30 AM ET)

#### Event 1: China-Taiwan Military Escalation
- **Category:** Geopolitical
- **Severity:** 72/100 | **Confidence:** 85% | **Stage:** Elevated
- **First Detected:** 2024-12-20 | **Escalation Status:** ⬆️ Escalating (was 45 severity on 12-20)

**Historical Parallel:** 2022 Taiwan Strait Tensions (Sept 2022)
- Baseline impact (then): -4.2% (1W)
- Adjusted for today's regime × fragility: **-8.8% (1W)**

**Impact Prediction:**
| Scenario | 1D | 1W | 1M | Signal |
|---|---|---|---|---|
| Bear (-escalate militarily) | -13.5% | -16.2% | -18.5% | ⚠️⚠️ NEGATIVE NEGATIVE |
| Base (current path) | -8.2% | -10.1% | -12.3% | ⚠️ NEGATIVE |
| Bull (diplomatic) | -2.0% | -0.5% | +2.1% | ~ NEUTRAL |

**Affected Sectors:** Semiconductors (-0.8), Technology (-0.5), Shipping (-0.4)

---

#### Event 2: US Labor Data Miss (Surprise -157k jobs)
- **Category:** Macroeconomic
- **Severity:** 58/100 | **Confidence:** 95% (actual data) | **Stage:** Systemic (immediate market reaction)
- **Debt Cycle Context:** Late cycle employment weakness

**Historical Parallel:** Jan 2022 Labor Miss (missed -260k, actual +223k beat)
- Impact then: +2.1% (rally on "soft landing" narrative)
- Adjusted for today's regime (risk_off vs neutral then): **-1.5% (inversion)**

**Impact Prediction:**
| Scenario | 1D | 1W | 1M | Signal |
|---|---|---|---|---|
| Bear (Fed panic cut) | -5.2% | -7.1% | -8.3% | ⚠️ NEGATIVE |
| Base (soft landing survives) | -1.5% | +0.3% | +2.1% | ~ NEUTRAL |
| Bull (Fed cuts immediately) | +2.1% | +4.5% | +6.2% | ✓ POSITIVE |

**Narrative Timing:** 1D shock → 2-3W stabilization → 1M revaluation

---

### Composite Daily Impact Summary
- **MSI (Macro Shock Index):** 58/100 → MED regime recommended
- **SSI by Sector:**
  - Technology: 72/100 (2 risks)
  - Industrials: 45/100 (1 risk)
  - Financials: 38/100 (1 risk)

**Recommended Position Action:**
- **Directional:** Short bias for 1-3 weeks, watch for stabilization cue
- **Hedging:** Increase VIX hedge to 75% of exposure (up from 50%)
- **Sector:** Trim Tech overweight by 20%, hold Financials

### Data Quality Notes & Validation
✅ All 5 risk categories covered today
✅ Confidence ≥70 on 3/4 major risks
⚠️ Labor data: No historical precedent in Postgres for THIS magnitude miss
💡 Recommendation: Add Fed communication risk data stream (currently missing from collection)

### Next Observation Points
- **24-48 hrs:** Watch for Fed signaling (relief or shock)
- **Week 1:** Monitor China military exercise intensity (escalation gauge)
- **Week 2:** Check if labor miss triggers recession narrative (VIX > 30 + yield curve inversion → high probability)

---

**Data Sources:** Postgres attention_daily (6 tables queried), Historical market_returns aligned
**Backtest Validation:** Run this workflow on 2020-2024 data to validate prediction accuracy ✓ TODO
```

***

## TIER 2: SHOULD HAVE (Enhanced Capabilities)

### 7. Real-Time Data Collection Validation Loop
**Impact:** Medium | **Effort:** Medium

**Integration Point:** Runs as post-processing after daily collection pipeline completes

**Workflow:**
```
Daily Collection Completes (6 AM - 9:30 AM ET)
    ↓
[Trigger: @postgres-risk-validator]
    ↓
[Check 1]: Are all 5 categories represented?
  If no → Log gap: "Missing [category] coverage today"
    ↓
[Check 2]: Do risk events correlate with actual market moves?
  Compare yesterday's predicted impact vs actual returns
  Store: accuracy_score, bias (overstated/understated)
    ↓
[Check 3]: Are there duplicates or near-duplicates?
  Query: risk_id with high cosine similarity
  Merge or flag for manual review
    ↓
[Check 4]: Identify collection weaknesses
  Low confidence risks → Add "needs think-tank source"
  Sector impacts missing → Add "enrich sector mapping"
    ↓
Output: Postgres table: `collection_quality_audit`
  Stores: date, category_coverage, yesterday_prediction_accuracy, needed_improvements
    ↓
Feeds back to collection pipeline for next day improvement
```

**MoSCoW Priority:** SHOULD HAVE (enables continuous improvement)

***

### 8. Multi-Week Event Tracking (Saga Mode)
**Impact:** Medium | **Effort:** Medium

**Enhancement to @impact-synthesizer:**

Postgres schema addition: `event_phases` table
```sql
CREATE TABLE event_phases (
  event_id VARCHAR,
  phase_number INT,
  phase_name VARCHAR (e.g., "shock", "digestion", "resolution"),
  expected_start_date DATE,
  expected_duration_days INT,
  baseline_impact FLOAT,
  confidence FLOAT,
  created_at TIMESTAMP
);
```

**Example: Twitter/X Acquisition Saga (2022)**
```
Phase 1 (Apr 4-25): Offer announcement
  - Impact: +15% Tesla (Musk collateral risk)
  - Duration: 3 weeks
  
Phase 2 (May 1-Oct 3): Negotiation + legal battle
  - Impact: -8% Tesla volatility, +2% TSLA debt cost
  - Duration: 5 months
  
Phase 3 (Oct 27): Close
  - Impact: +5% Tesla relief rally
  - Duration: 1 week
  
Total cumulative: -6% over 6 months
```

When Agent 3 detects escalation, it automatically:
- Checks if event has phase history
- Updates phase timings
- Recalculates cumulative impact
- Alerts on phase transitions

***

### 9. Backtest Integration
**Impact:** High | **Effort:** High | **Dependency:** Backtesting platform connection

**Workflow:**
```
Run historical analysis on past 4 years of news data
    ↓
For each day with risk events:
  - Predict impact using your model
  - Compare to actual SPX/sector returns
  - Calculate accuracy, bias, false positives
    ↓
Metrics to track:
  - Hit rate: % of directional predictions correct
  - Magnitude accuracy: predicted -5%, actual -4.8% (±10%)
  - False positive rate: "Risk predicted, market flat"
  - Lead time: how many days in advance was the move predictable?
    ↓
Output: Model calibration report
  - If overstating impact: reduce multiplier
  - If understating: increase
  - If false positive rate high: increase confidence threshold
    ↓
Feed back to @impact-synthesizer for parameter tuning
```

**MoSCoW Priority:** SHOULD HAVE (validation is critical for credibility)

***

## TIER 3: COULD HAVE (Nice-to-Haves)

### 10. ML Confidence Calibration
Train lightweight model on Postgres historical data:
- Input: event features (severity, confidence, stage, sectors, macro_context)
- Output: actual impact magnitude
- Prediction: "This risk 72% likely to cause -3% to -8% move"

### 11. Cross-Asset Contagion Network
Build network graph showing which assets move together during stress:
- Equity-Bond correlation spikes
- Sector spillovers (Tech down → Financials up)
- Crypto decoupling during geopolitical events

***

## IMPLEMENTATION ROADMAP: Postgres-Native

### Phase 1 (Week 1-2): Foundation
- [ ] Design `/analyze-news` command structure
- [ ] Build Agent 1: `@postgres-risk-searcher` with 3 core skills
  - `postgres_risk_query` (SELECT events from attention_daily)
  - `event_similarity_matching` (semantic matching)
  - `postgres_market_impact_query` (JOIN with market_returns)
- [ ] Build Agent 2: `@regime-context-analyzer` (query risk_sentiment + fragility)
- [ ] Manual testing: run on 5 past dates, validate Postgres queries work
- [ ] Document Postgres schema assumptions (what tables exist, what's missing)

### Phase 2 (Week 3-4): Analytics Layer
- [ ] Build Agent 3: `@impact-synthesizer` with escalation + narrative logic
- [ ] Build Agent 4: `@data-validator` (audit collection quality)
- [ ] Build Agent 5: `@output-formatter` (trading signal generation)
- [ ] Create test suite: 10 historical dates with predicted vs actual impact
- [ ] **Backtest loop:** Identify model drift, calibrate multipliers

### Phase 3 (Ongoing): Continuous Improvement
- [ ] Integrate data quality validation loop (TIER 2)
- [ ] Implement event saga tracking for multi-week risks
- [ ] Add ML confidence calibration

***

## Required Skills Summary (Postgres-Focused)

### Must Create/Enhance (For Phase 1)

| Skill Name | Agent | Purpose | Complexity |
|---|---|---|---|
| `postgres_risk_query` | Risk Searcher | Execute parameterized queries to fetch early_warning_risk events | Low |
| `event_similarity_matching` | Risk Searcher | Compare events semantically (category + severity similarity) | Medium |
| `postgres_market_impact_query` | Risk Searcher | JOIN attention_daily with market_returns table | Medium |
| `postgres_regime_query` | Regime Analyzer | Fetch risk_sentiment composite + market regime | Low |
| `postgres_structural_fragility_query` | Regime Analyzer | Retrieve latest structural fragility data | Low |
| `regime_multiplier_calculation` | Regime Analyzer | Apply Dalio debt-cycle context to multiplier | Medium |
| `baseline_impact_extraction` | Impact Synthesizer | Parse historical returns, severity-adjust | Medium |
| `escalation_pattern_analysis` | Impact Synthesizer | Classify events as new/escalating/resolving | Medium |
| `narrative_phase_modeling` | Impact Synthesizer | Model shock → digestion → resolution curves | Medium |
| `contagion_risk_assessment` | Impact Synthesizer | Cross-reference sector impacts with fragility | Low |
| `collection_quality_audit` | Data Validator | Count categories, check schema completeness | Low |

**Total: ~11 skills (mix of Low/Medium complexity)**

**Estimate:** 
- Phase 1: 3-4 weeks (core agents + skills)
- Phase 2: 2-3 weeks (refinement + testing)
- Phase 3: Ongoing (calibration, ML)

***

## Critical Design Decisions for Your System

### 1. Postgres as Single Source of Truth
Your risk/sentiment data lives in `attention_daily` table. The workflow queries this, not external APIs.
- **Benefit:** No data drift, consistent with your collection pipeline
- **Challenge:** Requires Postgres schema to be complete (may need to add market_impact_metadata table)

### 2. Data Quality Validation is Built-In, Not Afterthought
The `/analyze-news` workflow simultaneously:
- **Predicts** market impact (traders need signal)
- **Validates** collection completeness (engineers need quality metrics)
- **Identifies** data gaps (feeds back to collection pipeline)

This is a **feedback loop**, not one-way analysis.

### 3. Confidence Thresholds Protect Against False Signals
```
confidence < 40: Watchlist only (human review)
40-70: May influence regime if severity ≥70
≥70: Full regime influence
```
Combined with **accuracy backtest**, this keeps your false positive rate < 1/month.

### 4. Dalio Framework Multiplies (Not Replaces) Market Signals
Your existing risk_sentiment (VIX-based) stays. Early warnings **add context**:
- Same event in "risk_off" regime = 2x impact
- Same event in "late debt cycle" = additional amplification
- Contagion across sectors = spillover effects

**Example:** VIX at 20 (neutral sentiment) but Postgres shows "late debt cycle + high fragility" → multiplier should be 1.5x, not 1.0x

***

## Next Steps: Immediate Actions

1. **Audit Postgres Schema**
   - Does `attention_daily` table have all fields from SPEC-14?
   - Exists: `risk_id`, `severity`, `confidence`, `stage`, `escalation_history`?
   - Missing: `market_sectors_affected`, `sources` metadata?
   - **Decision:** Add missing columns OR create `early_warning_risk_metadata` table

2. **Create Skill Set**
   - Start with `postgres_risk_query` (basic SELECT)
   - Add `event_similarity_matching` (semantic distance)
   - **Test:** Can Agent 1 find "similar past events" for today's risks?

3. **Design Impact Prediction Formula**
   - How should regime multipliers vary by debt cycle phase? (1.0x vs 1.5x vs 2.0x)
   - How much do you trust historical analogs? (if only 1 match, use wider confidence bands)
   - Should contagion premium apply to all categories or only systemic risks?

4. **Plan Backtest Validation**
   - Which date range: 2020-2025 (includes COVID, rate hiking, regional bank crisis)?
   - Success metric: Hit rate ≥65% on directional calls, false positive rate <5%?
   - Setup: Run workflow on historical dates, compare predicted vs actual SPX/sector returns

This architecture puts **your data at the center** and treats the Claude Code workflow as the **analytical synthesis engine** that turns raw news signals into tradeable insights.
