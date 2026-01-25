# PromQL Query Builder - Examples

Usage examples demonstrating how the orchestrator delegates to this agent.

## Contents

| Example | Scenario |
|---------|----------|
| [delegation-examples.md](./delegation-examples.md) | Orchestrator delegation patterns for all operation types |

## Quick Example

```markdown
Task(promql-query-builder, "Build a PromQL query to detect p95 API latency by service")
```

Expected output: Validated query with metadata ready for grafana-dashboard-builder consumption.
