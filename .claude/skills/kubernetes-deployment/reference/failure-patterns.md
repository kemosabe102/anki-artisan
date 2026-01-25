# Kubernetes Failure Patterns Reference

**Purpose**: Systematic troubleshooting patterns for common K8s failure modes

**Audience**: deployment-release agent (reference during troubleshooting operations)

---

## Event-Driven Diagnosis Framework

**Core Principle**: Events first → Logs second → Describe third (minimize kubectl overhead)

### CrashLoopBackOff Pattern

**Detection**: `kubectl get events --sort-by=.lastTimestamp | grep <pod-name>` shows "BackOff" reason

**Investigation Steps**:

1. **Get Events**:
   ```bash
   AGENT_NAME=deployment-release kubectl get events --sort-by=.lastTimestamp | grep <pod-name>
   ```

2. **Retrieve Logs** (use `--previous` for crashed container):
   ```bash
   AGENT_NAME=deployment-release kubectl logs <pod-name> --previous
   ```

3. **Identify Root Cause**:
   - **Exit code analysis**:
     * `0` = Success (normal termination)
     * `1` = General error (check logs)
     * `137` = OOMKilled (exceeded memory limits)
     * `143` = SIGTERM (graceful shutdown)


   - **Log error patterns**:
     * Python traceback → Application code error
     * "Connection refused" → Dependency unavailable
     * "Missing environment variable" → ConfigMap/Secret issue

4. **Remediation**:
   - Missing env vars → Update ConfigMap/Secret, restart deployment
   - OOMKilled (137) → Increase memory limits
   - Liveness probe timeout → Adjust probe timings
   - Application error → Delegate to debugger

### ImagePullBackOff Pattern

**Detection**: Events show "Failed to pull image" or "ErrImagePull"

**Investigation**:
1. Get events filtering for "Failed to pull image"
2. **Identify Issue**:
   - Image tag doesn't exist → Check `image-versions.yaml`
   - Registry authentication → Verify imagePullSecrets
   - Network connectivity → Check network policies

**Remediation**:
- Invalid tag → Update in `kustomization.yaml`
- Missing credentials → Recreate imagePullSecret
- Network policy → Adjust to allow registry access

### Pending State Pattern

**Detection**: Pod status shows "Pending" for >30 seconds

**Investigation**:
```bash
AGENT_NAME=deployment-release kubectl describe pod <pod-name>
```

**Conditions**:
- "Insufficient cpu/memory" → Scale down or add nodes
- "No nodes available" → Check affinity rules
- "PersistentVolumeClaim not bound" → Check StorageClass



### OOMKilled Pattern

**Detection**: Exit code 137 in container status

**Investigation**:
```bash
AGENT_NAME=deployment-release kubectl describe pod <pod-name>
# Look for "Last State: Terminated" with "Reason: OOMKilled"

AGENT_NAME=deployment-release kubectl top pod <pod-name>
# Compare memory usage to limits
```

**Remediation**:
- Increase memory limits in deployment manifest
- Add memory requests for proper scheduling
- Investigate memory leak (delegate to debugger if recurring)

---

## Exit Code Reference

| Exit Code | Meaning | Common Causes | Remediation |
|-----------|---------|---------------|-------------|
| 0 | Success | Normal termination | No action needed |
| 1 | General error | Application error, dependency unavailable | Check logs, delegate to debugger |
| 137 | OOMKilled | Exceeded memory limits | Increase memory limits |
| 143 | SIGTERM | Graceful shutdown | Normal during rollouts |
| 255 | Docker error | Image pull failed, entrypoint error | Check image, verify entrypoint |

---

**See Also**:
- `kubectl-operations.md` - kubectl command reference
- `troubleshooting-workflows.md` - Error handling and retry strategies
