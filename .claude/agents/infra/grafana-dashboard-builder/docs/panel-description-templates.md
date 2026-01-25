# Panel Description Templates for Grafana Dashboards

**Purpose**: Reusable panel description templates following the WHY/WHAT/HOW/WHEN framework

**Quick Reference**: Copy-paste templates for common panel types with placeholder customization

---

## Section 1: Template Structure - The 4-Question Framework

Every Grafana panel description should answer these four critical questions to provide actionable context:

### 1. WHY (Business Impact)
**Purpose**: Explain why this metric matters to business operations, user experience, or system reliability.

**Format**: `"[Metric] directly impacts [business outcome] because [reason]. When [threshold condition], [consequence occurs]."`

**Example**: "Response latency directly impacts user satisfaction because delays >500ms cause 20% cart abandonment. When p95 exceeds 500ms, revenue drops measurably."

### 2. WHAT (Calculation)
**Purpose**: Define exactly what is being measured and how the calculation works.

**Format**: `"Tracks [metric_name] calculated as [formula]. Aggregation: [method] across [dimension]. Time window: [interval]."`

**Example**: "Tracks `http_request_duration_seconds` calculated as histogram percentiles (p50/p95/p99). Aggregation: histogram_quantile() across all service instances. Time window: $__rate_interval."

### 3. HOW (Interpretation)
**Purpose**: Teach users how to read the visualization and what patterns indicate problems.

**Format**: `"Visualization: [type]. Y-axis: [unit]. Expected baseline: [value]. Warning patterns: [condition]. Critical patterns: [condition]."`

**Example**: "Visualization: Time series line graph. Y-axis: milliseconds. Expected baseline: <100ms p95. Warning patterns: spikes >200ms. Critical patterns: sustained >500ms or increasing trend."

### 4. WHEN (Action Threshold)
**Purpose**: Define concrete thresholds for action and who should respond.

**Format**: `"Green: [condition] (no action). Yellow: [condition] (investigate within [timeframe]). Red: [condition] (immediate action required). Owner: [team/role]."`

**Example**: "Green: p95 <200ms (no action). Yellow: 200-500ms (investigate within 15 minutes, check upstream dependencies). Red: >500ms sustained for 5 minutes (immediate escalation to on-call engineer). Owner: Platform SRE team."

---

## Section 2: Templates by Panel Type

### Template 1: Latency Percentiles (Time Series)

```markdown
**WHY**: Response latency percentiles reveal user experience quality and identify performance degradation before it impacts all users. The [Service] latency directly affects [business metric] - when p95 exceeds [SLO threshold]ms, [specific consequence like "conversion rates drop by X%"].

**WHAT**: Tracks `[metric_name_duration_seconds]` histogram calculated as percentiles using `histogram_quantile()`. Shows p50 (median user experience), p95 (worst 5% of requests), and p99 (tail latency). Aggregation: across all [service_name] instances using $__rate_interval for rate calculation.

**HOW**: Time series visualization with three lines (p50/blue, p95/yellow, p99/red). Y-axis in milliseconds. Lower is better. Expected baseline: p50 <[X]ms, p95 <[Y]ms, p99 <[Z]ms. Warning pattern: p95 diverging from p50 indicates inconsistent performance. Critical pattern: all percentiles rising together suggests systemic bottleneck.

**WHEN**:
- Green: p95 <[SLO_value]ms (no action, within SLO)
- Yellow: p95 [SLO_value]-[1.5×SLO]ms sustained >2 minutes (investigate, check dependencies/CPU/memory, review recent deployments)
- Red: p95 >[2×SLO]ms or p99 >[3×SLO]ms sustained >5 minutes (immediate action, page on-call SRE, enable debug logging, check error logs)
- Owner: [Team Name] SRE
```

**Customization placeholders**: `[Service]`, `[business metric]`, `[specific consequence]`, `[SLO threshold]`, `[metric_name]`, `[service_name]`, `[X/Y/Z]` (baseline values), `[SLO_value]`, `[Team Name]`

---

### Template 2: Error Rates (Stat Panel)

```markdown
**WHY**: Error rate is a direct indicator of service reliability and user-facing failures. Every 1% increase in [Service] error rate costs approximately [cost_impact] in lost revenue and [support_tickets] additional support tickets. When error rate exceeds [threshold]%, [consequence like "users experience failures and churn increases"].

**WHAT**: Tracks `[metric_errors_total]` calculated as `(sum(rate(errors)) / sum(rate(requests))) * 100`. Shows percentage of failed requests over total requests. Time window: last [duration] using $__rate_interval. Error definition: HTTP 5xx responses, exceptions, timeouts, or circuit breaker trips.

**HOW**: Stat panel with large percentage value and sparkline showing 1-hour trend. Color coded by threshold (green/yellow/red). Current value represents error rate in last [time_window]. Sparkline reveals if errors are increasing, stable, or decreasing. Sudden spikes indicate incidents; gradual increases suggest degradation.

**WHEN**:
- Green: <[error_budget]% (no action, within error budget, normal operation)
- Yellow: [error_budget]-[2×error_budget]% (investigate within [timeframe], review logs for error patterns, check recent changes, monitor for escalation)
- Red: >[2×error_budget]% or any value >5% sustained >2 minutes (immediate action, page on-call, rollback recent deployment if applicable, activate incident response)
- Owner: [Team Name] On-Call Engineer
```

**Customization placeholders**: `[Service]`, `[cost_impact]`, `[support_tickets]`, `[threshold]`, `[consequence]`, `[metric_errors_total]`, `[duration]`, `[time_window]`, `[error_budget]`, `[timeframe]`, `[Team Name]`

---

### Template 3: Resource Utilization (Gauge)

```markdown
**WHY**: [Resource Type] utilization indicates capacity headroom and scaling needs. When [Resource] exceeds [threshold]%, [Service] experiences [performance impact]. High utilization costs [cost_consequence] in [metric like "compute costs" or "degraded throughput"].

**WHAT**: Tracks `[resource_metric]` calculated as `(used / total) * 100`. Formula: `[specific_calculation]`. Shows percentage of [Resource] consumed by [workload/service]. Aggregation: [method like "average" or "max"] across [dimension like "all instances" or "per pod"]. Updated every [refresh_interval].

**HOW**: Gauge visualization with 0-100% scale. Needle position shows current utilization. Threshold markers at [green_limit]% (green), [yellow_limit]% (yellow), [red_limit]% (red). Expected range: [normal_range]% during business hours, [off_hours_range]% off-peak. Sustained high utilization indicates need for scaling or optimization.

**WHEN**:
- Green: <[green_limit]% (no action, healthy headroom, normal operation)
- Yellow: [yellow_limit]-[red_limit]% (plan capacity increase within [timeframe], review utilization trends, schedule scaling evaluation)
- Red: >[red_limit]% or >[yellow_limit]% sustained >10 minutes (immediate action, scale up resources, review workload for optimization opportunities, investigate memory leaks or runaway processes)
- Critical: >95% (emergency scaling, consider load shedding or traffic reduction)
- Owner: [Team Name] Platform Engineering
```

**Customization placeholders**: `[Resource Type]`, `[threshold]`, `[Service]`, `[performance impact]`, `[cost_consequence]`, `[metric]`, `[resource_metric]`, `[specific_calculation]`, `[workload/service]`, `[method]`, `[dimension]`, `[refresh_interval]`, `[green_limit]`, `[yellow_limit]`, `[red_limit]`, `[normal_range]`, `[off_hours_range]`, `[timeframe]`, `[Team Name]`

---

### Template 4: Log Volume (Bar Chart)

```markdown
**WHY**: Log volume patterns detect anomalies, incidents, and cost overruns. [Service] log volume spikes correlate with [incident_type]. Sustained high volume costs [cost_per_GB] per GB in storage and [processing_cost] in log processing. When log volume exceeds [threshold] logs/sec, [consequence].

**WHAT**: Tracks log count from [log_source] calculated as `sum(rate([log_metric][$__rate_interval]))` grouped by [dimension like "log level" or "service"]. Shows logs per second for last [time_window]. Baseline expectation: [normal_volume] logs/sec during business hours. Count methodology: [explain any sampling or filtering].

**HOW**: Bar chart with horizontal bars, one per [dimension]. X-axis: logs per second. Bars sorted descending (highest volume first). Color coding: green (<baseline), yellow (1-2× baseline), red (>2× baseline). Compare current values to [comparison_period] baseline. Spike investigation: drill into time series, filter by log level (ERROR/WARN), correlate with deployment events.

**WHEN**:
- Green: Within [normal_range] of baseline (no action, normal operation)
- Yellow: [yellow_multiplier]× baseline sustained >5 minutes (investigate, check for application errors, review recent deployments, verify not a planned load test)
- Red: [red_multiplier]× baseline or >10,000 logs/sec sustained >3 minutes (immediate action, identify log source, check for log loops, consider rate limiting, review cost impact)
- Investigation steps: Filter by log level → Identify top services → Check recent deployments → Review application error logs
- Owner: [Team Name] Observability Team
```

**Customization placeholders**: `[Service]`, `[incident_type]`, `[cost_per_GB]`, `[processing_cost]`, `[threshold]`, `[consequence]`, `[log_source]`, `[log_metric]`, `[dimension]`, `[time_window]`, `[normal_volume]`, `[comparison_period]`, `[normal_range]`, `[yellow_multiplier]`, `[red_multiplier]`, `[Team Name]`

---

### Template 5: Cache Hit Rate (Stat Panel)

```markdown
**WHY**: Cache hit rate directly impacts response latency and backend load. Every 10% drop in [Cache Type] hit rate causes [latency_increase]ms average latency increase and [load_increase]% increase in [backend_system] load. Low hit rates cost [cost_impact] in additional [resource like "database queries" or "API calls"]. When hit rate drops below [threshold]%, [consequence].

**WHAT**: Tracks cache efficiency calculated as `(cache_hits / (cache_hits + cache_misses)) * 100`. Formula: `sum(rate([hit_metric][$__rate_interval])) / (sum(rate([hit_metric][$__rate_interval])) + sum(rate([miss_metric][$__rate_interval]))) * 100`. Shows percentage of cache requests served from cache vs. requiring backend fetch. Time window: last [duration].

**HOW**: Stat panel showing percentage with sparkline trend. Higher is better. Color coded by threshold. Expected range: [target_range]% for [Cache Type]. Sparkline reveals cache warming status (rising after deployment) or degradation (falling during load). Sudden drops indicate cache invalidation events or cold cache restarts.

**WHEN**:
- Green: >[green_threshold]% (no action, cache performing optimally)
- Yellow: [yellow_threshold]-[green_threshold]% (investigate within [timeframe], check cache size configuration, review eviction policy, analyze access patterns for optimization)
- Red: <[yellow_threshold]% sustained >5 minutes (immediate action, check if cache is full, review TTL settings, investigate if cache warming is needed post-deployment, check for cache key hotspots)
- Cost impact: <70% hit rate = [high_cost_consequence]
- Owner: [Team Name] Backend Engineering
```

**Customization placeholders**: `[Cache Type]`, `[latency_increase]`, `[load_increase]`, `[backend_system]`, `[cost_impact]`, `[resource]`, `[threshold]`, `[consequence]`, `[hit_metric]`, `[miss_metric]`, `[duration]`, `[target_range]`, `[green_threshold]`, `[yellow_threshold]`, `[timeframe]`, `[high_cost_consequence]`, `[Team Name]`

---

### Template 6: Request Rate (Time Series)

```markdown
**WHY**: Request rate reveals traffic patterns, capacity planning needs, and incident detection. [Service] request rate determines [scaling_decision] and costs [cost_per_1000_req] per 1000 requests. When request rate exceeds [threshold] req/sec, [consequence like "autoscaling triggers" or "rate limiting activates"]. Sudden drops indicate outages or client-side failures.

**WHAT**: Tracks incoming request count calculated as `sum(rate([request_metric][$__rate_interval]))` grouped by [dimension like "endpoint" or "status code"]. Shows requests per second aggregated across all [service] instances. Baseline expectation: [baseline_traffic] req/sec during business hours, [off_hours_traffic] req/sec off-peak. Spikes indicate [event_types like "traffic bursts, DDoS attempts, or legitimate load tests"].

**HOW**: Time series line graph. Y-axis: requests per second. Multiple lines if grouped by [dimension]. Expected patterns: diurnal cycle (peak [peak_hours], trough [trough_hours]), weekly pattern ([weekly_pattern description]). Warning pattern: sustained 2× baseline without corresponding business event. Critical pattern: sudden drop to zero (outage) or spike >5× baseline (attack or viral event).

**WHEN**:
- Green: Within [normal_multiplier]× baseline for time of day (no action, normal traffic)
- Yellow: [yellow_multiplier]× baseline sustained >3 minutes (capacity planning review, verify autoscaling working, check response latency for degradation)
- Red: >[red_multiplier]× baseline sustained >2 minutes (immediate action, verify not DDoS attack, check rate limiting configuration, scale proactively if legitimate traffic, review upstream client behavior) OR <10% of baseline for >1 minute (outage, investigate load balancer health, check DNS, verify service availability)
- Capacity planning threshold: Sustained traffic >[capacity_threshold]× baseline requires architecture review
- Owner: [Team Name] SRE + Infrastructure
```

**Customization placeholders**: `[Service]`, `[scaling_decision]`, `[cost_per_1000_req]`, `[threshold]`, `[consequence]`, `[request_metric]`, `[dimension]`, `[service]`, `[baseline_traffic]`, `[off_hours_traffic]`, `[event_types]`, `[peak_hours]`, `[trough_hours]`, `[weekly_pattern]`, `[normal_multiplier]`, `[yellow_multiplier]`, `[red_multiplier]`, `[capacity_threshold]`, `[Team Name]`

---

### Template 7: Saturation Metrics (Gauge)

```markdown
**WHY**: [Resource] saturation indicates resource exhaustion and queueing delays. When [Resource] saturation exceeds [threshold]%, [Service] experiences [performance_impact like "request queuing, timeouts, or dropped connections"]. High saturation precedes outages and requires preemptive scaling.

**WHAT**: Tracks [saturation_metric] calculated as [formula like "queue_depth / queue_capacity" or "connection_pool_active / connection_pool_max"]. Shows [Resource] demand vs. capacity ratio as percentage. Formula: `([current_usage] / [capacity_limit]) * 100`. Aggregation: [method] across [scope]. Capacity limit: [limit_value] [units].

**HOW**: Gauge visualization with 0-100% scale. Needle shows current saturation level. Threshold markers: green (<[green_limit]%), yellow ([yellow_limit]%), red (>[red_limit]%). Expected range: <[normal_limit]% during normal operation. Sustained saturation >[yellow_limit]% indicates resource constraint. Interpretation: [resource-specific guidance like "queue depth >80% means requests are waiting, check processing rate"].

**WHEN**:
- Green: <[green_limit]% (no action, sufficient capacity headroom)
- Yellow: [yellow_limit]-[red_limit]% (monitor closely, review [resource] allocation, check if temporary spike or sustained trend, prepare to scale)
- Red: >[red_limit]% sustained >2 minutes (immediate action, scale [resource] capacity, investigate [specific_causes like "slow consumers, increased load, or resource leak"], check queue flush rate vs. enqueue rate)
- Critical: >95% or [specific_condition like "queue depth approaching limit"] (emergency response, consider traffic shedding, reject non-critical requests, alert on-call immediately)
- Owner: [Team Name] Platform SRE
```

**Customization placeholders**: `[Resource]`, `[threshold]`, `[Service]`, `[performance_impact]`, `[saturation_metric]`, `[formula]`, `[Resource]`, `[current_usage]`, `[capacity_limit]`, `[method]`, `[scope]`, `[limit_value]`, `[units]`, `[green_limit]`, `[yellow_limit]`, `[red_limit]`, `[normal_limit]`, `[resource-specific guidance]`, `[specific_causes]`, `[Team Name]`

---

### Template 8: Network Traffic (Time Series)

```markdown
**WHY**: Network traffic patterns detect anomalies, capacity constraints, and security incidents. [Service] network usage costs [cost_per_GB] per GB egress and impacts [performance_metric]. When TX/RX exceeds [threshold] Mbps, [consequence like "bandwidth throttling occurs" or "costs escalate"]. Asymmetric traffic patterns may indicate data exfiltration or DDoS attacks.

**WHAT**: Tracks network bytes transmitted (TX) and received (RX) calculated as `rate([network_metric_tx][$__rate_interval])` and `rate([network_metric_rx][$__rate_interval])`. Shows Mbps for [interface/service]. Aggregation: sum across [dimension like "all pods" or "per node"]. Baseline: [baseline_tx] Mbps TX, [baseline_rx] Mbps RX during business hours. Bandwidth capacity: [total_bandwidth] Mbps.

**HOW**: Time series with two lines (TX/blue, RX/green). Y-axis: Mbps (megabits per second). Expected pattern: TX > RX for [service_type like "API services"], RX > TX for [service_type like "data ingestion"]. Warning pattern: sustained traffic approaching [warning_percent]% of bandwidth capacity. Critical pattern: asymmetric spike (TX >>RX or vice versa without explanation), sudden drop to zero (network failure).

**WHEN**:
- Green: Within [normal_range]% of bandwidth capacity (no action, normal traffic)
- Yellow: [yellow_percent]-[red_percent]% of capacity sustained >5 minutes (capacity planning review, check for data transfer inefficiencies, review large payload endpoints)
- Red: >[red_percent]% of capacity sustained >3 minutes (immediate action, identify top bandwidth consumers, check for misconfigured retries or data duplication, consider traffic shaping) OR asymmetric traffic >10× normal ratio (security review, investigate for data exfiltration or attack)
- Cost threshold: Sustained egress >[cost_threshold] GB/hour triggers cost review
- Owner: [Team Name] Network Engineering + Security
```

**Customization placeholders**: `[Service]`, `[cost_per_GB]`, `[performance_metric]`, `[threshold]`, `[consequence]`, `[network_metric_tx]`, `[network_metric_rx]`, `[interface/service]`, `[dimension]`, `[baseline_tx]`, `[baseline_rx]`, `[total_bandwidth]`, `[service_type]` (2 instances), `[warning_percent]`, `[normal_range]`, `[yellow_percent]`, `[red_percent]`, `[cost_threshold]`, `[Team Name]`

---

### Template 9: Cost Tracking (Stat Panel)

```markdown
**WHY**: Real-time cost visibility prevents budget overruns and identifies optimization opportunities. [Service/Resource] costs [current_cost] per [time_unit] at current utilization. When costs exceed [budget_threshold] per [time_unit], [consequence like "monthly budget exhausted early" or "CFO review triggered"]. Cost spikes >50% require immediate investigation to prevent waste.

**WHAT**: Tracks estimated cost calculated as [formula like "(instance_count × hourly_rate) + (storage_gb × storage_rate) + (network_gb × network_rate)"]. Shows cost per [hour/day/month] for [service/resource]. Current rate: [current_rate] [currency] per [time_unit]. Monthly projection: [monthly_projection] at current rate. Budget allocation: [budget_amount] per month.

**HOW**: Stat panel with currency value and sparkline showing [time_window] trend. Color coded by budget threshold. Sparkline reveals cost trends (rising = scaling or inefficiency, flat = stable, falling = optimization success). Compare current value to [comparison_period] for [percentage] change. Sudden spikes indicate [possible_causes like "autoscaling event, data transfer spike, or misconfigured resource"].

**WHEN**:
- Green: <[green_percent]% of monthly budget (no action, within budget, cost-efficient operation)
- Yellow: [yellow_percent]-[red_percent]% of monthly budget (cost review, identify top cost contributors, evaluate optimization opportunities, review resource utilization for waste)
- Red: >[red_percent]% of budget or daily cost exceeds [daily_limit] [currency] (immediate action, identify cost spike cause, pause non-critical workloads if necessary, implement cost controls, escalate to FinOps team)
- Optimization threshold: Any cost increase >[optimization_threshold]% without corresponding traffic increase warrants optimization review
- Owner: [Team Name] FinOps + Engineering Manager
```

**Customization placeholders**: `[Service/Resource]`, `[current_cost]`, `[time_unit]` (multiple instances), `[budget_threshold]`, `[consequence]`, `[formula]`, `[service/resource]`, `[current_rate]`, `[currency]` (multiple instances), `[monthly_projection]`, `[budget_amount]`, `[time_window]`, `[comparison_period]`, `[percentage]`, `[possible_causes]`, `[green_percent]`, `[yellow_percent]`, `[red_percent]`, `[daily_limit]`, `[optimization_threshold]`, `[Team Name]`

---

### Template 10: Token Usage (Stacked Area)

```markdown
**WHY**: LLM token consumption directly impacts operational costs and service viability. [Service] token usage costs [cost_per_1M_tokens] per million tokens (input: [input_cost], output: [output_cost], cache: [cache_cost]). When token usage exceeds [threshold] tokens/hour, [consequence like "daily budget exhausted in X hours" or "rate limits approached"]. Cache hit optimization saves [cache_savings_percent]% of token costs.

**WHAT**: Tracks token consumption by type: input tokens (prompt), output tokens (completion), cached tokens (prompt caching). Calculated as `sum(rate([token_metric_input][$__rate_interval]))`, `sum(rate([token_metric_output][$__rate_interval]))`, `sum(rate([token_metric_cached][$__rate_interval]))`. Shows tokens per second stacked by type. Cost formula: `(input_tokens × [input_cost_per_1M] + output_tokens × [output_cost_per_1M] + cached_tokens × [cache_cost_per_1M]) / 1,000,000`.

**HOW**: Stacked area chart with three layers: input (blue, bottom), output (green, middle), cached (yellow, top). Y-axis: tokens per second. Total height = total token consumption. Expected ratio: input:[input_ratio]%, output:[output_ratio]%, cached:[cache_ratio]%. Warning pattern: output tokens growing faster than input (verbose responses, potential prompt optimization needed). Cost-efficient pattern: cached tokens >30% of total (effective prompt caching).

**WHEN**:
- Green: <[green_threshold] tokens/sec, cache hit rate >[cache_target]% (no action, cost-efficient operation)
- Yellow: [yellow_threshold]-[red_threshold] tokens/sec or cache hit rate <[cache_warning]% (optimize prompts, review response verbosity, investigate cache misses, consider prompt compression techniques)
- Red: >[red_threshold] tokens/sec sustained >5 minutes or cache hit <[cache_critical]% (immediate action, implement rate limiting, review top consumers, optimize prompts urgently, check for prompt injection or abuse)
- Cost optimization targets: Input tokens <[input_target]% of total, output tokens <[output_target]%, cached >[cache_target]%
- Owner: [Team Name] AI Engineering + FinOps
```

**Customization placeholders**: `[Service]`, `[cost_per_1M_tokens]`, `[input_cost]`, `[output_cost]`, `[cache_cost]`, `[threshold]`, `[consequence]`, `[cache_savings_percent]`, `[token_metric_input]`, `[token_metric_output]`, `[token_metric_cached]`, `[input_cost_per_1M]`, `[output_cost_per_1M]`, `[cache_cost_per_1M]`, `[input_ratio]`, `[output_ratio]`, `[cache_ratio]`, `[green_threshold]`, `[cache_target]`, `[yellow_threshold]`, `[red_threshold]`, `[cache_warning]`, `[cache_critical]`, `[input_target]`, `[output_target]`, `[Team Name]`

---

## Section 3: Anti-Pattern Examples

### Anti-Pattern 1: Generic "Tracks X metric" Description

**BAD EXAMPLE** (vague, no actionable context):
```markdown
CPU Usage gauge display. Tracks avg metric. Thresholds indicate acceptable ranges.
```

**Why This Fails**:
- No business impact (WHY): Why does CPU usage matter?
- Missing calculation details (WHAT): Avg of what? Over what time window?
- No interpretation guidance (HOW): What's the baseline? What patterns indicate problems?
- No action thresholds (WHEN): What's "acceptable"? When should someone intervene?

**GOOD EXAMPLE** (actionable, complete context):
```markdown
**WHY**: CPU utilization above 85% causes request queuing and latency spikes >500ms, impacting user experience. Every 10% increase above 80% correlates with 2× latency increase.

**WHAT**: Tracks `node_cpu_seconds_total` calculated as `100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)`. Shows average CPU usage across all cores for the last 5 minutes.

**HOW**: Gauge with 0-100% scale. Expected baseline: 40-60% during business hours, <30% off-peak. Warning pattern: sustained >70%. Critical pattern: >85% for >3 minutes.

**WHEN**: Green <70% (normal) | Yellow 70-85% (investigate within 15 min, check top processes) | Red >85% (immediate scaling, review resource-intensive workloads) | Owner: Platform SRE
```

---

### Anti-Pattern 2: Missing Formulas or Calculations

**BAD EXAMPLE** (calculation unclear):
```markdown
Error rate percentage. Shows failed requests. Red means bad.
```

**Why This Fails**:
- No formula (WHAT): How is error rate calculated? What counts as an error?
- Missing numerator/denominator: Errors per what? Per request? Per second?
- Vague interpretation (HOW): "Red means bad" - what specific value triggers red?
- No time window: Is this instantaneous? Over 1 minute? 1 hour?

**GOOD EXAMPLE** (formula explicit):
```markdown
**WHY**: Error rate >1% violates our 99% availability SLO and causes customer churn (1% error rate = $5K revenue loss per hour).

**WHAT**: Tracks error percentage calculated as `(sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))) * 100`. Numerator: HTTP 5xx responses. Denominator: all HTTP requests. Time window: 5-minute rolling average.

**HOW**: Stat panel with percentage value. Expected baseline: <0.1%. Sudden spikes indicate deployment issues or dependency failures.

**WHEN**: Green <0.5% (within SLO) | Yellow 0.5-1% (investigate, check logs for error patterns) | Red >1% sustained >2 min (immediate rollback, page on-call) | Owner: Service SRE
```

---

### Anti-Pattern 3: No Threshold Explanations

**BAD EXAMPLE** (thresholds without context):
```markdown
Memory usage. Green: <70%. Yellow: 70-85%. Red: >85%.
```

**Why This Fails**:
- No WHY: Why do these thresholds matter? What happens at 85%?
- Missing consequences: What breaks at red threshold?
- No action guidance: What should someone do at yellow? At red?
- No time component: Is yellow for 1 second the same as yellow for 10 minutes?

**GOOD EXAMPLE** (thresholds with context and consequences):
```markdown
**WHY**: Memory utilization >85% triggers OOM (out of memory) killer, causing pod restarts and service disruption. Each restart costs 30 seconds of downtime.

**WHAT**: Tracks `container_memory_working_set_bytes / container_spec_memory_limit_bytes * 100`. Shows percentage of memory limit consumed. Kubernetes kills pods at 100%.

**HOW**: Gauge visualization. Expected baseline: 50-70%. Warning pattern: steady increase (memory leak). Critical pattern: >85% sustained (imminent OOM).

**WHEN**:
- Green <70% (healthy headroom, no action)
- Yellow 70-85% sustained >5 min (investigate, check for memory leaks, review top consumers, consider increasing memory limit)
- Red >85% sustained >2 min (immediate action, scale up pod memory, restart pod preemptively to avoid OOM kill, investigate memory leak urgently)
- Emergency >95% (imminent OOM, restart pod now)
- Owner: Platform SRE + App Team
```

---

### Anti-Pattern 4: No Action Guidance

**BAD EXAMPLE** (metric without action context):
```markdown
Shows request latency over time. Useful for monitoring performance.
```

**Why This Fails**:
- No WHEN: What latency value requires action?
- Missing SLO context: What's the target latency?
- No investigation steps: What should someone check when latency is high?
- No ownership: Who is responsible for responding?

**GOOD EXAMPLE** (clear action guidance):
```markdown
**WHY**: Request latency p95 is our primary user experience metric. Every 100ms increase above 200ms p95 causes 5% drop in conversion rate.

**WHAT**: Tracks `http_request_duration_seconds` histogram as p50/p95/p99 percentiles. Shows response time distribution for [service] API. SLO target: p95 <200ms.

**HOW**: Time series with three lines. Y-axis in milliseconds. Expected baseline: p50 <50ms, p95 <150ms, p99 <300ms. Warning: p95 approaching 200ms. Critical: p95 >200ms (SLO breach).

**WHEN**:
- Green: p95 <200ms (within SLO, no action)
- Yellow: p95 200-300ms (investigate within 15 min):
  1. Check downstream service latency (database, cache, external APIs)
  2. Review CPU/memory utilization for resource constraints
  3. Check for recent deployments (correlate with latency increase)
  4. Analyze slow query logs if database-backed
- Red: p95 >300ms sustained >5 min (immediate action):
  1. Page on-call SRE immediately
  2. Enable detailed tracing for affected endpoints
  3. Check for traffic spikes (DDoS or unexpected load)
  4. Consider rollback if recent deployment
  5. Scale up resources proactively
- Owner: [Service] SRE (primary), On-Call Engineer (escalation)
```

---

## Usage Guidelines

### Customization Workflow

1. **Copy template** for panel type matching your metric
2. **Replace placeholders** with specific values for your service:
   - `[Service]` → Your service name (e.g., "API Gateway", "Payment Processor")
   - `[metric_name]` → Exact Prometheus metric (e.g., `http_request_duration_seconds`)
   - `[SLO_value]` → Your SLO threshold (e.g., "200ms", "99%")
   - `[Team Name]` → Owning team (e.g., "Platform SRE", "Payments Team")
3. **Validate completeness**: Ensure all four questions (WHY/WHAT/HOW/WHEN) are answered
4. **Add context**: Include business impact values (cost, conversion rate, support tickets)
5. **Review with team**: Confirm thresholds and action steps match operational reality

### When to Use Each Template

- **Latency Percentiles**: Services with SLOs, user-facing APIs, response time monitoring
- **Error Rates**: Reliability tracking, SLO compliance, incident detection
- **Resource Utilization**: Capacity planning, cost optimization, scaling triggers
- **Log Volume**: Anomaly detection, cost management, incident correlation
- **Cache Hit Rate**: Performance optimization, cost reduction, backend load management
- **Request Rate**: Traffic patterns, capacity planning, incident detection
- **Saturation Metrics**: Queue depth, connection pools, resource exhaustion
- **Network Traffic**: Bandwidth capacity, cost tracking, security monitoring
- **Cost Tracking**: Budget management, FinOps optimization, waste detection
- **Token Usage**: LLM cost management, prompt optimization, cache efficiency

### Integration with Dashboard Linter

These templates are designed to pass `dashboard-linter` validation:

- All PromQL queries use `$__rate_interval` (not hardcoded intervals)
- Datasources reference `${DS_PROMETHEUS}` template variable (not hardcoded UIDs)
- Panel descriptions are comprehensive (not generic placeholders)
- Thresholds are explicitly defined with actionable values

**Reference**: See `docs/04-guides/observability/grafana-dashboard-validation.md` for complete linter rules.

---

## Related Documentation

- **[SRE Patterns](sre-patterns.md)**: Framework selection (RED/USE/Four Golden Signals)
- **[API Reference](api-reference.md)**: Python script integration for automated dashboard generation
- **[Dashboard Validation](../observability/grafana-dashboard-validation.md)**: Linter rules and standards

---

**Last Updated**: 2025-11-10
**Maintainer**: python-code-implementer
**Template Version**: 1.0.0
