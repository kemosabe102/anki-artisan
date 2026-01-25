# PromQL Query Construction Patterns & Signal Detection

**Category**: domain-specific
**Domain**: Observability - Prometheus query language for metric-based monitoring and alerting
**Confidence**: 0.85 (high-quality official documentation + industry best practices)
**Last Updated**: 2025-11-10T18:00:00Z
**Agent**: promql-query-builder

---

## Overview

This documentation provides AI-readable guidance for constructing PromQL queries that are efficient, maintainable, and aligned with observability best practices. It covers label cardinality management to prevent metric explosion, recording rule creation for query optimization, and time-period comparison patterns for trend analysis.

**Key Concepts**:

- **Label Cardinality**: The number of unique time series created by combining label values. High cardinality (>10K series per metric) causes memory exhaustion and query degradation.
- **Recording Rules**: Precomputed queries stored as new metrics to reduce dashboard load times and enable complex aggregations with minimal query cost.
- **Time-Period Offset**: Historical comparison technique using `offset` modifier to analyze trends (day-over-day, week-over-week) and detect anomalies.

---

## Core Frameworks

### Framework 1: Label Cardinality Management

**Purpose**: Prevent metric explosion and Prometheus performance degradation by controlling the number of unique time series per metric.

**When to Use**:

- Before introducing new labels to existing metrics
- When designing custom application metrics
- During metric cardinality audits (monthly recommended)
- After observing Prometheus query slowdowns or OOM errors

**Components**:

1. **Cardinality Thresholds**: Acceptable (<10 combinations/metric) | Warning (10-100) | Critical (>100) | System-wide alert (>10K total series)
2. **Low-Cardinality Labels** (safe): `status_code`, `http_method`, `region`, `environment`, `service_name`, `endpoint` (coarse-grained)
3. **High-Cardinality Labels** (dangerous): `user_id`, `session_id`, `request_id`, `ip_address`, `timestamp`, `trace_id`, `email`, `uuid`

**How to Apply**:

1. **Audit Existing Cardinality**: Run detection query to identify top 20 metrics by series count:

   ```promql
   topk(20, count by (__name__)({__name__=~".+"}))
   ```

2. **Classify Label Risk**: Review label values - if unbounded (e.g., user IDs) → remove or aggregate
3. **Refactor High-Cardinality Labels**: Use recording rules to pre-aggregate or move identifiers to exemplars/logs (not labels)
4. **Set Alerts**: Monitor total series count and per-metric cardinality:

   ```promql
   # Alert if any metric exceeds 1000 series
   count by (__name__)({__name__=~".+"}) > 1000
   ```

**Example from Codebase**:

```promql
# ❌ ANTI-PATTERN: High cardinality - creates series per user
http_requests_total{user_id="12345", endpoint="/api/v1/data"}

# ✅ BEST PRACTICE: Low cardinality - aggregates users, logs user_id separately
http_requests_total{endpoint="/api/v1/data", status_code="200"}
# Use exemplars or structured logs for user_id tracing
```

**Source**: [Prometheus Best Practices - Metric Naming](https://prometheus.io/docs/practices/naming/)

---

### Framework 2: Recording Rules Creation Criteria

**Purpose**: Optimize query performance and enable complex real-time aggregations by precomputing expensive PromQL expressions and storing results as new metrics.

**When to Use**:

- Query execution time >30 seconds (measured in Prometheus UI)
- Dashboard uses same aggregation 3+ times (DRY principle)
- Alert expressions involve multi-level aggregations (e.g., rate → sum → topk)
- Cardinality reduction >1000:1 (e.g., per-instance → per-service aggregation)
- Critical SLO/SLA calculations requiring sub-second response

**Components**:

1. **Naming Convention**: `<level>:<metric>:<operations>` (e.g., `job:http_requests:rate5m`)
   - `<level>`: Aggregation scope (`instance`, `job`, `cluster`, `region`)
   - `<metric>`: Original metric name (without suffixes like `_total`)
   - `<operations>`: Transformations applied (`rate`, `sum`, `avg`, `increase`)

2. **Evaluation Interval**: ≥4x scrape_interval (e.g., 10s scrape → 60s evaluation minimum)
   - Reason: Ensures sufficient data points for rate calculations (rate needs 2+ samples)

3. **Complexity Triggers**:
   - Multiple aggregations: `sum(rate(metric[5m]))` → creates `job:metric:rate5m`
   - Cross-label aggregations: Combining `by (label1, label2)` with `sum`, `avg`, `max`
   - Percentile calculations: `histogram_quantile(0.95, ...)` (expensive histogram operations)

**How to Apply**:

1. **Identify Candidates**: Check Prometheus slow query log or dashboard load times
2. **Calculate ROI**: Measure current query time × usage frequency vs recording rule storage cost
3. **Define Recording Rule**: Create rule in Prometheus config:

   ```yaml
   groups:
     - name: api_performance
       interval: 60s
       rules:
         - record: job:http_request_duration_seconds:p95
           expr: histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (job, le))
   ```

4. **Validate**: Query new metric `job:http_request_duration_seconds:p95` and compare values with original expression
5. **Update Dashboards**: Replace complex query with simple recording rule reference

**Example from Codebase**:

```promql
# Original complex query (30s execution time on large cluster):
sum(rate(http_requests_total{job="api-server"}[5m])) by (status_code)

# Recording rule (stored in Prometheus config):
- record: job:http_requests:rate5m
  expr: sum(rate(http_requests_total[5m])) by (job, status_code)

# Dashboard query (now <1s execution time):
job:http_requests:rate5m{job="api-server"}
```

**Source**: [Prometheus Recording Rules Documentation](https://prometheus.io/docs/prometheus/latest/configuration/recording_rules/)

---

### Framework 3: Time-Period Comparison Patterns (Offset)

**Purpose**: Analyze trends, detect anomalies, and compare current metrics against historical baselines using `offset` modifier for time-shifting queries.

**When to Use**:

- Monitoring week-over-week traffic growth/decline
- Alerting on deviation from historical patterns (e.g., >20% drop vs last week)
- Capacity planning based on monthly trends
- Incident root cause analysis (compare pre-incident vs current state)
- Seasonal pattern detection (day-of-week, hour-of-day comparisons)

**Components**:

1. **Common Offset Durations**:
   - `1h`: Recent trend comparison (rolling hour-over-hour)
   - `24h` (1d): Day-over-day comparison (detect daily anomalies)
   - `168h` (7d): Week-over-week comparison (account for weekly seasonality)
   - `720h` (30d): Month-over-month comparison (long-term trends)

2. **Missing Data Handling**:
   - **Zero-fill**: `or vector(0)` - treat missing data as zero (safe for counters)
   - **Gap detection**: `absent(metric)` - alert when metric disappears
   - **Cross-join with `up` metric**: Ensure comparison only when both timestamps have data

3. **Edge Cases**:
   - **DST transitions**: 23h or 25h days (manual adjustment needed for exact 24h offset)
   - **Scrape alignment**: Use range ≥4x scrape_interval to ensure data availability
   - **Metric restarts**: Counter resets (use `increase()` instead of raw values)

**How to Apply**:

1. **Basic Offset Query**: Compare current vs 7 days ago:

   ```promql
   # Current request rate
   rate(http_requests_total[5m])

   # Same time last week
   rate(http_requests_total[5m] offset 7d)
   ```

2. **Percentage Change Calculation**:

   ```promql
   # Calculate % change vs last week (with zero-fill for missing data)
   (
     rate(http_requests_total[5m]) -
     (rate(http_requests_total[5m] offset 7d) or vector(0))
   ) /
   (rate(http_requests_total[5m] offset 7d) or vector(1)) * 100
   ```

3. **Alert on Deviation**:

   ```promql
   # Alert if current traffic >30% below last week's baseline
   (
     (rate(http_requests_total[5m] offset 7d) - rate(http_requests_total[5m])) /
     rate(http_requests_total[5m] offset 7d)
   ) > 0.3
   ```

4. **Multi-Period Comparison**:

   ```promql
   # Compare current vs 1h, 24h, and 7d ago simultaneously
   rate(http_requests_total[5m]) or
   rate(http_requests_total[5m] offset 1h) or
   rate(http_requests_total[5m] offset 24h) or
   rate(http_requests_total[5m] offset 7d)
   ```

**Example from Codebase**:

```promql
# Dashboard panel: "API Traffic - Week-over-Week Comparison"
# Blue line: Current traffic
sum(rate(http_requests_total{job="api-server"}[5m])) by (endpoint)

# Red line: Same time last week
sum(rate(http_requests_total{job="api-server"}[5m] offset 7d)) by (endpoint)

# Alert: Traffic drop >50% vs last week (with 15min grace period)
ALERT ApiTrafficDropWeekOverWeek
  IF (
    (
      sum(rate(http_requests_total{job="api-server"}[5m] offset 7d)) -
      sum(rate(http_requests_total{job="api-server"}[5m]))
    ) /
    sum(rate(http_requests_total{job="api-server"}[5m] offset 7d))
  ) > 0.5
  FOR 15m
  ANNOTATIONS {
    summary = "API traffic dropped >50% vs last week",
    description = "Current: {{ $value }}% below baseline"
  }
```

**Source**: [Prometheus Query Functions - offset](https://prometheus.io/docs/prometheus/latest/querying/basics/#offset-modifier)

---

## Processes & Workflows

### Workflow 1: Cardinality Audit & Remediation

**Trigger Conditions**:

- Prometheus query latency increasing over time (p95 >5s)
- Memory usage >80% of allocated resources
- New metrics or labels added to application code
- Scheduled monthly cardinality review

**Steps**:

1. **Identify High-Cardinality Metrics**: Run audit query
   - **Input**: Access to Prometheus web UI or API
   - **Output**: List of top 20 metrics by series count
   - **Rationale**: Focus remediation effort on worst offenders (80/20 rule)

   ```promql
   topk(20, count by (__name__)({__name__=~".+"}))
   ```

2. **Analyze Label Combinations**: Inspect labels for each high-cardinality metric
   - **Input**: Metric name from step 1
   - **Output**: Label values causing cardinality explosion
   - **Rationale**: Distinguish between acceptable (10 regions × 5 status codes = 50 series) vs problematic (unbounded user IDs)

   ```promql
   # Count unique label value combinations
   count by (__name__, job, instance)(metric_name)
   ```

3. **Classify Remediation Strategy**:
   - **Input**: Label analysis results
   - **Output**: Action plan (remove label, aggregate, or recording rule)
   - **Rationale**: Choose appropriate fix based on label business value
   - **Decision Tree**: See "Decision 1: Label Retention vs Removal" below

4. **Apply Fix & Validate**: Remove labels or create recording rules
   - **Input**: Remediation strategy from step 3
   - **Output**: Updated metric configuration with reduced cardinality
   - **Rationale**: Verify cardinality reduction before deploying to production

   ```bash
   # Redeploy instrumentation code or Prometheus config
   # Re-run audit query to confirm series count reduction
   ```

**Success Criteria**:

- ✅ No single metric exceeds 1000 series (warning threshold)
- ✅ Total series count <500K for typical production deployment
- ✅ Query p95 latency <2s for common dashboard queries
- ✅ Prometheus memory usage stable (<70% allocated)

**Failure Handling**:

- If label removal breaks dashboards, create recording rule as interim solution
- If cardinality persists after remediation, consider metric sharding (split by service/region)

**Example Execution**:

A team discovers `http_requests_total` has 15K series due to `user_id` label. They remove `user_id` from metric labels, add it to structured logs instead, and create recording rule `service:http_requests:rate5m` aggregated by `service` and `endpoint` only. Series count drops to 200, dashboard performance improves from 12s to <1s load time.

---

### Workflow 2: Recording Rule Creation & Deployment

**Trigger Conditions**:

- Dashboard query execution time >30s
- Alert evaluation causing Prometheus rule evaluation lag (check `/rules` page)
- Same complex aggregation used in 3+ places (code duplication)
- Request from SRE for real-time SLO tracking with <1s latency

**Steps**:

1. **Capture Baseline Query Performance**: Measure current query execution time
   - **Input**: Original PromQL query from dashboard or alert
   - **Output**: Execution time (from Prometheus UI query stats)
   - **Rationale**: Quantify performance improvement after recording rule deployment

   ```promql
   # Example slow query (30s execution time):
   histogram_quantile(0.95,
     sum(rate(http_request_duration_seconds_bucket[5m])) by (job, le)
   )
   ```

2. **Design Recording Rule**: Follow naming convention and select interval
   - **Input**: Original query + aggregation scope
   - **Output**: Recording rule YAML definition
   - **Rationale**: Ensure rule is reusable across multiple dashboards/alerts

   ```yaml
   groups:
     - name: api_latency_rules
       interval: 60s
       rules:
         - record: job:http_request_duration_seconds:p95
           expr: histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (job, le))
   ```

3. **Validate Rule Locally**: Test in dev/staging Prometheus before production
   - **Input**: Recording rule YAML
   - **Output**: Validation report (rule compiles, produces expected values)
   - **Rationale**: Prevent production incidents from malformed rules

   ```bash
   promtool check rules /etc/prometheus/recording_rules.yml
   # Query new metric: job:http_request_duration_seconds:p95
   ```

4. **Deploy & Monitor**: Apply to production Prometheus, update dashboards
   - **Input**: Validated recording rule
   - **Output**: Updated Prometheus config, dashboard queries using new metric
   - **Rationale**: Measure actual performance improvement and storage impact

   ```promql
   # Old dashboard query: [complex 30s query]
   # New dashboard query: job:http_request_duration_seconds:p95{job="api-server"}
   ```

5. **Track Storage Impact**: Monitor Prometheus storage growth
   - **Input**: Recording rule deployment timestamp
   - **Output**: Storage delta (MB/day increase)
   - **Rationale**: Ensure storage cost justifies performance gain

   ```promql
   # Check storage growth rate
   rate(prometheus_tsdb_storage_blocks_bytes[1d])
   ```

**Success Criteria**:

- ✅ Query execution time reduced by >80% (30s → <5s)
- ✅ Recording rule evaluation completes within configured interval (no lag)
- ✅ Storage increase <10% of total Prometheus storage
- ✅ Dashboards and alerts migrated to use new recording rule

**Failure Handling**:

- If recording rule evaluation lags, increase interval or simplify aggregation
- If storage impact too high, reduce retention or use longer evaluation intervals
- If values differ from original query, check for label mismatches or scrape interval issues

**Example Execution**:

SRE team notices `/dashboard/api-performance` takes 45s to load. They identify the p95 latency panel uses a complex histogram query executed 12 times. They create recording rule `job:http_request_duration_seconds:p95` with 60s interval, validate in staging, deploy to prod. Dashboard load time drops to 2s, Prometheus storage increases by 3%.

---

### Workflow 3: Time-Period Comparison Alert Setup

**Trigger Conditions**:

- Need to detect anomalies vs historical patterns (not just static thresholds)
- Seasonal traffic patterns make absolute thresholds ineffective (e.g., weekday vs weekend)
- Incident post-mortem recommends "alert on >X% deviation from baseline"
- SRE team requests proactive capacity alerts based on growth trends

**Steps**:

1. **Define Baseline Period**: Choose offset duration (1h, 24h, 7d, 30d)
   - **Input**: Business context (seasonality, traffic patterns)
   - **Output**: Offset duration selection with rationale
   - **Rationale**: Match baseline to observed patterns (weekly seasonality → 7d offset)
   - **Decision Tree**: See "Decision 2: Offset Duration Selection" below

2. **Calculate Deviation Threshold**: Determine acceptable % change
   - **Input**: Historical data analysis (p50, p95 deviation)
   - **Output**: Threshold percentage (e.g., >30% drop triggers alert)
   - **Rationale**: Balance alert sensitivity vs noise (avoid over-alerting)

   ```promql
   # Measure historical deviation range (for threshold tuning)
   quantile(0.95,
     abs(
       (rate(metric[5m]) - rate(metric[5m] offset 7d)) /
       rate(metric[5m] offset 7d)
     )
   )
   ```

3. **Write Alert Rule with Offset**: Create alert with `offset` modifier
   - **Input**: Baseline offset + deviation threshold
   - **Output**: Alert rule YAML definition
   - **Rationale**: Detect anomalies while accounting for historical patterns

   ```yaml
   groups:
     - name: traffic_anomaly_alerts
       rules:
         - alert: ApiTrafficDropWeekOverWeek
           expr: |
             (
               (
                 sum(rate(http_requests_total{job="api"}[5m] offset 7d)) -
                 sum(rate(http_requests_total{job="api"}[5m]))
               ) /
               sum(rate(http_requests_total{job="api"}[5m] offset 7d))
             ) > 0.3
           for: 15m
           annotations:
             summary: "API traffic dropped >30% vs last week"
   ```

4. **Handle Missing Data Edge Cases**: Add zero-fill or `absent()` checks
   - **Input**: Alert rule from step 3
   - **Output**: Enhanced rule with missing data handling
   - **Rationale**: Prevent false positives from data gaps (scrape failures, metric restarts)

   ```promql
   # Enhanced with zero-fill for missing baseline data
   (
     (
       (sum(rate(metric[5m] offset 7d)) or vector(0)) -
       sum(rate(metric[5m]))
     ) /
     (sum(rate(metric[5m] offset 7d)) or vector(1))
   ) > 0.3
   ```

5. **Test & Tune Threshold**: Backtest alert on historical data
   - **Input**: Alert rule + 30 days historical metrics
   - **Output**: Alert frequency analysis (true positives vs false positives)
   - **Rationale**: Validate threshold before production deployment

   ```promql
   # Simulate alert over past 30 days to check frequency
   count_over_time(
     (
       (sum(rate(metric[5m] offset 7d)) - sum(rate(metric[5m]))) /
       sum(rate(metric[5m] offset 7d)) > 0.3
     )[30d:5m]
   )
   ```

**Success Criteria**:

- ✅ Alert fires on known incidents from historical data (true positive validation)
- ✅ Alert does NOT fire on expected pattern variations (e.g., holiday traffic dips)
- ✅ Alert latency <15min (time from anomaly start to alert firing)
- ✅ Alert includes actionable context (current value, baseline value, % deviation)

**Failure Handling**:

- If too many false positives, increase deviation threshold or add `for` duration
- If missing data causes flapping, strengthen zero-fill logic or cross-join with `up` metric
- If alert never fires, verify offset duration matches observed seasonality

**Example Execution**:

E-commerce platform wants to detect checkout API traffic anomalies. They analyze historical data and find 7-day seasonality (weekday vs weekend). They create alert with 7d offset and 30% deviation threshold. Backtest shows 2 true positives (past outages) and 1 false positive (Thanksgiving Day traffic drop). They add exception for major holidays using label filters, deploy to production.

---

## Decision Trees

### Decision 1: Label Retention vs Removal

```
IF label has unbounded cardinality (user_id, session_id, uuid, ip_address)
  THEN remove from metric labels, move to structured logs or exemplars
  BECAUSE unbounded labels cause metric explosion (>10K series)

ELSE IF label has bounded cardinality BUT >100 unique values (product_id, customer_segment)
  THEN evaluate business value:
    IF used in <3 dashboards AND no critical alerts
      THEN remove label, aggregate to higher level (e.g., product_category)
      BECAUSE storage cost outweighs query benefit
    ELSE IF used in 3+ places OR critical alerts
      THEN keep label BUT create recording rule to pre-aggregate
      BECAUSE query performance justifies storage cost

ELSE IF label has low cardinality (<10 values: region, environment, status_code)
  THEN keep label
  BECAUSE minimal storage impact, high query utility

ELSE (edge case: label cardinality unknown)
  THEN run exploratory query to count unique values
  BECAUSE data-driven decision required
```

**Example Scenarios**:

1. **Scenario**: `http_requests_total{user_id="..."}` has 500K unique user_ids → **Decision**: Remove `user_id`, log in structured format instead
2. **Scenario**: `cache_hits_total{cache_key="..."}` has 50K cache keys used in 5 dashboards → **Decision**: Keep `cache_key`, create recording rule `service:cache_hits:rate5m` aggregated by `service` only
3. **Scenario**: `db_queries_total{table_name="..."}` has 8 table names → **Decision**: Keep `table_name` label (low cardinality, high value)

---

### Decision 2: Offset Duration Selection

```
IF comparing intraday patterns (hourly traffic variation)
  THEN use offset 1h
  BECAUSE detects short-term anomalies (lunch rush vs normal hours)

ELSE IF comparing daily patterns (typical Monday vs current Monday)
  THEN use offset 24h (1d)
  BECAUSE accounts for daily seasonality (business hours vs overnight)

ELSE IF comparing weekly patterns (this week vs last week)
  THEN use offset 168h (7d)
  BECAUSE accounts for weekly seasonality (weekday vs weekend)

ELSE IF comparing monthly trends (this month vs last month)
  THEN use offset 720h (30d)
  BECAUSE detects long-term growth/decline trends

ELSE IF unknown seasonality
  THEN analyze historical data to identify patterns:
    - Run autocorrelation analysis on past 90 days
    - Identify strongest periodicity (1d, 7d, 30d)
    - Select offset matching detected period
  BECAUSE data-driven offset selection reduces false positives
```

**Example Scenarios**:

1. **Scenario**: Detect API latency spikes during business hours → **Decision**: offset 1h (compare current hour vs previous hour)
2. **Scenario**: Alert on Black Friday traffic anomalies → **Decision**: offset 7d (compare to last Friday, avoid weekday baseline mismatch)
3. **Scenario**: Monitor database growth rate month-over-month → **Decision**: offset 30d (long-term capacity planning)

---

## Best Practices

### Practice 1: Use Recording Rules for Reusable Aggregations

**Principle**: Don't Repeat Yourself (DRY) - Complex aggregations used multiple times should be precomputed to reduce query load and improve dashboard performance.

**Implementation**:

- Identify queries appearing in 3+ dashboards or alerts
- Extract common aggregation into recording rule with descriptive name
- Replace original queries with recording rule references
- Document recording rule purpose in Prometheus config comments

**Benefits**:

- ✅ Dashboard load time reduced by 70-90% (from 30s to <3s)
- ✅ Reduced Prometheus CPU usage (query evaluation happens once per interval, not per dashboard refresh)
- ✅ Consistent metric calculations across dashboards (no copy-paste errors)
- ✅ Easier debugging (single source of truth for aggregation logic)

**Trade-offs**:

- ⚠️ Increased storage (each recording rule creates new time series)
- ⚠️ Rule evaluation lag if interval too short (30s interval may not complete before next execution)
- ⚠️ Requires Prometheus config change + reload (not dynamic like queries)

**Example**:

```yaml
# Recording rule for API p95 latency (used in 7 dashboards)
groups:
  - name: api_performance
    interval: 60s
    rules:
      - record: job:http_request_duration_seconds:p95
        expr: histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (job, le))

# Dashboard queries change from:
# histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (job, le))
# To:
# job:http_request_duration_seconds:p95{job="api-server"}
```

---

### Practice 2: Always Handle Missing Data in Offset Comparisons

**Principle**: Offset queries fail gracefully when baseline data is missing (scrape failures, metric restarts) by using `or vector(0)` for zero-fill or `absent()` for gap detection.

**Implementation**:

- Add `or vector(0)` to offset expressions where missing data should default to zero (safe for counters)
- Use `absent(metric offset Xd)` to detect when historical data unavailable (alert on metric disappearance)
- Cross-join with `up` metric to ensure both current and baseline data exist before comparison
- Document missing data strategy in alert annotations

**Benefits**:

- ✅ Prevents alert flapping during scrape failures or metric restarts
- ✅ Clear distinction between "no data" and "value is zero"
- ✅ Dashboards show meaningful values instead of "No data" gaps
- ✅ Alerts include context about data availability issues

**Trade-offs**:

- ⚠️ Zero-fill may mask real issues (traffic actually dropped to zero vs scrape failed)
- ⚠️ Requires careful reasoning about when zero is safe default
- ⚠️ Additional query complexity (2-3 extra lines per offset comparison)

**Example**:

```promql
# ❌ FRAGILE: Fails with "No data" if baseline missing
(rate(metric[5m]) - rate(metric[5m] offset 7d)) / rate(metric[5m] offset 7d)

# ✅ ROBUST: Zero-fills missing baseline, prevents division by zero
(
  rate(metric[5m]) -
  (rate(metric[5m] offset 7d) or vector(0))
) /
(rate(metric[5m] offset 7d) or vector(1))

# ✅ EXPLICIT GAP DETECTION: Alert if baseline data missing
absent(rate(metric[5m] offset 7d))
```

---

### Practice 3: Namespace Recording Rules by Aggregation Level

**Principle**: Recording rule names should clearly indicate aggregation scope (`instance`, `job`, `cluster`) to prevent confusion and enable predictable querying patterns.

**Implementation**:

- Follow convention: `<level>:<metric>:<operations>`
  - `instance:metric:operation` - Finest granularity (per-pod/node)
  - `job:metric:operation` - Service-level aggregation (most common)
  - `cluster:metric:operation` - Cross-service aggregation
  - `region:metric:operation` - Multi-cluster aggregation
- Include time range in operation name when relevant: `rate5m`, `increase1h`, `avg15m`
- Avoid generic names like `my_metric_aggregated` (ambiguous scope)

**Benefits**:

- ✅ Self-documenting metric names (no need to check config to understand aggregation)
- ✅ Prevents accidental double-aggregation (trying to `sum()` a `job:`-level metric again)
- ✅ Enables predictable patterns (all `job:` rules aggregate `by (job)`)
- ✅ Easier onboarding (new team members understand hierarchy instantly)

**Trade-offs**:

- ⚠️ Longer metric names (impacts readability in dense dashboards)
- ⚠️ Requires discipline to maintain consistency across team
- ⚠️ Renaming rules breaks dashboards (migration needed)

**Example**:

```yaml
# ✅ CLEAR HIERARCHY: Aggregation level explicit in name
- record: instance:cpu_usage:rate5m
  expr: rate(node_cpu_seconds_total[5m])

- record: job:cpu_usage:rate5m
  expr: sum(rate(node_cpu_seconds_total[5m])) by (job)

- record: cluster:cpu_usage:rate5m
  expr: sum(rate(node_cpu_seconds_total[5m]))

# ❌ AMBIGUOUS: Cannot determine aggregation scope from name
- record: cpu_usage_rate
  expr: sum(rate(node_cpu_seconds_total[5m])) by (job)
```

---

## Anti-Patterns

### Anti-Pattern 1: Using High-Cardinality Labels Without Recording Rules

**Problem**: Adding unbounded labels (user_id, request_id, IP addresses) directly to metrics causes metric explosion, memory exhaustion, and query degradation. This is the #1 cause of Prometheus production incidents.

**Detection**:

- 🔴 Prometheus memory usage growing linearly with user growth
- 🔴 Query latency degrading over time (p95 >10s for simple queries)
- 🔴 Metric with >10K time series (check with `count by (__name__)(metric_name)`)
- 🔴 Prometheus logs show "out of memory" errors or OOM restarts

**Consequences**:

- ❌ Prometheus crashes or becomes unresponsive (OOM killer)
- ❌ Queries time out (>30s execution time)
- ❌ Dashboard load times >1 minute (unusable)
- ❌ Alert evaluation lag causes delayed incident detection
- ❌ Storage costs spiral (each series requires ~1-3KB memory)

**Better Approach**:

```promql
# ❌ ANTI-PATTERN: Unbounded user_id label
http_requests_total{user_id="user123", endpoint="/api/data"}
# Creates 1 series per user - 1M users = 1M series!

# ✅ PREFERRED PATTERN 1: Remove high-cardinality label, use structured logs
http_requests_total{endpoint="/api/data", status_code="200"}
# Log user_id in application logs or traces instead

# ✅ PREFERRED PATTERN 2: Aggregate into low-cardinality buckets
http_requests_total{endpoint="/api/data", user_tier="premium"}
# Group users into tiers: free, premium, enterprise (3 series max)

# ✅ PREFERRED PATTERN 3: Use exemplars (Prometheus 2.26+)
http_requests_total{endpoint="/api/data"}  # Exemplar: trace_id="abc123", user_id="user123"
# Exemplars provide sample drill-down without creating series
```

**Migration Strategy**:

1. **Audit**: Identify high-cardinality metrics with `topk(20, count by (__name__)({__name__=~".+"}))`
2. **Plan**: Decide label removal vs aggregation vs exemplars based on use case
3. **Update Instrumentation**: Modify application code to remove/aggregate labels
4. **Deploy Gradually**: Roll out to 10% traffic, monitor cardinality reduction
5. **Migrate Dashboards**: Update queries to use new label schema or recording rules
6. **Deprecate Old Metric**: After 30-day grace period, remove old high-cardinality metric

---

### Anti-Pattern 2: Creating Recording Rules for Every Query (Over-Optimization)

**Problem**: Creating recording rules for simple queries that execute quickly (<2s) adds unnecessary storage overhead and operational complexity without meaningful performance benefit.

**Detection**:

- 🔴 Recording rule catalog has >100 rules with <10 dashboard references each
- 🔴 Storage growth >50% after adding recording rules (check Prometheus TSDB size)
- 🔴 Many recording rules evaluate to <100 time series (minimal aggregation benefit)
- 🔴 Team spends significant time managing recording rule configs instead of dashboards

**Consequences**:

- ❌ Prometheus storage costs increase 2-3x (each recording rule creates new series)
- ❌ Recording rule evaluation lag (CPU saturated processing 100+ rules)
- ❌ Config management overhead (every dashboard change requires Prometheus reload)
- ❌ Harder debugging (indirection between dashboard and actual metric query)
- ❌ Reduced query flexibility (recording rule is static, dashboard queries can be dynamic)

**Better Approach**:

```yaml
# ❌ ANTI-PATTERN: Recording rule for trivial query (executes in <1s)
- record: job:up:sum
  expr: sum(up) by (job)
# This is unnecessary - original query is already fast

# ✅ PREFERRED: Query directly (no recording rule needed)
# Dashboard: sum(up) by (job)

# ❌ ANTI-PATTERN: Recording rule used in only 1 place
- record: job:http_errors:rate5m
  expr: sum(rate(http_errors_total[5m])) by (job)
# Used in single dashboard panel - not worth storage cost

# ✅ PREFERRED: Query directly until reused 3+ times
# Dashboard: sum(rate(http_errors_total[5m])) by (job)

# ✅ VALID USE CASE: Recording rule for expensive query used in 5+ dashboards
- record: job:http_request_duration_seconds:p95
  expr: histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (job, le))
# Complex histogram query, 30s execution time, used in 7 dashboards
```

**Migration Strategy**:

1. **Audit Recording Rules**: List all rules with usage count (grep dashboard JSON files)
2. **Identify Low-Value Rules**: Find rules with <3 references AND execution time <5s
3. **Deprecation Plan**: Mark low-value rules for removal with 30-day notice
4. **Update Dashboards**: Replace recording rule queries with original expressions
5. **Remove Rules**: Delete from Prometheus config after dashboard migration
6. **Monitor Storage**: Confirm storage reduction after rule removal

---

### Anti-Pattern 3: Hardcoding Offset Durations Without Seasonality Analysis

**Problem**: Choosing offset duration (1h, 24h, 7d) arbitrarily without analyzing actual traffic patterns causes misaligned baselines and false positive alerts.

**Detection**:

- 🔴 Week-over-week alerts fire every weekend (24h offset doesn't account for weekly seasonality)
- 🔴 Alerts fire at same time every day (1h offset misses daily pattern, should use 24h)
- 🔴 Month-over-month comparison uses 30d offset during 31-day months (misaligned dates)
- 🔴 Alert backtest shows >50% false positive rate vs known incidents

**Consequences**:

- ❌ High false positive rate (alert fatigue, team ignores notifications)
- ❌ Missed real incidents (baseline doesn't reflect expected pattern)
- ❌ Incorrect capacity planning (comparing weekday vs weekend traffic)
- ❌ Confusing anomaly detection (alert fires during normal seasonal variations)

**Better Approach**:

```promql
# ❌ ANTI-PATTERN: Using 24h offset for traffic with weekly seasonality
(
  sum(rate(http_requests_total[5m])) -
  sum(rate(http_requests_total[5m] offset 24h))
) / sum(rate(http_requests_total[5m] offset 24h))
# Fires every Saturday/Sunday when comparing to Friday traffic

# ✅ PREFERRED: Analyze seasonality first, use 7d offset for weekly patterns
# Step 1: Visualize traffic over 14 days to identify patterns
sum(rate(http_requests_total[5m]))

# Step 2: Use 7d offset to compare same day-of-week
(
  sum(rate(http_requests_total[5m])) -
  sum(rate(http_requests_total[5m] offset 7d))
) / sum(rate(http_requests_total[5m] offset 7d))

# ❌ ANTI-PATTERN: Month-over-month with fixed 30d offset
rate(metric[5m] offset 30d)
# Misaligned during 31-day months (comparing Jan 31 to Feb 28)

# ✅ PREFERRED: Use calendar-aware time ranges (Grafana variables)
rate(metric[5m] offset $__interval)  # Grafana calculates exact month duration
```

**Migration Strategy**:

1. **Analyze Historical Data**: Plot metric over 90 days to visually identify patterns (daily, weekly, monthly cycles)
2. **Calculate Autocorrelation**: Use statistical tools to detect strongest periodicity

   ```python
   # Example: Analyze API traffic autocorrelation
   from prometheus_api_client import PrometheusConnect
   prom = PrometheusConnect(url="http://prometheus:9090")
   data = prom.custom_query_range("rate(http_requests_total[5m])", start_time, end_time, step="5m")
   # Run autocorrelation analysis to find peak at 7d lag
   ```

3. **Select Offset**: Match offset to detected periodicity (7d for weekly, 24h for daily)
4. **Backtest Alert**: Run alert query against historical data to measure false positive rate
5. **Tune Threshold**: Adjust deviation threshold until false positive rate <10%
6. **Deploy with Documentation**: Document seasonality analysis in alert annotations

---

## Integration Points

### Integration 1: Grafana Dashboards

**Relationship**: PromQL queries power Grafana visualization panels, with recording rules optimizing dashboard load performance.

**Coordination Pattern**:

- Grafana sends PromQL queries to Prometheus API (`/api/v1/query` or `/api/v1/query_range`)
- Recording rules reduce dashboard complexity (simple metric reference vs complex aggregation)
- Grafana variables enable dynamic offset selection for time-period comparisons
- Alerting rules defined in Prometheus, visualized in Grafana alert panels

**Example Usage**:

```json
// Grafana dashboard panel JSON using recording rule
{
  "targets": [
    {
      "expr": "job:http_request_duration_seconds:p95{job=\"api-server\"}",
      "legendFormat": "p95 Latency",
      "refId": "A"
    }
  ],
  "title": "API Latency (p95)"
}

// Time-period comparison panel with variable offset
{
  "targets": [
    {
      "expr": "sum(rate(http_requests_total[5m])) by (endpoint)",
      "legendFormat": "Current - {{endpoint}}",
      "refId": "A"
    },
    {
      "expr": "sum(rate(http_requests_total[5m] offset $comparison_period)) by (endpoint)",
      "legendFormat": "Baseline - {{endpoint}}",
      "refId": "B"
    }
  ],
  "title": "Traffic Comparison",
  "templating": {
    "list": [
      {
        "name": "comparison_period",
        "type": "custom",
        "options": ["1h", "24h", "7d", "30d"]
      }
    ]
  }
}
```

**Dependencies**:

- Prometheus must be configured as Grafana data source
- Recording rules must be deployed in Prometheus before dashboard references them
- Grafana alerting requires Prometheus Alertmanager integration (for notification routing)

---

### Integration 2: Prometheus Alertmanager

**Relationship**: PromQL alert rules evaluate in Prometheus, firing alerts sent to Alertmanager for routing, grouping, and notification delivery.

**Coordination Pattern**:

- Alert rules defined in Prometheus config (`.../rules/*.yml`)
- Prometheus evaluates rules at `evaluation_interval` (default 1m)
- FIRING alerts sent to Alertmanager with labels and annotations
- Alertmanager groups related alerts, applies silences, routes to receivers (Slack, PagerDuty, email)

**Example Usage**:

```yaml
# Prometheus alert rule (cardinality threshold)
groups:
  - name: cardinality_alerts
    interval: 5m
    rules:
      - alert: HighMetricCardinality
        expr: count by (__name__)({__name__=~".+"}) > 1000
        for: 15m
        labels:
          severity: warning
          team: platform
        annotations:
          summary: "Metric {{ $labels.__name__ }} has high cardinality"
          description: "{{ $value }} series detected (threshold: 1000)"
          runbook_url: "https://wiki/runbooks/cardinality-remediation"

# Alertmanager config (routes by severity and team)
route:
  receiver: default
  group_by: [alertname, team]
  routes:
    - match:
        severity: critical
        team: platform
      receiver: pagerduty-platform
    - match:
        severity: warning
      receiver: slack-engineering
```

**Dependencies**:

- Prometheus `alerting.alertmanagers` config points to Alertmanager instances
- Alertmanager `receivers` configured for notification channels (Slack webhooks, PagerDuty keys)
- Alert rules reference recording rules for complex conditions (avoid expensive evaluations)

---

### Integration 3: Kubernetes Service Discovery & Relabeling

**Relationship**: Prometheus auto-discovers Kubernetes pods/services via API and applies relabeling rules to control label cardinality and metric enrichment.

**Coordination Pattern**:

- Prometheus scrapes Kubernetes API for pod metadata (namespace, pod name, labels, annotations)
- Relabel configs transform discovered labels before storing metrics
- Label cardinality controlled by dropping high-cardinality labels (`pod_uid`, `pod_ip`)
- Kubernetes service annotations enable per-service scrape config overrides

**Example Usage**:

```yaml
# Prometheus Kubernetes scrape config with relabeling
scrape_configs:
  - job_name: kubernetes-pods
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      # Keep only pods with prometheus.io/scrape annotation
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true

      # Use pod annotations for scrape path and port
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        target_label: __metrics_path__
        regex: (.+)

      # CARDINALITY CONTROL: Drop high-cardinality pod UID
      - action: labeldrop
        regex: __meta_kubernetes_pod_uid

      # CARDINALITY CONTROL: Aggregate by namespace (not pod name)
      - source_labels: [__meta_kubernetes_namespace]
        target_label: namespace
      - source_labels: [__meta_kubernetes_pod_label_app]
        target_label: app

      # Drop pod name label (high cardinality in large clusters)
      - action: labeldrop
        regex: pod
```

**Dependencies**:

- Prometheus requires Kubernetes RBAC permissions for API access
- Pod annotations `prometheus.io/scrape`, `prometheus.io/port`, `prometheus.io/path` control scrape behavior
- Relabeling rules must balance observability (useful labels) vs cardinality (storage cost)

---

## Validation & Quality Checks

### Check 1: Cardinality Threshold Compliance

**What to Validate**: No single metric exceeds 1000 time series; total series count within Prometheus memory capacity.

**Validation Method**:

1. **Run Cardinality Audit Query**:

   ```promql
   topk(20, count by (__name__)({__name__=~".+"}))
   ```

2. **Check Total Series Count**:

   ```promql
   prometheus_tsdb_head_series
   ```

3. **Inspect High-Cardinality Metrics**: For each metric >1000 series, query label combinations:

   ```promql
   count by (__name__, job, instance)(metric_name)
   ```

**Pass Criteria**:

- ✅ No metric exceeds 1000 series (warning threshold)
- ✅ Total series <500K for typical production deployment (<4GB memory usage)
- ✅ All labels follow low-cardinality guidelines (no user IDs, session IDs, UUIDs)

**Fail Criteria**:

- ❌ Any metric >5000 series (critical threshold - immediate remediation required)
- ❌ Total series >1M (Prometheus memory exhaustion risk)
- ❌ High-cardinality labels present (user_id, request_id, ip_address, etc.)

**Remediation**:

1. Remove high-cardinality labels from metric instrumentation code
2. Create recording rule to pre-aggregate problematic metric by low-cardinality labels only
3. Migrate label data to structured logs or exemplars
4. Redeploy application and verify series count reduction

---

### Check 2: Recording Rule Naming Convention Compliance

**What to Validate**: All recording rules follow `<level>:<metric>:<operations>` naming pattern and include appropriate aggregation scope.

**Validation Method**:

1. **Extract Recording Rules**: Parse Prometheus config files

   ```bash
   grep -A2 "record:" /etc/prometheus/rules/*.yml
   ```

2. **Check Naming Pattern**: Validate format with regex:

   ```regex
   ^(instance|job|cluster|region):[a-z_]+:[a-z0-9_]+$
   ```

3. **Verify Aggregation Matches Name**: For `job:*` rules, expression must include `by (job)`:

   ```yaml
   # Valid: Name matches aggregation scope
   - record: job:http_requests:rate5m
     expr: sum(rate(http_requests_total[5m])) by (job)

   # Invalid: Name says "job:" but aggregates by "instance"
   - record: job:http_requests:rate5m
     expr: sum(rate(http_requests_total[5m])) by (instance)
   ```

**Pass Criteria**:

- ✅ All recording rules follow `<level>:<metric>:<operations>` pattern
- ✅ Aggregation scope in expression matches `<level>` prefix
- ✅ Operation suffix describes transformations (e.g., `rate5m`, `p95`, `sum`)

**Fail Criteria**:

- ❌ Generic names like `my_aggregation`, `custom_metric` (no semantic meaning)
- ❌ Mismatch between name level and aggregation scope
- ❌ Missing operation suffix (unclear what transformation applied)

**Remediation**:

1. Rename non-compliant rules following naming convention
2. Update all dashboard and alert references to new names
3. Add deprecation notices for old names (30-day grace period)
4. Document naming convention in team wiki with examples

---

### Check 3: Alert Backtest Accuracy

**What to Validate**: Time-period comparison alerts fire on known historical incidents (true positives) and do NOT fire on normal traffic variations (false positives).

**Validation Method**:

1. **Identify Historical Incidents**: List known outages/incidents from past 90 days with timestamps
2. **Run Alert Query Over Historical Range**:

   ```promql
   # Simulate alert over past 90 days (5min resolution)
   count_over_time(
     (
       (
         sum(rate(http_requests_total[5m] offset 7d)) -
         sum(rate(http_requests_total[5m]))
       ) /
       sum(rate(http_requests_total[5m] offset 7d)) > 0.3
     )[90d:5m]
   )
   ```

3. **Compare Alert Timestamps to Incident Log**:
   - True Positive: Alert fired within 15min of known incident start
   - False Positive: Alert fired when no incident occurred
   - False Negative: Incident occurred but alert did NOT fire

**Pass Criteria**:

- ✅ True positive rate >90% (alert fired on 9 out of 10 known incidents)
- ✅ False positive rate <10% (alert fired incorrectly <10% of total firing events)
- ✅ Alert latency <15min (time from incident start to alert firing)

**Fail Criteria**:

- ❌ True positive rate <70% (missing real incidents)
- ❌ False positive rate >30% (excessive noise, alert fatigue)
- ❌ Alert fires during expected seasonal variations (e.g., weekend traffic dips)

**Remediation**:

1. **If false negatives high**: Decrease deviation threshold (e.g., 30% → 20%) or shorten offset duration
2. **If false positives high**: Increase deviation threshold (e.g., 30% → 50%) or add `for` clause (e.g., `for: 15m`)
3. **If seasonal mismatch**: Adjust offset duration to match detected seasonality (24h → 7d for weekly patterns)
4. **Add exclusions**: Use label filters to exclude known expected variations (holidays, maintenance windows)

---

## Common Pitfalls & Solutions

| Pitfall                                   | Detection                                                     | Solution                                                                 |
| ----------------------------------------- | ------------------------------------------------------------- | ------------------------------------------------------------------------ |
| High-cardinality user_id labels          | Metric >10K series, Prometheus memory growth                 | Remove user_id from labels, use structured logs or exemplars            |
| Recording rule evaluation lag             | Prometheus rule evaluation >interval duration                 | Increase evaluation interval or simplify aggregation expression         |
| Offset comparison missing data            | Dashboard shows "No data" or alerts flap                      | Add `or vector(0)` for zero-fill or `absent()` for gap detection        |
| Wrong offset duration (seasonality)       | Alerts fire every weekend or at same time daily               | Analyze traffic autocorrelation, match offset to detected periodicity   |
| Division by zero in % change              | Alert fails with "division by zero" error                     | Add `or vector(1)` to denominator in division expressions               |
| Recording rule name doesn't match scope   | Confusion when querying (is it job or instance level?)        | Follow `<level>:<metric>:<operations>` naming convention                |
| Too many recording rules (storage bloat)  | Prometheus storage >50% growth, many rules with <3 references | Audit rules, remove low-value ones, query directly for simple cases     |
| Alert threshold too sensitive             | >50% false positive rate, alert fatigue                       | Backtest on historical data, increase deviation threshold               |
| Histogram percentile without rate()       | P95 values incorrect or query fails                           | Always wrap `histogram_quantile()` with `rate()` or `increase()`        |
| Forgetting `for` clause in alerts         | Alerts fire on transient spikes (<1min)                       | Add `for: 15m` to require sustained condition before firing             |
| Using `avg()` instead of quantile for SLO | SLO target missed due to tail latency masking                 | Use `histogram_quantile(0.95, ...)` instead of `avg(...)` for latency   |
| Label name collisions in relabeling       | Original label overwritten by Kubernetes metadata             | Use unique target label names (`k8s_namespace` not `namespace`)         |
| Hard-coded time ranges in queries         | Dashboard breaks when changing time range picker              | Use Grafana variables `$__range` instead of fixed `[5m]` ranges         |
| Recording rule with no downstream usage   | Storage waste, rule never queried                             | Add usage comments to rule config, deprecate after 90 days if unused    |

---

## Tools & Resources

### Recommended Tools

1. **promtool**
   - **Purpose**: Validates PromQL syntax and rule configs offline before deployment
   - **When to Use**: Pre-commit checks for recording rules and alerts, CI/CD pipeline validation
   - **Documentation**: [https://prometheus.io/docs/prometheus/latest/command-line/promtool/](https://prometheus.io/docs/prometheus/latest/command-line/promtool/)
   - **Example**:

     ```bash
     # Validate recording rules syntax
     promtool check rules /etc/prometheus/rules/recording_rules.yml

     # Test alert expression matches expected results
     promtool test rules /etc/prometheus/rules/tests.yml
     ```

2. **PromLens**
   - **Purpose**: Visual PromQL query builder with execution plan analysis and performance profiling
   - **When to Use**: Learning PromQL, debugging slow queries, optimizing aggregations
   - **Documentation**: [https://promlens.com/](https://promlens.com/)
   - **Example**: Paste complex query → View tree structure → Identify expensive operations → Suggest recording rule

3. **Prometheus API Client (Python)**
   - **Purpose**: Programmatic query execution for backtesting alerts and cardinality analysis
   - **When to Use**: Automated cardinality audits, alert validation, historical data analysis
   - **Documentation**: [https://github.com/4n4nd/prometheus-api-client-python](https://github.com/4n4nd/prometheus-api-client-python)
   - **Example**:

     ```python
     from prometheus_api_client import PrometheusConnect
     prom = PrometheusConnect(url="http://prometheus:9090")
     cardinality = prom.custom_query('count by (__name__)({__name__=~".+"})')
     print(f"High-cardinality metrics: {[m for m in cardinality if int(m['value'][1]) > 1000]}")
     ```

4. **Grafana Explore**
   - **Purpose**: Interactive PromQL query playground with instant visualization and metrics browser
   - **When to Use**: Ad-hoc metric exploration, query prototyping before dashboard creation
   - **Documentation**: [https://grafana.com/docs/grafana/latest/explore/](https://grafana.com/docs/grafana/latest/explore/)
   - **Example**: Select metric from dropdown → Add filters → View instant graph → Export to dashboard panel

---

### Learning Resources

1. **Prometheus Best Practices - Official Documentation**: [https://prometheus.io/docs/practices/](https://prometheus.io/docs/practices/)
   - **Topic**: Metric naming, label design, recording rules, instrumentation patterns
   - **Quality**: High (authoritative source, regularly updated)

2. **PromQL Cheat Sheet by PrometheusLabs**: [https://promlabs.com/promql-cheat-sheet/](https://promlabs.com/promql-cheat-sheet/)
   - **Topic**: Quick reference for aggregation operators, functions, range vectors
   - **Quality**: High (curated by Prometheus experts, includes real-world examples)

3. **Robust Perception Blog - PromQL Deep Dives**: [https://www.robustperception.io/blog/](https://www.robustperception.io/blog/)
   - **Topic**: Advanced PromQL patterns, cardinality optimization, recording rule design
   - **Quality**: High (written by Prometheus core contributor Brian Brazil)

4. **Grafana Labs - PromQL Tutorial Series**: [https://grafana.com/blog/2020/02/04/introduction-to-promql-the-prometheus-query-language/](https://grafana.com/blog/2020/02/04/introduction-to-promql-the-prometheus-query-language/)
   - **Topic**: Beginner to intermediate PromQL with Grafana integration examples
   - **Quality**: Medium-High (good for learning basics, less depth than Robust Perception)

5. **Cardinality Explorer Tool**: [https://github.com/prometheus/prometheus/tree/main/documentation/examples/cardinality](https://github.com/prometheus/prometheus/tree/main/documentation/examples/cardinality)
   - **Topic**: Scripts and queries for cardinality auditing and visualization
   - **Quality**: Medium (community-contributed examples, not officially maintained)

---

## Glossary

- **Label Cardinality**: Number of unique time series created by all combinations of label values for a given metric. Example: `http_requests_total{method, status_code}` with 4 methods × 10 status codes = 40 cardinality.
- **Recording Rule**: Precomputed PromQL query stored as a new metric to optimize dashboard performance and enable complex real-time aggregations.
- **Offset Modifier**: PromQL syntax `metric offset <duration>` to shift query time window backwards for historical comparison (e.g., `rate(metric[5m] offset 7d)`).
- **Time Series**: Unique combination of metric name + label set with associated timestamp-value pairs. Example: `cpu_usage{host="server1", region="us-east"}` is one time series.
- **Scrape Interval**: Frequency at which Prometheus collects metrics from targets (default 15s). Recording rule evaluation intervals should be ≥4x scrape_interval.
- **Exemplar**: Trace sample attached to metric aggregation without creating new time series. Enables drill-down into individual requests while maintaining low cardinality.
- **High-Cardinality Label**: Label with unbounded or very large number of unique values (e.g., user_id, request_id, ip_address). Should be avoided in metric labels.
- **Aggregation Operator**: PromQL function that combines multiple time series (e.g., `sum()`, `avg()`, `max()`, `topk()`, `count()`).
- **Range Vector**: Metric query over a time window (e.g., `http_requests_total[5m]`). Required for `rate()`, `increase()`, and `histogram_quantile()` functions.
- **Instant Vector**: Metric query at a single timestamp (e.g., `http_requests_total`). Result of most aggregations and arithmetic operations.

---

## Sources & References

1. **Prometheus Official Documentation - Querying Basics**: [https://prometheus.io/docs/prometheus/latest/querying/basics/](https://prometheus.io/docs/prometheus/latest/querying/basics/)
   - Accessed: 2025-11-10
   - Confidence: 1.0 (authoritative source)

2. **Prometheus Best Practices - Metric and Label Naming**: [https://prometheus.io/docs/practices/naming/](https://prometheus.io/docs/practices/naming/)
   - Accessed: 2025-11-10
   - Confidence: 1.0 (official guidelines)

3. **Prometheus Configuration - Recording Rules**: [https://prometheus.io/docs/prometheus/latest/configuration/recording_rules/](https://prometheus.io/docs/prometheus/latest/configuration/recording_rules/)
   - Accessed: 2025-11-10
   - Confidence: 1.0 (official configuration reference)

4. **Robust Perception - Cardinality is Key**: [https://www.robustperception.io/cardinality-is-key](https://www.robustperception.io/cardinality-is-key)
   - Accessed: 2025-11-10
   - Confidence: 0.95 (expert opinion from Prometheus core contributor)

5. **Grafana Blog - Introduction to PromQL**: [https://grafana.com/blog/2020/02/04/introduction-to-promql-the-prometheus-query-language/](https://grafana.com/blog/2020/02/04/introduction-to-promql-the-prometheus-query-language/)
   - Accessed: 2025-11-10
   - Confidence: 0.9 (reputable source with practical examples)

6. **PromLabs PromQL Cheat Sheet**: [https://promlabs.com/promql-cheat-sheet/](https://promlabs.com/promql-cheat-sheet/)
   - Accessed: 2025-11-10
   - Confidence: 0.9 (curated reference by Prometheus experts)

---

## Changelog

- **2025-11-10T18:00:00Z**: Initial documentation created (confidence: 0.85) - Synthesized from official Prometheus docs, expert blog posts, and industry best practices for label cardinality management, recording rules, and offset patterns.

---

## Related Documentation

- **Grafana Dashboard Builder Guide**: `C:/Users/kemos/Repos/gauntlet-agents/docs/04-guides/grafana-dashboard-builder/` (integration with PromQL queries)
- **Loki Query Specialist Guide**: `C:/Users/kemos/Repos/gauntlet-agents/.claude/agents/loki-query-specialist.md` (LogQL patterns for complementary log analysis)
- **Observability Stack Overview**: `C:/Users/kemos/Repos/gauntlet-agents/docs/04-guides/observability/INDEX.md` (Prometheus role in monitoring architecture)
- **Kubernetes Metrics Collection**: `C:/Users/kemos/Repos/gauntlet-agents/docs/04-guides/kubernetes/prometheus-operator-guide.md` (service discovery and relabeling patterns)
