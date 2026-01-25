# Kustomize Integration Guide

**Purpose**: Kustomize workflow patterns for k8s-deployment agent

**Audience**: k8s-deployment agent (reference during manifest management and deployments)

---

## Kustomize Workflow: Base → Overlays → Patches → Transformers

### Architecture Overview

```
k8s/
├── base/                      # Environment-agnostic resources
│   ├── kustomization.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   └── secret-template.yaml
├── local/                     # Local development overlay
│   ├── kustomization.yaml
│   ├── local-development-patch.yaml
│   └── image-versions.yaml
├── staging/                   # Staging overlay
│   ├── kustomization.yaml
│   └── staging-patch.yaml
└── production/                # Production overlay
    ├── kustomization.yaml
    └── production-patch.yaml
```

---

## Base Resources

**Location**: `k8s/base/**`

**Purpose**: Core manifests shared across all environments

**Contents**:
- Deployment, Service, ConfigMap, Secret templates
- Environment-agnostic configuration
- Shared across local/staging/production

**Example `k8s/base/kustomization.yaml`**:
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - deployment.yaml
  - service.yaml
  - configmap.yaml
  - secret-template.yaml

commonLabels:
  app: gauntlet-agents
  app.kubernetes.io/name: gauntlet-agents
  app.kubernetes.io/part-of: financial-research-system
```

---

## Overlays

**Locations**:
- `k8s/local/**` - Local development
- `k8s/staging/**` - Staging environment
- `k8s/production/**` - Production environment

**Purpose**: Environment-specific customizations

**Environment-Specific Kustomization**:

### Local Development (`k8s/local/kustomization.yaml`)

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

bases:
  - ../base

namespace: gauntlet-agents

images:
  - name: gauntlet-agents
    newTag: local  # Local builds

replicas:
  - name: gauntlet-agents
    count: 1  # Single replica for local

patches:
  - path: local-development-patch.yaml
    target:
      kind: Deployment

commonLabels:
  environment: local
```

### Staging (`k8s/staging/kustomization.yaml`)

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

bases:
  - ../base

namespace: gauntlet-agents-staging

images:
  - name: gauntlet-agents
    newTag: main  # CI builds from main branch

replicas:
  - name: gauntlet-agents
    count: 2  # 2 replicas for HA

patches:
  - path: staging-patch.yaml
    target:
      kind: Deployment

commonLabels:
  environment: staging
```

### Production (`k8s/production/kustomization.yaml`)

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

bases:
  - ../base

namespace: gauntlet-agents-prod

images:
  - name: gauntlet-agents
    newTag: v1.2.3  # Tagged releases only

replicas:
  - name: gauntlet-agents
    count: 5  # 5 replicas for production scale

patches:
  - path: production-patch.yaml
    target:
      kind: Deployment

commonLabels:
  environment: production
```

---

## Strategic Patches

**Purpose**: Apply environment-specific modifications to base resources

### Local Development Patch

**File**: `k8s/local/local-development-patch.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gauntlet-agents
spec:
  template:
    spec:
      containers:
        - name: gauntlet-agents
          env:
            - name: LOG_LEVEL
              value: DEBUG  # Verbose logging for local
          resources:
            limits:
              cpu: 500m  # Reduced limits for local
              memory: 512Mi
            requests:
              cpu: 100m
              memory: 128Mi
```

### Production Patch

**File**: `k8s/production/production-patch.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gauntlet-agents
spec:
  template:
    spec:
      containers:
        - name: gauntlet-agents
          env:
            - name: LOG_LEVEL
              value: INFO  # Production logging
          resources:
            limits:
              cpu: 2000m  # Higher limits for production
              memory: 2Gi
            requests:
              cpu: 500m
              memory: 512Mi
      # Production security hardening
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
  # Autoscaling for production
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
```

---

## Transformers

**Purpose**: Automated resource modifications via plugins

### Label Injection

**Adds labels to all resources**:
```yaml
commonLabels:
  environment: local
  app.kubernetes.io/version: v1.0.0
  app.kubernetes.io/managed-by: kustomize
```

### Namespace Prefix/Suffix

**Adds namespace prefix**:
```yaml
nameSuffix: -dev
# Result: gauntlet-agents → gauntlet-agents-dev
```

### Image Name/Tag Replacements

**Overrides image tags**:
```yaml
images:
  - name: gauntlet-agents
    newName: registry.example.com/gauntlet-agents
    newTag: v1.2.3
```

---

## Resource Ordering

**CRITICAL**: Resources must be applied in dependency order to prevent failures

### Dependency Graph

```
1. Namespace (first - all other resources depend on it)
   ↓
2. ConfigMap, Secret (before Deployments - consumed by pods)
   ↓
3. PersistentVolumeClaim (before StatefulSets - mounted by pods)
   ↓
4. Service (before Ingress - referenced by ingress rules)
   ↓
5. Deployment, StatefulSet, DaemonSet (core workloads)
   ↓
6. NetworkPolicy (after workloads - references pod labels)
```

### Kustomize Ordering Configuration

**File**: `k8s/base/kustomization.yaml`

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

# Explicit resource ordering
resources:
  - namespace.yaml        # 1. Namespace first
  - configmap.yaml        # 2. ConfigMap
  - secret-template.yaml  # 2. Secret
  - pvc.yaml              # 3. PVC (if StatefulSet used)
  - service.yaml          # 4. Service
  - deployment.yaml       # 5. Deployment
  - networkpolicy.yaml    # 6. NetworkPolicy last
```

**Why ordering matters**:
- **ConfigMap before Deployment**: Pods fail to start if ConfigMap doesn't exist
- **Service before Ingress**: Ingress fails validation if Service not found
- **Namespace first**: All namespaced resources fail if namespace missing

---

## Common Kustomize Operations

### Build Without Applying (Preview)

```bash
AGENT_NAME=k8s-deployment kubectl kustomize k8s/local/
```

**What it does**:
- Generates final manifests without applying
- Useful for previewing changes before deployment

### Apply Kustomize Directory

```bash
AGENT_NAME=k8s-deployment kubectl apply -k k8s/local/
```

**IMPORTANT**: This command is **BLOCKED** by security policy.
**Use instead**: `bash scripts/deployment/deploy-local-k8s.sh`

### Diff Preview

```bash
AGENT_NAME=k8s-deployment kubectl diff -k k8s/local/
```

**What it does**:
- Shows differences between current cluster state and manifests
- Useful before applying changes

### Delete Kustomize Resources

```bash
AGENT_NAME=k8s-deployment kubectl delete -k k8s/local/
```

**IMPORTANT**: This command is **BLOCKED** by security policy.
**Use instead**: `bash scripts/deployment/deploy-local-k8s.sh --cleanup`

---

## Image Version Management

**Strategy**: Separate image versions from Kustomize config for easier updates

**File**: `k8s/local/image-versions.yaml`

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

images:
  - name: gauntlet-agents
    newTag: local-20250107-a3b2c1
  - name: postgresql
    newTag: 15-alpine
  - name: redis
    newTag: 7-alpine
```

**Reference in `kustomization.yaml`**:
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - image-versions.yaml
```

**Update workflow**:
1. Edit `image-versions.yaml` to change tag
2. Validate: `bash scripts/deployment/validate-k8s-manifests.sh --mode=standard`
3. Apply: `bash scripts/deployment/deploy-local-k8s.sh`
4. Monitor: `kubectl rollout status deployment/<name>`

---

## Kustomize Best Practices

### 1. Keep Base Minimal

- **DO**: Store only environment-agnostic resources in base
- **DON'T**: Put environment-specific values in base

### 2. Use Patches for Differences

- **DO**: Use strategic patches for environment variations
- **DON'T**: Duplicate entire manifests across overlays

### 3. Version Image Tags

- **DO**: Use explicit tags (v1.2.3, local-20250107-a3b2c1)
- **DON'T**: Use `latest` tag (breaks reproducibility)

### 4. Validate Before Applying

- **DO**: Always run validation script before deployment
- **DON'T**: Apply manifests without dry-run validation

### 5. Use Script-Based Deployment

- **DO**: Use `bash scripts/deployment/deploy-local-k8s.sh`
- **DON'T**: Run `kubectl apply -k` directly (blocked by security)

---

**See Also**:
- `kubectl-operations.md` - kubectl command reference
- `failure-patterns.md` - Troubleshooting K8s failures
- `troubleshooting-workflows.md` - Error handling and retry strategies
- `.claude/agents/k8s-deployment.md` - Complete deployment workflow
- `docs/04-guides/k8s-deployment/manifest-editing-protocol.md` - Manifest editing guide
- `k8s/base/kustomization.yaml` - Base configuration reference
- `k8s/local/kustomization.yaml` - Local overlay example
