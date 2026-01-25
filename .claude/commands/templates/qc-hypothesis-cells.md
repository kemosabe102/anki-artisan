---
title: "QC Hypothesis Test Cell Templates"
version: 1.0
used-by: algo-hypothesis-test.md
---

# QuantConnect Research Notebook Templates

## Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| {symbols} | List of ticker symbols | ["SPY", "QQQ"] |
| {timeframe} | Historical data period | "2Y" |
| {cause} | Hypothesis cause statement | "RSI(14) crosses below 30" |
| {indicator_code} | Python code for indicator | signal_df = ... |
| {alpha} | Significance threshold | 0.05 |
| {effect_bars} | Forward returns lookback | 5 |

---

## Cell 1: Setup

```python
# QuantConnect Research Environment Setup
from QuantConnect import *
from QuantConnect.Research import *
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

qb = QuantBook()
print("QuantBook initialized")
```

---

## Cell 2: Data Fetch

```python
# Fetch historical data
SYMBOLS = [{symbols}]  # e.g., ["SPY", "QQQ"]
TIMEFRAME = "{timeframe}"  # e.g., "2Y"

symbols = [qb.add_equity(s, Resolution.DAILY).symbol for s in SYMBOLS]
history = qb.history(symbols, int(TIMEFRAME.replace("Y",""))*252, Resolution.DAILY)
print(f"Fetched {{len(history)}} bars for {{SYMBOLS}}")
```

---

## Cell 3: Indicator Calculation

```python
# Calculate indicator from hypothesis CAUSE
# Hypothesis: {cause}
{indicator_code}

# Preview signal
signal_df.tail(10)
```

---

## Cell 4: Statistical Tests

```python
# Statistical validation (alpha = {alpha})
from scipy.stats import pearsonr, spearmanr
from statsmodels.tsa.stattools import adfuller

# Align signal with forward returns
forward_returns = prices.pct_change().shift(-{effect_bars})
aligned = pd.concat([signal_df['signal'], forward_returns], axis=1).dropna()

# Correlation tests
pearson_r, pearson_p = pearsonr(aligned.iloc[:,0], aligned.iloc[:,1])
spearman_r, spearman_p = spearmanr(aligned.iloc[:,0], aligned.iloc[:,1])

# Stationarity test
adf_stat, adf_p, _, _, _, _ = adfuller(signal_df['signal'].dropna())

print(f"Pearson:  r={{pearson_r:.3f}}, p={{pearson_p:.4f}} {{'✓' if pearson_p < {alpha} else '✗'}}")
print(f"Spearman: ρ={{spearman_r:.3f}}, p={{spearman_p:.4f}} {{'✓' if spearman_p < {alpha} else '✗'}}")
print(f"ADF:      stat={{adf_stat:.3f}}, p={{adf_p:.4f}} {{'✓' if adf_p < {alpha} else '✗'}}")
```

---

## Cell 5: Visualization

```python
# Visualize signal vs returns
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# Scatter plot
axes[0,0].scatter(aligned.iloc[:,0], aligned.iloc[:,1], alpha=0.3)
axes[0,0].set_xlabel('Signal')
axes[0,0].set_ylabel('Forward Returns')
axes[0,0].set_title(f'Signal vs {effect_bars}-bar Returns')

# Time series
axes[0,1].plot(signal_df.index, signal_df['signal'])
axes[0,1].set_title('Signal Time Series')

# Returns distribution by signal quintile
quintiles = pd.qcut(aligned.iloc[:,0], 5, labels=['Q1','Q2','Q3','Q4','Q5'])
aligned['quintile'] = quintiles
aligned.boxplot(column=aligned.columns[1], by='quintile', ax=axes[1,0])
axes[1,0].set_title('Returns by Signal Quintile')

# Cumulative returns of signal-based strategy
aligned['strategy'] = np.sign(aligned.iloc[:,0]) * aligned.iloc[:,1]
axes[1,1].plot((1 + aligned['strategy']).cumprod())
axes[1,1].set_title('Cumulative Strategy Returns')

plt.tight_layout()
plt.show()
```

---

## Cell 6: GO/NO-GO Decision

```python
# Hypothesis validation decision
alpha = {alpha}
go_criteria = (
    (pearson_p < alpha or spearman_p < alpha) and  # Significant correlation
    abs(pearson_r) > 0.1  # Meaningful effect size
)

if go_criteria and adf_p < alpha:
    print("🟢 GO - Hypothesis shows statistical support. Proceed to backtest.")
    print("   Next: /algo-strategy to build full backtest algorithm")
elif go_criteria and adf_p >= alpha:
    print("🟡 CAUTION - Signal correlates but is non-stationary.")
    print("   Consider adding regime filter before backtesting.")
else:
    print("🔴 NO-GO - Insufficient statistical evidence.")
    print("   Archive hypothesis and formulate new one.")
```
