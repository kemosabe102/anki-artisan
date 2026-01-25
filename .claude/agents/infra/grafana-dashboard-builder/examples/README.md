# Grafana Dashboard Builder Examples

Examples demonstrating agent delegation patterns and usage scenarios.

## Contents

| Example | Purpose |
|---------|---------|
| `delegation-examples.md` | k8s-deployment and researcher-external delegation patterns with templates |
| `k8s-deployment-delegation.md` | Detailed k8s-deployment agent delegation examples |
| `researcher-web-delegation.md` | Detailed researcher-external agent delegation examples |

## Quick Reference

**k8s-deployment Delegation**: Use for deploying ConfigMaps to Kubernetes after dashboard generation.

**researcher-external Delegation**: Use for researching SRE best practices for unfamiliar domains (Redis, Kafka, custom services).

## Example Usage Flow

```
1. User: "Create dashboard for Redis monitoring"
2. grafana-dashboard-builder: Analyzes intent -> USE method (resource monitoring)
3. grafana-dashboard-builder: Delegates to researcher-external for Redis-specific metrics
4. grafana-dashboard-builder: Creates dashboard JSON + ConfigMap
5. grafana-dashboard-builder: Delegates to k8s-deployment for deployment
6. Output: Dashboard accessible in Grafana UI
```
