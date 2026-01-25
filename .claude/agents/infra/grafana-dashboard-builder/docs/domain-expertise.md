# Domain Expertise: Visualization Design

Comprehensive guide for Grafana dashboard visualization following WCAG 2.1 AA accessibility standards and data visualization best practices.

---

## 1. Chart Type Selection (6-Category Decision Tree)

| Category | When to Use | Chart Type | Configuration |
|----------|-------------|------------|---------------|
| **Comparison** | Categorical data (services, regions, error types) | Bar Chart | Horizontal if >6 categories |
| **Trend** | Change over time, continuous temporal | Time Series | Max 7 series, linear interpolation |
| **Distribution** | Frequency, density visualization | Histogram/Heatmap | Histogram for frequency, Heatmap for 2D density |
| **Composition** | Part-to-whole breakdown | Stacked Bar/Table | NEVER Pie Chart if >3 slices |
| **Single Metric** | Current value, KPI | Stat/Gauge | Stat for unbounded, Gauge for 0-100% |
| **Correlation** | Relationship between metrics | Parallel Time Series | Aligned X-axes, avoid scatter plots |

### Panel Type Configuration

**Stat Panel**: Compact (6w x 6h), sparkline enabled, color by threshold
```json
{"type": "stat", "options": {"graphMode": "area", "colorMode": "value"}}
```

**Gauge Panel**: Larger (8w x 8h), show threshold markers, requires min/max
```json
{"type": "gauge", "options": {"showThresholdLabels": true, "showThresholdMarkers": true}}
```

**Time Series**: Fill opacity 10%, max 7 series, table legend with calcs
```json
{"type": "timeseries", "options": {"legend": {"displayMode": "table", "calcs": ["last", "mean", "max"]}}}
```

---

## 2. Accessibility (WCAG 2.1 AA Compliance)

### Contrast Requirements
- **Text**: 4.5:1 minimum (standard), 3:1 (large text 18pt+)
- **UI Components**: 3:1 against adjacent colors
- **Testing**: WebAIM Contrast Checker, Color Oracle (colorblindness simulator)

### Color Independence (CRITICAL)
**NEVER use color alone** - always add 2+ visual elements:
1. **Icons**: checkmark, warning triangle, X, info circle
2. **Text labels**: "OK", "Warning", "Critical"
3. **Shapes**: Circle (normal), Triangle (caution), Square (error)
4. **Patterns**: Solid, stripes, dots, cross-hatch
5. **Borders**: 1px normal, 3px warning, 5px critical

### 5 Colorblind-Safe Palettes

| Palette | Colors | Best For |
|---------|--------|----------|
| **Okabe-Ito** | 9-color universal | Categorical data, multi-series (up to 9) |
| **IBM Carbon** | 5-color high-contrast | Sequential data, max 5 categories |
| **Blue-Orange** | Binary states | Two-metric comparisons, healthy/unhealthy |
| **Monochromatic** | Single hue gradients | Heatmaps, total colorblindness support |
| **Viridis/Magma** | Perceptually uniform | Heatmaps, continuous scales |

**Okabe-Ito Hex Values**: #E69F00 (orange), #56B4E9 (sky blue), #009E73 (bluish green), #F0E442 (yellow), #0072B2 (blue), #D55E00 (vermillion), #CC79A7 (reddish purple)

### Semantic Color Usage (Traffic Light Alternatives)
- **Avoid**: Pure red/green (8% of males are colorblind)
- **Use**: Bluish-green #009E73 (not pure green), Vermillion #D55E00 (not pure red)
- **60-30-10 Rule**: 60% neutral background, 30% primary data (blue/teal), 10% accent alerts (orange/vermillion)

### Typography
- **Font size**: >=14px operational, >=16px executive
- **Font family**: Lato or system sans-serif
- **Line height**: 1.4-1.65 body, 1.0-1.3 headings

---

## 3. Layout Design Patterns

### F-Pattern (Operational Dashboards)
Eye-tracking research: users scan F-shaped (horizontal top, vertical left, horizontal middle)

```
Row 1 (y=0, h=6): Global KPIs - Highest priority
  Panel 1-4 (x=0/6/12/18, w=6): Request Rate, Error Rate, Latency p95, Saturation

Row 2 (y=6, h=8): Time Series Trends
  Panel 5-6 (x=0/12, w=12): Request Rate Over Time, Error Rate Breakdown

Row 3 (y=14, h=12): Detailed Analysis
  Panel 7 (x=0, w=24): Log Stream (full-width)
```

**Rules**: Primary content at x=0, critical metrics top row, stat panels h=6-8, timeseries h=8-12

### Z-Pattern (Executive Dashboards)
Sparse layouts with 4-6 panels maximum

```
Top-left (primary KPI) -----> Top-right (secondary KPI)
         \                           /
          v                         v
Bottom-left (trend) ------> Bottom-right (status)
```

**Rules**: 2x2 grid, large stat panels (w=12, h=10), font 48px+, single-value focus

### Grouping Strategies
- **0-1 unit gap**: Related panels (same metric family)
- **2 unit gap**: Unrelated groups (different domains)
- **Row titles**: Descriptive (not "Metrics 1"), collapsible sections
- **Consistent heights**: Panels within group have same height

### Progressive Disclosure
Summary panels with drill-down links to detailed dashboards:
```
Global Overview -> Service Health -> Error Analysis / Latency Analysis / Logs
```

---

## 4. Panel Descriptions (4-Question Framework)

Every panel description MUST answer:

### WHY (Business Impact)
Why does this metric matter? User experience, cost, reliability impact.
> "p95 latency affects user satisfaction - delays >500ms cause 20% cart abandonment"

### WHAT (Calculation)
What is measured and how? Formula, aggregation, time window.
> "Tracks http_request_duration_seconds as histogram percentiles. Aggregation: histogram_quantile() across all instances. Window: $__rate_interval"

### HOW (Interpretation)
How to read the visualization? Baseline expectations, warning patterns.
> "Time series with 3 lines (p50/p95/p99). Expected baseline: p95 <150ms. Warning: p95 diverging from p50"

### WHEN (Action Threshold)
When to take action? Concrete thresholds with specific actions.
> "Green: p95 <200ms (no action). Yellow: 200-500ms (investigate within 15min). Red: >500ms for 5min (page SRE, enable debug logging)"

### Anti-Pattern Examples
**BAD**: "CPU Usage gauge display. Tracks avg metric." (no WHY, no formula, no action)
**GOOD**: Full 4-question framework with business impact, formula, interpretation, and actions

---

## 5. Signal-to-Noise Optimization (12 Techniques)

| # | Technique | Implementation |
|---|-----------|----------------|
| 1 | **Threshold colors** | Grayscale until breach (gray <80%, yellow 80-90%, red >90%) |
| 2 | **Reference baselines** | Gray dashed line/band showing expected +-10% |
| 3 | **Grid minimization** | Opacity 0.1-0.2, major intervals only |
| 4 | **Legend optimization** | Hidden (tooltips), bottom (list), or right (table with calcs) |
| 5 | **Annotation selectivity** | Max 5-10 per timeframe (deployments, incidents, SLA breaches only) |
| 6 | **Unit formatting** | SI prefixes (5.2K not 5200), appropriate decimals |
| 7 | **Whitespace as signal** | 0 units related, 2 units unrelated |
| 8 | **Single-purpose panels** | Each answers ONE question, max 5-7 series |
| 9 | **Color discipline** | Max 5 colors (gray, green, yellow, red, blue) |
| 10 | **Dynamic range** | Auto-scale for trends, fixed 0-100 for SLA |
| 11 | **Text panel economy** | Max 2-3 per dashboard, <50 words each |
| 12 | **Conditional visibility** | Hide when healthy, show when alerting |

### Data-Ink Ratio Principles (Tufte/Few/Cleveland)
- Target <20% non-data ink
- Remove: grid lines, legends when tooltips suffice, decorative backgrounds
- Avoid: 3D effects, gradients, drop shadows, rainbow palettes
- Hierarchy: Position > Length > Angle > Area > Color

---

## References

- **Grafana**: [Panel Types](https://grafana.com/docs/grafana/latest/panels-visualizations/), [Best Practices](https://grafana.com/docs/grafana/latest/dashboards/build-dashboards/best-practices/)
- **Accessibility**: [WCAG 2.1](https://www.w3.org/WAI/WCAG21/quickref/), [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- **Theory**: Tufte (Visual Display), Few (Dashboard Design), Cleveland & McGill (Graphical Perception)
