---
title: "Kubernetes Deployment Troubleshooting Framework"
date: 2025-11-08
status: ACTIVE
tags: [claude-docs]
---
# Kubernetes Deployment Troubleshooting Framework

**Category**: review
**Domain**: Kubernetes deployment diagnostics and failure mode resolution
**Confidence**: 0.95 (based on official Kubernetes documentation and established best practices)
**Last Updated**: 2025-10-24T00:00:00Z
**Agent**: deployment-release

---

## Overview

This documentation provides a structured, event-driven troubleshooting framework for diagnosing and resolving the four most common Kubernetes pod failure modes. The framework uses a universal diagnostic command sequence and pattern-matching approach to efficiently identify root causes and implement solutions.

**Key Concepts**:

- **Event-Driven Diagnosis**: Use kubectl events as primary source of truth for failure classification
- **Universal Command Sequence**: Standard diagnostic path applicable to all failure modes (get → describe → events → logs)
- **Exit Code Pattern Matching**: Map container exit codes to specific failure categories for rapid diagnosis

---

## Core Frameworks

### Framework 1: Universal Diagnostic Workflow

**Purpose**: Provide a consistent, efficient path from symptom detection to root cause identification for any pod failure.

**When to Use**:

- Any pod not reaching Running state
- Pod experiencing restarts or terminations
- Initial triage of unknown failures
- Validation after deployment changes

**Components**:

1. **Symptom Detection**: Identify pod state (Pending, CrashLoopBackOff, Error, etc.)
2. **Event Analysis**: Extract failure signatures from Kubernetes events
3. **Resource Inspection**: Examine pod specifications, limits, and node capacity
4. **Log Correlation**: Connect events to application-level failures

**How to Apply**:

1. **Check pod status**: `kubectl get pods -n <namespace>` to identify failing pods
2. **Inspect pod details**: `kubectl describe pod <pod-name> -n <namespace>` to extract state, events, and container info
3. **Review events**: `kubectl get events -n <namespace> --sort-by='.lastTimestamp'` for cluster-wide context
4. **Analyze logs**: `kubectl logs <pod-name> -n <namespace> --previous` (use --previous for restarted containers)

**Example from Codebase**:

```bash
# Standard diagnostic sequence
kubectl get pods -n production
# Output: api-deployment-7d8f5b9c6d-xyz12   0/1   CrashLoopBackOff   5   10m

kubectl describe pod api-deployment-7d8f5b9c6d-xyz12 -n production
# Look for: Last State, Exit Code, Events section

kubectl get events -n production --sort-by='.lastTimestamp' | grep api-deployment
# Extract: Event signatures and timing patterns

kubectl logs api-deployment-7d8f5b9c6d-xyz12 -n production --previous
# Correlate: Application errors with Kubernetes events
```

**Source**: Kubernetes Official Documentation - Troubleshooting Applications (https://kubernetes.io/docs/tasks/debug/debug-application/)

---

### Framework 2: Exit Code Classification System

**Purpose**: Map container exit codes to specific failure categories for rapid diagnosis and targeted resolution.

**When to Use**:

- Container terminations with non-zero exit codes
- Distinguishing between application errors and resource limits
- Automating failure classification in monitoring systems

**Components**:

1. **Exit Code 137**: OOM (Out of Memory) Kill - memory limit exceeded
2. **Exit Code 1**: General application error - check logs for specifics
3. **Exit Code 0**: Clean exit - investigate unexpected terminations with this code
4. **Exit Codes 126-127**: Permission/command issues - verify container entrypoint

**How to Apply**:

1. Extract exit code from `kubectl describe pod` output (Last State → Terminated → Exit Code)
2. Match exit code to category using classification table
3. Apply category-specific diagnostic workflow
4. Document resolution for pattern library

**Example from Codebase**:

```yaml
# kubectl describe pod output excerpt
Last State: Terminated
  Reason: OOMKilled
  Exit Code: 137
  Started: Wed, 23 Oct 2024 14:30:15 +0000
  Finished: Wed, 23 Oct 2024 14:31:47 +0000

# Classification: Exit Code 137 → OOM Kill → Check memory limits
kubectl describe pod <pod-name> | grep -A5 "Limits:"
# Resolution path: Compare actual memory usage vs limits, adjust resources
```

**Source**: Standard POSIX exit codes + Kubernetes-specific signals (SIGKILL=137)

---

### Framework 3: Event Signature Pattern Matching

**Purpose**: Use Kubernetes event messages as diagnostic fingerprints to classify failures without deep log analysis.

**When to Use**:

- Rapid triage of multiple failing pods
- Automated alerting and classification
- Initial diagnosis before detailed investigation

**Components**:

1. **CrashLoopBackOff Signature**: "Back-off restarting failed container"
2. **ImagePullBackOff Signature**: "Failed to pull image", "ErrImagePull"
3. **OOMKilled Signature**: "Reason: OOMKilled" in Events section
4. **Pending Signature**: "FailedScheduling", "Insufficient cpu/memory", "no nodes matched"

**How to Apply**:

1. Extract Events section from `kubectl describe pod` output
2. Search for signature patterns using grep or log aggregation
3. Match pattern to failure mode category
4. Execute category-specific diagnostic workflow

**Example from Codebase**:

```bash
# Pattern extraction
kubectl describe pod <pod-name> -n <namespace> | grep -A10 "Events:"

# Example output with signature
Events:
  Type     Reason     Age                From               Message
  ----     ------     ----               ----               -------
  Normal   Scheduled  5m                 default-scheduler  Successfully assigned namespace/pod to node1
  Normal   Pulling    5m                 kubelet            Pulling image "myapp:v1.2.3"
  Warning  Failed     3m (x3 over 5m)    kubelet            Failed to pull image "myapp:v1.2.3": rpc error: code = Unknown desc = Error response from daemon: manifest for myapp:v1.2.3 not found
  Warning  Failed     3m (x3 over 5m)    kubelet            Error: ErrImagePull
  Normal   BackOff    2m (x5 over 4m)    kubelet            Back-off pulling image "myapp:v1.2.3"
  Warning  Failed     2m (x5 over 4m)    kubelet            Error: ImagePullBackOff

# Signature match: "Failed to pull image" + "ErrImagePull" → ImagePullBackOff diagnosis path
```

**Source**: Kubernetes Event Architecture (https://kubernetes.io/docs/reference/kubernetes-api/cluster-resources/event-v1/)

---

## Processes & Workflows

### Workflow 1: CrashLoopBackOff Diagnosis

**Trigger Conditions**:

- Pod status shows `CrashLoopBackOff` in STATUS column
- Event signature: "Back-off restarting failed container"
- Exponential backoff timing pattern (10s, 20s, 40s… max 5min)

**Steps**:

1. **Extract Exit Code**:
   - **Input**: Pod name and namespace
   - **Output**: Exit code from Last State → Terminated
   - **Rationale**: Exit code indicates whether application error (1), OOM (137), or other issue
   - **Command**: `kubectl describe pod <pod-name> -n <namespace> | grep -A10 "Last State"`

2. **Retrieve Application Logs**:
   - **Input**: Pod name and previous container state
   - **Output**: Application error messages from failed container
   - **Rationale**: Application logs reveal configuration errors, missing dependencies, or runtime failures
   - **Command**: `kubectl logs <pod-name> -n <namespace> --previous`

3. **Inspect Resource Configuration**:
   - **Input**: Pod specification from describe output
   - **Output**: CPU/memory requests, limits, and liveness probe settings
   - **Rationale**: Insufficient resources or aggressive liveness probes can cause crashes
   - **Command**: `kubectl describe pod <pod-name> -n <namespace> | grep -A10 "Limits:"`

4. **Review Events Timeline**:
   - **Input**: Events section from describe output
   - **Output**: Chronological failure pattern and restart count
   - **Rationale**: Event timing reveals whether issue is transient (network) or persistent (config)
   - **Command**: `kubectl get events -n <namespace> --field-selector involvedObject.name=<pod-name> --sort-by='.lastTimestamp'`

**Success Criteria**:

- ✅ Root cause identified from logs or events
- ✅ Exit code mapped to specific failure category
- ✅ Resolution path documented (config change, resource adjustment, etc.)

**Failure Handling**:

- If logs are empty/truncated, check container command/entrypoint: `kubectl get pod <pod-name> -n <namespace> -o jsonpath='{.spec.containers[0].command}'`
- If exit code is 0 (clean exit), investigate liveness probe configuration for false positive kills
- If pattern is intermittent, enable debug logging and increase log retention

**Example Execution**:

```bash
# Step 1: Identify crash pattern
kubectl get pods -n production | grep CrashLoopBackOff
# Output: api-deployment-7d8f5b9c6d-xyz12   0/1   CrashLoopBackOff   8   25m

# Step 2: Extract exit code
kubectl describe pod api-deployment-7d8f5b9c6d-xyz12 -n production | grep -A5 "Last State"
# Output: Exit Code: 1 (application error)

# Step 3: Get previous logs
kubectl logs api-deployment-7d8f5b9c6d-xyz12 -n production --previous
# Output: ERROR: Database connection failed - host 'postgres-service' port 5432: connection refused

# Step 4: Verify service existence
kubectl get svc postgres-service -n production
# Output: Error from server (NotFound): services "postgres-service" not found

# Resolution: Incorrect service name in application config, should be "postgres"
```

---

### Workflow 2: ImagePullBackOff Diagnosis

**Trigger Conditions**:

- Pod status shows `ImagePullBackOff` or `ErrImagePull`
- Event signature: "Failed to pull image", "manifest not found", "unauthorized"
- Container remains in Waiting state with Reason: ImagePullBackOff

**Steps**:

1. **Extract Image Details**:
   - **Input**: Pod specification
   - **Output**: Full image name, tag, and pull policy
   - **Rationale**: Verify image name, tag, and registry URL are correct
   - **Command**: `kubectl get pod <pod-name> -n <namespace> -o jsonpath='{.spec.containers[*].image}'`

2. **Verify Image Existence**:
   - **Input**: Image name and tag from step 1
   - **Output**: Confirmation of image availability in registry
   - **Rationale**: Distinguish between typos, missing tags, and authentication issues
   - **Command**: `docker pull <image-name:tag>` (manual verification) or check registry UI

3. **Check Image Pull Secrets**:
   - **Input**: Pod specification and namespace
   - **Output**: imagePullSecrets configuration and secret existence
   - **Rationale**: Private registries require valid authentication credentials
   - **Command**: `kubectl describe pod <pod-name> -n <namespace> | grep -A5 "Image Pull Secrets"` then `kubectl get secret <secret-name> -n <namespace>`

4. **Inspect Events for Error Details**:
   - **Input**: Events section from describe output
   - **Output**: Specific error message (unauthorized, not found, rate limit, network timeout)
   - **Rationale**: Event messages pinpoint exact failure reason (auth vs availability vs network)
   - **Command**: `kubectl describe pod <pod-name> -n <namespace> | grep -A15 "Events:"`

**Success Criteria**:

- ✅ Image name and tag verified as correct
- ✅ Image accessibility confirmed (exists in registry)
- ✅ Authentication credentials validated (if private registry)

**Failure Handling**:

- If image doesn't exist, check CI/CD pipeline for build failures or incorrect deployment manifest
- If authentication fails, regenerate imagePullSecret and update in namespace: `kubectl create secret docker-registry <name> --docker-server=<registry> --docker-username=<user> --docker-password=<pass> -n <namespace>`
- If rate limited (e.g., Docker Hub), implement registry mirror or upgrade registry plan

**Example Execution**:

```bash
# Step 1: Identify image pull failure
kubectl get pods -n staging | grep ImagePullBackOff
# Output: frontend-7b8c9d-abc45   0/1   ImagePullBackOff   3   5m

# Step 2: Extract image details
kubectl get pod frontend-7b8c9d-abc45 -n staging -o jsonpath='{.spec.containers[0].image}'
# Output: myregistry.io/frontend:v2.1.0

# Step 3: Check events for error
kubectl describe pod frontend-7b8c9d-abc45 -n staging | grep -A5 "Failed to pull"
# Output: Failed to pull image "myregistry.io/frontend:v2.1.0": rpc error: code = Unknown desc = Error response from daemon: manifest for myregistry.io/frontend:v2.1.0 not found: manifest unknown: manifest unknown

# Step 4: Verify image in registry
curl -u <user>:<token> https://myregistry.io/v2/frontend/tags/list
# Output: {"name":"frontend","tags":["v2.0.0","v2.0.1"]} # v2.1.0 missing!

# Resolution: v2.1.0 tag doesn't exist in registry, update deployment to use v2.0.1
```

---

### Workflow 3: OOMKilled Diagnosis

**Trigger Conditions**:

- Pod status shows repeated restarts with Last State: OOMKilled
- Exit code 137 in terminated container
- Event signature: "Reason: OOMKilled" in Events section

**Steps**:

1. **Confirm OOM Kill Signal**:
   - **Input**: Pod describe output
   - **Output**: Exit code 137 and Reason: OOMKilled
   - **Rationale**: Exit code 137 (128 + SIGKILL=9) definitively indicates OOM termination
   - **Command**: `kubectl describe pod <pod-name> -n <namespace> | grep -A5 "Last State"`

2. **Extract Memory Limits**:
   - **Input**: Pod resource specification
   - **Output**: Memory requests and limits for affected container
   - **Rationale**: Compare actual usage to configured limits to determine if limits are too low
   - **Command**: `kubectl get pod <pod-name> -n <namespace> -o jsonpath='{.spec.containers[0].resources.limits.memory}'`

3. **Measure Current Memory Usage**:
   - **Input**: Running pod (if available) or historical metrics
   - **Output**: Actual memory consumption in MB/GB
   - **Rationale**: Determine if OOM is from traffic spike, memory leak, or baseline too high
   - **Command**: `kubectl top pod <pod-name> -n <namespace>` (requires metrics-server)

4. **Analyze Memory Growth Pattern**:
   - **Input**: Application logs and metrics history
   - **Output**: Memory usage trend over time (steady, growing, spike)
   - **Rationale**: Distinguish between insufficient limits (quick fix) vs memory leak (code fix)
   - **Command**: Review monitoring dashboards (Prometheus/Grafana) or kubectl logs for memory-related warnings

**Success Criteria**:

- ✅ Memory limit vs actual usage gap quantified
- ✅ Memory growth pattern identified (steady, leak, spike)
- ✅ Resolution strategy selected (increase limits, fix leak, add HPA)

**Failure Handling**:

- If memory usage is close to limit under normal load, increase memory limits by 50-100%
- If memory usage grows continuously, investigate memory leaks in application code (heap dumps, profiling)
- If node-level OOM (not container limit), check node capacity: `kubectl describe node <node-name> | grep -A5 "Allocated resources"`

**Example Execution**:

```bash
# Step 1: Identify OOMKilled pod
kubectl get pods -n production | grep OOMKilled
# Output: worker-6f9d8c-def78   0/1   OOMKilled   2   8m

# Step 2: Confirm exit code 137
kubectl describe pod worker-6f9d8c-def78 -n production | grep -A5 "Last State"
# Output:
#   Last State: Terminated
#     Reason: OOMKilled
#     Exit Code: 137

# Step 3: Check memory limits
kubectl get pod worker-6f9d8c-def78 -n production -o jsonpath='{.spec.containers[0].resources.limits.memory}'
# Output: 512Mi

# Step 4: Review usage before kill
kubectl top pod worker-6f9d8c-def78 -n production
# Output: NAME                     CPU(cores)   MEMORY(bytes)
#         worker-6f9d8c-def78      100m         498Mi  # Usage near limit!

# Resolution: Increase memory limit from 512Mi to 1Gi in deployment manifest
```

---

### Workflow 4: Pending Pod Diagnosis

**Trigger Conditions**:

- Pod status stuck in `Pending` state for >30 seconds
- Event signature: "FailedScheduling", "Insufficient cpu/memory", "no nodes matched"
- Pod not assigned to any node (NODE column shows `<none>`)

**Steps**:

1. **Check Scheduling Events**:
   - **Input**: Pod events section
   - **Output**: FailedScheduling reason (resources, selector, taints, PVC)
   - **Rationale**: Events contain exact reason scheduler couldn't place pod
   - **Command**: `kubectl describe pod <pod-name> -n <namespace> | grep -A10 "Events:"`

2. **Verify Node Resources**:
   - **Input**: Node capacity and allocated resources
   - **Output**: Available CPU and memory across all nodes
   - **Rationale**: Determine if cluster has sufficient capacity for pod requests
   - **Command**: `kubectl describe nodes | grep -A5 "Allocated resources"`

3. **Validate Node Selectors & Affinity**:
   - **Input**: Pod spec nodeSelector, affinity, and tolerations
   - **Output**: Node label requirements and matching nodes
   - **Rationale**: Ensure pod constraints allow scheduling to available nodes
   - **Command**: `kubectl get pod <pod-name> -n <namespace> -o jsonpath='{.spec.nodeSelector}'` then `kubectl get nodes --show-labels`

4. **Inspect PersistentVolume Bindings**:
   - **Input**: Pod volumes and PVC status
   - **Output**: PVC binding state and available PVs
   - **Rationale**: PVC mount failures prevent pod scheduling even with sufficient compute resources
   - **Command**: `kubectl get pvc -n <namespace>` and check STATUS column for `Bound`

**Success Criteria**:

- ✅ Scheduling failure reason identified (resources, selector, taints, PVC)
- ✅ Cluster capacity validated (sufficient nodes available)
- ✅ Resolution path documented (scale nodes, relax constraints, fix PVC)

**Failure Handling**:

- If insufficient resources, scale cluster: `kubectl scale deployment <name> --replicas=N` or add nodes to cluster
- If node selector mismatch, either relax pod constraints or add matching labels to nodes: `kubectl label nodes <node-name> <key>=<value>`
- If PVC unbound, check storage class exists: `kubectl get storageclass` and provision PV if needed

**Example Execution**:

```bash
# Step 1: Identify pending pod
kubectl get pods -n production | grep Pending
# Output: database-5c7d9f-ghi89   0/1   Pending   0   3m

# Step 2: Check events
kubectl describe pod database-5c7d9f-ghi89 -n production | grep -A10 "Events:"
# Output:
#   Type     Reason            Age   From               Message
#   Warning  FailedScheduling  2m    default-scheduler  0/3 nodes are available: 3 Insufficient memory.

# Step 3: Check node resources
kubectl describe nodes | grep -A5 "Allocated resources"
# Output shows all nodes at >90% memory allocation

# Step 4: Verify pod memory request
kubectl get pod database-5c7d9f-ghi89 -n production -o jsonpath='{.spec.containers[0].resources.requests.memory}'
# Output: 4Gi

# Resolution: Either add nodes to cluster or reduce memory request if overprovisioned
```

---

## Decision Trees

### Decision 1: Initial Failure Mode Classification

```
IF pod status = "CrashLoopBackOff"
  THEN execute CrashLoopBackOff Diagnosis Workflow (check exit code → logs → probe config)
  BECAUSE pod is starting but application/config causes container exit

ELSE IF pod status = "ImagePullBackOff" OR "ErrImagePull"
  THEN execute ImagePullBackOff Diagnosis Workflow (verify image → check auth → test pull)
  BECAUSE container image cannot be retrieved from registry

ELSE IF last_state.reason = "OOMKilled" AND exit_code = 137
  THEN execute OOMKilled Diagnosis Workflow (check limits → measure usage → analyze trend)
  BECAUSE container exceeded memory limits and was killed by kernel

ELSE IF pod status = "Pending" AND scheduling_events contain "FailedScheduling"
  THEN execute Pending Pod Diagnosis Workflow (check resources → validate selectors → inspect PVC)
  BECAUSE scheduler cannot find suitable node for pod placement

ELSE
  THEN follow Universal Diagnostic Workflow (get → describe → events → logs)
  BECAUSE failure mode doesn't match common patterns, requires deeper investigation
```

**Example Scenarios**:

1. **Scenario**: Pod shows status `CrashLoopBackOff`, events show "Back-off restarting", exit code 1 → **Decision**: Execute CrashLoopBackOff workflow, focus on application logs for config errors
2. **Scenario**: Pod shows status `Pending`, events show "0/3 nodes available: 2 Insufficient cpu, 1 node(s) had taint" → **Decision**: Execute Pending Pod workflow, check resource requests and tolerations

---

### Decision 2: CrashLoopBackOff Root Cause Routing

```
IF exit_code = 137
  THEN route to OOMKilled Diagnosis (this is memory limit issue, not application crash)
  BECAUSE exit code 137 specifically indicates SIGKILL from OOM

ELSE IF exit_code = 1 AND logs show "connection refused" OR "cannot connect"
  THEN investigate dependent services (DNS, database, external APIs)
  BECAUSE application cannot reach required upstream dependencies

ELSE IF exit_code = 1 AND logs show "permission denied" OR "EACCES"
  THEN check security context, file permissions, and ServiceAccount
  BECAUSE pod lacks necessary permissions for filesystem or Kubernetes API access

ELSE IF exit_code = 0 AND liveness_probe configured
  THEN review liveness probe settings (timeout, period, threshold)
  BECAUSE clean exit with liveness probe suggests false positive health check failure

ELSE IF logs are empty OR minimal
  THEN verify container command/entrypoint and check image health
  BECAUSE container may be exiting before application starts logging

ELSE
  THEN deep-dive application logs with increased verbosity
  BECAUSE standard patterns not detected, requires application-specific debugging
```

**Example Scenarios**:

1. **Scenario**: Exit code 1, logs show "Error: ECONNREFUSED 10.96.0.10:5432" → **Decision**: Check if postgres service exists and is ready (`kubectl get svc,ep`)
2. **Scenario**: Exit code 0, liveness probe with 1s timeout → **Decision**: Increase timeout to 5s and initialDelaySeconds to 30s

---

### Decision 3: ImagePullBackOff Resolution Path

```
IF events contain "manifest not found" OR "manifest unknown"
  THEN verify image tag exists in registry (CI/CD build issue or typo)
  BECAUSE image with specified tag was never pushed to registry

ELSE IF events contain "unauthorized" OR "authentication required"
  THEN check imagePullSecrets exist and are valid (credentials may be expired)
  BECAUSE registry requires authentication and provided credentials failed

ELSE IF events contain "TLS handshake timeout" OR "dial tcp timeout"
  THEN investigate network connectivity (firewall, proxy, DNS resolution)
  BECAUSE registry is unreachable from cluster network

ELSE IF events contain "toomanyrequests" OR "rate limit"
  THEN implement registry mirror OR upgrade registry plan
  BECAUSE hitting Docker Hub or other registry rate limits

ELSE IF events contain "server gave HTTP response to HTTPS client"
  THEN configure insecure registry in container runtime (for testing only)
  BECAUSE registry requires HTTP but runtime expects HTTPS

ELSE
  THEN manually test image pull: `docker pull <image>` from cluster node
  BECAUSE error message unclear, need direct validation of image accessibility
```

**Example Scenarios**:

1. **Scenario**: Events show "Failed to pull image: unauthorized: incorrect username or password" → **Decision**: Regenerate imagePullSecret with valid credentials and restart pod
2. **Scenario**: Events show "manifest for myapp:latest not found" → **Decision**: Check CI pipeline logs, verify image build succeeded and was pushed

---

### Decision 4: OOMKilled Resolution Strategy

```
IF (memory_usage / memory_limit) > 0.9 AND usage_trend = "steady"
  THEN increase memory limits by 25-50% (pod needs more baseline memory)
  BECAUSE application consistently uses near-limit memory under normal load

ELSE IF memory_usage grows over time (leak pattern)
  THEN escalate to development team for memory profiling and leak fix
  BECAUSE application has memory leak requiring code-level fix (increasing limits only delays)

ELSE IF memory_usage spikes during specific events (traffic surge)
  THEN implement HorizontalPodAutoscaler (HPA) to scale replicas during load
  BECAUSE workload is bursty, need dynamic scaling instead of static over-provisioning

ELSE IF node shows "System OOM" (not container limit)
  THEN check node capacity and reduce pod density OR add nodes
  BECAUSE node itself ran out of memory, not just container limit

ELSE IF memory_requests << memory_limits (e.g., 100Mi request, 2Gi limit)
  THEN align requests closer to limits (e.g., 1.5Gi request, 2Gi limit)
  BECAUSE low requests cause over-scheduling and node-level OOM

ELSE
  THEN collect heap dump and analyze memory distribution
  BECAUSE standard patterns not detected, requires application profiling
```

**Example Scenarios**:

1. **Scenario**: Memory usage steady at 950Mi, limit 1Gi, no growth over 24h → **Decision**: Increase limit to 1.5Gi
2. **Scenario**: Memory usage grows from 200Mi to 1Gi over 6 hours → **Decision**: Memory leak, escalate to developers for heap dump analysis

---

## Best Practices

### Practice 1: Event-First Diagnosis

**Principle**: Always start troubleshooting with Kubernetes events rather than pod logs, as events provide structured failure classification.

**Implementation**:

- Use `kubectl describe pod` as first diagnostic command (includes events)
- Sort events by timestamp: `kubectl get events --sort-by='.lastTimestamp'`
- Filter events by object: `kubectl get events --field-selector involvedObject.name=<pod-name>`
- Correlate event timing with pod restarts/transitions

**Benefits**:

- ✅ Faster root cause identification (events are pre-classified by Kubernetes)
- ✅ Reduced need for deep log analysis in 80% of cases
- ✅ Events persist after pod deletion (unlike logs)

**Trade-offs**:

- ⚠️ Events expire after 1 hour by default (increase retention if needed)
- ⚠️ Events may be truncated in high-volume clusters
- ⚠️ Application-specific errors still require log analysis

**Example**:

```bash
# ✅ Event-first approach
kubectl describe pod failing-pod -n production | grep -A15 "Events:"
# Immediately see: "FailedScheduling: Insufficient memory" → Resolution clear

# vs. ❌ Log-first approach (less efficient)
kubectl logs failing-pod -n production
# Output: (empty, pod never started) → Still need to check describe output
```

---

### Practice 2: Structured Exit Code Analysis

**Principle**: Map container exit codes to diagnostic categories to enable rapid classification and automated alerting.

**Implementation**:

- Extract exit code from Last State → Terminated → Exit Code field
- Maintain exit code lookup table:
  - 0: Clean exit (investigate unexpected terminations)
  - 1: General application error (check logs)
  - 137: OOMKilled (SIGKILL from memory limit)
  - 139: Segmentation fault (SIGSEGV, possible code bug)
  - 143: Graceful termination (SIGTERM, expected during rollouts)
- Document application-specific exit codes in deployment annotations

**Benefits**:

- ✅ Instant classification without reading logs
- ✅ Enables automated remediation (e.g., auto-scale on exit 137)
- ✅ Clearer escalation paths (exit 1 → logs, exit 137 → resources)

**Trade-offs**:

- ⚠️ Requires disciplined application error handling (return meaningful exit codes)
- ⚠️ Some applications use exit code 1 for all errors (reduces usefulness)

**Example**:

```yaml
# Document custom exit codes in deployment annotations
apiVersion: apps/v1
kind: Deployment
metadata:
  annotations:
    exit-codes: |
      2: Configuration validation failed
      3: Database migration error
      4: Required external service unavailable
spec:
  template:
    spec:
      containers:
        - name: app
          image: myapp:v1
```

---

### Practice 3: Resource Request-Limit Alignment

**Principle**: Keep memory requests and limits close (within 20%) to prevent node overcommitment and reduce OOMKilled incidents.

**Implementation**:

- Set memory requests to 80-90% of limits (e.g., 800Mi request, 1Gi limit)
- For CPU: Use lower requests for burstable workloads (e.g., 100m request, 1000m limit)
- Monitor actual usage with `kubectl top` before setting initial values
- Use Vertical Pod Autoscaler (VPA) for automatic right-sizing

**Benefits**:

- ✅ Reduces node-level OOM risk (scheduler has accurate memory expectations)
- ✅ Prevents excessive pod density causing cascading failures
- ✅ Limits provide safety bounds for memory leaks without wasting resources

**Trade-offs**:

- ⚠️ May reduce cluster utilization if requests are over-provisioned
- ⚠️ Requires iterative tuning based on actual workload patterns

**Example**:

```yaml
# ✅ Good: Aligned requests and limits
resources:
  requests:
    memory: "800Mi"
    cpu: "100m"
  limits:
    memory: "1Gi"
    cpu: "1000m"

# ❌ Bad: Large gap causes overcommitment
resources:
  requests:
    memory: "100Mi"   # Scheduler thinks pod needs 100Mi
    cpu: "50m"
  limits:
    memory: "4Gi"     # Pod actually uses 3Gi → node overcommitted
    cpu: "2000m"
```

---

## Anti-Patterns

### Anti-Pattern 1: Log-Only Debugging Without Events

**Problem**: Starting troubleshooting with `kubectl logs` skips structured Kubernetes event data, leading to slower diagnosis and missed cluster-level issues.

**Detection**:

- 🔴 First command is `kubectl logs` instead of `kubectl describe pod`
- 🔴 Spending >5 minutes analyzing logs before checking pod events
- 🔴 Missing scheduling failures, image pull errors, or resource constraints

**Consequences**:

- ❌ Slower time to resolution (logs don't show scheduling/image issues)
- ❌ Incomplete diagnosis (application logs don't reveal cluster constraints)
- ❌ Repeated investigations of same root cause (events provide pattern)

**Better Approach**:

```bash
✅ Preferred Pattern:
# 1. Start with events for structured failure classification
kubectl describe pod <pod-name> -n <namespace> | grep -A15 "Events:"
# Outcome: Immediate identification of ImagePullBackOff, FailedScheduling, OOMKilled

# 2. Only then get logs for application-specific errors
kubectl logs <pod-name> -n <namespace> --previous

❌ Anti-Pattern:
# Starting with logs misses cluster-level issues
kubectl logs <pod-name> -n <namespace>
# Outcome: No output (pod never started due to ImagePullBackOff)
# Now must go back to kubectl describe → wasted time
```

**Migration Strategy**:

1. Train team to always run `kubectl describe pod` first (embed in runbooks)
2. Create shell alias: `alias kdbg='kubectl describe pod'` to encourage event-first approach
3. Build monitoring alerts from Kubernetes events (not just logs)

---

### Anti-Pattern 2: Ignoring Exit Codes

**Problem**: Not checking container exit codes leads to misclassification of failures (treating OOMKilled as application error).

**Detection**:

- 🔴 Immediate log analysis without checking Last State → Exit Code
- 🔴 Describing OOMKilled as "application crash" instead of resource limit issue
- 🔴 Missing pattern: repeated exit code 137 without memory limit investigation

**Consequences**:

- ❌ Wrong resolution applied (debugging application instead of increasing memory)
- ❌ Repeated failures (increasing limits would prevent recurrence)
- ❌ Wasted developer time (investigating "bugs" that are resource constraints)

**Better Approach**:

```bash
✅ Preferred Pattern:
# Always check exit code before diving into logs
kubectl describe pod <pod-name> -n <namespace> | grep -A5 "Last State"
# Output: Exit Code: 137, Reason: OOMKilled → Memory limit issue, not application bug

# Then verify with resource inspection
kubectl get pod <pod-name> -n <namespace> -o jsonpath='{.spec.containers[0].resources.limits.memory}'
# Resolution: Increase memory limit

❌ Anti-Pattern:
# Skipping exit code check
kubectl logs <pod-name> -n <namespace> --previous
# Outcome: No obvious error in logs (application was killed mid-operation)
# Spend hours debugging "application bug" that doesn't exist
```

**Migration Strategy**:

1. Add exit code check to standard troubleshooting checklist
2. Create monitoring alert rules for specific exit codes (137=OOM, 139=segfault)
3. Document exit code meanings in deployment annotations for team reference

---

### Anti-Pattern 3: Blanket Memory/CPU Increases Without Analysis

**Problem**: Automatically doubling resources on every OOMKilled incident without measuring actual usage or investigating memory leaks.

**Detection**:

- 🔴 Increasing memory limits without checking `kubectl top` or historical metrics
- 🔴 Pattern: limit increased 2x, 4x, 8x over time but OOMKilled continues
- 🔴 No distinction between baseline insufficiency vs memory leak

**Consequences**:

- ❌ Wasteful resource allocation (cluster costs grow exponentially)
- ❌ Memory leaks hidden by increased limits (problem deferred, not solved)
- ❌ Eventually hits node capacity limits (can't scale further)

**Better Approach**:

```bash
✅ Preferred Pattern:
# 1. Measure actual usage before OOMKilled
kubectl top pod <pod-name> -n <namespace>
# Output: 480Mi / 512Mi (memory limit) → Usage near limit, increase justified

# 2. Check usage trend over time (requires monitoring)
# Query Prometheus: rate(container_memory_usage_bytes[1h])
# Outcome: Usage steady at 480Mi → Increase to 768Mi (50% headroom)
#          Usage growing 10Mi/hour → Memory leak, escalate to developers

# 3. Set limits based on measured usage + 20-30% headroom
kubectl set resources deployment <name> --limits=memory=768Mi -n <namespace>

❌ Anti-Pattern:
# Blindly doubling limits without measurement
kubectl set resources deployment <name> --limits=memory=2Gi -n <namespace>
# Outcome: OOMKilled continues (was memory leak), now wasting 2x resources
```

**Migration Strategy**:

1. Require `kubectl top` output or metrics screenshot before approving limit increases
2. Implement Vertical Pod Autoscaler (VPA) for data-driven recommendations
3. Set up Grafana dashboard showing memory usage trend over 24h for leak detection

---

### Anti-Pattern 4: Using `latest` Tag in Production

**Problem**: `latest` tag causes ImagePullBackOff confusion (what version is actually deployed?) and prevents rollback to known-good versions.

**Detection**:

- 🔴 Image field in deployment: `image: myapp:latest`
- 🔴 ImagePullBackOff with `latest` tag (can't tell if image was pulled before)
- 🔴 Unable to identify which code version is running in production

**Consequences**:

- ❌ Ambiguous troubleshooting (which version caused the failure?)
- ❌ Cannot rollback (no specific version to target)
- ❌ Cache confusion (nodes may have different `latest` versions)

**Better Approach**:

```yaml
✅ Preferred Pattern:
# Use semantic versioning or git commit SHA
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
      - name: app
        image: myapp:v1.2.3  # Immutable tag
        # OR
        image: myapp:sha-a1b2c3d  # Git SHA for traceability

# Set imagePullPolicy to IfNotPresent (don't re-pull same tag)
        imagePullPolicy: IfNotPresent

❌ Anti-Pattern:
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
      - name: app
        image: myapp:latest  # Ambiguous version
        imagePullPolicy: Always  # Re-pulls every time, hitting rate limits
```

**Migration Strategy**:

1. Update CI/CD to tag images with version + SHA: `v1.2.3-sha-a1b2c3d`
2. Add admission webhook to reject deployments with `latest` tag in production namespace
3. Document version → deployment mapping in release notes for rollback reference

---

## Integration Points

### Integration 1: Debugger Agent

**Relationship**: deployment-release delegates to debugger agent when application-level bugs are confirmed (after ruling out cluster/config issues).

**Coordination Pattern**:

- deployment-release performs initial triage: classify failure mode, check events, inspect resources
- If exit code 1 + logs show application errors (stack traces, exceptions) → delegate to debugger
- debugger uses deployment-release's findings as context (exit code, logs, resource constraints)
- debugger performs code-level analysis: trace errors, inspect code paths, propose fixes

**Example Usage**:

```
User Request: "Pod keeps crashing with CrashLoopBackOff"

deployment-release workflow:
1. Check events: "Back-off restarting failed container" ✓
2. Extract exit code: 1 (application error) ✓
3. Get logs: "NullPointerException at line 142 in PaymentService.java" → Application bug identified
4. Delegate to debugger: "Investigate NullPointerException in PaymentService.java (pod logs attached)"

debugger workflow:
5. Read PaymentService.java around line 142
6. Trace null reference to missing config validation
7. Propose fix: Add null check before accessing payment gateway config
```

**Dependencies**:

- deployment-release depends on debugger for application code fixes
- debugger depends on deployment-release for pod context (logs, events, resource info)

---

### Integration 2: development Agent

**Relationship**: deployment-release identifies configuration or resource specification issues in manifests, development applies fixes.

**Coordination Pattern**:

- deployment-release diagnoses root cause in Kubernetes manifests (wrong resource limits, missing secrets, incorrect selectors)
- Delegate to development with specific fix requirements (file path, change description)
- development modifies YAML files following Kubernetes best practices
- deployment-release validates fix by re-deploying and checking pod status

**Example Usage**:

```
User Request: "Fix OOMKilled errors in production API"

deployment-release workflow:
1. Confirm OOMKilled (exit code 137) ✓
2. Check limits: memory=512Mi, usage=498Mi → Limit too low
3. Delegate to development: "Increase memory limit from 512Mi to 1Gi in k8s/production/api-deployment.yaml"

development workflow:
4. Read k8s/production/api-deployment.yaml
5. Update resources.limits.memory: 512Mi → 1Gi
6. Update resources.requests.memory: 400Mi → 800Mi (maintain alignment)
7. Return: File modified successfully

deployment-release validation:
8. kubectl apply -f k8s/production/api-deployment.yaml
9. kubectl rollout status deployment/api -n production
10. Monitor for OOMKilled recurrence → Success
```

**Dependencies**:

- deployment-release depends on development for manifest modifications
- development depends on deployment-release for Kubernetes-specific validation

---

### Integration 3: Test-Runner Agent

**Relationship**: deployment-release validates deployment health after fixes, test-runner executes integration tests to confirm end-to-end functionality.

**Coordination Pattern**:

- deployment-release applies fix and verifies pod reaches Running state
- Delegate to test-runner to execute smoke tests or integration test suite
- test-runner reports PASS/FAIL with test output
- If FAIL, deployment-release checks for new pod failures (rollback if needed)

**Example Usage**:

```
User Request: "Deploy new version and validate"

deployment-release workflow:
1. kubectl set image deployment/api api=myapp:v2.0.0 -n production
2. kubectl rollout status deployment/api -n production → SUCCESS (pods running)
3. Delegate to test-runner: "Execute integration tests against production API"

test-runner workflow:
4. uv run pytest tests/integration/ --env=production
5. Return: 8 passed, 0 failed → PASS

deployment-release validation:
6. Monitor pod stability for 5 minutes (no restarts)
7. Report: Deployment successful, all tests passing
```

**Dependencies**:

- deployment-release depends on test-runner for functional validation
- test-runner depends on deployment-release to ensure pods are ready before testing

---

## Validation & Quality Checks

### Check 1: Pod Health Validation

**What to Validate**: All pods reach Running state with 1/1 ready containers after troubleshooting actions.

**Validation Method**:

1. Check pod status: `kubectl get pods -n <namespace> | grep <pod-name>`
2. Verify ready column shows "1/1" (or N/N for multi-container pods)
3. Confirm status is "Running" (not Pending, CrashLoopBackOff, etc.)
4. Check restart count hasn't increased for 5 minutes
5. Verify liveness/readiness probes passing: `kubectl describe pod <pod-name> -n <namespace> | grep -A5 "Liveness:"`

**Pass Criteria**:

- STATUS = "Running"
- READY = "1/1" (all containers ready)
- RESTARTS = stable (no new restarts in last 5 minutes)
- Events section shows no warnings/errors in last 5 minutes

**Fail Criteria**:

- Pod stuck in Pending, CrashLoopBackOff, or Error
- Ready shows "0/1" or partial readiness
- Restart count incrementing
- Recent events show failures (ImagePullBackOff, FailedScheduling, OOMKilled)

**Remediation**: Re-run appropriate diagnostic workflow based on failure mode, verify fix was applied correctly, check for secondary issues.

---

### Check 2: Resource Utilization Validation

**What to Validate**: Pod resource usage is within healthy bounds after OOMKilled or scheduling fixes (not approaching limits).

**Validation Method**:

1. Measure current usage: `kubectl top pod <pod-name> -n <namespace>`
2. Extract limits: `kubectl get pod <pod-name> -n <namespace> -o jsonpath='{.spec.containers[0].resources.limits}'`
3. Calculate utilization: `(usage / limit) × 100%`
4. Verify CPU and memory usage are <80% of limits under normal load
5. Monitor for 15-30 minutes to ensure stability (no growth toward limit)

**Pass Criteria**:

- Memory usage <80% of limit (e.g., 600Mi usage with 1Gi limit)
- CPU usage <70% of limit on average (<90% peaks acceptable)
- Usage stable over 15+ minutes (no continuous growth)

**Fail Criteria**:

- Memory usage >90% of limit (OOM risk)
- CPU throttling (usage hits limit frequently)
- Usage growing continuously (memory leak pattern)

**Remediation**: If usage >80%, increase limits by 25-50%. If usage growing, investigate memory leak (heap dump, profiling). If CPU throttling, increase CPU limits or add more replicas (HPA).

---

### Check 3: Event Log Validation

**What to Validate**: No error/warning events in past 10 minutes after applying fixes (confirms resolution).

**Validation Method**:

1. Get recent events: `kubectl get events -n <namespace> --sort-by='.lastTimestamp' | tail -20`
2. Filter for pod name: `kubectl get events -n <namespace> --field-selector involvedObject.name=<pod-name>`
3. Check for Type=Warning or Type=Error in last 10 minutes
4. Verify no "FailedScheduling", "BackOff", "FailedMount", or "Unhealthy" events
5. Confirm only Normal events (Scheduled, Pulled, Created, Started)

**Pass Criteria**:

- No Type=Warning or Type=Error events in last 10 minutes
- Recent events show successful operations: "Scheduled", "Pulling", "Pulled", "Created", "Started"
- No events related to previous failure mode (e.g., no more ImagePullBackOff events)

**Fail Criteria**:

- Warning/Error events present after fix application
- Repeated failure events (same failure mode recurring)
- New failure mode introduced (e.g., fixed ImagePullBackOff but now OOMKilled)

**Remediation**: Analyze new events to determine if fix was incomplete, caused secondary issue, or different root cause exists. Re-run diagnostic workflow for new failure mode.

---

## Common Pitfalls & Solutions

| Pitfall                                                          | Detection                                                                                            | Solution                                                                                                                                                 |
| ---------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| Using `kubectl logs` without `--previous` flag after pod restart | Logs show current running container (which may be starting successfully) instead of failed container | Always use `--previous` flag when investigating CrashLoopBackOff: `kubectl logs <pod> --previous`                                                        |
| Ignoring liveness probe configuration in CrashLoopBackOff        | Exit code 0 (clean exit) but pod keeps restarting                                                    | Check liveness probe settings in describe output: timeout too short, initialDelaySeconds insufficient, or failureThreshold too low                       |
| Assuming ImagePullBackOff means image doesn't exist              | All ImagePullBackOff treated as build failures                                                       | Check events for specific error: "unauthorized" (auth issue), "not found" (missing image), "timeout" (network issue), "rate limit" (registry throttling) |
| Increasing memory limits without checking actual usage           | Memory limit increased 2x, 4x but OOMKilled continues                                                | Use `kubectl top pod` to measure actual usage before increase; if usage growing over time, it's a leak (code fix needed, not higher limits)              |
| Not checking node capacity when pod is Pending                   | Assume scheduling failure is always node selector/taint issue                                        | Run `kubectl describe nodes                                                                                                                              | grep -A5 "Allocated resources"` to verify cluster has available capacity |
| Debugging node-level OOM as container OOM                        | Treating all OOMKilled as container limit issue                                                      | Check if exit code 137 with "System OOM" in node logs vs container limit (node-level OOM requires adding nodes or reducing pod density)                  |
| Using `latest` tag in production deployments                     | ImagePullBackOff doesn't clearly indicate which version failed, cannot rollback to specific version  | Use semantic versioning (v1.2.3) or git SHA tags; reserve `latest` for development only                                                                  |
| Not checking PVC binding status for Pending pods                 | Assuming Pending is only due to resource/selector issues                                             | Run `kubectl get pvc -n <namespace>` to verify all PVCs are Bound before investigating other causes                                                      |
| Applying fixes without validation                                | Assuming fix worked without verifying pod status/events                                              | Always validate with health checks (pod status, events, resource usage) after applying fixes                                                             |
| Skipping event timestamp analysis                                | Missing correlation between external events (deploy, node failure) and pod issues                    | Sort events by timestamp and correlate with deployment timing, node events, or traffic changes                                                           |

---

## Tools & Resources

### Recommended Tools

1. **kubectl**
   - **Purpose**: Primary interface for Kubernetes cluster interaction and diagnostics
   - **When to Use**: All troubleshooting scenarios (get, describe, logs, events, top)
   - **Documentation**: https://kubernetes.io/docs/reference/kubectl/

2. **kubectl top**
   - **Purpose**: Real-time resource usage metrics (requires metrics-server)
   - **When to Use**: OOMKilled diagnosis, resource optimization, capacity planning
   - **Documentation**: https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#top

3. **kubectl describe**
   - **Purpose**: Comprehensive pod/node information including events, status, and configuration
   - **When to Use**: Primary diagnostic tool for all failure modes (start here)
   - **Documentation**: https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#describe

4. **stern**
   - **Purpose**: Multi-pod log tailing with color coding (aggregates logs from multiple pods)
   - **When to Use**: Debugging applications with multiple replicas, following logs during rollouts
   - **Documentation**: https://github.com/stern/stern

5. **k9s**
   - **Purpose**: Terminal-based UI for Kubernetes cluster management and troubleshooting
   - **When to Use**: Visual exploration of cluster state, rapid navigation between resources
   - **Documentation**: https://k9scli.io/

6. **kubectx + kubens**
   - **Purpose**: Fast switching between clusters (contexts) and namespaces
   - **When to Use**: Managing multiple environments (dev/staging/production), reducing typing errors
   - **Documentation**: https://github.com/ahmetb/kubectx

### Learning Resources

1. **Kubernetes Official Troubleshooting Guide**: https://kubernetes.io/docs/tasks/debug/debug-application/
   - **Topic**: Application debugging, pod lifecycle, common failure modes
   - **Quality**: High (official documentation, comprehensive coverage)

2. **Kubernetes Failure Stories**: https://k8s.af/
   - **Topic**: Real-world Kubernetes failure case studies with post-mortems
   - **Quality**: High (community-curated, detailed incident reports)

3. **Kubernetes Events Deep Dive**: https://kubernetes.io/docs/reference/kubernetes-api/cluster-resources/event-v1/
   - **Topic**: Event structure, types, reasons, and lifecycle
   - **Quality**: High (official API reference)

4. **Container Exit Code Reference**: https://tldp.org/LDP/abs/html/exitcodes.html
   - **Topic**: Standard POSIX exit codes and signal mappings
   - **Quality**: High (POSIX standard documentation)

5. **Resource Management Guide**: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
   - **Topic**: Requests, limits, QoS classes, resource quotas
   - **Quality**: High (official documentation with best practices)

---

## Glossary

- **CrashLoopBackOff**: Pod restart state with exponential backoff (10s, 20s, 40s… max 5min) after repeated container failures
- **ImagePullBackOff**: Pod state where Kubernetes retries image pull with exponential backoff after initial failure (ErrImagePull)
- **OOMKilled**: Container termination by kernel due to exceeding memory limits (exit code 137 = 128 + SIGKILL)
- **Exit Code**: Integer returned by process on termination indicating success (0) or failure type (1-255)
- **Liveness Probe**: Health check determining if container is alive (failed probes trigger container restart)
- **Readiness Probe**: Health check determining if container can receive traffic (failed probes remove from service endpoints)
- **Events**: Time-ordered cluster state changes and failures recorded by Kubernetes control plane
- **kubectl describe**: Command providing comprehensive resource details including events, status, and configuration
- **kubectl top**: Command showing real-time CPU and memory usage for pods/nodes (requires metrics-server)
- **--previous flag**: kubectl logs option to retrieve logs from previously terminated container (essential for CrashLoopBackOff)
- **Node Selector**: Pod constraint requiring specific node labels for scheduling (e.g., gpu=true)
- **Taints and Tolerations**: Mechanism to repel pods from nodes unless pod has matching toleration
- **Resource Requests**: Minimum CPU/memory guaranteed to container (affects scheduling)
- **Resource Limits**: Maximum CPU/memory container can use (exceeding memory limit triggers OOMKilled)
- **PersistentVolumeClaim (PVC)**: Request for storage that must be bound to PersistentVolume before pod starts
- **imagePullSecrets**: Kubernetes secret containing registry credentials for private image repositories

---

## Sources & References

1. Kubernetes Official Documentation - Debug Running Pods: https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/
   - Accessed: 2025-10-24
   - Confidence: 1.0

2. Kubernetes Official Documentation - Debug Pods: https://kubernetes.io/docs/tasks/debug/debug-application/debug-pods/
   - Accessed: 2025-10-24
   - Confidence: 1.0

3. Kubernetes Official Documentation - Resource Management: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
   - Accessed: 2025-10-24
   - Confidence: 1.0

4. Kubernetes Event API Reference: https://kubernetes.io/docs/reference/kubernetes-api/cluster-resources/event-v1/
   - Accessed: 2025-10-24
   - Confidence: 1.0

5. Linux Exit Code Standards: https://tldp.org/LDP/abs/html/exitcodes.html
   - Accessed: 2025-10-24
   - Confidence: 0.95

6. Container Runtime Interface (CRI) Specification: https://github.com/kubernetes/cri-api
   - Accessed: 2025-10-24
   - Confidence: 0.9

---

## Changelog

- **2025-10-24**: Initial documentation created from troubleshooting framework research findings (confidence: 0.95)

---

## Related Documentation

- `.claude/agents/deployment-release.md`: Agent definition and capabilities
- `.claude/docs/schemas/deployment-release.schema.json`: Output schema specification
- `docs/04-guides/development/kubernetes-best-practices.md`: Deployment best practices (if exists)
- `.claude/docs/guides/debugger/`: Application debugging workflows
- `.claude/docs/guides/development/`: Manifest modification patterns
