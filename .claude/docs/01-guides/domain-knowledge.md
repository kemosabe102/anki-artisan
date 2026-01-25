---
title: "Kubernetes Deployment Domain Knowledge"
date: 2025-11-08
status: ACTIVE
tags: [claude-docs]
---
# Kubernetes Deployment Domain Knowledge

**Category**: domain-specific
**Domain**: Kubernetes deployment, Kustomize configuration, GitOps workflows
**Confidence**: 0.95
**Last Updated**: 2025-10-24T00:00:00Z
**Agent**: deployment-release

---

## Overview

This documentation provides comprehensive domain knowledge for deployment-release operations, covering kubectl command patterns, Kustomize configuration workflows, GitOps deployment principles, rolling update strategies, local Kubernetes environments, and observability stack integration for the Gauntlet Agents project.

**Key Concepts**:

- **kubectl Approved Commands**: Five safe read-only and deployment management commands for cluster interaction
- **Kustomize Workflow**: Declarative configuration management using base + overlays + patches pattern
- **GitOps Principles**: Four core principles ensuring declarative, versioned, and continuously reconciled deployments

---

## Core Frameworks

### Framework 1: kubectl Command Patterns

**Purpose**: Provide safe, read-only cluster inspection and deployment management without imperative modifications.

**When to Use**:

- Inspecting cluster state for validation
- Retrieving resource configurations for analysis
- Managing deployment rollouts and rollbacks
- Accessing container logs for debugging
- Port forwarding for local development access

**Components**:

1. **kubectl get**: List resources with flexible output formatting and filtering
2. **kubectl describe**: Detailed resource state including events and conditions
3. **kubectl logs**: Container log access with streaming and historical options
4. **kubectl rollout**: Deployment lifecycle management (status/history/undo/pause/resume/restart)
5. **kubectl port-forward**: Local port forwarding to cluster services

**How to Apply**:

1. Use `kubectl get` with output formats for structured data (`-o json|yaml|wide`)
2. Apply label selectors (`-l app=myapp`) or field selectors (`--field-selector status.phase=Running`) for filtering
3. Use `kubectl describe` for event-driven debugging (check Events section)
4. Follow logs in real-time with `kubectl logs -f` or retrieve previous container logs with `--previous`
5. Manage rollouts with `kubectl rollout status deployment/myapp` (check progress) or `kubectl rollout undo` (rollback)

**Example from Codebase**:

```bash
# Get all pods in JSON format with label selector
kubectl get pods -n gauntlet-agents -l app=api -o json

# Describe deployment to check events and conditions
kubectl describe deployment api -n gauntlet-agents

# Follow logs from specific container
kubectl logs -f deployment/api -n gauntlet-agents -c api --tail=100

# Check rollout status
kubectl rollout status deployment/api -n gauntlet-agents

# Port forward to local development
kubectl port-forward -n gauntlet-agents service/api 8080:80
```

**Source**: Kubernetes Official Documentation (https://kubernetes.io/docs/reference/kubectl/)

---

### Framework 2: Kustomize Configuration Management

**Purpose**: Manage Kubernetes configuration across environments using declarative composition and patching without templating.

**When to Use**:

- Multi-environment deployments (local, staging, production)
- Common configuration sharing across resources
- Environment-specific customizations (image tags, replicas, resource limits)
- ConfigMap/Secret generation with content hashing

**Components**:

1. **Base**: Shared configuration common to all environments
2. **Overlays**: Environment-specific customizations (local, staging, production)
3. **Patches**: Targeted modifications to specific resources
4. **Transformers**: Cross-cutting changes (labels, namespaces, image tags)
5. **Generators**: ConfigMap/Secret creation with hash suffixes

**How to Apply**:

1. Structure directories: `k8s/base/` for shared config, `k8s/local/`, `k8s/staging/`, `k8s/production/` for overlays
2. Define resource composition order in `kustomization.yaml`: namespace → dependencies → workloads
3. Use `patchesStrategicMerge` or `patchesJson6902` for targeted modifications
4. Apply common labels with `commonLabels` (includes `includeSelectors: true` and `includeTemplates: true`)
5. Transform images with `images` field for environment-specific tags

**Example from Codebase**:

```yaml
# k8s/base/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - namespace.yaml
  - configmap.yaml
  - deployment.yaml
  - service.yaml

commonLabels:
  app.kubernetes.io/name: gauntlet-agents
  app.kubernetes.io/component: api

# k8s/local/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

bases:
  - ../base

namespace: gauntlet-agents

images:
  - name: gauntlet-api
    newName: gauntlet-api
    newTag: local-dev

patchesStrategicMerge:
  - deployment-patch.yaml

configMapGenerator:
  - name: app-config
    files:
      - config.yaml
    # Generates app-config-{hash} with content hash suffix
```

**Source**: `k8s/local/` directory in codebase

---

### Framework 3: GitOps Deployment Principles

**Purpose**: Ensure reliable, auditable, and self-healing deployments by treating Git as the single source of truth.

**When to Use**:

- Production deployments requiring audit trails
- Multi-environment synchronization from version control
- Automated drift detection and remediation
- Rollback capabilities via Git history

**Components**:

1. **Declarative**: Describe desired state (YAML manifests), not steps (imperative commands)
2. **Versioned and Immutable**: Git commits as single source of truth with full audit trail
3. **Pulled Automatically**: Agent-based synchronization (ArgoCD, Flux) with no CI/CD cluster write access
4. **Continuously Reconciled**: Self-healing with drift detection and auto-remediation

**How to Apply**:

1. Store all Kubernetes manifests in Git repository (`k8s/` directory)
2. Use declarative Kustomize configurations (never imperative kubectl commands in CI/CD)
3. Deploy GitOps operator (ArgoCD/Flux) with pull-based synchronization
4. Configure sync policies: automatic sync, self-heal, prune orphaned resources
5. Monitor sync status and application health through GitOps dashboard

**Example from Codebase**:

```yaml
# ArgoCD Application definition (example)
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: gauntlet-agents-local
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/gauntlet-agents
    targetRevision: main
    path: k8s/local
  destination:
    server: https://kubernetes.default.svc
    namespace: gauntlet-agents
  syncPolicy:
    automated:
      prune: true # Remove resources deleted from Git
      selfHeal: true # Revert manual cluster changes
    syncOptions:
      - CreateNamespace=true
```

**Source**: GitOps Principles (https://opengitops.dev/)

---

### Framework 4: Rolling Update Strategy

**Purpose**: Achieve zero-downtime deployments by gradually replacing old pods with new versions while maintaining availability.

**When to Use**:

- Production deployments requiring high availability
- Deployments with backward compatibility between versions
- Controlled rollout with quick rollback capability

**Components**:

1. **maxSurge**: Temporary over-provisioning during updates (e.g., 25% = 1 extra pod for 4 replicas)
2. **maxUnavailable**: Acceptable unavailability during updates (e.g., 0 = no downtime)
3. **Readiness Probes**: Health checks determining when new pods accept traffic
4. **Backward Compatibility**: Old and new versions coexist during rollout

**How to Apply**:

1. Set `maxSurge: 25%` and `maxUnavailable: 0` for zero-downtime deployments
2. Configure readiness probes with appropriate `initialDelaySeconds` and `periodSeconds`
3. Ensure API backward compatibility (old clients work with new servers)
4. Monitor rollout progress with `kubectl rollout status`
5. Rollback immediately if health checks fail with `kubectl rollout undo`

**Example from Codebase**:

```yaml
# k8s/base/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25% # 1 extra pod during update (3 * 0.25 = 0.75 → 1)
      maxUnavailable: 0 # No unavailability during update
  template:
    spec:
      containers:
        - name: api
          image: gauntlet-api:latest
          ports:
            - containerPort: 8080
          readinessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 5
            failureThreshold: 3
```

**Source**: `k8s/local/api.yaml` in codebase

---

## Processes & Workflows

### Workflow 1: Local Deployment with Kustomize

**Trigger Conditions**:

- Developer wants to deploy to local Kubernetes (Docker Desktop, Minikube, kind)
- Configuration changes need validation before staging/production
- Testing observability stack integration locally

**Steps**:

1. **Build Kustomize Configuration**:
   - **Input**: Base manifests + local overlay patches
   - **Output**: Rendered Kubernetes YAML
   - **Rationale**: Preview exact configuration before applying to cluster
   - **Command**: `kubectl kustomize k8s/local`

2. **Apply Configuration to Cluster**:
   - **Input**: Rendered YAML from kustomize build
   - **Output**: Resources created/updated in cluster
   - **Rationale**: Deploy declarative configuration to local cluster
   - **Command**: `kubectl apply -k k8s/local`

3. **Verify Deployment Status**:
   - **Input**: Deployment name and namespace
   - **Output**: Rollout status and pod health
   - **Rationale**: Ensure all pods are running and ready
   - **Command**: `kubectl rollout status deployment/api -n gauntlet-agents`

4. **Check Pod Logs**:
   - **Input**: Deployment/pod selector
   - **Output**: Container logs
   - **Rationale**: Verify application started successfully
   - **Command**: `kubectl logs -f deployment/api -n gauntlet-agents --tail=50`

5. **Port Forward for Access**:
   - **Input**: Service name and ports
   - **Output**: Local port access to cluster service
   - **Rationale**: Access application locally without LoadBalancer/Ingress
   - **Command**: `kubectl port-forward -n gauntlet-agents service/api 8080:80`

**Success Criteria**:

- ✅ All pods in `Running` state with `Ready 1/1`
- ✅ Deployment rollout completed successfully
- ✅ Application health endpoint returns 200 OK
- ✅ Observability stack components accessible (Prometheus, Grafana, Jaeger)

**Failure Handling**:

- If pod stuck in `Pending`, check `kubectl describe pod` for scheduling issues (resource constraints, node affinity)
- If pod stuck in `CrashLoopBackOff`, check `kubectl logs` for application errors
- If readiness probe fails, verify health endpoint path and port configuration
- If rollout stuck, run `kubectl rollout undo deployment/api -n gauntlet-agents` to rollback

**Example Execution**:

```bash
# 1. Preview configuration
kubectl kustomize k8s/local > /tmp/rendered.yaml
cat /tmp/rendered.yaml  # Inspect before applying

# 2. Apply to cluster
kubectl apply -k k8s/local

# 3. Wait for rollout
kubectl rollout status deployment/api -n gauntlet-agents
# Output: deployment "api" successfully rolled out

# 4. Check logs
kubectl logs -f deployment/api -n gauntlet-agents --tail=50

# 5. Port forward
kubectl port-forward -n gauntlet-agents service/api 8080:80
# Access at http://localhost:8080
```

---

### Workflow 2: Observability Stack Deployment

**Trigger Conditions**:

- Local development requires monitoring and tracing
- Validating OpenTelemetry instrumentation
- Debugging distributed traces or metrics collection

**Steps**:

1. **Deploy Observability Components**:
   - **Input**: Observability stack manifests (Prometheus, Grafana, Jaeger, OTel Collector)
   - **Output**: Monitoring infrastructure deployed
   - **Rationale**: Standalone observability stack for local development
   - **Command**: `kubectl apply -k k8s/local/observability`

2. **Verify OTel Collector Endpoints**:
   - **Input**: OTel Collector service name
   - **Output**: OTLP gRPC (4317) and HTTP (4318) endpoints available
   - **Rationale**: Ensure telemetry ingestion endpoints accessible
   - **Command**: `kubectl get svc otel-collector -n gauntlet-agents`

3. **Check Prometheus Scrape Targets**:
   - **Input**: Prometheus UI port-forward
   - **Output**: Active scrape targets status
   - **Rationale**: Verify dual-scrape (OTel + Windows Exporter) configuration
   - **Command**: `kubectl port-forward -n gauntlet-agents service/prometheus 9090:9090` → Access http://localhost:9090/targets

4. **Access Grafana Dashboards**:
   - **Input**: Grafana UI port-forward
   - **Output**: Pre-provisioned dashboards with live data
   - **Rationale**: Visualize metrics and validate data flow
   - **Command**: `kubectl port-forward -n gauntlet-agents service/grafana 3000:3000` → Access http://localhost:3000

5. **Verify Jaeger Trace Ingestion**:
   - **Input**: Jaeger UI port-forward
   - **Output**: Distributed traces from application
   - **Rationale**: Validate OpenTelemetry trace export
   - **Command**: `kubectl port-forward -n gauntlet-agents service/jaeger 16686:16686` → Access http://localhost:16686

**Success Criteria**:

- ✅ OTel Collector receiving OTLP traffic on ports 4317 (gRPC) and 4318 (HTTP)
- ✅ Prometheus scraping metrics from OTel Collector and Windows Exporter
- ✅ Grafana dashboards displaying live metrics
- ✅ Jaeger UI showing distributed traces from application

**Failure Handling**:

- If OTel Collector unhealthy, check `kubectl logs deployment/otel-collector` for configuration errors
- If Prometheus not scraping, verify ServiceMonitor CRDs or scrape configs in ConfigMap
- If Grafana datasource fails, check provisioned datasource URL matches service DNS
- If Jaeger shows no traces, verify application OTLP exporter endpoint configuration

**Example Execution**:

```bash
# 1. Deploy observability stack
kubectl apply -k k8s/local/observability

# 2. Verify OTel Collector
kubectl get svc otel-collector -n gauntlet-agents
# NAME             TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)
# otel-collector   ClusterIP   10.96.100.123   <none>        4317/TCP,4318/TCP

# 3. Check Prometheus targets
kubectl port-forward -n gauntlet-agents service/prometheus 9090:9090
# Access http://localhost:9090/targets - verify all targets UP

# 4. Access Grafana
kubectl port-forward -n gauntlet-agents service/grafana 3000:3000
# Login with admin/admin, check dashboards

# 5. Verify Jaeger traces
kubectl port-forward -n gauntlet-agents service/jaeger 16686:16686
# Search for traces, verify spans present
```

---

## Decision Trees

### Decision 1: kubectl Command Selection

```
IF need to list resources (pods, deployments, services)
  THEN use kubectl get with output format (-o json|yaml|wide)
  BECAUSE provides structured data for programmatic processing

ELSE IF need detailed resource state with events
  THEN use kubectl describe
  BECAUSE events section shows recent activity and errors

ELSE IF need container logs
  THEN use kubectl logs with flags (-f for follow, --tail for recent, --previous for crashed container)
  BECAUSE provides application-level debugging information

ELSE IF need to manage deployment lifecycle
  THEN use kubectl rollout (status|history|undo|pause|resume|restart)
  BECAUSE safe deployment management without imperative modifications

ELSE IF need local access to cluster service
  THEN use kubectl port-forward
  BECAUSE enables localhost access without exposing services externally

ELSE
  THEN FORBIDDEN - imperative modifications not allowed
  BECAUSE GitOps requires declarative configuration via Git
```

**Example Scenarios**:

1. **Scenario**: Check if deployment rollout completed → **Decision**: `kubectl rollout status deployment/api -n gauntlet-agents`
2. **Scenario**: Debug pod crash → **Decision**: `kubectl logs pod/api-abc123 -n gauntlet-agents --previous` (previous container logs)
3. **Scenario**: View deployment configuration → **Decision**: `kubectl get deployment api -n gauntlet-agents -o yaml`
4. **Scenario**: Access Grafana locally → **Decision**: `kubectl port-forward -n gauntlet-agents service/grafana 3000:3000`
5. **Scenario**: Rollback bad deployment → **Decision**: `kubectl rollout undo deployment/api -n gauntlet-agents`

---

### Decision 2: Local Kubernetes Environment Selection

```
IF need multi-node cluster with production-like behavior
  THEN use kind (Kubernetes in Docker)
  BECAUSE container-based nodes, YAML declarative config, closest to production

ELSE IF need rich addon ecosystem (dashboard, ingress, metrics-server)
  THEN use Minikube
  BECAUSE VM-based with extensive addon support

ELSE IF need simplest setup with bundled Kubernetes
  THEN use Docker Desktop Kubernetes
  BECAUSE single-node, bundled, zero configuration

ELSE IF need Windows/Linux hybrid cluster testing
  THEN use Minikube with multi-node profile
  BECAUSE supports heterogeneous node operating systems

ELSE
  THEN use kind (default recommendation)
  BECAUSE best balance of features and production similarity
```

**Example Scenarios**:

1. **Scenario**: Testing multi-replica deployments → **Decision**: kind with 3 worker nodes
2. **Scenario**: Quick local development → **Decision**: Docker Desktop (already running)
3. **Scenario**: Testing ingress controllers → **Decision**: Minikube with ingress addon
4. **Scenario**: Validating node affinity rules → **Decision**: kind with labeled nodes

---

### Decision 3: Kustomize Patch Strategy

```
IF need to modify simple fields (replicas, image tags, resource limits)
  THEN use patchesStrategicMerge
  BECAUSE more readable and maintainable for common use cases

ELSE IF need complex transformations (array element targeting, conditional logic)
  THEN use patchesJson6902
  BECAUSE RFC 6902 JSON Patch provides precise targeting

ELSE IF need to apply same change across multiple resources
  THEN use transformers (commonLabels, namePrefix, namespace)
  BECAUSE applies cross-cutting changes consistently

ELSE IF need to replace entire resource definition
  THEN use overlay resource (define complete resource in overlay)
  BECAUSE clearer intent for complete replacement

ELSE
  THEN use patchesStrategicMerge (default)
  BECAUSE covers 80% of use cases with best readability
```

**Example Scenarios**:

1. **Scenario**: Change replica count for production → **Decision**: patchesStrategicMerge with `spec.replicas: 10`
2. **Scenario**: Add sidecar container to specific deployment → **Decision**: patchesJson6902 targeting `spec.template.spec.containers` array
3. **Scenario**: Apply environment label to all resources → **Decision**: commonLabels transformer
4. **Scenario**: Override complete ConfigMap content → **Decision**: Define complete ConfigMap in overlay

---

## Best Practices

### Practice 1: Resource Composition Order

**Principle**: Deploy dependencies before consumers to avoid transient errors and ensure clean startup.

**Implementation**:

- Order resources in `kustomization.yaml`: namespace → configmaps/secrets → services → deployments
- Place persistent volumes and storage classes before deployments using them
- Deploy monitoring stack (Prometheus, Grafana) before application instrumentation

**Benefits**:

- ✅ Reduces transient errors during initial deployment
- ✅ Ensures ConfigMaps/Secrets available before pods start
- ✅ Services have stable IPs before deployments reference them

**Trade-offs**:

- ⚠️ Requires manual ordering in kustomization.yaml (not automatically determined)
- ⚠️ May need to split large deployments into multiple kustomize phases

**Example**:

```yaml
# k8s/base/kustomization.yaml - correct order
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  # 1. Namespace first (scope for all resources)
  - namespace.yaml

  # 2. Configuration before consumers
  - configmap.yaml
  - secret.yaml

  # 3. Services before deployments (stable IPs)
  - service.yaml

  # 4. Workloads last (consume configs and services)
  - deployment.yaml
```

---

### Practice 2: ConfigMap Hash Suffix Generation

**Principle**: Use Kustomize ConfigMapGenerator with hash suffixes to trigger automatic pod restarts when configuration changes.

**Implementation**:

- Use `configMapGenerator` instead of raw ConfigMap YAML
- Kustomize appends content hash to ConfigMap name (e.g., `app-config-abc123`)
- Deployment references ConfigMap by base name; Kustomize updates reference automatically
- ConfigMap change triggers new hash → new ConfigMap → deployment rollout

**Benefits**:

- ✅ Automatic pod restarts on configuration changes (no manual rollout restart)
- ✅ Immutable ConfigMaps (old versions preserved during rollout)
- ✅ Safe rollback capability (old ConfigMap still exists)

**Trade-offs**:

- ⚠️ ConfigMap cleanup required for old versions (manual or controller)
- ⚠️ Requires Kustomize-aware deployments (not compatible with raw kubectl)

**Example**:

```yaml
# k8s/local/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

configMapGenerator:
  - name: app-config # Base name
    files:
      - config.yaml
    # Generated: app-config-mt5hg8426f

# Deployment references base name
# k8s/base/deployment.yaml
spec:
  template:
    spec:
      volumes:
        - name: config
          configMap:
            name: app-config # Kustomize rewrites to app-config-mt5hg8426f
```

---

### Practice 3: Common Labels Injection

**Principle**: Apply consistent labels across all resources for observability, ownership tracking, and label selector queries.

**Implementation**:

- Use `commonLabels` in kustomization.yaml with `includeSelectors: true` and `includeTemplates: true`
- Apply app.kubernetes.io/\* labels (name, component, version, managed-by)
- Include custom labels for team, environment, cost-center

**Benefits**:

- ✅ Consistent labeling across entire application stack
- ✅ Enables powerful kubectl queries (`kubectl get all -l app.kubernetes.io/name=gauntlet-agents`)
- ✅ Supports monitoring and cost allocation dashboards

**Trade-offs**:

- ⚠️ Label changes trigger resource updates (can cause rollouts)
- ⚠️ Selectors are immutable (changing labels on Deployments requires delete/recreate)

**Example**:

```yaml
# k8s/base/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

commonLabels:
  app.kubernetes.io/name: gauntlet-agents
  app.kubernetes.io/component: api
  app.kubernetes.io/managed-by: kustomize
  team: platform
  environment: local
# Applied to all resources AND selectors AND pod templates
```

---

### Practice 4: Readiness Probe Configuration

**Principle**: Configure appropriate readiness probes to ensure zero-downtime deployments and accurate service mesh routing.

**Implementation**:

- Define HTTP GET readiness probe pointing to dedicated `/health` endpoint
- Set `initialDelaySeconds` based on startup time (e.g., 10s for fast apps, 60s for slow)
- Use `periodSeconds: 5` for responsive health checks
- Set `failureThreshold: 3` to avoid flapping (15s grace period)

**Benefits**:

- ✅ Prevents traffic routing to unhealthy pods
- ✅ Enables zero-downtime rolling updates
- ✅ Supports service mesh health-based load balancing

**Trade-offs**:

- ⚠️ Requires dedicated health endpoint implementation in application
- ⚠️ Conservative settings can slow down deployment rollouts

**Example**:

```yaml
# k8s/base/deployment.yaml
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
        - name: api
          image: gauntlet-api:latest
          ports:
            - containerPort: 8080
          readinessProbe:
            httpGet:
              path: /health
              port: 8080
              scheme: HTTP
            initialDelaySeconds: 10 # Wait 10s after pod start
            periodSeconds: 5 # Check every 5s
            timeoutSeconds: 3 # 3s timeout per check
            successThreshold: 1 # 1 success = ready
            failureThreshold: 3 # 3 failures = not ready (15s total)
```

---

## Anti-Patterns

### Anti-Pattern 1: Imperative kubectl apply Commands

**Problem**: Imperative modifications (kubectl edit, kubectl patch, kubectl scale) create configuration drift between Git and cluster state, breaking GitOps principles.

**Detection**:

- 🔴 Manual `kubectl edit` or `kubectl patch` commands in deployment scripts
- 🔴 CI/CD pipelines running `kubectl set image` instead of updating Git manifests
- 🔴 Configuration drift detected by ArgoCD/Flux sync status

**Consequences**:

- ❌ No audit trail for changes (who, what, when)
- ❌ Rollback requires guessing previous state
- ❌ Multi-environment inconsistency (prod config different from staging)
- ❌ Team members overwrite each other's manual changes

**Better Approach**:

```yaml
✅ Preferred Pattern (GitOps):
# 1. Update Git manifest
# k8s/production/kustomization.yaml
images:
  - name: gauntlet-api
    newTag: v1.2.3  # Changed from v1.2.2

# 2. Commit to Git
git add k8s/production/kustomization.yaml
git commit -m "feat: update API to v1.2.3"
git push

# 3. ArgoCD/Flux automatically syncs cluster to Git state
# (or manual: kubectl apply -k k8s/production)

❌ Anti-Pattern (Imperative):
kubectl set image deployment/api api=gauntlet-api:v1.2.3 -n gauntlet-agents
# No Git record, no audit trail, no easy rollback
```

**Migration Strategy**:

1. Audit current cluster state: `kubectl get all -n gauntlet-agents -o yaml > current-state.yaml`
2. Migrate to Kustomize: Create base + overlays matching current state
3. Validate: `kubectl diff -k k8s/production` (should show no changes)
4. Enable GitOps sync: Deploy ArgoCD/Flux with auto-sync enabled
5. Enforce policy: Block direct kubectl write access via RBAC (read-only for humans)

---

### Anti-Pattern 2: Hardcoded Image Tags in Base Manifests

**Problem**: Using static image tags (e.g., `image: gauntlet-api:latest`) in base manifests prevents environment-specific versions and creates unpredictable deployments.

**Detection**:

- 🔴 Base deployment.yaml contains `image: myapp:latest` or `image: myapp:v1.0.0`
- 🔴 All environments (local, staging, production) use same image tag
- 🔴 No `images` transformer in overlay kustomization.yaml

**Consequences**:

- ❌ Cannot deploy different versions to different environments
- ❌ `latest` tag creates unpredictable behavior (which version am I running?)
- ❌ Rollback requires changing base manifest (affects all environments)
- ❌ Testing new versions requires temporary base changes

**Better Approach**:

```yaml
✅ Preferred Pattern (Overlay Image Transformation):
# k8s/base/deployment.yaml
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
        - name: api
          image: gauntlet-api  # No tag in base (placeholder)

# k8s/local/kustomization.yaml
images:
  - name: gauntlet-api
    newTag: local-dev        # Local development tag

# k8s/production/kustomization.yaml
images:
  - name: gauntlet-api
    newTag: v1.2.3          # Production version tag

❌ Anti-Pattern (Hardcoded in Base):
# k8s/base/deployment.yaml
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
        - name: api
          image: gauntlet-api:latest  # Hardcoded, unpredictable
```

**Migration Strategy**:

1. Remove tags from base deployment.yaml (use placeholder names only)
2. Add `images` transformer to each overlay kustomization.yaml
3. Pin production to specific version tags (not `latest`)
4. Use `local-dev` or `main` tags for development environments
5. Update CI/CD to bump image tags in Git (not kubectl)

---

### Anti-Pattern 3: Missing Readiness Probes

**Problem**: Deployments without readiness probes cause traffic routing to unhealthy pods during rollouts, resulting in 5xx errors and failed requests.

**Detection**:

- 🔴 Deployment.yaml missing `readinessProbe` field
- 🔴 Pods become `Ready` immediately upon container start (before app initialization)
- 🔴 Rollout shows brief 5xx error spike when new pods receive traffic too early

**Consequences**:

- ❌ Zero-downtime deployments fail (users hit unhealthy pods)
- ❌ Service mesh routes traffic to initializing pods
- ❌ Load balancer health checks fail transiently
- ❌ Rollbacks occur too late (after user impact)

**Better Approach**:

```yaml
✅ Preferred Pattern (Readiness Probe):
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
        - name: api
          image: gauntlet-api:latest
          readinessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 5
            failureThreshold: 3

❌ Anti-Pattern (No Readiness Probe):
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
        - name: api
          image: gauntlet-api:latest
          # No readiness probe - pod ready immediately
```

**Migration Strategy**:

1. Implement `/health` endpoint in application (return 200 when ready to accept traffic)
2. Add readiness probe to deployment.yaml with conservative `initialDelaySeconds`
3. Test rollout: `kubectl rollout status deployment/api` (verify gradual rollout)
4. Tune `initialDelaySeconds` based on observed startup time
5. Monitor rollout errors before/after probe addition (should see reduction in 5xx errors)

---

### Anti-Pattern 4: Single Kustomization File for All Environments

**Problem**: Using one kustomization.yaml for all environments (dev, staging, prod) creates fragile conditionals and environment-specific complexity.

**Detection**:

- 🔴 Single `k8s/kustomization.yaml` with conditional patches
- 🔴 Comments like "# Uncomment for production"
- 🔴 Environment-specific logic in base manifests

**Consequences**:

- ❌ High risk of deploying wrong configuration to production
- ❌ Manual intervention required for environment selection
- ❌ No clear separation of environment concerns
- ❌ Difficult to validate environment-specific configurations

**Better Approach**:

```yaml
✅ Preferred Pattern (Overlay Structure):
k8s/
├── base/                  # Shared configuration
│   ├── kustomization.yaml
│   ├── deployment.yaml
│   └── service.yaml
├── local/                 # Local development overlay
│   ├── kustomization.yaml
│   └── patches/
├── staging/               # Staging overlay
│   ├── kustomization.yaml
│   └── patches/
└── production/            # Production overlay
    ├── kustomization.yaml
    └── patches/

# Deploy specific environment:
kubectl apply -k k8s/production

❌ Anti-Pattern (Single File):
k8s/
└── kustomization.yaml  # Contains if/else logic for environments
```

**Migration Strategy**:

1. Create directory structure: `k8s/base/`, `k8s/local/`, `k8s/staging/`, `k8s/production/`
2. Move common manifests to `base/`
3. Extract environment-specific settings to overlay patches
4. Update CI/CD to target specific overlays: `kubectl apply -k k8s/$ENVIRONMENT`
5. Test each overlay independently before removing old structure

---

## Integration Points

### Integration 1: OpenTelemetry Collector

**Relationship**: deployment-release manages OTel Collector deployment while observability stack consumes telemetry data.

**Coordination Pattern**:

- Deploy OTel Collector as Kubernetes Deployment with dual OTLP receivers (gRPC 4317, HTTP 4318)
- Configure Prometheus ServiceMonitor to scrape OTel Collector metrics endpoint (port 8888)
- Export traces to Jaeger via OTLP exporter
- Use Kubernetes service discovery for scrape target configuration

**Example Usage**:

```yaml
# k8s/base/otel-collector.yaml
apiVersion: v1
kind: Service
metadata:
  name: otel-collector
spec:
  ports:
    - name: otlp-grpc
      port: 4317
      targetPort: 4317
    - name: otlp-http
      port: 4318
      targetPort: 4318
    - name: metrics
      port: 8888
      targetPort: 8888
  selector:
    app: otel-collector

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: otel-collector
spec:
  replicas: 1
  template:
    spec:
      containers:
        - name: otel-collector
          image: otel/opentelemetry-collector-contrib:latest
          ports:
            - containerPort: 4317
            - containerPort: 4318
            - containerPort: 8888
          volumeMounts:
            - name: config
              mountPath: /etc/otel-collector
      volumes:
        - name: config
          configMap:
            name: otel-collector-config
```

**Dependencies**:

- Requires ConfigMap with OTel Collector configuration (receivers, processors, exporters)
- Jaeger must be deployed before OTel Collector (OTLP exporter target)
- Application code must send telemetry to `otel-collector:4317` (gRPC) or `:4318` (HTTP)

---

### Integration 2: Prometheus Scrape Configuration

**Relationship**: deployment-release configures Prometheus to scrape metrics from OTel Collector and Windows Exporter (dual-scrape architecture).

**Coordination Pattern**:

- Use ServiceMonitor CRDs (if Prometheus Operator) or scrape_configs (if vanilla Prometheus)
- Configure Kubernetes service discovery for automatic target detection
- Apply relabeling rules for consistent metric naming
- Use separate jobs for OTel Collector and Windows Exporter

**Example Usage**:

```yaml
# k8s/base/prometheus-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s

    scrape_configs:
      # OTel Collector metrics
      - job_name: 'otel-collector'
        kubernetes_sd_configs:
          - role: service
        relabel_configs:
          - source_labels: [__meta_kubernetes_service_name]
            regex: otel-collector
            action: keep
          - source_labels: [__meta_kubernetes_service_port_name]
            regex: metrics
            action: keep

      # Windows Exporter metrics (if deployed)
      - job_name: 'windows-exporter'
        static_configs:
          - targets: ['host.docker.internal:9182']
```

**Dependencies**:

- OTel Collector service must expose metrics port (8888)
- Windows Exporter must be accessible from cluster (host networking or NodePort)
- Prometheus must have RBAC permissions for Kubernetes service discovery

---

### Integration 3: Grafana Dashboard Provisioning

**Relationship**: deployment-release provisions Grafana with pre-configured datasources and dashboards via ConfigMaps.

**Coordination Pattern**:

- Mount datasource YAML as ConfigMap volume in Grafana pod
- Mount dashboard JSON files as ConfigMap volume
- Configure Grafana to auto-load provisioned resources on startup
- Use consistent datasource names across dashboards

**Example Usage**:

```yaml
# k8s/base/grafana-datasource.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: grafana-datasources
data:
  datasources.yaml: |
    apiVersion: 1
    datasources:
      - name: Prometheus
        type: prometheus
        url: http://prometheus:9090
        isDefault: true
        access: proxy
      - name: Jaeger
        type: jaeger
        url: http://jaeger:16686
        access: proxy

# k8s/base/grafana-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: grafana
spec:
  template:
    spec:
      containers:
        - name: grafana
          image: grafana/grafana:latest
          volumeMounts:
            - name: datasources
              mountPath: /etc/grafana/provisioning/datasources
            - name: dashboards
              mountPath: /etc/grafana/provisioning/dashboards
      volumes:
        - name: datasources
          configMap:
            name: grafana-datasources
        - name: dashboards
          configMap:
            name: grafana-dashboards
```

**Dependencies**:

- Prometheus service must be deployed before Grafana (datasource target)
- Jaeger service must be deployed before Grafana (datasource target)
- Dashboard JSON must reference correct datasource names

---

### Integration 4: GitOps Sync with ArgoCD

**Relationship**: deployment-release defines Kubernetes manifests; ArgoCD continuously syncs cluster state to Git.

**Coordination Pattern**:

- Store all manifests in Git repository (k8s/ directory)
- Define ArgoCD Application resource pointing to Git repo + path
- Configure sync policy (automatic, self-heal, prune)
- Monitor sync status via ArgoCD UI or CLI

**Example Usage**:

```yaml
# argocd/application.yaml (deployed to ArgoCD namespace)
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: gauntlet-agents-local
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/gauntlet-agents
    targetRevision: main
    path: k8s/local
  destination:
    server: https://kubernetes.default.svc
    namespace: gauntlet-agents
  syncPolicy:
    automated:
      prune: true # Remove resources deleted from Git
      selfHeal: true # Revert manual cluster changes
    syncOptions:
      - CreateNamespace=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
```

**Dependencies**:

- ArgoCD must be deployed in cluster (argocd namespace)
- Git repository must be accessible from cluster (public or credentials configured)
- Kustomize must be enabled in ArgoCD (default)

---

## Validation & Quality Checks

### Check 1: Deployment Rollout Status

**What to Validate**: Deployment successfully rolled out with all pods running and ready.

**Validation Method**:

1. Run `kubectl rollout status deployment/<name> -n <namespace>`
2. Check for output: `deployment "<name>" successfully rolled out`
3. Verify pod count matches desired replicas: `kubectl get deployment <name> -n <namespace>`

**Pass Criteria**:

- Rollout status shows success message
- READY column shows `X/X` (all replicas ready)
- AGE column shows recent update timestamp

**Fail Criteria**:

- Rollout stuck (no progress after 10 minutes)
- READY column shows `0/X` or `<X/X` (some pods not ready)
- Pod status shows `CrashLoopBackOff`, `ImagePullBackOff`, or `Pending`

**Remediation**:

- Check pod logs: `kubectl logs deployment/<name> -n <namespace> --tail=100`
- Describe pods: `kubectl describe pod -l app=<name> -n <namespace>`
- Rollback: `kubectl rollout undo deployment/<name> -n <namespace>`

---

### Check 2: Kustomize Build Validation

**What to Validate**: Kustomize build produces valid Kubernetes YAML without errors.

**Validation Method**:

1. Run `kubectl kustomize k8s/<overlay>` (e.g., `k8s/local`)
2. Check for YAML output without error messages
3. Validate YAML structure: `kubectl kustomize k8s/<overlay> | kubectl apply --dry-run=client -f -`

**Pass Criteria**:

- Clean YAML output with all resources rendered
- Dry-run validation passes without errors
- No warnings about deprecated API versions

**Fail Criteria**:

- Error messages during kustomize build
- Invalid YAML structure
- Dry-run validation fails with schema errors

**Remediation**:

- Check kustomization.yaml for syntax errors
- Verify all referenced files exist (resources, patches, configMapGenerator)
- Validate patch targets match base resources (kind, name, namespace)

---

### Check 3: Observability Stack Health

**What to Validate**: All observability components (Prometheus, Grafana, Jaeger, OTel Collector) are healthy and data flows correctly.

**Validation Method**:

1. Check pod status: `kubectl get pods -n gauntlet-agents -l component=observability`
2. Verify Prometheus targets: Port-forward and check http://localhost:9090/targets (all UP)
3. Verify Grafana datasources: Port-forward and check datasource connectivity
4. Verify Jaeger receives traces: Port-forward and search for recent traces

**Pass Criteria**:

- All observability pods in `Running` state with `Ready 1/1`
- Prometheus shows all scrape targets UP
- Grafana datasources show green status
- Jaeger UI displays traces from application

**Fail Criteria**:

- Observability pods stuck in `Pending` or `CrashLoopBackOff`
- Prometheus targets DOWN or UNKNOWN
- Grafana datasources show red status
- Jaeger shows no traces (empty results)

**Remediation**:

- Check OTel Collector logs: `kubectl logs deployment/otel-collector -n gauntlet-agents`
- Verify service endpoints: `kubectl get svc -n gauntlet-agents`
- Check ConfigMap configurations: `kubectl get configmap otel-collector-config -n gauntlet-agents -o yaml`
- Verify application OTLP exporter endpoint matches service DNS

---

## Common Pitfalls & Solutions

| Pitfall                           | Detection                                        | Solution                                                                                                                                             |
| --------------------------------- | ------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Pods stuck in Pending**         | `kubectl get pods` shows `Pending` status        | Check `kubectl describe pod <name>` for events (insufficient CPU/memory, node affinity unsatisfied). Adjust resource requests or add nodes.          |
| **ImagePullBackOff**              | `kubectl get pods` shows `ImagePullBackOff`      | Verify image name/tag exists in registry. Check imagePullSecrets if private registry. Fix image name in deployment or overlay.                       |
| **CrashLoopBackOff**              | `kubectl get pods` shows `CrashLoopBackOff`      | Check `kubectl logs <pod-name> --previous` for application error. Fix application code or configuration causing crash.                               |
| **Rollout stuck at 50%**          | `kubectl rollout status` shows partial progress  | Check readiness probe configuration (too strict or wrong endpoint). Verify maxSurge/maxUnavailable settings.                                         |
| **Service not accessible**        | Cannot reach service via port-forward or ingress | Verify service selector matches pod labels. Check service port matches container port. Use `kubectl describe service <name>` to check endpoints.     |
| **ConfigMap changes not applied** | Updated ConfigMap but pods still use old config  | If using raw ConfigMap (not generator), run `kubectl rollout restart deployment/<name>`. Or migrate to configMapGenerator with hash suffixes.        |
| **Kustomize build fails**         | `kubectl kustomize` shows error                  | Check kustomization.yaml syntax. Verify all resources/patches exist. Ensure patch targets match base resources exactly.                              |
| **ArgoCD sync fails**             | ArgoCD UI shows degraded/failed sync             | Check ArgoCD application logs. Verify Git repo accessible. Ensure kustomize build succeeds locally first.                                            |
| **Prometheus not scraping**       | Prometheus targets page shows DOWN               | Verify ServiceMonitor CRD or scrape_configs correct. Check service port name matches scrape config. Ensure Prometheus RBAC allows service discovery. |
| **Grafana datasource fails**      | Grafana datasource shows red status              | Check datasource URL matches service DNS (e.g., `http://prometheus:9090`). Verify services deployed in same namespace or use FQDN.                   |

---

## Tools & Resources

### Recommended Tools

1. **kubectl**
   - **Purpose**: Kubernetes CLI for cluster interaction
   - **When to Use**: All cluster operations (get, describe, logs, rollout, port-forward)
   - **Documentation**: https://kubernetes.io/docs/reference/kubectl/

2. **kustomize**
   - **Purpose**: Declarative configuration management
   - **When to Use**: Multi-environment deployments, configuration customization
   - **Documentation**: https://kustomize.io/

3. **kind (Kubernetes in Docker)**
   - **Purpose**: Local multi-node Kubernetes clusters
   - **When to Use**: Testing multi-replica deployments, production-like local environment
   - **Documentation**: https://kind.sigs.k8s.io/

4. **ArgoCD**
   - **Purpose**: GitOps continuous delivery
   - **When to Use**: Production deployments with automated sync and drift detection
   - **Documentation**: https://argo-cd.readthedocs.io/

5. **kubectx/kubens**
   - **Purpose**: Fast context and namespace switching
   - **When to Use**: Working with multiple clusters or namespaces
   - **Documentation**: https://github.com/ahmetb/kubectx

6. **k9s**
   - **Purpose**: Terminal UI for Kubernetes
   - **When to Use**: Interactive cluster exploration and debugging
   - **Documentation**: https://k9scli.io/

### Learning Resources

1. **Kubernetes Official Documentation**: https://kubernetes.io/docs/
   - **Topic**: Comprehensive Kubernetes reference
   - **Quality**: High

2. **Kustomize Documentation**: https://kubectl.docs.kubernetes.io/guides/
   - **Topic**: Kustomize patterns and best practices
   - **Quality**: High

3. **GitOps Principles**: https://opengitops.dev/
   - **Topic**: GitOps workflow and principles
   - **Quality**: High

4. **OpenTelemetry Documentation**: https://opentelemetry.io/docs/
   - **Topic**: Observability instrumentation and configuration
   - **Quality**: High

5. **Prometheus Documentation**: https://prometheus.io/docs/
   - **Topic**: Metrics collection and querying
   - **Quality**: High

---

## Glossary

- **kubectl**: Kubernetes command-line tool for cluster interaction
- **Kustomize**: Kubernetes native configuration management tool using declarative YAML
- **GitOps**: Deployment methodology using Git as single source of truth
- **Rolling Update**: Deployment strategy gradually replacing old pods with new versions
- **Readiness Probe**: Health check determining when pod is ready to accept traffic
- **maxSurge**: Maximum number of extra pods created during rolling update
- **maxUnavailable**: Maximum number of unavailable pods during rolling update
- **Overlay**: Kustomize environment-specific customization layer
- **Patch**: Targeted modification to base Kubernetes resource
- **ConfigMapGenerator**: Kustomize feature creating ConfigMaps with content hash suffixes
- **ServiceMonitor**: Prometheus Operator CRD for scrape target configuration
- **OTLP**: OpenTelemetry Protocol for telemetry data transmission
- **OTel Collector**: OpenTelemetry component for receiving, processing, and exporting telemetry
- **Port Forward**: kubectl feature enabling local access to cluster services
- **Rollout**: Deployment lifecycle operation (status, history, undo, restart)

---

## Sources & References

1. Kubernetes Official Documentation: https://kubernetes.io/docs/
   - Accessed: 2025-10-24
   - Confidence: 0.98

2. Kustomize Documentation: https://kubectl.docs.kubernetes.io/guides/
   - Accessed: 2025-10-24
   - Confidence: 0.95

3. GitOps Principles: https://opengitops.dev/
   - Accessed: 2025-10-24
   - Confidence: 0.92

4. OpenTelemetry Documentation: https://opentelemetry.io/docs/
   - Accessed: 2025-10-24
   - Confidence: 0.90

5. Codebase Reference: k8s/local/api.yaml
   - Pattern: Rolling update configuration with readiness probes
   - Usage: Local deployment manifest for API service

6. Codebase Reference: k8s/local/kustomization.yaml
   - Pattern: Overlay structure with image transformations
   - Usage: Local environment Kustomize configuration

---

## Changelog

- **2025-10-24**: Initial documentation created from research findings (confidence: 0.95)

---

## Related Documentation

- `.claude/agents/deployment-release.md`: Agent definition and capabilities
- `.claude/docs/schemas/deployment-release.schema.json`: Agent output schema
- `docs/01-planning/features/006-opentelemetry-monitoring-infrastructure/SPEC.md`: Observability stack specification
- `.claude/docs/guides/file-operation-protocol.md`: File editing protocol for manifest updates
