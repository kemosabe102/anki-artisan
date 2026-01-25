# Kubernetes Security Patterns

**Category**: security
**Domain**: Kubernetes deployment security hardening and threat mitigation
**Confidence**: 0.95 (based on industry best practices and CNI documentation)
**Last Updated**: 2025-10-24T00:00:00Z
**Agent**: deployment-release

---

## Overview

This documentation covers security hardening patterns for Kubernetes deployments, focusing on defense-in-depth strategies: network isolation, minimal attack surface, secret protection, and immutability enforcement. These patterns form the foundation of a zero-trust security posture in Kubernetes environments.

**Key Concepts**:

- **Default Deny Network Policies**: Block ALL traffic by default, explicitly allow only required flows (prevent lateral movement)
- **Distroless Images**: Remove shell, package managers, and debugging tools to eliminate 80-90% of CVE exposure
- **Secret Rotation Safety**: Prevent accidental password rotation through explicit flags and validation gates
- **ConfigMap Immutability**: Use content-hash suffixes and immutable flags to prevent runtime configuration tampering

---

## Core Frameworks

### Framework 1: Network Policy Defense-in-Depth

**Purpose**: Implement zero-trust network segmentation to prevent lateral movement and data exfiltration after pod compromise.

**When to Use**:

- All production deployments (no exceptions)
- Multi-tenant clusters (namespace isolation)
- External-facing services (ingress/egress control)
- Compliance requirements (PCI-DSS, HIPAA, SOC2)

**Components**:

1. **Default Deny Policy**: Block ALL ingress and egress traffic at namespace level
2. **Allow Policies**: Explicitly whitelist required traffic flows with pod selectors
3. **CNI Validation**: Verify Calico/Cilium/Weave Net support before applying policies

**How to Apply**:

1. **Create default deny policy first** (apply to all namespaces):

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {} # Empty = applies to ALL pods in namespace
  policyTypes:
    - Ingress
    - Egress
```

2. **Add explicit allow policies** (specific pod-to-pod communication):

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-api-to-db
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: postgres # Target pods
  policyTypes:
    - Ingress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: production
          podSelector:
            matchLabels:
              app: api # Source pods (AND operator with namespace)
      ports:
        - protocol: TCP
          port: 5432
```

3. **Allow DNS and essential services** (required for functionality):

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-dns-egress
  namespace: production
spec:
  podSelector: {} # All pods need DNS
  policyTypes:
    - Egress
  egress:
    - to:
        - namespaceSelector:
            matchLabels:
              name: kube-system
          podSelector:
            matchLabels:
              k8s-app: kube-dns
      ports:
        - protocol: UDP
          port: 53
```

**Threat Mitigation**:

- **Lateral Movement**: Attacker compromises 1 pod → Cannot reach other pods without explicit policy
- **Data Exfiltration**: Default deny egress blocks external communication unless whitelisted
- **Port Scanning**: Empty policy blocks all ingress, prevents service discovery

**CNI Compatibility Check**:

```bash
# Verify CNI plugin supports NetworkPolicy
kubectl get nodes -o jsonpath='{.items[*].spec.podCIDR}'
kubectl describe node | grep -i cni

# Common CNI plugins with NetworkPolicy support:
# - Calico (most feature-rich, advanced policies)
# - Cilium (eBPF-based, high performance)
# - Weave Net (simple, easy to set up)
# - Flannel (NO NetworkPolicy support)
```

**Source**: Kubernetes Network Policies Documentation, Calico Security Best Practices

---

### Framework 2: Distroless Images for Attack Surface Reduction

**Purpose**: Eliminate 80-90% of CVE exposure by removing shell, package managers, and unnecessary binaries from container images.

**When to Use**:

- All production container images (especially external-facing services)
- Security-critical applications (authentication, payment processing)
- Compliance-driven environments (reduces attack vectors)
- Long-running services (limits runtime tampering)

**Components**:

1. **Multi-Stage Build**: Compile in full image, copy binaries to distroless base
2. **Distroless Base Images**: Google-maintained minimal runtime images (gcr.io/distroless/)
3. **Ephemeral Debug Containers**: kubectl debug for troubleshooting (no shell in main container)

**How to Apply**:

1. **Multi-stage Dockerfile** (build → distroless runtime):

```dockerfile
# Stage 1: Build stage with full toolchain
FROM python:3.13-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --target=/app/packages -r requirements.txt
COPY src/ /app/src/

# Stage 2: Distroless runtime (NO shell, NO package manager)
FROM gcr.io/distroless/python3-debian12:nonroot
WORKDIR /app
COPY --from=builder /app/packages /app/packages
COPY --from=builder /app/src /app/src
ENV PYTHONPATH=/app/packages
USER nonroot:nonroot
ENTRYPOINT ["python3", "/app/src/main.py"]
```

2. **Choose appropriate distroless variant**:

```yaml
# Available distroless base images:
- gcr.io/distroless/static-debian12:nonroot # Static binaries (Go, Rust)
- gcr.io/distroless/base-debian12:nonroot # glibc + minimal libs
- gcr.io/distroless/python3-debian12:nonroot # Python runtime only
- gcr.io/distroless/java17-debian12:nonroot # Java 17 runtime
- gcr.io/distroless/nodejs20-debian12:nonroot # Node.js 20 runtime

# :nonroot tag = runs as UID 65532 (security best practice)
```

3. **Debug with ephemeral containers** (no shell in main container):

```bash
# Attach debug container to running distroless pod
kubectl debug -it my-pod --image=busybox:1.36 --target=my-container

# Copy files for local inspection
kubectl cp my-pod:/app/config.json ./config.json

# View logs without exec
kubectl logs my-pod --tail=100 --follow
```

**Threat Mitigation**:

- **Shell Access Exploits**: No bash/sh = attacker cannot execute arbitrary commands
- **Privilege Escalation**: No package manager (apt/yum) = cannot install malicious tools
- **Supply Chain Attacks**: Minimal dependencies = reduced third-party library exposure
- **Zero-Day Exploits**: 80-90% fewer binaries = smaller CVE attack surface

**Performance Benefits**:

- **Image Size**: 50-200MB (distroless) vs 500MB-1GB (alpine/debian)
- **Startup Time**: 30-50% faster (fewer layers to unpack)
- **Scan Time**: 70% faster security scanning (fewer packages to analyze)

**Trade-offs**:

- ⚠️ **Debugging Complexity**: Requires kubectl debug instead of kubectl exec
- ⚠️ **Learning Curve**: Team must adapt to ephemeral debug workflows
- ⚠️ **Tool Compatibility**: Some legacy tools expect shell access

**Source**: Google Distroless GitHub, NIST Container Security Guide SP 800-190

---

### Framework 3: Secret Management and Rotation Safety

**Purpose**: Protect sensitive credentials through base64 encoding, rotation safeguards, and validation gates to prevent accidental exposure or breakage.

**When to Use**:

- Database passwords, API keys, TLS certificates
- Service account tokens, OAuth client secrets
- Encryption keys, signing keys
- Any credential rotation scenario

**Components**:

1. **Cross-Platform Base64 Encoding**: Handle Windows/Linux newline differences
2. **Rotation Safety Gates**: Explicit flags or environment variables required
3. **Security File Protection**: chmod 600 for secrets YAML files
4. **Validation Before Sourcing**: Prevent code injection attacks

**How to Apply**:

1. **Safe base64 encoding** (cross-platform):

```bash
# Function handles Windows CRLF and Linux LF
safe_base64() {
  local input="$1"
  if command -v base64 &> /dev/null; then
    # macOS base64 uses -w 0 for no wrapping
    echo -n "$input" | base64 | tr -d '\n\r'
  else
    # Windows Git Bash fallback
    echo -n "$input" | openssl base64 -A
  fi
}

# Usage
DB_PASSWORD_B64=$(safe_base64 "my-secure-password")
echo "  password: $DB_PASSWORD_B64" >> k8s/secrets.yaml
```

2. **Rotation safety with explicit flags**:

```bash
# secrets-manager.sh script pattern
ALLOW_ROTATION="${ALLOW_ROTATION:-false}"

rotate_password() {
  local service="$1"

  if [[ "$ALLOW_ROTATION" != "true" ]]; then
    echo "❌ Password rotation blocked. Set ALLOW_ROTATION=true to proceed."
    echo "This prevents accidental rotation that breaks active connections."
    exit 1
  fi

  echo "🔄 Rotating $service password..."
  # Generate new password, update secrets, restart pods
}

# Safe invocation
ALLOW_ROTATION=true ./scripts/rotate-db-password.sh postgres
```

3. **Security file protection**:

```bash
# Apply restrictive permissions to secrets files
chmod 600 k8s/secrets.yaml
chmod 600 k8s/tls-certs/
chown $(whoami):$(whoami) k8s/secrets.yaml

# Add to .gitignore
echo "k8s/secrets.yaml" >> .gitignore
echo "k8s/tls-certs/*.key" >> .gitignore
```

4. **Validation before sourcing**:

```bash
# Prevent code injection when sourcing .env files
validate_env_file() {
  local env_file="$1"

  # Check for executable content
  if grep -E '^[^#]*(\$\(|\`|;|\||&)' "$env_file"; then
    echo "❌ Detected potential code injection in $env_file"
    exit 1
  fi

  # Check for valid key=value format
  if ! grep -E '^[A-Z_][A-Z0-9_]*=' "$env_file" | grep -v '^#'; then
    echo "❌ Invalid environment variable format in $env_file"
    exit 1
  fi

  echo "✅ $env_file validation passed"
}

# Safe sourcing
validate_env_file .env
source .env
```

**Threat Mitigation**:

- **Accidental Exposure**: chmod 600 prevents other users from reading secrets
- **Git Leaks**: .gitignore prevents committing secrets to version control
- **Code Injection**: Validation blocks malicious commands in .env files
- **Rotation Breakage**: Explicit flags prevent unintended password changes during active sessions

**Kubernetes Secret Best Practices**:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-credentials
  namespace: production
type: Opaque
data:
  # Base64-encoded values (use safe_base64 function)
  username: cG9zdGdyZXM=
  password: <base64-encoded-password>
stringData:
  # Plain text (Kubernetes encodes automatically)
  connection-string: 'postgresql://user:pass@localhost/db'
---
# Pod mounts secret as environment variable
apiVersion: v1
kind: Pod
spec:
  containers:
    - name: app
      env:
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: password
```

**Source**: Kubernetes Secrets Documentation, OWASP Secrets Management Cheat Sheet

---

### Framework 4: ConfigMap Immutability and Change Tracking

**Purpose**: Prevent runtime configuration tampering and enable automatic pod restarts on configuration changes through hash-suffix mechanism or native immutability.

**When to Use**:

- Application configuration files (immutable: true for static configs)
- Hash suffixes for configs that change frequently (Kustomize pattern)
- Certificate Authority certificates (immutable: true)
- Feature flags and environment-specific settings (hash suffix)

**Components**:

1. **Hash Suffix Mechanism**: Kustomize appends content hash to ConfigMap name
2. **Native Immutability**: immutable: true makes ConfigMap read-only after creation
3. **Automatic Pod Restart**: Deployment references change when hash changes

**How to Apply**:

1. **Kustomize hash suffix pattern** (changing configurations):

```yaml
# kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

configMapGenerator:
  - name: app-config # Kustomize adds hash suffix: app-config-6f7d8c9b4
    files:
      - config.yaml
    options:
      disableNameSuffixHash: false # Enable hash suffix

resources:
  - deployment.yaml
# Generated ConfigMap name: app-config-6f7d8c9b4
# Deployment automatically references new name when config changes
```

2. **Native immutability** (static configurations):

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: ca-certificates
  namespace: production
immutable: true # Cannot be updated (must delete and recreate)
data:
  ca.crt: |
    -----BEGIN CERTIFICATE-----
    MIID...
    -----END CERTIFICATE-----
```

3. **Deployment with hash-suffixed ConfigMap**:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
spec:
  template:
    spec:
      containers:
        - name: api
          envFrom:
            - configMapRef:
                name: app-config # Kustomize replaces with app-config-6f7d8c9b4
          volumeMounts:
            - name: config
              mountPath: /etc/app/config.yaml
              subPath: config.yaml
      volumes:
        - name: config
          configMap:
            name: app-config # Hash suffix triggers rolling update
```

4. **Update workflow with automatic restart**:

```bash
# 1. Modify configuration file
vim k8s/overlays/production/config.yaml

# 2. Apply with Kustomize (generates new hash)
kubectl apply -k k8s/overlays/production/
# Output: configmap/app-config-8a9b4c5d6 created
#         deployment.apps/api configured

# 3. Rolling update triggered automatically
kubectl rollout status deployment/api
# New pods mount app-config-8a9b4c5d6
# Old ConfigMap app-config-6f7d8c9b4 remains (supports rollback)
```

**Threat Mitigation**:

- **Runtime Tampering**: immutable: true prevents attackers from modifying mounted configs
- **Configuration Drift**: Hash suffix ensures pods always restart with correct config
- **Rollback Safety**: Old ConfigMaps preserved, enabling instant rollback
- **Change Tracking**: Git history + hash suffix creates audit trail

**Performance Benefits**:

- **API Server Load**: Immutable ConfigMaps cached aggressively (90% reduced etcd watches)
- **Read Performance**: 30-40% faster reads for immutable ConfigMaps
- **Network Traffic**: Reduced reconciliation loops

**Decision Matrix**:

```
Configuration Type          | Pattern           | Rationale
----------------------------|-------------------|---------------------------
CA certificates             | immutable: true   | Never changes, max performance
Database connection strings | Hash suffix       | Changes per environment
Feature flags              | Hash suffix       | Frequent updates, need restarts
Static API endpoints       | immutable: true   | Rarely changes
Environment-specific vars  | Hash suffix       | Different per overlay
```

**Source**: Kubernetes ConfigMap Immutability KEP, Kustomize Documentation

---

## Processes & Workflows

### Workflow 1: Secure Deployment Pipeline

**Trigger Conditions**:

- New feature deployment to production
- Security patch rollout
- Configuration update requiring pod restart
- Certificate rotation

**Steps**:

1. **Network Policy Validation**:
   - **Input**: Deployment YAML, namespace, required network flows
   - **Output**: Default deny policy + explicit allow policies
   - **Rationale**: Establish zero-trust perimeter before deploying workload

2. **Image Security Hardening**:
   - **Input**: Application source code, dependencies
   - **Output**: Distroless multi-stage Dockerfile
   - **Rationale**: Minimize attack surface before pushing to registry

3. **Secret Management**:
   - **Input**: Database passwords, API keys, TLS certificates
   - **Output**: secrets.yaml with base64-encoded values, chmod 600
   - **Rationale**: Protect credentials during deployment process

4. **ConfigMap Immutability Assessment**:
   - **Input**: Configuration files, change frequency
   - **Output**: Kustomize configMapGenerator or immutable: true ConfigMap
   - **Rationale**: Prevent runtime tampering, enable automatic restarts

5. **Pre-Deployment Validation**:
   - **Input**: All manifests (deployments, services, policies, secrets)
   - **Output**: kubectl dry-run results, policy validation
   - **Rationale**: Catch errors before impacting production

6. **Rolling Deployment**:
   - **Input**: Validated manifests
   - **Output**: Gradual pod replacement with health checks
   - **Rationale**: Zero-downtime deployment with automatic rollback

**Success Criteria**:

- ✅ Default deny network policy applied to namespace
- ✅ All images use distroless base (verified with `docker inspect`)
- ✅ No secrets committed to Git (validated with git-secrets hook)
- ✅ ConfigMaps use hash suffix or immutable flag
- ✅ All pods pass health checks and readiness probes
- ✅ Zero downtime during deployment

**Failure Handling**:

- If network policy fails CNI check → Use namespace labels for soft isolation
- If distroless build fails → Debug with intermediate builder stage
- If secret validation fails → Block deployment, notify security team
- If health checks fail → Automatic rollback to previous ReplicaSet

**Example Execution**:

```bash
# 1. Apply network policies first
kubectl apply -f k8s/network-policies/default-deny.yaml
kubectl apply -f k8s/network-policies/allow-api-to-db.yaml

# 2. Build and push distroless image
docker build -t gcr.io/project/api:v1.2.3 -f Dockerfile.distroless .
docker push gcr.io/project/api:v1.2.3

# 3. Create secrets (validated and protected)
./scripts/generate-secrets.sh --validate
kubectl apply -f k8s/secrets.yaml

# 4. Deploy with Kustomize (hash-suffixed ConfigMaps)
kubectl apply -k k8s/overlays/production/

# 5. Monitor rollout
kubectl rollout status deployment/api -n production
```

---

### Workflow 2: Security Incident Response

**Trigger Conditions**:

- CVE disclosure affecting deployed images
- Suspected pod compromise (anomalous network traffic)
- Failed secret rotation
- Network policy violation detected

**Steps**:

1. **Isolate Affected Pods**:
   - **Input**: Pod name, namespace, compromise indicators
   - **Output**: Quarantine network policy, pod labeled for isolation
   - **Rationale**: Prevent lateral movement while investigating

2. **Forensic Analysis**:
   - **Input**: Isolated pod, logs, network flow logs
   - **Output**: Root cause analysis, attack timeline
   - **Rationale**: Understand attack vector before remediation

3. **Patch and Rebuild**:
   - **Input**: CVE details, updated dependencies
   - **Output**: New distroless image with fixes
   - **Rationale**: Eliminate vulnerability from image

4. **Secret Rotation**:
   - **Input**: Potentially compromised credentials
   - **Output**: New secrets, updated pods
   - **Rationale**: Revoke attacker access to credentials

5. **Redeployment with Enhanced Policies**:
   - **Input**: Patched image, rotated secrets, stricter network policies
   - **Output**: Secure deployment with additional monitoring
   - **Rationale**: Prevent recurrence with defense-in-depth

**Success Criteria**:

- ✅ Compromised pods isolated within 5 minutes
- ✅ Root cause identified and documented
- ✅ Patched image deployed with zero vulnerabilities
- ✅ All secrets rotated and old credentials revoked
- ✅ Enhanced network policies prevent similar attacks

**Failure Handling**:

- If isolation fails → Manually cordon node and drain pods
- If forensics inconclusive → Preserve pod for deeper analysis (kubectl debug)
- If patch unavailable → Apply compensating controls (WAF rules, network policies)
- If rotation fails → Initiate emergency credential revocation

**Example Execution**:

```bash
# 1. Quarantine compromised pod
kubectl label pod suspicious-pod-abc123 quarantine=true
kubectl apply -f - <<EOF
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: quarantine-policy
spec:
  podSelector:
    matchLabels:
      quarantine: "true"
  policyTypes:
  - Ingress
  - Egress
  # No ingress/egress rules = complete isolation
EOF

# 2. Collect forensic data
kubectl logs suspicious-pod-abc123 --all-containers > forensics.log
kubectl describe pod suspicious-pod-abc123 > pod-details.txt

# 3. Rebuild with patched dependencies
docker build -t gcr.io/project/api:v1.2.4-patched -f Dockerfile.distroless .
docker scan gcr.io/project/api:v1.2.4-patched  # Verify no critical CVEs

# 4. Rotate secrets with explicit flag
ALLOW_ROTATION=true ./scripts/rotate-all-secrets.sh

# 5. Deploy patched version
kubectl set image deployment/api api=gcr.io/project/api:v1.2.4-patched
kubectl rollout status deployment/api
```

---

## Decision Trees

### Decision 1: Network Policy Scope Selection

```
IF deploying to production namespace
  THEN apply default deny policy to entire namespace
  BECAUSE zero-trust requires explicit allow for all traffic

ELSE IF deploying to development namespace
  THEN apply default deny policy only to specific pods
  BECAUSE developers need flexibility for debugging

ELSE IF CNI plugin does not support NetworkPolicy
  THEN use namespace labels + service mesh (Istio/Linkerd)
  BECAUSE network policies have no effect without CNI support

ELSE
  THEN warn user and apply namespace isolation only
  BECAUSE soft isolation better than no isolation
```

**Example Scenarios**:

1. **Scenario**: Production API deployment → **Decision**: Default deny for entire `production` namespace + explicit allow for API→DB, API→Redis
2. **Scenario**: Development environment with Flannel CNI → **Decision**: Use namespace labels, recommend Calico upgrade
3. **Scenario**: Multi-tenant SaaS platform → **Decision**: Default deny per tenant namespace + cross-namespace policies for shared services

---

### Decision 2: Distroless vs Alpine Base Image

```
IF application requires shell access for health checks
  THEN use Alpine with minimal utilities
  BECAUSE distroless has no shell

ELSE IF application is security-critical (auth, payments)
  THEN use distroless + ephemeral debug containers
  BECAUSE 80-90% CVE reduction outweighs debugging complexity

ELSE IF team lacks kubectl debug experience
  THEN use Alpine initially, migrate to distroless after training
  BECAUSE operational readiness > security gains

ELSE IF image size and startup time are critical
  THEN use distroless static (for Go/Rust) or language-specific variant
  BECAUSE 50-200MB vs 500MB-1GB significantly impacts scale

ELSE
  THEN default to distroless
  BECAUSE security-by-default principle
```

**Example Scenarios**:

1. **Scenario**: Payment processing API → **Decision**: Distroless Python with ephemeral busybox for debugging
2. **Scenario**: Internal admin tool with frequent debugging → **Decision**: Alpine 3.19 with minimal shell utilities
3. **Scenario**: Stateless microservice at scale (1000+ pods) → **Decision**: Distroless static for 3x faster startup

---

### Decision 3: Secret Rotation Strategy

```
IF rotating database password
  THEN require ALLOW_ROTATION=true flag
  BECAUSE accidental rotation breaks active connections

ELSE IF rotating API key with gradual rollout
  THEN dual-key approach (old + new keys valid for 24h)
  BECAUSE zero-downtime rotation

ELSE IF rotating TLS certificate
  THEN use ConfigMap with immutable: false + reload signal
  BECAUSE pods need graceful certificate refresh

ELSE IF rotating OAuth client secret
  THEN coordinate with identity provider first
  BECAUSE external dependency requires sync

ELSE
  THEN validate secrets before applying
  BECAUSE prevention better than rollback
```

**Example Scenarios**:

1. **Scenario**: Postgres password rotation during peak traffic → **Decision**: Maintenance window + ALLOW_ROTATION=true + connection pooler restart
2. **Scenario**: JWT signing key rotation → **Decision**: Dual-key validation for 24h, then remove old key
3. **Scenario**: TLS cert expiring in 7 days → **Decision**: Automate with cert-manager, immutable: false ConfigMap for reload

---

### Decision 4: ConfigMap Immutability Pattern

```
IF configuration changes frequently (feature flags)
  THEN use Kustomize hash suffix pattern
  BECAUSE automatic pod restart on config change

ELSE IF configuration is static (CA certificates)
  THEN use immutable: true ConfigMap
  BECAUSE performance optimization + tamper prevention

ELSE IF rolling back config is common
  THEN use hash suffix pattern
  BECAUSE old ConfigMaps preserved for instant rollback

ELSE IF config size > 1MB
  THEN use ConfigMap with immutable: true (if static) OR volume mount (if dynamic)
  BECAUSE ConfigMaps limited to 1MB, immutability enables aggressive caching

ELSE
  THEN default to hash suffix pattern
  BECAUSE change tracking + automatic restarts cover most use cases
```

**Example Scenarios**:

1. **Scenario**: Nginx configuration with frequent rule changes → **Decision**: Hash suffix, rolling update every config change
2. **Scenario**: Root CA bundle (changes once per year) → **Decision**: immutable: true, 40% read performance boost
3. **Scenario**: Application config with rollback requirement → **Decision**: Hash suffix, maintain last 5 ConfigMap versions

---

## Best Practices

### Practice 1: Layered Network Security

**Principle**: Defense-in-depth with multiple network isolation layers (namespace, pod selector, port restrictions)

**Implementation**:

- Start with default deny at namespace level (broadest scope)
- Add pod selector policies for specific services (targeted scope)
- Use port restrictions to limit attack surface (protocol-level control)
- Combine namespace + pod selectors for cross-namespace communication

**Benefits**:

- ✅ Lateral movement blocked at multiple layers
- ✅ Explicit documentation of required traffic flows
- ✅ Reduced blast radius of compromised pod

**Trade-offs**:

- ⚠️ Increased policy complexity (requires policy management tooling)
- ⚠️ Debugging network issues requires policy analysis
- ⚠️ CNI plugin dependency (policies ineffective without support)

**Example**:

```yaml
# Layer 1: Namespace-level default deny
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress

---
# Layer 2: Service-specific allow (pod selector)
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-api
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: frontend
      ports:
        - protocol: TCP
          port: 8080

---
# Layer 3: External access (ingress controller only)
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-ingress-to-frontend
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: frontend
  policyTypes:
    - Ingress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: ingress-nginx
          podSelector:
            matchLabels:
              app: ingress-nginx
      ports:
        - protocol: TCP
          port: 80
```

---

### Practice 2: Immutable Infrastructure with Distroless

**Principle**: Treat containers as immutable artifacts - no runtime modifications, rebuild and redeploy for changes

**Implementation**:

- Use distroless base images to prevent runtime package installation
- Multi-stage builds with all dependencies baked in at build time
- Ephemeral debug containers for troubleshooting (no persistent shell access)
- Configuration changes via ConfigMaps/Secrets (external to image)

**Benefits**:

- ✅ 80-90% reduction in CVE exposure (no shell, no package managers)
- ✅ Prevents privilege escalation attacks (no tools to install malware)
- ✅ Forces proper CI/CD discipline (changes via Git, not kubectl exec)

**Trade-offs**:

- ⚠️ Debugging requires kubectl debug workflow (learning curve)
- ⚠️ Cannot hotfix production pods (must rebuild and redeploy)
- ⚠️ Requires robust CI/CD pipeline (slow builds impact iteration speed)

**Example**:

```dockerfile
# Multi-stage build for Python application
FROM python:3.13-slim AS builder
WORKDIR /app

# Install dependencies in builder stage
COPY requirements.txt .
RUN pip install --no-cache-dir --target=/app/packages -r requirements.txt

# Copy application code
COPY src/ /app/src/

# Runtime stage: distroless (no shell, no package manager)
FROM gcr.io/distroless/python3-debian12:nonroot
WORKDIR /app

# Copy artifacts from builder (only what's needed)
COPY --from=builder /app/packages /app/packages
COPY --from=builder /app/src /app/src

# Set Python path and run as nonroot user (UID 65532)
ENV PYTHONPATH=/app/packages
USER nonroot:nonroot
ENTRYPOINT ["python3", "/app/src/main.py"]

# Debug without shell access:
# kubectl debug -it my-pod --image=busybox:1.36 --target=my-container
```

---

### Practice 3: Secrets Lifecycle Management

**Principle**: Treat secrets as first-class citizens with validation, rotation, and audit trails

**Implementation**:

- Base64 encoding with cross-platform compatibility (safe_base64 function)
- Explicit rotation flags to prevent accidental changes (ALLOW_ROTATION=true)
- File permissions (chmod 600) and .gitignore for secrets files
- Validation before sourcing .env files (prevent code injection)
- Kubernetes Secrets with restrictive RBAC (least privilege access)

**Benefits**:

- ✅ Prevents accidental credential exposure (validation gates)
- ✅ Audit trail for rotation events (explicit flags logged)
- ✅ Cross-platform compatibility (Windows/Linux/macOS)

**Trade-offs**:

- ⚠️ Extra friction for legitimate rotation (requires explicit flag)
- ⚠️ Manual validation steps (automation reduces human error)
- ⚠️ Base64 is encoding, not encryption (use sealed-secrets for encryption)

**Example**:

```bash
#!/bin/bash
# scripts/generate-secrets.sh

set -euo pipefail

ALLOW_ROTATION="${ALLOW_ROTATION:-false}"
SECRETS_FILE="k8s/secrets.yaml"

# Cross-platform base64 encoding
safe_base64() {
  local input="$1"
  if command -v base64 &> /dev/null; then
    echo -n "$input" | base64 | tr -d '\n\r'
  else
    echo -n "$input" | openssl base64 -A
  fi
}

# Validate before rotation
if [[ -f "$SECRETS_FILE" ]] && [[ "$ALLOW_ROTATION" != "true" ]]; then
  echo "❌ Secrets file exists. Set ALLOW_ROTATION=true to rotate."
  exit 1
fi

# Generate secrets
DB_PASSWORD=$(openssl rand -base64 32)
API_KEY=$(openssl rand -hex 32)

# Create secrets YAML
cat > "$SECRETS_FILE" <<EOF
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
  namespace: production
type: Opaque
data:
  db-password: $(safe_base64 "$DB_PASSWORD")
  api-key: $(safe_base64 "$API_KEY")
EOF

# Protect secrets file
chmod 600 "$SECRETS_FILE"

echo "✅ Secrets generated: $SECRETS_FILE"
echo "⚠️  Apply with: kubectl apply -f $SECRETS_FILE"
```

---

## Anti-Patterns

### Anti-Pattern 1: Privileged Containers Without Justification

**Problem**: Running containers with `privileged: true` or `hostNetwork: true` unnecessarily expands attack surface and bypasses Kubernetes security controls.

**Detection**:

- 🔴 `securityContext.privileged: true` in pod spec
- 🔴 `hostNetwork: true`, `hostPID: true`, or `hostIPC: true`
- 🔴 `allowPrivilegeEscalation: true` without clear justification
- 🔴 Capabilities like `CAP_SYS_ADMIN` granted broadly

**Consequences**:

- ❌ Container can access host resources (filesystem, processes, network)
- ❌ Bypasses network policies (hostNetwork allows direct host IP access)
- ❌ Kernel exploits can compromise entire node
- ❌ Breaks namespace isolation (shared PID/IPC namespace)

**Better Approach**:

```yaml
✅ Preferred Pattern (Least Privilege):
apiVersion: v1
kind: Pod
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 65532  # nonroot user
    fsGroup: 65532
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: app
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
        - ALL
        add:
        - NET_BIND_SERVICE  # Only if needed for port <1024

❌ Anti-Pattern (Overprivileged):
apiVersion: v1
kind: Pod
spec:
  hostNetwork: true  # ❌ Bypasses network policies
  hostPID: true      # ❌ Can see all host processes
  containers:
  - name: app
    securityContext:
      privileged: true  # ❌ Full host access
      capabilities:
        add:
        - SYS_ADMIN  # ❌ Kernel-level operations
```

**Migration Strategy**:

1. Audit existing pods: `kubectl get pods -o json | jq '.items[].spec.securityContext.privileged'`
2. Identify legitimate use cases (CNI plugins, monitoring agents)
3. Apply least privilege: Drop ALL capabilities, add only required ones
4. Use PodSecurityStandards to enforce cluster-wide: `kubectl label namespace production pod-security.kubernetes.io/enforce=restricted`

---

### Anti-Pattern 2: Storing Secrets in ConfigMaps

**Problem**: ConfigMaps are not encrypted at rest and have weaker RBAC controls than Secrets, making them unsuitable for sensitive data.

**Detection**:

- 🔴 Database passwords in ConfigMap data fields
- 🔴 API keys stored as plain text in ConfigMaps
- 🔴 TLS private keys in ConfigMap (should be in Secret with type: kubernetes.io/tls)
- 🔴 OAuth client secrets in ConfigMaps

**Consequences**:

- ❌ Credentials visible to anyone with ConfigMap read access (broad RBAC)
- ❌ Not encrypted at rest (etcd stores ConfigMaps as plain text)
- ❌ Audit logs don't flag ConfigMap access as sensitive
- ❌ Secret scanning tools miss credentials in ConfigMaps

**Better Approach**:

```yaml
✅ Preferred Pattern (Kubernetes Secret):
apiVersion: v1
kind: Secret
metadata:
  name: db-credentials
  namespace: production
type: Opaque
data:
  username: cG9zdGdyZXM=  # Base64: postgres
  password: <base64-encoded-password>
---
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: app
    env:
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: db-credentials
          key: password

❌ Anti-Pattern (ConfigMap with Credentials):
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  db-password: "my-secret-password"  # ❌ Plain text, visible to all
  api-key: "sk-1234567890"           # ❌ Not encrypted at rest
```

**Migration Strategy**:

1. Identify ConfigMaps with credentials: `kubectl get configmaps -o yaml | grep -i "password\|key\|token"`
2. Create Secrets with proper type: `kubectl create secret generic db-creds --from-literal=password=...`
3. Update pod specs to reference Secrets instead of ConfigMaps
4. Delete old ConfigMaps after verifying pods work: `kubectl delete configmap app-config`
5. Enable Secrets encryption at rest: Configure `EncryptionConfiguration` in kube-apiserver

---

### Anti-Pattern 3: Implicit Network Allow (No Default Deny)

**Problem**: Without default deny policies, all pods can communicate freely, enabling lateral movement after compromise.

**Detection**:

- 🔴 Namespace has no NetworkPolicy resources: `kubectl get networkpolicy -n production` returns empty
- 🔴 NetworkPolicies exist but don't cover all pods (gaps in podSelector)
- 🔴 Only ingress policies (egress still open for data exfiltration)
- 🔴 Policies applied after deploying workloads (window of vulnerability)

**Consequences**:

- ❌ Compromised pod can scan and attack other services (lateral movement)
- ❌ Attacker can exfiltrate data to external servers (no egress control)
- ❌ Difficult to audit allowed traffic flows (implicit allow = no documentation)
- ❌ Compliance violations (PCI-DSS, HIPAA require network segmentation)

**Better Approach**:

```yaml
✅ Preferred Pattern (Default Deny First):
# Step 1: Apply default deny BEFORE deploying workloads
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {} # Applies to ALL pods
  policyTypes:
    - Ingress
    - Egress

---
# Step 2: Explicitly allow required traffic
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-api-to-db
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: postgres
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: api
      ports:
        - protocol: TCP
          port: 5432

❌ Anti-Pattern (Implicit Allow):
# No default deny policy in namespace
# Pods can access any service on any port
# Lateral movement unrestricted
```

**Migration Strategy**:

1. Document current traffic flows: `kubectl logs -n production --all-containers | grep -i "connection"`
2. Create default deny policy in test namespace first: `kubectl apply -f default-deny.yaml -n staging`
3. Add explicit allow policies based on observed traffic
4. Verify application functionality with policies: Run integration tests
5. Roll out to production during maintenance window
6. Monitor policy violations: `kubectl logs -n kube-system calico-node-xxx | grep "policy denied"`

---

### Anti-Pattern 4: Mutable ConfigMaps for Static Configuration

**Problem**: Allowing runtime modification of ConfigMaps enables attackers to tamper with configuration without triggering pod restarts or audit alerts.

**Detection**:

- 🔴 ConfigMaps with static data (CA certs, static endpoints) lack `immutable: true`
- 🔴 ConfigMap updates don't trigger pod restarts (hash suffix missing)
- 🔴 Multiple manual `kubectl edit configmap` operations (drift from Git)
- 🔴 ConfigMap size >100KB without compression (performance impact)

**Consequences**:

- ❌ Attacker can modify mounted config without detection (no pod restart)
- ❌ Configuration drift from version control (manual kubectl edits)
- ❌ Performance degradation (etcd watches on large mutable ConfigMaps)
- ❌ Rollback complexity (no versioned ConfigMap history)

**Better Approach**:

```yaml
✅ Preferred Pattern (Immutable for Static Configs):
apiVersion: v1
kind: ConfigMap
metadata:
  name: ca-certificates
  namespace: production
immutable: true # Cannot be modified (delete and recreate only)
data:
  ca.crt: |
    -----BEGIN CERTIFICATE-----
    MIID...
    -----END CERTIFICATE-----

---
✅ Preferred Pattern (Hash Suffix for Dynamic Configs):
# kustomization.yaml
configMapGenerator:
  - name: app-config
    files:
      - config.yaml
    options:
      disableNameSuffixHash: false # Kustomize adds hash: app-config-6f7d8c9b4

# Deployment references configMap by base name
# Kustomize replaces with hashed name (triggers rolling update)

❌ Anti-Pattern (Mutable Static Config):
apiVersion: v1
kind: ConfigMap
metadata:
  name: ca-certificates
# immutable: true missing - can be modified at runtime
data:
  ca.crt: |
    -----BEGIN CERTIFICATE-----
    ...
```

**Migration Strategy**:

1. Identify static ConfigMaps: `kubectl get configmaps -o yaml | grep -A5 "kind: ConfigMap"`
2. Add `immutable: true` to CA certs, static endpoints, read-only configs
3. Migrate dynamic configs to Kustomize hash suffix pattern: Convert to configMapGenerator
4. Enable admission webhook to enforce immutability: Use OPA/Gatekeeper policy
5. Monitor ConfigMap modifications: Alert on kubectl edit attempts

---

## Integration Points

### Integration 1: CI/CD Pipeline (GitOps)

**Relationship**: deployment-release security patterns integrate with GitOps workflows to enforce security-as-code principles.

**Coordination Pattern**:

- Git repository as single source of truth for manifests
- Kustomize overlays for environment-specific security policies (dev/staging/production)
- Automated validation in CI pipeline (network policy linting, image scanning)
- ArgoCD/Flux syncs validated manifests to cluster (no manual kubectl apply)

**Example Usage**:

```yaml
# .github/workflows/deploy.yml
name: Secure Kubernetes Deployment

on:
  push:
    branches: [main]
    paths: ['k8s/**']

jobs:
  validate-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # 1. Validate network policies (require default deny)
      - name: Validate Network Policies
        run: |
          if ! grep -q "podSelector: {}" k8s/network-policies/default-deny.yaml; then
            echo "❌ Missing default deny policy"
            exit 1
          fi

      # 2. Scan images for vulnerabilities
      - name: Scan Distroless Image
        run: |
          docker pull gcr.io/project/api:${{ github.sha }}
          docker scan gcr.io/project/api:${{ github.sha }} --severity high

      # 3. Validate secrets not in ConfigMaps
      - name: Check Secrets in ConfigMaps
        run: |
          if grep -ri "password\|api.?key" k8s/configmaps/; then
            echo "❌ Credentials found in ConfigMaps"
            exit 1
          fi

      # 4. Apply with Kustomize (hash-suffixed ConfigMaps)
      - name: Deploy to Production
        run: |
          kubectl apply -k k8s/overlays/production/
          kubectl rollout status deployment/api -n production
```

**Dependencies**:

- **Upstream**: Git repository (manifests), container registry (distroless images), secrets manager (Vault/Sealed Secrets)
- **Downstream**: Kubernetes cluster, ArgoCD/Flux, monitoring (Prometheus alerts on policy violations)

---

### Integration 2: Observability and Monitoring

**Relationship**: Security patterns generate telemetry for incident detection and compliance auditing.

**Coordination Pattern**:

- Network policy violations logged to centralized system (Elasticsearch, Splunk)
- Distroless container metrics (CVE count, image size) tracked in Prometheus
- Secret access audited via Kubernetes audit logs (kube-apiserver)
- ConfigMap immutability violations trigger alerts (OPA policy decisions)

**Example Usage**:

```yaml
# prometheus-rules.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: security-alerts
spec:
  groups:
    - name: network-policy-violations
      interval: 30s
      rules:
        - alert: NetworkPolicyDenied
          expr: |
            rate(calico_denied_packets_total[5m]) > 10
          for: 2m
          annotations:
            summary: 'Network policy blocked {{ $value }} packets/sec'
            description: 'Potential lateral movement attempt detected'
          labels:
            severity: warning

    - name: privileged-containers
      interval: 60s
      rules:
        - alert: PrivilegedPodDetected
          expr: |
            kube_pod_container_status_running{container_security_context_privileged="true"} > 0
          for: 1m
          annotations:
            summary: 'Privileged container detected: {{ $labels.pod }}'
            description: 'Overprivileged container violates security policy'
          labels:
            severity: critical

    - name: secret-access
      interval: 60s
      rules:
        - alert: FrequentSecretAccess
          expr: |
            rate(apiserver_audit_event_total{objectRef_resource="secrets",verb="get"}[5m]) > 100
          for: 5m
          annotations:
            summary: 'Abnormal secret access rate detected'
            description: 'Potential credential harvesting attack'
          labels:
            severity: high
```

**Dependencies**:

- **Upstream**: Kubernetes audit logs, CNI plugin (Calico metrics), kube-state-metrics
- **Downstream**: Prometheus, Alertmanager, PagerDuty/Slack (alert routing)

---

### Integration 3: Certificate Management (cert-manager)

**Relationship**: TLS certificate lifecycle automation integrates with ConfigMap immutability patterns for secure certificate distribution.

**Coordination Pattern**:

- cert-manager provisions certificates as Kubernetes Secrets
- ConfigMaps reference certificates for non-TLS use cases (CA bundles)
- Immutable ConfigMaps for CA certificates (long-lived, rarely change)
- Automatic rotation triggers pod restarts (hash suffix pattern)

**Example Usage**:

```yaml
# cert-manager Certificate resource
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: api-tls
  namespace: production
spec:
  secretName: api-tls-secret # Stored as Kubernetes Secret
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer
  dnsNames:
    - api.example.com
  duration: 2160h # 90 days
  renewBefore: 360h # 15 days before expiry

---
# Immutable ConfigMap for CA bundle
apiVersion: v1
kind: ConfigMap
metadata:
  name: ca-certificates
  namespace: production
immutable: true # CA bundle rarely changes
data:
  ca-bundle.crt: |
    -----BEGIN CERTIFICATE-----
    MIID...
    -----END CERTIFICATE-----

---
# Pod mounts both Secret (TLS) and ConfigMap (CA bundle)
apiVersion: v1
kind: Pod
spec:
  containers:
    - name: api
      volumeMounts:
        - name: tls-cert
          mountPath: /etc/tls/
          readOnly: true
        - name: ca-bundle
          mountPath: /etc/ssl/certs/ca-bundle.crt
          subPath: ca-bundle.crt
          readOnly: true
  volumes:
    - name: tls-cert
      secret:
        secretName: api-tls-secret # cert-manager manages
    - name: ca-bundle
      configMap:
        name: ca-certificates # Immutable for security
```

**Dependencies**:

- **Upstream**: cert-manager, Let's Encrypt/internal CA, DNS01/HTTP01 solver
- **Downstream**: Ingress controller (TLS termination), application pods (mTLS)

---

## Validation & Quality Checks

### Check 1: Network Policy Coverage Validation

**What to Validate**: Ensure all namespaces have default deny policies and all pods are covered by at least one allow policy.

**Validation Method**:

1. List all namespaces: `kubectl get namespaces -o name`
2. For each namespace, check for default deny policy:

```bash
kubectl get networkpolicy -n production -o yaml | grep -A2 "podSelector: {}"
```

3. Verify all pods have matching allow policies:

```bash
# Get all pods
kubectl get pods -n production -o jsonpath='{.items[*].metadata.labels}' | jq .

# Check each pod label against NetworkPolicy podSelectors
kubectl get networkpolicy -n production -o yaml | grep -A5 "podSelector:"
```

**Pass Criteria**:

- ✅ Every namespace has at least one NetworkPolicy with `podSelector: {}` and `policyTypes: [Ingress, Egress]`
- ✅ All running pods match at least one allow policy (no uncovered pods)
- ✅ DNS egress allowed for all pods (kube-dns/CoreDNS)

**Fail Criteria**:

- ❌ Namespace missing default deny policy
- ❌ Pods with no matching NetworkPolicy allow rules
- ❌ Overly broad allow policies (e.g., `podSelector: {}` with allow rules = implicit allow)

**Remediation**:

```bash
# Apply default deny to missing namespace
kubectl apply -f - <<EOF
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
EOF

# Verify policy applied
kubectl describe networkpolicy default-deny-all -n production
```

---

### Check 2: Distroless Image Verification

**What to Validate**: Confirm all production images use distroless base and have no shell binaries.

**Validation Method**:

1. List all images in production namespace:

```bash
kubectl get pods -n production -o jsonpath='{.items[*].spec.containers[*].image}' | tr ' ' '\n' | sort -u
```

2. Inspect each image for shell presence:

```bash
docker pull gcr.io/project/api:v1.2.3
docker run --rm gcr.io/project/api:v1.2.3 /bin/sh -c "echo test" 2>&1
# Expected output: "executable file not found" (no shell)
```

3. Check image layers for distroless base:

```bash
docker history gcr.io/project/api:v1.2.3 | grep distroless
```

**Pass Criteria**:

- ✅ All production images based on gcr.io/distroless/\* variants
- ✅ No shell binaries (/bin/sh, /bin/bash) in final image layer
- ✅ Image size <200MB (distroless indicator)

**Fail Criteria**:

- ❌ Images based on alpine, debian, ubuntu (non-distroless)
- ❌ Shell executable found in image
- ❌ Image size >500MB (likely full OS base)

**Remediation**:

```dockerfile
# Convert existing Dockerfile to multi-stage distroless
# Before (Alpine base):
FROM python:3.13-alpine
COPY . /app
CMD ["python", "app.py"]

# After (Distroless):
FROM python:3.13-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --target=/app/packages -r requirements.txt
COPY src/ /app/src/

FROM gcr.io/distroless/python3-debian12:nonroot
WORKDIR /app
COPY --from=builder /app/packages /app/packages
COPY --from=builder /app/src /app/src
ENV PYTHONPATH=/app/packages
USER nonroot:nonroot
ENTRYPOINT ["python3", "/app/src/main.py"]
```

---

### Check 3: Secret Encryption at Rest

**What to Validate**: Verify Kubernetes Secrets are encrypted at rest in etcd (not stored as plain text).

**Validation Method**:

1. Check kube-apiserver configuration for EncryptionConfiguration:

```bash
kubectl get pods -n kube-system kube-apiserver-* -o yaml | grep encryption-provider-config
```

2. Test secret encryption by directly querying etcd:

```bash
# Get etcd pod
ETCD_POD=$(kubectl get pods -n kube-system -l component=etcd -o name | head -n1)

# Query secret directly from etcd (should be encrypted)
kubectl exec -n kube-system $ETCD_POD -- etcdctl \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  get /registry/secrets/production/db-credentials

# Expected: Encrypted blob (binary data), NOT plain text password
```

**Pass Criteria**:

- ✅ EncryptionConfiguration file exists and referenced by kube-apiserver
- ✅ Secrets stored as encrypted blobs in etcd (aescbc, kms, secretbox)
- ✅ Encryption key rotated within last 90 days

**Fail Criteria**:

- ❌ No EncryptionConfiguration in kube-apiserver (secrets stored as plain text)
- ❌ etcd query returns plain text password
- ❌ Encryption key never rotated (stale key risk)

**Remediation**:

```yaml
# /etc/kubernetes/encryption-config.yaml
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
- resources:
  - secrets
  providers:
  - aescbc:
      keys:
      - name: key1
        secret: <base64-encoded-32-byte-key>
  - identity: {}  # Fallback for unencrypted secrets (migration)

# Update kube-apiserver manifest
# /etc/kubernetes/manifests/kube-apiserver.yaml
spec:
  containers:
  - command:
    - kube-apiserver
    - --encryption-provider-config=/etc/kubernetes/encryption-config.yaml
    volumeMounts:
    - name: encryption-config
      mountPath: /etc/kubernetes/encryption-config.yaml
      readOnly: true
  volumes:
  - name: encryption-config
    hostPath:
      path: /etc/kubernetes/encryption-config.yaml

# Recreate all secrets to encrypt (one-time migration)
kubectl get secrets -A -o json | kubectl replace -f -
```

---

## Common Pitfalls & Solutions

| Pitfall                                                | Detection                                                                         | Solution                                                                                                                            |
| ------------------------------------------------------ | --------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| **Network policies applied after workload deployment** | Namespace created → Pods deployed → NetworkPolicy added (window of vulnerability) | Apply default deny policy BEFORE first pod deployment (use namespace creation hook)                                                 |
| **CNI plugin doesn't support NetworkPolicy**           | Policies exist but have no effect (Flannel, some cloud CNIs)                      | Verify CNI support: `kubectl get nodes -o jsonpath='{.items[*].status.nodeInfo.containerRuntimeVersion}'`, migrate to Calico/Cilico |
| **Distroless debugging without kubectl debug**         | Developers exec into pods (fails with "executable not found")                     | Train team on `kubectl debug -it pod --image=busybox --target=container`, provide runbooks                                          |
| **Secret rotation breaks active connections**          | Database password rotated → All connections fail → Outage                         | Require ALLOW_ROTATION=true flag, use connection poolers (PgBouncer), implement dual-key validation period                          |
| **ConfigMap updates don't trigger pod restarts**       | Config changed → Pods mount old version → Behavior unchanged                      | Use Kustomize hash suffix pattern (configMapGenerator), verify deployment references hashed name                                    |
| **Privileged containers for monitoring agents**        | DaemonSets run with `hostNetwork: true` and `privileged: true` unnecessarily      | Use minimal capabilities: `NET_ADMIN` for network monitoring, `SYS_PTRACE` for process inspection (drop ALL, add specific)          |
| **Secrets stored in Git repository**                   | Credentials committed to version control → Exposed in Git history                 | Use .gitignore, git-secrets hook, migrate to sealed-secrets (encrypted in Git)                                                      |
| **Immutable ConfigMaps prevent hot fixes**             | Production issue → Need config change → immutable: true blocks update             | Use immutable: false for configs requiring hot fixes, hash suffix for automatic restarts, emergency kubectl replace workflow        |
| **Network policies too restrictive**                   | Pods can't communicate → Application broken → Rollback policies                   | Start permissive (allow all), add default deny incrementally, use network flow logs (Cilium Hubble) to identify required flows      |

---

## Tools & Resources

### Recommended Tools

1. **Calico**
   - **Purpose**: CNI plugin with advanced NetworkPolicy support (global policies, DNS-based policies, layer 7 rules)
   - **When to Use**: Production clusters requiring fine-grained network segmentation, compliance environments
   - **Documentation**: https://docs.tigera.io/calico/latest/about/

2. **kubectl-netpol (kubectl plugin)**
   - **Purpose**: Interactive NetworkPolicy testing and visualization
   - **When to Use**: Debugging policy configurations, validating allow rules before production
   - **Documentation**: https://github.com/nupam/kubectl-netpol

3. **Trivy**
   - **Purpose**: Vulnerability scanner for container images, Kubernetes manifests, IaC files
   - **When to Use**: CI/CD pipeline, pre-deployment validation, periodic security audits
   - **Documentation**: https://aquasecurity.github.io/trivy/

4. **cert-manager**
   - **Purpose**: Automates TLS certificate provisioning and renewal (Let's Encrypt, internal CA)
   - **When to Use**: All production clusters, ingress TLS, service mesh mTLS
   - **Documentation**: https://cert-manager.io/docs/

5. **Sealed Secrets (Bitnami)**
   - **Purpose**: Encrypt Secrets for safe Git storage (GitOps-compatible)
   - **When to Use**: GitOps workflows, need to version control secrets securely
   - **Documentation**: https://github.com/bitnami-labs/sealed-secrets

6. **OPA Gatekeeper**
   - **Purpose**: Policy enforcement for Kubernetes (admission controller)
   - **When to Use**: Enforce security standards (no privileged pods, require NetworkPolicies, ConfigMap immutability)
   - **Documentation**: https://open-policy-agent.github.io/gatekeeper/

7. **Falco**
   - **Purpose**: Runtime security monitoring (detect anomalous pod behavior)
   - **When to Use**: Production clusters, incident response, compliance auditing
   - **Documentation**: https://falco.org/docs/

### Learning Resources

1. **Kubernetes Network Policy Recipes**: https://github.com/ahmetb/kubernetes-network-policy-recipes
   - **Topic**: Real-world NetworkPolicy examples (deny all, allow DNS, cross-namespace)
   - **Quality**: High (community-maintained, tested patterns)

2. **Google Distroless GitHub**: https://github.com/GoogleContainerTools/distroless
   - **Topic**: Distroless base images, debugging guide, language-specific variants
   - **Quality**: High (official Google project, well-documented)

3. **NIST SP 800-190 (Container Security)**: https://csrc.nist.gov/publications/detail/sp/800-190/final
   - **Topic**: Container security threats, countermeasures, image hardening
   - **Quality**: High (authoritative source, compliance frameworks reference)

4. **OWASP Kubernetes Security Cheat Sheet**: https://cheatsheetseries.owasp.org/cheatsheets/Kubernetes_Security_Cheat_Sheet.html
   - **Topic**: Comprehensive security controls (RBAC, Secrets, network policies, pod security)
   - **Quality**: High (OWASP-maintained, regularly updated)

5. **CIS Kubernetes Benchmark**: https://www.cisecurity.org/benchmark/kubernetes
   - **Topic**: Security configuration benchmarks for Kubernetes clusters
   - **Quality**: High (industry standard, auditable controls)

---

## Glossary

- **Default Deny Policy**: NetworkPolicy with empty `podSelector: {}` that blocks all ingress/egress traffic, requiring explicit allow rules for any communication
- **Distroless Image**: Minimal container base image containing only application runtime (no shell, no package manager), reducing attack surface by 80-90%
- **Ephemeral Debug Container**: Temporary container attached to running pod for debugging distroless containers without shell access (`kubectl debug`)
- **Hash Suffix Pattern**: Kustomize mechanism that appends content hash to ConfigMap/Secret names, triggering pod restarts on configuration changes
- **Immutable ConfigMap**: ConfigMap with `immutable: true` field, preventing modifications after creation (performance optimization + tamper prevention)
- **Lateral Movement**: Attacker technique to pivot from compromised pod to other services within cluster (blocked by NetworkPolicies)
- **Multi-Stage Build**: Dockerfile pattern with separate build and runtime stages, copying only necessary artifacts to final image
- **Pod Selector**: Label-based targeting mechanism in NetworkPolicies (`podSelector: matchLabels: app=api`) for fine-grained traffic control
- **Rotation Safety Gate**: Explicit flag or environment variable (ALLOW_ROTATION=true) required to prevent accidental credential rotation
- **Zero-Trust Network**: Security model where all network traffic is denied by default, explicit allow rules required (default deny + explicit allow)

---

## Sources & References

1. **Kubernetes Network Policies Documentation**: https://kubernetes.io/docs/concepts/services-networking/network-policies/
   - Accessed: 2025-10-24
   - Confidence: 1.0 (official documentation)

2. **Google Distroless GitHub Repository**: https://github.com/GoogleContainerTools/distroless
   - Accessed: 2025-10-24
   - Confidence: 1.0 (official project)

3. **Calico NetworkPolicy Best Practices**: https://docs.tigera.io/calico/latest/network-policy/
   - Accessed: 2025-10-24
   - Confidence: 0.95 (vendor documentation, industry-proven patterns)

4. **NIST SP 800-190 Container Security**: https://csrc.nist.gov/publications/detail/sp/800-190/final
   - Accessed: 2025-10-24
   - Confidence: 1.0 (authoritative government standard)

5. **Kubernetes Secrets Encryption at Rest**: https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/
   - Accessed: 2025-10-24
   - Confidence: 1.0 (official documentation)

6. **Kustomize ConfigMapGenerator Documentation**: https://kubectl.docs.kubernetes.io/references/kustomize/builtins/#_configmapgenerator_
   - Accessed: 2025-10-24
   - Confidence: 1.0 (official Kustomize docs)

7. **OWASP Kubernetes Security Cheat Sheet**: https://cheatsheetseries.owasp.org/cheatsheets/Kubernetes_Security_Cheat_Sheet.html
   - Accessed: 2025-10-24
   - Confidence: 0.95 (OWASP-maintained, community-reviewed)

8. **CIS Kubernetes Benchmark v1.8**: https://www.cisecurity.org/benchmark/kubernetes
   - Accessed: 2025-10-24
   - Confidence: 0.95 (industry standard, auditable)

---

## Changelog

- **2025-10-24**: Initial documentation created from research findings (confidence: 0.95)
  - Network policy patterns (default deny, CNI compatibility, pod selectors)
  - Distroless images (attack surface reduction, multi-stage builds, debugging)
  - Secret management (rotation safety, base64 encoding, validation)
  - ConfigMap immutability (hash suffix, native immutability, decision matrix)
  - Security workflows (deployment pipeline, incident response)
  - Anti-patterns (privileged containers, secrets in ConfigMaps, implicit network allow)
  - Integration points (CI/CD, observability, cert-manager)
  - Validation checks (network policy coverage, distroless verification, secret encryption)

---

## Related Documentation

- **deployment-release Agent Definition**: `.claude/agents/deployment-release.md`
- **Network Policy Cookbook**: `.claude/docs/guides/deployment-release/network-policy-cookbook.md` (to be created)
- **Distroless Migration Guide**: `.claude/docs/guides/deployment-release/distroless-migration.md` (to be created)
- **Secret Management Runbook**: `.claude/docs/guides/deployment-release/secret-management.md` (to be created)
- **GitOps Security Patterns**: `.claude/docs/guides/deployment-release/gitops-security.md` (to be created)
