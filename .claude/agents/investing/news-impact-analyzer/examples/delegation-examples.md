# Delegation Examples

Patterns for orchestrator delegation to news-impact-analyzer.

## Basic Delegation

### Full Daily Analysis

```python
Task(news-impact-analyzer,
  "Analyze news impact for 2026-01-04.
   Return regime context, impact predictions, and scenarios.")
```

### Category-Filtered Analysis

```python
Task(news-impact-analyzer,
  "Analyze geopolitical risk events for 2026-01-04.
   Category filter: geopolitical. Minimum severity: 50.")
```

### Regime Status Only

```python
Task(news-impact-analyzer,
  "Get current market regime status.
   Date: 2026-01-04. Return regime_context only.")
```

## Integration Patterns

### With Risk Management Specialist

```python
# Step 1: Get news impact
news_result = Task(news-impact-analyzer,
  "Analyze news impact for today. Return composite metrics.")

# Step 2: Adjust position sizing based on MSI
if news_result.composite_metrics.msi_macro_shock_index > 60:
    Task(risk-management-specialist,
      f"Reduce position sizing. MSI elevated at {msi}. 
       Apply 0.7x multiplier to all new positions.")
```


### With Strategy Builder

```python
# Step 1: Check regime before strategy execution
regime = Task(news-impact-analyzer,
  "Get regime status for today. Return classification and multiplier.")

# Step 2: Adjust strategy based on regime
if regime.regime_context.classification == "risk_off":
    Task(strategy-builder,
      "Pause new long entries. Current regime: risk_off.
       Wait for regime shift to neutral before resuming.")
```

## Error Handling

### Handling Stale Data

```python
result = Task(news-impact-analyzer, "Analyze news impact for today.")

if result.status == "FAILURE":
    if result.failure_category == "regime_data_stale":
        # Use fallback VIX-only classification
        Task(news-impact-analyzer,
          "Analyze news impact. Use VIX-only regime fallback.")
    elif result.failure_category == "data_unavailable":
        # Skip analysis, log warning
        log.warning(f"News analysis unavailable: {result.error_details}")
```

### Handling No Events

```python
result = Task(news-impact-analyzer, 
  "Analyze news impact for 2026-01-04. Min severity: 40.")

if result.events_analyzed == 0:
    # Low-risk day, proceed with normal operations
    log.info("No significant risk events. Regime-only context available.")
    regime = result.regime_context
```

## Parallel Execution

### Multi-Day Analysis

```python
# Analyze last 5 days in parallel
results = parallel([
    Task(news-impact-analyzer, f"Analyze news for 2026-01-0{i}.")
    for i in range(1, 6)
])

# Aggregate trend
avg_msi = mean(r.composite_metrics.msi_macro_shock_index for r in results)
```
