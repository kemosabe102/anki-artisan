# Node Sizing Guide

*Decision tree for QuantConnect node selection based on algorithm memory requirements.*

---

## QC Node Tiers

| Node | Memory | CPU | Cost/Min | Monthly Cap (730 hrs) |
|------|--------|-----|----------|----------------------|
| S1 | 8 GB | 1 core | $0.01 | $438 |
| S2 | 16 GB | 2 cores | $0.02 | $876 |
| L1 | 32 GB | 4 cores | $0.04 | $1,752 |
| L2 | 64 GB | 8 cores | $0.08 | $3,504 |

### Memory Safety Margins

Always maintain 50% headroom for:
- GC overhead and memory fragmentation
- Peak usage during warmup
- Unexpected data spikes

| Node | Usable Memory | Safe Estimate Range |
|------|---------------|---------------------|
| S1 | 4 GB | < 4 GB estimated |
| S2 | 8 GB | 4-8 GB estimated |
| L1 | 16 GB | 8-16 GB estimated |
| L2 | 32 GB | 16-32 GB estimated |

---

## Node Selection Decision Tree

```
START: Calculate estimated memory
  │
  ├─ Estimate < 4 GB?
  │   └─ YES → S1 node (PROCEED)
  │   └─ NO ↓
  │
  ├─ Estimate < 8 GB?
  │   └─ YES → S2 node (WARN_MEDIUM)
  │   └─ NO ↓
  │
  ├─ Estimate < 16 GB?
  │   └─ YES → L1 node (WARN_HIGH)
  │   └─ NO ↓
  │
  ├─ Estimate < 32 GB?
  │   └─ YES → L2 node (WARN_CRITICAL)
  │   └─ NO ↓
  │
  └─ Estimate >= 32 GB?
      └─ BLOCK: Must optimize algorithm before running
```

---

## When to Optimize vs Scale Up

### Optimize First (Cost-Effective)

| Situation | Optimization | Memory Saved |
|-----------|--------------|--------------|
| Universe > 500 | Add CoarseFundamental filters | 50-90% |
| Minute resolution | Switch to hourly | 68% |
| Wide options chain | Narrow SetFilter | 80-99% |
| History() in OnData | Use RollingWindow | 95% |

### Scale Up (Time-Effective)

| Situation | Justification |
|-----------|---------------|
| Estimate only 10-20% over limit | Faster than refactoring |
| Research/exploration phase | Optimize after validation |
| Options strategies requiring chain depth | Optimization not possible |
| Tick data for HFT research | Resolution cannot change |

---

## Cost Considerations

### Cost Per Backtest Hour

| Node | 1 Hour | 10 Hours | 100 Hours |
|------|--------|----------|-----------|
| S1 | $0.60 | $6.00 | $60.00 |
| S2 | $1.20 | $12.00 | $120.00 |
| L1 | $2.40 | $24.00 | $240.00 |
| L2 | $4.80 | $48.00 | $480.00 |

### Break-Even Analysis

```
optimization_time_hours × your_hourly_rate 
vs
(larger_node_cost - smaller_node_cost) × expected_backtest_hours
```

**Example**: 
- 2 hours to optimize algorithm ($200 at $100/hr)
- 50 backtests expected, 30 min each = 25 hours
- S2 vs S1 difference: $0.01/min × 25 hrs × 60 = $15

Result: Don't optimize, use S2 (saves $185 vs optimization time).

---

## Multi-Algorithm Memory

When running multiple algorithms:

```
total_node_memory >= sum(algorithm_estimates) × 1.2
```

### Shared vs Isolated

| Deployment | Memory Model | Recommendation |
|------------|--------------|----------------|
| Single algorithm | Full node available | Use estimates directly |
| Multiple algorithms | Shared pool | Each algorithm < 25% node |
| Live + backtest | Competing | Separate node for backtest |

---

## Quick Reference Table

| Estimated Memory | Node | Status | Action |
|------------------|------|--------|--------|
| < 4 GB | S1 | PROCEED | Run backtest |
| 4-8 GB | S2 | WARN_MEDIUM | Consider optimization |
| 8-16 GB | L1 | WARN_HIGH | Recommend optimization |
| 16-32 GB | L2 | WARN_CRITICAL | Optimize or use L2 |
| > 32 GB | N/A | BLOCK | Must optimize |

