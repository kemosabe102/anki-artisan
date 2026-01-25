# Gate Thresholds

Tier-specific gate definitions and Deflated Sharpe Ratio (DSR) calculation.

**Source of Truth**: `C:/Users/kemos/Repos/trendy-trader/quantconnect/tier-config.json`

---

## Quick Reference Table

| Tier | Periods | Sharpe | Max DD | Min Trades | Win Rate | Regime CV | OOS/IS | Monte Carlo | Capacity |
|------|---------|--------|--------|------------|----------|-----------|--------|-------------|----------|
| 1 | 2 | >= 0.20 | <= 50% | >= 20 | - | - | - | - | - |
| 2 | 6 | >= 0.30 | <= 35% | >= 50 | >= 35% | < 0.5 | - | - | - |
| 3 | 15 | >= 0.50 | <= 30% | >= 100 | >= 40% | < 0.4 | - | Optional | >= 70% (SOFT) |
| 4 | 10 | >= 0.35 (DSR) | <= 25% | >= 150 | >= 42% | < 0.7 | >= 0.5 | p < 0.05 (HARD) | >= 75% (HARD) |

---

## Tier-Specific Rules

### Tier 1 - Sanity Check

**Periods**: 2 (post_gfc_bull, gfc_bear)

**Purpose**: Confirm strategy non-random across bull/bear regimes.

**Gates**:
- Sharpe >= 0.20
- Max Drawdown <= 50%
- Min Trades >= 20

## Deflated Sharpe Ratio (DSR) Calculation

Used at Tier 4 to penalize multiple trials and prevent overfitting.

### Formula

```
DSR = SR * sqrt(1 - gamma * trials)

Where:
  SR = Raw Sharpe Ratio from backtest
  gamma = 0.08 (penalty factor)
  trials = number of hypothesis trials completed
```

### Example Calculation

```
Raw SR = 0.50
Trials = 5
Deflation = sqrt(1 - 0.08 * 5) = sqrt(0.6) = 0.775
DSR = 0.50 * 0.775 = 0.387 (passes >= 0.35 threshold)
```

### Trial Penalty Table

| Trials | Deflation Factor | 0.50 SR becomes |
|--------|------------------|-----------------|
| 1 | 0.960 | 0.480 |
| 2 | 0.917 | 0.459 |
| 3 | 0.872 | 0.436 |
| 4 | 0.825 | 0.412 |
| 5 | 0.775 | 0.387 |

**Additional Gates**:
- `bull_competence`: return > 0 in bull period
- `bear_loss_controlled`: loss <= SPY loss in bear period

---

### Tier 2 - Moderate Validation

**Periods**: 6 (post_gfc_bull, gfc_bear, tech_boom, covid_crash, inflation_bear_2022, vol_lehman)

**Purpose**: Multi-regime robustness test.

**Gates**:
- Sharpe >= 0.30
- Max Drawdown <= 35%
- Min Trades >= 50
- Win Rate >= 35%
- Regime CV < 0.5

**Regime Breakdown Gates**:
- `bull_sharpe` >= 0.2
- `bear_sharpe` >= -0.2
- `high_vol_sharpe` >= 0.0

---

### Tier 3 - Comprehensive Development

**Periods**: 15 (from development group)

**Purpose**: Final optimization before parameter lock.

**Gates**:
- Sharpe >= 0.50
- Max Drawdown <= 30%
- Min Trades >= 100
- Win Rate >= 40%
- Regime CV < 0.4

**Curve-Fit Detection**:
- OOS/IS ratio >= 0.85: WARNING
- OOS/IS ratio >= 0.70: threshold (below = FAIL)

**Important**: LAST tier allowing parameter modifications.

---

### Tier 4 - Final UAT

**Periods**: 10 (from validation group)

**Purpose**: True out-of-sample test with locked parameters.

**Prerequisites**:
- MANDATORY: Parameter lock verification (git hash check)
- All parameters must be locked (no unlocked params)

**Gates**:
- Sharpe >= 0.35 (uses DSR, not raw Sharpe)
- Max Drawdown <= 25%
- Min Trades >= 150
- Win Rate >= 42%
- Regime CV < 0.7
- OOS/IS ratio >= 0.5

---

## Gate Application Order

Gates are applied in sequence. First failure halts validation:

1. `trade_count` >= minimum
2. `sharpe` >= minimum (DSR for Tier 4)
3. `drawdown` <= maximum
4. `win_rate` >= minimum (Tier 2+)
5. `regime_cv` < threshold (Tier 2+)
6. `oos_is_ratio` >= threshold (Tier 4)
7. `monte_carlo_pvalue` < 0.05 (Tier 4 MANDATORY)
8. `capacity_score` >= threshold (Tier 3+ MANDATORY)

**All gates are HARD**: First failure = FAIL verdict (no soft warnings at Tier 4).

---

## Monte Carlo Validation (MANDATORY at Tier 4)

To distinguish luck from edge, validate DSR results with bootstrap simulation.

### Methodology

1. **Collect trade data** from the backtest period
2. **Shuffle entry/exit times** within the regime (1000 iterations)
3. **Calculate simulated Sharpe** for each permutation
4. **Build distribution** of simulated Sharpe ratios
5. **Compare actual DSR** to simulation distribution
6. **Calculate p-value** as percentile of actual vs simulated

### Interpretation

| p-value | Interpretation | Action |
|---------|----------------|--------|
| < 0.01 | Highly significant edge | Strong PASS signal |
| 0.01-0.05 | Significant edge | PASS with confidence |
| 0.05-0.10 | Marginal significance | WARN, may be luck |
| > 0.10 | Not significant | Likely luck, investigate |

### Implementation

**MODE: monte_carlo** in `backtester` agent:

```
Task(backtester, prompt="MODE: monte_carlo
  Algorithm: {algorithm}
  Tier: {tier}
  Trade data: {trades_json}
  Simulations: 1000
  
  Return: {
    actual_dsr: number,
    simulated_mean: number,
    simulated_std: number,
    percentile: number,
    p_value: number,
    verdict: SIGNIFICANT|MARGINAL|NOT_SIGNIFICANT
  }")
```


### Example Output

```json
{
  "actual_dsr": 0.45,
  "simulated_mean": 0.12,
  "simulated_std": 0.18,
  "percentile": 96.2,
  "p_value": 0.038,
  "verdict": "SIGNIFICANT",
  "interpretation": "DSR of 0.45 exceeds 96.2% of random permutations (p=0.038)"
}
```

### When to Apply

- **Tier 3**: OPTIONAL but recommended
- **Tier 4**: MANDATORY - Backtest will FAIL if Monte Carlo not run or p-value >= 0.05
- **Requirement**: DSR must pass threshold first (Monte Carlo validates edge, DSR measures magnitude)
- **Computation**: Approximately 30-60 seconds for 1000 simulations

### Tier 4 Enforcement

```
IF tier == 4:
  IF monte_carlo_pvalue is NULL or MISSING:
    FAIL "Monte Carlo validation required at Tier 4. Run MODE: monte_carlo first."
  IF monte_carlo_pvalue >= 0.05:
    FAIL "Monte Carlo p-value {pvalue} >= 0.05 threshold. Edge not statistically significant."
  ELSE:
    PASS with confidence level
```

### Caveats

- Monte Carlo tests edge existence, not magnitude
- Does not account for transaction costs in simulation
- Requires minimum 50 trades for reliable statistics
- Results sensitive to regime boundaries used for shuffling

---

## Capacity Scaling Test (Tier 3+)

Tests strategy's capacity limits by simulating increased capital deployment. Answers: "How much capital can this pattern sustain before it collapses?"

### Philosophy

> Patterns can collapse under exploitation. The more capital deployed, the more market impact. Test at scale before deploying.

### Methodology

1. Run baseline backtest with initial_capital (e.g., $100K)
2. Re-run with scaled capital: 2x, 5x, 10x
3. Apply slippage model based on position size vs ADV
4. Compare Sharpe ratio degradation at each scale
5. Calculate capacity ceiling

### Scaling Test Parameters

| Scale | Capital | Expected Max Degradation |
|-------|---------|-------------------------|
| 1x (baseline) | $100K | 0% (reference point) |
| 2x | $200K | < 10% degradation |
| 5x | $500K | < 20% degradation |
| 10x | $1M | < 30% degradation |

### Capacity Score Formula

```
Capacity_Score = (Sharpe_10x / Sharpe_baseline) × 100

Example:
  Baseline Sharpe: 0.65
  10x Sharpe: 0.48
  Capacity Score: (0.48 / 0.65) × 100 = 73.8%
```

### Slippage Model

```
Estimated_Slippage_bps = (Position_Size / ADV) / Participation_Rate × 10000

Where:
  ADV = Average Daily Volume (shares)
  Participation_Rate = 0.02 (2% of ADV, conservative)
  
If Estimated_Slippage > 50 bps: Apply full slippage penalty
If Estimated_Slippage > 25 bps: Apply half slippage penalty
If Estimated_Slippage <= 25 bps: No penalty
```

### Gate Thresholds

| Tier | Capacity Score Threshold | Gate Type |
|------|-------------------------|-----------|
| 1-2 | Not required | N/A |
| 3 | >= 70% | SOFT (warning only) |
| 4 | >= 75% | HARD (fail if below) |

### Implementation

```
Task(backtester, prompt="MODE: capacity_test
  hypothesis_id: {hypothesis_id}
  baseline_capital: 100000
  scale_factors: [2, 5, 10]
  slippage_model: volume_proportional
  
  Return: {
    baseline_sharpe: number,
    scaled_results: [{scale, capital, sharpe, degradation_pct}],
    capacity_score: number,
    estimated_capacity_ceiling_usd: number,
    verdict: PASS|WARN|FAIL
  }")
```

### Example Output

```json
{
  "capacity_test_results": {
    "baseline_sharpe": 0.65,
    "scaled_results": [
      {"scale": 2, "capital": 200000, "sharpe": 0.62, "degradation_pct": 4.6},
      {"scale": 5, "capital": 500000, "sharpe": 0.55, "degradation_pct": 15.4},
      {"scale": 10, "capital": 1000000, "sharpe": 0.48, "degradation_pct": 26.2}
    ],
    "capacity_score": 73.8,
    "estimated_capacity_ceiling_usd": 750000,
    "verdict": "PASS"
  }
}
```

### Interpretation

| Capacity Score | Interpretation | Action |
|----------------|----------------|--------|
| >= 90% | Excellent scalability | Deploy with confidence |
| 75-89% | Good scalability | Monitor at scale |
| 70-74% | Marginal scalability | Limit deployment capital |
| < 70% | Poor scalability | Do not scale beyond baseline |

### Caveats

- Slippage model is simplified; real market impact may differ
- Does not account for competitor crowding
- Best used in combination with Monte Carlo validation
- Results most accurate for liquid securities (ADV > 1M shares)
