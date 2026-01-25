# Grafana 12.x Kubernetes Provisioning via Sidecar Pattern

**Purpose**: AI-readable documentation for Grafana dashboard provisioning using Kubernetes sidecar containers

**Target Agent**: grafana-dashboard-builder
**Technology Domain**: Grafana 12.x, Kubernetes, kiwigrid/k8s-sidecar
**Last Updated**: 2025-10-30
**Sources**:

- grafana/helm-charts (official Grafana Helm charts)
- kiwigrid/k8s-sidecar (sidecar container implementation)
- Grafana 12.x official documentation

---

## 1. Overview: Grafana 12.x Kubernetes Provisioning via Sidecar Pattern

### What is the Sidecar Pattern?

The **sidecar pattern** is a Kubernetes deployment strategy where a secondary container (sidecar) runs alongside the main application container (Grafana) in the same pod. The sidecar watches for ConfigMaps/Secrets and automatically provisions dashboards without requiring pod restarts.

**Architecture**:

```
┌─────────────────────────────────────┐
│         Grafana Pod                 │
├─────────────────────────────────────┤
│  ┌──────────────┐  ┌─────────────┐ │
│  │   Grafana    │  │  k8s-sidecar│ │
│  │  Container   │←─│  Container  │ │
│  │              │  │             │ │
│  │  :3000       │  │  Watches    │ │
│  │              │  │  ConfigMaps │ │
│  └──────────────┘  └─────────────┘ │
│         ↑                 ↑         │
│         └─────────────────┘         │
│           Shared Volume             │
│       /tmp/dashboards/              │
└─────────────────────────────────────┘
           ↑
           │ Watches for ConfigMaps
           │ with label selector
           │
    ┌──────┴──────┐
    │  ConfigMaps │
    │  (labeled)  │
    └─────────────┘
```

**Key Benefits**:

1. **Zero-downtime updates**: Dashboards update without pod restarts
2. **GitOps-friendly**: Dashboards stored as ConfigMaps in version control
3. **Declarative**: Infrastructure-as-code approach
4. **Auto-reload**: Changes detected and applied automatically

### Grafana 12.x Compatibility

**Schema Version**: 12.x uses **dashboard schema version 38+**

**Major Changes from v10.x**:

- AngularJS panels removed (deprecated in v10, removed in v11)
- Legacy alerting completely removed (unified alerting only)
- Panel type migrations required: `graph` → `timeseries`, `singlestat` → `stat`
- New plugin system (no more legacy plugin compatibility layer)

---

## 2. Core Frameworks: Sidecar Configuration

### 2.1 Sidecar Container Configuration Schema

**Image**: `quay.io/kiwigrid/k8s-sidecar:1.27.6` (latest stable as of 2025-10)

**Essential Environment Variables**:

| Variable                  | Purpose                           | Example Value         | Required                   |
| ------------------------- | --------------------------------- | --------------------- | -------------------------- |
| `LABEL`                   | ConfigMap label selector          | `grafana_dashboard`   | ✅ YES                     |
| `FOLDER`                  | Target directory in Grafana pod   | `/tmp/dashboards`     | ✅ YES                     |
| `METHOD`                  | Watch method (WATCH or SLEEP)     | `WATCH`               | ❌ No (default: WATCH)     |
| `NAMESPACE`               | Kubernetes namespace to watch     | `ALL` or `monitoring` | ❌ No (default: ALL)       |
| `RESOURCE`                | Resource type to watch            | `configmap`           | ❌ No (default: configmap) |
| `FOLDER_ANNOTATION`       | Annotation key for folder mapping | `grafana_folder`      | ❌ No                      |
| `SCRIPT`                  | Post-processing script path       | `/app/script.sh`      | ❌ No                      |
| `WATCH_SERVER_TIMEOUT`    | API server timeout (seconds)      | `60`                  | ❌ No                      |
| `UNIQUE_FILENAMES`        | Prevent filename collisions       | `true`                | ❌ No (recommended)        |
| `UPDATE_INTERVAL_SECONDS` | Poll interval (SLEEP mode only)   | `60`                  | ❌ No (WATCH mode only)    |

**Complete Sidecar Container Spec**:

```yaml
sidecarContainers:
  dashboards:
    enabled: true
    image: quay.io/kiwigrid/k8s-sidecar:1.27.6
    imagePullPolicy: IfNotPresent
    env:
      - name: LABEL
        value: 'grafana_dashboard'
      - name: FOLDER
        value: '/tmp/dashboards'
      - name: METHOD
        value: 'WATCH'
      - name: NAMESPACE
        value: 'ALL'
      - name: RESOURCE
        value: 'configmap'
      - name: FOLDER_ANNOTATION
        value: 'grafana_folder'
      - name: UNIQUE_FILENAMES
        value: 'true'
      - name: WATCH_SERVER_TIMEOUT
        value: '60'
    volumeMounts:
      - name: sc-dashboard-volume
        mountPath: '/tmp/dashboards'
    resources:
      requests:
        cpu: 50m
        memory: 64Mi
      limits:
        cpu: 100m
        memory: 128Mi
```

### 2.2 Label Selectors & Discovery

**How Sidecar Finds Dashboards**:

1. Watches Kubernetes API for ConfigMaps with matching label
2. Label key matches `LABEL` environment variable
3. Label value can be any string (typically `"1"` or `"true"`)

**Label Selector Examples**:

```yaml
# Simple label (most common)
labels:
  grafana_dashboard: "1"

# Multi-environment labeling
labels:
  grafana_dashboard: "production"
  environment: "prod"

# Team-based organization
labels:
  grafana_dashboard: "1"
  team: "platform"
  category: "infrastructure"
```

**Discovery Pattern**:

```
ConfigMap with label grafana_dashboard: "1"
    ↓
Sidecar detects via Kubernetes watch API
    ↓
Extracts dashboard JSON from ConfigMap data
    ↓
Writes to /tmp/dashboards/<filename>.json
    ↓
Grafana auto-detects via file provisioning
    ↓
Dashboard appears in UI
```

### 2.3 Folder Mapping Patterns

Grafana organizes dashboards into **folders** (logical groupings). Three methods to assign folders:

#### Method 1: Annotation-Based (Recommended)

**Use When**: You want ConfigMap-level control over folder placement

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: infrastructure-dashboard
  annotations:
    grafana_folder: 'Infrastructure' # ← Annotation key matches FOLDER_ANNOTATION env var
  labels:
    grafana_dashboard: '1'
data:
  dashboard.json: |-
    {
      "dashboard": { ... }
    }
```

**Result**: Dashboard appears in "Infrastructure" folder in Grafana UI

#### Method 2: Dashboard JSON `folderUid` (Explicit)

**Use When**: You want dashboard-level control and have pre-created folders

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: kubernetes-monitoring
  labels:
    grafana_dashboard: '1'
data:
  dashboard.json: |-
    {
      "dashboard": {
        "title": "Kubernetes Cluster Monitoring",
        "uid": "k8s-cluster-001",
        "folderUid": "infra-monitoring"  # ← Must match existing folder UID
      }
    }
```

**Result**: Dashboard appears in folder with UID "infra-monitoring"

**Prerequisites**: Folder must be pre-created (manually or via folder provisioning)

#### Method 3: File Structure (Path-Based)

**Use When**: Using Helm chart with nested directory structure

```
dashboards/
├── infrastructure/
│   └── nodes.json
├── applications/
│   └── api-metrics.json
└── monitoring/
    └── prometheus.json
```

**Grafana Helm Chart Configuration**:

```yaml
dashboardProviders:
  dashboardproviders.yaml:
    apiVersion: 1
    providers:
      - name: 'infrastructure'
        folder: 'Infrastructure'
        type: file
        options:
          path: /tmp/dashboards/infrastructure
      - name: 'applications'
        folder: 'Applications'
        type: file
        options:
          path: /tmp/dashboards/applications
```

**Decision Tree for Folder Mapping**:

```
Do you need dynamic folder creation?
├─ YES → Use annotation-based (grafana_folder)
└─ NO
   └─ Do you have pre-created folders with known UIDs?
      ├─ YES → Use folderUid in dashboard JSON
      └─ NO → Use file structure + dashboard providers
```

---

## 3. Processes & Workflows: ConfigMap Deployment

### 3.1 Six ConfigMap Examples (Production-Ready)

#### Example 1: Simple Single Dashboard (Minimal)

**Use Case**: Quick dashboard deployment with automatic folder creation

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: simple-dashboard
  namespace: monitoring
  labels:
    grafana_dashboard: '1'
  annotations:
    grafana_folder: 'General'
data:
  simple-dashboard.json: |-
    {
      "dashboard": {
        "title": "Simple CPU Monitoring",
        "uid": "simple-cpu-001",
        "tags": ["kubernetes", "cpu"],
        "timezone": "browser",
        "schemaVersion": 38,
        "version": 1,
        "panels": [
          {
            "id": 1,
            "type": "timeseries",
            "title": "CPU Usage",
            "targets": [
              {
                "expr": "rate(container_cpu_usage_seconds_total[5m])",
                "legendFormat": "{{pod}}"
              }
            ],
            "fieldConfig": {
              "defaults": {
                "unit": "percentunit"
              }
            }
          }
        ]
      }
    }
```

**Key Points**:

- `schemaVersion: 38` (Grafana 12.x compatibility)
- `grafana_folder` annotation creates "General" folder if missing
- Panel type `timeseries` (12.x standard, replaces legacy `graph`)

---

#### Example 2: Dashboard with `folderUid` (Explicit Folder Assignment)

**Use Case**: Place dashboard in pre-existing folder with known UID

**Prerequisites**: Folder with UID "platform-infra" must exist

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: node-exporter-dashboard
  namespace: monitoring
  labels:
    grafana_dashboard: '1'
    team: 'platform'
data:
  node-exporter.json: |-
    {
      "dashboard": {
        "title": "Node Exporter Full",
        "uid": "node-exporter-full",
        "folderUid": "platform-infra",
        "tags": ["prometheus", "node-exporter"],
        "schemaVersion": 38,
        "version": 2,
        "panels": [
          {
            "id": 1,
            "type": "timeseries",
            "title": "CPU Usage by Mode",
            "targets": [
              {
                "expr": "sum by (mode) (rate(node_cpu_seconds_total[5m]))",
                "legendFormat": "{{mode}}"
              }
            ]
          },
          {
            "id": 2,
            "type": "stat",
            "title": "Total Memory",
            "targets": [
              {
                "expr": "node_memory_MemTotal_bytes",
                "legendFormat": "Total"
              }
            ],
            "fieldConfig": {
              "defaults": {
                "unit": "bytes"
              }
            }
          }
        ]
      }
    }
```

**Key Points**:

- `folderUid: "platform-infra"` explicitly assigns folder
- No `grafana_folder` annotation (folderUid takes precedence)
- Uses both `timeseries` and `stat` panel types (12.x standard)

---

#### Example 3: Multi-Dashboard ConfigMap (Multiple Dashboards in One ConfigMap)

**Use Case**: Deploy related dashboards together (e.g., full observability stack)

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: observability-stack
  namespace: monitoring
  labels:
    grafana_dashboard: '1'
  annotations:
    grafana_folder: 'Observability'
data:
  prometheus-overview.json: |-
    {
      "dashboard": {
        "title": "Prometheus Overview",
        "uid": "prometheus-overview",
        "schemaVersion": 38,
        "panels": [ ... ]
      }
    }

  loki-logs.json: |-
    {
      "dashboard": {
        "title": "Loki Log Analytics",
        "uid": "loki-logs",
        "schemaVersion": 38,
        "panels": [ ... ]
      }
    }

  jaeger-tracing.json: |-
    {
      "dashboard": {
        "title": "Jaeger Distributed Tracing",
        "uid": "jaeger-tracing",
        "schemaVersion": 38,
        "panels": [ ... ]
      }
    }
```

**Key Points**:

- All dashboards share same folder ("Observability")
- Each dashboard has unique UID
- Single ConfigMap update triggers reload of all three dashboards
- Useful for atomic deployments (all-or-nothing updates)

---

#### Example 4: Timeseries Panel (Modern Visualization)

**Use Case**: Time-series metrics with modern panel features (12.x best practice)

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: timeseries-example
  namespace: monitoring
  labels:
    grafana_dashboard: '1'
  annotations:
    grafana_folder: 'Examples'
data:
  timeseries-demo.json: |-
    {
      "dashboard": {
        "title": "Timeseries Panel Examples",
        "uid": "timeseries-demo",
        "schemaVersion": 38,
        "panels": [
          {
            "id": 1,
            "type": "timeseries",
            "title": "Request Rate with Thresholds",
            "targets": [
              {
                "expr": "rate(http_requests_total[5m])",
                "legendFormat": "{{method}} {{status}}"
              }
            ],
            "fieldConfig": {
              "defaults": {
                "unit": "reqps",
                "thresholds": {
                  "mode": "absolute",
                  "steps": [
                    { "value": null, "color": "green" },
                    { "value": 100, "color": "yellow" },
                    { "value": 500, "color": "red" }
                  ]
                },
                "custom": {
                  "drawStyle": "line",
                  "lineInterpolation": "smooth",
                  "fillOpacity": 10,
                  "showPoints": "auto"
                }
              }
            },
            "options": {
              "legend": {
                "displayMode": "table",
                "placement": "bottom",
                "calcs": ["mean", "max", "last"]
              },
              "tooltip": {
                "mode": "multi",
                "sort": "desc"
              }
            }
          }
        ]
      }
    }
```

**Key Features**:

- **Thresholds**: Color-coded regions (green/yellow/red)
- **Custom drawing**: Smooth line interpolation, fill opacity
- **Legend configuration**: Table mode with calculations (mean, max, last)
- **Tooltip options**: Multi-series mode with descending sort
- **Units**: `reqps` (requests per second)

**Migration Note**: Replaces legacy `graph` panel type

---

#### Example 5: Stat Panel (Single Value Metrics)

**Use Case**: Display current value with threshold coloring (gauges, single stats)

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: stat-panel-example
  namespace: monitoring
  labels:
    grafana_dashboard: '1'
  annotations:
    grafana_folder: 'Examples'
data:
  stat-demo.json: |-
    {
      "dashboard": {
        "title": "Stat Panel Examples",
        "uid": "stat-demo",
        "schemaVersion": 38,
        "panels": [
          {
            "id": 1,
            "type": "stat",
            "title": "Current Active Users",
            "targets": [
              {
                "expr": "sum(active_users)",
                "legendFormat": ""
              }
            ],
            "fieldConfig": {
              "defaults": {
                "unit": "short",
                "thresholds": {
                  "mode": "absolute",
                  "steps": [
                    { "value": null, "color": "green" },
                    { "value": 1000, "color": "yellow" },
                    { "value": 5000, "color": "red" }
                  ]
                },
                "mappings": []
              }
            },
            "options": {
              "reduceOptions": {
                "values": false,
                "calcs": ["lastNotNull"]
              },
              "orientation": "auto",
              "textMode": "value_and_name",
              "colorMode": "background",
              "graphMode": "area",
              "justifyMode": "auto"
            }
          }
        ]
      }
    }
```

**Key Features**:

- **Reduce options**: `lastNotNull` (shows most recent non-null value)
- **Color mode**: `background` (colors entire panel background)
- **Graph mode**: `area` (shows sparkline graph behind value)
- **Text mode**: `value_and_name` (displays both metric name and value)

**Migration Note**: Replaces legacy `singlestat` panel type

---

#### Example 6: Secret-Based Dashboard (Sensitive Data)

**Use Case**: Store dashboard with sensitive query credentials in Kubernetes Secret

**Why Use Secrets**:

- Credentials embedded in dashboard JSON (e.g., API tokens, database passwords)
- Separate RBAC permissions for secrets vs configmaps
- Audit trail for sensitive dashboard access

**Sidecar Configuration Change**:

```yaml
sidecarContainers:
  dashboards:
    env:
      - name: RESOURCE
        value: 'both' # ← Watch both configmaps AND secrets
```

**Kubernetes Secret**:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: sensitive-dashboard
  namespace: monitoring
  labels:
    grafana_dashboard: '1'
  annotations:
    grafana_folder: 'Restricted'
type: Opaque
stringData:
  db-metrics.json: |-
    {
      "dashboard": {
        "title": "Database Metrics (Sensitive)",
        "uid": "db-metrics-sensitive",
        "schemaVersion": 38,
        "panels": [
          {
            "id": 1,
            "type": "timeseries",
            "title": "Query Performance",
            "targets": [
              {
                "datasource": "PostgreSQL",
                "rawSql": "SELECT time, query_duration FROM metrics WHERE api_key = 'REDACTED'"
              }
            ]
          }
        ]
      }
    }
```

**Key Points**:

- Use `Secret` instead of `ConfigMap`
- Same label selector (`grafana_dashboard: "1"`)
- Sidecar `RESOURCE` must be `both` or `secret`
- `stringData` automatically base64-encodes on creation
- Use `grafana_folder: "Restricted"` to isolate sensitive dashboards

**Security Best Practices**:

- Never commit secrets to Git (use sealed-secrets or external-secrets-operator)
- Restrict RBAC: only authorized users can view secrets
- Use folder permissions in Grafana to limit dashboard access

---

### 3.2 Auto-Reload Mechanics

#### WATCH Method (Recommended - Default)

**How It Works**:

1. Sidecar opens persistent watch connection to Kubernetes API
2. API server sends events when ConfigMaps/Secrets change
3. Sidecar receives event instantly (sub-second latency)
4. Extracts dashboard JSON and writes to `/tmp/dashboards/`
5. Grafana detects file change via inotify (Linux kernel feature)
6. Dashboard reloads in UI automatically

**Configuration**:

```yaml
env:
  - name: METHOD
    value: 'WATCH'
  - name: WATCH_SERVER_TIMEOUT
    value: '60' # Reconnect if no events for 60 seconds
```

**Advantages**:

- Near-instant updates (<5 seconds from ConfigMap apply to UI)
- Efficient (no polling overhead)
- Kubernetes-native event stream

**Disadvantages**:

- Watch connections can timeout (requires reconnection logic)
- API server load increases with many watchers

**Event Flow**:

```
kubectl apply -f dashboard-configmap.yaml
    ↓
Kubernetes API creates/updates ConfigMap
    ↓
API server sends MODIFIED event to sidecar watch stream
    ↓ (< 1 second)
Sidecar writes updated JSON to /tmp/dashboards/my-dashboard.json
    ↓ (< 1 second)
Grafana inotify detects file change
    ↓ (< 3 seconds)
Grafana reloads dashboard from file
    ↓
UI shows updated dashboard
```

**Total latency**: Typically 3-5 seconds

---

#### SLEEP Method (Polling - Fallback)

**How It Works**:

1. Sidecar lists all ConfigMaps/Secrets with matching label
2. Compares against cached state
3. Updates files if changes detected
4. Sleeps for `UPDATE_INTERVAL_SECONDS`
5. Repeats from step 1

**Configuration**:

```yaml
env:
  - name: METHOD
    value: 'SLEEP'
  - name: UPDATE_INTERVAL_SECONDS
    value: '60' # Poll every 60 seconds
```

**Advantages**:

- Simpler logic (no watch reconnection handling)
- Predictable resource usage

**Disadvantages**:

- Delayed updates (up to `UPDATE_INTERVAL_SECONDS`)
- Higher API server load (periodic LIST operations)
- Less efficient than WATCH

**When to Use**:

- Legacy Kubernetes clusters with unreliable watch APIs
- Air-gapped environments with proxy issues
- Testing/development (easier to reason about)

---

### 3.3 Complete Deployment Workflow

**Step-by-Step Production Deployment**:

```bash
# 1. Create namespace
kubectl create namespace monitoring

# 2. Deploy Grafana with sidecar (Helm chart)
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

helm install grafana grafana/grafana \
  --namespace monitoring \
  --set sidecar.dashboards.enabled=true \
  --set sidecar.dashboards.label=grafana_dashboard \
  --set sidecar.dashboards.folder=/tmp/dashboards \
  --set sidecar.dashboards.folderAnnotation=grafana_folder

# 3. Wait for Grafana pod to be ready
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=grafana -n monitoring --timeout=300s

# 4. Apply dashboard ConfigMaps
kubectl apply -f dashboard-configmaps/ -n monitoring

# 5. Verify sidecar detected dashboards
kubectl logs -n monitoring -l app.kubernetes.io/name=grafana -c k8s-sidecar --tail=20

# Expected output:
# INFO: Detected new ConfigMap: simple-dashboard
# INFO: Writing dashboard to /tmp/dashboards/simple-dashboard.json
# INFO: Dashboard provisioned successfully

# 6. Access Grafana UI
kubectl port-forward -n monitoring svc/grafana 3000:80

# 7. Verify dashboards in UI
# Navigate to http://localhost:3000 → Dashboards → Browse
# Should see dashboards in configured folders
```

**Verification Checklist**:

- [ ] Sidecar container running (check pod status)
- [ ] ConfigMaps have correct label (`grafana_dashboard: "1"`)
- [ ] Sidecar logs show "Dashboard provisioned successfully"
- [ ] Grafana UI shows dashboards in correct folders
- [ ] Dashboard UID matches ConfigMap (no duplicates)

---

## 4. Decision Trees: Folder Mapping & Migration

### 4.1 Folder Mapping Selection Decision Tree

```
START: Where should this dashboard appear in Grafana?
│
├─ Do you need to create a NEW folder dynamically?
│  ├─ YES → Use annotation-based mapping
│  │        ├─ Add to ConfigMap metadata:
│  │        │   annotations:
│  │        │     grafana_folder: "Your Folder Name"
│  │        └─ Grafana creates folder if missing
│  │
│  └─ NO (folder already exists)
│     │
│     ├─ Do you know the folder UID?
│     │  ├─ YES → Use folderUid in dashboard JSON
│     │  │        └─ Add to dashboard object:
│     │  │            "folderUid": "existing-folder-uid"
│     │  │
│     │  └─ NO (only know folder name)
│     │     │
│     │     ├─ Can you restructure ConfigMaps by directory?
│     │     │  ├─ YES → Use file structure method
│     │     │  │        └─ Configure dashboard providers with path mapping
│     │     │  │
│     │     │  └─ NO → Use annotation-based (simplest)
│     │     │           └─ grafana_folder annotation with folder name
│     │     │
│     │     └─ RECOMMENDATION: Query folder UID and use folderUid method
│     │                        (most explicit, prevents folder duplication)
```

**Folder UID Query** (if needed):

```bash
# Get folder UID from Grafana API
curl -s -H "Authorization: Bearer ${GRAFANA_API_TOKEN}" \
  http://grafana:3000/api/folders | jq -r '.[] | "\(.title): \(.uid)"'

# Example output:
# Infrastructure: infra-uid-123
# Applications: apps-uid-456
```

---

### 4.2 Grafana v10 → v11 Migration Path

**Critical Breaking Changes**:

| Component                | v10 Behavior           | v11 Behavior      | Migration Action            |
| ------------------------ | ---------------------- | ----------------- | --------------------------- |
| **Schema Version**       | 36-37                  | 38+               | Update `schemaVersion: 38`  |
| **graph panel**          | Supported (deprecated) | Removed           | Replace with `timeseries`   |
| **singlestat panel**     | Supported (deprecated) | Removed           | Replace with `stat`         |
| **AngularJS panels**     | Deprecated             | Removed           | Rewrite with React panels   |
| **Legacy alerting**      | Supported              | Removed           | Migrate to unified alerting |
| **Plugin compatibility** | Legacy bridge exists   | No legacy support | Update all plugins          |

---

#### Step 1: Pre-Migration Inventory

**Identify Panels Requiring Updates**:

```bash
# Find all dashboards using legacy panel types
kubectl get configmaps -n monitoring -l grafana_dashboard=1 -o json | \
  jq -r '.items[] |
    .metadata.name as $name |
    .data[] |
    fromjson |
    .dashboard.panels[]? |
    select(.type == "graph" or .type == "singlestat") |
    "\($name): Panel \(.id) - Type: \(.type)"'

# Example output:
# node-exporter-dashboard: Panel 1 - Type: graph
# node-exporter-dashboard: Panel 5 - Type: singlestat
# app-metrics: Panel 2 - Type: graph
```

**Check Schema Versions**:

```bash
kubectl get configmaps -n monitoring -l grafana_dashboard=1 -o json | \
  jq -r '.items[] |
    "\(.metadata.name): schemaVersion \(.data | to_entries[0].value | fromjson | .dashboard.schemaVersion)"'

# Example output:
# node-exporter-dashboard: schemaVersion 36
# app-metrics: schemaVersion 37
```

---

#### Step 2: Panel Type Migrations

**graph → timeseries Migration**:

**Before (v10 graph panel)**:

```json
{
  "id": 1,
  "type": "graph",
  "title": "CPU Usage",
  "targets": [
    {
      "expr": "rate(cpu_usage[5m])",
      "legendFormat": "{{instance}}"
    }
  ],
  "lines": true,
  "linewidth": 2,
  "fill": 1,
  "legend": {
    "show": true,
    "alignAsTable": true,
    "avg": true,
    "max": true
  },
  "yaxes": [
    {
      "label": "CPU %",
      "format": "percent"
    }
  ]
}
```

**After (v11 timeseries panel)**:

```json
{
  "id": 1,
  "type": "timeseries",
  "title": "CPU Usage",
  "targets": [
    {
      "expr": "rate(cpu_usage[5m])",
      "legendFormat": "{{instance}}"
    }
  ],
  "fieldConfig": {
    "defaults": {
      "unit": "percent",
      "custom": {
        "drawStyle": "line",
        "lineWidth": 2,
        "fillOpacity": 10
      }
    }
  },
  "options": {
    "legend": {
      "displayMode": "table",
      "placement": "bottom",
      "calcs": ["mean", "max"]
    }
  }
}
```

**Key Mapping**:

- `lines: true` → `custom.drawStyle: "line"`
- `linewidth: 2` → `custom.lineWidth: 2`
- `fill: 1` → `custom.fillOpacity: 10` (0-100 scale)
- `legend.alignAsTable` → `options.legend.displayMode: "table"`
- `yaxes[0].format` → `fieldConfig.defaults.unit`

---

**singlestat → stat Migration**:

**Before (v10 singlestat panel)**:

```json
{
  "id": 2,
  "type": "singlestat",
  "title": "Total Requests",
  "targets": [
    {
      "expr": "sum(http_requests_total)"
    }
  ],
  "format": "short",
  "valueName": "current",
  "sparkline": {
    "show": true,
    "full": false
  },
  "gauge": {
    "show": false
  },
  "thresholds": "1000,5000",
  "colors": ["green", "yellow", "red"]
}
```

**After (v11 stat panel)**:

```json
{
  "id": 2,
  "type": "stat",
  "title": "Total Requests",
  "targets": [
    {
      "expr": "sum(http_requests_total)"
    }
  ],
  "fieldConfig": {
    "defaults": {
      "unit": "short",
      "thresholds": {
        "mode": "absolute",
        "steps": [
          { "value": null, "color": "green" },
          { "value": 1000, "color": "yellow" },
          { "value": 5000, "color": "red" }
        ]
      }
    }
  },
  "options": {
    "reduceOptions": {
      "values": false,
      "calcs": ["lastNotNull"]
    },
    "graphMode": "area",
    "colorMode": "value"
  }
}
```

**Key Mapping**:

- `format: "short"` → `fieldConfig.defaults.unit: "short"`
- `valueName: "current"` → `options.reduceOptions.calcs: ["lastNotNull"]`
- `sparkline.show: true` → `options.graphMode: "area"`
- `thresholds: "1000,5000"` → `thresholds.steps` array
- `colors` array → `thresholds.steps[].color`

---

#### Step 3: Schema Version Update

**Update All Dashboards**:

```json
{
  "dashboard": {
    "schemaVersion": 38,  // ← Change from 36/37
    ...
  }
}
```

**Automated Update Script** (Python):

```python
import json
import yaml
from pathlib import Path

def migrate_dashboard(dashboard_json):
    """Migrate dashboard to v11 schema"""
    dashboard = json.loads(dashboard_json)

    # Update schema version
    dashboard['dashboard']['schemaVersion'] = 38

    # Migrate panels
    for panel in dashboard['dashboard'].get('panels', []):
        if panel['type'] == 'graph':
            panel['type'] = 'timeseries'
            # ... additional graph → timeseries transformations
        elif panel['type'] == 'singlestat':
            panel['type'] = 'stat'
            # ... additional singlestat → stat transformations

    return json.dumps(dashboard, indent=2)

# Process all ConfigMaps
for configmap_file in Path('dashboard-configmaps/').glob('*.yaml'):
    with open(configmap_file) as f:
        configmap = yaml.safe_load(f)

    for key, dashboard_json in configmap['data'].items():
        migrated = migrate_dashboard(dashboard_json)
        configmap['data'][key] = migrated

    with open(configmap_file, 'w') as f:
        yaml.dump(configmap, f)
```

---

#### Step 4: Validation Checklist

**Before Applying Migrated Dashboards**:

- [ ] All `graph` panels replaced with `timeseries`
- [ ] All `singlestat` panels replaced with `stat`
- [ ] Schema version updated to 38+
- [ ] Panel IDs remain unchanged (preserves links)
- [ ] Dashboard UIDs unchanged (preserves URLs)
- [ ] Thresholds converted to new format
- [ ] Legend configuration migrated
- [ ] Units/formats preserved
- [ ] No AngularJS plugins referenced

**Validation Command**:

```bash
# Check for legacy panel types
kubectl get configmaps -n monitoring -l grafana_dashboard=1 -o json | \
  jq -r '.items[].data[] | fromjson | .dashboard.panels[]? |
    select(.type == "graph" or .type == "singlestat" or .type == "table-old") |
    "❌ LEGACY PANEL FOUND: \(.type)"' || echo "✅ No legacy panels detected"
```

---

#### Step 5: Rollout Strategy

**Blue-Green Deployment** (Recommended for Production):

```bash
# 1. Deploy migrated dashboards to new folder
kubectl apply -f migrated-dashboards/ -n monitoring
# (All have grafana_folder: "V11 Migrated" annotation)

# 2. Test in Grafana UI
# Navigate to "V11 Migrated" folder
# Verify all panels render correctly
# Check query performance

# 3. If successful, update production dashboards
kubectl apply -f migrated-dashboards/ -n monitoring
# (Change grafana_folder annotations to production folders)

# 4. Delete old v10 dashboards
kubectl delete configmap old-dashboard-v10 -n monitoring
```

**Canary Rollout** (For Large Deployments):

```bash
# 1. Migrate 10% of dashboards
# 2. Monitor for errors (check Grafana logs)
# 3. Gradual rollout: 25% → 50% → 100%
```

---

## 5. Anti-Patterns: Common Mistakes

### 5.1 Missing Labels

**❌ WRONG - No label selector**:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: my-dashboard
  # Missing labels section!
data:
  dashboard.json: '...'
```

**Result**: Sidecar never detects ConfigMap (no matching label)

**✅ CORRECT**:

```yaml
metadata:
  labels:
    grafana_dashboard: '1' # ← Must match sidecar LABEL env var
```

---

### 5.2 Incorrect folderUid

**❌ WRONG - Non-existent folder UID**:

```json
{
  "dashboard": {
    "folderUid": "my-folder-123" // Folder doesn't exist
  }
}
```

**Result**: Grafana creates dashboard in "General" folder (fallback)

**✅ CORRECT - Verify folder exists first**:

```bash
# Query existing folders
curl -H "Authorization: Bearer $TOKEN" http://grafana:3000/api/folders | jq '.[].uid'

# Use valid UID
"folderUid": "verified-folder-uid"
```

**Alternative**: Use `grafana_folder` annotation (auto-creates folder)

---

### 5.3 Schema Version Mismatch

**❌ WRONG - Old schema version**:

```json
{
  "dashboard": {
    "schemaVersion": 16 // ← Very old version (Grafana v5.x)
  }
}
```

**Result**: Panels may not render, features broken, errors in logs

**✅ CORRECT - Use current version**:

```json
{
  "dashboard": {
    "schemaVersion": 38 // Grafana 12.x
  }
}
```

**How to Check Current Version**:

1. Create dashboard in Grafana UI
2. Export as JSON
3. Check `schemaVersion` field

---

### 5.4 Duplicate Dashboard UIDs

**❌ WRONG - Same UID in multiple ConfigMaps**:

```yaml
# configmap-1.yaml
data:
  dashboard.json: '{"dashboard": {"uid": "my-dash"}}'

# configmap-2.yaml
data:
  dashboard.json: '{"dashboard": {"uid": "my-dash"}}'  # ← DUPLICATE!
```

**Result**: Last-write-wins (one dashboard overwrites the other)

**✅ CORRECT - Unique UIDs**:

```yaml
# configmap-1.yaml
data:
  dashboard.json: '{"dashboard": {"uid": "my-dash-v1"}}'

# configmap-2.yaml
data:
  dashboard.json: '{"dashboard": {"uid": "my-dash-v2"}}'
```

**UID Naming Convention**:

- `<team>-<component>-<version>`: `platform-k8s-001`
- `<env>-<service>-<view>`: `prod-api-latency`

---

### 5.5 Incorrect JSON Encoding in YAML

**❌ WRONG - Unescaped quotes**:

```yaml
data:
  dashboard.json: "{"dashboard": {"title": "My Dashboard"}}"  # ← Syntax error!
```

**Result**: YAML parsing fails, ConfigMap not created

**✅ CORRECT - Use literal block scalar**:

```yaml
data:
  dashboard.json: |-
    {
      "dashboard": {
        "title": "My Dashboard"
      }
    }
```

**Alternative - Escaped quotes**:

```yaml
data:
  dashboard.json: '{"dashboard": {"title": "My Dashboard"}}'
```

---

### 5.6 Sidecar Resource Limits Too Low

**❌ WRONG - Insufficient resources**:

```yaml
resources:
  limits:
    cpu: 10m # ← Too low for watching many ConfigMaps
    memory: 16Mi # ← Insufficient for JSON parsing
```

**Result**: Sidecar OOMKilled or CPU throttled, dashboards not updated

**✅ CORRECT - Production-grade limits**:

```yaml
resources:
  requests:
    cpu: 50m
    memory: 64Mi
  limits:
    cpu: 100m
    memory: 128Mi
```

**Scaling Guide**:

- <10 dashboards: 50m CPU, 64Mi memory
- 10-50 dashboards: 100m CPU, 128Mi memory
- 50-200 dashboards: 200m CPU, 256Mi memory
- 200+ dashboards: 500m CPU, 512Mi memory

---

## 6. Integration Points: deployment-release Agent Handoff

### 6.1 Agent Responsibilities

**grafana-dashboard-builder Agent**:

- Generate dashboard JSON from requirements
- Ensure schema version compatibility (v38+)
- Apply panel type best practices (timeseries, stat)
- Validate JSON syntax and structure
- Output ConfigMap YAML with proper labels/annotations

**deployment-release Agent**:

- Apply ConfigMap to Kubernetes cluster
- Verify sidecar detected dashboard (check logs)
- Troubleshoot deployment issues (RBAC, network)
- Monitor sidecar resource usage
- Handle Grafana Helm chart upgrades

### 6.2 Handoff Protocol

**grafana-dashboard-builder Outputs**:

```yaml
# Output file: dashboards/my-dashboard.configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: my-dashboard
  namespace: monitoring # ← deployment-release uses this
  labels:
    grafana_dashboard: '1'
  annotations:
    grafana_folder: 'Production'
data:
  my-dashboard.json: |-
    {
      "dashboard": {
        "title": "My Dashboard",
        "uid": "my-dash-001",
        "schemaVersion": 38,
        ...
      }
    }
```

**deployment-release Consumes**:

```bash
# 1. Validate ConfigMap syntax
kubectl apply --dry-run=client -f dashboards/my-dashboard.configmap.yaml

# 2. Apply to cluster
kubectl apply -f dashboards/my-dashboard.configmap.yaml -n monitoring

# 3. Verify sidecar detection
kubectl logs -n monitoring -l app.kubernetes.io/name=grafana -c k8s-sidecar --tail=10

# Expected: "INFO: Detected new ConfigMap: my-dashboard"
```

### 6.3 Error Handling & Escalation

**grafana-dashboard-builder Errors**:

- Invalid JSON syntax → Fix and regenerate
- Missing required fields (title, uid) → Add defaults
- Unsupported panel type → Migrate to v11 equivalent

**deployment-release Errors**:

- RBAC permission denied → Check ServiceAccount permissions
- Sidecar not detecting → Verify label selector matches
- Dashboard not appearing → Check Grafana logs for import errors

**Escalation Path**:

```
grafana-dashboard-builder generates invalid JSON
    ↓
deployment-release kubectl apply fails
    ↓
deployment-release reports syntax error to orchestrator
    ↓
Orchestrator delegates back to grafana-dashboard-builder
    ↓
grafana-dashboard-builder fixes JSON, outputs new ConfigMap
    ↓
deployment-release retries apply
    ↓
SUCCESS
```

---

## 7. Reference: Complete Sidecar Configuration

**Production-Ready Grafana Helm Values** (`values.yaml`):

```yaml
# Grafana Helm Chart - Sidecar Configuration
grafana:
  # Enable sidecar container
  sidecar:
    dashboards:
      enabled: true
      image:
        repository: quay.io/kiwigrid/k8s-sidecar
        tag: 1.27.6

      # Discovery configuration
      label: grafana_dashboard
      labelValue: '' # Any value (empty string matches all)
      folder: /tmp/dashboards
      folderAnnotation: grafana_folder

      # Watch configuration
      resource: both # Watch configmaps AND secrets
      watchMethod: WATCH
      watchServerTimeout: 60

      # Namespace scope
      namespace: ALL # Watch all namespaces

      # File handling
      uniqueFilenames: true

      # Resource limits
      resources:
        requests:
          cpu: 50m
          memory: 64Mi
        limits:
          cpu: 100m
          memory: 128Mi

  # Dashboard provisioning config
  dashboardProviders:
    dashboardproviders.yaml:
      apiVersion: 1
      providers:
        - name: sidecar
          orgId: 1
          folder: '' # Empty = use folder from ConfigMap annotation
          type: file
          disableDeletion: false
          editable: true
          options:
            path: /tmp/dashboards

  # Enable persistence for dashboard edits
  persistence:
    enabled: true
    storageClassName: standard
    size: 10Gi
```

**Deploy Command**:

```bash
helm install grafana grafana/grafana \
  --namespace monitoring \
  --create-namespace \
  --values values.yaml
```

---

## 8. Troubleshooting Guide

### Issue: Dashboard Not Appearing in UI

**Diagnosis Steps**:

```bash
# 1. Verify ConfigMap exists with correct label
kubectl get configmap -n monitoring -l grafana_dashboard=1

# 2. Check sidecar logs
kubectl logs -n monitoring -l app.kubernetes.io/name=grafana -c k8s-sidecar --tail=50

# 3. Verify file was written
kubectl exec -n monitoring -c grafana $(kubectl get pod -n monitoring -l app.kubernetes.io/name=grafana -o name) -- ls -la /tmp/dashboards/

# 4. Check Grafana logs for import errors
kubectl logs -n monitoring -l app.kubernetes.io/name=grafana -c grafana --tail=50 | grep -i dashboard
```

**Common Causes**:

- Label mismatch (sidecar `LABEL` env var ≠ ConfigMap label)
- Invalid JSON syntax (check sidecar logs for parse errors)
- Folder UID doesn't exist (dashboard falls back to "General")
- Schema version too old (Grafana rejects incompatible versions)

---

### Issue: Sidecar Not Detecting ConfigMap Changes

**Diagnosis**:

```bash
# Check sidecar is running
kubectl get pod -n monitoring -l app.kubernetes.io/name=grafana -o jsonpath='{.items[0].spec.containers[*].name}'
# Expected: grafana k8s-sidecar

# Verify WATCH method
kubectl get pod -n monitoring -l app.kubernetes.io/name=grafana -o jsonpath='{.items[0].spec.containers[?(@.name=="k8s-sidecar")].env[?(@.name=="METHOD")].value}'
# Expected: WATCH

# Check for watch connection errors
kubectl logs -n monitoring -l app.kubernetes.io/name=grafana -c k8s-sidecar | grep -i error
```

**Solutions**:

- Restart sidecar: `kubectl rollout restart deployment grafana -n monitoring`
- Switch to SLEEP method (less efficient but more reliable)
- Check RBAC: sidecar ServiceAccount needs `get`, `list`, `watch` on ConfigMaps

---

### Issue: Dashboard Appears in Wrong Folder

**Diagnosis**:

```bash
# Check folder annotation
kubectl get configmap my-dashboard -n monitoring -o jsonpath='{.metadata.annotations.grafana_folder}'

# Check folderUid in dashboard JSON
kubectl get configmap my-dashboard -n monitoring -o jsonpath='{.data.dashboard\.json}' | jq -r '.dashboard.folderUid'
```

**Priority Order** (Grafana uses first match):

1. `folderUid` in dashboard JSON (highest priority)
2. `grafana_folder` annotation on ConfigMap
3. Dashboard provider `folder` configuration
4. "General" folder (default fallback)

**Fix**:

- Remove `folderUid` from dashboard JSON if using annotations
- Verify annotation key matches sidecar `FOLDER_ANNOTATION` env var
- Ensure folder exists if using `folderUid`

---

## 9. Best Practices Summary

**ConfigMap Organization**:

- ✅ One dashboard per ConfigMap key (easier updates)
- ✅ Group related dashboards in single ConfigMap (atomic deploys)
- ✅ Use descriptive ConfigMap names (`team-component-dashboard`)
- ❌ Don't mix test and production dashboards in same ConfigMap

**Folder Management**:

- ✅ Use annotation-based for dynamic folder creation
- ✅ Use folderUid for guaranteed folder assignment
- ✅ Document folder UID mapping in team wiki
- ❌ Don't hardcode folder names without annotation/UID

**Schema Version**:

- ✅ Always use latest stable schema version (38+ for 12.x)
- ✅ Test in Grafana UI before provisioning
- ✅ Export from UI to get correct schema
- ❌ Don't copy old dashboard JSON without migration

**Security**:

- ✅ Use Secrets for dashboards with embedded credentials
- ✅ Restrict RBAC on sensitive dashboard ConfigMaps
- ✅ Use folder permissions in Grafana for access control
- ❌ Don't commit API keys or tokens to Git

**Resource Limits**:

- ✅ Size sidecar resources based on dashboard count
- ✅ Monitor sidecar CPU/memory usage (Prometheus metrics)
- ✅ Use `WATCH` method for production (more efficient)
- ❌ Don't starve sidecar resources (causes missed updates)

---

## 10. Additional Resources

**Official Documentation**:

- [Grafana Helm Chart](https://github.com/grafana/helm-charts/tree/main/charts/grafana)
- [k8s-sidecar Repository](https://github.com/kiwigrid/k8s-sidecar)
- [Grafana 12.x Release Notes](https://grafana.com/docs/grafana/latest/whatsnew/)
- [Dashboard Schema Documentation](https://grafana.com/docs/grafana/latest/dashboards/build-dashboards/view-dashboard-json-model/)

**Migration Guides**:

- [Grafana v10 → v11 Breaking Changes](https://grafana.com/docs/grafana/latest/breaking-changes/breaking-changes-v11-0/)
- [Panel Type Migration Guide](https://grafana.com/docs/grafana/latest/panels-visualizations/)

**Community Examples**:

- [Kubernetes Monitoring Dashboards](https://github.com/kubernetes-monitoring/kubernetes-mixin)
- [Prometheus Community Dashboards](https://github.com/prometheus-operator/kube-prometheus/tree/main/manifests)

---

**Document Version**: 1.0.0
**Last Validated**: 2025-10-30
**Grafana Compatibility**: v11.0 - v11.3+
**k8s-sidecar Version**: 1.27.6
