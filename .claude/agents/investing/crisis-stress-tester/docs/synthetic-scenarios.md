# Synthetic Crisis Scenarios

## Purpose

Defines synthetic stress test scenarios that go beyond historical crisis replay. Synthetic scenarios allow testing strategy robustness against:

1. **Worse-than-historical conditions** - What if 2008 was even worse?
2. **Novel combinations** - Correlation spike + liquidity crisis simultaneously
3. **Strategy-specific vulnerabilities** - Stress test known weak points

**PREREQUISITE**: Historical crises MUST pass before synthetic testing. A strategy that fails historical replay has no business being tested against hypothetical scenarios.

---

## Execution Order

Synthetic tests run ONLY after historical crisis validation passes:

```
GFC 2008 (PASS) -> COVID 2020 (PASS) -> Rate Hike 2022 (PASS) -> Synthetic Tests
```

If ANY historical crisis fails, synthetic testing is skipped with verdict: FRAGILE.

---

## Scenario Types

### 1. Correlation Spike (`correlation_spike`)

#### Description
Simulates all portfolio assets moving in lockstep, destroying diversification benefits. During crises, correlations spike as "all correlations go to 1."

#### Default Parameters
- **correlation**: 0.9
- **duration**: 30 days

#### Historical Reference
GFC 2008 saw cross-asset correlations spike to 0.9+ as credit contagion spread across all markets. Asset classes that historically provided diversification (commodities, international equities) moved in tandem with US equities.

#### Implementation Formula
```python
# Simulate correlated returns for portfolio assets
def simulate_correlation_spike(asset_returns, target_corr, duration_days):
    """
    Transform independent returns into correlated returns.
    Uses Cholesky decomposition to impose correlation structure.
    """
    n_assets = len(asset_returns)
    
    # Create correlation matrix (all pairs at target_corr)
    corr_matrix = np.full((n_assets, n_assets), target_corr)
    np.fill_diagonal(corr_matrix, 1.0)
    
    # Cholesky decomposition
    L = np.linalg.cholesky(corr_matrix)
    
    # Transform returns
    correlated_returns = independent_returns @ L.T
    
    return correlated_returns[-duration_days:]
```

#### Pass Criteria
```
Portfolio DD < 1.5x Single-Asset DD
```

**Rationale**: If diversification is working, portfolio drawdown should be less than individual asset drawdowns. At 1.5x, the portfolio is still capturing some diversification benefit even under stress. Above 1.5x suggests false diversification.

---

### 2. Volatility Surge (`volatility_surge`)

#### Description
Simulates extreme volatility environment with VIX spiking to panic levels. Tests position sizing, stop-loss behavior, and margin requirements under stress.

#### Default Parameters
- **vix_level**: 80
- **duration**: 14 days
- **vol_path**: spike_decay (default)

#### Vol Path Options
| Path | Description | Use Case |
|------|-------------|----------|
| `spike_decay` | Sharp spike, gradual decay | Most common crisis pattern |
| `sustained` | High volatility maintained | Prolonged uncertainty |
| `oscillating` | Repeated spikes and drops | Choppy recovery period |

#### Historical Reference
COVID 2020 saw VIX peak at **82.69** on March 16, 2020. The GFC 2008 VIX peaked at **89.53** on November 20, 2008. These represent the upper bounds of historical volatility.

#### Implementation Formula
```python
def simulate_volatility_surge(base_returns, vix_target, duration, vol_path='spike_decay'):
    """
    Scale returns to match target VIX-implied volatility.
    VIX represents annualized volatility, so convert to daily.
    """
    target_daily_vol = vix_target / 100 / np.sqrt(252)  # VIX to daily vol
    current_daily_vol = np.std(base_returns)
    
    vol_multiplier = target_daily_vol / current_daily_vol
    
    if vol_path == 'spike_decay':
        # Exponential decay from peak
        decay_factors = np.exp(-np.arange(duration) / (duration / 3))
        multipliers = 1 + (vol_multiplier - 1) * decay_factors
    elif vol_path == 'sustained':
        multipliers = np.full(duration, vol_multiplier)
    elif vol_path == 'oscillating':
        # Sine wave between 1 and vol_multiplier
        multipliers = 1 + (vol_multiplier - 1) * (0.5 + 0.5 * np.sin(np.arange(duration) * np.pi / 3))
    
    stressed_returns = base_returns[-duration:] * multipliers
    return stressed_returns
```

#### Pass Criteria
```
1. No margin violations during stress period
2. Maximum DD < 50%
```

**Rationale**: Margin violations during volatility spikes cause forced liquidation at worst prices. The 50% DD threshold matches COVID 2020 gate, ensuring strategy survives VIX 80+ environments.

---

### 3. Liquidity Crisis (`liquidity_crisis`)

#### Description
Simulates market liquidity drying up with bid-ask spreads widening dramatically. Tests execution assumptions and slippage models.

#### Default Parameters
- **spread_multiplier**: 5x
- **duration**: 7 days

#### Historical Reference
March 2020 saw bid-ask spreads widen **5-10x** normal levels across equity, bond, and ETF markets. Some ETFs traded at significant discounts to NAV due to authorized participant dysfunction.

#### Implementation Formula
```python
def simulate_liquidity_crisis(trades, normal_spread_bps, spread_multiplier, duration):
    """
    Apply widened spreads to trade execution.
    Assumes mid-price execution in normal conditions.
    """
    stressed_spread_bps = normal_spread_bps * spread_multiplier
    
    adjusted_trades = []
    for trade in trades[-duration:]:
        # Half spread applied to each side (buy at ask, sell at bid)
        slippage_pct = stressed_spread_bps / 10000 / 2
        
        if trade['side'] == 'BUY':
            adjusted_price = trade['price'] * (1 + slippage_pct)
        else:
            adjusted_price = trade['price'] * (1 - slippage_pct)
        
        adjusted_trades.append({
            **trade,
            'executed_price': adjusted_price,
            'slippage_bps': stressed_spread_bps / 2
        })
    
    return adjusted_trades
```

#### Pass Criteria
```
1. Strategy remains profitable after slippage adjustment
2. No individual trade executed at > 1% slippage (100 bps)
```

**Rationale**: Strategies that rely on tight spreads for profitability will fail in liquidity crises. The 1% single-trade slippage cap prevents strategies that would execute at catastrophic prices.

---

### 4. Custom Scenario (`custom`)

#### Description
User-defined stress parameters allowing for scenario combinations and strategy-specific stress testing.

#### Usage
```json
{
  "scenario_type": "custom",
  "scenario_params": {
    "correlation": 0.85,
    "vix_level": 60,
    "spread_multiplier": 3,
    "duration_days": 21,
    "description": "Moderate stress across all dimensions"
  }
}
```

#### Validation
All custom parameters must fall within defined bounds (see Parameter Bounds Table below).

---

## Parameter Bounds

| Parameter | Min | Max | Default | Unit |
|-----------|-----|-----|---------|------|
| `correlation` | 0.5 | 0.99 | 0.9 | coefficient |
| `vix_level` | 30 | 100 | 80 | VIX points |
| `spread_multiplier` | 2 | 10 | 5 | multiple |
| `duration_days` | 1 | 90 | 14 | days |

**Validation Rules**:
- Parameters outside bounds are rejected with error
- Min values represent "elevated but not crisis" conditions
- Max values represent "worse than any historical crisis"

---

## Pre-built Scenario Combos

Ready-to-use scenario combinations for common stress testing needs.

### Worse Than 2008
```json
{
  "name": "worse_than_2008",
  "description": "Conditions exceeding GFC severity",
  "params": {
    "correlation": 0.95,
    "vix_level": 100,
    "spread_multiplier": 7,
    "duration_days": 45
  },
  "rationale": "Tests survival if next crisis is worse than GFC"
}
```

### Flash Crash Extended
```json
{
  "name": "flash_crash_extended",
  "description": "Flash crash conditions sustained over days",
  "params": {
    "correlation": 0.85,
    "vix_level": 90,
    "spread_multiplier": 10,
    "duration_days": 3
  },
  "rationale": "Tests survival if 2010-style event lasted longer"
}
```

### Slow Bleed
```json
{
  "name": "slow_bleed",
  "description": "Prolonged mild stress eroding returns",
  "params": {
    "correlation": 0.6,
    "vix_level": 35,
    "spread_multiplier": 2,
    "duration_days": 90
  },
  "rationale": "Tests survival in grinding bear market (like 2022 but longer)"
}
```

---

## Output Structure

### Synthetic Test Result Schema

```json
{
  "status": "SUCCESS|FAILURE",
  "hypothesis_id": "HYP-001",
  "test_type": "synthetic_test",
  
  "synthetic_test_results": {
    "scenario_type": "correlation_spike",
    "scenario_name": "default",
    
    "parameters": {
      "correlation": 0.9,
      "duration_days": 30
    },
    
    "results": {
      "portfolio_dd": -42,
      "single_asset_avg_dd": -35,
      "dd_ratio": 1.2,
      "margin_violations": 0,
      "max_slippage_bps": 45,
      "period_return": -38.5
    },
    
    "gate_status": "PASS",
    "gate_threshold": "Portfolio DD < 1.5x Single-Asset DD",
    "gate_value": "1.2 < 1.5",
    
    "warnings": [],
    "recommendations": []
  },
  
  "historical_prerequisite": {
    "gfc_2008": "PASS",
    "covid_2020": "PASS",
    "rate_hike_2022": "PASS"
  },
  
  "verdict": "CRISIS_PROOF",
  "confidence": 0.85
}
```

### Multi-Scenario Result

When running multiple synthetic scenarios:

```json
{
  "status": "SUCCESS",
  "hypothesis_id": "HYP-001",
  "test_type": "synthetic_suite",
  
  "scenarios_tested": [
    {
      "scenario_type": "correlation_spike",
      "gate_status": "PASS"
    },
    {
      "scenario_type": "volatility_surge",
      "gate_status": "PASS"
    },
    {
      "scenario_type": "liquidity_crisis",
      "gate_status": "WARN",
      "warning": "Strategy profitable but 2 trades at >80 bps slippage"
    }
  ],
  
  "overall_synthetic_status": "PASS_WITH_WARNINGS",
  "verdict": "VULNERABLE"
}
```

---

## Integration with Agent

### Task() Invocation for Synthetic Test

```python
Task(crisis-stress-tester): {
  "hypothesis_id": "HYP-001",
  "mode": "synthetic_test",
  "scenario_type": "correlation_spike",
  "scenario_params": {
    "correlation": 0.95,
    "duration_days": 30
  },
  "strategy_spec": { ... },
  "request": "Run synthetic correlation spike test with 0.95 correlation for 30 days"
}
```

### Full Synthetic Suite

```python
Task(crisis-stress-tester): {
  "hypothesis_id": "HYP-001",
  "mode": "synthetic_test",
  "scenario_type": "suite",
  "scenarios": ["correlation_spike", "volatility_surge", "liquidity_crisis"],
  "strategy_spec": { ... },
  "request": "Run full synthetic crisis suite with default parameters"
}
```

### Pre-built Combo Invocation

```python
Task(crisis-stress-tester): {
  "hypothesis_id": "HYP-001",
  "mode": "synthetic_test",
  "scenario_type": "custom",
  "scenario_name": "worse_than_2008",
  "strategy_spec": { ... },
  "request": "Run 'Worse Than 2008' pre-built scenario"
}
```

---

## Validation Checklist

- [ ] Historical crises passed (GFC 2008, COVID 2020, Rate Hike 2022)
- [ ] Scenario parameters within bounds
- [ ] hypothesis_id provided
- [ ] Scenario-specific gates evaluated
- [ ] Results include all required fields
- [ ] Warnings surfaced for near-failures
- [ ] Recommendations actionable
