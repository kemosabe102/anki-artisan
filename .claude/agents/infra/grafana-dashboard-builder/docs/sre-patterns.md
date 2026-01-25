# SRE Best Practices for Grafana Dashboards

**Purpose**: Reference guide for SRE monitoring patterns and signal-to-noise optimization

## Four Golden Signals (Google SRE)

**Latency**: 50th/95th/99th percentile time series, thresholds at SLO boundaries
**Traffic**: Request rate (req/s) with sum aggregation across instances
**Errors**: Error rate percentage with alert threshold markers
**Saturation**: Resource utilization gauges with capacity limits

## RED Method (Services)

**Rate**: Requests per second, group by endpoint or service
**Errors**: Error percentage with 5xx filter, compare to SLO
**Duration**: Response time percentiles, highlight SLO breaches

## USE Method (Resources)

**Utilization**: CPU/Memory/Disk percentage, gauge visualization
**Saturation**: Queue depth, connection pool usage, wait times
**Errors**: Resource-specific errors (OOM, disk full, network drops)

## Signal vs Noise Optimization

### Rate Interval Selection

- **Short intervals (1m)**: Tactical, real-time monitoring, high sensitivity
- **Medium intervals (5m)**: Balanced, default for most dashboards, noise reduction
- **Long intervals (1h)**: Strategic, trend analysis, smooth curves

### Smoothing Techniques

- Moving averages: `avg_over_time(metric[5m])` for noisy metrics
- Percentiles: Filter outliers, focus on typical behavior (p50/p95)
- Label filtering: Remove low-signal labels (exclude jobs, include services)

### Aggregation Strategy

- **High cardinality** (>100 series): Apply `topk(10, ...)` or summarize by fewer labels
- **Low cardinality** (<10 series): Full breakdown, detailed visualization
- **Alert-worthy signals**: Separate panel with clear thresholds

## Panel Type Decision Tree

### Time Series (default for most metrics)
- Use for: Trends over time, rate/counter metrics, histograms
- Configuration: Line graph, fill opacity 10%, gradient mode "opacity"
- Thresholds: Green (<100ms), yellow (100-500ms), red (>500ms) for latency

### Stat (single value)
- Use for: Current state, latest value, instant queries
- Configuration: Sparkline enabled for trend context
- Color by: Threshold or value (semantic coloring)

### Gauge (percentage/ratio)
- Use for: Utilization (0-100%), saturation metrics
- Configuration: Show min/max, threshold markers
- Thresholds: Green (0-70%), yellow (70-85%), red (>85%)

### Bar Chart (distribution)
- Use for: Comparing across labels, top-N analysis
- Configuration: Horizontal orientation for readability
- Sort: Descending by value (most significant first)

### Heatmap (density visualization)
- Use for: Histogram buckets, latency distribution over time
- Configuration: Color scheme "Spectral", opacity "0.7"
- Bucket size: Auto or explicit (e.g., 50ms buckets)

## Intent-to-Framework Mapping

| Intent Keywords | Framework | Signals |
|----------------|-----------|---------|
| "latency", "response time", "duration" | RED (Duration) | Histogram percentiles (p50/p95/p99) |
| "errors", "failures", "5xx" | RED (Errors) | Error rate percentage |
| "traffic", "requests", "throughput" | RED (Rate) | Requests per second |
| "CPU", "memory", "disk" | USE (Utilization) | Resource percentage |
| "queue", "pool", "wait" | USE (Saturation) | Queue depth, wait time |
| "OOM", "disk full", "network drop" | USE (Errors) | Resource-specific errors |
| "availability", "uptime", "SLO" | Golden Signals (All) | Composite dashboard |

## Framework Templates

### RED Method Template (for services)
- Panel 1: Request rate (time series)
- Panel 2: Error rate percentage (time series with threshold)
- Panel 3: Latency percentiles (time series, p50/p95/p99)

### USE Method Template (for resources)
- Panel 1: Utilization percentage (gauge)
- Panel 2: Saturation (time series, queue depth)
- Panel 3: Error count (stat with sparkline)

### Four Golden Signals Template (comprehensive)
- Row 1: Latency (percentiles) + Traffic (rate)
- Row 2: Errors (percentage) + Saturation (utilization)
