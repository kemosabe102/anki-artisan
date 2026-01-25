---
name: promql-queries
description: >
  Use this skill when constructing PromQL queries, selecting rate intervals,
  creating recording rules, or optimizing metric queries. Covers query patterns,
  label refinement, cardinality management, and Grafana variable syntax.
  Keywords: promql, prometheus, rate, recording rule, cardinality, metrics.
---

# PromQL Query Construction

Construct optimized PromQL queries with validated syntax, appropriate rate intervals, and cardinality-aware label selection.

## Reference Documentation

**Detailed Guides** (read when relevant):
- **Cardinality Management** → [reference/cardinality-management.md](reference/cardinality-management.md)

## Scripts

**Validation Tools**:
- **Validate Query** → `python scripts/validate_promql.py "your_query"`

## Quick Reference

### Rate Functions

| Function | Use Case | Example |
|----------|----------|---------|
| `rate()` | Per-second average over range | `rate(http_requests_total[5m])` |
| `irate()` | Instant rate (last 2 samples) | `irate(http_requests_total[5m])` |
| `increase()` | Total increase over range | `increase(http_requests_total[1h])` |
| `delta()` | Gauge difference over range | `delta(temperature[1h])` |
| `deriv()` | Per-second derivative (gauge) | `deriv(temperature[1h])` |

### Common Aggregations

```promql
# Sum by label
sum by (namespace) (rate(container_cpu_usage_seconds_total[5m]))

# Average across instances
avg without (instance) (node_memory_MemFree_bytes)

# Top 5 by value
topk(5, rate(http_requests_total[5m]))

# Quantile calculation
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
```

---

## Rate Interval Selection

| Context | Interval | Rationale |
|---------|----------|-----------|
| **Minimum** | 4x scrape_interval | Ensures at least 4 samples for accurate rate |
| **Standard** | 5m | Dashboard queries (15s scrape = 20 samples) |
| **Extended** | 1h+ | Long-term trend analysis, capacity planning |
| **Grafana** | `$__rate_interval` | Dynamic adjustment based on dashboard range |

### Scrape Interval Mapping

| scrape_interval | Minimum rate() | Recommended |
|-----------------|----------------|-------------|
| 15s | 1m | 2m-5m |
| 30s | 2m | 5m |
| 1m | 4m | 5m-10m |

**Grafana**: Always prefer `$__rate_interval` - it calculates optimal interval based on scrape_interval and query range.

---

## Query Construction Patterns

### Counter Metrics

Counters only increase (or reset). Always use `rate()` or `increase()`.

```promql
# Request rate per second
rate(http_requests_total{job="api"}[5m])

# Error rate percentage
sum(rate(http_requests_total{status=~"5.."}[5m])) 
/ sum(rate(http_requests_total[5m])) * 100
```

### Gauge Metrics

Gauges can increase or decrease. Use directly or with `avg_over_time()`.

```promql
# Memory usage percentage
(1 - node_memory_MemFree_bytes / node_memory_MemTotal_bytes) * 100
```

### Histogram Metrics

Use `histogram_quantile()` with `_bucket` suffix.

```promql
# 95th percentile latency by endpoint
histogram_quantile(0.95, 
  sum by (le, endpoint) (rate(http_request_duration_seconds_bucket[5m]))
)
```

---

## Recording Rule Thresholds

Create recording rules when ANY condition is met:

| Threshold | Condition |
|-----------|-----------|
| **Complexity** | >3 operators in query |
| **Execution** | >500ms query time |
| **Frequency** | >10 queries/min |

### Recording Rule Template

```yaml
groups:
  - name: request_metrics
    interval: 30s
    rules:
      - record: namespace:http_requests:rate5m
        expr: sum by (namespace) (rate(http_requests_total[5m]))
```

### Naming Convention: `level:metric:operations`

- **level**: Aggregation level (`namespace`, `cluster`, `job`)
- **metric**: Base metric name
- **operations**: Applied functions (`rate5m`, `ratio`)

---

## Cardinality Management

### Label Selection Hierarchy (Low to High)

```
1. namespace    (5-20 values)     <- Start here
2. service      (10-50 values)
3. job          (10-100 values)
4. endpoint     (50-200 values)
5. pod          (100-1000 values) <- Use sparingly
6. instance     (varies)          <- Avoid in aggregations
```

### Cardinality Warnings

| Series Count | Severity | Action |
|--------------|----------|--------|
| <1000 | OK | No action needed |
| 1000-10000 | Warning | Review label usage |
| >10000 | Critical | Reduce labels, use recording rules |

---

## OODA Clarifying Questions

Before constructing queries, clarify intent:

1. **What signal?** Alert threshold, trend, or comparison?
2. **What time period?** Real-time, historical, or offset comparison?
3. **What labels?** Which dimensions need breakdown?
4. **What aggregation?** Sum, average, rate, or percentile?

---

## Anti-Patterns

| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| `rate(metric[1m])` with 30s scrape | Too few samples | `rate(metric[2m])` minimum |
| `irate()` in alerts | Too volatile | Use `rate()` for stability |
| Raw counters in dashboards | Shows ever-increasing values | Always use `rate()` |
| `.*` regex on high-cardinality | Performance impact | Use specific label values |
| Missing `by` clause | Aggregates everything | Specify grouping explicitly |
| Hardcoded intervals in Grafana | Breaks at zoom levels | Use `$__rate_interval` |

### Common Syntax Errors

```promql
# WRONG: Missing range vector
rate(http_requests_total)

# CORRECT
rate(http_requests_total[5m])

# WRONG: rate() on gauge
rate(node_memory_MemFree_bytes[5m])

# CORRECT: Use avg_over_time() for gauges
avg_over_time(node_memory_MemFree_bytes[5m])
```

---

## Quick Reference Checklist

Before finalizing a query:

- [ ] Rate interval at least 4x scrape_interval (or `$__rate_interval`)
- [ ] Appropriate function for metric type (rate for counters, direct for gauges)
- [ ] Low-cardinality labels first in grouping
- [ ] Estimated series count <1000 (or has recording rule)
- [ ] Grafana variables used (`$namespace`, `$__rate_interval`)
- [ ] Syntax validated against Prometheus API

### Validation Commands

```bash
# Test query syntax
curl -g 'http://prometheus:9090/api/v1/query?query=rate(http_requests_total[5m])'

# Check cardinality
curl -g 'http://prometheus:9090/api/v1/query?query=count(http_requests_total)'
```
