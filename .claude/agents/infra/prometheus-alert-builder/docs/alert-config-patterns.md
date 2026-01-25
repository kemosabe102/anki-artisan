# Prometheus Alert Configuration Patterns & Infrastructure

## Table of Contents
1. [Introduction](#introduction)
2. [Core Alert Patterns](#core-alert-patterns)
3. [Alertmanager Configuration](#alertmanager-configuration)
4. [Recording Rules for Alert Efficiency](#recording-rules-for-alert-efficiency)
5. [Label Strategy & Cardinality Management](#label-strategy--cardinality-management)
6. [Testing & Validation](#testing--validation)

---

## Introduction

This document provides comprehensive guidance on alert configuration patterns and infrastructure setup. While the Alert Rules Reference document shows individual alert examples, this guide focuses on **patterns**, **infrastructure configuration**, and **operational strategies** for effective alerting at scale.

### Document Purpose

- Learn reusable alert configuration patterns
- Configure Alertmanager for proper routing and grouping
- Implement recording rules to optimize alert performance
- Manage label cardinality to prevent system issues
- Validate and test alert configurations

### Prerequisites

Before using this guide, you should:
- Understand basic Prometheus concepts (metrics, labels, PromQL)
- Have reviewed the Alert Rules Reference document
- Have access to a Prometheus and Alertmanager installation

---

## Core Alert Patterns

These patterns represent proven approaches to common alerting scenarios. Each pattern includes when to use it, how to implement it, and real-world considerations.

### Pattern 1: Multi-Tier Severity Alerting

**When to Use**: When you need different response times and escalation paths for different severity levels of the same issue.

**Problem Solved**: Single-threshold alerts can't differentiate between "high but manageable" and "critically high" conditions.

**Implementation**:

```yaml
# Warning: Early indication of elevated resource usage
- alert: HighCPUWarning
  expr: |
    100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 85
  for: 15m
  labels:
    severity: warning
    team: infrastructure
    tier: 1
  annotations:
    summary: "Elevated CPU on {{ $labels.instance }}"
    description: "CPU at {{ $value | humanizePercentage }}. Monitor for further increase."

# Critical: Requires immediate action
- alert: HighCPUCritical
  expr: |
    100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 95
  for: 5m
  labels:
    severity: critical
    team: infrastructure
    tier: 2
  annotations:
    summary: "CRITICAL CPU on {{ $labels.instance }}"
    description: "CPU at {{ $value | humanizePercentage }}. Immediate intervention required."
```

**Key Characteristics**:
- Same metric, different thresholds (85% vs 95%)
- Different `for` durations (15m vs 5m) - critical fires faster
- Different severity labels route to different channels
- Warning gives early heads-up, critical demands immediate action

**Decision Tree for Thresholds**:
```
Is it affecting users NOW?
├─ Yes → Critical (requires immediate action)
└─ No
   ├─ Will it affect users in < 30 minutes? → Critical
   └─ Will it affect users in 30m-2h? → Warning
      └─ Will it affect users in > 2h? → Info (or no alert)
```

**Routing Strategy**:
```yaml
# In Alertmanager
routes:
  - match:
      severity: critical
    receiver: pagerduty
    group_wait: 10s
    repeat_interval: 5m
    
  - match:
      severity: warning
    receiver: slack
    group_wait: 5m
    repeat_interval: 4h
```

---

### Pattern 2: SLO-Based Multi-Window Burn Rate

**When to Use**: When you have defined SLOs and want to alert based on error budget consumption rate.

**Problem Solved**: Traditional threshold alerts don't account for how quickly you're consuming your error budget.

**Concept**: Google's multi-window multi-burn-rate approach detects both fast burns (complete budget exhaustion in hours) and slow burns (gradual degradation over days).

**Implementation**:

```yaml
# Fast burn: 2% of monthly budget consumed in 1 hour
- alert: ErrorBudgetBurnRateFast
  expr: |
    (
      sum(rate(http_requests_total{status=~"5.."}[1h])) by (service)
      /
      sum(rate(http_requests_total[1h])) by (service)
    ) > (1 - 0.999) * 14.4  # 99.9% SLO, 14.4x burn rate
    and
    (
      sum(rate(http_requests_total{status=~"5.."}[5m])) by (service)
      /
      sum(rate(http_requests_total[5m])) by (service)
    ) > (1 - 0.999) * 14.4
  for: 2m
  labels:
    severity: critical
    team: "{{ $labels.service }}-team"
    slo: "availability"
    burn_rate: "fast"
  annotations:
    summary: "Fast error budget burn for {{ $labels.service }}"
    description: |
      Burning error budget at 14.4x normal rate.
      Monthly budget will be exhausted in ~2 hours at this rate.
      
      Current error rate: {{ $value | humanizePercentage }}
      SLO: 99.9% availability
      
      This is a P1 incident requiring immediate response.

# Slow burn: 5% of monthly budget consumed in 6 hours  
- alert: ErrorBudgetBurnRateSlow
  expr: |
    (
      sum(rate(http_requests_total{status=~"5.."}[6h])) by (service)
      /
      sum(rate(http_requests_total[6h])) by (service)
    ) > (1 - 0.999) * 6  # 99.9% SLO, 6x burn rate
    and
    (
      sum(rate(http_requests_total{status=~"5.."}[30m])) by (service)
      /
      sum(rate(http_requests_total[30m])) by (service)
    ) > (1 - 0.999) * 6
  for: 15m
  labels:
    severity: warning
    team: "{{ $labels.service }}-team"
    slo: "availability"
    burn_rate: "slow"
  annotations:
    summary: "Sustained elevated errors for {{ $labels.service }}"
    description: |
      Burning error budget at 6x normal rate for 6+ hours.
      5% of monthly budget consumed.
      
      Current error rate: {{ $value | humanizePercentage }}
      SLO: 99.9% availability
      
      Investigate and address to prevent SLO violation.
```

**Burn Rate Calculation**:

For a 99.9% SLO (0.1% error budget):
- **14.4x burn rate** = consuming 2% of monthly budget per hour = budget exhausted in ~2 hours
- **6x burn rate** = consuming 5% of monthly budget per 6 hours = budget exhausted in ~5 days

**Multi-Window Validation**:
Both long window (1h or 6h) AND short window (5m or 30m) must exceed threshold to fire. This prevents:
- False positives from brief spikes (short window alone)
- Delayed detection (long window alone)

**Choosing Burn Rates**:

| Burn Rate | Budget Consumed | Time to Exhaustion | Severity | Use When |
|-----------|-----------------|-------------------|----------|----------|
| 14.4x | 2% in 1 hour | 2 hours | Critical | Fast-moving incidents |
| 6x | 5% in 6 hours | 5 days | Warning | Sustained degradation |
| 3x | 10% in 3 days | 10 days | Info | Long-term trends |

---

### Pattern 3: Symptom + Cause Pairing

**When to Use**: When you want to alert on user-facing impact (symptom) but also track potential root causes.

**Problem Solved**: Alerting only on causes (e.g., high CPU) can fire when there's no user impact. Alerting only on symptoms can delay root cause identification.

**Implementation**:

```yaml
# Symptom: What users actually experience
- alert: HighErrorRateUserFacing
  expr: |
    (
      sum(rate(http_requests_total{status=~"5.."}[5m])) by (service)
      /
      sum(rate(http_requests_total[5m])) by (service)
    ) * 100 > 1
  for: 10m
  labels:
    severity: critical
    team: "{{ $labels.service }}-team"
    alert_type: symptom
    pages: "true"
  annotations:
    summary: "Users experiencing errors in {{ $labels.service }}"
    description: "{{ $value | humanizePercentage }} of requests failing"

# Cause: Technical issue that may explain the symptom
- alert: DatabaseConnectionPoolExhaustion
  expr: |
    (db_connections_active / db_connections_max) * 100 > 95
  for: 5m
  labels:
    severity: warning
    team: database
    alert_type: cause
    pages: "false"
  annotations:
    summary: "Database connection pool near limit"
    description: "May cause application errors if exhausted"

# Cause: Another potential root cause
- alert: HighBackendLatency
  expr: |
    histogram_quantile(0.99, sum(rate(backend_duration_seconds_bucket[5m])) by (le, service)) > 5
  for: 10m
  labels:
    severity: warning
    team: backend
    alert_type: cause
    pages: "false"
  annotations:
    summary: "Backend latency elevated for {{ $labels.service }}"
    description: "May contribute to user-facing errors"
```

**Correlation Strategy**:

When the symptom alert fires, check which cause alerts are also active:

```yaml
# In Alertmanager - group symptom and cause together
route:
  group_by: ['service', 'alert_type']
  group_wait: 30s
  
  routes:
    - match:
        alert_type: symptom
      receiver: pagerduty
      continue: true  # Also process cause alerts
      
    - match:
        alert_type: cause
      receiver: slack
```

**Labels for Correlation**:
- Both symptom and cause should share common labels (e.g., `service`)
- Use `alert_type` to differentiate
- Page only on symptoms (`pages: "true"`)
- Log causes for correlation (`pages: "false"`)

---

### Pattern 4: Predictive Alerting

**When to Use**: When you can predict resource exhaustion before it happens.

**Problem Solved**: Reactive alerts fire when it's already too late. Predictive alerts give time to intervene.

**Implementation**:

```yaml
# Predict disk will fill in 4 hours
- alert: DiskWillFillIn4Hours
  expr: |
    (
      node_filesystem_avail_bytes{fstype!~"tmpfs|fuse.*|overlay"}
      / node_filesystem_size_bytes{fstype!~"tmpfs|fuse.*|overlay"}
    ) > 0.1  # Still have some space
    and
    predict_linear(
      node_filesystem_avail_bytes{fstype!~"tmpfs|fuse.*|overlay"}[1h],
      4 * 3600
    ) < 0
  for: 15m
  labels:
    severity: warning
    team: infrastructure
    alert_type: predictive
  annotations:
    summary: "Disk {{ $labels.mountpoint }} will fill in ~4 hours"
    description: |
      At current fill rate, disk will be full in 4 hours.
      
      Current available: {{ query "node_filesystem_avail_bytes{instance='{{ $labels.instance }}', mountpoint='{{ $labels.mountpoint }}'}" | first | value | humanize1024 }}
      
      Take action now to prevent outage.

# Predict memory exhaustion in 2 hours
- alert: MemoryWillExhaustIn2Hours
  expr: |
    node_memory_MemAvailable_bytes > 1000000000  # At least 1GB available
    and
    predict_linear(node_memory_MemAvailable_bytes[30m], 2 * 3600) < 0
  for: 10m
  labels:
    severity: critical
    team: infrastructure
    alert_type: predictive
  annotations:
    summary: "Memory exhaustion predicted in 2h on {{ $labels.instance }}"
    description: "Current trend will exhaust memory in 2 hours"
```

**predict_linear() Parameters**:
```
predict_linear(metric[range], seconds_into_future)
```

- `range`: Historical window to analyze (typically 30m-2h)
- `seconds_into_future`: How far ahead to predict

**Choosing Time Horizons**:

| Resource | Historical Window | Prediction Horizon | Rationale |
|----------|------------------|-------------------|-----------|
| **Disk** | 1h | 4h | Slow-changing, predictable |
| **Memory** | 30m | 2h | Faster-changing, less predictable |
| **Traffic** | 2h | 1h | Cyclical patterns, longer history needed |

**Validation**:
- Ensure current state is not already critical (`> 0.1` remaining)
- Require sustained trend (`for: 15m`) to avoid noise
- Combine with reactive alerts (fire whichever comes first)

---

### Pattern 5: Percentage Over Threshold

**When to Use**: For SLO compliance checking - ensuring X% of samples are within acceptable range.

**Problem Solved**: Simple threshold alerts miss the distribution. You care about "95% of requests under 500ms", not just "some requests over 500ms".

**Implementation**:

```yaml
# Latency SLO: 95% of requests under 500ms
- alert: LatencySLOViolation
  expr: |
    (
      sum(rate(http_request_duration_seconds_bucket{le="0.5"}[5m])) by (service)
      /
      sum(rate(http_request_duration_seconds_count[5m])) by (service)
    ) < 0.95
  for: 10m
  labels:
    severity: warning
    team: "{{ $labels.service }}-team"
    slo_type: latency
  annotations:
    summary: "Latency SLO violation for {{ $labels.service }}"
    description: |
      Only {{ $value | humanizePercentage }} of requests completing under 500ms.
      SLO target: 95%
      
      This indicates user-facing performance degradation.

# Availability SLO: 99% of requests successful
- alert: AvailabilitySLOViolation
  expr: |
    (
      sum(rate(http_requests_total{status!~"5.."}[5m])) by (service)
      /
      sum(rate(http_requests_total[5m])) by (service)
    ) < 0.99
  for: 10m
  labels:
    severity: warning
    team: "{{ $labels.service }}-team"
    slo_type: availability
  annotations:
    summary: "Availability SLO violation for {{ $labels.service }}"
    description: "Success rate at {{ $value | humanizePercentage }} (target: 99%)"
```

**Using Histogram Buckets**:

For latency SLOs, leverage histogram buckets efficiently:

```promql
# Percentage of requests in bucket 'le="0.5"' (under 500ms)
sum(rate(http_request_duration_seconds_bucket{le="0.5"}[5m]))
/
sum(rate(http_request_duration_seconds_count[5m]))
```

**Multiple Threshold Checking**:

```yaml
# Tiered latency SLO
- alert: LatencyP95Degraded
  expr: |
    histogram_quantile(0.95, 
      sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service)
    ) > 1
  for: 10m
  labels:
    severity: warning

- alert: LatencyP99Degraded
  expr: |
    histogram_quantile(0.99,
      sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service)
    ) > 3
  for: 10m
  labels:
    severity: critical
```

---

### Pattern 6: Aggregation for Noise Reduction

**When to Use**: When individual instance alerts create too much noise and you care about aggregate service health.

**Problem Solved**: 50 instances with individual alerts = 50 notifications for the same issue.

**Implementation**:

```yaml
# BAD: Per-instance alert (creates 50 alerts for 50 instances)
- alert: HighCPUPerInstance
  expr: |
    100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) by (instance) * 100) > 90
  for: 10m
  labels:
    severity: warning
# Result: Alert storm when there's a region-wide issue

# GOOD: Aggregate by service (creates 1 alert per service)
- alert: HighCPUByService
  expr: |
    avg by(service) (
      100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) by (instance, service) * 100)
    ) > 90
  for: 10m
  labels:
    severity: warning
    team: "{{ $labels.service }}-team"
  annotations:
    summary: "High CPU for service {{ $labels.service }}"
    description: |
      Service {{ $labels.service }} average CPU: {{ $value | humanizePercentage }}
      
      Affected instances: {{ query "count(100 - (avg(rate(node_cpu_seconds_total{mode='idle',service='{{ $labels.service }}'}[5m])) by (instance) * 100) > 90)" | first | value }}

# BETTER: Alert when percentage of instances affected
- alert: ServiceInstancesDegraded
  expr: |
    (
      count(
        100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) by (instance, service) * 100) > 90
      ) by (service)
      /
      count(
        up{job="node"} == 1
      ) by (service)
    ) * 100 > 25
  for: 10m
  labels:
    severity: critical
    team: "{{ $labels.service }}-team"
  annotations:
    summary: "{{ $value | humanizePercentage }} of {{ $labels.service }} instances degraded"
    description: "More than 25% of instances have high CPU"
```

**Aggregation Strategies**:

| Strategy | When to Use | Example |
|----------|-------------|---------|
| **avg by(service)** | Care about overall service health | Average latency across all instances |
| **sum by(service)** | Care about total capacity | Total throughput, total error count |
| **count() / count()** | Care about percentage affected | % of instances down |
| **max by(service)** | Care about worst instance | Worst-case latency |
| **min by(service)** | Care about best instance | Best-case scenario |

**Preserving Instance Information**:

Even with aggregation, provide instance details in annotations:

```yaml
annotations:
  description: |
    Service-level CPU at {{ $value }}%.
    
    Top 5 instances by CPU:
    {{- range query "topk(5, 100 - (avg(rate(node_cpu_seconds_total{mode='idle',service='myservice'}[5m])) by (instance) * 100))" }}
    - {{ .Labels.instance }}: {{ .Value | humanizePercentage }}
    {{- end }}
```

---

### Pattern 7: Template-Based Dynamic Labels

**When to Use**: When you need dynamic routing but must avoid high cardinality.

**Problem Solved**: Hardcoding team names doesn't scale. Dynamic values can explode cardinality.

**Implementation**:

```yaml
# GOOD: Dynamic but bounded
- alert: ServiceErrorRate
  expr: |
    (sum(rate(http_requests_total{status=~"5.."}[5m])) by (service) / sum(rate(http_requests_total[5m])) by (service)) > 0.01
  for: 10m
  labels:
    severity: warning
    team: "{{ $labels.service }}-team"  # Dynamic but bounded (limited services)
    environment: "{{ $labels.environment }}"  # Dynamic but bounded (prod/staging/dev)
  annotations:
    summary: "Errors in {{ $labels.service }}"

# BAD: Unbounded cardinality
- alert: SlowRequest
  expr: request_duration > 1
  labels:
    severity: warning
    request_id: "{{ $labels.request_id }}"  # DON'T DO THIS - unbounded
    duration: "{{ $value }}"  # DON'T DO THIS - every value creates new alert
```

**Safe Template Usage**:

✅ **Safe** (bounded cardinality):
- Service names (controlled set)
- Environment names (prod, staging, dev)
- Team names (derived from service)
- Component types (api, database, cache)
- Region names (us-east-1, eu-west-1)

❌ **Unsafe** (unbounded cardinality):
- Request IDs
- User IDs
- Pod names (in large clusters)
- Timestamps
- Metric values (`$value`)
- URLs/paths without grouping

**Team Routing Pattern**:

```yaml
# Service-to-team mapping via label
labels:
  team: "{{ $labels.service }}-team"
  
# In Alertmanager
routes:
  - match_re:
      team: "payment-team"
    receiver: payment-slack
    
  - match_re:
      team: "auth-team"
    receiver: auth-slack
```

**Validation**:
Run this query to check label cardinality:
```promql
count by(__name__, job, le) ({__name__=~".+"})
```

If alert instances are growing unboundedly, you have a cardinality issue.

---

### Pattern 8: Minimum Traffic Threshold

**When to Use**: When low-traffic periods make percentage-based alerts unreliable.

**Problem Solved**: 1 error out of 2 requests = 50% error rate (alert fires), but it's not actually a problem.

**Implementation**:

```yaml
# Error rate with minimum traffic threshold
- alert: HighErrorRate
  expr: |
    (
      sum(rate(http_requests_total{status=~"5.."}[5m])) by (service)
      /
      sum(rate(http_requests_total[5m])) by (service)
    ) > 0.01
    and
    sum(rate(http_requests_total[5m])) by (service) > 10  # Minimum 10 req/s
  for: 10m
  labels:
    severity: warning
    team: "{{ $labels.service }}-team"
  annotations:
    summary: "Error rate {{ $value | humanizePercentage }} for {{ $labels.service }}"
    description: |
      Error rate above threshold with sufficient traffic.
      
      Error rate: {{ query "sum(rate(http_requests_total{status=~'5..',service='{{ $labels.service }}'}[5m]))" | first | value }}/s
      Total rate: {{ query "sum(rate(http_requests_total{service='{{ $labels.service }}'}[5m]))" | first | value }}/s

# Cache hit rate with minimum traffic threshold
- alert: LowCacheHitRate
  expr: |
    (
      rate(cache_hits_total[10m])
      /
      (rate(cache_hits_total[10m]) + rate(cache_misses_total[10m]))
    ) < 0.8
    and
    (rate(cache_hits_total[10m]) + rate(cache_misses_total[10m])) > 10
  for: 15m
  labels:
    severity: warning
  annotations:
    summary: "Cache hit rate low with sufficient traffic"
```

**Choosing Minimum Thresholds**:

| Metric | Minimum Threshold | Rationale |
|--------|------------------|-----------|
| **Error rate** | 10 req/s | Below this, individual errors are noise |
| **Cache hit rate** | 10 req/s | Cache warmup period needs traffic |
| **Latency percentiles** | 100 req/5m | Percentiles unreliable with low sample count |
| **Success rate** | 5 req/s | Sufficient for statistical significance |

**Time-of-Day Awareness**:

For services with known traffic patterns:

```yaml
# Higher threshold during business hours
- alert: ErrorRateBusiness Hours
  expr: |
    (error_rate > 0.01 and traffic > 100)
    and
    hour() >= 9 and hour() <= 17
  for: 5m
  labels:
    severity: critical

# Lower threshold during off-hours
- alert: ErrorRateOffHours
  expr: |
    (error_rate > 0.05 and traffic > 10)
    and
    (hour() < 9 or hour() > 17)
  for: 15m
  labels:
    severity: warning
```

---

## Alertmanager Configuration

### Grouping Configuration

**Purpose**: Batch related alerts together to reduce notification spam.

**Complete Example**:

```yaml
global:
  resolve_timeout: 5m

route:
  receiver: 'default'
  group_by: ['alertname', 'cluster', 'service']
  group_wait: 30s       # Wait this long for more alerts before first notification
  group_interval: 5m    # Wait this long before sending update on group changes
  repeat_interval: 4h   # Resend notification if still firing
  
  routes:
    # Critical alerts to PagerDuty immediately
    - match:
        severity: critical
      receiver: pagerduty
      group_wait: 10s
      group_interval: 5m
      repeat_interval: 5m
      continue: true  # Also process other routes
      
    # Warnings to Slack  
    - match:
        severity: warning
      receiver: slack
      group_wait: 5m
      group_interval: 10m
      repeat_interval: 12h
      
    # Team-specific routing
    - match_re:
        team: ".*-team"
      receiver: '{{ $labels.team }}'
      group_by: ['alertname', 'team', 'service']
      
    # SLO violations to dedicated channel
    - match:
        slo: "true"
      receiver: slo-violations
      group_by: ['service', 'slo_type']
      
    # Predictive alerts to separate channel
    - match:
        alert_type: predictive
      receiver: capacity-planning
      group_wait: 10m
      repeat_interval: 24h
```

**Parameter Guidance**:

| Parameter | Purpose | Typical Values | Rationale |
|-----------|---------|----------------|-----------|
| **group_wait** | Initial wait for grouping | 10s-5m | Shorter for critical, longer for warnings |
| **group_interval** | Update interval | 5m-30m | How often to send updates on active alerts |
| **repeat_interval** | Resend interval | 1h-12h | How often to remind about ongoing issues |
| **group_by** | Grouping labels | alertname, cluster, service | Batch related alerts together |

**Grouping Strategy Examples**:

```yaml
# Group by service and alertname (typical)
group_by: ['alertname', 'service']
# Result: All "HighCPU" alerts for "payment-api" in one notification

# Group by severity and team
group_by: ['severity', 'team']
# Result: All critical alerts for "infrastructure-team" together

# Group by cluster and namespace (Kubernetes)
group_by: ['cluster', 'namespace', 'alertname']
# Result: All alerts in "prod-us-east-1" cluster's "backend" namespace together
```

---

### Inhibition Rules

**Purpose**: Suppress downstream/related alerts when a root cause alert is firing.

**Complete Example**:

```yaml
inhibit_rules:
  # Service down inhibits instance down
  - source_match:
      alertname: 'ServiceDown'
    target_match:
      alertname: 'InstanceDown'
    equal: ['service', 'cluster']
  # Logic: If entire service is down, don't alert on individual instances
  
  # Critical inhibits warning (same alert)
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
    equal: ['alertname', 'instance']
  # Logic: If critical CPU alert fires, suppress warning CPU alert
  
  # Database down inhibits replication lag
  - source_match:
      alertname: 'DatabaseDown'
    target_match:
      alertname: 'ReplicationLag'
    equal: ['database', 'cluster']
  # Logic: If database is down, replication lag is expected
  
  # Node down inhibits all node-level alerts
  - source_match:
      alertname: 'NodeDown'
    target_match_re:
      alertname: 'Node.*'
    equal: ['instance']
  # Logic: If node is down, suppress CPU/memory/disk alerts for that node
  
  # Network partition inhibits service alerts
  - source_match:
      alertname: 'NetworkPartition'
    target_match_re:
      alertname: '.*Degraded'
    equal: ['cluster', 'datacenter']
  # Logic: During network partition, service degradation is expected
  
  # Planned maintenance window
  - source_match:
      alertname: 'MaintenanceWindow'
    target_match_re:
      alertname: '.*'
    equal: ['cluster']
  # Logic: During maintenance, suppress all alerts for that cluster
```

**Inhibition Rule Parameters**:

- `source_match`: The alert that causes inhibition (root cause)
- `target_match`: The alert(s) to suppress (symptoms)
- `equal`: Labels that must match between source and target
- `source_match_re` / `target_match_re`: Regex patterns

**Common Inhibition Patterns**:

| Scenario | Source Alert | Target Alert | Reason |
|----------|--------------|--------------|--------|
| **Infrastructure → Service** | NodeDown | ServiceDegraded | Node failure explains service issues |
| **Network → All** | NetworkPartition | * | Network issues affect everything |
| **Severity escalation** | Critical | Warning (same alert) | Don't need both severity levels |
| **Parent → Child** | ClusterDown | PodDown | Cluster down explains pod failures |
| **Database → App** | DatabaseDown | HighErrorRate | Database unavailability causes app errors |

**Testing Inhibition**:

```bash
# Send test alerts to verify inhibition
amtool alert add alertname=DatabaseDown database=prod severity=critical
amtool alert add alertname=ReplicationLag database=prod severity=warning

# Check which alerts are active (ReplicationLag should be inhibited)
amtool alert query
```

---

### Receiver Configuration

**Purpose**: Define notification channels and formats.

**Complete Example**:

```yaml
receivers:
  - name: 'default'
    webhook_configs:
      - url: 'http://logging-service/alerts'
  
  - name: 'pagerduty'
    pagerduty_configs:
      - service_key: '<pagerduty-integration-key>'
        severity: '{{ .GroupLabels.severity }}'
        description: '{{ .GroupLabels.alertname }}: {{ .CommonAnnotations.summary }}'
        details:
          firing: '{{ .Alerts.Firing | len }}'
          resolved: '{{ .Alerts.Resolved | len }}'
          group_labels: '{{ .GroupLabels.SortedPairs.Values | join ", " }}'
  
  - name: 'slack'
    slack_configs:
      - api_url: '<slack-webhook-url>'
        channel: '#alerts'
        title: '{{ .GroupLabels.alertname }} ({{ .GroupLabels.severity }})'
        text: |
          {{ range .Alerts }}
          *Alert:* {{ .Labels.alertname }}
          *Severity:* {{ .Labels.severity }}
          *Summary:* {{ .Annotations.summary }}
          *Description:* {{ .Annotations.description }}
          {{ if .Annotations.runbook_url }}*Runbook:* {{ .Annotations.runbook_url }}{{ end }}
          {{ if .Annotations.dashboard_url }}*Dashboard:* {{ .Annotations.dashboard_url }}{{ end }}
          *Status:* {{ .Status }}
          {{ end }}
        send_resolved: true
  
  - name: 'email'
    email_configs:
      - to: 'oncall@example.com'
        from: 'alertmanager@example.com'
        smarthost: 'smtp.example.com:587'
        auth_username: 'alertmanager'
        auth_password: '<password>'
        headers:
          Subject: '[{{ .Status | toUpper }}] {{ .GroupLabels.alertname }}'
        html: |
          <h2>{{ .GroupLabels.alertname }}</h2>
          <p><strong>Status:</strong> {{ .Status }}</p>
          <p><strong>Severity:</strong> {{ .CommonLabels.severity }}</p>
          <p><strong>Summary:</strong> {{ .CommonAnnotations.summary }}</p>
          <p><strong>Description:</strong> {{ .CommonAnnotations.description }}</p>
          
  - name: 'teams'
    webhook_configs:
      - url: '<microsoft-teams-webhook>'
        send_resolved: true
  
  - name: 'opsgenie'
    opsgenie_configs:
      - api_key: '<opsgenie-api-key>'
        priority: '{{ if eq .GroupLabels.severity "critical" }}P1{{ else }}P3{{ end }}'
        description: '{{ .CommonAnnotations.summary }}'
        details:
          runbook: '{{ .CommonAnnotations.runbook_url }}'
```

**Template Variables**:

Available in receiver configurations:

| Variable | Description | Example |
|----------|-------------|---------|
| `.Status` | firing or resolved | firing |
| `.GroupLabels` | Labels used for grouping | {alertname: HighCPU, service: api} |
| `.CommonLabels` | Labels common to all alerts in group | {severity: warning} |
| `.CommonAnnotations` | Annotations common to all alerts | {summary: "High CPU"} |
| `.Alerts` | List of all alerts in group | [{Labels: ..., Annotations: ...}] |
| `.Alerts.Firing` | Only firing alerts | [...] |
| `.Alerts.Resolved` | Only resolved alerts | [...] |

**Conditional Routing to Receivers**:

```yaml
routes:
  # Production critical alerts → PagerDuty
  - match:
      severity: critical
      environment: production
    receiver: pagerduty
    
  # Staging critical alerts → Slack (not PagerDuty)
  - match:
      severity: critical
      environment: staging
    receiver: slack
    
  # Warnings → Slack
  - match:
      severity: warning
    receiver: slack
```

---

## Recording Rules for Alert Efficiency

### When to Use Recording Rules

**Purpose**: Pre-compute expensive queries used in alerts to improve performance and reliability.

**Use Recording Rules When**:
1. Alert expression is computationally expensive
2. Same calculation used in multiple alerts
3. High-cardinality aggregation needed
4. Time-series data needs downsampling

**Example Scenario**:

```yaml
# WITHOUT recording rule - expensive query in alert
- alert: HighErrorRate
  expr: |
    (
      sum(rate(http_requests_total{status=~"5.."}[5m])) by (service, environment)
      /
      sum(rate(http_requests_total[5m])) by (service, environment)
    ) > 0.01
  # This query runs every evaluation (default 1m)
  # Heavy aggregation on every evaluation

# WITH recording rule - pre-computed
recording_rules.yaml:
  - record: service:http_errors:rate5m
    expr: |
      sum(rate(http_requests_total{status=~"5.."}[5m])) by (service, environment)
  
  - record: service:http_requests:rate5m
    expr: |
      sum(rate(http_requests_total[5m])) by (service, environment)
  
  - record: service:http_error_ratio:rate5m
    expr: |
      service:http_errors:rate5m / service:http_requests:rate5m

alert_rules.yaml:
  - alert: HighErrorRate
    expr: service:http_error_ratio:rate5m > 0.01
    # Much faster - just a simple threshold check
```

### Recording Rule Naming Convention

**Google's Recommended Format**:
```
level:metric:operations
```

**Examples**:
- `job:http_requests:rate5m` - aggregated by job
- `instance:cpu_usage:avg` - aggregated by instance
- `service:http_errors:rate5m` - aggregated by service
- `cluster:memory_usage:sum` - aggregated by cluster

**Operations Suffix**:
- `rate5m` - rate over 5 minutes
- `rate1h` - rate over 1 hour
- `sum` - sum aggregation
- `avg` - average aggregation
- `ratio` - division of two metrics

### Complete Recording Rules Example

```yaml
groups:
  - name: service_metrics
    interval: 30s  # Evaluate every 30 seconds
    rules:
      # HTTP request rates
      - record: service:http_requests:rate5m
        expr: |
          sum(rate(http_requests_total[5m])) by (service, environment, status)
      
      # HTTP error rate  
      - record: service:http_errors:rate5m
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m])) by (service, environment)
      
      # HTTP error ratio
      - record: service:http_error_ratio:rate5m
        expr: |
          service:http_errors:rate5m
          /
          (sum(service:http_requests:rate5m) by (service, environment))
      
      # HTTP latency percentiles (pre-computed)
      - record: service:http_latency:p50
        expr: |
          histogram_quantile(0.50,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service, environment)
          )
      
      - record: service:http_latency:p95
        expr: |
          histogram_quantile(0.95,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service, environment)
          )
      
      - record: service:http_latency:p99
        expr: |
          histogram_quantile(0.99,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service, environment)
          )
  
  - name: infrastructure_metrics
    interval: 30s
    rules:
      # CPU usage by instance
      - record: instance:cpu_usage:rate5m
        expr: |
          100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
      
      # Memory usage by instance
      - record: instance:memory_usage:ratio
        expr: |
          (
            node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes
          ) / node_memory_MemTotal_bytes
      
      # Disk usage by instance and mountpoint
      - record: instance:disk_usage:ratio
        expr: |
          (
            node_filesystem_size_bytes{fstype!~"tmpfs|fuse.*"}
            - node_filesystem_avail_bytes{fstype!~"tmpfs|fuse.*"}
          ) / node_filesystem_size_bytes{fstype!~"tmpfs|fuse.*"}
```

### Using Recording Rules in Alerts

```yaml
alert_rules.yaml:
  - alert: HighErrorRate
    expr: service:http_error_ratio:rate5m > 0.01
    for: 10m
    labels:
      severity: warning
    annotations:
      summary: "High error rate for {{ $labels.service }}"
  
  - alert: HighP99Latency
    expr: service:http_latency:p99 > 1
    for: 15m
    labels:
      severity: warning
    annotations:
      summary: "High P99 latency for {{ $labels.service }}"
  
  - alert: HighCPU
    expr: instance:cpu_usage:rate5m > 90
    for: 15m
    labels:
      severity: warning
    annotations:
      summary: "High CPU on {{ $labels.instance }}"
```

### Performance Benefits

**Before Recording Rules**:
- Alert expression: 100,000 time series → aggregated every minute
- Evaluation time: 5-10 seconds
- Resource usage: High CPU/memory during evaluation

**After Recording Rules**:
- Recording rule: 100,000 time series → 50 pre-computed results
- Alert expression: 50 time series → simple threshold check
- Evaluation time: < 100ms
- Resource usage: Minimal

---

## Label Strategy & Cardinality Management

### Understanding Cardinality

**Cardinality**: The number of unique time series created by label combinations.

**Example**:
```
metric_name{label1="value1", label2="value2"}
```

With 10 possible values for label1 and 20 for label2:
- Cardinality = 10 × 20 = 200 time series

### Cardinality Problems

**High cardinality causes**:
- Prometheus memory exhaustion
- Slow queries
- Alertmanager overload
- Alert explosion

**Common High-Cardinality Culprits**:

| Label Type | Example | Cardinality | Problem |
|------------|---------|-------------|---------|
| **User IDs** | user_id="12345" | Millions | Creates time series per user |
| **Request IDs** | request_id="abc-123" | Infinite | New series for every request |
| **Timestamps** | timestamp="2025-12-06T08:00:00Z" | Infinite | New series every second |
| **URLs** | url="/api/users/123/orders/456" | Thousands | Creates series per URL path |
| **Pod names** | pod="app-7f8b9c-xyz" | Hundreds/Thousands | In large Kubernetes clusters |
| **IP addresses** | ip="192.168.1.100" | Thousands | Creates series per IP |

### Label Strategy Best Practices

#### ✅ DO: Use Bounded Labels

```yaml
# Good labels (finite, controlled cardinality)
labels:
  service: payment-api           # ~10-100 services
  environment: production        # 3-5 environments
  region: us-east-1             # ~5-20 regions
  team: backend-team            # ~10-50 teams
  severity: critical            # 3-4 severity levels
  component: database           # ~10-20 components
  http_status: "500"            # ~100 status codes
```

#### ❌ DON'T: Use Unbounded Labels

```yaml
# Bad labels (unbounded cardinality)
labels:
  user_id: "{{ $labels.user_id }}"          # Millions
  request_id: "{{ $labels.request_id }}"    # Infinite
  pod: "{{ $labels.pod }}"                  # Hundreds/Thousands
  ip_address: "{{ $labels.ip }}"            # Thousands
  timestamp: "{{ now }}"                    # Infinite
  error_message: "{{ $labels.error }}"      # Thousands
```

### Fixing High-Cardinality Alerts

**Problem**: Per-pod alerts in Kubernetes

```yaml
# BAD: Creates alert for every pod
- alert: PodHighCPU
  expr: |
    container_cpu_usage > 0.9
  # With 1000 pods, creates 1000 alerts
```

**Solution 1**: Aggregate by service

```yaml
# GOOD: One alert per service
- alert: ServiceHighCPU
  expr: |
    avg by(service, namespace) (container_cpu_usage) > 0.8
  # Creates one alert per service, not per pod
  annotations:
    summary: "Service {{ $labels.service }} high CPU"
    description: |
      Average CPU across pods: {{ $value | humanizePercentage }}
      
      Affected pods: {{ query "count(container_cpu_usage{service='{{ $labels.service }}'} > 0.9)" | first | value }}
```

**Solution 2**: Alert on percentage of pods affected

```yaml
# GOOD: Alert when significant portion affected
- alert: ServicePodsHighCPU
  expr: |
    (
      count(container_cpu_usage{service="payment"} > 0.9) by (service)
      /
      count(container_cpu_usage{service="payment"}) by (service)
    ) > 0.3
  # Alerts when > 30% of pods have high CPU
  annotations:
    summary: "{{ $value | humanizePercentage }} of {{ $labels.service }} pods high CPU"
```

### Cardinality Monitoring

**Check current cardinality**:

```promql
# Count unique time series per metric
count by(__name__) ({__name__=~".+"})

# Total time series in Prometheus
prometheus_tsdb_symbol_table_size_bytes

# Top metrics by cardinality
topk(20, count by(__name__) ({__name__=~".+"}))
```

**Alert on high cardinality**:

```yaml
- alert: HighMetricCardinality
  expr: |
    count by(__name__) ({__name__=~".+"}) > 10000
  for: 10m
  labels:
    severity: warning
  annotations:
    summary: "Metric {{ $labels.__name__ }} has high cardinality"
    description: "{{ $value }} time series for this metric"
```

### Label Normalization

**Problem**: Inconsistent label values

```
# Three different ways to say the same thing:
environment=prod
environment=production  
env=prod
```

**Solution**: Use relabel_configs to normalize

```yaml
# In prometheus.yml
scrape_configs:
  - job_name: 'my-app'
    relabel_configs:
      # Normalize environment label
      - source_labels: [environment]
        regex: 'production|prod'
        target_label: environment
        replacement: 'prod'
      
      - source_labels: [environment]
        regex: 'staging|stage'
        target_label: environment
        replacement: 'staging'
      
      # Drop high-cardinality labels
      - regex: 'pod|request_id|user_id'
        action: labeldrop
```

---

## Testing & Validation

### 1. Validate Alert Rules Syntax

```bash
# Check alert rules file for syntax errors
promtool check rules /path/to/alert_rules.yaml

# Expected output for valid rules:
# Checking /path/to/alert_rules.yaml
#   SUCCESS: 5 rules found
```

**Common Syntax Errors**:
- Missing `|` for multi-line expressions
- Unmatched parentheses in PromQL
- Invalid label names (must match `[a-zA-Z_][a-zA-Z0-9_]*`)
- Missing required fields (expr, alert)

### 2. Test Alert Expressions

```bash
# Test if expression returns expected results
promtool query instant http://prometheus:9090 \
  '100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)'

# Test with specific time
promtool query instant http://prometheus:9090 \
  'up{job="myapp"} == 0' \
  --time='2025-12-06T10:00:00Z'

# Test range query
promtool query range http://prometheus:9090 \
  'rate(http_requests_total[5m])' \
  --start='2025-12-06T09:00:00Z' \
  --end='2025-12-06T10:00:00Z' \
  --step=1m
```

### 3. Unit Test Alert Rules

Create test file `alert_test.yaml`:

```yaml
rule_files:
  - alert_rules.yaml

evaluation_interval: 1m

tests:
  # Test HighCPU alert fires when CPU > 90%
  - interval: 1m
    input_series:
      - series: 'node_cpu_seconds_total{instance="host1",mode="idle"}'
        values: '100+0x15'  # 100, 100, 100 ... (16 values)
      - series: 'node_cpu_seconds_total{instance="host1",mode="user"}'
        values: '900+10x15'  # 900, 910, 920 ... (high CPU)
    
    alert_rule_test:
      - eval_time: 10m
        alertname: HighCPU
        exp_alerts:
          - exp_labels:
              severity: warning
              instance: host1
            exp_annotations:
              summary: "High CPU usage on host1"
  
  # Test alert does NOT fire when CPU < 90%
  - interval: 1m
    input_series:
      - series: 'node_cpu_seconds_total{instance="host2",mode="idle"}'
        values: '700+0x15'  # Idle 70%
      - series: 'node_cpu_seconds_total{instance="host2",mode="user"}'
        values: '300+0x15'  # User 30%
    
    alert_rule_test:
      - eval_time: 10m
        alertname: HighCPU
        exp_alerts: []  # Should not fire
```

Run tests:
```bash
promtool test rules alert_test.yaml
```

### 4. Simulate Alert Conditions

```bash
# Trigger CPU alert with stress test
stress --cpu 8 --timeout 600s

# Trigger memory alert by filling memory
stress --vm 4 --vm-bytes 8G --timeout 300s

# Trigger disk alert by filling disk
dd if=/dev/zero of=/tmp/bigfile bs=1M count=50000

# Trigger HTTP error alert with curl loop
for i in {1..1000}; do curl -X POST http://myapp/fail; done

# Trigger container OOMKill
kubectl run memory-hog --image=polinux/stress \
  --command -- stress --vm 1 --vm-bytes 1G --vm-hang 0
```

### 5. Verify Alert Routing

```bash
# Send test alert to Alertmanager
amtool alert add \
  alertname=TestAlert \
  severity=warning \
  service=test \
  --alertmanager.url=http://localhost:9093

# Check alert status
amtool alert query --alertmanager.url=http://localhost:9093

# Test routing configuration
amtool config routes test \
  --config.file=alertmanager.yml \
  severity=critical \
  team=infrastructure-team

# Expected output shows which receiver it would route to
```

### 6. Validate Inhibition Rules

```bash
# Send both source and target alerts
amtool alert add \
  alertname=DatabaseDown \
  database=prod \
  severity=critical

amtool alert add \
  alertname=ReplicationLag \
  database=prod \
  severity=warning

# Check which alerts are active (ReplicationLag should be inhibited)
amtool alert query | grep -E "DatabaseDown|ReplicationLag"
```

### 7. Alert Quality Metrics

Track these metrics to monitor alert health:

```promql
# Alert firing rate
rate(ALERTS{alertstate="firing"}[1h])

# Most frequent alerts (potential noise)
topk(10, 
  count_over_time(ALERTS{alertstate="firing"}[7d])
)

# Alerts by severity
count by(severity) (ALERTS{alertstate="firing"})

# Alert flapping (fires/resolves repeatedly)
count_over_time(ALERTS{alertname="HighCPU"}[1h]) > 5

# Time in pending state
ALERTS_FOR_STATE{alertstate="pending"}

# Total active alerts
count(ALERTS{alertstate="firing"})
```

**Create dashboard to track**:
- Alert firing frequency
- Mean time to resolution
- Alert distribution by severity
- Flapping alerts
- Most noisy alerts

### 8. Production Validation Checklist

Before deploying alert rules to production:

- [ ] Syntax validated with `promtool check rules`
- [ ] Expressions tested with `promtool query`
- [ ] Unit tests pass
- [ ] Alert fires in test environment when condition is true
- [ ] Alert does NOT fire when condition is false
- [ ] Alert resolves when condition clears
- [ ] `for` clause duration tested and appropriate
- [ ] Annotations render correctly with actual label values
- [ ] Runbook URL is accessible
- [ ] Alertmanager routing works (test with amtool)
- [ ] Inhibition rules work as expected
- [ ] Team notified of new alerts
- [ ] False positive rate acceptable (< 20%)
- [ ] Cardinality checked (< 1000 time series per alert)

---

## Related Documents

- **Alert Rules Reference** (`alert-rules-ref.md`) - Library of alert examples showing anti-patterns and best practices
- **Alert Tuning Methodology** (`alert-tuning-methodology.md`) - How to analyze and tune existing alerts in production

---

This document provides the operational foundation for effective alerting. Use these patterns and configuration strategies to build a robust, scalable alerting infrastructure.