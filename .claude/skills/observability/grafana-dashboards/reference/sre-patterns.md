# SRE Patterns Reference

Detailed implementation patterns for RED, USE, and Four Golden Signals frameworks.

## Table of Contents

- [RED Method Deep Dive](#red-method-deep-dive)
- [USE Method Deep Dive](#use-method-deep-dive)
- [Four Golden Signals Implementation](#four-golden-signals-implementation)
- [Signal-to-Noise Optimization](#signal-to-noise-optimization)
- [Threshold Configuration](#threshold-configuration)
- [Framework Selection Matrix](#framework-selection-matrix)
- [Panel JSON Snippets](#panel-json-snippets)

---

## RED Method Deep Dive

### Rate Queries

**Basic request rate**:
```promql
sum(rate(http_requests_total{service="$service"}[$__rate_interval]))
```

**Rate by endpoint**:
```promql
sum by (endpoint) (rate(http_requests_total{service="$service"}[$__rate_interval]))
```

**Rate by status code family**:
```promql
sum by (status_code) (rate(http_requests_total{service="$service"}[$__rate_interval]))
```

### Error Queries

**Error rate percentage**:
```promql
sum(rate(http_requests_total{service="$service", status=~"5.."}[$__rate_interval]))
/
sum(rate(http_requests_total{service="$service"}[$__rate_interval]))
* 100
```

**Error rate by type**:
```promql
sum by (status) (rate(http_requests_total{service="$service", status=~"5.."}[$__rate_interval]))
```

### Duration Queries

**Latency percentiles**:
```promql
histogram_quantile(0.50, sum by (le) (rate(http_request_duration_seconds_bucket{service="$service"}[$__rate_interval])))
histogram_quantile(0.95, sum by (le) (rate(http_request_duration_seconds_bucket{service="$service"}[$__rate_interval])))
histogram_quantile(0.99, sum by (le) (rate(http_request_duration_seconds_bucket{service="$service"}[$__rate_interval])))
```

**Latency for successful requests only**:
```promql
histogram_quantile(0.95, sum by (le) (rate(http_request_duration_seconds_bucket{service="$service", status!~"5.."}[$__rate_interval])))
```

---

## USE Method Deep Dive

### Utilization Queries

**CPU utilization**:
```promql
100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[$__rate_interval])) * 100)
```

**Memory utilization**:
```promql
(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100
```

**Disk utilization**:
```promql
(1 - (node_filesystem_avail_bytes / node_filesystem_size_bytes)) * 100
```

### Saturation Queries

**Load average (normalized)**:
```promql
node_load1 / count without (cpu, mode) (node_cpu_seconds_total{mode="idle"})
```

**Connection pool saturation**:
```promql
(db_pool_active_connections / db_pool_max_connections) * 100
```

**Queue depth**:
```promql
sum(queue_messages_ready{queue=~"$queue"})
```

### Error Queries (Resources)

**OOM kills**:
```promql
increase(node_vmstat_oom_kill[$__rate_interval])
```

**Disk I/O errors**:
```promql
rate(node_disk_io_time_weighted_seconds_total[$__rate_interval])
```

---

## Four Golden Signals Implementation

### Latency

Track percentiles separately for successful and failed requests:

```promql
# Success latency p95
histogram_quantile(0.95, sum by (le) (rate(http_request_duration_seconds_bucket{status!~"5.."}[$__rate_interval])))

# Error latency p95 (often faster than success - timeout vs slow success)
histogram_quantile(0.95, sum by (le) (rate(http_request_duration_seconds_bucket{status=~"5.."}[$__rate_interval])))
```

### Traffic

Total request volume with breakdown:

```promql
# Total traffic
sum(rate(http_requests_total[$__rate_interval]))

# Traffic by endpoint (top 10)
topk(10, sum by (endpoint) (rate(http_requests_total[$__rate_interval])))
```

### Errors

Error budget tracking:

```promql
# Current error rate
sum(rate(http_requests_total{status=~"5.."}[$__rate_interval])) / sum(rate(http_requests_total[$__rate_interval])) * 100

# Error budget remaining (assuming 99.9% SLO = 0.1% error budget)
0.1 - (sum(rate(http_requests_total{status=~"5.."}[$__rate_interval])) / sum(rate(http_requests_total[$__rate_interval])) * 100)
```

### Saturation

Combined resource pressure:

```promql
# CPU + Memory combined pressure (weighted average)
(avg(100 - (rate(node_cpu_seconds_total{mode="idle"}[$__rate_interval]) * 100)) * 0.5)
+
(avg((1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100) * 0.5)
```

---

## Signal-to-Noise Optimization

### Rate Interval Selection

| Interval | Use Case | Characteristics |
|----------|----------|-----------------|
| 1m | Real-time alerting | High sensitivity, more noise |
| 5m | Default dashboards | Balanced signal/noise |
| 15m | Trend analysis | Smooth curves, delayed signal |
| 1h | Capacity planning | Long-term patterns |

### Smoothing Techniques

**Moving average** (for noisy metrics):
```promql
avg_over_time(metric_name[5m])
```

**Percentile filtering** (remove outliers):
```promql
histogram_quantile(0.95, rate(metric_bucket[$__rate_interval]))
```

### Aggregation Strategy

| Cardinality | Strategy |
|-------------|----------|
| >100 series | Apply `topk(10, ...)` or aggregate labels |
| 10-100 series | Use table legend with filtering |
| <10 series | Full breakdown in visualization |

---

## Threshold Configuration

### SLO-Based Thresholds

| SLO Target | Green | Yellow | Red |
|------------|-------|--------|-----|
| 99.9% availability | <0.05% errors | 0.05-0.1% | >0.1% |
| 200ms p95 latency | <150ms | 150-200ms | >200ms |
| 70% resource utilization | <60% | 60-70% | >70% |

### Multi-Window Multi-Burn-Rate Alerting

**Fast-burn** (5 minute window):
- Detects rapid degradation
- Threshold: >14.4x burn rate (exhausts 30-day budget in 2 hours)

**Slow-burn** (1 hour window):
- Detects gradual erosion
- Threshold: >1x burn rate (on track to exhaust budget)

```promql
# Fast burn (5 minute window, 14.4x rate)
sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) > 14.4 * 0.001

# Slow burn (1 hour window, 1x rate)
sum(rate(http_requests_total{status=~"5.."}[1h])) / sum(rate(http_requests_total[1h])) > 0.001
```

---

## Framework Selection Matrix

| Monitoring Target | Framework | Rationale |
|-------------------|-----------|-----------|
| API endpoint | RED | Service-centric, user-facing |
| Database server | USE | Resource-centric, capacity |
| Kubernetes pod | USE | Container resources |
| Message queue | USE (Saturation) | Queue depth focus |
| Overall service health | Four Golden Signals | Comprehensive view |
| SLO dashboard | Four Golden Signals | Error budget tracking |

---

## Panel JSON Snippets

### Time Series with Thresholds

```json
{
  "type": "timeseries",
  "fieldConfig": {
    "defaults": {
      "thresholds": {
        "mode": "absolute",
        "steps": [
          {"color": "#009E73", "value": null},
          {"color": "#F0E442", "value": 70},
          {"color": "#D55E00", "value": 85}
        ]
      },
      "custom": {
        "lineWidth": 2,
        "fillOpacity": 10
      }
    }
  }
}
```

### Stat with Sparkline

```json
{
  "type": "stat",
  "options": {
    "graphMode": "area",
    "colorMode": "value",
    "textMode": "value_and_name"
  },
  "fieldConfig": {
    "defaults": {
      "thresholds": {
        "steps": [
          {"color": "#009E73", "value": null},
          {"color": "#F0E442", "value": 70},
          {"color": "#D55E00", "value": 90}
        ]
      }
    }
  }
}
```

### Gauge with Min/Max

```json
{
  "type": "gauge",
  "options": {
    "showThresholdLabels": true,
    "showThresholdMarkers": true
  },
  "fieldConfig": {
    "defaults": {
      "min": 0,
      "max": 100,
      "unit": "percent",
      "thresholds": {
        "steps": [
          {"color": "#009E73", "value": 0},
          {"color": "#F0E442", "value": 70},
          {"color": "#D55E00", "value": 85}
        ]
      }
    }
  }
}
```
