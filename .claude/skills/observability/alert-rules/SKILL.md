---
name: alert-rules
description: >
  Use this skill when creating Prometheus alert rules, tuning noisy alerts,
  or reviewing alert configurations. Covers anti-patterns, threshold selection,
  for-clause rationale, severity matrix, and SLO-based alerting.
  Keywords: prometheus, alert, alerting, threshold, for clause, severity, SLO.
---

# Prometheus Alert Rules

Expert guidance for constructing, validating, and tuning Prometheus alert rules with optimal signal-to-noise ratio.

## Reference Documentation

**Detailed Guides** (read when relevant):
- **Anti-Patterns** → [reference/anti-patterns.md](reference/anti-patterns.md)
- **Threshold Guide** → [reference/threshold-guide.md](reference/threshold-guide.md)

## Scripts

**Validation Tools**:
- **Validate Alert Rules** → `python scripts/validate_alert_rules.py alerts.yaml`

---

## 5 Clarifying Questions

Before constructing any alert, ask:

| # | Question | Purpose |
|---|----------|---------|
| 1 | What user impact justifies this alert? | Distinguish symptoms from causes |
| 2 | What severity levels are needed? | Critical pages vs warning notifies |
| 3 | What `for` duration prevents false positives? | Filter transient spikes |
| 4 | What labels enable proper routing? | Team, service, environment |
| 5 | Does this need SLO-based burn rate alerting? | Error budget approach |

---

## Top 10 Anti-Patterns

Quick reference - see [reference/anti-patterns.md](reference/anti-patterns.md) for detailed explanations.

| # | Anti-Pattern | Problem | Fix |
|---|--------------|---------|-----|
| 1 | Missing `for` clause | Flapping on transient spikes | Add 5-15m based on metric |
| 2 | Using `irate()` | Too volatile for alerting | Use `rate()` instead |
| 3 | High-cardinality labels | Alert explosion, memory issues | Remove `$value`, `request_id` |
| 4 | Absolute thresholds | Don't scale with traffic | Use percentages |
| 5 | Alerting on every error | Noise drowns signal | Consider total volume |
| 6 | Missing severity labels | Cannot route or prioritize | Add severity: warning/critical |
| 7 | No annotations | Responders lack context | Add summary, description, runbook_url |
| 8 | Mixing 4xx and 5xx | Different ownership, causes | Separate into distinct alerts |
| 9 | No minimum traffic | Low-volume noise | Add `and rate(...) > threshold` |
| 10 | Alerting on causes | Multiple alerts per incident | Alert on user-facing symptoms |

---

## Threshold Quick Reference

| Metric Type | Warning | Critical | For Clause | Notes |
|-------------|---------|----------|------------|-------|
| CPU | >85% | >95% | 10-15m | Sustained, not transient |
| Memory | >85% | >95% | 10m | Allow for GC cycles |
| Disk | <20% free | <10% free | 30m | Slow to change |
| Error rate | >1% | >5% | 10m | Of total requests |
| P99 latency | >1s | >3s | 15m | User-perceivable impact |
| Pod restarts | >3/hour | >10/hour | 5m | Crash loops |
| Queue depth | >1000 | >5000 | 10m | Processing lag |

---

## For-Clause Selection Guide

The `for` clause duration should match metric behavior:

| Metric Behavior | Recommended For | Rationale |
|-----------------|-----------------|-----------|
| Volatile (CPU, latency) | 10-15m | Filters spikes |
| Stable (disk, queue) | 30m-1h | Slow to change |
| Critical (availability) | 1-5m | Fast response needed |
| Predictive (burn rate) | 5m-1h | Based on window |

**Decision Tree:**
1. Is downtime critical? → 1-5m
2. Is metric naturally volatile? → 10-15m
3. Does metric change slowly? → 30m-1h
4. Is it SLO burn rate? → Match burn rate window

---

## Severity Matrix

| Severity | Response Time | Notification | Use When |
|----------|---------------|--------------|----------|
| **critical** | Immediate | Page on-call | User-facing impact, data loss risk |
| **warning** | Next business day | Slack/email | Degraded performance, trending issues |
| **info** | As capacity | Dashboard only | Informational, no action needed |

**Multi-Tier Pattern:**
```yaml
# Warning tier
- alert: HighCPUWarning
  expr: instance:cpu_usage:rate5m > 0.85
  for: 10m
  labels:
    severity: warning

# Critical tier
- alert: HighCPUCritical
  expr: instance:cpu_usage:rate5m > 0.95
  for: 5m
  labels:
    severity: critical
```

---

## SLO-Based Alerting Patterns

### Burn Rate Alerting

For services with SLOs, alert on error budget consumption rate:

```yaml
# Fast burn: 14.4x burn rate over 1h (2% budget in 1h)
- alert: SLOFastBurn
  expr: |
    (
      sum(rate(http_requests_total{code=~"5.."}[1h]))
      /
      sum(rate(http_requests_total[1h]))
    ) > (14.4 * 0.001)  # 14.4x of 0.1% error budget
  for: 2m
  labels:
    severity: critical

# Slow burn: 3x burn rate over 6h
- alert: SLOSlowBurn
  expr: |
    (
      sum(rate(http_requests_total{code=~"5.."}[6h]))
      /
      sum(rate(http_requests_total[6h]))
    ) > (3 * 0.001)
  for: 15m
  labels:
    severity: warning
```

### Multi-Window Approach

| Window | Burn Rate | For Clause | Severity |
|--------|-----------|------------|----------|
| 1h | 14.4x | 2m | critical |
| 6h | 6x | 5m | critical |
| 3d | 1x | 30m | warning |

---

## Alert Tuning Workflow

When an alert is noisy or flapping, follow this 5-step process:

### Step 1: Analyze Firing Frequency
```promql
# Count fires per hour
count_over_time(ALERTS{alertname="YourAlert"}[1h])
```
- >10 fires/hour = flapping candidate

### Step 2: Check For Clause
- Missing? Add appropriate duration from threshold table
- Too short? Increase based on metric volatility

### Step 3: Evaluate Threshold
- Absolute → Convert to percentage
- Too sensitive → Increase by 10-20%
- Consider multi-tier (warning + critical)

### Step 4: Review Function
- `irate()` → Replace with `rate()`
- Short range `[1m]` → Increase to `[5m]` or `[10m]`

### Step 5: Consolidation Check
- Do multiple alerts fire together? → Create aggregate alert
- Are there redundant alerts? → Remove duplicates

---

## Annotation Templates

### Required Annotations

```yaml
annotations:
  summary: "{{ $labels.instance }}: High CPU usage ({{ $value | printf \"%.1f\" }}%)"
  description: >
    CPU usage on {{ $labels.instance }} has been above 85% for more than 10 minutes.
    Current value: {{ $value | printf "%.1f" }}%.
    This may indicate resource exhaustion or runaway processes.
  runbook_url: "https://wiki.example.com/runbooks/high-cpu"
  dashboard_url: "https://grafana.example.com/d/cpu?var-instance={{ $labels.instance }}"
```

### Annotation Checklist

- [ ] `summary`: One-line description with key values
- [ ] `description`: Context for responders (what, why, impact)
- [ ] `runbook_url`: Link to remediation steps
- [ ] `dashboard_url`: Link to relevant Grafana dashboard

---

## Label Strategy

### Required Labels

| Label | Purpose | Example |
|-------|---------|---------|
| `severity` | Routing and prioritization | `critical`, `warning` |
| `team` | Ownership routing | `platform`, `payments` |
| `service` | Service identification | `api-gateway` |
| `environment` | Env differentiation | `production`, `staging` |

### Label Best Practices

1. **Keep cardinality low**: Labels should have bounded values
2. **Use consistent naming**: `team` not `owner` or `squad`
3. **Avoid dynamic values**: No `$value`, timestamps, request IDs
4. **Environment separation**: Different thresholds per env if needed

```yaml
labels:
  severity: warning
  team: platform
  service: api-gateway
  environment: production
```

---

## Alert YAML Template

```yaml
groups:
  - name: <service>-alerts
    rules:
      - alert: <MetricCondition>
        # Use rate() not irate(), percentage-based, minimum traffic
        expr: |
          (
            sum(rate(metric_name{filter="value"}[5m])) by (instance)
            /
            sum(rate(total_metric{filter="value"}[5m])) by (instance)
          ) > 0.05
          and
          sum(rate(total_metric{filter="value"}[5m])) by (instance) > 10
        for: 10m  # Based on metric volatility
        labels:
          severity: warning  # or critical
          team: <owning-team>
          service: <service-name>
        annotations:
          summary: "<Instance> <condition> ({{ $value | printf \"%.2f\" }})"
          description: |
            <Detailed description of the alert condition>
            Instance: {{ $labels.instance }}
            Current value: {{ $value | printf "%.2f" }}
            Threshold: <threshold value>
          runbook_url: "https://wiki.example.com/runbooks/<alert-name>"
          dashboard_url: "https://grafana.example.com/d/<dashboard-id>"
```

---

## Good Patterns Summary

| Pattern | Implementation |
|---------|----------------|
| Percentage-based | `error_rate / total_rate > 0.05` |
| Minimum traffic | `and rate(requests[5m]) > 10` |
| Multi-tier severity | Separate warning (85%) and critical (95%) rules |
| Exclude temp filesystems | `{fstype!~"tmpfs\|overlay"}` |
| Predictive alerting | `predict_linear(disk_free[6h], 3600*24) < 0` |
| SLO burn rate | Multi-window with different burn rates |

---

## Validation Checklist

Before deploying alert rules:

- [ ] `for` clause present and appropriate for metric volatility
- [ ] Uses `rate()` not `irate()` for alerting
- [ ] Percentage-based thresholds (not absolute counts)
- [ ] Minimum traffic guard for low-volume services
- [ ] Severity label present (critical, warning, info)
- [ ] Team and service labels for routing
- [ ] All annotations present (summary, description, runbook_url)
- [ ] Tested against historical data for false positive rate
