# Alert Threshold Guide

Comprehensive guidance for selecting appropriate thresholds for Prometheus alerts.

## Table of Contents

- [Threshold Selection Principles](#threshold-selection-principles)
- [Threshold Reference by Metric Type](#threshold-reference-by-metric-type)
- [For-Clause Selection Matrix](#for-clause-selection-matrix)
- [Multi-Tier Severity Strategy](#multi-tier-severity-strategy)
- [Environment-Specific Thresholds](#environment-specific-thresholds)
- [Threshold Tuning Process](#threshold-tuning-process)
- [SLO-Based Thresholds](#slo-based-thresholds)

---

## Threshold Selection Principles

### 1. Start Conservative, Tune Based on Data

Begin with industry-standard thresholds, then adjust based on:
- Historical firing data
- False positive rate
- Team feedback

### 2. Use Percentages Over Absolutes

| Absolute (Bad) | Percentage (Good) |
|----------------|-------------------|
| `errors > 100` | `errors / total > 0.01` |
| `latency > 500ms` | `quantile(0.99, latency) > 500ms` |
| `queue_depth > 1000` | `queue_depth / capacity > 0.8` |

### 3. Consider Baseline Variance

For metrics with natural variance (CPU, latency), threshold = baseline + (2-3 * standard deviation).

---

## Threshold Reference by Metric Type

### Infrastructure Metrics

| Metric | Warning | Critical | For Clause | Rationale |
|--------|---------|----------|------------|-----------|
| CPU utilization | >85% | >95% | 10-15m | Allow for burst handling |
| Memory utilization | >85% | >95% | 10m | Account for GC cycles |
| Disk space free | <20% | <10% | 30m | Slow to change |
| Disk I/O utilization | >80% | >95% | 15m | Filter burst I/O |
| Network utilization | >80% | >95% | 10m | Sustained saturation |

### Application Metrics

| Metric | Warning | Critical | For Clause | Rationale |
|--------|---------|----------|------------|-----------|
| Error rate (5xx) | >1% | >5% | 10m | User impact threshold |
| P50 latency | >200ms | >500ms | 10m | Typical user experience |
| P99 latency | >1s | >3s | 15m | Tail latency budget |
| Request rate drop | <50% baseline | <25% baseline | 5m | Traffic anomaly |
| Queue depth | >1000 items | >5000 items | 10m | Processing backlog |

### Database Metrics

| Metric | Warning | Critical | For Clause | Rationale |
|--------|---------|----------|------------|-----------|
| Connection utilization | >80% | >95% | 5m | Connection pool exhaustion |
| Replication lag | >1s | >10s | 5m | Data consistency |
| Lock wait time | >100ms | >1s | 5m | Contention issues |
| Query duration (P99) | >1s | >5s | 10m | Slow query impact |
| Cache hit ratio | <90% | <80% | 15m | Performance degradation |

### Kubernetes Metrics

| Metric | Warning | Critical | For Clause | Rationale |
|--------|---------|----------|------------|-----------|
| Pod restarts | >3/hour | >10/hour | 5m | Crash loops |
| Node CPU | >85% | >95% | 10m | Node saturation |
| Node memory | >85% | >95% | 10m | OOM risk |
| PVC utilization | >80% | >90% | 30m | Storage exhaustion |
| Pod pending time | >5m | >15m | 0m | Scheduling issues |

---

## For-Clause Selection Matrix

| Metric Characteristic | Recommended For | Examples |
|-----------------------|-----------------|----------|
| Highly volatile | 10-15m | CPU, latency spikes |
| Moderately stable | 5-10m | Error rates, throughput |
| Slow changing | 30m-1h | Disk usage, replication lag |
| Critical availability | 1-5m | Service up/down |
| Predictive alerts | 5m | Burn rate, linear prediction |

### For-Clause Anti-Patterns

| Bad Practice | Problem | Better Approach |
|--------------|---------|-----------------|
| No `for` clause | Fires on every transient | Add appropriate duration |
| `for: 1m` on volatile metric | Too sensitive | Increase to 5-15m |
| `for: 1h` on availability | Too slow to respond | Reduce to 1-5m |
| Same `for` for all alerts | One size doesn't fit all | Tune per metric type |

---

## Multi-Tier Severity Strategy

### Pattern: Warning + Critical

```yaml
# Warning: gives time to investigate
- alert: DiskSpaceLow
  expr: disk_free_percent < 20
  for: 30m
  labels:
    severity: warning

# Critical: immediate action required
- alert: DiskSpaceCritical
  expr: disk_free_percent < 10
  for: 15m
  labels:
    severity: critical
```

### Threshold Gaps

Ensure sufficient gap between warning and critical:
- Minimum 10% gap for percentage metrics
- Minimum 2x gap for rate metrics
- Critical should be "truly critical" (user impact imminent)

| Metric | Warning | Critical | Gap |
|--------|---------|----------|-----|
| CPU | 85% | 95% | 10% |
| Memory | 85% | 95% | 10% |
| Error rate | 1% | 5% | 4x |
| Latency | 1s | 3s | 3x |

---

## Environment-Specific Thresholds

### Production vs Non-Production

| Environment | Adjustment | Rationale |
|-------------|------------|-----------|
| Production | Baseline thresholds | User-facing, requires attention |
| Staging | 1.5x production | More tolerance for testing |
| Development | Disable or 2x | Avoid noise during development |

### Implementation

```yaml
# Production
- alert: HighCPU
  expr: |
    node_cpu_usage{environment="production"} > 0.85

# Staging - higher threshold
- alert: HighCPU
  expr: |
    node_cpu_usage{environment="staging"} > 0.95
```

---

## Threshold Tuning Process

### Step 1: Establish Baseline

```promql
# P50, P90, P99 over 7 days
histogram_quantile(0.50, sum(rate(metric_bucket[7d])) by (le))
histogram_quantile(0.90, sum(rate(metric_bucket[7d])) by (le))
histogram_quantile(0.99, sum(rate(metric_bucket[7d])) by (le))
```

### Step 2: Set Initial Threshold

Warning = P90 + margin (10-20%)
Critical = P99 + margin (10-20%)

### Step 3: Monitor False Positive Rate

Target: <5% false positive rate
If higher: increase threshold or `for` duration

### Step 4: Monitor Detection Rate

Ensure alerts fire before user complaints
If alerts fire too late: decrease threshold or `for` duration

### Step 5: Iterate

Review quarterly based on:
- Service changes
- Traffic patterns
- Team feedback

---

## SLO-Based Thresholds

For SLO-driven alerting, derive thresholds from error budgets:

| SLO | Monthly Error Budget | Burn Rate Threshold |
|-----|---------------------|---------------------|
| 99.9% | 43.2 minutes | Alert at 14.4x (2% budget/hour) |
| 99.5% | 3.6 hours | Alert at 6x (5% budget/hour) |
| 99.0% | 7.2 hours | Alert at 3x (10% budget/hour) |

### Burn Rate Formula

```
burn_rate = (actual_error_rate / error_budget_rate)
```

Alert when `burn_rate > threshold` sustained for `for` duration.
