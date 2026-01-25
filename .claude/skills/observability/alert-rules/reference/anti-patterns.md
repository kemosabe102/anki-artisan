# Alert Rule Anti-Patterns

Detailed explanations of the top 10 anti-patterns in Prometheus alerting.

## Table of Contents

- [1. Missing `for` Clause](#1-missing-for-clause)
- [2. Using `irate()` in Alert Expressions](#2-using-irate-in-alert-expressions)
- [3. High-Cardinality Labels](#3-high-cardinality-labels)
- [4. Absolute Thresholds](#4-absolute-thresholds)
- [5. Alerting on Every Error](#5-alerting-on-every-error)
- [6. Missing Severity Labels](#6-missing-severity-labels)
- [7. No Annotations](#7-no-annotations)
- [8. Mixing 4xx and 5xx Errors](#8-mixing-4xx-and-5xx-errors)
- [9. No Minimum Traffic Threshold](#9-no-minimum-traffic-threshold)
- [10. Alerting on Causes Instead of Symptoms](#10-alerting-on-causes-instead-of-symptoms)

---

## 1. Missing `for` Clause

**Problem**: Alerts fire on every transient spike, causing flapping and alert fatigue.

**Bad Example**:
```yaml
- alert: HighCPU
  expr: cpu_usage > 0.85
  # No 'for' clause - fires immediately on any spike
```

**Good Example**:
```yaml
- alert: HighCPU
  expr: cpu_usage > 0.85
  for: 10m  # Only fires if sustained for 10 minutes
```

**Rationale**: Most infrastructure metrics experience brief spikes that self-resolve. The `for` clause filters these transients.

---

## 2. Using `irate()` in Alert Expressions

**Problem**: `irate()` calculates instantaneous rate from the last two data points, making it extremely volatile and unsuitable for alerting.

**Bad Example**:
```yaml
- alert: HighErrorRate
  expr: irate(http_errors_total[1m]) > 10
```

**Good Example**:
```yaml
- alert: HighErrorRate
  expr: rate(http_errors_total[5m]) > 10
```

**Rationale**: `rate()` smooths over the entire range, providing stable values. Use `irate()` only for graphing where you want to see spikes.

---

## 3. High-Cardinality Labels

**Problem**: Labels like `$value`, `request_id`, or `user_id` create unique time series for each value, causing memory explosion and alert storms.

**Bad Example**:
```yaml
annotations:
  summary: "Error for user {{ $labels.user_id }}: {{ $value }}"
```

**Good Example**:
```yaml
annotations:
  summary: "Error rate: {{ $value | printf \"%.2f\" }}%"
  description: "Check logs for user-specific details"
```

**Rationale**: Prometheus stores each unique label combination as a separate time series. High-cardinality labels can crash Prometheus.

---

## 4. Absolute Thresholds

**Problem**: Fixed thresholds don't scale with traffic. `> 100 errors` might be critical for 1000 requests but noise for 1M requests.

**Bad Example**:
```yaml
- alert: HighErrors
  expr: sum(rate(errors_total[5m])) > 100
```

**Good Example**:
```yaml
- alert: HighErrors
  expr: |
    sum(rate(errors_total[5m])) 
    / 
    sum(rate(requests_total[5m])) > 0.01
```

**Rationale**: Percentage-based thresholds automatically scale with traffic volume.

---

## 5. Alerting on Every Error

**Problem**: Alerting on raw error counts without context creates noise. Some errors are expected (client errors, retries).

**Bad Example**:
```yaml
- alert: ErrorOccurred
  expr: increase(errors_total[1m]) > 0
```

**Good Example**:
```yaml
- alert: HighErrorRate
  expr: |
    sum(rate(errors_total{type="server"}[5m])) 
    / 
    sum(rate(requests_total[5m])) > 0.01
    and
    sum(rate(requests_total[5m])) > 100  # Minimum traffic
```

**Rationale**: Consider error rate relative to total volume, filter by error type, and require minimum traffic.

---

## 6. Missing Severity Labels

**Problem**: Without severity labels, alerts cannot be routed or prioritized. All alerts look equally important.

**Bad Example**:
```yaml
- alert: DiskFull
  expr: disk_free_percent < 10
```

**Good Example**:
```yaml
- alert: DiskFull
  expr: disk_free_percent < 10
  labels:
    severity: critical
    team: platform
```

**Rationale**: Alertmanager routes based on labels. Severity enables different notification channels and response times.

---

## 7. No Annotations

**Problem**: Responders receive alerts with no context about what's wrong, what to check, or how to remediate.

**Bad Example**:
```yaml
- alert: ServiceDown
  expr: up == 0
```

**Good Example**:
```yaml
- alert: ServiceDown
  expr: up == 0
  annotations:
    summary: "{{ $labels.job }} on {{ $labels.instance }} is down"
    description: |
      The service {{ $labels.job }} on instance {{ $labels.instance }} 
      has been unreachable for more than 5 minutes.
    runbook_url: "https://wiki.example.com/runbooks/service-down"
```

**Rationale**: Good annotations reduce MTTR by providing immediate context and remediation guidance.

---

## 8. Mixing 4xx and 5xx Errors

**Problem**: Client errors (4xx) and server errors (5xx) have different causes and ownership. Mixing them creates confusion.

**Bad Example**:
```yaml
- alert: HighHttpErrors
  expr: rate(http_requests_total{code=~"[45].."}[5m]) > 10
```

**Good Example**:
```yaml
# Server errors - platform team
- alert: HighServerErrors
  expr: rate(http_requests_total{code=~"5.."}[5m]) > 10
  labels:
    team: platform

# Client errors - may indicate API misuse
- alert: HighClientErrors  
  expr: rate(http_requests_total{code=~"4.."}[5m]) > 100
  labels:
    team: api
```

**Rationale**: 5xx errors indicate server issues requiring immediate attention. 4xx may indicate client problems or API documentation issues.

---

## 9. No Minimum Traffic Threshold

**Problem**: Low-traffic periods can trigger percentage-based alerts on just a few errors.

**Bad Example**:
```yaml
- alert: HighErrorRate
  expr: errors / requests > 0.05  # 1 error out of 10 requests = 10%!
```

**Good Example**:
```yaml
- alert: HighErrorRate
  expr: |
    errors / requests > 0.05
    and
    requests > 100  # Require minimum traffic
```

**Rationale**: Statistical significance requires sufficient sample size. Minimum traffic prevents low-volume noise.

---

## 10. Alerting on Causes Instead of Symptoms

**Problem**: Alerting on every potential cause (high CPU, memory, connections) results in multiple alerts for a single incident.

**Bad Example**:
```yaml
# All fire during same incident
- alert: HighCPU
- alert: HighMemory
- alert: HighConnections
- alert: SlowResponses
```

**Good Example**:
```yaml
# Alert on user-facing symptom
- alert: SlowResponses
  expr: histogram_quantile(0.99, rate(http_duration_seconds_bucket[5m])) > 1

# Causes as lower-severity or informational
- alert: HighCPU
  labels:
    severity: warning  # Lower severity, supporting info
```

**Rationale**: Alert on what users experience (symptoms). Use cause-based alerts as supporting information or lower severity.
