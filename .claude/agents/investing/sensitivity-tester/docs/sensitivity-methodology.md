# Sensitivity Testing Methodology

## Theory: Why Sensitivity Testing Matters

Backtesting produces optimistic results because:
1. **Survivorship bias**: Only surviving strategies are tested
2. **Look-ahead bias**: Parameters chosen with hindsight
3. **Curve-fitting**: Parameters tuned to historical noise

Sensitivity testing addresses #3 by asking: "Would this strategy work if parameters were slightly different?"

## Noise Injection

### Purpose
Detect strategies that only work at exact parameter values (curve-fit).

### Methodology

1. **Parameter Identification**: Extract all numeric parameters
   - Lookback periods (e.g., 20-day SMA)
   - Thresholds (e.g., RSI > 70)
   - Multipliers (e.g., 2x ATR stop)

2. **Noise Application**: For each parameter P:
   ```
   noised_values = [P * 0.90, P * 0.95, P * 1.05, P * 1.10]
   ```

3. **Backtest Each Variation**: Run with noised parameters
4. **Aggregate Results**: Calculate mean and std of Sharpe ratios

### Passing Criteria
```
degradation_pct = ((base_sharpe - noise_sharpe_mean) / base_sharpe) * 100
PASS if degradation_pct < 30%
```

### Interpretation
- <15%: Highly robust parameters
- 15-30%: Acceptable sensitivity
- 30-50%: Fragile, consider wider parameter bands
- >50%: Curve-fit, do not deploy

## Walk-Forward Analysis

### Purpose
Validate that strategy generalizes to unseen data (out-of-sample).


### Methodology

1. **Window Definition**:
   - Minimum 5 folds (3 for limited data)
   - IS:OOS ratio of 3:1 (e.g., 3 years IS, 1 year OOS)
   - Non-overlapping OOS periods

2. **Rolling Execution**:
   ```
   Fold 1: IS=[2015-2017], OOS=[2018]
   Fold 2: IS=[2016-2018], OOS=[2019]
   Fold 3: IS=[2017-2019], OOS=[2020]
   ...
   ```

3. **Efficiency Ratio Calculation**:
   ```
   efficiency_ratio = mean(OOS_sharpe) / mean(IS_sharpe)
   ```

### Passing Criteria
```
PASS if efficiency_ratio >= 0.50
```

### Interpretation
- >=0.70: Excellent generalization
- 0.50-0.69: Acceptable decay
- 0.30-0.49: Significant overfitting
- <0.30: Severe curve-fitting

## Parameter Stability

### Purpose
Identify "cliff-edge" parameters where small changes cause large performance drops.

### Methodology

1. **Fine-Grained Perturbation**: Test at ±5% (smaller than noise test)
2. **Cliff Detection**: Flag if any ±5% change causes >50% Sharpe drop
3. **Classification**:
   - STABLE: <20% variation
   - SENSITIVE: 20-50% variation
   - CLIFF_EDGE: >50% drop

### Passing Criteria
SOFT gate: Warn if cliff-edge parameters exist, but don't fail.

## Robustness Score Formula

```
sensitivity_score = (
  noise_stability_score * 0.40 +
  walk_forward_score * 0.40 +
  parameter_stability_score * 0.20
)

Where:
- noise_stability_score = max(0, 100 - (degradation_pct * 3.33))
- walk_forward_score = min(100, efficiency_ratio * 200)
- parameter_stability_score = 100 - (cliff_edge_count * 25)
```

## References

- Bailey, D. H., & Lopez de Prado, M. (2014). "The Deflated Sharpe Ratio"
- Pardo, R. (2008). "The Evaluation and Optimization of Trading Strategies"
- Aronson, D. (2006). "Evidence-Based Technical Analysis"
