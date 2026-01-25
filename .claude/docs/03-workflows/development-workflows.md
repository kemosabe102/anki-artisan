---
title: "Kubernetes Deployment Development Workflows"
date: 2025-11-08
status: ACTIVE
tags: [claude-docs]
---
# Kubernetes Deployment Development Workflows

**Category**: development
**Domain**: Kubernetes deployment automation and troubleshooting
**Confidence**: 0.92
**Last Updated**: 2025-10-24T00:00:00Z
**Agent**: deployment-release

---

## Overview

This documentation covers the complete lifecycle of Kubernetes deployment workflows for the gauntlet-agents system, from initial deployment through configuration changes, troubleshooting, rollbacks, and secret rotation. These workflows enable safe, repeatable deployment operations with built-in validation and recovery mechanisms.

**Key Concepts**:

- **Idempotent Deployment**: Operations that can be safely repeated without changing the result beyond the initial application
- **Hash-Based Immutability**: ConfigMaps and Secrets use hash suffixes to trigger automatic pod restarts on configuration changes
- **Event-Driven Diagnosis**: Troubleshooting workflow that follows Kubernetes events to identify root causes systematically

---

## Core Frameworks

### Framework 1: 7-Phase Deployment Pipeline

**Purpose**: Provides a structured, validated approach to deploying the gauntlet-agents application to Kubernetes with comprehensive health checks.

**When to Use**:

- Initial deployment to a new cluster or namespace
- Full redeployment after cluster reset
- Deploying a new version of the application from main branch

**Components**:

1. **Prerequisites Check**: Validates kubectl context and gh CLI availability
2. **Authentication Setup**: Configures GHCR authentication using GitHub token
3. **Image Pull**: Pre-pulls container images to detect registry issues early
4. **Namespace Creation**: Creates gauntlet-agents namespace idempotently
5. **Application Deployment**: Applies Kustomize configuration with dependency ordering
6. **Validation**: Executes synthetic health checks via port-forwarding
7. **Status Display**: Reports pod, service, and event status

**How to Apply**:

1. Validate prerequisites: `kubectl config current-context` and `gh --version`
2. Authenticate to GHCR: `gh auth token | docker login ghcr.io -u kemosabe102 --password-stdin`
3. Pull image: `docker pull ghcr.io/kemosabe102/gauntlet-agents:main`
4. Create namespace: `kubectl create namespace gauntlet-agents --dry-run=client -o yaml | kubectl apply -f -`
5. Deploy with ordering: `kubectl apply -k k8s/local/ && kubectl rollout status deployment/postgres -n gauntlet-agents`
6. Validate health: Execute `scripts/validate_deployment.py` with port-forwarding if ClusterIP
7. Display status: `kubectl get pods,services,events -n gauntlet-agents`

**Example from Codebase**:

```bash
# Full deployment sequence
kubectl config use-context docker-desktop
gh auth token | docker login ghcr.io -u kemosabe102 --password-stdin
docker pull ghcr.io/kemosabe102/gauntlet-agents:main

kubectl create namespace gauntlet-agents --dry-run=client -o yaml | kubectl apply -f -
kubectl apply -k k8s/local/

# Wait for each component in order
kubectl rollout status deployment/postgres -n gauntlet-agents
kubectl rollout status deployment/redis -n gauntlet-agents
kubectl rollout status deployment/api -n gauntlet-agents

# Validate deployment
python scripts/validate_deployment.py --namespace gauntlet-agents
```

**Source**: Research findings from deployment-release domain investigation

---

### Framework 2: Hash-Based Configuration Management

**Purpose**: Ensures configuration changes trigger automatic pod restarts using Kustomize's ConfigMapGenerator hash suffix mechanism.

**When to Use**:

- Updating application configuration (environment variables, feature flags)
- Modifying database connection strings or API endpoints
- Changing logging levels or debug settings

**Components**:

1. **Hash Generation**: Kustomize automatically appends hash suffix to ConfigMap names
2. **Immutability Enforcement**: Each configuration version gets a unique ConfigMap
3. **Automatic Restart**: Pods reference ConfigMap by hash, triggering restart on change
4. **Garbage Collection**: Old ConfigMaps are retained for rollback, cleaned up manually

**How to Apply**:

1. Edit source YAML: Modify `k8s/local/config/app-config.yaml`
2. Generate manifest: `kubectl kustomize k8s/local/ > manifest.yaml` (inspect hash suffix)
3. Dry-run validation: `kubectl apply -k k8s/local/ --dry-run=server`
4. Apply changes: `kubectl apply -k k8s/local/`
5. Monitor restart: `kubectl rollout status deployment/api -n gauntlet-agents`
6. Verify configuration: `kubectl exec deployment/api -n gauntlet-agents -- env | grep CONFIG_KEY`

**Example from Codebase**:

```yaml
# k8s/local/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

configMapGenerator:
  - name: app-config
    files:
      - config/app-config.yaml
    options:
      disableNameSuffixHash: false # Enable hash suffix

# Result: app-config-5t4mb9chc7 (hash suffix triggers pod restart)
```

**Source**: Kustomize ConfigMapGenerator documentation - https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/configmapgenerator/

---

### Framework 3: Event-Driven Troubleshooting

**Purpose**: Provides a systematic approach to diagnosing Kubernetes deployment issues by following event chains and resource states.

**When to Use**:

- Pods are in CrashLoopBackOff, ImagePullBackOff, or Pending state
- Deployment validation fails with unclear errors
- Services are not responding to health checks

**Components**:

1. **Symptom Identification**: Determine pod status via `kubectl get pods`
2. **Event Analysis**: Inspect Events section in `kubectl describe pod`
3. **Log Inspection**: Review current and previous container logs
4. **Resource Validation**: Check node resource availability (CPU, memory)
5. **Configuration Verification**: Validate ConfigMaps and Secrets exist and are readable
6. **Network Validation**: Test service endpoints and internal connectivity
7. **Image Validation**: Verify image availability and authentication

**How to Apply**:

1. Identify symptom: `kubectl get pods -n gauntlet-agents` (note pod status)
2. Analyze events: `kubectl describe pod <pod-name> -n gauntlet-agents | grep -A 20 Events`
3. Inspect logs: `kubectl logs <pod-name> -n gauntlet-agents --previous` (for CrashLoopBackOff)
4. Check resources: `kubectl describe node | grep -A 5 "Allocated resources"`
5. Verify config: `kubectl get configmap,secret -n gauntlet-agents`
6. Test network: `kubectl exec deployment/api -n gauntlet-agents -- curl -v http://postgres:5432`
7. Validate image: `docker pull ghcr.io/kemosabe102/gauntlet-agents:main`

**Example from Codebase**:

```bash
# Troubleshooting CrashLoopBackOff
kubectl get pods -n gauntlet-agents
# NAME                        READY   STATUS             RESTARTS   AGE
# api-7d9f8c5b6d-xyz12        0/1     CrashLoopBackOff   5          3m

kubectl describe pod api-7d9f8c5b6d-xyz12 -n gauntlet-agents
# Events:
#   Type     Reason     Age                From               Message
#   ----     ------     ----               ----               -------
#   Warning  BackOff    2m                 kubelet            Back-off restarting failed container

kubectl logs api-7d9f8c5b6d-xyz12 -n gauntlet-agents --previous
# Error: Cannot connect to database at postgres:5432

# Diagnosis: Database connection failure
# Verification: Check postgres service
kubectl get svc postgres -n gauntlet-agents
kubectl exec deployment/api -n gauntlet-agents -- nslookup postgres
```

**Source**: Kubernetes troubleshooting best practices - https://kubernetes.io/docs/tasks/debug/

---

## Processes & Workflows

### Workflow 1: Full Deployment Workflow

**Trigger Conditions**:

- Initial deployment to new cluster
- Complete redeployment after namespace deletion
- Major version upgrade requiring clean deployment

**Steps**:

1. **Prerequisites Check**: Validate cluster access and tooling
   - **Input**: kubectl config, gh CLI installation
   - **Output**: Validated cluster context and authenticated CLI
   - **Rationale**: Prevents deployment failures due to missing tools or wrong cluster

2. **Authentication Setup**: Configure container registry access
   - **Input**: GitHub token from `gh auth token`
   - **Output**: Authenticated Docker client for GHCR
   - **Rationale**: Required for pulling private container images

3. **Image Pull**: Pre-fetch container images
   - **Input**: Image tag from deployment manifest
   - **Output**: Cached image in local Docker daemon
   - **Rationale**: Detects registry authentication issues before deployment

4. **Namespace Creation**: Create isolated deployment namespace
   - **Input**: Namespace name (gauntlet-agents)
   - **Output**: Created or existing namespace
   - **Rationale**: Provides resource isolation and RBAC boundaries

5. **Application Deployment**: Apply Kustomize manifests with dependency ordering
   - **Input**: Kustomize directory (`k8s/local/`)
   - **Output**: Deployed resources (postgres → redis → api)
   - **Rationale**: Sequential rollout ensures dependencies are ready before dependents start

6. **Validation**: Execute synthetic health checks
   - **Input**: Deployed services and endpoints
   - **Output**: 6 synthetic test results (health, readiness, metrics, etc.)
   - **Rationale**: Confirms application is functioning correctly before marking deployment successful

7. **Status Display**: Report deployment state
   - **Input**: Namespace resources
   - **Output**: Pod status, service endpoints, recent events
   - **Rationale**: Provides visibility into deployment outcome for human operators

**Success Criteria**:

- ✅ All pods in Running state with 1/1 READY
- ✅ All rollout status commands return "successfully rolled out"
- ✅ 6/6 synthetic health checks pass
- ✅ No error events in recent event list

**Failure Handling**:

- If image pull fails, verify GHCR authentication: `docker logout ghcr.io && gh auth token | docker login ghcr.io -u kemosabe102 --password-stdin`
- If pod stays in Pending, check node resources: `kubectl describe nodes`
- If health checks fail, inspect logs: `kubectl logs deployment/api -n gauntlet-agents`
- If services not created, check Kustomize output: `kubectl kustomize k8s/local/`

**Example Execution**:

```bash
# User request: "Deploy gauntlet-agents to local Kubernetes cluster"

# Phase 1: Prerequisites
kubectl config current-context
# docker-desktop
gh --version
# gh version 2.40.1

# Phase 2: Authentication
gh auth token | docker login ghcr.io -u kemosabe102 --password-stdin
# Login Succeeded

# Phase 3: Image Pull
docker pull ghcr.io/kemosabe102/gauntlet-agents:main
# main: Pulling from kemosabe102/gauntlet-agents
# Status: Downloaded newer image for ghcr.io/kemosabe102/gauntlet-agents:main

# Phase 4: Namespace Creation
kubectl create namespace gauntlet-agents --dry-run=client -o yaml | kubectl apply -f -
# namespace/gauntlet-agents created

# Phase 5: Application Deployment
kubectl apply -k k8s/local/
# configmap/app-config-5t4mb9chc7 created
# secret/app-secrets created
# service/postgres created
# service/redis created
# service/api created
# deployment.apps/postgres created
# deployment.apps/redis created
# deployment.apps/api created

kubectl rollout status deployment/postgres -n gauntlet-agents
# deployment "postgres" successfully rolled out
kubectl rollout status deployment/redis -n gauntlet-agents
# deployment "redis" successfully rolled out
kubectl rollout status deployment/api -n gauntlet-agents
# deployment "api" successfully rolled out

# Phase 6: Validation
python scripts/validate_deployment.py --namespace gauntlet-agents
# ✅ Health check passed
# ✅ Readiness check passed
# ✅ Metrics endpoint accessible
# ✅ Database connectivity verified
# ✅ Redis connectivity verified
# ✅ API response time < 200ms
# All checks passed: 6/6

# Phase 7: Status Display
kubectl get pods,services -n gauntlet-agents
# NAME                            READY   STATUS    RESTARTS   AGE
# pod/postgres-7d9f8c5b6d-abc12   1/1     Running   0          2m
# pod/redis-5f6g7h8i9j-def34      1/1     Running   0          2m
# pod/api-8k9l0m1n2o3-ghi56       1/1     Running   0          2m
#
# NAME               TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
# service/postgres   ClusterIP   10.96.10.10     <none>        5432/TCP   2m
# service/redis      ClusterIP   10.96.20.20     <none>        6379/TCP   2m
# service/api        ClusterIP   10.96.30.30     <none>        8000/TCP   2m

# Deployment complete ✅
```

---

### Workflow 2: Configuration Change Workflow

**Trigger Conditions**:

- Application behavior needs modification without code changes
- Environment-specific configuration updates (database URLs, feature flags)
- Debugging requires temporary configuration changes (log levels)

**Steps**:

1. **Manifest Editing**: Update base YAML or Kustomize overlays
   - **Input**: Configuration key-value pairs to change
   - **Output**: Modified YAML file in `k8s/local/config/`
   - **Rationale**: Git-tracked configuration enables version control and rollback

2. **Hash Suffix Generation**: Kustomize generates new ConfigMap hash
   - **Input**: Modified ConfigMap source file
   - **Output**: ConfigMap with new hash suffix (e.g., app-config-7h3j9k2m4p)
   - **Rationale**: Hash suffix triggers automatic pod restart on apply

3. **Validation**: Syntax and RBAC validation via dry-run
   - **Input**: Modified Kustomize directory
   - **Output**: Server-side validation results
   - **Rationale**: Catches errors before applying to cluster (prevents downtime)

4. **Application**: Apply configuration with immutability enforcement
   - **Input**: Validated Kustomize configuration
   - **Output**: New ConfigMap created, old ConfigMap retained
   - **Rationale**: Immutable ConfigMaps enable instant rollback

5. **Pod Restart**: Automatic restart due to ConfigMap reference change
   - **Input**: Deployment with ConfigMap reference
   - **Output**: Rolling restart with new ConfigMap mounted
   - **Rationale**: Ensures all pods use consistent configuration version

6. **Rollout Verification**: Monitor restart progress and health
   - **Input**: Deployment name and namespace
   - **Output**: Rollout status and event stream
   - **Rationale**: Detects configuration-induced failures early

7. **Validation**: Execute health checks post-deployment
   - **Input**: Restarted pods and services
   - **Output**: Synthetic test results confirming expected behavior
   - **Rationale**: Verifies configuration change achieved desired outcome

**Success Criteria**:

- ✅ Dry-run validation passes with no errors
- ✅ New ConfigMap created with different hash suffix
- ✅ Old ConfigMap retained for potential rollback
- ✅ Rollout completes without errors
- ✅ Health checks pass with new configuration

**Failure Handling**:

- If dry-run fails, check YAML syntax: `kubectl apply -k k8s/local/ --dry-run=server 2>&1 | grep error`
- If pods fail to start, check logs: `kubectl logs deployment/api -n gauntlet-agents --previous`
- If health checks fail, rollback: `kubectl rollout undo deployment/api -n gauntlet-agents`
- If ConfigMap not updated, check Kustomize build: `kubectl kustomize k8s/local/ | grep ConfigMap`

**Example Execution**:

```bash
# User request: "Change LOG_LEVEL from INFO to DEBUG"

# Step 1: Edit manifest
vim k8s/local/config/app-config.yaml
# Change: LOG_LEVEL=INFO → LOG_LEVEL=DEBUG

# Step 2: Inspect hash generation
kubectl kustomize k8s/local/ | grep -A 5 "kind: ConfigMap"
# apiVersion: v1
# kind: ConfigMap
# metadata:
#   name: app-config-7h3j9k2m4p  # New hash suffix
# data:
#   LOG_LEVEL: DEBUG

# Step 3: Validate
kubectl apply -k k8s/local/ --dry-run=server
# configmap/app-config-7h3j9k2m4p created (dry run)
# deployment.apps/api configured (dry run)

# Step 4: Apply
kubectl apply -k k8s/local/
# configmap/app-config-7h3j9k2m4p created
# configmap/app-config-5t4mb9chc7 unchanged  # Old ConfigMap retained
# deployment.apps/api configured

# Step 5: Pod restart (automatic)
kubectl get pods -n gauntlet-agents -w
# api-8k9l0m1n2o3-ghi56   1/1   Terminating   0     5m
# api-8k9l0m1n2o3-jkl78   0/1   Pending       0     0s
# api-8k9l0m1n2o3-jkl78   0/1   ContainerCreating   0     2s
# api-8k9l0m1n2o3-jkl78   1/1   Running             0     10s

# Step 6: Verify rollout
kubectl rollout status deployment/api -n gauntlet-agents
# deployment "api" successfully rolled out

# Step 7: Validate
kubectl exec deployment/api -n gauntlet-agents -- env | grep LOG_LEVEL
# LOG_LEVEL=DEBUG

python scripts/validate_deployment.py --namespace gauntlet-agents
# ✅ All checks passed: 6/6

# Configuration change complete ✅
```

---

### Workflow 3: Troubleshooting Workflow

**Trigger Conditions**:

- Deployment validation fails with unclear error messages
- Pods are not reaching Running state
- Application behavior deviates from expected (health checks fail)

**Steps**:

1. **Symptom Identification**: Determine pod status and initial symptoms
   - **Input**: Namespace and deployment name
   - **Output**: Pod status (Pending, CrashLoopBackOff, ImagePullBackOff, etc.)
   - **Rationale**: Pod status indicates category of failure (scheduling, image, runtime)

2. **Event Analysis**: Inspect Kubernetes events for root cause signals
   - **Input**: Pod name from step 1
   - **Output**: Event stream with timestamps and reasons
   - **Rationale**: Events contain direct error messages from kubelet and scheduler

3. **Log Inspection**: Review current and previous container logs
   - **Input**: Pod name and container name
   - **Output**: Application logs and stack traces
   - **Rationale**: Application errors often not visible in Kubernetes events

4. **Resource Validation**: Check node capacity and resource quotas
   - **Input**: Cluster nodes and namespace
   - **Output**: CPU/memory allocation vs. capacity
   - **Rationale**: Pending pods may indicate resource exhaustion

5. **Configuration Verification**: Validate ConfigMaps and Secrets exist and are mounted
   - **Input**: Deployment manifest references
   - **Output**: ConfigMap/Secret names and data keys
   - **Rationale**: Missing configuration prevents container startup

6. **Network Validation**: Test internal service connectivity and DNS resolution
   - **Input**: Service names and endpoints
   - **Output**: curl results and nslookup responses
   - **Rationale**: Network issues cause inter-service communication failures

7. **Image Validation**: Verify container image availability and registry authentication
   - **Input**: Image name and tag from deployment
   - **Output**: Image pull result and manifest inspection
   - **Rationale**: ImagePullBackOff indicates registry or authentication issues

**Success Criteria**:

- ✅ Root cause identified with specific error message
- ✅ Remediation action determined (fix configuration, increase resources, etc.)
- ✅ Verification method defined (re-deploy, scale up, etc.)

**Failure Handling**:

- If events provide no clues, check admission webhooks: `kubectl get validatingwebhookconfigurations`
- If logs are empty, check init containers: `kubectl logs <pod> -c <init-container>`
- If resources sufficient but pod still Pending, check taints and tolerations: `kubectl describe node | grep Taints`

**Example Execution**:

```bash
# User report: "API deployment is failing after configuration change"

# Step 1: Identify symptom
kubectl get pods -n gauntlet-agents
# NAME                        READY   STATUS             RESTARTS   AGE
# api-8k9l0m1n2o3-jkl78       0/1     CrashLoopBackOff   5          3m

# Step 2: Analyze events
kubectl describe pod api-8k9l0m1n2o3-jkl78 -n gauntlet-agents
# Events:
#   Type     Reason     Age                From               Message
#   ----     ------     ----               ----               -------
#   Normal   Scheduled  3m                 default-scheduler  Successfully assigned gauntlet-agents/api-8k9l0m1n2o3-jkl78 to docker-desktop
#   Normal   Pulling    3m                 kubelet            Pulling image "ghcr.io/kemosabe102/gauntlet-agents:main"
#   Normal   Pulled     3m                 kubelet            Successfully pulled image
#   Normal   Created    2m (x4 over 3m)    kubelet            Created container api
#   Normal   Started    2m (x4 over 3m)    kubelet            Started container api
#   Warning  BackOff    1m (x10 over 3m)   kubelet            Back-off restarting failed container

# Step 3: Inspect logs
kubectl logs api-8k9l0m1n2o3-jkl78 -n gauntlet-agents --previous
# Traceback (most recent call last):
#   File "main.py", line 45, in <module>
#     db_client = connect_database(os.environ['DATABASE_URL'])
# KeyError: 'DATABASE_URL'

# Diagnosis: Missing environment variable

# Step 4: Skip (not resource-related)
# Step 5: Verify configuration
kubectl get configmap app-config-7h3j9k2m4p -n gauntlet-agents -o yaml | grep DATABASE_URL
# (no output - variable missing)

kubectl describe deployment api -n gauntlet-agents | grep -A 10 "Environment"
# Environment Variables from:
#   app-config-7h3j9k2m4p  ConfigMap  Optional: false

# Root cause identified: DATABASE_URL not defined in ConfigMap

# Remediation:
vim k8s/local/config/app-config.yaml
# Add: DATABASE_URL=postgresql://postgres:5432/gauntlet

kubectl apply -k k8s/local/
# configmap/app-config-9m5n7p2q4r created

kubectl rollout status deployment/api -n gauntlet-agents
# deployment "api" successfully rolled out

kubectl get pods -n gauntlet-agents
# NAME                        READY   STATUS    RESTARTS   AGE
# api-8k9l0m1n2o3-mno89       1/1     Running   0          30s

# Troubleshooting complete ✅
```

---

### Workflow 4: Rollback Procedure

**Trigger Conditions**:

- Deployment validation fails after configuration change
- New version introduces critical bugs detected in production
- Performance degradation observed after deployment

**Steps**:

1. **Failure Detection**: Identify deployment requiring rollback
   - **Input**: Failed health checks or user report
   - **Output**: Deployment name and namespace
   - **Rationale**: Determines scope of rollback operation

2. **Rollout History**: Inspect previous deployment revisions
   - **Input**: Deployment name
   - **Output**: Revision list with change causes
   - **Rationale**: Identifies last known-good revision

3. **Revision Inspection**: Review specific revision details
   - **Input**: Revision number from history
   - **Output**: Full manifest of historical revision
   - **Rationale**: Confirms rollback target matches expectations

4. **Rollback Execution**: Revert to previous revision
   - **Input**: Deployment name and optional revision number
   - **Output**: Rollout to previous ConfigMap/image version
   - **Rationale**: Restores last known-good state

5. **Rollout Monitoring**: Track rollback progress
   - **Input**: Deployment rollout status
   - **Output**: Rolling restart with previous configuration
   - **Rationale**: Ensures rollback completes successfully

6. **Validation**: Re-run health checks to confirm restoration
   - **Input**: Rolled-back services
   - **Output**: Synthetic test results
   - **Rationale**: Verifies rollback resolved the issue

7. **Git Revert**: Revert manifest changes in version control
   - **Input**: Git commit that introduced bad configuration
   - **Output**: Revert commit restoring previous state
   - **Rationale**: Maintains GitOps consistency (cluster state = Git state)

**Success Criteria**:

- ✅ Rollback completes without errors
- ✅ Pods restart with previous configuration
- ✅ Health checks pass after rollback
- ✅ Git repository reflects rolled-back state

**Failure Handling**:

- If rollback fails, check revision exists: `kubectl rollout history deployment/api -n gauntlet-agents`
- If pods fail to start after rollback, check for persistent issues: `kubectl describe pod <pod-name>`
- If specific revision needed, use explicit rollback: `kubectl rollout undo deployment/api --to-revision=3`

**Example Execution**:

```bash
# User request: "Rollback API deployment - new config causing errors"

# Step 1: Failure detection
python scripts/validate_deployment.py --namespace gauntlet-agents
# ❌ Health check failed: 500 Internal Server Error
# Deployment requires rollback

# Step 2: Rollout history
kubectl rollout history deployment/api -n gauntlet-agents
# REVISION  CHANGE-CAUSE
# 1         Initial deployment
# 2         ConfigMap update: app-config-5t4mb9chc7
# 3         ConfigMap update: app-config-7h3j9k2m4p (current - FAILING)

# Step 3: Inspect revision 2
kubectl rollout history deployment/api -n gauntlet-agents --revision=2
# Pod Template:
#   Labels:       app=api
#                 pod-template-hash=8k9l0m1n2o3
#   Containers:
#    api:
#     Image:      ghcr.io/kemosabe102/gauntlet-agents:main
#     Environment Variables from:
#       app-config-5t4mb9chc7  ConfigMap  Optional: false

# Confirmed: Revision 2 is last known-good

# Step 4: Rollback execution
kubectl rollout undo deployment/api -n gauntlet-agents
# deployment.apps/api rolled back

# Step 5: Monitor rollout
kubectl rollout status deployment/api -n gauntlet-agents
# Waiting for deployment "api" rollout to finish: 1 old replicas are pending termination...
# deployment "api" successfully rolled out

kubectl get pods -n gauntlet-agents
# NAME                        READY   STATUS    RESTARTS   AGE
# api-8k9l0m1n2o3-pqr90       1/1     Running   0          45s

# Step 6: Validate
python scripts/validate_deployment.py --namespace gauntlet-agents
# ✅ All checks passed: 6/6

# Step 7: Git revert
git log --oneline k8s/local/config/app-config.yaml
# abc1234 feat: update LOG_LEVEL to DEBUG (BAD CONFIG)
# def5678 feat: add DATABASE_URL

git revert abc1234
# [main 9gh0ijk] Revert "feat: update LOG_LEVEL to DEBUG"
#  1 file changed, 1 insertion(+), 1 deletion(-)

git push origin main

# Rollback complete ✅
```

---

### Workflow 5: Secret Rotation Workflow

**Trigger Conditions**:

- Scheduled credential rotation policy (e.g., quarterly database password changes)
- Security incident requiring immediate credential invalidation
- Onboarding new environment requiring unique secrets

**Steps**:

1. **.env File Validation**: Verify format and required keys
   - **Input**: `.env` file with key-value pairs
   - **Output**: Validated environment variables
   - **Rationale**: Prevents deployment failures from malformed secrets

2. **Base64 Encoding**: Encode all secret values
   - **Input**: Plaintext secret values from .env
   - **Output**: Base64-encoded strings
   - **Rationale**: Kubernetes Secrets require base64 encoding

3. **Template Substitution**: Generate secrets.yaml from template
   - **Input**: secrets.yaml.template with placeholders
   - **Output**: secrets.yaml with actual encoded values
   - **Rationale**: Separates secret storage (.env) from structure (template)

4. **Password Rotation**: Generate new database password if requested
   - **Input**: `--rotate-db-password` flag
   - **Output**: New password in .env and secrets.yaml
   - **Rationale**: Enables automated rotation without manual password generation

5. **Immutability Enforcement**: Hash-based secret versioning
   - **Input**: Secret content hash
   - **Output**: Secret with hash suffix (e.g., app-secrets-4k8m2n6p)
   - **Rationale**: Triggers pod restart on secret change (same as ConfigMap)

6. **Application**: Apply secrets to cluster
   - **Input**: Generated secrets.yaml
   - **Output**: Kubernetes Secret resource
   - **Rationale**: Makes secrets available for pod mounting

7. **Pod Restart**: Automatic restart with new secret reference
   - **Input**: Deployment with Secret reference
   - **Output**: Rolling restart with new secrets mounted
   - **Rationale**: Ensures application uses updated credentials

8. **Security Cleanup**: Set restrictive file permissions
   - **Input**: Generated secrets.yaml and .env
   - **Output**: Files with 600 permissions (owner read/write only)
   - **Rationale**: Prevents unauthorized access to sensitive files

**Success Criteria**:

- ✅ .env file passes validation (no placeholders, all required keys present)
- ✅ secrets.yaml generated with base64-encoded values
- ✅ Secret applied to cluster without errors
- ✅ Pods restart and mount new secrets successfully
- ✅ File permissions set to 600 for security

**Failure Handling**:

- If .env validation fails, check for placeholder values: `grep -E 'YOUR_|CHANGEME|TODO' .env`
- If base64 encoding fails, check for special characters: Use `safe_base64()` function
- If pods fail to start, check secret mounting: `kubectl describe pod <pod-name> | grep -A 10 Mounts`
- If secret not created, check RBAC: `kubectl auth can-i create secrets --namespace gauntlet-agents`

**Example Execution**:

```bash
# User request: "Rotate database password for security compliance"

# Step 1: Validate .env
cat .env
# DATABASE_PASSWORD=old_password_12345
# REDIS_PASSWORD=redis_secret_67890
# API_KEY=api_key_abcdef

grep -E 'YOUR_|CHANGEME|TODO' .env
# (no output - validation passed)

# Step 2: Base64 encode (automated by script)
echo -n "old_password_12345" | base64
# b2xkX3Bhc3N3b3JkXzEyMzQ1

# Step 3: Generate new password
python scripts/rotate_secrets.py --rotate-db-password
# Generated new database password: JkL9#mN2pQ5rS8tU
# Updated .env file
# Generated secrets.yaml

cat .env
# DATABASE_PASSWORD=JkL9#mN2pQ5rS8tU  # Updated
# REDIS_PASSWORD=redis_secret_67890   # Unchanged
# API_KEY=api_key_abcdef              # Unchanged

# Step 4: Inspect generated secret
cat k8s/local/secrets.yaml
# apiVersion: v1
# kind: Secret
# metadata:
#   name: app-secrets-4k8m2n6p  # Hash suffix
#   namespace: gauntlet-agents
# type: Opaque
# data:
#   database-password: SmtMOSNtTjJwUTVyUzh0VQ==  # New password
#   redis-password: cmVkaXNfc2VjcmV0XzY3ODkw
#   api-key: YXBpX2tleV9hYmNkZWY=

# Step 5: Apply secret
kubectl apply -f k8s/local/secrets.yaml
# secret/app-secrets-4k8m2n6p created

# Step 6: Pod restart (automatic)
kubectl get pods -n gauntlet-agents -w
# postgres-7d9f8c5b6d-abc12   1/1   Terminating   0     10m
# postgres-7d9f8c5b6d-stu34   0/1   Pending       0     0s
# postgres-7d9f8c5b6d-stu34   1/1   Running       0     15s

kubectl rollout status deployment/postgres -n gauntlet-agents
# deployment "postgres" successfully rolled out

# Step 7: Security cleanup
chmod 600 .env k8s/local/secrets.yaml
ls -l .env k8s/local/secrets.yaml
# -rw------- 1 user user  180 Oct 24 10:30 .env
# -rw------- 1 user user  450 Oct 24 10:30 k8s/local/secrets.yaml

# Step 8: Validate
kubectl exec deployment/postgres -n gauntlet-agents -- psql -c "\conninfo"
# You are connected to database "gauntlet" as user "postgres" via socket in "/var/run/postgresql" at port "5432".
# Authentication successful with new password ✅

# Secret rotation complete ✅
```

---

## Decision Trees

### Decision 1: Deployment Failure Root Cause Analysis

```
IF pod status = "ImagePullBackOff"
  THEN check image name and registry authentication
    1. Verify image exists: docker pull <image>
    2. Check credentials: gh auth token | docker login ghcr.io
    3. Inspect image reference: kubectl get pod <pod> -o yaml | grep image
  BECAUSE image availability is prerequisite for pod startup

ELSE IF pod status = "CrashLoopBackOff"
  THEN inspect application logs and configuration
    1. Review logs: kubectl logs <pod> --previous
    2. Check ConfigMap: kubectl get configmap -n <namespace>
    3. Verify Secret mounting: kubectl describe pod <pod> | grep Mounts
  BECAUSE application runtime errors indicate configuration issues

ELSE IF pod status = "Pending"
  THEN validate node resources and scheduling constraints
    1. Check resources: kubectl describe nodes | grep Allocated
    2. Check taints: kubectl describe nodes | grep Taints
    3. Check node selector: kubectl get pod <pod> -o yaml | grep nodeSelector
  BECAUSE scheduler cannot place pod due to constraints

ELSE IF pod status = "Running" AND health checks fail
  THEN validate network connectivity and service configuration
    1. Test endpoints: kubectl exec <pod> -- curl http://service:port
    2. Check DNS: kubectl exec <pod> -- nslookup service
    3. Inspect Service: kubectl describe service <service>
  BECAUSE network issues prevent inter-service communication

ELSE
  THEN review Kubernetes events for cluster-level issues
    1. Cluster events: kubectl get events --sort-by='.lastTimestamp'
    2. Admission webhooks: kubectl get validatingwebhookconfigurations
    3. Resource quotas: kubectl describe resourcequota -n <namespace>
  BECAUSE uncommon failures require broad investigation
```

**Example Scenarios**:

1. **Scenario**: Pod stuck in ImagePullBackOff after changing image tag → **Decision**: Verify image exists with `docker pull`, check typo in deployment manifest
2. **Scenario**: Pod crashes immediately with "KeyError: DATABASE_URL" → **Decision**: Inspect logs, verify ConfigMap contains DATABASE_URL key, check envFrom reference

---

### Decision 2: Configuration Change Strategy Selection

```
IF change affects sensitive data (passwords, API keys)
  THEN use Secret rotation workflow
    1. Update .env file with new credentials
    2. Generate secrets.yaml with base64 encoding
    3. Apply Secret with hash suffix for immutability
  BECAUSE secrets require secure handling and encryption at rest

ELSE IF change affects application behavior (feature flags, log levels)
  THEN use ConfigMap update workflow
    1. Edit k8s/local/config/app-config.yaml
    2. Apply with Kustomize to trigger hash-based restart
    3. Validate with health checks
  BECAUSE ConfigMaps are transparent and version-controlled

ELSE IF change requires code modification
  THEN use full deployment workflow with new image
    1. Build new container image
    2. Push to GHCR
    3. Update image tag in deployment
    4. Apply with rollout monitoring
  BECAUSE code changes require container rebuild

ELSE IF change is experimental/temporary
  THEN use kubectl set env for live patch (non-GitOps)
    1. kubectl set env deployment/<name> KEY=VALUE
    2. Monitor rollout status
    3. Revert if issues: kubectl rollout undo
  BECAUSE temporary changes avoid polluting Git history

ELSE
  THEN default to ConfigMap workflow
  BECAUSE most configuration changes are non-sensitive
```

**Example Scenarios**:

1. **Scenario**: Database password compromised, need immediate rotation → **Decision**: Secret rotation workflow with `--rotate-db-password` flag
2. **Scenario**: Enable debug logging temporarily for troubleshooting → **Decision**: `kubectl set env deployment/api LOG_LEVEL=DEBUG`, revert after investigation

---

### Decision 3: Rollback Scope Determination

```
IF failure affects single deployment
  THEN use deployment-level rollback
    1. kubectl rollout undo deployment/<name>
    2. Monitor rollout status
    3. Validate with health checks
  BECAUSE isolated rollback minimizes impact

ELSE IF failure affects multiple deployments with shared ConfigMap
  THEN rollback ConfigMap and affected deployments
    1. Revert ConfigMap change in Git
    2. kubectl apply -k k8s/local/ to restore previous ConfigMap
    3. Verify all dependent deployments restart
  BECAUSE shared configuration requires coordinated rollback

ELSE IF failure is cluster-wide (bad network policy, broken admission webhook)
  THEN restore entire namespace or cluster state
    1. kubectl delete namespace <name>
    2. Re-apply full Kustomize configuration
    3. Run full deployment validation
  BECAUSE cluster-level issues require clean slate

ELSE IF failure is data-related (corrupted database)
  THEN restore from backup before rollback
    1. Stop database deployment: kubectl scale deployment/postgres --replicas=0
    2. Restore volume from backup
    3. Restart deployment: kubectl scale deployment/postgres --replicas=1
  BECAUSE application rollback cannot fix data corruption

ELSE
  THEN escalate to manual investigation
  BECAUSE complex failures require human judgment
```

**Example Scenarios**:

1. **Scenario**: API deployment failing after ConfigMap change, postgres and redis unaffected → **Decision**: Deployment-level rollback for API only
2. **Scenario**: All services failing after network policy update → **Decision**: Delete and re-apply entire namespace configuration

---

## Best Practices

### Practice 1: Idempotent Deployment Commands

**Principle**: Design kubectl commands that can be safely executed multiple times without unintended side effects.

**Implementation**:

- Use `kubectl apply` instead of `kubectl create` (apply is idempotent)
- Generate resources with `--dry-run=client -o yaml | kubectl apply -f -` pattern
- Enable Kustomize hash suffixes for ConfigMaps/Secrets (automatic versioning)
- Use `kubectl rollout status` to wait for completion (blocking behavior)

**Benefits**:

- ✅ Safe to re-run deployment scripts after failures
- ✅ Consistent behavior in CI/CD pipelines
- ✅ Easier to debug and recover from partial failures

**Trade-offs**:

- ⚠️ Slightly more verbose command syntax
- ⚠️ Requires understanding of apply vs. create semantics

**Example**:

```bash
✅ Idempotent Pattern:
kubectl create namespace gauntlet-agents --dry-run=client -o yaml | kubectl apply -f -
# Namespace created on first run, unchanged on subsequent runs

kubectl apply -k k8s/local/
# Updates existing resources, creates missing ones

❌ Non-Idempotent Anti-Pattern:
kubectl create namespace gauntlet-agents
# Error: namespace "gauntlet-agents" already exists (on second run)

kubectl create -f k8s/local/deployment.yaml
# Error: deployment "api" already exists (on second run)
```

---

### Practice 2: Rollout Dependency Ordering

**Principle**: Deploy components in dependency order (stateful services before stateless applications) to prevent startup failures.

**Implementation**:

- Deploy databases first (postgres, redis)
- Wait for rollout completion before deploying dependents
- Use init containers for runtime dependency checks
- Implement readiness probes with dependency validation

**Benefits**:

- ✅ Reduces transient connection errors during startup
- ✅ Cleaner logs without connection retry noise
- ✅ Faster overall deployment time (no unnecessary retries)

**Trade-offs**:

- ⚠️ Sequential deployment takes longer than parallel
- ⚠️ Requires explicit knowledge of dependency graph

**Example**:

```bash
✅ Ordered Deployment:
kubectl apply -k k8s/local/
kubectl rollout status deployment/postgres -n gauntlet-agents --timeout=5m
kubectl rollout status deployment/redis -n gauntlet-agents --timeout=5m
kubectl rollout status deployment/api -n gauntlet-agents --timeout=5m
# Each component waits for previous to be ready

❌ Parallel Deployment Anti-Pattern:
kubectl apply -k k8s/local/
# All deployments start simultaneously
# API pods crash with "connection refused" to postgres
# Kubernetes eventually recovers but with noisy logs and longer startup
```

---

### Practice 3: Validation-Driven Deployment

**Principle**: Execute synthetic health checks after every deployment operation to catch failures immediately.

**Implementation**:

- Define comprehensive health check script (HTTP endpoints, database connectivity, etc.)
- Run validation after initial deployment, configuration changes, and rollbacks
- Implement automatic rollback on validation failure (in CI/CD)
- Port-forward to ClusterIP services for local validation

**Benefits**:

- ✅ Detects issues before users encounter them
- ✅ Provides clear success/failure signal for automation
- ✅ Documents expected application behavior

**Trade-offs**:

- ⚠️ Adds 30-60 seconds to deployment time
- ⚠️ Requires maintenance when application endpoints change

**Example**:

```python
# scripts/validate_deployment.py
def validate_deployment(namespace: str) -> bool:
    checks = [
        check_health_endpoint(),      # GET /health returns 200
        check_readiness_endpoint(),   # GET /ready returns 200
        check_metrics_endpoint(),     # GET /metrics returns Prometheus format
        check_database_connectivity(), # psql connection test
        check_redis_connectivity(),    # redis-cli ping
        check_response_time()         # API responds in <200ms
    ]
    return all(checks)

# Usage in deployment script:
kubectl apply -k k8s/local/
kubectl rollout status deployment/api -n gauntlet-agents

if ! python scripts/validate_deployment.py --namespace gauntlet-agents; then
    echo "Validation failed, rolling back"
    kubectl rollout undo deployment/api -n gauntlet-agents
    exit 1
fi
```

---

## Anti-Patterns

### Anti-Pattern 1: Direct Pod Editing

**Problem**: Editing pods directly with `kubectl edit pod` loses changes on next deployment and creates configuration drift.

**Detection**:

- 🔴 Running `kubectl edit pod <pod-name>` in production
- 🔴 Using `kubectl set image pod/<pod>` instead of deployment
- 🔴 Configuration exists in cluster but not in Git

**Consequences**:

- ❌ Changes lost on pod restart or deployment update
- ❌ Configuration drift between environments
- ❌ No audit trail for changes
- ❌ Rollback impossible (no previous version stored)

**Better Approach**:

```bash
✅ Preferred Pattern (GitOps):
# Edit source manifest in Git
vim k8s/local/deployment.yaml
git commit -am "feat: increase replica count to 3"
kubectl apply -k k8s/local/

# Change is persistent and version-controlled

❌ Anti-Pattern (Direct Edit):
kubectl edit pod api-8k9l0m1n2o3-jkl78
# Change "replicas: 2" to "replicas: 3"
# Pod restarts, change is lost
# No record of who made the change or why
```

**Migration Strategy**:

1. Identify drift: `kubectl diff -k k8s/local/` (shows differences between cluster and Git)
2. Update source manifests to match cluster state
3. Document configuration rationale in commit messages
4. Enforce GitOps with admission controllers (prevent direct pod edits)

---

### Anti-Pattern 2: Using `latest` Image Tag

**Problem**: `latest` tag provides no version control, prevents rollback, and makes deployments non-deterministic.

**Detection**:

- 🔴 Image reference contains `:latest` or no tag specified
- 🔴 Rollout history shows all revisions with same image
- 🔴 Unable to identify which code version is deployed

**Consequences**:

- ❌ Rollback restores same broken image (latest is mutable)
- ❌ Different environments may run different code with same tag
- ❌ No way to correlate deployed version with Git commit
- ❌ Cache invalidation issues (Kubernetes may not pull updated image)

**Better Approach**:

```yaml
✅ Preferred Pattern (Immutable Tags):
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
spec:
  template:
    spec:
      containers:
      - name: api
        image: ghcr.io/kemosabe102/gauntlet-agents:v1.2.3-abc1234  # Git tag + commit hash
        imagePullPolicy: IfNotPresent  # Cache immutable images

# Rollback to specific version:
kubectl set image deployment/api api=ghcr.io/kemosabe102/gauntlet-agents:v1.2.2-def5678

❌ Anti-Pattern (Mutable Tag):
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
spec:
  template:
    spec:
      containers:
      - name: api
        image: ghcr.io/kemosabe102/gauntlet-agents:latest  # Mutable tag
        imagePullPolicy: Always  # Forces pull every time (slow)

# Rollback attempts pull same "latest" tag:
kubectl rollout undo deployment/api  # Still broken!
```

**Migration Strategy**:

1. Implement CI/CD tagging: `${GIT_TAG}-${GIT_COMMIT_SHORT}`
2. Update deployment manifests with explicit tags
3. Add image tag validation in CI/CD (block :latest)
4. Document version correlation in release notes

---

### Anti-Pattern 3: Skipping Dry-Run Validation

**Problem**: Applying manifests directly to cluster without validation can cause immediate downtime from syntax errors or RBAC issues.

**Detection**:

- 🔴 No `--dry-run` flag in deployment scripts
- 🔴 Syntax errors discovered after `kubectl apply` completes
- 🔴 Deployment failures due to insufficient RBAC permissions

**Consequences**:

- ❌ Cluster enters broken state requiring emergency rollback
- ❌ No warning before destructive changes (e.g., deleting volumes)
- ❌ Wastes time debugging issues that dry-run would catch

**Better Approach**:

```bash
✅ Preferred Pattern (Validation Before Apply):
# Client-side validation (fast, checks syntax)
kubectl apply -k k8s/local/ --dry-run=client
# configmap/app-config-7h3j9k2m4p created (dry run)
# deployment.apps/api configured (dry run)

# Server-side validation (slow, checks RBAC and admission webhooks)
kubectl apply -k k8s/local/ --dry-run=server
# Error: admission webhook "validate-deployment" denied request: missing required label "app"

# Fix issue, then apply for real
vim k8s/local/deployment.yaml  # Add missing label
kubectl apply -k k8s/local/
# configmap/app-config-7h3j9k2m4p created
# deployment.apps/api configured

❌ Anti-Pattern (No Validation):
kubectl apply -k k8s/local/
# Error: error parsing k8s/local/deployment.yaml: yaml: line 15: mapping values are not allowed in this context
# Deployment partially applied, cluster in inconsistent state
```

**Migration Strategy**:

1. Add dry-run to all deployment scripts as mandatory step
2. Implement pre-commit hooks for client-side validation
3. Configure CI/CD pipelines with server-side validation stage
4. Document dry-run usage in deployment runbooks

---

## Integration Points

### Integration 1: CI/CD Pipeline (GitHub Actions)

**Relationship**: deployment-release workflows integrate with GitHub Actions for automated deployment on merge to main.

**Coordination Pattern**:

- GitHub Actions workflow triggers on push to main branch
- Workflow builds container image and pushes to GHCR
- deployment-release agent executes full deployment workflow
- Validation results reported back to GitHub commit status

**Example Usage**:

```yaml
# .github/workflows/deploy.yml
name: Deploy to Kubernetes

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Build and push image
        run: |
          docker build -t ghcr.io/kemosabe102/gauntlet-agents:${{ github.sha }} .
          echo ${{ secrets.GITHUB_TOKEN }} | docker login ghcr.io -u ${{ github.actor }} --password-stdin
          docker push ghcr.io/kemosabe102/gauntlet-agents:${{ github.sha }}

      - name: Deploy to Kubernetes
        run: |
          # Update image tag in kustomization
          cd k8s/local
          kustomize edit set image ghcr.io/kemosabe102/gauntlet-agents:${{ github.sha }}

          # Execute full deployment workflow
          kubectl apply -k .
          kubectl rollout status deployment/postgres -n gauntlet-agents
          kubectl rollout status deployment/redis -n gauntlet-agents
          kubectl rollout status deployment/api -n gauntlet-agents

      - name: Validate deployment
        run: |
          python scripts/validate_deployment.py --namespace gauntlet-agents
          if [ $? -ne 0 ]; then
            kubectl rollout undo deployment/api -n gauntlet-agents
            exit 1
          fi
```

**Dependencies**:

- GitHub Actions depends on deployment-release workflows for deployment logic
- deployment-release depends on GHCR for container image availability
- Both depend on kubectl context configuration in CI environment

---

### Integration 2: Observability Stack (Prometheus/Grafana)

**Relationship**: deployment-release workflows expose metrics endpoints validated by monitoring systems.

**Coordination Pattern**:

- Deployments include Prometheus annotations for scraping
- Validation workflow checks `/metrics` endpoint accessibility
- Monitoring alerts on deployment failures or health check issues
- Grafana dashboards visualize deployment rollout metrics

**Example Usage**:

```yaml
# k8s/local/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
spec:
  template:
    metadata:
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8000"
        prometheus.io/path: "/metrics"
    spec:
      containers:
      - name: api
        ports:
        - containerPort: 8000
          name: http

---
# Validation script checks metrics endpoint
def check_metrics_endpoint() -> bool:
    response = requests.get("http://api:8000/metrics")
    if response.status_code != 200:
        return False

    # Verify Prometheus format
    if "# HELP" not in response.text:
        return False

    return True
```

**Dependencies**:

- Prometheus depends on deployment-release for service discovery annotations
- deployment-release validation depends on metrics endpoint availability
- Grafana depends on Prometheus for deployment rollout metrics

---

### Integration 3: Git Repository (GitOps Workflow)

**Relationship**: deployment-release workflows maintain bidirectional sync with Git repository for configuration source of truth.

**Coordination Pattern**:

- All configuration changes committed to Git before applying to cluster
- Rollback operations include Git revert to maintain consistency
- Deployment scripts validate cluster state matches Git state
- Admission controllers enforce GitOps compliance (optional)

**Example Usage**:

```bash
# Configuration change workflow with Git integration
vim k8s/local/config/app-config.yaml
git diff k8s/local/config/app-config.yaml
# - LOG_LEVEL=INFO
# + LOG_LEVEL=DEBUG

git add k8s/local/config/app-config.yaml
git commit -m "feat: enable debug logging for troubleshooting"
git push origin main

# Apply to cluster (GitOps sync)
kubectl apply -k k8s/local/

# If rollback needed, revert Git first
git log --oneline k8s/local/config/app-config.yaml
# abc1234 feat: enable debug logging for troubleshooting
# def5678 feat: add database connection string

git revert abc1234
git push origin main

# Then rollback cluster to match Git
kubectl rollout undo deployment/api -n gauntlet-agents
```

**Dependencies**:

- deployment-release depends on Git for configuration versioning
- Git hooks depend on deployment-release validation scripts
- Rollback workflow depends on Git history for previous configurations

---

## Validation & Quality Checks

### Check 1: Deployment Health Validation

**What to Validate**: Application readiness and correct configuration after deployment.

**Validation Method**:

1. Execute `scripts/validate_deployment.py --namespace gauntlet-agents`
2. Check all 6 synthetic tests pass (health, readiness, metrics, database, redis, response time)
3. Verify no error events in recent event list
4. Confirm all pods in Running state with 1/1 READY

**Pass Criteria**:

- All 6 synthetic tests return ✅
- No error/warning events in last 5 minutes
- All pods Running with 0 restarts

**Fail Criteria**:

- Any synthetic test returns ❌
- Error events present (e.g., BackOff, Failed, Unhealthy)
- Pods in CrashLoopBackOff or ImagePullBackOff

**Remediation**:

- If health check fails, inspect logs: `kubectl logs deployment/api -n gauntlet-agents`
- If database connectivity fails, verify postgres service: `kubectl get svc postgres -n gauntlet-agents`
- If validation script errors, check port-forward: `kubectl port-forward svc/api 8000:8000 -n gauntlet-agents`

---

### Check 2: Configuration Consistency Validation

**What to Validate**: Cluster state matches Git repository state (GitOps compliance).

**Validation Method**:

1. Generate manifest from Git: `kubectl kustomize k8s/local/ > /tmp/git-manifest.yaml`
2. Get cluster state: `kubectl get all -n gauntlet-agents -o yaml > /tmp/cluster-state.yaml`
3. Compare relevant fields (image tags, ConfigMap hashes, replica counts)
4. Report any drift detected

**Pass Criteria**:

- ConfigMap hashes in cluster match Kustomize output
- Image tags in deployments match manifest
- Replica counts match specified values

**Fail Criteria**:

- Cluster ConfigMap hash differs from Kustomize hash
- Image tags manually edited in cluster (not in Git)
- Replica count modified without updating manifest

**Remediation**:

- If drift detected, re-apply from Git: `kubectl apply -k k8s/local/`
- If manual changes needed, update Git first then apply
- Consider admission controllers to prevent drift (e.g., OPA Gatekeeper)

---

### Check 3: Rollback Capability Validation

**What to Validate**: Ability to rollback deployment to previous revision without data loss.

**Validation Method**:

1. Check rollout history exists: `kubectl rollout history deployment/api -n gauntlet-agents`
2. Verify at least 2 revisions present (current + previous)
3. Inspect previous revision: `kubectl rollout history deployment/api --revision=N`
4. Confirm previous ConfigMap still exists in cluster
5. Test rollback in non-production environment

**Pass Criteria**:

- Rollout history shows 2+ revisions
- Previous ConfigMap exists (not garbage collected)
- Rollback test completes successfully

**Fail Criteria**:

- Only 1 revision in history (no previous state to rollback to)
- Previous ConfigMap deleted (immutability broken)
- Rollback test fails with errors

**Remediation**:

- If history missing, adjust `.spec.revisionHistoryLimit` in deployment
- If ConfigMap deleted, restore from Git: `kubectl apply -k k8s/local/`
- If rollback fails, use explicit revision: `kubectl rollout undo deployment/api --to-revision=N`

---

## Common Pitfalls & Solutions

| Pitfall                                  | Detection                                               | Solution                                                                                             |
| ---------------------------------------- | ------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| **Forgot to authenticate GHCR**          | ImagePullBackOff with "401 Unauthorized"                | `gh auth token \| docker login ghcr.io -u kemosabe102 --password-stdin`                              |
| **ConfigMap not updating pods**          | Pods running but configuration unchanged                | Enable Kustomize hash suffix: `disableNameSuffixHash: false` in kustomization.yaml                   |
| **Secrets in base64 but not working**    | Pods crashing with environment variable errors          | Check for newline in base64: use `echo -n` or `safe_base64()` function                               |
| **Port-forward fails during validation** | "Unable to listen on port 8000: address already in use" | Kill existing port-forward: `pkill -f "port-forward.*8000"`                                          |
| **Deployment hangs at rollout status**   | `kubectl rollout status` never completes                | Check pod events: `kubectl describe pod <pod>` for image pull or resource issues                     |
| **Rollback restores same broken config** | `kubectl rollout undo` doesn't fix issue                | Check revision history: `kubectl rollout history deployment/api` to verify different revision exists |
| **Dry-run passes but apply fails**       | Server-side validation succeeds but apply errors        | Check admission webhooks: `kubectl get validatingwebhookconfigurations`                              |
| **Old ConfigMaps accumulating**          | `kubectl get configmap` shows many unused ConfigMaps    | Manually garbage collect: `kubectl delete configmap app-config-<old-hash>`                           |

---

## Tools & Resources

### Recommended Tools

1. **kubectl**
   - **Purpose**: Primary Kubernetes CLI for cluster interaction
   - **When to Use**: All deployment, validation, and troubleshooting operations
   - **Documentation**: https://kubernetes.io/docs/reference/kubectl/

2. **Kustomize**
   - **Purpose**: Template-free Kubernetes configuration management with overlays
   - **When to Use**: Generating manifests with hash suffixes, managing multi-environment configs
   - **Documentation**: https://kubectl.docs.kubernetes.io/references/kustomize/

3. **kubectx / kubens**
   - **Purpose**: Fast context and namespace switching
   - **When to Use**: Managing multiple clusters or frequent namespace changes
   - **Documentation**: https://github.com/ahmetb/kubectx

4. **k9s**
   - **Purpose**: Terminal-based Kubernetes UI for navigation and debugging
   - **When to Use**: Real-time cluster monitoring, log inspection, resource editing
   - **Documentation**: https://k9scli.io/

5. **stern**
   - **Purpose**: Multi-pod log tailing (aggregates logs from multiple pods)
   - **When to Use**: Debugging distributed issues across pod replicas
   - **Documentation**: https://github.com/stern/stern

### Learning Resources

1. **Kubernetes Official Documentation - Deployments**: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
   - **Topic**: Deployment lifecycle, rollout strategies, rollback procedures
   - **Quality**: High

2. **Kustomize ConfigMapGenerator Guide**: https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/configmapgenerator/
   - **Topic**: Hash suffix generation, immutability patterns
   - **Quality**: High

3. **Kubernetes Troubleshooting Guide**: https://kubernetes.io/docs/tasks/debug/debug-application/
   - **Topic**: Event-driven debugging, log inspection, resource validation
   - **Quality**: High

4. **GitOps Principles**: https://opengitops.dev/
   - **Topic**: Git as source of truth, declarative configuration, automated sync
   - **Quality**: High

---

## Glossary

- **Idempotent**: Operation that produces the same result regardless of how many times it is executed
- **Hash Suffix**: Unique identifier appended to ConfigMap/Secret names based on content hash (e.g., app-config-5t4mb9chc7)
- **Immutability**: Property where configuration resources cannot be modified after creation (new hash triggers new resource)
- **Rollout**: Process of deploying new pod replicas while terminating old ones (rolling update strategy)
- **Dry-Run**: Validation mode that simulates operation without applying changes to cluster
- **GitOps**: Operational model where Git repository is single source of truth for infrastructure configuration
- **Synthetic Test**: Automated health check that simulates user behavior to validate application functionality
- **ClusterIP**: Kubernetes service type that exposes service only within cluster (requires port-forward for external access)
- **GHCR**: GitHub Container Registry - OCI-compliant container registry integrated with GitHub
- **Kustomize**: Kubernetes-native configuration management tool that uses overlays for multi-environment deployments

---

## Sources & References

1. **Kubernetes Deployment Documentation**: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
   - Accessed: 2025-10-24
   - Confidence: 0.95

2. **Kustomize ConfigMapGenerator**: https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/configmapgenerator/
   - Accessed: 2025-10-24
   - Confidence: 0.90

3. **Kubernetes Troubleshooting Best Practices**: https://kubernetes.io/docs/tasks/debug/
   - Accessed: 2025-10-24
   - Confidence: 0.92

4. **GitHub Container Registry Authentication**: https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry
   - Accessed: 2025-10-24
   - Confidence: 0.93

5. **GitOps Principles**: https://opengitops.dev/
   - Accessed: 2025-10-24
   - Confidence: 0.88

6. **Research Findings**: deployment-release domain investigation
   - Source: Internal research coordination
   - Confidence: 0.92

---

## Changelog

- **2025-10-24**: Initial documentation created from research findings (confidence: 0.92)
  - 5 core workflows documented with step-by-step procedures
  - 3 decision trees for root cause analysis, configuration strategy, and rollback scope
  - 3 best practices with examples and trade-offs
  - 3 anti-patterns with detection and migration strategies
  - 3 integration points (CI/CD, observability, GitOps)
  - 3 validation checks with pass/fail criteria

---

## Related Documentation

- `.claude/agents/deployment-release.md`: Agent definition and capabilities
- `k8s/local/kustomization.yaml`: Kustomize configuration with hash suffix settings
- `scripts/validate_deployment.py`: Synthetic health check implementation
- `docs/04-guides/kubernetes/deployment-strategies.md`: Advanced deployment patterns (if exists)
- `.github/workflows/deploy.yml`: CI/CD integration example (if exists)
