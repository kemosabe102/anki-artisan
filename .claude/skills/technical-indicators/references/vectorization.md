# Vectorization Reference

Performance optimization patterns for technical indicator computation.

---

## Core Rule

**NO ROW-BY-ROW LOOPS** - Use vectorized operations exclusively.

---

## Vectorization Patterns

### Rolling Operations

```python
# BAD: Row-by-row loop
for i in range(len(df)):
    result[i] = df['close'].iloc[max(0,i-14):i+1].mean()

# GOOD: Vectorized rolling
result = df['close'].rolling(14).mean()
```

### Shift Operations

```python
# BAD: Manual indexing
for i in range(1, len(df)):
    result[i] = df['close'].iloc[i] - df['close'].iloc[i-1]

# GOOD: Vectorized shift
result = df['close'] - df['close'].shift(1)
```


### Cumulative Operations

```python
# BAD: Accumulator loop
total = 0
for i in range(len(df)):
    total += df['volume'].iloc[i]
    result[i] = total

# GOOD: Vectorized cumsum
result = df['volume'].cumsum()
```

---

## Performance Gains

| Operation | Loop Speed | Vectorized Speed | Speedup |
|-----------|-----------|------------------|---------|
| Rolling mean | 100ms/1K | 1ms/1K | 100x |
| Shift | 50ms/1K | 0.5ms/1K | 100x |
| Cumsum | 30ms/1K | 0.3ms/1K | 100x |

---

## Memory Management

### Float32 vs Float64

```python
# 50% memory reduction with <0.01% precision loss
df = df.astype('float32')
```


### Chunking Strategy

For datasets >200MB:

```python
chunk_size = len(df) // 4  # 4 chunks of ~50MB each
results = []
for i in range(0, len(df), chunk_size):
    chunk = df.iloc[i:i+chunk_size]
    results.append(compute_indicators(chunk))
final = pd.concat(results)
```

---

## SLA Targets

| Dataset Size | Max Latency | Memory Limit |
|--------------|-------------|--------------|
| 10K rows | 1 second | 200MB |
| 100K rows | 5 seconds | 200MB |
| 1M+ rows | 30 seconds | 200MB (chunked) |

---

## Avoid These Functions

| Function | Why Slow | Alternative |
|----------|----------|-------------|
| `df.apply()` | Python-level iteration | Vectorized equivalent |
| `df.iterrows()` | Creates Series per row | Boolean indexing |
| `for i in range(len(df))` | Pure Python loop | numpy/pandas native ops |


---

## Batch Computation

Compute multiple indicators in single pass:

```python
# GOOD: Batch computation
ema_20 = df['close'].ewm(span=20).mean()
rsi_14 = calculate_rsi(df['close'], 14)
atr_14 = calculate_atr(df['high'], df['low'], df['close'], 14)
```

Cache intermediate results:

```python
# EMA(T-1) needed for EMA(T) - cache it
ema_cache = {}
for period in [5, 10, 20, 50]:
    ema_cache[period] = df['close'].ewm(span=period).mean()
```
