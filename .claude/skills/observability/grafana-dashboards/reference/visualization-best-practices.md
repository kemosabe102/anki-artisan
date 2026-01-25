# Grafana Visualization Best Practices

## Table of Contents

1. [Color Theory & Accessibility](#color-theory--accessibility)
2. [Panel Layout Principles](#panel-layout-principles)
3. [Chart Type Selection](#chart-type-selection)
4. [Panel Description Framework](#panel-description-framework)
5. [Signal-to-Noise Optimization](#signal-to-noise-optimization)
6. [SRE Dashboard Patterns](#sre-dashboard-patterns)

---

## Color Theory & Accessibility

### WCAG 2.1 AA Compliance

| Requirement | Minimum Ratio |
|-------------|---------------|
| Standard text | 4.5:1 |
| Large text (18pt+) | 3:1 |
| UI components | 3:1 |

### Color Independence Rule (CRITICAL)

**NEVER use color alone—always add 2+ visual elements:**

1. Icons: ✓ (success), ⚠️ (warning), ❌ (critical)
2. Text labels: "OK", "Warning", "Critical"
3. Shapes: Circle (normal), Triangle (caution), Square (error)
4. Borders: 1px normal, 3px warning, 5px critical

### Colorblind-Safe Palettes

#### Okabe-Ito (9-color, Universal)

```
Orange: #E69F00    Sky Blue: #56B4E9
Bluish Green: #009E73    Yellow: #F0E442
Blue: #0072B2    Vermillion: #D55E00
Reddish Purple: #CC79A7    Black: #000000
Gray: #999999
```

#### 3-Tier Thresholds (Colorblind-Safe)

```json
{
  "thresholds": {
    "steps": [
      {"color": "#009E73", "value": null},
      {"color": "#F0E442", "value": 70},
      {"color": "#D55E00", "value": 85}
    ]
  }
}
```

### 60-30-10 Color Rule

- **60% Dominant**: Neutral background (white/dark gray)
- **30% Secondary**: Primary data (Blue #0072B2, Teal #009E73)
- **10% Accent**: Alerts (Orange #E69F00, Vermillion #D55E00)

---

## Panel Layout Principles

### F-Pattern (Operational Dashboards)

```
Row 1 (y=0): Global KPIs - Highest priority
  Panel 1 (x=0, w=6):  Request Rate
  Panel 2 (x=6, w=6):  Error Rate %
  Panel 3 (x=12, w=6): Latency p95
  Panel 4 (x=18, w=6): Saturation %

Row 2 (y=6): Time Series Trends
  Panel 5 (x=0, w=12):  Rate Over Time
  Panel 6 (x=12, w=12): Error Breakdown

Row 3 (y=14): Detailed Analysis
  Panel 7 (x=0, w=24): Log Stream (full-width)
```

### Z-Pattern (Executive Dashboards)

```
Top-left (primary) ───────────> Top-right (secondary)
      \                               /
       \                             /
        v                           v
Bottom-left (trend) ─────────> Bottom-right (status)
```

### Grid Width Standards

| Width | Usage |
|-------|-------|
| w=24 | Full-width (logs, tables) |
| w=12 | Half-width (comparisons) |
| w=8 | Third-width (KPIs) |
| w=6 | Quarter-width (stats) |

### Panel Height Standards

| Type | Height |
|------|--------|
| Stat | h=6-8 |
| Timeseries | h=8-12 |
| Gauge | h=6-8 |
| Table | h=12-16 |
| Row | h=1 |

---

## Chart Type Selection

### Decision Guide

| Data Type | Chart Type | Panel |
|-----------|------------|-------|
| Categorical comparison | Bar Chart | barchart |
| Time trends | Line Chart | timeseries |
| Distribution | Histogram/Heatmap | histogram, heatmap |
| Part-to-whole | Stacked Bar | barchart (stacked) |
| Single metric (bounded) | Gauge | gauge |
| Single metric (unbounded) | Stat | stat |

### Rules

- **NEVER Pie Chart** when >3 slices
- **Max 7 series** per timeseries panel
- **Use Stat** for counts, rates (unbounded)
- **Use Gauge** for percentages, utilization (0-100)

---

## Panel Description Framework

### 4-Question Format

Every panel description answers:

1. **WHY**: Business impact
2. **WHAT**: Calculation/formula
3. **HOW**: Interpretation guide
4. **WHEN**: Action thresholds

### Template

```
[METRIC NAME] [VISUALIZATION TYPE]. [PURPOSE].
Calculated using [FORMULA].
[INTERPRETATION GUIDE].
Thresholds: Red >[X] (action), Yellow >[Y] (warn), Green <[Y] (healthy).

Business Impact: [WHY THIS MATTERS].
Action Required: [SPECIFIC ACTIONS WHEN THRESHOLDS BREACHED].
```

### Example

```
API Gateway Request Rate time series. Tracks HTTP requests/sec.
Calculated using sum(rate(http_requests_total{service="api"}[5m])).
Shows temporal trends with 5-minute rate window.
Thresholds: Red >5000 (capacity), Yellow >4000 (scale), Green <4000.

Business Impact: Traffic patterns and capacity utilization.
Action Required: Scale when sustained >4000 req/s for 15 minutes.
```

---

## Signal-to-Noise Optimization

### 12 Techniques

1. **Threshold-based color activation** - Gray until threshold breach
2. **Reference line baselines** - Subtle gray expected behavior line
3. **Grid line minimization** - Opacity 10-20%
4. **Legend placement optimization** - Bottom or hidden
5. **Annotation selectivity** - Max 5-10 per timeframe
6. **Unit formatting** - Short units with SI prefixes
7. **Whitespace as signal** - 0-1 unit gaps (related), 2 units (unrelated)
8. **Single-purpose panels** - One question per panel
9. **Color palette discipline** - Max 5 colors
10. **Dynamic range adjustment** - Auto for trends, fixed for SLO
11. **Text panel economy** - Max 2-3 per dashboard
12. **Conditional visibility** - Hide when healthy

### Color Palette (5 colors max)

```
Gray:      #999999  (normal state)
Green:     #009E73  (healthy)
Yellow:    #F0E442  (warning)
Vermillion: #D55E00  (critical)
Blue:      #0072B2  (informational)
```

---

## SRE Dashboard Patterns

### Four Golden Signals Layout

```
Row 1: KPI Overview
  Request Rate | Error Rate % | Latency p95 | Saturation %

Row 2: Temporal Correlation
  Request/Error Rate Over Time | Latency Percentiles

Row 3: Saturation Detail
  CPU % | Memory % | Queue Depth
```

### RED Method (Service-Centric)

```
Left Column: Rate & Errors
  Request Rate Trend
  Error Rate % (stat)
  Error Count by Type (bar)

Right Column: Duration
  Latency p95 (stat)
  Latency Percentiles Trend
  Latency Histogram (heatmap)
```

### USE Method (Resource-Centric)

```
Utilization: CPU %, Memory %, Disk %
Saturation: Load Average, Queue Depth
Errors: Hardware Errors, OOM Kills
```

### SLO Integration

```json
{
  "type": "gauge",
  "title": "SLO Compliance (99.9%)",
  "fieldConfig": {
    "defaults": {
      "min": 0, "max": 100,
      "thresholds": {
        "steps": [
          {"color": "#D55E00", "value": 0},
          {"color": "#F0E442", "value": 90},
          {"color": "#009E73", "value": 99.9}
        ]
      }
    }
  }
}
```

---

## Sources

- Grafana Dashboard Best Practices
- WCAG 2.1 Guidelines
- Google SRE Book - Monitoring Distributed Systems
- Edward Tufte: The Visual Display of Quantitative Information
