---
name: qc-memory-profiling
description: >
  Use this skill for QuantConnect backtest memory estimation and optimization.
  Analyzes algorithm specs for memory footprint before execution.
  Trigger keywords: memory estimate, QC memory, backtest memory, universe sizing,
  node selection, OOM prevention, memory optimization.
---

# QuantConnect Memory Profiling

*Pre-execution memory estimation with node selection and optimization guidance.*

## Table of Contents

1. [Quick Reference](#quick-reference)
2. [Memory Estimation Algorithm](#memory-estimation-algorithm)
3. [Decision Matrix](#decision-matrix)
4. [Anti-Patterns](#anti-patterns)
5. [Reference Documentation](#reference-documentation)

---



## Quick Reference

### Memory Formula

```
total_memory = base_memory + history_memory + options_memory + overhead
```

| Component | Formula |
|-----------|---------|
| Base Memory | `universe_size × asset_base_mb × resolution_factor` |
| History Memory | `universe_size × history_years × 2MB × resolution_factor` |
| Options Memory | `underlying_count × chain_depth × 0.5MB` |
| Overhead | `(base + history + options) × 0.15` |

### Resolution Factors

| Resolution | Factor | Rationale |
|------------|--------|-----------|
| Daily | 1.0x | Baseline - 252 bars/year |
| Hour | 2.5x | 6.5 hours × 252 = 1,638 bars/year |
| Minute | 8.0x | 390 min × 252 = 98,280 bars/year |
| Second | 50.0x | 23,400 sec × 252 = 5.9M bars/year |
| Tick | 200.0x | Variable, assume 4x second volume |

### Node Tiers

| Node | Memory | Cost/Min | Best For |
|------|--------|----------|----------|
| S1 | 8 GB | $0.01 | < 100 assets, daily resolution |
| S2 | 16 GB | $0.02 | < 500 assets, hourly resolution |
| L1 | 32 GB | $0.04 | < 1000 assets, minute resolution |
| L2 | 64 GB | $0.08 | Options, tick data, large universes |

---



## Memory Estimation Algorithm

### Step 1: Parse Algorithm for Memory Factors

Extract these variables from the algorithm code:

```python
# Key variables to identify
universe_size: int       # AddUniverse coarse/fine filter output size
resolution: str          # Resolution.Daily, .Hour, .Minute, .Second, .Tick
history_window: int      # History() or RollingWindow lookback period
options_enabled: bool    # AddOption() present
chain_depth: int         # SetFilter() strike/expiry range
warmup_period: int       # SetWarmUp() days
asset_types: list        # Equity, Forex, Crypto, Options
```

### Step 2: Calculate Component Memory

```python
def estimate_memory(
    universe_size: int,
    resolution: str,
    history_days: int,
    asset_type: str = "equity",
    options_underlyings: int = 0,
    chain_depth: int = 10,
    warmup_months: int = 0
) -> dict:
    # Asset base memory (MB)
    asset_base = {
        "equity": 7.5,      # 5-10 MB average
        "forex": 4.0,       # 3-5 MB average  
        "crypto": 6.0,      # 4-8 MB average
        "options": 22.5     # 15-30 MB per underlying
    }
    
    # Resolution multipliers
    resolution_factor = {
        "daily": 1.0,
        "hour": 2.5,
        "minute": 8.0,
        "second": 50.0,
        "tick": 200.0
    }
    
    res_mult = resolution_factor.get(resolution.lower(), 1.0)
    base_mb = asset_base.get(asset_type.lower(), 7.5)
    
    # Calculate components
    base_memory = universe_size * base_mb * res_mult
    history_years = history_days / 365
    history_memory = universe_size * history_years * 2.0 * res_mult
    options_memory = options_underlyings * chain_depth * 0.5
    
    subtotal = base_memory + history_memory + options_memory
    warmup_overhead = subtotal * (warmup_months * 0.10)
    overhead = subtotal * 0.15
    
    total_mb = subtotal + warmup_overhead + overhead
    total_gb = total_mb / 1024
    
    return {
        "base_memory_mb": base_memory,
        "history_memory_mb": history_memory,
        "options_memory_mb": options_memory,
        "overhead_mb": overhead + warmup_overhead,
        "total_gb": total_gb
    }
```

### Step 3: Select Node and Status

```python
def get_recommendation(total_gb: float) -> tuple[str, str]:
    if total_gb < 4:
        return "S1", "PROCEED"
    elif total_gb < 8:
        return "S2", "WARN_MEDIUM"
    elif total_gb < 16:
        return "L1", "WARN_HIGH"
    else:
        return "L2", "WARN_CRITICAL"
```

---



## Decision Matrix

| Estimated Memory | Recommended Node | Status | Action |
|------------------|------------------|--------|--------|
| < 4 GB | S1 (8 GB) | PROCEED | Run backtest, 50% headroom |
| 4-8 GB | S2 (16 GB) | WARN_MEDIUM | Review history windows, consider optimization |
| 8-16 GB | L1 (32 GB) | WARN_HIGH | Recommend universe reduction or resolution downgrade |
| > 16 GB | L2 (64 GB) | WARN_CRITICAL | Must optimize before running, risk of OOM |

### Status Actions

| Status | User Guidance |
|--------|---------------|
| PROCEED | Safe to run. Memory estimate within comfortable node limits. |
| WARN_MEDIUM | Review algorithm for unnecessary history depth. Consider daily resolution. |
| WARN_HIGH | Reduce universe size or use CoarseFundamental filters. Drop resolution tier. |
| WARN_CRITICAL | Algorithm requires redesign. See optimization patterns in reference docs. |

---


## Anti-Patterns

| Anti-Pattern | Problem | Memory Impact | Correct Approach |
|--------------|---------|---------------|------------------|
| `History(symbol, 1000, Resolution.Minute)` | Massive per-symbol buffers | 8x per call | Use RollingWindow with Updates |
| Unfiltered `AddUniverse(coarse)` | 8000+ symbols subscribed | 60+ GB | Apply `.Where()` filters |
| `SetFilter(-50, 50, -180, 180)` for options | Excessive chain depth | 50+ MB/underlying | Use `-5, 5, 0, 30` focused filters |
| Multiple `History()` calls per OnData | Repeated memory allocation | Compounds each bar | Cache in Initialize() |
| No `RemoveSecurity()` for rotations | Zombie subscriptions | Accumulates forever | Clean up monthly |
| Tick resolution for large universe | Exponential memory growth | 200x multiplier | Use consolidated minute bars |

---



## Reference Documentation

Detailed guides for specific memory scenarios:

| Topic | Reference File |
|-------|----------------|
| Memory estimation formulas | [reference/memory-estimation-formulas.md](reference/memory-estimation-formulas.md) |
| Optimization patterns | [reference/optimization-patterns.md](reference/optimization-patterns.md) |
| Node sizing guide | [reference/node-sizing-guide.md](reference/node-sizing-guide.md) |

### Schema

Output format for memory estimates: [schemas/memory-estimate.schema.json](schemas/memory-estimate.schema.json)

### Usage Examples

Invocation patterns: [examples/usage-examples.md](examples/usage-examples.md)

---

## Quick Estimation Table

For rapid estimates without full calculation:

| Universe Size | Daily | Hourly | Minute | Second |
|---------------|-------|--------|--------|--------|
| 50 assets | 0.4 GB | 1.0 GB | 3.2 GB | 20 GB |
| 100 assets | 0.8 GB | 2.0 GB | 6.4 GB | 40 GB |
| 500 assets | 4.0 GB | 10 GB | 32 GB | 200 GB |
| 1000 assets | 8.0 GB | 20 GB | 64 GB | 400 GB |

*Assumes 1-year history, equity assets, no options. Add 50% for options chains.*

---

## Validation Workflow

1. **Parse**: Extract universe size, resolution, history depth from algorithm
2. **Calculate**: Apply memory formula with component breakdown
3. **Compare**: Match total against node tiers
4. **Recommend**: Return node + status + optimizations if WARN
5. **Output**: Generate JSON per schema specification

