# Usage Examples

*Invocation patterns for the qc-memory-profiling skill.*

---

## Example 1: Basic Memory Estimation

### User Request

> "Estimate memory for my algorithm that trades 200 stocks at minute resolution with 1 year of history."

### Skill Output

```json
{
  "algorithm": "user-momentum-strategy",
  "estimated_memory_gb": 12.8,
  "breakdown": {
    "base_memory_mb": 12000,
    "history_memory_mb": 3200,
    "options_memory_mb": 0,
    "overhead_mb": 2280
  },
  "inputs": {
    "universe_size": 200,
    "resolution": "minute",
    "history_days": 365,
    "asset_type": "equity",
    "options_underlyings": 0,
    "chain_depth": 0,
    "warmup_months": 0
  },
  "recommended_node": "L1",
  "status": "WARN_HIGH",
  "optimizations": [
    "Consider hourly resolution (reduces to ~3.2 GB)",
    "Reduce universe to 100 stocks (reduces to ~6.4 GB)",
    "Use RollingWindow instead of History() calls"
  ],
  "timestamp": "2025-01-16T10:30:00Z"
}
```

### Interpretation

Memory estimate of 12.8 GB requires L1 node (32 GB). Status WARN_HIGH indicates optimization is recommended. Three suggestions provided to reduce memory.

---


## Example 2: Options Strategy Estimation

### User Request

> "I'm trading SPY options with SetFilter(-10, 10, 0, 60). Estimate memory."

### Skill Output

```json
{
  "algorithm": "spy-options-strategy",
  "estimated_memory_gb": 0.45,
  "breakdown": {
    "base_memory_mb": 22.5,
    "history_memory_mb": 0,
    "options_memory_mb": 168,
    "overhead_mb": 28.6
  },
  "inputs": {
    "universe_size": 1,
    "resolution": "minute",
    "history_days": 0,
    "asset_type": "options",
    "options_underlyings": 1,
    "chain_depth": 336,
    "warmup_months": 0
  },
  "recommended_node": "S1",
  "status": "PROCEED",
  "optimizations": [],
  "timestamp": "2025-01-16T10:35:00Z"
}
```

### Chain Depth Calculation

```
SetFilter(-10, 10, 0, 60)
= 21 strikes × 8 weeks × 2 (puts+calls)
= 336 contracts
```

Memory is well under S1 limits. PROCEED status indicates safe to run.

---

## Example 3: Large Universe with Optimization Recommendations

### User Request

> "Analyze memory for 1000 stock universe, minute data, 2 years history, 3 month warmup."

### Skill Output

```json
{
  "algorithm": "large-universe-backtest",
  "estimated_memory_gb": 89.7,
  "breakdown": {
    "base_memory_mb": 60000,
    "history_memory_mb": 32000,
    "options_memory_mb": 0,
    "overhead_mb": 41600
  },
  "inputs": {
    "universe_size": 1000,
    "resolution": "minute",
    "history_days": 730,
    "asset_type": "equity",
    "options_underlyings": 0,
    "chain_depth": 0,
    "warmup_months": 3
  },
  "recommended_node": "L2",
  "status": "WARN_CRITICAL",
  "optimizations": [
    "CRITICAL: Estimated 89.7 GB exceeds L2 capacity (64 GB)",
    "Reduce universe to 500 stocks (45 GB - fits L2)",
    "Switch to hourly resolution (11.2 GB - fits L1)",
    "Reduce history to 1 year (44.8 GB - fits L2)",
    "Combine: 500 stocks + hourly = 5.6 GB (fits S2)"
  ],
  "timestamp": "2025-01-16T10:40:00Z"
}
```

### Interpretation

WARN_CRITICAL status means algorithm cannot run without optimization. Multiple optimization paths provided with resulting memory estimates.

---

## Example 4: Tier Context from Backtester

### Integration with Backtester Agent

When backtester agent parses tier context, it can invoke this skill:

```python
# Backtester extracts from tier context
tier_params = {
    "universe_size": 100,
    "resolution": "daily",
    "history_days": 252,
    "asset_type": "equity"
}

# Skill returns estimate
result = qc_memory_profiling.estimate(**tier_params)

# Backtester uses for node selection
if result["status"] == "PROCEED":
    node = result["recommended_node"]  # "S1"
elif result["status"] in ["WARN_HIGH", "WARN_CRITICAL"]:
    # Present optimizations to user before proceeding
    show_optimizations(result["optimizations"])
```

---

## Invocation Triggers

The skill activates on these keywords:

| Trigger Phrase | Example |
|----------------|---------|
| "memory estimate" | "Give me a memory estimate for this algorithm" |
| "QC memory" | "What's the QC memory requirement?" |
| "backtest memory" | "Check backtest memory before running" |
| "universe sizing" | "Help with universe sizing for memory" |
| "node selection" | "Which node should I use?" |
| "OOM prevention" | "Prevent OOM in my backtest" |
| "memory optimization" | "Optimize memory for this strategy" |

