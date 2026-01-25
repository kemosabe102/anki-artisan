# SRE Monitoring Frameworks

Reference guide for SRE monitoring patterns and their Grafana dashboard implementations.

---

## Intent-to-Framework Mapping

| Intent Keywords | Framework | Primary Signals |
|----------------|-----------|-----------------|
| "latency", "response time", "duration" | RED (Duration) | Histogram percentiles (p50/p95/p99) |
| "errors", "failures", "5xx" | RED (Errors) | Error rate percentage |
| "traffic", "requests", "throughput" | RED (Rate) | Requests per second |
| "CPU", "memory", "disk" | USE (Utilization) | Resource percentage |
| "queue", "pool", "wait" | USE (Saturation) | Queue depth, wait time |
| "OOM", "disk full", "network drop" | USE (Errors) | Resource-specific errors |
| "availability", "uptime", "SLO" | Golden Signals | Composite (all 4 signals) |

---

## Four Golden Signals (Google SRE)

**Principle**: Display ALL service health signals on ONE PAGE for temporal correlation.

### Layout Structure
```
Row 1 (y=0, h=6): [Service] Health - KPI Overview
  Panel 1 (x=0, w=6):  Request Rate (stat + sparkline)
  Panel 2 (x=6, w=6):  Error Rate % (stat + threshold)
  Panel 3 (x=12, w=6): Latency p95 (stat + sparkline)
  Panel 4 (x=18, w=6): Saturation % (gauge)

Row 2 (y=6, h=8): [Service] Trends - Temporal Correlation
  Panel 5 (x=0, w=12):  Request/Error Rate (2 series, shared Y)
  Panel 6 (x=12, w=12): Latency Percentiles (p50, p90, p99)

Row 3 (y=14, h=8): [Service] Saturation Detail
  Panel 7-9 (x=0/8/16, w=8): CPU%, Memory%, Queue Depth
```

### Critical Insight
**Track latency separately for successful vs failed requests**: "Slow error is worse than fast error"
```promql
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{status!~"5.."}[5m]))
```

---

## RED Method (Service-Centric)

**RED = Rate, Errors, Duration** - Use for APIs, microservices, web applications.

### Two-Column Layout
```
Left Column (w=12): Rate & Errors
  Panel 1 (y=0, h=8):  Request Rate Trend (timeseries)
  Panel 2 (y=8, h=6):  Error Rate % (stat + threshold)
  Panel 3 (y=14, h=10): Error Count by Type (bar chart: 4xx vs 5xx)

Right Column (w=12): Duration
  Panel 4 (y=0, h=6):  Latency p95 (stat + sparkline)
  Panel 5 (y=6, h=12): Latency Percentiles (timeseries: p50/p95/p99)
  Panel 6 (y=18, h=10): Latency Histogram (heatmap)
```

### PromQL Patterns
```promql
# Rate: Requests per second
sum(rate(http_requests_total[5m])) by (service)

# Errors: Error percentage
sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) * 100

# Duration: Latency percentiles
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service))
```

---

## USE Method (Resource-Centric)

**USE = Utilization, Saturation, Errors** - Use for infrastructure (servers, containers, databases).

### Three-Column Layout
```
Left (w=8): Utilization
  Panel 1-3 (y=0/8/16, h=8): CPU%, Memory%, Disk% (gauges)
  Panel 4 (y=24, w=24): Network Utilization Trend

Center (w=8): Saturation
  Panel 5 (y=0, h=8): Load Average (stat: 1/5/15 min)
  Panel 6 (y=8, h=16): Queue Depth Over Time

Right (w=8): Errors
  Panel 7-9 (y=0/8/16, h=8): Hardware Errors, OOM Kills, Disk I/O Errors
```

### PromQL Patterns
```promql
# Utilization: Resource percentage
(1 - avg(rate(node_cpu_seconds_total{mode="idle"}[5m]))) * 100

# Saturation: Queue depth / capacity
redis_connected_clients / redis_connected_clients_max * 100

# Errors: Resource-specific
rate(node_disk_io_time_seconds_total[5m])
```

---

## Threshold-SLO Integration

### Example: 99.9% SLO Configuration
```json
{
  "thresholds": {
    "steps": [
      {"color": "#D55E00", "value": 0},      // Red: SLO breach
      {"color": "#F0E442", "value": 90},     // Yellow: 90% budget consumed
      {"color": "#009E73", "value": 99.9}    // Green: Meeting SLO
    ]
  }
}
```

### Error Budget Formula
```
Error Budget = 100% - SLO Target = 0.1% (for 99.9% SLO)
Allowed Downtime = 43 minutes per 30 days
```

### Multi-Window Multi-Burn-Rate Alerting
- **Fast-burn (5 min)**: <99.9% for 5 consecutive minutes (catches outages)
- **Slow-burn (1 hour)**: <99.95% over 1h rolling average (catches degradation)

---

## Signal vs Noise Optimization

### Rate Interval Selection
| Interval | Use Case | Sensitivity |
|----------|----------|-------------|
| 1m | Tactical, real-time | High (noisy) |
| 5m | Balanced, default | Medium |
| 1h | Strategic, trends | Low (smooth) |

### High-Cardinality Reduction
```promql
# Before (1000s of series)
rate(http_requests_total[5m])

# After (10s of series)
sum(rate(http_requests_total[5m])) by (service, status)

# Or: Top 10 only
topk(10, sum(rate(http_requests_total[5m])) by (service))
```

### Aggregation Strategy
- **High cardinality (>100 series)**: Apply `topk(10, ...)` or summarize by fewer labels
- **Low cardinality (<10 series)**: Full breakdown, detailed visualization
- **Alert-worthy signals**: Separate panel with clear thresholds

---

## Panel Type Decision by Framework

| Framework | Signal | Panel Type | Configuration |
|-----------|--------|------------|---------------|
| RED | Rate | Time Series | Line, 5m rate interval |
| RED | Errors | Stat | Percentage, threshold colors |
| RED | Duration | Time Series | Multiple percentiles (p50/p95/p99) |
| USE | Utilization | Gauge | 0-100%, threshold markers |
| USE | Saturation | Time Series | Queue depth over time |
| USE | Errors | Stat | Count with sparkline |
| Golden | All 4 | Mixed | Row of stats + row of trends |

---

## ConfigMap Template

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: grafana-dashboard-<name>
  namespace: observability
  labels:
    grafana_dashboard: '1'  # Required for sidecar detection
data:
  <name>.json: |
    {"dashboard": {...}, "folderId": null, "overwrite": true}
```

---

## References

- [Google SRE Book - Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/)
- [RED Method](https://grafana.com/blog/2018/08/02/the-red-method-how-to-instrument-your-services/)
- [USE Method](http://www.brendangregg.com/usemethod.html)
