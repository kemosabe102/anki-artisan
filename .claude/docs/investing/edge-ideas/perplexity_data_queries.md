# Perplexity Queries for Custom Data (Trading-Focused)

**Objective:** Use Perplexity as a data extraction agent to supplement QuantConnect + FRED

---

## Strategy 1: Debt-Cycle Optimizer

### Weekly Queries (Takes 15 minutes, run Sundays)

#### Query 1: Current Debt Metrics
```
"As of [TODAY'S DATE], what is:
1. US Debt-to-GDP ratio (%)
2. Debt service ratio (%)
3. Credit market debt growth rate (YoY %)
4. Federal Reserve policy stance (tightening/stable/easing)
5. Yield curve (10Y-2Y spread)

Source FRED data or Federal Reserve reports. Format as CSV:
metric,value,date,source"
```

**Expected output:**
```
debt_to_gdp,129.5,2026-01-04,FRED
debt_service_ratio,5.2,2025-Q4,Federal Reserve
credit_growth_yoy,3.1,2025-12,FRED
fed_stance,stable,2026-01,Federal Reserve
yield_curve_10y2y,-0.15,2026-01-03,FRED
```

**Why ask Perplexity instead of FRED API:** Faster for recent changes, gets qualitative context ("is Fed about to pivot?")

---

#### Query 2: Historical Debt Cycle Precedents
```
"When was the US last in a LATE debt cycle phase (debt >110% GDP, rising service costs)?
List all instances in past 30 years with:
- Start date and end date of late phase
- Key events (recessions, market crashes)
- Equity market performance before/during/after
- Debt metrics at peak"
```

**Expected output:**
```
Late Cycle Period: 2005-2008 (GFC)
  Peak debt/GDP: 120% (2008)
  Peak debt service: 6.5% (2008)
  Equity drawdown: SPX -57% (2008)
  Recovery time: 4 years

Late Cycle Period: 1999-2001 (Tech bubble)
  ...
```

**Why ask:** Validates historical pattern (debt cycle → drawdown correlation)

---

### Monthly Queries (Takes 10 minutes)

#### Query 3: Fed Policy Changes
```
"Has the Federal Reserve signaled any changes to:
1. Interest rate trajectory (next 6 months)
2. Quantitative easing/tightening plans
3. Reserve requirement changes
4. Regulatory constraints on bank lending

Source latest FOMC minutes and speeches. Format decision impacts on debt-cycle phase."
```

**Why ask:** Detects policy shifts that change debt phase classification

---

## Strategy 2: Institutional Liquidity Arb

### Quarterly Queries (Takes 30 minutes, run day after quarter-end + 45 days)

#### Query 1: Top Institutional Changes
```
"Based on latest SEC 13F filings (released [45 days after quarter end]),
which institutions are INCREASING their small-cap value position?

For each institution showing >15% increase in Russell 2000 value holdings:
- Institution name
- Total small-cap value AUM increase ($M)
- Top 5 new positions (stock, shares, portfolio weight)

Also list institutions DECREASING small-cap value by >15%:
- Institution name
- Total small-cap value AUM decrease ($M)
- Top 5 sold positions"
```

**Expected output:**
```
INCREASING:
Berkshire Hathaway, +$2.1B, [stocks list]
Soros Fund, +$450M, [stocks list]

DECREASING:
BlackRock (passive flows), -$8.2B, [stocks list]
Vanguard, -$12.1B, [stocks list]
```

**Why ask:** Identifies when institutions are exiting small-cap (your signal to enter)

---

#### Query 2: Crowding Monitor
```
"How much AUM is currently in small-cap value ETFs and funds?

List:
1. Total AUM in Russell 2000 value focused products
   - Russell 2000 Value ETF (IWN, VBR, SLYV)
   - Factor funds focused on small-cap value
2. YoY change in AUM ($B)
3. Performance of small-cap value vs Russell 2000 (past 12 months)
4. Average expense ratio
5. Estimated crowding level (low/med/high)"
```

**Expected output:**
```
IWN (iShares Russell 2000 Value): $8.2B AUM, YoY +$1.1B
VBR (Vanguard Russell 2000 Value): $12.5B AUM, YoY +$0.8B
SLYV (SPDR Russell 2000 Value): $4.3B AUM, YoY -$0.2B
Total small-cap value ETF AUM: $94.7B
Crowding: MEDIUM (up 5% YoY but performance declining)
```

**Why ask:** Monitors if strategy is getting crowded (Sharpe decay signal)

---

#### Query 3: Institutional Mandates (Annual)
```
"What percentage of Russell 2000 holdings are currently:
1. Index funds/passive (tracking Russell 2000)
2. Active value funds
3. Growth-focused (underweight value)
4. Foreign investors (capital flows)

Has this mix changed significantly in past 5 years?
What does this imply for value premium persistence?"
```

**Why ask:** Detects if institutions' liquidity preferences are changing

---

### Ongoing: Quarterly 13F Deep-Dives (Takes 1 hour per top 5 institutions)

#### Query 4: Single Institution Deep-Dive
```
"Based on Berkshire Hathaway's latest 13F filing, what is their
current small-cap value concentration?

Show:
1. Top 10 positions in Russell 2000 value universe
2. % of portfolio allocated to small-cap value
3. Average position size ($M)
4. Entry timing (rough estimate from changes)
5. Any large exits or additions?
6. Geographic/sector bias?"
```

**Why ask:** Understand what smart money is doing; mimic if thesis is sound

---

## Strategy 3: Kuzushi Bubble Detector

### Weekly Queries (Takes 20 minutes)

#### Query 1: Emerging Theme Detection
```
"What are the top 3-5 investment themes showing the fastest growth in:
1. Google search volume (YoY growth %)
2. News mentions (YoY growth %)
3. Retail trader interest (Reddit mentions, options volume)
4. Stock price momentum

For each theme:
- Theme name
- Growth rate (%)
- Key companies
- Current sentiment (bullish/neutral/frothy)
- Risk: Is it approaching parabolic?"
```

**Expected output:**
```
Theme: AI Infrastructure (semiconductor + chips)
  Google Trends: +180% YoY (NVIDIA, SMCI, PLTR mentions)
  News: +240% YoY mentions
  Options volume: Call/put ratio = 2.5:1 (bullish)
  Sentiment: FROTHY (red flag for kuzushi near)
  
Theme: AI Chips Mining (MSTR, CLSK, RIOT focus on Bitcoin)
  Growth: +320% YoY
  Sentiment: EXTREMELY FROTHY (high risk)
```

**Why ask:** Identifies bubbles at early stage; track for kuzushi signals

---

#### Query 2: Theme Stability Check
```
"For [THEME] (e.g., 'AI stocks', 'crypto'), what is the current:
1. Breadth: % of theme stocks above 50-day MA
2. Correlation: Average daily correlation between top 10 names
3. Momentum exhaustion: Is price parabolic? (RSI > 70, 5-day range)
4. Insider activity: Are insiders buying or selling?
5. Short interest: % of float shorted
6. Kuzushi indicators present?

Format red flags and confidence level (1-5, 5=high kuzushi risk)."
```

**Expected output:**
```
Theme: Meme stocks (January 2021 history)
  Breadth: 35% above 50MA (declining, red flag)
  Correlation: 0.78 (rising, herd selling, red flag)
  Momentum: RSI 78, 5-day range +28% (parabolic, red flag)
  Insider selling: +250% vs historical average (red flag)
  Kuzushi confidence: 4.5 / 5 (high conviction short setup)
```

**Why ask:** Validates multi-metric kuzushi signal before entry

---

#### Query 3: Theme Lifecycle Position
```
"Where is [THEME] in its lifecycle (early/mature/parabolic/collapsing)?

Analyze:
1. Birth date (when did narrative start? When did institutions start buying?)
2. Duration (how long has theme been hot? Compare to historical bubbles)
3. Participation breadth (% of retail traders interested? Google Trends peak?)
4. Price momentum (how many 52-week highs? Multiple of mean reversion target?)
5. Comparable bubbles (which past theme does this resemble? What was outcome?)

Expected outcome if kuzushi is triggered."
```

**Expected output:**
```
Theme: SPACs (2020-2021)
  Birth: Q3 2020
  Duration: 18 months at peak
  Participation: 92 percentile Google Trends (near peak)
  Price momentum: 8x from start (parabolic)
  Comparable: Dotcom bubble structure
  Outcome forecast: 60-80% drawdown, 12-18 month decline
```

**Why ask:** Estimates timing and magnitude of collapse for position sizing

---

### Daily/Weekly Sentiment Checks (Takes 10 minutes)

#### Query 4: Real-Time Sentiment Flip
```
"Has sentiment on [THEME] changed in the past week?

Check:
1. News tone (% negative vs positive articles)
2. Social media (Reddit, Twitter sentiment shift)
3. Options market (put/call ratio change)
4. Insider selling activity
5. Retail flow reversals

Alert level: Green / Yellow / Red"
```

**Why ask:** Catches early reversal signals before full kuzushi

---

## Strategy 4: Cross-Strategy Monitoring (Weekly)

### Query: Macro Risk Check
```
"Current status check across macro risk indicators:

1. Equity valuations (CAPE ratio, S&P 500 P/E)
2. Credit stress (high-yield spread, investment-grade spread)
3. Volatility (VIX level vs 20-day MA)
4. Correlation (average equity-to-equity correlation)
5. Sentiment extremes (AAII bullish %, CNN Fear/Greed index)
6. Debt-cycle phase (from Query 1 above)

Score each: Low risk (0-2) / Medium (3-5) / High (6-10)
Overall risk regime: [color coded by debt-cycle + sentiment combo]"
```

**Why ask:** Single weekly health check for all strategies

---

## Implementation: Perplexity as a Data Agent

### Option A: Manual (Weekly 30 minutes)

1. Copy-paste one query above into Perplexity
2. Save output as CSV/JSON to your local data folder
3. Import into backtester weekly
4. Merge with QuantConnect price data

**Frequency:** Weekly (Sundays 5pm) for debt-cycle, quarterly for 13F, daily for sentiment

**Time:** 15-30 min per week

---

### Option B: Automated (If Perplexity launches API)

```python
# Pseudo-code: Perplexity agent pulling data weekly

class PerplexityDataAgent:
    def __init__(self, perplexity_api_key):
        self.api_key = perplexity_api_key
    
    def query_debt_metrics(self):
        query = "As of [today], what is US debt-to-GDP, debt service ratio, ..."
        response = self.call_perplexity(query)
        return self._parse_csv(response)
    
    def query_institutional_flows(self, quarter):
        query = f"Based on latest 13F filings, which institutions increased small-cap value by >15%?"
        response = self.call_perplexity(query)
        return self._parse_csv(response)
    
    def query_theme_kuzushi(self, theme):
        query = f"What is kuzushi confidence level for {theme}? Check breadth, correlation, insider selling..."
        response = self.call_perplexity(query)
        return self._parse_json(response)
    
    def call_perplexity(self, query):
        # Once Perplexity API available
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"model": "mistral", "messages": [{"role": "user", "content": query}]}
        )
        return response.json()['choices'][0]['message']['content']

# Run weekly
agent = PerplexityDataAgent(api_key)
debt_data = agent.query_debt_metrics()
institutional_flows = agent.query_institutional_flows("Q4-2025")
kuzushi_ai = agent.query_theme_kuzushi("AI infrastructure")

# Merge with QuantConnect data and run strategy
```

**If Perplexity API launches:** This becomes fully automated. Cost: ~$0.01-0.10 per query = $0.50-5/week

---

## Cost-Benefit Analysis

### Current Option (Manual Perplexity Queries)

| Query | Frequency | Time | Cost | Value |
|-------|-----------|------|------|-------|
| Debt metrics | Weekly | 10 min | $0 | High (validates regime) |
| Institutional flows | Quarterly | 20 min | $0 | High (signals crowding) |
| Theme kuzushi | Weekly-daily | 10 min | $0 | Medium (noisy but useful) |
| **Total/month** | - | 2-3 hours | $0 | Very high |

### Alternative (Paid Data)

| Provider | Cost/Month | Setup Time | Data Quality | Advantage |
|----------|-----------|-----------|--------------|-----------|
| FactSet | $1000+ | 4 hours | 99% | Real-time 13F |
| Morningstar | $500+ | 2 hours | 95% | Institutional ownership % |
| Alternative Data | $200-500 | 1 hour | 85% | Theme sentiment |
| **Free Perplexity** | $0 | 5 min per query | 80% | Good enough for MVP |

**Verdict:** Start with free Perplexity queries. Only upgrade if backtests show edge works and you need higher precision.

---

## Sample Weekly Data Pull (Copy-Paste)

### Sunday Evening Data Collection Script

```
1. FRED API pull (Python script, 5 minutes):
   - Debt/GDP
   - Debt service ratio
   - Credit impulse
   - Fed Funds rate
   - 10Y-2Y spread
   → Save to /data/debt_metrics_2026-01-05.csv

2. QuantConnect pull (Your backtester, 5 minutes):
   - SPY daily close, volume
   - Small-cap basket daily close
   - Russell 2000 daily close
   → Auto-updated

3. Perplexity query (Manual, 10 minutes):
   Copy Query #1 (Debt Metrics)
   Copy Query #1b (Historical precedents, monthly)
   Paste response to /data/perplexity_debt_2026-01-05.txt
   Extract key insights

4. Perplexity query (Manual, 10 minutes):
   Copy Query #2 (Theme detection)
   Paste response to /data/perplexity_themes_2026-01-05.txt
   Flag any new bubbles

Total time: 30 minutes
Cost: $0
Frequency: Weekly Sunday 5pm
```

---

## Red Flags If Data Quality Breaks

| Signal | Action |
|--------|--------|
| Perplexity query returns outdated info | Rephrase with "[TODAY'S DATE]" or switch to FRED API |
| 13F data shows obvious errors | Validate against SEC EDGAR directly; use SEC API |
| Google Trends stops working | Switch to Perplexity: "What's trending on Google this week?" |
| Institutional flows contradict market | Double-check against latest 13F; confirm filing date |
| Debt metrics from Perplexity conflict with FRED | Always trust FRED (official source); use Perplexity for context |

---

## Summary: Data Stack for MVP

| Strategy | Primary Data | Secondary Data | Frequency | Cost | Effort |
|----------|--------------|-----------------|-----------|------|--------|
| **Debt-Cycle** | FRED API | Perplexity (context) | Weekly | $0 | 15 min |
| **Liquidity Arb** | QuantConnect + SEC EDGAR | Perplexity (13F changes) | Quarterly | $0 | 30 min |
| **Kuzushi** | QuantConnect (prices) | Perplexity (theme + sentiment) | Weekly-daily | $0 | 20 min |

**All three strategies can launch with $0 custom data spend. Upgrade only if backtests validate.**

---

## Final Recommendation

**Week 1:** Build debt-cycle optimizer using FRED API + QuantConnect

**Week 2:** Backtest 2000-2025

**Week 3:** If backtest shows Sharpe >0.8, add Perplexity queries for weekly monitoring

**Week 4:** Deploy with quarterly rebalance automation

**Week 5+:** Once live, assess data quality and decide if paying for FactSet/Morningstar API is worth it

**Don't over-engineer data collection. Ship fast with free data. Upgrade only when you need precision, not upfront.**
