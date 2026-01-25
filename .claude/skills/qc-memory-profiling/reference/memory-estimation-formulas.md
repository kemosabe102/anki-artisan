# Memory Estimation Formulas

*Detailed breakdown of QuantConnect memory consumption patterns.*

---

## Base Memory Per Asset Type

Each subscribed security consumes base memory for metadata, price history buffers, and algorithm state.

| Asset Type | Base Memory (MB) | Range | Notes |
|------------|------------------|-------|-------|
| Equity | 5-10 MB | 7.5 avg | OHLCV + fundamentals |
| Forex | 3-5 MB | 4.0 avg | Bid/ask spreads, no volume |
| Crypto | 4-8 MB | 6.0 avg | Higher tick frequency |
| Options | 15-30 MB | 22.5 avg | Per underlying, chain metadata |
| Futures | 8-15 MB | 11.5 avg | Contract specifications |
| CFD | 4-6 MB | 5.0 avg | Derivative pricing |

### Why Options Are Expensive

Options memory scales with chain complexity:
- Each underlying has multiple expirations
- Each expiration has multiple strikes (puts + calls)
- Greeks calculated per contract
- **Formula**: `underlying_base + (active_contracts × 0.5MB)`

---

## Resolution Multipliers

Resolution determines bar count and thus memory for history buffers.

| Resolution | Multiplier | Bars/Year | Rationale |
|------------|------------|-----------|-----------|
| Daily | 1.0x | 252 | Trading days only |
| Hour | 2.5x | 1,638 | 6.5 hours × 252 days |
| Minute | 8.0x | 98,280 | 390 minutes × 252 days |
| Second | 50.0x | 5,896,800 | 23,400 seconds × 252 days |
| Tick | 200.0x | Variable | Highly asset-dependent, ~4x second |



### Resolution Selection Guidelines

```
IF universe_size > 500 AND resolution == "minute":
    WARN: Consider hourly resolution (8x memory reduction)
    
IF universe_size > 100 AND resolution == "second":
    BLOCK: Memory will exceed L2 node capacity
    
IF resolution == "tick" AND universe_size > 20:
    BLOCK: Tick data infeasible for broad universes
```

---

## History Buffer Calculations

History windows are the largest memory consumer for most algorithms.

### Formula

```
history_memory_mb = universe_size × history_years × 2MB × resolution_factor
```

### Component Breakdown

| History Call | Memory Per Asset/Year | With Resolution Factor |
|--------------|----------------------|------------------------|
| `History(symbol, 252, Resolution.Daily)` | 2 MB | 2 MB |
| `History(symbol, 252, Resolution.Hour)` | 2 MB | 5 MB |
| `History(symbol, 252, Resolution.Minute)` | 2 MB | 16 MB |

### Why 2 MB/Year Baseline?

- OHLCV data: 5 floats × 8 bytes = 40 bytes/bar
- Daily bars: 252 bars × 40 bytes = 10 KB/year raw
- DataFrame overhead: Index, dtypes, pandas internals = ~100x
- Safety margin: 2 MB accounts for peak usage and fragmentation

---

## Options Chain Memory Modeling

Options chains require specialized memory modeling due to their complexity.


### Chain Memory Formula

```
options_memory_mb = underlying_count × chain_depth × 0.5MB
```

### Chain Depth Calculation

Chain depth = number of active contracts per underlying:

```python
# SetFilter parameters determine chain size
def calculate_chain_depth(
    min_strike: int, max_strike: int,
    min_expiry: int, max_expiry: int
) -> int:
    strike_range = max_strike - min_strike + 1  # ITM to OTM
    expiry_count = (max_expiry - min_expiry) // 7  # Weekly expirations
    contracts = strike_range * expiry_count * 2  # Puts + Calls
    return contracts

# Example: SetFilter(-10, 10, 0, 60)
# = 21 strikes × 8 weeks × 2 = 336 contracts
# Memory: 336 × 0.5MB = 168 MB per underlying
```

### Typical Chain Sizes

| Filter Configuration | Chain Depth | Memory/Underlying |
|---------------------|-------------|-------------------|
| `SetFilter(-5, 5, 0, 30)` | ~80 contracts | 40 MB |
| `SetFilter(-10, 10, 0, 60)` | ~336 contracts | 168 MB |
| `SetFilter(-20, 20, 0, 90)` | ~1,100 contracts | 550 MB |
| `SetFilter(-50, 50, -180, 180)` | ~10,000 contracts | 5 GB |

---

## Warmup Period Impact

Warmup periods pre-load historical data, adding to initial memory footprint.

### Formula

```
warmup_overhead = base_memory × (warmup_months × 0.10)
```

### Rationale

- 1 month warmup: +10% memory overhead
- 3 month warmup: +30% memory overhead
- 12 month warmup: +120% memory overhead (doubles memory)

Warmup data is released after initialization, but peak memory occurs during warmup phase.

---

## Complete Memory Formula

```python
def total_memory_gb(
    universe_size: int,
    resolution: str,
    history_days: int,
    asset_type: str,
    options_underlyings: int,
    chain_depth: int,
    warmup_months: int
) -> float:
    # Constants
    ASSET_BASE_MB = {"equity": 7.5, "forex": 4.0, "crypto": 6.0, "options": 22.5}
    RES_FACTOR = {"daily": 1.0, "hour": 2.5, "minute": 8.0, "second": 50.0, "tick": 200.0}
    
    rf = RES_FACTOR.get(resolution.lower(), 1.0)
    ab = ASSET_BASE_MB.get(asset_type.lower(), 7.5)
    
    base = universe_size * ab * rf
    history = universe_size * (history_days / 365) * 2.0 * rf
    options = options_underlyings * chain_depth * 0.5
    
    subtotal = base + history + options
    warmup = subtotal * (warmup_months * 0.10)
    overhead = subtotal * 0.15
    
    return (subtotal + warmup + overhead) / 1024
```

