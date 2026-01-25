# PromQL Cardinality Management

## Table of Contents

1. [Label Cardinality Fundamentals](#label-cardinality-fundamentals)
2. [Cardinality Thresholds](#cardinality-thresholds)
3. [Detection Methods](#detection-methods)
4. [Recording Rules for Optimization](#recording-rules-for-optimization)
5. [Time-Period Comparison Patterns](#time-period-comparison-patterns)
6. [Decision Trees](#decision-trees)
7. [Anti-Patterns](#anti-patterns)

---

## Label Cardinality Fundamentals

**Cardinality**: Number of unique time series created by combining label values.

### Classification

| Level | Unique Values | Examples | Risk |
|-------|---------------|----------|------|
| Low | <20 | status_code, http_method, region | Safe |
| Medium | 20-100 | pod_name, endpoint (coarse) | Monitor |
| High | >100 | user_id, request_id, ip_address | Dangerous |

### Why It Matters

- High cardinality (>10K series per metric) causes memory exhaustion
- Query performance degrades exponentially with series count
- Each series requires ~1-3KB memory

---

## Cardinality Thresholds

### Per-Metric Thresholds

| Threshold | Series Count | Action |
|-----------|--------------|--------|
| Acceptable | <1,000 | No action |
| Warning | 1,000-5,000 | Review label usage |
| Critical | >5,000 | Immediate remediation |

### System-Wide Thresholds

| Threshold | Total Series | Memory Impact |
|-----------|--------------|---------------|
| Healthy | <500K | ~2GB |
| Warning | 500K-1M | ~4GB |
| Critical | >1M | OOM risk |

---

## Detection Methods

### Audit Query (Top Offenders)

```promql
topk(20, count by (__name__)({__name__=~".+"}))
```

### Total Series Count

```promql
prometheus_tsdb_head_series
```

### Label Value Count

```promql
count(count by (label_name) ({namespace="prod"}[5m]))
```

### High-Cardinality Label Alert

```promql
count by (__name__)({__name__=~".+"}) > 1000
```

---

## Recording Rules for Optimization

### When to Create Recording Rules

- Query execution time >30 seconds
- Same aggregation used 3+ times
- Cardinality reduction >1000:1
- Critical SLO calculations

### Naming Convention

```
<level>:<metric>:<operations>
```

Examples:
- `job:http_requests:rate5m`
- `cluster:cpu_usage:avg5m`
- `instance:memory_usage:p95`

### Example Recording Rule

```yaml
groups:
  - name: api_performance
    interval: 60s
    rules:
      - record: job:http_request_duration_seconds:p95
        expr: histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (job, le))
```

### Evaluation Interval

**Rule**: ≥4x scrape_interval

- 15s scrape → 60s evaluation minimum
- Ensures sufficient data points for rate calculations

---

## Time-Period Comparison Patterns

### Offset Duration Selection

| Pattern | Offset | Use Case |
|---------|--------|----------|
| Hourly | 1h | Intraday anomalies |
| Daily | 24h | Day-over-day comparison |
| Weekly | 7d (168h) | Weekly seasonality |
| Monthly | 30d (720h) | Long-term trends |

### Basic Offset Query

```promql
# Current vs 7 days ago
rate(http_requests_total[5m])
rate(http_requests_total[5m] offset 7d)
```

### Percentage Change with Zero-Fill

```promql
(
  rate(metric[5m]) -
  (rate(metric[5m] offset 7d) or vector(0))
) /
(rate(metric[5m] offset 7d) or vector(1)) * 100
```

### Deviation Alert (>30% drop)

```promql
(
  (
    sum(rate(http_requests_total[5m] offset 7d)) -
    sum(rate(http_requests_total[5m]))
  ) /
  sum(rate(http_requests_total[5m] offset 7d))
) > 0.3
```

---

## Decision Trees

### Label Retention vs Removal

```
IF unbounded cardinality (user_id, session_id, uuid)
  → REMOVE from labels, move to logs/exemplars

ELSE IF bounded but >100 values (product_id)
  IF used in <3 dashboards AND no critical alerts
    → REMOVE, aggregate to higher level
  ELSE
    → KEEP but create recording rule

ELSE IF low cardinality (<10 values)
  → KEEP label
```

### Offset Duration Selection

```
IF comparing hourly patterns
  → offset 1h

ELSE IF daily patterns (business hours)
  → offset 24h

ELSE IF weekly seasonality (weekday/weekend)
  → offset 7d

ELSE IF monthly trends
  → offset 30d

ELSE (unknown seasonality)
  → Analyze autocorrelation first
```

---

## Anti-Patterns

### Anti-Pattern 1: Unbounded Labels

```promql
# ❌ BAD: Creates series per user
http_requests_total{user_id="12345"}

# ✅ GOOD: Aggregate, log user_id separately
http_requests_total{endpoint="/api/data", status_code="200"}
```

### Anti-Pattern 2: Over-Creating Recording Rules

```yaml
# ❌ BAD: Trivial query doesn't need recording rule
- record: job:up:sum
  expr: sum(up) by (job)

# ✅ GOOD: Only for complex/expensive queries
- record: job:http_request_duration_seconds:p95
  expr: histogram_quantile(0.95, sum(rate(...)) by (job, le))
```

### Anti-Pattern 3: Wrong Offset Duration

```promql
# ❌ BAD: 24h offset fires every weekend
(rate(metric[5m]) - rate(metric[5m] offset 24h)) / rate(metric[5m] offset 24h)

# ✅ GOOD: 7d offset accounts for weekly seasonality
(rate(metric[5m]) - rate(metric[5m] offset 7d)) / rate(metric[5m] offset 7d)
```

### Anti-Pattern 4: Missing Zero-Fill

```promql
# ❌ BAD: Fails with "No data" if baseline missing
(rate(metric[5m]) - rate(metric[5m] offset 7d)) / rate(metric[5m] offset 7d)

# ✅ GOOD: Zero-fills missing baseline
(
  rate(metric[5m]) -
  (rate(metric[5m] offset 7d) or vector(0))
) /
(rate(metric[5m] offset 7d) or vector(1))
```

---

## Common Pitfalls & Solutions

| Pitfall | Solution |
|---------|----------|
| High-cardinality user_id labels | Remove from labels, use logs/exemplars |
| Recording rule evaluation lag | Increase interval or simplify expression |
| Offset comparison missing data | Add `or vector(0)` for zero-fill |
| Wrong offset duration | Analyze traffic autocorrelation first |
| Division by zero | Add `or vector(1)` to denominator |

---

## Sources

- Prometheus Best Practices: https://prometheus.io/docs/practices/naming/
- Recording Rules: https://prometheus.io/docs/prometheus/latest/configuration/recording_rules/
- Robust Perception Blog: https://www.robustperception.io/cardinality-is-key
