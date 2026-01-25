# Prometheus Alert Builder - Examples

Delegation examples and usage patterns.

## Contents

| Document | Purpose |
|----------|---------|
| [delegation-examples.md](./delegation-examples.md) | How orchestrator invokes this agent |

## Quick Example

```json
{
  "task_id": "alert-001",
  "operation_type": "construct_alert",
  "intent_description": "Alert when API error rate exceeds 5% for 10 minutes",
  "alert_context": {
    "service": "payment-api",
    "team": "payments",
    "severity_preference": "warning_critical"
  }
}
```
