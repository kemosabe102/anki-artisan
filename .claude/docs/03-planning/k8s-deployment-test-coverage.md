# deployment-release Test Coverage Plan

## ⚠️ CRITICAL SECURITY GAP - HIGH RISK AGENT WITHOUT TEST COVERAGE

**Status**: deployment-release is a **HIGH risk agent** (Bash execution, kubectl operations, cluster access) currently **WITHOUT automated test coverage**.

**Required Tests** (future work - not part of this agent definition update):

### 1. Schema Validation Tests

- Verify all outputs conform to `deployment-release.schema.json`
- Test SUCCESS state structure (deployment evidence, rollout status, service endpoints)
- Test FAILURE state structure (recovery guidance, error classification, remediation steps)

### 2. K8s Operation Tests

- Mock kubectl command execution and validate AGENT_NAME prefix usage
- Test script orchestration order (setup-k8s-secrets.sh → deploy-local-k8s.sh)
- Verify dry-run validation before apply operations
- Test error classification (PERMANENT/TRANSIENT/AMBIGUOUS)
- Validate circuit breaker behavior (3 consecutive failures → stop)

### 3. Security Tests

- Verify blocked commands rejected (`kubectl apply`, `kubectl delete`)
- Test audit logging (AGENT_NAME traceability)
- Validate no secrets leaked in outputs
- Test cluster-level resource restrictions

## Security Risk Until Tests Implemented

Without test coverage, regressions in security controls (AGENT_NAME prefix, command blocking, secret handling) may go undetected.

## Recommendation

Prioritize test creation for HIGH risk agents before adding new K8s deployment features.
