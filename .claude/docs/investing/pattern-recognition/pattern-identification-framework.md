# Pattern Identification Framework: The River, The Rocks, and The Surfers
## A First-Principles Approach to Market Pattern Recognition

**Date:** January 4, 2026  
**Framework:** Water Flow Metaphor + SCAMPER + Varma/Dalio Principles

---

## The Metaphor: Understanding Market Patterns as River Dynamics

### The River = The Market
- **Water flow** = capital, liquidity, order flow
- **Current strength** = volatility, momentum
- **River width** = market breadth, participation
- **Water temperature/clarity** = regime state (calm vs turbulent)

### The Rocks = Market Patterns
- **Visible rocks** = known patterns (momentum, mean reversion, seasonality)
- **Rock formation** = structural forces (regulation, institutional behavior, macro cycles)
- **Rock erosion** = alpha decay as capital crowds the pattern
- **Rock size** = pattern signal strength, statistical significance
- **Rock stability** = pattern persistence across regimes

### The Surfers = Traders
- **Your weight** = capital size, position size
- **Surfing skill** = execution quality, timing
- **Number of surfers** = crowding, competition
- **Surfboard choice** = strategy selection, timeframe

### The Key Insight
**Patterns exist because of underlying structural forces (rocks), not just statistical noise. But patterns collapse when too much capital tries to exploit them (rock erodes under weight) OR when the regime changes (river flow shifts, rock becomes submerged or exposed).**

---

## First Principles of Pattern Identification

### Principle 1: Patterns Are Byproducts of Constraints

**Why patterns exist at all:**
- Markets are NOT pure random walks
- Structural constraints create predictable behaviors:
  - **Institutional constraints:** 13F reporting deadlines → quarter-end window dressing
  - **Regulatory constraints:** Tax calendar → loss harvesting in December
  - **Behavioral constraints:** Herding, recency bias → momentum and reversals
  - **Liquidity constraints:** Institutions avoid illiquid stocks → small-cap anomalies persist

**The rock formation question:** "What structural force creates THIS pattern?"

**Examples:**
- Momentum: Behavioral underreaction + institutional trend-following
- Mean reversion: Behavioral overreaction + liquidity provision
- January effect: Tax-loss harvesting + institutional window dressing
- End-of-day ramp: Passive fund tracking + benchmark hugging

**Action:** For every pattern, ask via Perplexity: "What regulatory, institutional, or behavioral constraint creates [pattern]? When was it documented? Has the constraint changed?"

---

### Principle 2: Pattern Strength = Structural Force Strength

**Not all rocks are equal:**
- Weak patterns (statistical noise): disappear when tested out-of-sample
- Strong patterns (structural): persist across decades, regimes, markets

**The durability test:**
- Does the pattern exist because of a *persistent constraint* that can't easily change?
- Or because of a *temporary arbitrage* that capital can eliminate?

**Examples:**
- **Persistent:** Tax-loss harvesting (tax code unlikely to change fundamentally)
- **Persistent:** End-of-quarter rebalancing (institutional mandates won't disappear)
- **Temporary:** Post-earnings-announcement drift (mostly arbitraged away by algos)
- **Temporary:** Calendar anomalies discovered in 1980s (mostly disappeared)

**Signal formula:**
```
Pattern_durability = f(
    constraint_permanence,      # Can the structural force be eliminated?
    arbitrage_capacity,         # How much capital can exploit this?
    execution_difficulty        # How hard is it to capture?
)
```

**Action:** Use Perplexity to research: "Is [structural force] likely to persist? Have regulations/institutions changed since pattern was discovered?"

---

### Principle 3: Patterns Have Lifecycles (Birth, Peak, Decay, Death)

**The rock lifecycle:**
1. **Formation (Birth):** Structural force creates exploitable inefficiency
2. **Discovery:** Academic paper or practitioner identifies it
3. **Peak Exploitation:** Smart money quietly exploits (high Sharpe)
4. **Publication:** Becomes public knowledge (factor funds, ETFs)
5. **Crowding:** Capital floods in, Sharpe decays
6. **Erosion (Death):** Pattern becomes noisy or reverses

**Historical examples:**
- **Value premium:** Fama-French 1992 paper → value funds → value underperformed 2010-2020
- **Momentum:** Jegadeesh-Titman 1993 → momentum ETFs → crashes in 2009, 2020
- **Low vol anomaly:** Discovered 1970s → AQR productized → crowded by 2018

**Key insight (Varma):** "Edges decay as capital discovers them." Your job: identify patterns BEFORE publication OR after decay when capital leaves.

**Signal formula:**
```
Pattern_lifecycle_stage = {
    PRE_DISCOVERY: No academic papers, no ETFs, Sharpe >2
    EARLY_ADOPTION: 1-2 papers, no retail products, Sharpe 1.5-2
    MATURE: Multiple papers, factor ETFs exist, Sharpe 0.8-1.2
    CROWDED: Everyone knows it, Sharpe <0.5
    DEAD: Sharpe <0 out-of-sample
}
```

**Action:** For each pattern, use Perplexity: "When was [pattern] first published? Are there ETFs/funds targeting it? What's recent performance?"

---

### Principle 4: Regime Determines Which Rocks Are Surfable

**Same rock, different water flow = different outcome.**

A momentum pattern that works beautifully in:
- LOW vol, ABOVE 200DMA, LOW correlation regime (2017-2019)

Fails catastrophically in:
- HIGH vol, BELOW 200DMA, HIGH correlation regime (March 2020)

**The regime-pattern interaction matrix:**

| Pattern Type | LOW Risk Regime | MED Risk Regime | HIGH Risk Regime |
|--------------|----------------|-----------------|------------------|
| **Momentum** | Excellent (Sharpe 1.5+) | Good (Sharpe 1.0) | Terrible (Sharpe <0, whipsaws) |
| **Mean Reversion** | Weak (small moves) | Good (Sharpe 0.8) | Excellent (Sharpe 1.8+, panic reversals) |
| **Breakouts** | False breakouts common | Mixed | Strong if confirmed |
| **Carry** | Works (low vol = stable) | Risky | Fails (carry crashes) |

**Key insight (Varma + Dalio):**
- Varma: "Classify risk state first, THEN decide which patterns to trade."
- Dalio: "Environment determines what works. There's no universal best strategy."

**Signal formula:**
```
Pattern_regime_suitability = {
    MOMENTUM: (regime == LOW_RISK) AND (trend == UP) AND (correlation < 0.5)
    MEAN_REVERSION: (regime == HIGH_RISK) OR (vol > 75th percentile)
    BREAKOUT: (regime == LOW_RISK) AND (breadth_expanding)
    CARRY: (regime == LOW_RISK) AND (vol < 25th percentile)
}
```

**Action:** Build regime-pattern performance matrix via backtesting. For each pattern, compute Sharpe in LOW/MED/HIGH risk regimes separately.

---

### Principle 5: Pattern Capacity = How Many Can Surf Before Rock Collapses

**The crowding question:** "How much capital can exploit this pattern before alpha decays to zero?"

**Small rocks (low capacity):**
- Small-cap value, illiquid stocks, high-frequency arb
- Capacity: $10M - $500M

**Medium rocks (medium capacity):**
- Sector rotation, factor timing, volatility strategies
- Capacity: $500M - $5B

**Large rocks (high capacity):**
- Momentum across large-caps, trend-following, macro strategies
- Capacity: $5B - $100B+

**Signal formula:**
```
Pattern_capacity = f(
    market_size,           # Total addressable liquidity
    execution_slippage,    # How much does your trade move price?
    current_AUM,           # How much capital already there?
    decay_rate             # How fast does Sharpe decline per $1B AUM?
)

Pattern_available_capacity = Pattern_capacity - current_AUM
```

**Key data (via Perplexity):**
- "How much AUM is in [momentum/value/low-vol] ETFs and factor funds?"
- "What is average daily volume in [small-cap/mid-cap] universe?"
- "Which hedge funds are known to run [strategy type]?"

**Red flag:** If you discover a "pattern" that Renaissance, AQR, Two Sigma would obviously know → it's already crowded or dying.

**Action:** Estimate current crowding by tracking:
1. ETF AUM in that factor
2. 13F filings mentioning that strategy
3. Google Trends + news mentions of that pattern
4. Performance decay over time (rolling 3-year Sharpe)

---

### Principle 6: Upstream Rocks (Future Patterns) Signal via Early Warnings

**You're moving downstream (forward in time). You need to see rocks forming AHEAD, not just react to rocks you're already passing.**

**Categories of "upstream rocks" (future patterns emerging):**

#### 1. Regulatory Changes → New Structural Patterns
- Example: Dodd-Frank 2010 → bank trading restrictions → reduced market-making liquidity → increased short-term vol patterns
- **Signal:** Use your early-warning system (FR-EWR regulatory category)
- **Ask Perplexity:** "What major financial regulations are pending in US/EU/Asia? What market structures will they change?"

#### 2. Technological Shifts → New Arbitrage Opportunities
- Example: HFT adoption 2005-2010 → decimalization arbitrage disappeared but latency arb emerged
- Example: Passive investing 2010-2020 → end-of-day ramps, rebalance arb, closure arb
- **Signal:** Track institutional technology adoption
- **Ask Perplexity:** "What % of trading volume is algorithmic? What new trading technologies are being adopted?"

#### 3. Macro Regime Shifts → Different Patterns Dominate
- Example: 2008-2020 (ZIRP) → growth outperformed value, momentum dominated
- Example: 2022+ (rate normalization) → value comeback, momentum whipsaws
- **Signal:** Use Dalio debt-cycle phase + policy bias from your early-warning spec
- **Ask Perplexity:** "What is current central bank policy trajectory? Are we entering tightening or easing cycle?"

#### 4. Behavioral Shifts → Sentiment-Driven Patterns
- Example: Retail surge 2020-2021 (Robinhood, meme stocks) → new momentum patterns in small-caps
- Example: ESG investing 2015-2020 → ESG premium emerged then faded
- **Signal:** Track Google Trends, news narrative intensity, retail flow proxies
- **Ask Perplexity:** "What investment themes are gaining mainstream retail attention?"

**The "rock ahead" signal framework:**
```
Upstream_pattern_emergence = {
    REGULATORY: (regulatory_risk_elevated) AND (affects_market_structure)
    TECHNOLOGICAL: (adoption_curve_inflection) AND (changes_execution_costs)
    MACRO: (debt_cycle_phase_shift) OR (policy_regime_change)
    BEHAVIORAL: (narrative_intensity >80th pct) AND (retail_participation_surging)
}
```

**Action:** Use your early-warning MSI/SSI system to detect structural shifts BEFORE they materialize in prices. When MSI >60, ask: "Which existing patterns will break? Which new patterns will emerge?"

---

## Practical Pattern Identification Workflow

### Stage 1: Pattern Discovery (Finding Rocks)

**Data sources (all accessible via Perplexity):**
1. **Academic literature:** "What trading anomalies have been documented in past 5 years?"
2. **Practitioner knowledge:** "What strategies do quant funds discuss in latest letters?"
3. **Structural analysis:** "What institutional constraints create predictable behaviors?"
4. **Historical events:** "What market patterns preceded [recession/crisis/rally]?"

**Candidate pattern criteria:**
- [ ] Has a plausible structural explanation (not just data mining)
- [ ] Persists across multiple regimes (not regime-specific)
- [ ] Has multi-year track record (not just recent)
- [ ] Not yet fully productized (no dedicated ETF with >$1B AUM)

**Output:** List of 10-20 candidate patterns with structural rationale

---

### Stage 2: Pattern Structural Analysis (Understanding Rock Formation)

**For each candidate pattern, research via Perplexity:**

1. **When did this pattern form?**
   - "When was [pattern] first documented academically?"
   - "Has the structural force creating it changed since discovery?"

2. **What constraint creates it?**
   - "What behavioral/institutional/regulatory force causes [pattern]?"
   - "Is this force permanent or temporary?"

3. **How crowded is it?**
   - "How much AUM is in funds/ETFs targeting [pattern]?"
   - "What is recent performance vs historical?"

4. **What kills it?**
   - "What regime conditions cause [pattern] to fail?"
   - "What future changes could eliminate the structural force?"

**Output:** Structural risk assessment per pattern

---

### Stage 3: Pattern Regime Testing (Which Rocks Work in Which Water)

**Backtest each pattern separately by regime:**

| Regime | Vol | Trend | Correlation | Credit | Sentiment |
|--------|-----|-------|-------------|--------|-----------|
| **LOW** | <25th pct | Above 200DMA | <0.5 | Tight | Neutral |
| **MED** | 25-75th pct | Mixed | 0.5-0.7 | Normal | Mixed |
| **HIGH** | >75th pct | Below 200DMA | >0.7 | Wide | Extreme |

**For each pattern, compute:**
- Sharpe ratio in LOW/MED/HIGH regimes
- Max drawdown in LOW/MED/HIGH regimes
- Win rate in LOW/MED/HIGH regimes
- Trade count in LOW/MED/HIGH regimes

**Pattern regime suitability:**
```
IF sharpe_LOW > 1.5 × sharpe_HIGH:
    pattern_type = "LOW_RISK_ONLY" (only trade in benign regimes)
    
IF sharpe_HIGH > 1.5 × sharpe_LOW:
    pattern_type = "HIGH_RISK_ONLY" (contrarian, crisis alpha)
    
IF sharpe_LOW ≈ sharpe_MED ≈ sharpe_HIGH:
    pattern_type = "ALL_WEATHER" (rare, valuable)
```

**Output:** Regime-pattern performance matrix

---

### Stage 4: Pattern Capacity Estimation (How Many Surfers?)

**Estimate crowding:**

1. **Direct crowding (via Perplexity):**
   - "How much AUM is in [momentum/value/quality] factor funds?"
   - "Which major quant funds run [strategy type]?"

2. **Indirect crowding:**
   - Google Trends for "[pattern] trading strategy"
   - News mentions of "[pattern] underperformance/crowding"
   - Number of ETFs launched targeting that factor

3. **Performance decay test:**
   - Compute rolling 3-year Sharpe
   - Has it declined >30% from peak? → crowding signal
   - Has it rebounded after drawdown? → capacity still available

**Crowding classification:**
```
IF (factor_ETF_AUM > $10B) OR (Sharpe_recent < 0.5 × Sharpe_historical):
    crowding_level = HIGH
    recommended_action = AVOID or WAIT_FOR_WASHOUT
    
ELIF (factor_ETF_AUM $1B-$10B) AND (Sharpe_recent ≈ 0.7 × Sharpe_historical):
    crowding_level = MEDIUM
    recommended_action = TRADE_SELECTIVELY (only in best regimes)
    
ELSE:
    crowding_level = LOW
    recommended_action = EXPLOIT_FULLY
```

**Output:** Crowding risk score per pattern

---

### Stage 5: Pattern Monitoring (Watching Rock Erosion)

**Ongoing surveillance (weekly/monthly):**

1. **Performance tracking:**
   - Is Sharpe declining month-over-month?
   - Has max drawdown exceeded historical worst?
   - Are win rates declining?

2. **Crowding tracking (via Perplexity):**
   - "Has [factor] ETF AUM increased significantly?"
   - "Are hedge funds discussing [strategy] more frequently?"
   - Google Trends for "[pattern name]"

3. **Structural change tracking:**
   - "Have regulations affecting [pattern] changed?"
   - "Has the constraint creating [pattern] weakened?"

4. **Regime shift tracking:**
   - Has the regime changed to one where pattern historically fails?
   - Use your early-warning MSI: if MSI >60, re-evaluate all patterns

**Pattern health scorecard:**
```
Pattern_health = f(
    sharpe_trend,              # Improving, stable, or declining?
    crowding_trend,            # AUM increasing or decreasing?
    structural_force_intact,   # Yes/No
    regime_suitability         # Currently in favorable regime?
)

IF Pattern_health == DEGRADING:
    action = REDUCE_EXPOSURE or ELIMINATE
    
IF Pattern_health == STABLE:
    action = MAINTAIN
    
IF Pattern_health == IMPROVING:
    action = INCREASE_EXPOSURE (rock re-formed after washout)
```

**Output:** Monthly pattern health report

---

## Advanced Pattern Identification: The 21 SCAMPER Ideas

I generated 21 specific pattern identification approaches using SCAMPER. Here are the top 10 by strategic value:

### Top 10 High-Impact Patterns to Explore

#### 1. **Water Flow Volume Analysis → Pattern Load Capacity** [SUBSTITUTE]
**The insight:** Track how much capital is already exploiting a pattern via 13F filings, ETF flows, hedge fund letters.
**The signal:** Pattern capacity = (historical Sharpe) × (1 - crowding_coefficient)
**Data sources:** 13F filings, ETF creation/redemption, Google Trends, hedge fund letters
**Ask Perplexity:** "How many hedge funds mentioned [momentum/value] in latest quarterly letters?"

---

#### 2. **Dynamic Pattern Lifespan Tracking** [SUBSTITUTE]
**The insight:** Patterns have birth dates (when constraint emerged), peak dates (max Sharpe), decay dates (crowding).
**The signal:** Pattern age since publication. Decay accelerates post-publication.
**Data sources:** Academic publication dates, Google Trends, factor returns by cohort
**Ask Perplexity:** "When was [factor anomaly] first documented? How has performance changed post-publication?"

---

#### 3. **Regime Classification × Pattern Lifespan** [COMBINE]
**The insight:** Same pattern works differently in different regimes. Test separately by LOW/MED/HIGH risk.
**The signal:** Pattern_regime_fit = sharpe_in_regime / sharpe_overall. >1.5 = regime-specific edge.
**Data sources:** 5-factor regime (vol, correlation, credit, sentiment, trend) + pattern returns
**Ask Perplexity:** "Which market patterns historically perform best in [specific regime]?"

---

#### 4. **Early-Warning Risk × Pattern Invalidation** [COMBINE]
**The insight:** Your MSI/SSI system detects "rocks ahead" that will destroy downstream patterns.
**The signal:** Pattern_survival_prob = 1 - (MSI/100 × pattern_vol_sensitivity)
**Data sources:** Early-warning MSI/SSI, historical pattern performance during crises
**Ask Perplexity:** "What macro events historically invalidated [momentum/carry/arb] strategies?"

---

#### 5. **Breadth Divergence × Narrative Shift** [COMBINE]
**The insight:** River narrows (fewer stocks up) while headline looks strong. Rock shifting underwater.
**The signal:** Divergence_score = |index_return - median_stock_return|. >2 stdev = exhaustion.
**Data sources:** Market breadth (% above 200DMA), sector rotation, news sentiment
**Ask Perplexity:** "What % of S&P sectors are declining despite index gains?"

---

#### 6. **Dynamic Stop-Loss by Pattern Confidence** [ADAPT]
**The insight:** Stable rocks (10+ years data) get tight stops (1.5 ATR). New rocks get loose stops (3 ATR).
**The signal:** Stop_distance = base_ATR × (1 + (1 - pattern_confidence))
**Data sources:** Pattern age, consistency (Sharpe by 3-year windows), regime-specific drawdowns
**Ask Perplexity:** "When was [pattern] first documented? How consistent has performance been?"

---

#### 7. **Correlation Regime → Pattern Independence Filter** [ADAPT]
**The insight:** In HIGH correlation (>0.7), only trade patterns with LOW beta to market.
**The signal:** Pattern_allowed = (correlation_to_market < 0.5) OR (regime == LOW_CORR)
**Data sources:** Rolling stock correlation, strategy beta to SPY by regime
**Ask Perplexity:** "Which strategies have low beta to equity markets during crises?"

---

#### 8. **Pattern Entry Timing → Kuzushi Detection** [MODIFY]
**The insight:** Don't surf when everyone's on rock. Wait for them to fall off (pullback), then enter.
**The signal:** Entry = (trend_up) AND (3day_pullback >= 0.5 ATR) AND (volume_spike_down)
**Data sources:** Intraday vol spikes, short-term sentiment flips, volume exhaustion
**Ask Perplexity:** "What are typical retracement depths before trend continuation?"

---

#### 9. **News Narrative Patterns → Sentiment Exhaustion** [PUT_TO_ANOTHER_USE]
**The insight:** When narrative intensity hits 90th percentile + sentiment extreme, pattern about to collapse.
**The signal:** Exhaustion = (mention_count > 90th pct) AND (sentiment > 80th pct)
**Data sources:** Google Trends, news mentions, AAII sentiment, social media
**Ask Perplexity:** "Show me news mention frequency and sentiment for [AI/crypto/theme] over past 12 months."

---

#### 10. **Remove Trades in Neutral Regimes (Shi Absence)** [ELIMINATE]
**The insight:** Don't surf flat water. Wu wei: only trade when regime extremes create clear advantage.
**The signal:** Trade_allowed = (regime_extreme_count >= 2). If <2 factors extreme, stay flat.
**Data sources:** 5-factor regime classification
**Ask Perplexity:** "What are characteristics of low-conviction market environments?"

---

## Implementation: Building Pattern Identification Skills & Agents

### Skills Needed (MoSCoW Priority)

#### MUST Have (Foundation)
1. **Regime Classifier Skill**
   - Input: Market data (price, vol, correlation, credit, sentiment)
   - Output: LOW/MED/HIGH risk regime + confidence
   - Uses: 5-factor model (vol, correlation, credit, sentiment, 200DMA)

2. **Pattern Performance Tracker Skill**
   - Input: Strategy returns, regime history
   - Output: Sharpe by regime, drawdown by regime, trade count by regime
   - Uses: Splits backtest results by regime automatically

3. **Structural Force Research Skill (Perplexity-Powered)**
   - Input: Pattern name (e.g., "momentum")
   - Output: Academic publication date, structural explanation, regulatory dependencies
   - Uses: Perplexity queries + structured parsing

4. **Crowding Monitor Skill (Perplexity-Powered)**
   - Input: Pattern/factor name
   - Output: ETF AUM, hedge fund mentions, Google Trends, performance decay trend
   - Uses: Perplexity queries for 13F filings, ETF data, news mentions

#### SHOULD Have (Enhancement)
5. **Pattern Lifecycle Classifier Skill**
   - Input: Pattern name, publication date, crowding data, recent performance
   - Output: Lifecycle stage (PRE_DISCOVERY / EARLY / MATURE / CROWDED / DEAD)
   - Uses: Combines crowding + performance decay + time-since-publication

6. **Early-Warning Pattern Invalidation Skill**
   - Input: Current patterns being traded, MSI/SSI scores
   - Output: Pattern_survival_probability for each
   - Uses: Maps pattern vol-sensitivity × MSI to predict breakage

7. **Multi-Timeframe Confirmation Skill**
   - Input: Signal on daily timeframe
   - Output: Confirmation score (0-1) based on weekly/monthly alignment
   - Uses: Checks if daily signal confirmed by higher timeframes

#### COULD Have (Advanced)
8. **Narrative Exhaustion Detector Skill (Perplexity-Powered)**
   - Input: Theme/sector name
   - Output: Mention frequency percentile, sentiment score, exhaustion flag
   - Uses: Google Trends + news mentions via Perplexity

9. **Patent/Innovation Tracker Skill (Perplexity-Powered)**
   - Input: Sector name
   - Output: Patent filing trends, R&D spending, innovation momentum score
   - Uses: USPTO data + company filings via Perplexity

10. **Insider Transaction Analyzer Skill (Perplexity-Powered)**
    - Input: Sector or stock ticker
    - Output: Insider buy/sell ratio, unusual activity flags
    - Uses: SEC Form 4 filings via Perplexity

---

### Agents Needed (MoSCoW Priority)

#### MUST Have
1. **pattern-identifier Agent**
   - Role: Discovers candidate patterns via structural analysis
   - Skills: structural-force-research, academic-literature-search
   - Output: List of patterns with structural rationale + initial viability score

2. **regime-pattern-analyst Agent**
   - Role: Tests patterns across regimes, generates performance matrix
   - Skills: regime-classifier, pattern-performance-tracker
   - Output: Sharpe/DD/Win-rate by regime for each pattern

3. **pattern-health-monitor Agent**
   - Role: Tracks ongoing pattern health, detects decay/crowding
   - Skills: crowding-monitor, pattern-performance-tracker, lifecycle-classifier
   - Output: Weekly pattern health scorecard + action recommendations (increase/maintain/reduce)

#### SHOULD Have
4. **upstream-risk-analyst Agent**
   - Role: Detects "rocks ahead" that will invalidate current patterns
   - Skills: early-warning-pattern-invalidation, narrative-exhaustion-detector
   - Output: Pattern survival probabilities given current MSI/SSI

5. **pattern-entry-optimizer Agent**
   - Role: Finds optimal entry timing (kuzushi moments, pullbacks)
   - Skills: multi-timeframe-confirmation, volume-analysis, sentiment-flip-detection
   - Output: Entry score (0-100) for each pattern signal

#### COULD Have
6. **innovation-scout Agent (Perplexity-Powered)**
   - Role: Identifies emerging sectors/themes via patent/R&D trends
   - Skills: patent-tracker, narrative-monitor, institutional-flow-tracker
   - Output: Early-stage sector momentum signals (1-2 years ahead)

---

## Pattern Identification Example: Complete Workflow

### Example: Evaluating "Small-Cap Value" Pattern

#### Stage 1: Discovery
**Query Perplexity:** "What is the structural explanation for small-cap value outperformance?"
**Answer:** Fama-French size + value premiums. Small-cap value = high risk, illiquid, institutionally underowned → requires premium.

#### Stage 2: Structural Analysis
**Query Perplexity:** "When was small-cap value premium documented? What is recent performance?"
**Answer:** 
- Fama-French 1992 paper
- Premium strong 1926-2000 (Sharpe ~0.8)
- Premium weak 2000-2020 (Sharpe ~0.2)
- Recent resurgence 2021-2023 (Sharpe ~1.0)

**Query Perplexity:** "How much AUM is in small-cap value ETFs?"
**Answer:** ~$50B in dedicated small-cap value ETFs (IWN, VBR, SLYV, etc.)

**Structural force:** Institutional liquidity preference (they avoid illiquid small-caps) + behavioral value bias (underreaction to fundamentals).

**Assessment:** Constraint is persistent (institutions won't suddenly prioritize illiquidity). Crowding is MEDIUM ($50B is significant but not extreme).

#### Stage 3: Regime Testing
**Backtest small-cap value 2000-2025, split by regime:**

| Regime | Sharpe | Max DD | Win Rate | Notes |
|--------|--------|--------|----------|-------|
| LOW (2003-2007, 2017-2019) | 1.2 | 15% | 58% | Works well, steady |
| MED (2010-2015, 2021-2023) | 0.8 | 22% | 54% | Mixed, choppy |
| HIGH (2008-2009, 2020) | -0.3 | 45% | 38% | Catastrophic crashes |

**Conclusion:** Small-cap value is **regime-dependent**. Only works in LOW/MED risk regimes. Collapses in HIGH risk (liquidity crunch).

#### Stage 4: Capacity Estimation
**Market size:** ~$2 trillion total small-cap market cap
**Current AUM targeting:** ~$50B in dedicated ETFs + unknown hedge fund capital
**Execution slippage:** High (illiquid, wide spreads)

**Estimate:** Capacity ~$100B total before alpha decay. Currently at $50B+ → **MEDIUM crowding**.

**Action:** Trade selectively, avoid when MSI >50 (high risk regime likely).

#### Stage 5: Pattern Monitoring
**Monthly checks:**
- Performance: IWN (iShares Russell 2000 Value ETF) vs Russell 2000
- Crowding: IWN + VBR AUM trends
- Regime: Current 5-factor regime state
- Early warnings: MSI from your early-warning system

**Current status (Jan 2026):**
- Regime: MED (vol normal, above 200DMA, moderate correlation)
- MSI: 45 (no major systemic risks)
- Crowding: Stable at $50B
- Recent performance: Sharpe ~0.6 trailing 12 months

**Recommendation:** MAINTAIN exposure, size at 1.0x (baseline). If MSI >60, cut to 0.5x or eliminate.

---

## Summary: Key Takeaways

### The Water/Surfing Metaphor Teaches Us:

1. **Patterns (rocks) exist because of structural forces (geology), not luck**
   - Find patterns with persistent structural explanations
   - Avoid purely statistical patterns (data mining)

2. **Patterns erode as capital crowds them (rock wears down)**
   - Monitor crowding via ETF AUM, 13F filings, Google Trends
   - Expect Sharpe decay of 30-50% post-publication

3. **Regime determines which patterns work (water flow changes surfability)**
   - Same pattern, different regime = different outcome
   - Test patterns separately by LOW/MED/HIGH risk regimes

4. **Upstream rocks (future events) signal pattern changes ahead**
   - Use your early-warning MSI/SSI to detect structural shifts
   - When MSI >60, re-evaluate all active patterns

5. **Wu wei: only surf when conditions favor you (don't force trades)**
   - Eliminate trades in neutral regimes (no clear advantage)
   - Only act when regime extremes create positional advantage (Shi presence)

### Implementation Priority:

**Phase 1 (Weeks 1-2): Foundation**
- Build regime-classifier skill (5-factor)
- Build pattern-performance-tracker skill (by-regime reporting)
- Build structural-force-research skill (Perplexity-powered)

**Phase 2 (Weeks 3-4): Discovery**
- Build pattern-identifier agent (finds candidates)
- Build regime-pattern-analyst agent (tests by regime)
- Evaluate 10 candidate patterns using workflow above

**Phase 3 (Weeks 5-6): Monitoring**
- Build pattern-health-monitor agent (crowding, decay, lifecycle)
- Build upstream-risk-analyst agent (MSI × pattern survival)
- Deploy weekly pattern health reports

**Phase 4 (Ongoing): Optimization**
- Build pattern-entry-optimizer agent (timing, kuzushi)
- Build innovation-scout agent (upstream pattern discovery)
- Refine based on live performance

---

**The goal: Identify high-capacity, structurally-sound patterns that work in your target regimes, avoid crowded patterns, and react when upstream risks signal pattern invalidation. You're not predicting—you're observing, classifying, and reacting.**
