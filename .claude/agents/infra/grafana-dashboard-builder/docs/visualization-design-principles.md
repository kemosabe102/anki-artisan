# Grafana Visualization Design Principles

**Purpose**: Comprehensive guide for creating readable, accessible, and signal-focused Grafana dashboards following SRE best practices, WCAG 2.1 AA standards, and data visualization theory.

**Target Audience**: Dashboard builders, SRE teams, platform engineers, observability specialists

**Last Updated**: 2025-11-10

---

## 1. Color Theory & Accessibility (WCAG 2.1 AA Compliance)

### Contrast Requirements

**WCAG 2.1 AA Standards**:
- **Text contrast**: 4.5:1 minimum for standard text, 3:1 for large text (18pt+/14pt bold)
- **UI components**: 3:1 against adjacent colors (buttons, borders, form controls)
- **Testing approach**: Check weakest contrast areas on gradients and overlays
- **Grafana tools**: Built-in color picker contrast checker, validate with [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)

**Implementation Example**:
```json
{
  "fieldConfig": {
    "defaults": {
      "color": {"mode": "thresholds"},
      "custom": {
        "lineWidth": 2
      }
    }
  }
}
```

### Color Independence (CRITICAL RULE)

**NEVER use color alone—always add 2+ visual elements**:

1. **Icons**: ✓ (success), ⚠️ (warning), ❌ (critical), ℹ️ (info) - Use Unicode or SVG
2. **Text labels**: "OK", "Warning", "Critical", "Unknown" alongside color indicators
3. **Shapes**: Circle (normal), Triangle (caution), Square (error), Diamond (degraded)
4. **Patterns**: Solid, stripes, dots, cross-hatch (available via SVG patterns in Grafana themes)
5. **Borders**: Thickness variation (1px normal, 3px warning, 5px critical)
6. **Animation**: Pulse effect for critical states (use sparingly to avoid distraction)

**Why This Matters**: 8% of males and 0.5% of females have some form of color vision deficiency. Color-only indicators exclude these users entirely.

### Colorblind-Safe Palettes (5 Options)

#### Palette 1: Okabe-Ito (9-color, Universal Coverage)

**Use for**: Categorical data, multi-series charts (up to 9 categories)

**Colors**:
- Orange: `#E69F00`
- Sky Blue: `#56B4E9`
- Bluish Green: `#009E73`
- Yellow: `#F0E442`
- Blue: `#0072B2`
- Vermillion: `#D55E00`
- Reddish Purple: `#CC79A7`
- Black: `#000000`
- Gray: `#999999`

**Coverage**: Protanopia, deuteranopia, tritanopia, achromatopsia

**Grafana Implementation**:
```json
{
  "fieldConfig": {
    "overrides": [
      {
        "matcher": {"id": "byName", "options": "Series 1"},
        "properties": [
          {"id": "color", "value": {"fixedColor": "#E69F00", "mode": "fixed"}}
        ]
      },
      {
        "matcher": {"id": "byName", "options": "Series 2"},
        "properties": [
          {"id": "color", "value": {"fixedColor": "#56B4E9", "mode": "fixed"}}
        ]
      }
    ]
  }
}
```

#### Palette 2: IBM Carbon (5-color, High-Contrast)

**Use for**: Sequential data, maximum 5 categories

**Colors**:
- Blue: `#648FFF`
- Purple: `#785EF0`
- Magenta: `#DC267F`
- Orange: `#FE6100`
- Gold: `#FFB000`

**Grafana Implementation**: Apply as ordered sequence in field overrides

#### Palette 3: Blue-Orange Foundation (Binary States)

**Use for**: Two-metric comparisons, before/after, healthy/unhealthy states

**Colors**:
- Primary Blue: `#0072B2`
- Primary Orange: `#E69F00`
- Light Blue: `#56B4E9`
- Vermillion: `#D55E00`

**Coverage**: Universal (all colorblindness types including achromatopsia)

**Example Use Case**: Network traffic (blue = inbound, orange = outbound)

#### Palette 4: Monochromatic (Accessibility First)

**Use for**: Single-metric gradients, heatmaps, sequential scales

**Strategy**: Single hue, vary lightness/saturation
- Near-black → Dark Teal → Medium Teal → Light Teal → Near-white

**Coverage**: Including total colorblindness (achromatopsia)

**Required Supplement**: Patterns or text labels for categorical data

#### Palette 5: Viridis/Magma (Sequential, Perceptually Uniform)

**Use for**: Heatmaps, continuous scales, density visualization

**Colors**:
- **Viridis**: Dark purple → Teal → Green → Yellow
- **Magma**: Black → Dark purple → Magenta → Orange → Yellow

**Coverage**: Protanopia, deuteranopia

**Grafana**: Available in standard "Continuous color schemes" dropdown

### Semantic Color Usage (Traffic Light Conventions)

#### Traditional Traffic Light (AVOID for accessibility)

❌ **Problems**:
- Red: Critical, overdue, over-budget, requires action
- Yellow/Amber: Warning, approaching threshold, increasing risk
- Green: Success, on-track, within budget
- **Issue**: Red-green combination is invisible to ~8% of males (deuteranopia/protanopia)

#### Accessible Alternatives

✅ **Option 1: Warm-Cold Scheme**
- Orange/Red (negative states) vs Blue/Cyan (positive states)
- Universally distinguishable across all color vision types

✅ **Option 2: Sequential Severity**
- Light blue → Yellow → Dark orange → Red (increasing urgency)
- Uses hue + lightness changes for redundancy

✅ **Option 3: Shape Coding**
- Circle with solid fill (OK)
- Triangle with border (Warning)
- Square with thick border (Critical)

✅ **Option 4: Pattern Overlay**
- Solid fill (OK)
- Diagonal stripes (Warning)
- Cross-hatch pattern (Critical)

#### Grafana Threshold Implementation with Accessibility

```json
{
  "type": "timeseries",
  "fieldConfig": {
    "defaults": {
      "thresholds": {
        "mode": "absolute",
        "steps": [
          {"color": "#009E73", "value": null},    // Bluish-green (not pure green)
          {"color": "#F0E442", "value": 70},      // Yellow + ⚠️ icon
          {"color": "#D55E00", "value": 85}       // Vermillion (not pure red) + ❌ icon
        ]
      }
    },
    "overrides": [
      {
        "matcher": {"id": "byValue", "options": {"reducer": "last", "op": "gt", "value": 85}},
        "properties": [
          {"id": "custom.drawStyle", "value": "line"},
          {"id": "custom.lineWidth", "value": 3},  // Thicker border for critical
          {"id": "mappings", "value": [
            {"type": "value", "options": {"85": {"text": "Critical ❌", "color": "#D55E00"}}}
          ]}
        ]
      }
    ]
  }
}
```

### Typography Standards

**Font Sizing**:
- **Minimum**: 14px for operational monitoring dashboards
- **Executive dashboards**: 16px+ for readability at a distance
- **Large displays**: 18-24px for wall-mounted monitors

**Font Family**:
- **Primary**: Lato (high readability at small sizes)
- **Fallback**: System sans-serif (Inter, Roboto, -apple-system)

**Line Height**:
- **Body text**: 1.4-1.65 (comfortable reading)
- **Headings**: 1.0-1.3 (tighter spacing for impact)
- **Captions**: 1.3 (data labels, legend text)

**Font Weight**:
- **Regular (400)**: Default for all text
- **Bold (600-700)**: Use sparingly for emphasis only
- **Maintain 4.5:1 minimum contrast** with background across all weights

**Grafana Configuration**:
```json
{
  "dashboard": {
    "style": {
      "fontSize": "14px",
      "fontFamily": "Lato, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    }
  }
}
```

### 60-30-10 Color Rule

**Proportional Color Distribution**:
- **60% Dominant**: Neutral background
  - Light theme: White or light gray (#F5F5F5)
  - Dark theme: Dark gray (#1E1E1E, #2D2D2D)
- **30% Secondary**: Primary data color
  - Normal states: Blue (#0072B2) or Teal (#009E73)
  - Trends, lines, non-alerting data
- **10% Accent**: Alert and highlight colors
  - Orange (#E69F00) for warnings
  - Vermillion (#D55E00) for critical states

**Application Strategy**: Reserve vibrant colors for alerts—this creates immediate visual hierarchy where problems stand out.

---

## 2. Panel Layout Principles

### F-Pattern Reading (Operational Dashboards)

**Eye-Tracking Research**: Users scan in F-shaped pattern:
1. Horizontal movement across top (primary KPIs)
2. Vertical movement down left side (scanning for relevance)
3. Horizontal movement across middle (secondary metrics)

**Grafana 24-Column Grid Layout**:

```
Row 1 (y=0, h=6): Global KPIs - Highest priority metrics
  Panel 1 (x=0, w=6):  Request Rate (Stat)
  Panel 2 (x=6, w=6):  Error Rate % (Stat with threshold)
  Panel 3 (x=12, w=6): Latency p95 (Stat with sparkline)
  Panel 4 (x=18, w=6): Saturation % (Gauge)

Row 2 (y=6, h=8): Time Series Trends - Temporal analysis
  Panel 5 (x=0, w=12):  Request Rate Over Time
  Panel 6 (x=12, w=12): Error Rate Breakdown

Row 3 (y=14, h=12): Detailed Analysis - Drill-down data
  Panel 7 (x=0, w=24): Log Stream (full-width, scrollable)
  Panel 8 (x=0, w=12): Error Details Table
  Panel 9 (x=12, w=12): Latency Histogram
```

**Layout Rules**:
- **Primary content**: Always start at x=0 (left edge)
- **Critical metrics**: Place in top row (y=0) for immediate visibility
- **Stat panels**: 1 row height (h=6-8) for compact KPIs
- **Time series**: 2-3 row height (h=8-12) for trend visibility
- **Tables/logs**: Bottom placement (h=12-16) with scrollability

### Z-Pattern Scanning (Executive Dashboards)

**Use for**: Sparse layouts with 4-6 panels maximum, high-level overview

**Visual Flow**:
```
Top-left (primary KPI) -----------------> Top-right (secondary KPI)
      \                                           /
       \                                         /
        \                                       /
         \                                     /
          v                                   v
Bottom-left (supporting trend) -----> Bottom-right (status)
```

**Grafana Implementation**:
```json
{
  "panels": [
    {"id": 1, "title": "Total Revenue", "gridPos": {"x": 0, "y": 0, "w": 12, "h": 10}},
    {"id": 2, "title": "Active Users", "gridPos": {"x": 12, "y": 0, "w": 12, "h": 10}},
    {"id": 3, "title": "Growth Trend", "gridPos": {"x": 0, "y": 10, "w": 12, "h": 10}},
    {"id": 4, "title": "System Health", "gridPos": {"x": 12, "y": 10, "w": 12, "h": 10}}
  ]
}
```

**Characteristics**:
- **2 rows × 2 columns** for balanced composition
- **Large stat panels** (w=12, h=10) for visibility
- **Minimal text**, font size 48px+ for at-a-glance reading
- **Single-value focus** per panel (no multi-series complexity)

### Cognitive Load Reduction via Grouping

#### Panel Grouping Strategies

**1. Proximity Grouping**:
- **0-1 unit gap**: Between related panels (same metric family)
- **2 unit gap**: Between unrelated groups (different metric domains)

**2. Row Collapsing**:
```json
{
  "type": "row",
  "title": "API Performance Metrics",
  "collapsed": true,
  "panels": [
    {"id": 1, "title": "Request Rate", "gridPos": {"x": 0, "y": 1, "w": 8, "h": 8}},
    {"id": 2, "title": "Error Rate", "gridPos": {"x": 8, "y": 1, "w": 8, "h": 8}},
    {"id": 3, "title": "Latency p95", "gridPos": {"x": 16, "y": 1, "w": 8, "h": 8}}
  ]
}
```

**3. Consistent Heights**:
- Panels within a group should have the same height for visual harmony
- Creates predictable scanning pattern

**4. Visual Separators**:
- Use row titles with descriptive names (not "Metrics 1", "Metrics 2")
- Avoid blank panels as separators (wastes space)

#### Example: API Performance Group

```json
{
  "type": "row",
  "title": "🚀 API Performance (Service: api-gateway)",
  "collapsed": false,
  "panels": [
    {
      "id": 1,
      "title": "Request Rate",
      "type": "stat",
      "gridPos": {"x": 0, "y": 1, "w": 8, "h": 8},
      "description": "Total HTTP requests per second across all endpoints."
    },
    {
      "id": 2,
      "title": "Error Rate %",
      "type": "stat",
      "gridPos": {"x": 8, "y": 1, "w": 8, "h": 8},
      "description": "Percentage of requests returning 5xx status codes."
    },
    {
      "id": 3,
      "title": "Latency p95",
      "type": "stat",
      "gridPos": {"x": 16, "y": 1, "w": 8, "h": 8},
      "description": "95th percentile response time—worst case for 95% of users."
    }
  ]
}
```

### Progressive Disclosure (Summary → Detail)

**Pattern**: High-level overview panels with drill-down links to detailed dashboards

**Benefits**:
- Reduces cognitive overload on main dashboard
- Provides context-appropriate detail level
- Enables efficient troubleshooting workflow

**Grafana Implementation**:
```json
{
  "type": "stat",
  "title": "Error Rate: 5.2%",
  "fieldConfig": {
    "defaults": {
      "thresholds": {
        "steps": [
          {"color": "green", "value": 0},
          {"color": "yellow", "value": 2},
          {"color": "red", "value": 5}
        ]
      }
    }
  },
  "links": [
    {
      "title": "🔍 View Error Details",
      "url": "/d/error-analysis?var-time=$__from&var-service=${service:csv}&var-endpoint=${endpoint}",
      "targetBlank": false
    }
  ],
  "description": "Click to view detailed error breakdown by endpoint, status code, and user impact."
}
```

**Dashboard Hierarchy Example**:
```
📊 Global Overview Dashboard (executive view)
  ├─> 🔧 Service Health Dashboard (per-service operational view)
  │     ├─> 🚨 Error Analysis Dashboard (drill-down)
  │     ├─> ⏱️ Latency Analysis Dashboard (drill-down)
  │     └─> 📝 Logs Dashboard (drill-down)
  ├─> 💻 Infrastructure Dashboard (resource utilization)
  │     ├─> CPU Deep Dive
  │     ├─> Memory Analysis
  │     └─> Network Traffic
  └─> 💰 Cost Analysis Dashboard (business metrics)
```

---

## 3. Chart Type Selection Decision Tree

### Decision Framework (6 Categories)

#### Category 1: Comparison (Categorical Data)

**When to use**: Comparing discrete categories (services, regions, error types, endpoints)

**Chart type**: Bar Chart
- **Horizontal orientation**: >6 categories (provides better label space)
- **Vertical orientation**: ≤6 categories with short labels

**Grafana panel**: `barchart`

**Configuration**:
```json
{
  "type": "barchart",
  "options": {
    "orientation": "horizontal",
    "showValue": "auto",
    "barWidth": 0.8
  }
}
```

**Avoid**: Time series panel (no temporal axis needed for categorical comparisons)

#### Category 2: Trend (Time Series Data)

**When to use**: Showing change over time, continuous temporal data

**Chart type**: Line Chart (Time Series panel)

**Best practices**:
- **Max 7 series** before visual clutter (use table legend with filtering)
- **Stacking**: Use for cumulative metrics (CPU cores, network bytes), avoid for comparing independent metrics
- **Line interpolation**: "linear" for accurate data representation, "smooth" for high-level trends

**Grafana configuration**:
```json
{
  "type": "timeseries",
  "options": {
    "tooltip": {"mode": "multi"},
    "legend": {"displayMode": "table", "placement": "bottom", "calcs": ["last", "mean", "max"]}
  },
  "fieldConfig": {
    "defaults": {
      "custom": {
        "lineInterpolation": "linear",
        "fillOpacity": 10,
        "drawStyle": "line",
        "showPoints": "auto"
      }
    }
  }
}
```

**Avoid**: Bar charts for continuous time data (creates chunking artifacts)

#### Category 3: Distribution (Statistical Analysis)

**Histogram**: Frequency distribution (latency buckets, request size distribution)
- Use for: Understanding data spread and identifying outliers
- Grafana: `histogram` panel

**Heatmap**: 2D density over time (latency percentiles × time)
- Use for: Visualizing patterns in high-cardinality data
- Grafana: `heatmap` panel with log2 bucket sizing

**Configuration Example**:
```json
{
  "type": "histogram",
  "options": {
    "bucketSize": 10
  },
  "fieldConfig": {
    "defaults": {
      "unit": "ms"
    }
  }
}
```

**Avoid**: Single point-in-time visualizations (use Stat panel instead)

#### Category 4: Composition (Part-to-Whole)

**When to use**: Component breakdown (disk usage by directory, traffic by endpoint, error distribution)

**Chart type**: Stacked Bar or Table

**NEVER use Pie Chart** when >3 slices:
- Human angle perception is inaccurate beyond 3 segments
- Difficult to compare similar-sized slices
- Labels overlap and clutter

**Grafana implementation**:
```json
{
  "type": "barchart",
  "options": {
    "orientation": "vertical",
    "stacking": "normal"
  }
}
```

**Alternative - Table with percentage**:
```json
{
  "type": "table",
  "fieldConfig": {
    "overrides": [
      {
        "matcher": {"id": "byName", "options": "Percentage"},
        "properties": [
          {"id": "custom.displayMode", "value": "gradient-gauge"},
          {"id": "unit", "value": "percent"}
        ]
      }
    ]
  }
}
```

#### Category 5: Correlation (Relationship Between Metrics)

**Rarely used**: Scatter plots have limited value in operational dashboards

**Better alternative**: Parallel Time Series panels with aligned X-axes
- Visual correlation through overlapping trends
- More intuitive for operational use cases

**Example**:
```json
{
  "type": "timeseries",
  "options": {
    "tooltip": {"mode": "multi"},
    "legend": {"displayMode": "list"}
  },
  "targets": [
    {"expr": "cpu_usage", "legendFormat": "CPU %"},
    {"expr": "request_rate", "legendFormat": "Requests/s"}
  ]
}
```

**Avoid**: Complex scatter plots in operational dashboards (analysis belongs in exploratory tools like Jupyter)

#### Category 6: Single Metric Monitoring

**Stat Panel**: Current value with optional sparkline
- **Size**: Compact (6w × 6h typical)
- **Use for**: Counts, rates, error percentages, any metric with unlimited range
- **Sparkline**: Shows 24-hour trend underneath value

**Gauge Panel**: Visual percentage/capacity indicator
- **Size**: Larger footprint (8w × 8h typical)
- **Use for**: Utilization (CPU, memory, disk), capacity (queue depth 0-100), SLO compliance (0-100%)
- **Requires**: Meaningful min/max range

**Decision criteria**:
- **Has natural min/max** (0-100%, 0-capacity) → Gauge
- **Unbounded range** (latency, counts, rates) → Stat

**Configuration Examples**:

```json
// Stat Panel
{
  "type": "stat",
  "options": {
    "graphMode": "area",
    "colorMode": "value",
    "textMode": "value_and_name"
  },
  "fieldConfig": {
    "defaults": {
      "unit": "reqps",
      "decimals": 1
    }
  }
}

// Gauge Panel
{
  "type": "gauge",
  "options": {
    "showThresholdLabels": true,
    "showThresholdMarkers": true
  },
  "fieldConfig": {
    "defaults": {
      "min": 0,
      "max": 100,
      "unit": "percent"
    }
  }
}
```

### Panel Type Configuration Best Practices

#### Time Series Panel

```json
{
  "type": "timeseries",
  "options": {
    "tooltip": {"mode": "multi"},
    "legend": {
      "displayMode": "table",
      "placement": "bottom",
      "calcs": ["last", "mean", "max"]
    }
  },
  "fieldConfig": {
    "defaults": {
      "custom": {
        "lineInterpolation": "smooth",    // "linear" for accuracy, "smooth" for trends
        "fillOpacity": 10,                // 10 for overlapping lines, 50 for stacked
        "drawStyle": "line",              // "line" for continuous, "bars" for events
        "showPoints": "auto",             // Hides at high density, shows when zoomed
        "pointSize": 4
      },
      "color": {"mode": "palette-classic"}
    }
  }
}
```

#### Stat Panel

```json
{
  "type": "stat",
  "options": {
    "graphMode": "area",          // Shows sparkline underneath value
    "colorMode": "value",         // Colors the number ("background" for full panel)
    "orientation": "auto",        // Auto-switches based on panel size
    "textMode": "value_and_name"  // Shows both value and field name
  },
  "fieldConfig": {
    "defaults": {
      "unit": "short",            // Use appropriate unit (reqps, ms, bytes, percent)
      "decimals": 1,              // 0 for counts, 1-2 for rates, 3+ for percentages
      "thresholds": {
        "mode": "absolute",
        "steps": [
          {"color": "green", "value": null},
          {"color": "yellow", "value": 70},
          {"color": "red", "value": 90}
        ]
      }
    }
  }
}
```

#### Gauge Panel

```json
{
  "type": "gauge",
  "options": {
    "orientation": "auto",
    "showThresholdLabels": true,
    "showThresholdMarkers": true
  },
  "fieldConfig": {
    "defaults": {
      "min": 0,
      "max": 100,                 // Always define max for gauge
      "unit": "percent",
      "thresholds": {
        "mode": "absolute",
        "steps": [
          {"color": "green", "value": 0},
          {"color": "yellow", "value": 70},
          {"color": "red", "value": 85}
        ]
      }
    }
  }
}
```

---

## 4. Effective Panel Descriptions (4-Question Framework)

Every panel description should answer:

1. **WHY** (Business Impact): Why does this metric matter to the business or operations?
2. **WHAT** (Calculation): What is being measured and how is it calculated?
3. **HOW** (Interpretation): How should I read and interpret this visualization?
4. **WHEN** (Action Threshold): When should I take action, and what action?

### Template Examples by Panel Type

#### Latency Percentiles (Time Series)

```
[Service Name] latency percentiles tracking response time distribution.
Calculated using histogram_quantile([p50/p95/p99], rate([metric_name][$__rate_interval])).
p95 represents worst-case for 95% of requests—this is what most users experience.
Thresholds: Red >[SLO+50%] (user-impacting), Yellow >[SLO+20%] (degrading), Green <=[SLO] (healthy).

Business Impact: Directly affects user-perceived performance and customer satisfaction.
Action Required: Investigate when p95 exceeds [X]ms for more than [Y] minutes. Check for database slow queries, external API delays, or resource saturation.
```

#### Error Rates (Stat Panel)

```
[Service Name] error rate percentage calculated as (failed requests / total requests) × 100.
Formula: sum(rate([errors_metric][$__rate_interval])) / sum(rate([requests_metric][$__rate_interval])) × 100.
Displays current error rate with 24-hour trend sparkline underneath value.
Thresholds: Red >[SLO error budget] (alert), Yellow >[50% error budget] (warn), Green <[50% error budget] (healthy).

Business Impact: Service reliability and SLA compliance. High error rates lead to customer churn and revenue loss.
Action Required: Alert on-call engineer when exceeding [X]% for [Y] minutes. Check recent deployments, database health, external dependencies.
```

#### Resource Utilization (Gauge)

```
[Resource Type] utilization percentage showing current usage vs total capacity.
Formula: ([used_resource] / [total_capacity]) × 100. Updates every [scrape_interval] seconds.
Gauge visualization provides at-a-glance capacity assessment with color-coded thresholds.
Thresholds: Red >90% (near capacity, scaling urgent), Yellow >70% (plan scaling), Green <70% (healthy).

Business Impact: System capacity planning and performance headroom. High utilization leads to latency spikes and potential outages.
Action Required: Scale horizontally when sustained >70% for [X] minutes. Review resource allocation and consider vertical scaling if pattern persists.
```

#### Log Volume (Bar Chart)

```
Log volume breakdown by severity level (ERROR, WARNING, INFO, DEBUG) over selected time range.
Counted using count_over_time([label_selector][$__auto]) grouped by log level.
Bar chart shows relative volume for easy comparison across log levels and identification of anomalies.
Normal baseline: [X] ERROR/hour, [Y] WARNING/hour. Spikes indicate application issues or infrastructure problems.

Business Impact: Application health and debugging signal. ERROR spikes often precede user-facing incidents.
Action Required: Investigate ERROR spikes >2× baseline immediately. WARNING sustained >5× baseline suggests degradation. Review logs in detail using drill-down link.
```

#### Cache Hit Rate (Stat)

```
Cache hit rate percentage showing successful cache retrievals vs total cache requests.
Formula: (cache_hits / (cache_hits + cache_misses)) × 100.
High hit rate (>80%) indicates efficient caching. Low hit rate suggests cache invalidation issues or insufficient cache size.
Thresholds: Red <60% (ineffective caching), Yellow 60-80% (suboptimal), Green >80% (healthy).

Business Impact: Database load reduction and API response time. Low hit rate increases database queries by [X]× and latency by [Y]ms.
Action Required: If sustained <70% for >1 hour, investigate cache invalidation logic, cache size limits, or cache key distribution.
```

### Anti-Pattern Examples (Generic, Avoid)

#### Bad Description #1

```
CPU Usage gauge display. Tracks avg metric. Thresholds indicate acceptable ranges.
```

**Problems**:
- ❌ No formula or data source specified
- ❌ No action guidance ("acceptable" is vague)
- ❌ No business context (why does CPU matter?)
- ❌ States the obvious (title already says "CPU Usage")

#### Bad Description #2

```
Cluster CPU Usage current value. Tracks sum metric.
```

**Problems**:
- ❌ Restates title without adding value
- ❌ No interpretation help (is 50% good or bad?)
- ❌ No thresholds explained
- ❌ No actionable guidance

#### Good Description (Contrast)

```
Kubernetes cluster CPU utilization as percentage of total allocatable CPU cores.
Formula: sum(rate(container_cpu_usage_seconds_total[5m])) / sum(kube_node_status_allocatable{resource="cpu"}) × 100.
Shows aggregate CPU usage across all nodes in cluster. Does not include system/kernel CPU.
Thresholds: Red >85% (cluster near capacity, pod scheduling may fail), Yellow >70% (plan node addition), Green <70% (healthy).

Business Impact: Cluster capacity planning and workload scheduling reliability. High utilization risks pod eviction and scheduling failures.
Action Required: Add nodes when sustained >70% for 1 hour. Review resource requests/limits if spiky. Consider horizontal pod autoscaling for elastic workloads.
```

---

## 5. Signal-to-Noise Optimization (12 Techniques)

### Technique 1: Threshold-Based Color Activation

**Rule**: All panels remain grayscale until threshold breach—color = alert signal

**Implementation**:
```json
{
  "fieldConfig": {
    "defaults": {
      "color": {"mode": "thresholds"},
      "thresholds": {
        "steps": [
          {"color": "gray", "value": null},
          {"color": "yellow", "value": 80},
          {"color": "red", "value": 90}
        ]
      }
    }
  }
}
```

**Example**: CPU line gray <80%, yellow 80-90%, red >90% with area fill + thicker border

### Technique 2: Reference Line Baselines

**Rule**: Show expected behavior as subtle gray line or shaded band

**Purpose**: Provides context for "normal" vs "anomalous" without cluttering

**Grafana implementation**:
```json
{
  "fieldConfig": {
    "overrides": [
      {
        "matcher": {"id": "byName", "options": "Expected Baseline"},
        "properties": [
          {"id": "custom.lineStyle", "value": {"dash": [10, 10], "fill": "dash"}},
          {"id": "custom.lineWidth", "value": 1},
          {"id": "color", "value": {"fixedColor": "gray", "mode": "fixed"}},
          {"id": "custom.fillOpacity", "value": 15}
        ]
      }
    ]
  }
}
```

**Example**: Expected request rate baseline ±10% as gray band, actual request rate as solid blue line

### Technique 3: Grid Line Minimization

**Rule**: Reduce grid opacity to barely visible (10-20%), remove minor grid lines

**Grafana configuration**:
```json
{
  "options": {
    "graph": {
      "gridPos": {"opacity": 0.1}
    }
  }
}
```

**Target intervals**:
- 24-hour view: Hourly major grid only
- 7-day view: Daily major grid only
- 30-day view: Weekly major grid only

### Technique 4: Legend Placement Optimization

**Problem**: Legends consume 20-30% of vertical space and repeat information

**Solutions**:

**Option 1: Hidden** (use tooltips only)
```json
{"legend": {"displayMode": "hidden"}}
```
- Best for: Single-series panels, obvious metric names

**Option 2: Bottom Horizontal**
```json
{"legend": {"displayMode": "list", "placement": "bottom"}}
```
- Best for: Multi-series <7 lines

**Option 3: Table Mode**
```json
{"legend": {"displayMode": "table", "placement": "right", "calcs": ["last", "mean", "max"]}}
```
- Best for: 7+ series, sortable columns needed
- Example: 10-server CPU dashboard with current/avg/max columns

### Technique 5: Annotation Selectivity

**Rule**: Only annotate high-impact events (max 5-10 per visible timeframe)

**Appropriate annotations**:
- ✅ Deployments with Git SHA
- ✅ Incidents with ticket link
- ✅ SLA breaches
- ✅ Configuration changes
- ❌ Routine alerts (creates visual clutter)
- ❌ Informational events

**Grafana annotation query**:
```json
{
  "datasource": "Prometheus",
  "expr": "ALERTS{alertstate=\"firing\", severity=\"critical\"}",
  "tagKeys": "alertname,severity",
  "textFormat": "{{alertname}}: {{summary}}",
  "titleFormat": "🚨 Critical Alert"
}
```

### Technique 6: Unit Formatting Consistency

**Rule**: Use short units with SI prefixes for readability

**Grafana units**:
- **Bytes**: `bytes` (auto SI: 5.2MB, 1.3GB)
- **Rates**: `reqps`, `Bps` (requests/bytes per second)
- **Counts**: `short` (5.2K, 1.3M)
- **Time**: `ms`, `s` (auto format: 1.5s, 250ms)

**Decimal places**:
- 0 decimals: Counts
- 1-2 decimals: Rates, percentages
- 3+ decimals: Scientific measurements

**Example**: "5.2M req/s" instead of "5,234,567 requests per second"

### Technique 7: Whitespace as Signal

**Rule**: Use spacing intentionally to group related content

**Implementation**:
- **0 units**: Directly related panels (e.g., CPU + Memory in same server)
- **1 unit**: Related metrics (e.g., different services in same row)
- **2 units**: Unrelated metric groups (e.g., API metrics vs Database metrics)

**Example**:
```
Database Metrics [y=0]
  Panel 1: Query Rate (x=0)
  Panel 2: Connection Pool (x=6)  // 0 gap - same database

[1 unit vertical gap]

API Metrics [y=9]
  Panel 3: Request Rate (x=0)
  Panel 4: Error Rate (x=6)       // 0 gap - same API
```

### Technique 8: Single-Purpose Panels

**Rule**: Each panel answers ONE question, max 5-7 series per timeseries

**Anti-pattern**: "Kitchen sink" panels with 20+ series
- Impossible to distinguish lines
- Legend consumes entire panel
- No actionable insight

**Solution**: Separate panels for distinct questions
- ✅ Panel 1: Request Rate
- ✅ Panel 2: Error Rate
- ✅ Panel 3: Latency p95
- ❌ Panel 1: "API Health" (combining all metrics)

### Technique 9: Color Palette Discipline

**Rule**: Define maximum 5-color palette and stick to it

**Recommended palette**:
- **Gray** (#999999): Normal state, non-alert data
- **Green** (#009E73): Success, healthy, within SLO
- **Yellow** (#F0E442): Warning, approaching threshold
- **Red** (#D55E00): Critical, SLO breach, immediate action
- **Blue** (#0072B2): Informational, secondary data

**NEVER use**: Default rainbow palette (12+ colors creates visual chaos)

**Grafana custom theme**:
```json
{
  "colors": {
    "series": ["#999999", "#009E73", "#F0E442", "#D55E00", "#0072B2"]
  }
}
```

### Technique 10: Dynamic Range Adjustment

**Auto-scale**: Use for trend analysis (allows zooming to detail)
```json
{"fieldConfig": {"defaults": {"min": null, "max": null}}}
```
- Best for: Latency, request rates, variable metrics

**Fixed scale**: Use for SLA monitoring (consistent reference frame)
```json
{"fieldConfig": {"defaults": {"min": 0, "max": 100}}}
```
- Best for: Percentages, SLO compliance, utilization

**Soft min/max**: Auto-scale with floor/ceiling
```json
{"fieldConfig": {"defaults": {"min": 0, "max": null}}}
```
- Best for: Rates that can't go negative but have no upper bound

### Technique 11: Text Panel Economy

**Rule**: Maximum 2-3 text panels per dashboard

**Appropriate uses**:
- Dashboard title and purpose (1 line)
- Critical instructions or SLA links (2-3 lines)
- On-call rotation contact (1 line)

**Use panel descriptions instead** (ℹ️ icon) for:
- Metric explanations
- Threshold rationale
- Troubleshooting tips

**Example text panel**:
```markdown
# API Gateway Operational Dashboard
**Purpose**: Monitor request rates, error rates, latency, and saturation for api-gateway service
**SLA**: 99.9% uptime, p95 latency <200ms | [SLA Doc](https://wiki/sla) | On-call: @team-backend
```

### Technique 12: Conditional Visibility

**Rule**: Hide panels when healthy, show when alerting (progressive disclosure)

**Grafana implementation**:
- Dashboard links to "Incidents" dashboard for active problems
- Use template variables filtered by alert state
- Panel repeat with conditional query

**Example**:
```json
{
  "panels": [{
    "repeat": "alert_state",
    "repeatDirection": "v",
    "targets": [{
      "expr": "ALERTS{alertstate=\"firing\"}"
    }]
  }]
}
```

**Note**: Requires careful testing—users must know where to look for problems

---

## 6. SRE Dashboard Design Patterns

### Four Golden Signals (Google SRE)

**Principle**: Display ALL service health signals on ONE PAGE for temporal correlation

**Why it matters**: When latency spikes, you need to see if errors also increased, traffic changed, or saturation occurred—all in one glance.

#### Layout Structure

```
Row 1 (y=0, h=6): [Service Name] Health - KPI Overview
  Panel 1 (x=0, w=6):  Request Rate (stat with sparkline)
  Panel 2 (x=6, w=6):  Error Rate % (stat with threshold colors)
  Panel 3 (x=12, w=6): Latency p95 (stat with sparkline)
  Panel 4 (x=18, w=6): Saturation % (gauge: CPU, memory, or queue depth)

Row 2 (y=6, h=8): [Service Name] Trends - Temporal Correlation
  Panel 5 (x=0, w=12):  Request/Error Rate Over Time (2 series, shared Y-axis)
  Panel 6 (x=12, w=12): Latency Percentiles (p50, p90, p99)

Row 3 (y=14, h=8): [Service Name] Saturation Detail
  Panel 7 (x=0, w=8):  CPU Utilization %
  Panel 8 (x=8, w=8):  Memory Utilization %
  Panel 9 (x=16, w=8): Queue Depth / Connection Pool
```

#### Critical Insight

**Track latency separately for successful vs failed requests**:
- "Slow error is worse than fast error"
- Query: `histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{status!~"5.."}[5m]))`

### RED Method (Service-Centric)

**RED = Rate, Errors, Duration**

**Use for**: Service-level monitoring (APIs, microservices, web applications)

#### Two-Column Layout

```
Left Column (w=12): Rate & Errors
  Panel 1 (y=0, h=8):  Request Rate Trend (timeseries)
  Panel 2 (y=8, h=6):  Error Rate % (stat with threshold)
  Panel 3 (y=14, h=10): Error Count by Type (bar chart: 4xx vs 5xx, horizontal)

Right Column (w=12): Duration
  Panel 4 (y=0, h=6):  Latency p95 (stat with sparkline)
  Panel 5 (y=6, h=12): Latency Percentiles Trend (timeseries: p50, p95, p99)
  Panel 6 (y=18, h=10): Latency Histogram (heatmap showing distribution over time)
```

#### Integration Point

**Link RED (user-facing) to USE (infrastructure)**:
- Click anomaly in RED dashboard → Drill to USE dashboard
- Example: High latency in RED → Check CPU/Memory/Disk in USE

### USE Method (Resource-Centric)

**USE = Utilization, Saturation, Errors**

**Use for**: Infrastructure monitoring (servers, containers, databases, network)

#### Three-Column Layout

```
Left Column (w=8): Utilization
  Panel 1 (y=0, h=8):  CPU % (gauge)
  Panel 2 (y=8, h=8):  Memory % (gauge)
  Panel 3 (y=16, h=8): Disk % (gauge)
  Panel 4 (y=24, h=8): Network Utilization Trend (timeseries, w=24 full-width)

Center Column (w=8): Saturation
  Panel 5 (y=0, h=8):  Load Average (stat, 1/5/15 min)
  Panel 6 (y=8, h=16): Queue Depth Over Time (timeseries)

Right Column (w=8): Errors
  Panel 7 (y=0, h=8):  Hardware Error Rate (stat)
  Panel 8 (y=8, h=8):  OOM Kills Count (stat)
  Panel 9 (y=16, h=8): Disk I/O Errors (timeseries)
```

### Threshold Configuration for SLO Integration

**Pattern**: Tie threshold colors to SLO targets with error budget visualization

#### Example: 99.9% SLO Configuration

```json
{
  "type": "gauge",
  "title": "SLO Compliance (Target: 99.9%)",
  "fieldConfig": {
    "defaults": {
      "min": 0,
      "max": 100,
      "unit": "percent",
      "thresholds": {
        "mode": "absolute",
        "steps": [
          {"color": "#D55E00", "value": 0},      // Red: SLO breach
          {"color": "#F0E442", "value": 90},     // Yellow: 90% error budget consumed
          {"color": "#009E73", "value": 99.9}    // Green: Meeting SLO
        ]
      }
    }
  },
  "description": "SLO Compliance: 99.9% uptime target (43 minutes downtime allowed per 30 days). Yellow at 90% error budget consumed (10% safety margin), red if SLO breached. Error budget = (100% - actual_uptime). Action: Alert when <99.9% for 5min (fast-burn) or <99.95% for 1h (slow-burn) using multi-window multi-burn-rate alerting."
}
```

#### Multi-Window Multi-Burn-Rate Alerting

**Fast-burn window** (5 minutes):
- Detects rapid SLO consumption (outages, severe degradation)
- Threshold: <99.9% for 5 consecutive minutes

**Slow-burn window** (1 hour):
- Detects gradual SLO erosion (performance degradation, elevated errors)
- Threshold: <99.95% over 1 hour rolling average

**Why both**: Fast-burn catches incidents quickly, slow-burn catches subtle degradation before total budget exhaustion

---

## 7. Dashboard Maturity & Management

### Maturity Progression

#### Low Maturity (Ad-Hoc)

❌ **Characteristics**:
- Uncontrolled dashboard creation (anyone can create/edit)
- Dashboard duplication (copy + minor changes)
- No version control (browser editing only)
- Dashboard sprawl (100s of unused dashboards)
- No ownership tracking

❌ **Problems**:
- Update propagation failures (fix in one, breaks in copy)
- No change history or rollback
- Unknown maintenance burden

#### Medium Maturity (Structured)

⚠️ **Characteristics**:
- Template variables prevent duplication (single dashboard, multiple instances)
- Hierarchical drill-down links (summary → detail)
- Color conventions documented (blue=healthy, red=problem)
- Version-controlled JSON in Git

⚠️ **Remaining gaps**:
- Still allows browser editing (changes bypass Git)
- No automated testing
- Manual deployment

#### High Maturity (Production-Grade)

✅ **Characteristics**:
- Active sprawl reduction (periodic dashboard reviews, automated cleanup)
- Scripted dashboard generation (Grafonnet, Grafanalib, Terraform)
- No browser editing (viewers adjust via template variables only)
- Dedicated testing instance (validate before production)
- Automated deployment via CI/CD
- Dashboard-as-code with PR reviews

✅ **Benefits**:
- Consistent quality and design patterns
- Change tracking and rollback capability
- Scalable maintenance (generate 100s of dashboards from templates)
- Reduced technical debt

### Anti-Patterns to Avoid

#### Anti-Pattern 1: Dashboard Sprawl

**Problem**: Copying dashboards with minor changes creates update propagation failures
- Fix a bug in original → Need to fix in 10 copies
- Copy inconsistencies (some have fix, some don't)

**Solution**: Use template variables
- **Bad**: Separate dashboard per namespace (api-prod, api-staging, api-dev)
- **Good**: Single dashboard with `$namespace` variable

**Example**:
```json
{
  "templating": {
    "list": [
      {
        "name": "namespace",
        "type": "query",
        "query": "label_values(kube_pod_info, namespace)",
        "multi": false
      }
    ]
  },
  "panels": [{
    "targets": [{
      "expr": "sum(rate(http_requests_total{namespace=\"$namespace\"}[5m]))"
    }]
  }]
}
```

#### Anti-Pattern 2: Missing Ownership

**Problem**: No indication of who maintains dashboard or its purpose
- Dashboards become orphaned over time
- No one knows if dashboard is still needed
- Unclear who to ask for changes

**Solution**: Include ownership identifiers and lifecycle tags
- **Dashboard title**: "TEST - API Monitoring (owner: @alice, team: backend)"
- **Tags**: `owner:alice`, `team:backend`, `lifecycle:production`
- **Description**: Purpose, SLA links, maintenance schedule

**TEST/TMP Prefix Convention**:
- `TEST -` prefix signals temporary/experimental dashboard
- Automated cleanup: Delete TEST dashboards >30 days old
- Promotion process: Remove TEST prefix when productionized

#### Anti-Pattern 3: No Tag Hygiene

**Problem**: Copying dashboards includes tags, creating false search results
- Search for `prod` returns dev/staging dashboards
- Tag sprawl (100+ unique tags with typos)

**Solution**: Clear tags when duplicating, use consistent taxonomy

**Recommended Tag Structure**:
- **Environment**: `env:prod`, `env:staging`, `env:dev`
- **Team**: `team:backend`, `team:frontend`, `team:data`
- **Type**: `type:service-health`, `type:infrastructure`, `type:business`
- **SLO Criticality**: `slo:critical`, `slo:important`, `slo:informational`

---

## 8. Reusable Configuration Patterns

### Pattern 1: Semantic Token Color Scheme

**Purpose**: Consistent color meaning across dashboards (blue=input, green=output, purple=cache)

```json
{
  "fieldConfig": {
    "overrides": [
      {
        "matcher": {"id": "byName", "options": "input"},
        "properties": [
          {"id": "color", "value": {"fixedColor": "#0072B2", "mode": "fixed"}}
        ]
      },
      {
        "matcher": {"id": "byName", "options": "output"},
        "properties": [
          {"id": "color", "value": {"fixedColor": "#009E73", "mode": "fixed"}}
        ]
      },
      {
        "matcher": {"id": "byName", "options": "cache_read"},
        "properties": [
          {"id": "color", "value": {"fixedColor": "#CC79A7", "mode": "fixed"}}
        ]
      },
      {
        "matcher": {"id": "byName", "options": "cache_write"},
        "properties": [
          {"id": "color", "value": {"fixedColor": "#E69F00", "mode": "fixed"}}
        ]
      }
    ]
  }
}
```

### Pattern 2: Comprehensive Description Template

```
[METRIC NAME] [VISUALIZATION TYPE]. [PURPOSE IN 1 SENTENCE]. [CALCULATION FORMULA]. [INTERPRETATION GUIDE]. Thresholds: [THRESHOLD VALUES AND MEANINGS].

Business Impact: [WHY THIS MATTERS TO OPERATIONS/BUSINESS].
Action Required: [SPECIFIC ACTIONS WHEN THRESHOLDS BREACHED].
```

**Example**:
```
API Gateway Request Rate time series. Tracks total HTTP requests per second across all endpoints. Calculated using sum(rate(http_requests_total{service="api-gateway"}[5m])). Shows temporal trends with 5-minute rate window. Thresholds: Red >5000 req/s (approaching capacity), Yellow >4000 req/s (scaling recommended), Green <4000 req/s (healthy).

Business Impact: Indicates traffic patterns and capacity utilization. Sustained high rates may require infrastructure scaling.
Action Required: Scale horizontally when sustained >4000 req/s for 15 minutes. Review traffic sources for unexpected spikes >2× baseline.
```

### Pattern 3: Log Level Color Overrides

**Purpose**: Consistent semantic colors for log severity levels

```json
{
  "fieldConfig": {
    "overrides": [
      {
        "matcher": {"id": "byName", "options": "ERROR"},
        "properties": [
          {"id": "color", "value": {"fixedColor": "#D55E00", "mode": "fixed"}}
        ]
      },
      {
        "matcher": {"id": "byName", "options": "WARNING"},
        "properties": [
          {"id": "color", "value": {"fixedColor": "#F0E442", "mode": "fixed"}}
        ]
      },
      {
        "matcher": {"id": "byName", "options": "INFO"},
        "properties": [
          {"id": "color", "value": {"fixedColor": "#0072B2", "mode": "fixed"}}
        ]
      },
      {
        "matcher": {"id": "byName", "options": "DEBUG"},
        "properties": [
          {"id": "color", "value": {"fixedColor": "#CC79A7", "mode": "fixed"}}
        ]
      }
    ]
  }
}
```

### Pattern 4: Butterfly Chart Configuration (Add/Remove Visualization)

**Purpose**: Compare opposing metrics (lines added vs removed, bytes in vs out)

```json
{
  "type": "timeseries",
  "fieldConfig": {
    "defaults": {
      "custom": {
        "axisCenteredZero": true
      }
    },
    "overrides": [
      {
        "matcher": {"id": "byName", "options": "Lines Added"},
        "properties": [
          {"id": "color", "value": {"fixedColor": "#009E73", "mode": "fixed"}},
          {"id": "custom.fillOpacity", "value": 30}
        ]
      },
      {
        "matcher": {"id": "byName", "options": "Lines Removed"},
        "properties": [
          {"id": "color", "value": {"fixedColor": "#D55E00", "mode": "fixed"}},
          {"id": "custom.transform", "value": "negative-Y"},
          {"id": "custom.fillOpacity", "value": 30}
        ]
      }
    ]
  }
}
```

### Pattern 5: 3-Tier Performance Thresholds (Colorblind-Safe)

```json
{
  "fieldConfig": {
    "defaults": {
      "thresholds": {
        "mode": "absolute",
        "steps": [
          {"color": "#009E73", "value": null},    // Bluish-green (not pure green)
          {"color": "#F0E442", "value": 70},      // Yellow
          {"color": "#D55E00", "value": 85}       // Vermillion (not pure red)
        ]
      }
    }
  }
}
```

### Pattern 6: Table Formatting with Gradient Gauge

**Purpose**: Percentage columns with visual gradient bars

```json
{
  "type": "table",
  "fieldConfig": {
    "overrides": [
      {
        "matcher": {"id": "byName", "options": "Utilization %"},
        "properties": [
          {"id": "custom.displayMode", "value": "gradient-gauge"},
          {"id": "unit", "value": "percent"},
          {"id": "min", "value": 0},
          {"id": "max", "value": 100},
          {"id": "thresholds", "value": {
            "steps": [
              {"color": "green", "value": 0},
              {"color": "yellow", "value": 70},
              {"color": "red", "value": 85}
            ]
          }}
        ]
      }
    ]
  }
}
```

### Pattern 7: Stacked Area Chart

**Purpose**: Composition over time (resource breakdown, traffic by endpoint)

```json
{
  "type": "timeseries",
  "fieldConfig": {
    "defaults": {
      "custom": {
        "drawStyle": "line",
        "fillOpacity": 50,
        "stacking": {"mode": "normal"}
      }
    }
  }
}
```

### Pattern 8: Legend with Calculations

**Purpose**: Show current/average/max values in table legend

```json
{
  "options": {
    "legend": {
      "displayMode": "table",
      "placement": "bottom",
      "calcs": ["last", "mean", "max"],
      "sortBy": "Last",
      "sortDesc": true
    }
  }
}
```

---

## 9. Validation Checklist

Use this checklist for every dashboard created or modified:

### Accessibility (WCAG 2.1 AA)

- [ ] **Text contrast** ≥4.5:1 for standard text (use [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/))
- [ ] **UI component contrast** ≥3:1 against adjacent colors
- [ ] **Color NEVER sole indicator** (2+ visual elements: icons + text labels + shapes/patterns + borders)
- [ ] **Colorblind-safe palette** used (Okabe-Ito, IBM Carbon, or Blue-Orange)
- [ ] **Font size** ≥14px for operational dashboards, ≥16px for executive dashboards
- [ ] **Line height** 1.4-1.65 for body text, 1.0-1.3 for headings

### Panel Configuration

- [ ] **All panels have descriptions** answering WHY/WHAT/HOW/WHEN (not generic templates)
- [ ] **Thresholds tied to SLO targets** or operational limits (not arbitrary round numbers)
- [ ] **Units specified** for all metrics (reqps, ms, bytes, percent, short)
- [ ] **Legend placement consistent** (bottom for timeseries, right/hidden for comparisons)
- [ ] **Max 5-7 series** per timeseries panel (use filtering or separate panels)
- [ ] **Decimal precision** appropriate (0 for counts, 1-2 for rates, 3+ for percentages)

### Layout & Organization

- [ ] **F-pattern or Z-pattern layout** followed (KPIs top-left, details bottom)
- [ ] **Related panels grouped** with 0-1 unit gaps
- [ ] **Unrelated groups separated** by 2 unit gaps
- [ ] **Row titles** used for collapsible sections (descriptive, not generic)
- [ ] **Progressive disclosure** (summary panels link to detail dashboards)
- [ ] **Consistent panel heights** within groups

### Signal-to-Noise

- [ ] **Grid opacity** ≤0.2 (barely visible background)
- [ ] **Color palette** ≤5 colors (gray, green, yellow, red, blue)
- [ ] **Annotations** ≤10 per visible timeframe (deployments, incidents, SLA breaches only)
- [ ] **Text panels** ≤3 per dashboard (title, instructions, critical alerts)
- [ ] **Whitespace** used intentionally (not random spacing)
- [ ] **Single-purpose panels** (each answers one question)

### SRE Principles

- [ ] **Dashboard tells a story** or answers a specific question
- [ ] **One-page temporal correlation** for related metrics (Four Golden Signals on one page)
- [ ] **Threshold gradients** show state transitions (gradient mode enabled where appropriate)
- [ ] **Template variables** prevent dashboard sprawl (use `$variable` instead of duplicating dashboards)
- [ ] **Ownership documented** (title includes owner/team, tags applied, description includes purpose)
- [ ] **SLO integration** (thresholds tied to error budgets, multi-window alerting configured)

### Chart Type Appropriateness

- [ ] **Comparison** (categorical) → Bar Chart (horizontal if >6 categories)
- [ ] **Trend** (time series) → Line Chart (Time Series panel)
- [ ] **Distribution** → Histogram or Heatmap
- [ ] **Composition** → Stacked Bar or Table (NEVER Pie Chart if >3 slices)
- [ ] **Single metric** → Stat (unbounded) or Gauge (0-100% bounded)

---

## References & Further Reading

**Official Grafana Documentation**:
- [Panel and Visualization Types](https://grafana.com/docs/grafana/latest/panels-visualizations/)
- [Thresholds and Overrides](https://grafana.com/docs/grafana/latest/panels-visualizations/configure-thresholds/)
- [Dashboard Best Practices](https://grafana.com/docs/grafana/latest/dashboards/build-dashboards/best-practices/)

**Accessibility Standards**:
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [Color Oracle](https://colororacle.org/) (colorblindness simulator)

**Data Visualization Theory**:
- Edward Tufte: *The Visual Display of Quantitative Information*
- Stephen Few: *Information Dashboard Design*
- Cleveland & McGill: *Graphical Perception* (perceptual hierarchy research)

**SRE Patterns**:
- [Google SRE Book - Chapter 6: Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/)
- [RED Method](https://grafana.com/blog/2018/08/02/the-red-method-how-to-instrument-your-services/)
- [USE Method](http://www.brendangregg.com/usemethod.html)

---

**This guide provides comprehensive visualization expertise for creating readable, accessible, signal-focused Grafana dashboards following SRE best practices, WCAG 2.1 AA accessibility standards, and data visualization theory from Tufte, Few, and Cleveland.**
