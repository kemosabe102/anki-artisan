# deployment-release Agent Handoff Protocol for grafana-dashboard-builder

**Purpose**: AI-readable integration protocol for delegating Grafana dashboard deployment operations from grafana-dashboard-builder to deployment-release agent.

**Audience**:

- **grafana-dashboard-builder agent** - Primary consumer for delegation decisions

- **Orchestrator** - Coordination and workflow management

- **deployment-release agent** - Target agent for deployment operations

**Version**: 1.0 (2025-10-30)

**Version Compatibility**: See [README.md](./README.md#version-compatibility) for Grafana 12.x, Prometheus 3.x, and Jaeger 2.x compatibility details.

---

## 1. Overview: Integration Protocol

### Delegation Flow

```

grafana-dashboard-builder (JSON generation)

  → Orchestrator (coordination)

    → deployment-release (ConfigMap deployment + pod restart)

      → Verification (4 kubectl checks)

        → SUCCESS/FAILURE response

```

### Division of Responsibilities

**grafana-dashboard-builder Domain**:

- Grafana dashboard JSON generation (panel layout, queries, variables)

- Dashboard validation (schema compliance, query syntax)

- Integration with observability stack (Prometheus data sources, Jaeger queries)

- Dashboard content creation (metrics, traces, logs)

**deployment-release Domain**:

- Kubernetes manifest editing (ConfigMap YAML)

- Deployment script orchestration (`bash scripts/deployment/deploy-local-k8s.sh`)

- Pod lifecycle management (rollout restart for ConfigMap updates)

- Infrastructure verification (kubectl status checks)

- Rollback execution (if deployment fails)

**Handoff Boundary**: JSON dashboard content (grafana-dashboard-builder) → ConfigMap deployment (deployment-release)

---

## 2. Core Frameworks

### Framework 1: deployment-release Operation Types

deployment-release supports 6 operation types:

| Operation | Purpose | When to Use | Example Task |

|-----------|---------|-------------|--------------|

| **deploy** | Full stack deployment | Initial setup, major changes | Deploy observability stack with Grafana |

| **config_update** | ConfigMap/Secret updates | Dashboard updates, config changes | Update grafana-dashboards ConfigMap |

| **validate** | Pre-deployment validation | Before applying changes | Validate manifest syntax |

| **troubleshoot** | Failure diagnosis | Pod crashes, deployment issues | Debug CrashLoopBackOff |

| **rollback** | Revert to previous version | Deployment failures | Rollback to previous ConfigMap |

| **rollout** | Monitor deployment progress | Track rollout status | Check deployment rollout status |

**Delegation Decision Tree**:

```

Dashboard JSON ready?

├─ YES → Existing deployment?

│  ├─ YES → Use config_update (update ConfigMap only)

│  └─ NO → Use deploy (full stack deployment)

└─ NO → grafana-dashboard-builder completes generation first

```

### Framework 2: Input Contract Schema

deployment-release expects structured JSON input via Task delegation:

#### config_update Operation (Most Common for Dashboards)

```json
{
  "operation_type": "config_update",

  "context": "Update Grafana dashboard ConfigMap with new dashboard JSON",

  "config_update": {
    "config_type": "configmap",

    "config_name": "grafana-dashboards",

    "namespace": "gauntlet-agents",

    "data": {
      "dashboard-name.json": "<dashboard_json_content>"
    },

    "immutability_enforcement": true
  },

  "validation": {
    "mode": "standard",

    "diff": true
  },

  "restart_pods": true,

  "pod_selector": "app=grafana"
}
```

**Key Parameters**:

- `config_type`: Always "configmap" for dashboard updates

- `config_name`: ConfigMap name (typically "grafana-dashboards")

- `namespace`: Kubernetes namespace (typically "gauntlet-agents")

- `data`: Key-value map of dashboard filename → JSON content

- `immutability_enforcement`: Always `true` (Kubernetes best practice)

- `restart_pods`: Always `true` (ConfigMaps don't hot-reload)

- `pod_selector`: Label selector for Grafana pods

#### deploy Operation (Full Stack)

```json
{
  "operation_type": "deploy",

  "context": "Deploy Grafana with observability stack",

  "deployment_target": {
    "cluster_context": "local",

    "namespace": "gauntlet-agents",

    "manifest_path": "k8s/local"
  },

  "validation": {
    "mode": "full",

    "secrets_check": true,

    "observability_check": true
  }
}
```

**Key Parameters**:

- `cluster_context`: Kubernetes context (always "local" for dev)

- `manifest_path`: Directory with kustomization.yaml

- `validation.mode`: "quick"/"standard"/"full" (use "full" for initial deployments)

- `secrets_check`: Verify required secrets exist

- `observability_check`: Run verify_observability.py after deployment

### Framework 3: Delegation Patterns

#### Pattern 1: Dashboard Update (Existing Deployment)

**Scenario**: Update dashboard JSON in existing Grafana deployment

**Steps**:

1. grafana-dashboard-builder generates dashboard JSON

2. Orchestrator delegates to deployment-release with `config_update` operation

3. deployment-release edits ConfigMap YAML (adds/updates dashboard JSON)

4. deployment-release validates manifest (`--mode=standard`)

5. deployment-release applies changes via deployment script

6. deployment-release restarts Grafana pods (`kubectl rollout restart`)

7. deployment-release verifies pod status and dashboard accessibility

**Task Invocation**:

```python

Task(

  agent="deployment-release",

  prompt="""UPDATE grafana-dashboards ConfigMap with new dashboard JSON.



Operation: config_update

ConfigMap: grafana-dashboards

Namespace: gauntlet-agents

Dashboard JSON:

{dashboard_json}



Validation: Run standard validation before applying

Restart: Trigger Grafana pod restart after update

Verification: Check pod readiness and dashboard endpoint"""

)

```

#### Pattern 2: Initial Deployment (New Stack)

**Scenario**: Deploy Grafana as part of observability stack

**Steps**:

1. grafana-dashboard-builder generates initial dashboard set

2. Orchestrator delegates to deployment-release with `deploy` operation

3. deployment-release runs full deployment pipeline:
   - Secret setup (`bash scripts/deployment/setup-k8s-secrets.sh`)

   - Manifest application (`bash scripts/deployment/deploy-local-k8s.sh`)

   - Rollout monitoring

   - Health checks

   - Observability verification (`verify_observability.py`)

4. deployment-release returns deployment evidence

**Task Invocation**:

```python

Task(

  agent="deployment-release",

  prompt="""DEPLOY Grafana with observability stack (Prometheus, Jaeger, OTEL Collector).



Operation: deploy

Namespace: gauntlet-agents

Manifests: k8s/local

Validation: Full validation (client + server + kustomize)

Checks: Secrets, health, observability endpoints

Dashboards: Will be added post-deployment via config_update"""

)

```

#### Pattern 3: Deployment Failure Recovery

**Scenario**: Dashboard update causes pod crash or deployment failure

**Steps**:

1. deployment-release detects failure (pod CrashLoopBackOff, validation error)

2. deployment-release attempts rollback (`kubectl rollout undo`)

3. deployment-release verifies rollback success

4. deployment-release returns FAILURE with diagnostics

5. Orchestrator reports to grafana-dashboard-builder for JSON correction

6. Retry with corrected dashboard JSON

**Task Invocation** (after failure):

```python

Task(

  agent="deployment-release",

  prompt="""ROLLBACK grafana deployment to previous revision.



Operation: rollback

Deployment: grafana

Namespace: gauntlet-agents

Reason: Dashboard JSON caused pod crash

Target Revision: Previous (automatic detection)

Verification: Check pod health after rollback"""

)

```

---

## 3. Processes & Workflows

### Workflow 1: Standard Dashboard Update

**Pre-Conditions**:

- Grafana deployment exists in cluster

- grafana-dashboards ConfigMap exists

- Dashboard JSON validated by grafana-dashboard-builder

**Execution Flow**:

```

1. grafana-dashboard-builder Phase:

   ├─ Generate dashboard JSON (panels, queries, variables)

   ├─ Validate JSON schema

   ├─ Validate query syntax

   └─ Return SUCCESS with dashboard JSON



2. Orchestrator Phase:

   ├─ Receive dashboard JSON

   ├─ Construct deployment-release Task (config_update)

   └─ Delegate to deployment-release



3. deployment-release Phase:

   ├─ Read current grafana-dashboards ConfigMap

   ├─ Edit ConfigMap YAML (add/update dashboard JSON)

   ├─ Validate change (bash scripts/deployment/validate-k8s-manifests.sh --mode=standard)

   ├─ Apply change (bash scripts/deployment/deploy-local-k8s.sh)

   ├─ Restart Grafana pods (kubectl rollout restart deployment/grafana)

   ├─ Monitor rollout (kubectl rollout status deployment/grafana)

   └─ Verify dashboard accessible



4. Verification Phase (deployment-release):

   ├─ Check 1: ConfigMap updated (kubectl get configmap grafana-dashboards -o yaml)

   ├─ Check 2: Pods running (kubectl get pods -l app=grafana)

   ├─ Check 3: Volume mounted (kubectl describe pod <grafana-pod>)

   └─ Check 4: Dashboard endpoint (curl http://localhost:3000/api/dashboards/...)



5. Response Phase (deployment-release → Orchestrator):

   └─ Return SUCCESS with deployment evidence OR FAILURE with diagnostics

```

**Success Criteria**:

- ConfigMap contains updated dashboard JSON

- Grafana pods restarted successfully

- All pods in `Running` state

- Dashboard accessible via Grafana API

**Failure Modes**:

- ConfigMap edit fails (YAML syntax error)

- Validation fails (immutable field change)

- Pod restart timeout (> 5 minutes)

- Dashboard not accessible (JSON syntax error in Grafana)

### Workflow 2: ConfigMap Generation (grafana-dashboard-builder Scope)

**Purpose**: Generate ConfigMap manifest with dashboard JSON for initial deployment

**Execution Flow**:

```

1. Dashboard Generation:

   ├─ grafana-dashboard-builder generates dashboard JSON

   ├─ Validate JSON schema

   └─ Return dashboard JSON



2. ConfigMap Manifest Creation:

   ├─ Orchestrator creates ConfigMap YAML structure

   ├─ Embed dashboard JSON in data section

   └─ Write to k8s/local/grafana-dashboards.yaml



3. Deployment Delegation:

   └─ Delegate to deployment-release with deploy operation

```

**ConfigMap Structure**:

```yaml
apiVersion: v1

kind: ConfigMap

metadata:
  name: grafana-dashboards

  namespace: gauntlet-agents

  labels:
    app: grafana

data:
  api-gateway-dashboard.json: |

    {

      "dashboard": {

        "title": "API Gateway Metrics",

        "panels": [...],

        "templating": {...}

      }

    }

  traces-dashboard.json: |

    {

      "dashboard": {

        "title": "Distributed Traces",

        "panels": [...],

        "templating": {...}

      }

    }
```

**Key Considerations**:

- Each dashboard is a separate key in ConfigMap data

- JSON must be properly indented (2 spaces per level)

- File extension `.json` required for Grafana auto-import

- Multiple dashboards can coexist in single ConfigMap

---

## 4. Decision Trees

### Decision Tree 1: Operation Selection

```

User Request: "Deploy Grafana dashboard"

↓

Dashboard JSON ready?

├─ NO → grafana-dashboard-builder generates first

└─ YES → Check deployment state

    ↓

    Grafana deployed?

    ├─ NO → Use deploy operation (full stack)

    │   └─ Includes: Prometheus, Jaeger, OTEL, Grafana

    └─ YES → Use config_update operation (ConfigMap only)

        ↓

        Dashboard exists in ConfigMap?

        ├─ YES → Update existing dashboard (replace JSON)

        └─ NO → Add new dashboard (append to data section)

```

### Decision Tree 2: Rollback Strategy

```

Deployment Failed?

↓

Failure Type Classification:

├─ ConfigMap validation error (exit code 2)

│   └─ Fix Forward: Correct YAML syntax, re-apply

│       ├─ Immutable field error → Delete + recreate ConfigMap

│       └─ Schema error → Fix manifest, re-validate

│

├─ Pod CrashLoopBackOff

│   └─ Investigate Root Cause:

│       ├─ Dashboard JSON syntax error (Grafana logs)

│       │   └─ Fix Forward: Correct JSON, update ConfigMap

│       ├─ Missing data source (Prometheus/Jaeger)

│       │   └─ Fix Forward: Deploy data source first

│       └─ ConfigMap mount failure

│           └─ Rollback: kubectl rollout undo

│

├─ Pod pending (> 5 minutes)

│   └─ Resource constraints:

│       ├─ Insufficient CPU/memory → Increase limits

│       └─ PVC not bound → Check storage provisioner

│

└─ Validation timeout

    └─ Retry with increased timeout

```

### Decision Tree 3: Validation Mode Selection

```

Operation Type?

├─ Quick syntax check before editing

│   └─ Use: --mode=quick (2-3 seconds)

│       └─ Client-side only, no cluster access

│

├─ Pre-deployment validation

│   └─ Use: --mode=standard (5-7 seconds, default)

│       └─ Client + server validation, catches immutable field issues

│

├─ CI/CD pipeline validation

│   └─ Use: --mode=full (7-10 seconds)

│       └─ Comprehensive with kustomize build check

│

├─ Post-edit verification

│   └─ Use: --mode=standard --verbose

│       └─ Detailed error messages for debugging

│

└─ Show deployment diff

    └─ Use: --mode=standard --diff

        └─ Preview changes before applying

```

**Exit Code Interpretation**:

- `0` - All validations passed → Proceed to deployment

- `1` - Client-side error (syntax) → Fix YAML and retry

- `2` - Server-side error (immutable field) → May require delete+recreate

- `3` - Kustomize build error → Fix kustomization.yaml

- `4` - Prerequisites missing → Install kubectl or check cluster

---

## 5. Anti-Patterns

### Anti-Pattern 1: Direct kubectl Commands

**❌ WRONG**:

```python

Bash("kubectl apply -f k8s/local/grafana-dashboards.yaml")

```

**Why It Fails**:

- `kubectl apply` is BLOCKED by `.claude/settings.json` security policy

- Security hooks reject command with error

**✅ CORRECT**:

```python

Task(

  agent="deployment-release",

  prompt="""UPDATE grafana-dashboards ConfigMap.



Operation: config_update

Use deployment script: bash scripts/deployment/deploy-local-k8s.sh"""

)

```

**Rationale**: Deployment scripts are allowed (`Bash(bash:*)` permission) and execute kubectl safely within controlled workflows.

### Anti-Pattern 2: Skipping Validation

**❌ WRONG**:

```python

# Edit ConfigMap → Apply immediately (no validation)

Edit(file="k8s/local/grafana-dashboards.yaml", ...)

Bash("bash scripts/deployment/deploy-local-k8s.sh")

```

**Why It's Risky**:

- YAML syntax errors crash Grafana pods

- Immutable field changes fail silently

- No opportunity to catch errors before applying

**✅ CORRECT**:

```python

# Edit → Validate → Apply (validate CHANGED content)

Edit(file="k8s/local/grafana-dashboards.yaml", ...)

Bash("bash scripts/deployment/validate-k8s-manifests.sh --mode=standard gauntlet-agents k8s/local")

Bash("bash scripts/deployment/deploy-local-k8s.sh")

```

**Critical Order**: ALWAYS validate AFTER editing, BEFORE applying. Validates new content, not old.

### Anti-Pattern 3: Forgetting Pod Restart

**❌ WRONG**:

```python

# Update ConfigMap but don't restart pods

Task(

  agent="deployment-release",

  prompt="Update grafana-dashboards ConfigMap (no pod restart)"

)

```

**Why It Fails**:

- Kubernetes ConfigMaps don't hot-reload

- Grafana continues using old dashboard version

- Changes invisible until pod restart or manual restart

**✅ CORRECT**:

```python

Task(

  agent="deployment-release",

  prompt="""Update grafana-dashboards ConfigMap.



CRITICAL: Trigger Grafana pod restart after update.

Command: kubectl rollout restart deployment/grafana"""

)

```

**Verification**: Check pod age after restart - all pods should be < 2 minutes old.

### Anti-Pattern 4: Missing Verification

**❌ WRONG**:

```python

# Deploy → Assume success → Return

Task(agent="deployment-release", ...)

return SUCCESS  # No verification

```

**Why It's Incomplete**:

- Deployment may fail silently

- Pods may crash after initial startup

- Dashboard may not be accessible

**✅ CORRECT**:

```python

Task(

  agent="deployment-release",

  prompt="""Deploy dashboard and VERIFY:

1. ConfigMap exists: kubectl get configmap grafana-dashboards -o yaml

2. Pods running: kubectl get pods -l app=grafana

3. Volume mounted: kubectl describe pod <grafana-pod> | grep grafana-dashboards

4. Dashboard accessible: curl http://localhost:3000/api/dashboards/..."""

)

```

**4-Check Verification Protocol**: Always run all 4 checks before returning SUCCESS.

### Anti-Pattern 5: Editing with CLI Args (YAML Special Characters)

**❌ WRONG**:

```bash

# Using --old and --new CLI args for YAML content

uv run python scripts/file_ops.py \

  --file k8s/local/grafana-dashboards.yaml \

  --old "data: {}" \

  --new "data: {dashboard.json: {...}}"

```

**Why It Fails**:

- YAML contains shell special characters: `$()`, `<>`, `|`, `>`

- Environment variables: `$(POD_NAME)`, `${VAR}`

- Shell interprets these as command substitution or redirection

- Quotes and colons break shell parsing

**✅ CORRECT**:

```python

from file_ops import create_temp_edit_files



old_file, new_file = create_temp_edit_files(

    "deployment-release",

    old_yaml_content,  # Full YAML with special chars

    new_yaml_content   # Updated YAML

)



Bash(f"uv run python scripts/file_ops.py --file k8s/local/grafana-dashboards.yaml --old-file {old_file} --new-file {new_file}")

```

**Rationale**: File-based input eliminates shell escaping issues (industry standard for diff, patch, kubectl diff).

---

## 6. Integration Points

### Orchestrator Coordination

**Delegation Pattern**:

```python

# Step 1: grafana-dashboard-builder generates dashboard

dashboard_result = Task(

  agent="grafana-dashboard-builder",

  prompt="Generate API Gateway metrics dashboard"

)



# Step 2: Extract dashboard JSON

dashboard_json = dashboard_result["agent_specific_output"]["dashboard_json"]



# Step 3: Delegate deployment to deployment-release

deployment_result = Task(

  agent="deployment-release",

  prompt=f"""UPDATE grafana-dashboards ConfigMap.



Operation: config_update

ConfigMap: grafana-dashboards

Namespace: gauntlet-agents

Dashboard JSON:

{dashboard_json}



Validation: standard mode

Restart: Grafana pods after update

Verification: 4-check protocol"""

)



# Step 4: Orchestrator processes result

if deployment_result["status"] == "SUCCESS":

    # Report success to user

    print("Dashboard deployed successfully")

else:

    # Handle failure

    failures = deployment_result["failure_details"]

    # Retry or escalate

```

**Output Processing**:

- **SUCCESS**: Extract deployment evidence (ConfigMap version, pod names, endpoint URLs)

- **FAILURE**: Parse failure_details for recovery suggestions, decide retry/escalate

### Multi-Agent Workflows

**Upstream Dependencies** (grafana-dashboard-builder):

- Dashboard JSON generation

- Schema validation

- Query syntax validation

- Panel configuration

**Downstream Integration** (deployment-release):

- ConfigMap deployment

- Pod lifecycle management

- Infrastructure verification

- Rollback execution

**State Management**:

- deployment-release tracks state via kubectl (Kubernetes API is source of truth)

- No internal state retention between Task invocations

- Each Task is stateless, context provided in prompt

**Conflict Resolution**:

- Sequential execution only (no parallel ConfigMap edits)

- Kubernetes handles resource locking

- deployment-release serializes operations on same ConfigMap

### Verification Protocol (4 Checks)

deployment-release MUST run these checks before returning SUCCESS:

**Check 1: ConfigMap Updated**

```bash

kubectl get configmap grafana-dashboards -n gauntlet-agents -o yaml | grep -A 10 "dashboard-name.json"

```

**Expected**: Dashboard JSON present in ConfigMap data section

**Check 2: Pod Status**

```bash

kubectl get pods -n gauntlet-agents -l app=grafana

```

**Expected**: All pods in `Running` state, age < 5 minutes

**Check 3: Volume Mount**

```bash

kubectl describe pod <grafana-pod> -n gauntlet-agents | grep -A 5 "Mounts:"

```

**Expected**: `/etc/grafana/provisioning/dashboards/` mount from grafana-dashboards ConfigMap

**Check 4: Dashboard Accessible**

```bash

kubectl port-forward -n gauntlet-agents svc/grafana 3000:3000 &

curl -s http://localhost:3000/api/dashboards/db/dashboard-name | jq .meta.slug

```

**Expected**: Dashboard metadata returned (HTTP 200)

**Verification Failure Actions**:

- Check 1 fails → ConfigMap update failed, rollback

- Check 2 fails → Pod crash, investigate logs, rollback

- Check 3 fails → Volume mount issue, check manifest

- Check 4 fails → Dashboard JSON error, rollback + fix JSON

---

## 7. Complete Task Invocation Examples

### Example 1: Update Existing Dashboard

```python

Task(

  agent="deployment-release",

  prompt="""UPDATE grafana-dashboards ConfigMap with API Gateway dashboard.



## Operation Details

- Operation Type: config_update

- ConfigMap Name: grafana-dashboards

- Namespace: gauntlet-agents

- Dashboard File: api-gateway.json



## Dashboard JSON

{

  "dashboard": {

    "title": "API Gateway Metrics",

    "uid": "api-gateway",

    "panels": [

      {

        "id": 1,

        "type": "graph",

        "title": "Request Rate",

        "targets": [

          {

            "expr": "rate(http_requests_total[5m])",

            "legendFormat": "{{method}} {{status}}"

          }

        ]

      }

    ],

    "templating": {

      "list": [

        {

          "name": "namespace",

          "type": "query",

          "query": "label_values(namespace)"

        }

      ]

    }

  }

}



## Validation

- Mode: standard

- Show diff: true

- Validate before apply: required



## Pod Restart

- Restart pods: YES (ConfigMaps don't hot-reload)

- Deployment: grafana

- Wait for rollout: true (max 5 minutes)



## Verification (4 checks)

1. ConfigMap contains api-gateway.json

2. All Grafana pods running (age < 5 min)

3. Volume mounted at /etc/grafana/provisioning/dashboards/

4. Dashboard accessible at http://localhost:3000/api/dashboards/db/api-gateway



## Expected Outcome

- ConfigMap updated successfully

- Grafana pods restarted

- Dashboard visible in Grafana UI

- SUCCESS response with deployment evidence"""

)

```

### Example 2: Full Stack Deployment

```python

Task(

  agent="deployment-release",

  prompt="""DEPLOY Grafana with observability stack.



## Operation Details

- Operation Type: deploy

- Namespace: gauntlet-agents

- Manifests: k8s/local

- Cluster Context: local



## Deployment Components

1. Prometheus (metrics collection)

2. Jaeger v2 (distributed tracing)

3. OTEL Collector (telemetry pipeline)

4. Grafana (visualization + dashboards)



## Validation

- Mode: full (client + server + kustomize)

- Secrets check: true

- Observability check: true (verify_observability.py)



## Deployment Pipeline (7 phases)

1. Pre-flight validation (cluster connectivity, manifest syntax)

2. Secret setup (bash scripts/deployment/setup-k8s-secrets.sh)

3. Manifest application (bash scripts/deployment/deploy-local-k8s.sh)

4. Rollout monitoring (kubectl rollout status)

5. Health checks (pod readiness, liveness probes)

6. Observability verification (Grafana/Jaeger/Prometheus endpoints)

7. Validation testing (validate_deployment.py)



## Service Endpoints

- Grafana: http://localhost:3000

- Prometheus: http://localhost:9090

- Jaeger UI: http://localhost:16686

- OTEL Collector: localhost:4317 (gRPC), localhost:4318 (HTTP)



## Expected Outcome

- All 4 components deployed successfully

- Services accessible via port-forward

- verify_observability.py passes

- validate_deployment.py passes

- SUCCESS response with service URLs"""

)

```

### Example 3: Rollback After Failure

```python

Task(

  agent="deployment-release",

  prompt="""ROLLBACK Grafana deployment to previous revision.



## Context

- Deployment: grafana

- Namespace: gauntlet-agents

- Reason: Dashboard JSON caused pod CrashLoopBackOff

- Failure Mode: Grafana failed to parse dashboard JSON (syntax error)



## Rollback Strategy

- Method: kubectl rollout undo deployment/grafana

- Target Revision: Previous (automatic detection)

- Wait for rollout: true (max 5 minutes)



## Root Cause (for reference)

- Dashboard JSON contained invalid panel configuration

- Error: "panels[0].targets[0].expr: invalid PromQL syntax"

- Impact: All Grafana pods crashed on startup



## Verification After Rollback

1. Check rollout history (kubectl rollout history)

2. Verify pods running (kubectl get pods -l app=grafana)

3. Check dashboard count (should be N-1 after rollback)

4. Test Grafana UI accessibility



## Expected Outcome

- Rollback successful

- Grafana pods healthy

- Previous dashboard set active

- FAILURE response with diagnostics:

  - Root cause: Invalid PromQL syntax in dashboard

  - Recovery: Fix dashboard JSON, re-deploy

  - Rollback evidence: Revision N-1 active



## Handoff to grafana-dashboard-builder

- Return diagnostics to orchestrator

- Orchestrator delegates JSON correction to grafana-dashboard-builder

- Retry deployment after JSON fix"""

)

```

---

## 8. Performance Characteristics

### Operation Timings

| Operation | Duration | Bottleneck | Optimization |

|-----------|----------|------------|--------------|

| **config_update** | 30-60s | Pod restart (20-40s) | Pre-warm Grafana pods |

| **deploy** | 3-5min | Image pulls, init containers | Use cached images |

| **validate** | 5-10s | Server-side validation | Use quick mode for syntax |

| **rollback** | 30-45s | Pod termination (10-20s) | None (Kubernetes-limited) |

| **troubleshoot** | 2-5min | Log retrieval, event parsing | Target specific failure mode |

### Scaling Considerations

**Dashboard Count**:

- 1-5 dashboards: <50KB ConfigMap, fast updates

- 5-20 dashboards: 50-200KB ConfigMap, moderate updates

- 20+ dashboards: >200KB ConfigMap, consider splitting into multiple ConfigMaps

**ConfigMap Size Limits**:

- Kubernetes limit: 1MB per ConfigMap

- Recommended max: 500KB (leaves headroom)

- If exceeding: Split into multiple ConfigMaps (e.g., `grafana-dashboards-metrics`, `grafana-dashboards-traces`)

**Pod Restart Performance**:

- Rolling update: 1 pod at a time (safer, slower)

- Recreate: All pods at once (faster, brief downtime)

- Default: Rolling update for production-like behavior

---

## 9. Troubleshooting Workflow

### Issue: ConfigMap Update Fails

**Symptoms**: Validation script returns exit code 2 (server-side error)

**Diagnosis**:

1. Check error message for "immutable field" or "field is immutable"

2. Identify which field was changed (likely ConfigMap metadata)

3. Confirm not trying to change immutable fields (name, namespace, certain labels)

**Resolution**:

- **If immutable field changed**: Revert to valid field, re-apply

- **If ConfigMap needs replacement**: Delete old ConfigMap + create new one

**Prevention**: Use Python script with file-based input (eliminates YAML escaping issues)

### Issue: Pod CrashLoopBackOff After Dashboard Update

**Symptoms**: Pods restart repeatedly, never reach Running state

**Diagnosis**:

1. Check pod logs: `kubectl logs <grafana-pod> -n gauntlet-agents`

2. Look for dashboard parsing errors (e.g., "invalid panel configuration")

3. Check events: `kubectl get events --sort-by=.lastTimestamp | grep <pod-name>`

**Resolution**:

- **Dashboard JSON syntax error**: Fix JSON, update ConfigMap, restart pods

- **Missing data source**: Deploy Prometheus/Jaeger first

- **ConfigMap mount failure**: Check volume mount in pod spec

**Prevention**: Validate dashboard JSON with Grafana API before deploying

### Issue: Dashboard Not Visible in Grafana UI

**Symptoms**: ConfigMap updated, pods running, but dashboard missing

**Diagnosis**:

1. Check ConfigMap content: `kubectl get configmap grafana-dashboards -o yaml`

2. Verify dashboard file extension is `.json` (required for auto-import)

3. Check Grafana provisioning logs: `kubectl logs <grafana-pod> | grep provisioning`

4. Verify volume mount: `kubectl describe pod <grafana-pod> | grep Mounts`

**Resolution**:

- **Missing .json extension**: Rename file in ConfigMap, restart pods

- **Volume not mounted**: Check Grafana deployment volume configuration

- **Provisioning disabled**: Enable dashboard provisioning in Grafana config

**Prevention**: Always use `.json` extension, verify volume mount in deployment manifest

---

## 10. References

### Primary Sources

**deployment-release Agent Definition**:

- File: `.claude/agents/deployment-release.md`

- Lines 1-831 (complete agent definition)

- Operation types: Lines 581-683

- Validation protocol: Lines 799-810

- Manifest editing protocol: Lines 366-489

**orchestrator-workflow.md**:

- File: `.claude/docs/orchestrator-workflow.md`

- Agent coordination patterns: Lines 192-246

- Delegation patterns: Lines 606-620

**agent-selection-guide.md**:

- File: `.claude/docs/guides/agent-selection-guide.md`

- Domain-first thinking: Lines 84-579

- Work type recognition: Lines 583-880

- Multi-agent decisions: Lines 1194-1387

### Related Guides

**Observability Stack**:

- `docs/04-guides/observability/jaeger-troubleshooting.md` - Jaeger v2 ConfigMap mounting

- `docs/04-guides/observability/otel-collector-troubleshooting.md` - Memory limiter configuration

- `docs/04-guides/observability/grafana-troubleshooting.md` - Data source provisioning

**Telemetry Validation**:

- `.claude/docs/01-guides/infrastructure/observability/../observability/telemetry-disambiguation.md` - Infrastructure testing boundaries

- `.claude/docs/01-guides/infrastructure/observability/../observability/telemetrygen-usage.md` - CLI syntax for stack validation

### Deployment Scripts

**Primary Scripts**:

- `scripts/deployment/deploy-local-k8s.sh` - Full deployment pipeline

- `scripts/deployment/setup-k8s-secrets.sh` - Secret generation

- `scripts/deployment/validate-k8s-manifests.sh` - Manifest validation

**Validation Scripts**:

- `scripts/deployment/verify_observability.py` - Observability stack verification

- `scripts/deployment/validate_deployment.py` - Synthetic API tests

---

## 11. Change Log

| Version | Date | Author | Changes |

|---------|------|--------|---------|

| 1.0 | 2025-10-30 | documentation | Initial creation from research findings |

**Next Review**: 2025-11-30 (30 days)

**Feedback**: Report documentation gaps or inaccuracies to orchestrator for documentation updates.

---

**This handoff protocol provides complete integration guidance for grafana-dashboard-builder → deployment-release delegation, including operation selection, input contracts, verification protocols, and anti-pattern avoidance.**
