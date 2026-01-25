# k8s-deployment Documentation

**Purpose**: Externalized domain knowledge for Kubernetes deployment orchestration

---

## Contents

| File | Purpose | When to Use |
|------|---------|-------------|
| `domain-expertise.md` | Primary responsibilities, workflow operations, integration points | Deep reference for implementation details |
| `frameworks.md` | OODA adaptations, validation protocols, error handling | Understanding methodology |
| `failure-patterns.md` | Event-driven diagnosis patterns | Troubleshooting CrashLoopBackOff, ImagePullBackOff, Pending, OOMKilled |
| `kubectl-operations.md` | Approved kubectl commands, script reference | Before executing any kubectl operation |
| `kustomize-integration.md` | Base/overlay/patch/transformer patterns | Manifest management |
| `troubleshooting-workflows.md` | Error classification, retry strategies, circuit breaker | Error recovery |
| `manifest-editing-protocol.md` | Platform-aware manifest editing workflow | ConfigMap/Secret updates |
| `observability-stack-validation.md` | Telemetrygen testing, stack validation | After deploying observability infrastructure |

---

## Quick Reference

**Most common lookups**:
1. **Deployment failing?** → `failure-patterns.md`
2. **Which kubectl command?** → `kubectl-operations.md`
3. **How to edit manifests?** → `manifest-editing-protocol.md`
4. **Kustomize structure?** → `kustomize-integration.md`

---

## See Also

- **Main agent**: `../k8s-deployment.md`
- **Examples**: `../examples/`
- **Schema**: `../schemas/k8s-deployment.schema.json`
