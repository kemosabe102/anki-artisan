# Kubernetes Development Knowledge

---

Essential Kubernetes patterns, troubleshooting, and best practices for local development environments.

**📖 Complete Reference**: For comprehensive Kubernetes development workflows and enterprise patterns, see [Kubernetes Workflows: Kustomize & Troubleshooting](../../../../docs/04-guides/kubernetes/Kubernetes Workflows - Kustomize & Troubleshooting.md) - a detailed technical briefing covering modern Kubernetes development lifecycle, declarative configuration management, and systematic troubleshooting frameworks.

## Docker Desktop Kubernetes Local Development

### Local Image Management with `imagePullPolicy: Never`

**Critical Understanding**: When using `imagePullPolicy: Never` for local Docker images:

1. **Kubernetes NEVER pulls from registry** - only uses locally available images
2. **Local image updates require deployment restart** - Kubernetes caches image references
3. **Rebuilding same tag doesn't auto-update** - deployment continues using old cached reference

### Local Image Update Workflow

```bash
# 1. Build updated local image
docker build -t app-name:local .

# 2. MANDATORY: Restart deployment to use updated image
kubectl rollout restart deployment/app-name -n namespace

# 3. Verify new pods are using updated image
kubectl get pods -n namespace
kubectl describe pod <new-pod-name> -n namespace
```

### Alternative Force-Update Methods

```bash
# Method 1: Rolling restart (Kubernetes v1.15+) - PREFERRED
kubectl rollout restart deployment/app-name -n namespace

# Method 2: Timestamp environment variable
kubectl set env deployment/app-name REDEPLOY_TIME="$(date)" -n namespace

# Method 3: Add changing annotation (via Kustomize patch)
# Add timestamp annotation to deployment spec.template.metadata.annotations
```

## Kustomize Local Development Patterns

### Image Configuration for Local Development

```yaml
# kustomization.yaml - Local development approach
images:
  - name: ghcr.io/org/app-name
    newName: app-name # Local Docker image name
    newTag: local # Specific local tag (avoid 'latest')

# Local development patches
patches:
  - path: local-development-patch.yaml
    target:
      kind: Deployment
      name: app-name
```

```yaml
# local-development-patch.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-name
spec:
  template:
    spec:
      containers:
        - name: app-name
          imagePullPolicy: Never # CRITICAL: Use local images only
          resources:
            requests:
              memory: '256Mi' # Lower resource limits for local dev
              cpu: '100m'
            limits:
              memory: '512Mi'
              cpu: '500m'
```

### Why Separate Patch Files Are Better Than Inline

**Recommended**: Use separate patch files instead of inline patches in `kustomization.yaml`

- **Better organization**: Separates concerns between orchestration and configuration
- **Easier maintenance**: Patch files can be edited independently
- **Version control friendly**: Cleaner diffs when patches change
- **Reusability**: Patch files can be shared across environments

## Kustomize Development Patterns

### Core Concepts from Enterprise Workflows

**Base + Overlays Structure**:

```
my-app/
├── base/                    # Environment-agnostic common configuration
│   ├── deployment.yaml      # Generic deployment manifest
│   ├── service.yaml         # Common service definition
│   └── kustomization.yaml   # Lists base resources
└── overlays/                # Environment-specific overrides
    ├── development/         # Dev environment patches
    ├── staging/             # Staging configuration
    └── production/          # Production settings
```

**Key Principles**:

- **DRY Architecture**: Overlays contain only the differences, not full duplicates
- **Valid YAML**: Every file remains valid Kubernetes YAML (no templating)
- **GitOps Ready**: Clean, human-readable diffs in pull requests

### Dynamic Configuration with Generators

**ConfigMap/Secret Generation**:

```yaml
# kustomization.yaml
configMapGenerator:
  - name: my-app-config
    files:
      - config.properties # File becomes key, content becomes value
secretGenerator:
  - name: my-app-secrets
    literals:
      - username=admin # Direct key-value pairs
```

**Automatic Rolling Updates**:
When source files change, Kustomize generates new ConfigMap/Secret names with content hashes (e.g., `my-config-a1b2c3d4`). References are automatically updated, triggering Kubernetes rolling updates without manual intervention.

### Environment-Specific Transformers

**Image Management**:

```yaml
# Base uses generic tag
images:
  - name: my-app
    newTag: latest

# Production overlay specifies exact version
images:
  - name: my-app
    newTag: v1.2.3-stable
```

**Resource Scaling**:

```yaml
# Development: Single replica
replicas:
  - name: my-app
    count: 1

# Production: High availability
replicas:
  - name: my-app
    count: 10
```

## Docker Build and Timeout Handling

### Understanding Build Timeouts

**Common Issue**: Command timeouts during `docker build` don't mean the build failed

- **Tool timeout ≠ Docker failure**: CLI tools may timeout while Docker continues
- **Check for completion**: Look for final export messages in Docker output
- **Verify image creation**: Use `docker images` to confirm successful build

### Docker Build Verification

```bash
# Always verify image was created after potential timeout
docker images | grep app-name

# Check image details and creation time
docker inspect app-name:local

# Verify image size and layers are reasonable
docker history app-name:local
```

## Kubernetes Troubleshooting Patterns

### ImagePullBackOff vs ErrImageNeverPull

**ImagePullBackOff**: Kubernetes tried to pull from registry but failed

- Check registry accessibility, authentication, image existence
- Common with `imagePullPolicy: Always` or `IfNotPresent`

**ErrImageNeverPull**: Kubernetes configured to never pull, but image not found locally

- Check local image exists: `docker images`
- Verify image name/tag matches exactly
- Common with `imagePullPolicy: Never`

### Pod Lifecycle Debugging

```bash
# Check pod status and recent events
kubectl describe pod <pod-name> -n namespace

# View pod logs (current and previous containers)
kubectl logs <pod-name> -n namespace
kubectl logs <pod-name> -n namespace --previous

# Check container resource usage
kubectl top pod <pod-name> -n namespace

# Debug with interactive shell (if container allows)
kubectl exec -it <pod-name> -n namespace -- /bin/bash
```

## Systematic Troubleshooting Framework

### The Essential Diagnostic Sequence: Events → Describe → Logs

**Step 1: kubectl get events** - The cluster's nervous system

- Always check events first: `kubectl get events --sort-by='.metadata.creationTimestamp'`
- Provides cluster-wide view of issues affecting multiple pods
- Filter by type: `--field-selector type=Warning`

**Step 2: kubectl describe pod <pod-name>** - Detailed resource inspection

- **Status & Conditions**: Current state (Pending/Running/Failed) and why
- **Events section**: Pod-specific chronological events showing scheduler decisions
- **Last State**: For containers, shows exit codes and termination reasons

**Step 3: kubectl logs <pod-name>** - Application-level diagnostics

- Use `--previous` flag for crashed containers to see logs from terminated instance
- Essential for CrashLoopBackOff troubleshooting

### Interactive Debugging (Modern Kubernetes)

**Ephemeral Debug Containers** (Kubernetes v1.25+):

```bash
# Attach debug container to running pod (ideal for distroless images)
kubectl debug <pod-name> -it --image=busybox --target=<container-name>
```

**Traditional Debugging**:

```bash
# Direct shell access (requires shell in container)
kubectl exec -it <pod-name> -- /bin/sh

# Port forwarding for local tool access
kubectl port-forward <pod-name> <local-port>:<remote-port>
```

## Common Pod Failure Patterns

### ImagePullBackOff / ErrImagePull

**Causes**: Incorrect image name/tag, private registry authentication, network issues  
**Diagnosis**: `kubectl describe pod` Events section shows specific error (NotFound, access denied, etc.)

### CrashLoopBackOff

**Causes**: Application startup error, misconfiguration, incorrect command/entrypoint  
**Critical Command**: `kubectl logs <pod-name> --previous` (shows crash logs from terminated container)

### Pending State

**Causes**: Insufficient cluster resources, scheduling constraints, unbound PVCs  
**Diagnosis**: Events section shows scheduler's exact failure reason (e.g., "0/3 nodes available: 3 Insufficient cpu")

### OOMKilled (Exit Code 137)

**Causes**: Memory limit too low, application memory leak, node memory pressure  
**Diagnosis**: Last State shows "Reason: OOMKilled", requires memory usage analysis

## Best Practices Summary

### Image Management

- **Use specific tags** (not `latest`) for predictable behavior
- **Set imagePullPolicy explicitly** based on image source
- **Always restart deployments** after local image updates
- **Document image sources** in deployment comments

### Local Development

- **Separate patch files** for environment-specific configurations
- **Lower resource limits** for local development
- **Use consistent naming** for local images across projects
- **Verify builds complete** even after tool timeouts

### Troubleshooting

- **Follow systematic framework** - Events → Describe → Logs sequence
- **Use ephemeral debug containers** for minimal/distroless images
- **Check events first** with `kubectl describe pod` for scheduler/kubelet messages
- **Document common issues** for team reference

## 2025 Kubernetes Updates

### Image Pull Policy Changes (v1.33)

- **Enhanced security**: Kubelet now verifies pod credentials before using cached images
- **Backward compatibility**: Existing `imagePullPolicy` behavior preserved
- **Security improvement**: Addresses 10-year-old image access security issue

### Deployment Best Practices Evolution

- **Rolling restart**: `kubectl rollout restart` is the standard approach for force updates
- **Image verification**: More stringent validation of image access permissions
- **Local development**: Enhanced support for hybrid local/remote image workflows