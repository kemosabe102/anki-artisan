---
name: grafana-dashboards
description: >
  Use this skill when creating Grafana dashboards, designing panel layouts,
  selecting visualization types, or applying SRE patterns. Covers RED/USE/Golden
  Signals frameworks, panel types, ConfigMap generation, and accessibility.
  Keywords: grafana, dashboard, panel, RED, USE, golden signals, visualization.
---

# Grafana Dashboard Construction

Build production-ready Grafana dashboards using SRE best practices, WCAG 2.1 AA accessibility, and signal-focused visualization design.

## Reference Documentation

**Detailed Guides** (read when relevant):
- **SRE Patterns** → [reference/sre-patterns.md](reference/sre-patterns.md)
- **Visualization Best Practices** → [reference/visualization-best-practices.md](reference/visualization-best-practices.md)
- **Dashboard JSON Schema** → [reference/dashboard-json-schema.md](reference/dashboard-json-schema.md)

## Scripts

**Validation Tools**:
- **Validate Dashboard** → `python scripts/validate_dashboard.py dashboard.json`
- **Generate ConfigMap** → `python scripts/generate_configmap.py dashboard.json`

---

## SRE Framework Selection

Map user intent keywords to the appropriate SRE framework:

| Intent Keywords | Framework | Primary Signals |
|-----------------|-----------|-----------------|
| "latency", "response time", "duration", "slow" | RED (Duration) | Histogram percentiles (p50/p95/p99) |
| "errors", "failures", "5xx", "exceptions" | RED (Errors) | Error rate percentage |
| "traffic", "requests", "throughput", "load" | RED (Rate) | Requests per second |
| "CPU", "memory", "disk", "network" | USE (Utilization) | Resource percentage (0-100%) |
| "queue", "pool", "connections", "wait" | USE (Saturation) | Queue depth, wait time |
| "OOM", "disk full", "network drops" | USE (Errors) | Resource-specific errors |
| "availability", "uptime", "SLO", "SLA" | Four Golden Signals | Composite (all signals) |

**Selection Rule**: If keywords span multiple frameworks, use Four Golden Signals for comprehensive coverage.

---

## RED Method (Services)

**Use for**: APIs, microservices, web applications

### Panel Configuration

**Rate** (requests per second):
- Panel type: Time series
- Query pattern: `sum(rate(http_requests_total{service="$service"}[$__rate_interval]))`
- Group by: endpoint, status code, or method

**Errors** (error percentage):
- Panel type: Stat with sparkline
- Query pattern: `sum(rate(http_requests_total{status=~"5.."}[$__rate_interval])) / sum(rate(http_requests_total[$__rate_interval])) * 100`
- Threshold: Red > SLO error budget

**Duration** (latency percentiles):
- Panel type: Time series (3 lines: p50, p95, p99)
- Query pattern: `histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[$__rate_interval]))`
- Threshold: Red > SLO latency target

### RED Layout Template

```
Row 1 (y=0, h=6): KPI Summary
  Panel 1 (x=0, w=8):  Request Rate (stat)
  Panel 2 (x=8, w=8):  Error Rate % (stat)
  Panel 3 (x=16, w=8): Latency p95 (stat)

Row 2 (y=6, h=10): Trends
  Panel 4 (x=0, w=12):  Rate + Errors Over Time
  Panel 5 (x=12, w=12): Latency Percentiles
```

---

## USE Method (Resources)

**Use for**: Servers, containers, databases, network infrastructure

### Panel Configuration

**Utilization** (resource percentage):
- Panel type: Gauge (0-100% scale)
- Query pattern: `(resource_used / resource_total) * 100`
- Thresholds: Green <70%, Yellow 70-85%, Red >85%

**Saturation** (queue/wait metrics):
- Panel type: Time series
- Query pattern: `queue_depth` or `connection_pool_active / connection_pool_max * 100`
- Warning: Sustained >80%

**Errors** (resource failures):
- Panel type: Stat with sparkline
- Query pattern: `sum(rate(resource_errors_total[$__rate_interval]))`
- Any non-zero value requires investigation

### USE Layout Template

```
Row 1 (y=0, h=8): Utilization Gauges
  Panel 1 (x=0, w=8):  CPU % (gauge)
  Panel 2 (x=8, w=8):  Memory % (gauge)
  Panel 3 (x=16, w=8): Disk % (gauge)

Row 2 (y=8, h=8): Saturation
  Panel 4 (x=0, w=12):  Queue Depth (time series)
  Panel 5 (x=12, w=12): Connection Pool (time series)

Row 3 (y=16, h=6): Errors
  Panel 6 (x=0, w=24):  Resource Errors (stat)
```

---

## Four Golden Signals Template

**Use for**: Comprehensive service health, SLO dashboards

### Layout Structure

```
Row 1 (y=0, h=6): Golden Signals KPIs
  Panel 1 (x=0, w=6):  Request Rate (stat)
  Panel 2 (x=6, w=6):  Error Rate % (stat)
  Panel 3 (x=12, w=6): Latency p95 (stat)
  Panel 4 (x=18, w=6): Saturation % (gauge)

Row 2 (y=6, h=8): Temporal Correlation
  Panel 5 (x=0, w=12):  Rate + Errors Over Time
  Panel 6 (x=12, w=12): Latency Percentiles

Row 3 (y=14, h=8): Saturation Detail
  Panel 7 (x=0, w=8):  CPU %
  Panel 8 (x=8, w=8):  Memory %
  Panel 9 (x=16, w=8): Queue Depth
```

**Critical**: Display ALL signals on ONE PAGE for temporal correlation during incident response.

---

## Panel Type Decision Tree

| Data Type | Panel Type | Configuration |
|-----------|------------|---------------|
| Single current value (unbounded) | Stat | sparkline enabled, threshold colors |
| Single value (0-100%) | Gauge | show min/max, threshold markers |
| Trend over time | Time series | max 7 series, table legend |
| Category comparison | Bar chart | horizontal if >6 categories |
| Distribution | Histogram/Heatmap | log2 bucket sizing for heatmap |
| Part-to-whole | Stacked bar or Table | NEVER pie chart if >3 slices |

### Anti-Pattern

**NEVER** use pie charts with >3 slices. Human angle perception is inaccurate beyond 3 segments.

---

## Layout Patterns

### F-Pattern (Operational Dashboards)

Users scan in F-shape: horizontal across top, vertical down left, horizontal across middle.

**Placement Rules**:
- Row 1 (y=0): Global KPIs - highest priority metrics
- Primary content: Always start at x=0 (left edge)
- Critical metrics: Place in top row for immediate visibility

### Z-Pattern (Executive Dashboards)

Sparse layouts with 4-6 panels maximum for high-level overview.

**Characteristics**:
- 2 rows x 2 columns for balanced composition
- Large stat panels (w=12, h=10)
- Single-value focus per panel

### Panel Grouping

- **0-1 unit gap**: Related panels (same metric family)
- **2 unit gap**: Unrelated groups (different domains)
- **Consistent heights**: Panels within group should match

---

## ConfigMap Template

Generate Kubernetes ConfigMap for Grafana sidecar provisioning:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: grafana-dashboard-<name>
  namespace: observability
  labels:
    grafana_dashboard: '1'
data:
  <name>.json: |
    {
      "dashboard": { ... },
      "folderId": null,
      "overwrite": true
    }
```

**Critical Label**: `grafana_dashboard: "1"` enables sidecar auto-detection.

---

## Panel Description Framework (WHY/WHAT/HOW/WHEN)

Every panel description must answer:

1. **WHY** (Business Impact): Why does this metric matter?
2. **WHAT** (Calculation): What formula/query produces this value?
3. **HOW** (Interpretation): How to read the visualization?
4. **WHEN** (Action Threshold): When to act and what action?

### Example

```
**WHY**: Response latency >500ms causes 20% cart abandonment.

**WHAT**: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

**HOW**: Time series with p50/p95/p99 lines. Lower is better. Expected: p95 <200ms.

**WHEN**: Green <200ms | Yellow 200-500ms (investigate) | Red >500ms (page on-call)
Owner: Platform SRE
```

---

## Accessibility Standards (WCAG 2.1 AA)

### Contrast Requirements

- Text contrast: 4.5:1 minimum
- UI components: 3:1 against adjacent colors

### Color Independence (CRITICAL)

**NEVER use color alone**. Always add 2+ visual elements:
- Icons: check, warning triangle, X
- Text labels: "OK", "Warning", "Critical"
- Shapes: circle (normal), triangle (caution), square (error)
- Border thickness: 1px normal, 3px warning, 5px critical

### Colorblind-Safe Palette (Okabe-Ito)

| Purpose | Color | Hex |
|---------|-------|-----|
| Normal/Info | Blue | #0072B2 |
| Success | Bluish Green | #009E73 |
| Warning | Yellow | #F0E442 |
| Critical | Vermillion | #D55E00 |
| Secondary | Sky Blue | #56B4E9 |

**Coverage**: Protanopia, deuteranopia, tritanopia, achromatopsia

---

## Quality Standards

- **Schema**: Grafana 12.x (schemaVersion 38+)
- **Panel IDs**: Unique, auto-increment from 1
- **Queries**: All PromQL validated via `$__rate_interval`
- **Datasource**: Reference `${DS_PROMETHEUS}` (not hardcoded UIDs)
- **Series limit**: Max 7 per timeseries panel

---

## Anti-Patterns

| Pattern | Problem | Solution |
|---------|---------|----------|
| Pie chart >3 slices | Human angle perception inaccurate | Use bar chart or table |
| Color-only indicators | 8% of males colorblind | Add icons + text + shapes |
| >7 series per panel | Visual clutter | Split into multiple panels |
| Generic descriptions | No actionable context | Use WHY/WHAT/HOW/WHEN |
| Hardcoded datasource UID | Breaks portability | Use `${DS_PROMETHEUS}` |
| Dashboard sprawl | Update propagation failures | Use template variables |

---

## Validation Checklist

Before finalizing any dashboard:

- [ ] All panels have descriptions (WHY/WHAT/HOW/WHEN)
- [ ] Thresholds tied to SLO targets
- [ ] Colorblind-safe palette used
- [ ] Color NEVER sole indicator
- [ ] Max 7 series per timeseries panel
- [ ] ConfigMap has `grafana_dashboard: "1"` label
- [ ] All queries use `$__rate_interval`
- [ ] Font size >= 14px for operational dashboards
