# Grafana Dashboard Builder Documentation

Documentation supporting the grafana-dashboard-builder agent.

## Contents

| Document | Purpose |
|----------|---------|
| `domain-expertise.md` | Chart selection, accessibility (WCAG 2.1 AA), layout patterns, panel descriptions (WHY/WHAT/HOW/WHEN), signal-to-noise optimization |
| `frameworks.md` | SRE monitoring frameworks (Four Golden Signals, RED, USE), threshold-SLO integration, intent-to-framework mapping |
| `visualization-design-principles.md` | Comprehensive visualization guide: color theory, WCAG compliance, panel layouts, chart types, signal-to-noise techniques |
| `panel-description-templates.md` | Templates for effective panel descriptions (latency, errors, utilization, logs, cache, requests) |
| `sre-patterns.md` | Detailed SRE pattern implementations |
| `api-reference.md` | Prometheus API and Grafana API reference |

## Quick Reference

**Chart Selection**: 6-category decision tree (comparison/trend/distribution/composition/single/correlation)

**Accessibility**: WCAG 2.1 AA (4.5:1 contrast), 5 colorblind-safe palettes (Okabe-Ito, IBM Carbon, Blue-Orange, Monochromatic, Viridis)

**Layouts**: F-pattern (operational), Z-pattern (executive), 24-column Grafana grid

**Panel Descriptions**: WHY (business impact), WHAT (calculation), HOW (interpretation), WHEN (action threshold)

**Signal-to-Noise**: 12 techniques (threshold colors, reference lines, grid minimization, legend placement, annotation selectivity, unit formatting, whitespace, single-purpose panels, color discipline, dynamic range, text economy, conditional visibility)
