# Prometheus Alert Rules: Anti-Patterns & Best Practices Reference

## Table of Contents
1. [Introduction](#introduction)
2. [Understanding Alert Anti-Patterns](#understanding-alert-anti-patterns)
3. [Poorly-Configured Alert Examples](#poorly-configured-alert-examples)
4. [Well-Configured Alert Examples](#well-configured-alert-examples)
5. [Side-by-Side Comparisons](#side-by-side-comparisons)
6. [Quick Reference Summary](#quick-reference-summary)

---

## Introduction

This reference document provides a comprehensive library of alert rule examples, showcasing both **anti-patterns** (what NOT to do) and **best practices** (what TO do). Use this as a pattern catalog when writing or reviewing Prometheus alerting rules.

### Why This Matters

- **Alert Fatigue**: Too many noisy alerts cause teams to ignore notifications, missing critical issues
- **False Positives**: Poorly-tuned thresholds trigger on non-issues, wasting engineering time
- **Lack of Context**: Alerts without proper annotations leave responders confused about what to do
- **Scalability Issues**: High-cardinality labels and misconfigured alerts can crash monitoring systems

### How to Use This Document

- **Writing new alerts**: Reference the "Well-Configured" section for your use case
- **Reviewing existing alerts**: Check against "Poorly-Configured" patterns to identify issues
- **Training**: Use side-by-side comparisons to teach alerting best practices
- **Debugging noisy alerts**: Find similar patterns in the anti-patterns section

---

## Understanding Alert Anti-Patterns

### The 10 Most Common Anti-Patterns

1. **Missing `for` Clause**: Alerts fire immediately on transient spikes
2. **Overly Sensitive Thresholds**: Low thresholds create constant noise
3. **Missing or Poor Labels**: Cannot route or prioritize alerts properly
4. **Inadequate Annotations**: Responders don't know what the alert means or how to fix it
5. **Alerting on Raw Metrics**: CPU/memory percentages instead of user-facing symptoms
6. **Using irate() in Alerts**: Creates flapping alerts due to volatility
7. **High-Cardinality Labels**: Dynamic labels like `$value`, `request_id`, or `user_id`
8. **No Alert Grouping**: Individual alerts flood the system instead of being grouped
9. **Absolute Thresholds**: Fixed numbers that don't adapt to traffic patterns
10. **Alerting on Every Error**: Any 5xx error triggers a page immediately

### Detailed Anti-Pattern Explanations

#### Anti-Pattern #1: Missing `for` Clause
**Problem**: Alert fires on the first evaluation where the condition is true, even if it's a momentary spike.

**Impact**: 
- Alert flapping (firing and resolving rapidly)
- Alert fatigue from transient issues
- Cannot distinguish between brief spikes and sustained problems

**Example**:
```yaml
# BAD: No for clause
- alert: HighCPU
  expr: cpu_usage > 80
```

#### Anti-Pattern #2: Overly Sensitive Thresholds
**Problem**: Thresholds set too conservatively (e.g., CPU > 70%, memory > 60%).

**Impact**:
- Constant alerts during normal operations
- Teams become desensitized to alerts
- Real issues get buried in noise

**Example**:
```yaml
# BAD: 70% CPU is often normal
- alert: CPUHigh
  expr: cpu_usage > 70
  for: 1m  # Also too short!
```

#### Anti-Pattern #3: No Severity Labels
**Problem**: All alerts treated equally, no way to prioritize.

**Impact**:
- Cannot route critical alerts differently than warnings
- On-call gets paged for non-urgent issues
- No way to filter or silence by severity

**Example**:
```yaml
# BAD: No severity label
- alert: HighMemory
  expr: memory_usage > 90
  labels:
    team: infrastructure  # Good!
    # Missing: severity
```

#### Anti-Pattern #4: Missing Annotations
**Problem**: Alert has no description, summary, or runbook link.

**Impact**:
- Responders don't know what the alert means
- No guidance on how to investigate or resolve
- Wastes time during incidents

**Example**:
```yaml
# BAD: No annotations
- alert: DatabaseDown
  expr: up{job="database"} == 0
  for: 5m
  labels:
    severity: critical
  # Missing: annotations with context
```

#### Anti-Pattern #5: Using irate() for Alerts
**Problem**: `irate()` only looks at last two data points, very volatile.

**Impact**:
- Alert fires and resolves rapidly (flapping)
- `for` clause doesn't work as expected
- Misses sustained issues if they don't appear in last two points

**Example**:
```yaml
# BAD: irate() is too volatile
- alert: HighTraffic
  expr: irate(http_requests_total[5m]) > 100
  for: 5m  # for clause ineffective with irate()
```

#### Anti-Pattern #6: High-Cardinality Labels
**Problem**: Using unbounded label values like user IDs, request IDs, or dynamic values.

**Impact**:
- Creates thousands or millions of alert instances
- Exhausts memory and storage
- Alertmanager becomes unresponsive

**Example**:
```yaml
# BAD: Dynamic value in label
- alert: SlowRequest
  expr: request_duration > 1
  labels:
    severity: warning
    request_id: "{{ $labels.request_id }}"  # DON'T DO THIS
    current_value: "{{ $value }}"  # ALSO DON'T DO THIS
```

#### Anti-Pattern #7: Alerting on Symptoms, Not Impact
**Problem**: Alerting on CPU/memory/disk without understanding user impact.

**Impact**:
- Alerts fire when there's no user-facing problem
- Can't tell if issue is actually affecting service
- Wastes engineering time

**Example**:
```yaml
# BAD: High CPU might not affect users
- alert: HighCPU
  expr: cpu_usage > 85
  for: 10m
# Better: Alert on increased latency or errors
```

#### Anti-Pattern #8: Absolute Error Count Thresholds
**Problem**: Alert when error count > 100, regardless of total traffic.

**Impact**:
- 100 errors out of 1M requests (0.01%) is fine
- 100 errors out of 200 requests (50%) is critical
- Alert doesn't scale with traffic

**Example**:
```yaml
# BAD: Absolute error count
- alert: TooManyErrors
  expr: sum(rate(http_errors[5m])) > 10
# 10 errors/sec could be 0.1% or 50% depending on traffic
```

#### Anti-Pattern #9: No Alert Grouping
**Problem**: Individual alerts for each instance instead of aggregating.

**Impact**:
- Alert storms (50 instances = 50 alerts)
- Can't see aggregate impact
- Root cause obscured

**Example**:
```yaml
# BAD: Per-instance alerts
- alert: HighMemory
  expr: memory_usage{instance=~".*"} > 90
# Creates separate alert for EACH instance
```

#### Anti-Pattern #10: Alerting on Every Error
**Problem**: Any 5xx error triggers an alert immediately.

**Impact**:
- Transient errors cause pages
- One-off errors are noise
- Team becomes desensitized

**Example**:
```yaml
# BAD: Any error triggers alert
- alert: HTTPErrors
  expr: http_requests_total{status=~"5.."} > 0
# Single error = page
```

---

## Poorly-Configured Alert Examples

Below are 50+ examples of **poorly-configured alerts** demonstrating common anti-patterns. Each example includes the problems and why it's problematic.

### Infrastructure: CPU Alerts

#### ❌ BAD Example 1: No `for` clause
```yaml
groups:
  - name: cpu_bad_examples
    rules:
      - alert: HighCPU
        expr: node_cpu_usage_percent > 80
        labels:
          severity: critical
```
**Problems**:
- Fires immediately on any spike
- No time tolerance
- Will flap constantly

#### ❌ BAD Example 2: Too sensitive threshold
```yaml
      - alert: CPUHigh
        expr: 100 - (avg by(instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 70
        for: 1m
        labels:
          severity: page
```
**Problems**:
- 70% CPU is often normal
- 1m is too short
- Will create constant noise
- Using irate() (also problematic)

#### ❌ BAD Example 3: Using irate() for alerting
```yaml
      - alert: CPUSpike
        expr: irate(node_cpu_seconds_total[5m]) > 0.8
        for: 5m
```
**Problems**:
- `irate()` is too volatile
- `for` clause doesn't work well with `irate()`
- Will miss sustained high CPU

#### ❌ BAD Example 4: No labels or annotations
```yaml
      - alert: CPU
        expr: cpu_usage > 90
        for: 2m
```
**Problems**:
- No severity label for routing
- No annotations explaining the issue
- No context for responders
- Vague alert name

#### ❌ BAD Example 5: High-cardinality label
```yaml
      - alert: HighCPUWithValue
        expr: node_cpu_usage > 85
        for: 3m
        labels:
          severity: warning
          current_value: "{{ $value }}"  # DON'T DO THIS
```
**Problems**:
- `current_value` changes every evaluation
- Creates new alert instance each time
- Causes alert explosion

### Infrastructure: Memory Alerts

#### ❌ BAD Example 6: Too sensitive memory threshold
```yaml
      - alert: HighMemory
        expr: node_memory_usage_percent > 70
        labels:
          severity: critical
```
**Problems**:
- No `for` clause
- 70% is often normal for caching
- No context about memory type
- Critical severity too aggressive

#### ❌ BAD Example 7: Alerting on cache memory
```yaml
      - alert: MemoryPressure
        expr: node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes > 8000000000
        for: 1m
```
**Problems**:
- Absolute threshold in bytes (8GB)
- Doesn't account for total memory size
- 1m is too short
- Doesn't use MemAvailable properly

#### ❌ BAD Example 8: Missing severity
```yaml
      - alert: OutOfMemory
        expr: node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes * 100 < 10
        for: 2m
        annotations:
          description: "Low memory"
```
**Problems**:
- No severity label
- Vague description
- No runbook link
- 2m might be too short for memory issues

#### ❌ BAD Example 9: No grouping consideration
```yaml
      - alert: MemoryIssue
        expr: memory_used_percent{job="node"} > 80
        for: 5m
        labels:
          instance: "{{ $labels.instance }}"  # Redundant, already exists
```
**Problems**:
- Redundant label
- Will create separate alert per instance
- Should use alert grouping instead

### Infrastructure: Disk Alerts

#### ❌ BAD Example 10: Immediate disk full alert
```yaml
      - alert: DiskFull
        expr: node_filesystem_avail_bytes / node_filesystem_size_bytes * 100 < 15
```
**Problems**:
- No `for` clause
- 15% might be hours away from full
- No prediction of when disk will fill
- Doesn't exclude tmpfs

#### ❌ BAD Example 11: All filesystems treated equally
```yaml
      - alert: LowDisk
        expr: disk_free_percent < 20
        for: 5m
        labels:
          severity: critical
```
**Problems**:
- Alerts on temp filesystems equally
- Should exclude tmpfs, devtmpfs
- 20% for 100TB is different than 1GB disk
- No filesystem type filtering

#### ❌ BAD Example 12: No mountpoint context
```yaml
      - alert: DiskSpace
        expr: node_filesystem_avail_bytes < 10000000000  # 10GB
        for: 10m
```
**Problems**:
- Absolute threshold (10GB)
- No indication which mountpoint
- 10GB might be fine or critical depending on disk size

#### ❌ BAD Example 13: Using wrong metric
```yaml
      - alert: DiskUsage
        expr: node_filesystem_size_bytes > 1000000000000
        for: 5m
        labels:
          severity: warning
```
**Problems**:
- Alerting on total size, not usage
- Wrong metric entirely
- Will fire once and never resolve
- Makes no sense

### Application: HTTP Error Alerts

#### ❌ BAD Example 14: Alert on any 5xx error
```yaml
      - alert: HTTPErrors
        expr: http_requests_total{status=~"5.."} > 0
```
**Problems**:
- Fires on single error
- No `for` clause
- Doesn't consider total request volume
- Counter value, not rate

#### ❌ BAD Example 15: Absolute error count
```yaml
      - alert: TooManyErrors
        expr: sum(rate(http_requests_total{status=~"5.."}[5m])) > 10
        for: 2m
        labels:
          severity: critical
```
**Problems**:
- Absolute count doesn't scale
- 10 errors/sec out of 1000 req/sec is fine
- 10 errors/sec out of 20 req/sec is disaster
- No context on total traffic

#### ❌ BAD Example 16: Per-endpoint alerts
```yaml
      - alert: EndpointErrors
        expr: rate(http_requests_total{status="500"}[5m]) > 1
        for: 3m
        labels:
          endpoint: "{{ $labels.path }}"  # High cardinality!
```
**Problems**:
- Path creates high cardinality
- Will create hundreds of alerts
- Should aggregate or use recording rules

#### ❌ BAD Example 17: Mixing 4xx and 5xx
```yaml
      - alert: HTTPErrorRate
        expr: rate(http_requests_total{status=~"[45].."}[5m]) > 0.05
        for: 5m
```
**Problems**:
- 4xx errors are often expected (client errors)
- Mixes server errors with client errors
- Wrong signal for alerting

### Application: Latency Alerts

#### ❌ BAD Example 18: Average latency threshold
```yaml
      - alert: SlowAPI
        expr: avg(http_request_duration_seconds) > 1
        for: 5m
```
**Problems**:
- Average is misleading (one slow request skews it)
- Should use percentiles (p95, p99)
- 1 second might be fine or terrible depending on endpoint
- No aggregation labels

#### ❌ BAD Example 19: irate() for latency
```yaml
      - alert: LatencySpike
        expr: irate(http_request_duration_seconds_sum[5m]) > 2
        for: 3m
```
**Problems**:
- `irate()` inappropriate for latency
- Looking at sum, not rate or percentile
- Flapping alert
- Wrong calculation

#### ❌ BAD Example 20: No percentile
```yaml
      - alert: RequestSlow
        expr: histogram_quantile(0.5, http_request_duration_seconds_bucket) > 0.5
        for: 5m
        labels:
          severity: page
```
**Problems**:
- Using p50 (median) instead of p95/p99
- Median doesn't show tail latency
- Missing outliers that affect users
- Paging on median is too aggressive

### Database Alerts

#### ❌ BAD Example 21: Connection count without context
```yaml
      - alert: TooManyConnections
        expr: db_connections > 100
        for: 2m
```
**Problems**:
- Absolute number without max connections context
- 100 of 1000 is fine, 100 of 120 is critical
- No `severity` label
- No percentage calculation

#### ❌ BAD Example 22: Query time without aggregation
```yaml
      - alert: SlowQuery
        expr: mysql_query_duration_seconds > 5
        labels:
          severity: warning
```
**Problems**:
- No `for` clause
- Single slow query triggers alert
- Should use rate() or percentile
- Counter metric used directly

#### ❌ BAD Example 23: Replication lag absolute
```yaml
      - alert: ReplicationLag
        expr: mysql_slave_lag_seconds > 60
        for: 1m
        labels:
          severity: critical
```
**Problems**:
- 60 seconds might be acceptable
- Too short `for` duration (1m)
- No context on impact
- Critical severity too aggressive

### Message Queue Alerts

#### ❌ BAD Example 24: Queue depth without rate
```yaml
      - alert: QueueBacklog
        expr: queue_depth > 1000
```
**Problems**:
- No `for` clause
- Doesn't show if queue is growing or shrinking
- Absolute number without context
- 1000 might be normal backlog

#### ❌ BAD Example 25: Consumer lag single threshold
```yaml
      - alert: ConsumerLag
        expr: kafka_consumer_lag > 10000
        for: 5m
        labels:
          severity: critical
```
**Problems**:
- Same threshold for all topics
- Doesn't consider message rate
- Some topics might always have lag
- No percentage calculation

### Kubernetes Alerts

#### ❌ BAD Example 26: Pod restarts without time window
```yaml
      - alert: PodRestarting
        expr: rate(kube_pod_container_status_restarts_total[5m]) > 0
```
**Problems**:
- Triggers on single restart
- No `for` clause
- No severity differentiation
- Too sensitive

#### ❌ BAD Example 27: OOM kills too sensitive
```yaml
      - alert: PodOOMKilled
        expr: increase(kube_pod_container_status_terminated_reason{reason="OOMKilled"}[5m]) > 0
        for: 1m
```
**Problems**:
- 1m is too short
- Single OOM might be acceptable
- Should check for repeated OOMs
- Too aggressive

#### ❌ BAD Example 28: Pending pods immediate
```yaml
      - alert: PodsPending
        expr: kube_pod_status_phase{phase="Pending"} > 0
        labels:
          severity: page
```
**Problems**:
- No `for` clause (pods can be briefly pending)
- Severity too high
- No context on how long pending
- Paging on any pending pod

### Service Health Alerts

#### ❌ BAD Example 29: Target down immediate
```yaml
      - alert: ServiceDown
        expr: up{job="myapp"} == 0
```
**Problems**:
- No `for` clause
- Single scrape failure triggers alert
- Network blips cause false alerts
- No instance count context

#### ❌ BAD Example 30: Health check without aggregation
```yaml
      - alert: UnhealthyInstance
        expr: probe_success == 0
        for: 30s
        labels:
          severity: critical
```
**Problems**:
- 30s is too short
- Should check multiple instances
- No instance identification in annotations
- Per-instance instead of service-level

### Certificate Expiry Alerts

#### ❌ BAD Example 31: Certificate expiry too late
```yaml
      - alert: CertExpiring
        expr: (probe_ssl_earliest_cert_expiry - time()) / 86400 < 7
        for: 1h
```
**Problems**:
- 7 days too short for remediation
- Should have multiple warnings (30d, 14d, 7d)
- No severity escalation
- Only one warning level

#### ❌ BAD Example 32: No certificate subject
```yaml
      - alert: SSLCertExpiry
        expr: probe_ssl_earliest_cert_expiry - time() < 604800
        labels:
          severity: warning
        annotations:
          summary: "Certificate expiring soon"
```
**Problems**:
- Doesn't identify which certificate
- Vague annotation
- No runbook
- No subject or domain info

### Network Alerts

#### ❌ BAD Example 33: Network errors immediate
```yaml
      - alert: NetworkErrors
        expr: rate(node_network_receive_errs_total[5m]) > 0
```
**Problems**:
- No `for` clause
- Any error triggers alert
- Should have threshold based on total packets
- Too sensitive

#### ❌ BAD Example 34: Bandwidth absolute
```yaml
      - alert: HighBandwidth
        expr: rate(node_network_receive_bytes_total[5m]) > 1000000
        for: 5m
```
**Problems**:
- Absolute bandwidth threshold
- Doesn't account for interface capacity
- 1MB/s might be normal or critical
- No percentage of capacity

### Custom Application Metrics

#### ❌ BAD Example 35: Business metric without context
```yaml
      - alert: LowRevenue
        expr: revenue_total < 1000
        for: 5m
```
**Problems**:
- Absolute threshold
- Doesn't account for time of day
- Should use rate or compare to baseline
- No context on normal values

#### ❌ BAD Example 36: User count drop
```yaml
      - alert: UserDropoff
        expr: active_users < 500
        labels:
          severity: critical
```
**Problems**:
- No `for` clause
- Doesn't account for daily patterns
- Absolute number doesn't scale
- No baseline comparison

### Cache Alerts

#### ❌ BAD Example 37: Cache hit rate too strict
```yaml
      - alert: LowCacheHitRate
        expr: cache_hit_rate < 0.99
        for: 10m
```
**Problems**:
- 99% might be unrealistic for some caches
- No context on cache warming
- Fixed threshold for all cache types
- Too strict

#### ❌ BAD Example 38: Cache evictions
```yaml
      - alert: CacheEvictions
        expr: rate(cache_evictions_total[5m]) > 0
        labels:
          severity: warning
```
**Problems**:
- Evictions are normal in LRU caches
- No `for` clause
- Any eviction triggers alert
- Wrong signal

### Load Balancer Alerts

#### ❌ BAD Example 39: Backend down without grace
```yaml
      - alert: BackendDown
        expr: haproxy_backend_up == 0
```
**Problems**:
- No `for` clause
- Deployments cause false alerts
- No context on total backends
- Too immediate

#### ❌ BAD Example 40: Connection queue depth
```yaml
      - alert: ConnectionQueueing
        expr: haproxy_backend_current_queue > 0
        for: 1m
```
**Problems**:
- Any queueing triggers alert
- Brief queuing is normal
- No threshold on queue depth
- Too sensitive

### DNS Alerts

#### ❌ BAD Example 41: DNS query failures
```yaml
      - alert: DNSFailures
        expr: rate(dns_query_failures_total[5m]) > 0
```
**Problems**:
- Single failure triggers alert
- No `for` clause
- Should use percentage of total queries
- Too sensitive

### Storage System Alerts

#### ❌ BAD Example 42: IOPS threshold absolute
```yaml
      - alert: HighIOPS
        expr: rate(node_disk_io_time_seconds_total[5m]) > 100
        for: 5m
```
**Problems**:
- Absolute IOPS number
- Doesn't account for disk capabilities
- Different for SSD vs HDD
- No capacity percentage

#### ❌ BAD Example 43: Disk saturation
```yaml
      - alert: DiskSaturated
        expr: node_disk_io_time_weighted_seconds_total > 1
        labels:
          severity: page
```
**Problems**:
- No rate() function
- No `for` clause
- Counter value used directly
- Will never resolve

### API Gateway Alerts

#### ❌ BAD Example 44: Rate limit hits
```yaml
      - alert: RateLimitHit
        expr: rate(api_rate_limit_exceeded_total[5m]) > 0
```
**Problems**:
- Rate limiting is expected behavior
- Should alert on percentage, not any hits
- No `for` clause
- Wrong signal

### Authentication Service Alerts

#### ❌ BAD Example 45: Login failures absolute
```yaml
      - alert: LoginFailures
        expr: rate(auth_login_failures_total[5m]) > 5
        for: 2m
        labels:
          severity: critical
```
**Problems**:
- Absolute number doesn't scale
- 5 failures out of 1000 logins is normal
- Should use percentage
- No total login context

### Service Dependencies

#### ❌ BAD Example 46: Dependency timeout
```yaml
      - alert: DependencyTimeout
        expr: rate(external_service_timeout_total[5m]) > 0
        labels:
          severity: page
```
**Problems**:
- Single timeout pages team
- External service might have issues
- Should have circuit breaker logic
- Too aggressive

### Batch Job Alerts

#### ❌ BAD Example 47: Job failure immediate
```yaml
      - alert: BatchJobFailed
        expr: batch_job_status{status="failed"} == 1
```
**Problems**:
- No `for` clause
- Jobs might retry
- No context on which job
- Too immediate

#### ❌ BAD Example 48: Job duration fixed threshold
```yaml
      - alert: JobTooSlow
        expr: batch_job_duration_seconds > 3600
        for: 5m
        labels:
          severity: warning
```
**Problems**:
- Same threshold for all jobs
- Some jobs should take longer
- No baseline comparison
- Fixed 1 hour threshold

### Garbage Collection Alerts

#### ❌ BAD Example 49: GC pause time
```yaml
      - alert: LongGCPause
        expr: jvm_gc_pause_seconds > 1
        labels:
          severity: critical
```
**Problems**:
- No rate() or aggregation
- Single long pause triggers alert
- Should look at frequency and percentiles
- No `for` clause

### Thread Pool Alerts

#### ❌ BAD Example 50: Thread pool exhaustion
```yaml
      - alert: ThreadPoolFull
        expr: thread_pool_active_threads / thread_pool_max_threads > 0.9
        for: 1m
```
**Problems**:
- 1m too short
- 90% might be normal under load
- No context on queue depth
- Too aggressive

### Container Resource Alerts

#### ❌ BAD Example 51: Container CPU throttling
```yaml
      - alert: ContainerThrottled
        expr: rate(container_cpu_cfs_throttled_seconds_total[5m]) > 0
```
**Problems**:
- Any throttling triggers alert
- Brief throttling is normal
- Should use percentage of total CPU time
- No `for` clause

### Service Mesh Alerts

#### ❌ BAD Example 52: Circuit breaker open
```yaml
      - alert: CircuitBreakerOpen
        expr: circuit_breaker_state == 1
        labels:
          severity: page
```
**Problems**:
- Circuit breakers are designed to open
- No `for` clause
- Should alert if stuck open
- Paging on expected behavior

---

## Well-Configured Alert Examples

Below are 30 examples of **well-configured alerts** demonstrating best practices. Each example includes explanations of why it's effective.

### Infrastructure: CPU Alerts

#### ✅ GOOD Example 1: Proper CPU alert with time tolerance
```yaml
groups:
  - name: cpu_best_practices
    rules:
      - alert: HighCPUUsage
        expr: |
          100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 90
        for: 15m
        labels:
          severity: warning
          team: infrastructure
          component: compute
        annotations:
          summary: "High CPU usage on {{ $labels.instance }}"
          description: |
            CPU usage is {{ $value | humanizePercentage }} on {{ $labels.instance }}.
            This has persisted for 15 minutes and may impact application performance.
          runbook_url: "https://runbooks.example.com/high-cpu"
          dashboard_url: "https://grafana.example.com/d/node-dashboard?var-instance={{ $labels.instance }}"
```
**Why it's good**:
- Uses `rate()` instead of `irate()` for stability
- 15m `for` clause prevents flapping on transient spikes
- Proper severity labels for routing (warning, not critical)
- Multiple routing labels (team, component)
- Rich annotations with context and value
- Links to runbook and dashboard for quick investigation
- 90% threshold is appropriate for action

#### ✅ GOOD Example 2: Critical CPU with escalation
```yaml
      - alert: CriticalCPUUsage
        expr: |
          100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 95
        for: 10m
        labels:
          severity: critical
          team: infrastructure
          component: compute
          alert_type: resource_exhaustion
        annotations:
          summary: "Critical CPU usage on {{ $labels.instance }}"
          description: |
            CPU usage has exceeded 95% (current: {{ $value | humanizePercentage }}) 
            on {{ $labels.instance }} for more than 10 minutes.
            
            This requires immediate attention to prevent service degradation.
            
            Immediate actions:
            1. Check top processes consuming CPU
            2. Review recent deployments
            3. Consider scaling horizontally
          runbook_url: "https://runbooks.example.com/critical-cpu"
          pagerduty_priority: "P1"
```
**Why it's good**:
- Higher threshold (95%) for critical severity
- Shorter `for` duration (10m) for urgent issues
- Detailed remediation steps in description
- Multiple routing labels including alert_type
- PagerDuty integration hint for P1 escalation
- Clear escalation from warning to critical

#### ✅ GOOD Example 3: CPU with team routing
```yaml
      - alert: HighCPUByService
        expr: |
          avg by(service, environment) (
            rate(container_cpu_usage_seconds_total[5m])
          ) * 100 > 80
        for: 20m
        labels:
          severity: warning
          team: "{{ $labels.service }}-team"
          environment: "{{ $labels.environment }}"
        annotations:
          summary: "High CPU for service {{ $labels.service }}"
          description: |
            Service {{ $labels.service }} in {{ $labels.environment }} 
            is experiencing {{ $value | humanizePercentage }} CPU usage.
            
            Check if this is expected behavior or requires optimization.
          runbook_url: "https://runbooks.example.com/service-cpu/{{ $labels.service }}"
```
**Why it's good**:
- Aggregates by service for better grouping
- Dynamic team routing based on service name
- Environment-aware alerting
- Service-specific runbook URLs
- 20m for clause appropriate for service-level

### Infrastructure: Memory Alerts

#### ✅ GOOD Example 4: Memory pressure with proper calculation
```yaml
      - alert: HighMemoryPressure
        expr: |
          (
            node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes
          ) / node_memory_MemTotal_bytes * 100 > 90
        for: 10m
        labels:
          severity: warning
          team: infrastructure
          component: memory
        annotations:
          summary: "High memory pressure on {{ $labels.instance }}"
          description: |
            Memory usage is at {{ $value | humanizePercentage }} on {{ $labels.instance }}.
            Available memory: {{ query "node_memory_MemAvailable_bytes{instance='{{ $labels.instance }}'}" | first | value | humanize1024 }}
            
            Consider:
            - Checking for memory leaks
            - Reviewing OOM events
            - Scaling instance memory
          runbook_url: "https://runbooks.example.com/memory-pressure"
```
**Why it's good**:
- Uses MemAvailable (includes reclaimable cache)
- Percentage-based works for any instance size
- Includes current available memory in description
- Actionable remediation steps
- 10m for clause appropriate for memory issues

#### ✅ GOOD Example 5: Memory prediction alert
```yaml
      - alert: MemoryWillExhaustSoon
        expr: |
          predict_linear(node_memory_MemAvailable_bytes[1h], 4 * 3600) < 0
        for: 15m
        labels:
          severity: warning
          team: infrastructure
          alert_type: predictive
        annotations:
          summary: "Memory will exhaust in ~4 hours on {{ $labels.instance }}"
          description: |
            Based on current trends, {{ $labels.instance }} will run out of memory 
            in approximately 4 hours.
            
            Current available: {{ query "node_memory_MemAvailable_bytes{instance='{{ $labels.instance }}'}" | first | value | humanize1024 }}
            
            Take action now to prevent OOM events.
          runbook_url: "https://runbooks.example.com/memory-exhaustion-prediction"
```
**Why it's good**:
- Predictive alerting prevents issues before they occur
- Gives time to remediate (4 hours warning)
- Clear time horizon in summary
- Marked as predictive alert type
- Proactive rather than reactive

### Infrastructure: Disk Alerts

#### ✅ GOOD Example 6: Disk space with proper filtering
```yaml
      - alert: DiskSpaceLow
        expr: |
          (
            node_filesystem_avail_bytes{fstype!~"tmpfs|fuse.*|overlay"} 
            / node_filesystem_size_bytes{fstype!~"tmpfs|fuse.*|overlay"}
          ) * 100 < 15
        for: 30m
        labels:
          severity: warning
          team: infrastructure
          component: storage
        annotations:
          summary: "Low disk space on {{ $labels.instance }}:{{ $labels.mountpoint }}"
          description: |
            Disk space is {{ $value | humanizePercentage }} available on:
            - Instance: {{ $labels.instance }}
            - Mountpoint: {{ $labels.mountpoint }}
            - Filesystem: {{ $labels.fstype }}
            
            Available: {{ query "node_filesystem_avail_bytes{instance='{{ $labels.instance }}', mountpoint='{{ $labels.mountpoint }}'}" | first | value | humanize1024 }}
            Total: {{ query "node_filesystem_size_bytes{instance='{{ $labels.instance }}', mountpoint='{{ $labels.mountpoint }}'}" | first | value | humanize1024 }}
          runbook_url: "https://runbooks.example.com/disk-space"
```
**Why it's good**:
- Excludes temporary filesystems (tmpfs, overlay)
- Percentage-based threshold scales with disk size
- Identifies exact mountpoint affected
- Shows both available and total space
- 30m for clause appropriate for disk issues

#### ✅ GOOD Example 7: Disk will fill prediction
```yaml
      - alert: DiskWillFillIn4Hours
        expr: |
          (
            node_filesystem_avail_bytes{fstype!~"tmpfs|fuse.*|overlay"}
            / node_filesystem_size_bytes{fstype!~"tmpfs|fuse.*|overlay"}
          ) > 0.1
          and
          predict_linear(node_filesystem_avail_bytes{fstype!~"tmpfs|fuse.*|overlay"}[1h], 4 * 3600) < 0
        for: 15m
        labels:
          severity: critical
          team: infrastructure
          alert_type: predictive
        annotations:
          summary: "Disk {{ $labels.mountpoint }} will fill in ~4 hours on {{ $labels.instance }}"
          description: |
            At current fill rate, disk will be full in approximately 4 hours.
            
            Mountpoint: {{ $labels.mountpoint }}
            Current available: {{ query "node_filesystem_avail_bytes{instance='{{ $labels.instance }}', mountpoint='{{ $labels.mountpoint }}'}" | first | value | humanize1024 }}
            
            Immediate actions required:
            1. Identify large files/logs
            2. Clear old data
            3. Consider expanding storage
          runbook_url: "https://runbooks.example.com/disk-filling-fast"
```
**Why it's good**:
- Predictive with time horizon (4 hours)
- Prevents disk full events proactively
- Critical severity for urgency
- Clear action items in numbered list
- Combines current state check with prediction

### Application: HTTP Error Alerts

#### ✅ GOOD Example 8: Error rate percentage-based
```yaml
      - alert: HighHTTP5xxErrorRate
        expr: |
          (
            sum(rate(http_requests_total{status=~"5.."}[5m])) by (service)
            /
            sum(rate(http_requests_total[5m])) by (service)
          ) * 100 > 1
        for: 10m
        labels:
          severity: warning
          team: "{{ $labels.service }}-team"
          component: application
        annotations:
          summary: "High 5xx error rate for {{ $labels.service }}"
          description: |
            Service {{ $labels.service }} is experiencing {{ $value | humanizePercentage }} 5xx errors.
            
            Error rate: {{ query "sum(rate(http_requests_total{service='{{ $labels.service }}', status=~'5..'}[5m]))" | first | value | humanize }}/s
            Total rate: {{ query "sum(rate(http_requests_total{service='{{ $labels.service }}'}[5m]))" | first | value | humanize }}/s
            
            Check application logs and recent deployments.
          runbook_url: "https://runbooks.example.com/5xx-errors"
          dashboard_url: "https://grafana.example.com/d/service-{{ $labels.service }}"
```
**Why it's good**:
- Percentage-based, scales automatically with traffic
- Aggregated by service, not per-instance
- Shows both error rate and total rate for context
- Dynamic team routing by service
- Links to both runbook and dashboard

#### ✅ GOOD Example 9: SLO-based error budget alert (fast burn)
```yaml
      - alert: ErrorBudgetBurnRateCritical
        expr: |
          (
            sum(rate(http_requests_total{status=~"5.."}[1h])) by (service)
            /
            sum(rate(http_requests_total[1h])) by (service)
          ) > (1 - 0.999) * 14.4  # 99.9% SLO, 14.4x burn rate
        for: 5m
        labels:
          severity: critical
          team: "{{ $labels.service }}-team"
          slo: "true"
          burn_rate: "fast"
        annotations:
          summary: "Fast error budget burn for {{ $labels.service }}"
          description: |
            Service {{ $labels.service }} is burning through error budget at 14.4x the normal rate.
            At this rate, the monthly error budget will be exhausted in ~2 hours.
            
            Current error rate: {{ $value | humanizePercentage }}
            SLO target: 99.9% success rate
            
            This requires immediate attention.
          runbook_url: "https://runbooks.example.com/error-budget-burn"
```
**Why it's good**:
- SLO-based alerting aligned with business objectives
- Multi-window burn rate detection (fast burn)
- Critical for fast burn (2% budget in 1 hour)
- Clear impact statement (budget exhaustion time)
- Labeled as SLO alert for proper routing

#### ✅ GOOD Example 10: SLO-based error budget alert (slow burn)
```yaml
      - alert: ErrorBudgetBurnRateSlow
        expr: |
          (
            sum(rate(http_requests_total{status=~"5.."}[6h])) by (service)
            /
            sum(rate(http_requests_total[6h])) by (service)
          ) > (1 - 0.999) * 6  # 99.9% SLO, 6x burn rate
        for: 30m
        labels:
          severity: warning
          team: "{{ $labels.service }}-team"
          slo: "true"
          burn_rate: "slow"
        annotations:
          summary: "Elevated error rate for {{ $labels.service }}"
          description: |
            Service {{ $labels.service }} has sustained elevated errors for 6+ hours.
            At this rate, 5% of monthly error budget will be consumed.
            
            Current error rate: {{ $value | humanizePercentage }}
            SLO target: 99.9% success rate
            
            Investigate and address to prevent SLO violation.
          runbook_url: "https://runbooks.example.com/sustained-errors"
```
**Why it's good**:
- Catches sustained issues with longer window (6h)
- Different severity than fast burn (warning vs critical)
- Longer time windows and for duration (30m)
- Explains budget impact clearly
- Complementary to fast burn alert

### Application: Latency Alerts

#### ✅ GOOD Example 11: P99 latency with histogram
```yaml
      - alert: HighP99Latency
        expr: |
          histogram_quantile(0.99,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (service, le)
          ) > 1
        for: 15m
        labels:
          severity: warning
          team: "{{ $labels.service }}-team"
          component: performance
        annotations:
          summary: "High P99 latency for {{ $labels.service }}"
          description: |
            The 99th percentile latency for {{ $labels.service }} is {{ $value }}s.
            
            This means 1% of requests are taking longer than 1 second.
            
            P95: {{ query "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{service='{{ $labels.service }}'}[5m])) by (le))" | first | value }}s
            P99: {{ $value }}s
            
            Check for:
            - Slow database queries
            - External service timeouts
            - Resource contention
          runbook_url: "https://runbooks.example.com/high-latency"
```
**Why it's good**:
- Uses P99 percentile, not average
- Histogram-based calculation (accurate)
- Shows multiple percentiles for context
- Specific investigation steps
- Explains impact (1% of requests affected)

#### ✅ GOOD Example 12: Latency SLO burn rate
```yaml
      - alert: LatencySLOBurnRate
        expr: |
          (
            sum(rate(http_request_duration_seconds_bucket{le="0.5"}[1h])) by (service)
            /
            sum(rate(http_request_duration_seconds_count[1h])) by (service)
          ) < 0.95  # 95% of requests under 500ms SLO
        for: 10m
        labels:
          severity: warning
          team: "{{ $labels.service }}-team"
          slo: "latency"
        annotations:
          summary: "Latency SLO violation for {{ $labels.service }}"
          description: |
            Only {{ $value | humanizePercentage }} of requests are completing within 500ms.
            SLO target: 95% of requests under 500ms
            
            Current percentile performance:
            P50: {{ query "histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket{service='{{ $labels.service }}'}[5m])) by (le))" | first | value }}s
            P95: {{ query "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{service='{{ $labels.service }}'}[5m])) by (le))" | first | value }}s
            P99: {{ query "histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{service='{{ $labels.service }}'}[5m])) by (le))" | first | value }}s
          runbook_url: "https://runbooks.example.com/latency-slo"
```
**Why it's good**:
- SLO-based latency alerting
- Uses histogram buckets efficiently
- Shows all key percentiles (P50, P95, P99)
- Clear SLO target stated in description
- Measures compliance, not just latency

### Database Alerts

#### ✅ GOOD Example 13: Connection pool exhaustion
```yaml
      - alert: DatabaseConnectionPoolNearLimit
        expr: |
          (
            db_connections_active
            /
            db_connections_max
          ) * 100 > 85
        for: 10m
        labels:
          severity: warning
          team: database
          component: connection_pool
        annotations:
          summary: "Database {{ $labels.database }} connection pool at {{ $value | humanizePercentage }}"
          description: |
            Connection pool utilization is {{ $value | humanizePercentage }} for {{ $labels.database }}.
            
            Active connections: {{ query "db_connections_active{database='{{ $labels.database }}'}" | first | value }}
            Max connections: {{ query "db_connections_max{database='{{ $labels.database }}'}" | first | value }}
            
            Action items:
            1. Review connection leak in application
            2. Analyze slow queries holding connections
            3. Consider increasing max_connections
          runbook_url: "https://runbooks.example.com/db-connections"
```
**Why it's good**:
- Percentage of max, not absolute count
- Shows actual numbers in description
- Specific troubleshooting steps
- Warning before complete exhaustion (85%)
- Database-specific context

#### ✅ GOOD Example 14: Replication lag with context
```yaml
      - alert: DatabaseReplicationLagHigh
        expr: |
          mysql_slave_lag_seconds > 300
        for: 15m
        labels:
          severity: warning
          team: database
          component: replication
        annotations:
          summary: "Replication lag {{ $value }}s on {{ $labels.instance }}"
          description: |
            Replica {{ $labels.instance }} is {{ $value }} seconds behind master.
            
            This may cause:
            - Stale reads from replica
            - Backup delays
            - Failover issues
            
            Check for:
            - Long-running transactions on master
            - Network issues
            - Replica resource constraints
          runbook_url: "https://runbooks.example.com/replication-lag"
```
**Why it's good**:
- Reasonable threshold (5 minutes/300s)
- Explains business impact clearly
- Multiple investigation paths
- 15m `for` prevents brief lag alerts
- Balanced severity (warning, not critical)

### Message Queue Alerts

#### ✅ GOOD Example 15: Queue depth with growth rate
```yaml
      - alert: QueueDepthGrowing
        expr: |
          (
            queue_depth
            and
            deriv(queue_depth[15m]) > 10
          ) > 1000
        for: 20m
        labels:
          severity: warning
          team: messaging
          component: queue
        annotations:
          summary: "Queue {{ $labels.queue }} is growing"
          description: |
            Queue {{ $labels.queue }} depth is {{ $value }} and growing at 
            {{ query "deriv(queue_depth{queue='{{ $labels.queue }}'}[15m])" | first | value }} messages/second.
            
            This indicates consumers are falling behind producers.
            
            Actions:
            1. Scale consumer instances
            2. Check for consumer errors
            3. Review message processing time
          runbook_url: "https://runbooks.example.com/queue-backlog"
```
**Why it's good**:
- Combines depth AND growth rate
- Distinguishes growing vs stable backlog
- Shows rate of growth in description
- Actionable remediation steps
- 20m for clause prevents noise

### Kubernetes Alerts

#### ✅ GOOD Example 16: Pod restart loop detection
```yaml
      - alert: PodCrashLooping
        expr: |
          rate(kube_pod_container_status_restarts_total[15m]) > 0.1
        for: 15m
        labels:
          severity: critical
          team: platform
          component: kubernetes
        annotations:
          summary: "Pod {{ $labels.namespace }}/{{ $labels.pod }} is crash looping"
          description: |
            Pod {{ $labels.pod }} in namespace {{ $labels.namespace }} is restarting 
            {{ $value }} times per second.
            
            Container: {{ $labels.container }}
            
            Actions:
            1. Check pod logs: kubectl logs -n {{ $labels.namespace }} {{ $labels.pod }} --previous
            2. Describe pod: kubectl describe pod -n {{ $labels.namespace }} {{ $labels.pod }}
            3. Review recent changes
          runbook_url: "https://runbooks.example.com/crash-loop"
```
**Why it's good**:
- Uses rate to detect looping pattern
- Threshold (0.1/s) prevents single restart alerts
- Provides kubectl commands for investigation
- Identifies namespace, pod, and container
- 15m for clause confirms crash loop pattern

### Service Health Alerts

#### ✅ GOOD Example 17: Service down with multi-instance awareness
```yaml
      - alert: ServiceDown
        expr: |
          avg by(job) (up{job="myapp"}) < 0.5
        for: 5m
        labels:
          severity: critical
          team: application
          component: availability
        annotations:
          summary: "Service {{ $labels.job }} has multiple instances down"
          description: |
            More than 50% of {{ $labels.job }} instances are down.
            
            Healthy instances: {{ query "sum(up{job='{{ $labels.job }}'})" | first | value }}
            Total instances: {{ query "count(up{job='{{ $labels.job }}'})" | first | value }}
            
            This is a critical availability issue requiring immediate attention.
            
            Check:
            1. Recent deployments
            2. Infrastructure health
            3. Load balancer health checks
          runbook_url: "https://runbooks.example.com/service-down"
```
**Why it's good**:
- Requires multiple instances down (> 50%)
- Shows healthy vs total instances
- Critical severity for major outage
- Multiple investigation paths
- Doesn't alert on single instance failure

### Certificate Expiry Alerts

#### ✅ GOOD Example 18: Multi-stage certificate warning
```yaml
      - alert: CertificateExpiringSoon30d
        expr: |
          (probe_ssl_earliest_cert_expiry - time()) / 86400 < 30
        for: 6h
        labels:
          severity: warning
          team: security
          component: certificates
        annotations:
          summary: "Certificate for {{ $labels.instance }} expires in {{ $value }} days"
          description: |
            SSL certificate for {{ $labels.instance }} will expire in {{ $value }} days.
            
            Certificate subject: {{ $labels.subject }}
            Expiry date: {{ probe_ssl_earliest_cert_expiry }}
            
            Renew certificate soon to avoid service disruption.
          runbook_url: "https://runbooks.example.com/cert-renewal"
```
**Why it's good**:
- 30 days gives adequate time to renew
- Identifies certificate subject and instance
- Shows expiry date for planning
- Warning severity appropriate for 30 days
- 6h for clause prevents flapping

#### ✅ GOOD Example 19: Critical certificate expiry
```yaml
      - alert: CertificateExpiryCritical7d
        expr: |
          (probe_ssl_earliest_cert_expiry - time()) / 86400 < 7
        for: 1h
        labels:
          severity: critical
          team: security
          component: certificates
        annotations:
          summary: "URGENT: Certificate for {{ $labels.instance }} expires in {{ $value }} days"
          description: |
            SSL certificate for {{ $labels.instance }} expires in {{ $value }} days!
            
            This is URGENT. Service will fail if certificate expires.
            
            Certificate subject: {{ $labels.subject }}
            Expiry: {{ probe_ssl_earliest_cert_expiry }}
            
            Renew immediately.
          runbook_url: "https://runbooks.example.com/cert-renewal-urgent"
          pagerduty_priority: "P1"
```
**Why it's good**:
- Escalated severity for urgency (7 days)
- Clear urgency in message ("URGENT")
- Same metric, different threshold (multi-tier)
- PagerDuty P1 escalation
- Implements multi-tier alerting strategy

### Network Alerts

#### ✅ GOOD Example 20: Network error rate percentage
```yaml
      - alert: HighNetworkErrorRate
        expr: |
          (
            rate(node_network_receive_errs_total[5m]) + rate(node_network_transmit_errs_total[5m])
          ) / (
            rate(node_network_receive_packets_total[5m]) + rate(node_network_transmit_packets_total[5m])
          ) * 100 > 1
        for: 15m
        labels:
          severity: warning
          team: infrastructure
          component: network
        annotations:
          summary: "High network error rate {{ $value | humanizePercentage }} on {{ $labels.instance }}"
          description: |
            Network interface {{ $labels.device }} on {{ $labels.instance }} has 
            {{ $value | humanizePercentage }} packet error rate.
            
            This may indicate:
            - Hardware issues
            - Cable problems
            - Driver issues
            
            Check interface status and logs.
          runbook_url: "https://runbooks.example.com/network-errors"
```
**Why it's good**:
- Percentage of total packets (scales)
- Combines RX and TX errors
- Reasonable threshold (1%)
- Hardware troubleshooting hints
- Identifies specific device/interface

### Custom Application Metrics

#### ✅ GOOD Example 21: Business metric with baseline
```yaml
      - alert: RevenueBelowBaseline
        expr: |
          (
            sum(rate(revenue_total[5m]))
            /
            avg_over_time(sum(rate(revenue_total[5m]))[1d:5m] offset 1w)
          ) < 0.7
        for: 30m
        labels:
          severity: warning
          team: business
          component: revenue
        annotations:
          summary: "Revenue {{ $value | humanizePercentage }} of weekly baseline"
          description: |
            Current revenue is {{ $value | humanizePercentage }} of last week's average.
            
            Current: {{ query "sum(rate(revenue_total[5m]))" | first | value }}/s
            Baseline: {{ query "avg_over_time(sum(rate(revenue_total[5m]))[1d:5m] offset 1w)" | first | value }}/s
            
            This may indicate:
            - Service issues affecting conversions
            - Marketing campaign changes
            - Seasonal variation
          runbook_url: "https://runbooks.example.com/revenue-drop"
```
**Why it's good**:
- Compares to baseline, not absolute value
- Week-over-week comparison (accounts for weekly patterns)
- Accounts for daily patterns (1d window)
- Shows both current and baseline values
- Multiple possible causes listed

### Cache Alerts

#### ✅ GOOD Example 22: Cache hit rate with minimum traffic
```yaml
      - alert: LowCacheHitRate
        expr: |
          (
            rate(cache_hits_total[10m])
            /
            (rate(cache_hits_total[10m]) + rate(cache_misses_total[10m]))
          ) < 0.8
          and
          (rate(cache_hits_total[10m]) + rate(cache_misses_total[10m])) > 10
        for: 20m
        labels:
          severity: warning
          team: infrastructure
          component: cache
        annotations:
          summary: "Cache {{ $labels.cache_name }} hit rate {{ $value | humanizePercentage }}"
          description: |
            Cache {{ $labels.cache_name }} hit rate is {{ $value | humanizePercentage }}.
            
            Hit rate: {{ query "rate(cache_hits_total{cache_name='{{ $labels.cache_name }}'}[10m])" | first | value }}/s
            Miss rate: {{ query "rate(cache_misses_total{cache_name='{{ $labels.cache_name }}'}[10m])" | first | value }}/s
            
            Low hit rates cause increased backend load.
          runbook_url: "https://runbooks.example.com/cache-hit-rate"
```
**Why it's good**:
- Requires minimum traffic (> 10 req/s)
- Avoids alerting during cache warmup or low traffic
- Shows hit and miss rates separately
- Explains impact (backend load)
- 20m for clause prevents transient alerts

### Load Balancer Alerts

#### ✅ GOOD Example 23: Backend availability
```yaml
      - alert: LoadBalancerBackendsDegraded
        expr: |
          (
            sum by(backend) (haproxy_backend_up)
            /
            count by(backend) (haproxy_backend_up)
          ) < 0.5
        for: 5m
        labels:
          severity: critical
          team: infrastructure
          component: loadbalancer
        annotations:
          summary: "Less than 50% backends healthy for {{ $labels.backend }}"
          description: |
            Backend {{ $labels.backend }} has {{ $value | humanizePercentage }} healthy servers.
            
            Healthy: {{ query "sum(haproxy_backend_up{backend='{{ $labels.backend }}'})" | first | value }}
            Total: {{ query "count(haproxy_backend_up{backend='{{ $labels.backend }}'})" | first | value }}
            
            This impacts service capacity and redundancy.
          runbook_url: "https://runbooks.example.com/backend-down"
```
**Why it's good**:
- Percentage of healthy backends
- Allows some failures (< 50% threshold)
- Shows healthy vs total count
- Critical severity when < 50%
- 5m for clause allows brief maintenance

### Storage System Alerts

#### ✅ GOOD Example 24: Disk latency percentile
```yaml
      - alert: HighDiskLatency
        expr: |
          histogram_quantile(0.95,
            sum(rate(node_disk_io_time_seconds_bucket[5m])) by (device, le)
          ) > 0.1
        for: 15m
        labels:
          severity: warning
          team: infrastructure
          component: storage
        annotations:
          summary: "High disk latency on {{ $labels.instance }}:{{ $labels.device }}"
          description: |
            P95 disk I/O latency is {{ $value }}s on device {{ $labels.device }}.
            
            This may indicate:
            - Disk saturation
            - Hardware degradation
            - Excessive I/O load
            
            Check disk utilization and IOPS.
          runbook_url: "https://runbooks.example.com/disk-latency"
```
**Why it's good**:
- Uses P95 percentile (not average)
- Device-specific alerting
- Multiple investigation paths
- 100ms threshold (0.1s) reasonable for most workloads
- 15m for clause confirms sustained issue

### Batch Job Alerts

#### ✅ GOOD Example 25: Job failure with retry awareness
```yaml
      - alert: BatchJobFailedAfterRetries
        expr: |
          time() - max by(job_name) (batch_job_last_success_timestamp) > 7200
          and
          batch_job_status{status="failed"} == 1
        for: 10m
        labels:
          severity: warning
          team: data
          component: batch
        annotations:
          summary: "Batch job {{ $labels.job_name }} failing for 2+ hours"
          description: |
            Batch job {{ $labels.job_name }} has not succeeded for {{ $value }} seconds.
            
            Last success: {{ batch_job_last_success_timestamp }}
            Current status: {{ $labels.status }}
            
            Check job logs and dependencies.
          runbook_url: "https://runbooks.example.com/batch-job-{{ $labels.job_name }}"
```
**Why it's good**:
- Checks time since last success (allows retries)
- 2 hour threshold appropriate for batch jobs
- Job-specific runbook URL
- Explains time duration in description
- 10m for clause confirms persistent failure

### Container Resource Alerts

#### ✅ GOOD Example 26: Container throttling percentage
```yaml
      - alert: ContainerCPUThrottlingHigh
        expr: |
          (
            rate(container_cpu_cfs_throttled_seconds_total[5m])
            /
            rate(container_cpu_cfs_periods_total[5m])
          ) * 100 > 25
        for: 15m
        labels:
          severity: warning
          team: platform
          component: resources
        annotations:
          summary: "Container {{ $labels.container }} throttled {{ $value | humanizePercentage }}"
          description: |
            Container {{ $labels.container }} in pod {{ $labels.pod }} is being 
            CPU throttled {{ $value | humanizePercentage }} of the time.
            
            Namespace: {{ $labels.namespace }}
            
            This indicates CPU limits may be too low.
            
            Current limits: {{ query "kube_pod_container_resource_limits{namespace='{{ $labels.namespace }}', pod='{{ $labels.pod }}', container='{{ $labels.container }}', resource='cpu'}" | first | value }}
            
            Consider increasing CPU limits or optimizing application.
          runbook_url: "https://runbooks.example.com/cpu-throttling"
```
**Why it's good**:
- Percentage of throttling, not absolute time
- Shows current CPU limits for context
- Clear remediation options (increase limits or optimize)
- 25% threshold allows some normal throttling
- Identifies namespace, pod, and container

### Service Mesh Alerts

#### ✅ GOOD Example 27: Circuit breaker stuck open
```yaml
      - alert: CircuitBreakerStuckOpen
        expr: |
          circuit_breaker_state == 1
        for: 30m
        labels:
          severity: warning
          team: platform
          component: servicemesh
        annotations:
          summary: "Circuit breaker for {{ $labels.service }} stuck open for 30m"
          description: |
            Circuit breaker for {{ $labels.service }} -> {{ $labels.upstream }} 
            has been open for 30+ minutes.
            
            This may indicate:
            - Persistent upstream issues
            - Circuit breaker misconfiguration
            - Need for manual intervention
            
            Check upstream service health.
          runbook_url: "https://runbooks.example.com/circuit-breaker"
```
**Why it's good**:
- Allows circuit breaker to work (30m threshold)
- Alerts when stuck, not when functioning normally
- Identifies both source and upstream services
- Multiple investigation paths
- Warning severity (not critical for expected behavior)

### Application: Rate Limiting Alerts

#### ✅ GOOD Example 28: Rate limit threshold with percentage
```yaml
      - alert: HighRateLimitHitRate
        expr: |
          (
            sum(rate(api_rate_limit_exceeded_total[10m])) by (service, endpoint)
            /
            sum(rate(api_requests_total[10m])) by (service, endpoint)
          ) * 100 > 10
        for: 15m
        labels:
          severity: warning
          team: "{{ $labels.service }}-team"
          component: api
        annotations:
          summary: "{{ $value | humanizePercentage }} of requests rate limited for {{ $labels.service }}/{{ $labels.endpoint }}"
          description: |
            Endpoint {{ $labels.endpoint }} in service {{ $labels.service }} has 
            {{ $value | humanizePercentage }} of requests hitting rate limits.
            
            This may indicate:
            - Legitimate traffic spike requiring limit increase
            - Potential abuse or misconfigured client
            - Application retry storm
            
            Review traffic patterns and client behavior.
          runbook_url: "https://runbooks.example.com/rate-limiting"
```
**Why it's good**:
- Percentage of total requests (10% threshold)
- Aggregated by service and endpoint
- Multiple possible causes identified
- 15m for clause prevents noise from bursts
- Warning severity (rate limiting is working as designed)

### Multi-Service Dependency Alerts

#### ✅ GOOD Example 29: Dependency failure impact
```yaml
      - alert: CriticalDependencyDegraded
        expr: |
          (
            sum(rate(dependency_call_errors_total{dependency=~"payment|auth"}[5m])) by (service, dependency)
            /
            sum(rate(dependency_call_total{dependency=~"payment|auth"}[5m])) by (service, dependency)
          ) * 100 > 5
        for: 10m
        labels:
          severity: critical
          team: "{{ $labels.service }}-team"
          component: dependencies
          affected_dependency: "{{ $labels.dependency }}"
        annotations:
          summary: "Critical dependency {{ $labels.dependency }} failing for {{ $labels.service }}"
          description: |
            Service {{ $labels.service }} is experiencing {{ $value | humanizePercentage }} 
            errors when calling critical dependency {{ $labels.dependency }}.
            
            Error rate: {{ query "sum(rate(dependency_call_errors_total{service='{{ $labels.service }}', dependency='{{ $labels.dependency }}'}[5m]))" | first | value }}/s
            Total rate: {{ query "sum(rate(dependency_call_total{service='{{ $labels.service }}', dependency='{{ $labels.dependency }}'}[5m]))" | first | value }}/s
            
            Check:
            1. {{ $labels.dependency }} service health
            2. Network connectivity
            3. Circuit breaker state
          runbook_url: "https://runbooks.example.com/dependency-failure/{{ $labels.dependency }}"
```
**Why it's good**:
- Filters to critical dependencies only (payment, auth)
- Percentage-based error rate
- Shows both error and total rates
- Dependency-specific runbook
- Critical severity for critical dependencies
- Identifies both caller and callee

### Monitoring System Self-Monitoring

#### ✅ GOOD Example 30: Prometheus itself
```yaml
      - alert: PrometheusTSDBCompactionFailing
        expr: |
          rate(prometheus_tsdb_compactions_failed_total[1h]) > 0
        for: 4h
        labels:
          severity: warning
          team: observability
          component: prometheus
        annotations:
          summary: "Prometheus {{ $labels.instance }} TSDB compaction failures"
          description: |
            Prometheus instance {{ $labels.instance }} has been failing TSDB compactions 
            for the last 4 hours.
            
            This may lead to:
            - Increased disk usage
            - Slower queries
            - Potential data loss
            
            Check:
            1. Disk space available
            2. Prometheus logs for errors
            3. TSDB health metrics
          runbook_url: "https://runbooks.example.com/prometheus-tsdb-compaction"
```
**Why it's good**:
- Monitors the monitoring system itself
- 4h for clause (compaction failures can be transient)
- Explains downstream impact
- Multiple investigation steps
- Warning severity (not immediately critical)
- Self-healing observability

---

## Side-by-Side Comparisons

### Comparison 1: CPU Alert

| Aspect | ❌ Poorly Configured | ✅ Well Configured |
|--------|---------------------|-------------------|
| **Expression** | `node_cpu_usage > 80` | `100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 90` |
| **For Clause** | Missing | `for: 15m` |
| **Function** | None (gauge used directly) | `rate()` for stability |
| **Threshold** | 80% (too low) | 90% (appropriate) |
| **Aggregation** | None | `avg by(instance)` |
| **Labels** | `severity: critical` only | `severity: warning`, `team: infrastructure`, `component: compute` |
| **Annotations** | None | `summary`, `description` with context, `runbook_url`, `dashboard_url` |
| **Impact** | Constant noise, alert fatigue | Actionable, meaningful alerts |

### Comparison 2: Memory Alert

| Aspect | ❌ Poorly Configured | ✅ Well Configured |
|--------|---------------------|-------------------|
| **Expression** | `memory_used_percent > 70` | `(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100 > 90` |
| **For Clause** | Missing or too short (1m) | `for: 10m` |
| **Metric Used** | Simple percentage | MemAvailable (includes reclaimable cache) |
| **Threshold** | 70% (too sensitive) | 90% (allows caching) |
| **Context** | None | Shows available memory, troubleshooting steps |
| **Calculation** | Assumes all used memory is pressure | Correctly accounts for Linux memory management |
| **Result** | False positives from caching | Only alerts on actual pressure |

### Comparison 3: HTTP Error Rate

| Aspect | ❌ Poorly Configured | ✅ Well Configured |
|--------|---------------------|-------------------|
| **Expression** | `http_errors > 10` | `(sum(rate(http_requests_total{status=~"5.."}[5m])) by (service) / sum(rate(http_requests_total[5m])) by (service)) * 100 > 1` |
| **Threshold Type** | Absolute count | Percentage |
| **Scalability** | Breaks as traffic grows | Scales automatically with traffic |
| **For Clause** | Missing | `for: 10m` |
| **Aggregation** | None (per instance) | By service |
| **Function** | Counter value directly | `rate()` for rate calculation |
| **Context** | None | Shows error rate, total rate, percentages |
| **SLO Alignment** | No | Can align with 99% availability SLO |
| **Traffic Awareness** | 10 errors is always 10 errors | 10 errors is 0.1% or 50% depending on traffic |

### Comparison 4: Disk Space

| Aspect | ❌ Poorly Configured | ✅ Well Configured |
|--------|---------------------|-------------------|
| **Expression** | `disk_free_bytes < 10000000000` | `(node_filesystem_avail_bytes{fstype!~"tmpfs..."} / node_filesystem_size_bytes{fstype!~"tmpfs..."}) * 100 < 15` |
| **Threshold Type** | Absolute (10GB) | Percentage-based |
| **Filesystem Filtering** | None (alerts on tmpfs, overlay) | Excludes temporary filesystems |
| **For Clause** | Missing | `for: 30m` |
| **Information** | None | Mountpoint, filesystem type, available, total space |
| **Scalability** | 10GB is different on 50GB vs 5TB disk | 15% works for any disk size |
| **Predictive** | No | Can add predict_linear() for time-to-full |
| **Context** | No indication which disk | Identifies exact mountpoint and instance |

---

## Quick Reference Summary

### Essential Checklist for Every Alert

✅ **Must Have**:
1. Proper `for` clause (typically 5-15 minutes)
2. Severity label (`critical`, `warning`, `info`)
3. Team/owner label for routing
4. Summary annotation explaining what's wrong
5. Description with context and impact
6. Runbook URL linking to resolution steps

✅ **Should Have**:
7. Component label for categorization
8. Dashboard URL for quick visualization
9. Environment label if multi-environment
10. Template variables showing current values

❌ **Never Do**:
1. No `for` clause on volatile metrics
2. Use `irate()` in alert expressions
3. Dynamic/high-cardinality labels (`$value`, `request_id`)
4. Absolute thresholds that don't scale
5. Alert on every error without percentage
6. Mix 4xx and 5xx errors in same alert
7. Use average for latency (use percentiles)
8. Alert on symptoms without understanding impact

### Common Threshold Guidelines

| Metric Type | Warning | Critical | Notes |
|-------------|---------|----------|-------|
| **CPU** | > 85% | > 95% | Use `rate()`, 10-15m `for` clause |
| **Memory** | > 85% | > 95% | Use MemAvailable, 10m `for` clause |
| **Disk** | < 20% free | < 10% free | Exclude tmpfs, 30m `for` clause |
| **Error Rate** | > 1% | > 5% | Percentage of total, 10m `for` clause |
| **P99 Latency** | > 1s | > 3s | Use histogram_quantile, 15m `for` clause |
| **Replication Lag** | > 300s | > 600s | Context dependent, 15m `for` clause |

### Time Window Recommendations

| Metric Behavior | Recommended `for` | Reasoning |
|-----------------|-------------------|-----------|
| **Fast oscillating** | 15-30m | Prevents flapping on spikes |
| **Slow changing** | 5-10m | Can detect issues faster |
| **Network metrics** | 10-15m | Accounts for brief network issues |
| **Disk filling** | 30m | Predictive alerts need longer window |
| **Pod restarts** | 15m | Confirms crash loop pattern |
| **Error rates** | 10m | Balance between speed and accuracy |

### Label Strategy

**Good Labels** (bounded cardinality):
- `severity`: critical, warning, info
- `team`: team-name (bounded set)
- `service`: service-name (bounded set)
- `component`: compute, storage, network, etc.
- `environment`: prod, staging, dev
- `alert_type`: symptom, cause, predictive

**Bad Labels** (unbounded cardinality):
- `current_value`: "{{ $value }}"
- `request_id`: "{{ $labels.request_id }}"
- `user_id`: "{{ $labels.user_id }}"
- `timestamp`: "{{ $labels.timestamp }}"
- `pod`: "{{ $labels.pod }}" (use aggregation instead)

### Function Usage Guide

| Use Case | ✅ Use | ❌ Avoid |
|----------|--------|---------|
| **Counter metrics** | `rate()`, `increase()` | `irate()` in alerts |
| **Gauges** | Direct value, `avg()` | `rate()` |
| **Latency** | `histogram_quantile()` | `avg()` |
| **Predictions** | `predict_linear()` | Manual extrapolation |
| **Aggregation** | `sum by()`, `avg by()` | No aggregation |
| **Threshold checking** | `> threshold`, `< threshold` | `!= threshold` |

---

## Related Documents

For more information, see:
- **Alert Configuration Patterns & Infrastructure** (`alert-configuration-patterns.md`) - How to configure alerting infrastructure and apply configuration patterns
- **Alert Tuning & Analysis Methodology** (`alert-tuning-methodology.md`) - How to analyze and tune alerts in production environments

---

This reference document provides a comprehensive catalog of alert patterns. Use it as your go-to resource when writing, reviewing, or debugging Prometheus alerts.