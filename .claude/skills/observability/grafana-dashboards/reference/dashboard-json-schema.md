# Grafana Dashboard JSON Schema Reference

> Schema Version 39 | Grafana 11.x

---

## Table of Contents

1. [Top-Level Structure](#top-level-structure)
2. [Time Settings](#time-settings)
3. [Templating Variables](#templating-variables)
4. [Panel Structure](#panel-structure)
5. [Panel Types](#panel-types)
6. [GridPos Layout System](#gridpos-layout-system)
7. [Field Configuration](#field-configuration)
8. [Prometheus Targets](#prometheus-targets)
9. [Provisioning](#provisioning)
10. [Quick Reference](#quick-reference)

---

## Top-Level Structure

```json
{
  "id": null,
  "uid": "unique-dashboard-id",
  "title": "Dashboard Title",
  "description": "Dashboard description",
  "tags": ["tag1", "tag2"],
  "schemaVersion": 39,
  "version": 1,
  "editable": true,
  "graphTooltip": 1,
  "timezone": "browser",
  "refresh": "30s",
  "time": {},
  "timepicker": {},
  "templating": {},
  "annotations": {},
  "panels": [],
  "links": []
}
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | number/null | Auto-assigned. Use `null` for new dashboards |
| `uid` | string | Unique ID (8-40 chars). Used in URLs |
| `schemaVersion` | number | Use 39 for Grafana 11.x |
| `graphTooltip` | number | 0=default, 1=shared crosshair, 2=shared tooltip |
| `refresh` | string | "5s", "30s", "1m", "5m", "15m", "30m", "1h" |

---

## Time Settings

```json
{
  "time": {
    "from": "now-6h",
    "to": "now"
  },
  "timepicker": {
    "refresh_intervals": ["5s", "10s", "30s", "1m", "5m"],
    "hidden": false
  }
}
```

### Time Expressions

| Expression | Description |
|------------|-------------|
| `now` | Current time |
| `now-1h` | 1 hour ago |
| `now-6h` | 6 hours ago |
| `now/d` | Start of current day |
| `now-1d/d` | Start of yesterday |

---

## Templating Variables

```json
{
  "templating": {
    "list": [
      {
        "name": "datasource",
        "type": "datasource",
        "query": "prometheus",
        "current": {},
        "hide": 0
      },
      {
        "name": "namespace",
        "type": "query",
        "datasource": {"type": "prometheus", "uid": "${datasource}"},
        "query": "label_values(kube_namespace_labels, namespace)",
        "includeAll": true,
        "multi": true,
        "allValue": ".*",
        "refresh": 2,
        "sort": 1
      }
    ]
  }
}
```

### Variable Types

| Type | Use Case |
|------|----------|
| `datasource` | Select datasource |
| `query` | Dynamic values from datasource |
| `interval` | Time interval selection |
| `custom` | Static list of values |
| `constant` | Hidden constant |
| `textbox` | Free-text input |

### Refresh Options

| Value | Behavior |
|-------|----------|
| 0 | Never |
| 1 | On dashboard load |
| 2 | On time range change |

### Hide Options

| Value | Behavior |
|-------|----------|
| 0 | Visible |
| 1 | Label hidden |
| 2 | Completely hidden |

---

## Panel Structure

```json
{
  "id": 1,
  "type": "timeseries",
  "title": "Panel Title",
  "description": "Panel description",
  "gridPos": {"x": 0, "y": 0, "w": 12, "h": 8},
  "datasource": {"type": "prometheus", "uid": "${datasource}"},
  "targets": [],
  "options": {},
  "fieldConfig": {},
  "transformations": []
}
```

| Field | Description |
|-------|-------------|
| `id` | Unique within dashboard (auto-increment from 1) |
| `type` | Panel visualization type |
| `gridPos` | Position and size |
| `repeat` | Variable name to repeat panel for |
| `repeatDirection` | "h" or "v" |

---

## Panel Types

### Time Series

```json
{
  "type": "timeseries",
  "options": {
    "tooltip": {"mode": "multi", "sort": "desc"},
    "legend": {
      "displayMode": "table",
      "placement": "bottom",
      "calcs": ["mean", "max", "last"]
    }
  },
  "fieldConfig": {
    "defaults": {
      "custom": {
        "drawStyle": "line",
        "fillOpacity": 10,
        "lineWidth": 1,
        "showPoints": "never",
        "stacking": {"mode": "none"}
      },
      "unit": "percent",
      "min": 0,
      "max": 100
    }
  }
}
```

### Stat

```json
{
  "type": "stat",
  "options": {
    "reduceOptions": {
      "calcs": ["lastNotNull"]
    },
    "colorMode": "value",
    "graphMode": "area"
  },
  "fieldConfig": {
    "defaults": {
      "thresholds": {
        "mode": "absolute",
        "steps": [
          {"color": "red", "value": null},
          {"color": "yellow", "value": 80},
          {"color": "green", "value": 95}
        ]
      }
    }
  }
}
```

### Gauge

```json
{
  "type": "gauge",
  "options": {
    "showThresholdLabels": false,
    "showThresholdMarkers": true
  },
  "fieldConfig": {
    "defaults": {
      "min": 0,
      "max": 100,
      "thresholds": {
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

### Table

```json
{
  "type": "table",
  "options": {
    "showHeader": true,
    "cellHeight": "sm"
  },
  "fieldConfig": {
    "defaults": {
      "custom": {
        "filterable": true
      }
    }
  }
}
```

### Row

```json
{
  "type": "row",
  "title": "Section Title",
  "collapsed": false,
  "gridPos": {"x": 0, "y": 0, "w": 24, "h": 1},
  "panels": []
}
```

---

## GridPos Layout System

24-column grid system.

```json
{
  "gridPos": {
    "x": 0,    // Column (0-23)
    "y": 0,    // Row position
    "w": 12,   // Width (1-24)
    "h": 8    // Height (grid units)
  }
}
```

### Standard Widths

| Width | Columns | Use Case |
|-------|---------|----------|
| 24 | Full | Wide graphs, tables |
| 12 | Half | Two panels |
| 8 | Third | Three panels |
| 6 | Quarter | Four stats |
| 4 | Sixth | Six small stats |

### Standard Heights

| Height | Use Case |
|--------|----------|
| 1 | Row panels |
| 4 | Stat panels |
| 6 | Gauges |
| 8 | Standard charts |
| 10-12 | Large graphs |
| 16 | Full-height tables |

---

## Field Configuration

```json
{
  "fieldConfig": {
    "defaults": {
      "unit": "bytes",
      "decimals": 2,
      "min": 0,
      "displayName": "${__field.name}",
      "thresholds": {
        "mode": "absolute",
        "steps": [
          {"color": "green", "value": null},
          {"color": "red", "value": 90}
        ]
      },
      "mappings": []
    },
    "overrides": [
      {
        "matcher": {"id": "byName", "options": "cpu_usage"},
        "properties": [
          {"id": "unit", "value": "percent"}
        ]
      }
    ]
  }
}
```

### Common Units

| Unit | Description |
|------|-------------|
| `percent` | Percentage (0-100) |
| `percentunit` | Percentage (0-1) |
| `bytes` | Bytes (auto-scale) |
| `s` | Seconds |
| `ms` | Milliseconds |
| `reqps` | Requests/second |
| `short` | Short number |

---

## Prometheus Targets

```json
{
  "targets": [
    {
      "refId": "A",
      "datasource": {"type": "prometheus", "uid": "${datasource}"},
      "expr": "rate(http_requests_total{namespace=\"$namespace\"}[$__rate_interval])",
      "legendFormat": "{{pod}} - {{method}}",
      "instant": false,
      "range": true,
      "format": "time_series"
    }
  ]
}
```

### Built-in Variables

| Variable | Description |
|----------|-------------|
| `$__rate_interval` | Recommended rate interval |
| `$__interval` | Auto-calculated interval |
| `$__range` | Dashboard time range |
| `$__from` | Start time (Unix ms) |
| `$__to` | End time (Unix ms) |

---

## Provisioning

### Kubernetes ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: grafana-dashboards
  namespace: monitoring
  labels:
    grafana_dashboard: "1"
data:
  my-dashboard.json: |
    {
      "dashboard": {...},
      "folderId": 0,
      "overwrite": true
    }
```

---

## Quick Reference

### Minimal Dashboard

```json
{
  "uid": "template",
  "title": "Dashboard Template",
  "schemaVersion": 39,
  "editable": true,
  "time": {"from": "now-6h", "to": "now"},
  "refresh": "30s",
  "templating": {"list": []},
  "annotations": {"list": []},
  "panels": []
}
```

### Panel Template

```json
{
  "id": 1,
  "type": "timeseries",
  "title": "Panel Title",
  "gridPos": {"x": 0, "y": 0, "w": 12, "h": 8},
  "datasource": {"type": "prometheus", "uid": "${datasource}"},
  "targets": [
    {
      "refId": "A",
      "expr": "up",
      "legendFormat": "{{instance}}"
    }
  ],
  "options": {},
  "fieldConfig": {"defaults": {}, "overrides": []}
}
```

### Schema Versions

| Grafana | Schema |
|---------|--------|
| 11.x | 39 |
| 10.x | 38 |
| 9.x | 37 |

---

**Source**: Grafana Documentation via Context7
